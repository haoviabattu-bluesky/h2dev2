# -*- coding: utf-8 -*-
"""Tiếng chuông "ting" RIÊNG TỪNG LANE (anh chốt 2026-09-30: mỗi lane 1 tiếng chuông khác nhau).

Chọn bằng config "bell_style" (khai trong profile lane: assemble.subscribe.bell_style).
Tất cả tự tổng hợp bằng sine (không bản quyền); _write() của so_sounds chuẩn hoá đỉnh 0.89 như nhau.
Sửa/thêm kiểu → tăng SYNTH_VERSION trong so_sounds.py (không thì cache cũ vẫn được dùng).
"""
from __future__ import annotations

import numpy as np

SR = 48000


def _t(sec):
    return np.arange(int(SR * sec)) / SR


def _note(t, partials, attack=0.002):
    """partials = [(tần số, biên độ, tau tắt dần)]."""
    x = np.zeros_like(t)
    for f, a, tau in partials:
        x += a * np.sin(2 * np.pi * f * t) * np.exp(-t / tau)
    return x * (1 - np.exp(-t / attack))


def _place(total, parts):
    """Ghép nhiều nốt lệch giờ: parts = [(giây bắt đầu, mảng)]."""
    out = np.zeros(int(SR * total))
    for t0, x in parts:
        i = int(SR * t0)
        n = min(len(x), len(out) - i)
        out[i:i + n] += x[:n]
    return out


def bell_1_ting():
    """Bản 1 anh chốt (lane L): ting sáng 1320 Hz."""
    return _note(_t(1.3), ((1320, 1.0, 0.45), (2650, 0.5, 0.30), (3960, 0.25, 0.18), (5300, 0.12, 0.10)))


def bell_2_tram_am():
    """Chuông trầm ấm 784 Hz (Sol5), hoạ âm lệch kiểu chuông chùa nhỏ — hợp kể chuyện đời người."""
    return _note(_t(1.6), ((784, 1.0, 0.60), (784 * 2.76, 0.35, 0.28), (784 * 5.40, 0.12, 0.12), (1568, 0.3, 0.40)))


def bell_3_hai_not():
    """"Ding-dong" 2 nốt đi lên (Re6 → Sol6) — vui, nhẹ nhàng."""
    n1 = _note(_t(0.9), ((1175, 1.0, 0.30), (2350, 0.3, 0.15)))
    n2 = _note(_t(1.2), ((1568, 1.0, 0.40), (3136, 0.3, 0.20)))
    return _place(1.35, [(0.0, n1 * 0.8), (0.13, n2)])


def bell_4_chuong_gio():
    """Chuông gió: 3 nốt cao rơi nhanh (Do7 · Mi7 · Sol6) — trong, lấp lánh."""
    notes = [(2093, 0.0), (2637, 0.06), (1568, 0.12)]
    parts = [(t0, _note(_t(0.9), ((f, 1.0, 0.25), (f * 2.0, 0.2, 0.10)))) for f, t0 in notes]
    return _place(1.1, parts)


def bell_5_kim_loai():
    """Tiếng "keng" kim loại mảnh kiểu triangle 2400 Hz, hoạ âm không nguyên — sắc, ngân lâu."""
    return _note(_t(1.5), ((2400, 1.0, 0.55), (2400 * 1.51, 0.45, 0.35), (2400 * 2.33, 0.25, 0.20),
                           (1200, 0.25, 0.30)), attack=0.001)


def bell_6_moc_cam():
    """Mộc cầm (marimba) 2 nốt đi xuống (Sol5 → Mi5), gỗ ấm, tắt nhanh — Lane N (senior_korekara, 2026-09-30)."""
    def mo(f):
        return _note(_t(0.8), ((f, 1.0, 0.22), (f * 4.0, 0.35, 0.05), (f * 10.0, 0.08, 0.02)), attack=0.001)
    return _place(1.0, [(0.0, mo(784) * 0.85), (0.16, mo(659))])


BELLS = {"1_ting": bell_1_ting, "2_tram_am": bell_2_tram_am, "3_hai_not": bell_3_hai_not,
         "4_chuong_gio": bell_4_chuong_gio, "5_kim_loai": bell_5_kim_loai,
         "6_moc_cam": bell_6_moc_cam}
BELL_DEFAULT = "1_ting"
