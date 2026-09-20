# TASK 4 BRIEF (trich tu plan 2026-09-18-p0-buoc1-gates.md)

## Global Constraints

- Dự án KHÔNG có git → mỗi task kết thúc bằng chạy pytest + 1 lệnh chạy thật trên tập STT3 (`E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-03-Kmxva85WKec`) thay cho commit. Trước khi sửa file có sẵn: copy `<file>` → `pipeline/_bak_<file>_<HHMM>` (theo lệ `_bak_stock_sources_1551.py` đã có).
- Chế độ cổng (anh chốt 2026-09-18): chỉ **PHÁN XÉT SEMANTIC** (B5P conflict, mapping mismatch) chạy **WARN-only** (`--mode warn` mặc định) trên 2 tập đầu để đo false-positive. **Invariant/lỗi cơ học chắc chắn FAIL ngay từ tập đầu:** số đoạn không tồn tại; mapping vi phạm ràng buộc bắt buộc (không giảm theo thứ tự); thiếu/trùng ID; **artifact STALE** (hash script khác hash nguồn đã ghi); output malformed; thiếu artifact bắt buộc.
- **Histogram chia đều (2,3,2,3…) KHÔNG phải FAIL cơ học** — chỉ đánh dấu `SUSPICIOUS` (WARN) và **bắt buộc chạy semantic QC** cho tập đó (không được `--no-llm` khi suspicious). FAIL của bản `img_doan` cũ STT3 trong hồi quy phải đến từ semantic mismatch (`--mode fail`) hoặc invariant thật, không phải vì "đều quá".
- **Fingerprint thay vì mtime:** khi sinh xong B5/B5.5, ghi `<slug>/artifact_meta.json` = `{"script_sha256": <sha>, "artifacts": {"img_prompts.txt": {"generated_from_script_sha256": <sha>, "sha256": <sha_file>}, "img_doan.txt": {...}}}`. Cổng `kiem_stale`: sha256(script.txt) hiện tại ≠ `generated_from_script_sha256` → **STALE = FAIL, chặn handoff**. mtime chỉ là fast-check phụ trợ (chưa có meta → dùng mtime + WARN "chưa có fingerprint").
- LLM: **không** làm ma trận 130×50. Facts: 1 lời gọi/10 đoạn; kiểm prompt: 1 lời gọi/15 prompt kèm facts của dải đoạn liên quan; mapping semantic: 1 lời gọi/8 đoạn kèm prompt đã map. ≈20 lời gọi/tập là **mục tiêu ban đầu, không phải trần cứng**. Mọi cổng ghi vào `metrics.llm` = `{"calls", "tokens_in", "tokens_out", "latency_s", "errors"}` (từ `gate_common.LLM_STATS`) để sau 2 tập có số thật rồi tối ưu.
- Mọi lời gọi LLM qua `gate_common.goi_llm_json` (task `"analysis"`, `temperature=0`, `tries_per_model=2`). Lỗi hạ tầng ném `QcError` → cổng báo `status="FAIL"` với `infra=True`, KHÔNG được coi là "0 lỗi" (bẫy 503 im lặng, memory `cong-b3q-phai-verify-bang-may`).
- Đường dẫn tuyệt đối: `E:\CLAUDE\YOUTUBE\h2dev\pipeline\` (gọi tắt `pipeline/`). Chạy test: `cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests -q`.
- Mọi script mới: đầu file `sys.stdout.reconfigure(encoding="utf-8")` trong try/except (Windows cp1252), đặt trong `pipeline/`, có docstring tiếng Việt không dấu hoặc có dấu nhất quán với file, CLI `--slug`, exit 1 khi FAIL, ghi JSON kết quả vào `<slug>/logs/`.
- Không sửa `render_engine.py`, `assemble.py`, `chay_buoc3.py`, `qc_visual.py`, `qc_script.py`.
- Định dạng kết quả cổng (dùng chung): `{"gate": str, "status": "PASS|WARN|FAIL|SKIPPED|ESCALATED", "attempt": int, "blocking_issues": [str], "warnings": [str], "metrics": {}, "infra": bool, "timestamp": ISO}`.

---


### Task 4: `qc_transcript.py` (B2Q) + sidecar segments từ `fetch_script.py`

**Files:**
- Modify: `pipeline/fetch_script.py:310-317` (thêm ghi sidecar; backup trước)
- Create: `pipeline/qc_transcript.py`
- Create: `pipeline/tests/test_qc_transcript.py`

**Interfaces:**
- Sidecar: `<out>.segments.json` = `{"video_id": str, "source": "api|ytdlp|whisper", "video_duration_sec": float, "segments": [{"start": float, "duration": float, "text": str}]}` — `video_duration_sec` lấy từ `fetch_script.video_minutes(vid)*60` (0 nếu không lấy được).
- `qc_transcript.do(seg_json: dict) -> (status, blocking, warnings, metrics)` với ngưỡng: `coverage < 0.80` → FAIL; `0.80 ≤ coverage < 0.92` → WARN; `max_gap > 45s` (bỏ 60s đầu/cuối) → WARN; `duplicate_ratio > 0.15` → FAIL; `chars_per_min < 120` → WARN; `video_duration_sec == 0` → coverage SKIPPED (WARN "khong co thoi luong").
- CLI: `py -3.13 qc_transcript.py --slug <dir>` đọc `competitor.segments.json`; thiếu sidecar → `SKIPPED` exit 0 (tập cũ); ghi `logs/B2Q_attempt_NNN.json`.

- [ ] **Step 1: Viết test thất bại**

```python
# pipeline/tests/test_qc_transcript.py
import json
from pathlib import Path
import qc_transcript as Q


