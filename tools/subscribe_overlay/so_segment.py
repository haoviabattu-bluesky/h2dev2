# -*- coding: utf-8 -*-
"""Mode "segment": chỉ encode lại các GOP chứa nút, phần còn lại stream-copy (đo ep06 21:54: 71,6s thay vì 278s).

Các bước:
  1. quét keyframe;
  2. cắt video (không audio) thành .ts tại keyframe;
  3. KIỂM độ dài từng đoạn;
  4. encode lại đoạn có nút, giữ pix_fmt/range nguồn;
  5. concat copy + trộn âm trên toàn track.
Cắt lệch / nguồn lạ → ném SegmentError để apply_to_video rơi về mode "full".
"""
from __future__ import annotations

import os
import re
import shutil
import tempfile
from fractions import Fraction
from pathlib import Path

import so_compose
import so_ffmpeg as ff

CUT_BACKOFF = 0.015  # bẫy: "177.800000" > pts thật 177.7999 → muxer cắt sang GOP SAU (nút lệch 8s mà số khung vẫn đúng)
MAX_PART_ERR = 0.05
_PROFILES = {"high": "high", "main": "main", "constrained baseline": "baseline", "baseline": "baseline"}


class SegmentError(RuntimeError):
    pass


def keyframes(src) -> list[float]:
    p = ff.run(["-skip_frame", "nokey", "-i", str(src), "-an", "-vf", "showinfo", "-f", "null", "-"], check=False)
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", p.stderr.decode("utf-8", "replace"))]


def plan_windows(kf: list[float], starts: list[float], d: float) -> list[tuple[float, float | None, list[float]]]:
    """Mỗi mốc → cửa sổ [keyframe ≤ start, keyframe ≥ start+d). Cửa sổ chồng/chạm nhau → gộp. b=None = tới hết."""
    wins: list = []
    for s in starts:
        a = max((k for k in kf if k <= s + 1e-6), default=0.0)
        b = min((k for k in kf if k >= s + d - 1e-6), default=None)
        if wins and (wins[-1][1] is None or a < wins[-1][1] - 1e-6):
            pa, pb, ps = wins[-1]
            wins[-1] = (pa, None if (pb is None or b is None) else max(pb, b), ps + [s])
        else:
            wins.append((a, b, [s]))
    return wins


def _check_source(info: dict) -> None:
    if info["vcodec"] != "h264" or info["pix_fmt"] not in ("yuv420p", "yuvj420p"):
        raise SegmentError(f"nguồn {info['vcodec']}/{info['pix_fmt']} — segment chỉ hỗ trợ h264 yuv(j)420p")


def video_end(src, info: dict) -> float:
    """Độ dài THẬT của track hình = số khung / fps. Container `Duration` lấy theo track DÀI HƠN — tiếng dài
    hơn hình vài chục ms (ep06 lane L: 0,057s) làm đoạn cuối "thiếu" giả và rơi oan về full (2026-09-30)."""
    err = ff.run(["-i", str(src), "-map", "0:v:0", "-c", "copy", "-f", "null", "-"], check=False).stderr.decode("utf-8", "replace")
    m = re.findall(r"frame=\s*(\d+)", err)
    if not m:
        return info["duration"]
    return min(info["duration"], int(m[-1]) / float(Fraction(str(info["fps"]))))


