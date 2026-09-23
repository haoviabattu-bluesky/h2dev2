# SOP — LANE E: 健康の知恵袋 (シニア健康・食事習慣, Nhật, medical-explainer list video)

> Kênh mẫu: シニアいきiki健康 (https://www.youtube.com/channel/UCBODlDy5sXo_49pC7KPr7vQ).
> Kênh của mình: **健康の知恵袋** `@70dai-kenko` (profile `kenko-chiebukuro`, mail dòng 6 sheet
> GMAIL — normaneileenpm218@gmail.com). Khác 3 lane kia ở chỗ: không có nhân vật host cố định
> (mỗi mục trong list là 1 người minh hoạ khác nhau), giọng NAM bác sĩ/phát thanh viên (khác
> satori nữ tâm tình, khác toshi nam điều tra viên), và cấu trúc là **list đếm ngược N mục**
> chứ không phải 悟り hay 5 chương.

| Anh nói | Profile | SOP |
|---|---|---|
| "video satori / người già / Nhật kể chuyện đời" | `satori-jp-obaa` | `SOP_SATORI_JP.md` |
| "video 都市伝説 / vũ trụ / bí ẩn / Lane A" | `toshi-densetsu-jp` | `SOP_TOSHI_DENSETSU_JP.md` |
| "video sức khoẻ người già / Lane E / 健康の知恵袋" | **`kenko-chiebukuro`** | **file này** |

Nguồn nghiên cứu: **KHÔNG phải `docs/channel_dna/`** — dự án `TRENDING-RESEARCH` (khác
`SPACE_RESEARCH`) đã bàn giao hồ sơ đầy đủ hơn, user duyệt 2026-09-13:
```
FlowHandoff_local/results/laneE_from_research/
├── LANE_E_HANDOFF.md                    ← đọc trước (14 mục bàn giao, tự chứa)
├── channel_analysis_ikiki.json          ← Channel DNA dạng JSON (schema chuẩn)
├── channel_analysis_ikiki_report.html   ← báo cáo duyệt đầy đủ
└── data/
    ├── analysis_ikiki_raw.json          ← 17 video + baseline thô
    ├── ikiki_transcripts_final.json     ← transcript THẬT của 3/17 video (có timestamp)
    ├── ikiki_comments_breakout.json / ikiki_comments_mid.json
    └── ikiki_thumb_all.png              ← 17/17 thumbnail ghép lưới
```
⚠️ Chỉ 3/17 video lấy được transcript thật (IP bị YouTube chặn 429 lúc TRENDING-RESEARCH crawl).
Hook/script formula rút ra từ 3 video đó + pattern title/thumbnail của cả 17 video — KHÔNG phải
transcript toàn kênh. Số liệu nghiên cứu của kênh mẫu dùng tên viện MƠ HỒ (`国立○○センター`) —
kênh mình KHÔNG được copy thói quen này, số nào không kiểm chứng được thì diễn đạt định tính.

---

## 0. BẢNG DELTA — khác 3 lane kia chỗ nào

| Khâu | Satori | Toshi (Lane A) | **Lane E** |
|---|---|---|---|
| Người kể | Cụ bà ngôi 1 kể đời mình | Người dẫn tài liệu ngôi 3, nam trầm | **Bác sĩ/phát thanh viên ngôi 2, nam trầm, nói CHUYỆN với khán giả** |
| Giọng | George @0.92 · 270 chữ/ph | Akira @1.15 · 380,3 chữ/ph | **Papa Ji - Deep Wise** `elevenlabs_rDiGqdvxRVKhplqZE31x` @**1.0** · **290,9 chữ/ph** (đo thật 2026-09-16, mẫu story) |
| Cấu trúc | 悟り 3 tầng kết | 5 chương 第1章…第5章 | **List đếm ngược 5 mục** (`structure="list_countdown"`, mỗi mục: cơ chế→story minh hoạ→%nghiên cứu→mini chốt) |
| Thời lượng mục tiêu | 30' | 31,5' (~10.546 chữ) | **20' = 5.818 chữ** (kênh mẫu 16-36', chọn mức thấp cho tập đầu — dossier §12 khuyến nghị) |
| Nhân vật lặp lại | CÓ (REF-LOCK bắt buộc) | KHÔNG | **KHÔNG** — mỗi mục 1 người minh hoạ ẩn danh khác nhau, `image.ref_lock=false` |
| Thân video | Ảnh AI toàn bộ | Clip stock | **Ảnh AI minh hoạ (tranh vẽ tay ấm áp)**, `body.mode="ai_images"` |
| Thumbnail | Chân dung REF-LOCK | Ảnh vũ trụ, không mặt người | **Nền đen + chữ 4 tầng (cam/trắng/đỏ/xanh) + 1 ảnh THẬT đồ ăn**, `require_face=false` |
| Rủi ro pháp lý/nội dung | — | — | **Y khoa**: mọi kịch bản BẮT BUỘC có câu tham khảo bác sĩ, cấm tuyên bố chữa khỏi bệnh |

---

## 0b. CHANNEL ANALYZER — ĐÃ CHẠY TOÀN BỘ KÊNH, do Máy 1 tự làm (2026-09-16, cập nhật lần 2)

Ban đầu định BỎ QUA bước này vì hồ sơ TRENDING-RESEARCH đã đầy đủ hơn (xem lịch sử bên dưới). Nhưng
`channel_analyzer.py` **KHÔNG cần máy 2** — chạy được ở BẤT KỲ máy nào có Python + mạng (đọc kỹ
docstring đầu file: "không bắt buộc phải qua máy 2"). User chốt 2026-09-16: máy 2 chưa sẵn sàng thì
**Máy 1 (h2dev) tự chạy luôn**, không đợi.

**Lần 1** chỉ lấy `--n-videos 8` (mặc định của tool — ĐÃ lọc theo view giảm dần trước khi cắt, xem
`crawl_catalog()`, không phải chọn ngẫu nhiên). User hỏi lại "sao chỉ 8, kênh có bao nhiêu video" →
soi catalog đầy đủ thì kênh có **20 video** (không phải 17 như TRENDING-RESEARCH ghi ngày
2026-09-13 — kênh đăng thêm 3 video mới: `sHQfJS9e8Zc`/`ELaeDwNFs0Y`/`YbDaVO9McTQ`). Kênh nhỏ nên
chi phí phân tích hết không đáng kể → **chạy lại LẦN 2 lấy đủ 20/20**:

```bash
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
py -3.13 channel_analyzer.py --channel-url "https://www.youtube.com/channel/UCBODlDy5sXo_49pC7KPr7vQ" \
    --out-dir E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\ikiiki-kenko --n-candidates 20 --n-select 20 \
    --niche-hint "シニア・高齢者向け健康・食事習慣（60〜85歳、医師解説風、実在人物のエピソード＋研究データ引用）"
```
(⚠️ Lệnh trên đã chạy bằng bản CLI CŨ, dùng cờ `--n-videos 20` — bản CLI đó đã bị **1 tab khác đổi
giữa chừng cùng ngày 2026-09-16** thành `--n-candidates`/`--n-select` (`--n-candidates` = pool ứng
viên tối đa xét theo view, kênh ít hơn số này thì xét HẾT; `--n-select` = số video được chọn đưa
vào Gemini). Kết quả 20/20 video đã chạy KHÔNG bị ảnh hưởng gì — file `.py` bị sửa sau khi dữ liệu
đã ghi xong. Lệnh mẫu ở trên đã cập nhật theo CLI MỚI, nhưng **luôn chạy `--help` trước khi copy
lệnh** — nhiều tab cùng sửa `pipeline/channel_analyzer.py` (file dùng chung mọi lane) nên interface
có thể đổi bất cứ lúc nào, đừng tin mù quáng lệnh mẫu kể cả trong chính file SOP này.)

Kết quả đo thật (lần 2, đè lên lần 1): **215s tổng, 20/20 video lấy được transcript** (IP máy này
không bị chặn 429 — khác lúc TRENDING-RESEARCH chỉ được 3/17), QC DNA "ĐẠT 11/11 đề mục",
`CHANNEL_DNA.md` dài 14.247 ký tự (gấp ~1,6 lần bản 8 video). Ra
`docs/channel_dna/ikiiki-kenko/CHANNEL_DNA.md` + `VIDEO_ANALYSIS/*.json` (20 file, bao gồm cả video
YẾU để học anti-pattern, không chỉ video HIT). Đã test
`retrieve_videos.py --dna-dir docs\channel_dna\ikiiki-kenko --topic "転倒・骨折予防 食品 高齢者"`
— chạy tốt.

