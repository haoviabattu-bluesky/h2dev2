# -*- coding: utf-8 -*-
r"""qc_transcript.py — cong B2Q: transcript doi thu co DAY DU khong (P0, 2026-09-18).

fetch_script.py co 3 duong du phong (api -> yt-dlp subs -> whisper) nhung khong duong nao kiem
"lay du chua": transcript cut nua chung thi B3 viet tren nua cau chuyen, B3Q --competitor van PASS.
Do tat dinh tu sidecar <competitor>.segments.json (fetch_script ghi kem tu P0):
  coverage = moc cuoi / thoi luong video   (<0.80 FAIL · <0.92 WARN · khong co thoi luong -> WARN)
  max_gap  = khoang trong dai nhat (bo 60s dau/cuoi)  (>45s WARN)
  duplicate_ratio = ti le cau trung nguyen van  (>0.15 FAIL — subtitle bi lap block)
  chars_per_min   (<120 WARN — qua thua, kha nang mat doan)
Khong co sidecar (tap cu) -> SKIPPED, exit 0.

  py -3.13 qc_transcript.py --slug <tap> [--name competitor]
"""
import argparse
import collections
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate_common as G   # noqa: E402

GATE = "B2Q"


def _f(v, mac_dinh=0.0):
    """float an toan: None/chuoi hong/thieu key -> mac_dinh (do() khong duoc nem loi voi sidecar lech)."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return mac_dinh


def do(seg_json):
    if not isinstance(seg_json, dict):
        seg_json = {}
    segs = sorted((s for s in (seg_json.get("segments") or []) if isinstance(s, dict)), key=lambda s: _f(s.get("start")))
    dur = _f(seg_json.get("video_duration_sec"))
    blocking, warnings = [], []
    if not segs:
        return "FAIL", ["transcript rong"], [], {"n_seg": 0}
    last = _f(segs[-1].get("start")) + _f(segs[-1].get("duration"))
    text_all = " ".join(str(s.get("text") or "") for s in segs)
    n_chars = len(text_all.replace(" ", ""))
    coverage = None
    if dur > 0:
        coverage = round(min(last / dur, 1.0), 4)
        if coverage < 0.80:
            blocking.append(f"coverage {coverage:.0%} < 80% — transcript ket thuc som ({last:.0f}s / {dur:.0f}s)")
        elif coverage < 0.92:
            warnings.append(f"coverage {coverage:.0%} < 92%")
    else:
        warnings.append("khong co thoi luong video -> khong do duoc coverage")
    max_gap, gap_at = 0.0, 0.0
    for a, b in zip(segs, segs[1:]):
        end_a = _f(a.get("start")) + _f(a.get("duration"))
        g = _f(b.get("start")) - end_a
        if 60 <= end_a and (dur == 0 or _f(b.get("start")) <= dur - 60) and g > max_gap:
            max_gap, gap_at = g, end_a
    if max_gap > 45:
        warnings.append(f"gap {max_gap:.0f}s khong co transcript tai {gap_at:.0f}s")
    texts = [str(s.get("text") or "").strip() for s in segs if len(str(s.get("text") or "").strip()) >= 8]
    dup = sum(c - 1 for c in collections.Counter(texts).values() if c > 1)
    duplicate_ratio = round(dup / max(len(texts), 1), 4)
    if duplicate_ratio > 0.15:
        blocking.append(f"duplicate_ratio {duplicate_ratio:.0%} > 15% — subtitle bi lap block")
    minutes = (dur or last) / 60
    cpm = round(n_chars / minutes, 1) if minutes else 0
    if minutes and cpm < 120:
        warnings.append(f"mat do {cpm} ky tu/phut < 120 — qua thua, kha nang mat doan")
    status = "FAIL" if blocking else ("WARN" if warnings else "PASS")
    metrics = {"n_seg": len(segs), "source": seg_json.get("source"), "video_duration": dur,
               "last_timestamp": round(last, 1), "coverage": coverage, "max_gap_sec": round(max_gap, 1),
               "duplicate_ratio": duplicate_ratio, "chars_per_min": cpm}
    return status, blocking, warnings, metrics


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--name", default="competitor")
    a = ap.parse_args(argv)
    d = Path(a.slug)
    side = d / f"{a.name}.segments.json"
    if not side.exists():
        kq = G.ket_qua(GATE, "SKIPPED", warnings=[f"khong co {side.name} (tap cu, fetch truoc P0)"])
        G.ghi_log(d, GATE, kq)
        print(f"=== {GATE}: SKIPPED (khong co sidecar)")
        return 0
    try:
        status, blocking, warnings, metrics = do(json.loads(side.read_text(encoding="utf-8")))
    except (OSError, ValueError) as e:   # sidecar hong/khong doc duoc = artifact malformed -> FAIL co hoc
        status, blocking, warnings, metrics = "FAIL", [f"{side.name} hong, khong doc duoc: {str(e)[:120]}"], [], {}
    G.ghi_log(d, GATE, G.ket_qua(GATE, status, blocking=blocking, warnings=warnings, metrics=metrics))
    print(f"=== {GATE}: {status} · coverage={metrics.get('coverage')} gap={metrics.get('max_gap_sec')}s "
          f"dup={metrics.get('duplicate_ratio')} cpm={metrics.get('chars_per_min')}")
    for b in blocking:
        print("  ✗", b)
    for w in warnings:
        print("  ⚠", w)
    return 1 if status == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
