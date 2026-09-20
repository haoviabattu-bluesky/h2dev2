# TASK 1 BRIEF (trich tu plan 2026-09-18-p0-buoc1-gates.md)

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


### Task 1: `gate_common.py` — trạng thái, log attempt, LLM-JSON, escalation, rào mtime

**Files:**
- Create: `pipeline/gate_common.py`
- Create: `pipeline/tests/__init__.py` (rỗng)
- Create: `pipeline/tests/test_gate_common.py`

**Interfaces:**
- Produces:
  - `STATUS = ("PENDING","RUNNING","PASS","WARN","FAIL","ESCALATED","SKIPPED")`
  - `class QcError(RuntimeError)`
  - `ket_qua(gate: str, status: str, attempt=1, blocking=None, warnings=None, metrics=None, infra=False) -> dict`
  - `ghi_log(slug_dir: Path, gate: str, kq: dict) -> Path` — ghi `<slug>/logs/<gate>_attempt_NNN.json` (NNN tăng dần, không ghi đè) và `<slug>/logs/<gate>_latest.json`
  - `goi_llm_json(prompt: str, task="analysis", max_tokens=8000, timeout=600) -> dict|list` — gọi `llm_client.chat(..., temperature=0, tries_per_model=2, verbose=False)`, bóc JSON (kể cả trong ```json fence), ném `QcError` nếu hạ tầng/không phải JSON
  - `viet_escalation_report(slug_dir: Path, gate: str, attempts: list[dict], goi_y: str = "") -> Path` — ghi/nối `<slug>/ESCALATION_REPORT.md`
  - `LLM_STATS: dict` = `{"calls":0,"tokens_in":0,"tokens_out":0,"latency_s":0.0,"errors":0}` — `goi_llm_json` cộng dồn (từ `ChatResult.usage`/`.elapsed`); `llm_stats_snapshot() -> dict` trả bản sao để cổng ghi vào `metrics.llm`
  - `sha256_file(path: Path) -> str`
  - `ghi_fingerprint(slug_dir: Path, artifacts=("img_prompts.txt","img_doan.txt")) -> Path` — ghi/cập nhật `<slug>/artifact_meta.json` (khuôn ở Global Constraints), chỉ ghi artifact tồn tại
  - `kiem_stale(slug_dir: Path, artifacts=("img_prompts.txt","img_doan.txt")) -> (blocking: list[str], warnings: list[str])` — hash script hiện tại ≠ `generated_from_script_sha256` → blocking `"STALE: ..."`; artifact có trong meta nhưng `sha256` file đổi → warning (artifact sửa tay sau khi stamp, không chặn); **chưa có meta** → dùng `kiem_mtime_script_vs_prompts` làm phụ trợ: mtime báo lỗi → blocking, ngược lại warning `"chua co artifact_meta.json (fingerprint) — chay `py -3.13 gate_common.py --slug <d> --stamp` sau B5"`
  - `kiem_mtime_script_vs_prompts(slug_dir: Path) -> list[str]` — fast-check phụ trợ: `script.txt` mới hơn `img_prompts.txt`/`img_doan.txt` quá 2 giây
  - `phan_bo_xen_ke(counts: list[int]) -> bool` — True nếu dãy số ảnh/đoạn là mẫu chia đều cơ học (**chỉ dùng làm SUSPICIOUS/WARN**, không FAIL)
  - CLI: `py -3.13 gate_common.py --slug <d> --stamp` (ghi fingerprint) · `--check` (in kết quả `kiem_stale`, exit 1 nếu blocking)

- [ ] **Step 1: Viết test thất bại**

```python
# pipeline/tests/test_gate_common.py
import json, os, time
from pathlib import Path
import pytest
import gate_common as G


def test_ket_qua_schema():
    k = G.ket_qua("B5P", "WARN", attempt=2, warnings=["x"], metrics={"n": 1})
    assert k["gate"] == "B5P" and k["status"] == "WARN" and k["attempt"] == 2
    assert k["blocking_issues"] == [] and k["warnings"] == ["x"] and k["infra"] is False
    assert "timestamp" in k
    with pytest.raises(ValueError):
        G.ket_qua("B5P", "OK")


def test_ghi_log_khong_ghi_de(tmp_path):
    p1 = G.ghi_log(tmp_path, "B5P", G.ket_qua("B5P", "FAIL", blocking=["a"]))
    p2 = G.ghi_log(tmp_path, "B5P", G.ket_qua("B5P", "PASS"))
    assert p1.name == "B5P_attempt_001.json" and p2.name == "B5P_attempt_002.json"
    latest = json.loads((tmp_path / "logs" / "B5P_latest.json").read_text(encoding="utf-8"))
    assert latest["status"] == "PASS" and latest["attempt"] == 2


def test_goi_llm_json_boc_fence(monkeypatch):
    class R: text = "```json\n{\"a\": 1, \"b\": [1,2]}\n```"
    monkeypatch.setattr(G.llm_client, "chat", lambda *a, **k: R())
    assert G.goi_llm_json("x") == {"a": 1, "b": [1, 2]}


def test_goi_llm_json_loi_ha_tang(monkeypatch):
    def boom(*a, **k): raise G.llm_client.LLMError("het chuoi")
    monkeypatch.setattr(G.llm_client, "chat", boom)
    with pytest.raises(G.QcError):
        G.goi_llm_json("x")


def test_goi_llm_json_khong_phai_json(monkeypatch):
    class R: text = "toi khong biet"
    monkeypatch.setattr(G.llm_client, "chat", lambda *a, **k: R())
    with pytest.raises(G.QcError):
        G.goi_llm_json("x")


def test_escalation_report(tmp_path):
    att = [{"attempt": 1, "status": "FAIL", "blocking_issues": ["loi A", "loi B"]},
           {"attempt": 2, "status": "FAIL", "blocking_issues": ["loi A"]}]
    p = G.viet_escalation_report(tmp_path, "B3Q", att, goi_y="sua tay doan 3")
    t = p.read_text(encoding="utf-8")
    assert "B3Q" in t and "loi A" in t and "sua tay doan 3" in t and "attempt 2" in t.lower()
    G.viet_escalation_report(tmp_path, "B5P", att)
    assert p.read_text(encoding="utf-8").count("## ") >= 2


def test_mtime_rao(tmp_path):
    (tmp_path / "img_prompts.txt").write_text("p", encoding="utf-8")
    (tmp_path / "img_doan.txt").write_text("001.png|1", encoding="utf-8")
    time.sleep(0.05)
    (tmp_path / "script.txt").write_text("s", encoding="utf-8")
    now = time.time()
    os.utime(tmp_path / "script.txt", (now + 10, now + 10))
    loi = G.kiem_mtime_script_vs_prompts(tmp_path)
    assert len(loi) == 2 and "img_prompts.txt" in loi[0]
    os.utime(tmp_path / "img_prompts.txt", (now + 20, now + 20))
    os.utime(tmp_path / "img_doan.txt", (now + 20, now + 20))
    assert G.kiem_mtime_script_vs_prompts(tmp_path) == []


def test_phan_bo_xen_ke():
    assert G.phan_bo_xen_ke([2, 3] * 25) is True            # STT3 that: 2,3,2,3... 50 doan
    assert G.phan_bo_xen_ke([3, 2] * 10 + [5, 3]) is True     # 20/22 cap xen ke
    assert G.phan_bo_xen_ke([2, 5, 3, 3, 2, 4, 3, 2, 5, 2, 2, 3, 4, 3, 3, 2, 3, 5, 2, 3, 3, 2]) is False
    assert G.phan_bo_xen_ke([2, 3, 2, 3]) is False            # < 20 doan: khong ket luan
    assert G.phan_bo_xen_ke([3] * 30) is True                 # hang so tuyet doi cung la chia deu


def test_llm_stats_cong_don(monkeypatch):
    class R:
        text = "{\"ok\": 1}"; elapsed = 1.5
        usage = {"prompt_tokens": 100, "completion_tokens": 20}
    monkeypatch.setattr(G.llm_client, "chat", lambda *a, **k: R())
    truoc = G.llm_stats_snapshot()
    G.goi_llm_json("x"); G.goi_llm_json("y")
    sau = G.llm_stats_snapshot()
    assert sau["calls"] - truoc["calls"] == 2 and sau["tokens_in"] - truoc["tokens_in"] == 200
    assert sau["tokens_out"] - truoc["tokens_out"] == 40 and sau["latency_s"] - truoc["latency_s"] == 3.0
    def boom(*a, **k): raise G.llm_client.LLMError("x")
    monkeypatch.setattr(G.llm_client, "chat", boom)
    with pytest.raises(G.QcError):
        G.goi_llm_json("z")
    assert G.llm_stats_snapshot()["errors"] - sau["errors"] == 1


def _tap(tmp_path, script="s1", prompts="p1", doan="001.png|1"):
    (tmp_path / "script.txt").write_text(script, encoding="utf-8")
    (tmp_path / "img_prompts.txt").write_text(prompts, encoding="utf-8")
    (tmp_path / "img_doan.txt").write_text(doan, encoding="utf-8")
    return tmp_path


def test_fingerprint_stamp_va_stale(tmp_path):
    d = _tap(tmp_path)
    p = G.ghi_fingerprint(d)
    meta = json.loads(p.read_text(encoding="utf-8"))
    sha_s = G.sha256_file(d / "script.txt")
    assert meta["script_sha256"] == sha_s
    assert meta["artifacts"]["img_prompts.txt"]["generated_from_script_sha256"] == sha_s
    assert meta["artifacts"]["img_doan.txt"]["sha256"] == G.sha256_file(d / "img_doan.txt")
    b, w = G.kiem_stale(d)
    assert b == [] and w == []
    (d / "script.txt").write_text("s2 da sua", encoding="utf-8")       # script doi -> STALE
    b, w = G.kiem_stale(d)
    assert len(b) == 2 and all("STALE" in x for x in b)
    G.ghi_fingerprint(d)                                                # stamp lai -> het stale
    (d / "img_doan.txt").write_text("001.png|1\n002.png|1", encoding="utf-8")   # artifact sua tay
    b, w = G.kiem_stale(d)
    assert b == [] and len(w) == 1 and "img_doan.txt" in w[0]


def test_stale_chua_co_meta_dung_mtime(tmp_path):
    d = _tap(tmp_path)
    b, w = G.kiem_stale(d)                                    # chua stamp, mtime hop le -> chi warn
    assert b == [] and any("fingerprint" in x for x in w)
    now = time.time()
    os.utime(d / "script.txt", (now + 30, now + 30))          # script moi hon -> mtime chan
    b, w = G.kiem_stale(d)
    assert len(b) == 2 and "img_prompts.txt" in b[0]


def test_fingerprint_chi_ghi_artifact_ton_tai(tmp_path):
    (tmp_path / "script.txt").write_text("s", encoding="utf-8")
    (tmp_path / "img_prompts.txt").write_text("p", encoding="utf-8")
    meta = json.loads(G.ghi_fingerprint(tmp_path).read_text(encoding="utf-8"))
    assert "img_doan.txt" not in meta["artifacts"] and "img_prompts.txt" in meta["artifacts"]
```

- [ ] **Step 2: Chạy test để thấy fail**

Run: `cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests/test_gate_common.py -q`
Expected: `ModuleNotFoundError: No module named 'gate_common'`

- [ ] **Step 3: Viết `gate_common.py`**

```python
# -*- coding: utf-8 -*-
r"""gate_common.py — phan dung chung cho MOI cong QC buoc 1 (chot 2026-09-18, P0).

Truoc day moi qc_*.py tu in "✗ ..." mot kieu, tu quyet retry mot kieu, khong luu lich su lan chay,
khong co bao cao escalation — nguoi doc phai doan lai tu log terminal. Module nay chuan hoa:
  - trang thai cong: PASS/WARN/FAIL/ESCALATED/SKIPPED (+PENDING/RUNNING cho orchestrator)
  - ket qua cong = 1 dict cung khuon, ghi <slug>/logs/<gate>_attempt_NNN.json (KHONG ghi de)
  - goi LLM tra JSON: bọc llm_client.chat, boc fence, loi ha tang -> QcError (khong bao gio la "0 loi")
  - ESCALATION_REPORT.md khi vong sua khong hoi tu
  - 2 rule CO HOC chac chan (anh chot FAIL ngay): script.txt moi hon img_prompts/img_doan;
    phan bo anh/doan xen ke deu (dau hieu img_doan.txt sinh bang cong thuc, khong doc noi dung)
"""
import datetime as _dt
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import llm_client  # noqa: E402

STATUS = ("PENDING", "RUNNING", "PASS", "WARN", "FAIL", "ESCALATED", "SKIPPED")


class QcError(RuntimeError):
    """Loi HA TANG (mang/model/JSON hong) — tach hẳn khoi phat hien noi dung."""


def ket_qua(gate, status, attempt=1, blocking=None, warnings=None, metrics=None, infra=False):
    if status not in STATUS:
        raise ValueError(f"status la {status!r}, phai thuoc {STATUS}")
    return {
        "gate": gate, "status": status, "attempt": int(attempt),
        "blocking_issues": list(blocking or []), "warnings": list(warnings or []),
        "metrics": dict(metrics or {}), "infra": bool(infra),
        "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
    }


def ghi_log(slug_dir, gate, kq):
    logs = Path(slug_dir) / "logs"
    logs.mkdir(exist_ok=True)
    n = 1 + len(list(logs.glob(f"{gate}_attempt_*.json")))
    kq = dict(kq, attempt=n)
    p = logs / f"{gate}_attempt_{n:03d}.json"
    p.write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
    (logs / f"{gate}_latest.json").write_text(json.dumps(kq, ensure_ascii=False, indent=1),
                                              encoding="utf-8")
    return p


def _boc_json(txt):
    t = re.sub(r"^```(json)?|```$", "", (txt or "").strip(), flags=re.MULTILINE).strip()
    m = re.search(r"[\[{].*[\]}]", t, re.DOTALL)
    if not m:
        raise QcError(f"LLM tra ve khong phai JSON: {t[:200]}")
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError as e:
        raise QcError(f"JSON hong: {e}") from None


LLM_STATS = {"calls": 0, "tokens_in": 0, "tokens_out": 0, "latency_s": 0.0, "errors": 0}


def llm_stats_snapshot():
    return dict(LLM_STATS)


def goi_llm_json(prompt, task="analysis", max_tokens=8000, timeout=600):
    """Goi LLM re tra JSON. Cong don LLM_STATS de sau 2 tap co so that (calls/token/latency/loi)."""
    LLM_STATS["calls"] += 1
    try:
        r = llm_client.chat(prompt, task=task, max_tokens=max_tokens, temperature=0,
                            timeout=timeout, tries_per_model=2, verbose=False)
    except llm_client.LLMError as e:
        LLM_STATS["errors"] += 1
        raise QcError(f"LLM het chuoi fallback: {str(e)[:200]}") from None
    except Exception as e:
        LLM_STATS["errors"] += 1
        raise QcError(f"LLM loi {type(e).__name__}: {str(e)[:200]}") from None
    u = getattr(r, "usage", None) or {}
    LLM_STATS["tokens_in"] += int(u.get("prompt_tokens") or 0)
    LLM_STATS["tokens_out"] += int(u.get("completion_tokens") or 0)
    LLM_STATS["latency_s"] += float(getattr(r, "elapsed", 0) or 0)
    try:
        return _boc_json(r.text)
    except QcError:
        LLM_STATS["errors"] += 1
        raise


# ---------------------------------------------------------------- fingerprint (artifact stale)
META_NAME = "artifact_meta.json"
ARTIFACTS_MAC_DINH = ("img_prompts.txt", "img_doan.txt")


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ghi_fingerprint(slug_dir, artifacts=ARTIFACTS_MAC_DINH):
    """Stamp sau khi B5/B5.5 xong: artifact nao sinh tu script co hash nao. Chi ghi file dang ton tai."""
    d = Path(slug_dir)
    p = d / META_NAME
    meta = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"artifacts": {}}
    sha_s = sha256_file(d / "script.txt")
    meta["script_sha256"] = sha_s
    meta["stamped_at"] = _dt.datetime.now().isoformat(timespec="seconds")
    meta.setdefault("artifacts", {})
    for a in artifacts:
        f = d / a
        if f.exists():
            meta["artifacts"][a] = {"generated_from_script_sha256": sha_s, "sha256": sha256_file(f)}
    p.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def kiem_stale(slug_dir, artifacts=ARTIFACTS_MAC_DINH):
    """Hash script hien tai != hash luc sinh artifact => STALE (blocking). mtime chi la phu tro
    khi chua co artifact_meta.json (tap cu)."""
    d = Path(slug_dir)
    s = d / "script.txt"
    if not s.exists():
        return [], []
    p = d / META_NAME
    if not p.exists():
        loi = kiem_mtime_script_vs_prompts(d)
        return loi, [] if loi else [f"chua co {META_NAME} (fingerprint) — chay `py -3.13 gate_common.py "
                                    f"--slug <tap> --stamp` sau khi xong B5/B5.5"]
    meta = json.loads(p.read_text(encoding="utf-8"))
    sha_now = sha256_file(s)
    blocking, warnings = [], []
    for a in artifacts:
        f = d / a
        if not f.exists():
            continue
        m = (meta.get("artifacts") or {}).get(a)
        if not m:
            warnings.append(f"{a} chua duoc stamp trong {META_NAME}")
            continue
        if m.get("generated_from_script_sha256") != sha_now:
            blocking.append(f"STALE: {a} sinh tu script.txt hash {str(m.get('generated_from_script_sha256'))[:10]}… "
                            f"nhung script.txt hien tai la {sha_now[:10]}… — script da sua sau khi viet {a}, "
                            f"phai ra soat/viet lai {a} roi stamp lai")
        elif m.get("sha256") != sha256_file(f):
            warnings.append(f"{a} da sua tay sau khi stamp (script khong doi) — chay --stamp lai de ghi nhan")
    return blocking, warnings


