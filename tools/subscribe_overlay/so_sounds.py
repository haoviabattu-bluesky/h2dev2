# -*- coding: utf-8 -*-
"""Âm thanh pop (nút hiện) / click / chuông "ting".

Ưu tiên file anh tự bỏ vào `sounds/` (click.wav, bell.wav, pop.wav) — hiện có pop.wav = "lấp lánh 3 nốt" anh chọn. Thiếu file nào thì TỰ TỔNG HỢP
bằng numpy (sóng sine, không có bản quyền) vào cache — không bao giờ làm hỏng bước render.
"""
from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

import so_bells

HERE = Path(__file__).resolve().parent
USER_DIR = HERE / "sounds"
SR = 48000
SYNTH_VERSION = 7  # v7: thêm chuông 6_moc_cam (Lane N) | v6: chuông riêng từng lane (so_bells.bell_style) | v5: click chuột dày hơn (anh chê nhỏ), chọn kiểu click theo lane | v4: thêm sub_click mạnh cho nút đăng ký | v3 (2026-09-30): chuông về lại bản 1 (anh chốt); âm popup = sounds/pop.wav (05_lap_lanh_3_not)


def _write(path: Path, x: np.ndarray) -> None:
    x = x * _edge(x.size)
    x = np.clip(x / (np.abs(x).max() + 1e-9) * 0.89, -1, 1)
    tmp = path.with_suffix(".partial.wav")
    with wave.open(str(tmp), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())
    tmp.replace(path)


def _t(sec):
    return np.arange(int(SR * sec)) / SR


def _edge(n, a_ms=3.0, r_ms=25.0):
    """Vào/ra dạng cosine — cắt thẳng biên độ ở đầu/cuối chính là tiếng "bụp/phụt"."""
    e = np.ones(n)
    a, r = int(SR * a_ms / 1000), int(SR * r_ms / 1000)
    e[:a] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a))
    e[-r:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, r))
    return e


def synth_pop() -> np.ndarray:
    """Dự phòng khi thiếu sounds/pop.wav: "pốp" tròn nhẹ lúc nút hiện."""
    t = _t(0.16)
    f = 520 + 380 * (1 - np.exp(-t / 0.03))                  # trượt 520 → 900 Hz
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.sin(np.pi * np.clip(t / 0.16, 0, 1)) ** 2
    return (np.sin(ph) + 0.12 * np.sin(2 * ph)) * env


def synth_bell() -> np.ndarray:
    """Tiếng "ting" BẢN 1 — anh chốt 2026-09-30 giữ nguyên (khớp file chuong_ting_ban1_da_chot.wav)."""
    t = _t(1.3)
    x = np.zeros_like(t)
    for f, a, tau in ((1320, 1.0, 0.45), (2650, 0.5, 0.30), (3960, 0.25, 0.18), (5300, 0.12, 0.10)):
        x += a * np.sin(2 * np.pi * f * t) * np.exp(-t / tau)
    return x * (1 - np.exp(-t / 0.002))


# ---- Tiếng click NÚT ĐĂNG KÝ "mạnh" (2026-09-30) ----
# YouTube thật KHÔNG phát âm khi bấm Subscribe (web im lặng; app chỉ rung haptic + hiệu ứng lấp lánh trên nút).
# Tiếng "click + đập" quen tai là do các creator TỰ lồng vào animation → 5 phương án để anh nghe chọn.


def _bp(x, lo, hi):
    """Lọc thông dải FIR (windowed-sinc) — nhiễu đã lọc nghe "tách" chứ không "xì/phụt"."""
    n = np.arange(-200, 201)
    h = (np.sinc(2 * hi / SR * n) * 2 * hi - np.sinc(2 * lo / SR * n) * 2 * lo) / SR * np.hamming(n.size)
    return np.convolve(x, h, mode="same")


def _mouse(t0=0.0, dur=0.20, bt=0.0025, bodyf=420, bodyt=0.006, bodya=0.5, g2=0.45):
    """Click chuột thật: nhấn (tách chính) + nhả (tách nhỏ) cách ~65ms."""
    t = _t(dur)
    rng = np.random.default_rng(3)
    x = np.zeros_like(t)
    for off, g in ((t0, 1.0), (t0 + 0.065, g2)):
        k = (t >= off)
        tt = np.where(k, t - off, 0)
        burst = _bp(rng.standard_normal(t.size), 1800, 6500) * np.exp(-tt / bt)
        body = np.sin(2 * np.pi * bodyf * tt) * np.exp(-tt / bodyt) * bodya
        x += g * k * (burst * 3 + body)
    return x


def _thump(dur=0.22, f_hi=150, f_lo=48, tau=0.07):
    """Cú "đập" trầm (kick): sine trượt tần số xuống nhanh."""
    t = _t(dur)
    f = f_lo + (f_hi - f_lo) * np.exp(-t / 0.025)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / tau) * (1 - np.exp(-t / 0.001))


def _pad(x, n):
    return np.pad(x, (0, max(0, n - x.size)))[:n]


def cand_click_that():          # 1: click chuột thật — anh CHỌN 2026-09-30 nhưng chê nhỏ → thân tiếng dày hơn
    return _mouse(bt=0.004, bodyf=300, bodyt=0.012, bodya=1.2, g2=0.6)


