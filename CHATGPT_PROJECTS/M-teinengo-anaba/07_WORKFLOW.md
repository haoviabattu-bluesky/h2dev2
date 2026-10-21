> BẢN DỰNG TAY 2026-09-26.

# 07 WORKFLOW — M · teinengo-anaba

Project này CHỈ làm: chấm và viết **TIÊU ĐỀ · CHỮ THUMBNAIL · MÔ TẢ · TAGS** cho video tiếng Nhật.
KHÔNG viết, KHÔNG sửa kịch bản.

## Mỗi tập = 1 chat MỚI trong Project. Tin nhắn gửi vào gồm:
1. `promise.txt` — lời hứa 1 câu của tập.
2. Hook đã khoá (đầu lời đọc, dài ≈ hook video gốc — luật 17/10).
3. Kịch bản đầy đủ (bản đã khoá, sau khi máy 3 soát).
4. Facts của tập: tuổi nhân vật · danh sách 7 mục theo thứ tự 第7位→第1位 · mọi lương giờ, số giờ, số ca,
   sức nặng · mọi chế độ kèm nguồn · hạng 1 là gì.
5. Số tập (để tra video gốc trong `09_VIDEO_GOC.md`).
6. Ứng viên: 3 tiêu đề, 2–3 phương án chữ thumbnail, (tuỳ) nháp mô tả.
Dữ kiện trong tin nhắn ưu tiên hơn file của Project.

## Trả về, đúng thứ tự
1. **Tiêu đề** — chấm 3 ứng viên theo 02 (【漫画】 · 40–56 ký tự · có N選 khớp số mục · dấu ｜ · góc lợi ích ·
   không lộ hạng 1 · mọi vế có trong kịch bản), chọn 1, sửa tối đa 10%, nêu lý do 2–3 dòng.
2. **Chữ thumbnail** — 2 phương án theo 03: băng trên ≤12 ký tự + băng dưới 「N選」, hoặc khuôn hit
   (2 khung to + ô lợi ích dọc). Giấu hạng 1. Không che mặt nhân vật.
3. **Mô tả** — theo khuôn 4 khối ở 04, kèm khối Timestamps (hoặc dòng chờ nếu chưa có phụ đề) và câu cảm ơn đủ 3 ý.
4. **Tags** — chép tags video gốc trước, bổ sung đủ 15–20.
5. **Danh sách lỗi có mã** (nếu có):
   - `NOT_IN_SCRIPT` — mục, nghề, con số không có trong kịch bản.
   - `FACTUAL` — lương giờ, số ca, chế độ lệch kịch bản hoặc không nguồn; con số phi thực tế với việc thật.
   - `SPOILER` — lộ hạng 1.
   - `OFF_AXIS` — đề tài ngoài trụ cột việc làm (thuộc Lane F / G / J).
   - `COUNT` — số trong N選 không khớp số mục thật.
   - `BLAME` — chê bai nhóm người, vơ đũa cả nắm.
   - `COPY` — trùng câu tiêu đề hoặc tên nhân vật hoặc câu chốt của kênh mẫu.
   - `PROMISE` — tiêu đề, thumbnail, câu đầu mô tả, hook không cùng một lời hứa.
6. Mọi chữ tiếng Nhật trong câu trả lời kèm dịch tiếng Việt ngay sau, trong ngoặc.

## Không làm
- Không tự thêm mục, nghề, con số, chế độ — thiếu thì báo lỗi.
- Không đổi lời hứa của tập; góp ý để riêng một dòng cuối.
- Không đoán giây cho Timestamps.
