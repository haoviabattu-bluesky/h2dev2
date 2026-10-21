# -*- coding: utf-8 -*-
"""Vẽ từng khung RGBA (Pillow, supersample) và encode thành overlay trong suốt.

webm = VP9 yuva420p (mặc định) | mov = ProRes 4444 | png = chuỗi PNG RGBA.
Trong lúc render đo alpha lớn nhất trên VIỀN canvas: >0 nghĩa là có hình bị cắt mép → báo lỗi.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import so_icons as ic
import so_layout as ly
from so_ffmpeg import popen

LANCZOS = Image.Resampling.LANCZOS
BICUBIC = Image.Resampling.BICUBIC


def _scaled(img: Image.Image, k: float) -> Image.Image:
    if abs(k - 1) < 1e-3:
        return img
    w, h = max(1, round(img.width * k)), max(1, round(img.height * k))
    return img.convert("RGBa").resize((w, h), LANCZOS).convert("RGBA")


def _paste_center(dst, spr, cx, cy):
    dst.alpha_composite(spr, dest=(int(round(cx - spr.width / 2)), int(round(cy - spr.height / 2))))


def _mix_color(a: str, b: str, u: float):
    ca, cb = ic.hex_rgb(a), ic.hex_rgb(b)
    return tuple(int(round(x + (y - x) * u)) for x, y in zip(ca, cb))


class Assets:
    """Sprite dựng 1 lần cho mỗi layout (ở kích thước supersample)."""

    def __init__(self, L: ly.Layout, cfg: dict, font_path: str, font_index: int = 0):
        P, st = L.P, cfg["style"]
        self.icon = ic.youtube_icon(int(P(ly.ICON_H)), st["red"])
        font = ImageFont.truetype(font_path, max(8, int(P(ly.FONT_U))), index=font_index)
        self.t_sub = ic.text_mask(cfg["subscribe_text"], font)
        self.t_subd = ic.text_mask(cfg["subscribed_text"], font)
        self.t_thx = ic.text_mask(cfg["thanks_text"], font) if cfg.get("thanks_text") else None
        self.avatar = ic.avatar_sprite(cfg["avatar_file"], int(P(ly.AVATAR_D))) if L.avatar else None
        cw, ch = int(P(L.card_w)), int(P(ly.CARD_H))
        self.card = ic.colorize(ic.rounded_mask(cw, ch, int(P(26))), st["card_bg"])
        self.shadow, self.sh_margin = ic.card_shadow(cw, ch, int(P(26)), max(1, int(P(9))), st["shadow_opacity"])
        bd = int(P(ly.BELL_D))
        circ = Image.new("L", (bd, bd), 0)
        ImageDraw.Draw(circ).ellipse((0, 0, bd - 1, bd - 1), fill=255)
        self.bell_bg = ic.colorize(circ, st["subscribed_bg"])
        self.bell = ic.colorize(ic.bell_mask(int(bd * 0.62)), st["bell_color"])
        self.cursor, self.tip = ic.cursor_sprite(int(P(ly.CURSOR_H)))


def _bell_group(L, st, A, cfg) -> Image.Image:
    P = L.P
    g = A.bell_bg.copy()
    b = A.bell
    piv = (b.width * ic.BELL_PIVOT[0], b.height * ic.BELL_PIVOT[1])
    if abs(st["bell_angle"]) > 0.01:
        b = b.convert("RGBa").rotate(st["bell_angle"], resample=BICUBIC, center=piv).convert("RGBA")
    _paste_center(g, b, g.width / 2, g.height / 2 - b.height * 0.02)
    if st["ring_alpha"] > 0.01:  # 2 cặp vạch cong hai bên chuông = đang reo
        m = Image.new("L", g.size, 0)
        d = ImageDraw.Draw(m)
        c, w = g.width / 2, max(1, int(P(2.2)))
        for r in (P(18), P(23)):
            box = (c - r, c - r, c + r, c + r)
            d.arc(box, -35, 35, fill=255, width=w)
            d.arc(box, 145, 215, fill=255, width=w)
        g.alpha_composite(ic.colorize(m, cfg["style"]["bell_color"], st["ring_alpha"]))
    return _scaled(g, st["bell_pop"] * st["bell_press"])


def render_frame(L: ly.Layout, st: dict, cfg: dict, A: Assets) -> Image.Image:
    P, sty = L.P, cfg["style"]
    W, H = L.canvas_w * L.ss, L.canvas_h * L.ss
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x, y, _, _ = L.card
    if cfg["enable_card"]:
        img.alpha_composite(A.shadow, dest=(int(P(x)) - A.sh_margin, int(P(y + 4)) - A.sh_margin))
        img.alpha_composite(A.card, dest=(int(P(x)), int(P(y))))
    if A.avatar is not None:
        _paste_center(img, A.avatar, P(L.avatar_c[0]), P(L.avatar_c[1]))
    img.alpha_composite(A.icon, dest=(int(P(L.icon_x)), int(P(L.cy) - A.icon.height / 2)))

    pw, ph, mix = int(P(st["pill_cur_w"])), int(P(ly.PILL_H)), st["mix"]
    pill = ic.colorize(ic.rounded_mask(pw, ph, ph // 2), _mix_color(sty["red"], sty["subscribed_bg"], mix))
    # chữ cũ tắt hẳn rồi chữ mới mới hiện — hoà 2 chữ cùng lúc nhìn thành một đống nhoè
    m2 = st["mix2"] if A.t_thx is not None else 0.0
    a_old, a_new = 1 - ly.smooth(mix * 2), ly.smooth(mix * 2 - 1) * (1 - ly.smooth(m2 * 2))
    texts = [(A.t_sub, sty["subscribe_text_color"], a_old), (A.t_subd, sty["subscribed_text_color"], a_new),
             (A.t_thx, sty["thanks_text_color"], ly.smooth(m2 * 2 - 1))]
    for mask, col, a in texts:
        if mask is not None and a > 0.01:
            _paste_center(pill, ic.colorize(mask, col, a), pw / 2, ph / 2)
    _paste_center(img, _scaled(pill, st["pill_press"] * st["thanks_pop"]), P(L.pill_x) + pw / 2, P(L.cy))

    if st["bell_on"] and st["bell_pop"] > 0.01:
        g = _bell_group(L, st, A, cfg)
        if st["bell_alpha"] < 0.999:
            g.putalpha(g.getchannel("A").point(lambda v: int(v * st["bell_alpha"])))
        _paste_center(img, g, P(L.bell_c[0]), P(L.bell_c[1]))

    if st["entry_scale"] < 0.999 or st["entry_dy"] > 0.01:  # trồi lên + phóng nhẹ lúc xuất hiện
        k, cx, cy = st["entry_scale"], P(x + L.card_w / 2), P(y + ly.CARD_H / 2)
        dy = P(st["entry_dy"])
        data = (1 / k, 0, cx - cx / k, 0, 1 / k, cy - (cy + dy) / k)
        img = img.convert("RGBa").transform(img.size, Image.Transform.AFFINE, data, BICUBIC).convert("RGBA")

    for (px, py), r, a in st["ripples"]:
        m = Image.new("L", (int(P(2 * r + 6)),) * 2, 0)
        c = m.width / 2
        ImageDraw.Draw(m).ellipse((c - P(r), c - P(r), c + P(r), c + P(r)), outline=255, width=max(1, int(P(2.5))))
        _paste_center(img, ic.colorize(m, "#000000", a), P(px), P(py))

    if st["cursor"]:
        (px, py), a, squash = st["cursor"]
        spr = _scaled(A.cursor, squash)
        tip = (A.tip[0] * squash, A.tip[1] * squash)
        if a < 0.999:
            spr = spr.copy()
            spr.putalpha(spr.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(spr, dest=(int(round(P(px) - tip[0])), int(round(P(py) - tip[1]))))

    out = img.convert("RGBa").resize((L.canvas_w, L.canvas_h), LANCZOS).convert("RGBA")
    if st["opacity"] < 0.999:
        op = st["opacity"]
        out.putalpha(out.getchannel("A").point(lambda v: int(v * op)))
    return out


def border_alpha(im: Image.Image) -> int:
    a = im.getchannel("A")
    w, h = im.size
    return max(a.crop(b).getextrema()[1] for b in ((0, 0, w, 2), (0, h - 2, w, h), (0, 0, 2, h), (w - 2, 0, w, h)))


def encode_overlay(L, cfg, A, fps: str, out_path: Path) -> dict:
    """Render toàn bộ khung → file overlay. Ghi file tạm rồi os.replace (không để cache dở dang)."""
    num, den = (int(v) for v in (fps.split("/") + ["1"])[:2])
    fps_f = num / den
    n = int(round(float(cfg["duration"]) * fps_f))
    fmt = cfg["overlay_format"]
    tmp = out_path.with_name(out_path.stem + ".partial" + out_path.suffix)
    size = f"{L.canvas_w}x{L.canvas_h}"
    enc = {"webm": ["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "20", "-deadline", "good",
                    "-cpu-used", "2", "-row-mt", "1", "-auto-alt-ref", "0", "-f", "webm"],
           "mov": ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-vendor", "apl0", "-f", "mov"]}
    proc = None
    if fmt == "png":
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True)
    else:
        proc = popen(["-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", size, "-framerate", fps, "-i", "-",
                      *enc[fmt], "-an", str(tmp)])
    worst = 0
    try:
        for i in range(n):
            fr = render_frame(L, ly.state(i / fps_f, cfg, L), cfg, A)
            worst = max(worst, border_alpha(fr))
            if proc:
                proc.stdin.write(fr.tobytes())
            else:
                fr.save(tmp / f"{i:05d}.png", compress_level=3)
    finally:
        if proc:
            proc.stdin.close()
            err = proc.stderr.read().decode("utf-8", "replace")
            if proc.wait() != 0:
                raise RuntimeError(f"Encode overlay lỗi:\n{err[-2000:]}")
    if fmt == "png" and out_path.exists():
        shutil.rmtree(out_path)
    os.replace(tmp, out_path)
    return {"frames": n, "border_alpha_max": worst}
