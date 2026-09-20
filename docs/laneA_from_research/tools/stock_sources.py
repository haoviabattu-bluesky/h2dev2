# -*- coding: utf-8 -*-
"""Bộ nối tới từng nguồn tư liệu. Mỗi hàm trả list dict {src,url,id,title,license,credit}.

Nguyên tắc chung: KHÔNG ĐOÁN giấy phép. Mục nào không ghi rõ public domain / Creative
Commons thì bỏ, kể cả khi nội dung trông có vẻ vô hại.
"""
from __future__ import annotations

import re
import time

import requests

UA = {"User-Agent": "Mozilla/5.0 (compatible; stock-research/1.0)"}
TIMEOUT = 45
SAFE_LICENSE = re.compile(r"(publicdomain|creativecommons\.org/(licenses|publicdomain))", re.I)


def _get(url, **kw):
    r = requests.get(url, headers=UA, timeout=TIMEOUT, **kw)
    r.raise_for_status()
    return r


# ---------- NASA: public domain, không cần key ----------
def nasa(query: str, n: int, media: str = "video") -> list[dict]:
    r = _get("https://images-api.nasa.gov/search", params={"q": query, "media_type": media})
    out = []
    for it in r.json()["collection"]["items"][: n * 3]:
        d = it["data"][0]
        if d.get("copyright"):
            continue                      # hiếm, nhưng NASA KHÔNG phải 100% public domain
        try:
            assets = _get(it["href"]).json()
        except Exception:
            continue
        want = ".mp4" if media == "video" else (".jpg", ".png")
        files = [u for u in assets if u.lower().endswith(want)]
        # Ưu tiên bản NHỎ. Đã dính thật: item không có bản ~medium thì rơi vào ~orig
        # và tải về 5,4 GB cho MỘT clip. ~orig luôn xếp cuối.
        rank = {"mobile": 0, "medium": 1, "small": 2, "large": 3}
        files.sort(key=lambda u: next((v for k, v in rank.items() if k in u), 4))
        if not files:
            continue
        out.append({"src": "nasa", "url": files[0], "title": d.get("title", ""),
                    "id": d.get("nasa_id", ""), "license": "Public Domain (NASA)",
                    "credit": f"NASA / {d.get('center', '')}".strip(" /")})
        if len(out) >= n:
            break
    return out


# ---------- Wikimedia Commons: đọc giấy phép của TỪNG file ----------
def commons(query: str, n: int) -> list[dict]:
    r = _get("https://commons.wikimedia.org/w/api.php", params={
        "action": "query", "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap", "gsrnamespace": 6,
        "gsrlimit": n * 2, "prop": "imageinfo",
        "iiprop": "url|extmetadata", "format": "json"})
    out = []
    for p in r.json().get("query", {}).get("pages", {}).values():
        ii = p["imageinfo"][0]
        em = ii.get("extmetadata", {})
        lic = em.get("LicenseShortName", {}).get("value", "")
        url_lic = em.get("LicenseUrl", {}).get("value", "")
        if not (SAFE_LICENSE.search(url_lic) or "public domain" in lic.lower()
                or lic.upper().startswith("CC")):
            continue                      # không rõ giấy phép ⇒ bỏ, không đoán
        time.sleep(0.4)   # Commons tra 429 khi goi lien tiep
        out.append({"src": "commons", "url": ii["url"], "title": p["title"],
                    "id": p["title"], "license": lic,
                    "credit": re.sub("<[^>]+>", "",
                                     em.get("Artist", {}).get("value", "")).strip()[:120]})
        if len(out) >= n:
            break
    return out


# ---------- Internet Archive: BẮT BUỘC lọc giấy phép ----------
def archive(query: str, n: int) -> list[dict]:
    q = (f'({query}) AND mediatype:movies AND '
         f'(licenseurl:*publicdomain* OR licenseurl:*creativecommons*)')
    r = _get("https://archive.org/advancedsearch.php", params=[
        ("q", q), ("fl[]", "identifier"), ("fl[]", "licenseurl"), ("fl[]", "title"),
        ("rows", str(n * 2)), ("output", "json")])
    out = []
    for d in r.json()["response"]["docs"]:
        lic = d.get("licenseurl", "")
        if not SAFE_LICENSE.search(str(lic)):
            continue
        try:
            files = _get(f"https://archive.org/metadata/{d['identifier']}").json().get("files", [])
        except Exception:
            continue
        mp4 = [f for f in files if f.get("name", "").lower().endswith(".mp4")]
        if not mp4:
            continue
        mp4.sort(key=lambda f: int(f.get("size") or 0))
        out.append({"src": "archive", "id": d["identifier"], "title": d.get("title", ""),
                    "url": f"https://archive.org/download/{d['identifier']}/{mp4[0]['name']}",
                    "license": lic, "credit": f"Internet Archive / {d['identifier']}"})
        if len(out) >= n:
            break
    return out


# ---------- Pexels / Pixabay: cần key miễn phí ----------
def pexels(query: str, n: int, key: str) -> list[dict]:
    if not key:
        return []
    r = requests.get("https://api.pexels.com/videos/search",
                     headers={**UA, "Authorization": key},
                     params={"query": query, "per_page": n}, timeout=TIMEOUT)
    r.raise_for_status()
    out = []
    for v in r.json().get("videos", []):
        files = sorted(v["video_files"], key=lambda f: f.get("width") or 0)
        hd = [f for f in files if (f.get("width") or 0) >= 1280] or files[-1:]
        out.append({"src": "pexels", "id": str(v["id"]), "url": hd[0]["link"],
                    "title": (v.get("url") or "").rstrip("/").split("/")[-1],
                    "license": "Pexels License (free commercial, no attribution)",
                    "credit": v.get("user", {}).get("name", "")})
    return out


