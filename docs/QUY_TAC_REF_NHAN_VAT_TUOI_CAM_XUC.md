# CHARACTER REF — AGE & EMOTION LOCK
> Luật chốt 01/10/2026 (anh giao). Áp dụng MỌI lane khi tạo ảnh REF nhân vật. Nguyên văn bản anh gửi, rút gọn định dạng.

## 1. Mục tiêu
REF KHÔNG được là "gương mặt đẹp / người Nhật chung chung". Phải đúng: tuổi trong kịch bản, mức lão hoá, màu tóc + tỷ lệ bạc, nếp nhăn/da/mắt/cổ/tay, vóc dáng, thần thái theo tính cách, cảm xúc theo scene làm REF.
Tuổi nhìn thấy phải gần tuổi script. 62 tuổi trông 45–50 = FAIL; 65 trông 80 = FAIL; 78 tóc đen da căng = FAIL; 55 làm như cụ 75 = FAIL. Ảnh đẹp nhưng sai tuổi = FAIL.

## 2. Trước khi tạo REF: bắt buộc đọc script / character sheet / tóm tắt nhân vật / timeline / scene dùng để xây REF, rồi khai:
```
CHARACTER_NAME / SEX / EXACT_AGE / NATIONALITY / ROLE / PERSONALITY /
CURRENT_LIFE_CONDITION / CURRENT_EMOTIONAL_STATE / HAIR / FACE_AGING /
BODY_BUILD / CLOTHING / SCENE_CONTEXT
```
Tuổi trong script = nguồn sự thật cao nhất. Không đoán tuổi theo nghề.

## 3. AGE VISUAL LOCK — không chỉ ghi "67-year-old"; phải mô tả dấu hiệu thị giác
- **50–59**: middle-aged; ít tóc bạc ở thái dương; nhăn nhẹ quanh mắt/khoé miệng; da bắt đầu mất căng; không quá già.
- **60–64**: early senior; tóc đen pha bạc rõ hơn; nhăn mắt/trán bắt đầu rõ; rãnh mũi–má nhẹ–vừa; vẫn khoẻ.
- **65–69**: senior; bạc ~30–60%; nhăn vừa; vùng mắt có dấu tuổi; da/cổ thể hiện tuổi thật; không trẻ, cũng không thành 80.
- **70–74**: elderly nhưng có thể khoẻ; bạc nhiều; nhăn rõ mắt/trán/miệng; da chảy xệ nhẹ; rãnh mũi–má rõ; cổ/tay thể hiện tuổi.
- **75–79**: tóc chủ yếu bạc/trắng; nhăn rõ; mắt/má/cổ lão hoá rõ; da mất đàn hồi; vẫn giữ cá tính/sức khoẻ theo script.
- **80–89**: bạc/trắng chiếm ưu thế; nhăn sâu hơn; da mỏng, chảy xệ tự nhiên; có thể hơi gầy nếu hợp; KHÔNG mặc định bệnh/khom/hấp hối.

## 4. Không dùng stereotype tuổi già
Tuổi cao ≠ yếu. Không mặc định: 70 = lom khom, 75 = chống gậy, 80 = bệnh, người già = buồn, nghỉ hưu = nghèo. Chỉ dùng khi script nói. 78 tuổi khoẻ, hoạt bát → trông đúng 78 nhưng khoẻ; không trẻ hoá xuống 60.

## 5. HAIR AGE LOCK — chỉ định: hair color · gray percentage · hair density · hair style
VD: `short dark hair mixed with ~40% natural gray, slightly thinning, gray concentrated at temples`. Nữ 72: `predominantly gray with some dark strands, not dyed jet-black`. Tóc đen rõ ở tuổi cao chỉ khi script nói nhuộm.

## 6. WRINKLE LOCK — cấm từ chung chung (old face / wrinkled face / elderly); chỉ rõ mức độ
- 66 tuổi: `moderate natural crow's feet, subtle forehead lines, visible but not deep nasolabial folds, slight skin laxity`.
- 81 tuổi: `clearly visible forehead wrinkles, deeper crow's feet, pronounced nasolabial folds, laxity at cheeks/jaw, visible aging at neck and hands`.
- Cấm: extreme wrinkles / deeply aged / very frail / ancient face — trừ khi script yêu cầu.

