# -*- coding: utf-8 -*-
"""Bộ nối tới từng nguồn tư liệu. Mỗi hàm trả list dict {src,url,id,title,license,credit}.

Nguyên tắc chung: KHÔNG ĐOÁN giấy phép. Mục nào không ghi rõ public domain / Creative
Commons thì bỏ, kể cả khi nội dung trông có vẻ vô hại.
"""
from __future__ import annotations

import itertools
import os
import re
import time

import requests

UA = {"User-Agent": "Mozilla/5.0 (compatible; stock-research/1.0)"}
TIMEOUT = 45
SAFE_LICENSE = re.compile(r"(publicdomain|creativecommons\.org/(licenses|publicdomain))", re.I)
# CLAUDE.md mục 9: "chỉ đề xuất PD + CC BY" — SA kéo cả video vào share-alike, NC cấm kiếm
# tiền, ND cấm cắt ghép. Kiểm CẢ license short name LẪN license URL, vì short name Commons
# đôi khi thiếu (rỗng) trong khi URL luôn có hậu tố /by-sa/, /by-nc/, /by-nd/.
_BAD_SUFFIX = re.compile(r"(-nc|-nd|-sa)([-/]|$)", re.I)


def _license_ok(lic: str, url_lic: str = "") -> bool:
    text = f"{lic} {url_lic}".lower()
    if "public domain" in text or "publicdomain" in text or text.strip().startswith("cc0"):
        return True
    if _BAD_SUFFIX.search(text):
        return False                      # by-sa / by-nc / by-nd bị loại dù có chữ "cc"
    return "cc by" in text or "cc-by" in text or "/licenses/by/" in text


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
        # Ưu tiên bản TO NHẤT còn nằm trong trần dung lượng — ~orig luôn xếp CUỐI (rank 4).
        #
        # ⚠️ ĐỪNG ĐẢO LẠI THÀNH mobile-first. Bản SPACE_RESEARCH đang xếp mobile trước để né
        # ~orig 5,4 GB; cái giá chỉ lộ ra ở video thành phẩm: NASA ~mobile là **320×180**, phóng
        # lên 1920×1080 là upscale 6× ⇒ nhoè như băng cũ. Đo thật trên video 1 (ep01-tagen-uchu):
        # **73% thời lượng** dựng từ clip 320×180, người xem gọi là "ảnh cũ mờ", và không AI nào
        # cứu nổi 320×180 phóng 6 lần.
        # Nỗi lo ~orig đã được chặn ở TẦNG KHÁC trong stockfetch.py: MAX_BYTES 250 MB (kiểm bằng
        # content-length lúc HEAD *và* kiểm lại giữa dòng tải), MIN_BPS 200 KB/s, MAX_FILE_S 90s.
        # Né bằng cách tự chọn bản bé nhất là chữa đúng bệnh ở sai chỗ.
        rank = {"large": 0, "medium": 1, "small": 2, "mobile": 3}
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
        if not _license_ok(lic, url_lic):
            continue                      # không rõ giấy phép, hoặc SA/NC/ND ⇒ bỏ
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
        if not (SAFE_LICENSE.search(str(lic)) and _license_ok("", str(lic))):
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
_PEXELS_LUOT = itertools.count()


def pexels_cac_key() -> list[str]:
    """Mọi key Pexels khai trong môi trường: `PEXELS_API_KEY` + `PEXELS_API_KEY_<tên>`.

    Hạn mức Pexels tính THEO TỪNG KEY (~200 request/giờ), nên nhiều key = nhiều hạn mức. Đọc theo
    TIỀN TỐ thay vì liệt kê cứng: thêm key mới chỉ cần thêm một dòng vào `.env`, không sửa code.
    """
    ra = []
    for ten, gt in sorted(os.environ.items()):
        if ten.upper().startswith("PEXELS_API_KEY") and gt.strip():
            ra.append(gt.strip())
    # Giữ thứ tự ổn định nhưng bỏ trùng (cùng một key khai hai tên).
    thay, sach = set(), []
    for k in ra:
        if k not in thay:
            thay.add(k)
            sach.append(k)
    return sach


