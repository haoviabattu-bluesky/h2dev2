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
    # 2026-09-23: bên cạnh transcript gộp, còn lưu thô để hook_stage.py (task sau) dùng lại mốc
    # giây thật + mô tả gốc + ảnh thumbnail — không phải mọi kênh đều cần nhưng ghi chung, rẻ.
    (out_dir / "_raw" / "segments").mkdir(parents=True, exist_ok=True)
    (out_dir / "_raw" / "meta").mkdir(parents=True, exist_ok=True)
    (out_dir / "_raw" / "thumbs").mkdir(parents=True, exist_ok=True)
    for rank, r in enumerate(rows, 1):
        try:
            segs, used = fetch_script.fetch_any(r["id"], langs, proxy=proxy)
            text = re.sub(r"\s+", " ", " ".join(s["text"] for s in segs)).strip()
            dau = re.sub(r"\s+", " ", " ".join(s["text"] for s in segs if float(s.get("start", 0)) < 30)).strip()
            meta = fetch_script.lay_meta_video(r["id"], proxy=proxy)
            (out_dir / "_raw" / "segments" / f"{r['id']}.json").write_text(
                json.dumps([{"start": float(s.get("start", 0)), "duration": float(s.get("duration", 0)),
                             "text": s["text"]} for s in segs], ensure_ascii=False), encoding="utf-8")
            (out_dir / "_raw" / "meta" / f"{r['id']}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1),
                                                                        encoding="utf-8")
            if meta.get("thumbnail_url"):
                fetch_script.tai_anh(meta["thumbnail_url"],
                                     out_dir / "_raw" / "thumbs" / f"{rank:02d}_{r.get('view_count', 0)}_{r['id']}.jpg",
                                     proxy=proxy)
            out.append({**r, "transcript": text, "description": meta.get("description", ""), "dau_0_30s": dau})
            print(f"  ✓ {r['id']} [{used}]: {len(text):,} ký tự — {r['title'][:50]}")
        except SystemExit as e:
            print(f"  ✗ {r['id']} bỏ qua: {e}")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


# --------------------------------------------- K1b: ĐỌC CHỮ TRÊN ẢNH THUMBNAIL (G7, 2026-09-23)
# Bàn giao TRENDING-RESEARCH: "K2 phải nhận ảnh thumbnail thật (vision) và chép chữ từng dòng, CẤM
# mục 'suy luận'". Trước đây DNA_PROMPT bảo model "mô tả suy luận được từ tiêu đề/nội dung" — tức là
# đoán chữ trên ảnh, đúng thứ bàn giao cấm. Ảnh đã tải sẵn ở `_raw/thumbs/` từ bước crawl, ở đây chỉ
# thêm một lượt đọc ảnh.
# Vì sao dùng sol_client chứ không llm_client: llm_client.chat() KHÔNG có đường truyền ảnh; sol_client
# đã có sẵn `image_path` + 3 đường fallback và chính là lớp QC vision của dự án (qc_thumbnail_sol.py).
THUMB_PROMPT = """Đây là ảnh thumbnail của một video YouTube.
CHÉP LẠI chữ trên ảnh, ĐÚNG NGUYÊN VĂN, mỗi dòng chữ một phần tử, theo thứ tự trên xuống dưới.
TUYỆT ĐỐI KHÔNG dịch, KHÔNG tóm tắt, KHÔNG suy luận, KHÔNG đoán chữ bị che. Chữ nào không đọc được
thì ghi "?" ở đúng vị trí đó.
Trả ĐÚNG 1 JSON: {"dong_chu": ["dòng 1", "dòng 2"], "bo_cuc": "1 câu tả bố cục: vị trí/màu từng khối chữ, có mặt người không", "doc_duoc": true}
Ảnh không có chữ nào thì trả "dong_chu": [] và "doc_duoc": true."""


