# 07 WORKFLOW — L-shakai-no-naze · shakai_no_naze

> Lane `shakai_no_naze`. File do tool YT-TITLE-RESEARCH TỰ XUẤT từ repo (E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH). Luật ở đây CHỈ áp cho kênh này, không dùng cho kênh khác.

## Cách tool hỏi anh (ChatGPT) trong Project này
- S3: chấm 3 tiêu đề ứng viên (do Fable viết) trên TOÀN BỘ kịch bản → chọn 1, được sửa ≤10%.
- S6: thanh tra tiêu đề + mô tả đã xuất → trả lỗi có mã (FACTUAL/MISLEADING/SPOILER…).
- S7: viết / thanh tra / góp ý chữ thumbnail. S8: chấm gói đăng (tiêu đề + thumbnail).
- Mỗi câu hỏi là 1 chat MỚI trong Project; dữ kiện của tập nằm TRONG tin nhắn (ưu tiên hơn file này).

# LANE L `shakai_no_naze` (tab `L-shakai-no-naze`) — mở 2026-09-24

**Thumbnail: PILOT — chưa khoá** — khuôn `config/lanes/shakai_no_naze.thumb.yaml` (layout `bar_panels`, viết tay từ số đo pixel 11/11).
**Tiêu đề: ĐÃ CÓ LUẬT** — `title_rules` trong `config/lanes/shakai_no_naze.json`. SOP: `docs/lanes/shakai_no_naze/SOP_TIEU_DE_THUMBNAIL_2026-09-24.md`.

