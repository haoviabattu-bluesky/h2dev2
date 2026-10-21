# HỌC KHOÁ H2DEV.VN — bóc video/transcript khoá học (không liên quan sản xuất video lane)

> Đã dọn khỏi CLAUDE.md 2026-09-16 (không lane nào cần đọc phần này khi sản xuất video — chỉ cần
> lúc bóc thêm bài học mới từ khoá h2dev.vn). Trạng thái: hạ tầng đã dựng xong 2026-09-06, dùng lại
> khi khoá có bài mới (xem `docs/PROGRESS.md`).

## NGHE VIDEO & GHI CHÚ (pipeline đã dựng — `tools/learn_grab.py`)
Video khoá stream qua player mona-cloud, KHÔNG tải trực tiếp được (segment khoá theo phiên; mở thẳng
link → 500/403; `page.on(response)` không bắt được request của iframe OOPIF). Cách chạy được:
1. Mở Chrome profile dự án kèm CDP + tắt cache:
   `chrome.exe --user-data-dir=E:\CLAUDE\YOUTUBE\h2dev\chrome_profile --profile-directory=Default --remote-debugging-port=9345 --disk-cache-size=1 --media-cache-size=1 https://h2dev.vn/learn/study/1`
2. `py -3.13 tools\learn_grab.py "<needle tên bài trong sidebar>" "<phần slug>" "<ten_output>"`
   → tạo `<ten_output>.wav` (audio đầy đủ).
3. `py -3.13 <scratchpad>\transcribe.py <ten_output>.wav <transcript>.txt` (faster-whisper small, vi).
Cơ chế lõi: điều hướng bằng **click sidebar SPA** (KHÔNG goto — chỉ vậy Playwright mới với được iframe);
móc `SourceBuffer.appendBuffer` qua `add_init_script` để lấy đúng media player nạp; phát 16x + đọc chunk
dần; media fMP4 hay re-init giữa chừng → tách theo ranh giới `ftyp`, decode từng phần rồi ghép.
Cần: `imageio-ffmpeg` + `faster-whisper` (đã cài trên Python 3.13). Whisper nghe sai chính tả vài từ tiếng
Việt (mail→"mêu", kênh→"cân", reup→"re-op"...) nhưng nội dung rõ — đọc hiểu theo ngữ cảnh.

## TRUY CẬP KHOÁ HỌC
- Trang học: `https://h2dev.vn/learn/study/1` (SPA Next.js; sidebar "Danh mục bài học" là JS click,
  KHÔNG phải thẻ `<a>`).
- Chrome profile RIÊNG của dự án (đã login sẵn tài khoản hduongwwork@gmail.com, gói PRO):
  ```
  "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir=E:\CLAUDE\YOUTUBE\h2dev\chrome_profile --profile-directory=Default --remote-debugging-port=9345
  ```
  Điều khiển bằng Playwright `connect_over_cdp("http://127.0.0.1:9345")`.
- **Trick bóc data khoá học** (đã dùng thành công): mỗi bài có JSON
  `https://h2dev.vn/learn/_next/data/<BUILD_ID>/study/<slug>.json?slug=<slug>` (fetch trong page
  context kèm credentials). `pageProps.dataCategoryTreeV2.lesson[]` = toàn bộ cây khoá học kèm
  description.html từng bài; `pageProps.lessonDetail` = bài hiện tại. BUILD_ID đổi theo deploy —
  sniff response khi reload trang study để lấy mới. `video_link` của bài PRO luôn `None`
  (stream qua player, không bóc được link trực tiếp).

## ⚠️ BÀI HỌC GRAB (2026-09-06) — tránh lặp lại
- **Output grab ghi ra file BỊ ĐỆM**: đọc trực tiếp (`tail`/`cat`) file task hay thấy RỖNG dù grab
  đang chạy tốt. TUYỆT ĐỐI KHÔNG kill grab vì "output rỗng" → đã lỡ kill 3 lần grab đang chạy ngon
  (M2 ở 65%, M3-03 ở t=1980/1990 ch=480 sát lúc lưu file). Nguồn chân lý = **Monitor (grep vòng lặp)**
  hoặc **chờ completion notification + kiểm file .wav**. Grab video 25–33ph mất ~5–7 phút, cứ chờ.
- **Auto-play sang bài kế**: grab xong player TỰ nhảy sang bài tiếp theo (thường là M4) → tab hiện bài
  KHÁC bài vừa grab. Đây KHÔNG phải học lại/học nhầm. Lọc trùng bằng PROGRESS.md + transcripts/.
- **Bug SCRIPT tag (ĐÃ FIX)**: `sidebar_click` cũ khớp cả `<script>` __NEXT_DATA__ (chứa mọi tiêu đề)
  → click no-op, lạc bài. Đã thêm `tagName!=='SCRIPT'&&tagName!=='STYLE'` vào filter.