def doc_chu_thumbnail(anh):
    """Trả dict {'dong_chu': [...], 'bo_cuc': str} hoặc None khi không đọc được.

    KHÔNG BAO GIỜ ném: thiếu ảnh / hỏng mạng / model trả rác chỉ làm mất phần thumbnail của MỘT
    video, không được làm gãy cả lượt phân tích kênh (cùng chính sách với bước tags: phụ trợ).
    """
    try:
        import sol_client
        r = sol_client.chat(THUMB_PROMPT, image_path=str(anh), max_tokens=800)
        d = json.loads(_strip_fence(r if isinstance(r, str) else getattr(r, "text", str(r))))
        return d if isinstance(d.get("dong_chu"), list) else None
    except Exception as e:
        print(f"  ! không đọc được chữ trên {Path(anh).name}: {type(e).__name__} {str(e)[:90]}")
        return None


def gan_chu_thumbnail(rows, out_dir):
    """Đọc chữ thumbnail cho từng video, ghi cache `_raw/thumb_text/<id>.json` (đọc lại KHÔNG tốn tiền lần 2)."""
    tdir, cdir = out_dir / "_raw" / "thumbs", out_dir / "_raw" / "thumb_text"
    cdir.mkdir(parents=True, exist_ok=True)
    for r in rows:
        c = cdir / f"{r['id']}.json"
        if c.exists():
            r["thumb_text"] = json.loads(c.read_text(encoding="utf-8"))
            continue
        anh = next((p for p in sorted(tdir.glob(f"*{r['id']}.jpg"))), None)
        if not anh:
            print(f"  ! {r['id']}: chưa tải được ảnh thumbnail — bỏ qua phần chữ")
            continue
        d = doc_chu_thumbnail(anh)
        if d:
            c.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            r["thumb_text"] = d
            print(f"  ✓ {r['id']}: {' / '.join(d.get('dong_chu') or []) or '(không có chữ)'}")
    return rows


def _thumb_block(r):
    d = r.get("thumb_text") or {}
    if not d:
        return "(CHƯA ĐỌC ĐƯỢC ẢNH — để trống mọi field về thumbnail, KHÔNG suy luận từ tiêu đề)"
    return " / ".join(d.get("dong_chu") or []) + f"   [bố cục: {d.get('bo_cuc', '')}]"


# ────────────── CỔNG CHỐNG CHẠY TRÙNG KÊNH MÁY 2 ĐÃ NGHIÊN CỨU (anh chốt 2026-09-24)
# Yêu cầu từ TRENDING-RESEARCH (máy 2):
# `FlowHandoff_local\shared\YEU_CAU_MAY1_2026-09-24_dung_chay_lai_k1k2.md` — máy 1 đã chạy lại K1+K2
# cho kênh 千種テンカ (Lane K) mà máy 2 đã nghiên cứu, tốn quota Gemini lần hai và có rủi ro hai bản
# CHANNEL_DNA.md lệch nhau (Gemini không tất định).
#
# Rào đặt trong TOOL chứ không trong tài liệu (memory `khong-giao-viec-thu-cong-rao-nam-trong-tool`):
# tài liệu thì phải có người nhớ mới tra, cổng thì không ai đi qua được mà không thấy.
#
# ⚠️ Cổng chỉ chặn khi bản của máy 2 THẬT SỰ DÙNG ĐƯỢC — tức có `CHANNEL_DNA.md` **và**
# `VIDEO_ANALYSIS/*.json` (K3 `retrieve_videos.py` bắt buộc cần cái sau). Đo thật 2026-09-24: gói
# `results\laneK_from_research\` chỉ có phiếu việc + report HTML + `data\`, KHÔNG có hai thứ này —
# nên chặn theo kiểu "hễ máy 2 có đụng vào kênh đó là cấm chạy" sẽ khoá máy 1 khỏi thứ nó buộc phải
# có. Thiếu → cổng chỉ CẢNH BÁO và chỉ đường xin bổ sung, vẫn cho chạy.
CHANNEL_ID_PAT = re.compile(r"UC[A-Za-z0-9_-]{20,}")


def _dinh_danh(channel_url):
    """Rút (channel_id, handle) từ URL để so khớp với bản máy 2 đã giao. Thiếu thì trả None."""
    u = (channel_url or "").strip()
    cid = CHANNEL_ID_PAT.search(u)
    m = re.search(r"@([A-Za-z0-9_.-]+)", u)
    return (cid.group(0) if cid else None), (m.group(1).lower() if m else None)


