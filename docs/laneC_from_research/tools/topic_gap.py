# -*- coding: utf-8 -*-
"""Dò KHO ĐỀ TÀI cho ngách bí ẩn/khoa học — đo cung–cầu của TỪNG đề tài cụ thể.

Phát hiện nền tảng (verify 2026-09-09): các kênh 都市伝説 Nhật đang lên KHÔNG tự nghĩ ra
tư liệu — họ kể lại những vụ đã nổi sẵn bằng TIẾNG ANH (Nibiru, Roswell, Boriska,
Fátima, Dienach...). 7/8 đề tài của kênh mẫu là gốc phương Tây, và nguồn cung tiếng Nhật
chỉ 0–8 video/tháng trong khi view vẫn 3.000–68.000.

→ Mỗi vụ bí ẩn nổi tiếng bằng tiếng Anh = một khoảng trống nội dung tiếng Nhật.
Script này chấm điểm khoảng trống đó để chọn đề tài làm trước.

  py -3.13 -X utf8 src/topic_gap.py --topics config/topics_mystery.yaml
"""
from __future__ import annotations

import argparse
import csv
import statistics
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from innertube import BotCheckError, InnerTube  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LOG = lambda *a: print(*a, file=sys.stderr, flush=True)  # noqa: E731


def probe(it: InnerTube, kw: str, windows=("month", "week")) -> dict:
    seen: dict[str, dict] = {}
    for w in windows:
        try:
            for v in it.search(kw, w):
                seen.setdefault(v["video_id"], v)
        except BotCheckError:
            raise
        except Exception as e:
            LOG(f"  ! {kw}[{w}]: {type(e).__name__}")
    vids = list(seen.values())
    views = sorted(v["views_it"] for v in vids)
    fresh = [v for v in vids if (v["age_hours_it"] or 9e9) <= 24 * 60]
    return {
        "supply": len(views),                       # cung: video mới trong 1-2 tháng
        "median_views": int(statistics.median(views)) if views else 0,
        "max_views": max(views) if views else 0,
        "fresh": len(fresh),
        "top_title": max(vids, key=lambda v: v["views_it"])["title"] if vids else "",
        "top_channel": max(vids, key=lambda v: v["views_it"])["channel"] if vids else "",
    }


def gap_score(r: dict) -> float:
    """Điểm khoảng trống: cầu chứng minh được, cung càng mỏng càng tốt.

    Cung = 0 KHÔNG phải điểm cao nhất — có thể đề tài đó người Nhật không quan tâm.
    Điểm cao nhất rơi vào: đã có vài video CHỨNG MINH có người xem, nhưng còn rất ít.
    """
    s, m = r["supply"], r["median_views"]
    if s == 0:
        return 0.0                      # chưa ai làm ⇒ chưa có bằng chứng có cầu
    import math
    demand = math.log10(max(m, 1))
    scarcity = 1.0 / (1.0 + s / 4.0)    # 1 video → 0.80 · 4 → 0.50 · 12 → 0.25
    return round(demand * scarcity * 25, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", default=str(ROOT / "config" / "topics_mystery.yaml"))
    ap.add_argument("--out", default=str(ROOT / "data" / "topic_gap.csv"))
    ap.add_argument("--hl", default="ja")
    ap.add_argument("--gl", default="JP")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.topics, encoding="utf-8"))
    it = InnerTube(hl=args.hl, gl=args.gl)
    rows = []
    for i, t in enumerate(cfg["topics"], 1):
        kw = t["kw"]
        try:
            r = probe(it, kw)
        except BotCheckError as e:
            LOG(f"!! BOT-CHECK: {e}")
            return 2
        r.update(kw=kw, origin=t.get("origin", ""), en=t.get("en", ""))
        r["gap_score"] = gap_score(r)
        rows.append(r)
        if i % 10 == 0:
            LOG(f"  ...{i}/{len(cfg['topics'])}")
    rows.sort(key=lambda r: r["gap_score"], reverse=True)

    cols = ["gap_score", "kw", "en", "supply", "median_views", "max_views",
            "origin", "top_channel", "top_title"]
    with open(args.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows([{c: r[c] for c in cols} for r in rows])

    print(f"\n{'ĐIỂM':>5} {'CUNG':>5} {'MEDIAN':>9} {'MAX':>10}  ĐỀ TÀI (nguồn gốc)")
    for r in rows:
        if r["supply"] == 0:
            continue
        print(f"{r['gap_score']:5.1f} {r['supply']:5} {r['median_views']:9,} "
              f"{r['max_views']:10,}  {r['kw']}  ({r['en']})")
    empty = [r["kw"] for r in rows if r["supply"] == 0]
    if empty:
        print(f"\nCHƯA AI LÀM (0 video — chưa có bằng chứng có cầu, rủi ro cao hơn):")
        print("  " + " · ".join(empty))
    LOG(f"[out] {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
