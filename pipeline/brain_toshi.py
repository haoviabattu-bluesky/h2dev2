# -*- coding: utf-8 -*-
"""brain_toshi.py — orchestrator NÃO CLAUDE cho Lane A (toshi-densetsu-jp), THỬ NGHIỆM 2026-09-17.

TÁCH HẲN khỏi brain_channel.py của Satori (memory `hai-tool-exe-tach-han` — cấm gộp 2 nhánh não).
Viết `script_claude.txt` (KHÔNG đè `script.txt` gốc não-ramcloud) để so sánh trực tiếp.

Vòng lặp mô phỏng đúng cơ chế đã verify của brain_channel.py (Satori) — không phát minh cách mới:
  1. `claude -p` viết outline → tự kiểm → viết script_claude.txt → tự soát 1 lượt (brain_toshi_steps).
  2. Orchestrator (NGOÀI Claude) chạy qc_numbers.py + qc_script.py (B3Q) để XÁC MINH — không tin lời
     bộ não tự khai (bài học `cong-qc-tu-khai-khong-do`).
  3. B3Q chưa đạt → spawn `claude -p` LẦN NỮA kèm đúng danh sách lỗi, sửa tại chỗ. Có CHỐT KHÔNG-
     HỘI-TỤ (dừng nếu số lỗi không giảm giữa 2 lượt — bài học `cong-llm-phai-dat-duoc`).
  4. B3Q đạt → chạy qc_facts.py (B3F). Trượt → DỪNG HẲN, KHÔNG tự lặp (đúng luật cũ Lane A
     `b3f-khong-duoc-noi-vao-vong-viet-lai`) — báo lỗi, cần người sửa series_ctx.txt.

    py -3.13 brain_toshi.py --slug ep08-fatima-akita --profile toshi-densetsu-jp [--minutes 31.5]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import profiles
import qc_facts
import qc_numbers

import brain_toshi_steps as bts

VONG_SUA_B3Q = 3
OUT_NAME = "script_claude.txt"


def _slug_dir(slug):
    p = Path(slug)
    if p.is_absolute():
        return p
    return HERE.parent / "assets" / "toshi-densetsu-jp" / slug


def check_numbers(d, out_name=OUT_NAME):
    sf = d / out_name
    hits = qc_numbers.arithmetic(sf.read_text(encoding="utf-8"))
    cao = [h for h in hits if h["sev"] == "cao"]
    if not hits:
        print("✓ qc_numbers: không thấy lỗi số học tất định nào")
    else:
        for h in hits:
            print(f"  [{h['sev']}] {h['kind']}: {h['msg']}")
    return not cao, [f"[{h['sev']}] {h['kind']}: {h['msg']}" for h in cao]


def check_b3q(prof, d, out_name=OUT_NAME):
    """Chạy `qc_script.py` qua subprocess (KHÔNG import trực tiếp) — cùng cách brain_channel.py
    (Satori) đã verify: chạy như CLI thật rồi bóc lỗi từ output in ra, tránh đoán sai cấu trúc dict
    trả về nội bộ của qc_script.run() khi hàm đó đổi theo thời gian."""
    sf, cf = d / out_name, d / "competitor.txt"
    cmd = [sys.executable, str(HERE / "qc_script.py"), "--profile", prof["id"], "--script", str(sf)]
    if cf.exists():
        cmd += ["--competitor", str(cf)]
    p = subprocess.run(cmd, cwd=str(HERE), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print(p.stdout)
    if p.stderr:
        print(p.stderr, file=sys.stderr)
    lines = p.stdout.splitlines()
    loi = [l.strip() for l in lines if l.strip().startswith("✗")]
    loi += [l.strip() for l in lines
            if re.match(r"^\[(cao|vua|thap|trung_binh)\]", l.strip()) and l.strip() not in loi]
    dat = p.returncode == 0
    if not loi and not dat:
        loi = ["qc_script.py thoát mã lỗi nhưng không liệt kê dòng ✗/[sev] cụ thể — xem log phía trên"]
    return dat, loi


def check_b3f(d, out_name=OUT_NAME):
    sf = d / out_name
    df = d / "series_ctx.txt"
    kq = qc_facts.kiem(sf.read_text(encoding="utf-8"), df.read_text(encoding="utf-8"))
    qc_facts.bao_cao(kq)
    return not kq["nang"], kq["nang"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--profile", default="toshi-densetsu-jp")
    ap.add_argument("--minutes", type=float, default=0.0)
    ap.add_argument("--out-name", default=OUT_NAME)
    args = ap.parse_args()

    d = _slug_dir(args.slug)
    if not d.exists():
        raise SystemExit(f"✗ Không thấy thư mục tập: {d}")
    prof = profiles.load(args.profile)
    minutes = args.minutes or float((prof.get("script", {}) or {}).get("target_minutes") or 30)

    print(f"=== NÃO CLAUDE (Lane A, thử nghiệm) · {d.name} · {minutes}' ===")
    ok, last = bts.run_creative(d, args.profile, minutes, out_name=args.out_name)
    if not ok:
        raise SystemExit(f"✗ NHỊP A/A.5/B/B.5 thất bại: {last}")

    dat_num, loi_num = check_numbers(d, args.out_name)
    if not dat_num:
        print("⚠️ Còn lỗi số học mức [cao] — cần xem tay, script vẫn tiếp tục qua B3Q "
              "(qc_numbers không tự lặp, đây là cổng máy tất định, không cần Claude sửa hộ).")

    dat_b3q, loi_b3q = check_b3q(prof, d, args.out_name)
    for luot in range(1, VONG_SUA_B3Q + 1):
        if dat_b3q:
            break
        truoc = len(loi_b3q)
        print(f"\n⟳ B3Q chưa đạt ({truoc} vấn đề) → sửa TẠI CHỖ [lượt {luot}/{VONG_SUA_B3Q}]")
        ok, last = bts.run_creative(
            d, args.profile, minutes, out_name=args.out_name,
            extra_prompt=(
                f"\n\n⛔ VIỆC DUY NHẤT LƯỢT NÀY: `{args.out_name}` RỚT CỔNG NỘI DUNG B3Q. Giữ nguyên "
                f"outline/cốt truyện và mọi mốc dữ kiện đã có; CHỈ sửa đúng những chỗ bị nêu dưới đây, "
                f"đừng viết lại cả bài (viết lại là lệch số học, phải nắn lại từ đầu):\n   - "
                + "\n   - ".join(loi_b3q[:15])
                + f"\nSửa xong in `BRAIN_TOSHI_DONE` rồi dừng."))
        if not ok:
            print(f"✗ Lượt sửa {luot} thất bại: {last}")
            break
        dat_b3q, loi_b3q = check_b3q(prof, d, args.out_name)
        if not dat_b3q and len(loi_b3q) >= truoc:
            print(f"⏹ số lỗi KHÔNG GIẢM ({truoc} → {len(loi_b3q)}) — dừng sửa tự động, cần sửa tay.")
            break

    if not dat_b3q:
        print(f"\n✗ B3Q vẫn chưa đạt sau {VONG_SUA_B3Q} lượt — DỪNG, không chạy B3F.")
        return 1

    dat_b3f, loi_b3f = check_b3f(d, args.out_name)
    if not dat_b3f:
        print(f"\n⛔ B3F TRƯỢT ({len(loi_b3f)} lỗi nặng) — DỪNG HẲN theo luật cũ Lane A. "
              f"KHÔNG tự viết lại script — chi tiết sai nằm ở TƯ LIỆU (series_ctx.txt) hoặc script bịa "
              f"thêm ngoài tư liệu. Sửa series_ctx.txt (nếu tư liệu thiếu) rồi chạy lại tool này, "
              f"hoặc sửa tay script_claude.txt cho khớp đúng tư liệu đã có.")
        return 1

    print(f"\n✓ HOÀN TẤT — {d / args.out_name} đạt B3Q + B3F. So sánh với script.txt gốc (não ramcloud) "
          f"để quyết định có chuyển hẳn hay không.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
