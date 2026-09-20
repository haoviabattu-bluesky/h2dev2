# SOP — SẢN XUẤT 1 VIDEO SATORI NHẬT (runbook chuẩn, gọi ra chạy ngay)

> **Trigger:** anh nói "làm video satori mới", "làm video Nhật (chủ đề X)", "nhân bản video <url> sang Nhật"
> → LÀM THEO ĐÚNG file này, KHÔNG tìm hiểu lại. Chuẩn cứng: **làm GIỐNG bản gốc simbot2** (25-30 phút, nhiều
> ảnh, thumbnail chữ to). Xem thêm memory: openspeaker-ai33-tts, uu-tien-lam-giong-ban-goc, ww2-pipeline.

Ngách ACTIVE: **Satori (悟り系) câu chuyện người già NHẬT** — nhân bản 70/30 từ kênh đối thủ
**simbot2「노년의 마음소리」** (Hàn, 노후/thừa kế/sức khoẻ/tang lễ). Ngôn ngữ output: **tiếng Nhật**.
Tất cả tool + key đã dựng & verify (2026-09-07). Chi phí ~**5.600đ/video** all-in.

## 0. HẠ TẦNG (đã có sẵn — chỉ kiểm nếu lỗi)
- `pipeline/` : fetch_script.py · gpti2_gen.py · gpti2_edit.py (REF-LOCK) · grok_gen.py (cảnh trẻ em) · gen_images.py (marker @REF/@REF2/@GROK) · qc_character.py (QC tuổi/giới nhân vật) · openspeaker_tts.py · tts.py · thumbnail_text.py · assemble.py
- Lib: youtube-transcript-api, yt-dlp, edge-tts, imageio-ffmpeg, PIL, requests (py -3.13, đã cài)
- Key gpti2 (ảnh) trong gpti2_gen.py · Key ai33/OpenSpeaker (giọng+BGM) trong openspeaker_tts.py + CLAUDE.md
- Login ai33 (nếu cần web): profile Chrome RIÊNG `E:\CLAUDE\YOUTUBE\h2dev\ai33_profile` CDP 9346 (KHÔNG dùng profile khoá học)
- Skill sáng tạo (TỔNG QUÁT + GLOBAL ở `~/.claude/skills/`, dùng cho mọi dự án; niche/market = tham số):
  `youtube-script` · `youtube-image-prompts` · `youtube-thumbnail` · `youtube-series-builder`. (Gọi qua Skill tool.)

## ⭐⭐ CỔNG QC BẮT BUỘC SAU MỖI BƯỚC (user chốt 2026-09-08: "phải có QC sau mỗi bước, sản phẩm đầu ra phải hoàn hảo")
KHÔNG được sang bước sau khi cổng QC bước trước còn lỗi thật. Chạy TẤT CẢ, không bỏ cổng nào. Tool: `qc_script.py` + `qc_visual.py`.
Lỗi HẠ TẦNG (mạng/model) ≠ "0 lỗi" — QC không chạy được thì KHÔNG PASS (bẫy 503 im lặng).
| Sau bước | Cổng | Lệnh | PASS khi |
|---|---|---|---|
| B2 transcript | **B2Q** (mới 2026-09-18) | `py -3.13 qc_transcript.py --slug ../assets/satori_jp/$SLUG` | PASS: coverage ≥92%, gap ≤45s, dup ≤15%; WARN (đi tiếp): coverage 80-92% / gap>45s / cpm<120 / không có thời lượng; FAIL: coverage<80%, dup>15%, transcript rỗng, sidecar hỏng; **SKIPPED** (không có `competitor.segments.json`) chỉ được đi tiếp với tập bóc TRƯỚC 2026-09-18 — tập mới mà SKIPPED = fetch không ghi sidecar, lỗi pipeline |
| B3 script | **B3Q** | `qc_script.py --profile <id> --script script.txt --competitor competitor_ko.txt` (gemini) | đọc-hiểu=ĐẠT, 0 mâu thuẫn tuổi/số/vai vế, **0 dấu vết ngôn ngữ nguồn** (半地下/紅参/文字=SMS/자개장…), 0 câu chép verbatim (nghĩa trùng do 70/30 thì chấp nhận) |
| B3 script (sau B3Q) | **B3S** (mới 2026-09-18, **bắt buộc mọi tập từ STT10**) | `py -3.13 qc_script_sol.py --script script.txt --title-file TIEU_DE_MO_TA.txt --profile satori-jp-obaa --out logs/B3S_sol_001.txt` (GPT-5.6-sol, lens `story`; flow B tự gọi trong `brain_channel.check_b3s`) | PASS · FIX → Claude sửa CHỈ mục **SAI** rồi sol chấm lại 1 lần, FIX nhẹ vẫn qua · REMAKE → Claude kiểm từng lỗi, sửa, tự chấm `logs/B3S_claude_verdict.txt` = `PASS` hoặc `SAI LỖI KỊCH BẢN KHÔNG SỬA ĐƯỢC` (dừng). Tầng 2 Claude chấm (`qc_claude.py`) **bỏ** — quy trình đầy đủ: `docs/SOP_CLONE_BRAIN.md` § "QUY TRÌNH QC BƯỚC 1 CHUẨN" |
| B4 giọng | **B4Q** | `qc_visual.py voice --script script.txt --srt voice.srt --audio-sec <s>` | SRT phủ ≥85% kịch bản, cue tăng dần, khớp thời lượng |
| B5R master | **B5RQ** | `qc_visual.py master --img _ref/001.png --age N --gender X --look "…" --world "…"` (mỗi master) | tuổi ±12, đúng giới, **era_ok/costume_ok/style_ok/face_clear=true** |
| B5 loạt ảnh | **B5Q** | `qc_visual.py images --dir img --prompts img_prompts.txt --world "…" --sample 20` | 0 hỏng/đen/trùng, vision mẫu 0 sai |
| B5 prompt↔script | **B5P** (mới 2026-09-18) | `py -3.13 qc_prompt_consistency.py --slug ../assets/satori_jp/$SLUG` (sau `gate_common.py --stamp`) | FAIL cơ học: số prompt ≠ số dòng `img_doan.txt`, `@REF/@REF2` thiếu nhân vật, prompt rỗng, **STALE** (sha256 script ≠ lúc sinh), LLM lỗi hạ tầng; WARN (đi tiếp, mode warn mặc định): PROMPT_CONFLICT / AMBIGUOUS — đọc `logs/B5P_latest.json → metrics.semantic.would_block`; `--mode fail` CHƯA bật production (đo 2 tập) |
| B5.5 mapping | **B55** (mới 2026-09-18) | `py -3.13 qc_img_doan.py --slug ../assets/satori_jp/$SLUG` | FAIL cơ học: dòng malformed, ≠ số prompt, thiếu/thừa/trùng ID, đoạn ngoài 1..N, số đoạn GIẢM theo thứ tự, STALE, thiếu `img_doan.txt`, LLM lỗi hạ tầng; WARN: SUSPICIOUS (chia đều 2,3,2,3 / lệch bất thường — BẮT BUỘC chạy có LLM, `--no-llm` khi SUSPICIOUS = chưa kiểm), semantic ≤2 (mode warn) — đọc `logs/B55_mapping_latest.json → metrics.semantic.would_block` |
| B8 video | **B8Q** | `qc_visual.py video --mp4 final.mp4 --srt voice.srt --audio-sec <s> --sample 12` | 0 khung đen, ảnh KHỚP lời đang đọc, phụ đề cháy đúng |
⚠️ **BÀI HỌC yokin-basho (2026-09-08):** làm xong "mượt" nhưng CHƯA chạy B3Q → lọt 8 lỗi thật vào video (chồng mất 2 vs 3 năm; 450万×3≠1300; Shota gọi em gái là 姉さん; 半地下/紅参/文字-SMS Hàn; câu chép). Soi frame chỉ thấy sync ảnh/lời, KHÔNG bắt được mâu thuẫn nội dung. → **luôn B3Q trước khi tiêu tiền giọng+ảnh.**

