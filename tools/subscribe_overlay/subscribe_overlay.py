# -*- coding: utf-8 -*-
"""Nút đăng ký kênh (チャンネル登録 → 登録済み + chuông) chèn vào video — CLI + API cho pipeline h2dev.

  py -3.12 subscribe_overlay.py --input video.mp4 --output video_final.mp4 --start 15 --language ja
  py -3.12 subscribe_overlay.py --generate-overlay --output subscribe_overlay.webm [--size 1080p]
  py -3.12 subscribe_overlay.py --masters            # render sẵn bộ master vào cache

Overlay render 1 lần cho mỗi cấu hình (khoá SHA256) rồi nằm trong cache; mỗi tập chỉ còn bước FFmpeg.
Gọi từ code:  import subscribe_overlay as so;  so.apply_to_video(inp, out, overrides={...})
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import so_compose  # noqa: E402
import so_config  # noqa: E402
import so_ffmpeg as ff  # noqa: E402
import so_fonts  # noqa: E402
import so_layout  # noqa: E402
import so_renderer  # noqa: E402
import so_segment  # noqa: E402
import so_sounds  # noqa: E402

SIZES = {"720p": (1280, 720), "1080p": (1920, 1080), "1440p": (2560, 1440), "4k": (3840, 2160),
         "vertical": (1080, 1920), "vertical_720p": (720, 1280)}
MASTERS = [("1080p", "ja"), ("1080p", "en"), ("720p", "ja"), ("vertical", "ja")]


def _log(msg: str) -> None:
    print(f"[subscribe] {msg}", flush=True)


def get_overlay(cfg: dict, vw: int, vh: int, fps: str, force: bool = False) -> tuple[Path, dict]:
    """Trả (file overlay, meta). Có sẵn trong cache → dùng lại, KHÔNG render."""
    texts = [t for t in (cfg["subscribe_text"], cfg["subscribed_text"], cfg.get("thanks_text")) if t]
    font_path, font_idx = so_fonts.find_font(texts, cfg.get("font_path"))
    width_px = so_config.overlay_width_px(cfg, vw, vh)
    fps = ff.fps_fraction(fps)
    key = so_config.cache_key(cfg, width_px, vh > vw, fps, font_path)
    cdir = so_config.cache_dir(cfg)
    ext = {"webm": ".webm", "mov": ".mov", "png": ""}[cfg["overlay_format"]]
    name = f"subscribe_{so_config.size_label(vw, vh)}_{cfg['language']}_{key[:12]}"
    out, meta_p = cdir / (name + ext), cdir / (name + ".json")
    if out.exists() and meta_p.exists() and not force:
        meta = json.loads(meta_p.read_text(encoding="utf-8"))
        meta.update(cached=True, cache_dir=str(cdir))
        return out, meta
    t0 = time.time()
    L = so_layout.build_layout(font_path, texts, width_px, int(cfg["supersample"]), cfg["enable_bell"], font_idx,
                               avatar=bool(cfg.get("avatar_file")))
    A = so_renderer.Assets(L, cfg, font_path, font_idx)
    _log(f"render overlay {L.canvas_w}x{L.canvas_h} @ {fps} fps, font {Path(font_path).name} → {out.name}")
    stat = so_renderer.encode_overlay(L, cfg, A, fps, out)
    if stat["border_alpha_max"] > 0:
        raise RuntimeError(f"Overlay chạm mép canvas (alpha viền = {stat['border_alpha_max']}) → hình bị cắt. Sửa lề trong so_layout.")
    meta = {"file": out.name, "format": cfg["overlay_format"], "canvas": [L.canvas_w, L.canvas_h],
            "card_box": L.card_box_px(), "fps": fps, "duration": cfg["duration"], "frames": stat["frames"],
            "font": font_path, "texts": texts, "key": key, "render_seconds": round(time.time() - t0, 1),
            "border_alpha_max": stat["border_alpha_max"]}
    meta_p.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    meta.update(cached=False, cache_dir=str(cdir))
    return out, meta


def apply_to_video(input_path, output_path, config_path=None, overrides: dict | None = None,
                   force: bool = False, mode: str | None = None) -> dict:
    """API cho pipeline: chèn nút vào video. enabled=false → copy nguyên file, không encode.

    mode "segment" (mặc định, config compose_mode) = chỉ encode lại đoạn có nút; lỗi cắt → tự rơi về "full".
    """
    cfg = so_config.load_config(config_path, overrides)
    inp, outp = Path(input_path), Path(output_path)
    if inp.resolve() == outp.resolve():
        raise ValueError("--output phải khác --input (không ghi đè video gốc)")
    if not cfg["enabled"]:
        shutil.copyfile(inp, outp)
        return {"skipped": True}
    info = ff.probe(inp)
    fps = cfg.get("fps") or info["fps"]
    t0 = time.time()
    ov, meta = get_overlay(cfg, info["w"], info["h"], fps, force)
    t1 = time.time()
    mode = mode or cfg.get("compose_mode", "segment")
    fallback = None
    if mode == "segment":
        try:
            res = so_segment.compose_segment(inp, outp, ov, meta, cfg, info)
        except so_segment.SegmentError as e:
            fallback = f"segment hỏng ({e}) → encode lại cả video"
            _log(f"CẢNH BÁO: {fallback}")
            res = so_compose.compose(inp, outp, ov, meta, cfg, info)
            res["warnings"].append(fallback)
    else:
        res = so_compose.compose(inp, outp, ov, meta, cfg, info)
    t2 = time.time()
    out_info = ff.probe(outp)
    res.update(input=info, output=out_info, overlay=str(ov), overlay_cached=meta["cached"],
               overlay_seconds=round(t1 - t0, 1), compose_seconds=round(t2 - t1, 1),
               duration_delta=round(out_info["duration"] - info["duration"], 3))
    return res


def _parse(argv=None):
    ap = argparse.ArgumentParser(description="Chèn nút đăng ký kênh YouTube (overlay RGBA) vào video")
    ap.add_argument("--input", help="video gốc")
    ap.add_argument("--output", help="video kết quả (hoặc file overlay khi --generate-overlay)")
    ap.add_argument("--config", help="đường dẫn subscribe_config.json (mặc định: cạnh script)")
    ap.add_argument("--generate-overlay", action="store_true", help="chỉ xuất overlay trong suốt")
    ap.add_argument("--masters", action="store_true", help="render sẵn bộ master vào cache")
    ap.add_argument("--size", default="1080p", help=f"cho --generate-overlay: {', '.join(SIZES)} hoặc WxH")
    ap.add_argument("--start", type=float, nargs="+", help="giây xuất hiện, được nhiều mốc (âm = tính từ cuối): --start 180 -120")
    ap.add_argument("--click-style", dest="sub_click_style", choices=sorted(so_sounds.CANDIDATES),
                    help="kiểu tiếng click nút đăng ký")
    ap.add_argument("--duration", type=float)
    ap.add_argument("--language", choices=sorted(so_config.LANG_TEXTS))
    ap.add_argument("--position", choices=so_config.POSITIONS)
    ap.add_argument("--format", dest="overlay_format", choices=["webm", "mov", "png"])
    ap.add_argument("--fps", help="fps overlay khi --generate-overlay (mặc định 30)")
    ap.add_argument("--has-subs", action="store_true", help="video có phụ đề đáy → đẩy nút lên")
    ap.add_argument("--sound", dest="enable_sound", action="store_true", default=None)
    ap.add_argument("--no-sound", dest="enable_sound", action="store_false")
    ap.add_argument("--encoder", dest="video_encoder", choices=["auto", "libx264", "h264_nvenc"])
    ap.add_argument("--mode", choices=["segment", "full"], help="segment = chỉ encode lại đoạn có nút (mặc định)")
    ap.add_argument("--force", action="store_true", help="bỏ qua cache, render lại overlay")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    a = _parse(argv)
    ov = {k: v for k, v in {"start_times": a.start, "duration": a.duration, "language": a.language,
                            "sub_click_style": a.sub_click_style,
                            "position": a.position, "overlay_format": a.overlay_format,
                            "enable_sound": a.enable_sound, "video_encoder": a.video_encoder}.items() if v is not None}
    if a.has_subs:
        ov["has_subtitles"] = True
    if a.masters:
        for size, lang in MASTERS:
            cfg = so_config.load_config(a.config, {**ov, "language": lang})
            p, m = get_overlay(cfg, *SIZES[size], a.fps or cfg.get("fps") or 30, a.force)
            _log(f"{'cache' if m['cached'] else 'MỚI'}  {p}")
        return 0
    if a.generate_overlay:
        if not a.output:
            raise SystemExit("Thiếu --output")
        cfg = so_config.load_config(a.config, ov)
        wh = SIZES.get(a.size) or tuple(int(v) for v in a.size.lower().split("x"))
        p, m = get_overlay(cfg, *wh, a.fps or cfg.get("fps") or 30, a.force)
        dst = Path(a.output)
        if p.is_dir():
            shutil.copytree(p, dst, dirs_exist_ok=True)
        else:
            shutil.copyfile(p, dst)
        _log(f"overlay {'(từ cache)' if m['cached'] else '(render mới ' + str(m['render_seconds']) + 's)'} → {dst}")
        _log(f"canvas {m['canvas']}, thẻ nút {m['card_box']} (x,y,w,h trong canvas)")
        return 0
    if not (a.input and a.output):
        raise SystemExit("Cần --input và --output (hoặc --generate-overlay / --masters). Xem --help")
    r = apply_to_video(a.input, a.output, a.config, ov, a.force, a.mode)
    if r.get("skipped"):
        _log("enabled=false → đã copy nguyên video, không chèn nút")
        return 0
    for w in r["warnings"]:
        _log(f"CẢNH BÁO: {w}")
    i, o = r["input"], r["output"]
    _log(f"xong → {a.output}")
    d = float(so_config.load_config(a.config, ov)["duration"])
    _log("nút hiện " + ", ".join(f"{s:.1f}s→{s + d:.1f}s" for s in r["starts"]) + f" tại x={r['x']} y={r['y']} | {r['mode']} | encoder {r['encoder']} | âm {'có' if r['sound'] else 'không'}")
    _log(f"overlay {'cache' if r['overlay_cached'] else 'render mới'} {r['overlay_seconds']}s | ghép {r['compose_seconds']}s")
    _log(f"video {i['w']}x{i['h']}@{i['fps']} {i['duration']:.3f}s → {o['w']}x{o['h']}@{o['fps']} {o['duration']:.3f}s (lệch {r['duration_delta']:+.3f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
