# Gemini Channel Analyzer + Retrieval Implementation Plan

> **For agentic workers:** thực thi Inline trong phiên hiện tại (không dispatch subagent-per-task) —
> dự án này KHÔNG có git repo (không commit được) và KHÔNG dùng pytest (quy ước kiểm thử của dự án là
> chạy thật với dữ liệu thật + đo thời gian, xem `docs/superpowers/specs/2026-09-16-gemini-channel-
> analyzer-design.md` + memory `bao-cao-test-phai-kem-thoi-gian`). Mỗi task thay bước "viết test thất
> bại/pytest" bằng "chạy script thật + kiểm output bằng mắt/số đo", thay bước "commit" bằng bỏ qua.

**Goal:** Xây 2 tool độc lập (`channel_analyzer.py`, `retrieve_videos.py`) tách phần đọc N video đối
thủ + tổng hợp DNA kênh + chọn video liên quan ra khỏi Claude, cộng 1 gói bàn giao tự chứa để user gửi
"máy 2" chạy không cần Claude.

**Architecture:** Xem `docs/superpowers/specs/2026-09-16-gemini-channel-analyzer-design.md` — tool
B1+B2 crawl + gọi Gemini 3.8 Flash qua `llm_client.py` (route mới `CHAINS["analysis"]`, tách khỏi
`CHAINS["script"]`) → ghi `CHANNEL_DNA.md` + `VIDEO_ANALYSIS/*.json`; tool B3 retrieval thuần Python
(substring match, không LLM) chọn N video liên quan chủ đề mới.

**Tech Stack:** Python 3.13, `yt-dlp`, `youtube-transcript-api`, `urllib` (đã có trong
`llm_client.py`, không thêm dependency HTTP mới).

## Global Constraints
- Không sửa skill global (`~/.claude/skills/youtube-series-builder`/`youtube-script`/`youtube-produce`).
- Không thêm model mới vào `llm_client.py` — chỉ tái dùng `gemini-3.8-flash`/`gpt-5.6-luna` đã verify.
- Kênh pilot: 今夜も都市伝説 (có trong `docs/laneA_from_research/data/titles.json`), tool tự crawl mới.
- Mọi báo cáo test phải kèm số đo thời gian thật (không mô tả cảm giác).

---

### Task 1: Thêm route `CHAINS["analysis"]` vào `llm_client.py`

**Files:**
- Modify: `e:\CLAUDE\YOUTUBE\h2dev\pipeline\llm_client.py:47-56` (dict `CHAINS`)

**Interfaces:**
- Produces: `CHAINS["analysis"]` — list `[(provider, model), ...]`, dùng bởi Task 2 qua
  `chat(prompt, task="analysis", ...)` đã có sẵn trong `llm_client.chat()`.

- [ ] **Bước 1: Sửa dict `CHAINS`, thêm entry mới**
```python
CHAINS = {
    # viết/nén kịch bản dài: gemini-3.8-flash ramclouds (văn hay nhất, Nhật hoá 8/9)
    "script": [("ramclouds", "gemini-3.8-flash"),
               ("ramclouds", "gpt-5.6-luna"),
               ("ns24", "gemini-3.8-flash")],
    # việc ngắn/máy móc (prompt ảnh, chữ thumbnail, tóm tắt): cùng model, rẻ và nhanh
    "short": [("ramclouds", "gemini-3.8-flash"),
              ("ns24", "gemini-3.8-flash"),
              ("ramclouds", "gpt-5.6-luna")],
    # tổng hợp DNA kênh (nhiều transcript gộp 1 lượt) — TÁCH RIÊNG khỏi "script" dù cùng model,
    # để đổi tham số viết-sáng-tạo sau này không vô tình ảnh hưởng bước phân tích kênh.
    "analysis": [("ramclouds", "gemini-3.8-flash"),
                 ("ramclouds", "gpt-5.6-luna"),
                 ("ns24", "gemini-3.8-flash")],
}
```
- [ ] **Bước 2: Kiểm chain mới còn sống** — chạy:
```
py -3.13 pipeline\llm_client.py --ask "Reply with exactly: ok" --task analysis
```
Kỳ vọng: in ra `--- ramclouds:gemini-3.8-flash · ... chữ · ...s` kèm nội dung `ok` (giống hệt cách
`--ping` đã verify cho "script"/"short" — không cần code thêm, `main()` đã hỗ trợ `--task` tuỳ ý qua
`choices=list(CHAINS)`).

