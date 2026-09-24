# BẮT ĐẦU LANE K — `yakkyoku-sukatto` · 薬局スカッと帳 (Yakkyoku Sukatto-chō, dịch: "Sổ tay quả báo hiệu thuốc")

> Anh nói **"thực hiện lane yakkyoku-sukatto"** (hoặc "LANE K") → tab này ĐỌC HẾT file này trước, mở đầu báo cáo bằng
> `@lane:yakkyoku-sukatto`, rồi làm ĐÚNG THỨ TỰ mục 4. Không tìm hiểu lại từ đầu, không đoán. File này là "cửa vào";
> chi tiết vận hành nằm ở SOP (mục 4 giai đoạn 2 sẽ viết). Cập nhật mục 2 mỗi khi trạng thái đổi.

## 1. ĐỊNH DANH (không đổi)
| Mục | Giá trị |
|---|---|
| Mã lane / profile id | `yakkyoku-sukatto` (thư mục `assets/yakkyoku-sukatto/`; tab sheet = **`K-yakkyoku-sukatto`**) |
| Kênh thật | 薬局スカッと帳 · `@yakkyoku-sukatto` · `UCk8E_FHIYjY7GN_qdpSKaMw` |
| Mail (GMAIL dòng 12) | `rosellagreysonbk920@gmail.com` — profile GPMLogin cùng tên, anh login tay |
| Kênh mẫu (clone) | 千種テンカ (Chigusa Tenka, dịch: "Tenka Chigusa" — tên riêng) `https://www.youtube.com/channel/UCEBA1RFfkXQtqgiDVLh4bcw` |
| NOTE | dòng 8 (STT 7) — cột L đã ghi `@yakkyoku-sukatto` = kênh đã setup |
| Tab sheet sản xuất | **`K-yakkyoku-sukatto`** (header A→K, mục 6) |
| Thư mục làm việc | `E:\CLAUDE\YOUTUBE\h2dev\assets\yakkyoku-sukatto\` (branding đã có; tập = `ep<NN>-<slug>\`) |
| Giao hàng bước 3 | `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\video_render\yakkyoku-sukatto\<slug>\` (quy tắc 24/09 — KHÔNG dùng tên tab) |
| Format | Manga công sở/nghề nghiệp, người kể ngôi 3 nhưng nội tâm chen ngôi 1 (không ngoặc kép), narration AI đa giọng kiểu VOICEVOX (nhiều giọng luân phiên theo nhân vật — KHÁC hẳn 1 giọng xuyên suốt của mọi lane khác). Cấu trúc: câu cửa miệng nhân viên tệ mở đầu → 20 năm bị đối xử tệ → sự kiện kích hoạt → nghỉ/bị thải → **KHÔNG có cảnh trả thù** (hậu quả tới từ HỆ THỐNG, không phải nhân vật ra tay) → câu cuối lặp lại đúng câu cửa miệng mở đầu |
| Giọng | **ĐÃ CHỐT 2026-09-24: ĐA GIỌNG VOICEVOX y như kênh gốc** — người kể 玄野武宏 · nhân vật chính 黒沢冴白 · 事務さん 波音リツ cố định; vai phụ theo `voice.cast_bank` (đo máy: `docs\channel_dna\yakkyoku-sukatto\GIONG_VAI.md`). Chi tiết: `docs\SOP_LANE_K.md` §0c. |
| Khác lane nào | KHÁC MỌI LANE: (1) ngách CÔNG SỞ/NGHỀ NGHIỆP (dược sĩ), không phải người già/hưu trí như E–J; (2) khán giả không rõ độ tuổi cụ thể (chưa đo, cần Channel Analyzer); (3) kỹ thuật giọng đa nhân vật VOICEVOX chưa từng làm ở lane nào |

## 2. TRẠNG THÁI (cập nhật mỗi lần đổi)
- ✅ 2026-09-24 nghiên cứu kênh xong bởi dự án TRENDING-RESEARCH (KHÔNG qua NOTE dòng thường lệ — đây là
  ỨNG VIÊN do TRENDING-RESEARCH tự phát hiện, không phải do anh đưa URL trước). Báo cáo DNA đầy đủ đã có sẵn
  (khác các lane E–J vốn chỉ có handoff ngắn), xem mục 3.
- ✅ 2026-09-24 anh chốt qua hội thoại: NOTE dòng 8 (STT 7) → Lane K, mã lane = `yakkyoku-sukatto` (anh chốt lại 2026-09-24: lane = tab = `K-yakkyoku-sukatto`, mọi tên/thư mục của lane dùng `yakkyoku-sukatto`).
- ✅ 2026-09-24 setup kênh A+B xong bằng `tools/channel_branding.py` (branding gpti2 + 6 mục settings, verify
  reload). Tên/handle/mô tả/hashtag/keywords do em đề xuất dựa theo văn phong disclaimer + hashtag thật của
  kênh mẫu (`#薬剤師 #薬局 #漫画 #スカッと` + thêm `#因果応報`), anh chưa duyệt riêng từng chữ — **soi lại nếu cần đổi**.
  Handle của kênh mình: `@yakkyoku-sukatto`.
  Sheet GMAIL dòng 12 + NOTE dòng 8 đã ghi, tab `K-yakkyoku-sukatto` + header đã tạo.
