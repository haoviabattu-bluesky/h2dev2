r"""khoa_ultra.py — KHOÁ dùng chung Chrome Ultra TUAN_PROFILE (nguyenquoctuan102000@gmail.com, cổng 9350).

Anh chốt 16/10/2026: profile Ultra này làm cả ẢNH hook (Google Flow, `anh_hook.py`) lẫn CLIP hook (Google Vids,
`tools\hook_lane_g\vids_hook.py`), và CÁC TẬP KHÔNG ĐƯỢC CHẠY PROFILE SONG SONG. Mọi tool lái profile phải giữ khoá này
suốt lúc chạy:
  - ảnh hook: khoá bận / cổng chết → đi 9router (rồi gpti2), KHÔNG chờ;
  - clip hook: không có đường thay tương đương → CHỜ khoá (in ai đang giữ).

Khoá = msvcrt.locking trên `E:\CLAUDE\YOUTUBE\TUAN_PROFILE.lock` (nằm CẠNH thư mục profile, không đụng gì bên trong).
Hệ điều hành tự nhả khi tiến trình chết → không có khoá "mồ côi". Ai đang giữ ghi ở `TUAN_PROFILE.lock.json`.

    py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\khoa_ultra.py      ← xem ai đang giữ + cổng sống không
"""
import json
import msvcrt
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

PROFILE = Path(r"E:\CLAUDE\YOUTUBE\TUAN_PROFILE")
CDP = "http://127.0.0.1:9350"
LOCK = PROFILE.with_name("TUAN_PROFILE.lock")
INFO = PROFILE.with_name("TUAN_PROFILE.lock.json")
MO_PROFILE = Path(r"E:\CLAUDE\YOUTUBE\GROK_VIDEO\open_tuan_profile.bat")


def cong_song(cdp=CDP, timeout=3):
    try:
        with urllib.request.urlopen(cdp.rstrip("/") + "/json/version", timeout=timeout) as r:
            return r.status == 200
    except Exception:
        return False


def mo_neu_chet(cdp=CDP, cho_s=30):
    """Cổng chết → mở lại ĐÚNG profile bằng lệnh cũ (open_tuan_profile.bat, cùng --user-data-dir) — luật Chrome profile
    mục 4. Không kill, không tạo lại thư mục. Trả True nếu cổng sống."""
    if cong_song(cdp):
        return True
    if not MO_PROFILE.exists():
        return False
    print(f"  cổng {cdp} chưa sống → mở profile Ultra bằng {MO_PROFILE}")
    subprocess.Popen(["cmd", "/c", str(MO_PROFILE)], creationflags=getattr(subprocess, "DETACHED_PROCESS", 0))
    t0 = time.time()
    while time.time() - t0 < cho_s:
        time.sleep(2)
        if cong_song(cdp):
            time.sleep(5)   # cho trang đầu tải xong
            return True
    return False


def ai_dang_giu():
    try:
        return json.loads(INFO.read_text(encoding="utf-8"))
    except Exception:
        return {}


class Khoa:
    """with Khoa("anh_hook", tap) as k: if k.co: ...  — k.co=False nghĩa là tập khác đang giữ profile."""

    def __init__(self, tool, tap="", cho_s=0, bao_moi_s=60):
        self.tool, self.tap, self.cho_s, self.bao_moi_s = tool, str(tap), cho_s, bao_moi_s
        self.f, self.co = None, False

    def thu(self):
        self.f = open(LOCK, "a+b")
        t0, bao = time.time(), 0.0
        while True:
            try:
                self.f.seek(0)
                msvcrt.locking(self.f.fileno(), msvcrt.LK_NBLCK, 1)
                self.co = True
                INFO.write_text(json.dumps({"tool": self.tool, "tap": self.tap, "pid": os.getpid(),
                                            "tu": time.strftime("%Y-%m-%d %H:%M:%S")}, ensure_ascii=False, indent=1),
                                encoding="utf-8")
                return True
            except OSError:
                if time.time() - t0 >= self.cho_s:
                    self.f.close(); self.f = None
                    return False
                if time.time() - bao >= self.bao_moi_s:
                    g = ai_dang_giu()
                    print(f"  ⏳ profile Ultra đang bận: {g.get('tool', '?')} · {g.get('tap', '?')} (pid {g.get('pid', '?')}, "
                          f"từ {g.get('tu', '?')}) — chờ tới lượt…", flush=True)
                    bao = time.time()
                time.sleep(5)

    def nha(self):
        if self.f:
            try:
                if self.co:
                    self.f.seek(0)
                    msvcrt.locking(self.f.fileno(), msvcrt.LK_UNLCK, 1)
                    INFO.unlink(missing_ok=True)
            except OSError:
                pass
            self.f.close()
        self.f, self.co = None, False

    def __enter__(self):
        self.thu()
        return self

    def __exit__(self, *a):
        self.nha()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    k = Khoa("kiem_tra")
    ranh = k.thu(); k.nha()
    print(f"cổng {CDP}: {'SỐNG' if cong_song() else 'CHẾT'} · khoá: "
          + ("RẢNH" if ranh else f"BẬN — {ai_dang_giu()}"))
