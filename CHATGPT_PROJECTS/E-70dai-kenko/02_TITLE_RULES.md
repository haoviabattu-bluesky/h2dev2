# 02 TITLE RULES — E-70dai-kenko · kenko-chiebukuro

> Lane `kenko-chiebukuro`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Độ dài (ký tự, KHÔNG tính prefix/suffix cố định)
- mục tiêu 46 · tối đa 55 · tối thiểu 35 · cảnh báo phần đầu 28
- prefix cố định: `` · suffix cố định: ``

## Luật số
LUẬT SỐ (anh chốt 2026-09-23, áp cho TIÊU ĐỀ và CHỮ THUMBNAIL): cái gì đếm được thì viết bằng CHỮ SỐ — 40年 / 25万 / 73歳 / 3年前 / 45,000円 — TUYỆT ĐỐI không viết 四十年, 二十五万, 七十三歳 (dài, mắt lướt trên điện thoại không bắt được). Riêng thành ngữ (一言, 一行, 一人, 十分…) giữ nguyên chữ Hán. Mô tả video thì KHÔNG áp luật này — mô tả vẫn dùng chữ Hán số cho êm giọng kể.

### title_rules
LUẬT TIÊU ĐỀ LANE E (健康の知恵袋 — sức khoẻ người 65-85, N選 đếm ngược, giọng kiểu bác sĩ) — chốt 2026-09-24 từ ĐỦ 27 video kênh mẫu シニアいきいき健康 (TRENDING-RESEARCH title_intel, xếp theo view/ngày của video ≥11 ngày):
1. CHỌN 1 TRONG 3 KHUÔN theo loại tập:
   F1 (tập món TỐT / thói quen người sống thọ — chép cách người đã thắng, thì quá khứ): 「70歳以上の方へ：長寿者が密かに続けていた9つの食習慣——ほとんどの方がご存知ない」 3.342/ngày · 「高齢者の方へ：70代から積極的に摂りたい5つの食品が筋肉の衰えを防いでいた」 2.446/ngày.
   F2 (tập 'tưởng tốt hoá hại' — lật NỖ LỰC người xem đang tự hào, nhất là ăn vì cơ bắp): 「ご注意ください：3つの一見体に良さそうな食習慣が、密かに筋肉を削り続けています——60代以上の方は必見」 1.762 · 「【要注意】60歳以上が知らずに選ぶ6つのタンパク質が腎臓に負担をかけている」 820.
   F3 (tập 1 triệu chứng phổ biến + chỗ xử lý bất ngờ): 「夜間頻尿・尿漏れで悩む方へ。ふくらはぎケアと食事改善で夜中のトイレ回数をゼロに近づける方法を医師が解説」 3.069 (video top kênh).
2. MỞ BẰNG ĐỐI TƯỢNG hoặc NHÃN (70歳以上の方へ：/高齢者の方へ：/ご注意ください：/【要注意】/〇〇で悩む方へ) — 7/8 tiêu đề thắng. Đối tượng tuổi phải có trong kịch bản (grep 七十/70/高齢); không có thì dùng nhãn hoặc triệu chứng.
3. CHỦ NGỮ LÀ VẬT CẦM ĐƯỢC: N つの食品/食習慣/タンパク質, bộ phận (筋肉/骨/腎臓/ふくらはぎ). CẤM danh từ trừu tượng làm chủ ngữ (兆候/だるさ/見落とし/あなたの未来) — 0/8 thắng, 3/6 thua.
4. KHÔNG RÀO: cấm 可能性/かもしれない/知っておきたい/見られた/検討したい (0/8 tiêu đề thắng có rào; rào để trong lời + mô tả). Động từ khẳng định kiểu 防いでいた/削り続けています/負担をかけている — nhưng KHÔNG mạnh hơn kịch bản (kịch bản nói 'liên quan/giúp' thì không viết 'ngăn chặn/chữa').
5. KHÔNG THUẬT NGỮ (抗炎症/認知機能/抗コリン/百寿者/血管内皮 → 0/8 thắng). Dùng lời người 70 tuổi tự nói (物忘れ, 足腰, 100歳まで元気な人).
6. MỘT CHIỀU: hoặc danh sách món TỐT, hoặc thói quen HẠI — không 'N món hại và N món tốt' (l0N9 61/ngày).
7. KHÔNG LỘ 第1位 trong tiêu đề; có thể gọi tên 1–2 mục GIỮA nếu làm tiêu đề cụ thể hơn.
8. Y KHOA: không hứa chữa khỏi, không số liệu/bội số không có trong kịch bản (kênh mẫu viết 卵の11倍/3ヶ月で — mình KHÔNG chép). Chữ số Ả Rập (70歳, 5つ).
9. Đề tài có trần: cụm 筋肉×食品/タンパク質 và 2 đề tài phổ quát (夜間頻尿, 長寿) thắng; trí nhớ 0/2, chân–tiểu đường thấp — tiêu đề tập ngoài cụm nên nối về cơ/xương/món ăn nếu kịch bản cho phép.
Mẫu XẤU (tiêu đề nháp cũ của mình): 「認知機能の低下で見られることがある5つの変化」 (thuật ngữ + rào + trừu tượng + 22 ký tự). Mẫu ĐẠT: 「70歳以上の方へ：長寿者が密かに続けていた9つの食習慣——ほとんどの方がご存知ない」.
Tự kiểm: "Người 72 tuổi lướt điện thoại, thấy ~28 ký tự đầu: biết video dành cho mình không? Có món/bộ phận cụ thể để hình dung không? Có điều gì mình đang làm bị lật lại không?" — ghi vào ly_do_bam.

### forbid_phrases
```
[
 "可能性",
 "かもしれない",
 "知っておきたい",
 "見られた",
 "検討したい",
 "完治",
 "治る",
 "薬がいらない",
 "医者いらず"
]
```

### fear_words
```
[
 "衝撃",
 "暴露",
 "残酷",
 "地獄",
 "悲劇",
 "末路",
 "手遅れ"
]
```

### separators_ok
True

### ctr_hint
Có ĐỐI TƯỢNG/NHÃN ở đầu (70歳以上の方へ：/ご注意ください：/〇〇で悩む方へ)? Chủ ngữ là VẬT cầm được (món, bộ phận, số N) chứ không phải danh từ trừu tượng (兆候/だるさ/見落とし/未来)? Lật đúng nỗ lực người xem đang tự hào, hoặc chép cách của người đã thắng (100歳まで元気な人)? Giấu tên món để người xem hỏi 'là món gì'? Có rào (可能性/かもしれない) hoặc thuật ngữ (抗炎症/認知機能) → ctr ≤ 4.

### brevity_hint
đối tượng + vật cầm được trong ≤{head_warn} ký tự đầu? tổng {target_min}–{max_chars} (mục tiêu {target_chars})? Dưới {target_min} hoặc quá {max_chars} = 0 điểm và KHÔNG được chọn.

### length_block
ĐỘ DÀI (luật cứng, đo từ 27 video kênh mẫu シニアいきいき健康, 2026-09-23): TỔNG {target_min}–{max_chars} ký tự (mục tiêu {target_chars}). Tiêu đề thắng 33–51 ký tự, thua 29–43. Điện thoại hiện ~2 dòng ≈ 40 ký tự: ĐỐI TƯỢNG/NHÃN + vật cầm được (món/bộ phận/N) phải nằm trong {head_warn} ký tự đầu, phần sau (——ほとんどの方がご存知ない / ——シニアの方は必見) phục vụ màn lớn.

<!-- export 762beca31b98 · 2026-09-26 -->