**Có 2 nguồn DNA song song cho Lane E, dùng cả hai, không cái nào thay cái nào:**
- `FlowHandoff_local/results/laneE_from_research/` (TRENDING-RESEARCH, 14 mục bàn giao, người
  duyệt tay, sâu hơn về hook/CTA/retention — nhưng chỉ 3/17 video có transcript thật, và THIẾU 3
  video mới nhất của kênh)
- `docs/channel_dna/ikiiki-kenko/` (channel_analyzer.py, tự động, **20/20 video** có transcript
  thật — **đầy đủ nhất, kể cả video yếu**, và là nguồn BẮT BUỘC nếu muốn dùng `retrieve_videos.py`)

Chọn chủ đề tập mới: chạy `retrieve_videos.py --dna-dir docs\channel_dna\ikiiki-kenko --topic "..."`
lấy N video liên quan + đọc `CHANNEL_DNA.md`, đối chiếu chéo với `LANE_E_HANDOFF.md` nếu cần thêm
chi tiết hook/CTA. Không cần chạy lại `channel_analyzer.py` cho Lane E nữa trừ khi kênh mẫu đăng
thêm nhiều video mới.

---

## 0c. K4 — SO SÁNH GIỌNG ĐỌC GIỮA CÁC VIDEO KÊNH MẪU (`pipeline/voice_fingerprint.py`, 2026-09-16)

Việc CẤP KÊNH (1 lần, giống K1-K3), trả lời: kênh mẫu dùng CHUNG 1 giọng đọc hay đổi giọng theo
video? Quyết định này chốt xong thì mới nên voice-clone và gán vào `profile.voice`.

**Phương pháp** (không dùng speaker-verification model nặng như resemblyzer/speechbrain — `torch`
chưa cài, `webrtcvad` không có wheel sẵn cho py3.13/Windows): tải audio 6 video trải đều theo
view_count qua yt-dlp, cắt 50s giữa clip (bỏ nhạc hiệu mở đầu), đo **F0 trung vị** (autocorrelation,
phân biệt nam/nữ rất đáng tin) + **vân tay MFCC trung bình** (13 hệ số, so bằng cosine similarity —
ước lượng THÔ, không phải embedding chuẩn, chỉ đủ bắt khác biệt RÕ RỆT).

**Kết quả đo thật (6 video, trải từ cao nhất đến thấp nhất view):**
| video_id | F0 trung vị | Nhóm |
|---|---|---|
| kN6wHIqYA0Q (view cao nhất, #1) | 188,2 Hz | A |
| aWXuORPaoH0 (nguồn `competitor.txt` tập 1) | 175,8 Hz | A |
| Uaj9mNJgm6g | 195,1 Hz | A |
| YbDaVO9McTQ (view thấp nhất) | 188,2 Hz | A |
| Og9pQzoKllo (「87歳の壁が**男性**だけを襲う」) | 97,0 Hz | B |
| c2EG9MLCHck (「あなたの未来」— cũng thuộc nhóm video 俺/僕 theo CHANNEL_DNA) | 94,7 Hz | B |

Cosine similarity trong nhóm A ≈ 0,99 (gần như cùng 1 giọng); trong nhóm B = 1,000; **giữa A và B
chỉ 0,84-0,89** (khác rõ). → **KẾT LUẬN: kênh mẫu dùng ÍT NHẤT 2 GIỌNG**, chia đúng theo ranh giới
đã thấy ở `CHANNEL_DNA.md` mục Narrative style (các video dùng đại từ 俺/僕 hướng nam giới — video
7, 11, 12, 17, 18, 19 — là nhóm B, giọng trầm nam rõ F0~95Hz; các video còn lại — kể cả video nguồn
`competitor.txt` tập 1 — là nhóm A, F0~176-195Hz).

⚠️ **F0 176-195Hz của nhóm A nằm ở dải THƯỜNG GẶP Ở GIỌNG NỮ** (nam thường 85-180Hz, nữ thường
165-255Hz) — mâu thuẫn với `profile.narrator.gender="male"` hiện tại (chọn dựa trên cảm nhận văn
phong "bác sĩ", chưa đối chiếu số đo). Đây LÀ SỐ ĐO, không phải suy đoán, nhưng vẫn cần anh nghe tay
xác nhận (máy đo F0 không tuyệt đối chắc chắn 100% về giới tính, nhất là giọng TTS/qua xử lý).

**Đã voice-clone thử nhóm A** (nguồn: `aWXuORPaoH0`, đúng video dùng làm `competitor.txt` tập 1) qua
OpenSpeaker (`docs/COURSE_NOTES` … xem mục "VOICE TRẢ PHÍ" trong `CLAUDE.md`), `remove_background=
true`: **`voice_id=2653739` → dùng trong profile là `clone_2653739`**. Đo `char_rate` thật:
**326,3 chữ/phút** (nhanh hơn ~12% so với giọng ElevenLabs "Papa Ji" đang dùng, 300,7 chữ/phút đo lại
cùng ngày — đổi giọng thì PHẢI đo lại `target_chars`, không dùng số cũ). File nghe thử để anh so
sánh: `assets/_voice_test/calib__2653739_10_none_story.mp3` (giọng clone từ kênh mẫu) vs
`assets/_voice_test/calib_plqZE31x_10_none_story.mp3` (Papa Ji hiện tại).

**Anh đã chốt (2026-09-16): dùng giọng clone từ kênh mẫu.** `profile.voice` đã đổi sang
`clone_2653739`, char_rate 326,3 chữ/phút. Vì char_rate đổi (290,9→326,3, +12%), `script.txt` tập 1
đã **VIẾT LẠI TỪ B3** cho khớp mục tiêu 20' mới (6.526 chữ) — bản cũ 5.738 chữ (đo theo giọng Papa
Ji cũ) đã lỗi thời, xem bản mới ở §6. Nhóm B (giọng nam trầm, dùng cho các tập kiểu "87歳の壁…"
hướng nam giới, ví dụ STT9 ở §1b) **CHƯA clone** — chỉ làm khi thật sự sản xuất tập thuộc nhóm này.

### ⭐ ĐÓNG VÒNG NGHI VẤN GENDER (2026-09-17) — mâu thuẫn ở trên ĐÃ XÁC NHẬN LÀ THẬT

Ở trên ghi "vẫn cần anh nghe tay xác nhận" nhưng KHÔNG AI quay lại làm việc đó trước khi sản xuất
ep01 thật — `profile.narrator.gender` vẫn để "male" suốt từ 2026-09-16 tới lúc giao hàng. Anh xem
xong ep01 mới phát hiện hình/giọng không khớp giới và báo lại (2026-09-17). Đo lại NGAY LÚC ĐÓ, lần
này đo trực tiếp **file OUTPUT** (`voice.mp3` đã tổng hợp thật, không chỉ audio nguồn) bằng đúng hàm
`voice_fingerprint.estimate_f0_median()`, 3 đoạn tách biệt (đầu/giữa/cuối video 20 phút):

| Đoạn | F0 trung vị |
|---|---|
| ~60s | 188,2 Hz |
| ~600s (giữa) | 179,8 Hz |
| ~1100s (cuối) | 183,9 Hz |

**Nhất quán 180-188Hz — CHÍNH XÁC dải nữ**, khớp với F0 đo nguồn (176-195Hz) ở trên. Kết luận: **bản
thân giọng clone KHÔNG sai** — cái sai DUY NHẤT là field `profile.narrator.gender="male"` (đã sửa
thành `"female"` 2026-09-17, kèm ghi chú lý do trong chính field đó) và mọi văn phong/kịch bản được
viết dưới giả định "male" trước đó. Đã kiểm nhanh `TIEU_DE_MO_TA.txt`/`DANG-TAI.txt` — tiếng Nhật
không có wording nam tính lộ liễu (「医師解説」= trung tính giới), nên rủi ro chính nằm ở SẮC THÁI văn
phong tinh tế trong `script.txt` (nếu có) hơn là lỗi lộ rõ.

**QUY TẮC MỚI (bắt buộc từ nay, ghi cả vào skill global
`C:\Users\admin\.claude\skills\openspeaker_voice_clone.md` §6b):**
1. Sau khi clone giọng cho MỘT KÊNH MỚI, **BẮT BUỘC đo F0 của chính audio OUTPUT** (không chỉ audio
   nguồn) trước khi ghi `narrator.gender`/viết `persona` vào profile — KHÔNG suy đoán theo cảm nhận
   văn phong. Nghi ngờ/biên giới thì nghe tay + hỏi user, đừng tự đoán rồi để trôi qua sản xuất thật.
2. Kênh mẫu có NHIỀU NHÓM GIỌNG (như Lane E: nhóm A nữ ~180Hz dùng cho hầu hết tập, nhóm B nam trầm
   ~95Hz dùng riêng cho tập hướng nam giới) → **tập nào thuộc nhóm giọng KHÁC với giọng đã clone thì
   PHẢI clone riêng đúng nhóm đó trước khi sản xuất tập**, không mặc định dùng lại giọng đã có cho
   mọi tập. Việc này ÁP DỤNG NGAY khi tới STT9 (hoặc bất kỳ tập nào rơi vào nhóm B).

