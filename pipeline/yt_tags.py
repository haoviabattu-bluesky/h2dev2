"""yt_tags.py — đọc VIDEO TAGS + CHANNEL KEYWORDS thẳng từ HTML YouTube (KHÔNG cần extension vidIQ,
KHÔNG cần API key, KHÔNG cần yt-dlp) — verify thật 2026-09-17 trên kênh 伊勢呂哲也 (泌尿器科).

Nguồn dữ liệu:
  - video tags   : ytInitialPlayerResponse.videoDetails.keywords  (trang /watch)
  - channel tags : ytInitialData.metadata.channelMetadataRenderer.keywords  (trang /about,
                    chính là "Channel keywords" chủ kênh tự khai trong YouTube Studio)

Đây LÀ chỗ vidIQ extension đọc panel "Video Tags"/"Channel Tags" — tool này đọc thẳng HTML,
không cần cài extension nào (xem C:\\Users\\admin\\.claude\\skills\\youtube_research_ext.md §vidIQ).

Dùng độc lập:
  py -3.13 yt_tags.py video <video_id_hoặc_url>
  py -3.13 yt_tags.py channel <channel_url>                    # chỉ channel keywords
  py -3.13 yt_tags.py stats out_dir/_raw/transcripts.json --out out_dir/TAG_STATS.json
      # gom tag của N video đã crawl (file rows kiểu channel_analyzer.py) → tần suất + view

Dùng như module (channel_analyzer.py gọi):
  from yt_tags import fetch_video_tags, fetch_channel_keywords, build_tag_stats
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "Chrome/128 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
_COOKIES = {"CONSENT": "YES+"}  # né trang consent EU chặn nội dung


def _get(url, proxy=None, retries=3):
    proxies = {"http": proxy, "https": proxy} if proxy else None
    last_err = None
    for i in range(retries):
        try:
            r = requests.get(url, headers=_HEADERS, cookies=_COOKIES, proxies=proxies,
                              timeout=20)
            r.raise_for_status()
            return r.text
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"GET thất bại sau {retries} lần: {url} ({last_err})")


def _extract_json_var(html, var_name):
    """Rút biến JS kiểu `var ytInitialData = {...};` khỏi HTML (regex tham lam có kiểm ngoặc)."""
    m = re.search(re.escape(var_name) + r"\s*=\s*(\{)", html)
    if not m:
        return None
    start = m.end(1) - 1
    depth = 0
    for i in range(start, len(html)):
        c = html[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(html[start:i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def video_id_of(s):
    s = s.strip()
    m = re.search(r"(?:v=|/shorts/|/embed/|youtu\.be/)([A-Za-z0-9_-]{11})", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    raise ValueError(f"Không nhận ra video id từ: {s}")


def fetch_video_tags(video_id, proxy=None):
    """Trả list tag của 1 video (rỗng nếu video không khai tag nào — KHÔNG phải lỗi)."""
    html = _get(f"https://www.youtube.com/watch?v={video_id}", proxy=proxy)
    data = _extract_json_var(html, "ytInitialPlayerResponse")
    if not data:
        raise RuntimeError(f"{video_id}: không đọc được ytInitialPlayerResponse "
                            "(có thể bị chặn IP/consent — thử --proxy)")
    return (data.get("videoDetails") or {}).get("keywords") or []


def fetch_channel_keywords(channel_url_or_id, proxy=None):
    """Trả (channel_keywords: list[str], channel_title: str). channel_url_or_id nhận URL đầy đủ
    (/channel/UC.., /@handle) hoặc UC id trần."""
    if channel_url_or_id.startswith("UC") and "/" not in channel_url_or_id:
        url = f"https://www.youtube.com/channel/{channel_url_or_id}/about"
    else:
        url = channel_url_or_id.rstrip("/").split("/videos")[0].split("/about")[0] + "/about"
    html = _get(url, proxy=proxy)
    data = _extract_json_var(html, "ytInitialData")
    if not data:
        raise RuntimeError(f"{url}: không đọc được ytInitialData (thử --proxy)")
    meta = ((data.get("metadata") or {}).get("channelMetadataRenderer")) or {}
    kw_raw = meta.get("keywords") or ""
    # channel keywords là 1 chuỗi, cụm nhiều từ bọc "..." ; tách đúng kiểu YouTube Studio lưu
    tags = [a or b for a, b in re.findall(r'"([^"]+)"|(\S+)', kw_raw)]
    return tags, meta.get("title", "")


def build_tag_stats(rows, proxy=None, sleep_s=0.3, log=print, channel_url=""):
    """rows: list [{"id","title","view_count",...}, ...] (định dạng channel_analyzer.py candidates).
    Trả dict {"video_tags": {tag: {"n_videos", "total_views", "avg_views", "video_ids":[...]}},
              "top_tags": [...sắp theo avg_views giảm dần...],
              "n_videos_with_tags": int, "n_videos_total": int,
              "channel_keywords": [...] (chỉ khi truyền channel_url), "channel_title": str}.
    channel_url: truyền vào thì gom thêm Channel keywords (chủ kênh tự khai trong Studio) — dùng làm
    gợi ý điền Channel keywords lúc setup kênh mới thay vì hardcode tay. Thiếu nó thì TAG_STATS chỉ
    có tag CỦA TỪNG VIDEO (thiếu sót đã phát hiện ở kênh どっこい日本史 2026-09-23).
    Lỗi từng video KHÔNG dừng cả lô — ghi log rồi bỏ qua (đúng kiểu crawl_transcripts đã làm)."""
    agg = {}
    n_ok = 0
    for r in rows:
        try:
            tags = fetch_video_tags(r["id"], proxy=proxy)
        except Exception as e:
            log(f"  ✗ {r['id']} tags lỗi: {type(e).__name__} {str(e)[:100]}")
            time.sleep(sleep_s)
            continue
        if tags:
            n_ok += 1
        for t in tags:
            slot = agg.setdefault(t, {"n_videos": 0, "total_views": 0, "video_ids": []})
            slot["n_videos"] += 1
            slot["total_views"] += r.get("view_count") or 0
            slot["video_ids"].append(r["id"])
        time.sleep(sleep_s)
    for t, slot in agg.items():
        slot["avg_views"] = round(slot["total_views"] / slot["n_videos"]) if slot["n_videos"] else 0
    # Ưu tiên n_videos trước avg_views: tag chỉ dùng ở 1 video (n=1) ăn nguyên view của video đó
    # nên dễ đội lên đầu nếu sort thẳng theo avg_views — trong khi tag LẶP LẠI ở nhiều video mới là
    # tín hiệu "kênh này cố ý đóng đinh chủ đề" (đáng tin hơn cho việc rút bộ từ khoá ngách).
    top_tags = sorted(agg.items(), key=lambda kv: (kv[1]["n_videos"], kv[1]["avg_views"]),
                       reverse=True)
    top_tags = [{"tag": t, **v} for t, v in top_tags]
    out = {
        "video_tags": agg,
        "top_tags": top_tags,
        "n_videos_with_tags": n_ok,
        "n_videos_total": len(rows),
    }
    if channel_url:
        try:
            kws, ch_title = fetch_channel_keywords(channel_url, proxy=proxy)
            out["channel_keywords"] = kws
            out["channel_title"] = ch_title
            log(f"  → {len(kws)} channel keyword ({ch_title})")
        except Exception as e:
            log(f"  ✗ channel keywords lỗi: {type(e).__name__} {str(e)[:100]}")
    return out


# ---------------------------------------------------------------------- CLI
def _cmd_video(args):
    tags = fetch_video_tags(video_id_of(args.target), proxy=args.proxy)
    print(f"{len(tags)} tag: {tags}")


def _cmd_channel(args):
    tags, title = fetch_channel_keywords(args.target, proxy=args.proxy)
    print(f"Kênh: {title}")
    print(f"{len(tags)} channel keyword: {tags}")


def _cmd_stats(args):
    rows = json.loads(Path(args.rows_json).read_text(encoding="utf-8"))
    print(f"[yt_tags] gom tag của {len(rows)} video ...")
    stats = build_tag_stats(rows, proxy=args.proxy)
    out_path = Path(args.out) if args.out else Path(args.rows_json).with_name("TAG_STATS.json")
    out_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → {stats['n_videos_with_tags']}/{stats['n_videos_total']} video có tag, "
          f"{len(stats['top_tags'])} tag khác nhau → {out_path}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("video", help="in tag của 1 video")
    p1.add_argument("target")
    p1.add_argument("--proxy", default=None)
    p1.set_defaults(func=_cmd_video)

    p2 = sub.add_parser("channel", help="in channel keywords của 1 kênh")
    p2.add_argument("target")
    p2.add_argument("--proxy", default=None)
    p2.set_defaults(func=_cmd_channel)

    p3 = sub.add_parser("stats", help="gom tag từ file rows JSON (id/title/view_count) → TAG_STATS.json")
    p3.add_argument("rows_json")
    p3.add_argument("--out", default=None)
    p3.add_argument("--proxy", default=None)
    p3.set_defaults(func=_cmd_stats)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