def viet_escalation_report(slug_dir, gate, attempts, goi_y=""):
    p = Path(slug_dir) / "ESCALATION_REPORT.md"
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"## {gate} — escalation {now}", "",
             f"Tu sua {len(attempts)} luot, KHONG hoi tu. Chuyen sang xem tay (Claude interactive/nguoi).",
             ""]
    for a in attempts:
        lines.append(f"### attempt {a.get('attempt', '?')} — {a.get('status', '?')}")
        for b in a.get("blocking_issues", []):
            lines.append(f"- {b}")
        for w in a.get("warnings", []):
            lines.append(f"- (warn) {w}")
        lines.append("")
    if goi_y:
        lines += ["**Goi y xem gi:** " + goi_y, ""]
    old = p.read_text(encoding="utf-8") if p.exists() else "# ESCALATION REPORT\n\n"
    p.write_text(old + "\n".join(lines) + "\n", encoding="utf-8")
    return p


def kiem_mtime_script_vs_prompts(slug_dir, do_tre_s=2.0):
    """script.txt sua SAU khi da viet prompt/img_doan => prompt viet tren ban script CU.
    Bang chung that STT3: img_prompts 16/09 18:36 < script 16/09 20:45 -> 3 anh mau thuan cot truyen."""
    d = Path(slug_dir)
    s = d / "script.txt"
    if not s.exists():
        return []
    ms = s.stat().st_mtime
    loi = []
    for f in ("img_prompts.txt", "img_doan.txt"):
        p = d / f
        if p.exists() and ms - p.stat().st_mtime > do_tre_s:
            loi.append(f"script.txt ({_dt.datetime.fromtimestamp(ms):%m-%d %H:%M}) MOI HON {f} "
                       f"({_dt.datetime.fromtimestamp(p.stat().st_mtime):%m-%d %H:%M}) — {f} dang "
                       f"bam ban script cu, phai ra soat/viet lai {f} sau khi sua script")
    return loi