---

## 1. QUYẾT ĐỊNH ĐÃ CHỐT (2026-09-16)

- **Mô hình sản xuất**: `body.mode = "ai_images"` (tranh vẽ tay ấm áp minh hoạ, không phải clip
  stock) — đúng định dạng gốc "illustration + narration" của kênh mẫu, đã verify khung hình thật
  lúc TRENDING-RESEARCH tải video soi frame.
- **Không REF-LOCK**: kênh mẫu không có 1 nhân vật host lặp lại — mỗi mục trong list nêu MỘT
  người minh hoạ khác (68 tuổi cựu nhân viên siêu thị, 75 tuổi giáo viên, 106 tuổi cô Matsumoto…).
  Đây là chi tiết ĐẠI DIỆN dùng để minh hoạ, KHÔNG phải người có thật xác định danh tính — script
  không được gắn họ tên thật hay tuyên bố đây là câu chuyện xác thực 100%.
- **Giọng**: Papa Ji - Deep Wise (nam, trầm, uy tín kiểu bác sĩ), tốc độ 1.0, char_rate đo thật
  **290,9 chữ/phút** (mẫu văn "story", vì nội dung thiên về câu chuyện + ví von hơn là mốc
  năm/địa danh dày đặc kiểu tài liệu — khác style "doc" của toshi).
- **Cấu trúc**: `list_countdown`, đã thêm nhánh code mới trong `pipeline/ai_steps.py`
  (`_cau_truc_block`) — KHÔNG dùng nhánh `chapters5` (tài liệu 5 chương) hay mặc định (悟り satori),
  cả hai đều sai hình dạng cho ngách này.
- **Thumbnail**: 4 tầng chữ (cam/trắng/đỏ/xanh lá) nền đen + 1 ảnh THẬT của món ăn/thực phẩm được
  nêu trong tập đó (không phải minh hoạ vẽ tay) — khác objet chân dung REF-LOCK của satori.
- **KHÔNG Ken Burns (không zoom/pan ảnh)** — chốt 2026-09-20: khán giả là người già, hiệu ứng
  ảnh "rung" (zoom/pan liên tục) dễ gây chóng mặt/khó chịu. `profile.assemble.zoom = 1.0` (khác
  satori/Lane A dùng zoom>1.0) — `assemble.py` hiểu zoom<=1.0 là tắt hẳn hiệu ứng, ảnh đứng yên
  hoàn toàn suốt clip. KHÔNG tăng số này lại cho Lane E.
- **Chuyển cảnh + phụ đề đã DUYỆT cho ep01 (2026-09-20), dùng làm chuẩn cho các tập sau**: thay vì
  100% crossfade đều của `assemble.py` mặc định, dùng skill global `video-chuyen-canh`
  (`C:\Users\admin\.claude\skills\video-chuyen-canh\scripts\ghep_anh_co_chuyen_canh.py`) với
  `--ratio 0.55 --zoom 1.0` (mix 5 kiểu: cắt thẳng/crossfade/zoom-từ-đen/đẩy ngang/mờ-vào, KHÔNG
  Ken Burns trong cảnh — giữ đúng rào phía trên) + `--srt voice.srt --font "Yu Gothic" --sub-size 32`
  (phụ đề tiếng Nhật cháy cứng, bottom-center, chữ trắng viền đen — khán giả già cần đọc theo).
  `timeline.csv` sinh từ `assemble.sync_durations()`/`anchor_durations()` của chính `assemble.py`
  (khớp đúng cách chia ảnh mà pipeline vẫn dùng), KHÔNG tự đoán thời lượng từng ảnh. ⚠️ Việc CHẠY
  B8 thật (bước ghép) vẫn là Bước 3 theo `CLAUDE.md` — Claude Code chỉ làm việc này khi user xác
  nhận ngoại lệ rõ ràng cho từng tập, không tự suy ra "đã làm 1 lần thì các tập sau cứ thế làm".

## 1b. DANH SÁCH 10 TẬP ĐẦU + QUY TẮC GHI TRANG TÍNH `70dai-kenko` (2026-09-16)

Học cách 2 lane khác điền trang tính (`shinya_shiryoshitsu` = Lane A, `irogatatarukioku` = Lane D)
rồi SỬA LẠI cho đúng đặc thù Lane E: **Lane E tự nghiên cứu bằng Claude Code + WebSearch**, KHÔNG có
dự án ngoài (kiểu SPACE_RESEARCH) liên tục đổ hồ sơ sẵn vào `_READY\`. Vì vậy vocab `TÌNH TRẠNG` và
cách dùng cột `FOLDER` khác 2 lane kia — chép nguyên xi là sai.

### Cột A→K (đổi thứ tự 2026-09-19 — bảng dưới đây là bản MỚI NHẤT, ghi đè bảng A→H cũ ở trên)
Header thật trong sheet: A=STT · B=NỘI DUNG · C=FOLDER · D=KỊCH BẢN · E=TITLE-DESCRIPTION ·
F=TAGS · G=THUMBNAIL · H=STATUS-IMG · I=VIDEO · J=LIST · K=GHI CHÚ.

| Cột | Field | Cách ghi cho Lane E |
|---|---|---|
| A | STT | Thứ tự ƯU TIÊN LÀM. Thư mục `assets/kenko-chiebukuro/ep<STT>-<slug>` phải khớp đúng số này. |
| C | FOLDER | Trỏ THẲNG vào `E:\CLAUDE\YOUTUBE\h2dev\assets\kenko-chiebukuro\ep<NN>-<slug>\`. Chỉ điền khi thư mục đã thật sự tồn tại. |
| D | KỊCH BẢN | Ghi **`done`** khi kịch bản đã QC nội dung xong **VÀ** đã chạy xong giọng nói (QC'd) **VÀ** đã viết xong prompt ảnh (text-only, chưa vẽ) — tức B3/B3Q/B3F/B3S/B4/B4Q/B5W/B5P đều đạt. Chốt 2026-09-19: đây là "bar" mới, XA hơn chỉ mỗi kịch bản — xem `docs/quy-uoc-cot-sheet-lane-satori.md`-tương-đương của Lane E (chưa có memory riêng, theo đúng đoạn này). |
| E/F/G | TITLE-DESCRIPTION/TAGS/THUMBNAIL | **TẠM THỜI CHƯA LÀM** (chốt 2026-09-19) — để trống tới khi có lệnh khác. TAGS **KHÔNG** được dùng làm chỗ ghi marker bàn giao máy 2 (bài học thật: đã dùng nhầm F cho marker "Xong nội dung - cần ảnh" 1 hôm, phải sửa lại — xem cột H bên dưới). |
| H | STATUS-IMG | **Ô BÀN GIAO MÁY 2 — GHI GỌN TRONG ĐÚNG 1 Ô** (chốt 2026-09-19, thay đổi so với cách cũ từng tách F=marker/H=path ra 2 ô). Format 2 dòng trong cùng 1 cell: dòng 1 = `Xong nội dung - cần ảnh`, dòng 2 = đường dẫn folder job Syncthing **`E:\CLAUDE\YOUTUBE\FlowHandoff_local\jobs\<slug>\`** (⚠️ KHÔNG có `h2dev\` — xem cảnh báo đường dẫn ngay dưới đây). Khi máy 2 vẽ xong, máy 2 (hoặc mình đọc kết quả rồi) ghi đè lại thành `Img done - X/Y ảnh`. |
| I | VIDEO | Đường dẫn `E:\CLAUDE\YOUTUBE\CHANEL\kenko-chiebukuro\ep<NN>-<slug>\` — CHỈ ghi khi B11 đã giao xong thật. |
| K | GHI CHÚ | Tự do — trạng thái từng bước (B3Q/B3F/B3S/B4Q/B5P đạt hay không), lịch đăng, cảnh báo. |

**Job folder Syncthing cho máy 2** (song song với ô H ở trên): trên MÁY 1 (máy Claude Code đang
chạy `make_video.py`), thư mục job thật sự nằm ở `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\<slug>\`
(có `h2dev\`). **Nhưng đường dẫn ghi vào Sheet cho máy 2 đọc PHẢI BỎ `h2dev\`** —
`E:\CLAUDE\YOUTUBE\FlowHandoff_local\jobs\<slug>\` — vì Syncthing ở máy 2 mount thư mục
`FlowHandoff_local` trực tiếp dưới `E:\CLAUDE\YOUTUBE\`, không lồng trong `h2dev\` như máy 1. Bài
học thật 2026-09-19: ghi nhầm cả `h2dev\` vào Sheet cho ep01-05, máy 2 báo path không tồn tại →
đã sửa lại. Mỗi job folder chứa `img_prompts.txt` (copy từ
`assets/kenko-chiebukuro/<slug>/img_prompts.txt`, **PHẢI kết thúc bằng newline** — thiếu newline
cuối làm `wc -l` phía máy 2 đếm thiếu 1 dòng so với `_BANGIAO.txt`, dù nội dung/số prompt vẫn đúng)
+ `_BANGIAO.txt` (job Loại B — plain, không REF-LOCK, vì Lane E không khoá nhân vật; nếu có dòng
bắt đầu bằng `@GROK` thì `_BANGIAO.txt` phải ghi rõ số dòng đó + lý do — cảnh có trẻ em/minor,
Nano Banana Pro/gpti2 chặn content-policy nên phải vẽ bằng Grok Imagine, phần chữ sau `@GROK ` vẫn
là prompt bình thường không bỏ đi). Kết quả máy 2 trả về ở `FlowHandoff_local\results\<slug>\`
(`NNN.png` + `manifest.json`).

### 10 tập đầu đã chọn (STT = thứ tự ưu tiên, dàn đều 5 trụ cột nội dung kênh mẫu)
| STT | Trụ cột (CHANNEL_DNA) | ĐỀ TÀI (tiếng Nhật, làm việc) | Slug dự kiến |
|---|---|---|---|
| 1 | #1 Chống suy giảm cơ bắp/té ngã | 転倒・骨折リスクを下げる安い食品5選 | `ep01-tento-kossetsu` (đã có `series_ctx.txt`) |
| 2 | #1 Chống suy giảm cơ bắp/té ngã | 気づかないうちに進む「筋肉の減少」5つのサイン | `ep02-sarukopenia-sign` |
| 3 | #2 Sai lầm ăn uống tưởng tốt hoá hại | 良かれと思って実は筋肉・腎臓に負担をかける食習慣5つ | `ep03-eiyou-machigai` |
| 4 | #3 Tuần hoàn/thần kinh/đôi chân | 血管・糖尿病の異変が足に出る5つのサイン | `ep04-ashi-sign` |
| 5 | #3 Tuần hoàn/thần kinh/đôi chân | 足の血流を良くして夜間頻尿を減らす5つの習慣 | `ep05-kettsuryuu-hinnyou` |
| 6 | #4 Viêm mãn tính/trục ruột-não | 腸と脳を守る抗炎症食品5選 | `ep06-koenshou-shokuhin` |
| 7 | #4 Viêm mãn tính/trục ruột-não | 見逃されやすい物忘れの初期サイン5つ | `ep07-monowasure-sign` |
| 8 | #5 Thói quen trường thọ | 100歳まで元気な人に共通する食習慣5つ | `ep08-hyakusaisha-shuukan` |
| 9 | #5 Thói quen trường thọ | 男性が87歳の壁を越えるためにすべきこと5つ | `ep09-87sai-kabe` |
| 10 | #2 Sai lầm ăn uống tưởng tốt hoá hại | 「体に悪い」と誤解されがちな安い食品5選 | `ep10-gokai-shokuhin` |

Nguyên tắc chọn:
- Mỗi tập là **1 chủ đề list-5 độc lập** (đúng `script.gate.list_item_count=5`, cấu trúc
  `list_countdown`) — kênh mẫu RỜI RẠC (xem `channel_dna` phần Audience), không ép thành chuỗi.
- Dàn đều 10 tập qua ĐỦ 5 trụ cột — không dồn hết vào trụ cột #1 dù nó chiếm ~40% ở kênh mẫu, tránh
  khán giả nhàm và tránh cạn ý tưởng sau 3 tập.
- STT chỉ là ưu tiên DỰ KIẾN — đổi được nếu tra cứu thực tế khó hơn (vd trụ cột #4 "trục ruột-não"
  còn ít nghiên cứu dịch sẵn bằng tiếng Anh so với #1/#3), sửa ở trang tính chứ không sửa file này.
- **CHỈ tập được anh chỉ định mới bắt đầu tra `series_ctx.txt`/`competitor.txt`** (luật chung dự án,
  memory `chi-chay-dong-duoc-chi-dinh`: "chạy dòng nào" phải hỏi rõ) — 10 dòng trên là DANH SÁCH
  CHỜ, không phải lệnh làm cả 10 cùng lúc.

⚠️ Hook 20–30s bắt buộc trước S2 — xem `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b.

