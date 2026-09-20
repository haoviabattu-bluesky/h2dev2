# -*- coding: utf-8 -*-
"""banner_text.py — phủ TÊN KÊNH lên ảnh nền banner YouTube, đặt đúng VÙNG AN TOÀN.

Vì sao cần file riêng (không dùng thumbnail_text.py): banner YouTube hiển thị KHÁC NHAU theo thiết
bị — TV thấy cả khung 2560×1440, máy tính chỉ thấy dải giữa 2560×423, điện thoại chỉ thấy ô giữa
**1546×423**. Chữ đặt ngoài ô 1546×423 là điện thoại KHÔNG THẤY, mà phần lớn người xem dùng điện
thoại. Đây là lỗi im lặng: trên máy mình nhìn vẫn đẹp.

Và như mọi chỗ khác trong dự án: chữ Nhật/Hàn **vẽ bằng PIL**, không nhờ model sinh ảnh render.

  py -3.13 banner_text.py --bg banner_bg.png --name "深夜の資料室" --sub "宇宙・都市伝説・未解決"
                          --out banner_final.png
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

def _ensure_std():
    """xem publish_kit.py._ensure_std — bẫy sys.stdout=None trong .exe --windowed.

    Gọi `sys.stdout.reconfigure()` thẳng ở CẤP MODULE là AttributeError câm lúc import khi đóng
    exe dạng --windowed (skill tao_tool_exe.md #30-35). Dùng chung một khuôn với các file khác.
    """
    import os
    for name in ("stdout", "stderr"):
        st = getattr(sys, name, None)
        if st is None:
            setattr(sys, name, open(os.devnull, "w", encoding="utf-8", errors="replace"))
            continue
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_ensure_std()

W, H = 2560, 1440
AN_TOAN_W, AN_TOAN_H = 1546, 423          # ô mọi thiết bị đều thấy, nằm giữa khung
FONTS = ("C:/Windows/Fonts/YuGothB.ttc", "C:/Windows/Fonts/meiryo.ttc",
         "C:/Windows/Fonts/msgothic.ttc")


def _font(co):
    for f in FONTS:
        if Path(f).exists():
            return ImageFont.truetype(f, co)
    raise SystemExit("Không có font Nhật (YuGoth/meiryo/msgothic).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bg", required=True)
    ap.add_argument("--name", required=True, help="tên kênh")
    ap.add_argument("--sub", default="", help="dòng phụ nhỏ dưới tên")
    ap.add_argument("--out", required=True)
    ap.add_argument("--side", default="center", choices=["center", "left"])
    ap.add_argument("--guide", action="store_true", help="vẽ khung vùng an toàn để soi (bản nháp)")
    a = ap.parse_args()

    img = Image.open(a.bg).convert("RGB")
    scale = max(W / img.width, H / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    img = img.crop(((img.width - W) // 2, (img.height - H) // 2,
                    (img.width - W) // 2 + W, (img.height - H) // 2 + H))

    x0, y0 = (W - AN_TOAN_W) // 2, (H - AN_TOAN_H) // 2
    # Làm tối nhẹ RIÊNG vùng chữ để tên nổi mà nền vẫn giữ chi tiết ở hai bên.
    # Mask phải ĐẬM Ở GIỮA, NHẠT DẦN RA MÉP thì blur mới có tác dụng. Mask tô đều một giá trị rồi
    # blur là không đổi gì (làm mờ ảnh phẳng vẫn ra ảnh phẳng) → mép dải tối thành đường vuông sắc
    # lẹm, nhìn như dán một hộp đen lên banner. Đã dính thật ở bản đầu.
    dem = 170                                   # rìa mềm rộng bao nhiêu px
    vung = img.crop((x0 - dem, y0 - dem, x0 + AN_TOAN_W + dem, y0 + AN_TOAN_H + dem))
    toi = Image.new("RGB", vung.size, (0, 0, 0))
    mask = Image.new("L", vung.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [dem, dem, vung.size[0] - dem, vung.size[1] - dem], radius=90, fill=165)
    mask = mask.filter(ImageFilter.GaussianBlur(dem * 0.55))
    img.paste(Image.composite(toi, vung, mask), (x0 - dem, y0 - dem))

    d = ImageDraw.Draw(img)
    co = 190
    f = _font(co)
    while d.textlength(a.name, font=f) > AN_TOAN_W * 0.86 and co > 60:
        co -= 6
        f = _font(co)
    cx = x0 + AN_TOAN_W // 2 if a.side == "center" else x0 + int(AN_TOAN_W * 0.30)
    cy = y0 + AN_TOAN_H // 2 - (int(co * 0.42) if a.sub else 0)
    for dx, dy in ((5, 6),):                       # bóng đổ
        d.text((cx + dx, cy + dy), a.name, font=f, fill=(0, 0, 0), anchor="mm")
    d.text((cx, cy), a.name, font=f, fill=(255, 255, 255), anchor="mm",
           stroke_width=max(3, co // 22), stroke_fill=(12, 12, 20))

    if a.sub:
        cos = max(34, int(co * 0.30))
        fs = _font(cos)
        sub = "　".join(a.sub)                      # giãn chữ cho ra dáng dòng phụ
        while d.textlength(sub, font=fs) > AN_TOAN_W * 0.9 and cos > 22:
            cos -= 2
            fs = _font(cos)
        d.text((cx, cy + int(co * 0.78)), sub, font=fs, fill=(214, 200, 255), anchor="mm",
               stroke_width=2, stroke_fill=(10, 10, 18))

    if a.guide:
        d.rectangle([x0, y0, x0 + AN_TOAN_W, y0 + AN_TOAN_H], outline=(255, 60, 60), width=5)
        d.rectangle([0, y0, W, y0 + AN_TOAN_H], outline=(60, 160, 255), width=4)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    img.save(a.out, quality=95)
    print(f"✓ Banner: {a.out} ({W}x{H}, tên {co}px, vùng an toàn {AN_TOAN_W}x{AN_TOAN_H})")


if __name__ == "__main__":
    main()
