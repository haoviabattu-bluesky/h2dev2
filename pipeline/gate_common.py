# -*- coding: utf-8 -*-
r"""gate_common.py — phan dung chung cho MOI cong QC buoc 1 (chot 2026-09-18, P0).

Truoc day moi qc_*.py tu in "✗ ..." mot kieu, tu quyet retry mot kieu, khong luu lich su lan chay,
khong co bao cao escalation — nguoi doc phai doan lai tu log terminal. Module nay chuan hoa:
  - trang thai cong: PASS/WARN/FAIL/ESCALATED/SKIPPED (+PENDING/RUNNING cho orchestrator)
  - ket qua cong = 1 dict cung khuon, ghi <slug>/logs/<gate>_attempt_NNN.json (KHONG ghi de)
  - goi LLM tra JSON: bọc llm_client.chat, boc fence, loi ha tang -> QcError (khong bao gio la "0 loi")
  - ESCALATION_REPORT.md khi vong sua khong hoi tu
  - fingerprint SHA256 (artifact_meta.json): img_prompts/img_doan sinh tu script hash nao; hash
    script hien tai khac => STALE = FAIL co hoc, chan handoff. mtime chi la phu tro khi chua co meta.
  - phan_bo_xen_ke: phan bo anh/doan xen ke deu (2,3,2,3...) — CHI la dau hieu SUSPICIOUS/WARN bat
    buoc chay semantic QC, KHONG phai FAIL co hoc (anh chot 2026-09-18).
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
    # 2026-09-24: chuẩn hoá CRLF→LF trước khi băm. Trước đây băm byte thô, còn hook_stage._sha_file đọc
    # dạng văn bản (Python tự đổi CRLF→LF) → cùng 1 script lưu CRLF ra 2 mã khác nhau, cổng HOOK báo
    # "lỗi thời" oan trên máy 2 (kenko ep01). File LF: kết quả y hệt cũ, không lock cũ nào bị đổi.
    with open(path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def ghi_fingerprint(slug_dir, artifacts=ARTIFACTS_MAC_DINH):
    """Stamp sau khi B5/B5.5 xong: artifact nao sinh tu script co hash nao. Chi ghi file dang ton tai."""
    d = Path(slug_dir)
    p = d / META_NAME
    if not (d / "script.txt").exists():
        raise QcError(f"khong the stamp: thieu {d / 'script.txt'} (stamp chi co nghia sau khi co script)")
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
    """True = so anh/doan la mau CHIA DEU co hoc (dau hieu SUSPICIOUS, khong phai FAIL):
    (hang so tuyet doi) hoac (hai gia tri ke nhau k,k+1 chiem >= nguong tong so doan VA cac cap ke
    nhau xen ke khac nhau >= nguong — cho phep vai outlier). Duoi `toi_thieu` doan: khong ket luan.
    Do that: STT3 ban loi [2,3]*25 -> True; STT3 ban gan tay theo noi dung -> False."""
    c = [int(x) for x in counts]
    if len(c) < toi_thieu:
        return False
    vals = sorted(set(c))
    if len(vals) == 1:
        return True
    # Hai gia tri KE NHAU (k, k+1) chiem >= nguong tong so doan (cho phep vai outlier), VA cac cap
    # ke nhau xen ke khac nhau >= nguong. Chi xet "a != b" khong du: day do noi dung quyet dinh
    # (2,4,3,5,2,...) cung hiem khi co 2 doan lien tiep bang nhau nhung KHONG phai chia deu.
    import collections
    cnt = collections.Counter(c)
    best = max(((cnt[k] + cnt[k + 1], k) for k in vals), key=lambda t: t[0])
    if best[0] / len(c) < nguong:
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
        try:
            print("✓ stamp", ghi_fingerprint(a.slug))
        except QcError as e:
            print("  ✗", e)
            return 1
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


# ---------------------------------------------------------------- LOCK sau Sol PASS (flow=lean)
# NO_TEXT_MUTATION_AFTER_FINAL_SOL_PASS (anh chốt 2026-09-20): Sol PASS lần cuối → ghi sha256 script.txt vào
# script.lock.json. Mọi bước sau (B5W prompt ảnh, handoff…) gọi kiem_lock(); sha đổi = FINAL_QC_STALE. Lane không
# dùng flow lean thì không có lock → chỉ WARN (không làm gãy lane cũ).
LOCK_NAME = "script.lock.json"


def ghi_lock(slug_dir, state, **info):
    """state ∈ PASS | ESCALATE | BLOCK. Ghi kèm sha256 script.txt hiện tại."""
    d = Path(slug_dir)
    s = d / "script.txt"
    meta = {"state": state, "at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "script_sha256": sha256_file(s) if s.exists() else None, **info}
    (d / LOCK_NAME).write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def kiem_lock(slug_dir):
    """Trả (ok, msg, level). level: 'FAIL' khi có lock mà state≠PASS hoặc sha lệch (FINAL_QC_STALE);
    'WARN' khi chưa có lock (lane luồng cũ); 'PASS' khi khớp."""
    d = Path(slug_dir)
    f = d / LOCK_NAME
    if not f.exists():
        return True, f"chưa có {LOCK_NAME} (lane luồng cũ hoặc chưa qua Sol) — không khoá", "WARN"
    try:
        meta = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"{LOCK_NAME} hỏng: {e}", "FAIL"
    if meta.get("state") != "PASS":
        return False, f"script state={meta.get('state')} — kịch bản CHƯA được Sol PASS, không được sang pha asset", "FAIL"
    now = sha256_file(d / "script.txt") if (d / "script.txt").exists() else None
    if now != meta.get("script_sha256") and (d / "script.txt").exists():
        # 2026-09-24: lock ký TRƯỚC khi sha256_file chuẩn hoá CRLF→LF (băm byte thô). File CRLF không đổi 1 byte
        # nào vẫn ra mã mới khác → báo STALE oan (Lane G ep01). Chấp nhận mã byte thô nếu khớp lock.
        import hashlib
        raw = hashlib.sha256((d / "script.txt").read_bytes()).hexdigest()
        if raw == meta.get("script_sha256"):
            now = raw
    if now != meta.get("script_sha256"):
        return False, (f"FINAL_QC_STALE: script.txt đã bị sửa SAU Sol PASS ({str(meta.get('script_sha256'))[:10]}… → "
                       f"{str(now)[:10]}…) — cấm mọi mutation sau lock; chạy lại B3 (lean) để Sol chấm lại"), "FAIL"
    return True, f"lock PASS khớp sha {str(now)[:10]}… ({meta.get('at')})", "PASS"
