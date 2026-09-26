# 02 TITLE RULES — K-yakkyoku-sukatto

> Lane `yakkyoku-sukatto`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Độ dài (ký tự, KHÔNG tính prefix/suffix cố định)
- mục tiêu 40 · tối đa 46 · tối thiểu 31 · cảnh báo phần đầu 24
- prefix cố định: `【漫画】` · suffix cố định: ``

## Luật số
LUẬT SỐ (anh chốt 2026-09-23, áp cho TIÊU ĐỀ và CHỮ THUMBNAIL): cái gì đếm được thì viết bằng CHỮ SỐ — 40年 / 25万 / 73歳 / 3年前 / 45,000円 — TUYỆT ĐỐI không viết 四十年, 二十五万, 七十三歳 (dài, mắt lướt trên điện thoại không bắt được). Riêng thành ngữ (一言, 一行, 一人, 十分…) giữ nguyên chữ Hán. Mô tả video thì KHÔNG áp luật này — mô tả vẫn dùng chữ Hán số cho êm giọng kể.

### title_rules
LUẬT TIÊU ĐỀ LANE K (薬局スカッと帳 — dược sĩ có câu cửa miệng toxic, quả báo từ hệ thống) — chốt 2026-09-24 từ title_intel/yakkyoku-sukatto.json (TRENDING-RESEARCH đo trên 4 video dài kênh mẫu 千種テンカ, kênh mới 706 sub nên MẪU NHỎ, không chắc chắn bằng lane có 15-27 video — đọc kỹ, không tin tuyệt đối):
1. KHUÔN DUY NHẤT (4/4 video gốc theo đúng khuôn, không có khuôn thay thế như lane E/F): 【漫画】「[câu cửa miệng NGUYÊN VĂN, trong「」]」が口ぐせの/だった薬剤師が、[hành động sai lầm cụ thể HOẶC mốc đếm lần N/mốc thời gian]結果… (hoặc 行き着く先…).
   Ví dụ thật: 「【漫画】「じゃあ、辞めます」が口ぐせの薬剤師が、3回目に同じことを言った結果…」(307k view/5 ngày — cao nhất kênh) · 「【漫画】「自分、仕事できるんで」が口ぐせの薬剤師が行き着く先…」(57.8k) · 「【漫画】「残業代入んないんで」が口ぐせの薬剤師が、閉店2分前に患者を追い返した結果…」(34.5k) · 「【漫画】「代わりはいくらでもいる」が口ぐせだった薬剤師が、定年後に6社目の面接を受けた結果…」(20.3k).
2. CÂU CỬA MIỆNG PHẢI TRÍCH NGUYÊN VĂN trong「」, và phải ĐÚNG câu cửa miệng nhân vật chính lặp lại xuyên suốt kịch bản tập đó (không viết câu khác rồi gọi là câu cửa miệng — máy S3c kiểm sẽ đối chiếu với script.txt).
3. KHÔNG LỘ KẾT QUẢ: tiêu đề luôn dừng ở 結果… hoặc 行き着く先… (dấu ba chấm), không viết tiếp ai thắng ai thua, không tiết lộ nhân vật bị sa thải/từ chối.
4. CẤM TỪ NGỮ TRẢ THÙ/HẢ HÊ: 復讐, 仕返し, ざまあ, 天罰 — kênh mẫu là 因果応報 (quả báo tới từ HỆ THỐNG: log giờ, hợp đồng, quy định), KHÔNG phải nhân vật khác 'ra tay trả đũa'. Đây là điểm khác biệt cốt lõi của lane này so với thể loại 復讐 thông thường — vi phạm luật này coi như hỏng chủ đề kênh, không chỉ hỏng 1 tiêu đề.
5. HÀNH ĐỘNG SAI LẦM/MỐC ĐẾM phải LẤY TỪ KỊCH BẢN thật của tập (không bịa số liệu/tình huống không có trong script) — mẫu thật dùng mốc đếm (3回目, 6社目) hoặc mốc thời gian/tình huống nghiệp vụ (閉店2分前, 定年後).
6. TỔNG {target_min}–{max_chars} ký tự tính cả 【漫画】 (mục tiêu {target_chars}) — xem length_block.
7. Y KHOA: đây là truyện công sở, KHÔNG phải nội dung y tế — không dùng từ như 効果がある/副作用/完治 trong tiêu đề dù bối cảnh là dược sĩ.
Mẫu ĐẠT (kênh mẫu, view cao nhất): 「【漫画】「じゃあ、辞めます」が口ぐせの薬剤師が、3回目に同じことを言った結果…」.
Tự kiểm: "Câu trong「」có đúng là câu cửa miệng LẶP LẠI trong kịch bản không? Tiêu đề có tiết lộ ai thắng/thua không (phải KHÔNG)? Có từ trả thù nào lọt vào không (phải KHÔNG)?" — ghi vào ly_do_bam.

### forbid_phrases
```
[
 "復讐",
 "仕返し",
 "ざまあ",
 "天罰",
 "絶対",
 "100%",
 "完治",
 "効果がある",
 "副作用"
]
```

### separators_ok
False

### ctr_hint
Có TRÍCH NGUYÊN VĂN câu cửa miệng trong 「」(4/4 tiêu đề gốc)? Chủ ngữ là 薬剤師 với câu cửa miệng cụ thể, không phải mô tả chung chung? Kết bằng 結果… hoặc 行き着く先… (không lộ kết quả)? Không có từ trả thù/hả hê (復讐/仕返し/ざまあ/天罰) — kênh mẫu là quả báo HỆ THỐNG, không phải trả đũa cá nhân → có 1 trong các từ đó = ctr ≤ 4.

### brevity_hint
câu cửa miệng trong 「」+ 薬剤師 đã xuất hiện trong {head_warn} ký tự đầu (kể cả 【漫画】)? tổng {target_min}–{max_chars} (mục tiêu {target_chars})? Dưới {target_min} hoặc quá {max_chars} = 0 điểm.

### length_block
ĐỘ DÀI (luật cứng, đo từ 4 video dài kênh mẫu 千種テンカ — mẫu nhỏ, đọc kỹ videos[] trong title_intel trước khi tin tuyệt đối): TỔNG {target_min}–{max_chars} ký tự (mục tiêu {target_chars}) TÍNH CẢ 【漫画】. Câu cửa miệng trong「」+ 薬剤師 phải trọn trong {head_warn} ký tự đầu. Không kể trước kết quả — tiêu đề LUÔN dừng ở 結果… hoặc 行き着く先… (dấu 3 chấm, không viết tiếp).

<!-- export 9b37b7ff3589 · 2026-09-26 -->
