> BẢN NHÁP 2026-09-26 — lane chưa có tập nào; luật rút từ kênh mẫu, anh duyệt/sửa trước khi dùng.

# 04 DESCRIPTION RULES — H · kokoro-kazoku

## Dữ liệu kênh mẫu
**CHƯA CÓ DỮ LIỆU mô tả (description) của kênh mẫu — anh bổ sung.** `_raw\transcripts.json` chỉ có id/tiêu đề/view/thời lượng/transcript.
Cái có: lời CTA trong transcript (DNA mục CTA patterns), ví dụ:
- 「このようなお話が必要だと感じられた方はチャンネル登録をしておいていただけると幸いです。」 (Nếu bạn thấy cần những câu chuyện thế này, xin hãy đăng ký kênh.)
- 「今日のお話が役に立ちましたらコメントで皆さんのご意見もお聞かせください。」 (Nếu hôm nay có ích, hãy cho biết ý kiến ở phần bình luận.)

## Khuôn đơn giản (đề xuất, anh duyệt)
Ngôi thứ ba lịch sự (です・ます), người dẫn giới thiệu nội dung — không kể như nhân vật.

1. **Câu đầu = lời hứa của tập**, cùng lời hứa với tiêu đề, chữ thumbnail và hook (luật G1 gói đăng chung). Dạng: nêu nghịch lý + hứa giải thích.
   Ví dụ khuôn: 「〜なのに、なぜ〜なのでしょうか。」 (Rõ ràng … vậy mà tại sao lại …?)
2. 1–2 câu: khái niệm tâm lý học chính của tập + tên nhà nghiên cứu/học thuyết (CHỈ khi kịch bản có nêu, đúng tên).
3. 1 câu: tập này có gì dùng được — "N câu nói / N điều" (đúng số mục trong kịch bản). KHÔNG tiết lộ đáp án 「これ」 nếu tiêu đề đang treo ẩn số.
4. 1 câu mời bình luận nhẹ nhàng, ví dụ: 「あなたのご家族の場合はいかがですか。よろしければコメントで教えてください。」 (Gia đình bạn thì sao? Nếu được, hãy kể ở phần bình luận.)
5. Câu minh bạch cố định (đề xuất): 「※動画内の家族のエピソードは、心理学の考え方を説明するための架空の例です。」 (※ Các câu chuyện gia đình trong video là ví dụ hư cấu để minh hoạ khái niệm tâm lý học.)
6. Dòng hashtag 3–5 cái — từ khoá có trong kịch bản. Kênh mẫu không có tag (0/8) nên chưa có danh sách đo; tạm dùng #心理学 (tâm lý học) + #家族 (gia đình) + 1–2 từ đề tài.

## Không được
- Số liệu/khảo sát không có trong kịch bản; tên nhà nghiên cứu viết sai hoặc gán sai học thuyết.
- Hứa "chữa khỏi", "giải quyết chắc chắn" quan hệ gia đình.
- Lời khuyên y khoa/tâm thần học (thuốc, chẩn đoán).
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
