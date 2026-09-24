# DỰ ÁN: HỌC & LÀM YOUTUBE THEO QUY TRÌNH H2DEV

Mục tiêu: học khoá h2dev.vn → xây kênh YouTube faceless view ngoại (RPM cao), sản xuất nội dung
bằng AI theo quy trình của khoá, tiến tới hệ thống nhiều kênh.

## 🚦 ROUTER LANE — LÀM ĐÚNG SOP CỦA ĐÚNG KÊNH (bắt buộc đọc trước mọi task sản xuất)
Dự án chạy **NHIỀU LANE song song**. Trước khi làm bất cứ video nào, chốt profile rồi mới mở SOP.
Vào nhầm lane = bật REF-LOCK cho kênh không có nhân vật (đốt tiền ảnh) hoặc viết văn cụ bà cho
giọng dẫn nam — cả hai đều chạy trót lọt, không báo lỗi, chỉ hỏng ở sản phẩm cuối.

| Anh nói | MÃ LANE (= `id` profile) | Thư mục làm việc | SOP | Thân video |
|---|---|---|---|---|
| "video satori · người già · nhân bản simbot2" | `satori-jp-obaa` | `assets/satori_jp/` | `docs/SOP_CLONE_BRAIN.md` (não Claude) · `docs/SOP_SATORI_JP.md` (não ramcloud) | Ảnh AI + REF-LOCK |
| "video 都市伝説 · vũ trụ · bí ẩn · Lane A" | `toshi-densetsu-jp` | `assets/toshi-densetsu-jp/` | `docs/SOP_TOSHI_DENSETSU_JP.md` | **Clip stock** (0đ), ảnh AI CHỈ cho thumbnail |
| "ảnh chiến tranh tô màu · 色が語る記憶 · Lane D" | `irogatatarukioku` | `assets/irogatatarukioku/` | ⭐ `docs/SOP_LANE_D.md` (runbook đầy đủ, 2026-09-16) | Ảnh thật WW2 tô màu AI (`ima2`, miễn phí — fallback `gpti2_edit.py` quality=medium khi ima2 bị siết quota) |
| "sức khoẻ người già Nhật · kể chuyện đời cá nhân ngôi 1" | `Lopezzapa68` | `assets/out/` | ⚠️ chưa có SOP riêng | Ảnh AI |
| "sức khoẻ người già Nhật · liệt kê kiểu bác sĩ giải thích · Lane E · 健康の知恵袋" | `kenko-chiebukuro` | `assets/kenko-chiebukuro/` | `docs/SOP_LANE_E.md` | Ảnh AI minh hoạ (không REF-LOCK, mỗi mục 1 người khác nhau) |
| "hưu trí Nhật · manga kịch tính tiền · Lane F · 定年後のリアル" | `teinengo-real` | `assets/teinengo-real/` | ⭐ `docs/BAT_DAU_LANE/teinengo-real.md` (cửa vào) · `docs/SOP_LANE_F.md` (runbook, 2026-09-20) | Manga AI, REF-LOCK 2 nhân vật trong tập |
| "hưu trí Nhật · manga list N選 vui/rẻ · Lane G · 定年後の楽しみ方" | `teinengo-tanoshimi` | `assets/teinengo-tanoshimi/` | ⭐ `docs/BAT_DAU_LANE/teinengo-tanoshimi.md` (cửa vào) · `docs/SOP_LANE_G.md` (runbook, 2026-09-20) | Manga AI, REF-LOCK nhân vật chính trong tập |
| "tâm lý gia đình người già Nhật · 【心理学】 · Lane H · 心の家族学" | `kokoro-kazoku` | `assets/kokoro-kazoku/` | ⭐ `docs/BAT_DAU_LANE/kokoro-kazoku.md` (cửa vào; SOP chưa viết) | Illustration ấm + narration, không REF-LOCK |
| "lịch sử Chiến quốc Nhật · manga chibi · Lane I · 戦国の裏側" | `sengoku-uragawa` | `assets/sengoku-uragawa/` | ⭐ `docs/BAT_DAU_LANE/sengoku-uragawa.md` (cửa vào; SOP chưa viết) | Manga chibi, REF-LOCK nhân vật chính trong tập, documentary |
| "vợ chồng sau hưu trí Nhật · manga cảm xúc · Lane J · 定年後の夫婦のカタチ" | `teinengo-fuufu` | `assets/teinengo-fuufu/` | ⭐ `docs/BAT_DAU_LANE/teinengo-fuufu.md` (cửa vào; SOP chưa viết) | Manga AI, REF-LOCK 2 nhân vật (vợ chồng) trong tập |
| "công sở/nghề nghiệp Nhật · dược sĩ quả báo · Lane K · 薬局スカッと帳" | `yakkyoku-sukatto` | `assets/yakkyoku-sukatto/` | ⭐ `docs/BAT_DAU_LANE/yakkyoku-sukatto.md` (cửa vào) · `docs/SOP_LANE_K.md` (runbook, 2026-09-24) | Manga AI, khoá mặt N nhân vật/tập (@CAST), ĐA GIỌNG VOICEVOX, bóng thoại có đuôi do máy vẽ |
| "xã hội/tâm lý xã hội Nhật · giải thích bằng số liệu · Lane L · 社会のなぜ研究室" | `shakai_no_naze` | `assets/shakai_no_naze/` | ⭐ `docs/BAT_DAU_LANE/shakai_no_naze.md` (cửa vào) · `docs/SOP_LANE_L.md` (runbook, 2026-09-24) | Anime AI kể chuyện, Sakura khoá mặt XUYÊN TẬP (1 ảnh gốc lane), ĐA GIỌNG ai33, bóng thoại không đuôi do máy vẽ |

**⚡ CÂU LỆNH "thực hiện lane <mã>"** (anh chốt 2026-09-20) → đọc HẾT `docs/BAT_DAU_LANE/<mã>.md` trước khi làm
bất cứ gì: file đó nói tài liệu ở đâu, tab sheet nào, cột gì, làm bước nào trước. Mỗi kênh mới sau khi setup
xong (`tools/channel_branding.py`) BẮT BUỘC có 1 file như vậy + 1 tab sheet (tool tự tạo tab).

