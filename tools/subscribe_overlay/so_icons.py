# -*- coding: utf-8 -*-
"""Icon tự vẽ (không screenshot, không tải mạng): logo play, chuông, con trỏ, bóng đổ.

Mọi hình vẽ thành MẶT NẠ "L" rồi mới tô màu — vẽ chữ/hình trực tiếp lên ảnh RGBA trong suốt
làm viền bị pha màu đen (quầng tối quanh chữ trắng) khi thu nhỏ.
"""
from __future__ import annotations

from PIL import Image, ImageChops, ImageDraw, ImageFilter


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def colorize(mask: Image.Image, color, alpha: float = 1.0) -> Image.Image:
    """Mặt nạ L + màu → sprite RGBA (không quầng)."""
    layer = Image.new("RGBA", mask.size, (*hex_rgb(color), 0) if isinstance(color, str) else (*color, 0))
    layer.putalpha(mask if alpha >= 0.999 else mask.point(lambda v: int(v * alpha)))
    return layer


def youtube_icon(h: int, red: str) -> Image.Image:
    w = int(h * 1.42)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=int(h * 0.26), fill=255)
    icon = colorize(m, red)
    tri = Image.new("L", (w, h), 0)
    tw, th = h * 0.36, h * 0.40
    cx, cy = w / 2 + tw * 0.08, h / 2
    ImageDraw.Draw(tri).polygon([(cx - tw / 2, cy - th / 2), (cx - tw / 2, cy + th / 2), (cx + tw / 2, cy)], fill=255)
    icon.alpha_composite(colorize(tri, "#FFFFFF"))
    return icon


def bell_mask(size: int) -> Image.Image:
    """Chuông trong ô vuông size×size; điểm treo (tâm xoay) ở (0.5, 0.12)·size."""
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    S = size
    pts_r = []
    n = 40
    for i in range(n + 1):  # nửa phải thân chuông: vòm → thân → loe đáy
        y = 0.20 + 0.52 * i / n
        k = (y - 0.20) / 0.52
        half = 0.10 + 0.20 * (k ** 0.5)
        if y > 0.58:
            half += 0.07 * ((y - 0.58) / 0.14) ** 2
        pts_r.append((0.5 + half, y))
    pts = [(0.5, 0.17)] + pts_r + [(1 - x, y) for x, y in reversed(pts_r)]
    d.polygon([(x * S, y * S) for x, y in pts], fill=255)
    d.ellipse((0.35 * S, 0.15 * S, 0.65 * S, 0.33 * S), fill=255)            # đỉnh vòm tròn
    d.rounded_rectangle((0.14 * S, 0.70 * S, 0.86 * S, 0.77 * S), radius=0.035 * S, fill=255)  # vành
    d.ellipse((0.43 * S, 0.77 * S, 0.57 * S, 0.89 * S), fill=255)            # quả lắc
    d.ellipse((0.455 * S, 0.08 * S, 0.545 * S, 0.17 * S), fill=255)          # núm treo
    return m


BELL_PIVOT = (0.5, 0.12)


def cursor_sprite(h: int) -> tuple[Image.Image, tuple[int, int]]:
    """Con trỏ mũi tên trắng viền đen. Trả (sprite, toạ độ mũi nhọn trong sprite)."""
    grid = [(0, 0), (0, 16), (4, 12.3), (6.6, 18.4), (9.2, 17.3), (6.7, 11.3), (11.6, 11.3)]
    k = h / 19.0
    ow = max(2, int(round(h * 0.07)))
    pad = ow * 2 + 2
    w_img, h_img = int(12 * k) + 2 * pad, int(19.5 * k) + 2 * pad
    inner = Image.new("L", (w_img, h_img), 0)
    ImageDraw.Draw(inner).polygon([(pad + x * k, pad + y * k) for x, y in grid], fill=255)
    outer = inner.filter(ImageFilter.MaxFilter(2 * ow + 1))
    spr = colorize(outer, "#111111")
    spr.alpha_composite(colorize(inner, "#FFFFFF"))
    return spr, (pad, pad)


def card_shadow(w: int, h: int, radius: int, blur: int, opacity: float) -> tuple[Image.Image, int]:
    """Bóng đổ mềm của thẻ. Trả (sprite, lề) — sprite lớn hơn thẻ `lề` px mỗi phía."""
    margin = blur * 3
    m = Image.new("L", (w + 2 * margin, h + 2 * margin), 0)
    ImageDraw.Draw(m).rounded_rectangle((margin, margin, margin + w, margin + h), radius=radius, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    return colorize(m, "#000000", opacity), margin


def rounded_mask(w: int, h: int, radius: int) -> Image.Image:
    m = Image.new("L", (max(1, w), max(1, h)), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=min(radius, h // 2, w // 2), fill=255)
    return m


def text_mask(text: str, font) -> Image.Image:
    l, t, r, b = font.getbbox(text)
    m = Image.new("L", (r - l + 4, b - t + 4), 0)
    ImageDraw.Draw(m).text((2 - l, 2 - t), text, font=font, fill=255)
    return m


def avatar_sprite(path: str, d: int) -> Image.Image:
    """Avatar kênh: cắt vuông giữa ảnh → tròn đường kính d + viền xám rất mảnh (tách khỏi nền thẻ trắng)."""
    im = Image.open(path).convert("RGBA")
    s = min(im.size)
    im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2))
    im = im.convert("RGBa").resize((d, d), Image.Resampling.LANCZOS).convert("RGBA")
    m = Image.new("L", (d, d), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
    im.putalpha(ImageChops.darker(im.getchannel("A"), m))
    ring = Image.new("L", (d, d), 0)
    ImageDraw.Draw(ring).ellipse((0, 0, d - 1, d - 1), outline=255, width=max(1, d // 40))
    im.alpha_composite(colorize(ring, "#DADADA"))
    return im
