# TASK 2 BRIEF (trich tu plan 2026-09-18-p0-buoc1-gates.md)

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


### Task 2: `qc_img_doan.py` — cổng mapping ảnh↔đoạn: MECHANICAL FAIL / SUSPICIOUS / SEMANTIC (WARN-only + `would_block`)

**Files:**
- Create: `pipeline/qc_img_doan.py`
- Create: `pipeline/tests/test_qc_img_doan.py`

**Interfaces:**
- Consumes: `gate_common.{ket_qua, ghi_log, goi_llm_json, QcError, phan_bo_xen_ke, kiem_stale, llm_stats_snapshot}`, `sinh_neo.doc_doan(script_path) -> list[str]` (chia đoạn theo dòng trống — KHÔNG viết lại). ⚠️ **KHÔNG dùng `sinh_neo.doc_img_doan`** (trả dict, mất thứ tự, nuốt trùng tên).
- Produces:
  - `doc_pairs(path) -> (rows: list[dict], malformed: list[str])` — mỗi dòng không rỗng/không `#` thành `{"line_no": int, "ten": str, "so": int}` theo đúng thứ tự file; dòng không đúng khuôn `ten|so` (thiếu `|`, số không phải int, tên rỗng) → chuỗi `"dong <n>: <noi dung> — malformed"` trong `malformed`, KHÔNG bỏ qua im lặng, KHÔNG gộp trùng.
  - `kiem_co_hoc(rows, n_doan, n_prompt) -> (blocking: list[str], suspicious: list[str], metrics: dict)`
    - **MECHANICAL FAIL (blocking):** số dòng ≠ `n_prompt`; thiếu ID bắt buộc (tập ID hợp lệ = `001.png..NNN.png` với NNN=n_prompt, thiếu cái nào liệt kê cái đó); ID ngoài tập hợp lệ; trùng tên; `so` ngoài `[1..n_doan]`; `so` giảm theo thứ tự dòng (order invariant); `n_doan == 0` hoặc `n_prompt == 0` (required data thiếu).
    - **SUSPICIOUS (không chặn):** `gate_common.phan_bo_xen_ke(counts)` → `"SUSPICIOUS: phan bo xen ke deu (2,3,2,3…) — BAT BUOC semantic QC"`; ≥30% đoạn có 0 ảnh trong khi ≥1 đoạn có >6 ảnh → `"SUSPICIOUS: phan bo lech bat thuong (…)"`.
    - `metrics`: `n_anh, n_doan, n_prompt, phan_bo (list), doan_0_anh (list), chia_deu (bool)`.
  - `kiem_semantic(rows, doan, prompts, chunk=8) -> (warnings: list[str], thap: list[dict], n_checked: int)` — mỗi lời gọi LLM = 1 chunk 8 đoạn liên tiếp + toàn bộ ảnh đã map vào các đoạn đó; LLM trả điểm 1-5/ảnh; ≤2 → warning `"045.png (doan 15) 2/5: <ly do> — goi y doan X"` + phần tử `thap`. `n_checked` = tổng ảnh đã được chấm.
  - CLI: `py -3.13 qc_img_doan.py --slug <dir> [--mode warn|fail] [--no-llm] [--chunk 8]`
    - Thứ tự: `doc_pairs` → malformed → blocking; `kiem_stale` → blocking; `kiem_co_hoc`; nếu **không** blocking và không `--no-llm` → `kiem_semantic`.
    - `--mode warn` (mặc định, 2 tập đầu): semantic thấp chỉ WARN; `--mode fail`: `thap` không rỗng → blocking `"semantic: N anh diem <=2 (mode fail)"`.
    - `--no-llm` khi SUSPICIOUS → WARN thêm `"da bo qua semantic QC trong khi SUSPICIOUS — chua duoc coi la da kiem"`.
    - `metrics.semantic` = `{"ran", "n_checked", "n_warn", "n_would_block", "would_block": bool, "chunk", "thap", "llm": llm_stats_snapshot()}` — `would_block = len(thap) > 0` (nếu bật `--mode fail` thì gate có chặn không), ghi **cả khi mode warn** để sau 2 tập đếm được.
    - Kết quả ghi `logs/B55_mapping_attempt_NNN.json`; exit 1 khi `status == FAIL` (blocking hoặc LLM lỗi hạ tầng).

