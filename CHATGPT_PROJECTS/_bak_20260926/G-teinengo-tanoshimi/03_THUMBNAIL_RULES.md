# 03 THUMBNAIL RULES — G-teinengo-tanoshimi

> Lane `teinengo-tanoshimi`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

KHÔNG dùng khuôn thumbnail của kênh khác. Khuôn riêng của lane này (file cấu hình máy dựng thumbnail):

```yaml
id: teinengo_tanoshimi
layout: bands_manga
dna_measured: true
delivery_contract:
  choices: 3
  labels:
  - A
  - B
  - C
  distinct_concepts: true
  distinct_visual_approaches: true
  selection_owner: human
  upload_public_links: true
  sheet:
    spreadsheet_id: 1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
    tab: G-teinengo-tanoshimi
    column: G
delivery_folder:
  root: E:/CLAUDE/YOUTUBE/CHANEL/G-teinengo-tanoshimi
  pattern: ep{stt:02d}-*
  filename: thumbnail.png
episode_sources:
  root: E:/CLAUDE/YOUTUBE/h2dev/assets/teinengo-tanoshimi
  require_character: false
structure:
  main_rows: 4
  min_rows: 2
  banner_required: false
font:
  path: ../../assets/fonts/NotoSansJP-Variable.ttf
  variation: Black
  fallback_path: C:/Windows/Fonts/YuGothB.ttc
composition:
  require_face: false
  subject_side: center
bands_manga:
  top_bar_ratio: 0.21
  top_bar_padding_ratio: 0.012
  top_bar_color: '#000000'
roles:
  top:
    color: '#FFFFFF'
    accent_color: '#FFE500'
    stroke_color: '#000000'
    stroke_ratio: 0.025
    width_ratio: 0.97
    max_chars: 13
    align: center
  lead:
    color: '#0A0A0A'
    box_color: '#FFE500'
    box_border: '#000000'
    box_padding_ratio: 0.22
    font_ratio: 0.1
    left_margin_ratio: 0.03
    gap_ratio: 0.02
    max_chars: 7
    optional: true
  quote:
    color: '#101010'
    bubble_color: '#FFFFFF'
    bubble_border: '#101010'
    font_ratio: 0.065
    side: auto
    top_ratio: 0.27
    max_chars: 8
    optional: true
  shock:
    color: '#E01010'
    accent_color: '#E01010'
    stroke_color: '#FFFFFF'
    stroke_ratio: 0.085
    shadow_ratio: 0.045
    shadow_color: '#2A0000'
    width_ratio: 0.94
    height_ratio: 0.24
    bottom_margin_ratio: 0.02
    max_chars: 9
    optional: true
banner: {}
background:
  provider_mode: text
  art_style: 'bright warm Japanese manga / anime illustration key art in the style of a retirement-life web comic: clean
    confident line art, flat cel shading, natural daylight or warm indoor light, an ordinary modern Japanese setting (living
    room, park, station, hot-spring town, supermarket, library); the main character is a Japanese man in his 60s with grey
    or silver hair, drawn LARGE so his expression reads on a phone; when the story compares two situations split the frame
    into 2-3 comic panels with thin white gutters. The top 21% and the bottom 24% must stay a PLAIN CONTINUATION OF THE
    SCENE (wall, floor, table, sky, ground) with no important detail — do NOT draw a coloured banner, a solid colour bar,
    a strip, a border or a title plate anywhere: those areas get typography laid over them later. NO text, no letters, no
    numbers, no speech bubbles, no logos, no watermark, no real photograph.'
  subject_position: centre
  keep_top_ratio: 0.26
  keep_bottom_ratio: 0.24
  forbid_real_person_likeness: true
content_strategy:
  lenses:
  - ranking_countdown
  - before_after_time
  - two_way_compare
  row_schema:
  - role: top
    max_chars: 13
    required: true
    description: 'TOP line inside the solid black bar. VERY SHORT natural Japanese, 7-11 characters, no punctuation clutter.
      Wrap the 2-5 character keyword in {curly braces} - that part is painted YELLOW, the rest stays white (the reference
      channel does this in 19/19 winning thumbnails). Example shape: 定年後、{図書館}が全て. Count only real characters: the two braces
      do not count toward the 11. RULE 1 (MANDATORY, measured on the reference channel: 17/20 winners obey it, all 3 videos
      that broke it lost): this line MUST reuse at least ONE content word that is literally written in the locked video title
      (定年後 / 60代 / the topic noun / the number+選 / the place). It echoes the title, it does not replace it - the rest of the
      line then adds the time, the place or the person that the title does not have. State which title word you reused in
      the rationale.'
  - role: lead
    max_chars: 7
    required: false
    description: 'Small YELLOW label box inside the artwork: a rank (第3位), a time jump (翌朝9時前) or the object that proves
      the story (妻の家計簿). 2-7 characters, no sentence. RULE 3 (MANDATORY when the episode is a ranking / N選 list, measured:
      4/4 winning ranking videos of the reference channel do this): show a MIDDLE rank only (第2位 / 第3位 / 第4位) and NEVER
      第1位 - the top item stays hidden so the viewer clicks to get it. RULE 5 (MANDATORY): the label must be a CONCRETE fact
      taken from the script - a number, an age, a price, a time, a place or a physical object (54歳・腰痛 / 片道2万円 / 11席だけ /
      妻の家計簿). A generic adjective or mood word (すごい効果 / 幸せな朝 / 意外な事実) is a FAIL.'
  - role: quote
    max_chars: 8
    required: false
    description: 'One short line of SPEECH from the character, drawn in a WHITE VERTICAL OVAL manga speech bubble with the
      characters stacked vertically (measured: 16/20 winners use the vertical oval): 3-8 characters, spoken Japanese, the
      reaction the viewer should feel (知らなかった / こんなに？ / もう戻れない). No narration. RULE 5 (MANDATORY): prefer a line that
      carries a concrete fact or a counter-intuitive item from the script (肉を食う / 何も買ってない / 孤独な生活) over a bare
      emotional adjective - what the reference channel puts in bubbles is information, not mood.'
  - role: shock
    max_chars: 9
    required: true
    description: 'The BIG RED payoff line across the lower artwork (red fill, thick white outline). 5-9 characters, the answer
      the viewer clicks for (道の下に川 / 暇に金を払う / 開館前に並ぶ). It must NOT repeat the top line, must be supported by the script,
      and must not spoil the final chapter. RULE 2 (MANDATORY, measured on all 19 thumbnails: winners paint 最強の / 最高の /
      共通点 red, the videos that painted 後悔 / 貧乏 / 残酷な現実 red are the whole losing group): anything drawn in RED - this line
      and any red accent inside the top bar - must be the DESIRABLE or SURPRISING-IN-A-GOOD-WAY side of the story: a
      superlative (最強の / 最高の), the shared trait that explains the win (意外な共通点), a reward (タダで一流), or a concrete
      counter-intuitive fact that is neutral-to-positive (誰かの息子かと / 開館前に並ぶ). A red line naming a loss, a decline, an
      illness, money trouble or regret (腕が上がらない / 半年で10キロ増 / 貧乏 / 後悔 / 手遅れ) is a FAIL even when the script supports
      it - put that content in the yellow label or the bubble instead, and keep red for the payoff.'
  banner_required: false
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
  - 残酷な現実
  - 手遅れ
  brief: 'Channel style measured 2026-09-23 on ALL 19 thumbnails of the reference channel 老後のお金ストーリー (UCI2cPqBmCPMxxKI4u2Gqs_Q).
    LOCKED look: (1) a SOLID BLACK bar over the top 21% of the frame holding ONE short headline in huge white type with
    the keyword painted yellow; (2) the artwork is a bright warm manga scene of a Japanese man in his 60s, usually 2-4 comic
    panels comparing two situations, faces large; (3) small yellow label boxes and white speech bubbles sit inside the artwork;
    (4) a HUGE RED line with a thick white outline across the lower artwork is the payoff. TEXT MUST BE SHORT: the reference
    channel uses 4-11 characters per line so the type can be enormous and readable on a phone. Never write a sentence where
    a phrase works. Every number, age, place and quote must come from the script; no invented figures, no generic hype (衝撃の真実
    / まさかの結末 / その理由とは？). Do not spoil the final chapter. FIVE MEASURED RULES THAT DECIDE WIN vs LOSE on this channel,
    all enforced in row_schema: (1) the black-bar line reuses at least one content word of the locked title (17/20 winners);
    (2) whatever is RED is the good/desirable/superlative side - red fear words are the losing group; (3) on a ranking episode
    show a middle rank and hide 第1位 (4/4 winners); (4) the speech bubble is a white VERTICAL oval with vertically stacked
    characters (16/20 winners); (5) labels and bubbles carry concrete facts or counter-intuitive items, never mood adjectives.'
  require_must_be_visible: false
scoring: {}
fable_review:
  score_keys:
  - japanese
  - story
  - hook_visible
  - motif
  - impact
  - curiosity
  criteria: '1. japanese — Tiếng Nhật tự nhiên, ĐỌC ĐƯỢC TRONG 1 GIÂY trên điện thoại; dòng trên 7–11 ký tự có {} tô vàng
    đúng cụm từ khoá; dòng đỏ 5–9 ký tự; không câu dài, không dấu thừa.

    2. story — Đúng kịch bản; KHÔNG bịa số/tuổi/chi tiết; dòng đỏ không lặp dòng trên; không spoil chương cuối. Tập xếp hạng
    thì nhãn vàng chỉ được hiện hạng GIỮA, CẤM 第1位 (luật 3, kênh gốc 4/4 video thắng đều giấu hạng 1).

    2b. 5 LUẬT ĐO ĐƯỢC — thiếu bất kỳ luật nào là TRỪ NẶNG, không phải gợi ý:
    (1) dòng băng đen PHẢI dùng lại ≥1 chữ nội dung có trong tiêu đề đã khoá (17/20 ảnh thắng; 3 ảnh phá luật đều thua);
    (2) chữ ĐỎ (dòng chốt + cụm đỏ trong băng) PHẢI là mặt TỐT/cực cấp/sự thật ngược thường thức trung tính-tích cực
    (最強の / 最高の / 意外な共通点 / 誰かの息子かと) — tô đỏ mất mát, bệnh, tăng cân, thiếu tiền, hối hận (腕が上がらない / 半年で10キロ増 /
    後悔 / 貧乏) là ĐÚNG KIỂU NHÓM THUA của kênh gốc ⇒ FAIL, đẩy nội dung đó xuống nhãn vàng hoặc bong bóng;
    (3) giấu hạng 1; (4) bong bóng là OVAL ĐỨNG chữ xếp dọc (16/20 — renderer đã vẽ đúng, đừng viết câu dài quá 8 ký tự
    kẻo cột chữ tràn); (5) nhãn vàng + bong bóng PHẢI mang SỰ THẬT CỤ THỂ (số/tuổi/giá/giờ/vật/món) hoặc mục ngược thường
    thức, KHÔNG phải tính từ cảm xúc chung (すごい効果 / 幸せな朝 / 意外な事実 = FAIL).

    3. hook_visible — Ảnh chứng minh được hook: mặt nhân vật TO, nhận ra cảm xúc ở 360px; có ít nhất 1 khung mặt tươi/bình
    thản (kênh gốc 20/20 như vậy).

    4. motif — Đúng khuôn kênh gốc: thanh ĐEN đặc trên (21% H) chữ trắng + cụm VÀNG · nhãn vàng chữ đen trong tranh · bong
    bóng thoại trắng · dòng ĐỎ viền TRẮNG dày ở nửa dưới. Thiếu thanh đen hoặc thiếu cụm vàng = trừ nặng.

    5. impact — Chữ TO hết cỡ, không có khoảng trống chết; ở 360px chữ và mặt đều đọc ngay.

    6. curiosity — Gây tò mò/sốc đúng khán giả hưu trí Nhật 60-75; cấm cụm sáo rỗng.'
```

<!-- export 7cb37cf2df7e · 2026-09-26 -->
