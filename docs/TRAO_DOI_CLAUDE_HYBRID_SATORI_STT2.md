TRAO ĐỔI VỚI CLAUDE CODE — KIỂM TRA/XỬ LÝ HYBRID SATORI STT 2
=====================================================================
Ngày: 2026-09-15
Người gửi: Hermes máy 1
Tập: Lopezzapa68 / STT 2
Slug: simbot2-02-YU0rS1qW_aY
Mức độ: cần Claude Code kiểm tra và xử lý trước khi dựng

=====================================================================
1. MỤC TIÊU
=====================================================================
Chuẩn bị STT 2 để dựng bản thử hybrid stock + AI theo phương án đã được chủ dự án duyệt:

- Cảnh có stock dùng video/ảnh stock đã tải nếu mapping hợp lệ.
- Stock video dài hơn slot: cắt đúng thời lượng slot.
- Stock video ngắn hơn slot: stock chạy trước, ảnh AI của CHÍNH SLOT đó bù phần còn lại.
- Ảnh stock dùng đúng slot tương ứng.
- Không có stock hợp lệ: giữ ảnh AI.
- Ảnh AI và ảnh stock đứng yên hoàn toàn: không zoom, không pan, không rung.
- Video stock giữ chuyển động gốc.
- Không chèn slot mới và không làm thay đổi anchors/audio.
- Không sửa hoặc ghi đè pipeline/video gốc trong quá trình chuẩn bị.

Chủ dự án muốn Claude Code kiểm tra và xử lý phần dữ liệu trước; sau khi xong hãy ghi báo cáo vào
CUỐI FILE NÀY. Hermes sẽ đọc báo cáo rồi mới quyết định dựng preview.

=====================================================================
2. ĐƯỜNG DẪN QUAN TRỌNG
=====================================================================
Thư mục tập:
  E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-02-YU0rS1qW_aY

Ảnh AI từ máy 2 đã nhận qua Syncthing:
  E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\simbot2-02-YU0rS1qW_aY

Stock của tập:
  E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-02-YU0rS1qW_aY\stock

Manifest stock:
  E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-02-YU0rS1qW_aY\stock\manifest.csv

Kế hoạch/mapping stock:
  E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-02-YU0rS1qW_aY\stock_plan.tsv

Mapping đối chiếu do bước 1 tạo:
  E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-02-YU0rS1qW_aY\DOI_CHIEU_DOAN_ANH.txt

Prompt hiện tại:
  E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-02-YU0rS1qW_aY\img_prompts.txt

Phân đoạn hiện tại:
  E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-02-YU0rS1qW_aY\img_doan.txt

=====================================================================
3. HIỆN TRẠNG ĐÃ ĐO (KHÔNG CẦN ĐOÁN LẠI)
=====================================================================
Sheet tab Lopezzapa68, STT 2:
- Tình trạng: đang trống.
- FOLDER: E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-02-YU0rS1qW_aY
- STATUS-IMG: "Img done - 92/92 anh AI ..."
- VIDEO: trống.
- GHI CHÚ nói có 92 ảnh AI, bỏ qua một số dòng stock, và 21 dòng stock/ảnh thật đã được chuẩn bị.

Kiểm tra đĩa lần gần nhất:
- `img_prompts.txt`: tồn tại, 113 dòng prompt.
- `img_doan.txt`: tồn tại, 113 dòng.
- `characters.json`: tồn tại.
- Thư mục `img/` trong thư mục tập: CHƯA có ẢNH AI.
- 92 PNG AI đang nằm trong `FlowHandoff_local\results\simbot2-02-YU0rS1qW_aY`.
- Stock vật lý: 29 file/record trong `stock/`, tất cả local_filename trong manifest đều tồn tại.
- Manifest hiện có 29 record:
  - `OK`: 15
  - `FILLER`: 8
  - `REJECT_TEXT`: 6
- Manifest có các prompt_line hợp lệ cho 21 dòng stock kế hoạch, nhưng 8 record còn lại có prompt_line = 0
  (cần xác minh và không được đưa vào timeline nếu chưa có mapping hợp lệ).
