# -*- coding: utf-8 -*-
"""Discovery keyless qua InnerTube + fallback đọc metadata kênh từ trang /about.

Không cần API key, không tốn quota. Verify 2026-09-09: HTTP 200, trả view count +
tuổi video + channelId; trang /about trả subs + total views + NGÀY TẠO KÊNH.
"""
from __future__ import annotations

import datetime as dt
import re
import time

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

# protobuf params: field1=sortBy(3=viewCount), field2={upload_date, type=video}
WINDOW_PARAMS = {
    "today": "CAMSBAgCEAE",
    "week": "CAMSBAgDEAE",
    "month": "CAMSBAgEEAE",
}

_SEARCH_URL = "https://www.youtube.com/youtubei/v1/search?prettyPrint=false"
_BOT_MARKERS = ("Sign in to confirm", "confirm you&#39;re not a bot", "consent.youtube.com")

_UNIT_MULT = {"万": 1e4, "億": 1e8, "천": 1e3, "만": 1e4,
              "K": 1e3, "M": 1e6, "B": 1e9, "k": 1e3}

# tiếng Nhật + tiếng Anh + tiếng Hàn (ngách khác dùng lại được)
_AGE_UNITS = {
    "秒": 1 / 3600, "分": 1 / 60, "時間": 1, "日": 24, "週間": 168, "か月": 730, "ヶ月": 730, "年": 8760,
    "second": 1 / 3600, "minute": 1 / 60, "hour": 1, "day": 24, "week": 168, "month": 730, "year": 8760,
    "초": 1 / 3600, "분": 1 / 60, "시간": 1, "일": 24, "주": 168, "개월": 730, "년": 8760,
}


class BotCheckError(RuntimeError):
    """YouTube trả trang xác minh thay vì dữ liệu — IP đang bị nghi ngờ."""


def parse_count(text: str | None) -> int:
    """'6,931回視聴' / '1.67万' / '16.7K subscribers' / '1,547,385' -> int."""
    if not text:
        return 0
    t = text.replace(",", "").replace(" ", " ")
    m = re.search(r"([\d.]+)\s*(万|億|천|만|K|k|M|B)?", t)
    if not m:
        return 0
    try:
        return int(float(m.group(1)) * _UNIT_MULT.get(m.group(2) or "", 1))
    except ValueError:
        return 0


def parse_length(text: str | None) -> int:
    """'15:29' / '1:02:11' -> số giây. Dùng khi chạy keyless (API không có mặt)."""
    if not text:
        return 0
    parts = text.strip().split(":")
    if not all(p.isdigit() for p in parts) or not 2 <= len(parts) <= 3:
        return 0
    secs = 0
    for p in parts:
        secs = secs * 60 + int(p)
    return secs


def parse_age_hours(text: str | None) -> float | None:
    """'23 時間前' / '2 days ago' / '3주 전' -> số giờ."""
    if not text:
        return None
    m = re.search(r"(\d+)\s*(秒|分|時間|日|週間|か月|ヶ月|年|초|분|시간|일|주|개월|년|"
                  r"second|minute|hour|day|week|month|year)", text)
    if not m:
        return None
    return int(m.group(1)) * _AGE_UNITS[m.group(2)]


def _walk_renderers(node, key: str, out: list) -> None:
    if isinstance(node, dict):
        if key in node:
            out.append(node[key])
        for v in node.values():
            _walk_renderers(v, key, out)
    elif isinstance(node, list):
        for v in node:
            _walk_renderers(v, key, out)


