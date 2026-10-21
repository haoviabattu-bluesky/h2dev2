r"""chay_phan_chu.py — chay PHAN CHU cua mot tap, DUNG TRUOC khau gen loat anh.

Thay cho cac script roi `run_sach_vNN.py` trong scratchpad (moi tap mot ban copy, sua tay so idx —
de quen, de lech). Day la buoc 2 cua THE CHAY trong docs/SOP_CLONE_BRAIN.md.

Ra: script.txt · characters.json · img_prompts.txt · thumb_text.txt + ANH MASTER da gen bang gpti2.
KHONG gen loat anh (viec cua may 2), KHONG TTS, KHONG render.

  py -3.13 chay_phan_chu.py --idx 1
  py -3.13 chay_phan_chu.py --idx 3 --profile satori-jp-obaa --channel "https://www.youtube.com/@simbot2"

`--idx` la VI TRI VIDEO trong bang quet kenh (`brain_channel.py --limit`), cung chinh la STT dong
trong tab trang tinh cua kenh — giu mot he so duy nhat tu kenh -> thu muc -> dong sheet, khoi truy
nguoc nham (xem CLAUDE.md muc "SO TAP LAY TU TRANG TINH").

In moc thoi gian moi dong (luat: bao cao test luon kem so do thoi gian).
"""
import argparse
import datetime as dt
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
os.chdir(HERE)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import profiles                      # noqa: E402
import brain_channel as bc           # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--idx", type=int, required=True, help="vi tri video trong bang quet kenh = STT dong sheet")
    ap.add_argument("--profile", required=True)   # 17/10/2026: lane Satori (satori-jp-obaa) đã BỎ — không còn profile mặc định, phải khai --profile.
    ap.add_argument("--channel", default="https://www.youtube.com/@simbot2")
    ap.add_argument("--handle", default="simbot2")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--budget", type=float, default=15.0)
    a = ap.parse_args()

    T0 = time.perf_counter()

    def log(s):
        print(f"[{dt.datetime.now():%H:%M:%S} · +{(time.perf_counter()-T0)/60:5.1f}′] {s}", flush=True)

    # scan_channel tra DICT (channel_title/handle/videos...), KHONG phai list — lay dung khoa
    # `videos`. Ban dau viet `vids[idx-1]` thang tren dict => KeyError: 0.
    vids = bc.scan_channel(a.channel, limit=a.limit).get("videos") or []
    if not 1 <= a.idx <= len(vids):
        log(f"✗ --idx {a.idx} ngoai khoang 1..{len(vids)}")
        return 2
    video = vids[a.idx - 1]
    prof = profiles.load(a.profile)

    log(f"=== BAT DAU · video #{a.idx}/{len(vids)} · {video.get('id')} ===")
    log(f"    {str(video.get('title',''))[:90]}")
    ok = bc.make_video_one(video, prof, handle=a.handle, idx=a.idx, minutes=0,
                           on_line=log, permission_mode="bypassPermissions",
                           budget_usd=a.budget, do_prepare=True, force_lane=False,
                           stop_before_render=True)
    log(f"=== KET THUC: {'OK' if ok else 'FAIL'} ===")
    print(f"\n=== TONG PHAN CHU: {(time.perf_counter()-T0)/60:.1f} phut ===")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
