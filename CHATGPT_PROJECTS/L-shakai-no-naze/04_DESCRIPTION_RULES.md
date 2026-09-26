# 04 DESCRIPTION RULES — L-shakai-no-naze · shakai_no_naze

> Lane `shakai_no_naze`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

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
LUẬT MÔ TẢ LANE L: hook_line cùng lời hứa với tiêu đề (cổng G1 qc_goi_dang h2dev đo câu đầu mô tả). Mọi số liệu/khảo sát/năm phải có NGUYÊN VĂN trong kịch bản, đúng nghĩa (ai khảo sát, đối tượng). Hashtag CHỈ ở field hashtags (5–8, #社会問題 luôn có + từ khoá đề tài có trong kịch bản), KHÔNG viết trong đoạn. Timestamps do tool dựng từ lời đọc thật. Không CTA đăng ký dài.

### desc_minimal
False

### doan_spec
ĐÚNG khuôn mô tả kênh mẫu 社会のウラガワ (10/11 video): hook_line = câu nêu HIỆN TƯỢNG cùng lời hứa với tiêu đề (「いま、〜が増えています。」 hoặc câu thoại gây sốc của truyện). Sau đó 3–4 đoạn ngắn, mỗi đoạn 1–3 câu, xuống dòng thoáng:
(1) 1–3 SỐ LIỆU THẬT có trong kịch bản, nói rõ ai khảo sát + năm (「日本能率協会マネジメントセンターの2023年の調査では…」) — CẤM số ngoài kịch bản;
(2) câu hỏi なぜ lặp lại lõi tiêu đề (「なぜ〜のでしょうか？」);
(3) 1–2 câu giới thiệu truyện: bối cảnh + nhân vật hư cấu (được nêu tên/tuổi/vai, có さくら nếu kịch bản có) + hé câu trả lời bằng khuôn 「その裏側には、〜があったのでした。」 — KHÔNG nói hết đáp án;
(4) đoạn cuối ĐÚNG 1 câu (giữ nguyên văn): 「※登場人物は架空ですが、数字は実在の調査・統計に基づいています。」. KHÔNG viết hashtag, KHÔNG viết lời chào/giới thiệu kênh trong đoạn (tool tự thêm khối Timestamps + lời chào kênh + dòng hashtag theo khuôn chung).

### desc_doan_range
```
[
 3,
 4
]
```

### tieu_de_keywords_line
False

### cam_on_default
最後までご覧いただき、ありがとうございます。このチャンネルでは、身近な社会の「なぜ？」を、漫画の物語と実際のデータで解き明かしています。

### tags_hint
5 tag chung của ngách (社会問題, 働き方, 雑学, 心理学, 漫画) + tag đề tài

<!-- export 16767427b92f · 2026-09-26 -->