## 7. EMOTION LOCK — REF không mặc định "đứng thẳng cười nhìn camera"; xác định BASE EMOTIONAL TONE từ nội dung video
- Vui/chữa lành: `warm gentle smile, relaxed eyes, subtle happiness, quietly optimistic` (không cười quảng cáo).
- Buồn: `subdued expression, slightly downcast eyes, quiet sadness, emotion held back, subtle tension around mouth` (không mặc định khóc).
- Cô đơn: `distant gaze, quiet loneliness, restrained, slightly tired eyes, emotionally withdrawn`.
- Hối hận: `regretful, slightly lowered gaze, subtle tension at eyebrows, quiet remorse`.
- Tức/bị xúc phạm: `controlled frustration, tense lips, slightly furrowed eyebrows, restrained anger` (không gào/hoạt hình).
- Sốc/phát hiện bí mật: `subtle shock, eyes slightly widened, frozen expression, controlled disbelief` (không há miệng to).

## 8–9. IDENTITY LOCK vs EMOTION VARIABLE
SAME PERSON — SAME AGE — DIFFERENT EMOTION.
- KHOÁ: age, gender, facial proportions, nose, eyes, jaw, face width, hair style, hair aging, skin aging, body build.
- ĐỔI THEO SCENE: expression, eye direction, pose, clothing (nếu timeline), lighting, location, camera angle, action.

## 10. Chống beautification
> ⚠️ Lane manga/anime: câu `authentic mature skin texture` / `realistic Japanese senior` dưới đây CHỈ dùng cho lane ảnh thật; lane anime thay bằng "aging drawn with line art, still anime style" (xem §17 STYLE).
Model hay tự làm da mịn, mắt trẻ, tóc đen hơn, ít nhăn, mặt người mẫu. Prompt REF phải có: `realistic age appearance, visible natural aging, authentic mature skin texture, do not beautify or de-age, not younger-looking than stated age, realistic Japanese senior`. Tránh: flawless skin, youthful, glamorous, perfect skin, anti-aging.

## 11. Negative age constraint — mỗi prompt có tuổi mục tiêu + vùng cấm
VD 68 tuổi: target 66–70; MUST NOT: <60, trông 50s, >76, extremely elderly, frail (trừ khi script). VD 79: target 77–81; MUST NOT: trông 60s, young-looking, 90+.

## 12. Age tolerance (tuổi nhìn thấy)
≤59: ±4 · 60–69: ±4 · 70–79: ±5 · ≥80: ±5. VD script 67: PASS 64–70 · BORDERLINE 61–63 / 71–73 · FAIL trông 55 hoặc 80.

## 13. REF QC — bắt buộc NHÌN ẢNH THẬT (không kết luận "prompt ghi 68 nên ảnh 68")
```
[ ] Gender  [ ] Perceived age  [ ] Hair gray level  [ ] Hair density
[ ] Wrinkle level  [ ] Skin aging  [ ] Eye aging  [ ] Neck aging
[ ] Body build  [ ] Emotional tone  [ ] Không beautify quá  [ ] Không già quá
[ ] Hợp vai trò  [ ] Hợp scene/video
```

## 14. REF AGE QC SCORE (bắt buộc trả)
```
SCRIPT_AGE / VISUAL_ESTIMATED_AGE / AGE_DELTA
HAIR_MATCH / SKIN_AGING_MATCH / WRINKLE_MATCH / BODY_AGE_MATCH / EMOTION_MATCH
FINAL: PASS / REGENERATE
```
AGE FAIL → bắt buộc REGENERATE; không cứu bằng "người trông trẻ hơn tuổi".

## 15. Cấm tự hợp lý hoá ảnh sai
Cấm: "Người Nhật thường trẻ hơn tuổi", "có thể chăm da tốt", "AI vẫn thể hiện nét trưởng thành". Script age = ground truth.

## 16. REF BUILD ORDER (không đảo để style lấn át tuổi)
1 Identity · 2 Exact age · 3 Visual age markers · 4 Hair aging · 5 Skin aging · 6 Body aging · 7 Personality · 8 Emotional state · 9 Clothing · 10 Scene/context · 11 Camera/composition · 12 Negative age constraints.

