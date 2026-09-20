# GHI CHÚ GIÁO TRÌNH H2DEV — "Quy Trình Thực Chiến Và Key Làm YOUTUBE"

> Nguồn: https://h2dev.vn/learn/study/1 — tài khoản hduongwwork@gmail.com (gói PRO).
> Thu thập ngày 2026-09-06 bằng cách bóc data Next.js của trang học (131 bài / 10 module, ~24.6 giờ video).
> File này là ghi chú KIẾN THỨC. Quy tắc vận hành dự án xem `../CLAUDE.md`.

## 1. MÔ HÌNH KINH DOANH CỐT LÕI

Xây kênh YouTube **faceless** (không quay phim, không lộ mặt, không vốn lớn) nhắm **view ngoại**
(US / Nhật / Hàn / Canada...) vì RPM cao hơn view Việt 5–10 lần (số liệu khoá học: RPM 6–15$ ở các
ngách Nhật/US so với ~2$ view Việt). Mục tiêu chuẩn: **build kênh đến bật kiếm tiền trong ~21 ngày**.

Hai lane sản xuất nội dung:

| Lane | Cách làm | Rủi ro chính |
|---|---|---|
| **REUP** | Lấy video từ Douyin / Bilibili (hoạt hình, câu cá, du lịch, cam cảnh sát...), edit lại (khung, tốc độ, ghép, vietsub/sub thị trường đích) rồi đăng | Lỗi "sử dụng lại nội dung" / bản quyền → có bài kháng riêng |
| **BÁN CONTENT AI** (nội dung tự sản xuất bằng AI) | Kịch bản bằng Claude/ChatGPT (prompt train sẵn) → giọng đọc TTS (ElevenLabs/Minimax) → ảnh AI (Whisk/Flow/Dreamina/nano banana) → edit + thumbnail | Lỗi "nội dung không trung thực" (inauthentic content, chính sách 2026) → có kỹ thuật edit né quét AI |

**Tư duy trung tâm — "NHÂN BẢN THỊ TRƯỜNG":** tìm 1 kênh/ngách đang nổ view ở thị trường A,
clone nguyên format sang thị trường B (US→Việt, Hàn→Nhật, Trung→US...). Không bao giờ thiếu ngách vì
mỗi ngách × mỗi thị trường = 1 cơ hội mới. Kịch bản thì "xào nấu": **giữ 70% kịch bản đối thủ + 30%
sáng tạo thêm** — đây là công thức lặp lại trong TẤT CẢ prompt của khoá.

## 2. CẤU TRÚC KHOÁ HỌC (131 video / 10 phần)

| # | Module | Video | Thời lượng | Nội dung lõi |
|---|---|---|---|---|
| 0a | Bắt đầu — Cộng đồng & Hỗ trợ | 2 | 9m | Group VIP, khám kênh học viên |
| 0b | Xử lý & Kháng lỗi kênh | 6 | 22m | Kháng "sử dụng lại nội dung"/trùng lặp/gậy bản quyền (99% về bờ); tạo Adsense an toàn không bị quét |
| 1 | **Nền tảng & Setup kênh chuẩn** (BẮT BUỘC) | 12 | 1h30 | Chọn mail (mới+cổ), kênh (mới+cổ) có trust; full setup 2026: tạo kênh → cài đặt → SEO từ khoá kênh/video/mô tả → **ngâm kênh** + xác minh trust; nuôi nhiều mail/kênh 1 thiết bị không dính spam (KHÔNG cần VPN/proxy); add quyền quản lý + mail khôi phục chống die hàng loạt; ngưỡng bỏ kênh (bao nhiêu video không lên thì bỏ); fix lỗi nội dung không trung thực |
| 2 | **Tự tìm Key/Ngách & Phân tích đối thủ** | 1 | 22m | Tư duy tìm/lọc key view ngoại, xác định key trends, key ngon (video FREE quan trọng nhất về phương pháp luận) |
| 2b | **Quy trình dùng Claude AI làm YouTube** | 4 | 2h36 | Chọn bản web/app + gói Claude; train prompt bất kỳ ngách nào; **đóng gói SKILL** để viết kịch bản/tạo ảnh/tạo thumb; quy trình bám 70% kịch bản đối thủ; Prompt Master nhân bản mọi thị trường |
| 3 | Tự train Prompt | 3 | 1h29 | Tự phân tích kênh đối thủ → tự tạo prompt cho chủ đề bất kỳ |
| 4 | **VIP - Share key thực chiến** (cập nhật liên tục) | 88 | 12h42 | Kho ngách cụ thể nhiều thị trường + hướng dẫn edit từng ngách (danh sách ngách ở mục 3 dưới) |
| 5 | Edit video & Thumbnail A-Z | 6 | 3h35 | Clone thumb giống 100% đối thủ (font, phong cách); edit key Chill Dude (người que), triết lý/khắc kỷ, Nonagon |
| 6 | Mẹo chống gãy view & die kênh | 4 | 44m | Khắc phục gãy view; bám key đối thủ để không bao giờ 0 view; edit né quét AI/không trung thực; trick test bản quyền trước khi reup douyin |
| 7 | Nhân bản thị trường & hệ thống kênh | 1 | 43m | Tư duy scale nhiều kênh |
| 8 | Công cụ & Tài nguyên | 4 | 14m | h2devtool.com (dịch phụ đề SRT, voice Việt Ngọc Huyền), 6 bộ tool free, tài khoản ElevenLabs/Minimax/ChatGPT giá rẻ |

