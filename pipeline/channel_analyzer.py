"""channel_analyzer.py — K1+K2 (đặt tên riêng K1/K2/K3, KHÔNG dùng B1/B2/B3 — trùng số bước B0-B11
của pipeline sản xuất 1 TẬP ở make_video.py, vd B3 ở MỌI lane = "viết kịch bản"; đây là việc CẤP
KÊNH, 1 lần/kênh, không phải 1 lần/tập): crawl N video top-view của 1 kênh đối thủ (K1, thuần
Python) + gọi Gemini tổng hợp thành CHANNEL_DNA.md + VIDEO_ANALYSIS/<id>.json (K2, ĐÂY mới gọi
Gemini). KHÔNG cần Claude phán xét lúc chạy — chạy độc lập, 1 lần/kênh, ở BẤT KỲ máy nào có Python +
mạng (không bắt buộc phải qua máy 2).

Tách phần "đọc N video + tổng hợp DNA" ra khỏi Claude (xem
docs/superpowers/specs/2026-09-16-gemini-channel-analyzer-design.md): Claude không còn phải tự đọc
transcript thô nữa, chỉ đọc CHANNEL_DNA.md (súc tích) + VIDEO_ANALYSIS/*.json (đã chọn lọc qua
retrieve_videos.py) để viết kịch bản.

Dùng:
  py -3.13 channel_analyzer.py --channel-url "https://www.youtube.com/channel/<id>" \
      --out-dir docs/channel_dna/<slug> --n-candidates 20 --n-select 10 --niche-hint "都市伝説・ミステリー"

Quy tắc chọn video (chốt 2026-09-16): xét TOÀN BỘ kênh nếu có <= --n-candidates (mặc định 20) video;
kênh lớn hơn thì chỉ xét top --n-candidates theo view_count. Từ pool ứng viên đó, CHỌN LỌC --n-select
(mặc định 10) video có view cao nhất VÀ lấy được transcript để đưa vào phân tích Gemini — ít hơn
--n-select thì lấy hết những gì có (không ép đủ số). Video đã có sẵn VIDEO_ANALYSIS/<id>.json từ lần
chạy trước (ví dụ mở rộng pool 8→20 của cùng 1 kênh) được TÁI DÙNG, không gọi lại Gemini — tiết kiệm
quota khi chạy lại/mở rộng cho cùng kênh.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import llm_client

sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------- K1: crawl
def crawl_catalog(channel_url, n_candidates, proxy=None, meta_lang=""):
    """Trả (tong_so_video_kenh, candidates): candidates = list [{"id","title","view_count",
    "duration"}] ứng viên. Kênh có <= n_candidates video → lấy HẾT; nhiều hơn → lấy top
    n_candidates theo view_count giảm dần (bước chọn lọc --n-select xảy ra ở nơi khác, sau khi
    đã biết video nào lấy được transcript).

    meta_lang: mã ngôn ngữ gốc của kênh ("ja", "ko"...). Mặc định "" = giữ hành vi cũ. YouTube trả
    TIÊU ĐỀ ĐÃ TỰ DỊCH theo ngôn ngữ giao diện (kênh Nhật ra title tiếng Anh) → phân tích công thức
    tiêu đề/độ dài tiêu đề trên bản dịch là SAI (đã dính thật ở kênh どっこい日本史 2026-09-23: DNA kết
    luận "tiêu đề Nhật 38-52 ký tự" trong khi title Nhật thật median 36). Đặt meta_lang thì crawl
    THÊM 1 lượt với extractor_args youtube:lang=<mã> để lấy title gốc rồi ghép theo video id —
    PHẢI ghép chứ không thay hẳn, vì lượt crawl có lang=... trả view_count = None."""
    import yt_dlp
    opts = {"quiet": True, "no_warnings": True, "extract_flat": True, "noprogress": True,
            "playlistend": 500}
    if proxy:
        opts["proxy"] = proxy
    url = channel_url.rstrip("/") + "/videos"
    with yt_dlp.YoutubeDL(opts) as y:
        info = y.extract_info(url, download=False)
    titles_native = {}
    if meta_lang:
        opts_native = dict(opts, extractor_args={"youtube": {"lang": [meta_lang]}})
        try:
            with yt_dlp.YoutubeDL(opts_native) as y:
                info_native = y.extract_info(url, download=False)
            titles_native = {e["id"]: e.get("title") or ""
                             for e in (info_native or {}).get("entries") or [] if e}
            print(f"  → lấy {len(titles_native)} tiêu đề gốc (lang={meta_lang}), thay bản dịch")
        except Exception as e:
            print(f"  ✗ không lấy được tiêu đề gốc lang={meta_lang}, dùng bản YouTube trả mặc "
                  f"định: {type(e).__name__} {str(e)[:100]}")
    rows = []
    for e in (info or {}).get("entries") or []:
        if not e:
            continue
        rows.append({"id": e.get("id"),
                     "title": titles_native.get(e.get("id")) or e.get("title") or "",
                     "view_count": e.get("view_count") or 0,
                     "duration": e.get("duration") or 0})
    total = len(rows)
    rows.sort(key=lambda r: r["view_count"], reverse=True)
    candidates = rows if total <= n_candidates else rows[:n_candidates]
    return total, candidates


def crawl_tag_stats(candidates, out_dir, proxy=None, channel_url=""):
    """Gom Video Tags (từ HTML /watch) của toàn bộ pool candidates + Channel Tags của kênh →
    out_dir/TAG_STATS.json. THUẦN PHỤ, không phải bước bắt buộc của K1/K2: lỗi (mạng, IP chặn,
    kênh không khai tag) chỉ in cảnh báo rồi trả None, KHÔNG raise — không được làm gãy pipeline
    DNA chính. Dùng candidates (pool đầy đủ, KHÔNG chỉ n-select) vì tag không cần transcript."""
    import yt_tags
    try:
        stats = yt_tags.build_tag_stats(candidates, proxy=proxy, channel_url=channel_url)
    except Exception as e:
        print(f"  ✗ TAG_STATS bỏ qua: {type(e).__name__} {str(e)[:120]}")
        return None
    out_path = out_dir / "TAG_STATS.json"
    out_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → {stats['n_videos_with_tags']}/{stats['n_videos_total']} video có tag, "
          f"{len(stats['top_tags'])} tag khác nhau → {out_path}")
    return stats


def crawl_transcripts(rows, langs, out_dir, proxy=None):
    """Ghi/tái dùng out_dir/_raw/transcripts.json. Trả list đã có transcript (video lỗi bị loại)."""
    import fetch_script
    raw_path = out_dir / "_raw" / "transcripts.json"
    if raw_path.exists():
        cached = json.loads(raw_path.read_text(encoding="utf-8"))
        if len(cached) >= len(rows):
            print(f"  … dùng lại {raw_path} ({len(cached)} video, bỏ qua crawl)")
            return cached
    out = []
    for r in rows:
        try:
            segs, used = fetch_script.fetch_any(r["id"], langs, proxy=proxy)
            text = re.sub(r"\s+", " ", " ".join(s["text"] for s in segs)).strip()
            out.append({**r, "transcript": text})
            print(f"  ✓ {r['id']} [{used}]: {len(text):,} ký tự — {r['title'][:50]}")
        except SystemExit as e:
            print(f"  ✗ {r['id']} bỏ qua: {e}")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


# ---------------------------------------------------------------- K2: Gemini
VIDEO_PROMPT = """Bạn phân tích 1 video YouTube ngách "{niche_hint}". Dữ liệu:
TIÊU ĐỀ: {title}
LƯỢT XEM: {view_count}
TRANSCRIPT (rút gọn nếu quá dài):
{transcript}

