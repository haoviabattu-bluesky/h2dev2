# -*- coding: utf-8 -*-
"""Ghép overlay (đã cache) vào video bằng FFmpeg — bước duy nhất chạy lại cho mỗi tập.

Giữ nguyên: fps (fps_mode passthrough), độ phân giải, thời lượng, audio (copy nếu không bật âm).
Chỉ video bị encode lại (bắt buộc khi vẽ đè), libx264 crf 18 mặc định.
Chèn được NHIỀU lần trong 1 video (start_times, vd [180, -120] = phút 3 + 2 phút trước khi hết) bằng 1 lần encode.
"""
from __future__ import annotations

import os
from pathlib import Path

import so_ffmpeg as ff
import so_sounds


def placement(cfg: dict, meta: dict, vw: int, vh: int) -> tuple[int, int]:
    """Toạ độ góc trái-trên của CANVAS overlay trên video, sao cho THẺ nút nằm đúng vị trí cấu hình."""
    cx, cy, cw, ch = meta["card_box"]
    # Shorts: đáy màn hình bị YouTube phủ tiêu đề/nút (~20%) → lề riêng cho video dọc
    key = "bottom_margin_ratio_vertical" if vh > vw else "bottom_margin_ratio"
    mb = float(cfg.get(key, cfg["bottom_margin_ratio"])) * vh
    if cfg.get("has_subtitles"):
        mb = max(mb, float(cfg["subtitle_safe_ratio"]) * vh)  # phụ đề nằm đáy → đẩy nút lên
    side = float(cfg["side_margin_ratio"]) * vw
    pos = cfg["position"]
    card_x = {"bottom_left": side, "bottom_right": vw - side - cw}.get(pos, (vw - cw) / 2)
    card_y = (vh - ch) / 2 if pos == "center" else vh - mb - ch
    return int(round(card_x - cx)), int(round(card_y - cy))


def resolve_starts(cfg: dict, video_dur: float) -> tuple[list[float], list[str]]:
    """start_times (list) hoặc start_time → các mốc hợp lệ, tăng dần, không chồng nhau.

    Số âm = tính từ cuối video. Mốc không vừa video → bỏ. Hai lần hiện cách nhau < min_gap → bỏ lần sau
    (video ngắn: phút 3 và "2 phút trước khi hết" có thể trùng nhau).
    """
    warn, d = [], float(cfg["duration"])
    raw = cfg.get("start_times") or [cfg["start_time"]]
    gap = float(cfg.get("min_gap", 30.0))
    if d > video_dur:
        return [0.0], ["video ngắn hơn animation → animation bị cắt đuôi"]
    out = []
    for s0 in raw:
        s = float(s0) + (video_dur if float(s0) < 0 else 0.0)
        if s + d > video_dur or s < 0:
            warn.append(f"mốc {s0}s không vừa video {video_dur:.2f}s → bỏ")
            continue
        out.append(round(s, 3))
    if not out:  # video quá ngắn cho mọi mốc → 1 lần theo start_time (dời vào trong nếu cần)
        s0 = float(cfg["start_time"])
        s = min(max(0.0, s0 + (video_dur if s0 < 0 else 0.0)), video_dur - d)
        warn.append(f"không mốc nào vừa → dùng start_time, hiện 1 lần lúc {s:.2f}s")
        out = [round(s, 3)]
    out.sort()
    keep = []
    for s in out:
        if keep and s < keep[-1] + d + gap:
            warn.append(f"mốc {s:.2f}s quá gần lần trước ({keep[-1]:.2f}s, cần cách ≥ {d + gap:.0f}s) → bỏ")
            continue
        keep.append(s)
    return keep, warn


def overlay_input_args(meta: dict, overlay_path) -> list:
    """Tham số -i cho file overlay (đặt ngay sau input video)."""
    fmt = meta["format"]
    if fmt == "webm":
        return ["-c:v", "libvpx-vp9", "-i", str(overlay_path)]  # PHẢI ép decoder libvpx, decoder vp9 gốc bỏ mất alpha
    if fmt == "png":
        return ["-framerate", meta["fps"], "-i", str(Path(overlay_path) / "%05d.png")]
    return ["-i", str(overlay_path)]


