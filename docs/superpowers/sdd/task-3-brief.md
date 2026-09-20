# TASK 3 BRIEF (trich tu plan 2026-09-18-p0-buoc1-gates.md)

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


### Task 3: `qc_prompt_consistency.py` — cổng B5P: prompt ↔ story facts (PROMPT_CONFLICT), WARN-only + `would_block`

**Trách nhiệm (anh chốt 2026-09-18):** B5P kiểm **prompt tự nó có sai cốt truyện không** (script/story facts ↔ `img_prompts.txt`) → nguyên nhân `PROMPT_CONFLICT`. Việc "prompt đúng nhưng gán nhầm đoạn" là của B5.5 (`qc_img_doan.py`, `MAPPING_MISMATCH`) — B5P KHÔNG chấm mapping. Ca không chắc → `AMBIGUOUS` (WARN, KHÔNG tính vào `would_block`).

**Files:**
- Create: `pipeline/qc_prompt_consistency.py`
- Create: `pipeline/tests/test_qc_prompt_consistency.py`

**Interfaces:**
- Consumes: `gate_common.{ket_qua, ghi_log, goi_llm_json, QcError, kiem_stale, llm_stats_snapshot}`, `sinh_neo.doc_doan`, `qc_img_doan.doc_pairs(path) -> (rows, malformed)` (tái dùng parser Task 2 để lấy đoạn của từng prompt làm NGỮ CẢNH — không kiểm mapping).
- Produces:
  - `kiem_co_hoc(prompts, rows, characters) -> list[str]` — MECHANICAL FAIL: số prompt ≠ số dòng img_doan (khi có img_doan.txt); dòng `@REF2` mà `characters.json` < 2 nhân vật; `@REF` mà 0 nhân vật; prompt rỗng.
  - `sinh_facts(doan, characters, chunk=10) -> dict` — `{"characters": {...}, "timeline": [{"doan": i, "location", "time", "season", "facts": [str]}]}`; 1 lời gọi/10 đoạn; gộp; đúng số đoạn (thiếu → `{"doan": i, "facts": []}`).
  - `kiem_prompts(prompts, rows, facts, characters, batch=15) -> (warnings: list[str], conflicts: list[dict], ambiguous: list[dict], n_checked: int)` — mỗi batch 15 prompt liên tiếp + facts của dải đoạn `[min−1 .. max+1]` mà batch map tới (theo `rows`; không có img_doan → dải theo tỉ lệ vị trí) + facts nhân vật toàn cục. LLM trả từng prompt `{"id", "status": "PASS|FAIL|AMBIGUOUS", "conflicts": [{"type": "character_state|age|relationship|location|time|season|object|money|count|plot", "detail"}]}`. FAIL → warning `"022.png (doan 6) PROMPT_CONFLICT: location: sa mac A Rap ≠ Tohoku"` + phần tử `conflicts` (có `"category": "PROMPT_CONFLICT"`); AMBIGUOUS → warning `"... AMBIGUOUS: <ly do>"` + phần tử `ambiguous` (KHÔNG would_block).
  - CLI: `py -3.13 qc_prompt_consistency.py --slug <dir> [--mode warn|fail] [--no-llm] [--reuse-facts] [--batch 15] [--chunk 10]`
    - Thứ tự: đọc prompts/rows/characters → `kiem_co_hoc` → `kiem_stale` (blocking) → (không blocking, không `--no-llm`) `sinh_facts` (ghi `story_facts.json`; `--reuse-facts` đọc lại nếu có) → `kiem_prompts`.
    - `--mode warn` (mặc định): FAIL của LLM chỉ WARN; `--mode fail`: `conflicts` không rỗng → blocking `"semantic: N prompt PROMPT_CONFLICT (mode fail)"`. AMBIGUOUS không bao giờ chặn.
    - `metrics.semantic` = `{"ran", "n_checked", "n_warn", "n_would_block", "n_ambiguous", "would_block", "batch", "chunk", "conflicts", "ambiguous", "llm": llm_stats_snapshot()}` — ghi cả khi mode warn.
    - Ghi `logs/B5P_attempt_NNN.json`; exit 1 khi `status == FAIL`.

- [ ] **Step 1: Viết test thất bại**