Trả về ĐÚNG 1 JSON (không kèm giải thích, không bọc ```markdown```), đúng khoá. QUAN TRỌNG: field
"topics" PHẢI viết bằng ĐÚNG ngôn ngữ gốc của TIÊU ĐỀ/TRANSCRIPT ở trên (không dịch sang tiếng Việt)
— vì sau này sẽ so khớp substring với câu hỏi cùng ngôn ngữ đó. Mỗi phần tử là 1 khái niệm NGẮN DUY
NHẤT (không ghép 2 khái niệm bằng dấu / hay dấu phẩy trong cùng 1 phần tử, vd viết "UFO" và "UAP"
thành 2 phần tử riêng thay vì "UFO/UAP"):
{{"topics": ["từ khoá ngắn 1 (ngôn ngữ gốc video)", "từ khoá ngắn 2 (ngôn ngữ gốc video)", "..."],
  "hook_type": "mô tả cách mở đầu, 1 câu",
  "structure": "mô tả cấu trúc/chương chính, 1-2 câu",
  "emotional_beats": ["cảm xúc chính 1", "..."],
  "title_formula": "công thức tiêu đề video này áp dụng, 1 câu",
  "notes": "chi tiết đáng chú ý khác, có thể để rỗng"}}"""

DNA_PROMPT = """Bạn là chuyên gia phân tích kênh YouTube ngách "{niche_hint}". Dưới đây là {n} video
top view của kênh (tiêu đề + lượt xem + toàn văn lời thoại). Hãy tổng hợp thành 1 tài liệu Markdown
CHANNEL_DNA.md đúng cấu trúc 11 đề mục sau (mỗi đề mục 1 heading ## + vài gạch đầu dòng, TRÍCH DẪN
BẰNG CHỨNG THẬT từ dữ liệu, không bịa, không chung chung):

