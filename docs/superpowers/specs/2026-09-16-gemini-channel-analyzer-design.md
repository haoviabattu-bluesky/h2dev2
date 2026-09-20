# Thiết kế: Gemini Channel Analyzer + Retrieval (Hybrid) — 2026-09-16

## Bối cảnh

Hiện trạng (đã audit toàn repo 2026-09-16, xem memory `gemini-analyzer-vs-hien-trang`): Claude tự đọc
transcript thô của 5-8 video đại diện (`youtube-series-builder` P1) để phân tích kênh đối thủ, không
sinh ra artifact tái dùng nào. Khi viết kịch bản mới, `youtube-script`/`youtube-produce` cũng đưa
thẳng transcript thô ("khung kể") vào prompt Claude. Gemini 3.8 Flash đã có hạ tầng production
(`pipeline/llm_client.py` qua proxy ramclouds/ns24) nhưng đang đóng vai "script writer rẻ"
(`CHAINS["script"]`) và "QC vision grader", KHÔNG đóng vai phân tích kênh.

## Mục tiêu

Tách phần "đọc N video đối thủ + tổng hợp DNA kênh + chọn video liên quan" ra khỏi Claude, giao cho
2 tool chạy độc lập (Python + Gemini, không cần Claude). Claude chỉ được gọi vào ở bước cuối cùng —
đọc kết quả đã tổng hợp sẵn (súc tích, có cấu trúc) rồi viết kịch bản. Mục đích: giảm token Claude
phải nuốt, có artifact tái dùng nhiều lần cho cùng 1 kênh, không phải phân tích lại từ đầu mỗi lượt.

**Phạm vi đã chốt với user:**
- Code chỉ nằm trong `pipeline/` của dự án h2dev — **không sửa skill global**
  (`youtube-series-builder`/`youtube-script`/`youtube-produce` ở `~/.claude/skills/`) vì các skill
  đó dùng chung cho mọi dự án YouTube khác của user.
- Kênh pilot để build + test: **toshi-densetsu-jp (Lane A)** — có sẵn
  `docs/laneA_from_research/LANE_A_NICHE_KIT.md` (viết tay/Claude, đã verify hữu ích) để đối chiếu.
- Nguồn dữ liệu: tool **tự crawl mới** (yt-dlp + youtube-transcript-api), không phụ thuộc dữ liệu
  research đã có sẵn của kênh nào — chạy được cho bất kỳ kênh nào ngay lập tức.

## Kiến trúc / luồng dữ liệu

```
[1] pipeline/channel_analyzer.py  (Python + Gemini, KHÔNG Claude)
    ├─ crawl catalog (yt-dlp --flat-playlist) → chọn top-N video theo view_count
    ├─ fetch_script.py (đã có, tái dùng nguyên hàm fetch_any()) → transcript từng video
    ├─ gọi Gemini 3.8 Flash lần 1 (task="short", ĐÃ CÓ SẴN chain, không đổi)
    │     mỗi video → VIDEO_ANALYSIS/<id>.json
    ├─ gọi Gemini 3.8 Flash lần 2 (task="analysis", CHAIN MỚI trong llm_client.py)
    │     toàn bộ N video → CHANNEL_DNA.md
    └─ ghi ra đĩa: docs/channel_dna/<kenh-slug>/

[2] pipeline/retrieve_videos.py (Python thuần, KHÔNG LLM, KHÔNG Claude)
    input: --dna-dir docs/channel_dna/<slug>/ --topic "<chủ đề video mới>" --top-n 8
    → so khớp substring giữa topic mới và field "topics"/"title" của từng VIDEO_ANALYSIS/*.json
    → in ra danh sách N video liên quan nhất (id + đường dẫn json)

[3] Claude Sonnet 5 (GIỮ VAI viết kịch bản — chỉ đổi INPUT)
    đọc: CHANNEL_DNA.md (súc tích) + N video_analysis.json (đã retrieval) 
        + (tuỳ chọn, giữ như hiện tại) 1 transcript ĐẦY của video "khung kể" gần chủ đề nhất
    → viết script.txt theo skill youtube-script (công thức 70/30) — KHÔNG ĐỔI
```

