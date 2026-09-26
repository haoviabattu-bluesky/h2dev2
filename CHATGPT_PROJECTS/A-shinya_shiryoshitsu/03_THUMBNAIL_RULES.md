# 03 THUMBNAIL RULES — A-shinya_shiryoshitsu · toshi-densetsu-jp

> Lane `toshi-densetsu-jp`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

KHÔNG dùng khuôn thumbnail của kênh khác. Khuôn riêng của lane này (file cấu hình máy dựng thumbnail):

```yaml
id: toshi_densetsu_jp
layout: bands
delivery_contract:
  choices: 3
  labels: [A, B, C]
  distinct_concepts: true
  distinct_visual_approaches: true
  selection_owner: human
  upload_public_links: true
  sheet:
    spreadsheet_id: 1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU
    tab: A-shinya_shiryoshitsu
    column: G
delivery_folder:
  root: E:/CLAUDE/YOUTUBE/CHANEL/A-shinya_shiryoshitsu
  pattern: "ep{stt:02d}-*"
  filename: thumbnail.png
episode_sources:
  # Sheet column C points at the SPACE_RESEARCH dossier; the produced episode lives in h2dev.
  root: E:/CLAUDE/YOUTUBE/h2dev/assets/toshi-densetsu-jp
  folder_pattern: "ep{basename}"
  require_character: false
structure:
  main_rows: 3
  min_rows: 2
  banner_required: false
font:
  path: ../../assets/fonts/ShipporiMinchoB1-ExtraBold.ttf
  fallback_path: C:/Windows/Fonts/YuGothB.ttc
composition:
  require_face: false
  subject_side: center
# Số đo MÁY trên 28 thumbnail kênh gốc 今夜も都市伝説 (2026-09-23, data/thumb_dna/toshi-densetsu-jp/out):
# băng trên cao 0,19–0,22 H · băng dưới 0,21–0,23 H · cả hai rộng 0,97–0,99 W · vàng #F5F62A–#FDFD0B ·
# đỏ #EF0707–#F00607 viền đen RẤT dày · độ phủ chữ q25 0,391 / trung vị 0,427 (video view thấp chỉ 0,21–0,27).
# 8 thumbnail cũ của lane đo được 0,268–0,367 → nâng height/width/stroke để chữ to bằng kênh gốc.
roles:
  top:
    band: top
    color: '#FBEE08'
    stroke_color: '#0A0A12'
    stroke_ratio: 0.10
    max_chars: 16
    width_ratio: 0.985
    height_ratio: 0.235
    top_margin_ratio: 0.02
    align: center
  lead:
    band: lead
    optional: true
    color: '#FFFFFF'
    stroke_color: '#000000'
    stroke_ratio: 0.12
    max_chars: 12
    font_ratio: 0.092
    left_margin_ratio: 0.018
    gap_ratio: 0.012
    align: left
  shock:
    band: bottom
    color: '#F00607'
    stroke_color: '#000000'
    stroke_ratio: 0.13
    max_chars: 14
    width_ratio: 0.99
    height_ratio: 0.25
    bottom_margin_ratio: 0.015
    align: center
banner: {}
bands:
  top_shade_ratio: 0.24
  bottom_shade_ratio: 0.30
  shade_max_alpha: 110
background:
  provider_mode: text
  art_style: >-
    cinematic dark documentary key art, deep navy and black palette with a faint violet or teal nebula glow,
    strong dramatic key light and a bright glow source on the subject (lights, beams, fire, screens or moonlight),
    volumetric light, heavy contrast, photorealistic, 8K; the subject itself must read as BRIGHT against the dark frame
  subject_position: centre
  keep_top_ratio: 0.22
  keep_bottom_ratio: 0.26
  forbid_real_person_likeness: true
content_strategy:
  lenses: [mask_answer, witness_quote, negation_or_cover_up]
  row_schema:
    - {role: top, max_chars: 16, required: true, description: "YELLOW headline: a noun phrase naming WHO did WHAT, in the channel's house pattern 『〜した男』 / 『Xが暴露した』 / 『〜した本当の理由』 (measured 6/9 on the reference channel). It MUST read as a complete idea on its own - never the first half of a sentence that the RED band finishes. Natural Japanese <=16 chars."}
    - {role: lead, max_chars: 12, required: false, description: "WHITE small lead-in line above the shock: the source or the timeframe (『1917年の証言』, 『100年前に答えは出ていた』). Present on 5/9 reference thumbnails - prefer including it. <=12 chars."}
    - {role: shock, max_chars: 14, required: true, must_contain_any: ["「", "●●"], description: "RED biggest shock line <=14 chars; MUST be either a 「witness quote taken WORD FOR WORD from the script AND spoken inside the first 40-60 seconds of it」 or a statement whose one concrete answer (an identity, object or name that the video reveals) is masked with ●●, e.g. 正体は●●だった. Never use ●● as a vague 'something' or inside a negative/inconclusive sentence. It must be a SENTENCE someone says - not a single word in quotation marks (「神話」, 「大統領」 are rejected), and it must not repeat what the title already says."}
  banner_required: false
  rubric:
    - story_accuracy
    - specificity
    - curiosity
    - title_complement
    - japanese_naturalness
    - one_two_second_clarity
    - no_fabrication
  forbidden_phrases: [衝撃の真実, まさかの結末, その理由とは？, 抹殺された, 消された天才]
  brief: >-
    Channel: Japanese 都市伝説 / 宇宙 / ミステリー documentary narration (third person, calm male voice). Thumbnail motif
    locked for the whole channel: a YELLOW full-width headline band at the top (premise), an optional small WHITE
    lead-in line, and a RED full-width shock band at the bottom that is the largest text and is either a 「witness quote
    taken from the script」 or masks ONE concrete answer that the video reveals with ●● (正体は●●だった); never use ●● for a
    vague "something" or in a negative/inconclusive sentence. The image is ONE cinematic AI key-art scene where the
    subject is HUGE, bright and glowing (UFO lights, beams, planets, pyramids, secret facilities); humans appear as
    silhouettes seen from behind or as small figures under the object — do not demand a clearly visible face; no real
    person's face or likeness, no recurring character, and NO copyrighted/trademarked characters, mascots or logos
    (describe an abstract or generic stand-in instead; the image API rejects them).
    Copy must be strictly supported by the script: never invent conspiracies, murders, cover-ups or deaths that the
    script does not state; mark claims the script frames as theories the same way (〜という説). Do not spoil the
    final chapter's conclusion. Prefer the concrete detail the title does not already reveal.
scoring: {}
# Fable QC ảnh (S7, gộp 2026-09-22): tiêu chí TEMPLATE.md §4 lane A; điểm 1-5 mỗi khoá, chọn 1 trong A/B/C.
fable_review:
  score_keys: [japanese, story, hook_visible, motif, impact, curiosity]
  criteria: |-
    1. japanese — Tiếng Nhật tự nhiên, đọc 1–2 giây; băng đỏ BẮT BUỘC có 「」 (lời nhân chứng) hoặc ●● che ĐÚNG 1 đáp án
       cụ thể; ngắt dòng không đổi nghĩa; glyph đúng 100%.
    2. story — Đúng script; KHÔNG bịa âm mưu/cái chết/thủ tiêu; bổ sung cho title (không lặp); không spoil chương cuối;
       claim script gọi là thuyết thì phải giữ khung 〜という説.
    3. hook_visible — Ảnh CHỨNG MINH hook: chủ thể to, sáng, nhận ra ở 360px; ●● không bị chính ảnh làm lộ đáp án;
       không mặt người thật rõ nét; không nhân vật/logo có bản quyền.
    4. motif — Băng VÀNG trên (tiền đề) / băng ĐỎ dưới TO NHẤT, full-width, chữ phủ ≥30% khung, không đè chủ thể chính,
       tông xanh-lạnh/tối bí ẩn cùng nhà với 12 mẫu kênh (research/COMPETITOR_TOP12).
    5. impact — Ở 360px chữ và chủ thể đều đọc ngay; lỗi AI (tay/chữ rác/vật sai era) trừ nặng.
    6. curiosity — Sức hút bấm với khán giả 都市伝説 25-55 hoài nghi, soi số.
```

## Thumbnail kênh mẫu
Bố cục cố định 9/9: 2 băng chữ trải NGANG toàn khung — trên: vàng viền đen, font có chân (Mincho) — dưới: đỏ viền đen, font nét cọ sần, to nhất; chủ thể AI điện ảnh ở giữa; nền xanh navy/đêm 8/9 (OU1r tím-hồng). Chữ đỏ trong 「」 6/9; ●● che đáp án 4/9 (đều thuộc 6 top: OU1r, GTwo, gWF, 8miF); dòng trắng nhỏ dẫn vào chữ đỏ 5/9 (人類の脅威は、/100年前に答えは出ていた/キリストの正体は…/エドガー・ケイシーが語った/火星の恐ろしい真相); mũi tên đỏ 5/9; có hình người (AI, không phải ảnh thật) 7/9. Chữ vàng thường là 『chủ thể + した男』 (5/9) hoặc 『X が暴露した / X が正しかった / 本当の理由』.

<!-- export 7c146d33f87d · 2026-09-26 -->
