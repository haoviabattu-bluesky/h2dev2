"""so_moc: chọn giây hiện nút tránh đè lời — test bằng mặt nạ lời giả (không cần video)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import so_config  # noqa: E402
import so_moc  # noqa: E402


def _speech(a, total, gaps):
    """Lời đọc liên tục, trừ các khoảng lặng (giây tuyệt đối)."""
    m = np.ones(int(total / so_moc.HOP), bool)
    for g0, g1 in gaps:
        m[int((g0 - a) / so_moc.HOP): int((g1 - a) / so_moc.HOP)] = False
    return m


def _best(speech, a, lo, hi, cuts, t0):
    cfg = so_config.load_config(None, {"enable_sound": True})
    ev = so_moc._events(cfg)
    grid = np.arange(lo, hi, 0.05)
    return min(((so_moc.score(float(t), speech, a, ev, cuts, t0), float(t)) for t in grid), key=lambda z: z[0][0])


def test_chuong_va_pop_roi_vao_khoang_lang():
    # khoảng lặng câu dài 0,6s, cách nhau đúng 3,28s (pop 0,05 · chuông 3,33)
    a = 100.0
    sp = _speech(a, 40, [(110.0, 110.6), (113.3, 113.9)])
    (_, over), t = _best(sp, a, 100, 125, [], 112.0)
    assert 109.9 <= t <= 110.3, t
    assert over < 0.5


def test_khong_co_khoang_lang_thi_van_tra_moc_gan_goc():
    a = 100.0
    sp = _speech(a, 40, [])
    (_, over), t = _best(sp, a, 100, 125, [], 112.0)
    assert abs(t - 112.0) < 0.06          # đè như nhau ở mọi nơi → phạt khoảng cách thắng
    assert over > 0


def test_uu_tien_chuyen_anh_khi_de_loi_ngang_nhau():
    a = 100.0
    sp = _speech(a, 40, [])
    (_, _), t = _best(sp, a, 100, 125, [118.0], 112.0)
    assert 117.7 <= t <= 118.5, t


def test_choose_starts_giu_khoang_cach(monkeypatch):
    calls = []

    def fake(video, t0, lo, hi, cfg, window=60.0, speech_db=-45.0):
        calls.append((t0, lo))
        return {"chon": t0 + 5}
    monkeypatch.setattr(so_moc, "pick_one", fake)
    cfg = so_config.load_config(None, {"start_times": [180, -120]})
    starts, _ = so_moc.choose_starts("x.mp4", cfg, 1200.0)
    assert starts == [185, 1085]
    assert calls[1][1] == 185 + cfg["duration"] + cfg["min_gap"]


def test_tranh_vung_trang_bong_thoai():
    # lời đọc như nhau mọi nơi; từ 110s–118s vùng thẻ bị bóng thoại trắng che → phải chọn chỗ khác
    a = 100.0
    sp = _speech(a, 40, [])
    cfg = so_config.load_config(None, {"enable_sound": True})
    fr = np.full((400, 72, 128), 90.0, np.float32)
    box = so_moc.card_region(cfg)
    x0, y0, x1, y1 = box
    fr[100:180, int(y0 * 72): int(y1 * 72), int(x0 * 128): int(x1 * 128)] = 255.0
    wf = so_moc.white_frac(fr, box)
    assert wf[150] > 0.9 and wf[50] == 0.0
    ev = so_moc._events(cfg)
    grid = np.arange(100, 125, 0.05)
    t = min(grid, key=lambda t: so_moc.score(float(t), sp, a, ev, [], 112.0, wf, 6.0)[0])
    assert not (104.0 < t < 118.0), t
