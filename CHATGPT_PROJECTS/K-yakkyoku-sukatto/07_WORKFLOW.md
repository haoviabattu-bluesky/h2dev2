# 07 WORKFLOW — K-yakkyoku-sukatto

> Lane `yakkyoku-sukatto`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Cách tool hỏi anh (ChatGPT) trong Project này
- S3: chấm 3 tiêu đề ứng viên (do Fable viết) trên TOÀN BỘ kịch bản → chọn 1, được sửa ≤10%.
- S6: thanh tra tiêu đề + mô tả đã xuất → trả lỗi có mã (FACTUAL/MISLEADING/SPOILER…).
- S7: viết / thanh tra / góp ý chữ thumbnail. S8: chấm gói đăng (tiêu đề + thumbnail).
- Mỗi câu hỏi là 1 chat MỚI trong Project; dữ kiện của tập nằm TRONG tin nhắn (ưu tiên hơn file này).



---
## SOP_TIEU_DE_THUMBNAIL_2026-09-24.md

# SOP TIÊU ĐỀ · MÔ TẢ · TAGS · THUMBNAIL — LANE K `yakkyoku-sukatto` (薬局スカッと帳 @yakkyoku-sukatto)

Mở lane 2026-09-24. Kênh mẫu: 千種テンカ `UCEBA1RFfkXQtqgiDVLh4bcw` (706 sub, chỉ 7 video/4 video dài — **kênh rất mới,
mẫu đo nhỏ hơn hẳn các lane khác**, đọc kỹ `title_intel` thay vì tin tuyệt đối như lane có 15–27 video). Sheet tab
`K-yakkyoku-sukatto`, dò dòng bằng cột C (đường dẫn thẳng vào thư mục tập h2dev). Hồ sơ gốc: `docs\BAT_DAU_LANE\yakkyoku-sukatto.md`
bên h2dev + `title_intel\yakkyoku-sukatto.json` bên TRENDING-RESEARCH.

## TRẠNG THÁI 2026-09-25 — HẠ TẦNG ĐỦ, CHẠY ĐƯỢC
1. h2dev xong Giai đoạn 2 + tập 1 `ep01-tantou-janai` đã có video hoàn chỉnh (char-rate đo thật 316,7 · SOP
   `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_K.md` · 10 tập ở tab A2:B11 · C2 = đường dẫn tập · script.txt + HOOK_TAP.md PASS).
   Thư mục giao `E:\CLAUDE\YOUTUBE\CHANEL\yakkyoku-sukatto\ep01-tantou-janai\` đã có (tập sau `dong_goi_may2.py --job` tự tạo).
2. `config\lanes\yakkyoku-sukatto.json` (luật tiêu đề) — xong 2026-09-24.
3. `config\lanes\yakkyoku-sukatto.thumb.yaml` — **DỰNG 2026-09-25**, layout MỚI `dialogue_split` (PILOT), xem mục Thumbnail.
4. `publish.title_auto` bên h2dev vẫn TẮT (kênh mới): anh chạy tay tập đầu, ưng rồi `goi_title.py --bat yakkyoku-sukatto`.

## Tiêu đề (luật đầy đủ trong `config\lanes\yakkyoku-sukatto.json` → `title_rules`)
Chỉ **1 khuôn duy nhất** (không có F1/F2/F3 như lane E/F, vì cả 4 video dài kênh mẫu đều theo đúng 1 khuôn):

```
【漫画】「[câu cửa miệng NGUYÊN VĂN của nhân vật chính, trong「」]」が口ぐせの/だった薬剤師が、
[hành động sai lầm cụ thể HOẶC mốc đếm lần N / mốc thời gian]結果… (hoặc 行き着く先…)
```

| Ví dụ thật (view) | Ghi chú |
|---|---|
| 「じゃあ、辞めます」が口ぐせの薬剤師が、3回目に同じことを言った結果… (307k/5 ngày) | mốc đếm lần 3 |
| 「自分、仕事できるんで」が口ぐせの薬剤師が行き着く先… (57.8k) | không mốc đếm, dùng 行き着く先 |
| 「残業代入んないんで」が口ぐせの薬剤師が、閉店2分前に患者を追い返した結果… (34.5k) | mốc thời gian nghiệp vụ |
| 「代わりはいくらでもいる」が口ぐせだった薬剤師が、定年後に6社目の面接を受けた結果… (20.3k) | mốc đếm 6社目 |

31–46 ký tự tính cả 【漫画】 (mục tiêu 40). Câu cửa miệng trong 「」+ 薬剤師 phải trọn trong 24 ký tự đầu. Câu cửa miệng
PHẢI đúng câu nhân vật chính lặp lại xuyên suốt kịch bản (S3c đối chiếu `script.txt`, không được bịa câu khác rồi gọi
là câu cửa miệng). Tiêu đề LUÔN dừng ở `結果…`/`行き着く先…` — không lộ ai thắng ai thua.

**Cấm cứng: 復讐, 仕返し, ざまあ, 天罰** — kênh mẫu là 因果応報 (quả báo tới từ HỆ THỐNG: log giờ, hợp đồng, quy định),
KHÔNG phải nhân vật khác "ra tay trả đũa". Đây là đặc trưng cốt lõi của lane, sai luật này là hỏng cả chủ đề kênh chứ
không chỉ hỏng 1 tiêu đề — xem thêm mục "Bẫy".

## Mô tả
Khuôn đo từ `description_rule` + `principles` (title_intel): trích câu cửa miệng 1 dòng → câu mở cố định "đây là câu
cửa miệng của một dược sĩ" → 2-4 câu hành vi cụ thể (không phán xét) → câu nhử không lộ kết quả → khối
`⚠️【免責事項】` (đã có sẵn nguyên văn trong `desc_fixed_defaults` của config lane, tool tự nối, lấy đúng disclaimer đã
dùng cho mô tả KÊNH) → もくじ mốc phút:giây (khớp 7 chặng trong `budget` của profile h2dev) → credit giọng VOICEVOX
(lấy từ `credits_giong.txt` của tập, KHÔNG tự bịa tên giọng) → 4 hashtag cố định `#薬剤師 #薬局 #漫画 #スカッと`.
**KHÔNG viết CTA đăng ký/like** — kênh mẫu không dùng (principles: "Không có CTA sub/like"). **KHÔNG có cảnh trả thù**
trong mô tả — hậu quả phải đến từ hệ thống/số liệu, không phải nhân vật "ra tay".

