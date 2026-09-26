# SOP LANE L — `shakai_no_naze` · 社会のなぜ研究室 (Phòng nghiên cứu Vì sao của xã hội)

Runbook sản xuất 1 tập. Cửa vào (định danh, trạng thái, quyết định của anh): `docs/BAT_DAU_LANE/shakai_no_naze.md`.
Số đo kênh mẫu: `docs/channel_dna/shakai-no-naze/DO_THUC_TE_2026-09-24.md`. Luồng kịch bản chung:
`docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md`. Khuôn kỹ thuật chép từ `docs/SOP_LANE_K.md`.

## §0 KHÁC CÁC LANE KHÁC Ở ĐÂU (bảng delta)
| Mục | Lane L | Lane K (khuôn gần nhất) |
|---|---|---|
| Nội dung | ESSAY なぜ〜のか: 1 câu chuyện hư cấu liền mạch + 2–3 số liệu xã hội THẬT có nguồn | truyện quả báo nơi làm việc, không số liệu |
| Người kể | ngôi 3, giọng NỮ | ngôi 3, giọng nam |
| Giọng | **ĐA GIỌNG ai33/MiniMax** (`voice.provider = "ai33"`, `tts_voicevox.py` nhánh ai33) — kênh gốc KHÔNG phải VOICEVOX | đa giọng VOICEVOX |
| Khoá mặt | N nhân vật/tập như K **+ Sakura khoá XUYÊN TẬP** bằng 1 ảnh gốc lane (`image.fixed_refs`) | N nhân vật/tập, không xuyên tập |
| Bóng thoại | oval **KHÔNG đuôi** (`assemble.bubble.tail=false`) | có đuôi |
| Chuyển cảnh | **mờ chồng 0,3s + zoom nhẹ 2,5% luân phiên vào/ra** (warpAffine, không rung) — anh chốt 24/09 sau ep01 | xfade 0,3s + zoom vào 2,5% |
| Chữ trên hình | **mức C (anh chốt 25/09, từ tập 2): lời kể 72px · thoại 56px** (cột ≤8, >24 chữ tách hộp; >30 chữ tách bóng). Tập 1 giao ở mức B 64/48 | 64/48 |
| Giao máy 2 | ĐÚNG 2 video `final.mp4` (đã có hook) + `final-vietsub.mp4`; hook tự ghép trong B8, mốc theo SỐ CÂU | final_with_hook.mp4 |
| Tiêu đề/mô tả/thumbnail | dự án TITLE, **`title_auto` BẬT từ tập 2** (25/09) | — |
| Hiệu ứng âm thanh | **CÓ trong thân video** (`assemble.sfx`, kho 14 tiếng ai33 `assets\shakai_no_naze\_sfx\`) + hook | không SFX, có nhạc nền |
| Nhịp ảnh | 7,5 s/ảnh (~145 ảnh/tập 18') | 8 s |
| Slide số liệu | **KHÔNG** (anh chốt: AI vẽ số không chuẩn) — số nằm trong lời kể/hộp chữ | — |
| CTA | có outro đăng ký cố định (`script.outro_line`) | không |

## §0b CHANNEL ANALYZER (bắt buộc)
- DNA: `docs/channel_dna/shakai-no-naze/` — `CHANNEL_DNA.md` (8 video, TRENDING-RESEARCH chạy), `VIDEO_ANALYSIS/*.json`,
  `TAG_STATS.json` (kênh gần như không gắn tag), `_raw/transcripts.json` (whisper, tên Sakura đúng).
- **Số đo thật (xem hình/nghe giọng) — đọc TRƯỚC:** `DO_THUC_TE_2026-09-24.md`.
- Transcript phụ đề tự động 11 video + 11 thumbnail + `channel.json` (mô tả gốc):
  `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\shakai_no_uragawa\`. Phụ đề tự động cắt tên 「さくら」 thành 「さ」.
- Tờ ảnh cảnh 5 video + trang so giọng: `assets\shakai_no_naze\_research\kenh_mau\` (`sheet_*.jpg`, `mat_*.jpg`, `nghe\SO_GIONG.html`).
- K3 mỗi tập: `py -3.13 pipeline\retrieve_videos.py --dna-dir docs\channel_dna\shakai-no-naze --topic "<chủ đề>"`.

## §0c GIỌNG (anh chốt 2026-09-24: "lấy top 1 máy chọn")
- Người kể **Kind Lady** `minimax_209536448462916` · Sakura **Graceful Maiden** `minimax_209536448462924` ·
  nam chính/sếp **Gentle Butler** `minimax_209536448462915`. Vai phụ: `voice.cast_bank` của profile (họ MiniMax).
- speed 1.0 · nghỉ 400 ms giữa câu · 700 ms giữa đoạn → **311,5 chữ/phút** (đo thật, kênh mẫu 268–313).
- Mỗi câu 1 task ai33, 8 luồng (đo: 11 câu 23s ⇒ tập ~350 câu ≈ 12–15'). Credit ≈ 1,27/chữ ⇒ tập 5.600 chữ ≈ 7.100 credit.
- Có cổng credit trước khi gửi + cổng nuốt chữ từng câu (tiếng < 35% độ dài kỳ vọng → đọc lại 3 lượt rồi DỪNG).
- ai33 không có điều khoản ghi công → không có `credits_giong.txt`, mô tả không cần khối ▼素材.

## §0d SAKURA — ảnh gốc lane
- `assets\shakai_no_naze\_ref_kenh\sakura\001.png` (gpti2 medium, QC tuổi/giới: ~22/F ĐẠT). Tóc đen dài buộc đuôi ngựa
  thấp, mắt nâu, ~25 tuổi — theo kiểu Sakura ở 4/5 video gốc.
- Mỗi tập `characters.json` PHẢI có `{"id":"sakura","name":"さくら","ref":true,"main":false,"age":25,"gender":"F",
  "look":"<trang phục theo vai của tập>","voice":{"voice_id":"minimax_209536448462924"}}`. `make_video.masters_from_bible`
  tự CHÉP ảnh gốc vào `_ref_sakura\001.png` của tập (không vẽ mặt mới). Chỉ đổi trang phục qua `look`/prompt.
- Cấm vẽ lại ảnh gốc khi đã có tập đầu dùng nó — đổi là lệch mặt giữa các tập.

## §1b CỘT SHEET TAB `L-shakai-no-naze` (A→K)
A STT · B NỘI DUNG (tiêu đề JP + dịch) · C FOLDER (ghi ngay khi tạo tập) · D KỊCH BẢN (`Done` khi xong phần máy 1) ·
E TITLE-DESCRIPTION · F TAGS · G THUMBNAIL · H STATUS-IMG (`cần ảnh (N ảnh, ~Xđ)` = lệnh cho máy 2) · I VIDEO · J LIST · K GHI CHÚ.
10 tập đầu đã ghi A2:B11 (2026-09-24) — thứ tự ưu tiên: tập 1–3 gần chủ đề video 431k (thế hệ/công sở) nhưng KHÔNG trùng.

## §2 MỘT TẬP — MÁY 1 (đúng thứ tự)
```
cd E:\CLAUDE\YOUTUBE\h2dev
:: S1 hồ sơ (tay, ~20'): assets\shakai_no_naze\epNN-<slug>\ gồm
::   competitor.txt (transcript gốc gần chủ đề nhất — lấy từ K3, file TRENDING-RESEARCH\data\shakai_no_uragawa\transcripts\<id>.json)
::   series_ctx.txt — TAB NÀY TỰ TRA (anh chốt): 3–6 dòng [Dn] số liệu/thuật ngữ, mỗi dòng có URL NGUỒN CHÍNH THỨC
::     (厚生労働省・総務省統計局・内閣府・日本生産性本部・リクルート/マイナビ調査…) + dòng SỐ ĐƯỢC PHÉP + QUY ƯỚC
::     (ghi BẮT BUỘC: câu hỏi なぜ của tiêu đề được trả lời bằng [Dn] nào; Sakura đóng vai gì).
::   title.txt (21–35 ký tự, có【漫画】) · promise.txt (1 câu) · hook\promise.txt
py -3.13 -X utf8 pipeline\make_video.py --profile shakai_no_naze --slug epNN-<slug> --den B3G
::   → S1Q/S1L → hook khoá (H1–H4) → Fable viết → S3 máy → Sol ×2 → LOCK. Lớp 3: đọc hết script.txt (luật §5).
:: characters.json (tay, sau khi đọc kịch bản): sakura (khuôn §0d) + MỌI vai có thoại hoặc ≥2 cảnh =
::   {id,name,vai,age,gender,look,ref:true,voice:{voice_id}} — voice_id chọn trong voice.cast_bank; nhân vật trung tâm "main":true.
py -3.13 -X utf8 pipeline\gan_vai.py --profile shakai_no_naze --slug assets\shakai_no_naze\epNN-<slug>
py -3.13 -X utf8 pipeline\make_video.py --profile shakai_no_naze --slug epNN-<slug> --only B5W
py -3.13 -X utf8 pipeline\make_video.py --profile shakai_no_naze --slug epNN-<slug> --only B5P
:: HOOK (máy 1 làm trọn HÌNH, docs\QUY_TAC_VIDEO_HOOK.md): ảnh hook @CAST (gen_images.py --cast-root <tập>) → clip Grok
::   → qc_hook_clip → SFX hook → hook_timeline.json → HOOK_TAP.md. Từ tập 2 (2026-09-25): GIỌNG thân do máy 2 lồng (ai33 không
::   tất định) nên hook_timeline.json ghi mốc THEO SỐ CÂU, KHÔNG theo giây: shots[].cau=[a,b] (câu a..b của voice_roles, nối
::   tiếp từ câu 1, mỗi cảnh nên ≥3s ⇒ gộp câu ngắn), sfx[].cau + lech (giây sau lúc câu bắt đầu). Máy 1 KHÔNG lồng giọng hook.
::   B8 máy 2 tự tính lại giây + cắt hook_voice.* từ giọng thân (ghep_hook_noi_truoc.neo_lai_theo_cau) rồi ghép THAY HÌNH.
py -3.13 -X utf8 pipeline\sfx_than.py --profile shakai_no_naze --slug assets\shakai_no_naze\epNN-<slug> --plan
::   (Opus chọn 18–40 chỗ đặt tiếng theo nội dung → sfx_plan.txt; thiếu file này dong_goi DỪNG; B8 máy 2 tự --kho + --tron)
py -3.13 -X utf8 pipeline\dong_goi_may2.py --job shakai_no_naze epNN-<slug>
::   (chép _ref_sakura từ ảnh gốc lane, vẽ master vai khác nếu thiếu, gói vai.txt + _ref_* + hook\, ghi sheet D=Done, H=cần ảnh)
```
Lần giao ĐẦU TIÊN của lane: bundle máy 2 phải có profile + code nhánh ai33 mới:
`py -3.13 pipeline\dong_goi_may2.py --bundle --profile-list shakai_no_naze`.

## §2b MÁY 2 (làm theo `_BANGIAO.txt`)
`make_video.py --profile shakai_no_naze --slug <tập> --redo-voice` → B4 đọc `vai.txt` bằng ai33 đa giọng (cần `AI33_API_KEY`)
→ ảnh bằng Flow Tool (mỗi id 1 Character trong CÙNG 1 project, `sakura` dùng đúng `_ref_sakura\001.png`) → B8:
`bong_thoai.do_mat` định vị mặt → assemble (bóng không đuôi, xfade + zoom 2,5%) → trộn SFX → **ghép hook TỰ ĐỘNG**
(`assemble.hook_tu_ghep`, 2026-09-25) → B10 → B11 giao `results\video_render\shakai_no_naze\<slug>\`.
**Giao ĐÚNG 2 video (anh chốt 2026-09-25):** `final.mp4` = bản đăng, ĐÃ có hook (100% video giao bắt buộc có hook ⇒ không còn
tên `final_with_hook`) + `final-vietsub.mp4` = cùng video cháy phụ đề Việt 720p cho anh đọc (`publish.ten_review`,
`review_vi_cao`). Kèm `phude.srt` + `tomtat.txt` (text). Máy 2 KHÔNG chạy ghep_hook tay.

## §3 GATE (profile, đo từ 11 video gốc)
title 21–35 ký tự (kể cả【漫画】) · 18' ≈ 5.600 chữ · 6 chặng `budget.sections` (chặng 1 đo, 2–6 ước lượng — đo lại sau 2 tập) ·
thoại ≤65% · 0,6–2 phẩy/câu · 7–14 chữ/nhịp · `dialogue_own_sentence` · hook H41/H22/H26/H13 + closer K23
(「その答えは、ある〜の物語の中にあった」) · gói đăng: lời hứa ≤60s, câu mâu thuẫn ≤30s, lõi tiêu đề ≤90s, nghi thức 「その答えは」.

## §5 LUẬT CỨNG (lớp 3 đọc bản khoá theo đúng danh sách này)
1. MỌI số liệu xã hội (%, 倍, 万人, 万円, năm khảo sát) có trong `series_ctx.txt` kèm URL và được diễn giải ĐÚNG NGHĨA
   (ai khảo sát, đối tượng nào, năm nào). Số ngoài tư liệu = viec_tay.
2. Câu hỏi なぜ của tiêu đề phải được TRẢ LỜI rõ ở chặng dữ liệu + kết.
3. Sakura là người hỏi (「えっ、どういうことですか？」…), không thành nhân vật chính có cốt truyện riêng.
4. Hậu quả đến từ cơ chế/thị trường/thời gian — không trả thù, không hả hê. Kết có tri ân + câu hỏi mời bình luận + outro.
5. Không dùng lại nhân vật/tình tiết đặc trưng 11 video gốc (田中の議事録AI, 退職代行, 母親のクレーム電話, 熊谷部長, 神谷…).
6. Mỗi lượt thoại mới phải rõ ai nói (câu người kể trước/sau) — `gan_vai.py` và bóng thoại dựa vào đó.
7. Không chữ/biểu đồ/poster trên ảnh (style_suffix đã cấm; soi lại prompt ảnh B5W).

## §5b PHÂN VAI MODEL
Fable viết (S2) · Opus vá (S4) + gắn vai (`gan_vai.py`) · Sol chấm (lens plain + `script_qc.lane_rules`) · Fable viết prompt
ảnh (B5W CAST) · máy: S3, ai33 đa giọng, bóng thoại.

## §9 BẪY ĐÃ GẶP / ĐÃ ĐO
| Triệu chứng | Nguyên nhân | Xử |
|---|---|---|
| Hồ sơ gốc ghi "1 cảnh minh hoạ/tập", "1 giọng", "Sakura khác mặt" | báo cáo chỉ đọc transcript, chưa xem hình/nghe giọng | đo thật `DO_THUC_TE_2026-09-24.md`: ~7,5 s/ảnh, đa giọng, Sakura cùng kiểu 4/5 video |
| Tưởng kênh gốc dùng VOICEVOX như Lane K | cùng khuôn manga đa giọng | so vân giọng 43 giọng VOICEVOX: trung vị 0,758 (K thật 0,881) → dùng ai33 |
| Đếm 「さくら」 trong phụ đề ra 0 | phụ đề tự động cắt tên thành 「さ」 | đếm trên `_raw/transcripts.json` (whisper): 95 lần |
| ep01 S3 ESCALATE "thoại dính lời dẫn" ở câu outro | outro_line cũ chứa 「なぜ？」 giữa câu người kể | đã bỏ ngoặc khỏi `script.outro_line` — cấm dùng 「」 trong outro/câu người kể |
| Sol FIX 3 vòng liên tiếp (chỉ [VỪA], mỗi patch lại sinh lỗi mới) | Sol không tất định | ep01: sửa tay 5 chỗ theo report vòng cuối + S3 sạch → `gate_common.ghi_lock(...,'PASS')` (quy ước lean-flow-fix-x3) |
| Câu nội tâm của さくら bị gán `ke` | gan_vai mặc định nội tâm = nhân vật chính | đã vá: `characters.json` khai `"inner_voice": true` cho sakura → gan_vai gán 心の声 cho vai đó |
| Câu trả lời khảo sát viết thành dòng「」riêng | không phải lời nhân vật → gan_vai phải gán cho ai đó | lớp 3: gộp vào lời người kể, không ngoặc |
| B8 `sinh_neo` lỗi "đoạn 19 không còn chỗ cho 120.png" | prompt_doan dồn 7 ảnh vào đoạn thoại ngắn (mỗi ảnh cần ≥1s trên cue riêng) | chuyển 2 ảnh cuối đoạn sang đoạn kế trong `img_doan.txt` (bản gốc giữ `img_doan.orig.txt`) |
| Bóng thoại câu dài: chữ lòi ra ngoài bóng | bóng hình viên thuốc, góc khối chữ vượt đường cong | đã vá `bong_thoai.render_cue`: tail=false → elip ngoại tiếp khối chữ (×1,42) |
| Hook dính 2 lần tiếng / lệch mốc nếu lồng tiếng hook riêng | ai33 đa giọng KHÔNG tất định (khác VOICEVOX) | hook = đoạn 1 của script → cắt `hook_voice.mp3` + `hook_voice_roles.json` THẲNG từ `voice.mp3`/`voice_roles.json` của thân; `ghep_hook_noi_truoc.py` tự vào chế độ THAY HÌNH |
| `ghep_hook_noi_truoc.py --tap ..\assets\...` ffmpeg lỗi | chạy ffmpeg với cwd=hook\ nên đường tương đối hỏng | đã vá `.resolve()`; vẫn nên truyền đường tuyệt đối |
| G1 gói đăng trượt vì promise.txt là CÂU TRẢ LỜI | cổng đo độ phủ lời hứa trong tiêu đề + 60s đầu | promise.txt viết dạng câu hỏi bám tiêu đề (ep01: 「エースの若手はなぜ出世を拒むのか。」) |

| ep02: S3 ESCALATE "script không bắt đầu bằng hook" | patch S4 của Opus chèn 1 đoạn số liệu TRƯỚC hook đã khoá (và vòng sau chèn chi tiết luật lao động/truy lĩnh tăng ca) | lớp 3 xoá đoạn chèn + sửa tay theo report Sol cuối → lock PASS; luôn soi đoạn đầu + chi tiết pháp lý mới xuất hiện sau patch |
| ep02: sfx_plan gắn tiếng vào câu 2 của hook | hook viết mỗi câu 1 dòng → trải nhiều "đoạn", bản cũ chỉ bỏ para 1 | đã vá `sfx_than.plan`: bỏ theo SỐ CÂU của hook_locked.txt |
| Anh xem ep01: chữ nhỏ · không chuyển cảnh · thiếu tiếng động | profile ban đầu 40px, cut, không SFX | 24/09: cỡ 64/48 + tách câu dài · xfade 0,3 + zoom 2,5% alt · `sfx_than.py` (plan máy 1 / trộn B8) |

## §10 SỐ ĐO TẬP 1 (máy 1 làm trọn, anh cho phép ngoại lệ 2026-09-24)
Kịch bản 6.017 chữ → video 20,1' (char_rate thật 299 → profile tự nắn 307,8) · ai33 đa giọng 299 câu 7 giọng 15' máy
(~7.500 credit) · 155 ảnh thân gpti2 14.890đ + 6 master + 7 ảnh hook · 7 clip Grok free (GPM dòng 106–112) · B8 5' ·
B4Q/B8Q ĐẠT · Tổng ~2 giờ. Sản phẩm: `FlowHandoff_local\results\video_render\shakai_no_naze\ep01-shusse-shitakunai\final_with_hook.mp4`.