**Không đổi (ngoài phạm vi):** `CHAINS["script"]` (viết/nén script trong `brain_channel.py`),
`qc_character.py`/`qc_visual.py`/`qc_canh.py` (QC vision), DeepSeek relay bước 3. Các thành phần này
tiếp tục hoạt động y hệt hiện tại.

## Thành phần 1 — `pipeline/channel_analyzer.py`

**CLI:**
```
py -3.13 pipeline\channel_analyzer.py --channel-url <URL> --out-dir docs/channel_dna/<slug>/ \
    [--n-videos 8] [--langs ja,en] [--force-recrawl]
```

**Bước xử lý:**
1. `yt-dlp --flat-playlist --print "%(view_count)s|%(duration)s|%(id)s|%(title)s" <URL>/videos`
   (đúng lệnh đã có trong skill `youtube-series-builder` P1) → sort theo view_count giảm dần →
   lấy top `--n-videos` (mặc định 8).
2. Với từng video: gọi `fetch_script.fetch_any(vid, langs)` (import trực tiếp hàm, không subprocess)
   → transcript text. Video nào lỗi (chặn 429, không phụ đề...) → **bỏ qua, ghi log cảnh báo, KHÔNG
   dừng cả batch** (đúng tinh thần "1 lỗi không giết cả lượt chạy" của `fetch_script.py` gốc).
3. Ghi thô ra `_raw/transcripts.json` (list `{video_id, title, view_count, duration, transcript}`) —
   để audit và **khỏi crawl lại** khi chạy `--force-recrawl` không được bật (mặc định: nếu
   `_raw/transcripts.json` đã tồn tại và đủ N video, dùng lại, không crawl lại).
