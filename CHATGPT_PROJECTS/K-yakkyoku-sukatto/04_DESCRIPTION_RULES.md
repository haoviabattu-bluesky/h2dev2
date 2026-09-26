# 04 DESCRIPTION RULES — K-yakkyoku-sukatto

> Lane `yakkyoku-sukatto`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

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
LUẬT MÔ TẢ LANE K (đo từ description_rule + principles title_intel 2026-09-24): L1 trích nguyên văn câu cửa miệng trong 「」→ L2 câu mở cố định kiểu 'đó là câu cửa miệng của một dược sĩ' → 2-4 câu hành vi cụ thể (không phán xét) → câu nhử không lộ kết quả → khối ⚠️【免責事項】(desc_fixed_blocks, tool tự nối) → もくじ mốc phút:giây (khớp budget 7 chặng của profile h2dev) → credit giọng VOICEVOX (lấy từ credits_giong.txt của tập, KHÔNG tự bịa) → 4 hashtag cố định #薬剤師 #薬局 #漫画 #スカッと (tags_seed profile). KHÔNG viết CTA đăng ký/like — kênh mẫu không dùng. KHÔNG có cảnh trả thù trong mô tả — hậu quả phải đến từ hệ thống/số liệu (log giờ, hợp đồng, quy định), không phải nhân vật 'ra tay'.

### doan_spec
2-3 đoạn tiếng {lang}, mỗi đoạn 2-4 câu, giọng người kể ngôi 3 điềm đạm KHÔNG phán xét: (1) trích lại câu cửa miệng trong 「」rồi 1 câu giới thiệu đó là câu cửa miệng của một dược sĩ ở một hiệu thuốc nhỏ — KHÔNG lộ tên nhân vật thật (hư cấu); (2) 2-4 câu tả hành vi cụ thể lặp lại của câu cửa miệng đó (không phán xét, chỉ tả); (3) câu nhử hướng tới kết cục nhưng KHÔNG lộ kết quả (kiểu 「これは、この男が〜までの話です」)

### desc_doan_range
```
[
 2,
 3
]
```

### desc_fixed_blocks
```
[
 "⚠️【免責事項】"
]
```

### desc_fixed_defaults
```
[
 "⚠️【免責事項】登場する人物・団体・薬局はすべて架空のフィクションです。医療や薬に関する助言ではありません。お薬のことはかかりつけの薬剤師・医師にご相談ください。"
]
```

### tieu_de_keywords_line
False

### tags_hint
5 tag chung của ngách (薬剤師, 薬局, 漫画, スカッと, 因果応報) + tags_seed cố định trong profile h2dev

<!-- export 9b37b7ff3589 · 2026-09-26 -->
