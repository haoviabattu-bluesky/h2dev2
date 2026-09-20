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
        "Tohoku') vi anh minh hoa se bi doi chieu tung chi tiet. CHI ghi dung nhung gi van ban NOI; KHONG "
        "suy dien them chat lieu/hinh thuc/dia diem/mua ma van ban khong neu (vd van ban chi noi 'tin nhan "
        "ngan' thi ghi 'tin nhan ngan', khong tu them 'giay viet tay'; doan khong neu dia diem thi de "
        "location rong).\n"
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
        "CHI FAIL khi facts NOI RO mot gia tri KHAC cho CUNG chi tiet do (cung mot canh/do vat/giay to/dia "
        "diem/nguoi thuc hien). Neu facts IM LANG ve chi tiet do (khong nhac toi; location rong hoac chi la "
        "suy doan tu boi canh; chi tiet co the thuoc doan khac cua truyen) thi la AMBIGUOUS, KHONG FAIL.\n"
        "AMBIGUOUS khi prompt co chi tiet khong xuat hien trong truyen nhung KHONG mau thuan (minh hoa "
        "chung chung, montage doi thuong, do vat phu hop boi canh) hoac ban khong du du kien de ket luan.\n"
        "PASS khi khop hoac chi la canh vat/do vat hop boi canh.\n"
        "Chi tra JSON array: [{\"id\": <int>, \"status\": \"PASS|FAIL|AMBIGUOUS\", \"conflicts\": "
        "[{\"type\": \"character_state|age|relationship|location|time|season|object|money|count|plot\", "
        "\"detail\": \"<=20 tu, neu ro prompt noi gi vs truyen noi gi>\"}]}]. Voi FAIL va AMBIGUOUS, "
        "conflicts LUON co it nhat 1 phan tu neu ly do (AMBIGUOUS: vi sao khong ket luan duoc); "
        "PASS thi conflicts = [].\n"
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
