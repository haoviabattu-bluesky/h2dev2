# -*- coding: utf-8 -*-
"""viet_huong_dan_may2.py — sinh HUONG_DAN_MAY2_STOCK.txt cho tap hybrid (khuon STT8, 2026-09-17).

May 2 (Google Flow) KHONG doc stock_plan.tsv, nen phai co 1 file chu nguoi doc duoc liet ke RO
cac dong KHONG can ve: dong STOCK that (clip video/anh that trong stock/manifest.csv, status=OK)
+ dong AI_FALLBACK (buoc 1 da tu ve bang gpti2, da nam trong img/). Cac dong con lai (group=AI)
may 2 ve binh thuong, dung master REF-LOCK trong characters.json.

  py -3.13 viet_huong_dan_may2.py --slug <thu muc tap>
"""
import argparse
import csv
import json
import textwrap
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()
    d = Path(a.slug).resolve()
    rows = list(csv.DictReader((d / "stock_plan.tsv").open(encoding="utf-8", newline=""), delimiter="\t"))
    n_all = sum(1 for _ in (d / "img_prompts.txt").read_text(encoding="utf-8").splitlines())
    stock = sorted(int(r["line"]) for r in rows if r["group"] == "STOCK")
    fb = sorted(int(r["line"]) for r in rows if r["group"] == "AI_FALLBACK")
    ai = sorted(int(r["line"]) for r in rows if r["group"] == "AI")
    have = {int(p.stem) for p in (d / "img").glob("*.png") if p.stem.isdigit()} if (d / "img").is_dir() else set()
    thieu_fb = [n for n in fb if n not in have]
    ok_stock = 0
    man = d / "stock" / "manifest.csv"
    if man.is_file():
        ok_stock = sum(1 for r in csv.DictReader(man.open(encoding="utf-8-sig", newline=""))
                       if r.get("prompt_line") and r["status"] == "OK")
    masters = []
    try:
        chars = json.loads((d / "characters.json").read_text(encoding="utf-8")).get("characters") or []
        masters = [f"{c['master']} ({c.get('name', '?')})" for c in chars if c.get("master")]
    except Exception:
        pass
    bo_qua = sorted(stock + fb)
    wrap = lambda xs: textwrap.fill(", ".join(str(x) for x in xs), width=88)
    txt = f"""HUONG DAN MAY 2 - BO QUA CAC DONG DA CO ANH (tap {d.name}) - {n_all} anh
=====================================================================
Tap nay dung hybrid stock + AI. Danh sach {len(bo_qua)} dong duoi day DA CO san ({len(stock)} dong stock that
trong stock/manifest.csv status=OK + {len(fb)} dong Claude da tu ve AI bu vao img/ vi stock bi loai/khong tim
thay - xem stock_plan.tsv cot group=STOCK vs group=AI_FALLBACK) - KHONG can may 2 ve nua.

CAC DONG CAN BO QUA (khong tao file .png cho cac dong nay):
{wrap(bo_qua)}

Cac dong CON LAI trong img_prompts.txt ({len(ai)}/{n_all} dong, group=AI trong stock_plan.tsv) can may 2
ve BINH THUONG nhu moi tap khac. Anh master REF-LOCK da co san:
{chr(10).join('  - ' + m for m in masters) or '  (xem characters.json)'}
- dung dung anh nay khi ve cac dong co marker @REF/@REF2.
Neu khong chac dong nao bo qua, doi chieu voi cot "group" trong stock_plan.tsv (group=STOCK
hoac AI_FALLBACK la bo qua, group=AI la ve nhu thuong).
=====================================================================
Kiem tra buoc 1 (tu dong): stock OK={ok_stock}/{len(stock)} · AI_FALLBACK da ve={len(fb) - len(thieu_fb)}/{len(fb)}"""
    if thieu_fb:
        txt += f"\n!! AI_FALLBACK CHUA VE (buoc 1 phai ve truoc khi giao): {thieu_fb}"
    (d / "HUONG_DAN_MAY2_STOCK.txt").write_text(txt + "\n", encoding="utf-8")
    print(f"{d.name}: bo qua {len(bo_qua)} (STOCK {len(stock)} + FALLBACK {len(fb)}) · may 2 ve {len(ai)}/{n_all}"
          + (f" · !! thieu fallback {thieu_fb}" if thieu_fb else ""))


if __name__ == "__main__":
    main()