def ban_cua_may2(channel_url, goc=None):
    """Tìm bản nghiên cứu của máy 2 cho ĐÚNG kênh này.

    Trả list dict {thu_muc, co_dna, n_video_analysis, nguon}. Quét 2 kênh truyền:
      · `FlowHandoff_local\\results\\channel_dna\\<slug>\\` — kênh truyền CHUẨN (6 kênh đang dùng),
        channel_id nằm trong `run_log.txt`;
      · `FlowHandoff_local\\results\\*_from_research\\` — kênh truyền hồ sơ ngách, channel_id nằm
        trong `data\\channel.json` (`meta.channel_id`).
    """
    cid, handle = _dinh_danh(channel_url)
    if not (cid or handle):
        return []
    goc = Path(goc) if goc else Path(__file__).resolve().parents[1] / "FlowHandoff_local" / "results"
    ra = []

    def _khop(text):
        t = (text or "").lower()
        return (cid and cid.lower() in t) or (handle and f"@{handle}" in t)

    for d in sorted((goc / "channel_dna").glob("*")) if (goc / "channel_dna").is_dir() else []:
        if d.is_dir() and _khop(_doc_an_toan(d / "run_log.txt")):
            ra.append(_mo_ta_ban(d, "results/channel_dna"))
    for d in sorted(goc.glob("*_from_research")):
        if not d.is_dir():
            continue
        if _khop(_doc_an_toan(d / "data" / "channel.json")) or any(
                _khop(_doc_an_toan(f)) for f in d.glob("*.md")):
            ra.append(_mo_ta_ban(d, "results/*_from_research"))
    return ra


def _doc_an_toan(p):
    p = Path(p)
    try:
        return p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""
    except OSError:
        return ""


def _mo_ta_ban(d, nguon):
    va = d / "VIDEO_ANALYSIS"
    return {"thu_muc": d, "nguon": nguon, "co_dna": (d / "CHANNEL_DNA.md").is_file(),
            "n_video_analysis": len(list(va.glob("*.json"))) if va.is_dir() else 0}


def cong_chong_trung(channel_url, force=False, goc=None):
    """In cảnh báo / chặn. Trả True = ĐƯỢC chạy tiếp.

    `goc` để test trỏ vào thư mục giả — nhận tham số thay vì bắt test monkeypatch `ban_cua_may2`
    (bản đầu làm vậy và dính đệ quy vô hạn: hàm giả gọi lại chính hàm đã bị vá)."""
    ban = ban_cua_may2(channel_url, goc=goc)
    if not ban:
        return True
    dung_duoc = [b for b in ban if b["co_dna"] and b["n_video_analysis"] > 0]
    for b in ban:
        print(f"  · máy 2 đã nghiên cứu kênh này: {b['thu_muc']} "
              f"(CHANNEL_DNA.md: {'có' if b['co_dna'] else 'KHÔNG'} · "
              f"VIDEO_ANALYSIS: {b['n_video_analysis']} file) [{b['nguon']}]")
    if not dung_duoc:
        print("  ⚠ Bản máy 2 giao THIẾU `CHANNEL_DNA.md` và/hoặc `VIDEO_ANALYSIS/*.json` — K3 "
              "(retrieve_videos.py) không chạy được nếu không có. VẪN CHẠY K1+K2 ở đây, nhưng hãy "
              "nhắn máy 2 bổ sung qua `FlowHandoff_local\\shared\\YEU_CAU_MAY2_*.md` để lần sau "
              "khỏi tốn quota Gemini hai lần.")
        return True
    if force:
        print("  ⚠ --force: vẫn chạy lại dù máy 2 đã giao bản dùng được (tốn quota Gemini lần hai, "
              "và sẽ có HAI bản CHANNEL_DNA.md có thể lệch nhau).")
        return True
    print(f"\n✗ DỪNG — kênh này máy 2 (TRENDING-RESEARCH) đã nghiên cứu và giao bản DÙNG ĐƯỢC.\n"
          f"  Dùng thẳng bản đó, đừng chạy lại (yêu cầu 2026-09-24:\n"
          f"  FlowHandoff_local\\shared\\YEU_CAU_MAY1_2026-09-24_dung_chay_lai_k1k2.md).\n"
          f"  Copy sang chỗ lane đọc:\n"
          f"     robocopy \"{dung_duoc[0]['thu_muc']}\" \"docs\\channel_dna\\<slug>\" /E\n"
          f"  Thiếu gì thì nhắn máy 2 qua FlowHandoff_local\\shared\\YEU_CAU_MAY2_*.md.\n"
          f"  Thật sự cần chạy lại (vd bản cũ hỏng) thì thêm --force.")
    return False


