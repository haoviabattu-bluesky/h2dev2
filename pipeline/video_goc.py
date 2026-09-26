#!/usr/bin/env python3
"""Ghi + tra cứu VIDEO GỐC của từng tập — cho dự án YT-TITLE-RESEARCH đối chiếu khi viết
tiêu đề/mô tả/thumbnail (giữ đúng cấu trúc tiêu đề + mô-típ thumbnail + tags của video gốc).

Theo docs/GIAO_VIEC_H2DEV_VIDEO_GOC_TUNG_TAP_2026-09-25.md (YT-TITLE-RESEARCH giao 2026-09-25).

BẮT BUỘC gọi ở BƯỚC 2 của MỌI lane mới (nơi ghi competitor.txt) — xem CLAUDE.md mục
"VIDEO GỐC TỪNG TẬP". Chạy độc lập, không import xong không hiểu vẫn không chặn B2 (bọc try/except
ở nơi gọi), nhưng bản thân module này không tự nuốt lỗi — nơi gọi quyết định.

Dùng:
  from video_goc import ghi_video_goc
  ghi_video_goc(ep_dir, video_id="XbwqD2SktC0", title="...", channel="...", channel_id="UC...",
                cach_xac_dinh="ghi tu B2 luc tai transcript", do_chac="chac_chan",
                view_count=299000, duration_s=1453)

CLI quét lại tập cũ (không có competitor.txt riêng thì bỏ qua):
  py -3.13 video_goc.py --scan --profile teinengo-real \
      --channel-dna-dir docs/channel_dna/rougonokurashi --channel "老後の暮らし研究所"
"""
import argparse
import difflib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def _lane_file(slug_dir):
    return ROOT / slug_dir / "VIDEO_GOC.json"


