# -*- coding: utf-8 -*-
r"""thumb_hai_o.py — dựng thumbnail 1280x720 khuôn 2 ô TRƯỚC→SAU từ <tập>\thumb_v2\SPEC.json (18/10/2026, sửa CTR thấp).

Khuôn: băng đen trên (spec.top) · 2 ô ảnh dọc bg\001.png (trái) / bg\002.png (phải) + mũi tên đỏ ·
nhãn ở đáy mỗi ô (spec.trai / spec.phai) · bóng thoại ô trái (spec.bubble) · băng đỏ dưới (spec.bot).
Chữ overlay bằng PIL (model không render chữ Nhật). Ảnh nền vẽ trước bằng pipeline\img_9router.py.
    py -3.13 -X utf8 tools\thumb_hai_o.py <thư mục tập> [<thư mục tập> ...]   → <tập>\thumbnail_v2.png
"""
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = r"C:\Windows\Fonts\YuGothB.ttc"
W, H = 1280, 720
TOP, BOT = 110, 82
MAU = {"WHT": (255, 255, 255), "YEL": (255, 226, 0), "RED": (225, 25, 25), "BLK": (0, 0, 0),
       "BLU": (20, 90, 220), "GRN": (20, 150, 60)}
BLK, WHT, RED, YEL = MAU["BLK"], MAU["WHT"], MAU["RED"], MAU["YEL"]


def font(sz):
    return ImageFont.truetype(FONT, sz)


def dong_chu(d, cum, y, h, max_w, sz):
    """1 dòng nhiều màu, căn giữa, tự thu nhỏ cho vừa max_w."""
    while True:
        f = font(sz)
        w = sum(f.getlength(t) for t, _ in cum)
        if w <= max_w or sz <= 36:
            break
        sz -= 2
    x = (W - w) / 2
    for t, c in cum:
        d.text((x, y + h / 2), t, font=f, fill=MAU[c], anchor="lm", stroke_width=6, stroke_fill=BLK)
        x += f.getlength(t)


def nhan(d, x_tam, y, t, fg, bg, sz=50):
    f = font(sz)
    while f.getlength(t) > 580 and sz > 30:
        sz -= 2
        f = font(sz)
    w, pad = f.getlength(t), 14
    x0 = max(8, min(x_tam - w / 2 - pad, W - 8 - w - 2 * pad))
    d.rounded_rectangle((x0 + 5, y + 5, x0 + w + 2 * pad + 5, y + sz + 2 * pad + 5), radius=12, fill=BLK)
    d.rounded_rectangle((x0, y, x0 + w + 2 * pad, y + sz + 2 * pad), radius=12, fill=MAU[bg], outline=WHT, width=4)
    d.text((x0 + pad, y + pad + sz / 2 + 2), t, font=f, fill=MAU[fg], anchor="lm")
    return y + sz + 2 * pad + 6


def o_anh(p, w, h, rong=540, dy=0):
    """Ảnh dọc thu về rộng `rong` để lộ mặt + thân; 2 bên lấp bằng chính ảnh phóng to làm mờ."""
    im = Image.open(p).convert("RGB")
    nen = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).crop((0, 0, w, h))
    nen = nen.filter(ImageFilter.GaussianBlur(18))
    nho = im.resize((rong, round(im.height * rong / im.width)), Image.LANCZOS)
    dy = min(dy, nho.height - h)
    nho = nho.crop((0, dy, rong, dy + h))   # dy>0: đẩy ảnh lên khi mặt nằm thấp
    nen.paste(nho, ((w - rong) // 2, 0))
    return nen


def lam(tap):
    tap = Path(tap)
    thu = tap / "thumb_v2"
    c = json.loads((thu / "SPEC.json").read_text(encoding="utf-8"))
    can = Image.new("RGB", (W, H), BLK)
    ph = H - TOP - BOT
    can.paste(o_anh(thu / "bg" / "001.png", 636, ph, dy=c.get("trai_dy", 0)), (0, TOP))
    can.paste(o_anh(thu / "bg" / "002.png", 636, ph, dy=c.get("phai_dy", 0)), (644, TOP))
    d = ImageDraw.Draw(can)
    d.rectangle((0, 0, W, TOP), fill=BLK)
    d.rectangle((0, H - BOT, W, H), fill=(170, 0, 0))
    d.rectangle((0, H - BOT, W, H - BOT + 5), fill=YEL)
    dong_chu(d, c["top"], 4, TOP - 8, W - 40, 96)
    dong_chu(d, c["bot"], H - BOT + 4, BOT - 6, W - 60, 74)
    cy = TOP + ph * 0.42
    d.polygon([(600, cy - 45), (650, cy - 45), (650, cy - 80), (712, cy), (650, cy + 80), (650, cy + 45),
               (600, cy + 45)], fill=RED, outline=WHT, width=5)
    for xs, ds in ((c.get("trai_x", 318), c.get("trai") or []), (c.get("phai_x", 962), c.get("phai") or [])):
        y = H - BOT - 4 - sum(50 + 34 for _ in ds)
        for t, fg, bg in ds:
            y = nhan(d, xs, y, t, fg, bg)
    if c.get("bubble"):
        t = c["bubble"]
        sz = 40
        while font(sz).getlength(t) > 520 and sz > 26:
            sz -= 2
        f = font(sz)
        w = f.getlength(t)
        tren = H - BOT - 4 - sum(50 + 34 for _ in (c.get("trai") or []))   # mép trên chồng nhãn ô trái
        x0, y0 = 22, c.get("bubble_y") or min(TOP + 300, tren - 96)
        d.ellipse((x0 - 10, y0 - 22, x0 + w + 40, y0 + 80), fill=WHT, outline=BLK, width=5)
        d.text((x0 + 15, y0 + 29), t, font=f, fill=BLK, anchor="lm")
    out = tap / "thumbnail_v2.png"
    can.save(out)
    print(out)


if __name__ == "__main__":
    for a in sys.argv[1:]:
        lam(a)
