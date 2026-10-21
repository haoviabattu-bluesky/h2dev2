# -*- coding: utf-8 -*-
"""Sinh clip hook bằng NHIỀU tài khoản Grok free SONG SONG (anh chốt 01/10/2026): mỗi luồng = 1 tài khoản = 1 cảnh.

Khác `grok_1tk.py` (tuần tự, 1 tài khoản/lượt): ở đây N luồng chạy cùng lúc.
  · MỞ profile (`gpm_grok_mo.py --pick`) được tuần tự bằng 1 khoá (tránh 2 luồng cùng chọn 1 profile) — phần sinh clip (~2 phút) chạy song song.
  · Mỗi clip ra thư mục riêng `clip/_w/<id>/` (results.csv riêng, không đụng nhau) rồi chuyển về `clip/<id>.mp4`.
  · Mã chống bot cache theo CỔNG CDP (`grok_headers_<port>.json`) nên các luồng không dùng nhầm của nhau.
  · LUÔN `--close` profile (tắt + ghi cột E) kể cả lỗi. Clip lệch ảnh gốc >15 hoặc lỗi → đưa lại hàng đợi (tối đa 3 lần/clip).

    py -3.13 grok_song_song.py <thư mục hook> [số luồng=8] [--chi 11-19 | 3,5,7]
"""
import json, os, re, shutil, subprocess, sys, threading, queue
from pathlib import Path

GV = Path(r"E:\CLAUDE\YOUTUBE\GROK_VIDEO")
HOOK = Path(sys.argv[1])
NT = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 8
CHI = None
if "--chi" in sys.argv:
    s = sys.argv[sys.argv.index("--chi") + 1]
    CHI = set()
    for p in s.split(","):
        a, _, b = p.partition("-")
        CHI |= set(range(int(a), int(b or a) + 1))
PY = ["py", "-3.13", "-X", "utf8"]
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
LOCK_MO = threading.Lock()
LOCK_IN = threading.Lock()
TOI_DA = 3


def log(*a):
    with LOCK_IN:
        print(*a, flush=True)


def run(cmd, env=ENV, timeout=900):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=GV, timeout=timeout)
    return (r.stdout or "") + (r.stderr or "")


sys.path.insert(0, str(Path(__file__).parent))


def lech_anh(img, clip):
    import io
    import imageio_ffmpeg
    from PIL import Image, ImageChops, ImageStat
    b = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-ss", "0.1", "-i", str(clip), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    x = Image.open(img).convert("L").resize((64, 36))
    y = Image.open(io.BytesIO(b)).convert("L").resize((64, 36))
    return ImageStat.Stat(ImageChops.difference(x, y)).mean[0]


def ids_can_lam():
    ids = [f"clip_{s['n']:02d}" for s in json.loads((HOOK / "hook_timeline.json").read_text(encoding="utf-8"))["shots"]]
    ra = []
    for i in ids:
        n = int(i.split("_")[1])
        if CHI is not None and n not in CHI:
            continue
        c = HOOK / "clip" / f"{i}.mp4"
        if c.exists() and c.stat().st_size > 10240:
            continue
        if (HOOK / "img" / f"{n:03d}.png").exists():
            ra.append(i)
    return ra


Q = queue.Queue()
LAN = {}
for i in ids_can_lam():
    Q.put(i)
    LAN[i] = 0


def luong(k):
    while True:
        try:
            clip = Q.get_nowait()
        except queue.Empty:
            return
        n = int(clip.split("_")[1])
        pid = row = None
        try:
            # --- mở tài khoản (tuần tự, có khoá) ---
            while True:
                with LOCK_MO:
                    out = run(PY + [str(GV / "gpm_grok_mo.py"), "--pick"], timeout=400)
                m = re.search(r"PORT=(\d+) VIDEO_CON=(\d+) PID=(\S+) ROW=(\d+)", out)
                if not m:
                    log(f"[L{k}] ✗ không mở được tài khoản cho {clip}: {out[-300:]}")
                    raise RuntimeError("khong mo duoc")
                port, con, pid, row = m.groups()
                if int(con) < 1:
                    log(f"[L{k}] dòng {row}: 0 lượt → đóng, lấy tài khoản khác")
                    run(PY + [str(GV / "gpm_grok_mo.py"), "--close", pid, row], timeout=120)
                    pid = row = None
                    continue
                break
            log(f"[L{k}] {clip} ← dòng {row} (cổng {port})")
            wd = HOOK / "clip" / "_w" / clip
            shutil.rmtree(wd, ignore_errors=True)
            wd.mkdir(parents=True)
            o = run(PY + [str(GV / "grok_batch.py"), "--jobs", str(HOOK / "grok_jobs.csv"), "--out", str(wd),
                          "--no-audio", "--gap", "5", "--retry", "0", "--only", clip],
                    env=dict(ENV, GROK_CDP=f"http://127.0.0.1:{port}"))
            c = wd / f"{clip}.mp4"
            if c.exists() and c.stat().st_size > 10240:
                d = lech_anh(HOOK / "img" / f"{n:03d}.png", c)
                if d > 15:
                    (HOOK / "clip" / "_sai").mkdir(exist_ok=True)
                    c.replace(HOOK / "clip" / "_sai" / f"{clip}_dong{row}.mp4")
                    log(f"[L{k}] ✗ {clip} SAI CẢNH (lệch {d:.0f} > 15) → xếp lại hàng đợi")
                    raise RuntimeError("sai canh")
                c.replace(HOOK / "clip" / f"{clip}.mp4")
                log(f"[L{k}] ✓ {clip} xong, khớp ảnh gốc (lệch {d:.1f})")
            else:
                log(f"[L{k}] ✗ {clip} không ra clip — " + " | ".join(o.strip().splitlines()[-4:])[-400:])
                raise RuntimeError("khong ra clip")
        except Exception:
            LAN[clip] += 1
            if LAN[clip] < TOI_DA:
                Q.put(clip)
            else:
                log(f"[L{k}] ⛔ {clip} hỏng {TOI_DA} lần — bỏ, xử lý tay")
        finally:
            if pid:
                r = run(PY + [str(GV / "gpm_grok_mo.py"), "--close", pid, row], timeout=120).strip().splitlines()
                log(f"[L{k}] " + (r[-1] if r else "close ?"))


if __name__ == "__main__":
    if Q.empty():
        print("✓ không còn clip cần làm"); sys.exit(0)
    print(f"{Q.qsize()} clip · {min(NT, Q.qsize())} luồng song song", flush=True)
    ts = [threading.Thread(target=luong, args=(k + 1,)) for k in range(min(NT, Q.qsize()))]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    shutil.rmtree(HOOK / "clip" / "_w", ignore_errors=True)
    print("còn thiếu:", ids_can_lam())
