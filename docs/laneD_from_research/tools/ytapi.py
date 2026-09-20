# -*- coding: utf-8 -*-
"""YouTube Data API v3 — lớp ENRICH (chính xác) cho pipeline.

Chi phí quota: videos.list / channels.list / playlistItems.list = 1 đơn vị mỗi lượt
(tối đa 50 id) → rẻ gấp 100 lần search.list. Discovery KHÔNG dùng file này.
"""
from __future__ import annotations

import datetime as dt
import re

import requests

BASE = "https://www.googleapis.com/youtube/v3"
QUOTA_COST = {"videos": 1, "channels": 1, "playlistItems": 1, "search": 100}
DAILY_QUOTA = 10_000

_DUR = re.compile(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")


def parse_duration(iso: str | None) -> int:
    """'PT37M22S' -> 2242 giây."""
    if not iso:
        return 0
    m = _DUR.fullmatch(iso)
    if not m:
        return 0
    d, h, mi, s = (int(x) if x else 0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def _chunks(seq, n=50):
    seq = list(seq)
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


class QuotaExhausted(RuntimeError):
    """Đã chạm ngưỡng an toàn — caller phải chuyển sang đường keyless."""


class YouTubeAPI:
    def __init__(self, api_key: str, safety_limit: int = 9_000):
        self.key = api_key
        self.used = 0
        self.safety_limit = safety_limit
        self._s = requests.Session()

    def _get(self, endpoint: str, **params) -> dict:
        cost = QUOTA_COST[endpoint]
        if self.used + cost > self.safety_limit:
            raise QuotaExhausted(f"quota {self.used}/{self.safety_limit}")
        params["key"] = self.key
        r = self._s.get(f"{BASE}/{endpoint}", params=params, timeout=30)
        self.used += cost
        if r.status_code == 403 and "quotaExceeded" in r.text:
            raise QuotaExhausted(r.text[:200])
        r.raise_for_status()
        return r.json()

    # ---------- videos ----------
    def videos_batch(self, video_ids) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for chunk in _chunks(video_ids):
            data = self._get("videos", part="snippet,statistics,contentDetails",
                             id=",".join(chunk), maxResults=50)
            for it in data.get("items", []):
                sn, st = it.get("snippet", {}), it.get("statistics", {})
                out[it["id"]] = {
                    "title_api": sn.get("title", ""),
                    "channel_id_api": sn.get("channelId", ""),
                    "published_at": sn.get("publishedAt", ""),
                    "views": int(st.get("viewCount", 0) or 0),
                    "likes": int(st.get("likeCount", 0) or 0),
                    "comments": int(st.get("commentCount", 0) or 0),
                    "duration_s": parse_duration(it.get("contentDetails", {}).get("duration")),
                    "category_id": sn.get("categoryId", ""),
                }
        return out

    # ---------- channels ----------
    def channels_batch(self, channel_ids) -> dict[str, dict]:
        today = dt.datetime.now(dt.timezone.utc)
        out: dict[str, dict] = {}
        for chunk in _chunks(channel_ids):
            data = self._get("channels", part="snippet,statistics,contentDetails",
                             id=",".join(chunk), maxResults=50)
            for it in data.get("items", []):
                sn, st = it.get("snippet", {}), it.get("statistics", {})
                created = sn.get("publishedAt", "")
                age = None
                if created:
                    try:
                        born = dt.datetime.fromisoformat(created.replace("Z", "+00:00"))
                        age = (today - born).days
                    except ValueError:
                        pass
                out[it["id"]] = {
                    "channel_title": sn.get("title", ""),
                    "ch_created_at": created,
                    "ch_age_days": age,
                    "ch_country": sn.get("country", ""),
                    "subs": int(st.get("subscriberCount", 0) or 0),
                    "ch_total_views": int(st.get("viewCount", 0) or 0),
                    "ch_video_count": int(st.get("videoCount", 0) or 0),
                    "uploads_playlist": (it.get("contentDetails", {})
                                         .get("relatedPlaylists", {}).get("uploads", "")),
                }
        return out

    # ---------- uploads (Phase 5: baseline + watchlist) ----------
    def recent_uploads(self, uploads_playlist: str, limit: int = 10) -> list[str]:
        """Trả video_id mới nhất của kênh — 1 quota cho tới 50 video."""
        data = self._get("playlistItems", part="contentDetails",
                         playlistId=uploads_playlist, maxResults=min(limit, 50))
        return [it["contentDetails"]["videoId"] for it in data.get("items", [])
                if it.get("contentDetails", {}).get("videoId")]

    def baseline_videos(self, uploads_playlist: str, want: int = 12,
                        min_age_days: int = 7, fetch: int = 24) -> list[dict]:
        """Video để tính baseline — BỎ video quá mới.

        Kênh faceless đăng mỗi ngày, nên 12 video mới nhất luôn có mấy cái vừa đăng
        chưa kịp tích view (đo thật: median 306 vs 460 khi lọc >=7 ngày). Không lọc
        thì median bị kéo xuống và `breakout` của mọi video bị thổi phồng.
        Vẫn 2 quota như cũ: playlistItems tối đa 50, videos.list tối đa 50 id/lượt.
        """
        stats = self.videos_batch(self.recent_uploads(uploads_playlist, fetch))
        now = dt.datetime.now(dt.timezone.utc)
        aged = []
        for d in stats.values():
            try:
                born = dt.datetime.fromisoformat(d["published_at"].replace("Z", "+00:00"))
            except (ValueError, KeyError):
                continue
            if (now - born).days >= min_age_days:
                aged.append(d)
        aged.sort(key=lambda d: d["published_at"], reverse=True)
        return aged[:want] or list(stats.values())[:want]
