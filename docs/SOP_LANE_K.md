# SOP LANE K — `yakkyoku-sukatto` · 薬局スカッと帳 (sổ tay nhà thuốc hả dạ)

> ⭐ **2026-09-26 — BÌNH LUẬN THẬT + CUNG CẢM XÚC** (anh chốt): trước khi viết tập mới đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\yakkyoku-sukatto\COMMENT_INSIGHT.md` (khối `## ĐƯA VÀO PROMPT` tự vào prompt S2). Tóm tắt: video 307.286 view là video gây giận nhất; khán giả bắt lỗi định mức dược sĩ/みなし残業 (tiền làm thêm khoán); người bị hại không được vô lý. Prompt S2 nay có cung 3 nhịp KÍCH → GIẢI TOẢ → VỊ THA (`script.cung_cam_xuc: true`) — lớp 3 kiểm nửa đầu có làm bực thật không + có câu đạo lý đáng nhớ ở kết không. Luật "không trả thù/không hả hê" của lane GIỮ NGUYÊN (nằm ở nhịp 2). Chi tiết `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2a/§2c.

Runbook sản xuất 1 tập. Cửa vào (định danh, trạng thái): `docs/BAT_DAU_LANE/yakkyoku-sukatto.md`.
Phương án kỹ thuật: `docs/PHUONG_AN_LANE_K_DA_GIONG_BONG_THOAI.md`. Luồng kịch bản chung: `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md`.

## §0 KHÁC CÁC LANE KHÁC Ở ĐÂU (bảng delta)
| Mục | Lane K | Lane F/G (khuôn gần nhất) |
|---|---|---|
| Người kể | NGÔI 3「彼」+ câu nội tâm「俺…」không ngoặc | ngôi 1「俺」 |
| Giọng | **ĐA GIỌNG VOICEVOX** (0đ), mỗi vai 1 giọng — `tts_voicevox.py` + `vai.txt` | 1 giọng ai33 |
| Khoá mặt | **N nhân vật/tập** (`characters.json` kiểu mới `{id, ref, voice}`, master `_ref_<id>/001.png`, prompt `@CAST:a,b`) — tối đa 3 mặt/ảnh (Flow Tool) | @REF/@REF2 |
| Chữ trên hình | MỌI câu: lời kể = hộp chữ nhật trắng chữ dọc · thoại + nội tâm = bóng tròn có ĐUÔI chỉ miệng người nói (`bong_thoai.py`, máy vẽ) | hộp chữ dọc cố định 1 bên (`tate_text.py`) |
| Nhịp ảnh | 8 s/ảnh (đo thật video gốc) | 10 s |
| Luật viết | mỗi câu thoại là 1 câu「…」riêng, không dính lời dẫn (máy S3 bắt `dialogue_own_sentence`) · trước mỗi lượt thoại phải rõ ai nói | — |

## §0b CHANNEL ANALYZER (bắt buộc)
- DNA: `docs/channel_dna/yakkyoku-sukatto/` — `CHANNEL_DNA.md` (11 đề mục), `VIDEO_ANALYSIS/*.json` (4 video dài),
  `TAG_STATS.json`, `_raw/transcripts.json` (whisper — **sai chữ nhiều, chỉ dùng đo độ dài**).
- Transcript sạch hơn (phụ đề tự động) + 7 thumbnail + `channel.json`: `FlowHandoff_local/results/laneK_from_research/data/`.
- Báo cáo đọc hiểu: `FlowHandoff_local/results/laneK_from_research/KENH_MAU_REPORT.html`.
- Giọng ↔ vai (đo máy): `docs/channel_dna/yakkyoku-sukatto/GIONG_VAI.md`.
- K3 mỗi tập: `py -3.13 pipeline\retrieve_videos.py --dna-dir docs\channel_dna\yakkyoku-sukatto --topic "<chủ đề>"`.

## §0c GIỌNG (chốt 2026-09-24)
- Engine: `E:\CLAUDE\YOUTUBE\VOICEVOX_ENGINE\0.25.2\run.exe --host 127.0.0.1 --port 50021` (máy 2 cài theo
  `FlowHandoff_local\shared\GIAO_VIEC_MAY2_CAI_VOICEVOX.md`).
