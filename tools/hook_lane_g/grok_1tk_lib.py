# -*- coding: utf-8 -*-
"""Hàm dùng chung cho grok_da_luong.py (chép từ grok_1tk.py — file đó chạy vòng lặp ngay khi import nên không import được)."""
import json, os, subprocess
from pathlib import Path

GV = Path(r"E:\CLAUDE\YOUTUBE\GROK_VIDEO")
PY = ["py", "-3.13", "-X", "utf8"]
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
ENV.setdefault("GROK_SHEET_ID", "1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU")


def run(cmd, env=None, timeout=900):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env or ENV, cwd=GV, timeout=timeout)
    return (r.stdout or "") + (r.stderr or "")


def lech_anh(img, clip):
    """Khung đầu clip so với ảnh gốc (xám 64x36, lệch trung bình 0–255). Clip đúng <3, Grok tự chế cảnh 54–68. Ngưỡng 15."""
    import io
    import imageio_ffmpeg
    from PIL import Image, ImageChops, ImageStat
    b = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-ss", "0.1", "-i", str(clip), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    x = Image.open(img).convert("L").resize((64, 36))
    y = Image.open(io.BytesIO(b)).convert("L").resize((64, 36))
    return ImageStat.Stat(ImageChops.difference(x, y)).mean[0]


def thieu(hook):
    hook = Path(hook)
    # 10/10: shot dùng lại clip cũ / clip số khác n (Lane N ep10) → lấy theo trường `clip`, thiếu mới rơi về n
    ids = list(dict.fromkeys(Path(s["clip"]).stem if s.get("clip") else f"clip_{s['n']:02d}"
                             for s in json.loads((hook / "hook_timeline.json").read_text(encoding="utf-8"))["shots"]))
    return [i for i in ids if not ((hook / "clip" / f"{i}.mp4").exists() and (hook / "clip" / f"{i}.mp4").stat().st_size > 10240)
            and (hook / "img" / f"{int(i.split('_')[1]):03d}.png").exists()]
