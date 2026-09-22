# BẮT ĐẦU LANE F — `teinengo-real` · 定年後のリアル (hưu trí Nhật, manga story kịch tính tiền)

> Anh nói **"thực hiện lane teinengo-real"** (hoặc "lane F") → tab này ĐỌC HẾT file này trước, mở đầu
> báo cáo bằng `@lane:teinengo-real`, rồi làm ĐÚNG THỨ TỰ mục 4. Không tìm hiểu lại từ đầu, không đoán.
> File này là "cửa vào"; chi tiết vận hành nằm ở SOP (mục 4, giai đoạn 2 sẽ viết). Cập nhật mục 2
> mỗi khi trạng thái đổi.

## 1. ĐỊNH DANH (không đổi)
| Mục | Giá trị |
|---|---|
| Mã lane / profile id | `teinengo-real` (= tên tab sheet = thư mục `assets/teinengo-real/`) |
| Kênh thật | 定年後のリアル · `@teinengo-real` · `UCIimxP275YufOXXIlu9y9Lg` |
| Mail (GMAIL dòng 7) | `VirgiliTraino95@gmail.com` — profile GPMLogin cùng tên, anh login tay |
| Kênh mẫu (clone) | 老後の暮らし研究所 `https://www.youtube.com/channel/UCRkP44Mcw-K8IktdTqxC9dg` |
| NOTE | dòng 3 (STT 2) — cột L đã ghi `@teinengo-real` = kênh đã setup |
| Tab sheet sản xuất | **`teinengo-real`** (header A→K, mục 3) |
| Thư mục làm việc | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-real\` (branding đã có; tập = `ep<NN>-<slug>\`) |
| Giao hàng bước 3 | `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-real\ep<NN>-<slug>\` |
| Format | Manga AI ngôi 1 「俺」, 1 nhân vật chính 60–67 tuổi + 1 nhân vật đối lập, kịch tính TIỀN, kết triết lý. KHÔNG list, KHÔNG bán hàng |
| Giọng | Nam trung niên, hồi ức — **`clone_2658911`** (clone kênh mẫu, anh duyệt 2026-09-20; SOP §0c) · 284,0 chữ/phút @0.95 |

## 2. TRẠNG THÁI (cập nhật mỗi lần đổi)
- ✅ 2026-09-13 nghiên cứu kênh xong (TRENDING-RESEARCH, anh duyệt).
- ✅ 2026-09-16 Channel Analyzer (K1+K2) đã chạy: 8 video, `✓ TỔNG`.
- ✅ 2026-09-20 setup kênh A+B xong (branding + 6 mục settings, verify reload), tab sheet + header đã tạo.
- ✅ 2026-09-20 giai đoạn 2: DNA copy về `docs/channel_dna/rougonokurashi/` · profile `teinengo-real.json`
  (gate ĐO từ 2 transcript story, `mode=fiction_facts` + `structure_block` 7 chặng — 2 field mới trong
  ai_steps.py/make_video.py) · giọng clone `clone_2658911` (F0 output 107 Hz khớp nguồn 105 Hz, nam) ·
  char-rate **284,0 chữ/phút @0.95** · `docs/SOP_LANE_F.md` · danh sách 10 tập (SOP §1b).
- ✅ 2026-09-20 anh duyệt: giọng `clone_2658911` GIỮ (video gốc giọng nữ thì tính sau) · 10 tập đã ghi
  tab sheet `teinengo-real` A2:B11.
- ✅ 2026-09-20 anh chốt **Fable 5.1** viết kịch bản (B3 PASS 0+1, `script.brain_model`) + nghiệm thu cuối (B3R,
  `script.final_review_model` + tiêu chí riêng `final_review_criteria`); CLI `claude` đã update 2.1.278.
- ✅ 2026-09-20 anh duyệt bật **flow lean** cho lane (từ tập 2): `--den B3G`, hồ sơ thêm `title.txt` + `SỐ ĐƯỢC PHÉP:`; profile khai `budget.sections` 7 chặng + `list_item_count=0` + `fact_exempt_units`. Quy trình chung: `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md`.
- ⚠️ **PHẠM VI HIỆN TẠI (anh chốt 2026-09-20): chỉ làm tới KỊCH BẢN + QC** (tập 1 `--den B3R`; từ tập 2 `--den B3G`).
  KHÔNG tiêu đề/mô tả/tags/thumbnail, KHÔNG sinh ảnh, KHÔNG video. Phần chuẩn bị ảnh (characters.json,
  img_prompts.txt) chỉ khi anh bảo. Quy trình chi tiết tới mốc này: `docs/SOP_LANE_F.md` §2b.
- ✅ 2026-09-20 **tập 3 (`ep03-kuriage-koukai`) LEAN → PASS, `Done`** (3 lượt, ~25').
- 📝 2026-09-21 **PHƯƠNG ÁN bước 2+3 (ảnh + video ở MÁY 2)**: `docs/PHUONG_AN_LANE_F_BUOC2_3.md` — chờ anh chốt 5 điểm (kiểu vẽ theo kênh mẫu · chữ dọc 縦書き · 10s/ảnh · ep01 vẽ 2 chặng · master ở máy 2). Khung hình thật kênh mẫu: `docs/laneF_visual_ref/`. Chưa code, chưa tốn tiền.
- ✅ 2026-09-20 **tập 2 (`ep02-saikoyou-hanbun`) chạy LEAN → Sol PASS, LOCK, cột D `Done`** — benchmark SOP §2d; tiền đề tập phải ghim đầu series_ctx.
- ✅ 2026-09-20 **tập 1 test xong tới B3R** (`ep01-fuufu-nenkin-sa`, cột D `script-qc-done`, bài học SOP §2c). CHƯA giọng/prompt ảnh/tiêu đề/thumbnail — chờ anh duyệt kịch bản + mở rộng phạm vi.

## 3. TÀI LIỆU — đọc theo thứ tự này, đường dẫn thật trên máy 1
1. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneF_from_research\LANE_F_HANDOFF.md` — 14 mục:
   công thức thắng §9, hard rules, title/hook formula §4–5, cấu trúc 7 chặng §6, tên/mô tả/hashtag/tag §12,
   đề tài tập 1 §13. Kèm `channel_analysis_老後の暮らし研究所.json` + `data/transcripts_LaneF.json` (3 transcript thật).
2. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\channel_dna\rougonokurashi\` — `CHANNEL_DNA.md` +
   `VIDEO_ANALYSIS/*.json` (8 video) + `TAG_STATS.json`. **Giai đoạn 2 phải copy sang
   `docs\channel_dna\rougonokurashi\`** rồi mới dùng `retrieve_videos.py`.
3. `FlowHandoff_local\shared\GIAO_VIEC_LANE_F.md` — tóm tắt việc + hard rules (bản ngắn của 1).
4. `assets\teinengo-real\branding\KENH.json` — tên/handle/mô tả/keywords/hashtag đã lên kênh (nguồn chân lý branding).
5. Khuôn để chép: `docs\SOP_LANE_E.md` (lane gần nhất, cùng kiểu manga/ảnh AI) + `profiles\profiles\kenko-chiebukuro.json`
   (khuôn profile) + `docs\SOP_SATORI_JP.md` §B5.0 (REF-LOCK nhân vật — lane này CÓ nhân vật lặp trong tập).
6. Luật toàn dự án: `CLAUDE.md` (router + ⛔ CẤM TUYỆT ĐỐI: Claude chỉ làm BƯỚC 1, không render, không tự
   upload-job lần đầu) · `docs\QUY_TRINH_SETUP_KENH.md` (đã làm, chỉ đọc khi cần sửa kênh).

## 4. QUY TRÌNH — làm bước nào trước
### Giai đoạn 2 — dựng hạ tầng lane (làm 1 LẦN, theo đúng thứ tự, xong mới sang giai đoạn 3)
1. **Copy DNA**: `FlowHandoff_local\results\channel_dna\rougonokurashi\` → `docs\channel_dna\rougonokurashi\`.
2. **Profile** `profiles\profiles\teinengo-real.json` (chép khuôn kenko-chiebukuro, sửa từng field):
   `id/slug_dir/competitor/channel_dossier/channel_dna_dir` · `narrator` = nam 60–67 ngôi 1 「俺」, hồi ức ·
   `script.mode` = fiction có ràng buộc số liệu thật (nhân vật hư cấu, chế độ hưu trí/số tiền PHẢI có nguồn —
   ghi `ctx_label`) · `script.structure` = 7 chặng handoff §6 (KHÔNG `list_countdown`, KHÔNG `chapters5`) ·
   `script.target_minutes` 16–24 · `body.mode=ai_images` · `image.ref_lock=true` (2 nhân vật: @REF/@REF2 trong
   1 tập, KHÔNG xuyên tập — kênh RỜI RẠC) · `image.style_suffix` manga nam trung niên, nội thất/đường phố Nhật ·
   `thumbnail` = ảnh người gần thật kịch tính + nền tối + chữ vàng/đỏ (handoff §11) · `publish.sheet_tab="teinengo-real"`.
   **`script.gate` PHẢI ĐO** từ 3 transcript thật (`data/transcripts_LaneF.json`): title_len, hook_chars,
   comma/breath — không chép số của lane khác (hàng rào #1 CLAUDE.md).
3. **Giọng CLONE** (anh chốt): tách 20–30s giọng sạch từ 1 video kênh mẫu (bỏ intro) → `POST /voice-clone`
   theo skill `openspeaker_voice_clone.md` → nghe thử A/B → **HỎI ANH trước khi giữ voice_id** (giọng người
   thật, chỉ giữ khi anh xác nhận) → ghi `voice.id=clone_<id>` vào profile.
4. **Char-rate**: `py -3.13 pipeline\calibrate.py --profile teinengo-real` (`calib_style=story`) → ghi
   `voice.char_rate` + `char_rate_measured_at`. Chưa đo thì `make_video.py` tự DỪNG — đúng thiết kế.
5. **SOP** `docs\SOP_LANE_F.md` theo khuôn `SOP_LANE_E.md`: §0 bảng delta (khác E/satori chỗ nào), **§0b Channel
   Analyzer** (bắt buộc), §1 quyết định, §1b danh sách 10 tập + quy tắc cột sheet, §2 lệnh chạy, §3 gate, §5b phân vai.
6. **Router**: thêm 1 dòng bảng lane trong `CLAUDE.md` + 1 dòng `docs\DANH_BA_LANE.md` + cập nhật mục 2 file này.
7. **Danh sách 10 tập** vào tab `teinengo-real` cột A (STT) + B (nội dung 2–4 câu): bám HIT §3 (nhân vật + tuổi +
   SỐ TIỀN + cảm xúc), tránh trùng tựa video hit của kênh mẫu. Tập 1 đã đề xuất §13:
   「【漫画】60歳で退職した妻と私…5年後、夫婦の年金生活に"差"が出た本当の理由」(góc vợ chồng, kênh mẫu chưa khai thác).

### Giai đoạn 3 — sản xuất 1 tập (CHỈ tập anh chỉ định "cho làm tập X", memory `chi-chay-dong-duoc-chi-dinh`)
1. Tạo `assets\teinengo-real\ep<NN>-<slug>\`, ghi cột C.
2. Hồ sơ đề tài: `competitor.txt` (1 transcript thật cùng dạng, chọn qua `retrieve_videos.py --dna-dir
   docs\channel_dna\rougonokurashi --topic "..."`) + `series_ctx.txt` (số liệu hưu trí Nhật CÓ NGUỒN — cấm bịa).
3. `py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-real --slug ep<NN>-<slug>` — chạy tới HẾT bước 1:
   B3 kịch bản + gate → B3Q/B3F (+B3S nếu bật) → B4 giọng + B4Q nghe → B5W prompt ảnh + B5P → master REF-LOCK
   2 nhân vật → `TIEU_DE_MO_TA.txt` + `thumb_text.txt` (bước 1 PHẢI để lại, không để bước 3 tự sinh).
4. Ghi cột D = `done` (chuẩn: kịch bản QC + giọng QC + prompt ảnh xong) + cột K trạng thái → **DỪNG**.
   KHÔNG tự `drive_handoff.py upload-job` lần đầu — chỉ khi anh nói "giao sang máy 2".
5. Khi anh bảo giao: job → `FlowHandoff_local\jobs\<slug>\`, ghi cột H đúng 1 ô 2 dòng
   `Xong nội dung - cần ảnh` + `E:\CLAUDE\YOUTUBE\FlowHandoff_local\jobs\<slug>\` (KHÔNG có `h2dev\`).
6. Bước 3 (ghép video) = agent khác theo `docs\QUY_TRINH_RENDER_VIDEO.md`; xong ghi cột I đường dẫn CHANEL,
   cột G thumbnail. Claude Code KHÔNG render.

## 5. LUẬT CỨNG RIÊNG LANE (handoff §3, đã trả giá thật ở kênh mẫu)
- Tựa PHẢI có nhân vật + tuổi + SỐ TIỀN cụ thể + cảm xúc; CẤM tựa chung chung / trùng tựa hit / thuế khô khan.
- Số liệu chế độ hưu trí phải có nguồn; nhân vật là hư cấu → không gắn họ tên người thật.
- Giọng nam trung niên tự nhiên, KHÔNG giọng bán hàng; QC nghe trước khi giao.
- KHÔNG nội dung nhạy cảm kiểu なるほど雑学 (đã loại).
- Lane F ≠ Lane G: F = nỗi sợ tiền mất; G = lối sống vui/rẻ. Đừng viết chéo.

## 6. CỘT SHEET TAB `teinengo-real` (A→K, giống Lane E §1b — H ghi 1 ô, path không `h2dev\`)
A STT (= số ep) · B NỘI DUNG · C FOLDER (chỉ điền khi thư mục tồn tại) · D KỊCH BẢN (`done` = kịch bản QC + giọng QC
+ prompt ảnh) · E TITLE-DESCRIPTION · F TAGS (KHÔNG dùng làm marker) · G THUMBNAIL · H STATUS-IMG (1 ô, 2 dòng) ·
I VIDEO (chỉ khi B11 giao xong) · J LIST · K GHI CHÚ (trạng thái từng cổng QC).