def _seg(n, step=10.0, dup=False):
    segs = [{"start": i * step, "duration": step, "text": ("같은 문장 반복" if dup else f"문장 {i} 입니다")} for i in range(n)]
    return {"video_id": "x", "source": "api", "video_duration_sec": n * step, "segments": segs}


def test_pass():
    s, b, w, m = Q.do(_seg(100))
    assert s == "PASS" and b == [] and m["coverage"] >= 0.99


def test_cut_som_fail():
    d = _seg(100); d["video_duration_sec"] = 100 * 10 / 0.7
    s, b, _, m = Q.do(d)
    assert s == "FAIL" and any("coverage" in x for x in b) and m["coverage"] < 0.8


def test_gap_warn():
    d = _seg(100); d["segments"][50]["start"] += 60; d["segments"][50]["duration"] = 10
    for k in range(51, 100): d["segments"][k]["start"] += 60
    d["video_duration_sec"] = d["segments"][-1]["start"] + 10
    s, b, w, m = Q.do(d)
    assert s == "WARN" and m["max_gap_sec"] >= 60 and any("gap" in x for x in w)


def test_trung_lap_fail():
    s, b, _, m = Q.do(_seg(100, dup=True))
    assert s == "FAIL" and m["duplicate_ratio"] > 0.15


def test_khong_co_thoi_luong_warn():
    d = _seg(100); d["video_duration_sec"] = 0
    s, b, w, m = Q.do(d)
    assert s == "WARN" and m["coverage"] is None


def test_cli_skip_khi_khong_sidecar(tmp_path):
    assert Q.main(["--slug", str(tmp_path)]) == 0
    latest = json.loads((tmp_path / "logs" / "B2Q_latest.json").read_text(encoding="utf-8"))
    assert latest["status"] == "SKIPPED"
```

- [ ] **Step 2: Chạy test để thấy fail**

Run: `py -3.13 -m pytest tests/test_qc_transcript.py -q`
Expected: `ModuleNotFoundError: No module named 'qc_transcript'`

- [ ] **Step 3: Viết `qc_transcript.py`**

```python
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


def do(seg_json):
    segs = sorted((s for s in seg_json.get("segments", []) if isinstance(s, dict)), key=lambda s: float(s.get("start", 0)))
    dur = float(seg_json.get("video_duration_sec") or 0)
    blocking, warnings = [], []
    if not segs:
        return "FAIL", ["transcript rong"], [], {"n_seg": 0}
    last = float(segs[-1]["start"]) + float(segs[-1].get("duration", 0))
    text_all = " ".join(str(s.get("text", "")) for s in segs)
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
        end_a = float(a["start"]) + float(a.get("duration", 0))
        g = float(b["start"]) - end_a
        if 60 <= end_a and (dur == 0 or float(b["start"]) <= dur - 60) and g > max_gap:
            max_gap, gap_at = g, end_a
    if max_gap > 45:
        warnings.append(f"gap {max_gap:.0f}s khong co transcript tai {gap_at:.0f}s")
    texts = [str(s.get("text", "")).strip() for s in segs if len(str(s.get("text", "")).strip()) >= 8]
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
    status, blocking, warnings, metrics = do(json.loads(side.read_text(encoding="utf-8")))
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
```

- [ ] **Step 4: Chạy test**

Run: `py -3.13 -m pytest tests/test_qc_transcript.py -q`
Expected: `6 passed`

- [ ] **Step 5: Backup rồi sửa `fetch_script.py` ghi sidecar**

Run trước: `copy fetch_script.py _bak_fetch_script_%TIME:~0,2%%TIME:~3,2%.py` (PowerShell: `Copy-Item fetch_script.py ("_bak_fetch_script_" + (Get-Date -Format HHmm) + ".py")`).

Sửa `main()` — thay đoạn từ `out = Path(args.out) ...` đến `print(f"✓ ...")`:

```python
    out = Path(args.out) if args.out else Path(f"{vid}_transcript.txt")
    out.write_text(text, encoding="utf-8")
    # Sidecar cho cong B2Q (qc_transcript.py): moc thoi gian tung doan + thoi luong video. Ghi KEM,
    # khong doi dinh dang competitor.txt (moi tool khac van doc .txt nhu cu).
    try:
        dur_sec = round(video_minutes(vid, proxy=args.proxy or None) * 60, 1)
    except Exception:
        dur_sec = 0.0
    side = out.with_name(out.stem + ".segments.json")
    side.write_text(json.dumps({"video_id": vid, "source": used, "video_duration_sec": dur_sec,
                                "segments": [{"start": float(s["start"]), "duration": float(s.get("duration", 0)),
                                              "text": s["text"]} for s in segs]},
                               ensure_ascii=False), encoding="utf-8")
    print(f"✓ {vid} [{used}]: {len(segs)} đoạn, {len(text):,} ký tự → {out}  (+{side.name})")
```

Thêm `import json` ở đầu file nếu chưa có (`grep -n "^import json" fetch_script.py`).

- [ ] **Step 6: Kiểm thật (1 video ngắn, không tốn tiền)**

Run: `py -3.13 fetch_script.py Kmxva85WKec --lang ko --out ..\scratch_analysis\_regress_b2q\competitor.txt` rồi `py -3.13 qc_transcript.py --slug ..\scratch_analysis\_regress_b2q`
Expected: sidecar `competitor.segments.json` tồn tại; `=== B2Q: PASS` (hoặc WARN nếu YouTube tụt xuống whisper). Nếu bị 429 cả 3 đường → ghi nhận, dùng `--method whisper --whisper-model tiny` cho test.

---