## Audience — khán giả là ai, nỗi đau/động cơ khiến họ xem
## Content pillars — các trụ cột chủ đề lặp lại
## Narrative style — giọng kể, ngôi kể, văn phong
## Hook formulas — cách mở đầu lặp lại, kèm ví dụ trích
## Story structure — cấu trúc/chương thường gặp
## Pacing — nhịp giữ chân (đảo chiều, mốc sự kiện, câu hỏi thẳng...), có số đo nếu đếm được
## Emotional triggers — cảm xúc được khai thác
## CTA patterns — lời kêu gọi hành động cuối video
## Title patterns — công thức tiêu đề lặp lại, độ dài tối ưu nếu tính được
## Thumbnail patterns — mô tả suy luận được từ tiêu đề/nội dung (không có ảnh thì ghi "không đủ dữ
   liệu", KHÔNG bịa)
## Rules for writing new videos — 5-8 quy tắc cụ thể để viết video MỚI giống đúng công thức kênh này

DỮ LIỆU {n} VIDEO:
{videos_block}"""


def _strip_fence(text):
    """Bỏ bọc ```json ... ``` nếu model trả kèm (bẫy đã biết trong dự án: gpt_api_codex.md)."""
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
        t = re.sub(r"\n?```$", "", t)
    return t.strip()


def load_or_analyze_video(row, niche_hint, out_dir):
    """Tái dùng VIDEO_ANALYSIS/<id>.json nếu đã có (lần chạy trước, vd mở rộng pool 8→20 của
    cùng kênh) — không gọi lại Gemini cho video đã phân tích rồi."""
    cache_path = out_dir / "VIDEO_ANALYSIS" / f"{row['id']}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8")), True
    data = analyze_one_video(row, niche_hint)
    cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data, False


def analyze_one_video(row, niche_hint):
    prompt = VIDEO_PROMPT.format(niche_hint=niche_hint, title=row["title"],
                                 view_count=row["view_count"],
                                 transcript=row["transcript"][:20000])
    r = llm_client.chat(prompt, task="short", max_tokens=2000, temperature=0.3, verbose=False)
    data = json.loads(_strip_fence(r.text))
    data["video_id"] = row["id"]
    data["title"] = row["title"]
    data["view_count"] = row["view_count"]
    data["duration_min"] = round(row["duration"] / 60.0, 1) if row["duration"] else 0.0
    return data


def synthesize_dna(rows, niche_hint):
    block = "\n\n".join(
        f"--- Video {i+1} ---\nTiêu đề: {r['title']}\nLượt xem: {r['view_count']}\n"
        f"Lời thoại: {r['transcript'][:15000]}"
        for i, r in enumerate(rows))
    prompt = DNA_PROMPT.format(niche_hint=niche_hint, n=len(rows), videos_block=block)
    r = llm_client.chat(prompt, task="analysis", max_tokens=16000, temperature=0.4,
                        min_chars=800, require_sentence_end=False)
    return r.text


# ---------------------------------------------------------------- QC
def qc_dna(text):
    n_chars = len(text.replace("\n", "").replace(" ", ""))
    n_heads = len(re.findall(r"^##\s", text, re.MULTILINE))
    ok = n_chars >= 800 and n_heads >= 8
    print(f"  {'✓' if ok else '✗'} QC DNA: {n_chars} ký tự, {n_heads}/11 đề mục "
          f"{'ĐẠT' if ok else 'TRƯỢT — kiểm lại prompt/model'}")
    return ok


# ---------------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel-url", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--n-candidates", type=int, default=20,
                    help="pool ứng viên tối đa xét theo view_count; kênh có ít hơn số này thì xét "
                         "HẾT kênh")
    ap.add_argument("--n-select", type=int, default=10,
                    help="số video CHỌN LỌC (view cao nhất, có transcript) đưa vào phân tích Gemini")
    ap.add_argument("--langs", default="ja,en")
    ap.add_argument("--meta-lang", default="",
                    help="mã ngôn ngữ GỐC của kênh (vd ja) để lấy TIÊU ĐỀ GỐC thay vì bản YouTube "
                         "tự dịch — bắt buộc khi muốn phân tích công thức/độ dài tiêu đề")
    ap.add_argument("--niche-hint", default="")
    ap.add_argument("--proxy", default="",
                    help="proxy HTTP(S) cho cả crawl catalog lẫn transcript, dùng khi IP bị "
                         "YouTube 429 kéo dài, vd http://user:pass@host:port")
    ap.add_argument("--no-tags", action="store_true",
                    help="tắt bước gom Video Tags/Channel Tags → TAG_STATS.json (bật mặc định, "
                         "phụ trợ, không ảnh hưởng K1/K2 nếu lỗi)")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    langs = args.langs.split(",")
    niche_hint = args.niche_hint or args.channel_url
    proxy = args.proxy or None

    t0 = time.time()
    print(f"[K1] Crawl catalog {args.channel_url} ...")
    total, candidates = crawl_catalog(args.channel_url, args.n_candidates, proxy=proxy,
                                      meta_lang=args.meta_lang)
    print(f"  → kênh có {total} video · lấy {len(candidates)} ứng viên (view cao nhất), "
          f"{time.time()-t0:.0f}s")

    if not args.no_tags:
        print(f"[K1] Gom Video Tags/Channel Tags ({len(candidates)} video, không cần transcript) ...")
        crawl_tag_stats(candidates, out_dir, proxy=proxy, channel_url=args.channel_url)

    t1 = time.time()
    print(f"[K1] Crawl transcript {len(candidates)} video ứng viên ...")
    candidates = crawl_transcripts(candidates, langs, out_dir, proxy=proxy)
    print(f"  → {len(candidates)}/{args.n_candidates} ứng viên có transcript, {time.time()-t1:.0f}s")
    if not candidates:
        raise SystemExit("Không crawl được transcript video nào — dừng.")

    # candidates đã sắp theo view_count giảm dần (giữ nguyên thứ tự từ crawl_catalog) → chọn lọc
    # --n-select video ĐẦU (view cao nhất, đã có transcript). Không đủ --n-select thì lấy hết.
    rows = candidates[:args.n_select]
    print(f"  → chọn lọc {len(rows)}/{args.n_select} video tốt nhất để đưa vào phân tích")

    t2 = time.time()
    print("[K2] Gọi Gemini phân tích từng video (task=short) ...")
    (out_dir / "VIDEO_ANALYSIS").mkdir(exist_ok=True)
    n_ok, n_cached = 0, 0
    for r in rows:
        try:
            _, from_cache = load_or_analyze_video(r, niche_hint, out_dir)
            n_ok += 1
            n_cached += 1 if from_cache else 0
            print(f"  {'…' if from_cache else '✓'} {r['id']} "
                  f"{'đã phân tích trước đó, dùng lại' if from_cache else 'phân tích xong'}")
        except Exception as e:
            print(f"  ✗ {r['id']} phân tích lỗi: {type(e).__name__} {str(e)[:120]}")
    pct = n_ok / len(rows) * 100 if rows else 0
    print(f"  → {n_ok}/{len(rows)} video ({pct:.0f}%) sẵn sàng ({n_cached} lấy từ cache cũ, "
          f"bỏ qua video đã làm), {time.time()-t2:.0f}s")
    if pct < 70:
        print("  ⚠ CẢNH BÁO: dưới 70% video phân tích được, kiểm lại lỗi ở trên")

    t3 = time.time()
    print("[K2] Gọi Gemini tổng hợp CHANNEL_DNA.md (task=analysis) ...")
    dna_text = synthesize_dna(rows, niche_hint)
    (out_dir / "CHANNEL_DNA.md").write_text(dna_text, encoding="utf-8")
    print(f"  → xong, {time.time()-t3:.0f}s")
    qc_dna(dna_text)

    print(f"\n✓ TỔNG: {time.time()-t0:.0f}s → {out_dir}")


if __name__ == "__main__":
    main()