```python
# pipeline/tests/test_qc_prompt_consistency.py
import json, re
from pathlib import Path
import pytest
import qc_prompt_consistency as Q
import gate_common as G

CHARS = {"characters": [{"name": "Shizue", "age": 73, "gender": "F", "master": "_ref/001.png"}]}


def _rows(n, per=2):
    return [{"line_no": i, "ten": f"{i:03d}.png", "so": (i + per - 1) // per} for i in range(1, n + 1)]


def test_co_hoc_ref_va_so_luong():
    prompts = ["@REF a", "@REF2 b", "c"]
    rows = _rows(3)
    loi = Q.kiem_co_hoc(prompts, rows, CHARS)
    assert any("@REF2" in x for x in loi) and not any("@REF " in x for x in loi)
    assert Q.kiem_co_hoc(prompts, rows[:2], CHARS)[0].startswith("img_prompts.txt co 3")
    assert Q.kiem_co_hoc(prompts, None, CHARS) == [x for x in Q.kiem_co_hoc(prompts, None, CHARS) if "@REF2" in x]
    assert any("rong" in x for x in Q.kiem_co_hoc(["a", "   "], _rows(2), CHARS))


def test_sinh_facts_chunk(monkeypatch):
    doan = [f"doan {i}" for i in range(1, 24)]
    calls = []
    def fake(prompt, **k):
        calls.append(prompt)
        ids = [int(x) for x in re.findall(r"\[doan (\d+)\]", prompt)]
        return {"characters": {"Shizue": {"age": 73}},
                "timeline": [{"doan": i, "location": "home", "time": "day", "season": "", "facts": [f"f{i}"]} for i in ids if i != 5]}
    monkeypatch.setattr(Q.G, "goi_llm_json", fake)
    f = Q.sinh_facts(doan, CHARS, chunk=10)
    assert len(calls) == 3 and len(f["timeline"]) == 23 and f["timeline"][22]["doan"] == 23
    assert f["timeline"][4] == {"doan": 5, "facts": []} and f["characters"]["Shizue"]["age"] == 73


def test_kiem_prompts_batch_conflict_ambiguous(monkeypatch):
    prompts = [f"p{i}" for i in range(1, 33)]
    rows = _rows(32)                                                   # doan 1..16
    facts = {"characters": {}, "timeline": [{"doan": i, "facts": [f"f{i}"]} for i in range(1, 17)]}
    calls = []
    def fake(prompt, **k):
        calls.append(prompt)
        ids = [int(x) for x in re.findall(r"\"id\":\s*(\d+)", prompt)]
        out = []
        for i in ids:
            if i == 20:
                out.append({"id": i, "status": "FAIL", "conflicts": [{"type": "character_state", "detail": "chong da mat"}]})
            elif i == 21:
                out.append({"id": i, "status": "AMBIGUOUS", "conflicts": [{"type": "object", "detail": "khong ro"}]})
            else:
                out.append({"id": i, "status": "PASS", "conflicts": []})
        return out
    monkeypatch.setattr(Q.G, "goi_llm_json", fake)
    warns, conf, amb, n = Q.kiem_prompts(prompts, rows, facts, CHARS, batch=15)
    assert len(calls) == 3 and n == 32                                  # 32/15 = 3 batch
    assert "[doan 9]" in calls[1] and "[doan 4]" not in calls[1]        # batch 2 = prompt 16-30 -> doan 8-15 (+-1)
    assert len(conf) == 1 and conf[0]["id"] == 20 and conf[0]["category"] == "PROMPT_CONFLICT"
    assert len(amb) == 1 and amb[0]["id"] == 21
    assert any("020.png" in w and "PROMPT_CONFLICT" in w and "chong da mat" in w for w in warns)
    assert any("021.png" in w and "AMBIGUOUS" in w for w in warns)


def _tap(tmp_path, prompts=("@REF a", "b")):
    (tmp_path / "script.txt").write_text("d1\n\nd2", encoding="utf-8")
    (tmp_path / "img_prompts.txt").write_text("\n".join(prompts), encoding="utf-8")
    (tmp_path / "img_doan.txt").write_text("001.png|1\n002.png|2", encoding="utf-8")
    (tmp_path / "characters.json").write_text(json.dumps(CHARS), encoding="utf-8")
    return tmp_path


def _latest(tmp_path):
    return json.loads((tmp_path / "logs" / "B5P_latest.json").read_text(encoding="utf-8"))


def _fake_chat(fail_ids, amb_ids=()):
    class R:
        def __init__(self, text): self.text = text
    def fake(prompt, **k):
        if "[doan" in prompt and "\"id\"" not in prompt:                 # loi goi facts
            ids = [int(x) for x in re.findall(r"\[doan (\d+)\]", prompt)]
            return R(json.dumps({"characters": {}, "timeline": [{"doan": i, "facts": []} for i in ids]}))
        ids = [int(x) for x in re.findall(r"\"id\":\s*(\d+)", prompt)]
        return R(json.dumps([{"id": i, "status": "FAIL" if i in fail_ids else ("AMBIGUOUS" if i in amb_ids else "PASS"),
                              "conflicts": [{"type": "plot", "detail": "x"}] if i in fail_ids or i in amb_ids else []} for i in ids]))
    return fake


def test_cli_warn_only_ghi_would_block(tmp_path, monkeypatch):
    _tap(tmp_path)
    monkeypatch.setattr(Q.G.llm_client, "chat", _fake_chat({2}, {1}))
    assert Q.main(["--slug", str(tmp_path)]) == 0
    L = _latest(tmp_path); s = L["metrics"]["semantic"]
    assert L["status"] == "WARN" and s["ran"] and s["n_checked"] == 2
    assert s["n_would_block"] == 1 and s["would_block"] is True and s["n_ambiguous"] == 1 and s["n_warn"] == 2
    assert s["llm"]["calls"] >= 2 and (tmp_path / "story_facts.json").exists()
    assert Q.main(["--slug", str(tmp_path), "--mode", "fail", "--reuse-facts"]) == 1
    assert any(b.startswith("semantic:") for b in _latest(tmp_path)["blocking_issues"])


def test_cli_ambiguous_khong_chan(tmp_path, monkeypatch):
    _tap(tmp_path)
    monkeypatch.setattr(Q.G.llm_client, "chat", _fake_chat(set(), {1, 2}))
    assert Q.main(["--slug", str(tmp_path), "--mode", "fail"]) == 0
    s = _latest(tmp_path)["metrics"]["semantic"]
    assert s["would_block"] is False and s["n_ambiguous"] == 2


def test_cli_no_llm_va_stale(tmp_path):
    _tap(tmp_path)
    assert Q.main(["--slug", str(tmp_path), "--no-llm"]) == 0
    assert _latest(tmp_path)["metrics"]["semantic"]["ran"] is False
    G.ghi_fingerprint(tmp_path)
    (tmp_path / "script.txt").write_text("d1 sua\n\nd2", encoding="utf-8")
    assert Q.main(["--slug", str(tmp_path), "--no-llm"]) == 1
    assert any("STALE" in b for b in _latest(tmp_path)["blocking_issues"])
```