## 2. LỆNH CHẠY (khi viết tập đầu tiên)

```bash
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline
py -3.13 -X utf8 make_video.py --profile kenko-chiebukuro --slug ep01-tento-kossetsu
```

Chủ đề tập 1 (đã chốt theo §13 `LANE_E_HANDOFF.md` — bám nỗi sợ té ngã/gãy xương, kênh mẫu
CHƯA đốt chủ đề này trong 17 video):
> 「70歳以上の方へ：5つの安い食品が、転倒・骨折のリスクを静かに下げていた——ほとんどの方がご存知ない」
> (50 ký tự — nằm trong ngưỡng `title_len` [35,55] đã đo)

**Trước khi chạy B3 thật, cần chuẩn bị hồ sơ đề tài** (`competitor.txt` + `series_ctx.txt`) theo
đúng khuôn PHA 3 của skill `youtube-produce`:
- `competitor.txt` = KHUNG KỂ — nay có **20/20 transcript thật** để chọn (không chỉ 3, xem §0b),
  lấy từ `docs/channel_dna/ikiiki-kenko/_raw/transcripts.json` hoặc chạy
  `retrieve_videos.py --topic "転倒・骨折予防 食品 高齢者"` để xếp hạng lại. Gần chủ đề té ngã/gãy
  xương nhất trong 20 bản: `aWXuORPaoH0` (「75歳以上の方へ：5つの天然食品が筋肉の消失を止める可能性」,
  list 5 mục, 20,4 phút) — cùng dạng list-5 với chủ đề tập 1.
- `series_ctx.txt` = TƯ LIỆU SỰ THẬT — **CHƯA CÓ**, phải tự tra cứu 5 thực phẩm rẻ tiền + cơ chế
  khoa học thật giúp giảm nguy cơ té ngã/gãy xương ở người 70+ (canxi/vitamin D/K2, protein, natto,
  cá nhỏ ăn cả xương…) kèm NGUỒN kiểm chứng được — tuyệt đối không bịa % hay tên nghiên cứu, không
  copy kiểu "国立○○センター" mơ hồ của kênh mẫu.

## 3. GATE — ngưỡng đã đo/hiệu chỉnh (xem chi tiết + ghi chú trong `profile.script.gate._gate_note`)

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| title_len | 35–55 ký tự | ĐO THẬT trên 5 tiêu đề HIT (37-51 ký tự) |
| hook_chars (120s đầu) | 550–750 chữ | ĐO THẬT trên 3 transcript thật (596-650 chữ) |
| list_item_count | 5 | Theo chủ đề tập 1 đã chốt |
| comma_per_sentence | 1,0–3,0 | HIỆU CHỈNH (transcript ASR thiếu dấu phẩy thật, không đo được đáng tin — xem note trong profile) |
| chars_per_breath | 10–24 | HIỆU CHỈNH tương tự, tham chiếu nhịp toshi (9-22, gần nhất đã có) |
| dialogue_ratio_max | 5% | Định tính — ngách này gần như không có hội thoại 「」 |
| require_next_ep_teaser | false | Video độc lập theo ngày, không phải series nối tiếp |

⚠️ 2 chỉ số "HIỆU CHỈNH" cần đo lại bằng B3Q ngay sau khi có kịch bản đầu tiên — đây là số phỏng
đoán có căn cứ, không phải số đo trực tiếp đáng tin 100% (bài học từ toshi: đừng chép mô tả cảm
giác thành gate cứng).

## 4. RỦI RO Y KHOA — bắt buộc đọc trước khi duyệt bất kỳ kịch bản nào

Theo §14 `LANE_E_HANDOFF.md`: ngách sức khoẻ có rủi ro y khoa thật. Mọi kịch bản của lane này:
- PHẢI có ít nhất 1 câu dạng "一般的な健康情報です。持病のある方は医師にご相談ください" (thông tin sức
  khoẻ mang tính tham khảo chung, người có bệnh nền xin hỏi ý kiến bác sĩ).
- KHÔNG được tuyên bố "chữa khỏi" bất kỳ bệnh gì một cách tuyệt đối.
- Số liệu % / nghiên cứu chỉ dùng khi có trong `series_ctx.txt` đã kiểm chứng — thấy số nào không
  chắc thì diễn đạt định tính ("nhiều nghiên cứu cho thấy…"), đừng nêu số cụ thể bịa ra.
