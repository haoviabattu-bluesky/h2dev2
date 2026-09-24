# BẮT ĐẦU LANE G — `teinengo-tanoshimi` · 定年後の楽しみ方 (hưu trí Nhật, manga list N選 vui/rẻ)

> Anh nói **"thực hiện lane teinengo-tanoshimi"** (hoặc "lane G") → tab này ĐỌC HẾT file này trước, mở đầu
> báo cáo bằng `@lane:teinengo-tanoshimi`, rồi làm ĐÚNG THỨ TỰ mục 4. Không tìm hiểu lại từ đầu, không đoán.
> File này là "cửa vào"; chi tiết vận hành nằm ở SOP (mục 4, giai đoạn 2 sẽ viết). Cập nhật mục 2 khi trạng thái đổi.

## 1. ĐỊNH DANH (không đổi)
| Mục | Giá trị |
|---|---|
| Mã lane / profile id | `teinengo-tanoshimi` (thư mục `assets/teinengo-tanoshimi/`; tab sheet = **`G-teinengo-tanoshimi`** từ 24/09) |
| Kênh thật | 定年後の楽しみ方 · `@teinengo-tanoshimi` · `UClETn8eAXgRRKM4PkYEKzvA` |
| Mail (GMAIL dòng 8) | `cobbytheona159@gmail.com` — profile GPMLogin cùng tên, anh login tay |
| Kênh mẫu (clone) | 老後のお金ストーリー `https://www.youtube.com/channel/UCI2cPqBmCPMxxKI4u2Gqs_Q` |
| NOTE | dòng 4 (STT 3) — cột L đã ghi `@teinengo-tanoshimi` = kênh đã setup |
| Tab sheet sản xuất | **`teinengo-tanoshimi`** (header A→K, mục 6) |
| Thư mục làm việc | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\` (branding đã có; tập = `ep<NN>-<slug>\`) |
| Giao hàng bước 3 | `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-tanoshimi\ep<NN>-<slug>\` |
| Format | Manga AI ngôi 1 + **list N選 (5/7 mục, 1つ目…Nつ目)**, nhân vật 55–66 tuổi khám phá cách sống VUI/RẺ, thoại 2 nhân vật, khép lại cảnh đầu, CTA giữa video |
| Giọng | Nam trung niên kể chuyện tự nhiên — anh chốt 2026-09-20: **CLONE RIÊNG** từ kênh mẫu 老後のお金ストーリー (KHÔNG dùng chung voice_id với Lane F; chưa làm, mục 4) |

## 2. TRẠNG THÁI (cập nhật mỗi lần đổi)
- ✅ 2026-09-13 nghiên cứu kênh xong (TRENDING-RESEARCH, anh duyệt).
- ✅ 2026-09-16 Channel Analyzer (K1+K2) đã chạy: `✓ TỔNG` tại `results\channel_dna\rougo-money-story`.
- ✅ 2026-09-20 setup kênh A+B xong (branding gpti2 + 6 mục settings, verify reload), tab sheet + header đã tạo.
- ✅ 2026-09-20 Giai đoạn 2 (phần không cần giọng): DNA đã copy `docs\channel_dna\rougo-money-story\` · profile
  `profiles\profiles\teinengo-tanoshimi.json` (gate ĐO từ 8 transcript thật) · nhánh code mới `manga_list`
  (`ai_steps._cau_truc_block`) + `gate.hook_marker` (`qc_script.mo_dau`) · SOP `docs\SOP_LANE_G.md` · router.
- ✅ 2026-09-20 K4: 4 video kênh mẫu CÙNG 1 giọng nam (F0 105–118Hz) → clone 1 lần `voice_id 2658912`
  (mẫu bgUqNHYZbq0 0:52–1:20, F0 output 116,8Hz khớp). ✅ anh duyệt → `voice.id=clone_2658912`, char-rate **323,7**.
- ✅ 2026-09-20 10 tập đã ghi tab sheet A2:B11 (+K). ⭐ **PHẠM VI HIỆN TẠI: CHỈ KỊCH BẢN** (`--den B3G`; viết + nghiệm thu cuối = **Fable 5.1**, chốt 2026-09-20). ✅ Tập 1 `ep01-asa-shukan` LOCK PASS 15:28 (luồng lean, Sol plain có sàn, sha 59d3f6bfc0), cột D `Done` (3 lớp tự duyệt: máy · Sol · Claude Code đọc bản lock — KHÔNG đẩy lên anh). **Lane chạy `flow=lean`** — SOP §1c khung đầu + `docs/QUY_TRINH_KICH_BAN_GON.md`. ✅ Tập 2 `ep02-1000yen-shumi` LOCK PASS 16:12 (sha 84beda216e, S2 viết đúng ngân sách +1,6%), cột D `Done` (anh chốt 20/09: chỉ ghi `Done`). ✅ **ep03–ep10 xong 20/09 tối — 10/10 tập LOCK PASS, D2:D11 = `Done`** (SOP §1f) — xem
  `SOP_LANE_G.md` §1c. Chưa: giọng/prompt ảnh/REF-LOCK/tiêu đề/thumbnail/ảnh/video (chờ anh mở) · soi thumbnail thật kênh mẫu.

## 3. TÀI LIỆU — đọc theo thứ tự này, đường dẫn thật trên máy 1
1. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneG_from_research\LANE_G_HANDOFF.md` — 14 mục:
   HIT/MISS §3, title formula §4, hook §5, cấu trúc §6, tên/mô tả/hashtag/tag §12, đề tài tập 1 §13, rủi ro §14.
   Kèm `channel_analysis_老後のお金ストーリー.json` + `data/` (3 transcript thật).
2. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\channel_dna\rougo-money-story\` — `CHANNEL_DNA.md` +
   `VIDEO_ANALYSIS/*.json` + `TAG_STATS.json`. **Giai đoạn 2 phải copy sang `docs\channel_dna\rougo-money-story\`.**
3. `FlowHandoff_local\shared\GIAO_VIEC_LANE_G.md` — tóm tắt việc + hard rules.
4. `FlowHandoff_local\shared\IDEA_GORO_LaneFG.md` — kho ý tưởng phụ (kênh 老後のごろ, NOTE STT 4) dùng chung F/G.
5. `assets\teinengo-tanoshimi\branding\KENH.json` — branding đã lên kênh (nguồn chân lý).
6. Khuôn để chép: `docs\SOP_LANE_E.md` + `profiles\profiles\kenko-chiebukuro.json` — **gần nhất** vì cùng
   cấu trúc list đếm (`script.structure="list_countdown"` đã có nhánh code trong `pipeline/ai_steps.py`).
7. Luật toàn dự án: `CLAUDE.md` (router + ⛔ Claude chỉ làm BƯỚC 1) · `docs\QUY_TRINH_SETUP_KENH.md`.

⚠️ Hook 20–30s bắt buộc trước S2 — xem `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b.

## 4. QUY TRÌNH — làm bước nào trước
### Giai đoạn 2 — dựng hạ tầng lane (1 LẦN, đúng thứ tự)
1. **Copy DNA** `results\channel_dna\rougo-money-story\` → `docs\channel_dna\rougo-money-story\`.
2. **Profile** `profiles\profiles\teinengo-tanoshimi.json` (khuôn kenko-chiebukuro): `narrator` = nam 55–66 ngôi 1,
   kể chuyện có thoại · `script.structure="list_countdown"` + `gate.list_item_count` 5 (hoặc 7 theo tập) ·
   `script.mode` fiction có ràng buộc dữ kiện thật (địa điểm/chi phí/thông tin Nhật phải có nguồn) ·
   `target_minutes` 18–25 · `body.mode=ai_images` · `image.ref_lock=true` cho NHÂN VẬT CHÍNH trong 1 tập (khác Lane E
   không REF-LOCK — ở đây 1 người dẫn xuyên suốt tập; không xuyên tập) · `image.style_suffix` manga tươi sáng ·
   `thumbnail` manga + nhân vật nam trung niên + chữ lớn (handoff §3.8) · `publish.sheet_tab="G-teinengo-tanoshimi"`.
   **`script.gate` PHẢI ĐO** từ 3 transcript thật trong `data/` — không chép số Lane E/F.
3. **Giọng CLONE RIÊNG** (anh chốt): tách 20–30s giọng sạch từ 1 video kênh mẫu 老後のお金ストーリー (bỏ intro, chọn
   đoạn kể không nhạc) → `POST /voice-clone` theo skill `openspeaker_voice_clone.md` → nghe thử A/B → **HỎI ANH trước
   khi giữ voice_id** (giọng người thật) → ghi `voice.id=clone_<id>` vào profile. Không dùng lại voice_id của Lane F.
4. **Char-rate**: `py -3.13 pipeline\calibrate.py --profile teinengo-tanoshimi` (`calib_style=story`).
5. **SOP** `docs\SOP_LANE_G.md` theo khuôn `SOP_LANE_E.md`, bắt buộc §0b Channel Analyzer, §1b danh sách tập + cột sheet.
6. **Router**: 1 dòng bảng lane `CLAUDE.md` + 1 dòng `docs\DANH_BA_LANE.md` + cập nhật mục 2 file này.
7. **Danh sách 10 tập** vào tab `teinengo-tanoshimi` cột A/B: mỗi tập = 1 list N選 CỤ THỂ (hành động/địa điểm + lợi ích),
   dàn đều trụ cột (trẻ khoẻ / du lịch-温泉-神社 / thú vui 0đ / phục hồi mệt / lối sống vừa đủ), CẤM đề tài trừu tượng
   (年金受給/人生/育ち — chết 986v–3k ở kênh mẫu). Tập 1 đã đề xuất §13:
   「【漫画】60代から始める「朝の習慣」5選…1年後、体と気持ちが驚くほど軽くなる理由」.

### Giai đoạn 3 — sản xuất 1 tập (CHỈ tập anh chỉ định)
1. Tạo `assets\teinengo-tanoshimi\ep<NN>-<slug>\`, ghi cột C.
2. Hồ sơ đề tài: `competitor.txt` (1 transcript thật cùng dạng N選 qua `retrieve_videos.py --dna-dir
   docs\channel_dna\rougo-money-story --topic "..."`) + `series_ctx.txt` (địa điểm/chi phí/thông tin thật CÓ NGUỒN).
3. `py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-tanoshimi --slug ep<NN>-<slug>` — chạy tới HẾT bước 1
   (B3 + gate → B3Q/B3F → B4 giọng + B4Q → B5W/B5P prompt ảnh → master REF-LOCK nhân vật chính →
   `TIEU_DE_MO_TA.txt` + `thumb_text.txt`). Nhớ chèn **comment CTA giữa video** (hard rule §3.6).
4. Cột D = `done` + cột K → **DỪNG**. Không tự upload-job lần đầu.
5. Anh bảo giao → job `FlowHandoff_local\jobs\<slug>\`, cột H 1 ô 2 dòng, path KHÔNG `h2dev\`.
6. Bước 3 = agent khác (`docs\QUY_TRINH_RENDER_VIDEO.md`); xong ghi cột I (CHANEL) + G. Claude Code KHÔNG render.

## 5. LUẬT CỨNG RIÊNG LANE (handoff §3)
- Chủ đề CỤ THỂ: N選 + hành động/địa điểm + lợi ích rõ; cấm trừu tượng.
- GIỮ HƯỚNG VUI/RẺ — không kịch tính tiền mất (đó là Lane F).
- Số liệu/địa điểm có nguồn; QC giọng trước render; giọng nam trung niên tự nhiên có thoại.
- Thêm CTA comment giữa video (kênh mẫu like-rate thấp).
- Title: 【漫画】{trạng thái}…{N}選…{lợi ích cụ thể}. Thumbnail: manga + nam trung niên + chữ lớn.

## 6. CỘT SHEET TAB `teinengo-tanoshimi` (A→K, giống Lane E §1b)
A STT (= số ep) · B NỘI DUNG · C FOLDER · D KỊCH BẢN (`done` = kịch bản QC + giọng QC + prompt ảnh) · E TITLE-DESCRIPTION ·
F TAGS (không làm marker) · G THUMBNAIL · H STATUS-IMG (1 ô, 2 dòng, path không `h2dev\`) · I VIDEO · J LIST · K GHI CHÚ.
