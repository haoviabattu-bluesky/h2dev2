# BẮT ĐẦU LANE H — `kokoro-kazoku` · 心の家族学

> Anh nói **"thực hiện lane kokoro-kazoku"** (hoặc "LANE H") → tab này ĐỌC HẾT file này trước, mở đầu báo cáo bằng
> `@lane:kokoro-kazoku`, rồi làm ĐÚNG THỨ TỰ mục 4. Không tìm hiểu lại từ đầu, không đoán. File này là "cửa vào";
> chi tiết vận hành nằm ở SOP (mục 4 giai đoạn 2 sẽ viết). Cập nhật mục 2 mỗi khi trạng thái đổi.

## 1. ĐỊNH DANH (không đổi)
| Mục | Giá trị |
|---|---|
| Mã lane / profile id | `kokoro-kazoku` (= tên tab sheet = thư mục `assets/kokoro-kazoku/`) |
| Kênh thật | 心の家族学 · `@kokoro-kazokugaku` · `UClHVEGr-4pG0CDW_YUKJ26g` |
| Mail (GMAIL dòng 9) | `FuentesMitsy202@gmail.com` — profile GPMLogin cùng tên, anh login tay |
| Kênh mẫu (clone) | 癒しの心理学 `https://www.youtube.com/channel/UCV_8D2Agr2EaGxod0s7KBtg` |
| NOTE | dòng 5 (STT 4) — cột L đã ghi `@kokoro-kazokugaku` = kênh đã setup |
| Tab sheet sản xuất | **`kokoro-kazoku`** (header A→K, mục 6) |
| Thư mục làm việc | `E:\CLAUDE\YOUTUBE\h2dev\assets\kokoro-kazoku\` (branding đã có; tập = `ep<NN>-<slug>\`) |
| Giao hàng bước 3 | `E:\CLAUDE\YOUTUBE\CHANEL\kokoro-kazoku\ep<NN>-<slug>\` |
| Format | Illustration ấm áp (nhân vật đầu tròn, tông cam) + narration NAM trầm. Ngôi 2 giải thích tâm lý: nghịch lý → 'nhiều người nghĩ… nhưng tâm lý học nói khác' → cơ chế → 2 kiểu người → lời khuyên nhẹ → kết động viên. KHÔNG dạy đời, không đổ lỗi |
| Giọng | Nam trầm, điềm đạm, giải thích (không phải kể chuyện đời) — CHƯA CHỐT: hỏi anh clone kênh mẫu hay giọng kho |
| Khác lane nào | Illustration + giải thích ngôi 2 (giống Lane E về kỹ thuật ảnh không REF-LOCK; khác E ở nội dung tâm lý gia đình, không y khoa) |

## 2. TRẠNG THÁI (cập nhật mỗi lần đổi)
- ✅ 2026-09-13 nghiên cứu kênh (TRENDING-RESEARCH, anh duyệt danh sách NOTE).
- ✅ 2026-09-16 Channel Analyzer (K1+K2) đã chạy: 8 video, `✓ TỔNG` tại `results\channel_dna\iyashi-no-shinrigaku`.
- ✅ 2026-09-20 setup kênh A+B xong bằng `tools/channel_branding.py` (branding gpti2 + 6 mục settings, verify
  reload), sheet GMAIL/NOTE đã ghi, tab sheet + header đã tạo. Tên/handle/mô tả/hashtag do em đề xuất, anh duyệt nguyên.
- ❌ CHƯA: profile JSON · giọng · char-rate · SOP · danh sách tập · bất kỳ kịch bản nào. Anh mới duyệt SETUP KÊNH,
  chưa ra lệnh giai đoạn 2 — tab mở phiên mới phải HỎI trước khi bắt đầu mục 4.

## 3. TÀI LIỆU — đọc theo thứ tự này, đường dẫn thật trên máy 1
1. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\GIAO_VIEC_LANE_H.md` — tóm tắt việc + công thức thắng + hard rules.
2. Hồ sơ nghiên cứu: FlowHandoff_local\shared\laneH_iyashi\channel_analysis_癒しの心理学.json + report_iyashi.html (KHÔNG có LANE_H_HANDOFF.md 14 mục — hồ sơ ở dạng JSON/HTML).
3. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\channel_dna\iyashi-no-shinrigaku\` — `CHANNEL_DNA.md` + `VIDEO_ANALYSIS/*.json`
   (8 video) + `TAG_STATS.json` + `_raw/` (transcript). **Giai đoạn 2 phải copy sang `docs\channel_dna\iyashi-no-shinrigaku\`.**
4. `assets\kokoro-kazoku\branding\KENH.json` — tên/handle/mô tả/keywords/hashtag đã lên kênh (nguồn chân lý branding).
5. Khuôn để chép: lane gần nhất đã đi hết giai đoạn 2 — `docs\SOP_LANE_F.md` + `profiles\profiles\teinengo-real.json`
   (fiction_facts + structure_block + Fable viết/B3R) và `docs\SOP_LANE_G.md` + `teinengo-tanoshimi.json`; `SOP_LANE_E.md`
   cho lane không REF-LOCK.
6. Luật toàn dự án: `CLAUDE.md` (router + ⛔ Claude chỉ làm BƯỚC 1, không render, không tự upload-job lần đầu) ·
   `docs\QUY_TRINH_SETUP_KENH.md` (đã làm, chỉ đọc khi cần sửa kênh).

⚠️ Hook 20–30s bắt buộc trước S2 — xem `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b.

## 4. QUY TRÌNH — làm bước nào trước
### Giai đoạn 2 — dựng hạ tầng lane (1 LẦN, đúng thứ tự, xong mới sang giai đoạn 3)
1. **Copy DNA** `results\channel_dna\iyashi-no-shinrigaku\` → `docs\channel_dna\iyashi-no-shinrigaku\`.
2. **Profile** `profiles\profiles\kokoro-kazoku.json` (chép khuôn teinengo-real/teinengo-tanoshimi, sửa từng field):
   `id/slug_dir/competitor/channel_dossier/channel_dna_dir` · `narrator` theo Format mục 1 · fiction_facts: ví dụ gia đình hư cấu, nhưng khái niệm tâm lý học/nghiên cứu nêu tên PHẢI có thật và có nguồn ·
   script.structure = khối 'nghịch lý → cơ chế → 2 kiểu → lời khuyên' (khai qua structure_block như Lane F, KHÔNG list_countdown) · `body.mode=ai_images` · ref_lock=false (mỗi ví dụ 1 gia đình minh hoạ khác nhau, không host cố định — giống Lane E) · `image.style_suffix` theo Format ·
   `thumbnail` = illustration ấm, nhân vật đầu tròn, tông cam/nóng + chữ lớn; tiêu đề LUÔN có prefix 【心理学】 · `publish.sheet_tab="kokoro-kazoku"` · `script.brain_model` Fable như F/G nếu anh giữ chủ trương đó.
   **`script.gate` PHẢI ĐO** từ transcript thật trong `_raw/` (title_len, hook_chars, comma/breath) — không chép số lane khác.
3. **Giọng**: Nam trầm, điềm đạm, giải thích (không phải kể chuyện đời) — CHƯA CHỐT: hỏi anh clone kênh mẫu hay giọng kho. Nếu clone: tách 20–30s sạch từ 1 video kênh mẫu → `POST /voice-clone` (skill `openspeaker_voice_clone.md`)
   → nghe A/B → **HỎI ANH trước khi giữ voice_id** (giọng người thật). Ghi `voice.id`.
4. **Char-rate**: `py -3.13 pipeline\calibrate.py --profile kokoro-kazoku` (`calib_style` theo văn phong) → ghi `voice.char_rate`.
5. **SOP** `docs\SOP_LANE_H.md` theo khuôn `SOP_LANE_F.md`: §0 bảng delta, **§0b Channel Analyzer** (bắt buộc),
   §1 quyết định, §1b danh sách 10 tập + quy tắc cột sheet, §2 lệnh chạy, §3 gate, §5b phân vai.
6. **Router**: 1 dòng bảng lane `CLAUDE.md` (đã có sẵn dòng cửa vào, chỉ cập nhật cột SOP) + `docs\DANH_BA_LANE.md` + mục 2 file này.
7. **Danh sách 10 tập** vào tab `kokoro-kazoku` cột A/B (bám HIT của kênh mẫu, tránh trùng tựa hit). Tập 1 đề xuất: 「【心理学】親が"してあげたこと"より"してしまったこと"を子どもは覚えている」(biến thể chưa trùng hit 718k).

### Giai đoạn 3 — sản xuất 1 tập (CHỈ tập anh chỉ định "cho làm tập X")
1. Tạo `assets\kokoro-kazoku\ep<NN>-<slug>\`, ghi cột C.
2. Hồ sơ đề tài: `competitor.txt` (1 transcript thật cùng dạng qua `retrieve_videos.py --dna-dir docs\channel_dna\iyashi-no-shinrigaku
   --topic "..."`) + `series_ctx.txt` (dữ kiện CÓ NGUỒN — cấm bịa).
3. `py -3.13 -X utf8 pipeline\make_video.py --profile kokoro-kazoku --slug ep<NN>-<slug>` — chạy tới mốc anh cho phép (F/G hiện
   dừng ở kịch bản + QC `--den B3R`); đủ bước 1 = B3 + gate → B3Q/B3F/B3S → B4 giọng + B4Q → B5W/B5P prompt ảnh →
   master REF-LOCK (nếu có) → `TIEU_DE_MO_TA.txt` + `thumb_text.txt`.
4. Ghi cột D + K → **DỪNG**. KHÔNG tự `upload-job` lần đầu — chỉ khi anh nói "giao sang máy 2".
5. Anh bảo giao → job `FlowHandoff_local\jobs\<slug>\`, cột H 1 ô 2 dòng, path KHÔNG `h2dev\`.
6. Bước 3 = agent khác (`docs\QUY_TRINH_RENDER_VIDEO.md`); xong ghi cột I (CHANEL) + G. Claude Code KHÔNG render.

## 5. LUẬT CỨNG RIÊNG LANE
- Title LUÔN có prefix 【心理学】 (5/21 video kênh mẫu thiếu prefix chết 1–4k view).
- Chủ đề = NGHỊCH LÝ quan hệ cha mẹ 60-80 – con cái / vợ chồng sau hưu; cấm lời khuyên chung chung.
- KHÔNG dạy đời, không đổ lỗi; kết bằng lời khuyên NHẸ ('đừng ép con về phe mình — hãy đứng về phe con').
- Khái niệm/nghiên cứu tâm lý nêu tên phải có thật; QC giọng + số liệu trước render.
- Rủi ro: kênh mẫu mới 4 tháng, 1/21 transcript thật, like-rate thấp — đo gate từ DNA 8 video, đừng tin cảm giác.

## 6. CỘT SHEET TAB `kokoro-kazoku` (A→K, giống Lane E §1b)
A STT (= số ep) · B NỘI DUNG · C FOLDER · D KỊCH BẢN (`done` = kịch bản QC + giọng QC + prompt ảnh; mốc tạm F/G là
`script-qc-done`) · E TITLE-DESCRIPTION · F TAGS (không làm marker) · G THUMBNAIL · H STATUS-IMG (1 ô, 2 dòng, path không
`h2dev\`) · I VIDEO · J LIST · K GHI CHÚ.