def compose_segment(input_path, output_path, overlay_path, meta: dict, cfg: dict, info: dict) -> dict:
    _check_source(info)
    src, out = Path(input_path), Path(output_path)
    x, y = so_compose.placement(cfg, meta, info["w"], info["h"])
    starts, warns = so_compose.resolve_starts(cfg, info["duration"])
    d, total = float(cfg["duration"]), info["duration"]
    kf = keyframes(src)
    if not kf:
        raise SegmentError("không đọc được keyframe")
    wins = plan_windows(kf, starts, d)
    cuts = sorted({c for a, b, _ in wins for c in (a, b) if c is not None and 0 < c < total - 0.01})
    work = Path(tempfile.mkdtemp(prefix="subseg_", dir=str(out.parent)))
    try:
        ff.run(["-y", "-i", str(src), "-map", "0:v:0", "-c", "copy", "-f", "segment",
                "-segment_times", ",".join(f"{c - CUT_BACKOFF:.6f}" for c in cuts) or "999999",
                "-reset_timestamps", "1", str(work / "p%03d.ts")])
        parts = sorted(work.glob("p*.ts"))
        bounds = [0.0] + cuts
        want = [b - a for a, b in zip(bounds, bounds[1:] + [video_end(src, info)])]
        got = [ff.probe(q)["duration"] for q in parts]
        bad = [(i, round(g, 3), round(w, 3)) for i, (g, w) in enumerate(zip(got, want)) if abs(g - w) > MAX_PART_ERR]
        if len(got) != len(want) or bad:
            raise SegmentError(f"cắt keyframe lệch: {len(got)} đoạn/cần {len(want)}; lệch (đoạn, có, cần) {bad[:3]}")
        pix = info["pix_fmt"]
        rng = "pc" if (info["color_range"] == "pc" or pix == "yuvj420p") else "tv"
        prof = _PROFILES.get(info["vprofile"], "high")
        ov_in = so_compose.overlay_input_args(meta, overlay_path)
        for a, _b, ss in wins:
            i = min(range(len(bounds)), key=lambda j: abs(bounds[j] - a))
            local = [round(s - a, 3) for s in ss]
            vf = so_compose.overlay_chain("[0:v]", 1, local, x, y, d, "[vo]") + f";[vo]format={pix}[v]"
            enc = work / f"r{i:03d}.ts"
            ff.run(["-y", "-i", str(parts[i]), *ov_in, "-filter_complex", vf, "-map", "[v]",
                    "-c:v", "libx264", "-preset", str(cfg.get("video_preset", "medium")),
                    "-crf", str(int(cfg.get("video_crf", 18))), "-pix_fmt", pix, "-color_range", rng,
                    "-profile:v", prof, "-fps_mode", "passthrough",
                    "-bsf:v", "h264_mp4toannexb", "-muxdelay", "0", "-f", "mpegts", str(enc)])
            if abs(ff.probe(enc)["duration"] - want[i]) > MAX_PART_ERR:
                raise SegmentError(f"đoạn encode lại {i} lệch độ dài")
            parts[i] = enc
        lst = work / "list.txt"
        lst.write_text("".join(f"file '{q.as_posix()}'\n" for q in parts), encoding="utf-8")
        args = ["-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(src)]
        sound_used = bool(cfg.get("enable_sound") and info["has_audio"])
        if sound_used:
            extra, afc = so_compose.sound_mix(cfg, meta, info, starts, "[1:a]", 2)
            args += extra + ["-filter_complex", afc, "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
        else:
            if cfg.get("enable_sound"):
                warns.append("video không có audio → bỏ qua âm thanh nút")
            args += ["-map", "0:v", "-map", "1:a?", "-c:a", "copy"]
        tmp = out.with_name(out.stem + ".partial" + out.suffix)
        ff.run(args + ["-c:v", "copy", "-map_metadata", "1", "-movflags", "+faststart", str(tmp)])
        dd = ff.probe(tmp)["duration"] - total
        if abs(dd) > 0.1:
            tmp.unlink(missing_ok=True)
            raise SegmentError(f"video ghép lệch thời lượng {dd:+.3f}s")
        os.replace(tmp, out)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return {"x": x, "y": y, "starts": starts, "start": starts[0], "end": round(starts[-1] + d, 3),
            "encoder": "libx264", "sound": sound_used, "warnings": warns, "mode": "segment",
            "windows": [(round(a, 3), None if b is None else round(b, 3)) for a, b, _ in wins],
            "reencoded_seconds": round(sum((total if b is None else b) - a for a, b, _ in wins), 2)}
