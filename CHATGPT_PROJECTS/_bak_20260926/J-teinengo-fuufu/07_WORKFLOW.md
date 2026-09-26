> BẢN NHÁP 2026-09-26 — lane chưa có tập nào; luật rút từ kênh mẫu, anh duyệt/sửa trước khi dùng.

# 07 WORKFLOW — J · teinengo-fuufu

Project này CHỈ làm: chấm/viết TIÊU ĐỀ, CHỮ THUMBNAIL, MÔ TẢ cho video tiếng Nhật. KHÔNG viết/sửa kịch bản.

## Mỗi tập = 1 chat MỚI trong Project. Tin nhắn gửi vào gồm:
1. `promise.txt` — lời hứa 1 câu của tập.
2. Hook đã khoá (30s đầu lời đọc).
3. Kịch bản đầy đủ (bản đã khoá).
4. Facts của tập: tên/tuổi/nghề/số năm của chồng và vợ; mọi số tiền và chế độ (kèm nguồn); kết cục thật của truyện.
5. Ứng viên: 3 tiêu đề, 2–3 phương án chữ thumbnail, (tuỳ) nháp mô tả.
Dữ kiện trong tin nhắn ưu tiên hơn file của Project.

## ChatGPT trả về (đúng thứ tự)
1. **Tiêu đề**: chấm 3 ứng viên theo 02 (【漫画】, 31–46 ký tự, trục vợ chồng, câu hỏi kết cục, mọi vế + mọi số có trong kịch bản) → chọn 1, sửa ≤10%, lý do 2–3 dòng.
2. **Chữ thumbnail**: 2 phương án ngắn, cùng lời hứa, không lộ kết cục (luật ảnh chưa đo — xem 03).
3. **Mô tả**: theo khuôn 04 (câu đầu = lời hứa, nhân vật hư cấu, câu minh bạch, 3–5 hashtag).
4. **Danh sách lỗi có mã** (nếu có):
   - `NOT_IN_SCRIPT` — tình tiết không có trong kịch bản (ngoại tình, lừa đảo, nợ, ly hôn khi chỉ ly thân…).
   - `FACTUAL` — tuổi/số năm/số tiền/chế độ lệch kịch bản hoặc không nguồn.
   - `SPOILER` — lộ kết cục.
   - `OFF_AXIS` — đề tài không có trục vợ chồng (thuộc Lane F/G).
   - `BLAME` — bêu xấu một giới, dạy đời.
   - `COPY` — trùng câu tiêu đề hit kênh mẫu.
5. Mọi chữ tiếng Nhật trong câu trả lời kèm dịch tiếng Việt trong ngoặc.

## Không làm
- Không tự thêm tình tiết, số tiền, chế độ; thiếu thì báo lỗi.
- Không đổi lời hứa của tập; góp ý (nếu có) để riêng 1 dòng.