def ghi_video_goc(ep_dir, video_id, title, channel="", channel_id=None,
                   cach_xac_dinh="", do_chac="chac_chan", view_count=None, duration_s=None,
                   slug_dir=None, lane_id=None):
    """Ghi video_goc.json TRONG thư mục tập + cập nhật VIDEO_GOC.json CẤP LANE.

    ep_dir: Path thư mục tập (vd assets/teinengo-real/ep04-xxx).
    slug_dir/lane_id: nếu không truyền, tự suy từ ep_dir (thư mục cha + tên thư mục cha của assets/).
    Không tự động thêm dòng vào HOOK_TAP.md — gọi hook_tap_ghi_video_goc() riêng nếu cần (một số
    lane sinh HOOK_TAP.md SAU B2, gọi ở đây có thể ghi vào file chưa tồn tại)."""
    ep_dir = Path(ep_dir)
    if slug_dir is None:
        slug_dir = str(ep_dir.parent.relative_to(ROOT)) if ep_dir.is_absolute() else str(ep_dir.parent)
    if lane_id is None:
        lane_id = ep_dir.parent.name

    entry = {
        "ep": ep_dir.name,
        "thu_muc": str(ep_dir),
        "video_goc": {
            "id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "kenh": channel,
            "channel_id": channel_id,
            "tieu_de": title,
        },
        "cach_xac_dinh": cach_xac_dinh,
        "do_chac": do_chac,
    }
    if view_count is not None:
        entry["video_goc"]["view_count"] = view_count
    if duration_s is not None:
        entry["video_goc"]["duration_s"] = duration_s

    # 1) file RIÊNG trong thư mục tập
    (ep_dir / "video_goc.json").write_text(
        json.dumps(entry, ensure_ascii=False, indent=1), encoding="utf-8")

    # 2) merge vào VIDEO_GOC.json cấp lane
    lane_f = _lane_file(slug_dir)
    if lane_f.exists():
        try:
            doc = json.loads(lane_f.read_text(encoding="utf-8"))
        except Exception:
            doc = {"lane": lane_id, "tap": []}
    else:
        doc = {"lane": lane_id, "tap": []}
    doc["tap"] = [t for t in doc.get("tap", []) if t.get("ep") != ep_dir.name] + [entry]
    doc["tap"].sort(key=lambda t: t["ep"])
    import datetime
    doc["cap_nhat"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    lane_f.parent.mkdir(parents=True, exist_ok=True)
    lane_f.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    return entry


def hook_tap_ghi_video_goc(ep_dir, video_id, title):
    """Thêm dòng 'Video gốc: <id> — <tiêu đề>' vào HOOK_TAP.md của tập (nếu file đã tồn tại)."""
    f = Path(ep_dir) / "HOOK_TAP.md"
    if not f.exists():
        return False
    text = f.read_text(encoding="utf-8")
    line = f"\nVideo gốc: {video_id} — {title}\n"
    if "Video gốc:" in text:
        return False
    f.write_text(text.rstrip("\n") + "\n" + line, encoding="utf-8")
    return True


# ---------- quét lại tập cũ (Việc 1 cho lane mới/tập cũ chưa có VIDEO_GOC.json) ----------

def load_transcripts(dna_dir: Path):
    f = dna_dir / "_raw" / "transcripts.json"
    if not f.exists():
        return []
    data = json.loads(f.read_text(encoding="utf-8"))
    out = []
    for x in data:
        vid = x.get("id") or x.get("video_id")
        if not vid:
            continue
        out.append({
            "id": vid, "title": x.get("title", ""),
            "transcript": x.get("transcript") or x.get("text") or "",
            "view_count": x.get("view_count"), "duration": x.get("duration"),
        })
    return out


def best_match(comp_text, transcripts, n=3000):
    scores = []
    for t in transcripts:
        sm = difflib.SequenceMatcher(None, comp_text[:n], t["transcript"][:n])
        scores.append((sm.ratio(), t))
    scores.sort(key=lambda x: -x[0])
    return scores


def scan_lane(slug_dir, dna_dir, channel_id, channel_name, lane_id, threshold_chac=0.9,
              threshold_uoc=0.3):
    slug = ROOT / slug_dir
    dna = ROOT / dna_dir
    transcripts = load_transcripts(dna)
    eps = sorted([d for d in slug.iterdir() if d.is_dir() and d.name.startswith("ep")])
    tap = []
    for d in eps:
        comp = d / "competitor.txt"
        if not comp.exists():
            tap.append({"ep": d.name, "thu_muc": str(d), "video_goc": None,
                        "ly_do": "khong co competitor.txt", "do_chac": None})
            continue
        text = comp.read_text(encoding="utf-8")
        scores = best_match(text, transcripts)
        if not scores:
            tap.append({"ep": d.name, "thu_muc": str(d), "video_goc": None,
                        "ly_do": "khong co transcripts.json de doi chieu", "do_chac": None})
            continue
        top_ratio, top = scores[0]
        second = scores[1][0] if len(scores) > 1 else 0
        do_chac = ("chac_chan" if top_ratio >= threshold_chac else
                    "uoc_doan" if top_ratio >= threshold_uoc else None)
        entry = {
            "ep": d.name, "thu_muc": str(d),
            "video_goc": None if do_chac is None else {
                "id": top["id"], "url": f"https://www.youtube.com/watch?v={top['id']}",
                "kenh": channel_name, "channel_id": channel_id, "tieu_de": top["title"],
                "view_count": top.get("view_count"), "duration_s": top.get("duration"),
            },
            "cach_xac_dinh": (f"difflib.SequenceMatcher 3000 ky tu dau competitor.txt vs "
                               f"{dna_dir}/_raw/transcripts.json -> ratio={top_ratio:.3f} "
                               f"(video {top['id']}), second={second:.3f}"),
            "do_chac": do_chac,
        }
        if do_chac is None:
            entry["ly_do"] = f"ratio cao nhat chi {top_ratio:.3f} - khong du tin cay"
        tap.append(entry)
    return tap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug-dir", default="")
    ap.add_argument("--channel-dna-dir", default="")
    ap.add_argument("--channel-id", default="")
    ap.add_argument("--channel", default="")
    a = ap.parse_args()
    if a.scan:
        import profiles
        p = profiles.load(a.profile)
        slug_dir = a.slug_dir or p.get("slug_dir")
        dna_dir = a.channel_dna_dir or p.get("channel_dna_dir")
        if not dna_dir:
            raise SystemExit("Thiếu --channel-dna-dir (profile không khai channel_dna_dir)")
        tap = scan_lane(slug_dir, dna_dir, a.channel_id or None, a.channel, a.profile)
        import datetime
        doc = {"lane": a.profile, "cap_nhat": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
               "tap": tap}
        out = ROOT / slug_dir / "VIDEO_GOC.json"
        out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"→ {out} ({sum(1 for t in tap if t.get('video_goc'))}/{len(tap)} tập có ID)")


if __name__ == "__main__":
    main()
