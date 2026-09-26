# 04 DESCRIPTION RULES — irogatatarukioku

> Lane `irogatatarukioku`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

### desc_note
Mô tả lane D = 1 hook + 2-3 đoạn ngắn tóm tắt bối cảnh và số phận nhân vật (có số liệu chính xác từ kịch bản, KHÔNG kể chi tiết cái chết/twist cuối) + 1 câu mời khán giả kể chuyện gia đình mình (ご家族に…はいますか). Tool sẽ tự nối đoạn miễn trừ AI tô màu và khối credit nguồn ảnh sau đó, KHÔNG viết lại 2 khối này.

### doan_spec
2-3 đoạn tiếng {lang}, mỗi đoạn 2-4 câu, giọng thuyết minh tài liệu ngôi 3 (です・ます): (1) bức ảnh + bối cảnh năm/nơi/ai với số liệu chính xác → (2) diễn biến tới trước biến cố cuối → (3) hé mở số phận KHÔNG kể chi tiết cuối cùng + lời mời xem đến cuối

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
 "当時の白黒写真をAIで色付けし",
 "【映像・画像クレジット】"
]
```

### desc_fixed_defaults
```
[
 "当時の白黒写真をAIで色付けし、色を推定して再現しています。細部の色は実際と異なる場合があります。\n注目してほしいのは色の正確さではなく、写真に映る人々の表情とその時代の空気です。",
 ""
]
```

### tieu_de_keywords_line
False

### tags_hint
5 tag format/ngách (AIカラー化, 白黒写真, 実際の写真, 昭和史, 太平洋戦争)

<!-- export 5153746a77e7 · 2026-09-26 -->