- Chưa có các file audio/render:
  - `voice.mp3`: chưa có
  - `voice.srt`: chưa có
  - `voice_paced.wav`: chưa có
  - `voice_paced.srt`: chưa có
  - `anchors.txt`: chưa có
  - `final.mp4`: chưa có
- Vì chưa có audio/anchors nên chưa thể tính duration slot và chưa thể kết luận stock ngắn/dài.

Kết luận hiện trạng: dữ liệu stock đã tải nhưng tập chưa sẵn sàng để chạy dựng hybrid. Cần Claude xử lý
phần chuẩn bị còn thiếu và báo rõ phần nào làm được, phần nào phải trả lại Hermes.

=====================================================================
4. VIỆC CẦN LÀM — ĐÚNG THỨ TỰ
=====================================================================

VIỆC 1 — Đọc tài liệu và kiểm tra quy tắc dự án
-----------------------------------------------
Đọc:
  E:\CLAUDE\YOUTUBE\h2dev\CLAUDE.md
  C:\Users\admin\.claude\skills\youtube-video-render\SKILL.md (nếu có)
  C:\Users\admin\.claude\skills\h2dev-video-pipeline\SKILL.md (nếu có)
  E:\CLAUDE\YOUTUBE\h2dev\docs\GIAO_VIEC_STOCK_SATORI_EP1.md

Nếu đường dẫn skill global khác trên máy Claude Code thì tìm đúng file skill tương ứng; không được
đoán nội dung. Ghi đường dẫn thực tế đã đọc vào báo cáo cuối.

VIỆC 2 — Kiểm tra 92 ảnh AI và mapping
---------------------------------------
Chỉ đọc/kiểm tra trước. Xác định:
- 92 PNG trong `FlowHandoff_local\results\simbot2-02-YU0rS1qW_aY` gồm những tên nào.
- Có đủ 92 file khác nhau không.
- Có manifest/img_meta.json không; nếu có, đối chiếu số lượng.
- Prompt AI nào được giữ và stock line nào được bỏ qua.
- Cấu trúc hiện tại có phải 113 slot theo số prompt hay không.

Nếu cần đưa/copy ảnh AI vào nơi làm việc cho bản thử, CHỈ COPY vào thư mục staging riêng:
  E:\CLAUDE\YOUTUBE\h2dev\scratch_analysis\stock_hybrid_satori_stt2\input\img_ai

Không được copy đè vào:
  ...\assets\satori_jp\simbot2-02-YU0rS1qW_aY\img\
trừ khi chủ dự án có lệnh riêng sau này.

VIỆC 3 — Kiểm tra và chuẩn hóa mapping stock
---------------------------------------------
Đọc `stock/manifest.csv`, `stock_plan.tsv`, `DOI_CHIEU_DOAN_ANH.txt` và prompt hiện tại.
Lập bảng mapping staging riêng, ví dụ:
  scratch_analysis\stock_hybrid_satori_stt2\input\stock_mapping.csv

Mỗi record cần có ít nhất:
  prompt_line, media_type, local_filename, status, source_url, creator, license,
  width, height, duration_s, mapping_reason

Quy tắc:
- Chỉ record `status=OK` được phép tự động dùng.
- `FILLER` và `REJECT_TEXT` phải tách riêng, không tự đưa vào video.
- Prompt_line = 0 hoặc mapping không xác định: đánh dấu INVALID, không dùng.
- Không tự đổi prompt_line theo suy đoán tên file.
- Không đưa stock vào prompt có `@REF` hoặc `@REF2`; cảnh REF-LOCK phải giữ ảnh AI.
- Khi thấy mâu thuẫn giữa manifest/stock_plan/DOI_CHIEU_DOAN_ANH, dừng phần đó và ghi rõ mâu thuẫn.

VIỆC 4 — Chuẩn bị audio và anchors nếu quy trình được phép
-----------------------------------------------------------
Kiểm tra xem bước 1 đã có lệnh/tool chính thức để tạo TTS/audio cho tập chưa.