| | |
|---|---|
| Kênh mình | 社会のなぜ研究室 `@shakai-no-naze` `UCjy5fWoigvtCfduJDJ3jTbg` |
| Kênh mẫu | 社会のウラガワ https://www.youtube.com/channel/UCFWFKb3Yr_1SrAT0kcvwFdw |
| Thư mục tập | `E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep<nn>-<slug>` |
| Giao hàng | `E:\CLAUDE\YOUTUBE\CHANEL\shakai_no_naze\ep<nn>-<slug>` |
| Sheet | `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU` tab `L-shakai-no-naze`, khớp dòng theo cột C (đường dẫn) |
| title_intel | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\shakai-no-naze.json` (tên gạch ngang — alias trong `src/title_intel.py`) |

## Nhật ký
- 2026-09-24: mở lane — config json + thumb.yaml + layout `bar_panels` + test `tests/thumb/test_lane_shakai.py` + SOP + chatgpt 05/06. Pilot ep01-shusse-shitakunai.

---
## SOP_TIEU_DE_THUMBNAIL_2026-09-24.md

# SOP TIÊU ĐỀ + THUMBNAIL — LANE L `shakai_no_naze` (社会のなぜ研究室, tab `L-shakai-no-naze`) — 2026-09-24

Kênh mẫu: 社会のウラガワ `UCFWFKb3Yr_1SrAT0kcvwFdw` (11 video, 66 ngày tuổi). Hồ sơ phía h2dev:
`E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\shakai_no_naze.md` · `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_L.md`.
Dữ liệu kênh mẫu: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\shakai-no-naze.json` (id lane YT-TITLE là
`shakai_no_naze` — `src\title_intel.py` tự tìm bản gạch ngang) · thumbnail gốc `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\shakai_no_uragawa\thumbs\`.

## 1. Tiêu đề — số đo 11/11 video
| view/ngày | thân (không 【漫画】) | khuôn |
|---|---|---|
| 9.393 | パワハラを盾に指導を拒否するZ世代の末路とは | F3 末路 |
| 8.134 | 『Z世代はもう雇わない』なぜ企業のZ世代の採用が激減してるのか | F1 thoại + なぜ |
| 4.251 | なぜ賢い人ほど群れないことを選ぶのか？ | F2 ほど |
| 2.860 | 独身は勝ち組⁉結婚しない男性が増えた納得の理由 | F4 phán quyết + 理由 |
| 2.001 | 【衝撃】日本のスマホ事情が激変！iPhoneからAndoridに乗り換える人が爆増した理由 | F4 爆増した理由 (dài 45) |
| 21–1.692 | 6 video còn lại (休日/氷河期/いい旦那/発達障害/正しい人/必要な仕事) | chủ ngữ trừu tượng / kêu oan / chẩn đoán |

Luật (đầy đủ ở `title_rules` của `config\lanes\shakai_no_naze.json`): 【漫画】 CUỐI (tool tự nối) · thân 16–34 (mục tiêu 24) ·
nhóm người trong 12 ký tự đầu · có lập trường gây tranh cãi · cấm khung kêu oan/bất công/chẩn đoán · số chỉ khi có nguyên văn
trong kịch bản · dùng lại chữ của hook đã khoá.

## 2. Thumbnail — 1 khuôn cố định (đo pixel 11/11)
- Thanh đen 0–16,1% H; 1 dòng 3 màu: `{vàng}` nhóm người #FACA28 · `[đỏ]` từ khoá sốc #FA3232 · trắng. 10/11 kết 理由, là câu VIẾT LẠI.
- 2 panel chia đôi (vạch đen x 638–643/1280). Mỗi panel 1 nhãn nền #FCC200 viền đen, y 19,7–32,9% H, căn giữa panel, 4–8 chữ.
  **⚠ 2026-09-25 anh chốt: nhãn của MÌNH đặt ở ĐÁY panel (`label_top_ratio: 0.838`)** — để ở đầu như kênh mẫu thì che mặt 3/3 tập ep01–03.
  Chữ không bao giờ được che mặt nhân vật. Nền giữ mặt ở dải giữa panel (`keep_top_ratio: 0.22` + prompt chừa 18% đáy).
- Sakura (tóc đen dài buộc đuôi ngựa thấp) có mặt 6/11 — dùng khi kịch bản có cô.
- Engine: layout MỚI `bar_panels` (`thumbnail_engine\bar_panels.py`), vai `top` / `lead` (panel trái) / `lead2` (panel phải).
  Ảnh lưới: `docs\lanes\shakai_no_naze\thumb\research\kenh_mau_top6.jpg`, demo khuôn `khuon_bar_panels_demo.png`.
- Bộ đo `tools\thumb_dna_measure` KHÔNG đo được khuôn này (nó tìm dòng chốt đáy, kênh này không có; kênh chỉ 7 video "thắng" < 10)
  → yaml viết tay, `dna_measured: false` ⇒ `lane-lock` sẽ từ chối (cố ý, giống lane E).

## 3. Mô tả
Khuôn 10/11 kênh mẫu: hiện tượng + 1–3 số liệu thật (ai khảo sát, năm) → câu hỏi なぜ → 「その裏側には、〜があったのでした。」 →
2 câu giới thiệu kênh (của mình, không chép) → 1 dòng 5–8 hashtag đề tài. Hook_line đặt LÊN ĐẦU (cổng G1 h2dev đo câu đầu mô tả),
câu chào kênh xuống cuối — khác kênh mẫu để 2 dòng xem trước trên YouTube là lời hứa chứ không phải lời chào.

## 4. Chuỗi lệnh 1 tập
```
cd E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH
py -3.13 -X utf8 cli.py run --slug E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep<NN>-<slug> --profile shakai_no_naze
::  → S0–S6 tiêu đề/mô tả + tags (song song) + thumb 3 ảnh + sol-check; mở research\XEM.html xem 3 ảnh
py -3.13 -X utf8 cli.py thumb-publish --slug E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep<NN>-<slug> --profile shakai_no_naze [--choose B]
py -3.13 -X utf8 cli.py sheet-publish --slug E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep<NN>-<slug> --profile shakai_no_naze
```
Tập có `hook\hook_lock.json` → tiêu đề mục tiêu = field `promise.title` (h2dev đã duyệt khớp hook); tool vẫn chạy S2/S3 để đối chiếu.
Giao hàng: `E:\CLAUDE\YOUTUBE\CHANEL\shakai_no_naze\ep<NN>-<slug>\` (TIEU_DE_MO_TA.txt + thumbnail.png).
Bật tự động bên h2dev sau khi tập 1 đạt: `py -3.13 E:\CLAUDE\YOUTUBE\h2dev\pipeline\goi_title.py --bat shakai_no_naze`.

<!-- export b6401c9722f0 · 2026-09-26 -->