def phan_bo_xen_ke(counts, toi_thieu=20, nguong=0.9):
    """True = so anh/doan la mau CHIA DEU co hoc: chi 1-2 gia tri khac nhau, va (hang so) hoac
    (xen ke k,k+1 deu dan >= nguong cac cap ke nhau). Duoi `toi_thieu` doan thi khong ket luan."""
    c = [int(x) for x in counts]
    if len(c) < toi_thieu:
        return False
    vals = sorted(set(c))
    if len(vals) == 1:
        return True
    if len(vals) != 2 or vals[1] - vals[0] != 1:
        return False
    xen = sum(1 for a, b in zip(c, c[1:]) if a != b)
    return xen / (len(c) - 1) >= nguong


# ---------------------------------------------------------------- CLI
def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--stamp", action="store_true", help="ghi fingerprint sau khi xong B5/B5.5")
    ap.add_argument("--check", action="store_true", help="kiem STALE (exit 1 neu chan)")
    a = ap.parse_args(argv)
    if a.stamp:
        print("✓ stamp", ghi_fingerprint(a.slug))
    if a.check or not a.stamp:
        b, w = kiem_stale(a.slug)
        for x in b:
            print("  ✗", x)
        for x in w:
            print("  ⚠", x)
        print("=== STALE-CHECK:", "FAIL" if b else ("WARN" if w else "PASS"))
        return 1 if b else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Chạy test**

Run: `cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests/test_gate_common.py -q`
Expected: `12 passed`

- [ ] **Step 5: Kiểm thật trên STT3 (thay commit)**

Run: `cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 gate_common.py --slug ..\assets\satori_jp\simbot2-03-Kmxva85WKec --check`
Expected: `=== STALE-CHECK: WARN` với 1 dòng ⚠ "chua co artifact_meta.json" (tập cũ chưa stamp; mtime hợp lệ vì prompt/img_doan sửa sau script ngày 18/09). Sau đó `--stamp` rồi `--check` lại → `PASS`. Nếu `--check` đầu ra FAIL → đọc lại mtime, không sửa code cho hợp.

---

