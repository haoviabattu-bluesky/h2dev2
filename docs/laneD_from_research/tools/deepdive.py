# -*- coding: utf-8 -*-
"""Đào sâu top video: transcript + comment → hook, pattern title, insight khán giả.

Tầng 1 (luôn chạy, không cần API ngoài): bóc dữ kiện thô — hook 30–60s đầu,
pattern title, comment nhiều like nhất.
Tầng 2 (tuỳ chọn): đưa dữ kiện đó cho LLM tóm tắt thành insight dùng được ngay.
"""
from __future__ import annotations

import collections
import re

_VOTE_UNITS = {"N": 1e3, "Tr": 1e6, "K": 1e3, "M": 1e6, "万": 1e4, "億": 1e8, "천": 1e3, "만": 1e4}


def parse_votes(v) -> int:
    """youtube-comment-downloader trả CHUỖI viết tắt theo locale ('311 N') — không int() thẳng."""
    if isinstance(v, int):
        return v
    if not v:
        return 0
    s = str(v).replace(",", "").replace(".", "").strip()
    m = re.match(r"([\d]+)\s*([A-Za-z万億천만]*)", s)
    if not m:
        return 0
    return int(int(m.group(1)) * _VOTE_UNITS.get(m.group(2), 1))


def fetch_transcript(video_id: str, languages: list[str]) -> list[dict]:
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    return api.fetch(video_id, languages=languages).to_raw_data()


def fetch_comments(video_id: str, limit: int = 80) -> list[dict]:
    from youtube_comment_downloader import SORT_BY_POPULAR, YoutubeCommentDownloader
    d = YoutubeCommentDownloader()
    out = []
    for c in d.get_comments(video_id, sort_by=SORT_BY_POPULAR):
        out.append({"text": c.get("text", ""), "votes": parse_votes(c.get("votes")),
                    "is_reply": bool(c.get("reply")), "author": c.get("author", "")})
        if len(out) >= limit:
            break
    return out


def hook_text(segments: list[dict], seconds: int = 45) -> str:
    return " ".join(s["text"] for s in segments if s["start"] < seconds).strip()


def title_patterns(titles: list[str], top: int = 8) -> str:
    """Cấu trúc title lặp lại trong ngày: khối 【】, con số, cụm mở đầu."""
    brackets = collections.Counter()
    numbers = collections.Counter()
    for t in titles:
        for b in re.findall(r"[【\[]([^】\]]{1,12})[】\]]", t):
            brackets[b] += 1
        for n in re.findall(r"(\d+)\s*(選|つ|個|の理由|大|位)", t):
            numbers["".join(n)] += 1
    parts = []
    if brackets:
        parts.append("【】: " + ", ".join(f"{k}×{v}" for k, v in brackets.most_common(top)))
    if numbers:
        parts.append("số: " + ", ".join(f"{k}×{v}" for k, v in numbers.most_common(top)))
    return " | ".join(parts) or "—"


def analyze(video: dict, languages: list[str], all_titles: list[str],
            comment_limit: int = 80) -> dict:
    """Tầng 1 — dữ kiện thô, không phụ thuộc dịch vụ ngoài. Lỗi thì ghi lý do, không ném."""
    out = {"video_id": video["video_id"], "hook": "", "transcript_chars": 0,
           "wpm": None, "top_comments": "", "title_pattern": title_patterns(all_titles),
           "errors": []}
    try:
        segs = fetch_transcript(video["video_id"], languages)
        out["hook"] = hook_text(segs)[:1200]
        full = " ".join(s["text"] for s in segs)
        out["transcript_chars"] = len(full)
        dur_min = max((video.get("duration_s") or 0) / 60, 1)
        out["wpm"] = round(len(full) / dur_min)
        out["_transcript"] = full[:12000]
    except Exception as e:
        out["errors"].append(f"transcript: {type(e).__name__}")
    try:
        cs = [c for c in fetch_comments(video["video_id"], comment_limit) if not c["is_reply"]]
        cs.sort(key=lambda c: c["votes"], reverse=True)
        out["top_comments"] = "\n".join(f"({c['votes']}👍) {c['text'][:180]}" for c in cs[:12])
        out["_comments"] = cs[:40]
    except Exception as e:
        out["errors"].append(f"comments: {type(e).__name__}")
    return out


INSIGHT_PROMPT = """Bạn phân tích 1 video YouTube đang bứt phá để tôi nhân bản công thức.

TIÊU ĐỀ: {title}
KÊNH: {channel} ({subs} subs, kênh {ch_age} ngày tuổi) — video đạt {views} view
30-45 GIÂY ĐẦU (hook): {hook}
TRANSCRIPT (rút gọn): {transcript}
COMMENT NHIỀU LIKE NHẤT:
{comments}

Trả lời NGẮN GỌN bằng tiếng Việt, đúng 4 mục, mỗi mục tối đa 3 gạch đầu dòng:
1. HOOK: cách mở đầu giữ chân người xem là gì
2. CẤU TRÚC: video được sắp xếp thế nào
3. INSIGHT KHÁN GIẢ: họ thực sự quan tâm/đau đáu điều gì (dựa vào comment)
4. 3 Ý TƯỞNG TITLE mới cho cùng ngách (viết bằng ngôn ngữ gốc của video)"""


def llm_insight(payload: dict, video: dict, base_url: str, api_key: str,
                model: str, timeout: int = 120) -> str:
    """Tầng 2 — tuỳ chọn. Không có key / lỗi mạng thì trả chuỗi rỗng, pipeline vẫn chạy."""
    if not api_key:
        return ""
    import requests
    prompt = INSIGHT_PROMPT.format(
        title=video.get("title", ""), channel=video.get("channel", ""),
        subs=video.get("subs", 0), ch_age=video.get("ch_age_days"),
        views=video.get("views", 0), hook=payload.get("hook", "")[:1500],
        transcript=payload.get("_transcript", "")[:6000],
        comments=payload.get("top_comments", "")[:2500])
    try:
        r = requests.post(f"{base_url}/chat/completions",
                          headers={"Authorization": f"Bearer {api_key}"},
                          json={"model": model, "messages": [{"role": "user", "content": prompt}],
                                "max_tokens": 900, "temperature": 0.4}, timeout=timeout)
        if r.status_code != 200:
            return f"[LLM {r.status_code}]"
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[LLM {type(e).__name__}]"