- [ ] **Step 1: Viết test thất bại**

```python
# pipeline/tests/test_qc_img_doan.py
import json, re
from pathlib import Path
import pytest
import qc_img_doan as Q
import gate_common as G


def _rows(counts):
    out, i = [], 1
    for doan, n in enumerate(counts, 1):
        for _ in range(n):
            out.append({"line_no": i, "ten": f"{i:03d}.png", "so": doan}); i += 1
    return out


def _viet(tmp_path, counts, n_doan=None, prompts=None):
    n_doan = n_doan or len(counts)
    rows = _rows(counts)
    (tmp_path / "script.txt").write_text("\n\n".join(f"doan {i}。" for i in range(1, n_doan + 1)), encoding="utf-8")
    (tmp_path / "img_prompts.txt").write_text("\n".join(prompts or [f"p{i}" for i in range(1, len(rows) + 1)]), encoding="utf-8")
    (tmp_path / "img_doan.txt").write_text("\n".join(f"{r['ten']}|{r['so']}" for r in rows), encoding="utf-8")
    return tmp_path


def test_doc_pairs_giu_thu_tu_va_trung(tmp_path):
    f = tmp_path / "img_doan.txt"
    f.write_text("# ghi chu\n002.png|3\n001.png|1\n002.png|3\n\nxyz\n004.png|abc\n|5\n", encoding="utf-8")
    rows, mal = Q.doc_pairs(f)
    assert [r["ten"] for r in rows] == ["002.png", "001.png", "002.png"]
    assert rows[0]["line_no"] == 2 and rows[1]["so"] == 1
    assert len(mal) == 3 and all("malformed" in m for m in mal) and "dong 6" in mal[0]


def test_co_hoc_dat():
    rows = _rows([2, 5, 3, 3, 2, 4, 3, 2, 5, 2, 2, 3, 4, 3, 3, 2, 3, 5, 2, 3, 3, 2])
    b, s, m = Q.kiem_co_hoc(rows, n_doan=22, n_prompt=len(rows))
    assert b == [] and s == [] and m["n_anh"] == len(rows) and m["chia_deu"] is False


def test_co_hoc_chia_deu_chi_suspicious():
    rows = _rows([2, 3] * 25)
    b, s, m = Q.kiem_co_hoc(rows, n_doan=50, n_prompt=128)
    assert b == [] and m["chia_deu"] is True and any("SUSPICIOUS" in x and "xen ke" in x for x in s)


def test_co_hoc_lech_bat_thuong_suspicious():
    counts = [0] * 8 + [9, 1, 2, 0, 1, 1, 1, 0, 1, 1, 1, 1]      # 10/20 doan 0 anh, 1 doan 9 anh
    b, s, m = Q.kiem_co_hoc(_rows(counts), n_doan=20, n_prompt=sum(counts))
    assert b == [] and any("lech bat thuong" in x for x in s)


def test_co_hoc_giam_ngoai_pham_vi_trung_thieu():
    rows = [{"line_no": 1, "ten": "001.png", "so": 1}, {"line_no": 2, "ten": "003.png", "so": 3},
            {"line_no": 3, "ten": "003.png", "so": 2}, {"line_no": 4, "ten": "009.png", "so": 9}]
    b, s, m = Q.kiem_co_hoc(rows, n_doan=5, n_prompt=4)
    j = " | ".join(b)
    assert "GIAM" in j and "ngoai pham vi" in j and "trung ten" in j
    assert "thieu ID" in j and "002.png" in j and "004.png" in j and "009.png" in j   # 009 ngoai tap hop le


def test_co_hoc_required_data_thieu():
    b, s, m = Q.kiem_co_hoc([], n_doan=0, n_prompt=0)
    assert any("required" in x.lower() or "thieu" in x for x in b)


def test_semantic_chunk_shortlist_va_n_checked(monkeypatch):
    doan = [f"doan {i} noi ve viec {i}" for i in range(1, 11)]
    prompts = [f"prompt {i}" for i in range(1, 21)]
    rows = [{"line_no": i, "ten": f"{i:03d}.png", "so": (i + 1) // 2} for i in range(1, 21)]
    calls = []
    def fake(prompt, **k):
        calls.append(prompt)
        ids = [int(x) for x in re.findall(r"\"id\":\s*(\d+)", prompt)]
        return [{"id": i, "score": 1 if i == 7 else 5, "reason": "r", "better_doan": 6 if i == 7 else None} for i in ids]
    monkeypatch.setattr(Q.G, "goi_llm_json", fake)
    warns, thap, n_checked = Q.kiem_semantic(rows, doan, prompts, chunk=8)
    assert len(calls) == 2 and n_checked == 20
    assert len(thap) == 1 and thap[0]["id"] == 7 and "007.png" in warns[0] and "doan 6" in warns[0]


def test_semantic_ha_tang_thanh_qcerror(monkeypatch):
    def boom(*a, **k): raise G.QcError("503")
    monkeypatch.setattr(Q.G, "goi_llm_json", boom)
    with pytest.raises(G.QcError):
        Q.kiem_semantic([{"line_no": 1, "ten": "001.png", "so": 1}], ["d1"], ["p1"])


def _fake_llm(sai_ids):
    def fake(prompt, **k):
        ids = [int(x) for x in re.findall(r"\"id\":\s*(\d+)", prompt)]
        return [{"id": i, "score": 1 if i in sai_ids else 5, "reason": "sai canh", "better_doan": None} for i in ids]
    return fake


def _latest(tmp_path):
    return json.loads((tmp_path / "logs" / "B55_mapping_latest.json").read_text(encoding="utf-8"))


def test_cli_suspicious_no_llm_warn(tmp_path):
    _viet(tmp_path, [2, 3] * 25)
    assert Q.main(["--slug", str(tmp_path), "--no-llm"]) == 0
    L = _latest(tmp_path)
    assert L["status"] == "WARN" and L["metrics"]["chia_deu"] is True
    assert any("SUSPICIOUS" in w for w in L["warnings"]) and any("bo qua semantic" in w for w in L["warnings"])


def test_cli_mode_warn_ghi_would_block(tmp_path, monkeypatch):
    _viet(tmp_path, [2, 3] * 25)
    monkeypatch.setattr(Q.G, "goi_llm_json", _fake_llm({10, 20, 30}))
    assert Q.main(["--slug", str(tmp_path)]) == 0                      # mode warn: khong chan
    L = _latest(tmp_path)
    s = L["metrics"]["semantic"]
    assert L["status"] == "WARN" and s["would_block"] is True and s["n_would_block"] == 3
    assert s["n_checked"] == 128 and s["n_warn"] == 3 and s["llm"]["calls"] >= 7


def test_cli_mode_fail_chan_theo_semantic(tmp_path, monkeypatch):
    _viet(tmp_path, [2, 3] * 25)
    monkeypatch.setattr(Q.G, "goi_llm_json", _fake_llm({10, 20, 30}))
    assert Q.main(["--slug", str(tmp_path), "--mode", "fail"]) == 1
    L = _latest(tmp_path)
    assert L["status"] == "FAIL" and any(b.startswith("semantic:") for b in L["blocking_issues"])


def test_cli_khong_fail_chi_vi_histogram(tmp_path, monkeypatch):
    _viet(tmp_path, [2, 3] * 25)
    monkeypatch.setattr(Q.G, "goi_llm_json", _fake_llm(set()))       # semantic sach
    assert Q.main(["--slug", str(tmp_path), "--mode", "fail"]) == 0
    L = _latest(tmp_path)
    assert L["status"] == "WARN" and L["metrics"]["semantic"]["would_block"] is False


def test_cli_malformed_va_stale_la_fail(tmp_path, monkeypatch):
    _viet(tmp_path, [1] * 20)
    (tmp_path / "img_doan.txt").write_text((tmp_path / "img_doan.txt").read_text(encoding="utf-8") + "\nhong", encoding="utf-8")
    assert Q.main(["--slug", str(tmp_path), "--no-llm"]) == 1
    assert any("malformed" in b for b in _latest(tmp_path)["blocking_issues"])
    _viet(tmp_path, [1] * 20)
    G.ghi_fingerprint(tmp_path)
    (tmp_path / "script.txt").write_text("\n\n".join(f"doan moi {i}。" for i in range(1, 21)), encoding="utf-8")
    assert Q.main(["--slug", str(tmp_path), "--no-llm"]) == 1
    assert any("STALE" in b for b in _latest(tmp_path)["blocking_issues"])
```