## Tags
Bước T v3 (docs/tags.md) — tag lấy từ video đối thủ thật. Kênh mẫu quá mới (7 video) nên hạ `min_channels_eff` 10→8,
nâng `max_per_channel` 2→3 như lane E. `fixed_tags` lấy 5 tag đầu của `tags_seed` trong profile h2dev
(薬剤師/薬局/漫画/スカッと/因果応報).

## Thumbnail — layout `dialogue_split` (dựng 2026-09-25, PILOT)
Đo PIXEL 4/4 thumbnail video dài (`E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneK_from_research\data\thumbs\*.jpg`,
1280×720 — số đo trùng từng pixel cả 4 ảnh, kênh dùng 1 khuôn cố định). `thumbnail_rule` tự động trong title_intel SAI, đừng dùng.

| Thành phần | Số đo | Vai (row) |
|---|---|---|
| Dải VÀNG dọc giữa | x 550–731 (43,0–57,2% W) màu #FDE006, viền đen ~5 px 2 bên; chữ DỌC đen + 1–2 cụm ĐỎ #D02414 | `band` — `[đỏ]`, `/` = sang cột |
| Panel TRÁI (0–43%) | người đưa hậu quả, bóng thoại chữ dọc XANH #1B3EB0 ở phía ngoài | `quote_left` |
| Panel PHẢI (57–100%) | nhân vật chính áo blouse trắng, bóng thoại chữ dọc ĐỎ #CC2325 = câu cửa miệng nguyên văn | `quote_right` |

- Renderer: `thumbnail_engine\dialogue_split.py` (chữ dọc dùng lại `bong_thoai.chia_cot/_ve_chu_doc` của h2dev — cùng bộ vẽ
  bóng thoại trong video). Test: `tests\thumb\test_lane_yakkyoku.py`.
- **Nền = gpti2 edit với 2 REF của TẬP** (`background.cast_refs: true`): phải = nhân vật chính (`_ref_shu`), trái = vai ghi trong
  `LEFT PANEL (<vai>)` đầu scene_prompt (khớp name/vai tiếng Nhật trong characters.json), không khớp thì vai nhiều thoại nhất
  trong vai.txt → mặt thumbnail khớp nhân vật trong video. Tập không có REF → gpti2_text.
- Pilot ep01 (chữ tay, 1 nền gpti2): `E:\CLAUDE\YOUTUBE\h2devssets\yakkyoku-sukatto\ep01-tantou-janai\_thumb_pilot\outest.png`.
- Giới hạn biết trước: vị trí bóng thoại CỐ ĐỊNH ở mép ngoài panel (prompt ép người đứng phía trong) — gpti2 đặt mặt lệch ra
  ngoài thì bóng có thể lấn tóc/má; Opus/ChatGPT chấm ảnh phải bắt lỗi này (fable_review mục hook_visible).

## Bẫy
- Kênh quá mới (706 sub, 4 video dài) — mọi số view/ngày trong bảng trên là **view/ngày kể từ lúc đăng, không phải
  view ổn định lâu dài** như lane có video cũ hàng năm; đọc `our_eps` khi có (hiện `title_intel` chưa có `our_eps` vì
  chưa có tập nào của mình).
- Đừng nhầm thư mục DNA: h2dev dùng `docs\channel_dna\yakkyoku-sukatto\` (đúng `dna_slug` trong config lane), còn
  TRENDING-RESEARCH tự đặt tên nội bộ khác (`docs\channel_dna\iyaku_labo\`, `key: "iyaku"` trong title_intel) — 2 thư
  mục cùng dữ liệu gốc nhưng KHÁC tên, đừng trỏ nhầm `dna_slug` sang `iyaku_labo` vì h2dev không có thư mục đó.
- `_raw\transcripts.json` (whisper) của h2dev SAI CHỮ nhiều chỗ (đã ghi trong `BAT_DAU_LANE`) — đo độ dài/nhịp thì
  dùng được, trích nguyên văn câu cửa miệng phải lấy transcript sạch hơn hoặc đối chiếu video.
- Giọng ngôi kể: NGÔI 3 (「彼」/「その男」) + nội tâm ngôi 1 không ngoặc — khác hẳn giọng ngôi 1 xuyên suốt của
  satori/F, đừng áp `pov_note` lane khác.

<!-- export 9b37b7ff3589 · 2026-09-26 -->