# ---------------------------------------------------------------- K2: Gemini
VIDEO_PROMPT = """Bạn phân tích 1 video YouTube ngách "{niche_hint}". Dữ liệu:
TIÊU ĐỀ: {title}
LƯỢT XEM: {view_count}
MÔ TẢ (description gốc, rút gọn): {description}
CHỮ TRÊN THUMBNAIL (đã ĐỌC TỪ ẢNH THẬT, không phải suy luận): {thumb_text}
ĐOẠN ĐẦU 0–30 GIÂY (nguyên văn theo mốc giây): {dau_0_30s}
TRANSCRIPT (rút gọn nếu quá dài):
{transcript}

Trả về ĐÚNG 1 JSON (không kèm giải thích, không bọc ```markdown```), đúng khoá. QUAN TRỌNG: field
"topics" PHẢI viết bằng ĐÚNG ngôn ngữ gốc của TIÊU ĐỀ/TRANSCRIPT ở trên (không dịch sang tiếng Việt)
— vì sau này sẽ so khớp substring với câu hỏi cùng ngôn ngữ đó. Mỗi phần tử là 1 khái niệm NGẮN DUY
NHẤT (không ghép 2 khái niệm bằng dấu / hay dấu phẩy trong cùng 1 phần tử, vd viết "UFO" và "UAP"
thành 2 phần tử riêng thay vì "UFO/UAP"):
{{"topics": ["từ khoá ngắn 1 (ngôn ngữ gốc video)", "từ khoá ngắn 2 (ngôn ngữ gốc video)", "..."],
  "hook_type": "mô tả cách mở đầu, 1 câu",
  "hook_0_30s": "chép lại nguyên văn 30 giây đầu (ngôn ngữ gốc), không tóm tắt",
  "hook_4_nhip": {{"event": "sự kiện cụ thể ở 0–5s hoặc null", "contradiction": "mâu thuẫn ở 5–12s hoặc null",
                   "stake": "cảm xúc/mất mát 12–20s hoặc null", "open_loop": "câu hỏi để ngỏ 20–30s hoặc null"}},
  "hook_kind": "A biến cố bất thường | B câu nói sốc | C mâu thuẫn | D hậu quả chưa rõ nguyên nhân | E hé reveal | none",
  "hook_score_0_12": 0,
  "loi_hua_video": "MỘT câu: video này hứa cho người xem điều gì (viết bằng ngôn ngữ gốc của video)",
  "promise_match": {{"title": "PASS|FAIL", "description": "PASS|FAIL|NA", "thumbnail": "PASS|FAIL|NA",
                     "hook": "PASS|FAIL", "verdict": "PASS|FAIL",
                     "ly_do": "1 câu: bốn chỗ (tiêu đề · chữ thumbnail · câu đầu mô tả · 30–45s đầu) có nói CÙNG một lời hứa không; chỗ nào lệch thì lệch thế nào"}},
  "cap_khop": {{"hook_tieu_de": "Khớp|Một phần|Lệch", "thumbnail_tieu_de": "Khớp|Một phần|Lệch",
                "thumbnail_hook": "Khớp|Một phần|Lệch", "ly_do": "mỗi cặp 1 câu lý do, nối bằng ' · '"}},
  "structure": "mô tả cấu trúc/chương chính, 1-2 câu",
  "emotional_beats": ["cảm xúc chính 1", "..."],
  "title_formula": "công thức tiêu đề video này áp dụng, 1 câu",
  "notes": "chi tiết đáng chú ý khác, có thể để rỗng"}}"""

