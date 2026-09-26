# 03 THUMBNAIL RULES — E-70dai-kenko · kenko-chiebukuro

> Lane `kenko-chiebukuro`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

KHÔNG dùng khuôn thumbnail của kênh khác. Khuôn riêng của lane này (file cấu hình máy dựng thumbnail):

```yaml
id: kenko_chiebukuro
layout: stack_left
# Dải dọc 4 dòng = TRUNG VỊ đo máy trên 26/27 ảnh 4 dòng (top 0,05/0,27/0,48/0,71 · cao 0,19/0,18/0,21/0,22 H);
# ANH CHỐT 2026-09-24 (sau pilot ep01): ảnh phải thấy ĐỦ các món (hoặc cụ bà khoẻ vui bên các món), chữ nói thẳng
# 「5つの食べ物 / 意外な効果 / 知らないかも」 — KHÔNG làm kiểu 1 món giấu tên nữa.
# PILOT (2026-09-24): khuôn viết tay từ số đo 27/27 thumbnail kênh mẫu シニアいきいき健康 — xem
# docs/lanes/kenko-chiebukuro/thumb/DO_THUMB_KENH_MAU_2026-09-24.md. Bộ đo tools/thumb_dna_measure chỉ hiểu khuôn
# `bands` (băng trên/dưới) nên KHÔNG dùng được cho khuôn 4 dòng xếp chồng này → không có thumb_dna.json, không `lane-lock`.
dna_measured: false
delivery_contract:
  choices: 3
  labels: [A, B, C]
  distinct_concepts: true
  distinct_visual_approaches: true
  selection_owner: human
  upload_public_links: true
  sheet:
    spreadsheet_id: 1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
    tab: E-70dai-kenko
    column: G
delivery_folder:
  root: E:/CLAUDE/YOUTUBE/CHANEL/E-70dai-kenko
  pattern: ep{stt:02d}-*
  filename: thumbnail.png
episode_sources:
  # Cột C của tab E-70dai-kenko trỏ THẲNG vào thư mục tập h2dev → không cần folder_pattern.
  root: E:/CLAUDE/YOUTUBE/h2dev/assets/kenko-chiebukuro
  require_character: false
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
  subject_side: right
stack_left:
  panel_color: '#000000'
  shade_solid_ratio: 0.44     # nền đen đặc tới 44 % W …
  shade_fade_ratio: 0.14      # … rồi mờ dần tới 58 % W (ảnh món bắt đầu hiện rõ)
  left_margin_ratio: 0.022
  text_width_ratio: 0.62      # kênh mẫu: chữ chạy tới ~60 % W, chồm nhẹ lên mép ảnh
roles:
  aim:        # dòng 1 CAM — đối tượng / tuổi / con số mở (「100歳まで元気な人」「特に60歳からは」)
    color: '#F39800'
    stroke_color: '#1A0E00'
    stroke_ratio: 0.02
    top_ratio: 0.05
    height_ratio: 0.19
    max_chars: 10
  hook:       # dòng 2 TRẮNG — nói thẳng danh sách có số (「5つの食べ物」「体にいい5品」)
    color: '#FFFFFF'
    stroke_color: '#000000'
    stroke_ratio: 0.03
    shadow_ratio: 0.03
    top_ratio: 0.27
    height_ratio: 0.18
    max_chars: 10
  hide:       # dòng 3 ĐỎ to — câu kéo rõ ràng (「意外な効果」「知らないかも」「実はすごい」)
    color: '#E60012'
    stroke_color: '#FFFFFF'
    stroke_ratio: 0.05
    top_ratio: 0.48
    height_ratio: 0.21
    max_chars: 8
  gain:       # dòng 4 XANH LÁ — lợi ích / cảm xúc (「医師も驚いた」「朝までぐっすり!!」)
    color: '#1E6B1E'
    stroke_color: '#FFFFFF'
    stroke_ratio: 0.05
    top_ratio: 0.71
    height_ratio: 0.22
    max_chars: 10
    optional: true
banner: {}
background:
  provider_mode: text
  art_style: 'bright, clear, appetising real food photograph for a Japanese senior-health YouTube channel, photorealistic,
    ALL the foods named in the episode shown together and each one instantly recognisable at phone size (separate small
    bowls, plates or glasses neatly arranged on a warm wooden table, or held around a smiling healthy Japanese woman in her
    70s), soft bright daylight, rich natural colour, sharp focus on every food, the background behind the foods dark so it
    melts into the black left side; no text, no labels on packages'
  subject_start_ratio: 0.45
content_strategy:
  lenses:
    - all_items_spread
    - happy_senior_with_items
    - unexpected_benefit
  row_schema:
    - role: aim
      max_chars: 10
      required: true
      description: 'LINE 1, ORANGE. Who it is for or the situation, plain words (70歳からの / 転ぶ前に / 毎日の食卓に). 4-10 characters.
        Arabic numerals only (70歳, 5つ).'
    - role: hook
      max_chars: 10
      required: true
      description: 'LINE 2, WHITE. State the list plainly with its number: 5つの食べ物 / 体にいい5品 / 骨と筋肉に5品. The viewer must
        understand in one second that the video gives FIVE foods.'
    - role: hide
      max_chars: 8
      required: true
      description: 'LINE 3, RED, big. A plain pull phrase, pick from: 意外な効果 / 実はすごい / 知らないかも / 見直された. No riddle,
        no question mark, no cure claim.'
    - role: gain
      max_chars: 10
      required: false
      description: 'LINE 4, GREEN. The plain benefit the script supports (骨と筋肉の材料 / 転ばない体へ / 毎日足すだけ). 4-10
        characters. Never a number or promise that is not in the script.'
  banner_required: false
  require_must_be_visible: false
  require_evidence_quote: true
  rubric:
    - story_accuracy
    - specificity
    - curiosity
    - title_complement
    - japanese_naturalness
    - one_two_second_clarity
    - no_fabrication
  forbidden_phrases:
    - 衝撃の真実
    - まさかの結末
    - その理由とは？
    - 完治
    - 治る
    - 必ず治
    - 薬がいらない
    - 医者いらず
  brief: 'Senior-health channel for Japanese viewers 65-85. Owner rule (2026-09-24, overrides the reference-channel habit of
    showing one hidden item): the thumbnail must be CLEAR at a glance - the picture shows ALL the foods / items the video
    recommends (for a 5-item list: all 5, each clearly recognisable, e.g. separate small bowls on one table), OR a smiling
    healthy Japanese woman in her 70s together with those foods. Never a single item alone, never a food that is not in the
    list. Layout: black left side with four stacked lines (ORANGE who/when, WHITE the list with its number e.g. 5つの食べ物,
    big RED pull like 意外な効果 / 知らないかも, GREEN plain benefit), photograph on the right. Copy must be plain, friendly
    and positive, readable in one second on a phone; every claim supported by the script; Arabic numerals.
    SELF-CHECK / WARNING-SIGN EPISODES (no foods, e.g. 5つのサイン): show ONE Japanese woman in her late 60s clearly DOING
    the sign from the hook (e.g. pushing both hands on the floor to stand up from a floor cushion), face large and readable,
    or 2-4 clear scenes of the signs in the list (never the 第1位 test); the hide line then says the plain pull, e.g.
    筋肉が減るサイン, and the hook line states the list, e.g. 自宅で5つ確認.
    COPY STYLE IS PLAIN, NOT CLEVER (owner approved exactly this kind): 転ぶ前に / 体にいい5つの食べ物 / 意外な効果 /
    知らない人が多い · 骨と筋肉のために / 毎日食べたい5品 / 実はすごい / 意外と知らない. No wordplay, no riddles with a
    question mark (プルーンと骨?), no abstract phrases (必要なものが違う / 年だけじゃない).
    scene_prompt MUST name every food of the list explicitly in English (e.g. "five small bowls: grilled salmon and a boiled
    egg, dried prunes, a glass of milk, tiny whole dried fish, natto") and ask for all of them to be clearly visible.'
scoring: {}
fable_review:
  score_keys:
    - japanese
    - story
    - hook_visible
    - motif
    - impact
    - curiosity
  criteria: '1. japanese — Tiếng Nhật tự nhiên, đọc trong 1 giây trên điện thoại; mỗi dòng 3–10 ký tự; chữ số Ả Rập (70歳).

    2. story — Đúng kịch bản; ảnh thể hiện ĐỦ các món trong danh sách (không thiếu, không món lạ); không claim chữa khỏi, không bịa số.

    3. hook_visible — Từng món nhận ra ngay ở 360px (hoặc cụ bà khoẻ vui bên các món), sắc nét, nằm nửa phải, không bị chữ che.

    4. motif — Nền đen trái + 4 dòng cam/trắng/ĐỎ to/xanh lá neo mép trái + ảnh ĐỦ các món (hoặc cụ bà khoẻ bên các món) bên phải.

    5. impact — Chữ TO hết cỡ, dòng đỏ to nhất; không khoảng trống chết.

    6. curiosity — Rõ ràng + tò mò: người 70+ hiểu ngay "5 món tốt cho sức khoẻ" và muốn biết công dụng không ngờ; không doạ dẫm.'
```

<!-- export 12d2ba70a351 · 2026-09-26 -->
