# 03 THUMBNAIL RULES — F-teinengo-real

> Lane `teinengo-real`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

KHÔNG dùng khuôn thumbnail của kênh khác. Khuôn riêng của lane này (file cấu hình máy dựng thumbnail):

```yaml
# 2026-09-25 VIẾT LẠI LẦN 2 sau khi đọc TAI_SAO.md của 3 video GỐC khớp đúng ep01/02/03 (XbwqD2SktC0, e_Zo7Ht5OH8,
# _VXUim2J9QM — E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\docs\lanes\teinengo-real\KENH_GOC\<id>\TAI_SAO.md, mục H5/C1/C5).
# Cả 3 hồ sơ đều tả ĐÚNG 1 khuôn: dải đen trên (2 màu trắng+vàng) → 2 panel manga đối lập → MỖI PANEL có 1 bong
# bóng thoại dọc + 1 nhãn vàng đáy (tức 2 nhãn + 2 bong bóng TỔNG, không phải 1+1 như lane G). Engine
# `bands_manga.py` đã thêm role `lead_left/lead_right` + `quote_left/quote_right` (25/09) để vẽ được đúng
# khuôn này mà không đụng hành vi role `lead`/`quote` cũ của lane G.
id: teinengo_real
layout: bands_manga
dna_measured: true
delivery_contract:
  choices: 3
  labels: [A, B, C]
  distinct_concepts: true
  distinct_visual_approaches: true
  selection_owner: human
  upload_public_links: true
  sheet: {spreadsheet_id: 1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU, tab: F-teinengo-real, column: G}
delivery_folder:
  {root: 'E:/CLAUDE/YOUTUBE/CHANEL/F-teinengo-real', pattern: 'ep{stt:02d}-*', filename: thumbnail.png}
episode_sources:
  {root: 'E:/CLAUDE/YOUTUBE/h2dev/assets/teinengo-real', require_character: false}
structure:
  {main_rows: 5, min_rows: 3, banner_required: false}
font:
  {path: ../../assets/fonts/NotoSansJP-Variable.ttf, variation: Black, fallback_path: 'C:/Windows/Fonts/YuGothB.ttc'}
composition:
  {require_face: false, subject_side: center}
bands_manga:
  top_bar_ratio: 0.21
  top_bar_padding_ratio: 0.012
  top_bar_color: '#000000'
roles:
  # 1) Thanh đen trên — chữ TRẮNG, mốc tuổi tô VÀNG, viền ĐEN dày (TAI_SAO C1 cả 3 video: 65歳/60歳/62歳 vàng +
  #    phần còn lại trắng, ví dụ 「65歳」vàng+「で定年退職」trắng · 「60歳」vàng+「で定年退職」trắng · 「62歳」vàng+「で年金受給」trắng).
  top:
    color: '#FFFFFF'
    accent_color: '#FFE500'
    stroke_color: '#000000'
    stroke_ratio: 0.045
    width_ratio: 0.95
    max_chars: 11
    align: center
  # 2) Nhãn NỀN VÀNG chữ ĐEN ở đáy — MỖI PANEL 1 NHÃN (TAI_SAO C1 cả 3 video: 65歳まで働く/60歳で退職 ·
  #    退職金1700万円/2か月後… · 60歳で定年/退職金が消える). role lead_left = panel trái, lead_right = panel phải.
  lead:
    color: '#0A0A0A'
    box_color: '#FFE500'
    box_border: '#000000'
    box_padding_ratio: 0.22
    font_ratio: 0.09
    left_margin_ratio: 0.03
    gap_ratio: 0.02
    max_chars: 8
  # 3) Bong bóng thoại OVAL ĐỨNG trắng viền đen, chữ đen xếp DỌC — MỖI PANEL 1 BONG BÓNG (TAI_SAO C1 cả 3 video:
  #    年下上司/給料激減 (trái) · もう自由だ (phải) · 再雇用は使わない/人生詰んだ · 毎日が休日/話が違う…). role quote_left/quote_right.
  quote:
    color: '#101010'
    bubble_color: '#FFFFFF'
    bubble_border: '#101010'
    font_ratio: 0.058
    top_ratio: 0.27
    max_chars: 6
  # lead_left/lead_right/quote_left/quote_right: alias role KHÁC TÊN cho engine `validate_plan` chấp nhận (nó chỉ
  # đối chiếu tên role có mặt trong khối `roles`, còn STYLE thật vẫn lấy từ khối `lead`/`quote` ở trên — xem
  # bands_manga.py::render()). Chỉ cần khai max_chars ở đây cho đúng.
  lead_left: {max_chars: 8}
  lead_right: {max_chars: 8}
  quote_left: {max_chars: 6}
  quote_right: {max_chars: 6}
  # 4) KHÔNG dùng dòng chốt đỏ to (shock) — 3 hồ sơ TAI_SAO không nhắc dòng đỏ to nào; khuôn dừng ở
  #    thanh đen + 2 nhãn + 2 bong bóng. Giữ định nghĩa để engine không lỗi thiếu key.
  shock:
    color: '#FEFE07'
    accent_color: '#FEFE07'
    stroke_color: '#0A0A0A'
    stroke_ratio: 0.1
    shadow_ratio: 0.04
    shadow_color: '#1A1A00'
    width_ratio: 0.9
    height_ratio: 0.16
    bottom_margin_ratio: 0.02
    max_chars: 9
    optional: true
banner: {}
background:
  provider_mode: text
  art_style: >-
    semi-realistic Japanese seinen manga illustration in the style of a retirement money-drama web comic:
    realistic adult proportions, clean bold ink line art with soft cel shading, ordinary modern Japanese settings
    (small apartment kitchen table, bank counter, pension office window, hospital waiting room, factory floor,
    izakaya, convenience store, tiled bathhouse, home genkan entrance). The frame is split into EXACTLY 2
    side-by-side comic panels with a thin white gutter. CLOSE MEDIUM SHOT in EACH panel: ONE Japanese man or
    woman in their 60s, head-and-shoulders to mid-chest, drawn LARGE so the face and expression fill a large part
    of the panel — but do NOT show the full body or a wide establishing shot, minimise empty background around
    the person. CRITICAL FRAMING RULE (measured defect, do not repeat): the TOP OF THE HEAD / HAIRLINE must start
    NO HIGHER than 28% down from the very top edge of the WHOLE image — the entire top quarter of the frame
    (from y=0 to y=28%) must be 100% empty background (wall, sky, ceiling, shelf, window) with absolutely NO
    hair, forehead, ear, shoulder or any part of a person in it, because a solid black bar covers exactly that
    strip afterwards and will hide anything drawn there. Compose each character noticeably LOWER in the frame
    than feels natural, chest near the bottom edge, so the whole head with room above the hair sits safely below
    that 28% line. The two panels are a BEFORE/AFTER of the same person OR two different people making opposite
    choices, with strongly contrasting expressions (one relaxed/proud/content, the other worried/regretful/
    shocked) and contrasting lighting (warm vs cold, or bright vs dim). Keep the lower ~20% of EACH panel simple
    for a label box laid over it later. NO text, no letters, no numbers, no speech bubbles or ovals drawn by the
    model, no logos, no watermark, no real photograph.
  subject_position: centre
  keep_top_ratio: 0.28
  keep_bottom_ratio: 0.2
  forbid_real_person_likeness: true
content_strategy:
  lenses: [two_way_compare, before_after_time, open_question]
  row_schema:
    - {description: 'TOP headline on the solid black bar. White text, 7-11 characters, no punctuation. Wrap the 2-4 character keyword the viewer applies to themself (usually an age) in {curly braces} — that part is painted YELLOW, the rest stays white (measured on 3 real thumbnails of this channel: all 3 do this — never solid yellow, never a full sentence, NOT the full video title). Example shape: {65歳}で定年退職 / {62歳}で年金受給.', max_chars: 11, required: true, role: top}
    - {description: 'YELLOW label box, bottom of the LEFT panel: a concrete fact from the script tied to that panel (an age+choice, a money amount, a time jump). 2-8 characters, no sentence, no mood word. Must pair with row lead_right as a before/after or A/B contrast.', max_chars: 8, required: true, role: lead_left}
    - {description: 'YELLOW label box, bottom of the RIGHT panel: the contrasting fact/outcome to lead_left (e.g. a time jump after lead_left is a state, or the consequence after lead_left is the cause). 2-8 characters, no sentence, no mood word.', max_chars: 8, required: true, role: lead_right}
    - {description: 'ONE short line of SPEECH the LEFT-panel character actually says (or a natural compression of it) in the script, drawn in a white oval bubble with black vertical text. 2-6 characters, natural spoken Japanese, not narration, not invented. Quote the exact script line in the rationale.', max_chars: 6, required: true, role: quote_left}
    - {description: 'ONE short line of SPEECH the RIGHT-panel character actually says (or a natural compression of it) in the script, drawn in a white oval bubble with black vertical text. 2-6 characters, natural spoken Japanese, not narration, not invented. Quote the exact script line in the rationale.', max_chars: 6, required: true, role: quote_right}
  banner_required: false
  require_must_be_visible: false
  rubric: [story_accuracy, specificity, curiosity, title_complement, japanese_naturalness, one_two_second_clarity, no_fabrication]
  forbidden_phrases: [衝撃の真実, まさかの結末, その理由とは？, 残酷な現実, 衝撃の現実, 末路, 老後破産の実態]
  brief: >-
    Reference channel 老後の暮らし研究所 (UCRkP44Mcw-K8IktdTqxC9dg). Mỗi tập của lane này được ánh xạ tới ĐÚNG 1 video gốc
    (xem docs/lanes/teinengo-real/KENH_GOC/<video_id>/TAI_SAO.md của tập đang làm) — theo ĐÚNG mô-típ bố cục của
    video đó (mục H5), không theo mô-típ trung bình cả kênh. Khuôn CHUNG cho cả 3 video gốc đã đối chiếu
    (XbwqD2SktC0, e_Zo7Ht5OH8, _VXUim2J9QM): (1) một thanh ĐEN đặc trên ~21% khung, MỘT dòng chữ to, TRẮNG với
    một cụm 2-4 ký tự (thường là tuổi) tô VÀNG, viền ĐEN dày; (2) ĐÚNG 2 panel cận mặt, tương phản mạnh (trước/sau
    cùng 1 người, hoặc 2 người chọn 2 hướng ngược nhau); (3) MỖI panel có 1 nhãn vàng viền đen chữ đen ở đáy (một
    sự thật cụ thể: tuổi+lựa chọn, số tiền, hoặc mốc thời gian) — 2 nhãn tạo thành cặp trước→sau hoặc A/B đối
    xứng; (4) MỖI panel có 1 bong bóng thoại trắng viền đen chữ đen xếp dọc, là lời nói THẬT của nhân vật đó
    trong kịch bản (không phải nhãn cảm xúc chung chung). KHÔNG số tiền LỚN nếu video gốc của tập đó thuộc nhóm
    THUA vì lý do đó (đọc rõ trong "Vì sao thắng/thua" của TAI_SAO.md trước khi quyết định nhãn nào dùng số tiền).
    Thumbnail luôn thêm một GÓC KHÁC so với tiêu đề (xem C4 của TAI_SAO), không lặp lại đúng những gì tiêu đề đã nói.
scoring: {}
fable_review:
  score_keys: [japanese, story, hook_visible, motif, impact, curiosity]
  criteria: |-
    1. japanese — Tiếng Nhật tự nhiên, đọc 1–2 giây; mỗi dòng đúng max_chars; ngắt dòng không đổi nghĩa; glyph đúng 100%.
    2. story — Đúng script; KHÔNG bịa chi tiết/âm mưu/cái chết không có trong script; bổ sung cho title (không lặp); không spoil chương cuối. Cả 2 bong bóng PHẢI là câu thoại có thật (trích được vị trí trong script), cả 2 nhãn PHẢI là sự thật cụ thể có trong script.
    3. hook_visible — Ảnh CHỨNG MINH hook: chủ thể to (mặt+vai chiếm ≥65% chiều cao panel), nhận ra ở 360px; không mặt người thật rõ nét; không nhân vật/logo có bản quyền.
    4. motif — Bands_manga ĐÚNG mô-típ video gốc của tập (xem TAI_SAO.md mục H5): thanh đen trên trắng+vàng, ĐỦ 2 nhãn (1/panel), ĐỦ 2 bong bóng (1/panel), 2 panel tương phản mạnh. CẤM: ảnh/chân dung người thật hoặc ảnh gần thật, chữ sốc trừu tượng 残酷な現実/衝撃の現実/末路, chép nguyên tiêu đề lên dải đen, chữ do model ảnh vẽ (chữ luôn do PIL vẽ đè lên), cảnh toàn thân/xa (phải cận mặt), thiếu 1 trong 2 nhãn/1 trong 2 bong bóng.
    5. impact — Ở 360px chữ và chủ thể đều đọc ngay; lỗi AI (tay/chữ rác/vật sai era) trừ nặng; nhân vật vẽ xa/nhỏ trừ nặng.
    6. curiosity — Sức hút bấm với khán giả người Nhật 58-67 tuổi sắp/vừa nghỉ hưu, lo tiền hưu; cấm cụm 衝撃の真実, まさかの結末, その理由とは？, 残酷な現実, 衝撃の現実, 末路, 老後破産の実態.
```

<!-- export 6d48a0ffc013 · 2026-09-26 -->