- Code đã tự đưa hướng dẫn này vào prompt viết script (`_cau_truc_block` nhánh `list_countdown`
  trong `pipeline/ai_steps.py`) — không cần nhắc lại tay mỗi lần.
- ⭐ Việc "B3Q nên có thêm 1 lượt kiểm câu tham khảo bác sĩ" đã LÀM XONG và VƯỢT dự tính ban đầu —
  xem **§4b B3S** ngay dưới đây, không phải sửa `qc_script.py` như từng dự kiến ở dòng này.

## 4b. B3S — QC ĐỘC LẬP KỊCH BẢN BẰNG GPT-5.6-SOL (chốt 2026-09-18, sau vụ ep01/ep02)

**Đây là hạ tầng DÙNG CHUNG mọi lane — đọc đầy đủ ở `docs/QC_SCRIPT_GPT_SOL.md`** (kiến trúc 2 lớp,
lý do cần lớp 2, chính sách dừng vòng lặp, 4 chiến lược sửa REMAKE không cần viết lại từ đầu, bẫy
headless `claude -p` tranh chấp OAuth). Mục này chỉ giữ phần RIÊNG của lane E.

Lane này đã bật `profile.script.sol_qc = true`, **chưa khai** `profile.script_qc.domain_focus` riêng
(đang dùng mặc định `DEFAULT_DOMAIN_FOCUS` về rủi ro sức khoẻ người già trong `qc_script_sol.py`, đã
đủ sát ngách này nên chưa cần tuỳ biến thêm).

Đã verify thật trên `ep01-tento-kossetsu` + `ep02-sarukopenia-sign` (2026-09-18) — cả 2 tập từng PASS
B3Q/B3F nội bộ và ĐÃ GIAO HÀNG THẬT trước khi B3S phát hiện lỗi an toàn thật (chi tiết lỗi cụ thể xem
doc chung). Sau khi sửa, verdict B3S cuối cùng của cả 2 tập = **FIX** (không REMAKE), sẵn sàng B4.

## 5. PUBLISH

