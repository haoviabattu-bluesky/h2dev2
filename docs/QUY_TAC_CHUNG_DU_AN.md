# QUY TẮC CHUNG DỰ ÁN — BẢN ĐẦY ĐỦ (chuyển nguyên văn từ CLAUDE.md ngày 2026-09-30)

> CLAUDE.md nay chỉ giữ router + tên luật (tiết kiệm token: file đó nạp vào MỌI lượt của MỌI tab).
> Chi tiết/lý do/bài học của từng luật đọc ở ĐÂY khi cần. Sửa luật → sửa cả 2 nơi (1 dòng ở CLAUDE.md, chi tiết ở đây).

Mục tiêu: học khoá h2dev.vn → xây kênh YouTube faceless view ngoại (RPM cao), sản xuất nội dung
bằng AI theo quy trình của khoá, tiến tới hệ thống nhiều kênh.

## 🚦 ROUTER LANE — LÀM ĐÚNG SOP CỦA ĐÚNG KÊNH (bắt buộc đọc trước mọi task sản xuất)
Dự án chạy **NHIỀU LANE song song**. Trước khi làm bất cứ video nào, chốt profile rồi mới mở SOP.
Vào nhầm lane = bật REF-LOCK cho kênh không có nhân vật (đốt tiền ảnh) hoặc viết văn cụ bà cho
giọng dẫn nam — cả hai đều chạy trót lọt, không báo lỗi, chỉ hỏng ở sản phẩm cuối.

| Anh nói | MÃ LANE (= `id` profile) | Thư mục làm việc | SOP | Thân video |
|---|---|---|---|---|
| "sức khoẻ người già Nhật · kể chuyện đời cá nhân ngôi 1" | `Lopezzapa68` | `assets/out/` | ⚠️ chưa có SOP riêng | Ảnh AI |
| "hưu trí Nhật · manga kịch tính tiền · Lane F · 定年後のリアル" | `teinengo-real` | `assets/teinengo-real/` | ⭐ `docs/BAT_DAU_LANE/teinengo-real.md` (cửa vào) · `docs/SOP_LANE_F.md` (runbook, 2026-09-20) | Manga AI, REF-LOCK 2 nhân vật trong tập |
| "hưu trí Nhật · manga list N選 vui/rẻ · Lane G · 定年後の楽しみ方" | `teinengo-tanoshimi` | `assets/teinengo-tanoshimi/` | ⭐ `docs/BAT_DAU_LANE/teinengo-tanoshimi.md` (cửa vào) · `docs/SOP_LANE_G.md` (runbook, 2026-09-20) | Manga AI, REF-LOCK nhân vật chính trong tập |
| "tâm lý gia đình người già Nhật · 【心理学】 · Lane H · 心の家族学" | `kokoro-kazoku` | `assets/kokoro-kazoku/` | ⭐ `docs/BAT_DAU_LANE/kokoro-kazoku.md` (cửa vào; SOP chưa viết) | Illustration ấm + narration, không REF-LOCK |
| "lịch sử Chiến quốc Nhật · manga chibi · Lane I · 戦国の裏側" | `sengoku-uragawa` | `assets/sengoku-uragawa/` | ⭐ `docs/BAT_DAU_LANE/sengoku-uragawa.md` (cửa vào; SOP chưa viết) | Manga chibi, REF-LOCK nhân vật chính trong tập, documentary |
| "vợ chồng sau hưu trí Nhật · manga cảm xúc · Lane J · 定年後の夫婦のカタチ" | `teinengo-fuufu` | `assets/J-teinengo-fuufu/` | ⭐ `docs/BAT_DAU_LANE/teinengo-fuufu.md` (cửa vào) · `docs/SOP_LANE_J.md` (runbook, 2026-09-30; tên kênh mới J-rougo_futari, mã lane đổi sau) | Manga AI, REF-LOCK 2 nhân vật (vợ chồng) trong tập |
| "công sở/nghề nghiệp Nhật · dược sĩ quả báo · Lane K · 薬局スカッと帳" | `yakkyoku-sukatto` | `assets/yakkyoku-sukatto/` | ⭐ `docs/BAT_DAU_LANE/yakkyoku-sukatto.md` (cửa vào) · `docs/SOP_LANE_K.md` (runbook, 2026-09-24) | Manga AI, khoá mặt N nhân vật/tập (@CAST), ĐA GIỌNG VOICEVOX, bóng thoại có đuôi do máy vẽ |
| "xã hội/tâm lý xã hội Nhật · giải thích bằng số liệu · Lane L · 社会のなぜ研究室" | `shakai_no_naze` | `assets/shakai_no_naze/` | ⭐ `docs/BAT_DAU_LANE/shakai_no_naze.md` (cửa vào) · `docs/SOP_LANE_L.md` (runbook, 2026-09-24) | Anime AI kể chuyện, Sakura khoá mặt XUYÊN TẬP (1 ảnh gốc lane), ĐA GIỌNG ai33, bóng thoại không đuôi do máy vẽ |
| "hưu trí Nhật · manga N選 việc làm thêm tuổi 60 · Lane M · 定年後の穴場ノート" | `teinengo-anaba` | `assets/M-teinengo-anaba/` (thư mục = tên tab) | ⭐ `docs/BAT_DAU_LANE/teinengo-anaba.md` (cửa vào) · `docs/SOP_LANE_M.md` (runbook, 2026-09-26) | Manga chibi AI, ông 田島誠 + vợ 春江 khoá mặt XUYÊN TẬP (`image.fixed_refs`) |
| "đời sống sau nghỉ việc Nhật · manga 1 nhân vật/tập · Lane N · シニアの人生これから" | `senior_korekara` | `assets/N-senior_korekara/` | ⭐ `docs/BAT_DAU_LANE/senior_korekara.md` (cửa vào) · `docs/SOP_LANE_N.md` (runbook, 2026-09-30) | Manga AI bán thực, REF-LOCK trong tập, ĐA GIỌNG 3 clone, ĐỔI NGHỀ nhân vật so video gốc |

