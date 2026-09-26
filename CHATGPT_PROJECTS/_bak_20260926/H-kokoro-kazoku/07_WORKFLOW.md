> BẢN NHÁP 2026-09-26 — lane chưa có tập nào; luật rút từ kênh mẫu, anh duyệt/sửa trước khi dùng.

# 07 WORKFLOW — H · kokoro-kazoku

Project này CHỈ làm: chấm/viết TIÊU ĐỀ, CHỮ THUMBNAIL, MÔ TẢ cho video tiếng Nhật. KHÔNG viết/sửa kịch bản.

## Mỗi tập = 1 chat MỚI trong Project. Tin nhắn gửi vào gồm:
1. `promise.txt` — lời hứa 1 câu của tập.
2. Hook đã khoá (30s đầu lời đọc).
3. Kịch bản đầy đủ (bản đã khoá).
4. Facts của tập: khái niệm tâm lý học + nhà nghiên cứu + số liệu, MỖI mục kèm nguồn.
5. Ứng viên: 3 tiêu đề, 2–3 phương án chữ thumbnail, (tuỳ) nháp mô tả.
Dữ kiện trong tin nhắn ưu tiên hơn file của Project.

## ChatGPT trả về (đúng thứ tự)
1. **Tiêu đề**: chấm 3 ứng viên theo 02_TITLE_RULES (tiền tố 【心理学】, độ dài 23–37, ẩn số/nghịch lý, mọi vế có trong kịch bản) → chọn 1, được sửa ≤10%, nêu lý do 2–3 dòng.
2. **Chữ thumbnail**: 2 phương án ngắn, cùng lời hứa với tiêu đề, mọi chữ có trong kịch bản (luật ảnh chưa đo — xem 03).
3. **Mô tả**: viết theo khuôn 04 (câu đầu = lời hứa, câu minh bạch ví dụ hư cấu, 3–5 hashtag).
4. **Danh sách lỗi có mã** (nếu có):
   - `FACTUAL` — khái niệm/số/tên nhà nghiên cứu không có nguồn trong tin nhắn.
   - `MISLEADING` — tiêu đề/thumbnail hứa điều kịch bản không trả lời.
   - `DIAGNOSIS` — gán nhãn bệnh/nhân cách lên người thân.
   - `BLAME` — đổ lỗi, dạy đời, doạ vượt kịch bản.
   - `SPOILER` — mô tả lộ đáp án của ẩn số 「これ」.
   - `COPY` — trùng câu với tiêu đề hit kênh mẫu.
5. Mọi chữ tiếng Nhật trong câu trả lời kèm dịch tiếng Việt trong ngoặc.

## Không làm
- Không tự thêm nguồn/số liệu; thiếu thì báo lỗi.
- Không đổi lời hứa của tập; nếu thấy lời hứa yếu → góp ý riêng 1 dòng, vẫn làm theo lời hứa đã khoá.
