# -*- coding: utf-8 -*-
"""Phan loai tung dong img_prompts.txt: AI (giu anh AI) hay STOCK (thay bang video/anh that).
Marker @REF/@REF2/@GROK -> AI cung. Dong plain -> deepseek-v4-flash (ramclouds) phan loai theo lo.
Ra: stock_plan.tsv (line, group, reason, era, video_query, image_query) + phan_loai_log.txt
Dung: py -3.13 phan_loai_stock.py --slug <thu muc tap> [--out <thu muc>]
"""
import argparse, json, re, sys, time
from pathlib import Path
sys.path.insert(0, r"E:\CLAUDE\YOUTUBE\h2dev\pipeline")
import llm_client as L

SYS = ("You classify English image prompts for a Japanese elderly-storytelling YouTube video. "
       "Output ONLY a JSON array, no prose.")
RULE = """For each prompt decide:
- "group": "STOCK" ONLY if NO human, no face, no hand, no arm, no silhouette, no back view, no body part is visible in the frame (pure scenery / object / interior / exterior / nature). Any person, hand, figure, shadow of a person => "AI".
- "era": "historical" if the scene is clearly the past (1960s-1980s, flashback, old photo, memory); else "modern".
- "video_query": <=8 English words describing the place/object/action for a stock VIDEO search (no character names; add "japan" or "japanese" when the setting is Japanese).
- "image_query": <=8 English words for a stock PHOTO search, same rules.
Return a JSON array of objects {"line":N,"group":"AI"|"STOCK","era":"modern"|"historical","video_query":"...","image_query":"..."} covering EVERY line given, in order."""

def ask(batch, log):
    body = "\n".join(f"{n}: {p}" for n, p in batch)
    for k in range(2):
        t = time.time()
        # task="short" thay cho provider/model ghim cung (2026-09-26): ghim thang ramclouds:
        # gemini-3.8-flash lam chuoi fallback chi con DUNG MOT muc — ramclouds hong la buoc nay
        # chet han. Chuoi "short" van bat dau bang CHINH model do, chi khac la co nguoi do phia sau
        # (ns24 gemini -> ramclouds luna -> gpt-5.6-sol).
        r = L.chat(RULE + "\n\nPROMPTS:\n" + body, system=SYS, task="short",
                   max_tokens=6000, temperature=0, tries_per_model=2, verbose=False)
        txt = r.text.strip(); txt = re.sub(r"^```(?:json)?|```$", "", txt, flags=re.M).strip()
        try:
            arr = json.loads(txt)
            got = {int(o["line"]): o for o in arr if "line" in o}
            log.append(f"lo {batch[0][0]}-{batch[-1][0]}: {len(got)}/{len(batch)} dong, {time.time()-t:.1f}s, lan {k+1}")
            if len(got) >= len(batch) - 1:
                return got
        except Exception as e:
            log.append(f"lo {batch[0][0]}-{batch[-1][0]}: parse hong lan {k+1}: {e}")
    return {}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--slug", required=True); ap.add_argument("--out", default=str(Path(__file__).resolve().parent))
    ap.add_argument("--lo", type=int, default=25); a = ap.parse_args()
    ep = Path(a.slug); out = Path(a.out); T0 = time.time(); log = []
    lines = [l.rstrip("\n") for l in (ep / "img_prompts.txt").read_text(encoding="utf-8").splitlines()]
    plan = {}; plain = []
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if not s: plan[i] = ("AI", "empty", "modern", "", ""); continue
        if re.match(r"^@(REF2?|GROK)\b", s): plan[i] = ("AI", "marker", "modern", "", "")
        else: plain.append((i, s))
    calls = 0
    for b in range(0, len(plain), a.lo):
        batch = plain[b:b + a.lo]; calls += 1
        got = ask(batch, log)
        for n, _ in batch:
            o = got.get(n)
            if not o: plan[n] = ("AI", "llm_fail", "modern", "", ""); continue
            g = "STOCK" if str(o.get("group", "")).upper() == "STOCK" else "AI"
            plan[n] = (g, "llm", "historical" if str(o.get("era", "")).lower().startswith("hist") else "modern",
                       str(o.get("video_query", ""))[:80], str(o.get("image_query", ""))[:80])
    rows = ["line\tgroup\treason\tera\tvideo_query\timage_query"] + [f"{i}\t" + "\t".join(plan[i]) for i in sorted(plan)]
    (out / "stock_plan.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    from collections import Counter
    c = Counter(plan[i][0] + "/" + plan[i][1] for i in plan); era = Counter(plan[i][2] for i in plan if plan[i][0] == "STOCK")
    summ = f"tong {len(plan)} dong · " + " · ".join(f"{k}={v}" for k, v in sorted(c.items())) + f" · STOCK era: {dict(era)} · {calls} lan goi · {(time.time()-T0)/60:.1f} phut"
    log.append(summ); (out / "phan_loai_log.txt").write_text("\n".join(log) + "\n", encoding="utf-8"); print(summ)

if __name__ == "__main__": main()
