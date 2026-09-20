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
