> BẢN NHÁP 2026-09-26 — lane chưa có tập nào; luật rút từ kênh mẫu, anh duyệt/sửa trước khi dùng.

# 04 DESCRIPTION RULES — J · teinengo-fuufu

## Dữ liệu kênh mẫu
**CHƯA CÓ DỮ LIỆU mô tả (description) của kênh mẫu — anh bổ sung.** `_raw\transcripts.json` không có trường mô tả.
Cái có:
- CTA cuối video trong transcript (DNA mục CTA patterns, 3 câu cố định):
  「もし心当たりがあれば是非コメントで教えてください。あなたのお話が同じ迷いを抱える誰かの気づきになるかもしれません。」 (Nếu thấy giống mình, hãy kể ở bình luận. Câu chuyện của bạn có thể giúp ai đó đang cùng băn khoăn.)
  「このチャンネルでは老後の暮らしにまつわる物語をお届けしています。」 (Kênh này mang đến những câu chuyện về cuộc sống tuổi già.)
- Tag 8/8 video: 老後のゴローさん · シニア (người cao tuổi) · ６０代 (tuổi 60) · ５０代 (tuổi 50) · 年金 (lương hưu) · 漫画 · マンガ (manga).
- IDEA_GORO §4: video 501k có CTA + link tài liệu miễn phí cuối video — khuyên thử từ tập 3–5, không đưa ngay tập đầu.

## Khuôn đơn giản (đề xuất, anh duyệt)
Ngôi thứ ba, です・ます (giống lớp "người dẫn" cuối video kênh mẫu), không kể bằng 俺.

1. **Câu đầu = lời hứa của tập** — cùng câu hỏi với tiêu đề, chữ thumbnail, hook (luật G1 gói đăng chung). Không lộ kết cục.
2. 1–2 câu nhân vật: tuổi + nghề cũ + số năm làm + tên hư cấu của chồng và vợ + quyết định (chỉ những gì kịch bản có).
3. 1 câu hỏi mời bình luận hướng về vợ chồng, ví dụ: 「あなたのご夫婦なら、どちらを選びますか？」 (Nếu là vợ chồng bạn, bạn chọn bên nào?)
4. Câu minh bạch (đề xuất): 「※登場人物は架空です。制度や金額は実在の情報に基づいています。」 (※ Nhân vật là hư cấu. Chế độ và số tiền dựa trên thông tin có thật.)
5. Hashtag 3–5 từ tag kênh mẫu + đề tài có trong kịch bản: #シニア (người cao tuổi) · #60代 (tuổi 60) · #夫婦 (vợ chồng) · #漫画 (manga) · 1 tag đề tài (vd #熟年離婚 — ly hôn tuổi già). KHÔNG dùng tag tên kênh mẫu 老後のゴローさん.

## Không được
- Kể kết cục, lộ ông lão/ngụ ngôn là chìa khoá.
- Số tiền/chế độ không có trong kịch bản; lời khuyên tài chính/pháp lý kiểu cam kết.
- Tình tiết ngoại tình/lừa đảo/nợ không có trong kịch bản.
- Timestamps bịa giây (khối Timestamps thì BẮT BUỘC có — xem mục dưới).

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
