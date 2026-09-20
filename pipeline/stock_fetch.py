# -*- coding: utf-8 -*-
"""Tai video/anh THAT (Pexels; Commons cho canh qua khu) cho cac dong STOCK trong stock_plan.tsv.
Uu tien VIDEO -> ANH. deepseek-v4-flash chon ung vien khop nhat (nguong noi long >=5/10).
Ra: <tap>/stock/*.mp4|jpg + manifest.csv (17 cot nhu ep1) + _filler/ (anh thien nhien chung) + fetch_log.txt
Dung: py -3.13 stock_fetch.py --slug <thu muc tap> --plan stock_plan.tsv
"""
import argparse, csv, json, os, re, sys, time
from datetime import datetime
from pathlib import Path
import requests
ROOT = Path(r"E:\CLAUDE\YOUTUBE\h2dev"); sys.path.insert(0, str(ROOT / "pipeline"))
for line in (ROOT / "pipeline" / ".env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"'))
from stock_sources import UA, TIMEOUT, pexels_cac_key, commons  # noqa: E402
import llm_client as L  # noqa: E402

MAX_VIDEO, MAX_IMG = 90 << 20, 20 << 20
COLS = ["asset_id","scene_id","prompt_line","source","source_url","creator","license","license_url","download_date",
        "media_type","search_query","local_filename","width","height","duration_s","size_bytes","status"]
FILLER_Q = ["autumn leaves japan","river water surface","overcast sky clouds","rain window glass",
            "japanese garden stone","sunset field grass","forest path fog","tea cup steam wood"]
_keys = pexels_cac_key(); _ki = [0]
SAFE = re.compile(r"[^A-Za-z0-9]")

def pget(path, params):
    last = None
    for i in range(len(_keys)):
        k = _keys[(_ki[0] + i) % len(_keys)]
        r = requests.get(f"https://api.pexels.com{path}", headers={**UA, "Authorization": k}, params=params, timeout=TIMEOUT)
        if r.status_code == 429: last = r; continue
        _ki[0] = (_ki[0] + i + 1) % len(_keys); return r
    return last

def video_cands(q, n=8):
    r = pget("/videos/search", {"query": q, "per_page": 15, "orientation": "landscape"})
    out = []
    if r is None or r.status_code != 200: return out
    for v in r.json().get("videos", []):
        dur = v.get("duration") or 0
        if not (4 <= dur <= 90): continue
        files = [f for f in v["video_files"] if f.get("link") and (f.get("width") or 0) >= 1280 and (f.get("width") or 0) >= (f.get("height") or 0)]
        if not files: continue
        files.sort(key=lambda f: (0 if (f.get("width") or 0) >= 1920 else 1, f.get("size") or 10**9))
        f = files[0]
        if (f.get("size") or 0) > MAX_VIDEO: continue
        slug = v["url"].rstrip("/").split("/")[-1]
        out.append({"id": str(v["id"]), "title": re.sub(r"-\d+$", "", slug).replace("-", " "), "media_type": "video",
                    "url": f["link"], "page_url": v["url"], "creator": v.get("user", {}).get("name", ""),
                    "width": f.get("width"), "height": f.get("height"), "duration_s": dur, "size": f.get("size")})
        if len(out) >= n: break
    return out

def image_cands(q, n=8):
    r = pget("/v1/search", {"query": q, "per_page": 15, "orientation": "landscape"})
    out = []
    if r is None or r.status_code != 200: return out
    for p in r.json().get("photos", []):
        if (p.get("width") or 0) < 1920 or not p.get("src", {}).get("original"): continue
        slug = p["url"].rstrip("/").split("/")[-1]
        out.append({"id": str(p["id"]), "title": (p.get("alt") or re.sub(r"-\d+$", "", slug).replace("-", " "))[:120], "media_type": "image",
                    "url": p["src"]["original"], "page_url": p["url"], "creator": p.get("photographer", ""),
                    "width": p.get("width"), "height": p.get("height"), "duration_s": None, "size": None})
        if len(out) >= n: break
    return out

# ---- Pixabay + Unsplash (anh có key sẵn, thêm 2026-09-20) — cùng khuôn dict với video_cands/image_cands ----
from stock_sources import pixabay as _pixabay, unsplash as _unsplash  # noqa: E402
_PIX_KEYS = [os.getenv(k, "") for k in ("PIXABAY_API_KEY", "PIXABAY_API_KEY_2", "PIXABAY_API_KEY_3")]
_UNS_KEYS = [os.getenv(k, "") for k in ("UNSPLASH_ACCESS_KEY", "UNSPLASH_ACCESS_KEY_2")]


def pixabay_video_cands(q, n=8):
    out = []
    try:
        hits = _pixabay(q, n, _PIX_KEYS, media="video")
    except Exception:
        return out
    for h in hits:
        out.append({"id": f"pixabay-v{h['id']}", "title": (h.get("title") or q)[:120], "media_type": "video",
                    "url": h["url"], "page_url": f"https://pixabay.com/videos/id-{h['id']}/", "creator": h.get("credit", ""),
                    "width": 1920, "height": 1080, "duration_s": 10, "size": None, "source": "pixabay",
                    "license": h.get("license", "Pixabay Content License"), "license_url": "https://pixabay.com/service/license-summary/"})
    return out


def pixabay_image_cands(q, n=8):
    out = []
    try:
        hits = _pixabay(q, n, _PIX_KEYS, media="photo")
    except Exception:
        return out
    for h in hits:
        out.append({"id": f"pixabay-p{h['id']}", "title": (h.get("title") or q)[:120], "media_type": "image",
                    "url": h["url"], "page_url": f"https://pixabay.com/photos/id-{h['id']}/", "creator": h.get("credit", ""),
                    "width": 1280, "height": 853, "duration_s": None, "size": None, "source": "pixabay",
                    "license": h.get("license", "Pixabay Content License"), "license_url": "https://pixabay.com/service/license-summary/"})
    return out


def unsplash_cands(q, n=8):
    out = []
    try:
        hits = _unsplash(q, n, _UNS_KEYS)
    except Exception:
        return out
    for h in hits:
        out.append({"id": f"unsplash-{h['id']}", "title": (h.get("title") or q)[:120], "media_type": "image",
                    "url": h["url"], "page_url": f"https://unsplash.com/photos/{h['id']}", "creator": h.get("credit", ""),
                    "width": 1920, "height": 1280, "duration_s": None, "size": None, "source": "unsplash",
                    "license": h.get("license", "Unsplash License"), "license_url": "https://unsplash.com/license",
                    "_download_location": h.get("_download_location"), "_unsplash_key": h.get("_unsplash_key")})
    return out


def _unsplash_dang_ky_tai(item):
    """Unsplash API Guidelines: mỗi ảnh dùng thật phải gọi download_location 1 lần (đăng ký lượt tải)."""
    dl, k = item.get("_download_location"), item.get("_unsplash_key")
    if dl and k:
        try:
            requests.get(dl, headers={**UA, "Authorization": f"Client-ID {k}"}, timeout=TIMEOUT)
        except Exception:
            pass


def pick(prompt, cands, used, log):
    cands = [c for c in cands if c["id"] not in used]
    if not cands: return None, 0
    lst = "\n".join(f"{c['id']}: {c['title']}" + (f" ({c['duration_s']}s)" if c["duration_s"] else "") for c in cands)
    q = ("A story video needs B-roll for this scene prompt:\n" + prompt[:500] + "\n\nCandidates (id: title):\n" + lst +
         "\n\nPick the single best matching candidate by SUBJECT/SETTING (Japanese context preferred, but any plausible match is acceptable). "
         "Score relevance 0-10. Reply ONLY JSON: {\"pick\": \"<id>\" or null, \"score\": N}")
    try:
        r = L.chat(q, provider="ramclouds", model="gemini-3.8-flash", max_tokens=100, temperature=0, tries_per_model=2, verbose=False)
        j = json.loads(re.sub(r"^```(?:json)?|```$", "", r.text.strip(), flags=re.M).strip())
        pid, sc = (str(j.get("pick")) if j.get("pick") else None), float(j.get("score") or 0)
    except Exception as e:
        log.append(f"   llm pick hong: {e}"); return None, 0
    c = next((c for c in cands if c["id"] == pid), None)
    return (c, sc) if c else (None, sc)

def download(item, dest):
    t0 = time.time(); cap = MAX_VIDEO if item["media_type"] == "video" else MAX_IMG; got = 0
    with requests.get(item["url"], headers=UA, timeout=TIMEOUT, stream=True) as r:
        r.raise_for_status()
        with dest.open("wb") as f:
            for ch in r.iter_content(1 << 16):
                got += len(ch)
                if got > cap or time.time() - t0 > 240: raise IOError("qua tran dung luong/thoi gian")
                f.write(ch)
    return got

def row_of(item, line, scene, q, fname, size, status):
    if not item:
        return ["", scene, line, "", "", "", "", "", datetime.now().isoformat(timespec="seconds"), "", q, fname, "", "", "", size or "", status]
    src = item.get("source", "pexels")
    return [f"{src}-{item['id']}", scene, line, src, item["page_url"], item["creator"],
            item.get("license", "Pexels License"), item.get("license_url", "https://www.pexels.com/license/"),
            datetime.now().isoformat(timespec="seconds"), item["media_type"], q, fname,
            item.get("width", ""), item.get("height", ""), item.get("duration_s") or "", size or "", status]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--slug", required=True); ap.add_argument("--plan", required=True)
    ap.add_argument("--min-score", type=float, default=5.0); a = ap.parse_args()
    ep = Path(a.slug); out = ep / "stock"; out.mkdir(exist_ok=True); (out / "_filler").mkdir(exist_ok=True)
    prompts = (ep / "img_prompts.txt").read_text(encoding="utf-8").splitlines()
    m = re.search(r"simbot2-(\d+)", ep.name); tag = f"ep{m.group(1)}" if m else ep.name[:8]
    plan = [r for r in csv.DictReader(Path(a.plan).open(encoding="utf-8"), delimiter="\t") if r["group"] == "STOCK"]
    man = out / "manifest.csv"; used = set(); log = []; T0 = time.time(); nvid = nimg = nnone = 0; llm_calls = 0
    with man.open("w", newline="", encoding="utf-8-sig") as mf:
        w = csv.writer(mf); w.writerow(COLS)
        for r in plan:
            line = int(r["line"]); scene = f"{tag}-L{line:03d}"; prompt = prompts[line - 1]; item = None; sc = 0; usedq = ""; tries = []
            if r["era"] == "historical":
                try:
                    cm = commons(r["image_query"], 6)
                    cc = [{"id": f"commons{i}", "title": str(c.get("title", ""))[:120], "media_type": "image", "url": c["url"],
                           "page_url": c.get("page", c["url"]), "creator": c.get("author", ""), "width": c.get("width", 1920),
                           "height": c.get("height", 1080), "duration_s": None, "size": None, "source": "commons",
                           "license": c.get("license", ""), "license_url": c.get("license_url", "")} for i, c in enumerate(cm or []) if c.get("url")]
                    if cc:
                        item, sc = pick(prompt, cc, used, log); llm_calls += 1; usedq = "commons:" + r["image_query"]
                        if item and sc < a.min_score: item = None
                except Exception as e: log.append(f"L{line}: commons loi {e}")
            # Thứ tự nguồn (2026-09-20, anh có key cả 3): VIDEO trước ẢNH; Pexels → Pixabay → Unsplash.
            for q, fn in ((r["video_query"], video_cands), (r["video_query"], pixabay_video_cands),
                          (r["image_query"], video_cands), (r["image_query"], pixabay_video_cands),
                          (r["image_query"], image_cands), (r["image_query"], pixabay_image_cands),
                          (r["image_query"], unsplash_cands),
                          (r["video_query"], image_cands), (r["video_query"], pixabay_image_cands),
                          (r["video_query"], unsplash_cands)):
                if item or not q: continue
                cands = fn(q); time.sleep(0.3)
                if not cands: tries.append(f"{fn.__name__}:{q}=0"); continue
                it, sc = pick(prompt, cands, used, log); llm_calls += 1
                tries.append(f"{fn.__name__}:{q}={len(cands)}c/{sc:.0f}")
                if it and sc >= a.min_score: item, usedq = it, q
            if not item:
                w.writerow(row_of(None, line, scene, " | ".join(tries), "", "", "NONE")); nnone += 1
                log.append(f"L{line}: NONE  ({' ; '.join(tries)})"); print(f"L{line:03d}: NONE", flush=True); mf.flush(); continue
            ext = ".mp4" if item["media_type"] == "video" else ".jpg"
            fname = f"L{line:03d}_{item.get('source','pexels')}_{SAFE.sub('', item['title'])[:22]}{ext}"
            try: size = download(item, out / fname)
            except Exception as e:
                w.writerow(row_of(item, line, scene, usedq, "", "", f"DOWNLOAD_FAIL:{e}")); log.append(f"L{line}: tai loi {e}"); mf.flush(); continue
            _unsplash_dang_ky_tai(item)     # Unsplash guideline: đăng ký lượt tải; nguồn khác bỏ qua êm
            used.add(item["id"]); w.writerow(row_of(item, line, scene, usedq, fname, size, "OK")); mf.flush()
            if item["media_type"] == "video": nvid += 1
            else: nimg += 1
            msg = f"L{line:03d}: OK {item['media_type']} {item['width']}x{item['height']} {item.get('duration_s') or ''}s score={sc:.0f} {size/1048576:.1f}MB - {item['title'][:50]!r}"
            print(msg, flush=True); log.append(msg)
        nfill = 0
        for q in FILLER_Q:
            cands = image_cands(q, 3); time.sleep(0.3)
            for c in cands:
                if c["id"] in used: continue
                fname = f"F{nfill+1:02d}_{SAFE.sub('', c['title'])[:22]}.jpg"
                try: size = download(c, out / "_filler" / fname)
                except Exception: continue
                used.add(c["id"]); w.writerow(row_of(c, 0, f"{tag}-FILLER", q, "_filler/" + fname, size, "FILLER")); nfill += 1; break
    summ = f"STOCK {len(plan)} dong: video={nvid} image={nimg} NONE={nnone} · filler={nfill} · llm={llm_calls} lan · {(time.time()-T0)/60:.1f} phut"
    log.append(summ); (Path(__file__).resolve().parent / "fetch_log.txt").write_text("\n".join(log) + "\n", encoding="utf-8"); print(summ)

if __name__ == "__main__": main()
