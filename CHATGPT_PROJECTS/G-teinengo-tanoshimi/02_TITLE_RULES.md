# 02 TITLE RULES — G-teinengo-tanoshimi

> Lane `teinengo-tanoshimi`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Độ dài (ký tự, KHÔNG tính prefix/suffix cố định)
- mục tiêu 40 · tối đa 45 · tối thiểu 33 · cảnh báo phần đầu 24
- prefix cố định: `【漫画】` · suffix cố định: ``

## Luật số
LUẬT SỐ (anh chốt 2026-09-23, áp cho TIÊU ĐỀ và CHỮ THUMBNAIL): cái gì đếm được thì viết bằng CHỮ SỐ — 40年 / 25万 / 73歳 / 3年前 / 45,000円 — TUYỆT ĐỐI không viết 四十年, 二十五万, 七十三歳 (dài, mắt lướt trên điện thoại không bắt được). Riêng thành ngữ (一言, 一行, 一人, 十分…) giữ nguyên chữ Hán. Mô tả video thì KHÔNG áp luật này — mô tả vẫn dùng chữ Hán số cho êm giọng kể.

### title_rules
LUẬT TIÊU ĐỀ LANE G (定年後の楽しみ方 — 漫画 hưu trí Nhật) — chốt 2026-09-24 từ 20 video kênh mẫu 老後のお金ストーリー (title_intel):
1. TIỀN TỐ 【漫画】 BẮT BUỘC (20/20 video kênh mẫu).
2. BẮT BUỘC có N選 (5選/7選) trừ khung F5 trải nghiệm-có-giá: sau bước ngoặt 18/8, 7 video N選 trung vị 5.124 view/ngày vs 4 video không N選 824 (6,2 lần).
3. BẮT BUỘC có 定年後 / 60代 / 65歳 (14/15 video sau bước ngoặt; video bỏ mất (_Az1) tụt 5,8 lần so với video cùng đề tài).
4. VẾ SAU LÀ PHẦN THƯỞNG, không phải lời doạ: 実は1円もかからない / 誰でもできて金もかからない / 平日ならほぼ独り占め. 6/6 video thắng có tiền đề phần thưởng; 5/7 video thua tiền đề mất mát.
5. CHỌN 1 TRONG 5 KHUNG ĐO ĐƯỢC:
   F1 定年後、{最強の}{đề tài}N選…実は{1円もかからない}{phần thưởng} (AOe 10,1x; bản làm lại _D8q 95.648 view/24h)
   F2 一生に一度は{歩き}たい…定年後に行くべき{tính từ hẹp}{địa điểm}N選 (BeIZ 3,7x)
   F3 なぜか{老けない}{tuổi+giới}が「{毎朝やっていること}」N選…同年代と差がつく意外な共通点 (bgUq 4,1x, nhiều view nhất kênh)
   F4 {60代}から人生が{心地よく}なる…定年後に見つけた{danh từ dịu}N選 (_EhP 6x, gánh bằng dòng đỏ thumbnail phủ định)
   F5 {thứ quen}に{giá sốc}！？{chuẩn quen}より高い{bản sang}に{tuổi}で乗ってみた結果… (ASBV 3,9x)
6. CẤM CHỮ SỢ trên tiêu đề: 年金・貧乏・破綻・後悔・失敗・不安・衝撃・残酷・地獄・末路 (4/4 video ≥11 ngày có chữ sợ đều ≤455 view/ngày).
7. CẤM TỪ NHẠT: おすすめ・人気・有名・最古級 (cặp cùng đề tài: _G9s 2.894 vs LGoe 1.580).
8. CẤM LỘ KẾT CỤC / TRẤN AN: それでも人生は終わらなかった, 実は贅沢なほど自由な老後生活 (cả hai ~1,1x).
9. MỌI VẾ PHẢI GREP ĐƯỢC TRONG script.txt. Cực cấp 最強/一流 được phép không có trong script CHỈ KHI danh sách trả đủ phần thưởng (ngoại lệ đo được của kênh mẫu) — vế bị script PHỦ NHẬN thì bỏ ngay (ep06 cũ: 1円も使わず/若返る bị phủ nhận).
10. ĐỘ DÀI 33–45 ký tự cả tiền tố; không dùng ｜ hay 【】 thứ hai.
Mẫu thắng kênh mẫu: 【漫画】定年後、最強の暇つぶし5選…実は1円もかからない楽しみ方がありました (13.885/ngày) · 【漫画】なぜか老けない50代男性が「毎日やっていること」7選…同年代と差がつく意外な共通点 (5.659/ngày) · 【漫画】一生に一度は参拝したい…定年後に行くべき格式の高い神社5選 (5.124/ngày).

### forbid_phrases
```
[
 "おすすめ",
 "人気",
 "有名",
 "最古級",
 "それでも",
 "実は贅沢"
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
 "貧乏",
 "破綻",
 "後悔",
 "失敗",
 "不安"
]
```

### separators_ok
False

### ctr_hint
Có 【漫画】 đầu? Có N選? Có 定年後/60代/65歳? Vế sau có PHẦN THƯỞNG (1円もかからない/誰でもできる/0円) thay vì lời doạ? Mọi vế grep được trong script? Tiêu đề chỉ tả nỗi sợ (年金/貧乏/後悔/不安) → ctr ≤ 3.

### brevity_hint
Có 【漫画】 + N選 + 定年後/60代 trong {head_warn} ký tự đầu? Tổng {target_min}–{max_chars} ký tự? Quá {max_chars} = 0 điểm.

### length_block
ĐỘ DÀI (đo thật kênh mẫu 老後のお金ストーリー): tiêu đề {target_min}–{max_chars} ký tự KỂ CẢ tiền tố 【漫画】 (mục tiêu {target_chars}).
Tiêu đề >45 ký tự nằm TRỌN trong nhóm thua (YKjW 52 ký tự = 27,8 view/ngày). Cú móc + 定年後/60代 phải trọn trong {head_warn} ký tự đầu.

<!-- export 953dd0827336 · 2026-09-26 -->
