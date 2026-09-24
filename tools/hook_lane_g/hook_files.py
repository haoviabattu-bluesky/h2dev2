# -*- coding: utf-8 -*-
"""Lớp 1 (Claude Code) — dựng file cho hook GHÉP TRƯỚC final.mp4 từ 1 kế hoạch cảnh viết tay (Lane G, 2026-09-24).

Đầu vào: <tập>/hook/hook_plan.json (Claude Code viết sau khi đọc hook_locked.txt + hook_voice.srt + script.txt):
  {"doc": "...", "fix": {"chữ STT sai": "chữ đúng"},
   "shots": [{"n":1, "ref":"@REF|@REF2|@REF12|", "img":"prompt ảnh (được dùng {MAIN} {MENTOR} {WIFE})",
              "ky_vong":"kỳ vọng tiếng Việt cho QC", "motion":"prompt chuyển động Grok", "cues":[c0,c1]}]}
Ra: img_prompts_hook.txt · hook_timeline.json (mốc = giữa 2 cue, không cắt ngang từ) · grok_jobs.csv (bản storyboard cũ giữ .bak)

    py -3.13 hook_files.py <thư mục tập>
"""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(r"E:\CLAUDE\YOUTUBE\h2dev")
D = Path(sys.argv[1]); H = D / "hook"
prof = json.loads((ROOT / r"profiles\profiles\teinengo-tanoshimi.json").read_text(encoding="utf-8"))
STYLE = prof["image"]["style_suffix"]
ch = json.loads((D / "characters.json").read_text(encoding="utf-8"))["characters"]
V = {"MAIN": ch[0]["look"], "MENTOR": ch[1]["look"] if len(ch) > 1 else "", "WIFE": ch[2]["look"] if len(ch) > 2 else ""}
plan = json.loads((H / "hook_plan.json").read_text(encoding="utf-8"))
NOTXT = " No text, no signs, no writing, no logos anywhere."
MOTION_TAIL = (" Keep the Japanese manga illustration style, the faces, hair and clothing exactly as in the image. "
               "Subtle natural motion, static locked-off camera apart from the move described. No text, no subtitles, "
               "no speech bubbles, no watermark, no new people entering the frame, no camera shake.")

cues = []
for blk in re.split(r"\n\s*\n", (H / "hook_voice.srt").read_text(encoding="utf-8-sig").strip()):
    ln = blk.strip().splitlines()
    a, b = ln[1].split(" --> ")
    f = lambda s: int(s[:2]) * 3600 + int(s[3:5]) * 60 + float(s[6:].replace(",", "."))
    cues.append((f(a), f(b), "".join(ln[2:])))
shots = plan["shots"]
end_total = cues[-1][1] + 0.4
bounds = [0.0] + [round((cues[s["cues"][1] - 1][1] + cues[s["cues"][1]][0]) / 2, 2) for s in shots[:-1]] + [round(end_total, 2)]


def sua(t):
    for a, b in (plan.get("fix") or {}).items():
        t = t.replace(a, b)
    return t


lines, tl, jobs = [], [], []
for i, s in enumerate(shots):
    n, mk = s["n"], s.get("ref", "")
    p = s["img"].format(**V)
    lines.append((f"{mk} " if mk else "") + f"{p}.{NOTXT} {STYLE}")
    c0, c1 = s["cues"]
    tl.append({"n": n, "t0": bounds[i], "t1": bounds[i + 1], "clip": f"clip/clip_{n:02d}.mp4", "img": f"img/{n:03d}.png",
               "voice": sua("".join(c[2] for c in cues[c0 - 1:c1])), "ky_vong": s["ky_vong"], "ref": mk or "none"})
    jobs.append({"id": f"clip_{n:02d}", "image": str(H / "img" / f"{n:03d}.png"), "prompt": s["motion"] + MOTION_TAIL,
                 "duration": 6, "resolution": "720p", "aspect": "16:9"})

(H / "img_prompts_hook.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
(H / "hook_timeline.json").write_text(json.dumps({"_doc": plan.get("doc", ""), "hook_voice_end_s": round(cues[-1][1], 3),
                                                  "tong_s": round(end_total, 2), "shots": tl}, ensure_ascii=False, indent=1), encoding="utf-8")
bak = H / "grok_jobs.csv.bak_storyboard"
if (H / "grok_jobs.csv").exists() and not bak.exists():
    bak.write_bytes((H / "grok_jobs.csv").read_bytes())
with open(H / "grok_jobs.csv", "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["id", "image", "prompt", "duration", "resolution", "aspect"])
    w.writeheader(); w.writerows(jobs)
for t in tl:
    print(t["n"], t["t0"], t["t1"], t["ref"], t["voice"])