def cand_click_dap():           # 2: click + cú đập trầm (kiểu creator hay dùng)
    n = int(SR * 0.25)
    return _pad(_mouse(), n) * 0.8 + _pad(_thump(), n) * 1.0


def cand_pop_dap():             # 3: "bộp" tròn (pitch rơi) + đập — mạnh, vui tai
    t = _t(0.12)
    f = 260 + 700 * np.exp(-t / 0.015)
    pop = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035)
    n = int(SR * 0.25)
    return _pad(pop, n) * 0.9 + _pad(_thump(f_hi=120, tau=0.06), n) * 0.8 + _pad(_mouse(dur=0.1), n) * 0.35


def cand_xac_nhan():            # 4: click + 2 nốt đi lên (âm "xác nhận" UI, sáng)
    n = int(SR * 0.45)
    t = _t(0.45)
    note = np.zeros_like(t)
    for off, f in ((0.03, 1046.5), (0.11, 1568.0)):
        tt = np.clip(t - off, 0, None)
        note += (t >= off) * (np.sin(2 * np.pi * f * tt) + 0.2 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt / 0.12)
    return _pad(_mouse(), n) * 0.7 + note * 0.55 + _pad(_thump(tau=0.05), n) * 0.5


def cand_impact():              # 5: gió hút ngắn DẪN VÀO cú đập + click (đặt sớm 0.12s) — mạnh nhất
    lead = 0.12
    t = _t(lead)
    rng = np.random.default_rng(5)
    swell = _bp(rng.standard_normal(t.size), 400, 3000) * (t / lead) ** 3 * 0.25
    n = int(SR * (lead + 0.3))
    hit = np.concatenate([np.zeros(t.size), _pad(_thump(f_hi=170, tau=0.09), n - t.size) * 1.0])
    clk = np.concatenate([np.zeros(t.size), _pad(_mouse(dur=0.1), n - t.size) * 0.7])
    return _pad(swell, n) + hit + clk


# tên kiểu → (hàm, lead giây, hệ số to). Hệ số đo 2026-09-30 trên giọng đọc kenko ep06 (RMS 50ms p95 = 0.166):
# mọi kiểu ≈ 0.16–0.22 RMS 15ms, tức NGANG hoặc nhỉnh hơn giọng đọc; đỉnh ≤ 0.80.
CANDIDATES = {"1_click_that": (cand_click_that, 0.0, 1.5), "2_click_dap": (cand_click_dap, 0.0, 1.0),
              "3_pop_dap": (cand_pop_dap, 0.0, 1.0), "4_xac_nhan": (cand_xac_nhan, 0.0, 1.0),
              "5_impact": (cand_impact, 0.12, 1.0)}
SUB_CLICK_DEFAULT = "1_click_that"  # anh chốt 2026-09-30; từng lane đổi bằng config "sub_click_style"

_SYNTH = {"pop": synth_pop, "click": cand_click_that, "bell": synth_bell}  # click chuông = cùng tiếng chuột


def ensure_sounds(cache: Path, files: dict | None = None) -> dict[str, Path]:
    """files = cfg["sound_files"]: {tên: đường dẫn wav} ghi đè từng âm (vd thử phương án khác)."""
    out = {}
    syn = cache / f"sounds_synth_v{SYNTH_VERSION}"
    table = dict(_SYNTH, **{f"sub_click:{k}": v[0] for k, v in CANDIDATES.items()},
                 **{f"bell:{k}": v for k, v in so_bells.BELLS.items()})
    for name, fn in table.items():
        key = name.split(":", 1)[0]  # sub_click:x / bell:x → file anh bỏ vào sounds/ (nếu có) thắng
        if (files or {}).get(key):
            out[name] = Path(files[key])
            continue
        user = USER_DIR / f"{key}.wav"
        if user.is_file():
            out[name] = user
            continue
        syn.mkdir(parents=True, exist_ok=True)
        p = syn / f"{name.replace(':', '_')}.wav"
        if not p.is_file():
            _write(p, fn())
        out[name] = p
    return out


def events(cfg: dict) -> list[tuple[str, float]]:
    """(tên âm, giây tính từ lúc overlay hiện)."""
    tl = cfg["timeline"]
    style = cfg.get("sub_click_style") or SUB_CLICK_DEFAULT
    _, lead, _ = CANDIDATES[style]  # âm có đoạn dẫn (impact) phải phát SỚM để cú đập trùng lúc click
    lead = float(cfg.get("sub_click_lead", lead))
    ev = [("pop", 0.05), (f"sub_click:{style}", max(0.0, tl["click1"] - lead))]
    if cfg["enable_bell"]:
        bell = cfg.get("bell_style") or so_bells.BELL_DEFAULT
        if bell not in so_bells.BELLS:
            raise ValueError(f"bell_style không có: {bell} (có: {', '.join(so_bells.BELLS)})")
        ev += [("click", tl["click2"]), (f"bell:{bell}", tl["click2"] + 0.03)]
    return ev


def gain_of(name: str) -> float:
    """Hệ số to riêng của kiểu click (nhân thêm với sound_gains trong config)."""
    if name == "click":  # click chuông dùng chung tiếng chuột 1_click_that
        return CANDIDATES["1_click_that"][2]
    return CANDIDATES[name.split(":", 1)[1]][2] if name.startswith("sub_click:") else 1.0
