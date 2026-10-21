# -*- coding: utf-8 -*-
"""Hình học (đơn vị thiết kế → pixel) + trạng thái animation tại thời điểm t.

Thiết kế theo "đơn vị" với thẻ cao 100 đơn vị; bề rộng thẻ phụ thuộc chữ. Hệ số s (px/đơn vị)
suy từ bề rộng khung mong muốn → cùng 1 bố cục cho 720p / 1080p / 4K / 9:16, không cứng 1920x1080.
Canvas chừa lề để con trỏ, bóng đổ, gợn click, chuông xoay KHÔNG bao giờ chạm mép (test kiểm).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from PIL import ImageFont

PAD, ICON_H, ICON_AR, PILL_H, GAP, BELL_D = 14, 50, 1.42, 56, 14, 56
CARD_H, FONT_U, TEXT_PAD, PILL_MIN = 100, 26, 28, 130
AVATAR_D = 70  # avatar kênh tròn, bên trái logo
M_LEFT, M_TOP, M_RIGHT, M_BOTTOM = 24, 30, 64, 96
CURSOR_H = 40


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    return 1 - (1 - clamp(x)) ** 3


def ease_out_back(x, k=1.6):
    x = clamp(x) - 1
    return 1 + (k + 1) * x ** 3 + k * x ** 2


def lerp(a, b, u):
    return a + (b - a) * u


@dataclass
class Layout:
    s: float            # px (kết quả) / đơn vị
    ss: int             # hệ số vẽ phóng to (supersample)
    card_w: float       # đơn vị
    pill_w: float       # bề rộng nút 登録済み (đơn vị)
    pill_full: float    # bề rộng nút đỏ チャンネル登録 (chiếm cả chỗ chuông)
    canvas_w: int       # px kết quả (chẵn — VP9 yuva420p bắt buộc)
    canvas_h: int
    bell: bool
    avatar: bool = False

    # ---- toạ độ đơn vị (gốc = góc trái trên canvas) ----
    @property
    def card(self):
        return (M_LEFT, M_TOP, self.card_w, CARD_H)

    @property
    def cy(self):
        return M_TOP + CARD_H / 2

    @property
    def avatar_c(self):
        return (M_LEFT + PAD + AVATAR_D / 2, self.cy)

    @property
    def icon_x(self):
        return M_LEFT + PAD + ((AVATAR_D + GAP) if self.avatar else 0)

    @property
    def pill_x(self):
        return self.icon_x + ICON_H * ICON_AR + GAP

    @property
    def bell_c(self):
        return (self.pill_x + self.pill_w + GAP + BELL_D / 2, self.cy)

    @property
    def click1(self):
        return (self.pill_x + self.pill_full / 2, self.cy)

    @property
    def cursor_home(self):
        return (M_LEFT + self.card_w + 8, M_TOP + CARD_H + 30)

    def card_box_px(self):
        """(x, y, w, h) của THẺ trong canvas, px kết quả — dùng để đặt nút lên video."""
        x, y, w, h = self.card
        return [round(x * self.s), round(y * self.s), round(w * self.s), round(h * self.s)]

    def P(self, v):
        """đơn vị → px trên ảnh supersample."""
        return v * self.s * self.ss


def _even(v):
    return max(2, int(round(v / 2)) * 2)


def build_layout(font_path, texts, width_px, ss, bell=True, font_index=0, avatar=False) -> Layout:
    font = ImageFont.truetype(font_path, 200, index=font_index)
    tw = max((font.getbbox(t)[2] - font.getbbox(t)[0]) / 200 * FONT_U for t in texts if t)
    pill_w = max(PILL_MIN, tw + 2 * TEXT_PAD)
    tail = (GAP + BELL_D) if bell else 0
    head = (AVATAR_D + GAP) if avatar else 0
    card_w = PAD + head + ICON_H * ICON_AR + GAP + pill_w + tail + PAD
    s = width_px / card_w
    return Layout(s=s, ss=ss, card_w=card_w, pill_w=pill_w, pill_full=pill_w + tail,
                  canvas_w=_even((M_LEFT + card_w + M_RIGHT) * s),
                  canvas_h=_even((M_TOP + CARD_H + M_BOTTOM) * s), bell=bell, avatar=avatar)


def _bell_angle(t, c2, ring, angles):
    if not (c2 <= t <= c2 + ring) or len(angles) < 2:
        return 0.0
    u = (t - c2) / ring * (len(angles) - 1)
    i = min(int(u), len(angles) - 2)
    f = (1 - math.cos(math.pi * (u - i))) / 2
    return lerp(angles[i], angles[i + 1], f)


def state(t: float, cfg: dict, L: Layout) -> dict:
    """Mọi thứ cần để vẽ khung hình tại giây t (tính từ lúc overlay bắt đầu)."""
    tl, d = cfg["timeline"], float(cfg["duration"])
    fi, fo = float(cfg["fade_in"]), float(cfg["fade_out"])
    st = {"opacity": min(smooth(t / fi) if fi > 0 else 1.0, smooth((d - t) / fo) if fo > 0 else 1.0)}
    e = ease_out(t / max(fi + 0.15, 0.35))
    st["entry_dy"], st["entry_scale"] = 14 * (1 - e), 0.94 + 0.06 * e

    c1, sw = tl["click1"], tl["switch"]
    u = (t - c1) / tl["press"]
    st["pill_press"] = 1 - (1 - cfg["press_scale"]) * math.sin(math.pi * u) if 0 <= u <= 1 else 1.0
    st["mix"] = smooth((t - sw) / 0.16)
    th = tl.get("thanks")
    st["mix2"] = smooth((t - th) / 0.2) if (cfg.get("thanks_text") and th is not None) else 0.0
    ut = (t - th) / 0.3 if th is not None else -1
    st["thanks_pop"] = 1 + 0.05 * math.sin(math.pi * ut) if (st["mix2"] > 0 and 0 <= ut <= 1) else 1.0
    shrink = smooth((t - sw - 0.05) / 0.25) if L.bell else 0.0
    st["pill_cur_w"] = lerp(L.pill_full, L.pill_w, shrink)

    c2 = tl["click2"]
    st["bell_on"] = L.bell and t >= sw + 0.12
    st["bell_pop"] = ease_out_back((t - sw - 0.12) / 0.3) if st["bell_on"] else 0.0
    st["bell_alpha"] = clamp((t - sw - 0.12) / 0.15)
    st["bell_angle"] = _bell_angle(t, c2, tl["ring"], cfg["bell_angles"]) if L.bell else 0.0
    ub = (t - c2) / 0.2
    st["bell_press"] = 1 - 0.08 * math.sin(math.pi * ub) if (L.bell and 0 <= ub <= 1) else 1.0
    ur = (t - c2) / tl["ring"]
    st["ring_alpha"] = math.sin(math.pi * ur) if (L.bell and 0 <= ur <= 1) else 0.0

    clicks = [c1] + ([c2] if L.bell else [])
    st["ripples"] = []
    for c, p in zip(clicks, [L.click1, L.bell_c]):
        ur = (t - c) / 0.4
        if 0 <= ur <= 1:
            st["ripples"].append((p, 6 + 24 * ease_out(ur), 0.35 * (1 - ur)))

    st["cursor"] = None
    if cfg["enable_cursor"]:
        cin, cout = tl["cursor_in"], tl["cursor_out"]
        a = min(clamp((t - cin) / 0.2), 1 - clamp((t - cout) / 0.3))
        if a > 0:
            home, p1 = L.cursor_home, L.click1
            p2 = L.bell_c if L.bell else p1
            if t < tl["cursor_move1"]:
                pos = home
            elif t < c1:
                pos = _mv(home, p1, smooth((t - tl["cursor_move1"]) / (c1 - tl["cursor_move1"])))
            elif not L.bell or t < tl["cursor_move2"]:
                pos = p1 if t < cout else _mv(p1, home, smooth((t - cout) / 0.3))
            elif t < c2:
                pos = _mv(p1, p2, smooth((t - tl["cursor_move2"]) / (c2 - tl["cursor_move2"])))
            else:
                pos = p2 if t < cout else _mv(p2, home, smooth((t - cout) / 0.3))
            squash = 1.0
            for c in clicks:
                uc = (t - c) / 0.14
                if 0 <= uc <= 1:
                    squash = 1 - 0.15 * math.sin(math.pi * uc)
            st["cursor"] = (pos, a, squash)
    return st


def _mv(a, b, u):
    return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))
