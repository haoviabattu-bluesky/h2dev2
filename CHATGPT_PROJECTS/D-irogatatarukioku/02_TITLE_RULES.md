# 02 TITLE RULES — irogatatarukioku

> Lane `irogatatarukioku`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Độ dài (ký tự, KHÔNG tính prefix/suffix cố định)
- mục tiêu 78 · tối đa 90 · tối thiểu 60 · cảnh báo phần đầu 35
- prefix cố định: `` · suffix cố định: `｜実際の写真をAIカラー化`

## Luật số
LUẬT SỐ (anh chốt 2026-09-23, áp cho TIÊU ĐỀ và CHỮ THUMBNAIL): cái gì đếm được thì viết bằng CHỮ SỐ — 40年 / 25万 / 73歳 / 3年前 / 45,000円 — TUYỆT ĐỐI không viết 四十年, 二十五万, 七十三歳 (dài, mắt lướt trên điện thoại không bắt được). Riêng thành ngữ (一言, 一行, 一人, 十分…) giữ nguyên chữ Hán. Mô tả video thì KHÔNG áp luật này — mô tả vẫn dùng chữ Hán số cho êm giọng kể.

### title_rules
LUẬT TIÊU ĐỀ LANE D (色が語る記憶 — ảnh WW2 thật tô màu, khán giả 50-80 yêu lịch sử, xem điện thoại) — chốt 2026-09-20 từ 20/20 video kênh mẫu:
1. MỞ BẰNG 【sự kiện/địa danh/năm/khí tài】 (【特攻】【硫黄島】【昭和21年 上野駅】【戦艦大和】) — người lạ đọc 4-6 ký tự đầu biết ngay video về gì. Không mở bằng câu trích hay mô tả mơ hồ.
2. HOOK = 1 KHOẢNH KHẮC CỤ THỂ NHÌN THẤY TRONG ẢNH, có vai + tuổi hoặc số: 出撃2時間前、17歳は子犬を抱いて笑っていた / 妻への手紙は「床の隙間を直して」だった. Không tóm tắt tiểu sử, không 'tướng X tư lệnh trận Y'.
3. —— HỆ QUẢ TÀN KHỐC/TWIST ngay sau hook: 翌朝、この写真に写る全員が帰らなかった / 36日後、彼は戦死した. Tương phản cười↔chết, bình yên↔hoang tàn, gia đình trong trại↔con ở tiền tuyến là công thức thắng (23K vs 3.6K).
4. ｜ SỐ LIỆU LỊCH SỬ CHÍNH XÁC đến từng chữ số, lấy đúng từ kịch bản/series_ctx: 孤児は12万3511人 / 3332人のうち276人 / 211人を救うために800人を失った. Cấm số tròn ước lượng, cấm số không có trong tư liệu.
5. ĐỘ DÀI 60-90 ký tự (mục tiêu 78) CHƯA tính suffix; 【】+hook trọn vẹn trong 35 ký tự đầu (điện thoại cắt ở ~40). Tool tự nối suffix 「｜実際の写真をAIカラー化」 — KHÔNG tự viết tagline, KHÔNG dùng 「AIフルカラー復元」 của kênh mẫu.
6. KHÔNG kể hết: giữ lại CÁCH chết / chi tiết cuối cùng / câu nói cuối cho video. Không phán xét chính trị, không tôn vinh chiến tranh, không từ ngữ xúc phạm bất kỳ bên nào.
7. Mẫu XẤU (tiêu đề cũ của mình, 0-11 view): 「真珠湾攻撃を成功させた提督は、三年後サイパンの洞窟で消えていった」 — không 【】, tiểu sử, không số liệu, không khoảnh khắc trong ảnh.
   Mẫu ĐẠT (kênh mẫu 107K): 「【特攻】出撃2時間前、17歳は子犬を抱いて笑っていた——翌朝、この写真に写る全員が帰らなかった｜残された最後の一枚」.
Tự kiểm: "Người Nhật 60 tuổi yêu lịch sử lướt điện thoại, thấy 【…】+ 30 ký tự đầu, có dừng lại không? Thấy khoảnh khắc gì? Muốn biết mảnh nào?" — ghi vào ly_do_bam.

### forbid_phrases
```
[
 "AIフルカラー復元",
 "色でたどる"
]
```

### separators_ok
True

### ctr_hint
Có 1 KHOẢNH KHẮC cụ thể nhìn thấy được trong ảnh (子犬を抱いて笑っていた, 手榴弾に覆いかぶさった) thay vì tóm tắt tiểu sử? Có tương phản (cười ↔ 2時間後 ai cũng không về; 家族は収容所 ↔ 息子は最前線)? Có con số làm người ta khựng lại (3332人のうち276人)? Tiêu đề chỉ nêu tên tướng + tên trận (tiểu sử) → ctr ≤ 4.

### brevity_hint
【】+hook trọn vẹn trong ≤{head_warn} ký tự đầu (điện thoại cắt ~40)? tổng {target_min}–{max_chars} chưa tính suffix (mục tiêu {target_chars})? Quá {max_chars} hoặc dưới {target_min} = 0 điểm và KHÔNG được chọn.

### length_block
ĐỘ DÀI (luật cứng, đo từ dữ liệu kênh mẫu + SERP 2026-09-20): TỔNG {target_min}–{max_chars} ký tự CHƯA tính suffix (mục tiêu {target_chars}); 【】+hook trọn vẹn trong {head_warn} ký tự đầu vì điện thoại chỉ hiện ~2 dòng ≈ 40 ký tự rồi cắt "…". Kênh mẫu 20/20 dài 73–81; ≥70 ký tự views gấp 3,5 lần <70; nhóm 31–40 ký tự (định dạng cũ của mình) tệ nhất gmean 1.4K. Có —— (hook——hệ quả) gấp 4–6 lần.

## Nhịp hook kênh mẫu (tiêu đề phải khớp lời hứa hook)
- 0–20s Mời nhìn 1 bức ảnh + tả chi tiết thấy được: Câu mời rồi 3–5 câu ngắn tả người/đồ vật/chữ trên biển hiệu. 4/9 dùng nguyên câu 「まずこの1枚(の白黒写真)を見ていただけるだろうか」, hDkg dùng 「これから何枚かの写真を見ていただく」; juow mở bằng con số, 3 video mới tả thẳng không mời.
- 8–26s Câu lật: Một câu làm người xem sửa lại điều vừa đoán: nơi này không phải Nhật, 2 người kia là dân đảo, ảnh chụp 2 giờ trước khi xuất kích. 5/6 video top lật ở ≤25.8s (WUOH là ngoại lệ, 86.3s).
- 20–75s Miễn trừ AI (~27s, gần như nguyên văn cố định): 9/9 video. Ở 8/9 video đặt SAU câu lật (WUOH đặt trước).
- 28–87s Nghi thức tô màu: 「この写真をカラー化してみる」 rồi 3–4 câu màu cụ thể (chất liệu + màu). 9/9 video, kể cả 3 video mới.
- 80–117s Con số chính xác: Số lẻ đến từng chữ số + phép quy đổi (1/10 dân số, 4 người có 1). 6/6 video top có trong 120s.
- 105–150s Khoá + hứa lộ trình: Hé kết cục ('1 năm sau thị trấn này biến mất', 'họ thuộc phía sống sót') rồi hứa phạm vi + số ảnh. 8/9 có lời hứa (4 trong 120s thật, 2 ước tính 144–151s).

<!-- export 5153746a77e7 · 2026-09-26 -->