def pexels(query: str, n: int, key: str = "") -> list[dict]:
    """Tìm video Pexels, XOAY VÒNG qua mọi key và NHẢY KEY khi dính hạn mức.

    Vì sao phải xoay: hạn mức tính theo key, mà dự án nghiên cứu bên kia dùng CHUNG một key với
    bên này — lúc cao điểm hai bên ăn vào cùng một hạn mức và chặn nhau. Lỗi này hiện ra dưới dạng
    **"từ khoá không có kết quả"** chứ không phải một thông báo lỗi, nên rất dễ đổ oan cho từ khoá.
    Nay: mỗi lượt gọi bắt đầu từ một key khác (round-robin), dính 429 thì thử ngay key kế tiếp;
    hết sạch key mới chịu trả rỗng.
    """
    keys = [key] if key else pexels_cac_key()
    if not keys:
        return []
    bat_dau = next(_PEXELS_LUOT) % len(keys)
    r = None
    for i in range(len(keys)):
        k = keys[(bat_dau + i) % len(keys)]
        r = requests.get("https://api.pexels.com/videos/search",
                         headers={**UA, "Authorization": k},
                         params={"query": query, "per_page": n}, timeout=TIMEOUT)
        if r.status_code == 429:
            print(f"  … key Pexels #{(bat_dau + i) % len(keys) + 1} hết hạn mức, đổi key")
            continue
        break
    if r is None or r.status_code == 429:
        print("  ! MỌI key Pexels đều hết hạn mức — trả rỗng (KHÔNG phải từ khoá không có hàng)")
        return []
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

# ==== Pixabay + Unsplash — chép từ SPACE_RESEARCH/tools/stock_sources.py 2026-09-20 (anh có key sẵn) ====

import hashlib
import json
import time
from pathlib import Path

MIN_HEIGHT = 720

_BANNED_TITLE = re.compile(r"\b(chart|diagram|graph|map of|screenshot|poster|logo|certificate)\b", re.I)


def _title_ok(title: str) -> bool:
    return not _BANNED_TITLE.search(title or "")


# E3: độ sáng trung bình ≥20 (thang 0-255) — đo thật: clip nguyệt thực lọt vào video 1 với độ
# sáng 14,0 nhìn như khung đen; ngưỡng 20 lấy từ khoảng hở thật trong dữ liệu (13,6 / 14,0 rồi
# nhảy thẳng lên 27,5). Không tải cả video để đo — sample THUMBNAIL nhỏ (vài chục KB) rồi bỏ,
# rẻ hơn hẳn tải video full (vài MB) rồi mới phát hiện quá tối.
MIN_BRIGHTNESS = 20




_CACHE_DIR = Path(__file__).parent / ".cache_pixabay"
CACHE_TTL_S = 86400


