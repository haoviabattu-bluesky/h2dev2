# TASK 4 REPORT — `qc_transcript.py` (B2Q) + sidecar `.segments.json` tu `fetch_script.py`

Ngay: 2026-09-18 · Python: `py -3.13` · Thu muc: `E:\CLAUDE\YOUTUBE\h2dev\pipeline\`
Trang thai: **DONE_WITH_CONCERNS** (2 deviation nho so voi brief, ghi o muc 5)

## 1. File tao / sua

| File | Loai | Dong |
|---|---|---|
| `pipeline\qc_transcript.py` | TAO MOI | 112 |
| `pipeline\tests\test_qc_transcript.py` | TAO MOI | 49 |
| `pipeline\fetch_script.py` | SUA (2 hunk) | 323 → 335 |
| `pipeline\_bak_fetch_script_1406.py` | BACKUP (hash trung ban goc, verify `Get-FileHash` = True truoc khi sua) | 323 |

`gate_common.py` KHONG sua (chi import `ket_qua`, `ghi_log`). Khong dung `render_engine.py`, `assemble.py`,
`chay_buoc3.py`, `qc_visual.py`, `qc_script.py`.

Diff `fetch_script.py` (unified, n=0) so voi backup — dung 2 hunk nhu brief:

```
@@ -18,0 +19 @@
+import json
@@ -317 +318,12 @@
-    print(f"✓ {vid} [{used}]: {len(segs)} đoạn, {len(text):,} ký tự → {out}")
+    # Sidecar cho cong B2Q (qc_transcript.py): moc thoi gian tung doan + thoi luong video. Ghi KEM,
+    # khong doi dinh dang competitor.txt (moi tool khac van doc .txt nhu cu).
+    try:
+        dur_sec = round(video_minutes(vid, proxy=args.proxy or None) * 60, 1)
+    except Exception:
+        dur_sec = 0.0
+    side = out.with_name(out.stem + ".segments.json")
+    side.write_text(json.dumps({"video_id": vid, "source": used, "video_duration_sec": dur_sec,
+                                "segments": [{"start": float(s["start"]), "duration": float(s.get("duration", 0)),
+                                              "text": s["text"]} for s in segs]},
+                               ensure_ascii=False), encoding="utf-8")
+    print(f"✓ {vid} [{used}]: {len(segs)} đoạn, {len(text):,} ký tự → {out}  (+{side.name})")
```

`import json` chua co o dau file (grep `^import json` = 0) → da them. `competitor.txt` van la 1 dong
(kiem thuc: `txt lines: 1 chars: 13236`), dinh dang khong doi — sidecar chi ghi KEM.

## 2. pytest

Step 2 (truoc khi co module) — dung nhu ky vong:
```
tests\test_qc_transcript.py:4: in <module>
    import qc_transcript as Q
E   ModuleNotFoundError: No module named 'qc_transcript'
1 error in 0.08s
```

Step 4 lan 1 (code y brief) — **1 failed, 5 passed**: `test_pass` ra WARN thay vi PASS:
```
('WARN', [], ['mat do 41.4 ky tu/phut < 120 — qua thua, kha nang mat doan'],
 {'n_seg': 100, 'source': 'api', 'video_duration': 1000.0, 'last_timestamp': 1000.0,
  'coverage': 1.0, 'max_gap_sec': 0.0, 'duplicate_ratio': 0.0, 'chars_per_min': 41.4})
```
Nguyen nhan: fixture trong brief `"문장 {i} 입니다"` chi ~7 ky tu (bo space) / 10 giay = 41 ky tu/phut,
tu vi pham nguong `cpm < 120 → WARN` cua chinh brief → test_pass khong bao gio PASS duoc. Code
`do()` dung y ngưỡng, loi nam o fixture → sua toi thieu fixture (xem muc 5).

Step 4 sau khi sua fixture:
```
py -3.13 -m pytest tests/test_qc_transcript.py -q
......                                                                   [100%]
6 passed in 0.04s
```
Full suite (32 cu + 6 moi):
```
py -3.13 -m pytest tests -q
......................................                                   [100%]
38 passed in 0.23s
```
(chay lai sau khi hardening `do()` + sau khi sua `fetch_script.py`: van `38 passed in 0.23s`).

## 3. Kiem that (Step 6, co mang)

Fetch (duong 1 API an ngay, KHONG dinh 429, khong tut xuong whisper) — **3 giay**:
```
py -3.13 fetch_script.py Kmxva85WKec --lang ko --out ..\scratch_analysis\_regress_b2q\competitor.txt
✓ Kmxva85WKec [api]: 694 đoạn, 13,236 ký tự → ..\scratch_analysis\_regress_b2q\competitor.txt  (+competitor.segments.json)
────────────────────────────────────────────────────────────
7년을 남편처럼 산 사람의 장례식에서 저는 방명록에 아는 사람이라고 적었습니다. ... (800 ky tu dau)
elapsed: 3s
```
Sidecar `scratch_analysis\_regress_b2q\competitor.segments.json` (65.674 byte):
```
video_id=Kmxva85WKec  source=api  video_duration_sec=1734.0
segments: 694, first={'start': 0.12, 'duration': 4.96, 'text': '7년을 남편처럼 산 사람의 장례식에서'},
               last={'start': 1732.159, 'duration': 3.4, 'text': '오래오래 건강하세요.'}
