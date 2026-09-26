# -*- coding: utf-8 -*-
"""Sinh clip hook bằng tài khoản Grok FREE trong GPM (tab GROK): 1 tài khoản = 1 clip (1 lượt/24h).

Mỗi lượt: gpm_grok_mo.py --pick → xoá cache mã chống bot cũ → grok_batch.py --only <clip còn thiếu> →
LUÔN gpm_grok_mo.py --close <PID> <ROW> (tắt profile ngay + ghi cột E), kể cả khi lỗi.
Danh sách clip cần = shots trong <hook>/hook_timeline.json.

    py -3.13 grok_1tk.py <thư mục hook> [số lượt tối đa]
"""
import json, os, re, subprocess, sys
from pathlib import Path

GV = Path(r"E:\CLAUDE\YOUTUBE\GROK_VIDEO")
HOOK = Path(sys.argv[1]); LAN = int(sys.argv[2]) if len(sys.argv) > 2 else 12
PY = ["py", "-3.13", "-X", "utf8"]
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def run(cmd, env=ENV, timeout=900):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=GV, timeout=timeout)
    return (r.stdout or "") + (r.stderr or "")


def lech_anh(img, clip):
    """Khung đầu clip so với ảnh gốc (xám 64x36, lệch trung bình 0–255). Đo thật 25/09: clip đúng <3, clip Grok
    tự chế cảnh (ảnh không được gắn → text→video) 54–68. Ngưỡng 15."""
    import io
    import imageio_ffmpeg
    from PIL import Image, ImageChops, ImageStat
    b = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-ss", "0.1", "-i", str(clip), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    x = Image.open(img).convert("L").resize((64, 36))
    y = Image.open(io.BytesIO(b)).convert("L").resize((64, 36))
    return ImageStat.Stat(ImageChops.difference(x, y)).mean[0]


def thieu():
    ids = [f"clip_{s['n']:02d}" for s in json.loads((HOOK / "hook_timeline.json").read_text(encoding="utf-8"))["shots"]]
    return [i for i in ids if not ((HOOK / "clip" / f"{i}.mp4").exists() and (HOOK / "clip" / f"{i}.mp4").stat().st_size > 10240)]


for _ in range(LAN):
    t = thieu()
    if not t:
        print("✓ đủ clip"); break
    out = run(PY + [str(GV / "gpm_grok_mo.py"), "--pick"], timeout=300)
    m = re.search(r"PORT=(\d+) VIDEO_CON=(\d+) PID=(\S+) ROW=(\d+)", out)
    print(next((l for l in out.splitlines() if l.startswith("tai khoan")), out[-300:]), flush=True)
    if not m:
        print("✗ không mở được tài khoản:", out[-500:]); break
    port, con, pid, row = m.groups()
    try:
        if int(con) < 1:
            print(f"  dòng {row}: 0 lượt → bỏ"); continue
        (GV / "grok_headers.json").unlink(missing_ok=True)      # mã chống bot của tài khoản khác → không dùng lại
        o = run(PY + [str(GV / "grok_batch.py"), "--jobs", str(HOOK / "grok_jobs.csv"), "--out", str(HOOK / "clip"),
                      "--no-audio", "--gap", "5", "--retry", "0", "--only", t[0]], env=dict(ENV, GROK_CDP=f"http://127.0.0.1:{port}"))
        print("  " + "\n  ".join(l for l in o.splitlines() if re.search(r"OK |QUOTA|REJECT|FAIL|TỤT|XONG", l))[-800:], flush=True)
        c = HOOK / "clip" / f"{t[0]}.mp4"
        if c.exists():
            n = int(t[0].split("_")[1])
            d = lech_anh(HOOK / "img" / f"{n:03d}.png", c)
            if d > 15:
                (HOOK / "clip" / "_sai").mkdir(exist_ok=True)
                c.replace(HOOK / "clip" / "_sai" / f"{t[0]}_dong{row}.mp4")
                print(f"  ✗ {t[0]} SAI CẢNH (lệch ảnh gốc {d:.0f} > 15 — Grok không gắn ảnh) → bỏ, chạy tài khoản khác", flush=True)
            else:
                print(f"  ✓ {t[0]} khớp ảnh gốc (lệch {d:.1f})", flush=True)
    finally:
        print("  " + run(PY + [str(GV / "gpm_grok_mo.py"), "--close", pid, row], timeout=120).strip().splitlines()[-1], flush=True)
print("còn thiếu:", thieu())