class InnerTube:
    def __init__(self, hl: str = "ja", gl: str = "JP", throttle: float = 0.45):
        self.hl, self.gl, self.throttle = hl, gl, throttle
        self.parse_ok = 0
        self.parse_fail = 0
        self.http_retry = 0
        self._s = requests.Session()
        self._s.headers.update({"User-Agent": UA, "Accept-Language": f"{hl},en"})

    @property
    def _ctx(self) -> dict:
        return {"client": {"clientName": "WEB", "clientVersion": "2.20250101.00.00",
                           "hl": self.hl, "gl": self.gl}}

    def search(self, query: str, window: str = "week", tries: int = 3) -> list[dict]:
        """Trả list video đã parse. `window` ∈ today|week|month, luôn sort theo view count.

        Quét nhiều keyword liên tiếp thỉnh thoảng ăn HTTP tạm thời (429/5xx). Không retry
        thì mất hẳn keyword đó và số liệu ngách bị hụt mà không ai biết.
        """
        body = {"context": self._ctx, "query": query, "params": WINDOW_PARAMS[window]}
        r = None
        for i in range(tries):
            r = self._s.post(_SEARCH_URL, json=body, timeout=30)
            time.sleep(self.throttle)
            if r.status_code == 200:
                break
            self.http_retry += 1
            if i < tries - 1:
                time.sleep(2 ** i + 0.5)
        if r.status_code != 200:
            raise RuntimeError(f"InnerTube search HTTP {r.status_code} for {query!r}")
        if any(m in r.text[:4000] for m in _BOT_MARKERS):
            raise BotCheckError(f"bot-check khi search {query!r} — IP đang bị chặn")
        renderers: list = []
        _walk_renderers(r.json(), "videoRenderer", renderers)
        rows = []
        for v in renderers:
            row = self._parse_video(v, query, window)
            if row:
                rows.append(row)
        return rows

    def _parse_video(self, v: dict, query: str, window: str) -> dict | None:
        try:
            owner = (v.get("ownerText") or {}).get("runs") or [{}]
            age_text = ((v.get("publishedTimeText") or {}).get("simpleText")
                        or (v.get("publishedTimeText") or {}).get("runs", [{}])[0].get("text"))
            row = {
                "video_id": v["videoId"],
                "title": (v.get("title") or {}).get("runs", [{}])[0].get("text", ""),
                "channel": owner[0].get("text", ""),
                "channel_id": (owner[0].get("navigationEndpoint") or {})
                              .get("browseEndpoint", {}).get("browseId", ""),
                "views_it": parse_count((v.get("viewCountText") or {}).get("simpleText")),
                "age_hours_it": parse_age_hours(age_text),
                "duration_s_it": parse_length(
                    (v.get("lengthText") or {}).get("simpleText")
                    or (v.get("lengthText") or {}).get("accessibility", {})
                    .get("accessibilityData", {}).get("label")),
                "keyword": query,
                "window": window,
            }
            if not row["video_id"] or not row["channel_id"]:
                raise KeyError("thiếu video_id/channel_id")
            self.parse_ok += 1
            return row
        except Exception:
            self.parse_fail += 1
            return None

    def channel_about(self, channel_id: str) -> dict:
        """Fallback khi Data API không có: subs, total views, ngày tạo kênh."""
        blank = {"subs_it": 0, "total_views_it": 0, "ch_created_it": "", "ch_age_days_it": None}
        try:
            t = self._s.get(f"https://www.youtube.com/channel/{channel_id}/about", timeout=30).text
        except Exception:
            return blank
        if any(m in t[:4000] for m in _BOT_MARKERS):
            raise BotCheckError(f"bot-check khi đọc /about {channel_id}")
        subs = re.search(r'"subscriberCountText":"([^"]{1,40})"', t)
        views = re.search(r'"viewCountText":"([\d,]+)[^"]{0,10}"', t)
        joined = re.search(r'"joinedDateText":\{"content":"([^"]{1,40})"', t)
        out = dict(blank)
        out["subs_it"] = parse_count(subs.group(1) if subs else None)
        out["total_views_it"] = parse_count(views.group(1) if views else None)
        if joined:
            out["ch_created_it"] = joined.group(1)
            d = re.search(r"(\d{4})[/\-年](\d{1,2})[/\-月](\d{1,2})", joined.group(1))
            if d:
                born = dt.date(int(d.group(1)), int(d.group(2)), int(d.group(3)))
                out["ch_age_days_it"] = (dt.date.today() - born).days
        return out
