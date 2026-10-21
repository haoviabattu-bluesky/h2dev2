# -*- coding: utf-8 -*-
"""Tìm ffmpeg, đọc thông số video, chọn encoder. Cùng cách h2dev (assemble.py:36): imageio_ffmpeg trước."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from fractions import Fraction

_NO_WINDOW = 0x08000000 if sys.platform.startswith("win") else 0  # không nháy cửa sổ cmd đen trong .exe
_FF = None
_ENCODER_CACHE: dict = {}


def ffmpeg_exe() -> str:
    global _FF
    if _FF:
        return _FF
    try:
        import imageio_ffmpeg
        _FF = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        _FF = shutil.which("ffmpeg")
    if not _FF:
        raise SystemExit("[LỖI] Không tìm thấy ffmpeg (cài: py -m pip install imageio-ffmpeg, hoặc thêm ffmpeg vào PATH)")
    return _FF


def run(args: list, stdin=None, check=True) -> subprocess.CompletedProcess:
    cmd = [ffmpeg_exe(), "-hide_banner", *([] if stdin is not None else ["-nostdin"]), *map(str, args)]
    p = subprocess.run(cmd, input=stdin, capture_output=True, creationflags=_NO_WINDOW)
    if check and p.returncode != 0:
        tail = p.stderr.decode("utf-8", "replace")[-2500:]
        raise RuntimeError(f"ffmpeg lỗi (exit {p.returncode}):\n{tail}")
    return p


def popen(args: list) -> subprocess.Popen:
    cmd = [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", *map(str, args)]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=_NO_WINDOW)


_COMMON_FPS = {23.98: "24000/1001", 23.976: "24000/1001", 29.97: "30000/1001", 59.94: "60000/1001"}


def fps_fraction(value) -> str:
    """'30' / 29.97 / '30000/1001' → chuỗi phân số chuẩn cho ffmpeg."""
    if isinstance(value, str) and "/" in value:
        return str(Fraction(value))
    v = round(float(value), 3)
    if v in _COMMON_FPS:
        return _COMMON_FPS[v]
    return str(Fraction(v).limit_denominator(1001))


def probe(path) -> dict:
    """Đọc w/h/fps/duration/has_audio từ stderr `ffmpeg -i` (imageio không kèm ffprobe)."""
    err = run(["-i", str(path)], check=False).stderr.decode("utf-8", "replace")
    dm = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", err)
    vm = re.search(r"Stream #\S+.*?Video:.*?(\d{2,5})x(\d{2,5})", err)
    if not (dm and vm):
        raise RuntimeError(f"Không đọc được video {path}:\n{err[-800:]}")
    fm = re.search(r"Video:.*?(\d+(?:\.\d+)?)\s*fps", err) or re.search(r"Video:.*?(\d+(?:\.\d+)?)\s*tbr", err)
    rot = re.search(r"rotation of (-?\d+(?:\.\d+)?)", err)
    w, h = int(vm.group(1)), int(vm.group(2))
    if rot and abs(float(rot.group(1))) in (90.0, 270.0):
        w, h = h, w  # video điện thoại quay dọc có metadata xoay
    am = re.search(r"Stream #\S+.*?Audio:.*?(\d+) Hz, (mono|stereo|[\d.]+\(?\w*\)?)", err)
    # "Video: h264 (High) (avc1 / 0x..), yuvj420p(pc, bt709, progressive), 1920x1080" — mode segment cần khớp nguồn
    cm = re.search(r"Video:\s*(\w+)(?:\s*\(([^)]*)\))?[^,]*,\s*(\w+)(?:\(([^)]*)\))?", err)
    vtags = [t.strip() for t in (cm.group(4) or "").split(",")] if cm else []
    return {"w": w, "h": h, "fps": fps_fraction(fm.group(1) if fm else 30),
            "vcodec": cm.group(1) if cm else "", "vprofile": (cm.group(2) or "").lower() if cm else "",
            "pix_fmt": cm.group(3) if cm else "", "color_range": "pc" if "pc" in vtags else "tv",
            "audio_rate": int(am.group(1)) if am else 48000,
            "audio_layout": am.group(2) if am and am.group(2) in ("mono", "stereo", "5.1", "5.1(side)") else "stereo",
            "duration": int(dm.group(1)) * 3600 + int(dm.group(2)) * 60 + float(dm.group(3)),
            "has_audio": bool(re.search(r"Stream #\S+.*?Audio:", err))}


def _works(enc: str) -> bool:
    p = run(["-f", "lavfi", "-i", "color=c=black:s=256x256:d=0.2", "-c:v", enc, "-f", "null", "-"], check=False)
    return p.returncode == 0


def video_encoder_args(cfg: dict) -> tuple[str, list]:
    """Trả (tên encoder, tham số). auto = thử NVENC THẬT (encode 0.2s), hỏng → libx264."""
    want = cfg.get("video_encoder", "auto")
    crf, preset = int(cfg.get("video_crf", 18)), str(cfg.get("video_preset", "medium"))
    enc = want
    if want == "auto":
        if "auto" not in _ENCODER_CACHE:
            _ENCODER_CACHE["auto"] = "h264_nvenc" if _works("h264_nvenc") else "libx264"
        enc = _ENCODER_CACHE["auto"]
    if enc == "h264_nvenc":
        return enc, ["-c:v", "h264_nvenc", "-preset", "p5", "-rc", "vbr", "-cq", str(crf + 1), "-b:v", "0",
                     "-pix_fmt", "yuv420p"]
    return "libx264", ["-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p"]