- ✅ 2026-09-24 đổi toàn bộ tên lane theo tên kênh mình → `yakkyoku-sukatto` (thư mục assets, file này, router, danh bạ); hồ sơ
  TRENDING-RESEARCH đã chép về `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneK_from_research\`.
- ✅ 2026-09-24 K1+K2 xong (4/4 video dài, DNA đủ 11 đề mục, K3 `retrieve_videos.py` chạy được) →
  `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\yakkyoku-sukatto\`. Lượt chạy là của TRENDING-RESEARCH (cùng lúc, cùng máy), chép
  nguyên về. ⚠️ `_raw\transcripts.json` là bản whisper, SAI CHỮ nhiều hơn phụ đề tự động (学知癖の役剤士 = 口癖の薬剤師
  (dược sĩ có câu cửa miệng), 斬業 = 残業 (tăng ca)) → đo độ dài/nhịp thì dùng được; trích nguyên văn thì lấy
  `laneK_from_research\data\transcripts\`.
  Hook 4 video dài: TRENDING-RESEARCH đang nạp vào `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\hooks.jsonl`.
- ✅ 2026-09-24 anh chốt: giọng ĐA NHÂN VẬT đúng như kênh gốc (VOICEVOX, không clone) · khoá mặt theo TỪNG TẬP (mỗi
  vai có thoại hoặc ≥2 cảnh = 1 ref; 1 ảnh Flow Tool khoá tối đa 3 nhân vật) · lời thoại hiện bằng BÓNG THOẠI chữ dọc có
  đuôi chỉ về người nói, vẽ bằng máy (không để AI vẽ chữ) · hook = clip Grok · Shorts làm sau.
- ✅ 2026-09-24 VOICEVOX engine 0.25.2 cài tại `E:\CLAUDE\YOUTUBE\VOICEVOX_ENGINE\0.25.2\run.exe` (cổng 50021). Gán giọng↔vai
  4 video gốc bằng máy: `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\yakkyoku-sukatto\GIONG_VAI.md` (3 giọng cố định: người kể
  玄野武宏 · nhân vật chính 黒沢冴白 · 事務さん 波音リツ; vai phụ đổi theo tập).
- ✅ 2026-09-24 GIAI ĐOẠN 2 XONG (anh giao làm hết 1→8 không cần duyệt): profile `profiles\profiles\yakkyoku-sukatto.json`
  (gate đo từ 4 video gốc) · giọng VOICEVOX 312,5 chữ/phút · code mới `cau_vai.py` `gan_vai.py` `tts_voicevox.py`
  `bong_thoai.py` + @CAST trong `gen_images.py`/`prompt_doan.py`/`make_video.py`/`dong_goi_may2.py` (test
  `pipeline\tests\test_lane_k_da_giong.py`) · **SOP `docs\SOP_LANE_K.md`** · 10 tập ở tab K-yakkyoku-sukatto A2:B11 ·
  đơn cài VOICEVOX cho máy 2 `FlowHandoff_local\shared\GIAO_VIEC_MAY2_CAI_VOICEVOX.md`. Từ nay LÀM THEO SOP, mục 4 dưới
  đây chỉ còn giá trị lịch sử.
- ✅ 2026-09-24 TẬP 1 `ep01-tantou-janai` xong phần máy 1 + ĐÃ GIAO máy 2: kịch bản LOCK PASS (Sol PASS×2, 5.665 chữ ≈ 18') · vai.txt 259 câu/10 vai · 8 master _ref_<id> · 136 prompt @CAST (B5W) + B5P · hook 7 ảnh + 7 clip Grok (QC PASS hết) + 4 SFX + HOOK_TAP.md · job `FlowHandoff_local\jobs\ep01-tantou-janai` · sheet D2=Done, H2=cần ảnh. Tiêu đề/thumbnail: kênh mới `title_auto` TẮT — anh chạy TITLE tay tập đầu.
- ⚠️ 2026-09-24 NGOẠI LỆ anh cho (CHỈ TẬP 1): máy 1 làm trọn video ep01 từ đầu đến cuối bằng ảnh gpti2 để dò vướng mắc (máy 2 chỉ vận hành, không code được). Từ tập 2 trở lại luật chung: máy 1 xong bước 1 → giao máy 2 vẽ ảnh bằng Google Flow Tool + dựng video.
- ✅ 2026-09-24 21:05 TẬP 1 VIDEO HOÀN CHỈNH (máy 1 làm trọn theo ngoại lệ): final_with_hook.mp4 17:20,8 · 1920×1080 30fps · B4Q ĐẠT · B5Q ĐẠT (136 ảnh gpti2 12.380đ) · B8Q ĐẠT sync 4,6 · hook thay hình 0–31,02s · B10 0 lỗi nặng · giao tại `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\video_render\yakkyoku-sukatto\ep01-tantou-janai\` (final_with_hook.mp4 + review_vi.mp4 + phude.srt + credits_giong.txt). Sheet H2=Video done, I2=đường dẫn. Chưa làm: tiêu đề/mô tả/thumbnail/tags (anh loại khỏi phạm vi).
- ✅ 2026-09-24 22:xx ep01 LÀM LẠI theo anh duyệt: chữ lời kể 64px sát mép (tách hộp khi >24 chữ) · thoại 48px · định vị mặt kẻ lưới cho cả 136 ảnh · chuyển cảnh + nhạc giống kênh gốc đo máy (mờ chồng 0,3s + phóng vào ×1,025 — NGOẠI LỆ luật cấm zoom, anh chốt; nhạc nền Suno thấp hơn giọng ~17,7 dB; gốc không SFX). Đủ điều kiện dự án tiêu đề `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH`: char_rate đo thật 316,7 · SOP · 10 tập A2:B11 · C2 = đường dẫn tập · script.txt + HOOK_TAP.md PASS + promise.txt · thư mục `E:\CLAUDE\YOUTUBE\CHANEL\yakkyoku-sukatto\ep01-tantou-janai\` đã tạo (tập sau `dong_goi_may2 --job` tự tạo). Còn thiếu BÊN ĐÓ: `config\lanes\yakkyoku-sukatto.thumb.yaml`; `title_auto` vẫn TẮT.
- ❌ (lịch sử, đã làm) profile JSON · giọng (nghi vấn đa giọng ở mục 1)
  · char-rate · SOP · danh sách tập · bất kỳ kịch bản nào. Anh mới duyệt SETUP KÊNH, chưa ra lệnh giai đoạn 2
  — tab mở phiên mới phải HỎI trước khi bắt đầu mục 4.

## 3. TÀI LIỆU — đọc theo thứ tự này, đường dẫn thật trên máy 1
1. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneK_from_research\GIAO_VIEC_LANE_K_2026-09-24.md` — hồ sơ giao việc gốc (tóm tắt
   lý do chọn, 4 video hit, còn treo).
2. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneK_from_research\KENH_MAU_REPORT.html` — báo cáo DNA ĐẦY ĐỦ NHẤT trong mọi
   lane hiện có: công thức tiêu đề (5 khối), cấu trúc chương/beat có mốc phút:giây thật, hook 0–90s + hook cả
   video cho 4 video full, cấu trúc thumbnail (đọc bằng mắt), kỹ thuật kể chuyện (đa giọng VOICEVOX, không có
   cảnh trả thù), 5 kênh tương tự để tham khảo, checklist 7 bước clone ngách khác. Artifact online (nếu cần xem
   nhanh không qua máy): `https://claude.ai/artifact/596TC5cpMco57xVVw9oEKr`.
3. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneK_from_research\data\` — dữ liệu thô: `channel.json` (meta + 7 video +
   description + tags), `thumbs\*.jpg`, `transcripts\*.json` (mốc giây thật).
4. `E:\CLAUDE\YOUTUBE\h2dev\assets\yakkyoku-sukatto\branding\KENH.json` — tên/handle/mô tả/keywords/hashtag đã lên kênh (nguồn chân lý branding).
5. Khuôn để chép: `docs\SOP_LANE_F.md` + `profiles\profiles\teinengo-real.json` (fiction_facts + structure_block +
   Fable viết/B3R) — gần nhất vì cùng REF-LOCK nhân vật lặp trong tập và cấu trúc kịch tính-quả báo. **Lưu ý: lane
   này KHÔNG giống list_countdown (E/G) và KHÔNG giống documentary lịch sử (I)** — cấu trúc riêng theo mục 1.
6. Luật toàn dự án: `CLAUDE.md` (router + ⛔ Claude chỉ làm BƯỚC 1, không render, không tự upload-job lần đầu;
   mục "🎙️ CHỖ MÁY 2 TRẢ HÀNG" + "XONG TẬP = GHI SHEET NGAY" + toàn bộ mục HOOK 2026-09-23/24) ·
   `docs\QUY_TRINH_SETUP_KENH.md` (đã làm, chỉ đọc khi cần sửa kênh) · `docs\QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md`
   (luồng lean, hook bắt buộc, cổng S1L) — lane K nên khai `flow="lean"` ngay từ đầu như F/G/satori thay vì
   luồng cũ, vì mọi lane mới sau 2026-09-20 đều dùng lean.

⚠️ Hook 20–30s bắt buộc trước S2 (video sinh Grok/Veo, không phải ảnh render trừ khi khai `visual_exception`) —
xem `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b + `docs/QUY_TAC_VIDEO_HOOK.md`. Cổng S1L (hook+gói đăng+
promise.txt) chặn CỨNG trước khi viết — không né được.

