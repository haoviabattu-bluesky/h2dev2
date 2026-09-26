# 03 THUMBNAIL RULES — K-yakkyoku-sukatto

> Lane `yakkyoku-sukatto`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

KHÔNG dùng khuôn thumbnail của kênh khác. Khuôn riêng của lane này (file cấu hình máy dựng thumbnail):

```yaml
# Lane K `yakkyoku-sukatto` (薬局スカッと帳, tab K-yakkyoku-sukatto) — viết tay 2026-09-25 từ số đo PIXEL 4/4 thumbnail video dài
# kênh mẫu 千種テンカ (UCEBA1RFfkXQtqgiDVLh4bcw), ảnh ở E:/CLAUDE/YOUTUBE/h2dev/FlowHandoff_local/results/laneK_from_research/data/thumbs/.
# 4 khuôn cũ (bands/bands_manga/panel/stack_left) + bar_panels đều không dựng được 2 bóng thoại chữ dọc → layout MỚI
# `dialogue_split` (thumbnail_engine/dialogue_split.py). Trạng thái: PILOT.
# Số đo (1280×720, trùng từng pixel cả 4 ảnh): dải vàng #FDE006 x 550–731 (43,0–57,2% W), viền đen ~5 px hai bên ·
# chữ dải: đen + đỏ #D02414 (7–14% diện tích dải) · bóng trái chữ xanh #1B3EB0, bóng phải chữ đỏ #CC2325 · vùng chữ
# bóng: đỉnh ~13% H, đáy 37–60% H, ở phía NGOÀI panel (trái x 5–16%, phải x 83–92%).
# thumbnail_rule tự động trong title_intel/yakkyoku-sukatto.json SAI (ghi "không có người") — đừng dùng.
id: yakkyoku_sukatto
layout: dialogue_split
dna_measured: false
delivery_contract:
  choices: 3
  labels: [A, B, C]
  distinct_concepts: true
  distinct_visual_approaches: true
  selection_owner: human
  upload_public_links: true
  sheet: {spreadsheet_id: 1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU, tab: K-yakkyoku-sukatto, column: G}
delivery_folder:
  {root: 'E:/CLAUDE/YOUTUBE/CHANEL/K-yakkyoku-sukatto', pattern: 'ep{stt:02d}-*', filename: thumbnail.png}
episode_sources:
  {root: 'E:/CLAUDE/YOUTUBE/h2dev/assets/yakkyoku-sukatto', require_character: false}
structure:
  {main_rows: 3, min_rows: 3, banner_required: false}
font:
  {path: ../../assets/fonts/NotoSansJP-Variable.ttf, variation: Black, fallback_path: 'C:/Windows/Fonts/YuGothB.ttc'}
composition:
  {require_face: false, subject_side: center}
dialogue_split:
  band_x0: 0.430
  band_x1: 0.572
  band_color: '#FDE006'
  band_edge_color: '#111111'
  band_edge_ratio: 0.0039
  bubble_top_ratio: 0.10
  bubble_edge_ratio: 0.016
roles:
  band:
    color: '#111111'
    accent_color: '#D02414'
    max_chars_per_col: 13
    pad_ratio: 0.03
    max_chars: 34
  quote_left:
    color: '#1B3EB0'
    font_ratio: 0.066
    max_chars_per_col: 5
    max_cols: 3
    max_chars: 14
  quote_right:
    color: '#CC2325'
    font_ratio: 0.066
    max_chars_per_col: 5
    max_cols: 3
    max_chars: 14
banner: {}
background:
  provider_mode: text          # tập không có REF → gpti2_text; có `_ref_<id>/001.png` → gpti2 edit 2 REF (cast_refs)
  cast_refs: true
  art_style: >-
    clean semi-realistic Japanese webtoon manga illustration of a Japanese workplace drama (dispensing pharmacy, pharmacy
    back office, head-office meeting room, interview room): crisp ink line art, soft cel shading, bright natural light,
    realistic adult proportions; pharmacists wear white lab coats over shirt and tie or blouse, office staff and managers
    wear dark suits; faces large with clear readable expressions (calm, smug, cold, troubled)
  subject_position: centre
  keep_top_ratio: 0.0
  keep_bottom_ratio: 0.0
  forbid_real_person_likeness: true
content_strategy:
  lenses: [catchphrase_vs_answer, consequence_moment, open_question]
  row_schema:
    - role: band
      max_chars: 34
      required: true
      description: >-
        VERTICAL text in the YELLOW centre band, read top-to-bottom, right column first. Write it as 1-2 columns separated
        by "/", 16-26 real characters in total. Wrap the 1-2 words that carry the promise in [square brackets] = RED, the
        rest is black. Measured shape on 4/4 reference thumbnails - a SHORTENED rewrite of the title, never the full title:
        [「自分、仕事できるんで」]/が口ぐせの男が[行き着く先] · [閉店2分前]に患者を/追い返した薬剤師の[結末] · 口ぐせ[「辞めます」]の/薬剤師に[店長]が返した言葉 ·
        [横柄]な薬剤師の[結末]/定年後[6]社目の面接にて. The catchphrase in 「」 must be the protagonist's real repeated line
        from the script. Numbers as digits (6社目, 2分前). Brackets and "/" do not count toward the 26.
    - role: quote_left
      max_chars: 14
      required: true
      description: >-
        BLUE speech bubble in the LEFT panel = what the OTHER person (the one who delivers the consequence: 店長 /
        面接官 / エリアマネージャー / 事務さん) says. 4-12 characters, a real line or a faithful short version of a line in the
        script, calm and polite, the answer that hurts (更新はしません / 残念ながら、不採用です / わかりました / 人にどう接するかで採っています).
        Must not reveal the final outcome of the story in full. Optional "/" sets the column break (分かり/ました).
    - role: quote_right
      max_chars: 14
      required: true
      description: >-
        RED speech bubble in the RIGHT panel = the PROTAGONIST's catchphrase, copied VERBATIM from the script (4/4 reference
        thumbnails: 自分、仕事できるんで / 残業代入んないんで / じゃあ、辞めます / あんたの代わりはいくらでもいる). 4-12 characters.
        Optional "/" sets the column break at a natural point (自分、/仕事/できるんで) - "/" does not count.
  banner_required: false
  require_must_be_visible: false
  rubric: [story_accuracy, specificity, curiosity, title_complement, japanese_naturalness, one_two_second_clarity, no_fabrication]
  forbidden_phrases: [復讐, 仕返し, ざまあ, 天罰, 衝撃の真実, まさかの結末, 末路, 副作用, 効果がある]
  brief: >-
    Reference channel 千種テンカ (UCEBA1RFfkXQtqgiDVLh4bcw), workplace manga about a pharmacist with a toxic catchphrase
    who meets consequences from the SYSTEM (contract, schedule, interview), never personal revenge. ONE FIXED TEMPLATE
    measured on 4/4 long-video thumbnails: LEFT panel = the other person (manager / interviewer / HR) in a dark suit or lab
    coat with a BLUE-text speech bubble; RIGHT panel = the protagonist pharmacist in a white lab coat with a RED-text
    speech bubble holding his catchphrase; a YELLOW vertical band in the centre with black vertical text and 1-2 RED words.
    The two faces look towards each other; the contrast is confident/smug catchphrase vs calm, polite answer that seals
    the consequence. ENGINE: the renderer draws the yellow band, both speech bubbles and all text itself. The scene_prompt
    MUST start with "LEFT PANEL (<the other person's role word exactly as the script writes it, e.g. 店長 / エリアマネージャー / 面接官>): …
    / RIGHT PANEL (主人公): …" and describe only the two people, their expression and a plain workplace background; it
    must NEVER ask for text, speech bubbles, empty ovals, labels or a title bar. Do not spoil the ending.
scoring: {}
fable_review:
  score_keys: [japanese, story, hook_visible, motif, impact, curiosity]
  criteria: |-
    1. japanese — Tiếng Nhật tự nhiên; dải vàng 16–26 chữ (1–2 cột, cột ngắt bằng "/"), 1–2 cụm [đỏ]; mỗi bóng thoại 4–12 chữ; số viết chữ số Ả Rập (6社目 không 六社目).
    2. story — Bóng PHẢI trích NGUYÊN VĂN câu cửa miệng của nhân vật chính trong kịch bản; bóng TRÁI là câu thật (hoặc rút gọn trung thành) của người đưa hậu quả; không bịa; không lộ kết cục; không có từ trả thù (復讐/仕返し/ざまあ/天罰).
    3. hook_visible — Ở 360px thấy ngay 2 người đối mặt: bên phải tự tin/ngạo, bên trái điềm tĩnh; mặt to, cảm xúc rõ; bóng thoại không che mặt.
    4. motif — Đúng khuôn 4/4 kênh mẫu: dải VÀNG dọc giữa (43–57% W) chữ đen + đỏ · bóng TRÁI chữ XANH · bóng PHẢI chữ ĐỎ · tranh manga bán thực, nhân vật chính áo blouse trắng. Không chép nguyên tiêu đề lên dải.
    5. impact — Chữ to đọc được ở 360px; ảnh không có chữ rác/bóng thoại rỗng/tay lỗi; mặt khớp nhân vật trong video (REF).
    6. curiosity — Sức hút với người Nhật đi làm từng gặp đồng nghiệp né việc bằng 1 câu cửa miệng; cấm 衝撃の真実, まさかの結末, 末路.
```

## Thumbnail kênh mẫu
(đo pixel 4/4 ảnh thật 2026-09-25 — dữ liệu tự động cũ ghi 'không có người' là SAI) 2 nhân vật manga đối mặt chia đôi khung; bong bóng thoại trái chữ XANH DƯƠNG (người đối chất), phải chữ ĐỎ = câu cửa miệng của dược sĩ; dải VÀNG dọc giữa, chữ dọc đen + 1–2 cụm ĐỎ nhấn (rút gọn tinh thần tiêu đề, không chép nguyên tiêu đề).

<!-- export 9b37b7ff3589 · 2026-09-26 -->