## 0b. CHANNEL ANALYZER — tổng hợp DNA kênh simbot2 (mới, 2026-09-16, chạy 1 lần không phải mỗi tập)

Trước đây B1/B2 mỗi tập đều phải tự đọc lại video mẫu để nắm giọng/cấu trúc kênh. Nay có
`pipeline/channel_analyzer.py` (thiết kế: `docs/superpowers/specs/2026-09-16-gemini-channel-
analyzer-design.md`) tổng hợp SẴN 1 lần thành `docs/channel_dna/simbot2/CHANNEL_DNA.md` +
`VIDEO_ANALYSIS/*.json` — **đã verify thật 2026-09-16** (4 video, 70s, 100% phân tích được, QC DNA
"ĐẠT" 11/11 đề mục, `topics` ra đúng tiếng Hàn nguyên bản).

**Đã có sẵn, không cần chạy lại** trừ khi muốn nạp thêm video mới:
```bash
py -3.13 pipeline\channel_analyzer.py --channel-url "https://www.youtube.com/@simbot2" \
    --out-dir docs\channel_dna\simbot2 --n-candidates 20 --n-select 10 --langs ko,en \
    --niche-hint "노후·가족·건강 이야기 (한국어 시니어 스토리 채널)"
```
(Chốt 2026-09-16: xét toàn kênh nếu <=20 video, kênh lớn hơn lấy top 20 theo view rồi chọn lọc 10
video tốt nhất có transcript đưa vào phân tích. Bản đã chạy trước đó dùng `--n-videos 4` kiểu cũ để
test nhanh — muốn phủ rộng hơn chạy lại lệnh trên, sẽ TỰ dùng lại video đã phân tích (không gọi lại
Gemini) và chỉ crawl/phân tích thêm phần còn thiếu.)

**Dùng khi chọn chủ đề mới (thay một phần B1 dưới đây):**
```bash
py -3.13 pipeline\retrieve_videos.py --dna-dir docs\channel_dna\simbot2 \
    --topic "<mô tả chủ đề tập sắp làm, tiếng Hàn>" --top-n 5
```
Đọc `CHANNEL_DNA.md` (công thức kênh, không cần tự đọc transcript thô để "cảm" nữa) + video top-1
trong kết quả trả về vẫn dùng làm `competitor.txt` ở B2 như cũ (giữ nguyên 1 transcript đầy để không
mất nhịp câu — xem giới hạn định lượng của DNA tự động ở `docs/superpowers/specs/2026-09-16-gemini-
channel-analyzer-design.md`, mục đã ghi ở SOP Lane A).

## QUY TRÌNH 8 BƯỚC (đặt SLUG cho video, mọi file nằm ở assets/satori_jp/$SLUG/)

### B1 — CHỌN CHỦ ĐỀ (nguồn = simbot2 hoặc anh chỉ định)
```bash
py -3.13 -m yt_dlp --no-warnings --flat-playlist -I 1:40 --print "%(view_count)s|%(duration)s|%(id)s|%(title)s" "https://www.youtube.com/@simbot2/videos"
```
Chọn video **cao view + gần đây (≤1-2 tháng)**. Lấy video_id.