def _pixabay_cache_get(key: str):
    f = _CACHE_DIR / f"{key}.json"
    if f.exists() and time.time() - f.stat().st_mtime < CACHE_TTL_S:
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def _pixabay_cache_set(key: str, data) -> None:
    _CACHE_DIR.mkdir(exist_ok=True)
    (_CACHE_DIR / f"{key}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def pixabay(query: str, n: int, keys, media: str = "photo") -> list[dict]:
    if isinstance(keys, str):
        keys = [keys] if keys else []
    keys = [k for k in keys if k]
    if not keys:
        return []
    cache_key = hashlib.sha1(f"{media}:{query}:{n}".encode()).hexdigest()[:20]
    cached = _pixabay_cache_get(cache_key)
    if cached is not None:
        return cached
    import random
    order = keys[:]
    random.shuffle(order)
    url = "https://pixabay.com/api/videos/" if media == "video" else "https://pixabay.com/api/"
    r = None
    for k in order:
        params = {"key": k, "q": query, "per_page": max(n * 2, 3), "safesearch": "true"}
        if media == "photo":
            params["image_type"] = "photo"
            # Verify thật 2026-09-19: dù lọc min_width=1920 ở query, ảnh TẢI VỀ qua largeImageURL
            # vẫn bị Pixabay ép trần 1280px cạnh dài (đo thật 6918×4612 gốc → tải về chỉ 1280×853) —
            # field fullHDURL/imageURL (không ép trần) chỉ có cho app được Pixabay duyệt riêng, app
            # thường KHÔNG có. min_width vẫn giữ lại vì lọc được nguồn chụp chất lượng thật (không
            # phải thumbnail bé tí), chỉ đừng kỳ vọng tải về đúng 1920px.
            params["min_width"] = 1920
        r = requests.get(url, headers=UA, params=params, timeout=TIMEOUT)
        if r.status_code == 429:
            continue          # key này hết ngạch giờ — thử key khác ngay
        break
    if r is None or r.status_code == 429:
        return []             # mọi key đều hết ngạch cùng lúc
    r.raise_for_status()
    out = []
    for h in r.json().get("hits", []):
        tags = h.get("tags", "")
        if not _title_ok(tags):
            continue                      # E4: loại chart/diagram/map/logo... lẫn trong tags
        if media == "photo" and h.get("isAiGenerated"):
            continue                      # Pixabay có LẪN ảnh AI trong kho — loại để giữ đúng mục
                                           # đích "ảnh THẬT thay AI" (Lane E cây cối/hoa lá)
        if media == "video":
            vids = h.get("videos", {})
            best = vids.get("large") or vids.get("medium") or vids.get("small")
            if not best or (best.get("height") or 0) < MIN_HEIGHT:
                continue
            link = best["url"]
        else:
            link = h.get("largeImageURL") or h.get("webformatURL")
            if not link:
                continue
        out.append({
            "src": "pixabay", "id": str(h["id"]), "url": link, "title": tags,
            "license": "Pixabay Content License (free commercial, no attribution)",
            "credit": h.get("user", "")})
        if len(out) >= n:
            break
    _pixabay_cache_set(cache_key, out)
    return out


# ---------- Unsplash: ảnh chất lượng cao, KHÔNG watermark (cả free và Unsplash+) ----------
# Verify 2026-09-19: rate limit theo APPLICATION (API key) — Demo 50/giờ, Production 1000/giờ
# (phải nộp app xin duyệt). Không watermark, nhưng ảnh Unsplash+ (trả phí) KHÔNG cùng license
# free — lọc PHÒNG THỦ nhiều tên field khả dĩ (docs chính thức chưa xác nhận chắc tên field) +
# bắt buộc có links.download_location (theo API Guidelines: mọi ảnh dùng thật phải gọi endpoint
# này để đăng ký lượt download — ảnh thiếu field này coi như đi ngoài luồng chuẩn, bỏ luôn).
# _download_location/_unsplash_key là field NỘI BỘ — stockfetch.py phải pop trước khi ghi
# manifest (không để lộ API key ra file dữ liệu dùng chung).
def unsplash(query: str, n: int, keys) -> list[dict]:
    if isinstance(keys, str):
        keys = [keys] if keys else []
    keys = [k for k in keys if k]
    if not keys:
        return []
    import random
    order = keys[:]
    random.shuffle(order)
    r, used_key = None, None
    for k in order:
        r = requests.get("https://api.unsplash.com/search/photos", headers={
            **UA, "Authorization": f"Client-ID {k}"},
            params={"query": query, "per_page": max(n * 2, 3), "orientation": "landscape"},
            timeout=TIMEOUT)
        if r.status_code in (429, 403):
            continue          # 429/403 = hết ngạch giờ của key này — thử key khác
        used_key = k
        break
    if r is None or r.status_code in (429, 403):
        return []
    r.raise_for_status()
    out = []
    for p in r.json().get("results", []):
        if p.get("premium") or p.get("is_premium") or p.get("plus"):
            continue                      # Unsplash+ — không cùng license free, bỏ
        dl = p.get("links", {}).get("download_location")
        if not dl:
            continue                      # thiếu endpoint download bắt buộc theo guideline ⇒ bỏ
        title = p.get("description") or p.get("alt_description") or ""
        if not _title_ok(title):
            continue                      # E4: loại chart/diagram/map/logo...
        link = p.get("urls", {}).get("full") or p.get("urls", {}).get("regular")
        if not link:
            continue
        out.append({
            "src": "unsplash", "id": p["id"], "url": link, "title": title,
            "license": "Unsplash License (free commercial, no attribution required)",
            "credit": p.get("user", {}).get("name", ""),
            "_download_location": dl, "_unsplash_key": used_key})
        if len(out) >= n:
            break
    return out