`profile.publish.upload_channel = "kenko-chiebukuro"` → B11 giao hàng vào
`E:\CLAUDE\YOUTUBE\CHANEL\kenko-chiebukuro\ep<N>-<tên tập>\`.

## 5b. PHÂN VAI GIỮA CÁC AI — Hiện tại vs Hybrid (2026-09-16)

### Giai đoạn NGHIÊN CỨU KÊNH (đã xong cho Lane E — bảng này để lane sau tham khảo)

| Việc | **Hiện tại** (đã xảy ra thật cho Lane E) | **Hybrid** (khi KHÔNG có sẵn hồ sơ từ dự án ngoài) |
|---|---|---|
| Tìm kênh mẫu + chấm điểm sơ bộ | **TRENDING-RESEARCH** (dự án/AI khác hẳn h2dev, không phải máy 2) | Người dùng tự chọn kênh, đưa URL cho Máy 1 |
| Đào sâu transcript/comment/thumbnail → DNA kênh | **TRENDING-RESEARCH** (thủ công + AI riêng của họ, 14 mục bàn giao — SÂU hơn channel_analyzer.py) | **Máy 2** chạy `channel_analyzer.py` (B1+B2) qua Syncthing, theo `GIAO_VIEC_MAY2_CHANNEL_ANALYZER.md` |
| Nhận hồ sơ, kiểm tra, quyết định mô hình sản xuất | **Máy 1** (h2dev — phiên đang viết SOP này) | **Máy 1** — đọc `CHANNEL_DNA.md` do máy 2 trả về |
| Viết `profile.json` + đo char-rate + viết SOP | **Máy 1** (`calibrate.py` chạy cục bộ, không cần máy khác) | **Máy 1** — không đổi ở bước này dù nguồn dữ liệu khác nhau |

### Giai đoạn "CHẠY TẬP X" — ĐÃ CHỐT 2026-09-16: 3 BƯỚC, học y nguyên khuôn satori/toshi,
### CHỈ KHÁC bước 2 (Máy 1 tự vẽ bằng gpti2, không giao Máy 2)

| Bước | Việc | Ai làm | Lệnh (`make_video.py --profile kenko-chiebukuro --slug <slug>`) |
|---|---|---|---|
| **1** | Tư liệu (`competitor.txt`/`series_ctx.txt`) → kịch bản 2-pass + gate → B3Q/B3F → **B4 giọng
  (voice.mp3+SRT)** → **B7 thumbnail** (mô-típ CỐ ĐỊNH toàn dự án — trái nền đen chữ, phải 1 ảnh
  THẬT món ăn, đúng ảnh chụp màn hình kênh gốc anh gửi 2026-09-16; đã khai sẵn trong
  `profile.thumbnail`, KHÔNG đổi cho từng tập, mỗi tập chỉ đổi `thumb_bg_subject.txt` + chữ) | **Máy
  1** (tab này) | `--only B4` rồi `--only B7` (B7 tự vẽ 1 ảnh nền riêng qua `dedicated_bg`, KHÔNG
  cần đợi B5) |
| **2** | Sinh ảnh AI minh hoạ THÂN video (~80-100 ảnh/tập, phong cách đúng kênh gốc — minh hoạ vẽ
  tay ấm áp, đã khai `image.style_suffix`) | **Máy 1** (anh đã cho phép 2026-09-16, vì Lane E
  `ref_lock=false` nên không cần REF-LOCK phức tạp như satori/toshi phải giao máy 2 — chi phí thấp
  hơn nhiều, ~4.000-5.500đ/tập bằng gpti2, chấp nhận được) | `--only B5` (rồi `--only B5Q` nếu
  có QC ảnh) |
| **3** | Dựng video từ kịch bản (bước 1) + ảnh (bước 2), **BẮT BUỘC QC video xong mới giao list**
  (mốc chương, phụ đề, khớp lời-ảnh, âm lượng…) | **Agent KHÁC** (không phải tab này — theo đúng
  `⛔ CẤM TUYỆT ĐỐI` đầu `CLAUDE.md`: Claude Code không tự ghép/render video) | Hồ sơ giao việc
  riêng cho Lane E — viết theo khuôn `docs/GIAO_VIEC_BUOC3_AGENT.md` (bản gốc cho toshi), đổi
  đường dẫn/lệnh cho đúng `kenko-chiebukuro` — CHƯA viết, xem §6 |

Khác satori/toshi ở ĐÚNG 1 chỗ: bước 2 của họ giao Máy 2 vẽ qua Google Flow (0đ) vì ảnh REF-LOCK
phức tạp cần canh mặt nhân vật nhất quán qua tay người; Lane E không có nhân vật lặp lại
(`ref_lock=false`, mỗi mục 1 người khác nhau) nên việc vẽ đơn giản hơn nhiều, chi phí gpti2 thấp
đủ để Máy 1 tự làm luôn mà không cần dựng thêm hạ tầng giao Máy 2 (hòm thư, quy ước đặt tên đơn
ảnh…) — anh đã xác nhận chấp nhận mức chi phí này.

## 0e. B3 (viết kịch bản) ĐỔI SANG "NÃO CLAUDE" — `script.engine = "claude_p"` (anh chốt 2026-09-17)

Trước đó Lane E viết kịch bản bằng Gemini (giống mọi lane não-ramcloud khác). Anh chốt đổi ĐÚNG
bước PASS 0 (bóc khung) + PASS 1 (viết bản nháp) của B3 sang **Claude thật**, gọi qua `claude -p`
headless — giống mô hình satori — nhưng **KHÁC CÁCH LÀM**: satori dùng `brain_channel.py` (Claude
là 1 AGENT ĐẦY ĐỦ, tự đọc/ghi file, tự lặp QC trong 1 phiên `claude -p` dài); Lane E dùng
`pipeline/claude_p_bridge.py` (Claude chỉ TRẢ CHỮ cho 1 prompt, `--tools ""` tắt hết tool) — cắm
thẳng vào đúng chỗ `ai_steps.py` đang gọi Gemini, KHÔNG đụng gì tới gate/nén/QC/retry đã chạy tốt.
**Nén khúc, hạ hội thoại, tách câu dài, VÀ TOÀN BỘ QC (`qc_script.py` B3Q, `qc_facts.py` B3F) vẫn
luôn Gemini** — đúng nguyên tắc "Claude viết, Gemini chấm độc lập" (satori cũng vậy: `qc_script.py`
bên đó là Gemini, không phải Claude tự chấm bài mình).

**Cách bật/tắt:** field `profile.script.engine = "claude_p"` (mặc định vắng mặt = Gemini như cũ).
Field-driven, đúng hàng rào #2 CLAUDE.md (cấm `if profile_id==`) — lane khác không khai field này
thì không đổi gì.

**Kết quả đo thật (chạy lại B3→B3F cho `ep01-tento-kossetsu`, 2026-09-17, viết bản MỚI thay bản
Gemini cũ):**
| | Bản Gemini (2026-09-16) | Bản Claude (2026-09-17) |
|---|---|---|
| Thời gian PASS 0+1 | ~1 phút | PASS0 53s + PASS1 229s ≈ **4,7 phút** (chậm hơn nhiều) |
| B3F lần đầu | 8-9 chi tiết bịa (nhiều lần chạy lại) | **0 phát hiện** |
| Ẩn dụ xuyên suốt | Trộn nhiều ẩn dụ rời rạc | 1 hệ ẩn dụ nhất quán cả bài (nhà=cột/kim khí, canxi=hàng giao, vitamin D=người giao hàng) |
| B3Q sau 1 lượt tự sửa | Thường cần 2 lượt | SUA sau 1 lượt (còn 1 lỗi NHẸ chấp nhận được) |

⚠️ **Bài học ngay trong lượt test này — ĐỪNG tin "B3F: 0 phát hiện" mù quáng**: bản thảo Claude viết
ra GỐC có câu ghi năm "2026年" cho một phân tích tổng hợp (rõ ràng vô lý — năm hiện tại); B3Q
(Gemini) tự phát hiện + tự sửa thành "2019年" — một năm KHÔNG có trong `series_ctx.txt` (cùng lỗi y
hệt bản Gemini cũ). Nhưng B3F (cũng Gemini, chạy NGAY SAU ĐÓ) lại **không bắt được** lỗi "2019年"
này — cùng loại lỗi mà chính B3F từng bắt được ở bản Gemini hôm trước. Xác nhận lại điều đã ghi ở
§6: **`qc_facts.py` là LLM phán đoán, KHÔNG phải rule cứng** — 0 phát hiện không đồng nghĩa sạch
100%, vẫn cần người soát tay ít nhất 1 lượt trước khi tin. Đã soát + sửa tay (`2019年` → `近年`,
diễn đạt định tính) rồi chạy lại B3F xác nhận sạch thật.

**Đã chạy tiếp B4+B4Q cho bản Claude (2026-09-17, để so sánh trọn Bước 1 — script+giọng — chứ
KHÔNG chạy B5 trở đi vì đó là Bước 2/3, không phải việc của Claude Code):**
| | Bản Gemini (2026-09-16, đã giao CHANEL) | Bản Claude (2026-09-17) |
|---|---|---|
| Chữ script | 6.758 | 6.782 |
| Giọng (voice.mp3) | 20:49 (1.249,6s) | **20:35 (1.235,7s)** |
| B4Q | ĐẠT | **ĐẠT, 0 vấn đề**, coverage 100%, phủ script 100%, đỉnh −2.5 dB |
| B3F (fact-check) | 8-9 chi tiết bịa qua nhiều lượt sửa | 0 (sau 1 lần sửa tay lỗi B3F bỏ sót — xem cảnh báo trên) |

Cả hai bản đều rơi đúng khung ~20-21 phút mục tiêu (20.0'), lệch nhau chỉ 14 giây — **não nào cũng
ra ĐÚNG NHỊP THỜI LƯỢNG** (nhờ cùng char_rate 326.3 đo thật + cùng gate `target_minutes`), khác biệt
thật nằm ở CHẤT LƯỢNG NỘI DUNG (số chi tiết bịa phải sửa tay) chứ không phải ở tốc độ/độ dài.

**CẬP NHẬT 2026-09-17: đã chạy trọn B5→B11 cho bản Claude, GHI ĐÈ bản Gemini đã giao** (anh yêu cầu
trực tiếp "chạy ảnh + dựng video lại cho phần vừa viết lại"). Kết quả: B5Q 0 vấn đề (88 ảnh, 4.400đ,
sau khi bắt+sửa 2 lỗi hạ tầng — xem dưới), B8Q ĐẠT sync_score 3.6/5, B10 "0 phát hiện (0 nặng)"
**NGAY LẦN ĐẦU** (không cần force-qc như bản Gemini trước). `E:\CLAUDE\YOUTUBE\CHANEL\kenko-chiebukuro\
ep01-tento-kossetsu\` giờ chứa bản Claude (final.mp4 20,6 phút). ⚠️ Bản Gemini cũ đã bị GHI ĐÈ mất,
không còn video để so bằng mắt — chỉ còn `script.txt` cũ ở `_truoc_khi_viet_lai/` + số liệu QC đã
ghi ở bảng trên. Chi tiết đầy đủ (bug + số đo + lệnh) đã ghi ở `docs/GIAO_VIEC_LANE_E_BUOC2.md` §3/§6.

**2 bug hạ tầng mới bắt được khi tự chạy lại (đã vá tại gốc, không phải riêng tập 1):**
1. `b5_images()` chỉ sinh `img_prompts.txt` khi file CHƯA TỒN TẠI — không so với `script.txt` đã đổi
   chưa. Viết lại kịch bản mà không tự tay xoá `img_prompts.txt` cũ → B5 âm thầm vẽ ảnh theo NỘI
   DUNG CŨ. Đã tốn 4.450đ vẽ nhầm 1 lần trước khi phát hiện. Chưa sửa code (rủi ro động vào ảnh
   hưởng lane khác dùng chung `make_video.py`) — đã ghi quy trình kiểm tay bắt buộc vào
   `GIAO_VIEC_LANE_E_BUOC2.md` §3 Lệnh 1.
2. Storyboard (đồng bộ ảnh theo câu SRT, gọi Gemini) bị lỗi hạ tầng TẠM THỜI 2/3 lần thử (cả 3 model
   dự phòng cùng lỗi trong ít giây) → tự lùi về "rải đều" kém chính xác hơn mà KHÔNG báo đỏ, chỉ 1
   dòng cảnh báo dễ bị bỏ qua trong log dài. Đã thêm bước kiểm/retry riêng (tách sinh-prompt khỏi
   vẽ-ảnh) vào `GIAO_VIEC_LANE_E_BUOC2.md` §3 Lệnh 1.
3. `ghi_cot_video.py --tab` bắt buộc trùng y hệt `profile.publish.upload_channel`, nhưng tab trang
   tính thật của Lane E là `70dai-kenko` (khác `upload_channel="kenko-chiebukuro"`). Đã vá: thêm
   field `publish.sheet_tab` tách 2 khái niệm, code đọc `sheet_tab` trước, thiếu thì mới lùi về
   `upload_channel` (lane khác không khai field này, hành vi cũ giữ nguyên).

**KẾT LUẬN BƯỚC 1 (script+giọng), não nào tốt hơn:** bản Claude thắng rõ ở CHẤT LƯỢNG NỘI DUNG (0 vs
8-9 chi tiết bịa cần sửa tay, ẩn dụ nhất quán hơn) — đây là tiêu chí quan trọng nhất vì chi tiết bịa
là lỗi có thể khiến video sai sự thật/dính chính sách. Đổi lại bản Claude CHẬM HƠN ~4-5 lần ở khâu
viết (4,7' vs ~1') và tốn quota Claude thay vì tiền Gemini rẻ. Với ngách sức khoẻ (rủi ro y khoa,
đòi hỏi chính xác cao) — chi phí thời gian đổi lấy giảm gần hết lỗi bịa là hợp lý; khuyến nghị dùng
`claude_p` làm mặc định cho Lane E từ tập 2 trở đi.

### ⚠️ NGOẠI LỆ MỘT LẦN cho bước 3 tập 1 (anh chốt 2026-09-16, SAU khi bước 1+2 đã xong)

`CLAUDE.md` (áp dụng CHUNG mọi lane) cấm tuyệt đối Claude Code tự render/ghép video (B8+). Với
RIÊNG tập 1 của Lane E, anh chủ động yêu cầu **đúng một lần ngoại lệ**: tab này (Máy 1) tự chạy
TRỌN VẸN B8→B8Q→B9→B10→B11 để "nắm hết quy trình" trước khi soạn hồ sơ giao Bước 3 cho agent khác
— nghiệm thu bằng chính tab này hoặc Gemini, KHÔNG phải người xem tay. Đây **KHÔNG PHẢI đổi quy tắc
chung** — quy tắc `CLAUDE.md` vẫn nguyên vẹn cho mọi tập SAU của Lane E và mọi lane khác; chỉ tập
`ep01-tento-kossetsu` được phép làm khác, đúng một lần, có lý do rõ (hiểu quy trình trước khi giao
việc), đã xin phép rõ ràng chứ không tự suy diễn.

### ⭐ QUYẾT ĐỊNH CUỐI (anh chốt 2026-09-16, SAU khi tập 1 chạy xong trọn vẹn): bước 2+3 GIAO AGENT
### KHÁC HẲN, giống hệt mô hình Lane D — KHÔNG cần Claude nữa

Sau khi tự chạy hết B5→B11 cho tập 1, kết luận: **bước 2 (sinh ảnh gpti2) KHÔNG cần Claude** — toàn
bộ là lệnh `make_video.py` gọi Gemini (sinh prompt) + gpti2 (vẽ) + Gemini vision (QC), không có
phán xét sáng tạo nào Claude phải làm sống (mọi quyết định "vẽ ai, vẽ gì, khuôn thumbnail" đã chốt
ở bước 1, nằm sẵn trong `profile.json`/`script.txt`/`thumb_bg_prompt.txt`). Bước 3 (ghép+QC+giao)
cũng vậy — thuần lệnh + đọc cổng. Đã gộp bước 2+3 thành **một hồ sơ giao việc duy nhất cho 1 agent
khác** (đúng mô hình Lane D — Lane D cũng gộp "tô màu ảnh còn lại + ghép + giao" vào 1 agent):
**`docs/GIAO_VIEC_LANE_E_BUOC2.md`**.

Trước khi viết hồ sơ, đã SỬA 2 lỗi hạ tầng tại GỐC (không chỉ ghi đè tay 1 lần cho tập 1 nữa) để
agent bước 2+3 không tự dính lại đúng những bẫy Claude vừa gặp:
- `profile.image.character_sheet` đổi từ mô tả tiếng Việt sang **văn bản tiếng Anh prompt-ready**
  ("không có nhân vật cố định, mỗi mục 1 người khác nhau") — B5 dùng thẳng, khỏi cần truyền
  `--sheet` tay mỗi tập.
- `b7_thumb()`: nền RIÊNG (`_thumb/001.png`, dedicated_bg) nay LUÔN được nhận sau 1 lần thử, KHÔNG
  còn so điểm QC thô với ảnh thân video dự phòng nữa (bug gốc gây ra việc B7 từng tự chọn nhầm ảnh ở
  tập 1) — sửa nghĩa là **từ tập 2 trở đi, agent bước 3 không cần lo B7 tự chọn sai ảnh nữa** (dù
  B7 vẫn luôn là việc của Claude/bước 1, không giao agent khác — chỉ là sửa để KHỎI PHẢI can thiệp
  tay lần nữa khi Claude tự làm bước 1 cho tập sau).

**Từ tập 2 trở đi**: Claude (bước 1) làm xong tới hết B7 (thumbnail) rồi DỪNG, giao thẳng hồ sơ
`GIAO_VIEC_LANE_E_BUOC2.md` cho agent khác — KHÔNG còn "Máy 1 tự vẽ ảnh rồi mới giao bước 3" như đã
làm (ngoại lệ) cho tập 1 nữa.

## 0d. ĐÃ KIỂM: KHÔNG DÍNH LỖI "64 dàn ý vs N đoạn văn thật" của satori (2026-09-16)

Sau khi satori-jp-obaa lộ lỗi gốc (`dan_y.txt` 64 dòng cố định ≠ số đoạn văn THẬT của `script.txt`,
dao động 39-63 giữa các tập; máy render đọc theo đoạn văn thật nhưng bộ não từng đánh số
`img_doan.txt` theo 64 → lệch số ảnh nặng, 64×~4,5 ≈ 290 thay vì đúng ~113) — đã soát lại toàn bộ
`pipeline/` xem Lane E (và mọi lane dùng `make_video.py`) có dính không.

**KHÔNG dính — khác kiến trúc, không phải may rủi:** lỗi trên chỉ tồn tại ở nhánh **"não Claude"**
(`brain_channel.py`/`render_engine.py`/`sinh_neo.py`/`sinh_img_doan.py`/`chay_buoc3.py` — riêng cho
satori qua `SOP_CLONE_BRAIN.md`, xem memory `hai-tool-exe-tach-han`). Nhánh Lane E dùng —
**"não ramcloud"** (`make_video.py`/`ai_steps.py`) — **KHÔNG có khái niệm "dàn ý N bước" nào cả**,
nên không thể có 2 đơn vị đếm lệch nhau:
- `ai_steps.write_img_prompts()` (B5, dòng ~1230): `n = max(20, round(giây_audio_THẬT / seconds_
  per_image))` — `giây_audio_THẬT` lấy từ `state["B4"]["seconds"]` (độ dài file .mp3 đã tổng hợp
  thật, KHÔNG suy ra từ số đoạn văn/số dòng dàn ý nào).
- `ai_steps.write_storyboard_prompts()` (B5K, dòng ~1107, khi có `voice.srt`): `n` tính từ chính
  mốc thời gian ĐẦU-CUỐI của phụ đề thật (`cues[-1][1]-cues[0][0]`), rồi neo từng khối ảnh vào cue
  thật — cùng logic "giây/ảnh" user vừa đúc kết cho satori, ramcloud đã làm vậy từ đầu.
- `img_doan.txt`/`dan_y.txt` **không tồn tại** trong nhánh này — đã `grep` xác nhận không file `.py`
  nào trong nhánh ramcloud tham chiếu 2 tên file đó.
- `profile.image.seconds_per_image = 14` (đã khai từ lúc lập profile) — khớp gần đúng con số
  14,2s/ảnh mà satori vừa đo thật, không cần sửa.

**Kết luận: không cần vá gì cho Lane E** (và suy rộng: không lane nào dùng `make_video.py` — Lane A
`toshi-densetsu-jp`, Lane D `irogatatarukioku` — dính lỗi này, vì cùng dùng chung `ai_steps.py`).
Lỗi 290/113 là đặc thù RIÊNG của nhánh não-Claude, không lan sang nhánh não-ramcloud.

## 6. CÒN TREO (chưa làm, nói thẳng)

- Tập 1 (`assets/kenko-chiebukuro/ep01-tento-kossetsu/`) **đã có kịch bản hoàn chỉnh** (bản MỚI
  NHẤT, viết lại 2026-09-16 17:28 sau khi đổi giọng sang `clone_2653739` — xem §0c):
  `series_ctx.txt` + `competitor.txt` (`aWXuORPaoH0`) → `script.txt` **6.758 chữ ≈ 20,7'** ĐẠT gate
  (mục tiêu mới 6.526 chữ, char_rate 326,3). Qua đủ B2→B3→B3Q→B3F, `--force-qc` cho B3F 2 lần liền
  (1 lần cho bản Papa Ji cũ, 1 lần cho bản viết lại này) — cùng 1 mẫu hình lặp lại đáng ghi nhớ:
  · **Lỗi THẬT đã SỬA TAY cả 2 lần**: chi tiết bịa không nguồn ("漁師町の知恵" — địa danh/văn hoá bịa;
    "50kg→50-60g" — số suy diễn từ công thức, không có sẵn trong tư liệu; "2019年" — năm bịa cho một
    phân tích tổng hợp mà tư liệu chỉ ghi "gần đây nhất", không có năm cụ thể).
  · **False-positive đã xác minh, KHÔNG sửa vì đúng, qua bằng `--force-qc`**: số liệu Ở DẠNG PARAPHRASE
    khác cách viết trong `series_ctx.txt` mà checker (LLM) không nhận ra khớp — "1kg"⇄"1キログラム",
    "153.902 người"⇄"15万人以上", "約50%"⇄"2人に1人". VÀ tuổi nhân vật minh hoạ hư cấu (71/72/74/76歳)
    — series_ctx.txt §LƯU Ý VIẾT #4 đã CHO PHÉP tự đặt tuổi cho nhân vật ẩn danh hư cấu, không cần
    nguồn, checker (LLM, không tất định) đôi khi vẫn seo vào diện "số liệu cần nguồn" — bài học: checker
    B3F là LLM phán đoán, KHÔNG phải rule cứng, nên vẫn cần người soát trước khi force-qc, không tin
    100% cũng không bỏ 100%. Xem `qc.json`/`qc_facts.json` trong thư mục tập (bản mới nhất).
- ✅ **TẬP 1 XONG TRỌN VẸN B2→B11 (2026-09-16, ngoại lệ 1 lần Máy 1 tự chạy bước 3 — xem §5b)**:
  voice.mp3 20:49 · B4Q ĐẠT · 89 ảnh (4 @REF + 85 cảnh, 4.450đ, B5Q 0 vấn đề) · `thumbnail_final.png`
  (natto, đúng mô-típ) · `final.mp4` 610MB ghép xong (B8, 9,1 phút xử lý) · B8Q ĐẠT (sync 4,6/5 sau
  khi sửa lỗi phụ đề oan — xem bài học bên dưới) · B10 nghiệm thu (force-qc 6 mục đã soát kỹ, xem
  `qc_facts.json._nghiem_thu_note`) · **B11 đã giao**: `E:\CLAUDE\YOUTUBE\CHANEL\kenko-chiebukuro\
  ep01-tento-kossetsu\` (final.mp4 + thumbnail.png + phude.srt + listting.txt + review-vi.mp4).
  Đã soi tay vài khung hình final.mp4 (0:30, 16:40) — chất lượng đẹp, đúng phong cách watercolor,
  không phụ đề cháy (đúng thiết kế).
- **5 lỗi hạ tầng THẬT đã bắt và sửa khi chạy B4→B11 lần đầu cho Lane E qua `make_video.py` (file
  DÙNG CHUNG mọi lane) — giữ lại làm bài học, lane sau dùng `ai_images` + `burn_subs=false` sẽ đỡ
  dính lại:**
  1. **`thumbnail_text.py` (file DÙNG CHUNG mọi lane) thiếu màu "ORANGE"** trong `COLORS` dict — chỉ
     có WHITE/YELLOW/RED/CYAN/GREEN. Profile Lane E khai `palette=["ORANGE",...]` từ lúc lập (để khớp
     đúng màu thumbnail kênh mẫu) nhưng KHÔNG có ai verify tool có hỗ trợ — B7Q vision bắt được
     "dòng đầu ra màu trắng thay vì cam yêu cầu". **Đã thêm `"ORANGE": (255,149,0)`** vào dict (thuần
     bổ sung, không đụng màu cũ — an toàn cho lane khác). Bài học: khai `palette` mới trong profile
     PHẢI kiểm `COLORS` dict của `thumbnail_text.py` có tên đó không, đừng chỉ tin theo mô tả kênh mẫu.
  2. **B7 tự chọn nền SAI KHUÔN khi nền chuyên dụng (`_thumb/001.png`) bị QC vision chê "vô cảm,
     không gợi tò mò"** (lỗi CẢM TÍNH, không phải lỗi cấu trúc) — code fallback sang ảnh THÂN VIDEO
     (`img/016.png`, cảnh minh hoạ watercolor mờ) vì nó có ÍT vấn đề QC hơn (2 < 3), nhưng ảnh thân
     video KHÔNG có nền đen + KHÔNG chừa chỗ chữ — sai hẳn mô-típ dự án dù điểm QC thấp hơn. Bộ đếm
     "số vấn đề" của B7 không phân biệt được lỗi CẤU TRÚC (sai khuôn) với lỗi CẢM TÍNH (ảnh hơi tẻ) —
     đây là giới hạn thật của cơ chế tự chọn, không phải bug ngẫu nhiên. **Đã ghi đè tay**: chạy lại
     `thumbnail_text.py --bg _thumb/001.png ... --side left` trực tiếp, sửa `state.json["B7"]` kèm
     ghi chú lý do. Bài học cho lane sau dùng `dedicated_bg=true`: LUÔN xem lại `thumbnail_final.png`
     bằng mắt sau B7, đừng tin "B7 xong" trong log là ảnh đúng khuôn.
  3. **`--den X` KHÔNG bỏ qua các bước TRƯỚC X chưa "done"** — chỉ chặn bước SAU X. Một lần `--dry-run`
     ở B5 (chỉ ghi `img_prompts.txt`, không gọi `self.done("B5",...)`) khiến B5 vẫn ở trạng thái CHƯA
     XONG trong `state.json`; lần chạy `--from B7 --den B7` sau đó tưởng chỉ chạm B7 nhưng thực ra
     chạy lại TOÀN BỘ B5 (89 ảnh, tốn tiền thật) vì B5 nằm TRƯỚC B7 trong `STEPS` và chưa "done" thì
     không bị `skip()`. May mắn lần này ảnh vẫn đúng ý & đã được duyệt trước qua `--dry-run`, nhưng
     đây là **bẫy thật, không phải hên xui**: `--dry-run` không tự đánh dấu bước đó "xong" — dùng
     `--only <BƯỚC>` (không phải `--den`) khi chỉ muốn chạm ĐÚNG 1 bước cụ thể.
  4. **`b8q_qc()` gọi `qc_visual.qc_video()` KHÔNG truyền `want_sub`** — hàm `qc_video()` VỐN ĐÃ có
     tham số này (dựng riêng để video KHÔNG cháy phụ đề khỏi bị chấm oan "thiếu phụ đề", chính sách
     dự án từ 2026-09-11), CLI `qc_visual.py` đã mở cờ `--no-sub` từ trước, nhưng lệnh gọi THƯ VIỆN
     bên trong `make_video.py::b8q_qc()` quên truyền — B8Q báo sai "10/10 khung KHÔNG thấy phụ đề"
     cho một video ĐÚNG THIẾT KẾ (burn_subs=false). Không lane nào khác dính vì satori/toshi trước
     đó chưa từng đi qua đúng tổ hợp (nhánh `ai_images`, không phải `stock_clips`) × (`burn_subs=
     false`) trong `make_video.py`. **Đã sửa**: `b8q_qc()` nay truyền `want_sub=self.chay_phu_de()`
     (đọc đúng `assemble.burn_subs` của profile) — sửa CODE DÙNG CHUNG, mọi lane hưởng lợi.
  5. **B8Q/B10 tự đánh dấu "done" NGAY CẢ KHI THẤT BẠI** (`self.done(...)` chạy TRƯỚC dòng `raise
     SystemExit` khi có lỗi) — lần chạy KẾ TIẾP mà không có `--from`, `skip()` thấy bước đã "done"
     là BỎ QUA LUÔN, không biết lần trước nó thất bại, nên KHÔNG cảnh báo gì và ĐI THẲNG XUỐNG bước
     sau (B11 vẫn giao hàng dù B10 vừa trượt ở lượt chạy sát trước) — đã dính thật: sau khi sửa
     `qc_facts.json` nhưng chỉ đổi giờ file (không dùng `--from B10`), lệnh `make_video.py` (không
     cờ) chạy tới B11 luôn mà KHÔNG re-check B10. Bài học: sau khi sửa nguyên nhân một bước đã
     THẤT BẠI, PHẢI dùng `--from <BƯỚC ĐÓ>` để buộc chấm lại — đừng tin "chạy lệnh trơn là nó tự
     biết đường quay lại kiểm", `skip()` không phân biệt "done vì ĐẠT" với "done vì đã BÁO LỖI".
- Danh sách 10 tập đầu đã chốt (§1b) — mới có tập 1 có tư liệu+kịch bản, 9 tập còn lại là Ý TƯỞNG,
  chưa nghiên cứu, đợi anh chỉ định dòng nào mới làm tiếp.
- `comma_per_sentence`/`chars_per_breath` VẪN là số hiệu chỉnh dù nay đã có **20/20 transcript
  thật** (`docs/channel_dna/ikiiki-kenko/_raw/transcripts.json`, chạy 2026-09-16) — đã soi lại, cả
  20 bản đều là dạng ASR gần như KHÔNG có dấu phẩy thật (giống 3 bản cũ), nên KHÔNG đo lại được đáng tin
  hơn. Cần đo trên chính KỊCH BẢN của mình (có dấu câu chuẩn) sau khi viết xong tập 1 qua B3Q.
- Chưa test nhánh code `list_countdown` mới trong `ai_steps.py` bằng kịch bản thật — verify khi
  chạy B3 tập 1.
- Thumbnail 4 tầng màu mới là THIẾT KẾ trên giấy (từ mô tả thumbnail kênh mẫu), chưa render thử.
- Mô hình Hybrid (Máy 2 vẽ ảnh, agent bước 3 ghép+giao hàng — xem §5b) CHƯA thiết lập cho Lane E;
  hiện B4 sẽ tự chạy trên Máy 1 nếu gọi `make_video.py` thẳng, tốn ~4.000-5.500đ/tập.

## HOOK 20–30 GIÂY ĐẦU — CÁCH CỦA RIÊNG LANE NÀY

> ⚠️ Mỗi lane một kiểu hook khác nhau. **Đừng mượn cách của lane khác.**

| | |
|---|---|
| Kiểu mở (`script.hook.patterns`) | H30 H31 H32 H33 H34 |
| Câu khoá (`script.hook.closer`) | K18 |
| Cách dựng hình (`script.hook.visual`) | `lien_mach_than` |
| Nguồn hình | **KHÔNG dựng clip hook riêng** — hook là 30 giây đầu của chính `script.txt`, dựng chung một lần với thân video |
| Công tắc (`script.hook.enabled`) | **đang BẬT** |

Runbook dựng đầy đủ (7 bước + 4 phép kiểm trước khi ghép): `docs\QUY_TAC_VIDEO_HOOK.md`, bảng so sánh
cách dựng của mọi lane ở §5b. Nguyên tắc nội dung hook: `C:\Users\admin\.claude\skills\youtube-hook-research\references\NGUYEN_TAC_HOOK_GOI_DANG.md`.

Viết hook: `py -3.13 pipeline\hook_stage.py --profile kenko-chiebukuro --slug <tập> --mode repair`
