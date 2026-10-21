#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""chay_hang_doi.py — HÀNG ĐỢI nhiều lane trong 1 lệnh. Mỗi lane = 1 lô chay_lo_tap.py (tập trong lane chạy
TUẦN TỰ, mỗi tập 1 `claude -p` sạch); các lane chạy SONG SONG tối đa --song-song lô (anh duyệt 21/10, bước 1).

Song song chỉ nhanh hơn theo giờ đồng hồ, KHÔNG giảm quota (tốn y như chạy lần lượt) và chạm trần 5 giờ của gói
Max sớm hơn → mặc định 2, tối đa 3. Chặng hook vẫn tự xếp hàng ở khoá Ultra/Grok (khoa_ultra.py, grok_da_luong.lock).

Dùng:
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\chay_hang_doi.py --hang "teinengo-fuufu:8-10 teinengo-anaba:13-15" --dry
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\tools\chay_hang_doi.py --hang "teinengo-fuufu:8-10 shakai_no_naze:22" --song-song 1
  --hang "<mã>:<từ>-<đến> <mã>:<stt> ..."   mã = id profile (bảng router CLAUDE.md); mỗi lane chỉ 1 lần
  --chi-chang/--model/--timeout-phut/--tran-usd/--tiep-khi-loi/--ghi-chu   chuyển nguyên cho chay_lo_tap.py
Kết quả: E:\CLAUDE\YOUTUBE\h2dev\logs\chay_lo_tap\TONG_KET_HANG_<giờ>.txt (gộp TONG_KET từng lane), in ở dòng cuối.
"""
import argparse
import datetime as _dt
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))

import profiles  # noqa: E402

LO = ROOT / "tools" / "chay_lo_tap.py"
LOG_DIR = ROOT / "logs" / "chay_lo_tap"
GIAN_CACH_S = 20          # lane sau mở chậm 20s: tránh 2 lô đọc/ghi sheet cùng một lúc


def doc_hang(s):
    """'a:8-10 b:5' → [('a', 8, 10), ('b', 5, 5)]; sai cú pháp / lane lặp / profile không có → SystemExit."""
    out, da = [], set()
    for muc in s.replace(",", " ").split():
        ma, _, khoang = muc.partition(":")
        tu, _, den = khoang.partition("-")
        if not (ma and tu.isdigit() and (not den or den.isdigit())):
            raise SystemExit(f"--hang sai cú pháp ở '{muc}' (đúng: <mã>:<từ>-<đến>)")
        if ma in da:
            raise SystemExit(f"lane {ma} xuất hiện 2 lần trong --hang (gộp thành 1 khoảng)")
        profiles.load(ma)                      # profile sai tên → lỗi ngay, trước khi mở lô nào
        da.add(ma)
        out.append((ma, int(tu), int(den or tu)))
    if not out:
        raise SystemExit("--hang trống")
    return out


def lenh_lo(ma, tu, den, a, dry):
    cmd = [sys.executable, "-X", "utf8", str(LO), "--profile", ma, "--tu", str(tu), "--den", str(den),
           "--model", a.model, "--timeout-phut", str(a.timeout_phut), "--tran-usd", str(a.tran_usd)]
    if a.chi_chang:
        cmd += ["--chi-chang", a.chi_chang]
    if a.tiep_khi_loi:
        cmd.append("--tiep-khi-loi")
    if a.ghi_chu:
        cmd += ["--ghi-chu", a.ghi_chu]
    if dry:
        cmd.append("--dry")
    return cmd


def chay_lane(ma, tu, den, a, gio, cho_s):
    time.sleep(cho_s)
    out = LOG_DIR / f"HANG_{gio}_{ma}.out"
    print(f"[{_dt.datetime.now():%H:%M}] mở lô {ma} STT {tu}→{den} · log {out}", flush=True)
    with open(out, "w", encoding="utf-8") as f:
        rc = subprocess.run(lenh_lo(ma, tu, den, a, False), cwd=str(ROOT), stdout=f, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace").returncode
    dong = out.read_text(encoding="utf-8", errors="replace").splitlines()
    tk = next((Path(d.split(":", 1)[1].strip()) for d in reversed(dong) if d.startswith("Tổng kết:")), None)
    noi_dung = tk.read_text(encoding="utf-8") if tk and tk.exists() else "\n".join(dong[-15:])
    print(f"[{_dt.datetime.now():%H:%M}] xong lô {ma} (mã thoát {rc}) · {tk or out}", flush=True)
    return f"===== {ma} STT {tu}→{den} · mã thoát {rc} · {tk or out}\n{noi_dung.rstrip()}\n"


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hang", required=True, help='"<mã>:<từ>-<đến> <mã>:<stt> ..."')
    ap.add_argument("--song-song", type=int, default=2, help="số lane chạy cùng lúc (mặc định 2, tối đa 3)")
    ap.add_argument("--chi-chang", choices=["kichban", "hook", "giao2"])
    ap.add_argument("--model", default="opus")
    ap.add_argument("--timeout-phut", type=int, default=240)
    ap.add_argument("--tran-usd", type=float, default=9.0)
    ap.add_argument("--tiep-khi-loi", action="store_true")
    ap.add_argument("--ghi-chu", default="")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args(argv)
    if not 1 <= a.song_song <= 3:
        raise SystemExit("--song-song chỉ 1–3 (song song không giảm quota, chỉ chạm trần 5 giờ sớm hơn)")

    hang = doc_hang(a.hang)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if a.dry:                                  # dry: in kế hoạch từng lane lần lượt, không gọi claude
        for ma, tu, den in hang:
            subprocess.run(lenh_lo(ma, tu, den, a, True), cwd=str(ROOT))
        print(f"→ bản thật: {len(hang)} lane, chạy {min(a.song_song, len(hang))} lane cùng lúc")
        return

    gio = _dt.datetime.now().strftime("%m%d_%H%M")
    print(f"HÀNG ĐỢI {gio}: {len(hang)} lane · song song {a.song_song} · model {a.model}", flush=True)
    with ThreadPoolExecutor(max_workers=a.song_song) as ex:
        kq = list(ex.map(lambda x: chay_lane(*x[1], a, gio, GIAN_CACH_S * min(x[0], a.song_song - 1)),
                         enumerate(hang)))
    bao = LOG_DIR / f"TONG_KET_HANG_{gio}.txt"
    bao.write_text(f"HÀNG ĐỢI {gio} · {a.hang} · song song {a.song_song}\n\n" + "\n".join(kq), encoding="utf-8")
    print(f"Tổng kết: {bao}")


if __name__ == "__main__":
    main()