4. **Gọi Gemini lần 1 — mỗi video một cuộc gọi nhỏ** (`task="short"`, KHÔNG đổi chain có sẵn):
   prompt yêu cầu trả về đúng 1 JSON (schema xem dưới) tóm tắt 1 video. Parse bằng `_strip_fence()`
   (bỏ bọc ```` ```json ```` nếu có — bẫy đã biết trong hệ sinh thái dự án, xem
   `gpt_api_codex.md`/`cong-qc-tu-khai-khong-do`) rồi `json.loads`. JSON không parse được → bỏ qua
   video đó, ghi log, KHÔNG dừng batch.
5. **Gọi Gemini lần 2 — một cuộc gọi tổng hợp DNA** (`task="analysis"`, CHAIN MỚI — xem Thành phần
   3): prompt đưa TOÀN BỘ N transcript + title + view_count (Gemini context 1M đủ chứa) + hướng dẫn
   đúng 12 đề mục (Audience, Content pillars, Narrative style, Hook formulas, Story structure,
   Pacing, Emotional triggers, CTA patterns, Title patterns, Thumbnail patterns, Rules for writing
   new videos — bỏ "Visual style"/"Image footage style" trùng lặp với Thumbnail patterns, gộp lại
   cho gọn theo đúng field đã chứng minh hữu ích trong `LANE_A_NICHE_KIT.md`).
6. Ghi `CHANNEL_DNA.md` + `VIDEO_ANALYSIS/<id>.json` (mỗi video 1 file) vào `--out-dir`.
7. **Cổng QC cuối** (in ra terminal, KHÔNG tự nhận "xong" nếu trượt):
   - `CHANNEL_DNA.md` tồn tại, ≥ 800 ký tự (không tính khoảng trắng), có ≥ 8 dòng bắt đầu bằng `##`
     (đủ 8/11 đề mục — thiếu hẳn 1 đề mục coi là bình thường nếu dữ liệu nguồn không đủ, nhưng thiếu
     quá nửa là dấu hiệu Gemini bị chặn/lỗi).
   - Số `VIDEO_ANALYSIS/*.json` ghi được ≥ 70% số video đã crawl thành công ở bước 2 — dưới ngưỡng
     này in cảnh báo rõ ràng kèm số liệu (không chỉ "OK", phải nói "5/8 video phân tích được").

**Schema `VIDEO_ANALYSIS/<id>.json`:**
```json
{
  "video_id": "saIym-x8dPc",
  "title": "...",
  "view_count": 101060,
  "duration_min": 75.8,
  "topics": ["月の秘密", "アポロ計画", "NASA隠蔽"],
  "hook_type": "mô tả ngắn cách mở đầu (1 câu)",
  "structure": "mô tả cấu trúc/chương chính (1-2 câu)",
  "emotional_beats": ["..."],
  "title_formula": "công thức tiêu đề áp dụng cho video này (vd 'kết thúc bằng ？')",
  "notes": "chi tiết đáng chú ý khác, có thể để rỗng"
}
```
Field `topics` là field DÙNG CHO RETRIEVAL (Thành phần 2) — bắt buộc phải có, các field khác có thể
rỗng nếu Gemini không trích được.

## Thành phần 2 — `pipeline/retrieve_videos.py`

**CLI:**
```
py -3.13 pipeline\retrieve_videos.py --dna-dir docs/channel_dna/<slug>/ --topic "<mô tả chủ đề mới>" --top-n 8
```

**Thuật toán (cố tình đơn giản, không dùng embedding/mecab):**
- Đọc toàn bộ `VIDEO_ANALYSIS/*.json` trong `--dna-dir`.
- Với mỗi video: `score = số phần tử trong topics[] xuất hiện dưới dạng SUBSTRING trong chuỗi
  --topic` + `số phần tử topics[] xuất hiện trong title` (cộng dồn, không trọng số phức tạp).
- **Lý do dùng substring thay vì tokenize từ**: tiếng Nhật không có khoảng trắng giữa từ, tokenize
  đúng cần thư viện ngoài (mecab/fugashi) — dự án hiện KHÔNG có dependency đó ở đâu. `topics[]` do
  Gemini sinh ra đã là các cụm từ khoá NGẮN (2-6 ký tự thường gặp), so khớp substring đủ dùng ở quy
  mô hiện tại (<50 video/kênh) và không cần thêm dependency.
- Sort giảm dần theo score, lấy top N. Nếu tất cả score = 0 (không khớp gì) → **in cảnh báo rõ**,
  vẫn trả về N video có view_count cao nhất làm phương án dự phòng (không trả rỗng).
- Output: in ra terminal + ghi `--dna-dir/_retrieved/<timestamp>.json` (danh sách video_id + score +
  đường dẫn file) để Claude đọc trực tiếp.

**Rào chắn:** nếu `VIDEO_ANALYSIS/` rỗng hoặc không tồn tại → `SystemExit` báo rõ "chưa chạy
channel_analyzer.py cho kênh này", không âm thầm trả danh sách rỗng.

## Thành phần 3 — sửa `pipeline/llm_client.py`

Thêm **đúng 1 entry mới** vào `CHAINS`, không sửa logic `chat()`:
```python
CHAINS = {
    "script": [...],   # KHÔNG ĐỔI
    "short": [...],    # KHÔNG ĐỔI — vẫn dùng cho VIDEO_ANALYSIS/*.json (bước 4 ở trên)
    "analysis": [("ramclouds", "gemini-3.8-flash"),
                 ("ramclouds", "gpt-5.6-luna"),
                 ("ns24", "gemini-3.8-flash")],   # MỚI — tách khỏi "script" theo đúng yêu cầu
}
```
Chain này dùng CÙNG model đã verify (không thêm model chưa test), chỉ tách KEY để tránh việc sau
này đổi tham số/model của `CHAINS["script"]` (phục vụ viết kịch bản sáng tạo) vô tình ảnh hưởng tới
việc tổng hợp DNA (một use-case khác hẳn về bản chất). Gọi qua `chat(prompt, task="analysis",
min_chars=800, require_sentence_end=False, max_tokens=16000)` — `require_sentence_end=False` vì
`CHANNEL_DNA.md` là markdown có heading, không phải văn xuôi kết bằng dấu câu.

## Thành phần 4 — sửa SOP của h2dev (không đụng skill global)

`docs/SOP_TOSHI_DENSETSU_JP.md` (và các SOP lane khác khi áp dụng thêm sau) thêm 1 bước MỚI đứng
TRƯỚC khi vào P1 của skill `youtube-series-builder`:
```
py -3.13 pipeline\channel_analyzer.py --channel-url <URL> --out-dir docs/channel_dna/<slug>/
```
rồi đọc `CHANNEL_DNA.md` thay vì tự chạy `yt-dlp`+transcript-api đọc thô như hướng dẫn gốc của skill
P1. Khi viết kịch bản 1 tập cụ thể, thêm bước:
```
py -3.13 pipeline\retrieve_videos.py --dna-dir docs/channel_dna/<slug>/ --topic "<chủ đề tập mới>"
```
rồi đọc N file trả về + `CHANNEL_DNA.md` làm input viết script (thay vì đọc 3-4 transcript thô).

Đây là sửa **tài liệu của riêng h2dev** (CLAUDE.md/docs của project này đè lên hướng dẫn skill global
theo đúng thứ tự ưu tiên đã nêu ở đầu phiên: chỉ thị riêng của user luôn thắng skill mặc định).

## Kế hoạch test (pilot)

1. Chạy `channel_analyzer.py --channel-url <URL kênh 今夜も都市伝説>` (kênh đã có trong
   `docs/laneA_from_research/data/titles.json`) — crawl fresh hoàn toàn, không đọc lại data cũ.
2. Đối chiếu `CHANNEL_DNA.md` tự sinh với `LANE_A_NICHE_KIT.md` viết tay: kiểm DNA tự động có bắt
   được các pattern ĐÃ BIẾT là thật không (vd: công thức tiêu đề "kết thúc bằng ？" ~62%, khối tag
   `【都市伝説 ミステリー 怖い話】`, nhịp giữ chân `しかし/だが`...). Đây là tiêu chí nghiệm thu chính —
   không phải "chạy không lỗi" mà là "nội dung DNA có đúng/đủ so với sự thật đã biết".
3. Chạy `retrieve_videos.py --topic "UFO và chính phủ che giấu"` (chủ đề giả định) → kiểm kết quả trả
   về có hợp lý (video về UFO/chính phủ được xếp hạng cao hơn video về khoảng cách vũ trụ) không.
4. Đo thời gian + số ký tự input/output mỗi cuộc gọi Gemini — ghi vào báo cáo test theo quy ước dự án
   (memory `bao-cao-test-phai-kem-thoi-gian`: mọi lần test phải kèm số đo thời gian).

## Ngoài phạm vi (KHÔNG làm ở lần này — YAGNI)

- Retrieval bằng embedding/vector DB — chỉ cần khi 1 kênh có >50-100 video, hiện tại các kênh h2dev
  đều dưới ngưỡng đó.
- Sửa skill global `youtube-series-builder`/`youtube-script`/`youtube-produce`.
- Áp dụng đồng loạt cho mọi lane (satori-jp-obaa, laneD...) — chỉ làm pilot Lane A trước, lane khác
  áp dụng sau khi pilot verify xong.
- Crawl comment (`youtube-comment-downloader`) — `LANE_A_NICHE_KIT.md` cho thấy comment rất hữu ích
  (phân khúc khán giả), nhưng đây là mở rộng có thể thêm SAU khi core (DNA + retrieval) đã chạy ổn;
  không đưa vào MVP để giữ phạm vi gọn.
