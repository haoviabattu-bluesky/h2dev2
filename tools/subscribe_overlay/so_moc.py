"""Chọn giây hiện nút (±cửa sổ quanh mốc gốc) để tiếng nút KHÔNG đè lời đọc.

Chỉ đổi GIÂY BẮT ĐẦU của lớp nút — video/giọng không bị dời, không bị cắt (nút là lớp phủ).
Nguồn sự thật = sóng âm của chính video (không dùng SRT: SRT do STT sinh lệch mốc 100–150ms).
  - Lời đọc = khung 10ms có mức > speech_db (mặc định −45 dBFS).
  - Chuyển ảnh = khung hình đổi mạnh (so ảnh xám 64×36, 10 khung/giây).
Điểm phạt 1 mốc t (càng thấp càng tốt):
  Σ trọng số × (số giây tiếng nút đè lên lời)  — chuông nặng nhất, rồi click, rồi pop
  − thưởng nếu nút hiện đúng lúc chuyển ảnh
  + phạt nhẹ theo khoảng cách tới mốc gốc
"""
from __future__ import annotations

import subprocess

import numpy as np

import so_ffmpeg as ff
import so_sounds

HOP = 0.01                     # 10ms / khung âm
SND_LEN = {"pop": 0.40, "sub_click": 0.25, "click": 0.20, "bell": 0.60}   # phần NGHE RÕ của mỗi tiếng (giây)
SND_W = {"pop": 0.5, "sub_click": 0.8, "click": 0.6, "bell": 1.0}
SCENE_BONUS = 0.30             # hiện đúng lúc chuyển ảnh ≈ đỡ 0,3 giây đè lời
SCENE_TOL = (-0.3, 0.5)        # nút hiện trong [cut−0,3; cut+0,5] = tính là "lúc chuyển ảnh"
DIST_W = 0.002                 # phạt 0,002 / giây lệch khỏi mốc gốc (60s = 0,12)
WHITE_W = 1.5                  # thẻ nằm trên bóng thoại/khung chữ trắng suốt 6s ≈ đè lời 1,5s (anh: không đè chữ)