- Cố định: người kể **玄野武宏** · nhân vật chính **黒沢冴白** · 事務さん **波音リツ**. Vai phụ chọn trong `voice.cast_bank`
  của profile (đúng giọng kênh gốc dùng cho vai đó). 店長 = **雀松朱司** (không clone 阿井田茂).
- speed 1.0 · nghỉ 500 ms giữa câu · 900 ms giữa đoạn → 312,5 chữ/phút (B4 tự nắn theo tập thật).
- Mô tả video BẮT BUỘC có khối ▼素材 = `credits_giong.txt` của tập (điều khoản 14 giọng: ghi 「VOICEVOX:tên」).

## §1b CỘT SHEET TAB `K-yakkyoku-sukatto` (A→K)
A STT · B NỘI DUNG (tiêu đề JP + dịch) · C FOLDER (ghi ngay khi tạo tập) · D KỊCH BẢN (tool tự ghi theo docsTRANG_THAI_COT_D_K.md; xong máy 1 = `Đã giao máy 2`) ·
E TITLE-DESCRIPTION · F TAGS · G THUMBNAIL · H STATUS-IMG (`cần ảnh (N ảnh, ~Xđ)` = lệnh cho máy 2) · I VIDEO · J LIST · K GHI CHÚ.
10 tập đầu đã ghi A2:B11 (2026-09-24).

