# QUY TRÌNH BƯỚC 1 — LANE SATORI-JP-OBAA (toàn diện, để bên ngoài đọc & tối ưu)

> Viết cho: bên thứ ba (người/AI khác) đọc để đánh giá và đề xuất tối ưu quy trình sản xuất.
> Ngày viết: 2026-09-18. Phạm vi: lane `satori-jp-obaa` (clone kênh Hàn Quốc `simbot2` sang tiếng
> Nhật, kể chuyện người già). Tài liệu này mô tả ĐÚNG những gì đang chạy thật, không phải thiết kế lý
> tưởng — số liệu/model lấy trực tiếp từ code (`E:\CLAUDE\YOUTUBE\h2dev\pipeline\`) tại thời điểm viết.

---

## 1. Bối cảnh: 3 bước của cả dây chuyền, "bước 1" là gì

Một video hoàn chỉnh đi qua 3 bước, do 3 "vai" khác nhau đảm nhận:

| Bước | Ai làm | Việc | Đặc điểm |
|---|---|---|---|
| **1 — ĐẦU NÃO** | **Claude (Opus/Sonnet)** — chủ đề của tài liệu này | Viết kịch bản, thiết kế nhân vật, viết prompt ảnh, phân loại tư liệu, viết tiêu đề/mô tả, kiểm nghiệm thu nội dung | Cần HIỂU nội dung — không giao được cho model rẻ |
| **2 — VẼ ẢNH** | Con người vận hành máy thứ 2 (thao tác Google Flow bằng tay) | Sinh ảnh AI hàng loạt theo prompt đã có sẵn | Thuần thao tác, không sáng tạo nội dung |
| **3 — GHÉP VIDEO** | Agent khác (Hermes/DeepSeek — model rẻ hơn) | Ghép ảnh+giọng+phụ đề thành file video cuối, đóng gói giao hàng | Thuần cơ học, KHÔNG hiểu nội dung |

**Nguyên tắc cứng chi phối toàn bộ thiết kế bước 1** (đúc kết sau nhiều sự cố thật, xem mục 8):
mọi thứ đòi hỏi HIỂU NỘI DUNG hay óc thẩm mỹ (kịch bản, tên nhân vật, việc gán ảnh vào đúng đoạn
truyện, tiêu đề, mô tả, mốc chương, chữ thumbnail...) phải làm XONG và ĐỂ LẠI THÀNH FILE ở bước 1.
Bước 2/3 chỉ được giao việc dạng "làm theo file có sẵn" — không được kỳ vọng chúng tự suy luận nội
dung, vì cả hai đều dùng model rẻ/thao tác tay, không đọc hiểu được truyện.

---

## 2. Hai biến thể pipeline bước 1 đang tồn tại song song

Đây là điểm ĐẦU TIÊN cần bên tối ưu lưu ý: lane này hiện có **2 cách vận hành bước 1 khác nhau**,
chưa hợp nhất.

### Biến thể A — "não ramcloud" (thủ công, runbook `docs/SOP_SATORI_JP.md`)
Claude (phiên chat tương tác, người vận hành gõ lệnh xác nhận từng bước) tự tay chạy từng lệnh CLI
theo trình tự B1→B9 (mục 3 dưới đây), tự đọc kết quả QC, tự quyết định sửa gì trước khi sang bước
kế. Đây là quy trình đã dùng để làm tập STT2, STT3, STT5, STT8, STT21 (đều là tập "hybrid" — xem
mục 5) trong phiên làm việc gần nhất.

### Biến thể B — "não Claude" tự động hoá (runbook `docs/SOP_CLONE_BRAIN.md`)
`pipeline/brain_channel.py` gọi `claude -p --model opus` chạy **headless** (không cần người ngồi
xem từng bước) để tự viết toàn bộ script + prompt ảnh + thumbnail, đi qua 4 cổng tự động
(`gate_check.py`, `qc_tien.py`, `qc_script.py`, `qc_claude.py`) rồi mới dừng chờ duyệt. Sau đó
`pipeline/render_engine.py` tự làm nốt bước 2 (gọi API vẽ ảnh) + bước 3 (ghép video) trong 1 lệnh.
Đã chạy thật 8 lượt trên kênh simbot2 (chốt 2026-09-11).

**Khác biệt cốt lõi:** biến thể A có người xem/quyết định giữa mỗi bước (chậm hơn, linh hoạt sửa
tại chỗ khi phát hiện lỗi lạ); biến thể B chạy 1 mạch không người giám sát giữa chừng (nhanh hơn,
nhưng phụ thuộc hoàn toàn vào 4 cổng tự động có bắt được lỗi hay không). Tài liệu này mô tả CHI TIẾT
biến thể A ở mục 3 (vì đó là quy trình vừa chạy thật gần nhất, có đầy đủ bằng chứng số liệu); biến
thể B tóm tắt ở mục 6.

---

## 3. Biến thể A — quy trình 9 bước + hàng ngang song song (hybrid stock)

Mỗi bước ghi rõ: **Input → Ai/model thực hiện → Output → Cổng QC ngay sau (model QC, tiêu chí ĐẠT)**.

### B1 — Chọn chủ đề
- Input: kênh nguồn `@simbot2` (YouTube, tiếng Hàn) hoặc `docs/channel_dna/simbot2/` (đã phân tích sẵn).
- Thực hiện: `yt-dlp` liệt kê danh sách + view (thuần lấy dữ liệu, KHÔNG model) → Claude đọc, chọn video theo view cao + gần đây.
- Output: 1 `video_id`.
- QC: không có cổng riêng (chọn sai chỉ tốn công B2, phát hiện được ngay khi đọc transcript).

### B2 — Bóc kịch bản đối thủ
- Input: `video_id`.
- Thực hiện: `fetch_script.py` — 3 tầng dự phòng thuần kỹ thuật (YouTube timedtext API → yt-dlp auto-subs → Whisper nghe lại nếu cả hai bị chặn). KHÔNG dùng LLM ở bước này.
- Output: `competitor.txt` (transcript tiếng Hàn) + sidecar `competitor.segments.json` (từ 2026-09-18, `fetch_script.py` luôn ghi).
- QC: Claude đọc để nắm cốt truyện/nhân vật/twist.
- **Cổng B2Q (mới 2026-09-18, KHÔNG LLM):** `py -3.13 qc_transcript.py --slug <tập>` — đo transcript cụt/lặp từ sidecar. PASS; WARN (coverage 80-92%, gap>45s, cpm<120, không có thời lượng) đi tiếp; FAIL (coverage<80%, duplicate>15%, transcript rỗng, sidecar hỏng) dừng; **SKIPPED** (không có sidecar) chỉ được đi tiếp với tập bóc TRƯỚC 2026-09-18 — tập mới mà SKIPPED = fetch không ghi sidecar, lỗi pipeline. Đo thật Kmxva85WKec: nguồn api, 694 đoạn, coverage 1.0, cpm 341.9, PASS.

### B3 — Viết kịch bản tiếng Nhật (70/30)
- Input: `competitor.txt` + hồ sơ giọng/độ dài của kênh (`pipeline/profiles/satori-jp-obaa.json`).
- Thực hiện: **Claude (Opus/Sonnet, chính là model đang chạy phiên này)** viết trực tiếp theo skill `youtube-script` — giữ 70% cấu trúc gốc + 30% sáng tạo, Nhật hoá 100% (luật thừa kế/介護/年金 đúng luật Nhật), tính độ dài bằng char-rate đo thật (309 chữ/phút cho giọng `ado`+`age med`).
- Output: `script.txt` (pure prose, voiceover-ready).
- **Cổng B3Q — 2 TẦNG:**
  | Tầng | Công cụ | Model | Đo gì | Ngưỡng ĐẠT |
  |---|---|---|---|---|
  | 1 (máy) | `qc_script.py` phần A | không có LLM | sót chữ tiếng Hàn/Latin, câu trùng lặp, mâu thuẫn tuổi/số, đoạn quá dài/ngắn | 0 lỗi máy móc |
  | 1 (LLM) | `qc_script.py` phần B | **gemini-3.8-flash** (qua proxy ramclouds, dự phòng ns24) | bảng dữ kiện nhân vật, 伏線 gieo↔trả, đoạn trùng ý, dấu vết văn hoá nguồn, mạch nối, so nhịp sự kiện với bản gốc | JSON schema cứng, 0 lỗi chặn |
  | 2 (giám khảo độc lập) | `qc_claude.py` | **`claude -p --model opus`, PHIÊN MỚI HOÀN TOÀN** (không thấy lịch sử phiên viết) | sai sự thật, dấu vết bản gốc còn sót, mâu thuẫn logic tầng 1 bỏ sót | góp ý không chặn nếu nhẹ; lỗi thật thì chặn |
  - Nếu rớt: **sửa tại chỗ** đúng câu bị nêu tên (không viết lại từ đầu), chạy lại CẢ HAI tầng.
  - Rớt lặp lại ở CÙNG một chỗ ≥3 lượt/nhiều model khác nhau → dừng vòng lặp tự động, đổi sang sửa tay trực tiếp (bài học: từng lặp 73 phút + tốn quota mà không hội tụ).

### B4 — Giọng đọc (TTS) + đồng bộ phụ đề
- Input: `script.txt`.
- Thực hiện: **OpenSpeaker/ai33.pro** (proxy giọng ElevenLabs, KHÔNG phải LLM) qua `tts.py --provider openspeaker --profile satori-jp-obaa` → giọng `ado`, làm già `age med`, tốc độ 0.92.
- Output: `voice.mp3` + `voice.srt` (do server STT nghe lại tạo, có thể sai đồng âm).
- **B4.1 (bắt buộc, cơ học, không LLM):** `srt_from_script.py` — dùng `difflib` khớp lại từng chữ SRT với `script.txt` gốc (SRT hay nghe nhầm đồng âm dù giọng đọc đúng).
- **B4.2 (bắt buộc, cơ học, không LLM):** `pace_audio.py` — cắt audio tại ranh câu + chèn khoảng lặng (câu 0,65s/giữa câu 0,20s/hết đoạn 1,5s) vì giọng người già cần nghỉ rõ. Output: `voice_paced.wav` + `voice_paced.srt`.
- **Cổng B4Q:** `qc_audio.py` (thuần phân tích sóng âm bằng ffmpeg/numpy, KHÔNG LLM) — đo `pause_misplaced` (nghỉ sai chỗ), `dropouts` (đứt tiếng), `srt_drift`. ĐẠT khi cả 3 chỉ số bằng 0/rất nhỏ.

### B5 — Thiết kế nhân vật + prompt ảnh + sinh ảnh
- **B5.0-BIBLE:** Claude viết `characters.json` (tuổi/ngoại hình/tính cách + toán tuổi quan hệ hợp lý: con = cha mẹ − 25..35 tuổi).
- **B5.0 REF-LOCK — sinh ảnh master:**
  - Sinh: `gen_images.py --prompts master.txt --out _ref` — gọi **gpti2** (GPT-image-2 qua proxy gpti2.store, KHÔNG phải LLM văn bản, là model ảnh).
  - QC: `qc_character.py` — **gemini-3.8-flash + grok-4.6** (lấy trung bình 2 model) ước lượng tuổi/giới nhìn thấy trên ảnh, so với tuổi thiết kế trong `characters.json`. FLAG nếu lệch >±12 tuổi/sai giới/chênh tuổi quan hệ vô lý.
- **Viết `img_prompts.txt`:** Claude viết trực tiếp theo skill `youtube-image-prompts` (~1 ảnh/6-7 giây kịch bản, ~280-300 ảnh/video 25-31 phút), đánh marker `@REF`/`@REF2` (khoá mặt nhân vật) hoặc `@GROK` (cảnh trẻ em — gpti2 chặn tuyệt đối nội dung trẻ em, phải route sang Grok Imagine).
- **Sinh ảnh hàng loạt:** `gen_images.py` — **gpti2** (ảnh `@REF`/`@REF2` khoá mặt, ~110đ/ảnh) hoặc **Grok Imagine** (`@GROK`, ~free) hoặc text-only (~50đ/ảnh).
- **Cổng B5Q:** `qc_visual.py images` — **gemini-3.8-flash** vision, lấy mẫu 20 ảnh kiểm hỏng/đen/trùng.

### B5.5 — Gán ảnh vào đúng đoạn truyện (`img_doan.txt`)
- Input: `script.txt` (đã chia N đoạn cách nhau dòng trống) + `img_prompts.txt` (M dòng, M > N).
- Thực hiện: **BẮT BUỘC Claude đọc nội dung** từng ảnh + từng đoạn, tự gán số đoạn cho từng ảnh (giữ thứ tự không giảm). ⚠️ **KHÔNG được sinh bằng thuật toán chia đều cơ học** (đo được sự cố thật: 1 tập bị sinh bằng công thức chia đều luân phiên 2-3 ảnh/đoạn, không đọc nội dung — gây "ảnh lệch lời" hàng loạt, phát hiện qua QC video ở B8Q).
- Output: `img_doan.txt` (`NNN.png|<số đoạn>`).
- Cổng: `sinh_neo.py --slug <tập>` (thuần thuật toán, KHÔNG LLM) — dò trong `voice_paced.srt` để tìm câu neo THẬT cho từng ảnh, báo lỗi nếu 1 đoạn có quá nhiều ảnh mà không đủ câu để trải ra (ép phải rải lại sang đoạn lân cận). Output: `anchors.txt`.
- **Stamp fingerprint (mới 2026-09-18, ngay sau khi viết xong `img_prompts.txt` + `img_doan.txt`):** `py -3.13 gate_common.py --slug <tập> --stamp` → `artifact_meta.json` (sha256 script ↔ artifact). Script sửa sau đó = **STALE, chặn cứng** ở mọi cổng dưới + `hybrid_chuan_bi.py`. Tập cũ chưa stamp: chạy 2 cổng dưới TRƯỚC rồi mới `--stamp` (cấm stamp mù cho tập biết là stale — STT7 script 07:58 mới hơn prompt 07:35).
- **Cổng B5P (mới 2026-09-18) — prompt ↔ story facts:** `py -3.13 qc_prompt_consistency.py --slug <tập>` — **gemini-3.8-flash** (5 lời gọi facts/10 đoạn + 9 batch/15 prompt ≈ 14 lời gọi). FAIL cơ học: số prompt ≠ số dòng img_doan, `@REF/@REF2` thiếu nhân vật, prompt rỗng, STALE, LLM lỗi hạ tầng. PROMPT_CONFLICT / AMBIGUOUS chỉ WARN (mode warn mặc định); `--mode fail` chỉ dùng hồi quy, CHƯA bật production. Đóng lỗi #4 mục 8.
- **Cổng B5.5-QC / B55 mapping (mới 2026-09-18) — ảnh ↔ đoạn:** `py -3.13 qc_img_doan.py --slug <tập>` — **gemini-3.8-flash** (1 lời gọi/8 đoạn ≈ 7 lời gọi). FAIL cơ học: dòng malformed, ≠ số prompt, thiếu/thừa/trùng ID, đoạn ngoài 1..N, số đoạn giảm theo thứ tự, STALE, thiếu `img_doan.txt`, LLM lỗi hạ tầng. WARN: SUSPICIOUS (chia đều 2,3,2,3 / lệch bất thường — bắt buộc chạy có LLM, `--no-llm` khi SUSPICIOUS = chưa kiểm), semantic ≤2 (mode warn). Đóng lỗi #2 mục 8.
- `would_block` (B5P/B55) = số ca sẽ bị chặn NẾU bật `--mode fail` — đọc `<tập>/logs/<gate>_latest.json → metrics.semantic`; sau 2 tập mới quyết bật.

### B6 — Nhạc nền
- Tái dùng track piano có sẵn (0 model), hoặc gen mới qua Suno API (không phải LLM văn bản, model nhạc).

### B7 — Thumbnail
- Claude viết `thumb_text.txt` (nội dung chữ, hook — cần hiểu script để chọn câu "giật" nhất).
- `thumbnail_text.py` (PIL, thuần cơ học phủ chữ lên ảnh nền — KHÔNG dùng model vẽ chữ vì model ảnh vẽ chữ sai chính tả).
- **Cổng QC thumbnail — 2 lớp độc lập:**
  | Lớp | Công cụ | Model |
  |---|---|---|
  | 1 | (ẩn trong pipeline QC ảnh chung) | gemini-3.8-flash |
  | 2 (mới, 2026-09-17) | `qc_thumbnail_sol.py` | **GPT-5.6-sol** qua proxy nội bộ `9router` (localhost, KHÁC hẳn nhóm gemini/ramclouds) — trả PASS/FIX/REMAKE kèm phê bình tiếng Việt |

### B7b — Tiêu đề + Mô tả đăng tải
- Claude viết trực tiếp `TIEU_DE_MO_TA.txt` (tiêu đề, 5 từ khoá, 3-4 đoạn mô tả, 8 mốc chương, hashtag) — **bắt buộc, không được để trống** (sự cố thật: 2 tập lọt tới người xem với mô tả rỗng vì bước 3 tưởng phải tự viết).
- Nếu chưa có audio thật (`voice_paced.srt`) tại thời điểm này → ghi placeholder + 8 câu mở đầu đoạn NGUYÊN VĂN để bước 3 tìm-thay bằng grep (việc cơ học, không cần model).
- Rào cứng bằng CODE: `brain_channel.py`/`brain_steps.py` coi bước 1 CHƯA xong nếu thiếu file này (áp dụng cho biến thể B; biến thể A do người vận hành tự kiểm tra).

### B8 — Ghép video (chỉ áp dụng tập KHÔNG hybrid)
- `assemble.py` (ffmpeg, thuần cơ học — Ken Burns, sync ảnh theo câu SRT, crossfade, burn phụ đề, mux BGM). KHÔNG LLM.
- **Cổng B8Q:** `qc_visual.py video` — **gemini-3.8-flash** vision, lấy mẫu N khung hình, so ảnh đang chiếu với câu đang đọc tại đúng giây đó (SYNC_SCHEMA) → chấm điểm khớp lời 1-5.

### B9 — QC video cuối (thủ công)
- Claude tự trích ~4 khung hình từ `final.mp4` rồi tự xem trực tiếp (vision của chính Claude, không gọi API riêng) — kiểm phụ đề cháy đúng, ảnh khớp lời, mặt nhân vật nhất quán.

---

## 4. Bảng tổng hợp TẤT CẢ cổng QC (tra nhanh)

| Cổng | Sau bước | Công cụ | Model | Input | Tiêu chí ĐẠT | Khi RỚT |
|---|---|---|---|---|---|---|
| B2Q (mới 2026-09-18) | B2 | `qc_transcript.py` | không (đo cơ học) | competitor.segments.json | coverage ≥92%, gap ≤45s, dup ≤15%; WARN đi tiếp; SKIPPED chỉ hợp lệ tập bóc trước 2026-09-18 | FAIL → bóc lại transcript (đổi tầng api/yt-dlp/whisper), không viết script |
| B3Q tầng 1-máy | B3 | `qc_script.py` phần A | không | script.txt | 0 lỗi máy móc (chữ nguồn/trùng lặp/mâu thuẫn số) | Sửa tại chỗ |
| B3Q tầng 1-LLM | B3 | `qc_script.py` phần B | gemini-3.8-flash | script.txt + competitor.txt | JSON schema, 0 lỗi chặn | Sửa tại chỗ, chạy lại |
| ~~B3Q tầng 2~~ (BỎ 2026-09-18) | B3 | `qc_claude.py` | claude -p opus | — | — | Tắt khi lane có `script.sol_qc` (cùng model chấm nhau vô nghĩa; gây B3Q không hội tụ 116'). Thay bằng B3S |
| **B3S** (mới 2026-09-18, chuẩn từ STT10) | B3 (sau B3Q) | `qc_script_sol.py` (flow B: `brain_channel.check_b3s`) | **GPT-5.6-sol** (9router, lens `story`, 1 call cả tập, 2,7') | script.txt + tiêu đề (dòng đầu dan_y.txt / TIEU_DE_MO_TA.txt) | PASS; FIX → Claude sửa CHỈ mục SAI → sol chấm lại 1 lần, FIX nhẹ vẫn qua; REMAKE → Claude kiểm từng lỗi, sửa, tự chấm `logs/B3S_claude_verdict.txt` | `SAI LỖI KỊCH BẢN KHÔNG SỬA ĐƯỢC` → ESCALATION_REPORT.md, người quyết lại cốt truyện. Resume: sha256 script trùng `logs/B3S_latest.json` → bỏ qua |
| B4Q | B4 | `qc_audio.py` + `qc_visual.py voice` | không (sóng âm) + gemini-3.8-flash (SRT coverage) | voice_paced.wav/srt | 0 nghỉ sai chỗ, 0 đứt tiếng, SRT phủ ≥85% | Chạy lại pace_audio với tham số khác |
| B5.0 (master) | B5 | `qc_character.py` | gemini-3.8-flash + grok-4.6 | ảnh master _ref/*.png | lệch tuổi ≤±12, đúng giới | Sửa prompt master, gen lại |
| B5Q | B5 | `qc_visual.py images` | gemini-3.8-flash | mẫu 20 ảnh | 0 hỏng/đen/trùng | Gen lại ảnh lỗi |
| B5P (mới 2026-09-18) | B5 (sau `gate_common.py --stamp`) | `qc_prompt_consistency.py` | gemini-3.8-flash (≈14 lời gọi) | script.txt + img_prompts.txt + img_doan.txt + characters.json | 0 lỗi cơ học (≠ số dòng, @REF thiếu nhân vật, prompt rỗng, STALE); PROMPT_CONFLICT/AMBIGUOUS = WARN (mode warn) | Cơ học/STALE → sửa prompt rồi `--stamp` lại; conflict → sửa prompt bị nêu, đọc `logs/B5P_latest.json` |
| B55 mapping (mới 2026-09-18) | B5.5 | `qc_img_doan.py` | gemini-3.8-flash (≈7 lời gọi) | img_doan.txt + script.txt + img_prompts.txt | 0 lỗi cơ học (malformed/≠ số prompt/thiếu-trùng ID/ngoài 1..N/giảm thứ tự/STALE); SUSPICIOUS + semantic ≤2 = WARN (mode warn) | Cơ học → sửa `img_doan.txt`; semantic → gán lại theo `better_doan` trong `logs/B55_mapping_latest.json` |
| (mới) img_doan | B5.5 | `sinh_neo.py` | không (thuật toán) | img_doan.txt + voice_paced.srt | mọi ảnh tìm được câu neo thật, ≥1.0s/ảnh | Rải lại ảnh sang đoạn lân cận |
| Thumbnail lớp 1 | B7 | (trong QC ảnh chung) | gemini-3.8-flash | thumbnail_final.png | không lỗi hiển thị | Sửa ảnh nền/chữ |
| Thumbnail lớp 2 | B7 | `qc_thumbnail_sol.py` | **GPT-5.6-sol** (proxy 9router riêng) | thumbnail_final.png + tiêu đề | PASS (không FIX/REMAKE) | Sửa chữ/nội dung, chạy lại tới khi PASS |
| B8Q | B8 | `qc_visual.py video` | gemini-3.8-flash | final.mp4 + voice_paced.srt | 0 khung đen, ảnh khớp lời, phụ đề đúng | Sửa img_doan.txt/anchors rồi ghép lại |
| B9 | B8 | Claude tự xem khung hình | Claude (vision trực tiếp, không gọi API riêng) | 4 khung final.mp4 | không phát hiện lỗi bằng mắt | Sửa điểm cụ thể |

**Nhận xét cho bên tối ưu:** gemini-3.8-flash gần như ĐỘC QUYỀN cho mọi cổng QC nội dung/hình ảnh
(6/9 cổng) — điểm rủi ro tập trung (1 model lỗi/bị chặn = nhiều cổng cùng nghẽn). 2 cổng dùng model
KHÁC hẳn để tránh trùng điểm mù: `qc_script_sol.py` (B3S, GPT-5.6-sol cho script — thay `qc_claude.py`
từ 2026-09-18) và `qc_thumbnail_sol.py` (GPT-5.6-sol cho thumbnail).

**Quy trình QC bước 1 CHUẨN (12 mốc, chứng nhận STT9 2026-09-18) — bản đầy đủ ở
`docs/SOP_CLONE_BRAIN.md` § "QUY TRÌNH QC BƯỚC 1 CHUẨN LANE SATORI"**; mọi tập từ STT10 theo đó, không
theo bảng cũ ở trên khi hai bản lệch nhau.

---

## 5. Rẽ nhánh riêng: tập "hybrid" (ảnh AI xen clip stock thật)

Một số tập dùng **stock footage thật** (Pexels) cho các cảnh không cần khuôn mặt nhân vật (giấy tờ,
nhà cửa, đồ vật) để giảm số ảnh AI cần vẽ. Nhánh này thêm các bước sau B5, TRƯỚC B5.5:

| Bước | Công cụ | Model | Việc |
|---|---|---|---|
| Phân loại dòng nào AI/STOCK | `phan_loai_stock.py` | **deepseek-v4-flash** (qua ramclouds) | Đọc từng dòng `img_prompts.txt`, quyết định AI (cần mặt người) hay STOCK (cảnh chung chung) |
| Tải clip/ảnh thật | `stock_fetch.py` | không (gọi API Pexels/Wikimedia Commons) | Tải file thật theo search query |
| Nghiệm thu tư liệu | `audit_stock.py` | **gemini-3.8-flash** vision | Loại clip có MẶT NGƯỜI RÕ hoặc CHỮ/LOGO to; giữ lại 1-3 khung/clip để chấm |
| **Hoàn thiện bước 1 hybrid (1 lệnh)** | `hybrid_chuan_bi.py` | gpti2 (cho phần vẽ bù) | Tự động: (a) dòng STOCK bị `audit_stock.py` loại → đổi nhóm `AI_FALLBACK` + tự vẽ bù bằng gpti2 (không cần hỏi lại, ~50-110đ/ảnh); (b) copy ảnh nhóm AI từ kết quả máy 2 vào `img/`; (c) chạy lại toàn bộ chuỗi B4→B4Q; (d) chạy `sinh_neo.py` ra `anchors.txt`. Dừng thật chỉ ở 2 trường hợp: máy 2 chưa trả đủ ảnh, hoặc B4Q rớt. |

**Luật cứng đã rút ra (từng sai thật rồi sửa):** với tập hybrid, số ảnh trong `img/` PHẢI bằng đúng
(tổng dòng − dòng STOCK thật OK) — thiếu đúng bằng số dòng STOCK là ĐÚNG THIẾT KẾ (bước 3 dùng clip
video thật ở đó), thiếu NHIỀU hơn thế là bước 1 làm chưa xong, TUYỆT ĐỐI không được trích khung tĩnh
từ clip stock nhét bù vào `img/` (làm mất tác dụng "clip có chuyển động thật" và có thể khiến bước 3
tưởng nhầm là tập không-hybrid).

Với tập hybrid, **bước 3 (ghép video) do agent khác đảm nhận riêng** (không dùng `assemble.py`
chung) — thuật toán ghép được giao qua văn bản đặc tả tự chứa (`docs/GIAO_VIEC_HYBRID_COMPOSITOR.md`),
Claude Code không tự ghép, chỉ bàn giao input đầy đủ + đọc báo cáo QC video của bước 3 gửi lại rồi
sửa tiếp dữ liệu bước 1 nếu cần (xem sự cố thật ở mục 8, mục 3).

---

## 6. Biến thể B — "não Claude" tự động hoá (tóm tắt)

`brain_channel.py --channel <url> --profile satori-jp-obaa` → chọn video → gọi `claude -p --model
opus` (headless, không cần người ngồi canh) theo **2 PHA** (P0, 2026-09-18 — thay lượt viết 1 lần cũ):
**pha SCRIPT** (`phase="script"`, chỉ khi thiếu `script.txt`) → cổng số → B3Q hội tụ → **pha ASSETS**
(`phase="assets"`, chỉ khi thiếu asset, ≤2 lượt, cấm sửa script) ra `characters.json + img_prompts.txt +
img_doan.txt + thumb_text.txt + TIEU_DE_MO_TA.txt`. Thứ tự đầy đủ: `competitor.txt → B2Q → pha SCRIPT → cổng số →
B3Q (≤3 vòng, không hội tụ → ESCALATION_REPORT.md) → pha ASSETS → stamp fingerprint artifact_meta.json → STALE-check →
REF-LOCK → B5P → B55 mapping → ⏸ dừng trước render → giao máy 2 (ảnh) → Hermes (ghép)`. Các cổng tự động trong luồng:

| Cổng | Đo gì | Model |
|---|---|---|
| `qc_transcript.py` (B2Q, mới) | transcript đối thủ cụt/lặp; SKIPPED chỉ hợp lệ tập bóc trước 2026-09-18 | không (đo cơ học) |
| `gate_check.py` | độ dài, phẩy/câu, chữ/nhịp thở, %hội thoại | không (đo cơ học) |
| `qc_tien.py` | số tiền có đúng là quy đổi của bản gốc (tránh AI tự bịa số) | không rõ, cần tra thêm mã nguồn nếu bên tối ưu cần chi tiết |
| `qc_script.py` tầng 1 | như mục 4 | gemini-3.8-flash |
| `qc_claude.py` tầng 2 | như mục 4 | claude -p opus phiên mới |
| `gate_common.kiem_stale` (STALE, mới) | sha256 script ≠ lúc sinh img_prompts/img_doan → chặn cứng | không |
| `qc_prompt_consistency.py` (B5P, mới) | như mục 4 — mode warn | gemini-3.8-flash |
| `qc_img_doan.py` (B55 mapping, mới) | như mục 4 — mode warn | gemini-3.8-flash |

Sau khi các cổng ĐẠT/WARN, dừng lại chờ duyệt (`stop_before_render=True` — production LUÔN dừng ở đây; nhánh
`render_engine.py` cuối hàm chỉ cho test/tập non-hybrid cũ) — **0 đồng tốn ngoài ~150-330đ ảnh master** vì chưa
TTS/chưa vẽ loạt. Handoff thật = máy 2 vẽ ảnh → Hermes ghép. `render_engine.py` (gộp bước 2+3 vào 1 lệnh, 12 bước con
B4→B10, xem `docs/QUY_TRINH_RENDER_VIDEO.md`) không còn là đường production.

**Số đo thật 2026-09-18 (tập STT3 `simbot2-03-Kmxva85WKec`, 128 prompt / 50 đoạn):**
- B55 mapping: 7 lời gọi, tok_in 20.077 / tok_out 4.883, 86s (bản gán tay: WARN 16/128, would_block 16); bản lỗi 2-3-2-3 `--mode fail`: FAIL 108/125, 6/6 ảnh mục tiêu bị bắt, 110s.
- B5P: 14 lời gọi (5 facts + 9 batch), tok_in ≈39-40k / tok_out ≈10.8k, 190-235s; hồi quy prompt cũ 5/5 (022/028/112/113/114) ở cả 3 run; bản sửa 4/5 sạch, 113 flag 1/3 run có lý do; 8 lỗi prompt thật mới phát hiện (002/027/074/081/082/111/118/125).
- Flow B smoke (bản copy STT3, `stop_before_render=True`): 23,7 phút (B3Q tầng 2 12,1'; B5P 7,2'; mapping 3,4'; 21 lời gọi LLM), 0 ✗, không gọi `claude -p` viết.
- B2Q trên Kmxva85WKec: nguồn api, 694 đoạn, coverage 1.0, cpm 341.9, PASS.
- Chi phí thêm/tập ≈10,6 phút + 21 lời gọi gemini-3.8-flash.

---

## 7. Bảng model/dịch vụ dùng trong TOÀN BỘ bước 1 (tra cứu nhanh)

| Model/dịch vụ | Vai trò | Dùng ở bước |
|---|---|---|
| **Claude (Opus/Sonnet)** — chạy trong phiên tương tác HOẶC headless `claude -p` | Viết nội dung (script, prompt ảnh, tiêu đề/mô tả, gán ảnh vào đoạn), ra quyết định sửa lỗi | B3, B5, B5.5, B7, B7b + toàn bộ quyết định điều phối |
| **gemini-3.8-flash** (qua proxy ramclouds, dự phòng ns24) | QC nội dung/hình ảnh giá rẻ | B3Q tầng 1-LLM, B4Q (SRT coverage), B5.0, B5Q, B8Q, thumbnail lớp 1 |
| **grok-4.6** | QC chéo tuổi/giới ảnh master (đối chiếu với gemini) | B5.0 |
| **claude -p --model opus** (phiên hoàn toàn mới) | Giám khảo độc lập tầng 2 cho script | B3Q tầng 2 |
| **deepseek-v4-flash** (qua ramclouds) | Phân loại dòng ảnh AI/STOCK (thuần văn bản) | Phân loại hybrid |
| **GPT-5.6-sol** (qua proxy nội bộ 9router, `cx/gpt-5.6-sol`) | QC thumbnail lớp 2, độc lập hẳn với nhóm gemini | Thumbnail lớp 2 |
| **gpti2** (GPT-image-2, proxy gpti2.store) | Sinh ảnh AI chính (chân dung, cảnh có mặt người) | B5, hybrid AI_FALLBACK |
| **Grok Imagine** (grok-imagine-image-2.0) | Sinh ảnh cảnh có trẻ em (gpti2 chặn tuyệt đối nội dung trẻ em) | B5 (marker `@GROK`) |
| **OpenSpeaker/ai33.pro** (proxy ElevenLabs) | Text-to-speech | B4 |
| **Suno** (qua ai33.pro) | Sinh nhạc nền (tuỳ chọn, thường tái dùng track có sẵn) | B6 |
| **yt-dlp / youtube-transcript-api / Whisper** | Lấy transcript đối thủ (3 tầng dự phòng) | B2 |
| **Pexels API / Wikimedia Commons** | Tải clip/ảnh thật cho tập hybrid | Phân loại hybrid |
| ffmpeg / PIL / difflib (thuần thuật toán, không model) | Ghép video, giãn nhịp audio, overlay chữ thumbnail, sửa SRT, gán neo thời gian | B4.1, B4.2, B5.5 (sinh_neo), B7 (overlay), B8 |

---

## 8. Sự cố thật đã xảy ra + cách đã vá (tham khảo khi tối ưu, đừng lặp lại)

1. **Bỏ qua B3Q rồi mới phát hiện lỗi** (tập "yokin-basho"): làm xong tưởng mượt, không chạy cổng nội
   dung trước → lọt 8 lỗi thật vào video (số năm/tiền mâu thuẫn, dấu vết ngôn ngữ nguồn còn sót,
   xưng hô sai vai vế). Bài học: B3Q phải chạy TRƯỚC khi tiêu tiền giọng+ảnh, không chạy sau.
2. **`img_doan.txt` bị sinh bằng thuật toán chia đều cơ học** (không đọc nội dung): phát hiện qua cổng
   B8Q ở bước 3 báo "ảnh lệch lời" — điều tra ra CẢ FILE (không chỉ vài điểm) bị chia đều luân phiên
   2-3 ảnh/đoạn bất kể đoạn dài ngắn/nội dung gì. Phải đọc lại toàn bộ script + prompt để gán tay lại.
3. **Trích khung tĩnh từ clip stock nhét vào `img/` để "đủ số ảnh"** — sai vì phá thiết kế (chỗ đó
   PHẢI là clip có chuyển động thật cho bước 3 dùng), lại còn dễ khiến bước 3 hiểu nhầm tập không
   phải hybrid. Đã phải xoá và làm lại đúng theo thiết kế (dùng `hybrid_chuan_bi.py`).
4. **Nội dung ảnh mâu thuẫn cốt truyện sót từ khi viết `img_prompts.txt`** — phát hiện muộn (khi đối
   chiếu toàn bộ prompt với script để sửa lỗi #2), không có cổng riêng nào bắt được lỗi "mâu thuẫn
   với chi tiết cốt truyện đã chốt ở đoạn khác" tại thời điểm viết prompt.
5. **`TIEU_DE_MO_TA.txt` bị bỏ trống, tưởng bước 3 tự viết được** — 2 tập lọt tới người xem với mô tả
   rỗng. Đã rào cứng: coi là file bắt buộc của bước 1, không được để bước 2/3 tự sinh nội dung.

**Gợi ý điểm có thể tối ưu (quan sát, không phải kết luận cuối):**
- Gemini-3.8-flash đang gánh 6/9 cổng QC (P0 thêm B5P + B55 cũng dùng gemini-3.8-flash) — có thể là điểm nghẽn/rủi ro tập trung.
- ✅ **ĐÃ LÀM 2026-09-18 (P0):** thứ tự B3Q → B5 — bộ não tách 2 pha (`phase="script"` → B3Q hội tụ → `phase="assets"`),
  prompt/mapping luôn viết trên bản script cuối; script sửa sau đó bị STALE chặn cứng (`artifact_meta.json`). Số đo mục 6.
- ✅ **ĐÃ LÀM 2026-09-18 (P0):** cổng `qc_prompt_consistency.py` (B5P) kiểm "prompt ảnh mâu thuẫn với các đoạn KHÁC của
  script" ngay sau B5 — hồi quy bắt 5/5 lỗi cũ (022/028/112/113/114) + lộ 8 lỗi prompt thật chưa từng biết của STT3. Còn
  WARN-only, chưa bật `--mode fail`.
- Hai biến thể pipeline (A thủ công / B tự động) đang cùng tồn tại cho cùng 1 lane — có thể cân nhắc
  hợp nhất hoặc quy định rõ khi nào dùng biến thể nào (P0 chỉ chuẩn hoá trạng thái cổng qua `gate_common.py`).
- ✅ **ĐÃ LÀM 2026-09-18 (P0), một phần:** `qc_img_doan.py` (B55 mapping) chấm semantic từng ảnh↔đoạn (1 lời gọi/8 đoạn,
  7 lời gọi/tập) + gợi ý `better_doan` — bản 2-3-2-3 cũ bị bắt 108/125, 6/6 ảnh mục tiêu. Việc GÁN vẫn do Claude đọc
  (bắt buộc), tool chỉ kiểm sau; chưa có gợi ý ứng viên trước khi gán.