## 4. QUY TRÌNH — làm bước nào trước
### Giai đoạn 2 — dựng hạ tầng lane (1 LẦN, đúng thứ tự, xong mới sang giai đoạn 3)
1. **Channel Analyzer K1+K2** cho kênh mẫu `UCEBA1RFfkXQtqgiDVLh4bcw` (7 video, kênh còn quá mới nên chạy hết
   toàn bộ video, không chỉ top-view) → `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\yakkyoku-sukatto\` (đặt tên thư mục theo mã lane cho nhất
   quán, KHÁC bản HTML report của TRENDING-RESEARCH ở mục 3 — 2 hồ sơ dùng SONG SONG: report HTML đọc hiểu văn
   phong/thumbnail, CHANNEL_DNA.md dùng `retrieve_videos.py` khi viết tập).
2. **HỎI ANH chốt giọng** (nghi vấn mục 1): đa giọng VOICEVOX-style hay đơn giản hoá 1–2 giọng ai33/OpenSpeaker.
   Đây là quyết định ảnh hưởng cả kiến trúc TTS của lane, không tự chọn.
3. **Profile** `profiles\profiles\yakkyoku-sukatto.json` (chép khuôn teinengo-real, sửa mạnh): `narrator` = kể ngôi 3 +
   nội tâm ngôi 1 không ngoặc · `script.mode = fiction_facts` (nhân vật/hiệu thuốc hư cấu, nhưng luật lao động/
   quy trình dược sĩ nêu tên phải có thật) · `script.structure` = cấu trúc riêng theo mục 1 (câu cửa miệng →
   20 năm → kích hoạt → nghỉ/thải → hệ thống trả giá, KHÔNG trả thù cá nhân → lặp câu cửa miệng) · `body.mode=
   ai_images` · `image.ref_lock=true` nhân vật chính trong tập · `publish.sheet_tab="K-yakkyoku-sukatto"`
   (khai NGUYÊN VĂN tên tab đã tạo — pipeline/sheet_tab.py đọc field này, KHÔNG suy ra từ lane_id) ·
   `publish.upload_channel="yakkyoku-sukatto"` (dùng cho `results\video_render\yakkyoku-sukatto\`) ·
   `script.flow="lean"` (mọi lane mới từ 20/09 dùng lean, xem mục 3.6) · `script.hook.enabled=true` +
   `script.hook.sfx=true` + `script.hook.visual_kind="video_sinh"` (bắt buộc, không có lý do dùng
   `visual_exception`). **`script.gate` PHẢI ĐO** từ transcript thật trong `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneK_from_research\data\transcripts\` và `docs\channel_dna\yakkyoku-sukatto\_raw\`.
4. **Char-rate**: `py -3.13 pipeline\calibrate.py --profile yakkyoku-sukatto` sau khi đã chốt giọng ở bước 2.
5. **SOP** `docs\SOP_LANE_K.md` theo khuôn `SOP_LANE_F.md`: §0 bảng delta, **§0b Channel Analyzer**, §0c giọng
   (ghi rõ quyết định đa giọng vs đơn giản hoá + lý do), §1 quyết định, §1b danh sách 10 tập + quy tắc cột sheet,
   §2 lệnh chạy, §3 gate, §5b phân vai.
6. **Router**: 1 dòng bảng lane `CLAUDE.md` + 1 dòng `docs\DANH_BA_LANE.md` + cập nhật mục 2 file này.
7. **Danh sách 10 tập** vào tab `K-yakkyoku-sukatto` cột A/B: mỗi tập 1 câu chuyện dược sĩ/nhân viên hiệu thuốc
   khác nhau (đủ đa dạng vị trí: quản lý, nhân viên mới, đại diện nhà thuốc/kho...), bám công thức tiêu đề 5
   khối trong report HTML mục 3.2, tránh trùng 4 tựa đã có của kênh mẫu.

### Giai đoạn 3 — sản xuất 1 tập (CHỈ tập anh chỉ định "cho làm tập X")
1. Tạo `E:\CLAUDE\YOUTUBE\h2dev\assets\yakkyoku-sukatto\ep<NN>-<slug>\`, ghi cột C.
2. Hồ sơ đề tài: `competitor.txt` (1 transcript thật qua `retrieve_videos.py --dna-dir docs\channel_dna\yakkyoku-sukatto
   --topic "..."`) + `series_ctx.txt` (luật lao động/quy trình dược sĩ Nhật CÓ NGUỒN — cấm bịa; nhân vật/hiệu
   thuốc hư cấu theo đúng disclaimer kênh mẫu).
3. `py -3.13 -X utf8 pipeline\make_video.py --profile yakkyoku-sukatto --slug ep<NN>-<slug>` — luồng lean, chạy tới
   mốc anh cho phép (mặc định theo các lane khác: kịch bản + QC, chưa ảnh/video).
4. Xong tập (phần máy 1) = **GHI SHEET NGAY**: tab `K-yakkyoku-sukatto` cột D = `Done`, cột H = `cần ảnh (N ảnh,
   ~Xđ)` khi tới lượt giao máy 2 — `pipeline\dong_goi_may2.py --job` tự ghi cả hai, KHÔNG hỏi "anh bấm giao".
5. Bước 3 (ghép video) = máy 2 nhận qua `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\video_render\yakkyoku-sukatto\<slug>\` (nguồn chân
   lý = dòng TRẢ HÀNG trong `_BANGIAO.txt`). Claude Code KHÔNG render (trừ hook: máy 1 được vẽ ảnh hook + sinh
   clip hook Grok theo quy tắc 24/09, xem `docs\QUY_TAC_VIDEO_HOOK.md`).

## 5. LUẬT CỨNG RIÊNG LANE (từ report HTML mục 5 "kỹ thuật kể chuyện")
- **KHÔNG có cảnh trả thù cá nhân** — hậu quả luôn tới từ HỆ THỐNG (khách hàng phàn nàn dồn lại, thanh tra, đồng
  nghiệp nghỉ việc kéo theo thiếu người...), nhân vật chính không bao giờ "ra tay" — đây là điểm khác hẳn thể
  loại 復讐/trả thù thông thường, giữ đúng mới đúng "quả báo" (因果応報) chứ không phải "phục thù".
- Câu cuối LUÔN lặp lại đúng câu cửa miệng mở đầu (đóng vòng).
- Miễn trừ trách nhiệm cố định 3 dòng đầu mô tả (bản dịch từ kênh mẫu): nội dung là hư cấu, không phải tư vấn y
  tế/dược, không viết chi tiết xác định được cửa hàng/cá nhân thật — BẮT BUỘC giữ nguyên tinh thần này khi viết
  mô tả video (không phải chỉ ở mô tả kênh).
- Người kể ngôi 3 nhưng để lộ nội tâm nhân vật chính bằng câu ngôi 1 KHÔNG đặt trong ngoặc kép — kỹ thuật viết
  riêng của ngách này, khác cách kể ngôi 1 xuyên suốt của satori/F.
- Số liệu/quy trình dược sĩ (năm kinh nghiệm, chức danh 管理薬剤師...) nêu ra phải hợp lý với luật lao động Nhật
  thật, không bịa số vô lý.

## 6. CỘT SHEET TAB `K-yakkyoku-sukatto` (A→K, giống mọi lane khác)
A STT (= số ep) · B NỘI DUNG · C FOLDER · D KỊCH BẢN (`Done` khi xong máy 1) · E TITLE-DESCRIPTION · F TAGS
(không làm marker) · G THUMBNAIL · H STATUS-IMG (`cần ảnh (N ảnh, ~Xđ)` khi tới lượt giao máy 2) · I VIDEO ·
J LIST · K GHI CHÚ.