## §2 MỘT TẬP — MÁY 1 (đúng thứ tự)
```
cd E:\CLAUDE\YOUTUBE\h2dev
:: S1 hồ sơ (tay, ~15'): assets\yakkyoku-sukatto\epNN-<slug>\ gồm competitor.txt + competitor.segments.json
::   (transcript gốc cùng dạng — lấy từ laneK_from_research\data\transcripts), series_ctx.txt ([Dn] có URL +
::   SỐ ĐƯỢC PHÉP + QUY ƯỚC ghi BẮT BUỘC 3 lần câu cửa miệng + hậu quả từ cơ chế), title.txt, promise.txt, hook\promise.txt
py -3.13 -X utf8 pipeline\make_video.py --profile yakkyoku-sukatto --slug epNN-<slug> --den B3G
```
> ⛔ **2026-09-27 — SOÁT BẰNG CHATGPT WEB (mặc định, thay máy 3):** lệnh trên tự DỪNG sau khi khoá và in 3 lệnh `soat_kb_gptweb.py --lan1` → thẩm định/phản biện (cổng giữ mở) → `--chot` → viec_tay → `--xong` (docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md §4b). Đoạn máy 3 dưới đây TẠM ẨN.
> (cũ, tạm ẩn) ⛔ **2026-09-26 — lệnh trên giờ TỰ DỪNG sau khi khoá kịch bản** và gửi máy 3 soát (`FlowHandoff_local\jobs\K-yakkyoku-sukatto\<slug>\review\`,
> cột D = `Chờ kiểm tra kịch bản`). Chờ anh báo D = `Đã sửa kịch bản` → `py -3.13 -X utf8 pipeline\review_may3.py --nhan --profile yakkyoku-sukatto --slug <slug>`
> rồi mới đi tiếp B5W/hook/`dong_goi_may2`. Chi tiết: `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §4c.
```
::   → hook khoá (H1–H4) → Fable viết → S3 máy → Sol ×2 → LOCK. Lớp 3: đọc hết script.txt (luật §5).
:: characters.json (tay, sau khi đọc kịch bản): MỌI vai có thoại hoặc ≥2 cảnh = {id,name,vai,age,gender,look,ref:true,
::   voice:{speaker,style}}; nhân vật chính id "shu" + "kuchiguse"; look khác nhau rõ (áo/tóc/kính) để máy nhận mặt.
py -3.13 -X utf8 pipeline\gan_vai.py --profile yakkyoku-sukatto --slug assets\yakkyoku-sukatto\epNN-<slug>
py -3.13 -X utf8 pipeline\make_video.py --profile yakkyoku-sukatto --slug epNN-<slug> --only B5W
py -3.13 -X utf8 pipeline\make_video.py --profile yakkyoku-sukatto --slug epNN-<slug> --only B5P
:: HOOK (máy 1 làm trọn hình, docs\QUY_TAC_VIDEO_HOOK.md): giọng hook đa vai (tts.py tự chuyển VOICEVOX, cần vai.txt)
::   → ảnh hook @CAST (anh_hook.py <tập>\hook — Google Flow Ultra → 9router → gpti2) → clip Grok → qc_hook_clip → SFX → hook_timeline.json → HOOK_TAP.md
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job yakkyoku-sukatto epNN-<slug>
::   (tự vẽ master _ref_<id> nếu thiếu, gói vai.txt + _ref_* + hook\, ghi sheet D=Đã giao máy 2 + K=lệnh máy 2, H=cần ảnh)
```
Bundle máy 2 phải có profile lane này (chỉ thêm/ghi đè profile được liệt kê, profile lane khác giữ nguyên):
`py -3.13 pipeline\dong_goi_may2.py --bundle --profile-list yakkyoku-sukatto`.

## §2a TẬP 1 — MÁY 1 LÀM TRỌN (ngoại lệ anh cho 2026-09-24)
Lệnh đã chạy thật: `make_video.py --den B4Q` → `--den B5Q` (gpti2 136 ảnh 12.380đ) → `--den B8Q` (bóng thoại, sync 4,6) → `ghep_hook_noi_truoc.py --tap <đường dẫn TUYỆT ĐỐI> --profile yakkyoku-sukatto` (tự thay hình) → `qc_final.py` (0 nặng) → `ban_xem_viet.py` → chép vào `results\video_render\yakkyoku-sukatto\<slug>\`. Từ tập 2 trở lại luật chung (máy 2 + Flow Tool).

## §2b MÁY 2 (làm theo `_BANGIAO.txt`)
`make_video.py --profile yakkyoku-sukatto --slug <tập> --redo-voice` → B4 đọc `vai.txt` bằng VOICEVOX → ảnh bằng Flow Tool
(mỗi id 1 Character trong CÙNG 1 project, mention đúng `@id` ở đầu dòng `@CAST`) → B8: `bong_thoai.do_mat` định vị mặt
(vision) → assemble `--bubble-roles/--bubble-faces` → final.mp4 → ghép hook → trả `results\video_render\yakkyoku-sukatto\<slug>\`.

## §3 GATE (profile, đo từ 4 video gốc)
title 31–46 ký tự (kể cả【漫画】) · 17,5' ≈ 5.469 chữ · 7 chặng `budget.sections` · thoại ≤45% · 0,6–2 phẩy/câu ·
7–14 chữ/nhịp · `dialogue_own_sentence` · hook: luật 21/10 bám sát cấu trúc hook video gốc (`E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`; patterns/closer cũ đã xoá) · gói đăng: câu cửa
miệng ≤10s, lời hứa ≤30s.

## §5 LUẬT CỨNG (lớp 3 đọc bản khoá theo đúng danh sách này)
1. Hậu quả đến từ CƠ CHẾ (nhân sự, hợp đồng, điều động) — không ai mắng, không trả thù, không cảnh hả hê.
2. Câu cửa miệng 3 lần; lần cuối trong chuyện quan trọng; câu CUỐI lặp đúng câu cửa miệng ('không còn ai nói nữa').
3. Người kể không phán xét; khán giả thấy cái giá qua chi tiết (người khác gánh thay).
4. Nghiệp vụ dược đúng [Dn]; không tên thuốc/thương hiệu; không lời khuyên dùng thuốc.
5. Không dùng lại 4 câu cửa miệng + tình tiết đặc trưng của kênh gốc.
6. Mỗi lượt thoại mới phải rõ ai nói (câu người kể trước/sau) — `gan_vai.py` và bóng thoại dựa vào đó.

## §5b PHÂN VAI MODEL
Fable viết (S2) · Opus vá (S4) + gắn vai (`gan_vai.py`) · Sol chấm (lens plain + `script_qc.lane_rules`) · Fable viết prompt
ảnh (B5W CAST) · máy: S3, VOICEVOX, bóng thoại.

## §9 BẪY ĐÃ GẶP
| Triệu chứng | Nguyên nhân | Xử |
|---|---|---|
| Câu cửa miệng ở giây 0 bị gán cho người khác | Opus không biết đó là câu của nhân vật chính | `characters.json` khai `kuchiguse` + `title.txt` có sẵn (gan_vai đọc cả hai) |
| Câu thoại bị gán nhầm người | kịch bản không nói ai lên tiếng | luật §5.6, đã nhồi vào `structure_block` |
| Transcript `_raw` sai chữ (学知癖の役剤士) | whisper | trích nguyên văn thì lấy `laneK_from_research\data\transcripts` |
| Máy S3 xoá mất câu cửa miệng (lặp nguyên văn ≥12 chữ) → Sol FIX mãi vì câu cụt | `_go_cau_trung` dedup | `gate.repeat_title_quote` (cụm「」đầu tiên của title.txt được phép lặp) |
| Cảnh ga tàu/sân bóng/phòng họp bị vẽ thành quầy thuốc | style_suffix chứa bối cảnh | style_suffix CHỈ nét vẽ; bối cảnh tả trong từng prompt |
| Sol bắt lỗi logic nhân sự 3 vòng (người né việc lại được làm 管理薬剤師) | hồ sơ S1 tự mâu thuẫn | S1 phải tự hợp lý: hậu quả = điều động bình thường, nhân vật TỰ nhận |
| Patch Opus bị từ chối vì vượt trần 1,05× | bản đã sát trần ngân sách | viec_tay ghi rõ "bù bằng rút chỗ khác"; khi vẫn bị từ chối → sửa tay đúng chỗ (ESCALATE, chưa khoá) rồi cho Sol chấm |
| Nối hook lên trước → nghe hook 2 lần | lean flow chép hook vào đầu script.txt | `ghep_hook_noi_truoc.py` tự nhận "script mở bằng hook" → CHẾ ĐỘ THAY HÌNH (phủ clip lên 0–T, giữ tiếng thân, tổng độ dài không đổi) |
| Hook dính G1/G3 ở B10 (lời hứa 52% trong 30s, câu mâu thuẫn ở giây 23) | hook kể bối cảnh trước khi nêu hậu quả | (luật viết hook cũ — đã thay bằng luật 21/10 bám sát cấu trúc hook video gốc) |
| Hộp lời kể nằm giữa khung che mặt (anh bắt ep01) | vision trả toạ độ mặt trên ảnh trần lệch tới ~20% ngang (005.png) + luật cũ nhắm 72% ngang | `bong_thoai._hoi_anh` kẻ lưới 10% lên ảnh trước khi hỏi (3/3 khớp); `_dat_mep`: SÁT mép phải, mép phải có người → mép trái, không bao giờ đè mặt |
| Chữ nhỏ khó đọc (40px) | — | anh chốt (so 3 mức, `_mau_chu/`): lời kể 64px cột ≤8 chữ, dài >24 chữ TÁCH nhiều hộp nối tiếp chia thời gian theo số chữ (`tach_loi_ke`); thoại 48px — field `assemble.bubble.font_size_ke/_thoai, max_chars_per_col_ke, ke_split_chars` |
| Hộp lời kể đè người ở ảnh "cảnh vật" (ep01 giây 300, cô y tá) | `do_mat` chỉ đo ảnh @CAST | nay đo MỌI ảnh img/NNN.png (người lạ = id `khac`); ep01: 136 ảnh, 107 ảnh có người |
| "Chưa có hiệu ứng chuyển cảnh, chưa có âm thanh" (anh xem ep01) | đo máy 2 video gốc: mờ chồng 9 khung + MỌI cảnh phóng vào ×1,02–1,03; nền có 1 bài nhạc acoustic lặp suốt video thấp hơn giọng ~17,7 dB, KHÔNG SFX (Gemini nghe 3 đoạn) | anh cho NGOẠI LỆ luật cấm zoom: `assemble.zoom 1.025 · zoom_dir in · xfade 0.3`; `assemble.py::_warp_clip` (warpAffine dưới-pixel, lệch chuẩn 0,016 px/khung vs zoompan 0,39 = rung). Nhạc `assets\yakkyoku-sukatto\_bgm\bgm_lane_k.mp3` (Suno/ai33 7.200 credit cho 2 bài, chọn bài 1) · `bgm_volume 0.075 · bgm_keep_voice` (amix mặc định chia đôi giọng −6 dB). `dong_goi_may2 --bundle` tự chép file nhạc cho máy 2 |
| Dự án tiêu đề dừng vì thiếu thư mục giao `E:\CLAUDE\YOUTUBE\CHANEL\yakkyoku-sukatto\<slug>\` | bên đó không tự tạo | `dong_goi_may2.py --job` tạo sẵn thư mục RỖNG khi `publish.listing_external` (không chép video vào) |