## 17. Prompt skeleton bắt buộc
```
[IDENTITY]  A [EXACT AGE]-year-old Japanese [man/woman], [role / background].
[AGE APPEARANCE]  Must visually appear approximately [AGE RANGE], realistic natural aging for this exact age.
Hair: [style], [color], [gray %], [density].
Face: [wrinkle level], [crow's feet], [forehead lines], [nasolabial folds], [skin elasticity], [mature skin texture].
Eyes: [age-related characteristics].
Neck/hands: [signs of aging where visible].
Body: [build], [posture], [health condition].
Do NOT beautify or de-age the character.
[PERSONALITY] ...
[EMOTIONAL STATE] Current emotional state: [..]. Expression: [specific visual expression].
[SCENE] ...
[STYLE] = THAM SỐ THEO LANE, KHÔNG mặc định ảnh thật. Lane ảnh thật: "Photorealistic, natural Japanese appearance, realistic skin texture, documentary/cinematic photography, not fashion photography, not beauty advertising." Lane MANGA/ANIME (vd Lane N): đặt khối STYLE của lane (anime/manga 2D, line art, cel shading, "NOT a photograph, NOT photorealistic, no skin pores") ĐẦU TIÊN trong prompt, và vẽ lão hoá bằng NÉT VẼ (đường chân chim, rãnh mũi–má, vệt tóc bạc), cấm các từ "authentic mature skin texture / documentary-realistic / age spots / skin pores" — chúng kéo model sang ảnh người thật (bài học 01/10/2026 Lane N ep01 shizue).
[NEGATIVE AGE LOCK] Must NOT look younger than ~[X]. Must NOT look older than ~[Y]. No youthful flawless skin. No excessive aging. No extreme wrinkles / frailty unless required.
```

## 18. Ví dụ hoàn chỉnh — Yoshio, 69, nam, vừa nghỉ hưu, tiết kiệm, trống rỗng, sức khoẻ bình thường
```
A 69-year-old Japanese man, recently retired after decades of office work.
He must visually appear approximately 66–72 years old, with realistic natural aging appropriate for a Japanese man of this age.
Short dark-gray hair with approximately 50–60% natural gray, slightly thinner around the crown, gray concentrated around the temples.
Moderate natural crow's feet, visible forehead lines, moderately defined nasolabial folds, slight age-related skin laxity around the cheeks and jawline, authentic mature skin texture.
Slight under-eye aging, physically healthy and not frail.
Average Japanese male build, upright but slightly less rigid posture than during his working years.
Personality: serious, disciplined, frugal. Recently retired, feels an unexpected sense of emptiness.
Expression: quietly pensive, slightly distant gaze, subtle loneliness, mouth relaxed with no smile, emotion restrained rather than dramatic.
Photorealistic Japanese documentary-style portrait, natural light, realistic skin, not fashion photography, not beauty advertising.
Do not beautify or de-age him.
He must NOT look like a man in his 40s or 50s. He must NOT look older than his mid-70s.
No flawless youthful skin. No fully black youthful hair. No extreme wrinkles. No frail body. No hunched posture.
```

## 19. Cảm xúc lấy từ STORY CONTEXT, không từ tuổi
Cùng 1 phụ nữ 73 tuổi: Story A (tìm lại niềm vui) → ấm, cười nhẹ · Story B (chồng mất) → kìm nén đau buồn, mắt mệt, không cười · Story C (bí mật chồng) → sốc kiềm chế, mắt hơi mở, miệng căng. Tuổi không đổi, chỉ cảm xúc đổi.

## 20. Timeline dài → AGE STAGES
Hiện tại 78 + flashback 52 → tạo `CHARACTER_REF_CURRENT_78` và `CHARACTER_REF_FLASHBACK_52`, KHÔNG dùng chung REF. Giữ: eye shape, nose, face proportions, jaw, identity. Đổi: hair color/density, skin aging, wrinkles, facial volume, body aging.

## 21. Quy tắc cuối
Ảnh đẹp sai tuổi = FAIL · đúng người sai cảm xúc nặng = FAIL · đúng tuổi nhưng bệnh yếu ngoài script = FAIL · bị beautify trẻ hơn 10–20 tuổi = FAIL · già hơn nhân vật quá nhiều = FAIL.
Ưu tiên: 1 đúng nhân vật → 2 đúng tuổi → 3 mức lão hoá → 4 tóc → 5 sức khoẻ/vóc dáng → 6 cảm xúc → 7 context → 8 MỚI ĐẾN đẹp/cinematic.
REF là "hồ sơ hình ảnh chuẩn", không phải ảnh minh hoạ đẹp nhất. Sai REF → mọi ảnh downstream sai theo. **Không APPROVE REF trước khi AGE QC và EMOTION QC đều PASS.**