DNA_PROMPT = """Bạn là chuyên gia phân tích kênh YouTube ngách "{niche_hint}". Dưới đây là {n} video
top view của kênh (tiêu đề + lượt xem + CHỮ TRÊN THUMBNAIL đọc từ ảnh thật + câu đầu mô tả + toàn
văn lời thoại). Hãy tổng hợp thành 1 tài liệu Markdown CHANNEL_DNA.md đúng cấu trúc 12 đề mục sau (mỗi đề mục 1 heading ## + vài gạch đầu dòng, TRÍCH DẪN
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
## Thumbnail patterns — CHỈ dựa trên khối "CHỮ TRÊN THUMBNAIL (đọc từ ảnh thật)" của từng video:
   chép lại chữ từng dòng, rồi rút khuôn (mấy dòng, dòng nào màu gì/vai trò gì, có chữ số không, có
   tên người không, có chép lại chữ của tiêu đề không). CẤM suy luận từ tiêu đề/nội dung. Video nào
   không có khối đó thì ghi rõ "chưa đọc được ảnh" và KHÔNG đếm nó vào tỉ lệ.
## Promise — LỜI HỨA của video: mỗi video 1 câu lời hứa, rồi kết luận kênh này nối lời hứa qua bốn
   chỗ (tiêu đề · chữ thumbnail · câu đầu mô tả · 30–45 giây đầu hook) như thế nào. Kèm SỐ ĐẾM
   Khớp/Một phần/Lệch cho ba cặp hook↔tiêu đề, thumbnail↔tiêu đề, thumbnail↔hook (vd "Khớp 6/9"),
   và nêu video lệch nhiều nhất kèm lý do.
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
    # description/dau_0_30s chỉ có ở transcript crawl MỚI (task 2 trở đi) — cache cũ không có 2
    # khoá này (.get trả None/"") vẫn format được, không KeyError.
    prompt = VIDEO_PROMPT.format(niche_hint=niche_hint, title=row["title"],
                                 view_count=row["view_count"],
                                 description=(row.get("description") or "")[:1500],
                                 thumb_text=_thumb_block(row),
                                 dau_0_30s=row.get("dau_0_30s") or row["transcript"][:300],
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
    ap.add_argument("--no-thumb-text", action="store_true",
                    help="tắt bước ĐỌC CHỮ TRÊN ẢNH thumbnail bằng vision (G7). Bật mặc định vì "
                         "bàn giao 2026-09-23 cấm 'suy luận' chữ thumbnail. TỐN TIỀN: 1 lượt gọi "
                         "sol_client/ảnh, có cache `_raw/thumb_text/` nên chạy lại không tính lại")
    ap.add_argument("--no-tags", action="store_true",
                    help="tắt bước gom Video Tags/Channel Tags → TAG_STATS.json (bật mặc định, "
                         "phụ trợ, không ảnh hưởng K1/K2 nếu lỗi)")
    ap.add_argument("--force", action="store_true",
                    help="chạy lại K1+K2 dù máy 2 (TRENDING-RESEARCH) đã giao bản dùng được — TỐN "
                         "QUOTA GEMINI LẦN HAI và sinh bản CHANNEL_DNA.md thứ hai có thể lệch bản cũ")
    args = ap.parse_args()

    # Cổng chống chạy trùng — đặt TRƯỚC mọi thứ (kể cả mkdir out_dir) để trượt là chưa tốn gì.
    if not cong_chong_trung(args.channel_url, force=args.force):
        return 1

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

    if not args.no_thumb_text:
        print(f"[K1b] Đọc CHỮ TRÊN ẢNH thumbnail ({len(rows)} video, vision — có cache) ...")
        rows = gan_chu_thumbnail(rows, out_dir)
        n = sum(1 for r in rows if r.get("thumb_text"))
        print(f"  → đọc được {n}/{len(rows)} ảnh"
              + ("" if n == len(rows) else " — video thiếu sẽ để TRỐNG phần thumbnail, không suy luận"))

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
    # `sys.exit(main())` chứ không phải `main()` trần: cổng chống chạy trùng trả 1 khi chặn, gọi trần
    # thì mã thoát vẫn là 0 — người/script gọi qua `&&` sẽ tưởng đã chạy xong và đi tiếp.
    sys.exit(main() or 0)
