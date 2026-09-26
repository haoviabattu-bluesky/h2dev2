# 02 TITLE RULES — F-teinengo-real

> Lane `teinengo-real`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Độ dài (ký tự, KHÔNG tính prefix/suffix cố định)
- mục tiêu 40 · tối đa 48 · tối thiểu 30 · cảnh báo phần đầu 26
- prefix cố định: `【漫画】` · suffix cố định: ``

## Luật số
LUẬT SỐ (anh chốt 2026-09-23, áp cho TIÊU ĐỀ và CHỮ THUMBNAIL): cái gì đếm được thì viết bằng CHỮ SỐ — 40年 / 25万 / 73歳 / 3年前 / 45,000円 — TUYỆT ĐỐI không viết 四十年, 二十五万, 七十三歳 (dài, mắt lướt trên điện thoại không bắt được). Riêng thành ngữ (一言, 一行, 一人, 十分…) giữ nguyên chữ Hán. Mô tả video thì KHÔNG áp luật này — mô tả vẫn dùng chữ Hán số cho êm giọng kể.

### title_rules
LUẬT TIÊU ĐỀ LANE F (定年後のリアル — 漫画 tiền hưu trí Nhật) — chốt 2026-09-24 từ 15 video kênh mẫu 老後の暮らし研究所 (title_intel teinengo-real):
1. TIỀN TỐ 【漫画】 BẮT BUỘC (15/15). Khuôn: 【漫画】{tuổi}で{quyết định}した{男/俺}…{mốc thời gian}、{ẨN SỐ}.
2. VẾ SAU PHẢI TREO ẨN SỐ (差 / 本当の理由 / どっちだったのか / 最強な理由 / N選 đếm thật) — thắng 4/4; kể hết kết cục (…消えました / …でも絶望しました) ≤200 view/ngày. Kiểm: che vế đầu, vế sau còn là câu hỏi không?
3. SỐ trên tiêu đề = số MẤT nhỏ-vừa của người thường (67万, 2万). CẤM số 退職金 lớn ≥1500万 (0/4 thắng; 4/4 có đều ≤766/ngày).
4. CẤM chữ sốc trừu tượng làm kết: 残酷な現実 / 衝撃の現実 / 末路. CẤM nhóm hẹp: 独身 / 元部長 / 非課税 / 繰り下げ70.
5. 5 khung đo được: F1 2 lựa chọn ngược nhau + 差 (không dùng 2 tập liền) · F2 số MẤT + 本当の理由 · F3 mệnh lệnh ngược + tuổi lệch + 最強な理由 (chỉ khi script kết luận nghiêng 1 phe) · F4 cảnh báo nhóm tuổi + N選 (chỉ khi script ĐẾM 第N位) · F5 mốc thời gian ngắn bất ngờ (dự phòng).
6. PHẢI dùng lại chữ của 30s hook đã khoá (hook/hook_locked.txt) — cổng qc_goi_dang của h2dev đo lời hứa phải được nói ≥60% trong 45 giây đầu; lõi tiêu đề 26–44 ký tự.
7. Mọi vế phải grep được trong script.txt; vế bị script phủ nhận → bỏ.
8. Viết CHỮ SỐ (60歳, 2万円), không chữ Hán số.
Mẫu thắng kênh mẫu: 【漫画】60歳で定年退職した男…5年後、65歳まで働いた同僚との差に絶望しました (6.194/ngày) · 【漫画】65歳で定年退職した男…2年後、貯金が67万円消えた本当の理由を知りました (4.005/ngày) · 【漫画】50代後半から要注意…老後破産する人がやっている貧乏になるお金の使い方6選 (6.744/ngày).

### forbid_phrases
```
[
 "残酷な現実",
 "衝撃の現実",
 "末路",
 "独身",
 "元部長",
 "非課税"
]
```

### fear_words
```
[
 "衝撃",
 "残酷",
 "地獄",
 "末路",
 "悲劇",
 "暴露"
]
```

### separators_ok
False

### ctr_hint
Có 【漫画】? Có tuổi + quyết định? Vế sau treo ẩn số? Số là số MẤT nhỏ? Không 残酷/末路? Mọi vế có trong script + hook?

### brevity_hint
Có 【漫画】 + tuổi trong {head_warn} ký tự đầu? Tổng {target_min}–{max_chars}?

### length_block
ĐỘ DÀI (đo kênh mẫu 老後の暮らし研究所): tiêu đề {target_min}–{max_chars} ký tự KỂ CẢ 【漫画】 (mục tiêu {target_chars}); thân thắng 23–37 ký tự, 1 lời hứa. Tuổi + quyết định phải trọn trong {head_warn} ký tự đầu.

<!-- export 6d48a0ffc013 · 2026-09-26 -->
