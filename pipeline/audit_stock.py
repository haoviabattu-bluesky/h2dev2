# -*- coding: utf-8 -*-
"""Nghiem thu NOI LONG cho asset stock (phong canh/do vat): file ton tai, decode, kich thuoc, license,
prompt_line khong trung dong @REF; + vision (gemini-3.8-flash) 1-3 khung hinh: CHI loai khi thay
MAT NGUOI ro (nguoi la lam gay mach truyen) hoac CHU/LOGO to. Nguoi khong ro mat (tay, lung) = chap nhan.
Ghi audit_report.md; cap nhat cot status trong manifest.csv (OK -> REJECT_FACE / REJECT_TEXT / BAD_FILE).
Dung: py -3.13 audit_stock.py --slug <thu muc tap>
"""
import argparse, csv, re, subprocess, sys, tempfile, time
from pathlib import Path
from collections import Counter
sys.path.insert(0, r"E:\CLAUDE\YOUTUBE\h2dev\pipeline")
import qc_visual as Q
from PIL import Image

VQ = ('Look at this frame. Reply ONLY JSON: {"face_visible":<bool: a human FACE is clearly recognizable>,'
      '"people_visible":<bool: any person or body part>,"text_visible":<bool: large readable text/logo/watermark>,'
      '"scene":"<=8 words what is shown"}')

def decode_ok(ff, p):
    r = subprocess.run([ff, "-v", "error", "-i", str(p), "-t", "3", "-f", "null", "-"], capture_output=True)
    return r.returncode == 0

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--slug", required=True); a = ap.parse_args()
    ep = Path(a.slug); st = ep / "stock"; man = st / "manifest.csv"; here = Path(__file__).resolve().parent
    ff = Q._ff(); T0 = time.time()
    prompts = (ep / "img_prompts.txt").read_text(encoding="utf-8").splitlines()
    marked = {i for i, l in enumerate(prompts, 1) if re.match(r"^@(REF2?|GROK)\b", l.strip())}
    rows = list(csv.DictReader(man.open(encoding="utf-8-sig", newline="")))
    tmp = Path(tempfile.mkdtemp(prefix="audit_stock_")); lines = []; rej = Counter(); vis_calls = 0
    for r in rows:
        if r["status"] not in ("OK", "FILLER"): lines.append(f"L{r['prompt_line']}: {r['status']}"); continue
        p = st / r["local_filename"]; ln = int(r["prompt_line"]); probs = []
        if ln in marked: probs.append("TRUNG DONG @REF")
        if not p.is_file(): probs.append("THIEU FILE")
        elif not decode_ok(ff, p): probs.append("KHONG DECODE")
        else:
            try:
                if r["media_type"] == "image":
                    with Image.open(p) as im: w, h = im.size
                    if str(w) != str(r["width"]) or str(h) != str(r["height"]): probs.append(f"KICH THUOC {w}x{h} != manifest")
                    if w < 1280 or w < h: probs.append("nho/doc")
            except Exception as e: probs.append(f"PIL {e}")
        if not r["source_url"] or not r["license"]: probs.append("THIEU LICENSE")
        face = text = False; scenes = []
        if not probs:
            frames = []
            if r["media_type"] == "video":
                d = float(r["duration_s"] or 6)
                for k, t in enumerate((0.25, 0.6)):
                    f = tmp / f"L{ln:03d}_{k}.jpg"
                    if Q._frame(p, d * t, f): frames.append(f)
            else:
                f = tmp / f"L{ln:03d}.jpg"
                with Image.open(p) as im: im.convert("RGB"); im.thumbnail((1280, 1280)); im.convert("RGB").save(f, quality=85)
                frames.append(f)
            for f in frames:
                try:
                    j = Q._vision(VQ, f); vis_calls += 1
                    face |= bool(j.get("face_visible")); text |= bool(j.get("text_visible")); scenes.append(str(j.get("scene", ""))[:40])
                except Q.QcError as e: scenes.append(f"vision loi {e}")
            if face: probs.append("MAT NGUOI RO")
            if text: probs.append("CHU/LOGO")
        if probs:
            new = "BAD_FILE" if any(x in probs[0] for x in ("THIEU", "KHONG", "KICH", "PIL", "TRUNG", "nho")) else ("REJECT_FACE" if face else "REJECT_TEXT")
            if r["status"] != "FILLER" or new != "BAD_FILE": r["status"] = new
            rej[new] += 1
        lines.append(f"L{ln:03d} {r['media_type']:5s} {r['status']:12s} {' | '.join(scenes)}" + (f"  <- {'; '.join(probs)}" if probs else ""))
    with man.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    c = Counter((r["status"], r["media_type"]) for r in rows)
    plan_stock = sum(1 for r in rows if r["prompt_line"] != "0")
    ok_v = c[("OK", "video")]; ok_i = c[("OK", "image")]; fill = sum(v for (s, _), v in c.items() if s == "FILLER")
    tot = sum(int(r["size_bytes"] or 0) for r in rows if r["status"] in ("OK", "FILLER"))
    head = [f"# Audit stock — {ep.name}", "", f"- Dong STOCK theo ke hoach: {plan_stock} · OK video {ok_v} · OK image {ok_i} · loai: {dict(rej)} · filler dung duoc {fill}",
            f"- Vision calls (gemini-3.8-flash): {vis_calls} · tong dung luong OK+filler: {tot/1048576:.1f} MB · {(time.time()-T0)/60:.1f} phut",
            "- Chinh sach NOI LONG: chi loai khi MAT NGUOI RO hoac CHU/LOGO to hoac file hong; nguoi khong ro mat (tay/lung) van nhan.",
            "- Day la kiem tra ad-hoc, chua co compositor, chua giao hang.", "", "```"] + lines + ["```"]
    # Ghi vao THU MUC TAP (stock/audit_report.md) — ban cu ghi canh tool nen chay 4 tap lien la ghi de
    # mat 3 bao cao (2026-09-20). Giu them ban canh tool cho tuong thich.
    rp = st / "audit_report.md"
    rp.write_text("\n".join(head) + "\n", encoding="utf-8")
    (here / "audit_report.md").write_text("\n".join(head) + "\n", encoding="utf-8")
    print("\n".join(head[2:5])); print(f"chi tiet: {rp}")

if __name__ == "__main__": main()