def _audio_db(video, a: float, dur: float) -> np.ndarray:
    raw = subprocess.run([ff.ffmpeg_exe(), "-v", "error", "-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", str(video),
                          "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float64) / 32768.0
    w = int(8000 * HOP)
    n = len(x) // w
    r = np.sqrt((x[: n * w].reshape(n, w) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(r)


def _frames(video, a: float, dur: float, fps: int = 10, W: int = 128, H: int = 72) -> np.ndarray:
    raw = subprocess.run([ff.ffmpeg_exe(), "-v", "error", "-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", str(video),
                          "-an", "-vf", f"fps={fps},scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8)[: len(raw) // (W * H) * W * H].reshape(-1, H, W).astype(np.float32)


def _scene_cuts(fr: np.ndarray, a: float, fps: int = 10, thr: float = 12.0) -> list[float]:
    """Mốc chuyển ảnh (giây tuyệt đối). Ảnh tĩnh → chênh ~0; lúc đổi ảnh chênh vọt lên."""
    if len(fr) < 2:
        return []
    d = np.abs(np.diff(fr.reshape(len(fr), -1), axis=0)).mean(1)
    cuts, prev = [], False
    for i, v in enumerate(d):
        on = v > thr
        if on and not prev:                 # đầu 1 đợt đổi (crossfade nhiều khung = 1 lần chuyển)
            cuts.append(a + (i + 1) / fps)
        prev = on
    return cuts


def card_region(cfg: dict) -> tuple[float, float, float, float] | None:
    """Vùng thẻ nút (x0, y0, x1, y1, tỉ lệ khung) — xấp xỉ theo config, đo trên ep01 lane L:
    thẻ cao ≈ 0,173 × bề rộng thẻ (px). Chỉ tính cho bottom_*; vị trí khác → None (bỏ điều kiện)."""
    pos = cfg.get("position", "bottom_center")
    if not pos.startswith("bottom"):
        return None
    w = float(cfg["overlay_width_ratio"])
    y1 = 1.0 - (float(cfg["subtitle_safe_ratio"]) if cfg.get("has_subtitles") else float(cfg["bottom_margin_ratio"]))
    y0 = y1 - w * 16 / 9 * 0.173
    x0 = {"bottom_center": 0.5 - w / 2, "bottom_left": 0.04, "bottom_right": 0.96 - w}[pos]
    return x0, y0, x0 + w, y1


def white_frac(fr: np.ndarray, box, lum: float = 238.0) -> np.ndarray:
    """Tỉ lệ điểm gần-trắng trong vùng thẻ mỗi khung — bóng thoại / khung chữ là nền trắng tinh."""
    if box is None or not len(fr):
        return np.zeros(len(fr))
    H, W = fr.shape[1:]
    x0, y0, x1, y1 = box
    reg = fr[:, int(y0 * H): max(int(y1 * H), int(y0 * H) + 1), int(x0 * W): int(x1 * W)]
    return (reg >= lum).reshape(len(fr), -1).mean(1)


def _events(cfg: dict) -> list[tuple[str, float, float, float]]:
    """(tên, lệch so với lúc nút hiện, độ dài nghe rõ, trọng số)."""
    out = []
    for name, off in so_sounds.events(cfg):
        base = name.split(":", 1)[0]
        out.append((base, off, SND_LEN.get(base, 0.3), SND_W.get(base, 0.5)))
    return out


def score(t: float, speech: np.ndarray, a: float, events, cuts, t0: float,
          white: np.ndarray | None = None, d: float = 6.0, fps: int = 10) -> tuple[float, float]:
    """Trả (điểm phạt, số giây đè lời). white = tỉ lệ trắng vùng thẻ theo khung (10 khung/giây từ a)."""
    over = 0.0
    for _, off, ln, w in events:
        i0 = int(round((t + off - a) / HOP))
        i1 = int(round((t + off + ln - a) / HOP))
        seg = speech[max(i0, 0): max(i1, 0)]
        over += w * float(seg.sum()) * HOP
    raw_over = over
    if any(SCENE_TOL[0] <= t - c <= SCENE_TOL[1] for c in cuts):
        over -= SCENE_BONUS
    if white is not None and len(white):
        seg = white[max(int((t - a) * fps), 0): max(int((t + d - a) * fps), 0)]
        if len(seg):
            over += WHITE_W * float(seg.mean())
    return over + DIST_W * abs(t - t0), raw_over


def pick_one(video, t0: float, lo: float, hi: float, cfg: dict, window: float = 60.0,
             speech_db: float = -45.0) -> dict:
    """Chọn t trong [max(lo, t0−window); min(hi, t0+window)]."""
    a = max(0.0, max(lo, t0 - window) - 1.0)
    b = min(hi, t0 + window)
    lo2 = max(lo, t0 - window)
    if b <= lo2:
        return {"goc": t0, "chon": t0, "de_loi_giay": None, "canh_bao": "không có chỗ trong cửa sổ → giữ mốc gốc"}
    span = (b - a) + float(cfg["duration"]) + 1.0
    db = _audio_db(video, a, span)
    speech = db > speech_db
    fr = _frames(video, a, span)
    cuts = _scene_cuts(fr, a)
    wf = white_frac(fr, card_region(cfg)) if cfg.get("tranh_vung_trang", True) else None
    ev, d = _events(cfg), float(cfg["duration"])
    grid = np.arange(lo2, b + 1e-9, 0.05)
    best = min(((score(float(t), speech, a, ev, cuts, t0, wf, d), float(t)) for t in grid), key=lambda z: z[0][0])
    (_, over), t = best
    goc = score(t0, speech, a, ev, cuts, t0)[1] if lo2 <= t0 <= b else None
    trang = None
    if wf is not None and len(wf):
        seg = wf[max(int((t - a) * 10), 0): int((t + d - a) * 10)]
        trang = round(float(seg.max()), 3) if len(seg) else None
    near = [round(c, 2) for c in cuts if SCENE_TOL[0] <= t - c <= SCENE_TOL[1]]
    return {"goc": round(t0, 3), "chon": round(t, 2), "de_loi_giay": round(over, 3),
            "de_loi_giay_neu_giu_goc": None if goc is None else round(goc, 3),
            "chuyen_anh": near[0] if near else None, "so_chuyen_anh_trong_cua_so": len(cuts),
            "vung_nut_trang_max": trang}


def choose_starts(video, cfg: dict, video_dur: float, window: float = 60.0) -> tuple[list[float], list[dict]]:
    """Mốc gốc (start_times, âm = tính từ cuối) → mốc đã chọn, lần lượt, giữ khoảng cách min_gap."""
    from so_compose import resolve_starts
    base, _ = resolve_starts(cfg, video_dur)
    d, gap = float(cfg["duration"]), float(cfg.get("min_gap", 30.0))
    hi_all = video_dur - d - 0.5
    chosen, report, lo = [], [], 0.0
    for t0 in base:
        r = pick_one(video, t0, lo, hi_all, cfg, window)
        chosen.append(r["chon"])
        report.append(r)
        lo = r["chon"] + d + gap
    return chosen, report
