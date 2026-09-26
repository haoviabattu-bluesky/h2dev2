# 02 TITLE RULES — L-shakai-no-naze · shakai_no_naze

> Lane `shakai_no_naze`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Độ dài (ký tự, KHÔNG tính prefix/suffix cố định)
- mục tiêu 24 · tối đa 34 · tối thiểu 16 · cảnh báo phần đầu 12
- prefix cố định: `` · suffix cố định: `【漫画】`

## Luật số
LUẬT SỐ (anh chốt 2026-09-23, áp cho TIÊU ĐỀ và CHỮ THUMBNAIL): cái gì đếm được thì viết bằng CHỮ SỐ — 40年 / 25万 / 73歳 / 3年前 / 45,000円 — TUYỆT ĐỐI không viết 四十年, 二十五万, 七十三歳 (dài, mắt lướt trên điện thoại không bắt được). Riêng thành ngữ (一言, 一行, 一人, 十分…) giữ nguyên chữ Hán. Mô tả video thì KHÔNG áp luật này — mô tả vẫn dùng chữ Hán số cho êm giọng kể.

### title_rules
LUẬT TIÊU ĐỀ LANE L (社会のなぜ研究室 — 漫画 giải thích hiện tượng xã hội Nhật) — chốt 2026-09-24 từ ĐỦ 11 video kênh mẫu 社会のウラガワ (title_intel shakai-no-naze + view/ngày yt-dlp):
1. SUFFIX 【漫画】 CUỐI câu (11/11) — tool tự nối, KHÔNG viết vào thân.
2. CHỦ NGỮ = NHÓM NGƯỜI mà người xem tự nhận hoặc đang phán xét (Z世代 / 若手 / 賢い人 / 独身男性 / ミドル層) nằm trong 12 ký tự đầu — 5/5 video thắng (≥2.000 view/ngày) có; 3 video thua nặng nhất (89, 21, 130/ngày) chủ ngữ trừu tượng (正しい人 / 社会に必要な仕事 / 発達障害の大人).
3. PHẢI CÓ LẬP TRƯỜNG gây tranh cãi, không kể khổ: câu thoại 『…』 (『Z世代はもう雇わない』 8.134/ngày), phán quyết ⁉ (独身は勝ち組⁉ 2.860/ngày), 末路 (9.393/ngày), 〜ほど〜ない (賢い人ほど群れない 4.251/ngày). Khung KÊU OAN / BẤT CÔNG (正しい人がバカをみる, 大変なのに給料が低い) = nhóm thua → cấm.
4. 4 KHUÔN đo được, chọn theo kịch bản:
   F1 『câu thoại sốc của nhân vật/xã hội』なぜ{nhóm}が{hiện tượng}のか — video top kênh; câu thoại PHẢI có nguyên văn (hoặc gần nguyên văn) trong kịch bản/hook.
   F2 なぜ{nhóm}ほど{điều ngược thường thức}のか？
   F3 {hành vi của nhóm}の末路とは — chỉ khi kịch bản có hậu quả rõ cho chính nhóm đó.
   F4 {phán quyết}⁉{nhóm}が{hiện tượng}した納得の理由 / {nhóm}が{爆増/激減}した理由.
5. Lõi なぜ〜のか / 〜理由 phải được kịch bản TRẢ LỜI (chặng dữ liệu + kết). Không hứa điều kịch bản không có.
6. Số liệu trên tiêu đề: chỉ khi có NGUYÊN VĂN trong kịch bản (đúng nghĩa ai khảo sát); viết CHỮ SỐ (77%, 6倍), không chữ Hán số. Thường KHÔNG cần số (4/5 video thắng không có số).
7. PHẢI dùng lại chữ của 30s hook đã khoá (hook/hook_locked.txt + hook_lock.json promise) — cổng qc_goi_dang h2dev đo lời hứa nói trong 60s đầu, lõi tiêu đề trong 90s đầu.
8. Không trùng đề tài/nhân vật 11 video kênh mẫu (Z世代採用, 群れない, パワハラ指導拒否, 独身男性, iPhone→Android, 氷河期転職, 休日の予定, いい旦那, 発達障害, 正直者, エッセンシャルワーカー).
Mẫu thắng kênh mẫu: 『Z世代はもう雇わない』なぜ企業のZ世代の採用が激減してるのか【漫画】 (8.134/ngày) · パワハラを盾に指導を拒否するZ世代の末路とは【漫画】 (9.393/ngày) · なぜ賢い人ほど群れないことを選ぶのか？【漫画】 (4.251/ngày) · 独身は勝ち組⁉結婚しない男性が増えた納得の理由【漫画】 (2.860/ngày).

### forbid_phrases
```
[
 "バカをみる",
 "バカを見る",
 "給料が低い",
 "発達障害",
 "衝撃の真実",
 "まさかの結末"
]
```

### fear_words
```
[
 "地獄",
 "残酷",
 "悲劇",
 "暴露",
 "バカをみる"
]
```

### separators_ok
True

### ctr_hint
Chủ ngữ là NHÓM NGƯỜI người xem tự nhận/đang phán xét (Z世代/若手/独身男性/賢い人) trong 12 ký tự đầu? Có LẬP TRƯỜNG gây tranh cãi (câu thoại 『…』 / 勝ち組⁉ / 末路 / ほど〜ない) thay vì kể khổ bất công (正しい人がバカを見る = nhóm thua)? Lõi なぜ〜のか/〜理由 trả lời được bằng kịch bản?

### brevity_hint
nhóm người + hiện tượng trong ≤{head_warn} ký tự đầu? thân {target_min}–{max_chars} (mục tiêu {target_chars}), chưa tính 【漫画】?

### length_block
ĐỘ DÀI (đo 11/11 video kênh mẫu 社会のウラガワ): THÂN {target_min}–{max_chars} ký tự (mục tiêu {target_chars}), CHƯA tính 【漫画】 do tool tự nối cuối — tổng thường 21–38. Nhóm người + hiện tượng phải trọn trong {head_warn} ký tự đầu.

<!-- export 16767427b92f · 2026-09-26 -->