**⚡ KÊNH MỚI "thực hiện kênh/lane ABC"** (anh chốt 2026-09-29) → áp NGUYÊN quy trình chuẩn mẫu Lane M ở
`docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` **§00** (model từng bước + field profile bắt buộc + cách copy `teinengo-anaba.json`);
không hỏi lại, không tự đổi model.
**⚡ CÂU LỆNH "thực hiện lane <mã>"** (anh chốt 2026-09-20) → đọc HẾT `docs/BAT_DAU_LANE/<mã>.md` trước khi làm
bất cứ gì: file đó nói tài liệu ở đâu, tab sheet nào, cột gì, làm bước nào trước. Mỗi kênh mới sau khi setup
xong (`tools/channel_branding.py`) BẮT BUỘC có 1 file như vậy + 1 tab sheet (tool tự tạo tab).
⚡ **"làm tập tiếp theo" của 1 lane đã setup xong** (2026-09-29, tránh đốt token đọc lan man) → mở đúng mục
"⚡ ĐỌC NHANH" ở đầu file `BAT_DAU_LANE/<mã>.md`: CHỈ cần đọc mục 4 Giai đoạn 3 + file nó trỏ tới trực tiếp,
KHÔNG cần chain-đọc SOP đầy đủ/CHANNEL_DNA/profile.json — các lệnh pipeline tự đọc chúng, Claude không cần
nạp lại vào context mỗi tập.

**TÊN TAB SHEET = `{Lane}-{tên kênh}` (anh chốt 2026-09-24)** — KHÔNG phải mã lane: `Satori-Lopezzapa68` ·
`E-70dai-kenko` · `F-teinengo-real` · `G-teinengo-tanoshimi` (H/I/J chưa đổi).
Nguồn chân lý: profile `publish.sheet_tab`; tool tra bằng `pipeline/sheet_tab.py` (`--tab` nhận cả tên cũ/mã lane).
Tab ≠ thư mục giao hàng: `CHANEL\<kênh>` giữ tên kênh không tiền tố (`publish.upload_channel`).

**Mỗi tab chat = một lane.** Mã lane chính là `id` trong `profiles/profiles/<mã>.json`, địa chỉ
làm việc chính là `slug_dir` của nó — cả hai đã có sẵn trong code nên không lệch nhau được.
Xưng hô giữa các tab: `@lane:<mã>`. Giao việc: ghi vào `docs/lane_inbox/<mã>.md`.
Danh bạ đầy đủ + khuôn giao việc: **`docs/DANH_BA_LANE.md`**.
⚠️ Giao việc **cấm lấy `E:\CLAUDE\YOUTUBE\h2dev` làm địa chỉ** — mọi lane đều nằm trong đó,
nói vậy là không chỉ được ai. Luôn dùng đường dẫn đầy đủ tới `slug_dir` của lane.

### ⛔ LUẬT ĐƯỜNG DẪN ĐẦY ĐỦ (2026-10-18, anh yêu cầu — luật cứng, không có ngoại lệ)
**Mọi đường dẫn báo cho anh PHẢI là đường dẫn TUYỆT ĐỐI ĐẦY ĐỦ từ ổ đĩa**, ví dụ
`E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep22-izakaya-hitode\XEM_THU_hook_giong_phude_VI.mp4`.
- **CẤM** viết tên file trần (`XEM_THU_hook_giong_phude_VI.mp4`), cấm đường dẫn tương đối
  (`assets/...`, `.\hook\...`), cấm rút gọn `...\hook\clip\clip_01.mp4`.