- [ ] **Step 2: Chạy test để thấy fail**

Run: `cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests/test_qc_prompt_consistency.py -q`
Expected: `ModuleNotFoundError: No module named 'qc_prompt_consistency'`

- [ ] **Step 3: Viết `qc_prompt_consistency.py`**

```python
# -*- coding: utf-8 -*-
r"""qc_prompt_consistency.py — cong B5P: prompt anh co MAU THUAN cot truyen khong (P0, 2026-09-18).

TRACH NHIEM (anh chot): B5P kiem PROMPT TU NO co sai story facts khong -> PROMPT_CONFLICT.
Prompt dung nhung gan nham doan la viec cua B5.5 (qc_img_doan.py, MAPPING_MISMATCH) — o day KHONG cham
mapping; img_doan.txt chi dung lam NGU CANH (prompt nay nam quanh doan nao) de rut facts lien quan.
Khong chac -> AMBIGUOUS: WARN, KHONG tinh would_block.

Bang chung that STT3: 112-114 ve "to khai dang ky ket hon" (ca truyen chua bao gio dang ky) · 022
"sa mac A Rap" (script: cong truong Tohoku/Kawaguchi) · 028 "ca phe goi" (script: tra houjicha).
Khong cong nao truoc do bat duoc.

CACH LAM (khong ma tran 130x50): (1) story facts: 1 loi goi / 10 doan -> story_facts.json; (2) kiem
prompt theo batch 15 + facts cua dai doan lien quan (+-1) + facts nhan vat toan cuc.
Co hoc (FAIL ngay): so prompt != so dong img_doan; @REF/@REF2 thieu nhan vat; prompt rong; STALE.
Mode mac dinh WARN (2 tap dau). Luon ghi metrics.semantic.would_block.

  py -3.13 qc_prompt_consistency.py --slug <tap> [--mode warn|fail] [--no-llm] [--reuse-facts] [--batch 15] [--chunk 10]
"""
import argparse
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
import qc_img_doan        # noqa: E402  (doc_pairs — parser img_doan giu thu tu)

GATE = "B5P"


def kiem_co_hoc(prompts, rows, characters):
    loi = []
    if rows is not None and len(prompts) != len(rows):
        loi.append(f"img_prompts.txt co {len(prompts)} prompt nhung img_doan.txt co {len(rows)} dong")
    chars = (characters or {}).get("characters") or []
    for i, p in enumerate(prompts, 1):
        s = p.strip()
        if not s:
            loi.append(f"dong {i}: prompt rong")
        elif s.startswith("@REF2") and len(chars) < 2:
            loi.append(f"dong {i} co @REF2 nhung characters.json chi co {len(chars)} nhan vat")
        elif s.startswith("@REF ") and len(chars) < 1:
            loi.append(f"dong {i} co @REF nhung characters.json khong co nhan vat nao")
    return loi


def _prompt_facts(doan_idx, doan, characters):
    ds = "\n".join(f"[doan {i}] {doan[i - 1]}" for i in doan_idx)
    ch = json.dumps((characters or {}).get("characters") or [], ensure_ascii=False)[:1500]
    return (
        "Doc cac doan kich ban tieng Nhat (co so) va rut ra SU KIEN CO THAT trong truyen de sau nay "
        "doi chieu voi anh minh hoa. Tra ve JSON: {\"characters\": {<ten>: {\"age\":..,\"gender\":..,"
        "\"status\": \"alive|deceased|unknown\",\"role\":..}}, \"timeline\": [{\"doan\": <so>, "
        "\"location\": \"..\", \"time\": \"..\", \"season\": \"..\", \"facts\": [\"<su kien/trang thai/"
        "do vat/dia diem quan trong, <=12 tu>\", ...]}]} — moi doan mot phan tu timeline, dung so doan da cho. "
        "Ghi RO cac dia danh, do vat, thuc uong, giay to duoc nhac ten (vd 'tra houjicha', 'cong truong "
        "Tohoku') vi anh minh hoa se bi doi chieu tung chi tiet.\n"
        f"Nhan vat da khai: {ch}\n\nDOAN:\n{ds}")


def sinh_facts(doan, characters, chunk=10):
    facts = {"characters": {}, "timeline": []}
    for start in range(1, len(doan) + 1, chunk):
        idx = list(range(start, min(start + chunk, len(doan) + 1)))
        r = G.goi_llm_json(_prompt_facts(idx, doan, characters))
        if not isinstance(r, dict):
            raise G.QcError("facts khong phai object")
        for k, v in (r.get("characters") or {}).items():
            facts["characters"].setdefault(k, {}).update(v if isinstance(v, dict) else {"note": v})
        got = {}
        for t in (r.get("timeline") or []):
            try:
                got[int(t.get("doan", 0))] = t
            except Exception:
                continue
        for i in idx:
            t = got.get(i) or {"doan": i, "facts": []}
            t["doan"] = i
            facts["timeline"].append(t)
    return facts


def _prompt_kiem(items, facts_slice, characters_facts):
    ps = "\n".join(json.dumps({"id": i, "file": t, "doan": d, "prompt": p[:350]}, ensure_ascii=False)
                   for i, t, d, p in items)
    fs = "\n".join(f"[doan {t['doan']}] loc={t.get('location','')} time={t.get('time','')} "
                   f"season={t.get('season','')} facts={t.get('facts', [])}" for t in facts_slice)
    return (
        "Ban kiem tra PROMPT VE ANH cho video ke chuyen. Voi MOI prompt, doi chieu voi SU KIEN CUA "
        "TOAN TRUYEN (nhan vat, song/chet, tuoi, quan he, dia danh/boi canh, thoi diem, mua, do vat/giay "
        "to/thuc uong duoc nhac ten, tien, so nguoi). CHI xet prompt CO SAI SU THAT CUA TRUYEN khong — "
        "KHONG cham viec prompt co dung doan da gan hay khong (viec do co cong khac lo).\n"
        "FAIL khi prompt mau thuan truc tiep: ve nguoi da mat con song o thoi diem sau; ve giay to/su viec "
        "KHONG he co trong truyen (vd to khai ket hon trong khi truyen noi ro chua bao gio dang ky); "
        "dia danh/boi canh khac han truyen (vd sa mac nuoc ngoai trong khi truyen noi cong truong trong "
        "nuoc); do vat/thuc uong cu the khac han truyen (vd ca phe goi trong khi truyen noi tra houjicha); "
        "sai mua/thoi diem; sai so nguoi/quan he.\n"
        "AMBIGUOUS khi prompt co chi tiet khong xuat hien trong truyen nhung KHONG mau thuan (minh hoa "
        "chung chung, montage doi thuong, do vat phu hop boi canh) hoac ban khong du du kien de ket luan.\n"
        "PASS khi khop hoac chi la canh vat/do vat hop boi canh.\n"
        "Chi tra JSON array: [{\"id\": <int>, \"status\": \"PASS|FAIL|AMBIGUOUS\", \"conflicts\": "
        "[{\"type\": \"character_state|age|relationship|location|time|season|object|money|count|plot\", "
        "\"detail\": \"<=20 tu, neu ro prompt noi gi vs truyen noi gi>\"}]}]\n"
        f"NHAN VAT (toan truyen): {json.dumps(characters_facts, ensure_ascii=False)[:2000]}\n"
        f"SU KIEN THEO DOAN:\n{fs}\n\nPROMPT:\n{ps}")


def kiem_prompts(prompts, rows, facts, characters, batch=15):
    warnings, conflicts, ambiguous, n_checked = [], [], [], 0
    tl = {int(t["doan"]): t for t in facts.get("timeline", [])}
    n_doan = max(tl) if tl else 1
    if rows:
        doan_of = {i + 1: r["so"] for i, r in enumerate(rows)}
    else:  # khong co img_doan.txt: uoc dai doan theo vi tri
        doan_of = {i: max(1, round(i * n_doan / max(len(prompts), 1))) for i in range(1, len(prompts) + 1)}
    ten_of = {i + 1: (rows[i]["ten"] if rows and i < len(rows) else f"{i + 1:03d}.png") for i in range(len(prompts))}
    for start in range(1, len(prompts) + 1, batch):
        ids = list(range(start, min(start + batch, len(prompts) + 1)))
        items = [(i, ten_of[i], doan_of.get(i, 0), prompts[i - 1]) for i in ids]
        ds = [doan_of.get(i, 0) for i in ids if doan_of.get(i, 0)]
        lo, hi = (max(1, min(ds) - 1), max(ds) + 1) if ds else (1, 1)
        fslice = [tl[k] for k in range(lo, hi + 1) if k in tl]
        res = G.goi_llm_json(_prompt_kiem(items, fslice, facts.get("characters", {})))
        if not isinstance(res, list):
            raise G.QcError("LLM khong tra array")
        for r in res:
            try:
                i = int(r["id"])
            except Exception:
                continue
            if not (1 <= i <= len(prompts)):
                continue
            n_checked += 1
            st = str(r.get("status", "PASS")).upper()
            c = [x for x in (r.get("conflicts") or []) if isinstance(x, dict)]
            chi_tiet = "; ".join(f"{x.get('type','?')}: {x.get('detail','')}" for x in c)[:160]
            rec = {"id": i, "file": ten_of[i], "doan": doan_of.get(i), "conflicts": c}
            if st == "FAIL":
                rec["category"] = "PROMPT_CONFLICT"
                warnings.append(f"{ten_of[i]} (doan {doan_of.get(i, '?')}) PROMPT_CONFLICT: {chi_tiet}")
                conflicts.append(rec)
            elif st == "AMBIGUOUS":
                rec["category"] = "AMBIGUOUS"
                warnings.append(f"{ten_of[i]} (doan {doan_of.get(i, '?')}) AMBIGUOUS: {chi_tiet}")
                ambiguous.append(rec)
    return warnings, conflicts, ambiguous, n_checked


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--mode", default="warn", choices=["warn", "fail"])
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--reuse-facts", action="store_true")
    ap.add_argument("--batch", type=int, default=15)
    ap.add_argument("--chunk", type=int, default=10)
    a = ap.parse_args(argv)
    d = Path(a.slug)
    if not (d / "img_prompts.txt").exists() or not (d / "script.txt").exists():
        kq = G.ket_qua(GATE, "FAIL", blocking=["thieu required artifact script.txt/img_prompts.txt"])
        G.ghi_log(d, GATE, kq); print(f"=== {GATE}: FAIL · thieu script/img_prompts"); return 1
    doan = sinh_neo.doc_doan(d / "script.txt")
    prompts = [l for l in (d / "img_prompts.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    rows, malformed = (qc_img_doan.doc_pairs(d / "img_doan.txt") if (d / "img_doan.txt").exists() else (None, []))
    cj = d / "characters.json"
    characters = json.loads(cj.read_text(encoding="utf-8")) if cj.exists() else {}
    blocking = list(malformed) + kiem_co_hoc(prompts, rows, characters)
    b_stale, w_stale = G.kiem_stale(d)
    blocking += b_stale
    warnings = list(w_stale)
    sem = {"ran": False, "n_checked": 0, "n_warn": 0, "n_would_block": 0, "n_ambiguous": 0,
           "would_block": False, "batch": a.batch, "chunk": a.chunk, "conflicts": [], "ambiguous": []}
    infra = False
    if not blocking and not a.no_llm:
        try:
            fp = d / "story_facts.json"
            if a.reuse_facts and fp.exists():
                facts = json.loads(fp.read_text(encoding="utf-8"))
            else:
                facts = sinh_facts(doan, characters, a.chunk)
                fp.write_text(json.dumps(facts, ensure_ascii=False, indent=1), encoding="utf-8")
            w_sem, conflicts, ambiguous, n_checked = kiem_prompts(prompts, rows, facts, characters, a.batch)
            warnings += w_sem
            sem.update(ran=True, n_checked=n_checked, n_warn=len(w_sem), n_would_block=len(conflicts),
                       n_ambiguous=len(ambiguous), would_block=bool(conflicts), conflicts=conflicts, ambiguous=ambiguous)
            if a.mode == "fail" and conflicts:
                blocking.append(f"semantic: {len(conflicts)} prompt PROMPT_CONFLICT (mode fail)")
        except G.QcError as e:
            infra = True
            blocking.append(f"LLM khong kiem duoc: {e}")
    sem["llm"] = G.llm_stats_snapshot()
    status = "FAIL" if blocking else ("WARN" if warnings else "PASS")
    kq = G.ket_qua(GATE, status, blocking=blocking, warnings=warnings,
                   metrics={"n_prompt": len(prompts), "n_doan": len(doan), "semantic": sem}, infra=infra)
    G.ghi_log(d, GATE, kq)
    print(f"=== {GATE}: {status} · {len(prompts)} prompt / {len(doan)} doan"
          f" · checked={sem['n_checked']} warn={sem['n_warn']} would_block={sem['n_would_block']} ambiguous={sem['n_ambiguous']}"
          f" · llm calls={sem['llm']['calls']} tok_in={sem['llm']['tokens_in']} tok_out={sem['llm']['tokens_out']} "
          f"latency={sem['llm']['latency_s']:.0f}s err={sem['llm']['errors']}")
    for b in blocking:
        print("  ✗", b)
    for w in warnings[:30]:
        print("  ⚠", w)
    return 1 if status == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Chạy test**

Run: `py -3.13 -m pytest tests/test_qc_prompt_consistency.py -q`
Expected: `6 passed`

- [ ] **Step 5: Hồi quy BẮT BUỘC trên bản prompt CŨ (5 lỗi production đã xác nhận: 022, 028, 112, 113, 114)**

Tạo bản copy `scratch_analysis/_regress_stt3_b5p_old` từ STT3 với 112-114 trả về nội dung cũ (022/028 hiện vẫn đang sai trong file thật nên giữ nguyên):
```
py -3.13 -c "
from pathlib import Path
d=Path(r'..\assets\satori_jp\simbot2-03-Kmxva85WKec'); t=Path(r'..\scratch_analysis\_regress_stt3_b5p_old'); t.mkdir(exist_ok=True)
for f in ('script.txt','img_doan.txt','characters.json'): (t/f).write_bytes((d/f).read_bytes())
L=(d/'img_prompts.txt').read_text(encoding='utf-8').splitlines()
L[111]='CLOSE-UP of a folded Japanese marriage registration form inside a clear plastic ziplock bag, a bright red hanko seal already stamped in the husband line, cinematic ultra-realistic color, 16:9, no text'
L[112]='CLOSE-UP of the empty witness fields and empty date field on a folded Japanese marriage registration form spread carefully on a low table, cinematic ultra-realistic color, 16:9, no text'
L[113]='@REF MEDIUM shot of the elderly Japanese woman holding the folded marriage registration form corner with trembling fingertips at a low table in her apartment, cinematic ultra-realistic color, 16:9, no text'
(t/'img_prompts.txt').write_text('\n'.join(L),encoding='utf-8'); print(t)"
py -3.13 gate_common.py --slug ..\scratch_analysis\_regress_stt3_b5p_old --stamp
py -3.13 qc_prompt_consistency.py --slug ..\scratch_analysis\_regress_stt3_b5p_old
```
Expected: `=== B5P: WARN` (mode warn), và trong ⚠ **đủ 5/5**: `022.png`, `028.png`, `112.png`, `113.png`, `114.png` với nhãn `PROMPT_CONFLICT` (không phải AMBIGUOUS). Thiếu cái nào → sửa wording `_prompt_kiem`/`_prompt_facts` (nhấn đúng loại chi tiết bị sót: địa danh / thức uống / giấy tờ không có trong truyện), chạy lại; KHÔNG hạ chuẩn, KHÔNG sửa test. Ghi: calls / tok_in / tok_out / latency / n_checked / n_warn / n_would_block / n_ambiguous.

- [ ] **Step 6: Bản ĐÃ SỬA — không được false FAIL**

Tạo `scratch_analysis/_regress_stt3_b5p_fixed` từ STT3 thật (112-114 đã sửa thành vị bài thờ) và sửa thêm 022/028 cho đúng script:
```
py -3.13 -c "
from pathlib import Path
d=Path(r'..\assets\satori_jp\simbot2-03-Kmxva85WKec'); t=Path(r'..\scratch_analysis\_regress_stt3_b5p_fixed'); t.mkdir(exist_ok=True)
for f in ('script.txt','img_doan.txt','characters.json'): (t/f).write_bytes((d/f).read_bytes())
L=(d/'img_prompts.txt').read_text(encoding='utf-8').splitlines()
L[21]='WIDE shot of Japanese construction workers in helmets and khaki work clothes at a 1970s Tohoku Japan building site, wooden scaffolding and a crane under an overcast sky, cinematic ultra-realistic color, photorealistic, 8K, warm emotional lighting, authentic Japanese setting, 16:9, no text'
L[27]='CLOSE-UP of a small ceramic teapot pouring hot houjicha roasted green tea into a cup beside a slice of yokan sweet bean jelly on a low table, weathered elderly hands nearby, cinematic ultra-realistic color, photorealistic, 8K, warm emotional lighting, authentic Japanese setting, 16:9, no text'
(t/'img_prompts.txt').write_text('\n'.join(L),encoding='utf-8'); print(t)"
py -3.13 gate_common.py --slug ..\scratch_analysis\_regress_stt3_b5p_fixed --stamp
py -3.13 qc_prompt_consistency.py --slug ..\scratch_analysis\_regress_stt3_b5p_fixed --mode fail
```
Expected: exit 0 (`PASS` hoặc `WARN` chỉ vì AMBIGUOUS), **không** có `022/028/112/113/114` trong PROMPT_CONFLICT; `n_would_block` nhỏ (≤3). Nếu vẫn báo PROMPT_CONFLICT cho prompt đã đúng → đó là false positive: ghi rõ prompt nào + lý do LLM vào report, sửa wording cho rõ ranh giới AMBIGUOUS vs FAIL, chạy lại. Ghi số đo. (Việc sửa 022/028 trong file THẬT của STT3 là việc nội dung, KHÔNG làm trong task này — chỉ sửa trong bản copy hồi quy.)

