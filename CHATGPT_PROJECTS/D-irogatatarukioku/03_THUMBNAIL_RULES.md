# 03 THUMBNAIL RULES — irogatatarukioku

> Lane `irogatatarukioku`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

KHÔNG dùng khuôn thumbnail của kênh khác. Khuôn riêng của lane này (file cấu hình máy dựng thumbnail):

```yaml
id: irogatatarukioku
layout: panel
delivery_contract:
  choices: 3
  labels: [A, B, C]
  distinct_concepts: true
  distinct_visual_approaches: true
  selection_owner: human
  upload_public_links: true
  sheet:
    spreadsheet_id: 1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
    tab: irogatatarukioku
    column: G
delivery_folder:
  root: E:/CLAUDE/YOUTUBE/CHANEL/irogatatarukioku
  pattern: "ep{stt:02d}-*"
  filename: thumbnail.png
episode_sources:
  # Sheet column C is the SPACE_RESEARCH dossier (dNN-slug) whose number does NOT match the episode
  # folder (epNN-slug); the produced episode is found by STT instead.
  root: E:/CLAUDE/YOUTUBE/h2dev/assets/irogatatarukioku
  folder_pattern: "ep{stt:02d}-*"
  require_character: false
  photos_dir: img
  photo_captions: anchors.txt
structure:
  main_rows: 4
  min_rows: 3
  banner_required: false
font:
  path: ../../assets/fonts/NotoSansJP-Variable.ttf
  variation: Black
  fallback_path: C:/Windows/Fonts/YuGothB.ttc
composition:
  require_face: false
  subject_side: left
roles:
  head:
    color: '#FFFFFF'
    max_chars: 10
    font_ratio: 0.080
  key:
    color: '#F5C400'
    stroke_color: '#000000'
    stroke_ratio: 0.05
    max_chars: 8
    font_ratio: 0.165
  sub:
    color: '#FFFFFF'
    max_chars: 12
    font_ratio: 0.072
  num:
    color: '#FF3B30'
    stroke_color: '#000000'
    stroke_ratio: 0.04
    max_chars: 8
    font_ratio: 0.115
banner: {}
panel:
  strip_ratio: 0.085
  strip_color: '#C8161D'
  strip_edge_color: '#F2C14E'
  strip_edge_ratio: 0.003
  tagline: 色が語る記憶
  tagline_color: '#FFFFFF'
  tagline_font_ratio: 0.075
  photo_ratio: 0.465
  photo_anchor_y: 0.22
  panel_color: '#0A0A0A'
  panel_padding_ratio: 0.022
  top_margin_ratio: 0.07
  block_gap_ratio: 0.035
  rule_y_ratio: 0.47
  lower_block_y_ratio: 0.60
  rule_color: '#D81F26'
  rule_thickness_ratio: 0.007
background:
  provider_mode: existing_photo
content_strategy:
  lenses: [human_stakes_number, last_moment, human_detail]
  row_schema:
    - {role: head, max_chars: 10, required: true, description: "WHITE small lead line <=10 chars (who / when / situation)"}
    - {role: key, max_chars: 8, required: true, description: "YELLOW biggest line <=8 chars: the one number, time or fact that stops the scroll (e.g. 出撃2時間前, 276人が帰った, 85%が柵の中)"}
    - {role: sub, max_chars: 12, required: true, description: "WHITE small line <=12 chars under the red rule (context of the second fact)"}
    - {role: num, max_chars: 8, required: true, description: "RED second concrete fact <=8 chars: a number, date, count or name from the script"}
  banner_required: false
  require_must_be_visible: false
  photo_choice: true
  require_evidence_quote: true
  rubric:
    - story_accuracy
    - specificity
    - curiosity
    - title_complement
    - japanese_naturalness
    - one_two_second_clarity
    - no_fabrication
  forbidden_phrases: [衝撃の真実, まさかの結末, その理由とは？, 英雄, 靖国, 反日, 売国]
  brief: >-
    Channel: Japanese WW2 documentary built on REAL archival photographs restored in colour by AI, narrated calmly in
    third person for middle-aged/elderly Japanese viewers whose families lived the war. Thumbnail motif locked for the
    whole channel: a red vertical strip with the channel tagline on the left, ONE real colourised photograph in the
    middle-left, and a black panel on the right with two text blocks: a small WHITE lead line over a huge YELLOW line
    (the single most striking exact number / time / fact), a thin red rule, then a small WHITE context line over a RED
    second fact. The numbers must carry the human stakes the way the reference channel does (出撃2時間前, 3332人が乗り /
    276人が帰った, 85%が柵の中, 17歳): hours before death, ages, how many left and how many came back, how long they held
    out — never administrative trivia such as unit formation dates, renaming dates or ranks. The three variants must
    differ in ANGLE (a number that carries the stakes / the last moment or last photograph / a human detail such as a
    letter, an object, a last order); never weaken a number just to avoid overlapping another variant. Every number, date, count, age and quote MUST appear in the script; put the supporting script sentence in
    evidence_quote. No emotional exaggeration words, no modern political opinion, no nationalist or accusatory framing,
    no heroization slogans; respect the dead. Choose, for each variant, the photo from sources.photos that best proves the
    copy (the portrait for a person-centred angle, a scene photo for a moment-centred angle); prefer photos where a human
    face or the key object is large and clear. The three variants must use three different angles and ideally different photos.
scoring: {}
# Fable QC ảnh (S7, gộp 2026-09-22): tiêu chí lane D (plan 260920-1450 + brief ở trên); điểm 1-5 mỗi khoá.
fable_review:
  score_keys: [japanese, story, stakes, photo, motif, curiosity]
  criteria: |-
    1. japanese — Tiếng Nhật tự nhiên, đọc 1–2 giây; dòng VÀNG (key) đứng một mình vẫn hiểu; không cụm cấm
       (衝撃の真実/まさかの結末/その理由とは？/英雄/靖国/反日/売国).
    2. story — MỌI số/ngày/tuổi/trích dẫn phải có trong script (đối chiếu evidence_quote trong strategy.json); không tô hồng,
       không quan điểm chính trị hiện đại. SỬA 2026-09-23 (bàn giao TRENDING-RESEARCH, NGUYEN_TAC_HOOK_GOI_DANG.md mục iro): thumbnail PHẢI dùng CHUNG cụm đầu của tiêu đề + 1 con số — BỎ luật cũ 'bổ sung cho title, không lặp'. Đo thật kênh mẫu: thumbnail↔tiêu đề Khớp 6/9, Lệch 0/9, thumbnail có chữ số 6/6 video top, có tên người 0/9 (hDkgnTPJw5g 119.799 view: 「出撃2時間前｜子犬を抱く17歳・最後の写真」 = đúng 3 cụm của tiêu đề). Của mình theo luật cũ: Khớp 0/11, Lệch 6/11, tên người trên banner 11/11 — tức luật cũ là nguyên nhân gốc, không phải lỗi thực thi.
    3. stakes — Con số mang SỨC NẶNG CON NGƯỜI (giờ trước khi chết, bao nhiêu đi/bao nhiêu về, tuổi) — không phải trivia
       hành chính (ngày thành lập đơn vị, quân hàm, mốc giờ kỹ thuật).
    4. photo — Ảnh tư liệu tô màu chọn ĐÚNG với copy (chân dung cho góc con người, cảnh cho góc khoảnh khắc); mặt/vật
       chính to, rõ, nguyên vẹn ở 360px, KHÔNG bị chữ đè, không méo/crop cụt đầu.
    5. motif — Dải đỏ trái + ảnh giữa-trái + panel đen phải (trắng nhỏ / VÀNG to / kẻ đỏ / trắng nhỏ / ĐỎ) đúng mô-típ
       khoá của kênh; tông cùng nhà với 11 tập đã đăng.
    6. curiosity — Sức hút bấm với khán giả Nhật trung-cao niên có người thân sống qua chiến tranh; tôn trọng người đã khuất.
```

## Thumbnail kênh mẫu
Khung cố định 9/9: dải đỏ dọc bên trái chữ trắng 「カラーでよみがえる」, ảnh chiếm ~45% trái, nền đen phải, 2 khối chữ ngăn bởi 1 vạch đỏ; mỗi khối = 1 dòng trắng + 1 dòng vàng viền đỏ. Khối trên = cụm đầu tiêu đề (6/9 khớp tiêu đề), khối dưới = nhãn sự kiện/con số. 7/9 có chữ số (6/6 top). 0/9 có tên người. Ảnh: 6/6 top là mặt người (trẻ em, thiếu niên, dân đảo, cặp vợ chồng, đám đông nisei); 2/9 KHÔNG tô màu (hDkg top 1 và WUOH). 3 video mới: tàu, máy bay nhỏ trong khung viền trắng, lính + chó.

<!-- export 5153746a77e7 · 2026-09-26 -->