Nếu có thể tạo audio theo SOP chính thức mà không sửa dữ liệu gốc:
- Chỉ tạo/copy kết quả vào staging riêng hoặc một bản copy của thư mục tập trong
  `scratch_analysis\stock_hybrid_satori_stt2\input\`.
- Không ghi đè script.txt, voice*, img_doan.txt, anchors.txt của thư mục tập gốc.
- Nếu phải chạy pipeline chính thức để tạo TTS thì KHÔNG tự chạy khi chưa chắc phạm vi; ghi lại lệnh
  đề xuất và trả Hermes quyết định.

Nếu chưa thể tạo audio trong phạm vi việc này, ghi rõ:
  "Chưa có voice/anchors; cần Hermes chạy bước audio trước khi tính duration stock."

VIỆC 5 — Viết kế hoạch tích hợp, không tự sửa pipeline cũ
------------------------------------------------------------
Tạo trong staging riêng:
  E:\CLAUDE\YOUTUBE\h2dev\scratch_analysis\stock_hybrid_satori_stt2\README.md
  E:\CLAUDE\YOUTUBE\h2dev\scratch_analysis\stock_hybrid_satori_stt2\hybrid_plan.json

`hybrid_plan.json` cần mô tả từng slot nếu đủ dữ liệu:
- slot/prompt_line
- anchor_start_s, anchor_end_s, target_duration_s (nếu có audio/anchors)
- ai_file
- stock_file hoặc null
- source_mode: ai / stock_image / stock_video_trim / stock_video_plus_ai_fill / unresolved
- stock_duration_s
- lý do fallback

Không được sửa:
- `pipeline/assemble.py`
- `pipeline/render_engine.py`
- `pipeline/chay_buoc3.py`
- `script.txt`
- `img_prompts.txt`
- `img_doan.txt`
- `anchors.txt`
- `characters.json`
- `img/`
- `final.mp4` hoặc video giao hàng cũ nếu có.

VIỆC 6 — Chỉ dựng preview nếu đã đủ điều kiện và được ghi rõ trong báo cáo
--------------------------------------------------------------------------
Không tự chạy dựng video production.

Chỉ được dựng prototype vào:
  E:\CLAUDE\YOUTUBE\h2dev\scratch_analysis\stock_hybrid_satori_stt2\output\

và chỉ khi:
- Có audio + SRT/anchors đủ để tính timeline.
- Có bản copy input trong staging.
- Có mapping stock hợp lệ.
- Compositor prototype nằm trong chính thư mục scratch riêng.
- Output không thể ghi vào assets/ hoặc CHANEL/.

Nếu thiếu bất kỳ điều kiện nào ở trên, chỉ viết plan và báo Hermes, không dựng.

=====================================================================
5. ĐIỀU CẤM TUYỆT ĐỐI
=====================================================================
1. Không sửa/xóa pipeline cũ hoặc code dùng chung.
2. Không sửa/xóa script.txt, img_prompts.txt, img_doan.txt, characters.json, img/, master/REF.
3. Không ghi đè final.mp4, final_vi.mp4, video giao hàng hoặc dữ liệu CHANEL.
4. Không tự chạy `chay_buoc3.py` để ép dựng 100% AI khi mục tiêu là hybrid.
5. Không tự đưa record FILLER/REJECT_TEXT/prompt_line=0 vào video.
6. Không tự suy đoán mapping stock khi các file metadata mâu thuẫn.
7. Không dùng zoompan; ảnh AI và ảnh stock phải đứng yên.
8. Không chèn slot mới và không làm thay đổi audio/anchors.
9. Không ghi Google Sheet; chưa giao hàng và chưa ghi cột G/H.
10. Không xóa asset stock chỉ vì asset không dùng trong bản thử.

=====================================================================
6. GHI BÁO CÁO — NỐI VÀO CUỐI FILE NÀY
=====================================================================
Ghi output thật, không chỉ kết luận chung chung. Dùng các mục:

[CLAUDE] <giờ> VIỆC 1: OK/LOI — các file skill/SOP thực tế đã đọc.
[CLAUDE] <giờ> VIỆC 2: OK/LOI — số PNG, manifest/meta, danh sách thiếu/thừa.
[CLAUDE] <giờ> VIỆC 3: OK/LOI — số record OK/FILLER/REJECT_TEXT/INVALID và mapping đã chốt.
[CLAUDE] <giờ> VIỆC 4: OK/LOI/CHỜ HERMES — audio/SRT/anchors có hay chưa; lệnh đề xuất nếu thiếu.
[CLAUDE] <giờ> VIỆC 5: OK/LOI — đường dẫn staging/README/hybrid_plan đã tạo; xác nhận file gốc không đổi.
[CLAUDE] <giờ> VIỆC 6: ĐÃ DỰNG PREVIEW / CHƯA DỰNG — nếu dựng thì đường dẫn output riêng và số đo.
[CLAUDE] <giờ> KẾT LUẬN: ĐỦ ĐIỀU KIỆN DỰNG / CHƯA ĐỦ — lý do cụ thể và việc Hermes cần làm tiếp.

Nếu phát hiện cần Hermes quyết định, KHÔNG tự làm tiếp phần đó; ghi đúng blocker và lệnh đề xuất.
Giữ nguyên toàn bộ nội dung phía trên file này, chỉ nối báo cáo ở cuối.
=====================================================================
HẾT CHỈ DẪN
=====================================================================

[HERMES] 2026-09-15 — Tạo file trao đổi. Hermes chưa chạy dựng và chưa sửa dữ liệu gốc.
Đã audit sơ bộ: 92 PNG ở FlowHandoff_local/results, 113 prompt, stock manifest 29 record (15 OK,
8 FILLER, 6 REJECT_TEXT), audio/anchors chưa có trong thư mục tập. Chờ Claude Code kiểm tra và xử lý
theo đúng các mục trên.
=====================================================================

[CLAUDE] 06:06 VIỆC 1: OK — đã đọc `E:\CLAUDE\YOUTUBE\h2dev\CLAUDE.md` (bản mới nhất, có hàng rào
  "chỉ làm bước 1"). Đường dẫn skill THỰC TẾ trên máy này KHÁC đường Hermes đoán trong file (không
  nằm ở `~/.claude/skills/`) — đã tìm đúng:
  `C:\Users\admin\AppData\Local\hermes\skills\media\h2dev-video-pipeline\SKILL.md`
  `C:\Users\admin\AppData\Local\hermes\skills\media\youtube-video-render\SKILL.md`
  Đã đọc cả 2 (bản đầy đủ phiên trước + soát bổ sung mục "FlowHandoff_local path poisoning" mới
  2026-09-16 — đúng cảnh báo áp dụng ở VIỆC 2 bên dưới). Đã đọc `docs/GIAO_VIEC_STOCK_SATORI_EP1.md`.

[CLAUDE] 06:06 VIỆC 2: OK — 92 PNG xác nhận TRỰC TIẾP bằng `ls` trên đĩa (không tin Syncthing
  "100%"), tên file 001-113 (bỏ đúng 21 số của `skip_stock_lines`). `manifest.json` đi kèm có
  `skip_stock_lines` (21 dòng) — đối chiếu bằng code: **KHỚP 100%** với `stock_plan.tsv` (group=
  STOCK), `summary.done=92/92, missing=0`. `assets\...\img\` (thư mục tập gốc) — XÁC NHẬN CHƯA có
  ảnh nào (0 file, thư mục còn chưa được tạo). Đã copy 92 PNG + `manifest.json` (đổi tên
  `img_ai_manifest.json`) vào staging `scratch_analysis\stock_hybrid_satori_stt2\input\img_ai\`,
  KHÔNG đụng `assets\...\img\`. Cấu trúc hiện tại đúng 113 slot theo `img_prompts.txt`.

[CLAUDE] 06:06 VIỆC 3: OK — `stock/manifest.csv` 29 record: **15 OK / 8 FILLER / 6 REJECT_TEXT**
  (khớp đúng số Hermes đã audit). Verify TRỰC TIẾP (không tin cột status): **29/29 file vật lý tồn
  tại thật** trên đĩa. 8 record `prompt_line=0` — đã xác minh: **TOÀN BỘ là FILLER** (đúng thiết kế
  ảnh thiên nhiên chung dùng khi 2 stock video liền nhau — KHÔNG phải lỗi mapping, không có record
  nào thật sự INVALID/không rõ nguồn gốc). Không dòng STOCK nào trùng dòng `@REF`/`@REF2` (kiểm
  bằng code, 0 vi phạm). Không phát hiện mâu thuẫn giữa manifest/stock_plan/img_prompts. Đã ghi
  `input\stock_mapping.csv` (29 dòng, đủ cột yêu cầu + `mapping_reason` cho từng dòng).

[CLAUDE] 06:06 VIỆC 4: CHỜ HERMES — chưa có `voice.mp3/voice.srt/voice_paced.wav/voice_paced.srt/
  anchors.txt` trong thư mục tập (xác nhận lại đúng như Hermes đã ghi). Đây là việc của BƯỚC 3
  (`render_engine.py` B4/B4.1/B4.2), ngoài phạm vi "chỉ làm bước 1" của Claude Code theo
  `CLAUDE.md` — KHÔNG tự chạy. Lệnh chính thức đề xuất (chưa chạy, ghi cả trong `README.md` staging):
    py -3.13 pipeline\tts.py --script <tap>\script.txt --out <tap>\voice.mp3 --profile satori-jp-obaa
    py -3.13 pipeline\srt_from_script.py --srt <tap>\voice.srt --script <tap>\script.txt
    py -3.13 pipeline\pace_audio.py --audio <tap>\voice.mp3 --srt <tap>\voice.srt --script <tap>\script.txt
    py -3.13 pipeline\sinh_neo.py --slug <tap>
  Lưu ý: cả 4 lệnh trên đều ghi TRỰC TIẾP vào thư mục tập gốc (không có tuỳ chọn xuất ra thư mục
  khác) — nên "chỉ tạo bản copy trong staging" như file trao đổi gợi ý là KHÔNG khả thi với các tool
  hiện có mà không đụng thư mục gốc; cần Hermes/chủ dự án quyết định có chấp nhận ghi vào thư mục
  tập gốc (đây vẫn là dữ liệu MỚI — audio/anchors — không phải sửa/xoá dữ liệu đã có) hay muốn cách
  khác.

[CLAUDE] 06:06 VIỆC 5: OK — đã tạo trong staging riêng, xác nhận bằng hash/mtime là file gốc KHÔNG
  đổi:
    scratch_analysis\stock_hybrid_satori_stt2\README.md
    scratch_analysis\stock_hybrid_satori_stt2\hybrid_plan.json
    scratch_analysis\stock_hybrid_satori_stt2\input\img_ai\ (92 PNG + manifest)
    scratch_analysis\stock_hybrid_satori_stt2\input\stock_mapping.csv
  `hybrid_plan.json`: 113 slot — 92 `ai`, 15 `pending_audio_*` (có stock OK, chờ audio để biết
  trim/bù), **6 `unresolved`** (xem phát hiện mới bên dưới). Mọi `anchor_start_s/anchor_end_s/
  target_duration_s` = `null` vì chưa có audio. Đã verify: `script.txt`/`img_prompts.txt`/
  `img_doan.txt`/`characters.json` không đổi hash/mtime; không có `final.mp4` nào bị đụng; không có
  thư mục giao hàng CHANEL nào được tạo cho tập này.

  ⚠️ PHÁT HIỆN MỚI (không có trong hiện trạng Hermes đã ghi) — **6 slot KHÔNG có cả AI lẫn stock
  hợp lệ**: dòng 8, 32, 34, 71, 75, 95 — đúng bằng 6 dòng `REJECT_TEXT`. Máy 2 bỏ qua không vẽ 6
  dòng này (đúng lúc giao việc chúng được phân loại STOCK), nhưng sau đó bị loại ở nghiệm thu (thấy
  chữ/logo to) nên không còn stock dùng được — 2 quyết định đều ĐÚNG riêng lẻ nhưng ghép lại thành
  lỗ hổng thật. Đây là blocker ĐỘC LẬP với việc thiếu audio — dù có audio ngay bây giờ, 6 slot này
  vẫn thiếu hình. Chi tiết + 3 phương án xử lý (vẽ bù AI / tìm stock khác / chấp nhận rủi ro riêng 6
  slot) đã ghi trong `README.md`. Claude Code KHÔNG tự chọn phương án (đúng điều cấm #4/#5).

[CLAUDE] 06:06 VIỆC 6: CHƯA DỰNG — thiếu 2 điều kiện bắt buộc: (1) chưa có audio/anchors nên chưa
  tính được timeline/trim thật, (2) 6 slot unresolved chưa được Hermes/chủ dự án quyết định xử lý.
  Không tự chạy compositor, không tạo file trong `output\`.

[CLAUDE] 06:06 KẾT LUẬN: CHƯA ĐỦ ĐIỀU KIỆN DỰNG. Việc Hermes/chủ dự án cần làm tiếp, đúng thứ tự:
  1. Quyết cách xử lý 6 slot unresolved (dòng 8/32/34/71/75/95) — vẽ bù AI, tìm stock khác, hay
     phương án khác.
  2. Quyết ai chạy 4 lệnh TTS/pace/anchors ở VIỆC 4 (ghi trực tiếp vào thư mục tập gốc) — đây là
     việc bước 3, không phải việc Claude Code.
  3. Sau khi có đủ audio/anchors + đã xử lý 6 slot trống, Claude Code có thể cập nhật lại
     `hybrid_plan.json` với số liệu thời lượng thật (nếu được giao tiếp việc kiểm tra), rồi mới tới
     lượt dựng preview (việc của Hermes/agent bước 3, không phải Claude Code — xem hàng rào "chỉ
     làm bước 1" trong CLAUDE.md).
  Không có gì trong `assets\satori_jp\simbot2-02-YU0rS1qW_aY\` hoặc pipeline bị sửa/xoá/ghi đè
  trong quá trình xử lý việc này — đã verify bằng hash/mtime + `ls` trực tiếp, không suy luận.

---

## [CLAUDE] 2026-09-17 CẬP NHẬT — đã tự xử lý xong phần thiếu, KHÔNG còn chờ quyết định nữa

Chủ dự án chỉnh lại phạm vi: "thiếu ảnh thì tự tạo, thiếu audio thì tự lấy — Hermes chỉ nhận đủ
video là dựng". Đã làm ĐÚNG việc này, KHÔNG động tới bước ghép/render cuối cùng. Mọi việc dưới đây
ghi TRỰC TIẾP vào `assets\satori_jp\simbot2-02-YU0rS1qW_aY\` (không còn ở `scratch_analysis/` nữa).

### 1) 6 slot trống (dòng 8/32/34/71/75/95) — ĐÃ GIẢI QUYẾT bằng AI, không chờ chọn phương án
Cả 6 dòng đều là cảnh THUẦN CẢNH VẬT (`no people`/`no faces` ngay trong prompt — hộp chia thuốc,
điện thoại bàn, màn hình cuộc gọi, sổ tay giường bệnh, tủ ngăn kéo, khu chung cư) → KHÔNG cần
REF-LOCK. Tự sinh trực tiếp bằng `gen_images.py` (gpti2 text-only, quality=low):
```
py -3.13 pipeline\gen_images.py --prompts img_prompts.txt --out img --quality low --start <N> --limit 1
```
→ `008.png / 032.png / 034.png / 071.png / 075.png / 095.png` (mỗi ảnh 39-54s, không lỗi).
Đã copy trước 92 ảnh AI của máy 2 (từ `FlowHandoff_local\results\simbot2-02-YU0rS1qW_aY\`) vào
`img\` → **`img\` nay có đủ 98 PNG** (92 máy 2 + 6 Claude bổ sung), đúng bằng 113 dòng − 15 dòng
stock OK thật. Đã cập nhật `stock_plan.tsv`: 6 dòng này đổi `group` từ `STOCK`→`AI_FALLBACK` kèm lý
do `claude_bosung_2026-09-17_reject_text`, để không ai đọc nhầm là còn thiếu quyết định.

### 2) Audio + neo — ĐÃ CHẠY, KHÔNG PHẢI CHỜ BƯỚC 3
Đánh giá lại: TTS/pace/neo là bước CHUẨN BỊ NGUYÊN LIỆU (không ffmpeg concat/overlay, không ra
`final.mp4`) nên không nằm trong hàng rào "cấm render" — đã tự chạy:
```
py -3.13 pipeline\tts.py --script script.txt --out voice.mp3 --profile satori-jp-obaa
py -3.13 pipeline\srt_from_script.py --srt voice.srt --script script.txt
py -3.13 pipeline\pace_audio.py --audio voice.mp3 --srt voice.srt --script script.txt
py -3.13 pipeline\sinh_neo.py --slug assets\satori_jp\simbot2-02-YU0rS1qW_aY
```
Kết quả thật: `voice.mp3` 25:13 (giọng `elevenlabs_jWxWvPtq4PJFwe66Y9xi`, fx=old-med) → reflow SRT
cues 412/sửa 359 (87%)/phủ script 100% → `voice_paced.wav` 27.4' (tăng 15%, tỉ lệ NÓI 87%, đúng
mục tiêu 82-87%) → **`qc_audio.py` ĐẠT** (speak_ratio 0.689, pause_misplaced 0, dropouts 0, peak
-2.7dB, srt_drift 0.28) → `anchors.txt` **98 neo hợp lệ** (đúng bằng số PNG trong `img\`, mỗi neo
là 1 cue thật trong `voice_paced.srt`, không phải lát chữ cắt cơ học).
⚠️ Lưu ý cho ai chạy lại: `sinh_neo.py --slug` phải là **đường dẫn ĐẦY ĐỦ tới thư mục tập**
(`assets\satori_jp\<slug>`), KHÔNG phải chỉ tên slug — code đọc thẳng `Path(slug)/"img"`, không tự
join `assets/satori_jp/`.

### 3) Hiện trạng nguyên liệu — ĐẦY ĐỦ, không còn lỗ hổng nào
- `img\`: 98 PNG (AI, có neo thời gian thật trong `anchors.txt`).
- `stock\`: 15 dòng OK thật (2 ảnh tĩnh L022/L063 + 13 clip video, xem `stock\manifest.csv`) + 8
  ảnh filler (`stock\_filler\`, dùng đệm giữa 2 cảnh stock liền nhau).
- `voice_paced.wav` + `voice_paced.srt` + `anchors.txt` + `script.txt`/`img_doan.txt` — đủ để tính
  mốc thời gian cho CẢ 15 dòng stock (dùng đúng công thức `dai_cue_cua_doan()` trong `sinh_neo.py`,
  tra theo đoạn của `img_doan.txt` cho 15 dòng đó — vì chúng không có PNG nên không lọt vào
  `anchors.txt`, nhưng script/srt/img_doan để tính tay/tính máy đều đã sẵn).
- `docs\GIAO_VIEC_HYBRID_COMPOSITOR.md` (đã viết từ trước) mô tả đúng thuật toán ghép 98 ảnh AI
  tĩnh + 15 clip/ảnh stock + 8 filler thành 1 timeline liên tục theo `anchors.txt`.

### 4) Việc DUY NHẤT còn lại = bước 3 (ghép/render `final.mp4`)
Không còn thiếu nguyên liệu gì nữa. Việc còn lại là chạy compositor theo
`docs\GIAO_VIEC_HYBRID_COMPOSITOR.md` để ra file video — đây LÀ hành vi ghép/dựng video (ffmpeg
concat/overlay ra file cuối) nên đúng ranh giới "Claude Code chỉ làm Bước 1" trong CLAUDE.md, Claude
Code dừng ở đây, KHÔNG tự chạy compositor/ffmpeg. Hermes/agent bước 3 chỉ cần đọc 4 file đã có
(`img\`, `stock\`, `anchors.txt`, `voice_paced.wav`) + spec compositor là dựng được, không cần hỏi
lại gì thêm.

### 5) Không đụng gì ngoài phạm vi
Không sửa `script.txt`/`img_prompts.txt`/`img_doan.txt`/`characters.json` (chỉ thêm PNG mới đúng số
thứ tự còn thiếu + cập nhật `stock_plan.tsv` đúng 6 dòng liên quan). Không chạy `assemble.py`/
`render_engine.py`/bất kỳ lệnh ffmpeg concat/overlay nào, không có `final.mp4`/`draft.mp4` nào được
tạo ra.
=====================================================================