def overlay_chain(src_label: str, ov_input: int, starts: list, x: int, y: int, d: float, out_label: str = "[v]") -> str:
    """filter_complex vẽ overlay lên src_label ở từng mốc starts (giây theo dòng thời gian của src)."""
    n = len(starts)
    split = "".join(f"[o{k}]" for k in range(n))
    vf = f"[{ov_input}:v]format=yuva420p,split={n}{split}" if n > 1 else f"[{ov_input}:v]format=yuva420p[o0]"
    prev = src_label
    for k, st in enumerate(starts):
        lab = out_label if k == n - 1 else f"[v{k}]"
        vf += (f";[o{k}]setpts=PTS-STARTPTS+{st}/TB[ov{k}];"
               f"{prev}[ov{k}]overlay=x={x}:y={y}:eof_action=pass:enable='between(t,{st},{st + d:.3f})'{lab}")
        prev = lab
    return vf


def sound_mix(cfg: dict, meta: dict, info: dict, starts: list, audio_src: str, first_idx: int) -> tuple[list, str]:
    """Trộn click/chuông vào audio gốc. Trả (tham số -i thêm, filter kết thúc bằng nhãn [a])."""
    snd = so_sounds.ensure_sounds(Path(meta["cache_dir"]), cfg.get("sound_files"))
    # ép âm click/chuông về ĐÚNG layout + sample rate audio gốc — không thì amix có thể hạ stereo → mono
    af = f"aformat=sample_rates={info['audio_rate']}:channel_layouts={info['audio_layout']}"
    args, parts, labels, idx = [], [], [], first_idx
    for st in starts:
        for name, off in so_sounds.events(cfg):
            args += ["-i", str(snd[name])]
            ms = int(round((st + off) * 1000))
            base = name.split(":", 1)[0]
            vol = float(cfg["sound_volume"]) * float(cfg.get("sound_gains", {}).get(base, 1.0)) * so_sounds.gain_of(name)
            # 4ms vào mềm: chặn "bụp" đầu file
            parts.append(f"[{idx}:a]{af},afade=t=in:d=0.004,adelay={ms}:all=1,volume={vol:.3f}[s{idx}]")
            labels.append(f"[s{idx}]")
            idx += 1
    # alimiter 0.891 (-1 dBFS) = mức assemble.py h2dev; QC B8Q (qc_visual VO_GHEP_DB) báo vỡ khi đỉnh ≥ -0.5 dBFS
    fc = (";".join(parts) + f";{audio_src}{af}[a0];[a0]{''.join(labels)}"
          f"amix=inputs={len(labels) + 1}:duration=first:normalize=0,"
          f"alimiter=limit=0.891:attack=1:release=60:level=0:latency=1,{af}[a]")
    return args, fc


def compose(input_path, output_path, overlay_path, meta: dict, cfg: dict, info: dict) -> dict:
    vw, vh = info["w"], info["h"]
    x, y = placement(cfg, meta, vw, vh)
    starts, warns = resolve_starts(cfg, info["duration"])
    d = float(cfg["duration"])
    args = ["-y", "-i", str(input_path), *overlay_input_args(meta, overlay_path)]
    vf = overlay_chain("[0:v]", 1, starts, x, y, d)
    maps = ["-map", "[v]"]
    sound_used = False
    if cfg.get("enable_sound") and info["has_audio"]:
        extra, afc = sound_mix(cfg, meta, info, starts, "[0:a]", 2)
        args += extra
        vf += ";" + afc
        maps += ["-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
        sound_used = True
    else:
        if cfg.get("enable_sound"):
            warns.append("video không có audio → bỏ qua âm thanh nút")
        maps += ["-map", "0:a?", "-c:a", "copy"]
    enc_name, enc_args = ff.video_encoder_args(cfg)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.stem + ".partial" + out.suffix)
    args += ["-filter_complex", vf, *maps, *enc_args, "-fps_mode", "passthrough",
             "-map_metadata", "0", "-movflags", "+faststart", str(tmp)]
    ff.run(args)
    os.replace(tmp, out)
    return {"x": x, "y": y, "starts": starts, "start": starts[0], "end": round(starts[-1] + d, 3),
            "encoder": enc_name, "sound": sound_used, "warnings": warns, "mode": "full"}
