"""Kiểm 1 kịch bản có đúng CÔNG THỨC WIN của lane không (đo vị trí theo % số chữ).

Cấu hình đọc từ profile `script.cong_thuc_win` (lane nào không khai = bỏ qua, không đoán).
Máy chỉ đo được phần có dấu hiệu chữ (mốc, câu đầu, con số đầu bài); phần ý nghĩa
(người cùng tuổi chọn ngược, kết còn mất mát thật…) in ra thành danh sách "kiểm bằng mắt".

    py -3.13 -X utf8 E:\\CLAUDE\\YOUTUBE\\h2dev\\pipeline\\kiem_cong_thuc_win.py --profile teinengo-anaba --slug ep12-keibi-tatteru
    py -3.13 -X utf8 E:\\CLAUDE\\YOUTUBE\\h2dev\\pipeline\\kiem_cong_thuc_win.py --profile teinengo-anaba --script <đường dẫn script.txt>

Mã thoát: 0 = đạt hết mốc máy đo · 1 = có mốc CHƯA đạt · 2 = lỗi cấu hình/thiếu file.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def tach_cau(text):
    """Câu = cắt theo 。！？ và xuống dòng; câu thoại 「…」 tính là 1 câu."""
    out, buf, sau = [], "", 0
    for ch in text:
        buf += ch
        if ch == "「":
            sau += 1
        elif ch == "」":
            sau = max(0, sau - 1)
            if sau == 0:
                out.append(buf)
                buf = ""
        elif sau == 0 and ch in "。！？\n":
            out.append(buf)
            buf = ""
    out.append(buf)
    return [c.strip() for c in out if c.strip()]


def kiem(cfg, text):
    n = len(text)
    kq = []  # (ten, dat, gia_tri, sua)

    cau = tach_cau(text)
    if cfg.get("cau_dau_thoai"):
        dau = cau[0] if cau else ""
        kq.append(("Câu đầu = thoại của người có quyền", dau.startswith("「"),
                   dau[:40], cfg.get("sua_cau_dau", "")))
    so_n = cfg.get("so_trong_n_cau")
    if so_n:
        doan = "".join(cau[:so_n])
        co_so = bool(re.search(r"[0-9０-９]|[一二三四五六七八九十百千万]+(日|円|年|か月|ヶ月|人|時間|回|割)", doan))
        kq.append((f"Con số bị mất trong {so_n} câu đầu", co_so, doan[:60],
                   cfg.get("sua_so_dau", "")))
    for rx in cfg.get("cam_mo_dau", []):
        dau = "".join(cau[:3])
        kq.append(("Không mở bằng tóm tắt/nội tâm/an ủi", not re.search(rx, dau), dau[:40],
                   cfg.get("sua_cam_mo_dau", "")))

    for m in cfg.get("moc", []):
        vt = [round(x.start() * 100 / n, 1) for x in re.finditer(m["regex"], text)]
        if m.get("lan") == "cuoi":
            vt = vt[-1:]
        elif m.get("lan") != "moi":
            vt = vt[:1]
        dat = bool(vt) and all(m.get("tu", 0) <= v <= m.get("den", 100) for v in vt)
        gt = ", ".join(f"{v}%" for v in vt) or "KHÔNG THẤY"
        kq.append((f"{m['ten']} ({m.get('tu', 0)}–{m.get('den', 100)}%)", dat, gt, m.get("sua", "")))
    return kq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug")
    ap.add_argument("--script")
    a = ap.parse_args()

    prof = json.loads((ROOT / "profiles" / "profiles" / f"{a.profile}.json").read_text(encoding="utf-8"))
    cfg = prof.get("script", {}).get("cong_thuc_win")
    if not cfg:
        print(f"[kiem_cong_thuc_win] profile {a.profile} chưa khai script.cong_thuc_win — bỏ qua.")
        return 2
    if a.script:
        sp = Path(a.script)
    elif a.slug:
        sp = ROOT / prof["slug_dir"] / a.slug / "script.txt"
    else:
        print("Cần --slug hoặc --script")
        return 2
    if not sp.exists():
        print(f"Không thấy {sp}")
        return 2

    kq = kiem(cfg, sp.read_text(encoding="utf-8"))
    print(f"KIỂM CÔNG THỨC WIN — {sp}")
    print(f"Công thức: {ROOT / cfg['file']}\n")
    for ten, dat, gt, sua in kq:
        print(f"{'✅ ĐÚNG' if dat else '❌ CHƯA'} | {ten} | đo: {gt}")
        if not dat and sua:
            print(f"         → sửa: {sua}")
    print("\nKIỂM BẰNG MẮT (máy không đo được, đọc kịch bản rồi chấm):")
    for i, d in enumerate(cfg.get("kiem_bang_mat", []), 1):
        print(f"  [{i}] {d}")
    thieu = sum(1 for _, dat, _, _ in kq if not dat)
    print(f"\nKẾT LUẬN MÁY ĐO: {'ĐẠT' if not thieu else f'CHƯA ĐẠT — {thieu} mốc phải sửa trước khi giao máy 3/máy 2'}")
    return 1 if thieu else 0


if __name__ == "__main__":
    sys.exit(main())