- **Đừng pre-navigate tới bài đích rồi grab**: nếu tab đã ở sẵn bài đích, grab re-click = no-op, player
  không re-mount → hook không gắn → **ch=0**. Phải để tab ở bài KHÁC, grab tự nhảy tới (player re-mount
  → hook bắt chunk). Quy trình: move tab sang bài đã học → chạy grab bài mới.
- **Đường dẫn trong Bash tool = dùng `/` KHÔNG dùng `\`** (Git Bash nuốt `\`, làm hỏng path câm lặng).

## 🔄 RESET CHROME KHI GRAB DEGRADATION (giữ login) — 2026-09-06
Sau ~10-12 bài grab liên tục, frame-acquisition chập chờn nặng (NO CONTENT FRAME + hang mid-capture liên
tục, grab_one FAIL cả 3 attempt nhiều lần). Nguyên nhân: phiên Chrome mở lâu + tích luỹ kết nối CDP/
add_init_script. FIX = **khởi động lại RIÊNG Chrome dự án bằng GRACEFUL close (KHÔNG force-kill)** để flush
cookie giữ login h2dev:
1. Đóng graceful qua CDP (KHÔNG taskkill /F — force kill làm MẤT login; taskkill thường KHÔNG đóng được Chrome):
   `py -3.13 -c "from playwright.sync_api import sync_playwright as s;
    b=s().start().chromium.connect_over_cdp('http://127.0.0.1:9345'); b.new_browser_cdp_session().send('Browser.close')"`
   (hoặc inline như đã dùng) → Chrome dự án đóng sạch trong ~1s, cookie được flush.
2. Chỉ lọc tiến trình chrome có cmdline chứa `h2dev*chrome_profile` (KHÔNG đụng Chrome cá nhân).
3. Relaunch: `chrome.exe --user-data-dir=E:\CLAUDE\YOUTUBE\h2dev\chrome_profile --profile-directory=Default
   --remote-debugging-port=9345 --disk-cache-size=1 --media-cache-size=1 --new-window https://h2dev.vn/learn/study/1`
4. Verify login: body KHÔNG chứa "Đăng nhập" + có ~5 cookie h2dev. ĐÃ TEST: login GIỮ NGUYÊN qua graceful close.
→ Làm định kỳ mỗi ~10 bài để grab luôn ổn định.

## TÀI LIỆU LIÊN QUAN (dọn từ CLAUDE.md 2026-09-29)
- `docs/COURSE_NOTES.md` — TOÀN BỘ kiến thức đã bóc từ khoá học (mô hình, quy trình, checklist,
  kho ngách, index tài sản). Mọi task content/kênh phải bám tài liệu này.
- `docs/VIDEO_NOTES.md` — ghi chú CHI TIẾT từng video đã NGHE (nội dung thực, không chỉ tên bài).
- `docs/PROGRESS.md` — sổ theo dõi đã học/chưa học. Học xong bài nào đánh `[x]`, KHÔNG nghe lại.
- `docs/transcripts/` — transcript gốc từng video.
- `docs/catalog.json` — danh mục 131 bài học (tên, slug, thời lượng, FREE/PRO, mô tả).
- `docs/desc_links.json` — toàn bộ link tài nguyên gốc (prompt docs, sheets, drive, tools).
- Khoá học cập nhật key mới liên tục (module 4 hiện 88 video) → định kỳ chạy lại bóc catalog để lấy
  bài mới + prompt mới (so sánh với `docs/catalog.json` cũ).
- Tool hỗ trợ của H2Dev: h2devtool.com (dịch SRT + voice Việt). Hotline/zalo H2Dev: 0777682597.

## TOOL .EXE ĐÓNG GÓI (đang làm, đọc 3 file trước khi code tool)
`docs/REPORT_RAMCLOUDS_HERMES.md` (provider/model nào dùng được, bẫy stream) ·
`docs/AB_SCRIPT_MODELS.md` (A/B thật 8 model + kiến trúc 2 PASS cho bước viết script) ·
`docs/PROFILE_ARCHITECTURE.md` (đa nhân vật: profile JSON per kênh, char-rate đo theo giọng, VOICE_FX).

## ⛔ KHÔNG TỰ RESTART CHROME QUA SCRIPT (2026-09-06)
Restart Chrome tự động (kể cả graceful Browser.close qua script) ĐÃ LÀM MẤT LOGIN h2dev lần 2 (cookie phiên
không flush kịp khi script disconnect + relaunch race). → KHÔNG dùng restart_and_grab tự động. Khi grab
degradation: chịu RETRY/SKIP (đánh dấu revisit), KHÔNG restart Chrome. Nếu thật sự cần restart, PHẢI hỏi
user trước + user tự đăng nhập lại. (Lần restart TAY thủ công trước đó may giữ được login nhưng KHÔNG đáng
tin — mỗi lần đóng Chrome là 1 lần rủi ro mất phiên học.)