### B2 — BÓC KỊCH BẢN ĐỐI THỦ
```bash
cd e:/CLAUDE/YOUTUBE/h2dev/pipeline
py -3.13 fetch_script.py "<video_id>" --lang ko --out ../assets/satori_jp/$SLUG/competitor.txt
py -3.13 qc_transcript.py --slug ../assets/satori_jp/$SLUG        # B2Q (mới 2026-09-18): transcript cụt/lặp → FAIL, không viết script trên transcript hỏng
```
- **B2Q `SKIPPED` chỉ được đi tiếp khi `competitor.txt` bóc TRƯỚC P0 (2026-09-18, không có sidecar
  `competitor.segments.json`).** `fetch_script.py` từ 2026-09-18 LUÔN ghi sidecar cạnh `competitor.txt` — tập mới mà
  B2Q báo SKIPPED là lỗi pipeline (fetch không ghi sidecar), phải xem lại, KHÔNG coi là qua. Đo thật Kmxva85WKec: nguồn api,
  694 đoạn, coverage 1.0, cpm 341.9 → PASS.
Đọc để nắm: cốt truyện, nhân vật, **bài học/twist**, cấu trúc.
- ⚠️ **TỐC ĐỘ:** YouTube hay chặn 429 endpoint timedtext theo IP → tool tụt xuống whisper (tải audio + nghe lại,
  chậm ~3-5' cho video 33'). KHÔNG phải thiếu repo — pipeline đã tối ưu 3 tầng (api→yt-dlp auto-subs→whisper).
  Tăng tốc = tầng yt-dlp auto-subs (vài giây, đã thêm retry backoff 429) / proxy dân cư (Deeper DPN) / cookies
  (`YTDLP_COOKIES`/`YTDLP_COOKIES_BROWSER=chrome`) / whisper model `tiny` (`--whisper-model tiny`, transcript chỉ tham chiếu). Thiếu thư mục $SLUG → tự `mkdir -p` trước (fetch_script không tự tạo).

### B3 — VIẾT SCRIPT NHẬT 70/30 (Claude làm, theo skill youtube-script)
- Ngôi 1 **người già Nhật** kể chuyện đời mình, bọc bài học thực tế.
- **Nhật hoá 100%:** 縁側/仏壇/四十九日/年金/相続/介護/終活... (KHÔNG để dấu vết Hàn). Nếu chủ đề pháp lý/tài chính →
  **chính xác luật Nhật** (vd 相続放棄/限定承認/熟慮期間3ヶ月/法定単純承認/仮払い150万/連帯保証).
