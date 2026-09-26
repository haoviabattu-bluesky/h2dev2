# 04 DESCRIPTION RULES — G-teinengo-tanoshimi

> Lane `teinengo-tanoshimi`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Cấu trúc file đăng BẮT BUỘC (mọi kênh, anh chốt 2026-09-25)
```
<tiêu đề>

<mô tả>

----------------------------------------------------------------------------------------------------
Timestamps:

0:00 <chương 1>
m:ss <chương 2> …
----------------------------------------------------------------------------------------------------

<lời cảm ơn / chào kênh>

----------------------------------------------------------------------------------------------------
#hashtag #hashtag …
```
- KHÔNG kênh nào được bỏ khối Timestamps (kể cả kênh mô tả tối giản — khi đó khối mốc đặt ngay trước dòng hashtag).
  ≥3 mốc, mốc đầu 0:00, cách nhau ≥10 giây; nên 6–9 chương.
- Giây của mốc lấy từ phụ đề THẬT của video, KHÔNG được đoán. Tin nhắn không đưa phụ đề/giây → chỉ đề xuất TÊN CHƯƠNG kèm
  số ĐOẠN kịch bản bắt đầu chương, khối mốc để dòng chờ `[CHƯA CÓ — máy 2 chèn mốc sau khi dựng video]`.
- Tên chương: tiếng Nhật 8–22 ký tự, gợi tò mò, KHÔNG lộ đáp án cuối, chữ số Ả Rập.
- Câu đầu mô tả nói CÙNG lời hứa với tiêu đề + chữ thumbnail + hook đầu video (1 lời hứa ở 4 chỗ).
- Hashtag và câu hỏi mời bình luận mỗi thứ chỉ 1 lần (không lặp).

## Tags (thay bước nghiên cứu tag cũ, 2026-09-25)
Chép nguyên tags của video gốc (09/10); dưới 10 tag thì bổ sung cho đủ 15–20 tag tiếng Nhật đúng nội dung kịch bản mình.
Tag gốc đứng đầu, bỏ trùng, tổng chuỗi nối bằng dấu phẩy ≤ 500 ký tự. Khi được hỏi, trả JSON `{"tags": [...]}`.

## Luật riêng của kênh

### desc_note
2026-09-25 anh chốt: BỎ khuôn tối giản — mô tả lane G dùng ĐỦ khuôn chuẩn dự án như mọi lane khác: câu chốt → GẠCH → Timestamps (bắt buộc mọi lane) → GẠCH → câu cảm ơn ngắn ngôi 3 (`cam_on_default`, KHÔNG dùng giọng bà cụ 🌸 của satori) → GẠCH → hashtag (từ S4). Quyết định cũ (kênh mẫu 0/10 dùng hashtag/Timestamps/cảm ơn) vẫn đúng về SỐ ĐO nhưng anh chọn ưu tiên khuôn thống nhất giữa các lane.

### desc_minimal
False

### doan_spec
ĐÚNG 4 khối, tổng 250–420 ký tự (kênh mẫu đo thật 247–508, trung vị 365):
(1) 1–2 câu hỏi/nghịch lý mở lấy Ý từ hook 0–30s (vd 定年後、毎日が自由になったはずなのに、なぜか疲れる。そんな感覚はありませんか？) — KHÔNG chép nguyên văn script;
(2) 1 đoạn 2–3 câu giới thiệu: tuổi + đã hưu bao lâu + gặp ai + học được gì (今回の漫画では…);
(3) 1 dòng liệt kê các mục bằng danh từ ngăn 、 — đúng các mục có trong script, KHÔNG spoil mục/hạng 1;
(4) 1 câu chốt: đối tượng + 「…5つの〇〇を漫画で紹介します」

### desc_doan_range
```
[
 2,
 3
]
```

### tieu_de_keywords_line
False

### cam_on_default
最後までご覧いただき、誠にありがとうございました。

### tags_hint
4–6 tag NGẮN kiểu kênh mẫu (シニア漫画, 定年後, シニアライフ, 老後の楽しみ) — KHÔNG nhồi tag

<!-- export 953dd0827336 · 2026-09-26 -->
