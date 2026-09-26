> BẢN NHÁP 2026-09-26 — lane chưa có tập nào; luật rút từ kênh mẫu, anh duyệt/sửa trước khi dùng.

# 04 DESCRIPTION RULES — I · sengoku-uragawa

## Dữ liệu kênh mẫu
**CHƯA CÓ DỮ LIỆU mô tả (description) của kênh mẫu — anh bổ sung.** `_raw\transcripts.json` không có trường mô tả.
Cái có: (a) tag video thật (`TAG_STATS.json`, 21/21 video có tag); (b) CTA cuối video trong transcript, ví dụ:
「あなたの考えを是非コメントで教えてください。」 (Hãy cho biết suy nghĩ của bạn ở phần bình luận.) ·
「歴史の裏側を見逃したくない方はチャンネル登録してお待ちください。」 (Ai không muốn bỏ lỡ mặt sau lịch sử, hãy đăng ký kênh.)

## Khuôn đơn giản (đề xuất, anh duyệt)
Ngôi thứ ba, です・ます, giọng người dẫn tài liệu.

1. **Câu đầu = lời hứa của tập** — cùng nghịch lý với tiêu đề, chữ thumbnail và hook (luật G1 gói đăng chung). Khuôn: 「〜と教わってきた〇〇。しかし史料を読むと〜。」 (Nhân vật mà ta được dạy là…. Nhưng đọc sử liệu thì….)
2. 1–2 câu: bối cảnh (năm, nơi, trận) — đúng như kịch bản.
3. 1 câu: tài liệu gốc chính được dùng trong tập (tên sử liệu + nơi lưu giữ nếu kịch bản có). Nếu tập có đoạn giai thoại/truyền thuyết → ghi rõ là 「逸話」 (giai thoại) / 「伝承」 (truyền thuyết).
4. 1 câu hỏi mở mời bình luận: 「あなたなら、どちらを選びましたか？」 (Nếu là bạn, bạn sẽ chọn bên nào?)
5. Câu minh bạch (đề xuất): 「※史料に基づいて構成していますが、会話・心情の描写には演出を含みます。諸説ある部分は動画内で明示しています。」 (※ Dựng theo sử liệu, nhưng lời thoại/nội tâm có phần dàn dựng. Chỗ có nhiều thuyết đã nói rõ trong video.)
6. Hashtag 3–5 — ưu tiên tag lặp nhiều nhất của kênh mẫu: #戦国 (Chiến quốc, 19/21) · #日本史 (sử Nhật, 20/21) · #歴史 (lịch sử, 20/21) · #大河ドラマ (phim Taiga, 19/21) + 1 tag tên nhân vật của tập.

## Không được
- Nêu năm/sử liệu/nơi lưu giữ không có trong kịch bản.
- Viết giai thoại như sự thật; khẳng định thuyết tranh cãi là chắc chắn.
- Dùng tên tác phẩm có bản quyền (manga/game) như thể kênh được liên kết; chỉ nhắc tên khi kịch bản có, dạng tham chiếu.
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
