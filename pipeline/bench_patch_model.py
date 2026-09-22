"""bench_patch_model.py — A/B offline cho model S4. Lệnh: py -3.13 -X utf8 pipeline/bench_patch_model.py --model claude-opus-5 --sol [--eps assets/<lane>/epNN ...] [--max N]
Kết quả 2026-09-22 (Opus 5 vs Fable, 9 lượt): xem memory opus-s4-patch-ab-test + docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md §0.

A/B offline: replay các lượt S4 "patch theo Sol" đã có thật (script.pre_patchN.txt + qc_sol_report_k.txt)
bằng model khác (mặc định claude-opus-5), so với bản Fable đã tạo. KHÔNG ghi gì vào thư mục tập —
mọi output vào --out. Đo: từ chối?, chữ, % đoạn đổi, số mất, câu đổi trong/ngoài phạm vi Sol nêu, Sol chấm lại."""
import argparse, json, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_steps, claude_p_bridge, lean_script, profiles, qc_script_sol  # noqa
from llm_client import LLMError  # noqa

SENT = re.compile(r"[^。！？\n]+[。！？]?")


def sents(t):
    return [s.strip() for s in SENT.findall(t) if s.strip()]


def quotes(rep):
    """Chuỗi tiếng Nhật Sol trích trong 「」 ở phần ĐIỂM KHÔNG HỢP LÝ (bỏ GÓP Ý THÊM)."""
    body = rep.split("GÓP Ý THÊM")[0]
    return [q for q in re.findall(r"「([^」]{6,})」", body)]


def scope_stats(old, new, qs):
    so, sn = sents(old), set(sents(new))
    changed = [s for s in so if s not in sn]
    def in_scope(s):
        return any(q in s or s in q or (len(q) >= 10 and q[:10] in s) for q in qs)
    ins = [s for s in changed if in_scope(s)]
    return {"sent_total": len(so), "sent_changed": len(changed), "in_scope": len(ins),
            "out_scope": len(changed) - len(ins), "out_scope_samples": [s[:60] for s in changed if s not in ins][:5]}


def cases(ep_dirs):
    """Ghép (pre_patchN, sol_report_k, bản Fable = pre_patch{N+1} | script.txt) từ log lock."""
    out = []
    for d in ep_dirs:
        lk = d / "script.lock.json"
        if not lk.exists():
            continue
        log = json.load(open(lk, encoding="utf-8")).get("log", [])
        last_sol = None
        for l in log:
            m = re.match(r"sol(\d+) ", l)
            if m:
                last_sol = int(m.group(1)); continue
            m = re.match(r"patch(\d+) sol ", l)
            if m and last_sol:
                n = int(m.group(1))
                pre = d / f"script.pre_patch{n}.txt"
                nxt = d / f"script.pre_patch{n+1}.txt"
                fable = nxt if nxt.exists() else d / "script.txt"
                rep = d / f"qc_sol_report_{last_sol}.txt"
                if pre.exists() and rep.exists():
                    out.append({"dir": d, "n": n, "sol_k": last_sol, "pre": pre, "rep": rep, "fable": fable, "log": l})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--eps", nargs="*", default=[])
    ap.add_argument("--max", type=int, default=99)
    ap.add_argument("--sol", action="store_true", help="cho Sol chấm lại bản patch của model thử")
    ap.add_argument("--out", default=str(ROOT / "scratch_analysis" / "bench_patch_model"))
    a = ap.parse_args()
    outd = Path(a.out); outd.mkdir(exist_ok=True)
    dirs = [ROOT / e for e in a.eps] if a.eps else sorted(ROOT.glob("assets/*/ep*"))
    cs = cases(dirs)[: a.max]
    print(f"{len(cs)} case · model thử {a.model}")
    claude_p_bridge.patch_model_of = lambda p: a.model     # ép model S4 cho lượt chạy này
    rows = []
    for c in cs:
        d = c["dir"]; lane = d.parent.name
        prof = profiles.load(lane)
        st = json.load(open(d / "state.json", encoding="utf-8")) if (d / "state.json").exists() else {}
        minutes = (st.get("B0") or {}).get("minutes") or profiles.target_minutes(prof)
        ns = lean_script.ngan_sach(prof, profiles.target_chars(prof, minutes))
        old = c["pre"].read_text(encoding="utf-8"); rep = c["rep"].read_text(encoding="utf-8")
        fab = c["fable"].read_text(encoding="utf-8")
        qs = quotes(rep)
        tag = f"{lane}_{d.name}_p{c['n']}"
        print(f"\n=== {tag} (Sol lần {c['sol_k']}, {len(qs)} câu trích) · Fable: {c['log'][:60]}")
        row = {"case": tag, "sol_quotes": len(qs), "fable": scope_stats(old, fab, qs) | {"chars": ai_steps.measure(fab)["chars"],
               "doan": round(lean_script._tyle_doan_doi(old, fab), 3), "mat_so": sorted(lean_script._nums(old) - lean_script._nums(fab))[:6]}}
        viec = [f"Theo báo cáo Sol dưới đây, sửa TẠI CHỖ từng điểm KHÔNG HỢP LÝ được đánh số (bỏ qua mục GÓP Ý THÊM):\n{rep}"]
        log = []; t0 = time.time()
        try:
            new = lean_script.patch(prof, old, viec, "sol", ns, log, c["n"])
            (outd / f"{tag}.{a.model}.txt").write_text(new, encoding="utf-8")
            row["test"] = scope_stats(old, new, qs) | {"chars": ai_steps.measure(new)["chars"], "doan": round(lean_script._tyle_doan_doi(old, new), 3),
                          "mat_so": sorted(lean_script._nums(old) - lean_script._nums(new))[:6], "elapsed": round(time.time() - t0), "rejected": None}
            if a.sol:
                v, r2 = lean_script.sol_qc(prof, new, lean_script._title(d), outd / f"{tag}.{a.model}.sol.txt", ns, ai_steps.measure(new))
                row["test"]["sol_verdict"] = v
        except LLMError as e:
            row["test"] = {"rejected": str(e)[:160], "elapsed": round(time.time() - t0)}
        print(json.dumps(row, ensure_ascii=False, indent=1))
        rows.append(row)
        (outd / f"results.{a.model}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n=== TÓM TẮT")
    print(f"{'case':46} {'Fable đổi/ngoài':>16} {'Test đổi/ngoài':>16} {'chữ F/T':>13} {'Sol':>6}")
    for r in rows:
        f, t = r["fable"], r["test"]
        if t.get("rejected"):
            print(f"{r['case']:46} {f['sent_changed']:>7}/{f['out_scope']:<8} {'TỪ CHỐI':>16} {f['chars']:>6}/-     ")
        else:
            print(f"{r['case']:46} {f['sent_changed']:>7}/{f['out_scope']:<8} {t['sent_changed']:>7}/{t['out_scope']:<8} {f['chars']:>6}/{t['chars']:<6} {t.get('sol_verdict','-'):>6}")


if __name__ == "__main__":
    main()
