> BẢN NHÁP 2026-09-26 — lane chưa có tập nào; luật rút từ kênh mẫu, anh duyệt/sửa trước khi dùng.

# 03 THUMBNAIL RULES — H · kokoro-kazoku

## Trạng thái dữ liệu
**CHƯA CÓ DỮ LIỆU THUMBNAIL THẬT — anh bổ sung.**
- `CHANNEL_DNA.md` mục Thumbnail patterns tự ghi: "Không đủ dữ liệu" (Channel Analyzer chỉ đọc transcript, không xem ảnh).
- `VIDEO_ANALYSIS/*.json` (8 file) không có trường mô tả thumbnail.
- Chưa tải ảnh thumbnail kênh mẫu về `_raw\thumbs\` (Lane I đã làm việc này — xem khuôn `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\dokkoi-nihonshi\THUMBNAIL_PATTERNS.md`).

## Định hướng đang có (CHƯA ĐO, chỉ là quyết định thiết kế ghi trong BAT_DAU)
Theo `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\kokoro-kazoku.md` mục 4.2:
- Illustration ấm, nhân vật đầu tròn, tông cam/nóng + chữ lớn.
- Không REF-LOCK (mỗi tập minh hoạ gia đình khác nhau).

## Luật tạm dùng được ngay (rút từ luật gói đăng chung, không phải từ ảnh kênh mẫu)
1. Chữ thumbnail cùng MỘT lời hứa với tiêu đề + câu đầu mô tả + hook 30–45s đầu, nhưng VIẾT LẠI ngắn, không chép nguyên tiêu đề.
2. Mọi chữ trên thumbnail phải có trong kịch bản.
3. Đếm được thì dùng chữ số (3つ, 50代).
4. Không nhãn chẩn đoán (毒親 — cha mẹ độc hại…) và không doạ vượt kịch bản.

## Việc cần làm trước khi khoá luật này
1. Tải ≥8 thumbnail thật của kênh mẫu (nên đủ 21) về `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\channel_dna\iyashi-no-shinrigaku\_raw\thumbs\`.
2. Đo: số dòng chữ, màu chữ/viền, số ký tự mỗi dòng, vị trí, có nhân vật không, tông màu nền.
3. Viết lại file này theo số đo; xoá phần "định hướng chưa đo".
