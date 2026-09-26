# 03 THUMBNAIL RULES — Satori-Lopezzapa68 · satori-jp-obaa

> Lane `satori-jp-obaa`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

KHÔNG dùng khuôn thumbnail của kênh khác. Khuôn riêng của lane này (file cấu hình máy dựng thumbnail):

```yaml
id: satori_jp
delivery_contract:
  choices: 3
  labels: [A, B, C]
  distinct_concepts: true
  distinct_visual_approaches: true
  selection_owner: human
  upload_public_links: true
  sheet:
    spreadsheet_id: 1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
    tab: Satori-Lopezzapa68
    column: G
quality_reference:
  path: docs/lanes/satori-jp-obaa/thumb/quality_reference/QUALITY_REFERENCE_CONTENT_TYPOGRAPHY_2026-09-19.png
  sha256: 24ccd02864873a188ba7e46c9f9645d0b63ac26d4e056bb929f5ec5f54dd663a
  scope: style_quality_reasoning_only
  forbid_pixel_template_copy: true
  forbid_cross_episode_wording_scene_subject_geometry_copy: true
delivery_folder:
  root: E:/CLAUDE/YOUTUBE/CHANEL/Satori-Lopezzapa68
  pattern: "ep{stt:02d}-*"
  filename: thumbnail.png
structure:
  main_rows: 3
  banner_required: true
font:
  path: C:/Windows/Fonts/YuGothB.ttc
  min_size_ratio: 0.075
  max_size_ratio: 0.34
  stroke_ratio: 0.035
  shadow_ratio: 0.040
  shadow_opacity: 175
composition:
  subject_side: right
  text_side: left
  enforce_subject_side: true
  subject_region_start_ratio: 0.67
  subject_visual_target_ratio: 0.333
  text_region_end_ratio: 0.70
  main_align: left
  hero_roles: [hero, hook, payoff]
  hero_min_scale_vs_others: 1.40
roles:
  context:
    color: '#FFFFFF'
    size_bias: 1.00
    max_chars: 9
    stroke_color: '#161218'
    stroke_ratio: 0.034
  hero:
    color: '#FFE033'
    size_bias: 1.70
    max_size_ratio: 0.25
    max_chars: 5
    stroke_color: '#161218'
    stroke_ratio: 0.040
  twist:
    color: '#F45B4F'
    size_bias: 1.15
    max_chars: 9
    stroke_color: '#FFFFFF'
    stroke_ratio: 0.036
    outer_stroke_color: '#161218'
    outer_stroke_ratio: 0.060
  relationship:
    color: '#FFE033'
    size_bias: 1.00
    stroke_color: '#161218'
  trigger:
    color: '#FFE033'
    size_bias: 0.95
    max_chars: 10
    stroke_color: '#161218'
    stroke_ratio: 0.036
  hook:
    color: '#F45B4F'
    size_bias: 1.45
    max_size_ratio: 0.27
    max_chars: 9
    stroke_color: '#FFFFFF'
    stroke_ratio: 0.036
    outer_stroke_color: '#161218'
    outer_stroke_ratio: 0.060
  payoff:
    color: '#F45B4F'
    size_bias: 1.35
    max_chars: 9
    stroke_color: '#FFFFFF'
    stroke_ratio: 0.036
    outer_stroke_color: '#161218'
    outer_stroke_ratio: 0.060
  emotion:
    color: '#FFFFFF'
    size_bias: 1.06
  discovery:
    color: '#FFE033'
    size_bias: 1.08
banner:
  background: '#D60916'
  text_color: '#FFFFFF'
  stroke_color: '#350003'
  stroke_ratio: 0.028
  border_color: '#FFFFFF'
  border_ratio: 0.006
  corner_radius_ratio: 0.11
  shadow_color: '#160003'
  shadow_ratio: 0.010
  horizontal_margin_ratio: 0.035
  vertical_padding_ratio: 0.12
  min_font_ratio: 0.10
  max_font_ratio: 0.20
  max_chars: 12
background:
  text_field_rgb: [54, 55, 54]
  text_field_blur_radius: 3.0
  text_field_blur_feather_ratio: 0.12
  subject_prominence: chest-up
  bottom_low_detail_ratio: 0.20
search:
  dark_overlay_opacities: [0, 20, 40]
content_strategy:
  # ── Luật viết CHỮ của lane satori (anh chốt 2026-09-23, xem docs/lanes/satori-jp-obaa/SOP_TIEU_DE_THUMBNAIL_2026-09-23.md)
  copy_doctrine:
    sop: docs/lanes/satori-jp-obaa/SOP_TIEU_DE_THUMBNAIL_2026-09-23.md
    must_be_spoken_line: true          # chữ là MỘT CÂU CÓ NGƯỜI NÓI RA, ưu tiên trích nguyên văn kịch bản trong 「」
    anchor_before_mystery: true        # phải có AI / Ở ĐÂU / CHUYỆN GÌ trước, rồi mới tới bí ẩn — cấm câu triết lý trừu tượng
    must_add_what_title_omits: true    # không nói lại thứ tiêu đề đã nói; tiêu đề ôm なぜ thì thumbnail không hỏi なぜ nữa
    hook_templates: [cau_hoi_thang, con_so_co_bi_mat, ket_qua_nguoc_ky_vong, mau_thuan_A_nhung_B, bi_mat_chua_noi, loi_thoai_soc]
    row_color_role_map: {WHITE: context, YELLOW: hero, TRIGGER: trigger, RED: twist, BANNER: banner}
    hard_char_limits: {context: 7, hero: 5, trigger: 7, twist: 7, banner: 12}
    numbers_as_digits: true            # 40年/25万/73歳 — không 四十年 (thành ngữ 一言/一行 giữ nguyên)
    scene_must_show_face: true         # tả nhân vật CÚI MẶT là gpti2 trượt cổng FACE, mất ảnh → luôn ghi FACE IS FULLY VISIBLE
  enforce_pre_render_review: true
  min_copy_directions: 3
  required_lenses: [contradiction, discovery_shock, emotional_conflict_secret]
  rubric:
    - story_accuracy
    - specificity
    - stakes
    - curiosity
    - title_complement
    - japanese_naturalness
    - one_two_second_clarity
  score_range: [1, 5]
  readability_hard_gate:
    enabled: true
    max_main_row_chars: 7
    clarity_score_key: one_two_second_clarity
    required_clarity_score: 5
    action_on_failure: rewrite_or_choose_another_hook
  specificity_over_brevity: false
  readability_and_specificity_are_co_gates: true
  seek_alternate_phrasing_or_hook_before_render: true
  title_thumbnail_complement: true
  no_semantic_weakening_for_font_size: true
  no_final_payoff_spoilers: true
  banner_must_add_independent_meaning: true
  forbidden_generic_banners: [衝撃の真実, まさかの結末, その理由とは？]
  post_render_questions:
    - can_any_row_be_materially_larger
    - is_there_wasted_safe_space
    - is_any_row_visibly_weak
    - does_visual_hierarchy_match_semantics
    - is_body_hand_prop_overprotected
    - does_360px_still_hit
    - is_visual_authority_materially_weaker_than_reference
scoring:
  visual_mass: 4.0
  min_row_authority: 3.0
  hero_prominence: 3.5
  hero_dominance: 3.0
  banner_weight: 2.0
  clearance_efficiency: 1.2
  wasted_space_penalty: 1.5
# Fable QC ảnh (S7, gộp 2026-09-22): tiêu chí TEMPLATE.md §9 lane satori (so với MASTER_REFERENCE); điểm 1-5 mỗi khoá.
fable_review:
  master_reference: docs/lanes/satori-jp-obaa/thumb/MASTER_REFERENCE.png
  score_keys: [japanese, story, typography, subject_scene, banner, impact360]
  criteria: |-
    1. japanese — 100% đúng glyph, đọc 1–2 giây, tự nhiên với người già Nhật; không spoil kết; không lặp title vô ích;
       không bịa chi tiết ngoài script.
    2. story — 3 dòng context → hero/hook → payoff nối thành 1 ý đúng script; banner đỏ thêm nghĩa ĐỘC LẬP (không phải
       衝撃の真実/まさかの結末/その理由とは？).
    3. typography — Táo bạo tương đương MASTER_REFERENCE: dòng hero rõ ràng lớn nhất (≥1.4× dòng khác), không khoảng
       trống chết bên trái, không dòng nào còn phóng to thêm được mà FACE vẫn sạch (câu hỏi này phải là NO).
    4. subject_scene — Nhân vật REF lớn ~1/3 phải, hoà tự nhiên vào cảnh toàn khung (KHÔNG panel chữ nhật/halo cutout/
       nền chia đôi đen-sáng); chữ KHÔNG đè mặt; cảnh sau chữ vẫn nhận ra ở 360px.
    5. banner — Banner đỏ gần full-width, đỏ bão hoà sạch, viền trắng, chữ trắng lớn nặng như master.
    6. impact360 — Ở 360px impact tương đương master (không chỉ "đọc được"); lỗi AI (tay/mặt biến dạng) trừ nặng.
```

## Thumbnail kênh mẫu
Chỉ chữ, không nhân vật, chép NGUYÊN tiêu đề (15/15), nền hoa mờ, chữ 3 màu viền dày.

<!-- export a3cda1862e52 · 2026-09-26 -->