---

### Task 2: Viết `pipeline/channel_analyzer.py`

**Files:**
- Create: `e:\CLAUDE\YOUTUBE\h2dev\pipeline\channel_analyzer.py`
- Dùng lại (import trực tiếp, không subprocess): `fetch_script.fetch_any`, `fetch_script.video_id`,
  `llm_client.chat`, `llm_client.LLMError`

**Interfaces:**
- Consumes: `fetch_script.fetch_any(vid, langs, method="auto") -> (segs, used)` (đã có,
  `e:\CLAUDE\YOUTUBE\h2dev\pipeline\fetch_script.py:204`); `llm_client.chat(prompt, system=None,
  task="short", min_chars=0, require_sentence_end=False, max_tokens=32000) -> ChatResult` (đã có,
  `pipeline/llm_client.py:182`, trường `.text`/`.model`/`.elapsed`).
- Produces: file `<out_dir>/CHANNEL_DNA.md`, thư mục `<out_dir>/VIDEO_ANALYSIS/<id>.json`, thư mục
  `<out_dir>/_raw/transcripts.json` — Task 4 (`retrieve_videos.py`) đọc `VIDEO_ANALYSIS/*.json`.

- [ ] **Bước 1: Viết hàm crawl catalog**
```python
def crawl_catalog(channel_url, n_videos):
    """Trả list [{"id","title","view_count","duration"}] top-N theo view_count giảm dần."""
    import yt_dlp
    opts = {"quiet": True, "no_warnings": True, "extract_flat": True, "noprogress": True,
            "playlistend": 200}
    url = channel_url.rstrip("/") + "/videos"
    with yt_dlp.YoutubeDL(opts) as y:
        info = y.extract_info(url, download=False)
    rows = []
    for e in (info or {}).get("entries") or []:
        if not e:
            continue
        rows.append({"id": e.get("id"), "title": e.get("title") or "",
                     "view_count": e.get("view_count") or 0,
                     "duration": e.get("duration") or 0})
    rows.sort(key=lambda r: r["view_count"], reverse=True)
    return rows[:n_videos]
```

- [ ] **Bước 2: Viết hàm crawl transcript từng video (bỏ qua lỗi, không chết cả batch)**
```python
def crawl_transcripts(rows, langs, out_dir):
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
            segs, used = fetch_script.fetch_any(r["id"], langs)
            text = re.sub(r"\s+", " ", " ".join(s["text"] for s in segs)).strip()
            out.append({**r, "transcript": text})
            print(f"  ✓ {r['id']} [{used}]: {len(text):,} ký tự — {r['title'][:50]}")
        except SystemExit as e:
            print(f"  ✗ {r['id']} bỏ qua: {e}")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
```
(`import re, json` ở đầu file cùng `import argparse, sys, time` từ pathlib `Path`.)

- [ ] **Bước 3: Viết prompt + gọi Gemini cho TỪNG video (task="short")**
```python
VIDEO_PROMPT = """Bạn phân tích 1 video YouTube ngách "{niche_hint}". Dữ liệu:
TIÊU ĐỀ: {title}
LƯỢT XEM: {view_count}
TRANSCRIPT (rút gọn nếu quá dài):
{transcript}

Trả về ĐÚNG 1 JSON (không kèm giải thích, không bọc ```markdown```), đúng khoá:
{{"topics": ["từ khoá ngắn 1", "từ khoá ngắn 2", "..."],
  "hook_type": "mô tả cách mở đầu, 1 câu",
  "structure": "mô tả cấu trúc/chương chính, 1-2 câu",
  "emotional_beats": ["cảm xúc chính 1", "..."],
  "title_formula": "công thức tiêu đề video này áp dụng, 1 câu",
  "notes": "chi tiết đáng chú ý khác, có thể để rỗng"}}"""


def _strip_fence(text):
    """Bỏ bọc ```json ... ``` nếu model trả kèm (bẫy đã biết trong dự án)."""
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
        t = re.sub(r"\n?```$", "", t)
    return t.strip()


