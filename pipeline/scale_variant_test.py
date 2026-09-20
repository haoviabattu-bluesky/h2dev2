"""scale_variant_test.py — thử NHIỀU BỘ cỡ chữ cho layout 4 dòng (WHITE/YELLOW/RED cố định trần +
scale, BANNER giữ nguyên logic thumbnail_text.py) để chọn bằng mắt. KHÔNG khoá gì, KHÔNG đụng
production/golden. Dùng lại draw_line()/hard-gate-check style của thumbnail_text.py cho DÒNG 1+2
(DÒNG 2 = YELLOW là mốc — cỡ gốc = cỡ lớn nhất để nó vừa trần zone.x-margin); DÒNG 3 (RED) được
phép đè vai/áo nên trần rộng hơn (0.88*W-margin) và MIỄN gate; BANNER luôn miễn gate.

Dùng:
  py -3.13 scale_variant_test.py <thư_mục_tập> [--max-size 200]
Yêu cầu thư mục có: bg_001.png (hoặc bg_*.png), thumb_text.txt (đúng 3 dòng main + 1 BANNER),
face.json (chạy face_box.py trước).
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thumbnail_text import (  # noqa: E402
    load_bg, parse_text, fit_font, fit_banner_font, draw_line, _ink_bbox_raster,
    _TEXT_BBOXES, FONT_BOLD, FONT_BANNER, BANNER_BG, LINE_LEAD, W, H,
)

sys.stdout.reconfigure(encoding="utf-8")

VARIANTS = [
    ("A", 0.55, 0.65),
    ("B", 0.62, 0.72),
    ("C", 0.70, 0.80),
    ("D", 0.55, 0.80),
    ("E", 0.70, 0.65),
]


def find_bg(folder: Path) -> Path:
    cand = folder / "bg_001.png"
    if cand.exists():
        return cand
    matches = sorted(folder.glob("bg_*.png"))
    if not matches:
        print(f"LỖI: không tìm thấy ảnh nền bg_*.png trong {folder}")
        sys.exit(1)
    return matches[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="thư mục tập (chứa bg_*.png + thumb_text.txt + face.json)")
    ap.add_argument("--max-size", type=int, default=200)
    args = ap.parse_args()

    folder = Path(args.folder)
    bg_path = find_bg(folder)
    text_path = folder / "thumb_text.txt"
    face_json_path = folder / "face.json"
    if not text_path.exists():
        print(f"LỖI: không tìm thấy {text_path}")
        sys.exit(1)
    if not face_json_path.exists():
        print(f"LỖI: THIẾU face.json, chạy face_box.py trước ({face_json_path})")
        sys.exit(1)

    face_data = json.loads(face_json_path.read_text(encoding="utf-8"))
    if "zone" not in face_data:
        print(f"LỖI: face.json thiếu khoá 'zone', chạy lại face_box.py")
        sys.exit(1)
    zone = face_data["zone"]
    zx, zy, zw, zh = zone["x"], zone["y"], zone["w"], zone["h"]
    zx0, zy0, zx1, zy1 = zx, zy, zx + zw, zy + zh

    lines, banner = parse_text(str(text_path))
    if len(lines) != 3:
        print(f"LỖI: cần đúng 3 dòng main (WHITE/YELLOW/RED) trong {text_path}, có {len(lines)}")
        sys.exit(1)
    (c1, t1, _), (c2, t2, _), (c3, t3, _) = lines

    out_dir = folder / "test_scale"
    out_dir.mkdir(parents=True, exist_ok=True)

    base_img = load_bg(str(bg_path), "left", keep_sharp=0.64, fit_height=False,
                       subject_side="right", photo_scale=1.0, flat=False)
    measure_draw = ImageDraw.Draw(base_img.copy())

    margin = int(W * 0.045)
    top_y = int(H * 0.035)
    cx, ax = margin, "l"

    cap12 = max(1, zx - margin)                     # DÒNG 1 & 2 — trần = zone.x - margin
    cap3 = max(1, int(0.88 * W) - margin)            # DÒNG 3 — trần rộng hơn, được đè vai/áo

    bfont = bh = by0 = None
    if banner:
        box_w = (W - 2 * margin) - 48
        bsize = fit_banner_font(measure_draw, banner, box_w, max_size=110)
        bfont = ImageFont.truetype(FONT_BANNER, bsize)
        _, bbox_top, _, bbox_bot = _ink_bbox_raster(bfont, banner)
        bh = int((bbox_bot - bbox_top) + 40)
        by0 = H - bh - int(H * 0.03)
    gap = int(H * 0.02)
    max_h = (by0 - gap - top_y) if banner else (int(H * 0.9) - top_y)

    # cỡ gốc = cỡ LỚN NHẤT để DÒNG 2 (YELLOW, mốc) vừa trần cap12
    base_size = fit_font(measure_draw, [(c2, t2, 1.0)], cap12, None, args.max_size)

    report = []
    for name, s1, s3 in VARIANTS:
        sz1 = max(20, int(base_size * s1))
        sz2 = base_size
        sz3 = max(20, int(base_size * s3))
        f1 = ImageFont.truetype(FONT_BOLD, sz1)
        f2 = ImageFont.truetype(FONT_BOLD, sz2)
        f3 = ImageFont.truetype(FONT_BOLD, sz3)
        lh1, lh2, lh3 = int(sz1 * LINE_LEAD), int(sz2 * LINE_LEAD), int(sz3 * LINE_LEAD)

        img = base_img.copy()
        draw = ImageDraw.Draw(img)
        _TEXT_BBOXES.clear()
        y = top_y
        draw_line(draw, cx, y, t1, f1, c1, ax); y += lh1
        draw_line(draw, cx, y, t2, f2, c2, ax); y += lh2
        draw_line(draw, cx, y, t3, f3, c3, ax); y += lh3

        # Gate CHỈ áp cho DÒNG 1 + DÒNG 2 (2 bbox đầu trong _TEXT_BBOXES) — DÒNG 3 & BANNER MIỄN.
        violations = []
        for label, l, t, r, b in _TEXT_BBOXES[:2]:
            ox0, ox1 = max(l, zx0), min(r, zx1)
            oy0, oy1 = max(t, zy0), min(b, zy1)
            if ox1 > ox0 and oy1 > oy0:
                violations.append((label, ox1 - ox0))

        out_path = out_dir / f"scale_{name}.png"
        if violations:
            result = "FAIL"
            file_str = "-- (vi phạm gate, KHÔNG lưu) --"
            detail = "; ".join(f"{lb} lấn {lan}px" for lb, lan in violations)
            print(f"BỘ {name} | s1={s1} s3={s3} | size=({sz1}/{sz2}/{sz3}) | FAIL: {detail}")
        else:
            if banner:
                draw.rounded_rectangle([margin - 6, by0, W - margin + 6, by0 + bh], radius=14,
                                       fill=BANNER_BG, outline=(255, 255, 255), width=4)
                draw.text((W // 2, by0 + bh // 2), banner, font=bfont, fill=(255, 255, 255),
                          anchor="mm", stroke_width=2, stroke_fill=(90, 0, 0))
            img.save(out_path, quality=95)
            result = "PASS"
            file_str = str(out_path)
            overflow = " (⚠ tràn max_h)" if (y > max_h + top_y) else ""
            print(f"BỘ {name} | s1={s1} s3={s3} | size=({sz1}/{sz2}/{sz3}) | PASS{overflow} | {file_str}")

        report.append((name, s1, s3, sz1, sz2, sz3, result, file_str))

    print()
    header = "{:<4} | {:<5} | {:<5} | {:<18} | {:<6} | {}".format(
        "bộ", "s1", "s3", "size D1/D2/D3", "gate", "file")
    print(header)
    print("-" * len(header))
    for name, s1, s3, sz1, sz2, sz3, result, file_str in report:
        print("{:<4} | {:<5} | {:<5} | {:<18} | {:<6} | {}".format(
            name, s1, s3, f"{sz1}/{sz2}/{sz3}", result, file_str))

    print(f"\nThư mục ảnh: {out_dir}")


if __name__ == "__main__":
    main()
