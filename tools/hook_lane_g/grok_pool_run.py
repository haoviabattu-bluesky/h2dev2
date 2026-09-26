# -*- coding: utf-8 -*-
"""Sinh clip hook Grok FREE mà KHÔNG gõ gì trên giao diện của tài khoản mới (Lane G, 2026-09-25).

Vì sao: nhặt mã chống bot (x-statsig-id) bằng cách gõ "ping"+Enter trên tài khoản mới làm lọt request → Grok sinh
video "ping" (hồ nước/đường rừng/chợ/con mèo) và ĂN lượt duy nhất; đo thật 17 tài khoản bị mất (ep05/ep06).
Cách này: nhặt mã trên 1 tài khoản ĐÃ HẾT lượt ("burner" — lọt cũng không mất gì), giữ mã trong file RIÊNG
(_pool.json, không dùng grok_headers.json chung với tab khác), rồi tài khoản mới chỉ gọi API với mã đó.
Mỗi clip xong: so khung đầu với ảnh gốc (lệch >15 = sai cảnh → bỏ) + LUÔN tắt profile + ghi cột E.

    py -3.13 grok_pool_run.py <thư mục hook> <email burner đã hết lượt> [số tài khoản tối đa]
"""
import json, os, re, subprocess, sys, time
from pathlib import Path

GV = Path(r"E:\CLAUDE\YOUTUBE\GROK_VIDEO")
sys.path.insert(0, str(GV))
HOOK = Path(sys.argv[1]); BURNER = sys.argv[2]; MAX = int(sys.argv[3]) if len(sys.argv) > 3 else 10
POOL = Path(__file__).with_name("_pool.json")
PY = ["py", "-3.13", "-X", "utf8"]
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def run(cmd, timeout=300):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV, cwd=GV, timeout=timeout)
    return (r.stdout or "") + (r.stderr or "")


def lech_anh(img, clip):
    import io, imageio_ffmpeg
    from PIL import Image, ImageChops, ImageStat
    b = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-ss", "0.1", "-i", str(clip), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    x = Image.open(img).convert("L").resize((64, 36)); y = Image.open(io.BytesIO(b)).convert("L").resize((64, 36))
    return ImageStat.Stat(ImageChops.difference(x, y)).mean[0]


def mo(email=None):
    out = run(PY + [str(GV / "gpm_grok_mo.py")] + ([email] if email else ["--pick"]))
    m = re.search(r"PORT=(\d+) VIDEO_CON=(\d+) PID=(\S+)(?: ROW=(\d+))?", out)
    print(next((l for l in out.splitlines() if l.startswith("tai khoan")), out[-200:])[:150], flush=True)
    return m.groups() if m else None


def dong(pid, row):
    print("  " + run(PY + [str(GV / "gpm_grok_mo.py"), "--close", pid, str(row)]).strip().splitlines()[-1], flush=True)


def lay_ma():
    """Nhặt 12 mã trên burner (đã hết lượt video → có lọt cũng không mất gì)."""
    from grok_client import GrokImagine
    g_ = mo(BURNER)
    if not g_:
        raise SystemExit("✗ không mở được burner")
    port, con, pid, row = g_
    try:
        if int(con) > 0:
            raise SystemExit(f"✗ burner {BURNER} còn {con} lượt — phải dùng tài khoản ĐÃ HẾT lượt")
        g = GrokImagine(cdp_url=f"http://127.0.0.1:{port}").open()
        g.mint_pool(want=12, max_submit=16)
        ids = list(g._pool); g.close()
        POOL.write_text(json.dumps({"ts": time.time(), "pool": ids}), encoding="utf-8")
        print(f"  ✓ nhặt {len(ids)} mã trên burner", flush=True)
    finally:
        rr = run(PY + [str(GV / "grok_tai_khoan.py"), "list"])
        rw = next((l.split()[1] for l in rr.splitlines() if BURNER in l), None)
        dong(pid, rw or 0)


def ma_tiep():
    d = json.loads(POOL.read_text(encoding="utf-8")) if POOL.exists() else {"ts": 0, "pool": []}
    if not d["pool"] or time.time() - d["ts"] > 1500:
        lay_ma(); d = json.loads(POOL.read_text(encoding="utf-8"))
    sid = d["pool"].pop(); POOL.write_text(json.dumps(d), encoding="utf-8")
    return sid


def thieu():
    tl = json.loads((HOOK / "hook_timeline.json").read_text(encoding="utf-8"))["shots"]
    return [s["n"] for s in tl if not ((HOOK / "clip" / f"clip_{s['n']:02d}.mp4").exists())]


jobs = {r["id"]: r for r in __import__("csv").DictReader(open(HOOK / "grok_jobs.csv", encoding="utf-8-sig"))}
for _ in range(MAX):
    t = thieu()
    if not t:
        print("✓ đủ clip"); break
    n = t[0]; j = jobs[f"clip_{n:02d}"]
    sid = ma_tiep()
    g_ = mo()
    if not g_:
        print("✗ hết tài khoản"); break
    port, con, pid, row = g_
    try:
        if int(con) < 1:
            print(f"  dòng {row}: 0 lượt → bỏ"); continue
        from grok_client import GrokImagine, GrokError
        g = GrokImagine(cdp_url=f"http://127.0.0.1:{port}").open()
        g._pool = [sid]
        g.mint_pool = lambda *a, **k: (_ for _ in ()).throw(GrokError("KHÔNG nhặt mã trên tài khoản mới"))
        dst = HOOK / "clip" / f"clip_{n:02d}.mp4"
        try:
            res = g.image_to_video(j["image"], j["prompt"], str(dst), duration=6, resolution="720p", aspect="16:9", skip_audio=True, raw_out=str(HOOK / "clip" / f"_raw_{n:02d}_dong{row}.txt"))
            d = lech_anh(HOOK / "img" / f"{n:03d}.png", dst)
            if d > 15:
                (HOOK / "clip" / "_sai").mkdir(exist_ok=True)
                dst.replace(HOOK / "clip" / "_sai" / f"clip_{n:02d}_dong{row}.mp4")
                print(f"  ✗ clip_{n:02d} SAI CẢNH (lệch {d:.0f}) → bỏ", flush=True)
            else:
                print(f"  ✓ clip_{n:02d} OK {res['seconds']}s · khớp ảnh gốc (lệch {d:.1f})", flush=True)
        except Exception as e:
            print(f"  ✗ clip_{n:02d} lỗi: {str(e)[:160]}", flush=True)
        finally:
            g.close()
    finally:
        dong(pid, row)
print("còn thiếu:", thieu())
