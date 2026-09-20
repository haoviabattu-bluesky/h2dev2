# -*- coding: utf-8 -*-
"""colorize_real_photo.py — CLI tô màu 1 ảnh B&W THẬT (Lane D) qua gpti2_edit.edit_from_paths().

`gpti2_edit.py` vốn chỉ là thư viện (không có CLI) — file này là lớp mỏng bọc CLI cho B5 thủ công
của SOP_LANE_D.md. Giữ nguyên 100% bố cục/chi tiết ảnh gốc, chỉ ước lượng màu tự nhiên.

Dùng:
  py -3.13 colorize_real_photo.py --in _src_photos/main01.jpg --out img/000.png
  py -3.13 colorize_real_photo.py --in a.jpg --out b.png --quality medium --era "1945, Pacific War"
"""
import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import gpti2_edit

PROMPT_TMPL = (
    "Colorize this black-and-white historical WWII photograph ({era}). Keep the composition, camera "
    "framing, every person's exact pose, position and count, every object, background and setting "
    "completely unchanged pixel-for-pixel in layout -- do not add, remove, move, crop, or redraw "
    "anything, do not invent new people or objects. Only estimate and apply natural, historically "
    "plausible color: skin tones, uniform colors period-appropriate for the branch/nationality shown, "
    "sky, terrain, foliage, water, metal and fabric tones. Preserve the original photographic grain, "
    "contrast and softness -- do not sharpen, do not smooth skin, do not apply cinematic color "
    "grading, no vignette, no stylization. The result should look like a real color photograph taken "
    "at the time, not a painting."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--quality", default="medium", choices=["low", "medium", "high"],
                    help="medium = mặc định đã verify (xem lane-d-colorize-test)")
    ap.add_argument("--era", default="1945, Pacific War", help="bối cảnh thời gian/địa lý cho prompt")
    ap.add_argument("--orientation", default="", help="landscape/portrait (mặc định tự đoán theo ảnh)")
    a = ap.parse_args()

    src = Path(a.inp)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not a.orientation:
        from PIL import Image
        with Image.open(src) as im:
            a.orientation = "landscape" if im.width >= im.height else "portrait"

    prompt = PROMPT_TMPL.format(era=a.era)
    print(f"[colorize] {src.name} -> {out.name} (quality={a.quality}, {a.orientation}) …")
    png = gpti2_edit.edit_from_paths(prompt, [str(src)], orientation=a.orientation, quality=a.quality)
    out.write_bytes(png)
    price = gpti2_edit.estimate_price_vnd(orientation=a.orientation, quality=a.quality, n_sources=1)
    print(f"✓ {out} (~{price}đ)")


if __name__ == "__main__":
    main()