```

QC tren thu muc moi:
```
py -3.13 qc_transcript.py --slug ..\scratch_analysis\_regress_b2q
=== B2Q: PASS · coverage=1.0 gap=0.0s dup=0.0 cpm=341.9
exit=0
```
`logs\B2Q_latest.json`: `{"gate":"B2Q","status":"PASS","attempt":1,"blocking_issues":[],"warnings":[],
"metrics":{"n_seg":694,"source":"api","video_duration":1734.0,"last_timestamp":1735.6,"coverage":1.0,
"max_gap_sec":0.0,"duplicate_ratio":0.0,"chars_per_min":341.9},"infra":false,"timestamp":"2026-09-18T14:06:41"}`

QC tren tap cu STT3 (khong co sidecar):
```
py -3.13 qc_transcript.py --slug ..\assets\satori_jp\simbot2-03-Kmxva85WKec
=== B2Q: SKIPPED (khong co sidecar)
exit=0
```
Chi ghi `logs\B2Q_attempt_001.json` + `B2Q_latest.json` (status SKIPPED, warning
`khong co competitor.segments.json (tap cu, fetch truoc P0)`); khong dung file nao khac trong tap.
(Chay lai lan 2 de xac nhan sau hardening → them `B2Q_attempt_002.json`, van SKIPPED exit 0.)

Kiem them (ngoai brief, de tu tin): sidecar hong `{not json` →
`=== B2Q: FAIL` + `✗ competitor.segments.json hong, khong doc duoc: Expecting property name ...` exit=1
(khong traceback).

## 4. Self-review

- `do()` khong nem loi: da probe `None`, `{}`, `{'segments': []}`, `{'segments': None}`,
  `{'segments': [None,'x',5]}`, seg thieu `start`, `video_duration_sec='abc'`, `duration=None`,
  `text=None` → tat ca tra ve tuple hop le (FAIL/WARN), 0 exception. **Ban code y brief NEM loi o 4/8
  case** (KeyError 'start', TypeError NoneType iterable, ValueError float, TypeError float None) → da
  hardening toi thieu (muc 5).
- Nguong dung brief: coverage `<0.80` FAIL / `<0.92` WARN · gap `>45s` (bo 60s dau/cuoi) WARN ·
  dup `>0.15` FAIL · cpm `<120` WARN · dur=0 → WARN + `coverage=None`. Khong doi con so nao.
- Sidecar ghi cho MOI lan fetch thanh cong (nam sau `out.write_text`, truoc print). `video_minutes`
  loi → `dur_sec=0.0` (B2Q se WARN "khong co thoi luong", khong gay chet fetch). `.txt` giu nguyen.
- Khong lam gi ngoai brief ngoai 2 deviation duoi.

## 5. Deviation so voi brief

1. **Fixture test `_seg()`** (tests/test_qc_transcript.py): doi text tu `"문장 {i} 입니다"` sang cau day
   du `"문장 {i} 입니다. 오늘은 날씨가 참 좋아서 산책을 나갔습니다."` (~27 ky tu/10s ≈ 160 cpm) — vi ly
   do o muc 2. Cac assert, so doan, step, `dup` text giu nguyen. Da ghi comment giai thich ngay trong test.
2. **Hardening `do()` + `main()`** (qc_transcript.py) de thoa muc "do() never raises on empty/odd input":
   - them helper `_f(v)` (float an toan, None/chuoi hong → 0.0); thay `float(s["start"])` bang
     `_f(s.get("start"))` o 4 cho; `str(s.get("text") or "")` thay `str(s.get("text",""))` (tranh dem
     chu `"None"`); `seg_json` khong phai dict → coi nhu `{}`; `segments=None` → `[]`.
   - `main()`: sidecar hong (JSON/OSError) → `FAIL` co blocking "…hong, khong doc duoc" + ghi log +
     exit 1, thay vi traceback (khop Global Constraint "output malformed = FAIL co hoc").
   Khong doi nguong/metric/format ket qua; 6 test + 32 test cu van pass.

## 6. Concerns

- `test_gap_warn` trong brief chi dat WARN vi gap; sau khi sua fixture cpm ≈ 151 (dur=1070s) nen
  khong lan WARN cpm — OK nhung neu sau nay ai giam text fixture thi test nay se WARN vi 2 ly do
  (van pass, chi kem ro rang).
- `coverage` bi `min(..., 1.0)`: `last_timestamp` (1735.6) > `video_duration` (1734.0) o video that
  (API tra duration seg cuoi vuot dau video 1.6s) → coverage 1.0. Binh thuong, ghi de biet.
- Sidecar `source` chi co gia tri `api|ytdlp|whisper` theo `fetch_any`; brief noi B2Q "WARN neu tut
  xuong whisper" nhung code `do()` KHONG co rule nao theo `source` (chi ghi vao metrics). Lan nay
  la `api` nen khong anh huong; neu muon whisper → WARN thi can 1 dong them (chua lam vi ngoai brief).
- Whisper path CHUA duoc kiem that lan nay (API an ngay) — sidecar tu whisper co `start/duration` tu
  `s.start`/`s.end - s.start` (float) nen ve ly thuyet ghi duoc; chua co so do thuc te.
- Thu muc `scratch_analysis\_regress_b2q\` (competitor.txt + .segments.json + logs/) de lai lam
  bang chung, khong xoa. Tap STT3 co them 2 file log `B2Q_attempt_001/002.json` + `B2Q_latest.json`.
