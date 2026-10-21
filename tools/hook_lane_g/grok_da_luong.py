# -*- coding: utf-8 -*-
"""Sinh clip hook Grok ĐA LUỒNG: mở cùng lúc N profile GPM (mỗi tài khoản FREE = 1 clip/24h), mỗi luồng 1 clip.

Khác grok_1tk.py (tuần tự): chọn trước N tài khoản rảnh bằng account_pool.pick_free, mỗi luồng mở ĐÚNG 1 profile
(gpm_grok_mo.py <email>), chạy grok_batch.py vào thư mục tạm riêng (results.csv không đè nhau; header chống bot đã
tách theo cổng grok_headers_<port>.json), kiểm khung đầu khớp ảnh gốc rồi chuyển clip vào <hook>/clip/.
LUÔN gpm_grok_mo.py --close <pid> <row> (tắt profile + ghi cột E) kể cả khi lỗi. Clip lỗi/sai cảnh → vòng sau
lấy tài khoản khác (bỏ tài khoản vừa lỗi), tối đa --vong vòng.
Số luồng tự chọn = min(số clip thiếu, số tài khoản rảnh), kẹp 5–10 (anh chốt 03/10); các luồng mở GPM lệch nhau
--gian giây để GPM không nghẽn khi mở 10 profile cùng lúc.

    py -3.13 grok_da_luong.py <thư mục hook TUYỆT ĐỐI> [--luong 5..10] [--vong 4] [--min-row 600]
"""
import argparse, os, re, shutil, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import grok_1tk_lib as L  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("hook")
ap.add_argument("--luong", type=int, default=10, help="trần số luồng, kẹp 5–10")
ap.add_argument("--gian", type=float, default=4, help="giây lệch giữa 2 lần mở profile GPM")
ap.add_argument("--vong", type=int, default=4)
ap.add_argument("--min-row", type=int, default=None)
ap.add_argument("--bo-kiem-chu", action="store_true", help="bỏ cổng chữ trên đạo cụ (chỉ khi anh cho phép)")
a = ap.parse_args()
a.luong = max(5, min(10, a.luong))
HOOK = Path(a.hook).resolve()
# 2026-10-10 (anh chốt): đạo cụ mang chữ trọng tâm phải được CHÈN CHỮ VÀO ẢNH TRƯỚC khi sinh clip (pipeline/chu_dao_cu.py)
if not a.bo_kiem_chu:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
    import chu_dao_cu  # noqa: E402
    chu_dao_cu.cong({}, HOOK.parent, "grok_da_luong (trước khi sinh clip)", sau_grok=False)
if a.min_row:
    L.ENV["GROK_MIN_ROW"] = str(a.min_row)
os.environ.update(L.ENV)
sys.path.insert(0, str(L.GV))
import account_pool  # noqa: E402

khoa_in = threading.Lock()


def log(*x):
    with khoa_in:
        print(*x, flush=True)


def lam(k, clip_id, tk):
    email, pid, row = tk["email"], tk["pid"], tk["row"]
    time.sleep(k % a.luong * a.gian)  # lệch giờ mở profile
    tmp = HOOK / "clip" / f"_tmp_{clip_id}_{row}"
    try:
        out = L.run(L.PY + [str(L.GV / "gpm_grok_mo.py"), email], timeout=300)
        m = re.search(r"PORT=(\d+) VIDEO_CON=(\d+) PID=(\S+)", out)
        if not m:
            log(f"[{clip_id}] ✗ không mở được {email} (dòng {row}): {out.strip()[-200:]}")
            return False
        port, con = m.group(1), int(m.group(2))
        if con < 1:
            log(f"[{clip_id}] dòng {row}: 0 lượt → bỏ")
            return False
        o = L.run(L.PY + [str(L.GV / "grok_batch.py"), "--jobs", str(HOOK / "grok_jobs.csv"), "--out", str(tmp),
                          "--no-audio", "--gap", "5", "--retry", "0", "--only", clip_id],
                  env=dict(L.ENV, GROK_CDP=f"http://127.0.0.1:{port}"))
        c = tmp / f"{clip_id}.mp4"
        if not (c.exists() and c.stat().st_size > 10240):
            log(f"[{clip_id}] ✗ không ra clip ({email}): " + " | ".join(o.strip().splitlines()[-4:])[-300:])
            return False
        n = int(clip_id.split("_")[1])
        d = L.lech_anh(HOOK / "img" / f"{n:03d}.png", c)
        if d > 15:
            (HOOK / "clip" / "_sai").mkdir(parents=True, exist_ok=True)
            c.replace(HOOK / "clip" / "_sai" / f"{clip_id}_dong{row}.mp4")
            log(f"[{clip_id}] ✗ SAI CẢNH (lệch {d:.0f} > 15) dòng {row}")
            return False
        c.replace(HOOK / "clip" / f"{clip_id}.mp4")
        log(f"[{clip_id}] ✓ khớp ảnh gốc (lệch {d:.1f}) · {email}")
        return True
    finally:
        log(f"[{clip_id}] " + (L.run(L.PY + [str(L.GV / "gpm_grok_mo.py"), "--close", pid, str(row)], timeout=120)
                               .strip().splitlines() or ["?"])[-1])
        shutil.rmtree(tmp, ignore_errors=True)


def lam_an_toan(x):
    """1 luồng ném lỗi (timeout grok_batch…) không được làm sập cả vòng."""
    k, clip_id, tk = x
    try:
        ok = lam(k, clip_id, tk)
    except Exception as e:  # noqa: BLE001
        log(f"[{clip_id}] ✗ lỗi luồng ({tk['email']}): {e!r}"[:300])
        ok = False
    if not ok:
        hong.add(tk["email"])
    return ok



def cho_luot_grok():
    """Khoá liên tiến trình (05/10): nhiều lane chạy lô cùng lúc → pick_free có thể bốc TRÙNG tài khoản trước khi
    profile kịp mở. Lane đến sau đứng chờ lane trước xong hẳn Grok (khoá tự nhả khi tiến trình thoát)."""
    import msvcrt
    f = open(Path(L.GV) / "grok_da_luong.lock", "a+")
    bao = False
    while True:
        try:
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            return f
        except OSError:
            if not bao:
                log("⏳ lane khác đang chạy Grok đa luồng → chờ tới lượt…")
                bao = True
            time.sleep(30)


_khoa_grok = cho_luot_grok()
hong = set()  # tài khoản lỗi trong lần chạy này → vòng sau không lấy lại
for v in range(1, a.vong + 1):
    t = L.thieu(HOOK)
    if not t:
        break
    tks = [x for x in account_pool.pick_free(need=len(t) + len(hong)) if x["email"] not in hong][:len(t)]
    if len(tks) < len(t):
        log(f"⚠ chỉ còn {len(tks)} tài khoản rảnh cho {len(t)} clip")
    viec = [(k, c, tk) for k, (c, tk) in enumerate(zip(t, tks))]
    if not viec:
        break
    n_luong = min(a.luong, len(viec))
    log(f"== vòng {v}: {len(viec)} clip, {n_luong} luồng: {[x[1] for x in viec]}")
    with ThreadPoolExecutor(n_luong) as ex:
        list(ex.map(lam_an_toan, viec))
con = L.thieu(HOOK)
print("✓ đủ clip" if not con else f"còn thiếu: {con}")
sys.exit(0 if not con else 2)
