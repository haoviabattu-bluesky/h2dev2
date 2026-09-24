# BẮT ĐẦU LANE J — `teinengo-fuufu` · 定年後の夫婦のカタチ

> Anh nói **"thực hiện lane teinengo-fuufu"** (hoặc "LANE J") → tab này ĐỌC HẾT file này trước, mở đầu báo cáo bằng
> `@lane:teinengo-fuufu`, rồi làm ĐÚNG THỨ TỰ mục 4. Không tìm hiểu lại từ đầu, không đoán. File này là "cửa vào";
> chi tiết vận hành nằm ở SOP (mục 4 giai đoạn 2 sẽ viết). Cập nhật mục 2 mỗi khi trạng thái đổi.

## 1. ĐỊNH DANH (không đổi)
| Mục | Giá trị |
|---|---|
| Mã lane / profile id | `teinengo-fuufu` (thư mục `assets/teinengo-fuufu/`; tab sheet hiện `teinengo-fuufu`, theo quy ước 24/09 sẽ là `J-teinengo-fuufu`) |
| Kênh thật | 定年後の夫婦のカタチ · `@teinengo-fuufu` · `UC6IkfxpGTksDdzG3ENYbVdg` |
| Mail (GMAIL dòng 11) | `MinyardJuan231@gmail.com` — profile GPMLogin cùng tên, anh login tay |
| Kênh mẫu (clone) | 老後のゴローさん `https://www.youtube.com/channel/UCxD2Exs2Q4lf7x0Q28OuKvg` |
| NOTE | dòng 7 (STT 6) — cột L đã ghi `@teinengo-fuufu` = kênh đã setup |
| Tab sheet sản xuất | **`teinengo-fuufu`** (header A→K, mục 6) |
| Thư mục làm việc | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-fuufu\` (branding đã có; tập = `ep<NN>-<slug>\`) |
| Giao hàng bước 3 | `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-fuufu\ep<NN>-<slug>\` |
| Format | Manga story ngôi 1 「俺」/vợ, CẶP VỢ CHỒNG 60–70 đối mặt 1 quyết định lớn sau hưu (熟年離婚 vs 家庭内別居, du thuyền bằng 退職金, 田舎移住, giấu tiền vợ…) → hậu quả 5 năm sau → cảm xúc vợ chồng cụ thể → bài học không dạy đời |
| Giọng | Nam trung niên hồi ức (kênh mẫu 871k dùng giọng nam) — CHƯA CHỐT: hỏi anh clone kênh mẫu hay giọng kho; KHÔNG dùng chung voice_id với F/G |
| Khác lane nào | Anh em với F (cùng manga ngôi 1, 2 nhân vật) nhưng trục là vợ chồng; nguồn nghiên cứu mỏng hơn F/G |

## 2. TRẠNG THÁI (cập nhật mỗi lần đổi)
- ✅ 2026-09-13 nghiên cứu kênh (TRENDING-RESEARCH, anh duyệt danh sách NOTE).
- ✅ 2026-09-16 Channel Analyzer (K1+K2) đã chạy: 8 video, `✓ TỔNG` tại `results\channel_dna\rougo-no-goro`.
- ✅ 2026-09-20 setup kênh A+B xong bằng `tools/channel_branding.py` (branding gpti2 + 6 mục settings, verify
  reload), sheet GMAIL/NOTE đã ghi, tab sheet + header đã tạo. Tên/handle/mô tả/hashtag do em đề xuất, anh duyệt nguyên.
- ❌ CHƯA: profile JSON · giọng · char-rate · SOP · danh sách tập · bất kỳ kịch bản nào. Anh mới duyệt SETUP KÊNH,
  chưa ra lệnh giai đoạn 2 — tab mở phiên mới phải HỎI trước khi bắt đầu mục 4.

## 3. TÀI LIỆU — đọc theo thứ tự này, đường dẫn thật trên máy 1
1. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\(không có)` — tóm tắt việc + công thức thắng + hard rules.
2. Hồ sơ nghiên cứu: KHÔNG có handoff/GIAO_VIEC riêng — chỉ `FlowHandoff_local\shared\IDEA_GORO_LaneFG.md` (kho 12 topic hit + công thức, vốn viết cho F/G) + DNA 8 video. Nếu cần hồ sơ 14 mục thì xin TRENDING-RESEARCH (anh chưa yêu cầu).
3. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\channel_dna\rougo-no-goro\` — `CHANNEL_DNA.md` + `VIDEO_ANALYSIS/*.json`
   (8 video) + `TAG_STATS.json` + `_raw/` (transcript). **Giai đoạn 2 phải copy sang `docs\channel_dna\rougo-no-goro\`.**
4. `assets\teinengo-fuufu\branding\KENH.json` — tên/handle/mô tả/keywords/hashtag đã lên kênh (nguồn chân lý branding).
5. Khuôn để chép: lane gần nhất đã đi hết giai đoạn 2 — `docs\SOP_LANE_F.md` + `profiles\profiles\teinengo-real.json`
   (fiction_facts + structure_block + Fable viết/B3R) và `docs\SOP_LANE_G.md` + `teinengo-tanoshimi.json`; `SOP_LANE_E.md`
   cho lane không REF-LOCK.
6. Luật toàn dự án: `CLAUDE.md` (router + ⛔ Claude chỉ làm BƯỚC 1, không render, không tự upload-job lần đầu) ·
   `docs\QUY_TRINH_SETUP_KENH.md` (đã làm, chỉ đọc khi cần sửa kênh).

⚠️ Hook 20–30s bắt buộc trước S2 — xem `docs/QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2b.

## 4. QUY TRÌNH — làm bước nào trước
### Giai đoạn 2 — dựng hạ tầng lane (1 LẦN, đúng thứ tự, xong mới sang giai đoạn 3)
1. **Copy DNA** `results\channel_dna\rougo-no-goro\` → `docs\channel_dna\rougo-no-goro\`.
2. **Profile** `profiles\profiles\teinengo-fuufu.json` (chép khuôn teinengo-real/teinengo-tanoshimi, sửa từng field):
   `id/slug_dir/competitor/channel_dossier/channel_dna_dir` · `narrator` theo Format mục 1 · fiction_facts: nhân vật hư cấu; số tiền/chế độ/giá (du thuyền, 修繕費, lương hưu) phải có nguồn thật ·
   script.structure = 7 chặng như Lane F nhưng trục là QUAN HỆ VỢ CHỒNG (không phải tiền mất): hook cảnh kịch tính → 2 vợ chồng tên/tuổi/nghề → quyết định → hậu quả → ngoặt → bài học · `body.mode=ai_images` · ref_lock=true 2 nhân vật (chồng @REF + vợ @REF2) trong 1 tập; không xuyên tập · `image.style_suffix` theo Format ·
   `thumbnail` = manga cặp vợ chồng 60 tuổi, tông ấm có khoảng cách, chữ vàng/đỏ lớn (khác F kịch tính tối, khác G vui sáng) · `publish.sheet_tab=<tên tab thật, quy ước J-teinengo-fuufu>` · `script.brain_model` Fable như F/G nếu anh giữ chủ trương đó.
   **`script.gate` PHẢI ĐO** từ transcript thật trong `_raw/` (title_len, hook_chars, comma/breath) — không chép số lane khác.
3. **Giọng**: Nam trung niên hồi ức (kênh mẫu 871k dùng giọng nam) — CHƯA CHỐT: hỏi anh clone kênh mẫu hay giọng kho; KHÔNG dùng chung voice_id với F/G. Nếu clone: tách 20–30s sạch từ 1 video kênh mẫu → `POST /voice-clone` (skill `openspeaker_voice_clone.md`)
   → nghe A/B → **HỎI ANH trước khi giữ voice_id** (giọng người thật). Ghi `voice.id`.
4. **Char-rate**: `py -3.13 pipeline\calibrate.py --profile teinengo-fuufu` (`calib_style` theo văn phong) → ghi `voice.char_rate`.
5. **SOP** `docs\SOP_LANE_J.md` theo khuôn `SOP_LANE_F.md`: §0 bảng delta, **§0b Channel Analyzer** (bắt buộc),
   §1 quyết định, §1b danh sách 10 tập + quy tắc cột sheet, §2 lệnh chạy, §3 gate, §5b phân vai.
6. **Router**: 1 dòng bảng lane `CLAUDE.md` (đã có sẵn dòng cửa vào, chỉ cập nhật cột SOP) + `docs\DANH_BA_LANE.md` + mục 2 file này.
7. **Danh sách 10 tập** vào tab `teinengo-fuufu` cột A/B (bám HIT của kênh mẫu, tránh trùng tựa hit). Tập 1 đề xuất: 「【漫画】60代夫婦の熟年離婚 VS 家庭内別居…5年後、どっちが幸せだったのか？」(IDEA_GORO #5, 810k ở kênh mẫu, chưa lane nào làm — đổi nhân vật/chi tiết để không trùng tựa).

### Giai đoạn 3 — sản xuất 1 tập (CHỈ tập anh chỉ định "cho làm tập X")
1. Tạo `assets\teinengo-fuufu\ep<NN>-<slug>\`, ghi cột C.
2. Hồ sơ đề tài: `competitor.txt` (1 transcript thật cùng dạng qua `retrieve_videos.py --dna-dir docs\channel_dna\rougo-no-goro
   --topic "..."`) + `series_ctx.txt` (dữ kiện CÓ NGUỒN — cấm bịa).
3. `py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-fuufu --slug ep<NN>-<slug>` — chạy tới mốc anh cho phép (F/G hiện
   dừng ở kịch bản + QC `--den B3R`); đủ bước 1 = B3 + gate → B3Q/B3F/B3S → B4 giọng + B4Q → B5W/B5P prompt ảnh →
   master REF-LOCK (nếu có) → `TIEU_DE_MO_TA.txt` + `thumb_text.txt`.
4. Ghi cột D + K → **DỪNG**. KHÔNG tự `upload-job` lần đầu — chỉ khi anh nói "giao sang máy 2".
5. Anh bảo giao → job `FlowHandoff_local\jobs\<slug>\`, cột H 1 ô 2 dòng, path KHÔNG `h2dev\`.
6. Bước 3 = agent khác (`docs\QUY_TRINH_RENDER_VIDEO.md`); xong ghi cột I (CHANEL) + G. Claude Code KHÔNG render.

## 5. LUẬT CỨNG RIÊNG LANE
- Trục cảm xúc VỢ CHỒNG là chính — F là tiền, G là vui/rẻ; J không được lặp 2 lane đó.
- Tựa theo IDEA_GORO §1: 【漫画】{2 lựa chọn hưu trí}…{5年後}…とは？ — hook giây đầu phải kịch tính ngay, không giới thiệu dài.
- Topic vàng chưa lane nào làm: 熟年離婚 VS 家庭内別居 どっちが幸せ (810k) — ưu tiên tập đầu.
- Số liệu thật có nguồn; QC giọng trước render.
- Hồ sơ nghiên cứu MỎNG (không handoff 14 mục) → gate PHẢI đo từ 8 VIDEO_ANALYSIS + transcript `_raw`, không suy từ F/G.

## 6. CỘT SHEET TAB `teinengo-fuufu` (A→K, giống Lane E §1b)
A STT (= số ep) · B NỘI DUNG · C FOLDER · D KỊCH BẢN (`done` = kịch bản QC + giọng QC + prompt ảnh; mốc tạm F/G là
`script-qc-done`) · E TITLE-DESCRIPTION · F TAGS (không làm marker) · G THUMBNAIL · H STATUS-IMG (1 ô, 2 dòng, path không
`h2dev\`) · I VIDEO · J LIST · K GHI CHÚ.