- **ĐỘ DÀI — dùng CHAR-RATE đã đo thật, đừng ước lượng mò:** giọng `ado`+`age med` ≈ **309 chữ (không tính
  xuống dòng/space, cả CJK) / phút**. → **30 phút ≈ 9.000-9.500 chữ**; 25' ≈ 7.700. **BẮT BUỘC đếm trước khi TTS:**
  `py -3.13 -c "t=open('script.txt',encoding='utf-8').read();print(len(t.replace(chr(10),'').replace(' ','').replace('　','')))"`
  rồi chia 309 ra phút. (Bài học thật EP4: viết 13.700 chữ = 44' → phải viết lại còn ~11.300. Đừng lặp.)
  Giọng khác thì đo lại char-rate 1 lần rồi ghi cạnh entry channels.json.
- Cấu trúc: mở cảnh điện ảnh (ngày+mùa+nơi+cử chỉ) → gieo伏線 → cao trào → **悟り** (1 câu triết lý) → 3 kết + comment-bait. Giữ nhân phẩm người già.
- Output **voiceover-ready** (pure prose, KHÔNG 「パート」/marker/heading). Lưu `assets/satori_jp/$SLUG/script.txt`.

### B4 — GIỌNG ĐỌC (ai33/OpenSpeaker + phụ đề) — GIỌNG THEO HỒ SƠ KÊNH
⚠️ **Giọng là cấu hình PER-KÊNH** (mỗi kênh = 1 nhân vật NHẤT QUÁN). Nạp tự động qua `--channel <id>`
(đọc `pipeline/channels.json`) để mọi video CÙNG kênh dùng CÙNG giọng:
```bash
py -3.13 tts.py --script ../assets/satori_jp/$SLUG/script.txt --provider openspeaker --channel satori-jp-obaa --out ../assets/satori_jp/$SLUG/voice.mp3
```
Kênh hiện tại `satori-jp-obaa` = **cụ bà** → voice `ado` + `age med` + speed 0.92 (nữ, làm già ấm chậm).
→ voice.mp3 + voice.srt (server-sync). Fallback free: thêm `--provider edge`.
- ⭐ **B4.1 SỬA PHỤ ĐỀ CHO KHỚP KỊCH BẢN (BẮT BUỘC, user chốt 2026-09-08):** voice.srt do server **STT NGHE LẠI** audio
  → sai vài chỗ đồng âm (他人様→しとぎ様, 満州→銃, 灯→智仁...). Audio đọc ĐÚNG nhưng phụ đề cháy SAI CHỮ (lỗi câm,
  chỉ thấy khi soi frame). PHẢI chạy: `py -3.13 srt_from_script.py --srt <slug>/voice.srt --script <slug>/script.txt`
  (giữ timestamp, thay chữ = script gốc qua difflib; backup .stt.srt). Rồi mới B5/B8 dùng voice.srt đã sửa.
- ⭐ **B4.2 GIÃN NHỊP LỜI KỂ (BẮT BUỘC — giọng người già, user chốt 2026-09-08):** OpenSpeaker đọc gần liền mạch
  (~0,14s nghỉ/cue) → khán giả già MỆT, không kịp lắng nghe/nhớ. Chạy `py -3.13 pace_audio.py --audio <slug>/voice.mp3
  --srt <slug>/voice.srt --script <slug>/script.txt` → cắt mp3 tại ranh cue + chèn im lặng (câu 0,65s / giữa câu
  0,20s / hết đoạn 1,5s / 0,5s đầu) → **voice_paced.wav + voice_paced.srt** (KHÔNG atempo nên KHÔNG trôi, lệch 6ms).
  Video dài thêm ~17-22% (đo youyoin 33'→38'). **B8 assemble dùng voice_paced.wav + voice_paced.srt.** Ảnh giữ
  nguyên (assemble chia theo cue-index). Chỉnh núm: `--sentence/--mid/--para` (giây). Thứ tự: B4 → B4.1 reflow → B4.2 pace.

**Quy tắc chọn giọng khi LẬP KÊNH MỚI** (khớp nhân vật/giới/tuổi của kênh, ghi vào channels.json):
- Giới phải khớp ngôi 1 của script: bà cụ→NỮ, ông cụ→NAM.
- NỮ: `ado`/naomi/hikari/kindlady/calmlady · NAM: `enishi`/papaji/akira/garyu/senior.
- **Làm già giọng** (`--age`): `med` = chuẩn người già (đã chốt), `mild` nhẹ hơn, `frail` già yếu run, `none` tắt.
  (age = hậu kỳ hạ pitch + cắt treble, giữ nguyên thời lượng → SRT vẫn khớp.)
Ghi lại thời lượng thật (voice) để tính số ảnh ở B5.

> **THÊM KÊNH MỚI:** thêm 1 entry vào `pipeline/channels.json` (market/niche/competitor/narrator/voice/age/
> speed/bgm) rồi dùng `--channel <id_mới>`. Mỗi kênh giữ nhân vật nhất quán; kênh khác = giọng/tuổi/giới khác.

### B5 — PROMPT ẢNH (Claude, theo skill youtube-image-prompts) + GEN
- ⚠️ **Tập có `stock_plan.tsv` ở gốc thư mục = tập HYBRID.** Sau khi máy 2 trả ảnh nhóm AI và
  `audit_stock.py` chấm xong nhóm STOCK, chạy NGAY:
  ```bash
  py -3.13 hybrid_chuan_bi.py --slug ../assets/satori_jp/$SLUG --profile satori-jp-obaa
  ```
  Tool này tự làm HẾT phần bước 1 (đổi dòng STOCK bị loại → AI_FALLBACK + tự vẽ bù bằng gpti2 +
  copy ảnh máy 2 vào `img/` + chuỗi audio B4→B4Q + `anchors.txt`) — chạy tới khi ra
  `>> ĐỦ ĐIỀU KIỆN GIAO BƯỚC 3` mới bàn giao. TUYỆT ĐỐI không tự trích khung tĩnh từ `stock/*.mp4`
  nhét vào `img/` (sự cố thật 2026-09-17, STT8 — memory `img-thieu-o-tap-hybrid-la-dung-thiet-ke`):
  8 dòng STOCK thật (`status=OK`) phải giữ nguyên KHÔNG có trong `img/`, chỉ compositor mới được
  dùng. Chi tiết phân việc + luật AI_FALLBACK: **`docs/GIAO_VIEC_HYBRID_COMPOSITOR.md` §3b/§3c**.
  Đường render đúng cho tập hybrid là compositor riêng ở file đó, KHÔNG PHẢI
  `render_engine.py`/`QUY_TRINH_RENDER_VIDEO.md`.
- ⭐ **3 lệnh BẮT BUỘC ngay sau khi viết xong `img_prompts.txt` + `img_doan.txt` (P0, 2026-09-18)** — stamp
  fingerprint rồi chạy 2 cổng, đọc `would_block` (= số ca sẽ bị chặn NẾU bật `--mode fail`; sau 2 tập mới quyết bật):
  ```bash
  py -3.13 gate_common.py --slug ../assets/satori_jp/$SLUG --stamp          # ghi artifact_meta.json (sha256 script ↔ prompt/img_doan); script sửa sau đó = STALE chặn cứng
  py -3.13 qc_prompt_consistency.py --slug ../assets/satori_jp/$SLUG        # B5P: prompt ↔ story facts → logs/B5P_latest.json
  py -3.13 qc_img_doan.py --slug ../assets/satori_jp/$SLUG                  # B55: mapping ảnh↔đoạn → logs/B55_mapping_latest.json
  ```
  Tập cũ chưa có `artifact_meta.json`: chạy 2 cổng QC TRƯỚC để biết prompt/mapping còn khớp script hiện tại không,
  RỒI MỚI `--stamp` — cấm stamp mù cho tập biết là stale (STT7: script 07:58 mới hơn prompt 07:35). Tập đã giao
  hàng (ep01/04/06/07…) không cần stamp trừ khi làm lại; STT3 đã stamp, STT8/STT2/STT5 stamp khi đụng tới.
  `hybrid_chuan_bi.py` cũng tự chạy STALE + `qc_img_doan --no-llm` ngay trước `sinh_neo.py` (exit 1 nếu rớt).
- **CHARACTER SHEET cố định** cho mỗi nhân vật (tuổi/tóc/trang phục) — LẶP nguyên văn trong mọi prompt.
  ⚠️ Text-only CHỈ giữ "cùng kiểu người", KHÔNG giữ cùng KHUÔN MẶT (gpti2 không seed — đo thật 2026-09-07:
  4 cảnh cùng 1 CHARACTER SHEET ra 4 ông cụ khác nhau, xem `assets/_char_test/COMPARE.png`).
- ⭐ **B5.0-BIBLE — HỒ SƠ NHÂN VẬT trước khi tạo ảnh (user chốt 2026-09-08).** Phải thiết kế nhân vật HÀI HOÀ
  (tuổi/ngoại hình/tính cách/phong cách) + **TOÁN TUỔI QUAN HỆ hợp lý** RỒI mới sinh master. Viết
  `<slug>/characters.json` (name/age/gender/role/look/personality + `relationships` với min_gap/max_gap). Suy tuổi
  từ chuyện: cưới ~22-27, sinh con → **tuổi con = tuổi cha mẹ − (25..35)**; mẹ 73 thì con ~40-50 (KHÔNG để con
  nhìn 10 tuổi hay ngang tuổi mẹ). Con cả > các con sau (đừng để con gái già hơn con cả). Con là TRẺ EM thật →
  route `@GROK`. Master prompt sinh RA TỪ bible (tuổi + đặc điểm độc nhất).
- ⭐ **B5.0 REF-LOCK — BẮT BUỘC (user chốt 2026-09-08: mặt nhân vật phải NHẤT QUÁN từ đầu đến cuối video).**
  4 EP đầu KHÔNG dùng REF-LOCK → mặt đổi từng cảnh = LỖI, không lặp lại. Quy trình 1-lượt (đã nâng cấp
  gen_images.py hỗ trợ marker `@REF` per-dòng 2026-09-08):
  1. Sinh 1 ảnh MASTER portrait mỗi nhân vật (nền xám trơn, chính diện, sáng đều, đặc điểm độc nhất
     như nốt ruồi/kiểu kính, **kèm TUỔI từ bible**): `gen_images.py --prompts <slug>/master.txt --out <slug>/_ref --quality medium`.
  1b. ⭐ **QC master bằng AI vision TRƯỚC khi gen loạt:** `py -3.13 qc_character.py --bible <slug>/characters.json`
     (model gemini-3.8-flash + grok-4.6, trung bình) → ước lượng tuổi/giới mỗi master + kiểm chênh tuổi quan hệ.
     FLAG (lệch >±12 tuổi / sai giới / nhìn trẻ con dù người lớn / chênh tuổi quan hệ vô lý) → **sửa master prompt
     rồi gen + QC lại**, ĐỪNG gen cả loạt khi master còn sai tuổi. (Đo thật EP1: Fumi ~73 ✅, con trai ~54 vs
     thiết kế 47 — đạt ngưỡng nhưng hơi già.)
  2. Trong `img_prompts.txt`: **mọi cảnh THẤY MẶT nhân vật chính → thêm tiền tố `@REF ` đầu dòng**; cảnh
     phong cảnh/đồ vật/tay/người ở xa để dòng THƯỜNG (không nhét mặt, rẻ 50đ). Prompt cảnh @REF nên nói rõ
     "the SAME person from the reference image, identical face, in a NEW scene: <SHOT>".
  3. Gen 1 lượt: `gen_images.py --prompts <slug>/img_prompts.txt --out <slug>/img --ref <slug>/_ref/001.png
     --orient landscape --quality low` → dòng `@REF` khoá mặt (**110đ**, gpti2 edit), dòng thường text-only
     (**50đ**), đúng thứ tự + resume. `low` đủ giữ mặt (ngang medium, rẻ ~4 lần — `assets/_char_test/COMPARE.png`).
  **2 nhân vật cần khoá mặt** (vd người kể + 1 người quan trọng): dùng `@REF` cho nhân vật 1 + `@REF2` cho nhân
  vật 2, chạy `gen_images.py --ref masterA.png --ref2 masterB.png` (nâng cấp 2026-09-08). Nhân vật xuất hiện ở
  NHIỀU độ tuổi (vd chồng lúc 20s/50s/70s) hoặc nhân vật một-lần → để plain (biến thiên là tự nhiên). Cảnh có cả
  2 nhân vật → đánh marker theo người ĐANG LÀ TÂM ĐIỂM khung. Tối đa 8 ảnh/`--ref`. Bẫy chi tiết: skill
  `youtube-image-prompts`.
- Viết **~1 ảnh / 6-7s** theo mạch truyện, granular (wide/medium/close/detail + nhiều khoảnh khắc). Video
  25-31' → **~280-300 ảnh**, trần chi phí **20.000đ/video** (user chốt 2026-09-09).
  **Định mức này lấy từ SỐ ĐO THẬT của đối thủ**, không phải ước lượng: simbot2 (vU5PWT2zLDs) chạy
  **~348 tranh cho 29 phút = 5,0s/tranh**, không tranh nào giữ quá 5s; bản clone cũ của mình 124 ảnh/31' =
  15,0s/ảnh, tức **chậm gấp 3 lần bản gốc**. Cách đo lại: memory `phan-tich-video-doi-thu`.
  **Công thức tiền (gpti2): n × (50 + 60×tỉ_lệ_ref) ≤ 20.000đ** — ảnh `@REF` là 110đ (50 + 60 phụ phí ref),
  ảnh thường 50đ. Cấu hình chuẩn: **290 ảnh = 87 ref (30%) × 110đ + 203 thường × 50đ = 19.720đ → 6,4s/ảnh.**
  ⚠️ **Giữ tỉ lệ `@REF` ≤ 30%** — đây là đòn bẩy chi phí lớn nhất: ở bản cũ 49/124 ảnh ref (40%) ngốn
  **59% tổng tiền cho 40% số ảnh**. Chỉ khoá mặt ở cảnh THẬT SỰ thấy rõ mặt; bàn tay/đồ vật/lưng/cảnh vật/
  over-shoulder → ảnh thường. Hạ 40%→30% mua thêm được ~20 ảnh trong cùng túi tiền.
  ⚠️ **KHÔNG tái dùng ảnh** (user chốt 2026-09-09): mỗi shot phải là ảnh MỚI — cấm cắt 1 ảnh thành nhiều
  khuôn hình để tăng nhịp. Đối thủ cũng vẽ mới hoàn toàn (đo: chỉ 26/387 cặp gần giống, đều là crossfade
  giây liền kề, không phải dùng lại).
  Style: `cinematic ultra-realistic color, photorealistic, 8K, warm emotional lighting, authentic Japanese setting,
  16:9, no text`. Người **Nhật**. Né gore.
- ⚠️ **Content-policy — 3 bẫy đã dính, viết prompt né sẵn:**
  (1) ⭐ **TRẺ EM/EM BÉ trên gpti2 = CHẶN TUYỆT ĐỐI** (đo thật 2026-09-08: 7/7 prompt trẻ em bị chặn, kể cả
  cảnh lành mạnh "bé 3 tuổi chơi đồ gỗ", kể cả **silhouette không thấy mặt**, kể cả "học sinh tiểu học" — Azure
  chặn theo TỪ/khái niệm minor: child/kid/baby/infant/toddler/students/little girl/số tuổi). → **2 cách xử lý:**
  (a) **cảnh có trẻ em → dùng marker `@GROK`** đầu dòng trong img_prompts.txt → gen_images route sang **Grok
  Imagine** (grok-imagine-image-2.0, cho phép ảnh trẻ em lành mạnh — verify: bé chơi, em bé quấn tã, bé gái ở mộ,
  mẹ ôm con trong bão tuyết đều OK; ảnh 1280×720). (b) nếu không muốn trẻ em thật → tả **VẬT tượng trưng**
  (おくるみ/産着/でんでん太鼓, KHÔNG có người = qua gpti2) hoặc **"bundle" ôm từ phía sau, KHÔNG gọi tên trẻ, không
  thấy mặt** (verify R4 OK trên gpti2). Bằng chứng: `assets/satori_jp/_reftest/childtest/`.
  (2) **cảnh tắm/sento** ("washing back", "steamy bathhouse", khoả thân) bị chặn "gợi dục" → **mặc kín** (quấn khăn
  cotton/yukata, phòng thay đồ, "modest and fully covered"). (3) bạo lực/máu → biểu tượng. Ảnh gpti2 lỗi:
  **sửa prompt rồi chạy lại (resume), retry ≤3 lần**; quá 3 lần → chuyển `@GROK` hoặc bỏ cảnh.
- Lưu `assets/satori_jp/$SLUG/img_prompts.txt` (mỗi dòng 1 prompt) rồi:
```bash
py -3.13 gen_images.py --prompts ../assets/satori_jp/$SLUG/img_prompts.txt --out ../assets/satori_jp/$SLUG/img --quality low --workers 6
```
(resume tự bỏ ảnh đã có; 1 prompt lỗi vẫn chạy tiếp → sửa prompt đó rồi chạy lại.)

### B6 — NHẠC NỀN BGM (tái dùng track có sẵn HOẶC gen mới)
Đã có `assets/satori_jp/_bgm/bgm1.mp3` (piano cảm xúc 3:55) — **dùng lại được cho mọi video**. Gen mới nếu muốn:
```bash
py -3.13 -c "import openspeaker_tts as o;open('../assets/satori_jp/_bgm/bgmX.mp3','wb').write(o.generate_music('gentle emotional piano, calm nostalgic tender, instrumental', instrumental=True))"
```

### B7 — THUMBNAIL CHỮ (kiểu simbot2: chữ to phủ + banner đỏ)
- Nền mềm: gpti2 gen 1 ảnh cảnh Nhật mờ/ấm (hoặc dùng lại 1 ảnh trong img/).
- Config `assets/satori_jp/$SLUG/thumb_text.txt` (mỗi dòng `MÀU|nội dung`, dòng cuối `BANNER|...`; MÀU=WHITE/YELLOW/RED):
```
WHITE|<hook dòng 1>
YELLOW|<hook dòng 2>
RED|<câu hỏi/keyword gây sốc>
BANNER|<sub "sự thật ... người X tiết lộ">
```
```bash
py -3.13 thumbnail_text.py --bg <nền.png> --text ../assets/satori_jp/$SLUG/thumb_text.txt --out ../assets/satori_jp/$SLUG/thumbnail_final.png --side left --side-width 0.60 --subject-side right --fit-height --fit-each --max-size 200
```
> ⭐⭐ **FREEZE 2026-09-17 — thumbnail ep1 đã HUMAN APPROVED → `docs/thumbnail_lanes/satori_jp/`
> (TEMPLATE.md hard lock · MASTER_REFERENCE.png · golden/GOLDEN_001_hidden_move.md). Từ tập 2: LOAD
> skill global `youtube-thumbnail` + TEMPLATE.md + MỞ MASTER_REFERENCE.png + golden liên quan TRƯỚC khi
> viết thumb_text; Final QC so với MASTER_REFERENCE. Golden/Master chỉ được thêm khi QC PASS + HUMAN
> APPROVED. Tóm tắt luật ngay dưới đây.**
> ⭐ **TEMPLATE THUMBNAIL LANE NÀY — HARD LOCK (user chốt 2026-09-17, ep1):** nhân vật bên PHẢI ·
> chữ chính bên TRÁI · **RED BOTTOM BANNER bắt buộc** (visual identity kênh — cấm bỏ dù "lặp ý") ·
> **SENIOR TYPOGRAPHY**: khán giả Nhật lớn tuổi → chữ trái phải RẤT LỚN, `--fit-each` fit TỪNG DÒNG
> theo bề ngang cột (dòng ngắn được to hơn dòng dài, không để dòng dài nhất ép cả khối), khối chữ SÁT
> nhau, không dàn đều khoảng dư. Ưu tiên FONT SIZE > khoảng trống. **Text structure: 3+1 PREFERRED, 4+1
> FALLBACK** (chỉ khi nén về 3 làm hỏng tiếng Nhật/mất contradiction — xem TEMPLATE.md §2). Cờ đã khai sẵn ở
> `profile.thumbnail.{side_width,max_font,extra_flags}` nên B7 (make_video/render_engine) tự dựng
> đúng lệnh. Đo thật ep1: 78/196/100px + banner ~100px. **HUMAN APPROVED 2026-09-18:** toàn bộ
> background phải là **một scene current-story liên tục toàn khung**, không chia một bên đen/một bên portrait.
> Subject REF lớn và hòa tự nhiên ở khoảng 1/3 phải; không panel chữ nhật/cutout halo. 3 dòng chữ đè trực tiếp
> lên scene bên trái, mặc định stroke/shadow đủ đọc; contrast veil chỉ rất nhẹ khi cần. Scene phải vẫn nhận ra
> ở 360px. Blur scene trái mặc định 3px với feather rộng ~12% canvas; vùng subject/mặt phải pixel-sharp.
> Giữ HERO/banner nếu đã đủ mạnh. Đạo cụ cầm CAO (banner che ~22% đáy). Quy tắc này
> CHỈ cho lane satori — lane khác có typography riêng.

> **CONTENT × TYPOGRAPHY QUALITY GATE (2026-09-19):** trước render phải tạo ít nhất 3 hướng từ
> TITLE + DESCRIPTION/SCRIPT hiện tại: A contradiction, B discovery/shock, C emotional conflict/secret.
> Chấm 1–5 theo accuracy, specificity, stakes, curiosity, title complement, Japanese naturalness,
> 1–2 second clarity; winner điểm cao nhất và phải khớp nguyên văn copy render. Không làm yếu semantic
> để đổi lấy font lớn. FACE hard-safe; BODY/HAND/PROP conditional. Banner phải có nghĩa độc lập, cấm
> `衝撃の真実` / `まさかの結末` / `その理由とは？`. Sau render phải challenge lại authority ở 360px,
> wasted space và semantic hierarchy; còn cải thiện đáng kể thì tự sửa/render lại.

### B7b — TIÊU ĐỀ + MÔ TẢ ĐĂNG TẢI (bắt buộc, bước 1 — KHÔNG để bước 3 tự viết)
⭐ **Chốt 2026-09-17 sau sự cố thật:** 2 tập (STT2, STT5) giao qua nhánh ghép video riêng (hybrid
compositor) đã lọt tới người xem với `listting.txt` chỉ là placeholder kỹ thuật (463-665 byte,
không tiêu đề thật/không mô tả/không mốc chương) — vì bước 2 (máy vẽ ảnh) và bước 3 (máy ghép video)
đều là công cụ CƠ HỌC, không hiểu nội dung, không viết được tiêu đề/mô tả tử tế. **Việc này PHẢI làm
ở bước 1**, ngay sau khi `script.txt` đã ĐẠT mọi cổng QC. File `TIEU_DE_MO_TA.txt` giờ nằm trong danh
sách file bắt buộc của `brain_channel.py`/`brain_steps.py` (rào cứng trong code, không chỉ ghi tài
liệu) — thiếu file này thì bộ não coi như CHƯA XONG bước 1.

Khuôn cố định: tiêu đề (1 dòng, hook mạnh nhất trong script) → 5 từ khoá cách nhau dấu phẩy → 3-4
đoạn mô tả (giọng người kể, bám đúng script, không bịa) → 8 mốc chương → lời cảm ơn → hashtag.
**Mốc chương chưa có audio ở bước 1 nên KHÔNG được bịa số phút** — viết placeholder
`[CHƯA CÓ — trích từ voice_paced.srt thật]` kèm 8 câu mở đầu đoạn NGUYÊN VĂN từ script.txt để bước 3
tìm-thay bằng grep/tìm chuỗi (việc cơ học, không cần AI thông minh). File này **chép NGUYÊN VĂN**
sang `listting.txt` khi giao hàng — bước 3 chỉ được điền mốc thời gian thật vào chỗ trống, TUYỆT ĐỐI
không viết lại tiêu đề/mô tả/hashtag.

### B7c — TIÊU ĐỀ + MÔ TẢ BẰNG TOOL `YT-TITLE-RESEARCH` (chốt 2026-09-20, THAY cách viết chay ở B7b)
⭐ **Quy trình đầy đủ của lane này: `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\docs\lanes\satori-jp-obaa.md`** (luật tiêu đề satori,
quyền sở hữu Fable/Opus/Sol, router QC, sheet, lệnh, nhật ký quyết định). Luật tiêu đề nằm ở `config/lanes/satori-jp-obaa.json`
→ lane khác KHÔNG dùng chung, phải có file lane riêng.
Lý do: STT1 viết chay đúng rubric docx chỉ 5 view; SERP JP cùng ngách 620K/399K nhờ cược cụ thể + động từ sự cố + 30–40 ký tự.
```bash
cd E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH
py -3.13 cli.py run   --slug ../h2dev/assets/satori_jp/$SLUG --profile satori-jp-obaa   # ~12 phút, cache từng bước
py -3.13 cli.py view  --slug ../h2dev/assets/satori_jp/$SLUG                            # XEM.html để duyệt (có mục ESCALATE)
py -3.13 cli.py sheet --profile satori-jp-obaa                                          # ghi tiêu đề lên cột E tab Lopezzapa68
```
Tool ghi `TIEU_DE_MO_TA.txt` đúng khuôn B7b (backup `.bak`, giữ Timestamps) + vá `DANG-TAI.txt` 1/2/3/5. Chạy SAU khi script đạt QC.

### B8 — GHÉP VIDEO (ảnh + giọng + phụ đề burn + BGM)
```bash
py -3.13 assemble.py --img ../assets/satori_jp/$SLUG/img --audio ../assets/satori_jp/$SLUG/voice.mp3 --srt ../assets/satori_jp/$SLUG/voice.srt --bgm ../assets/satori_jp/_bgm/bgm1.mp3 --bgm-volume 0.09 --transition xfade --out ../assets/satori_jp/$SLUG/final.mp4 --size 1920x1080
```
→ `final.mp4` (1080p): Ken Burns đa hướng + **SYNC ảnh theo câu (SRT)** + **CROSSFADE mềm** + giọng + phụ đề Nhật burn + nhạc nền. **Đăng được luôn — KHÔNG cần CapCut** (assemble.py đã thay vai trò dựng tay của CapCut). Dùng `--transition fade` nếu muốn dip-to-black, `cut` nếu cắt cứng.
> ⚠️ assemble lần đầu đôi khi lỗi transient ở bước mux (exit 1 sau khi render hết clip) → chạy LẠI y lệnh là xong.

### B9 — QC VIDEO CUỐI (bắt buộc, verify 2026-09-08)
Trích ~4 khung từ final.mp4 rồi XEM (kiểm phụ đề burn + ẢNH CÓ KHỚP LỜI + mặt nhất quán):
```bash
FF=$(py -3.13 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
for t in 00:00:18 00:08:30 00:15:30 00:24:30; do "$FF" -ss $t -i ../assets/satori_jp/$SLUG/final.mp4 -frames:v 1 -y qc_$t.png; done
```
Lỗi hay gặp: **ảnh trôi lệch lời ở giữa video** nếu mật độ ảnh không đều (xem §DONG BO ở skill youtube-image-prompts).

## §PHÂN TÍCH KÊNH TRƯỚC KHI LÀM (user chốt 2026-09-08) ⭐
Khi anh đưa 1 kênh tham khảo, **KHÔNG bốc đại 1 video**. Làm theo skill **`youtube-series-builder`**:
1. **TÓM TẮT TOÀN BỘ video trong kênh** (`yt-dlp` full title+view → ghi UTF-8; bóc mở đầu vài video kiểm người kể).
2. **PHÂN LOẠI kênh LIÊN TỤC hay RỜI RẠC** (mấu chốt — quyết định cách làm):
   - **RỜI RẠC** = mỗi video 1 người kể/chuyên gia KHÁC nhau, không đánh số tập, không nhân vật lặp, không mạch
     thời gian (kênh chủ đề). → **LÀM VIDEO ĐỘC LẬP**: mỗi video 1 nhân vật kể RIÊNG đúng giới/tuổi/nghề chuyện
     gốc; **nhất quán mặt TRONG từng video bằng REF-LOCK** (B5.0). KHÔNG ép tham chiếu chéo. (Tuỳ chọn: gom
     playlist theo cụm; host chỉ ở intro/outro nếu muốn nhận diện.)
   - **LIÊN TỤC** = cùng 1 nhân vật kể xuyên suốt / có mạch thời gian / đánh số tập. → **LÀM THEO THỨ TỰ dòng
     sự kiện**: 1 HOST xuyên suốt, **cùng 1 ảnh master REF-LOCK qua MỌI tập** (mặt giống nhau cả chuỗi), tham
     chiếu chéo THẬT (前回/次は), lặp nhân vật/kỷ vật.
3. **Chỉ khi LIÊN TỤC mới đưa vào channels.json + series bible**; khi RỜI RẠC thì mỗi video độc lập, vẫn REF-LOCK.
→ **simbot2 = RỜI RẠC** (21 video, 4 nguồn đã bóc = 4 người kể khác nhau: giám đốc NH / cụ bà 74 / giám đốc
tang lễ nam / bà thợ giặt). Đã chốt **Mô hình A = video độc lập** (2026-09-08). 3 cụm: 💰tiền(9) · ⚰️viện/tang(6)
· 👥quan hệ(5) — chi tiết `scratchpad/simbot2_catalog.txt`.
⚠️ 4 EP 静子 làm trước đây = **series ÉP GƯỢNG + không REF-LOCK** → coi là NHÁP, làm lại theo mô hình độc lập.
`docs/SERIES_shizuko_shukatsu.md` = DEPRECATED (chỉ giữ tham chiếu cách viết chéo cho trường hợp kênh LIÊN TỤC sau).

## CHI PHÍ / VIDEO (~23')
Giọng ~9.360 credit ($0.047) + Ảnh ~80-120×50đ (~4.000-6.000đ) + BGM 3.600 credit ($0.018, tái dùng ≈0) →
**~5.600đ (~$0.22)/video**. Gói $5 ai33 ≈ 77-107 video (voice+BGM).

## PITFALLS (đã dính — đừng lặp)
- TTS CJK: PHẢI Python requests (đã trong openspeaker_tts), KHÔNG curl -F (mangle UTF-8 câm lặng).
- `--rate` edge: dạng `--rate=-8%` (có `=`). gpti2/ffmpeg path Windows: bash dùng `/`.
- gpti2 low = đủ đẹp; content-policy chặn trẻ nhỏ. Thumbnail: chữ Nhật PIL (gpti2 không render chữ chuẩn).
- Suno endpoint = `/v1s/task/music-generation` (chữ `v1s`).
- Ảnh phải khớp SỐ prompt vs img cũ: nếu đổi img_prompts thì XOÁ img/ cũ trước khi gen (resume theo index).

## NHÂN BẢN SANG HÀN QUỐC (khi Nhật ra kết quả)
Copy 3 skill `*-satori-jp`→`*-satori-kr` (đổi tiếng Hàn + người Hàn 한옥/아파트 + thumbnail chữ Hàn). Tool giữ
nguyên: `fetch_script.py --lang ko` (nguồn), `tts.py --voice <ko-voice ai33>` hoặc `ko-KR-InJoonNeural` (edge).

## VIDEO MẪU ĐÃ LÀM (tham chiếu) — series **静子の終活ノート** (1 HOST cụ bà Shizuko, xem `docs/SERIES_shizuko_shukatsu.md`):
- `yokin-tozetsu/` EP1 相続/口座凍結 (nguồn 704k), 22:47, 79 ảnh (giọng Enishi — nên đổi sang ado cho khớp series).
- `roujin-home/` EP2 老人ホーム, 21:22, 62 ảnh, giọng Shizuko (ado med).
- `ep3-sougi/` EP3 葬式はするな (con gái sơ sinh, mộ 49 năm), 29:58, 67 ảnh, thumb cụ ông quét mộ.
- `ep4-tabidachi/` EP4 最期・6つの合図 (finale, nối EP1), 34:12, 74 ảnh, thumb nồi そうめん hồi quang.
- `saigo-no-bento/` = demo tự nghĩ trước đó (không thuộc series).
