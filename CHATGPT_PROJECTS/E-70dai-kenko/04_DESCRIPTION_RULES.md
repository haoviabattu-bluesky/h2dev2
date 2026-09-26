# 04 DESCRIPTION RULES — E-70dai-kenko · kenko-chiebukuro

> Lane `kenko-chiebukuro`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

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
LUẬT MÔ TẢ LANE E: câu đầu (hook_line) nói CÙNG lời hứa với tiêu đề bằng cơ thể/thói quen của người xem (kênh mẫu 3/3 video thắng mở mô tả đúng như câu mở của video). Mọi con số/nghiên cứu phải có trong kịch bản; KHÔNG tên viện mơ hồ kiểu 国立○○センター nếu kịch bản không có; không hứa chữa khỏi. cta_binh_luan = xin bình luận MỘT CHỮ gắn với tập (vd 「守ります」「やってみます」) + 1 câu hỏi cụ thể. Không tự viết khối like/LINE và khối miễn trừ — tool tự nối.

### doan_spec
3-4 đoạn tiếng {lang}, mỗi đoạn 2-4 câu, giọng người dẫn kiểu bác sĩ nói với khán giả (です・ます, ngôi 2 皆さん/あなた, không tự xưng là bác sĩ): (1) cơ thể/thói quen của người xem + 'không phải lỗi của bạn / không phải do tuổi' → (2) cơ chế nói bằng lời thường (1 ẩn dụ nếu kịch bản có) → (3) lời hứa cách làm cụ thể, rẻ, làm được ở nhà → (4) một đoạn bắt đầu bằng 「📌 今回ご紹介する…」 liệt kê CÁC MỤC từ 第5位 tới 第2位 đúng như kịch bản, còn 第1位 thì ghi 「第1位は動画の中でお伝えします」 (không lộ tên)

### desc_doan_range
```
[
 3,
 4
]
```

### desc_fixed_blocks
```
[
 "👍 この動画が",
 "⚠️【免責事項】"
]
```

### desc_fixed_defaults
```
[
 "👍 この動画が少しでもお役に立てたなら、高評価とチャンネル登録をお願いいたします。\n大切なご家族やご友人に、LINEで「これ見てみて」と送ってあげてください。",
 "⚠️【免責事項】この動画は一般的な健康情報の提供を目的としており、医療診断や治療の代わりになるものではありません。持病のある方、お薬を服用中の方、食事を大きく変えたい方は、必ずかかりつけの医師にご相談ください。"
]
```

### tieu_de_keywords_line
False

### cam_on_default
🍵 最後までご覧いただき、誠にありがとうございました。

### tags_hint
5 tag chung lặp lại của ngách (高齢者の健康, 健康長寿, シニアの食事, 老後の健康管理, 介護予防)

<!-- export 762beca31b98 · 2026-09-26 -->
