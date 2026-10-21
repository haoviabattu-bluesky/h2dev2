# -*- coding: utf-8 -*-
"""NGUYÊN MẪU: chỉ encode lại các đoạn GOP chứa nút đăng ký, phần còn lại stream-copy.

py -3.12 proto_segment.py <input.mp4> <output.mp4>
"""
import json, re, subprocess, sys, time
from pathlib import Path

TOOL = Path(r"E:\CLAUDE\YOUTUBE\SUB_BUTTON\tools\subscribe_overlay")
sys.path.insert(0, str(TOOL))
import so_config, so_compose, so_ffmpeg as ff, so_sounds  # noqa: E402
import subscribe_overlay as so  # noqa: E402

FF = ff.ffmpeg_exe()


def run(args):
    p = subprocess.run([FF, "-hide_banner", "-nostdin", "-loglevel", "error", *map(str, args)], capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.decode("utf-8", "replace")[-1500:])
    return p


def keyframes(src):
    p = subprocess.run([FF, "-hide_banner", "-skip_frame", "nokey", "-i", str(src), "-an", "-vf", "showinfo",
                        "-f", "null", "-"], capture_output=True)
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", p.stderr.decode("utf-8", "replace"))]


def main(src, dst):
    T0 = time.time()
    src, dst = Path(src), Path(dst)
    work = dst.parent / (dst.stem + "_work"); work.mkdir(exist_ok=True)
    cfg = so_config.load_config(overrides={"enable_sound": True})
    info = ff.probe(src)
    ov, meta = so.get_overlay(cfg, info["w"], info["h"], info["fps"])
    starts, _ = so_compose.resolve_starts(cfg, info["duration"])
    d = float(cfg["duration"])
    kf = keyframes(src); t_kf = time.time() - T0
    cuts, wins = [], []
    for s in starts:
        a = max(k for k in kf if k <= s)
        b = min((k for k in kf if k >= s + d), default=None)
        wins.append((a, b, s)); cuts += [a] + ([b] if b else [])
    cuts = sorted(set(c for c in cuts if c > 0))
    # 1) cắt video (không audio) thành đoạn theo đúng keyframe — stream copy
    run(["-y", "-i", src, "-map", "0:v", "-c", "copy", "-f", "segment", "-segment_times",
         ",".join(f"{c - 0.015:.6f}" for c in cuts), "-reset_timestamps", "1", work / "p%03d.ts"])
    parts = sorted(work.glob("p*.ts"))
    bounds = [0.0] + cuts
    got = [ff.probe(q)["duration"] for q in parts]
    want = [b2 - a2 for a2, b2 in zip(bounds, bounds[1:] + [info["duration"]])]
    bad = [(round(g, 3), round(w, 3)) for g, w in zip(got, want) if abs(g - w) > 0.05]
    if len(got) != len(want) or bad:
        raise SystemExit(f"CẮT SAI keyframe: {len(got)} đoạn / cần {len(want)}; lệch {bad}")
    x, y = so_compose.placement(cfg, meta, info["w"], info["h"])
    t1 = time.time()
    for a, b, s in wins:
        i = bounds.index(a) if a > 0 else 0
        seg = parts[i]; off = s - a
        out = work / f"r{i:03d}.ts"
        vf = (f"[1:v]format=yuva420p,setpts=PTS-STARTPTS+{off}/TB[ov];"
              f"[0:v][ov]overlay=x={x}:y={y}:eof_action=pass:enable='between(t,{off},{off + d:.3f})',format=yuvj420p[v]")
        run(["-y", "-i", seg, "-c:v", "libvpx-vp9", "-i", ov, "-filter_complex", vf, "-map", "[v]",
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuvj420p", "-color_range", "pc",
             "-profile:v", "high", "-bsf:v", "h264_mp4toannexb", "-muxdelay", "0", "-f", "mpegts", out])
        parts[i] = out
    t_enc = time.time() - t1
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    # 2) audio: trộn âm nút trên TOÀN track (AAC encode lại — nhanh), video ghép lại bằng concat copy
    snd = so_sounds.ensure_sounds(Path(meta["cache_dir"]), None)
    af = f"aformat=sample_rates={info['audio_rate']}:channel_layouts={info['audio_layout']}"
    args, parts_a, labels, idx = ["-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", src], [], [], 2
    for s in starts:
        for name, o in so_sounds.events(cfg):
            args += ["-i", snd[name]]
            vol = float(cfg["sound_volume"]) * float(cfg["sound_gains"].get(name.split(":")[0], 1)) * so_sounds.gain_of(name)
            parts_a.append(f"[{idx}:a]{af},afade=t=in:d=0.004,adelay={int(round((s + o) * 1000))}:all=1,volume={vol:.3f}[s{idx}]")
            labels.append(f"[s{idx}]"); idx += 1
    fc = ";".join(parts_a) + f";[1:a]{af}[a0];[a0]{''.join(labels)}amix=inputs={len(labels) + 1}:duration=first:normalize=0," \
         f"alimiter=limit=0.97:attack=1:release=60:level=0:latency=1,{af}[a]"
    t2 = time.time()
    run(args + ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-map_metadata", "1", "-movflags", "+faststart", dst])
    t_mux = time.time() - t2
    oi = ff.probe(dst)
    print(json.dumps({"starts": starts, "windows": [(round(a, 3), round(b, 3)) for a, b, _ in wins],
                      "reencoded_seconds": round(sum(b - a for a, b, _ in wins), 2),
                      "t_keyframe_scan": round(t_kf, 1), "t_encode_windows": round(t_enc, 1),
                      "t_audio_mux": round(t_mux, 1), "t_total": round(time.time() - T0, 1),
                      "in_dur": info["duration"], "out_dur": oi["duration"],
                      "in_size_mb": round(src.stat().st_size / 1e6, 1), "out_size_mb": round(dst.stat().st_size / 1e6, 1)},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:3])
