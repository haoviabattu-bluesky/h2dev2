"""search_side_width.py — dò side-width LỚN NHẤT còn qua được hard gate chống-đè-mặt của
thumbnail_text.py (xem face_box.py + face.json + gate trong main()). Thay cho việc tự tay chạy
từng --side-width một rồi so bằng mắt/crop pixel: quét từ hi xuống lo, DỪNG NGAY ở giá trị PASS
đầu tiên (đó chính là giá trị lớn nhất còn hợp lệ) — không tự chọn giá trị FAIL vì "lấn ít", không
tự sửa zone/pad, không bỏ qua exit code của thumbnail_text.py.

CLI:
  py -3.13 search_side_width.py <thư_mục_tập> [--lo 0.40] [--hi 0.95] [--step 0.02]

Yêu cầu thư mục có sẵn: bg_001.png (hoặc bg_*.png) + thumb_text.txt + face.json cùng chỗ với bg
(chạy face_box.py trước — thumbnail_text.py tự chặn nếu thiếu, script này không che giấu lỗi đó).
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PIPELINE_DIR = Path(__file__).resolve().parent
THUMBNAIL_TEXT = PIPELINE_DIR / "thumbnail_text.py"

# Bộ tham số CHUẨN của lane satori — ĐÚNG bộ đã dùng để tạo cand_0.90 tập 7 (đã verify chạy lại
# tay: --side left --subject-side right --fit-each --max-size 200, KHÔNG --fit-height vì face.json
# của tập này cũng được face_box.py tính KHÔNG --fit-height — hai bên phải cùng hệ toạ độ).
# side-width là biến DUY NHẤT bị dò ở đây; không tự đổi các flag còn lại.
FIXED_ARGS = ["--side", "left", "--subject-side", "right", "--fit-each", "--max-size", "200"]

RE_OVERLAP = re.compile(
    r"FACE OVERLAP \| dòng=(\S+) \| bbox=\([^)]*\) \| zone=\([^)]*\) \| side-width=\S+ \| lấn (\d+)px"
)
RE_PASS = re.compile(r"FACE GATE PASS \| side-width=\S+ \| khe hẹp nhất=(-?\d+)px")


def find_bg(folder: Path) -> Path:
    cand = folder / "bg_001.png"
    if cand.exists():
        return cand
    matches = sorted(folder.glob("bg_*.png"))
    if not matches:
        print(f"LỖI: không tìm thấy ảnh nền bg_*.png trong {folder}")
        sys.exit(1)
    return matches[0]


def find_text(folder: Path) -> Path:
    cand = folder / "thumb_text.txt"
    if not cand.exists():
        print(f"LỖI: không tìm thấy {cand}")
        sys.exit(1)
    return cand


def run_one(bg: Path, text: Path, out: Path, side_width: float):
    cmd = ([sys.executable, str(THUMBNAIL_TEXT), "--bg", str(bg), "--text", str(text),
            "--out", str(out), "--side-width", f"{side_width:.2f}"] + FIXED_ARGS)
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return proc.returncode, (proc.stdout or "") + "\n" + (proc.stderr or "")


def parse_output(text_out: str):
    """Trả về (nhãn dòng nặng nhất, lấn px, khe hẹp nhất px) — 2 trong 3 luôn None tuỳ PASS/FAIL."""
    overlaps = RE_OVERLAP.findall(text_out)
    if overlaps:
        worst_label, worst_lan = max(overlaps, key=lambda t: int(t[1]))
        return worst_label, int(worst_lan), None
    m = RE_PASS.search(text_out)
    if m:
        return None, None, int(m.group(1))
    return None, None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="thư mục tập (chứa bg_*.png + thumb_text.txt + face.json)")
    ap.add_argument("--lo", type=float, default=0.40)
    ap.add_argument("--hi", type=float, default=0.95)
    ap.add_argument("--step", type=float, default=0.02)
    args = ap.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        print(f"LỖI: không phải thư mục: {folder}")
        sys.exit(1)

    bg = find_bg(folder)
    text = find_text(folder)

    n_steps = int(round((args.hi - args.lo) / args.step))
    values = [round(args.hi - i * args.step, 2) for i in range(n_steps + 1) if args.hi - i * args.step >= args.lo - 1e-9]

    rows = []       # (side_width, "PASS"/"FAIL", nhãn, lấn, khe_hep_nhat)
    chosen = None
    for v in values:
        out = folder / f"cand_{v:.2f}.png"
        rc, out_text = run_one(bg, text, out, v)
        label, lan, gap = parse_output(out_text)
        if rc == 0:
            rows.append((v, "PASS", "-", "-", gap if gap is not None else "?"))
            chosen = (v, out)
            break
        else:
            rows.append((v, "FAIL", label or "?", lan if lan is not None else "?", "-"))

    col = "{:<11} | {:<7} | {:<22} | {:<9} | {:<18}"
    print(col.format("side-width", "kết quả", "dòng vi phạm nặng nhất", "lấn (px)", "khe hẹp nhất (px)"))
    print("-" * 80)
    for v, res, label, lan, gap in rows:
        print(col.format(f"{v:.2f}", res, str(label), str(lan), str(gap)))

    if chosen is None:
        print("KHÔNG CÓ GIÁ TRỊ HỢP LỆ")
        sys.exit(1)

    v, out = chosen
    print(f"CHỌN side-width={v:.2f}  ->  {out}")


if __name__ == "__main__":
    main()
