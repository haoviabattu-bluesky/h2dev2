# 03 THUMBNAIL RULES — L-shakai-no-naze · shakai_no_naze

> Lane `shakai_no_naze`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

KHÔNG dùng khuôn thumbnail của kênh khác. Khuôn riêng của lane này (file cấu hình máy dựng thumbnail):

```yaml
# Lane L `shakai_no_naze` (社会のなぜ研究室, tab L-shakai-no-naze) — viết tay 2026-09-24 từ số đo PIXEL 11/11 thumbnail kênh mẫu
# 社会のウラガワ (UCFWFKb3Yr_1SrAT0kcvwFdw). Bộ đo tools/thumb_dna_measure KHÔNG hiểu khuôn này (thanh đen + 2 nhãn panel, không có
# dòng chốt đáy) nên không sinh được thumb_dna.json hợp lệ → layout MỚI `bar_panels` (thumbnail_engine/bar_panels.py). Trạng thái: PILOT.
# Số đo (1280×720): thanh đen 0–116 px (16,1% H) ở 11/11 · nhãn vàng #FCC200 viền đen y 142–237 (19,7–32,9% H) ở 11/11, 1 nhãn/panel,
# căn giữa panel · vạch chia giữa x 638–643 ở 10/11 · chữ thanh: trắng #FFFFFF + vàng #FACA28 + đỏ #FA3232 · 10/11 dòng thanh kết 理由.
# Chi tiết + ảnh lưới: docs/lanes/shakai_no_naze/SOP_TIEU_DE_THUMBNAIL_2026-09-24.md
id: shakai_no_naze
layout: bar_panels
dna_measured: false
delivery_contract:
  choices: 3
  labels: [A, B, C]
  distinct_concepts: true
  distinct_visual_approaches: true
  selection_owner: human
  upload_public_links: true
  sheet: {spreadsheet_id: 1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU, tab: L-shakai-no-naze, column: G}
delivery_folder:
  {root: 'E:/CLAUDE/YOUTUBE/CHANEL/L-shakai-no-naze', pattern: 'ep{stt:02d}-*', filename: thumbnail.png}
episode_sources:
  {root: 'E:/CLAUDE/YOUTUBE/h2dev/assets/shakai_no_naze', require_character: false}
structure:
  {main_rows: 3, min_rows: 3, banner_required: false}
font:
  {path: ../../assets/fonts/NotoSansJP-Variable.ttf, variation: Black, fallback_path: 'C:/Windows/Fonts/YuGothB.ttc'}
composition:
  {require_face: false, subject_side: center}
bar_panels:
  top_bar_ratio: 0.161
  top_bar_padding_ratio: 0.012
  top_bar_color: '#000000'
  gutter_ratio: 0.0047
  gutter_color: '#000000'
  label_top_ratio: 0.838   # 2026-09-25 anh chốt: nhãn vàng xuống ĐÁY panel (kênh mẫu để 19,7% H nhưng ở ảnh mình CHE MẶT 3/3 tập)
  label_height_ratio: 0.132
  label_max_width_ratio: 0.94
roles:
  top:
    color: '#FFFFFF'
    accent_color: '#FACA28'
    accent2_color: '#FA3232'
    stroke_color: '#000000'
    stroke_ratio: 0.0
    width_ratio: 0.985
    max_chars: 19
    align: center
  lead:
    color: '#000000'
    box_color: '#FCC200'
    box_border: '#000000'
    max_chars: 9
  lead2:
    color: '#000000'
    box_color: '#FCC200'
    box_border: '#000000'
    max_chars: 9
banner: {}
background:
  provider_mode: text
  art_style: >-
    clean bright modern Japanese anime illustration (semi-realistic anime, soft cel shading, crisp line art, warm natural
    light) of ordinary modern Japan (open-plan office, meeting room, care home, apartment living room, phone shop, cafe,
    street); adults drawn with realistic proportions and readable expressions; when a young Japanese woman about 25 appears
    she has long straight BLACK hair tied in a low ponytail and brown eyes (the channel's recurring character Sakura)
  subject_position: centre
  keep_top_ratio: 0.22   # 25/09: nhãn đã xuống đáy → chỉ chừa thanh đen
  keep_bottom_ratio: 0.0
  forbid_real_person_likeness: true
content_strategy:
  lenses: [cause_vs_result, two_sides_contrast, open_question]
  row_schema:
    - role: top
      max_chars: 19
      required: true
      description: >-
        ONE line inside the solid black top bar, 9-15 real characters, THREE colours: wrap the SUBJECT GROUP (who: Z世代 /
        若手 / 賢い人 / 独身男性 / 氷河期世代) in {curly braces} = YELLOW, wrap the SHOCK KEYWORD (大量解雇 / 群れない / 爆増 /
        昇進を拒む) in [square brackets] = RED, everything else stays white. Measured shape on 10/11 reference thumbnails:
        {主語}が[キーワード]する理由 / {主語}ほど[キーワード]な理由 (1/11 ends 末路). It is a REWRITE of the title question
        into a flat statement ending in 理由 - shorter and punchier than the title, never the title copied. Braces and
        brackets do not count toward the 15. Numbers as digits (6倍, 77%), never kanji numerals.
    - role: lead
      max_chars: 9
      required: true
      description: >-
        YELLOW label box at the BOTTOM of the LEFT panel, 4-8 characters, black text. A short claim, an inner voice or a hard
        fact that the left picture proves (打たれ弱い / なんでもパワハラ / 独身は勝ち組 / 高すぎるiPhone). Left panel = the CAUSE
        or the common belief. Any number must be written in the script.
    - role: lead2
      max_chars: 9
      required: true
      description: >-
        YELLOW label box at the BOTTOM of the RIGHT panel, 4-8 characters, black text. The RESULT, the other side, or the
        hidden answer teased (すぐ辞める / 誰も助けない / 転職者数が6倍 / ○○が原因). Must not repeat the left label or the
        top line. Any number must be written in the script (the reference channel puts ONE real statistic here in 3/11:
        転職者数が6倍 / 15年で10倍 / ストレスが0).
  banner_required: false
  require_must_be_visible: false
  rubric: [story_accuracy, specificity, curiosity, title_complement, japanese_naturalness, one_two_second_clarity, no_fabrication]
  forbidden_phrases: [衝撃の真実, まさかの結末, その理由とは？, 驚愕, ヤバすぎる]
  brief: >-
    Reference channel 社会のウラガワ (UCFWFKb3Yr_1SrAT0kcvwFdw), anime-manga explainers of Japanese social phenomena
    (なぜ〜のか). ONE FIXED TEMPLATE measured on 11/11 thumbnails: (1) a SOLID BLACK bar over the top 16% holding ONE line
    in three colours - yellow subject group, red shock keyword, white particles - that rewrites the title question as
    「〇〇が△△する理由」 (10/11); (2) EXACTLY 2 anime panels split at the centre line, one scene each, faces large and
    emotional; the two panels CONTRAST (cause vs result / belief vs reality / two sides); (3) one YELLOW label box with
    black outline at the BOTTOM of EACH panel (4-8 characters; the reference channel puts it at the top, we moved it to the bottom because it covered faces). The recurring young woman Sakura (long black hair, low
    ponytail, ~25) appears in 6/11 thumbnails - use her in one panel when she is in the script. ENGINE: the renderer draws
    the black bar, the centre split and both label boxes itself - the scene_prompt must describe the LEFT panel scene and
    the RIGHT panel scene separately ("LEFT PANEL: … / RIGHT PANEL: …") and must NEVER ask for text, speech bubbles, empty
    label boxes, charts, arrows with numbers or a title bar. Every number/claim comes from the script; social statistics
    only as written in the script with the same meaning. Do not spoil the final answer of the なぜ.
scoring: {}
fable_review:
  score_keys: [japanese, story, hook_visible, motif, impact, curiosity]
  criteria: |-
    1. japanese — Tiếng Nhật tự nhiên, đọc trong 1 giây; dòng thanh đen 9–15 ký tự có {vàng} = nhóm chủ ngữ và [đỏ] = từ khoá sốc; nhãn 4–8 ký tự; chữ số Ả Rập (6倍 không 六倍).
    2. story — Đúng kịch bản; KHÔNG bịa số/khảo sát; số liệu xã hội đúng nghĩa như kịch bản (ai khảo sát, đối tượng); 2 nhãn không lặp nhau và không lặp dòng thanh; không trả lời hết câu なぜ.
    3. hook_visible — 2 panel tương phản đọc được ở 360px (nguyên nhân ↔ hậu quả / niềm tin ↔ thực tế); mặt to, cảm xúc rõ.
    4. motif — Đúng khuôn 11/11 kênh mẫu: thanh ĐEN 16% H + dòng 3 màu kết 理由 · 2 panel chia giữa · 1 nhãn vàng viền đen ở ĐÁY mỗi panel (anh chốt 25/09, không che mặt). Không chép nguyên tiêu đề lên thanh.
    5. impact — Chữ to hết cỡ; ảnh không có chữ rác/tay lỗi/bong bóng rỗng; MẶT nhân vật KHÔNG được bị chữ/nhãn che (lỗi đã bị anh bắt 25/09).
    6. curiosity — Sức hút với người Nhật 25–55 tuổi đi làm tò mò hiện tượng xã hội/thế hệ/nơi làm việc; cấm 衝撃の真実, まさかの結末, その理由とは？, 驚愕, ヤバすぎる.
```

## Thumbnail kênh mẫu
Băng đen 3 màu trên cùng (vàng=chủ ngữ, đỏ=từ khoá sốc, trắng=phần còn lại) + 2 khung minh hoạ AI phong cách anime + 2 ô chữ vàng viền đen. ⚠ CHỮ THUMBNAIL VIẾT LẠI ngắn gọn hơn, KHÔNG chép nguyên tiêu đề.

<!-- export 16767427b92f · 2026-09-26 -->