Full danh mục 131 bài (tên, slug, thời lượng, tag, FREE/PRO, mô tả): `docs/catalog.json`.

## 3. KHO NGÁCH (KEY) ĐÃ ĐƯỢC SHARE — theo thị trường

- **US/Canada/Anh:** triết lý Alan Watts (khắc kỷ), WW2 history, lịch sử quân sự ($100k/tháng case),
  quy luật kinh tế (Economy Rewind style), quy trình/nhà máy sản xuất (How It's Made style),
  sức khoẻ người già 55–80 (senior health), Bible explainer ("Every X Explained"), kiểm soát sinh học
  – chiến thuật – tâm lý, wildlife AI documentary, ngách triết lý US.
- **Hàn Quốc:** đứa trẻ/야담 truyện cổ ngủ ngon (구름야담 style, audiobook 70–90 phút), kinh tế,
  sức khoẻ, Đức Phật & Chúa, triết lý Hàn.
- **Nhật Bản:** drama, truyện + stories + triết lý, tâm linh/luật hấp dẫn, sức khoẻ, kinh tế (RPM 6–15).
- **Việt:** key sinh tồn, cam cảnh sát (nguồn douyin), reup vietsub, triết lý.
- **REUP đa thị trường:** hoạt hình Trung Quốc (Douyin/Bilibili), câu cá "vạn cân", du lịch, animation Douyin trends.

## 4. QUY TRÌNH SẢN XUẤT 1 VIDEO (lane AI content — rút từ bộ prompt)

1. **CHỦ ĐỀ:** prompt "Topic Creator" theo ngách → [X] title theo archetype đã kiểm chứng
   (vd WW2: Shock/Disbelief, Mockery→Reversal...; Watts: nghịch lý 6–12 từ).
2. **KỊCH BẢN:** prompt "Script Creator" — 2 chế độ:
   - Tự sáng tác theo persona (vd "You are Alan Watts himself"), 2500–5000 từ, sinh theo chunk
     800–1200 từ, lệnh `CONTINUE`/`TIẾP TỤC` từng phần, kết thúc `END`/`Script Completed`.
   - Xào nấu: dán full script đối thủ → giữ 70% + thêm 30% (chia 10–15 part × 1000–1100 từ).
   - Mật độ từ khác nhau theo dạng: talking ~130–150 wpm; wildlife documentary chỉ **70–90 wpm**
     (hình ảnh gánh 70%).
3. **GIỌNG ĐỌC:** output phải VOICEOVER-READY (không bracket/annotation) → ElevenLabs / Minimax clone.
4. **HÌNH ẢNH:** prompt tạo 8–10 image prompt/section (cinematic, documentary, --ar 16:9, no text
   overlay) → Whisk / Flow (Veo) / Dreamina / nano banana; nguồn video free: pixabay, vecteezy.
5. **EDIT:** CapCut; theo module 5 + các mẹo né quét (khung, ghép, biến đổi); reup thì test bản quyền trước.
6. **THUMBNAIL + SEO:** prompt thumb (3–5 concept, text 2–4 từ, palette đỏ/vàng/trắng/xám) +
   5 title <70 ký tự + 10 keywords + 10 hashtags; clone 100% phong cách thumb đối thủ.
7. **ĐĂNG:** SEO từ khoá kênh/video/mô tả theo chính sách 2026 (bài riêng module 1).

## 5. SETUP & NUÔI KÊNH — CHECKLIST RÚT GỌN (module 1)

- Mail: kết hợp **mail mới + mail cổ** (mail cổ có trust); kênh: **kênh mới + kênh cổ**.
- Tạo kênh → cài đặt kênh → SEO từ khoá kênh → **ngâm kênh** (xem/tương tác như người thật,
  tương tác kênh đối thủ cùng ngách) → xác minh trust ngay từ khi build.
- Nuôi nhiều mail/kênh trên cùng 1 thiết bị: có tút phân chia riêng, KHÔNG cần fake VPN/proxy.
- Add quyền quản lý kênh + mail khôi phục → tránh Google quét die hàng loạt; Adsense cũng add quyền dự phòng.
- Ngưỡng quyết định: có bài dạy "bao nhiêu video không lên là bỏ" + đọc chỉ số giữ lại làm tiếp.
- Khi dính lỗi: dùng các bài kháng (reused content, trùng lặp, gậy bản quyền — "99% về bờ").

## 6. TÀI SẢN ĐÃ TẢI VỀ (assets/)

### assets/prompts/ — 12 bộ prompt gốc (Google Docs của H2Dev)
| File | Ngách / thị trường |
|---|---|
| PROMPT NGÁCH NHỎ TRIẾT LÝ | Alan Watts / US (title + script persona Watts) |
| PROMPT KEY WORLD WAR II HISTORY | WW2 / US (4 archetype title) |
| PROMPT NGÁCH QUY LUẬT KINH TẾ | Economy Rewind style / US (70/30 rewrite) |
| PROMPT KEY QUY TRÌNH/NHÀ MÁY SẢN XUẤT | Industrial process / US ("Inside the...") |
| PROMPT NGÁCH ĐỨA TRẺ | 야담 truyện cổ Hàn — sleep audiobook 70–90 phút (prompt tiếng Hàn) |
| PROMPT: NGÁCH KINH TẾ - THỊ TRƯỜNG HÀN | Kinh tế / Hàn |
| PROMPT: NGÁCH Kiểm soát sinh học - chiến thuật - tâm lý | US, update 26/02/2026 |
| PROMPT TRAIN | Bộ 3 prompt lõi: xào kịch bản 70/30 + tạo image prompt + thumb/SEO (news-documentary) |
| PROMPT TRAIN NGÁCH TIỀN SỬ | Prehistoric |
| Prompt Key Nhật | Thị trường Nhật |
| Prompt + tài nguyên ngách nhỏ phật pháp | Phật pháp / Hàn |
| PROMPT THUMB + TỪ KHÓA SEO KEY SENIOR | Senior health 55–80 / US (title trigger "Doctors Warn:"...) |

### assets/skills/ — 5 Claude Skill đóng gói sẵn của H2Dev (đã unpack ở unpacked/)
- `script-bible-explainer` V2.1 — kịch bản Bible 25 phút "Every X Explained", 6 phase, voiceover-ready.
- `image-bible-explainer`, `thumbnail-bible-explainer` — ảnh + thumb cùng ngách.
- `script-wildlife-survival` — wildlife documentary photoreal, 6-beat formula, 70–90 wpm, prompt Flow/Veo 3.1.
- `wildlife-motion-prompt-master` — prompt video motion cho ngách wildlife.

### assets/sheets/ — 6 sheet nguồn tài nguyên
- `list link kênh key ở video ytb` — kênh YouTube đối thủ mẫu (WW2Tales, RealHowNotToDie, Biblehaven...).
- `LIST KÊNH NGUỒN REUP DOUYIN`, `LIST KÊNH DOUYIN NGUỒN TÀI NGUYÊN REUP` (kèm web tải douyin HD
  không logo: tikvideo.app, snapdouyin.app, snapvideotools.com), `NGUỒN VIDEO REUP DOUYIN + BILIBILI`,
  `LIST NGUỒN KÊNH/VIDEO KEY CAM CẢNH SÁT` (key Việt).
- `TOOL VÀ TÀI KHOẢN GIÁ RẺ` — ElevenLabs, Minimax clone, dịch SRT... (liên hệ zalo 0777682597).

### Tool online của H2Dev
- **h2devtool.com** — tool dịch phụ đề SRT chuyên vietsub/reup + voice tiếng Việt "Ngọc Huyền" (free).
- Drive 4 file mẫu edit/thumb key Nonagon (link trong `docs/desc_links.json`).

## 7. NHỮNG GÌ CHỈ CÓ TRONG VIDEO (chưa bóc được bằng text)

Video PRO stream qua player (không có link tải trực tiếp trong data). Các bài QUAN TRỌNG cần
anh xem/em nghe cùng để bóc chi tiết thao tác:
1. Module 1 bài 03 (20:02) — full quy trình setup kênh 2026.
2. Module 1 bài 04 (03:21) — SEO từ khoá kênh/video/mô tả.
3. Module 2 (22:38, FREE) — tư duy tìm/lọc key.
4. Module 2b bài 02 (1h12) — train prompt + đóng gói Skill bằng Claude.
5. Module 6 bài 03 (11:55) — edit né quét AI/không trung thực.

→ Khi học tới bài nào, có thể mở bài đó trong Chrome profile của dự án rồi nhờ em bóc thêm
(em đọc được DOM/notes/bình luận; hoặc anh bật video em chụp màn hình từng đoạn).
