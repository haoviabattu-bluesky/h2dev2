> BẢN DỰNG TAY 2026-09-26 — khuôn chung dự án + tag đo từ kênh mẫu.

# 04 DESCRIPTION RULES — M · teinengo-anaba

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
- KHÔNG được bỏ khối Timestamps. ≥3 mốc, mốc đầu 0:00, cách nhau ≥10 giây; nên 6–9 chương.
- Giây lấy từ phụ đề THẬT, **không đoán**. Chưa có phụ đề → chỉ đề xuất TÊN CHƯƠNG kèm số đoạn kịch bản,
  khối mốc để dòng chờ `[CHƯA CÓ — máy 2 chèn mốc sau khi dựng video]`.
- Tên chương tiếng Nhật 8–22 ký tự, gợi tò mò, KHÔNG lộ hạng 1, chữ số Ả Rập.
- Câu đầu mô tả nói CÙNG lời hứa với tiêu đề + chữ thumbnail + hook (một lời hứa ở 4 chỗ).
- Hashtag và câu mời bình luận mỗi thứ chỉ 1 lần.

## Khuôn mô tả của lane (4 khối, tổng 250–420 ký tự)
1. 1–2 câu hỏi hoặc nghịch lý mở, lấy Ý từ hook 0–30s — KHÔNG chép nguyên văn.
   Ví dụ: 求人票には「簡単な軽作業」と書いてあった。なのに翌朝、体が起き上がらなかった。
   (bảng tuyển ghi "việc nhẹ đơn giản", vậy mà sáng hôm sau không nhấc nổi người).
2. 2–3 câu giới thiệu: tuổi + đã nghỉ hưu bao lâu + thử mấy việc + ghi vào sổ tay gì
   (今回の漫画では… — trong tập manga lần này…).
3. 1 dòng liệt kê các mục bằng danh từ ngăn 、 — đúng các mục có trong kịch bản, **KHÔNG spoil hạng 1**.
4. 1 câu chốt: đối tượng + 「…7つの穴場の仕事を漫画で紹介します」 (giới thiệu 7 việc ít người biết bằng manga).

## Câu cảm ơn cuối (BẮT BUỘC — luật K7 của lane)
Phải đủ ba ý: cảm ơn đã xem hết + xin 高評価 (lượt thích) + xin チャンネル登録 (đăng ký).
Câu chuẩn của lane (`script.outro_line`):
最後までご覧いただき、本当にありがとうございました。少しでも参考になったら高評価とチャンネル登録で、また穴場ノートを一緒にめくってください。
(Cảm ơn anh chị đã xem đến hết. Nếu thấy có ích dù chỉ một chút, xin để lại lượt thích và đăng ký kênh,
rồi cùng lật tiếp cuốn sổ tay chỗ hay nhé.)

## Mời bình luận (loại bình luận nhiều nhất và được like cao nhất ở kênh mẫu)
Mời khán giả kể **việc làm thêm thật của chính họ**: nghề gì, mấy ca một tháng, chỗ nào khác với lúc nghe tuyển dụng.

## Tags
Chép nguyên tags của video gốc (xem `09_VIDEO_GOC.md`); dưới 10 tag thì bổ sung cho đủ 15–20 tag tiếng Nhật
đúng nội dung kịch bản của mình. Tag gốc đứng đầu, bỏ trùng, tổng chuỗi nối bằng dấu phẩy ≤ 500 ký tự.
Khi được hỏi, trả JSON `{"tags": [...]}`.

**Tag mạnh nhất đo được ở kênh mẫu** (theo view trung bình):
`シニア求人` · `老後の働き方` · `仕事選び` (51.000) · `シニアの仕事` · `再就職` (49.300) · `老後の仕事` · `無理なく続く仕事` (46.500) ·
`定年後の仕事` (36.200) · `60代の仕事` · `60代アルバイト` · `60代パート` · `60代再就職` (92.000, chỉ ở video hit).

**Hashtag mặc định của lane** (`profile.publish.hashtags`): #定年後 #60代 #アルバイト #シニアの仕事 …