- Áp dụng cho MỌI thứ anh cần mở: video xem thử, ảnh, clip, file kịch bản, log, thư mục, lệnh cần chạy.
- Đường dẫn đặt trong `code block` hoặc inline code để copy 1 phát là mở được; dùng `\` (Windows)
  vì anh mở bằng Explorer/trình phát trên Windows.
- Nhiều file → mỗi file **một dòng, đường dẫn đầy đủ**, không gộp "xem trong thư mục Y".
- Lệnh trong SOP vốn đã in đường dẫn tuyệt đối (tool tự in) → **dán nguyên văn**, không tự rút gọn lại.
- Vi phạm luật này = báo cáo sai, anh không mở được file → coi như chưa làm xong.

> Sửa 2026-09-11: bảng cũ trỏ lệnh satori/simbot2 sang `Lopezzapa68` — đó là lane KHÁC (ngách
> sức khoẻ người già, `assets/out`); lane satori thật là `satori-jp-obaa` → `assets/satori_jp`.
> **2026-09-29: Lane A (`toshi-densetsu-jp`), D (`irogatatarukioku`), E (`kenko-chiebukuro`) đã BỎ hẳn**
> — xoá toàn bộ assets/profile/SOP/channel_dna liên quan. Ba mã A/D/E coi như đã nghỉ hưu, KHÔNG tái sử
> dụng cho lane mới (tránh nhầm với tài liệu lịch sử còn sót lại nhắc tới 3 mã này).

Không rõ lane → **HỎI**, đừng đoán.

### 🧬 CHANNEL ANALYZER — cách mới để "nắm công thức kênh mẫu", ÁP DỤNG CHO MỌI LANE (2026-09-16)
**⚡ CÂU LỆNH:** anh nói "nghiên cứu/phân tích kênh <tên/URL>" ở bất kỳ tab nào → làm theo ĐÚNG
`docs/QUY_TRINH_NGHIEN_CUU_KENH.md` (quy trình đầy đủ: kiểm đã có chưa → chọn Phương án A
Channel Analyzer hay B SPACE_RESEARCH → việc bắt buộc sau khi có DNA). Phần dưới đây là tóm tắt kỹ
thuật của riêng Phương án A, đọc file trên trước khi làm.

> ⚠️ **Đặt tên bước RIÊNG, KHÔNG dùng B1/B2/B3** — dự án đã dùng B0-B11 cho pipeline sản xuất 1 TẬP
> (B3 = viết kịch bản ở MỌI lane, xem bảng phân vai model phía trên). Channel Analyzer là việc CẤP
> KÊNH (1 lần/kênh, không phải 1 lần/tập) nên đặt tên **K1/K2/K3** để KHÔNG bao giờ trùng — lỗi
> thật đã xảy ra 2026-09-16: 1 lane gọi `retrieve_videos.py` là "B3" trong báo cáo, đọc lẫn với B3
> thật (viết kịch bản) trong cùng bảng, gây hiểu nhầm.

Trước đây MỖI lane tự đọc transcript thô của kênh mẫu (Claude tự tóm tắt trong đầu, không ghi lại,
mỗi tab mới lại phải đọc lại từ đầu). Nay tách việc này ra khỏi Claude bằng 2 tool KHÔNG cần Claude:
`pipeline/channel_analyzer.py` (**K1+K2**: K1 = crawl N video top-view [thuần Python, KHÔNG gọi
Gemini]; K2 = gọi Gemini 3.8 Flash phân tích từng video + tổng hợp thành
`docs/channel_dna/<slug>/CHANNEL_DNA.md` + `VIDEO_ANALYSIS/*.json` [ĐÂY mới là chỗ gọi Gemini]) và
`pipeline/retrieve_videos.py` (**K3**: chọn N video liên quan 1 chủ đề mới, thuần Python KHÔNG LLM,
chạy máy nào cũng được). Thiết kế đầy đủ:
`docs/superpowers/specs/2026-09-16-gemini-channel-analyzer-design.md`.

**2026-09-17 thêm phụ: K1 giờ gom cả Video Tags + Channel Tags** (đọc thẳng HTML YouTube
`ytInitialPlayerResponse.videoDetails.keywords` + `ytInitialData...channelMetadataRenderer.keywords`
qua `pipeline/yt_tags.py`, KHÔNG cần cài extension vidIQ — xem
`C:\Users\admin\.claude\skills\youtube_research_ext.md`) → ghi `docs/channel_dna/<slug>/TAG_STATS.json`
(tag → n_videos/avg_views, sort ưu tiên tag LẶP LẠI nhiều video trước). Đây là bước PHỤ, tắt bằng
`--no-tags`, lỗi mạng/kênh không khai tag chỉ in cảnh báo KHÔNG làm gãy K1/K2. Dùng để: (a) rút bộ
từ khoá ngách đối thủ đưa vào B7 khi viết tags cho video mình, (b) copy `channel_keywords` (Channel
Tags — chủ kênh tự khai) làm gợi ý điền Channel keywords lúc setup kênh mới thay vì hardcode tay.

⛔ **KHÔNG tự chạy lại K1+K2 cho kênh MÁY 2 đã nghiên cứu (máy 2 yêu cầu 2026-09-24)** — tốn quota
Gemini lần hai + hai bản `CHANNEL_DNA.md` có thể lệch nhau. `channel_analyzer.py` đã có cổng tự chặn
(exit 1, in sẵn lệnh copy; `--force` để vượt). Cổng CHỈ chặn khi bản máy 2 dùng được (có
`CHANNEL_DNA.md` **và** `VIDEO_ANALYSIS/*.json`); thiếu thì vẫn chạy + nhắc gửi
`FlowHandoff_local/shared/YEU_CAU_MAY2_*.md`. Kênh máy 1 tự tìm: chạy bình thường.

**K1+K2 chạy được ở BẤT KỲ đâu có Python + mạng** — không bắt buộc phải qua máy 2. Máy 2 chỉ là 1
lựa chọn (gói tự chứa `FlowHandoff_local\shared\channel_analyzer_tool\` + hướng dẫn
`FlowHandoff_local\shared\GIAO_VIEC_MAY2_CHANNEL_ANALYZER.md`, dùng khi muốn tách khỏi máy 1 hoàn
toàn). **Lane cũng có thể tự chạy K1+K2 thẳng trong tab của mình** (Bash gọi `python
pipeline\channel_analyzer.py ...` — đây vẫn là việc THUẦN PYTHON, không phải Claude tự phán xét, nên
KHÔNG vi phạm quy tắc "Claude chỉ làm Bước 1" — công cụ chạy hộ, Claude chỉ bấm nút và đọc log).
Syncthing tự đồng bộ máy 2 về `FlowHandoff_local\results\channel_dna\<slug>\` nếu dùng máy 2; nếu tự
chạy tại máy 1 thì ghi thẳng `--out-dir docs\channel_dna\<slug>\`, khỏi cần bước copy. **K3 lane nào
cũng tự chạy được** tại chỗ, không cần máy 2, không cần mạng/API key.

**Trạng thái từng lane (đã chạy K1+K2 chưa, resume từ đâu)** → dọn sang
**`docs/CHANNEL_ANALYZER_STATUS.md`** (2026-09-29) — đọc file đó, KHÔNG cần đọc ở đây. Quy tắc chung
duy nhất giữ lại ở CLAUDE.md: lane mới viết SOP PHẢI thêm 1 mục §0b theo khuôn
`SOP_TOSHI_DENSETSU_JP.md`/`SOP_SATORI_JP.md` (tránh mỗi lane tự đọc transcript thô 1 kiểu khác nhau).

**Bốn hàng rào chống lẫn lane (đã dựng 2026-09-10, thêm #4 2026-09-16, đừng gỡ):**
1. `profiles.rate_measured()` + `gate_declared()` — kênh chưa đo char_rate hoặc chưa khai `script.gate`
   riêng thì make_video **DỪNG**, thay vì lặng lẽ mượn số của kênh khác (bài học EP4: lệch 20% =
   kịch bản "30 phút" ra 44 phút, viết lại từ đầu).
2. `profile.body.mode` (`ai_images` | `stock_clips`) là **ngã rẽ DUY NHẤT** giữa hai lane trong code.
   Cấm thêm `if profile_id == ...` ở bất cứ đâu khác — khác biệt nào cũng phải thành field profile.
3. `skills/` chỉ giữ bản TỔNG QUÁT (`youtube-script` · `youtube-image-prompts` · `youtube-thumbnail`).
   Bản khoá cứng ngách đã niêm cất ở `skills/_deprecated/` — đừng dùng, đừng sửa.
4. **`CLAUDE.md` LÀ ROUTER MỎNG — cấm viết chi tiết vận hành riêng 1 lane vào đây.** File này nạp
   TOÀN BỘ vào context của MỌI tab, mọi tin nhắn, kể cả tab không liên quan lane đó — mỗi dòng thêm
   vào đây là chi phí trả bởi TẤT CẢ lane khác, mãi mãi. Quy tắc cứng khi viết/sửa `CLAUDE.md`:
   - **Được viết ở đây**: bảng router (tên lane → SOP → thư mục), hàng rào chống lẫn lane, quy tắc
     TOÀN DỰ ÁN áp dụng như nhau cho mọi lane (vd "Claude chỉ làm Bước 1", quy tắc Chrome/Sheet/mail
     của khoá học), hạ tầng DÙNG CHUNG (TTS, ima2, channel_analyzer) — mô tả API/cách gọi CHUNG,
     KHÔNG kèm giọng/voice_id/ví dụ riêng 1 lane cụ thể.
   - **KHÔNG được viết ở đây**: lệnh chạy cụ thể của 1 lane, bẫy/pitfall riêng 1 pipeline, quy ước
     cột sheet của 1 tab kênh, số liệu đo (char-rate/giọng/giá) của 1 lane, quy trình bàn giao riêng
     1 lane — TẤT CẢ những thứ này viết vào **SOP của đúng lane đó** (`docs/SOP_<LANE>.md`), CLAUDE.md
     chỉ giữ 1 dòng trỏ sang.
   - **Bài học có thật (2026-09-16, đọc trước khi định "tiện tay viết thẳng vào đây")**: lúc audit
     phát hiện ~150 dòng chi tiết vận hành CHỈ CỦA Lane A (B5K/B5A, quy trình 3 bước, cột sheet,
     giao hàng) đang nằm lẫn trong CLAUDE.md dưới **nhầm cả tiêu đề "LANE D"** — tab nào đọc lướt
     cũng hiểu sai đang là quy tắc của Lane D. Không phải lỗi ai cụ thể — cứ viết thẳng vào đây vì
     tiện lúc đó là sẽ tới tình trạng này. Dọn lại việc này là việc RIÊNG, đã ghi nhận, chưa làm.
   - **Lane mới bắt buộc đọc quy tắc #4 này TRƯỚC khi viết dòng đầu tiên vào CLAUDE.md** — viết SOP
     riêng của lane trước, CLAUDE.md chỉ thêm 1 dòng bảng router + (nếu cần) 1 dòng trỏ sang mục
     "🧬 CHANNEL ANALYZER" nếu lane có dùng.

## ĐỌC TRƯỚC — CHỈ NHỮNG GÌ THẬT SỰ CHUNG (chi tiết từng lane nằm ở SOP riêng, xem bảng router trên)
- Mỗi lane có SOP riêng trong bảng router ở đầu file — KHÔNG lặp lại ở đây, mở đúng SOP của lane đang làm.
  (17/10/2026: lane Satori `satori-jp-obaa` đã BỎ như A/D/E.)
- `docs/HOC_KHOA_H2DEV.md` — bóc video/transcript bài học h2dev.vn (KHÔNG liên quan sản xuất video,
  chỉ đọc khi cần bóc thêm bài mới; gồm cả pointer sang COURSE_NOTES/VIDEO_NOTES/PROGRESS/catalog).
- `docs/QUY_TRINH_SETUP_KENH.md` — mail nuôi hàng loạt + branding kênh thật + bảng cột sheet GMAIL/NOTE
  (chỉ đọc khi đang MỞ 1 kênh mới, không phải mỗi lần sản xuất video).

## TÀI SẢN DỰ ÁN (assets/)
- `assets/prompts/` — 12 bộ prompt gốc H2Dev theo ngách (triết lý Watts, WW2, kinh tế, nhà máy,
  senior health, Hàn/Nhật...). Dùng làm nền khi viết kịch bản/title/thumb.
- `assets/skills/unpacked/` — 5 Claude Skill của H2Dev: `script-bible-explainer`,
  `image-bible-explainer`, `thumbnail-bible-explainer`, `script-wildlife-survival`,
  `wildlife-motion-prompt-master`. Đây vừa là skill dùng được ngay, vừa là MẪU CHUẨN khi
  tự đóng gói skill cho ngách mới.
- `assets/sheets/` — list kênh đối thủ + nguồn reup Douyin/Bilibili + tool giá rẻ.
- `assets/ww2/` — output pipeline WW2 (mỗi video 1 slug: competitor.txt/script.txt/img/thumb/draft.mp4);
  `_test/` chứa ảnh mẫu đã verify chất B&W tư liệu.

## ⭐ PIPELINE SẢN XUẤT (ngách ACTIVE = SATORI NHẬT — 2026-09-07)
Thị trường ACTIVE = **NHẬT BẢN** (đỡ cạnh tranh, RPM cao — user chốt). Ngách kênh đầu = **Satori (悟り系) câu
chuyện người già** (tiếng Nhật, RPM 8, M4-82/84). Sau khi ra kết quả → nhân bản **Hàn Quốc**. Công thức 70/30.
Quy trình đầy đủ + verify ở `pipeline/README.md`.
- ⚠️ **SKILL YOUTUBE = TỔNG QUÁT + GLOBAL (user chốt 2026-09-08):** đặt ở `~/.claude/skills/` (dùng cho MỌI dự
  án YouTube), tên `youtube-*` theo VAI TRÒ; niche/thị trường/ngôn ngữ = THAM SỐ (không khoá niche vào tên).
  Xem memory `ten-skill-prefix-youtube`. (Đã gộp 6 skill niche satori-jp/ww2 → 4 skill chung.)
- **4 skill tổng quát (global)**: `youtube-script` (kịch bản voiceover-ready mọi ngách, 70/30, char-rate 309,
  giới giọng khớp người kể), `youtube-image-prompts` (prompt ảnh + nhất quán nhân vật: bible→QC→REF-LOCK
  `@REF/@REF2/@GROK`), `youtube-thumbnail` (chữ phủ/cinematic), `youtube-series-builder` (phân tích kênh → độc lập/chuỗi).
- **REF-LOCK + phân tích kênh (simbot2 = RỜI RẠC/độc lập) + chi phí ảnh + giọng đọc** — chi tiết đầy đủ (nhiều
  hơn bản cũ từng nằm ở đây) đã dọn hết sang **`docs/SOP_SATORI_JP.md`** §B5.0/§B4/§PHÂN TÍCH KÊNH TRƯỚC KHI
  LÀM (2026-09-16, cùng đợt dọn Lane A) — đọc đúng file đó, đừng tìm ở CLAUDE.md nữa.
- **WW2 English gác lại làm TEMPLATE** (`skills/*-ww2-*` + prompt gốc) — kích hoạt nếu thêm thị trường Âu Mỹ sau.

## 🎙️ VOICE TRẢ PHÍ: AI33.PRO / OPENSPEAKER (hạ tầng dùng chung)
`AI33_API_KEY`/`AI33_API_KEY_2` (2 tài khoản chạy đan xen, tự xoay vòng trong `pipeline/openspeaker_tts.py`)
+ chi phí đo thật + cơ chế API — chi tiết đầy đủ ở **`docs/HA_TANG_TTS_AI33.md`** (dọn 2026-09-29).
Giọng cụ thể từng kênh khai ở `channels.json` per-kênh, KHÔNG tra ở đây.

## ⛔ THỨ TỰ PROVIDER ẢNH MỌI LANE (anh chốt 10/10/2026 · ẢNH HOOK đổi 16/10)
**ẢNH HOOK (16/10/2026, anh chốt):** Google Flow trên profile Ultra nguyenquoctuan (cổng 9350, cùng tài khoản clip Vids) →
cổng BẬN (tập khác đang giữ profile) hoặc lỗi → **9router** → **gpti2**. Một lệnh làm hết: `pipeline\anh_hook.py <tập>\hook`.
⛔ Các tập KHÔNG chạy profile Ultra song song (khoá `pipeline\khoa_ultra.py`). Chi tiết: `docs\QUY_TRINH_ANH_HOOK_GOOGLE_FLOW.md`.

Các ảnh KHÁC (ảnh cảnh, REF nhân vật, thumbnail nền, khung QC lẻ):
1. **ima2 TRƯỚC TIÊN** (`E:\CLAUDE\GPT_API\ima2_client.py`, server local `127.0.0.1:3333`, 0đ).
2. **Chỉ khi ima2 LỖI** (server không chạy/auth hỏng, 429/bị siết quota, timeout lặp lại, từ chối nội dung,
   ảnh trả về hỏng) → mới sang **gpti2** (skill `gpti2.md`).
3. gpti2 cũng lỗi/hết key → provider khác: ckey (`pipeline\ckey_gen.py`) → vilao.ai → imgstudio.
Ghi rõ provider đã dùng + lý do chuyển (nếu có) vào log/báo cáo tập. Cấm nhảy thẳng sang provider trả tiền khi
chưa thử ima2. Lưu ý: `pipeline\gen_images.py` hiện mặc định gpti2 → ckey, CHƯA có ima2 — tới khi wire xong,
chạy tay qua ima2 trước.

## 🖼️ ẢNH MIỄN PHÍ QUA GPT OAUTH — `ima2` (verify thật 2026-09-12, xem memory `ima2-gpt-oauth-image-gen`)
Lane sinh ảnh **KHÔNG TỐN TIỀN** (ăn quota gói ChatGPT Plus qua Codex CLI OAuth, khác hẳn gpti2/imgstudio/
ramclouds đều trả VNĐ) — **đọc đầy đủ ở skill global `C:\Users\admin\.claude\skills\gpt_api_codex.md`**
(client, setup, đa luồng, bẫy env var, rủi ro scale — toàn bộ chi tiết đã nằm ở skill, không lặp lại ở đây).
Tóm tắt: dùng `E:\CLAUDE\GPT_API\ima2_client.py`, REF-LOCK ngang/tốt hơn `gpti2_edit.py` mà 0đ, đa luồng
8 workers verify OK. Khuyến nghị làm **lane chính REF-LOCK**, giữ `gpti2_edit.py` làm fallback khi bị siết
quota/429 — KHÔNG xoá code gpti2 cũ. Chưa wire vào `pipeline/gen_images.py`.

## 🖼️✅ QC THUMBNAIL ĐỘC LẬP BẰNG GPT-5.6-SOL (verify thật 2026-09-17, mọi lane dùng chung)
Lớp QC THỨ HAI cho thumbnail (khác Gemini/ramclouds đang dùng ở mọi cổng QC khác), qua proxy 9router
LOCAL — **đọc đầy đủ ở `docs/QC_THUMBNAIL_GPT_SOL.md`** (endpoint/model, 2 tool `pipeline/qc_thumbnail_sol.py`
+ `pipeline/gen_thumb_bg_prompt_sol.py`, cách khai form riêng từng lane qua `profile.thumbnail_qc`,
bẫy "lỗi tưởng ở ảnh AI nhưng thật ra ở tool overlay chữ"). Ví dụ đã khai thật: `teinengo-anaba.json`.

## 🛟 GEMINI HỎNG → TỰ RƠI SANG MODEL KHÁC (2026-09-26, mọi lane + CẢ 2 MÁY, không phải khai gì)
Mọi bước dùng `gemini-3.8-flash` nay có lưới, bật sẵn trong `pipeline/llm_client.py` (chữ) +
`pipeline/qc_character.py` (nhìn ảnh). Nhìn ảnh: ramclouds gemini → ns24 deepseek-v4.1-flash →
hhtech glm-5.3-flash → gpt-5.6-sol. **9router tự nhận máy** (máy 1 dùng, máy 2 bỏ qua trong 0,4
giây) nên lưới chạy được ở cả nơi QC ảnh của máy 2. Bảng "bước nào gemini làm gì" · số đo 15 model
rẻ ở 3 proxy · bẫy model-suy-nghĩ ăn hết `max_tokens`: `docs/FALLBACK_GEMINI_SANG_SOL.md`.

## 📝✅ QC KỊCH BẢN ĐỘC LẬP BẰNG GPT-5.6-SOL (verify thật 2026-09-18, mọi lane dùng chung)
Lớp QC THỨ HAI cho KỊCH BẢN (khác Gemini đang dùng ở B3Q/B3F), cùng mô hình với QC thumbnail ở trên
— **đọc đầy đủ ở `docs/QC_SCRIPT_GPT_SOL.md`** (bước **B3S** trong `make_video.py`, tool
`pipeline/qc_script_sol.py`, cách khai `profile.script.sol_qc`, 4 chiến lược sửa REMAKE không cần
viết lại từ đầu, chính sách dừng vòng lặp). Ví dụ đã khai thật: `teinengo-anaba.json`.

## 📝⭐ QUY TRÌNH TẠO KỊCH BẢN CHUẨN MỌI LANE — `script.flow="lean"` (mọi chi tiết đã dọn sang
**`docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md`** + `docs/QUY_TAC_VIDEO_HOOK.md` + `docs/QUY_TAC_GOI_DANG.md`
2026-09-29 — CLAUDE.md chỉ giữ TÊN LUẬT + cổng nào chặn, KHÔNG lặp lại nội dung. Vào lane mới → đọc
đúng 3 file trên (không phải mục này) để lấy field profile cần khai + lệnh chạy + bảng ngoại lệ.**

Danh sách luật đang có hiệu lực (mọi lane trừ khi tự nêu ngoại lệ trong SOP riêng):
1. **Luồng viết** Fable viết đúng ngân sách (S2, ĐÚNG 1 LẦN) → máy đo → Sol chấm → mọi lượt SỬA dùng
   `patch_model` (Opus 5) → khoá SHA256. Lane không khai `flow` chạy luồng cũ.
2. **Soát kịch bản = ChatGPT Web mặc định** (F·G·K·L·M + lane mới) qua `pipeline\soat_kb_gptweb.py`
   (`--lan1` → `--chot` → `--xong`); luật cứng 2-tài-khoản/cổng ở `pipeline\gptweb_pool.py`.
3. **Chặng máy 3 soát kịch bản** (mọi lane TRỪ satori/E/A/D) — `make_video.py` tự dừng sau B3 khoá,
   nhận lại bằng `pipeline\review_may3.py --nhan`, KHÔNG có cửa sau `--from B4`.
4. **Bình luận thật + cung cảm xúc** (mọi lane trừ satori/E/A/D) — đọc `COMMENT_INSIGHT.md` trước khi
   viết; kịch bản đi 3 nhịp KÍCH → GIẢI TOẢ → VỊ THA.
5. **Hook bắt buộc mọi tập**, khoá TRƯỚC S2 bằng `pipeline/hook_stage.py`. Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn)
   (dài ≈ hook gốc) — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Mọi luật hook khác đã bỏ.
6. **Gói đăng — một lời hứa ở 4 chỗ** (tiêu đề/thumbnail/mô tả/hook), cổng tất định `pipeline/qc_goi_dang.py`.
7. **⛔ Cổng S1L** — không lane nào viết được kịch bản nếu chưa qua đủ 5 điều kiện (hook+goi_dang+promise.txt+visual_kind+sfx).
8. **⛔ Hook là VIDEO SINH (Veo/Grok), không phải ảnh render** — ảnh tĩnh là ngoại lệ phải khai
   `script.hook.visual_exception` (2 lane từng dùng ngoại lệ này đã bỏ 2026-09-29 — hiện KHÔNG lane
   nào đang hoạt động khai field này; lane mới cần thì khai, không copy nguyên lý do cũ).
9. **⛔ Hình hook do MÁY 1 làm, máy 2 chỉ ghép** — `dong_goi_may2.py` tự chặn nếu thiếu clip.
10. **⛔ Xong việc máy 1 = phải có `HOOK_TAP.md`** (sinh bằng `pipeline\hook_tap_md.py`) — dự án
    tiêu đề và máy 2 đọc file này để khớp lời hứa với hook.

Nội dung hook: CHỈ theo `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md` (17/10/2026 — kho kiểu hook / 10 nguyên tắc hook cũ không còn là luật viết hook).

## 🎞️ CHUYỂN CẢNH (mọi lane ảnh AI)
⛔ **ẢNH ĐỨNG YÊN HOÀN TOÀN — CẤM zoom/pan/rung (Ken Burns) ở BẤT KỲ mức nào >1.0, không ngoại lệ
lane nào bật `--zoom` >1.0.** `pipeline/assemble.py` default `--zoom 1.0` — chỉ dùng hiệu ứng CHUYỂN
CẢNH (crossfade/zoom-từ-đen/mờ-vào/đẩy ngang/cắt thẳng). Ngoại lệ DUY NHẤT: Lane K `yakkyoku-sukatto`
(phóng chậm ×1,025/cảnh, warpAffine dưới-pixel — `docs/SOP_LANE_K.md` §9) và clip hook Grok/Veo (không
phải zoom giả trên ảnh tĩnh). Đo công thức/dựng theo kênh mẫu → skill
`C:\Users\admin\.claude\skills\video-chuyen-canh\SKILL.md`. Dựng `final_fx.mp4` là việc BƯỚC 3 (agent
khác) — Claude Code chỉ đo công thức + viết `timeline.csv`/spec.

## QUY TẮC LÀM VIỆC DỰ ÁN NÀY
- ⛔ **SÀN NGHỈ KHI ĐỌC (user chốt 2026-10-03, mọi lane):** nghỉ hết câu ≥0,5s, nghỉ cuối đoạn ≥1,0s. Ghim cứng trong `pipeline\pace_audio.py` (`SAN_NGHI_CAU=0.5`, `SAN_NGHI_DOAN=1.1` — đoạn để 1,1 vì là mức F ep08 đã qua B4Q 5,92 chỗ/phút). Lý do: giọng 0.90 làm nhánh tự dò `target_lo` chia hệ số xuống (F ep09: câu 0,33s · đoạn 0,76s) → B4Q 0,12 chỗ nghỉ/phút, trượt; ep08 + ep09 dính liền 2 tập. Sàn đè cả giá trị `voice.pace_*` của hồ sơ; chỉnh tay: `--min-sentence/--min-para`.
0000. ⛔ **VIDEO GỐC TỪNG TẬP — MỌI LANE** (giao bởi `YT-TITLE-RESEARCH`): B2 (`make_video.py::b2_competitor`
   / `brain_channel.py::prepare_video`) **tự động** ghi `video_goc.json` qua `pipeline\video_goc.py` —
   không cần làm gì thêm khi B2 chạy qua 2 hàm đó. Không ghi khi B2 mượn `_khung_nhip.txt` dùng chung
   cả lane (không phải nguồn nội dung tập). Lane không có "video gốc" (vd lane dựng từ ảnh/lịch sử
   thật, không clone 1 video cụ thể) → `video_goc: null`
   kèm lý do, KHÔNG bỏ qua file. Backfill lane/tập cũ: `py -3.13 pipeline\video_goc.py --scan --profile
   <lane> --channel-dna-dir docs\channel_dna\<slug> --channel "<tên kênh mẫu>"` (difflib, KHÔNG BAO
   GIỜ bịa ID khi ratio thấp).
   ⛔ **(19/10, anh chốt) LINK VIDEO GỐC LÊN CỘT T:** bất kỳ tập nào chạy kịch bản thì link video gốc
   (nếu có) **PHẢI** nằm ở **cột T (VIDEO GỐC)** của tab lane. Máy tự ghi 3 mốc, không ai phải nhớ tay:
   B2 (`video_goc.ghi_video_goc` → `pipeline\ghi_cot_video_goc.py::ghi_tu_ep`), đóng gói máy 2
   (`dong_goi_may2.py --job`), backfill (`video_goc.py --scan`). Ghi tay/kiểm tra:
   `py -3.13 pipeline\ghi_cot_video_goc.py --tap <thư mục tập>` (hoặc `--profile <lane> --stt <n>`;
   `--lane <lane>` = backfill cả lane 1 lệnh, đọc sheet 1 lần + ghi `batchUpdate`; thêm `--thu` để chỉ
   xem, `--ghi-de` khi cần đè). Không có video gốc (`video_goc: null`) → KHÔNG ghi
   gì, chỉ in lý do. Lỗi Sheets KHÔNG chặn tập (bổ trợ).
00. ⛔ **CHỖ MÁY 2 TRẢ HÀNG — MỌI NHÁNH ĐỀU CÓ TẦNG LANE:** `results\img_render\<sheet_tab>\<slug>\` ·
   `results\video_render\<sheet_tab>\<slug>\` · `results\channel_dna\<slug kênh mẫu>\` ·
   `results\nghien_cuu\<mã lane>\`. Cấm để `<slug>` nằm thẳng gốc `results\`. **Tên thư mục = tên tab
   sheet** (`publish.sheet_tab`, vd `E-70dai-kenko`), kể cả `CHANEL\` — tra bằng `pipeline\duong_ket_qua.py`,
   cấm hardcode; tài liệu cũ ghi tên khác thì tin theo TRẠNG THÁI ĐĨA THẬT.
   ⚠️ `results\` ở máy 1 là **receiveonly** → cấu trúc do MÁY 2 quyết định: đổi bố cục phải ra đơn cho
   máy 2, máy 1 tự `mv` vô nghĩa (Syncthing kéo bản cũ về) và **xoá mất file thật** (đã mất 4 video Lane
   E kiểu này 25/09). Chi tiết: `docs/QUY_TRINH_GIAO_VIEC_MAY2.md` §6.0.
000. ⛔ **XONG TẬP (phần máy 1) = GHI SHEET NGAY, MỌI lane (anh chốt 2026-09-24):** tab `{Lane}-{kênh}` →
   **cột D (KỊCH BẢN) = `Đã giao máy 2`** (cũ `Done`, đổi 03/10 — `docs/TRANG_THAI_COT_D_K.md`) + **cột H (STATUS-IMG) = `cần ảnh (N ảnh, ~Xđ)`** (= lệnh giao việc để máy 2
   biết mà làm). `pipeline\dong_goi_may2.py --job` tự ghi cả hai; đóng gói tay/làm ngoài công cụ thì phải tự ghi.
0. ⛔ **MỌI chữ tiếng Nhật / tiếng nước ngoài trong báo cáo, bảng, câu hỏi gửi anh PHẢI kèm dịch tiếng Việt
   ngay sau, trong ngoặc** — vd 「六十八歳の私は」 (tôi 68 tuổi). Không có ngoại lệ, kể cả trích 1 từ, tên
   mục, câu trong bảng. Anh chốt 2026-09-24: không dịch thì anh không quyết được.
1. **Công thức nội dung 70/30:** giữ 70% cấu trúc/kịch bản đối thủ + 30% sáng tạo thêm. Output kịch
   bản luôn VOICEOVER-READY (pure prose, không bracket/heading) để dán thẳng vào TTS.
2. **Chọn ngách = chọn từ kho key có sẵn** trong `docs/COURSE_NOTES.md` mục 3 (ưu tiên RPM cao,
   cạnh tranh thấp, có prompt/skill sẵn) hoặc nhân bản thị trường từ kênh đối thủ đang nổ.
3. **Làm ngách mới → đóng gói thành Claude Skill** theo format 5 skill mẫu (SKILL.md: name,
   description trigger song ngữ, 6 phase, golden rules về word-density).
4. **Mật độ từ theo dạng video:** talking/documentary thường 130–150 wpm; dạng visual-heavy
   (wildlife...) chỉ 70–90 wpm.
5. **Hạ tầng sẵn có của mình được phép tái dùng:** tạo ảnh (skill `gpti2.md`, `imgstudio.md`,
   `gpt_api_codex.md`, nanobanana MCP), Google Sheets (skill `mpc_google.md`), đóng exe
   (`tao_tool_exe.md`). Ưu tiên pipeline của mình thay vì tool trả phí bên thứ 3 khi tương đương.
   Research ideal/insight từ YouTube (transcript đối thủ, export comment phân tích khách):
   theo skill `C:\Users\admin\.claude\skills\youtube_research_ext.md` §0 — đường chính KHÔNG cần
   extension: `youtube-transcript-api` + `youtube-comment-downloader` (py -3.13, đã verify chạy
   thật), Claude Code tự tóm tắt/phân tích. Extension gốc tại `E:\CLAUDE\YOUTUBE\EXTENSION` chỉ
   dành cho lúc ngồi xem tay hoặc IP bị block — NGOẠI LỆ: extension NotebookLM (ExtendLM, skill §8)
   đáng cài vào `chrome_profile` khi muốn đổ cả kênh/playlist đối thủ vào NotebookLM làm knowledge
   base hỏi-đáp trích nguồn (NotebookLM không có API công khai; có MCP bridge beta cho Claude Code).
6. **Chính sách 2026 là ràng buộc cứng:** mọi video phải qua bước né lỗi "nội dung không trung thực"
   + "sử dụng lại nội dung" (edit biến đổi, không xuất thô output AI). Khi dính lỗi → dùng bài kháng
   trong module "Xử lý & Kháng lỗi".
7. Kênh/mail vận hành theo checklist mục 5 của `docs/COURSE_NOTES.md` (mail cổ+mới, ngâm kênh,
   add quyền quản lý + mail khôi phục trước khi chạy số lượng).

## LỊCH SỬ DỰ ÁN
Roadmap ban đầu (Chrome profile, chốt ngách, mở Lane A...) đã dọn sang **`docs/LICH_SU_DU_AN.md`**
(2026-09-29) — trạng thái THẬT hiện tại lấy từ bảng router ở đầu file, không lấy từ lịch sử.

## ⛔ CẤM TUYỆT ĐỐI
- **Claude Code (mọi tab/lane) CHỈ LÀM BƯỚC 1 — ĐẦU NÃO**: viết kịch bản, lên phương án, phân loại/
  chọn asset, viết spec thuật toán, kiểm tra/nghiệm thu. Bước 2 (máy 2 vẽ ảnh/Google Flow) và bước 3
  (ghép video, dựng file cuối) do AGENT KHÁC làm — Claude Code dừng ở viết spec tự chứa
  (`docs/GIAO_VIEC_*.md`) rồi bàn giao, KHÔNG tự chạy render/ghép (`final.mp4`, ffmpeg concat/overlay),
  kể cả bản thử trong `scratch_analysis/`. Ngoại lệ 1 khung hình lẻ cho QC vision (`qc_visual._frame`)
  được phép — ghép nhiều khung thành video liên tục thì không.
  - **Ngoại lệ mọi lane**: HÌNH HOOK (máy 1 vẽ ảnh hook + sinh clip Grok + xem thử hook) — không áp
    cho ảnh/ghép thân video.
  - (Ngoại lệ tự-render từng có cho Lane A `toshi-densetsu-jp` đã hết hiệu lực — lane này bỏ 2026-09-29.
    Hiện KHÔNG lane nào đang hoạt động được phép tự chạy bước 2/3.)
  - **Ngược lại**: mọi thứ cần NỘI DUNG (kịch bản/tiêu đề/mô tả/hashtag/prompt ảnh...) BẮT BUỘC bước 1
    viết xong thành file, không để trống cho bước 2/3 "tự sinh" (bước 2/3 là công cụ cơ học, không
    hiểu nội dung — sự cố thật: 2 tập satori lọt tiêu đề/mô tả rỗng, xem memory
    `tieu-de-mo-ta-phai-o-buoc-1`).
  - **Mốc dừng chính xác**: "cho làm tập X" → chạy hết bước 1 (kịch bản, gate, characters.json,
    img_prompts.txt, master REF-LOCK, + phân loại/tải stock nếu hybrid) rồi DỪNG — KHÔNG tự chạy
    `upload-job`/ghi cột `STATUS-IMG` báo "cần ảnh" cho máy 2; đó là hành động RIÊNG cần xác nhận
    thêm. **Ngoại lệ**: sửa/cập nhật job ĐÃ giao rồi (slug đã có trong `jobs\`, chỉ vá dữ liệu) thì
    không cần hỏi lại — xem memory `upload-job-lan-dau-vs-sua-job`.
- KHÔNG `Stop-Process chrome`/`taskkill chrome` toàn bộ (giết luôn cửa sổ cá nhân của anh). Mỗi
  profile dùng `--user-data-dir` riêng = tiến trình tách biệt: chỉ mở thêm cửa sổ cho ĐÚNG profile đó
  hoặc điều hướng qua Playwright CDP trong chính profile đó.