- [ ] **Step 2: Chạy test để thấy fail**

Run: `cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests/test_qc_img_doan.py -q`
Expected: `ModuleNotFoundError: No module named 'qc_img_doan'`

- [ ] **Step 3: Viết `qc_img_doan.py`**

```python
# -*- coding: utf-8 -*-
r"""qc_img_doan.py — cong QC MAPPING anh<->doan (B5.5), chot 2026-09-18 (P0).

Bang chung that STT3: ca 128 dong img_doan.txt duoc sinh bang cong thuc chia deu xen ke 2,3,2,3...
(khong doc noi dung) -> QC video B8Q bao 7/14 moc "anh lech loi". Khong cong nao truoc B8Q bat duoc,
tuc phai ton ca luot ve anh may 2 + ghep video moi lo.

BA TANG (anh chot 2026-09-18):
  MECHANICAL FAIL (0d, tat dinh, chan ngay tu tap dau): dong malformed · so dong != so prompt ·
    thieu/thua/trung ID · so doan ngoai [1..N] · so doan GIAM theo thu tu · STALE (hash script khac
    luc sinh artifact, gate_common.kiem_stale) · thieu required data.
  SUSPICIOUS (khong chan, BAT BUOC chay semantic): phan bo xen ke deu 2,3,2,3 (gate_common.phan_bo_xen_ke)
    · phan bo lech bat thuong (nhieu doan 0 anh + co doan >6 anh).
  SEMANTIC (LLM re, WARN-only 2 tap dau; --mode fail de chan): moi loi goi = 1 chunk 8 doan lien
    tiep + cac anh da map vao do -> cham 1-5 tung anh; <=2 = lech. KHONG ma tran 130x50 (~7 loi goi/tap).
    Luon ghi metrics.semantic.would_block de sau 2 tap biet neu bat blocking thi chan bao nhieu ca.

Parser TU DOC img_doan.txt (KHONG dung sinh_neo.doc_img_doan — no tra dict, mat thu tu, nuot trung).

  py -3.13 qc_img_doan.py --slug <tap> [--mode warn|fail] [--no-llm] [--chunk 8]
exit 0 = PASS/WARN · exit 1 = FAIL (blocking hoac LLM loi ha tang — khong duoc coi la dat)
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
import sinh_neo           # noqa: E402

GATE = "B55_mapping"


# ------------------------------------------------------------------ parser (giu thu tu + trung)
def doc_pairs(path):
    rows, malformed = [], []
    for n, ln in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if "|" not in s:
            malformed.append(f"dong {n}: {s[:40]!r} — malformed (thieu '|')"); continue
        ten, so = (x.strip() for x in s.split("|", 1))
        if not ten:
            malformed.append(f"dong {n}: {s[:40]!r} — malformed (ten rong)"); continue
        if not so.lstrip("-").isdigit():
            malformed.append(f"dong {n}: {s[:40]!r} — malformed (so doan khong phai so nguyen)"); continue
        rows.append({"line_no": n, "ten": ten, "so": int(so)})
    return rows, malformed


# ------------------------------------------------------------------ tang A: co hoc + suspicious
def kiem_co_hoc(rows, n_doan, n_prompt):
    blocking, suspicious = [], []
    if n_doan <= 0 or n_prompt <= 0:
        blocking.append(f"thieu required data: script co {n_doan} doan, img_prompts co {n_prompt} prompt")
        return blocking, suspicious, {"n_anh": len(rows), "n_doan": n_doan, "n_prompt": n_prompt,
                                      "phan_bo": [], "doan_0_anh": [], "chia_deu": False}
    ten = [r["ten"] for r in rows]
    if len(rows) != n_prompt:
        blocking.append(f"img_doan.txt co {len(rows)} dong nhung img_prompts.txt co {n_prompt} prompt")
    trung = [t for t, c in collections.Counter(ten).items() if c > 1]
    if trung:
        blocking.append(f"trung ten anh: {trung[:5]}")
    hop_le = {f"{i:03d}.png" for i in range(1, n_prompt + 1)}
    thieu = sorted(hop_le - set(ten))
    ngoai_id = sorted(set(ten) - hop_le)
    if thieu:
        blocking.append(f"thieu ID bat buoc ({len(thieu)}): {thieu[:6]}")
    if ngoai_id:
        blocking.append(f"ID ngoai tap hop le 001..{n_prompt:03d}.png ({len(ngoai_id)}): {ngoai_id[:6]}")
    ngoai = [(r["ten"], r["so"]) for r in rows if r["so"] < 1 or r["so"] > n_doan]
    if ngoai:
        blocking.append(f"{len(ngoai)} anh gan so doan ngoai pham vi 1..{n_doan}: {ngoai[:5]}")
    giam = [(a, b) for a, b in zip(rows, rows[1:]) if b["so"] < a["so"]]
    if giam:
        blocking.append(f"{len(giam)} cho so doan GIAM theo thu tu (anh di lui): "
                        + ", ".join(f"{a['ten']}={a['so']}->{b['ten']}={b['so']}" for a, b in giam[:4]))
    counts = [0] * n_doan
    for r in rows:
        if 1 <= r["so"] <= n_doan:
            counts[r["so"] - 1] += 1
    chia_deu = G.phan_bo_xen_ke(counts)
    if chia_deu:
        suspicious.append("SUSPICIOUS: phan bo anh/doan xen ke deu (2,3,2,3…) — dau hieu img_doan.txt sinh "
                          "bang cong thuc, khong doc noi dung; BAT BUOC chay semantic QC (khong --no-llm)")
    zero = [i + 1 for i, c in enumerate(counts) if c == 0]
    if n_doan >= 10 and len(zero) / n_doan >= 0.30 and max(counts) > 6:
        suspicious.append(f"SUSPICIOUS: phan bo lech bat thuong — {len(zero)}/{n_doan} doan 0 anh, "
                          f"co doan toi {max(counts)} anh; kiem lai bang semantic")
    metrics = {"n_anh": len(rows), "n_doan": n_doan, "n_prompt": n_prompt, "phan_bo": counts,
               "doan_0_anh": zero, "chia_deu": chia_deu}
    return blocking, suspicious, metrics


# ------------------------------------------------------------------ tang B: semantic (chunk)
def _prompt_chunk(doan_idx, doan, items):
    ds = "\n".join(f"[doan {i}] {doan[i - 1][:400]}" for i in doan_idx)
    ps = "\n".join(json.dumps({"id": i, "file": t, "doan": d, "prompt": p[:300]}, ensure_ascii=False)
                   for i, t, d, p in items)
    return (
        "Ban la bien tap vien kiem tra video ke chuyen tieng Nhat. Duoi day la cac DOAN kich ban (co so) "
        "va cac ANH da duoc gan vao tung doan. Voi MOI anh, cham 1-5: anh co minh hoa DUNG doan da gan "
        "khong (5 = dung canh/thoi diem/nhan vat; 3 = minh hoa chung chung hop khong khi; 1 = thuoc canh "
        "KHAC HAN cua cau chuyen). Neu <=2, chi ra doan nao TRONG DANH SACH duoi day hop hon "
        "(better_doan), khong co thi null.\n"
        "Chi tra ve JSON array, moi phan tu: {\"id\": <int>, \"score\": <1-5>, \"reason\": \"<=15 tu\", "
        "\"better_doan\": <int|null>}.\n\nDOAN:\n" + ds + "\n\nANH:\n" + ps)


def kiem_semantic(rows, doan, prompts, chunk=8):
    warnings, thap, n_checked = [], [], 0
    idx_of = {r["ten"]: i + 1 for i, r in enumerate(rows)}
    for start in range(1, len(doan) + 1, chunk):
        doan_idx = list(range(start, min(start + chunk, len(doan) + 1)))
        items = [(idx_of[r["ten"]], r["ten"], r["so"], prompts[idx_of[r["ten"]] - 1])
                 for r in rows if r["so"] in doan_idx and idx_of[r["ten"]] - 1 < len(prompts)]
        if not items:
            continue
        res = G.goi_llm_json(_prompt_chunk(doan_idx, doan, items))
        if not isinstance(res, list):
            raise G.QcError("LLM khong tra array")
        for r in res:
            try:
                i, sc = int(r["id"]), int(r["score"])
            except Exception:
                continue
            if not (1 <= i <= len(rows)):
                continue
            n_checked += 1
            if sc <= 2:
                t, d = rows[i - 1]["ten"], rows[i - 1]["so"]
                bd = r.get("better_doan")
                goi_y = f" — goi y doan {bd}" if bd else ""
                warnings.append(f"{t} (doan {d}) {sc}/5: {str(r.get('reason', ''))[:80]}{goi_y}")
                thap.append({"id": i, "file": t, "doan": d, "score": sc, "better_doan": bd,
                             "reason": r.get("reason", "")})
    return warnings, thap, n_checked


# ------------------------------------------------------------------ CLI
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--mode", default="warn", choices=["warn", "fail"])
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--chunk", type=int, default=8)
    a = ap.parse_args(argv)
    d = Path(a.slug)
    doan = sinh_neo.doc_doan(d / "script.txt") if (d / "script.txt").exists() else []
    prompts = [l for l in (d / "img_prompts.txt").read_text(encoding="utf-8").splitlines() if l.strip()] \
        if (d / "img_prompts.txt").exists() else []
    if not (d / "img_doan.txt").exists():
        kq = G.ket_qua(GATE, "FAIL", blocking=["thieu required artifact img_doan.txt"])
        G.ghi_log(d, GATE, kq); print(f"=== {GATE}: FAIL · thieu img_doan.txt"); return 1
    rows, malformed = doc_pairs(d / "img_doan.txt")
    blocking = list(malformed)
    b_stale, w_stale = G.kiem_stale(d)
    blocking += b_stale
    b_co, suspicious, metrics = kiem_co_hoc(rows, len(doan), len(prompts))
    blocking += b_co
    warnings = list(w_stale) + list(suspicious)
    metrics["suspicious"] = suspicious
    sem = {"ran": False, "n_checked": 0, "n_warn": 0, "n_would_block": 0, "would_block": False, "chunk": a.chunk}
    infra = False
    if not blocking and not a.no_llm:
        try:
            w_sem, thap, n_checked = kiem_semantic(rows, doan, prompts, a.chunk)
            warnings += w_sem
            sem.update(ran=True, n_checked=n_checked, n_warn=len(w_sem), n_would_block=len(thap),
                       would_block=bool(thap), thap=thap)
            if a.mode == "fail" and thap:
                blocking.append(f"semantic: {len(thap)} anh diem <=2 (mode fail)")
        except G.QcError as e:
            infra = True
            blocking.append(f"LLM khong cham duoc: {e}")
    elif a.no_llm and suspicious:
        warnings.append("da bo qua semantic QC (--no-llm) trong khi mapping SUSPICIOUS — chua duoc coi la da kiem")
    sem["llm"] = G.llm_stats_snapshot()
    metrics["semantic"] = sem
    status = "FAIL" if blocking else ("WARN" if warnings else "PASS")
    kq = G.ket_qua(GATE, status, blocking=blocking, warnings=warnings, metrics=metrics, infra=infra)
    G.ghi_log(d, GATE, kq)
    print(f"=== {GATE}: {status} · {metrics['n_anh']} anh / {metrics['n_doan']} doan"
          + (" · SUSPICIOUS" if suspicious else "")
          + f" · semantic checked={sem['n_checked']} warn={sem['n_warn']} would_block={sem['n_would_block']}"
          + f" · llm calls={sem['llm']['calls']} tok_in={sem['llm']['tokens_in']} "
            f"tok_out={sem['llm']['tokens_out']} latency={sem['llm']['latency_s']:.0f}s err={sem['llm']['errors']}")
    for b in blocking:
        print("  ✗", b)
    for w in warnings[:25]:
        print("  ⚠", w)
    return 1 if status == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Chạy test**

Run: `py -3.13 -m pytest tests/test_qc_img_doan.py -q`
Expected: `13 passed`.

- [ ] **Step 5: Chạy thật trên STT3 bản đã sửa tay — KHÔNG được false FAIL**

Run: `py -3.13 qc_img_doan.py --slug ..\assets\satori_jp\simbot2-03-Kmxva85WKec` (đã stamp ở Task 1)
Expected: `=== B55_mapping: PASS` hoặc `WARN`, KHÔNG có SUSPICIOUS, không blocking; `would_block` có thể True do vài ảnh minh hoạ (045.png cho phép). Ghi vào "Số đo thật": llm calls / tok_in / tok_out / latency / n_checked / n_warn / n_would_block / danh sách ảnh ≤2.

- [ ] **Step 6: Hồi quy bản LỖI 2-3-2-3 — phải SUSPICIOUS rồi FAIL theo semantic (`--mode fail`)**

Run:
```
py -3.13 -c "
from pathlib import Path
d=Path(r'..\assets\satori_jp\simbot2-03-Kmxva85WKec'); t=Path(r'..\scratch_analysis\_regress_stt3_img_doan'); t.mkdir(exist_ok=True)
for f in ('script.txt','img_prompts.txt'): (t/f).write_bytes((d/f).read_bytes())
c=[2,3]*25; i=1; out=[]
for doan,n in enumerate(c,1):
    for _ in range(n): out.append(f'{i:03d}.png|{doan}'); i+=1
(t/'img_doan.txt').write_text('\n'.join(out),encoding='utf-8'); print(t)"
py -3.13 gate_common.py --slug ..\scratch_analysis\_regress_stt3_img_doan --stamp
py -3.13 qc_img_doan.py --slug ..\scratch_analysis\_regress_stt3_img_doan --no-llm
py -3.13 qc_img_doan.py --slug ..\scratch_analysis\_regress_stt3_img_doan --mode fail
```
Expected: lệnh `--no-llm` → `WARN` + dòng SUSPICIOUS + "bo qua semantic" (KHÔNG FAIL chỉ vì đều); lệnh `--mode fail` → `FAIL`, blocking `semantic: N anh diem <=2` với N ≥ 5, và trong ⚠ có ≥3/6 ảnh 027/045/056/066/095/115 (6 ảnh QC video từng nêu). Nếu N < 5 hoặc <3/6 → sửa wording `_prompt_chunk`, không hạ chuẩn. Ghi số đo vào plan.