**TÊN TAB SHEET = `{Lane}-{tên kênh}` (anh chốt 2026-09-24)** — KHÔNG phải mã lane: `A-shinya_shiryoshitsu` ·
`Satori-Lopezzapa68` · `E-70dai-kenko` · `F-teinengo-real` · `G-teinengo-tanoshimi` (H/I/J chưa đổi; Lane D chưa có tab).
Nguồn chân lý: profile `publish.sheet_tab`; tool tra bằng `pipeline/sheet_tab.py` (`--tab` nhận cả tên cũ/mã lane).
Tab ≠ thư mục giao hàng: `CHANEL\<kênh>` giữ tên kênh không tiền tố (`publish.upload_channel`).

**Mỗi tab chat = một lane.** Mã lane chính là `id` trong `profiles/profiles/<mã>.json`, địa chỉ
làm việc chính là `slug_dir` của nó — cả hai đã có sẵn trong code nên không lệch nhau được.
Xưng hô giữa các tab: `@lane:<mã>`. Giao việc: ghi vào `docs/lane_inbox/<mã>.md`.
Danh bạ đầy đủ + khuôn giao việc: **`docs/DANH_BA_LANE.md`**.
⚠️ Giao việc **cấm lấy `E:\CLAUDE\YOUTUBE\h2dev` làm địa chỉ** — mọi lane đều nằm trong đó,
nói vậy là không chỉ được ai. Luôn dùng đường dẫn đầy đủ tới `slug_dir` của lane.

> Sửa 2026-09-11: bảng cũ trỏ lệnh satori/simbot2 sang `Lopezzapa68` — đó là lane KHÁC (ngách
> sức khoẻ người già, `assets/out`); lane satori thật là `satori-jp-obaa` → `assets/satori_jp`.
> Lane D cũng đã có profile `irogatatarukioku` chứ không còn "CHƯA CÓ".

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

**Lane NHẬN dữ liệu (từ máy 2 hoặc tự chạy) rồi RESUME từ bước nào:**

| Lane | `docs/channel_dna/` | Kênh mẫu | SOP đã có §0b? | Resume từ |
|---|---|---|---|---|
| `toshi-densetsu-jp` | ✅ `imayamo-toshidensetsu` (đã mở rộng 8→**28 video** trong phiên, xem `run_log.txt`) | 今夜も都市伝説 `UCoFEha9rNMFqUio-4GQITfw` | ✅ `SOP_TOSHI_DENSETSU_JP.md` §0b | Chạy K3 (`retrieve_videos.py`) rồi vào §2 B2-tư-liệu như cũ |
| `satori-jp-obaa` | ✅ `simbot2` (mới 4 video test — nên chạy lại `--n-videos 8` khi rảnh) | simbot2 `@simbot2` | ✅ `SOP_SATORI_JP.md` §0b | Chạy K3 rồi vào B1-chọn-chủ-đề như cũ |
| `irogatatarukioku` (Lane D) | 🔄 đang chạy trực tiếp trên máy 1 (2026-09-16, không qua máy 2 — hợp lệ, xem lưu ý trên) | 色でたどる戦争の記録 `UCaj1dslbibbHEnOAOh0tyYw` (xem `docs/laneD_from_research/LANE_D_HANDOFF.md`) | Xem `docs/SOP_LANE_D.md` (đã có, kiểm lại §0b) | Kiểm kết quả K1+K2 xong chưa, cập nhật dòng này |
| `yakkyoku-sukatto` (Lane K) | ✅ `yakkyoku-sukatto` (4 video, 2026-09-24) | 千種テンカ `UCEBA1RFfkXQtqgiDVLh4bcw` | ✅ `SOP_LANE_K.md` §0b | Chạy K3 rồi vào §2 của SOP |
| `shakai_no_naze` (Lane L) | ✅ `shakai-no-naze` (8 video + số đo thật, 2026-09-24) | 社会のウラガワ `UCFWFKb3Yr_1SrAT0kcvwFdw` | ✅ `SOP_LANE_L.md` §0b | Chạy K3 rồi vào §2 của SOP |
| `Lopezzapa68` | ❌ chưa chạy | **CHƯA RÕ** — chưa có kênh mẫu nào được xác nhận trong tài liệu dự án | ❌ chưa có SOP | Hỏi user kênh mẫu trước khi chạy `channel_analyzer.py`, đừng tự đoán/bịa URL |