def analyze_one_video(row, niche_hint):
    prompt = VIDEO_PROMPT.format(niche_hint=niche_hint, title=row["title"],
                                 view_count=row["view_count"],
                                 transcript=row["transcript"][:20000])
    r = llm_client.chat(prompt, task="short", max_tokens=2000, temperature=0.3)
    data = json.loads(_strip_fence(r.text))
    data["video_id"] = row["id"]
    data["title"] = row["title"]
    data["view_count"] = row["view_count"]
    data["duration_min"] = round(row["duration"] / 60.0, 1) if row["duration"] else 0.0
    return data
```

- [ ] **Bước 4: Viết prompt + gọi Gemini tổng hợp DNA (task="analysis")**
```python
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
## Rules for writing new videet — 5-8 quy tắc cụ thể để viết video MỚI giống đúng công thức kênh này

DỮ LIỆU {n} VIDEO:
{videos_block}"""


def synthesize_dna(rows, niche_hint):
    block = "\n\n".join(
        f"--- Video {i+1} ---\nTiêu đề: {r['title']}\nLượt xem: {r['view_count']}\n"
        f"Lời thoại: {r['transcript'][:15000]}"
        for i, r in enumerate(rows))
    prompt = DNA_PROMPT.format(niche_hint=niche_hint, n=len(rows), videos_block=block)
    r = llm_client.chat(prompt, task="analysis", max_tokens=16000, temperature=0.4,
                        min_chars=800, require_sentence_end=False)
    return r.text
```

- [ ] **Bước 5: Viết cổng QC + hàm `main()` ghi file, in cảnh báo rõ ràng khi trượt ngưỡng**
```python
def qc_dna(text):
    n_chars = len(text.replace("\n", "").replace(" ", ""))
    n_heads = len(re.findall(r"^##\s", text, re.MULTILINE))
    ok = n_chars >= 800 and n_heads >= 8
    print(f"  {'✓' if ok else '✗'} QC DNA: {n_chars} ký tự, {n_heads}/11 đề mục "
          f"{'ĐẠT' if ok else 'TRƯỢT — kiểm lại prompt/model'}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel-url", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--n-videos", type=int, default=8)
    ap.add_argument("--langs", default="ja,en")
    ap.add_argument("--niche-hint", default="")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    langs = args.langs.split(",")
    niche_hint = args.niche_hint or args.channel_url

    t0 = time.time()
    print(f"[B1] Crawl catalog {args.channel_url} ...")
    rows = crawl_catalog(args.channel_url, args.n_videos)
    print(f"  → {len(rows)} video, {time.time()-t0:.0f}s")

    t1 = time.time()
    print(f"[B1] Crawl transcript {len(rows)} video ...")
    rows = crawl_transcripts(rows, langs, out_dir)
    print(f"  → {len(rows)}/{args.n_videos} video có transcript, {time.time()-t1:.0f}s")
    if not rows:
        raise SystemExit("Không crawl được transcript video nào — dừng.")

    t2 = time.time()
    print(f"[B2] Gọi Gemini phân tích từng video (task=short) ...")
    (out_dir / "VIDEO_ANALYSIS").mkdir(exist_ok=True)
    n_ok = 0
    for r in rows:
        try:
            data = analyze_one_video(r, niche_hint)
            (out_dir / "VIDEO_ANALYSIS" / f"{r['id']}.json").write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            n_ok += 1
        except Exception as e:
            print(f"  ✗ {r['id']} phân tích lỗi: {type(e).__name__} {str(e)[:120]}")
    pct = n_ok / len(rows) * 100
    print(f"  → {n_ok}/{len(rows)} video ({pct:.0f}%) phân tích được, {time.time()-t2:.0f}s")
    if pct < 70:
        print(f"  ⚠ CẢNH BÁO: dưới 70% video phân tích được, kiểm lại lỗi ở trên")

    t3 = time.time()
    print(f"[B2] Gọi Gemini tổng hợp CHANNEL_DNA.md (task=analysis) ...")
    dna_text = synthesize_dna(rows, niche_hint)
    (out_dir / "CHANNEL_DNA.md").write_text(dna_text, encoding="utf-8")
    print(f"  → xong, {time.time()-t3:.0f}s")
    qc_dna(dna_text)

    print(f"\n✓ TỔNG: {time.time()-t0:.0f}s → {out_dir}")


if __name__ == "__main__":
    main()
```
(Đầu file cần `import argparse, json, re, sys, time; from pathlib import Path; import llm_client`,
`sys.stdout.reconfigure(encoding="utf-8")` giống các file khác trong `pipeline/`.)

- [ ] **Bước 6: Chạy thật với kênh pilot, đo thời gian**
```
py -3.13 pipeline\channel_analyzer.py --channel-url https://www.youtube.com/@<handle 今夜も都市伝説> \
    --out-dir docs/channel_dna/imayamo-toshidensetsu --n-videos 8 --niche-hint "都市伝説・ミステリー"
```
Kỳ vọng: log từng bước B1/B2 kèm số đo thời gian, `CHANNEL_DNA.md` QC "ĐẠT", ≥ 6/8 video có file
JSON. Nếu channel URL/handle thật của "今夜も都市伝説" chưa biết chính xác — tra bằng
`docs/laneA_from_research/data/titles.json` (đã có `ch` field) hoặc tìm trên YouTube trước khi chạy.

- [ ] **Bước 7: Đối chiếu `CHANNEL_DNA.md` với `LANE_A_NICHE_KIT.md`**
Đọc cả 2 file, liệt kê: DNA tự động có nhắc tới các pattern đã biết là thật không (khối tag
`【都市伝説 ミステリー 怖い話】`, công thức tiêu đề kết bằng `？` ~62%, nhịp `しかし/だが` giữ chân...).
Ghi kết quả đối chiếu (đạt bao nhiêu/bao nhiêu điểm) vào báo cáo cuối cùng cho user.

---

### Task 3: Viết `pipeline/retrieve_videos.py`

**Files:**
- Create: `e:\CLAUDE\YOUTUBE\h2dev\pipeline\retrieve_videos.py`

**Interfaces:**
- Consumes: thư mục `<dna_dir>/VIDEO_ANALYSIS/*.json` (schema từ Task 2 Bước 3).
- Produces: in ra terminal + ghi `<dna_dir>/_retrieved/<timestamp>.json` — Claude đọc file này khi
  viết kịch bản (không phải interface hàm Python, vì bước sau do Claude đọc trực tiếp).

- [ ] **Bước 1: Viết toàn bộ file**
```python
"""retrieve_videos.py — chọn N video liên quan nhất 1 chủ đề mới, từ VIDEO_ANALYSIS/*.json đã có.

So khớp SUBSTRING (không tokenize/embedding): topics[] của mỗi video là cụm từ khoá ngắn do Gemini
sinh sẵn (channel_analyzer.py), so trực tiếp với chuỗi --topic là đủ dùng ở quy mô <50 video/kênh —
tiếng Nhật không có khoảng trắng giữa từ nên tokenize đúng cần mecab/fugashi, dự án này không có
dependency đó ở đâu khác nên cố tình không thêm.

Dùng:
  py -3.13 retrieve_videos.py --dna-dir docs/channel_dna/<slug>/ --topic "UFO và chính phủ che giấu" --top-n 8
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def load_videos(dna_dir):
    va_dir = dna_dir / "VIDEO_ANALYSIS"
    if not va_dir.exists():
        raise SystemExit(f"Chưa có {va_dir} — chạy channel_analyzer.py cho kênh này trước.")
    out = []
    for f in sorted(va_dir.glob("*.json")):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"  ✗ bỏ qua {f.name}: {type(e).__name__} {e}")
    if not out:
        raise SystemExit(f"{va_dir} rỗng hoặc mọi file lỗi — chạy lại channel_analyzer.py.")
    return out


def score(video, topic):
    topics = video.get("topics") or []
    title = video.get("title") or ""
    s = 0
    for t in topics:
        t = t.strip()
        if not t:
            continue
        if t in topic:
            s += 1
        if t in title:
            s += 1
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dna-dir", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--top-n", type=int, default=8)
    args = ap.parse_args()

    dna_dir = Path(args.dna_dir)
    videos = load_videos(dna_dir)
    ranked = sorted(videos, key=lambda v: score(v, args.topic), reverse=True)
    top_scores = [score(v, args.topic) for v in ranked[:args.top_n]]

    if max(top_scores or [0]) == 0:
        print("⚠ Không video nào khớp từ khoá chủ đề — trả về top view_count làm dự phòng.")
        ranked = sorted(videos, key=lambda v: v.get("view_count", 0), reverse=True)

    picked = ranked[:args.top_n]
    out_dir = dna_dir / "_retrieved"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{int(time.time())}.json"
    result = [{"video_id": v["video_id"], "title": v.get("title", ""),
              "score": score(v, args.topic), "topics": v.get("topics", [])} for v in picked]
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Top {len(picked)}/{len(videos)} video liên quan chủ đề: {args.topic!r}")
    for r in result:
        print(f"  [{r['score']:2d}] {r['video_id']}  {r['title'][:70]}")
    print(f"\n→ Đã ghi {out_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Bước 2: Chạy thật với chủ đề giả định, kiểm kết quả hợp lý**
```
py -3.13 pipeline\retrieve_videos.py --dna-dir docs/channel_dna/imayamo-toshidensetsu \
    --topic "UFO và chính phủ Mỹ che giấu bằng chứng" --top-n 5
```
Kỳ vọng: các video có `topics` chứa UFO/NASA/CIA/政府 xếp hạng cao hơn video về khoảng cách vũ trụ
thuần thiên văn.

---

### Task 4: Đóng gói bàn giao cho "máy 2" (chạy hoàn toàn không cần Claude)

**Files:**
- Create thư mục: `e:\CLAUDE\YOUTUBE\h2dev\handoff_may2_channel_analyzer\`
  - `HUONG_DAN.md` — hướng dẫn tự chứa, copy-paste được, không giả định người chạy biết dự án này
  - `channel_analyzer.py`, `retrieve_videos.py`, `fetch_script.py`, `llm_client.py`, `keys.py`,
    `paths.py` (copy nguyên bản từ `pipeline/`, KHÔNG sửa nội dung — máy 2 không có phần còn lại của
    `pipeline/` nên phải copy đủ mọi module mà 2 tool import tới)
  - `requirements.txt`

- [ ] **Bước 1: Kiểm `keys.py` và `paths.py` có import gì khác ngoài `pipeline/` không**
```
py -3.13 -c "import ast,sys; [print(n.names[0].name if hasattr(n,'names') else n.module) for n in ast.walk(ast.parse(open('pipeline/keys.py',encoding='utf-8').read())) if isinstance(n,(ast.Import,ast.ImportFrom))]"
```
Lặp lại cho `paths.py`. Nếu có import module khác trong `pipeline/` (vd `paths.py` import gì đó nội
bộ), copy luôn module đó vào `handoff_may2_channel_analyzer/`.

- [ ] **Bước 2: Copy 6 file Python bằng lệnh copy (không dùng Edit — giữ nguyên bit-for-bit)**
```
mkdir -p handoff_may2_channel_analyzer
cp pipeline/channel_analyzer.py pipeline/retrieve_videos.py pipeline/fetch_script.py \
   pipeline/llm_client.py pipeline/keys.py pipeline/paths.py handoff_may2_channel_analyzer/
```

- [ ] **Bước 3: Viết `requirements.txt`**
```
yt-dlp
youtube-transcript-api
```
(Không thêm `faster-whisper`/`imageio-ffmpeg` vào bắt buộc — đó là nhánh dự phòng cuối của
`fetch_script.py` khi 2 đường trên chết, ghi rõ trong `HUONG_DAN.md` là "cài thêm NẾU cần" thay vì
bắt buộc, tránh máy 2 phải tải mô hình whisper ~140MB không cần thiết.)

- [ ] **Bước 4: Viết `HUONG_DAN.md`** — nội dung đầy đủ, máy 2 đọc là chạy được, không cần hỏi lại:
```markdown
# Hướng dẫn chạy Channel Analyzer (không cần Claude)

## Cài đặt (1 lần)
```
pip install -r requirements.txt
```
Cần Python 3.10+ (đã test bằng `py -3.13`). Không cần GPU, không cần tài khoản Google.

## B1+B2 — Phân tích 1 kênh YouTube đối thủ
```
python channel_analyzer.py --channel-url "<URL kênh, ví dụ https://www.youtube.com/@tenkenh>" \
    --out-dir "ket_qua/<ten-kenh-viet-khong-dau>" \
    --n-videos 8 \
    --niche-hint "<mô tả ngắn ngách, ví dụ: 都市伝説・ミステリー hoặc horror mystery Japanese>"
```
Chạy mất khoảng 3-8 phút tuỳ số video và tốc độ mạng (log in ra từng bước kèm thời gian). Xong sẽ có:
```
ket_qua/<ten-kenh>/
  CHANNEL_DNA.md              ← quan trọng nhất
  VIDEO_ANALYSIS/<id>.json    ← 1 file/video
  _raw/transcripts.json       ← dữ liệu thô (giữ để chạy lại không phải crawl lại)
```
**Nếu log in "⚠ CẢNH BÁO: dưới 70% video phân tích được"** hoặc "QC DNA: ... TRƯỢT" — vẫn cứ gửi lại
toàn bộ thư mục `ket_qua/<ten-kenh>/`, ghi rõ trong tin nhắn gửi lại là "có cảnh báo X" — ĐỪNG tự sửa
prompt hay thử lại nhiều lần, để Claude quyết định.

## B3 — (Tuỳ chọn, có thể để Claude tự chạy) Chọn video liên quan 1 chủ đề mới
Chỉ chạy bước này nếu đã biết trước chủ đề video sắp viết. Nếu chưa biết, BỎ QUA bước này — Claude
sẽ tự chạy khi cần (không cần internet/API key, chạy máy nào cũng được).
```
python retrieve_videos.py --dna-dir "ket_qua/<ten-kenh>" --topic "<mô tả chủ đề video mới>" --top-n 8
```

## Cần API key gì?
File `llm_client.py` đã có sẵn key mặc định trong code (biến `PROVIDERS`) — CHẠY ĐƯỢC NGAY, không
cần set gì thêm. Nếu báo lỗi 401/403, báo lại cho Claude, đừng tự đổi key.

## GỬI LẠI CHO CLAUDE CÁI GÌ khi xong
Gửi lại NGUYÊN THƯ MỤC `ket_qua/<ten-kenh>/` (nén zip cũng được) — Claude cần cả 2 phần:
1. `CHANNEL_DNA.md` — để viết kịch bản đúng công thức kênh
2. Toàn bộ `VIDEO_ANALYSIS/*.json` — để tự chọn video liên quan cho từng tập cụ thể (Claude tự chạy
   `retrieve_videos.py`, không cần máy 2 chạy trước)
KHÔNG cần gửi lại `_raw/transcripts.json` (nặng, Claude không cần đọc lại transcript thô) — trừ khi
Claude yêu cầu debug lỗi cụ thể.
```

- [ ] **Bước 5: Zip thử để verify thư mục tự chứa (không thiếu file)**
```
py -3.13 -c "
import zipfile, pathlib
src = pathlib.Path('handoff_may2_channel_analyzer')
with zipfile.ZipFile('handoff_may2_channel_analyzer.zip', 'w') as z:
    for f in src.rglob('*'):
        if f.is_file():
            z.write(f, f.relative_to(src.parent))
print('OK', pathlib.Path('handoff_may2_channel_analyzer.zip').stat().st_size, 'bytes')
"
```

---

### Task 5: Cập nhật `docs/SOP_TOSHI_DENSETSU_JP.md`

**Files:**
- Modify: `e:\CLAUDE\YOUTUBE\h2dev\docs\SOP_TOSHI_DENSETSU_JP.md`

- [ ] **Bước 1: Thêm 1 mục mới TRƯỚC bước nghiên cứu kênh hiện tại**, trỏ sang 2 tool mới + gói
  bàn giao máy 2, dẫn đúng đường dẫn file đã tạo ở Task 2-4. Nội dung cụ thể viết khi đọc xong toàn
  văn SOP hiện tại (đọc trước khi sửa, giữ đúng văn phong/cấu trúc heading đang dùng trong file).

---

### Task 6: Báo cáo cuối cùng cho user

- [ ] Tổng hợp: thời gian chạy từng bước (Task 2 Bước 6, Task 3 Bước 2), kết quả đối chiếu
  `LANE_A_NICHE_KIT.md` (Task 2 Bước 7), đường dẫn gói zip bàn giao máy 2 (Task 4 Bước 5), và bất kỳ
  cảnh báo/lỗi nào gặp phải trong lúc chạy thật (không giấu, kể cả khi đã tự sửa được).