**Quy trình nhận hàng (mọi lane, cả 2 cách — qua máy 2 hoặc tự chạy tại máy 1):** nếu qua máy 2,
Syncthing tự đưa kết quả về `FlowHandoff_local\results\channel_dna\<slug>\` → copy nguyên thư mục đó
sang `docs/channel_dna/<slug-đúng-tên-trong-bảng-trên>/`; nếu tự chạy tại máy 1 thì đã sẵn ở đúng chỗ
rồi, khỏi copy. Sau đó chạy `retrieve_videos.py` tại chỗ (K3) → đọc `CHANNEL_DNA.md` + kết quả
retrieval thay cho việc tự đọc transcript thô như trước. K3 không cần mạng/API key nên lane nào cũng
tự chạy được ngay khi có `VIDEO_ANALYSIS/*.json`.

**Lane mới sau này (khi viết SOP mới):** bắt buộc thêm 1 mục §0b theo đúng khuôn của
`SOP_TOSHI_DENSETSU_JP.md`/`SOP_SATORI_JP.md` — đây là nguyên tắc chung, không phải tuỳ chọn, để
tránh lặp lại tình trạng "mỗi lane tự đọc transcript thô một kiểu khác nhau".

### ✅ LANE D — SẢN XUẤT ĐANG CHẠY, đọc `docs/SOP_LANE_D.md` (không phải mục này)
Lane D đã có kênh thật (色が語る記憶 · `UCtRuxojb7218QeFBf5TBCQQ`), profile `irogatatarukioku.json`,
giọng đã đo (Koji, 276,3 chữ/phút), và **runbook đầy đủ `docs/SOP_LANE_D.md`** (2026-09-16) — 7 tập
đã qua bước 1, 5 tập đã giao hàng. `LANE_D_HANDOFF.md` giờ chỉ còn giá trị lịch sử/bối cảnh nghiên
cứu kênh mẫu ban đầu — đọc `SOP_LANE_D.md` để lấy lệnh chạy thật, đừng copy lệnh từ HANDOFF.

### ✅ LANE A (toshi-densetsu-jp) — SẢN XUẤT ĐANG CHẠY, đọc `docs/SOP_TOSHI_DENSETSU_JP.md`
Quy trình 2 chặng chống đốt tiền khi máy 2 vẽ ảnh (§6d), phân việc Haiku/Sonnet + bàn giao bước 3
(§8e), quy ước số tập/cột sheet/giao hàng B11 (§8e) — **dọn khỏi CLAUDE.md 2026-09-16, đọc đúng file
SOP**, đừng tìm ở đây nữa (bài học: từng nằm lẫn dưới nhầm tiêu đề "LANE D" ở đúng chỗ này).

**Anh đưa 1 kênh / 1 video và bảo "làm video theo cái này" → gọi skill global `youtube-produce`**
(runbook 6 pha: nghiên cứu kênh → lập profile + đo char-rate → hồ sơ đề tài → chạy pipeline →
thumbnail theo mô-típ kênh → file đăng tải). Nội dung do dự án research bên ngoài đưa sang thì phải
đúng khuôn `docs/KHUON_HO_SO_DE_TAI.md` — pipeline ăn thẳng, không phải hỏi lại.

**NGUỒN TƯ LIỆU cho Lane A = dự án `E:\CLAUDE\YOUTUBE\SPACE_RESEARCH`** (chạy 24/7, chuyên đào đề
tài + dữ kiện đã kiểm chứng). Quy trình giao–nhận đầy đủ: **`docs/GIAO_VIEC_SPACE_RESEARCH.md`**
(dùng chung cho MỌI lane, không riêng Lane A).

**NGUỒN NGÁCH MỚI (Lane E/F/G...) = dự án `TRENDING-RESEARCH` (máy khác), giao qua Syncthing —
KÊNH TRUYỀN KHÁC HẲN SPACE_RESEARCH (không qua Sheet/`_READY`).** ⚠️ Bài học trả giá thật
2026-09-16: Syncthing ở máy này **CHỈ sync đúng 4 thư mục** `FlowHandoff_local\{jobs,results,shared}`
+ `CHANEL` — **`h2dev\docs\` KHÔNG nằm trong sync**. Máy kia ghi hồ sơ nghiên cứu đầy đủ (handoff
`.md` + report `.html` + Channel DNA `.json` + `data/` transcript/comment/thumbnail thật) vào
`docs\laneX_from_research\` bên máy NÓ thì máy này **không bao giờ thấy** — chỉ nhận được đúng 1
file tóm tắt việc (`shared\GIAO_VIEC_LANE_X.md`) mà tưởng thế là đủ, thiếu hẳn phần dữ liệu gốc để
kiểm chứng "số liệu phải có nguồn thật". Quy ước ĐÚNG (đã áp dụng cho E/F/G): hồ sơ NẶNG (chiều
2→1, máy kia gửi sang) đặt ở **`FlowHandoff_local\results\laneX_from_research\`**; chỉ file tóm tắt
việc cần làm đặt ở `FlowHandoff_local\shared\GIAO_VIEC_LANE_X.md` và trỏ đường dẫn tuyệt đối vào
đúng thư mục `results\laneX_from_research\` ở trên. Nhận việc lane mới → **luôn kiểm tra file tóm
tắt trỏ đúng vào `results\`, đừng tin theo path `docs\...` nếu file đó ghi vậy** (path cũ trong
handoff có thể là path bên máy nghiên cứu, không phải path ăn được ở máy này).

**⚡ CÂU LỆNH: "tạo nội dung gửi space research để hỗ trợ tìm kiếm thông tin"**
(hoặc bất kỳ cách nói nào mang nghĩa "giao việc nghiên cứu cho dự án kia") → làm ĐỦ 3 việc, KHÔNG
hỏi lại nếu chat này chỉ đang làm một lane:
1. Khai/kiểm khối `research` trong profile của lane đang làm (chưa có thì khai, ngưỡng **đo từ
   kênh tham chiếu của chính lane này**, cấm chép từ lane khác).
2. `py -3.13 pipeline\don_dat_hang.py --profile <lane>`
3. **Trả về cho anh ĐÚNG MỘT DÒNG đường dẫn để copy**, dạng
   `E:\CLAUDE\YOUTUBE\SPACE_RESEARCH\DON_DAT_HANG_<lane>.md`
Chat đang chạy NHIỀU lane cùng lúc thì mới hỏi lane nào. Đơn tự chứa mọi ngưỡng — anh chỉ việc đưa
đường dẫn sang chat của dự án kia, không phải giải thích gì thêm.

Tóm tắt vòng nhận hàng: chờ cột D của trang tính `gid=612920013` ghi **`DONE-READY`** → **chạy cổng
B0 trước khi động vào bất cứ thứ gì**:
```
py -3.13 pipeline\qc_hoso.py --folder "<...>\_READY\<nn>-<slug>" --profile <lane>
```
B0 ĐẠT mới copy vào thư mục tập rồi chạy `make_video.py`. B0 TRƯỢT thì **trả lại bên đó kèm danh
sách, KHÔNG tự sửa hộ** (tự sửa hộ = tập sau sai y hệt). Làm xong **chuyển thư mục hồ sơ sang
`_DONE\`** để bên đó không đào lại.

Hợp đồng của mỗi lane khai ở **`profile.research`**, cổng B0 đọc thẳng khối đó làm ngưỡng — sửa
hợp đồng là sửa JSON, **không sửa `qc_hoso.py`**. Lane không khai `research` = lane không nhận
hàng nghiên cứu (vd satori: chuyện cảm xúc, không có dữ kiện cần kiểm chứng).
Ranh giới: bên đó CHỈ nghiên cứu, bên này CHỈ làm video — đừng viết kịch bản ở đó, đừng đào tư liệu ở đây. Lane mới thì thêm 1 dòng vào bảng này + 1 SOP riêng; TUYỆT ĐỐI
không nhét vào SOP của lane đang có.

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

## ĐỌC TRƯỚC
- ⭐ `docs/SOP_SATORI_JP.md` — **RUNBOOK CHUẨN sản xuất 1 video Satori Nhật (8 bước, có lệnh copy-paste).**
  Khi anh nói "làm video satori/Nhật mới" hoặc "nhân bản video <url> sang Nhật" → CHẠY THEO file này,
  KHÔNG tìm hiểu/dựng lại. Chuẩn cứng: làm GIỐNG bản gốc simbot2 (25-30', ~90-120 ảnh, thumbnail chữ to).
- ⭐ `docs/SOP_TOSHI_DENSETSU_JP.md` — **RUNBOOK Lane A (都市伝説/vũ trụ/bí ẩn, Nhật, kể tài liệu).**
  Nghiên cứu ngách đầy đủ ở `docs/laneA_from_research/` (63 tiêu đề · 4 transcript · 190 comment ·
  12 thumbnail). Khác satori 4 chỗ: KHÔNG nhân vật lặp (bỏ REF-LOCK) · giọng nam trầm 374,9 chữ/phút ·
  thân video là CLIP STOCK · 5 chương 第◯章 với chương 4 luôn móc về Nhật Bản.
- ⭐ `docs/SOP_CLONE_BRAIN.md` — **RUNBOOK nhánh "não Claude"** (`brain_channel.py` → `claude -p` →
  `render_engine.py`), khác hẳn nhánh não-ramcloud `make_video.py`. Chốt 2026-09-11 sau 8 lượt chạy
  thật. **Nguyên tắc lớn nhất: Claude VIẾT — máy ĐO và NẮN** (`gate_check.py` đo, `fix_gate.py` nắn;
  Claude không đếm được ký tự khi đang sinh chữ — đã thử dặn 4 vòng đều thất bại, chỉ giao cho máy
  mới xong: 26 phút tự cắt → 2,4 phút máy nén). Kèm bảng 13 lỗi đã vá + số đo thời gian/chi phí thật.
- `docs/COURSE_NOTES.md` — TOÀN BỘ kiến thức đã bóc từ khoá học (mô hình, quy trình, checklist,
  kho ngách, index tài sản). Mọi task content/kênh phải bám tài liệu này.
- ⭐ **TOOL .EXE (đang làm, 2026-09-07)** — đọc 3 file này trước khi code tool:
  `docs/REPORT_RAMCLOUDS_HERMES.md` (provider/model nào dùng được, bẫy stream) ·
  `docs/AB_SCRIPT_MODELS.md` (A/B thật 8 model + kiến trúc 2 PASS cho bước viết script) ·
  `docs/PROFILE_ARCHITECTURE.md` (đa nhân vật: profile JSON per kênh, char-rate đo theo giọng, VOICE_FX).
- `docs/VIDEO_NOTES.md` — ghi chú CHI TIẾT từng video đã NGHE (nội dung thực trong video, không chỉ tên bài).
- `docs/PROGRESS.md` — sổ theo dõi đã học/chưa học. Học xong bài nào đánh `[x]`, KHÔNG nghe lại.
- `docs/transcripts/` — transcript gốc từng video.
- `docs/catalog.json` — danh mục 131 bài học (tên, slug, thời lượng, FREE/PRO, mô tả).
- `docs/desc_links.json` — toàn bộ link tài nguyên gốc (prompt docs, sheets, drive, tools).

## HỌC KHOÁ H2DEV.VN (bóc video/transcript bài học — KHÔNG liên quan sản xuất video)
Đã dọn sang **`docs/HOC_KHOA_H2DEV.md`** (2026-09-16) — cách grab video khoá học, truy cập, bài học
Chrome/grab degradation. Chỉ đọc khi cần bóc thêm bài mới từ h2dev.vn, không liên quan lane nào.

## TRANG TÍNH VẬN HÀNH (Google Sheet mặc định của dự án)
- URL: `https://docs.google.com/spreadsheets/d/1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU/edit?gid=0#gid=0`
- Spreadsheet ID: `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU`
- Tab làm việc mặc định: **`GMAIL`** (tên tab thật trong sheet là GMAIL — anh hay gõ "GAMIL", cùng 1 tab).
- Thứ tự cột A→L (**đọc lại header dòng 1 ngay trước khi ghi** — đã 2 lần ghi nhầm cột vì tin bảng này,
  16/09 và 20/09; `tools/channel_setup.py::col(svc, "TÊN KÊNH")` tra cột theo TÊN, cấm hardcode chữ cái):
  | Cột | Tên | Ghi chú thực tế (kiểm tra lại 2026-09-20) |
  |---|---|---|
  | A | STT | trạng thái tay: "Da login" / "Đã có kênh" / "kháng"... |
  | B | MAIL | địa chỉ Gmail |
  | C | FULLMAIL | format `mail\|pass\|app-password 8 nhóm 4 ký tự` |
  | D | MAIL\|PASS ACC | format `mail\|app-password 4 nhóm 4 ký tự` |
  | E | NGÀY REG | lẫn 2 kiểu: `7/2024` (tháng/năm) và `dd/mm/yyyy` |
  | F | PHONEVER | số điện thoại verify + link OTP — KHÔNG phải tên kênh |
  | G | TÊN KÊNH | **handle `@...`** (anh chốt: chỉ ghi handle) — điền khi setup kênh |
  | H | NGÀY TẠO KÊNH | `dd/mm/yyyy` |
  | I | NGÁCH | vd "Người già/Hưu trí Nhật (manga story)" |
  | J | THỊ TRƯỜNG | vd "NHẬT BẢN" |
  | K | KÊNH_CLONE | URL kênh mẫu |
  | L | GHI CHÚ | |
- Tab **NOTE** (danh sách kênh mẫu đã nghiên cứu, 1 dòng = 1 lane): A STT · B KÊNH (URL mẫu) · C NGÁCH ·
  D ĐIỂM · E FORMAT · F TÌNH TRẠNG · G NHẬN KÊNH · H MAIL · I HANDLE · J LANE · K PHÂN TÍCH KÊNH ·
  **L KÊNH (= @handle kênh mình, ghi khi setup xong để biết dòng đó đã làm)**.
- Trạng thái lúc kiểm tra: header dòng 1, **dòng 2 trống**, data từ dòng 3 → 16 (14 mail: mix mail
  cổ 2024–2025 và mail mới 2026, đúng chiến lược mail cổ+mới của khoá). Cột C/D chứa app password —
  KHÔNG log/paste ra nơi công khai.
- Thao tác sheet qua MCP `gsheets` (skill `mpc_google.md`). Nhắc lại quy tắc cứng toàn cục:
  **TUYỆT ĐỐI KHÔNG xoá dòng/cột/dữ liệu trong Google Sheet** — chỉ đọc/ghi thêm/cập nhật ô.

## SETUP KÊNH (mail nuôi + branding kênh thật)
Đã dọn sang **`docs/QUY_TRINH_SETUP_KENH.md`** (2026-09-16) — chỉ đọc khi đang MỞ 1 kênh mới
(`tools/channel_setup.py` cho mail nuôi hàng loạt, checklist branding A+B bắt buộc cho kênh thật).

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

## 🎙️ VOICE TRẢ PHÍ: AI33.PRO / OPENSPEAKER (đã mua gói + verify API 2026-09-07)
ai33.pro = **OpenSpeaker** (openspeaker.ai) — proxy ElevenLabs/MiniMax/Fish/Vbee giá $5/1.000.000 credit.
Đã mua gói, tài khoản ~1.003.209 credit. Voice trả phí CHÍNH cho satori (chất ElevenLabs); edge-tts free
trong `pipeline/tts.py` giữ làm fallback. **Đã đóng gói API mechanics đầy đủ thành skill dùng chung mọi
dự án:** `C:\Users\admin\.claude\skills\openspeaker_voice_clone.md` (endpoint, poll pattern, voice-clone,
pitfall UTF-8/curl — không lặp lại ở đây, đọc skill).
- **API key:** `AI33_API_KEY=sk_vdplz671t7nq190rwxrwd52lj30z1giekav30rh0mkaqzleo` (header `xi-api-key`,
  KHÔNG có prefix Bearer). Base: `https://api.openspeaker.ai`.
- **Chi phí đo thật:** 49 chữ Nhật = 62 credit. Video 30' ~10k chữ ≈ 13k credit → gói $5 ≈ 75–90 video
  30' (~1.500đ/video). Task fail tự hoàn credit.
- **Giọng đang dùng cho satori-jp-obaa: xem `docs/SOP_SATORI_JP.md` §B4** (hệ thống `channels.json`
  per-kênh, KHÔNG chép giọng cụ thể vào đây — dễ lệch khi đổi kênh/giọng mà quên sửa 2 chỗ).

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
bẫy "lỗi tưởng ở ảnh AI nhưng thật ra ở tool overlay chữ"). Ví dụ đã khai thật: `kenko-chiebukuro.json`.

## 📝✅ QC KỊCH BẢN ĐỘC LẬP BẰNG GPT-5.6-SOL (verify thật 2026-09-18, mọi lane dùng chung)
Lớp QC THỨ HAI cho KỊCH BẢN (khác Gemini đang dùng ở B3Q/B3F), cùng mô hình với QC thumbnail ở trên
— **đọc đầy đủ ở `docs/QC_SCRIPT_GPT_SOL.md`** (bước **B3S** trong `make_video.py`, tool
`pipeline/qc_script_sol.py`, cách khai `profile.script.sol_qc`, 4 chiến lược sửa REMAKE không cần
viết lại từ đầu, chính sách dừng vòng lặp). Ví dụ đã khai thật: `kenko-chiebukuro.json`.

## 📝⭐ QUY TRÌNH TẠO KỊCH BẢN CHUẨN MỌI LANE — `script.flow="lean"` (chốt 2026-09-20)
Lane mới/lane muốn đổi sang luồng gọn (Fable viết đúng ngân sách → máy đo → Sol lời cuối → patch ≤2 → khoá SHA256 → Claude Code
đọc bản khoá → sheet D = `Done`) → đọc **`docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md`** (field profile cần khai, khuôn `series_ctx.txt`,
lệnh chạy, 3 trạng thái, kênh `viec_tay.txt`). Thiết kế + số đo: `docs/QUY_TRINH_KICH_BAN_GON.md`. Lane không khai `flow` chạy luồng cũ y nguyên.
**Quy tắc phân vai model (anh chốt 2026-09-22, mọi lane `engine: claude_p`): model VIẾT (`brain_model`, Fable) chạm kịch bản
ĐÚNG 1 LẦN ở S2; mọi lượt SỬA (S4/B3S FIX/B3R FIX) = `patch_model` (Opus 5); Sol chỉ chấm.** Lane mới PHẢI khai cả 2 field —
chi tiết + bảng vai ở file trên §0a.
**HOOK 20–30s bắt buộc mọi tập (2026-09-23):** khoá TRƯỚC S2 bằng `pipeline/hook_stage.py`, đọc
`docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b; phương án gốc `docs/PHUONG_AN_HOOK_VIDEO.md`.
**GÓI ĐĂNG — MỘT LỜI HỨA ở 4 chỗ (tiêu đề · thumbnail · câu đầu mô tả · 30–45s đầu hook), chốt
2026-09-23:** luật G1–G8 + cổng tất định `pipeline/qc_goi_dang.py` (0 LLM, 0đ) → đọc
`docs/QUY_TAC_GOI_DANG.md`. Ngưỡng riêng từng lane khai ở `profile.goi_dang` kèm `_nguon`.
⛔ **CỔNG S1L — KHÔNG LANE NÀO VIẾT ĐƯỢC KỊCH BẢN NẾU CHƯA QUA (anh chốt 2026-09-24):** năm điều kiện
`script.hook.enabled: true` · `goi_dang.enabled: true` · `promise.txt` (1 câu) trong thư mục tập ·
`script.hook.visual_kind: "video_sinh"` · `script.hook.sfx: true`.
Trượt = DỪNG trước khi tốn lượt LLM nào (`qc_goi_dang.cong_truoc_khi_viet`, gọi ở CẢ luồng lean và
luồng cũ). Lời hứa còn được nhồi vào prompt của model VIẾT để nó viết đúng ngay lần đầu, thay vì
chấm-rồi-sửa. Lý do phải thành cổng: luật hook chốt 23/09 mà tới 24/09 mới có 3/6 lane bật công tắc —
luật nằm trong tài liệu thì phải có người nhắc mới chạy.

⛔ **HOOK LÀ VIDEO SINH, KHÔNG PHẢI ẢNH RENDER (anh chốt 2026-09-24, mặc định MỌI KÊNH kể cả chưa
lập):** hook dựng từ **Google Flow (Veo) hoặc Grok Imagine**, như `satori-jp-obaa` đã chạy thật
(`ep3-sougi`). Ảnh tĩnh/clip stock là NGOẠI LỆ, phải khai `script.hook.visual_exception` ghi lý do —
hiện chỉ `toshi-densetsu-jp` + `irogatatarukioku` (bán sự thật có hồ sơ, clip AI phá `credits.txt`).
**Hiệu ứng âm thanh BẮT BUỘC** (`script.hook.sfx`). **Kịch bản phải đổi theo clip** — 20–30s đầu chỉ
được dùng cảnh dựng nổi thành clip 5–6s; luật này tự nhồi vào prompt model VIẾT, không phải dặn tay.
Chi tiết + bảng nguồn hình từng lane: `docs/QUY_TAC_VIDEO_HOOK.md` §5b.

⛔ **HÌNH HOOK DO MÁY 1 LÀM, MÁY 2 CHỈ GHÉP (anh chốt 2026-09-24, MỌI lane — đang làm, chưa làm, tập đã làm):**
máy 1 vẽ ảnh hook (gpti2) + sinh clip hook (hiện: Grok free, tài khoản ở tab **GROK**, 1 clip/tài khoản/ngày)
+ QC (`pipeline/qc_hook_clip.py`: mỗi cảnh phải thấy MẶT + cảm xúc đúng) + SFX → giao máy 2 KÈM ĐỦ
`hook\{img,clip,sfx,qc}` + `hook_timeline.json`; `dong_goi_may2.py` tự gói và DỪNG nếu thiếu clip.
Máy 2 không vẽ/không sinh clip hook. Chi tiết: `docs/QUY_TAC_VIDEO_HOOK.md` §0.

⛔ **XONG VIỆC MÁY 1 = PHẢI GỬI KÈM FILE HOOK TEXT (anh chốt 2026-09-24, mọi lane):**
`<thư mục tập>\HOOK_TAP.md` — dự án tiêu đề `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH` **và máy 2** đọc file
này để viết tiêu đề · mô tả · chữ thumbnail cùng MỘT lời hứa với hook. Sinh/nghiệm thu:
`py -3.13 pipeline\hook_tap_md.py --slug <tập> --profile <lane>` (máy rút phần tất định; chỗ
`<<CẦN NGƯỜI:…>>` là bước 1 phải tự viết). Cổng chặn ở `dong_goi_may2.py` + B10 — thiếu file hoặc còn
chỗ chưa viết là KHÔNG giao được. Chi tiết: `docs/QUY_TAC_VIDEO_HOOK.md` §0b.

**Dựng CLIP hook (ảnh → clip Grok 6s → ghép vào đầu video cũ): `docs/QUY_TAC_VIDEO_HOOK.md`** — 7 bước, 4 thứ phải khớp (mức tiếng/fps/kiểu phụ đề/điểm nối), bảng kiểu hook từng lane. Nguyên tắc nội dung (10 nguyên tắc + khung 9 kênh mẫu): `C:\Users\admin\.claude\skills\youtube-hook-research\references\NGUYEN_TAC_HOOK_GOI_DANG.md`.

## 🎞️ CHUYỂN CẢNH — skill toàn cục `video-chuyen-canh` (2026-09-20, mọi lane ảnh AI dùng chung)
⛔ **ẢNH ĐỨNG YÊN HOÀN TOÀN — TUYỆT ĐỐI KHÔNG zoom/pan/rung dưới bất kỳ hình thức nào (chốt
2026-09-21, nâng lên mức tuyệt đối, áp dụng MỌI LANE, không còn ngoại lệ Lane E cũ):** Ken Burns
(dù mạnh hay nhẹ) gây cảm giác giật/rung nhức mắt khi xem nhiều ảnh liên tiếp — **CẤM DÙNG, ở BẤT
KỲ mức zoom nào >1.0**, kể cả khi bàn giao cho agent bước 3 dựng video. Chỉ được phép dùng **hiệu
ứng CHUYỂN CẢNH** giữa 2 ảnh (crossfade/xfade, zoom-từ-đen, mờ-vào, đẩy ngang, cắt thẳng — xem skill
`video-chuyen-canh` bên dưới); các option Ken Burns tồn tại trong công cụ (assemble.py `--zoom`,
`ghep_anh_co_chuyen_canh.py --zoom-mode/--pulse-*`) phải luôn để giá trị TẮT (`--zoom 1.0`), không
lane nào được bật lại, kể cả Lane E (`docs/SOP_LANE_E.md` cần đọc lại theo mốc mới này). Lane
mới/agent bước 3 nhận việc dựng video phải đọc đúng dòng này trước khi chọn tham số `--zoom`.
- `pipeline/assemble.py` đã đổi default **`--zoom 1.0`** (2026-09-21): ảnh tĩnh tuyệt đối, bỏ hẳn
  filter `zoompan` khi zoom≤1.0 (không chỉ đặt hệ số 0) — code thật ở `render_clip()`.
- **Ngoại lệ Lane K `yakkyoku-sukatto` (anh chốt 2026-09-24, CHỈ lane này):** phóng vào chậm ×1,025/cảnh giống kênh mẫu đo máy, dựng bằng warpAffine dưới-pixel (không rung) — chi tiết `docs/SOP_LANE_K.md` §9. Lane khác vẫn cấm.
- **Ngoại lệ hook (2026-09-23, xem §2b ở mục kịch bản trên):** 20–30s đầu là CLIP sinh sẵn (Grok/Veo)
  theo storyboard — không phải zoom/pan giả trên ảnh, không vi phạm luật ảnh tĩnh ở trên.

Muốn video có nhịp như kênh mẫu → gọi skill `C:\Users\admin\.claude\skills\video-chuyen-canh\SKILL.md`:
- "đo công thức chuyển cảnh của <video>" → `scripts/do_chuyen_canh.py`, ghi mục mới vào
  `references/cong-thuc-da-do.md` (§1 = kênh POV Hàn đã đo, §2 = chính ep08 của lane D).
- "dựng tập X có chuyển cảnh theo công thức <tên>" → sinh `timeline.csv` từ `anchor_durations`/
  `sync_durations` của `pipeline/assemble.py`, chạy `scripts/ghep_anh_co_chuyen_canh.py --zoom 1.0
  --fit blur --fit-audio` + tham số trong references (LUÔN giữ `--zoom 1.0`, bỏ mọi `--zoom-mode`/
  `--pulse-*` khác mặc định), xuất `final_fx.mp4` CẠNH final.mp4 (không ghi đè), rồi đo lại nghiệm
  thu: số khung = timeline, số khung đen = số zoom-từ-đen trong kế hoạch.
- Clip Veo/Grok đã dựng sẵn → `scripts/them_chuyen_canh_vao_clip.py` (giữ nguyên tổng khung).
Chưa nối vào make_video.py — muốn nối thì thêm `transition: "mix"` vào khối `assemble` của profile
và rẽ nhánh ở `b8_assemble`, giữ nguyên nhánh xfade cũ.
⚠️ Nhắc rào "Claude chỉ làm Bước 1": việc dựng `final_fx.mp4` là bước 3 — Claude Code chỉ đo công thức,
sinh `timeline.csv` và viết spec; chạy ghép là việc của agent bước 3.

## QUY TẮC LÀM VIỆC DỰ ÁN NÀY
00. ⛔ **CHỖ MÁY 2 TRẢ HÀNG — MỘT CHỖ DUY NHẤT, MỌI LANE (chốt 2026-09-24):**
   `FlowHandoff_local\results\video_render\<publish.upload_channel>\<slug>\` (vd lane E:
   `results\video_render\kenko-chiebukuro\<slug>\`). KHÔNG theo tên tab sheet (tên tab đổi được), KHÔNG
   `results\<slug>\`. Nguồn chân lý = dòng TRẢ HÀNG trong `_BANGIAO.txt` do `pipeline\dong_goi_may2.py` sinh —
   viết đơn/SOP/giao việc nào cũng CHỈ chép dòng đó, cấm tự gõ đường dẫn khác. Chi tiết: `docs/QUY_TRINH_GIAO_VIEC_MAY2.md` §6.
000. ⛔ **XONG TẬP (phần máy 1) = GHI SHEET NGAY, MỌI lane (anh chốt 2026-09-24):** tab `{Lane}-{kênh}` →
   **cột D (KỊCH BẢN) = `Done`** + **cột H (STATUS-IMG) = `cần ảnh (N ảnh, ~Xđ)`** (= lệnh giao việc để máy 2
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

## LỘ TRÌNH (cập nhật trạng thái tại đây)
- [x] Tạo Chrome profile + login khoá học (2026-09-06)
- [x] Bóc toàn bộ catalog + prompt + skill + sheet nguồn (2026-09-06)
- [ ] Anh xem 5 video cốt lõi (list ở COURSE_NOTES mục 7) — em bóc thêm chi tiết thao tác từng bài
- [x] **Chốt ngách: WORLD WAR II HISTORY (English, view ngoại US/UK/CA/AU)** (2026-09-07) — RPM cao,
      có prompt WW2 sẵn, sản xuất hàng loạt ảnh tĩnh + TTS. Xem `pipeline/README.md`.
- [x] **Dựng pipeline WW2** (2026-09-07): 3 skill (`skills/youtube-script`, `youtube-image-prompts`,
      `youtube-thumbnail`) + tool `pipeline/` (fetch_script.py bóc kịch bản đối thủ · gpti2_gen.py + gen_images.py
      gen ảnh B&W 2560x1440 đã VERIFY chất tư liệu · assemble.py Ken Burns). CÒN TTS (chốt sau).
- [x] **Mở LANE A: 都市伝説/vũ trụ/bí ẩn (JP)** (2026-09-10) — profile `toshi-densetsu-jp` (giọng nam
      trầm 374,9 chữ/phút đo thật), tool mới `stock_cut.py` (dựng thân video bằng clip stock, 0đ) +
      `qc_numbers.py` (cổng số học), SOP riêng `docs/SOP_TOSHI_DENSETSU_JP.md`, router lane ở đầu file này.
      **Video 1 (多元宇宙) đã dựng xong**: 29:30 · 408 cảnh · 9 cảnh ảnh bằng chứng có chú thích nguồn ·
      B8Q ĐẠT — `assets/toshi-densetsu-jp/ep01-tagen-uchu/` (chưa đăng, chờ anh duyệt).
- [ ] Setup mail + kênh theo checklist module 1, bắt đầu ngâm kênh
- [ ] Chốt TTS (ElevenLabs/edge-tts) + chạy thử 1 video WW2 hoàn chỉnh (đo thời gian/chi phí)
- [ ] Đăng đều, theo dõi chỉ số, áp ngưỡng bỏ/giữ kênh
- [ ] Nhân bản sang kênh/thị trường thứ 2

## LƯU Ý
- Khoá học cập nhật key mới liên tục (module 4 hiện 88 video) → định kỳ chạy lại bóc catalog để
  lấy bài mới + prompt mới (so sánh với `docs/catalog.json` cũ).
- Tool hỗ trợ của H2Dev: h2devtool.com (dịch SRT + voice Việt). Hotline/zalo H2Dev: 0777682597.

## ⛔ CẤM TUYỆT ĐỐI
- **Claude Code (mọi tab/lane) CHỈ LÀM BƯỚC 1 — ĐẦU NÃO: viết kịch bản, lên phương án, phân loại/
  chọn asset, viết spec thuật toán, kiểm tra/nghiệm thu (anh chốt 2026-09-16).**
  **⭐ NGOẠI LỆ MỌI LANE (2026-09-24): HÌNH HOOK** — máy 1 được vẽ ảnh hook + sinh clip hook (Grok) +
  dựng bản xem thử hook; KHÔNG áp cho ảnh/ghép thân video. Xem mục hook phía trên.
  **⭐ NGOẠI LỆ ĐÃ CHO PHÉP: lane `toshi-densetsu-jp` (Lane A) — anh chốt 2026-09-21, tab
  Lane A được tự tải kho stock, tự vẽ ảnh gpti2 (bước 2) VÀ tự chạy render/ghép `final.mp4` (bước 3)
  cho CHÍNH lane này. Chi tiết + lý do xem `docs/SOP_TOSHI_DENSETSU_JP.md` §Ngoại lệ tự render.
  KHÔNG áp dụng cho bất kỳ lane nào khác — lane khác vẫn theo đúng luật CẤM dưới đây, không suy diễn
  "Lane A làm được thì lane mình cũng làm được".**
  ⭐ **NGƯỢC LẠI, chính vì bước 2/3 chỉ là công cụ cơ học (không hiểu nội dung), MỌI thứ cần NỘI DUNG
  hay tiêu chuẩn thẩm mỹ (kịch bản, tiêu đề, mô tả, hashtag, mốc chương, prompt ảnh...) BẮT BUỘC bước
  1 viết xong và để lại thành file, KHÔNG được để trống rồi trông chờ bước 2/3 tự sinh** (chốt
  2026-09-17 sau sự cố thật: 2 tập lane satori-jp-obaa lọt tới người xem với tiêu đề/mô tả rỗng vì
  bước 3 tưởng phải tự viết mà công cụ đó không hiểu nội dung — xem
  `docs/SOP_SATORI_JP.md` §B7b + memory `tieu-de-mo-ta-phai-o-buoc-1`). TUYỆT ĐỐI KHÔNG tự
  chạy render/ghép video (dựng `final.mp4` hoặc bất kỳ bản mix nào bằng ffmpeg concat/overlay) — kể
  cả bản thử nghiệm trong `scratch_analysis/`. Bước 2 (máy 2 vẽ ảnh AI hàng loạt qua Google Flow) và
  bước 3 (ghép video, dựng file cuối) đều do MODEL/AGENT KHÁC đảm nhận (Hermes/DeepSeek, xem
  `docs/GIAO_VIEC_BUOC3_AGENT.md` + `docs/QUY_TRINH_RENDER_VIDEO.md`). Việc của Claude Code dừng ở
  viết **spec/thuật toán tự chứa** (file `docs/GIAO_VIEC_*.md`/`docs/TRAO_DOI_*.md`, có công thức,
  ngưỡng số, bước tuần tự rõ ràng đủ để agent khác code theo mà không hỏi lại) rồi bàn giao — không
  tự viết compositor và bấm chạy nó. Trích xuất 1 khung hình lẻ để QC vision (`qc_visual._frame`) là
  ngoại lệ chấp nhận được (không phải "dựng video"); ghép nhiều clip/ảnh thành 1 file video liên tục
  thì không.
  **⚠️ Mốc dừng chính xác (anh nhắc lại 2026-09-16): khi anh nói "cho làm tập X", Claude Code CHỈ
  được chạy tới HẾT bước 1 (viết kịch bản, gate, characters.json, img_prompts.txt, master REF-LOCK,
  và nếu là lane hybrid thì thêm phân loại/tải/nghiệm thu stock) rồi DỪNG — TUYỆT ĐỐI KHÔNG tự chạy
  `drive_handoff.py upload-job`, KHÔNG tự ghi cột `STATUS-IMG`/`F` báo "cần ảnh" để giao việc cho máy
  2.** Bước giao việc máy 2 (upload-job + ghi cột F) là một hành động RIÊNG, chỉ làm khi anh xác nhận
  thêm lần nữa (kiểu "giao luôn sang máy 2" như đã làm với STT1) — không suy luận "xong bước 1 thì
  giao luôn cho liền mạch".
  **⚠️ Phạm vi rào này (chốt 2026-09-16 sau vụ ep06 — xem memory `upload-job-lan-dau-vs-sua-job`):
  chỉ áp dụng cho lần GIAO MỚI đầu tiên của 1 tập** (thư mục `FlowHandoff_local\jobs\<slug>\` CHƯA
  từng tồn tại). Chạy lại `upload-job`/`ghi_don_buoc3.py` để **sửa/cập nhật job ĐÃ giao rồi** (slug
  đã có sẵn trong `jobs\`, chỉ vá lại dữ liệu — vd sau khi sửa `tim_anh_that.py`) thì KHÔNG cần hỏi
  lại mỗi lần — đó là vá cho quyết định đã chốt, không phải quyết định giao mới.
- KHÔNG được `Stop-Process chrome` / `taskkill chrome` / kill toàn bộ Chrome. Việc đó đóng luôn các
  cửa sổ Chrome cá nhân của anh (đã gây sự cố 2026-09-06). Profile dự án dùng `--user-data-dir` riêng
  = tiến trình tách biệt: chỉ mở thêm cửa sổ/tab cho ĐÚNG profile đó (`--new-window` với đúng
  `--user-data-dir=...\chrome_profile`) hoặc điều hướng qua Playwright CDP trong chính profile đó.
  Nếu cần tab "sạch" cho grab: mở tab mới trong profile dự án, KHÔNG kill Chrome.

(Bài học grab/reset Chrome khi bóc khoá học — xem `docs/HOC_KHOA_H2DEV.md`, không liên quan lane nào.)
