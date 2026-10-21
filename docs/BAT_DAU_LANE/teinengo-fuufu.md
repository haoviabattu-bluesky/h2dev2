# BẮT ĐẦU LANE J — `teinengo-fuufu` · 定年後の夫婦のカタチ

> Anh nói **"thực hiện lane teinengo-fuufu"** (hoặc "LANE J") → tab này ĐỌC HẾT file này trước, mở đầu báo cáo bằng
> `@lane:teinengo-fuufu`, rồi làm ĐÚNG THỨ TỰ mục 4. Không tìm hiểu lại từ đầu, không đoán. File này là "cửa vào";
> chi tiết vận hành nằm ở SOP (mục 4 giai đoạn 2 sẽ viết). Cập nhật mục 2 mỗi khi trạng thái đổi.

## ⚡ ĐỌC NHANH — "làm tập tiếp theo" (lane đã setup xong, mục 2 TRẠNG THÁI đã ✅ hạ tầng)
> 📌 **LÀM TẬP MỚI (tập 2 trở đi) → đọc ĐÚNG `E:\CLAUDE\YOUTUBE\h2dev\assets\J-teinengo-fuufu\HUONG_DAN_LAM_TAP.md`**
> (quy trình đã chạy trọn tập 1 ngày 30/09 + mọi bẫy gặp phải). Tập 1 đã giao máy 2 (D2=Done).
> 📌 01/10: tập 2 `ep02-sotsukon` đã giao máy 2 (nhạc nền hook = piano, anh duyệt). **Tập 3 → đọc `E:\CLAUDE\YOUTUBE\h2dev\assets\J-teinengo-fuufu\TAB_MOI_EP03.md`** (5 bài học tập 2: hook dài, ghi_chu_canh, cấm SFX, piano).
> ⭐ **2026-09-30 anh chốt — THẮNG mọi chỉ dẫn soát ChatGPT web bên dưới:** hook = Fable 5.1 viết 2 phương án theo luật hook 21/10 (bám sát cấu trúc hook video gốc: `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`);
> `make_video --den B3G` khoá xong là DỪNG, tự giao máy 3/anh soát (D=`Chờ kiểm tra kịch bản`). Anh sửa xong (D=`Đã sửa kịch bản`) →
> đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` để nhận + làm hook/ảnh/giao máy 2.

CHỈ cần đọc: mục 4 **Giai đoạn 3** (lệnh chạy đúng thứ tự) + đúng file mục 4 tự trỏ tới (thường chỉ
`COMMENT_INSIGHT.md`). KHÔNG cần mở lại toàn bộ mục 3 TÀI LIỆU, SOP đầy đủ, `CHANNEL_DNA.md`,
`profile.json` — các file đó là cho **Giai đoạn 2 (setup 1 LẦN)** hoặc được chính `pipeline\*.py` tự
đọc khi chạy lệnh, không phải để Claude nạp vào context mỗi tập. Chỉ mở thêm khi lệnh báo lỗi cần
quyết định thủ công (thiếu context, xung đột dữ liệu...).

## 1. ĐỊNH DANH (không đổi)
| Mục | Giá trị |
|---|---|
| Mã lane / profile id | `teinengo-fuufu` (thư mục `assets/J-teinengo-fuufu/`; tab sheet `Lane-J` (anh tạo 30/09)) |
| Kênh thật | **03/10/2026 KÊNH MỚI: 老後の知恵袋 · `@rougo_chie60` · `UCvLpzQtsS8gFAlthT-8YVlQ`** (mail `lethientan26061994@gmail.com`, AdsPower `k15n8xbk`; setup: `E:\CLAUDE\YOUTUBE\h2dev\assets\J-teinengo-fuufu\branding\rougo_chie60\KENH.json` + `E:\CLAUDE\YOUTUBE\h2dev\tools\channel_branding_ads.py`). Cũ: 定年後の夫婦のカタチ `UC6IkfxpGTksDdzG3ENYbVdg` |
| Mail | **2026-09-30: NOTE dòng 7 ghi `wunehasneha@gmail.com`** (kênh làm lại, tên mới **J-rougo_futari**, anh TỰ setup). Bản cũ: `MinyardJuan231@gmail.com` (GMAIL dòng 11) |
| Kênh mẫu (clone) | 老後のゴローさん `https://www.youtube.com/channel/UCxD2Exs2Q4lf7x0Q28OuKvg` |
| NOTE | dòng 7 (STT 6) — 2026-09-30 cột I (HANDLE) + L (KÊNH) TRỐNG: kênh mới chưa setup xong, anh làm tay |
| Tab sheet sản xuất | **`Lane-J`** (anh tạo 30/09; 10 tập A2:B11, ghi chú K, K2 = hướng dẫn chạy tập 1, link video gốc cột T). Tab `teinengo-fuufu` cũ bỏ. Đổi tên tab cùng lúc với mã lane |
| Thư mục làm việc | `E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-fuufu\` (branding đã có; tập = `ep<NN>-<slug>\`) |
| Giao hàng bước 3 | `E:\CLAUDE\YOUTUBE\CHANEL\teinengo-fuufu\ep<NN>-<slug>\` |
| Format | Manga story ngôi 1 「俺」/vợ, CẶP VỢ CHỒNG 60–70 đối mặt 1 quyết định lớn sau hưu (熟年離婚 vs 家庭内別居, du thuyền bằng 退職金, 田舎移住, giấu tiền vợ…) → hậu quả 5 năm sau → cảm xúc vợ chồng cụ thể → bài học không dạy đời |
| Giọng | Nam trung niên hồi ức (kênh mẫu 871k dùng giọng nam) — CHƯA CHỐT: hỏi anh clone kênh mẫu hay giọng kho; KHÔNG dùng chung voice_id với F/G |
| Khác lane nào | Anh em với F (cùng manga ngôi 1, 2 nhân vật) nhưng trục là vợ chồng; nguồn nghiên cứu mỏng hơn F/G |

## 2. TRẠNG THÁI (cập nhật mỗi lần đổi)
- ✅ 2026-09-13 nghiên cứu kênh (TRENDING-RESEARCH, anh duyệt danh sách NOTE).
- ✅ 2026-09-16 Channel Analyzer (K1+K2) đã chạy: 8 video, `✓ TỔNG` tại `results\channel_dna
ougo-no-goro`.
- ✅ 2026-09-20 setup kênh A+B xong bằng `tools/channel_branding.py` (branding gpti2 + 6 mục settings, verify
  reload), sheet GMAIL/NOTE đã ghi, tab sheet + header đã tạo. Tên/handle/mô tả/hashtag do em đề xuất, anh duyệt nguyên.
- ✅ **2026-09-28 NÂNG HỒ SƠ NGHIÊN CỨU: 8 video → 47/47 video (100% kênh).** Anh yêu cầu "bằng mọi giá phải clone được".
  Kết luận cũ "KHÔNG THỂ CLONE" **đã bị bác bỏ bằng số liệu** — xem mục 2b. Đã có:
  `docs\nghien_cuu_lane_ban_da_kiem\channel_analysis_golo__teinengo-fuufu.json` (schema h2dev 22 khoá) ·
  `docs\lane_inbox\teinengo-fuufu.md` (hộp thư + bằng chứng phản biện) ·
  `scratch_golo\CHANNEL_DNA_GOLO.md` (DNA **11 mục** đầy đủ) ·
  `scratch_golo\ORDER_15_VIDEO_UU_TIEN.md` (**15 video xếp thứ tự ưu tiên** + 3 nhóm A/B/C) ·
  `scratch_golo\VIDEO_ANALYSIS_GOLO\*.json` (15 hồ sơ video) ·
  `data\title_intel\teinengo-fuufu.json` (đã nâng `source` lên `channel_report_full`, `our_eps` 15 mục).
- ✅ **2026-09-30 GIAI ĐOẠN 2 (anh ra lệnh; máy 1 CHỈ làm nội dung, setup kênh anh làm tay, mã lane đổi sau):**
  hồ sơ phân tích bổ sung 4 video top 10 (`gpVr3OYPA-E` · `bZp51t9b-_g` · `Nu-1bKzC6tY` · `Hgo2qFDF0bM`) ·
  DNA copy sang `docs\channel_dna\rougo-no-goro\` (+7 transcript, VIDEO_ANALYSIS 10 video top, `COMMENT_INSIGHT.md`) ·
  profile `profiles\profiles\teinengo-fuufu.json` (mẫu Lane M, gate ĐO từ 15 transcript) · SOP `docs\SOP_LANE_J.md` ·
  10 tập vào tab `Lane-J` (xếp theo view video gốc). **Giai đoạn 3 chạy theo `SOP_LANE_J.md` §2**, thư mục `assets\J-teinengo-fuufu\`.
- ❌ CÒN CHẶN tập 1: giọng + char_rate (SOP_LANE_J §0c) · 2 Project ChatGPT soát (§4). Chưa đo khung hình/chữ kênh mẫu (§7).
- (cũ, hết hiệu lực) ❌ CHƯA: profile JSON · giọng · char-rate · SOP · danh sách tập · bất kỳ kịch bản nào. Anh mới duyệt SETUP KÊNH,
  chưa ra lệnh giai đoạn 2 — tab mở phiên mới phải HỎI trước khi bắt đầu mục 4.

## 2b. ⛔ KẾT LUẬN "KHÔNG THỂ CLONE" LÀ SAI — BẰNG CHỨNG

> Lý do cũ: *"trend 0,42 < 0,6; ch_mult 2,65 < 3,0; median lệch Mean 4×; top3 chiếm 43,8%"*. Cả 4 đều sai hoặc vô nghĩa.

| Chỉ số cũ | Số thật (tái lập 28/09) | Phán quyết |
|---|---|---|
| `ch_mult` **2,65 < 3,0** ❌ | `ch_mult = median_view ÷ subs = 28.881 ÷ 10.900 = **2,65**`. Ngưỡng **đúng cho lane là 2,0** (`src/find_lane_similar.py:71 CH_MULT_MIN = 2.0`), không phải 3,0 (3,0 là `CONSISTENT` của `explore_niches.py` — ngưỡng cho **luồng khám phá ngách mới**, không phải thẩm định lane đã chọn) | ✅ **ĐẠT** |
| `trend` **0,42 < 0,6** ❌ | **Không tái lập được.** Theo định nghĩa h2dev (`median_recent_longform_views ÷ baseline`, `channel_analysis_rougo-no-kurashi`): trend **= 0,85** (≤90 ngày, n=28). Theo VPD cùng cửa sổ ≤90 ngày: **+1,11** (n=28); còn ≤30 ngày thì **+3,75** (n=13) | ✅ **ĐẠT** |
| `median lệch Mean 4×` ❌ | mean/median = **4,05×**. Với kênh ngách 60+ dạng "1 video nổ + đuôi dài", **2–5× là BÌNH THƯỜNG**. Đây là dấu hiệu **có video đột biến = bài học copy được**, không phải lỗi | ✅ **BÌNH THƯỜNG** |
| `top3 chiếm 43,8%` ❌ | top3 = **43,8%** tổng view. Kênh có **công thức lặp lại** thì phân bố lệch là điều kiện để **nhân bản**, không phải để loại | ✅ **BÌNH THƯỜNG** |

**Bằng chứng bổ sung cho "clone được":**
- Cấu trúc **6 giai đoạn** giống nhau ở **47/47 video**.
- `【漫画】` **47/47 (100%)** — định dạng tuyệt đối đồng nhất.
- **4 nguyên nhân nổ/tụt đo được trên 46 hook** (3,18× / 2,09× / 13,5× / 3,7×) → **công thức kiểm soát được, không phải ăn may**.
- **1 narrator, 1 định dạng ảnh** (100% AI sinh manga anime) xuyên **7 tháng** → quy trình ổn định.
- `hit_rate` = 31,9% (15/47 video ≥100k) — **cao hơn nhiều** kênh ngách cùng tuổi.

**→ KA: clone được. Không còn lý do kỹ thuật nào để hoãn giai đoạn 2.**

## 3. TÀI LIỆU — đọc theo thứ tự này, đường dẫn thật trên máy 1
1. **⭐ MỚI 28/09 — đọc TRƯỚC TIÊN:** `docs\nghien_cuu_lane_ban_da_kiem\channel_analysis_golo__teinengo-fuufu.json`
   (schema h2dev, 47 video, có `channel_dna` 7 khoá + `winning_formula` + `anti_patterns` + `root_cause_4`).
2. `scratch_golo\CHANNEL_DNA_GOLO.md` — **DNA 11 mục** (audience / 6 content pillars / narrative / hook / story /
   pacing / emotional / CTA / title / thumbnail / **11 luật sản xuất**). Dựng từ 47/47 video, KHÔNG phải mẫu 8 video.
3. `scratch_golo\ORDER_15_VIDEO_UU_TIEN.md` — **15 video xếp thứ tự ưu tiên** (đa chiều: rel_VPD + rel_ENG +
   tuổi video + 4 tiêu chí hook; ❌ KHÔNG dùng view thuần) + 3 nhóm A/B/C + 3 video mẫu vàng.
4. `scratch_golo\VIDEO_ANALYSIS_GOLO\*.json` — 15 hồ sơ video schema h2dev (`topics`/`hook_type`/`structure`/
   `emotional_beats`/`title_formula`/`notes`) + `hook_45s` nguyên văn.
5. `data\title_intel\teinengo-fuufu.json` — **đã nâng 10 → 47 video**, `source=channel_report_full`,
   `our_eps` **15 mục đã điền** (trước RỖNG), + `root_cause_4` + `tu_khoa_an_view` + `khoang_trong`.
6. **Hồ sơ cũ (vẫn dùng được, mỏng hơn):** `FlowHandoff_local\shared\IDEA_GORO_LaneFG.md` +
   `results\channel_dna
ougo-no-goro\` (CHANNEL_DNA.md + VIDEO_ANALYSIS 8 video + TAG_STATS.json + `_raw/`).
   **Giai đoạn 2 phải copy sang `docs\channel_dna
ougo-no-goro\`.**
7. `assets\teinengo-fuufu\branding\KENH.json` — tên/handle/mô tả/keywords/hashtag đã lên kênh.
8. Khuôn để chép: `docs\SOP_LANE_F.md` + `profiles\profiles\teinengo-real.json` · `docs\SOP_LANE_G.md` +
   `teinengo-tanoshimi.json`; `SOP_LANE_E.md` cho lane không REF-LOCK.
9. Luật toàn dự án: `CLAUDE.md` · `docs\QUY_TRINH_SETUP_KENH.md`.

⚠️ Hook bắt buộc khoá trước S2 — Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn), dài ≈ hook gốc — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá.

## 3b. 💬 BÌNH LUẬN 15 VIDEO — ĐÃ GOM + PHÂN TÍCH XONG (648 bình luận)

**Phủ 15/15 video (100%) · 648 bình luận** · YouTube Data API `commentThreads` `order=relevance` · gom 28/09.
- Thô: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\comments_15videos.json`
- Phân tích: `...\scratch_golo\PHAN_TICH_BINH_LUAN_15VIDEO.md`
- Script: `...\scratch_golo\fetch_comments_15.py`

### 🚨 PHÁT HIỆN QUYẾT ĐỊNH — khán giả **CHÊ HÌNH VẼ GIÀ** rất nặng
6/20 bình luận like cao nhất là chê nhân vật vẽ già: `この絵は80歳ですね` (**446👍**),
`60代の人間は相当老人に見えてる` (384👍), `いい話だけど老けすぎてない？` (323👍),
`今の60代 こんな昭和な感じの描き方は違う` (252👍), `節子さん６２歳なのに８０歳位に見える` (218👍).

**3 LUẬT CỨNG MỚI cho khâu dựng hình (từ bình luận, không đoán):**
1. **Nhân vật 60–65 tuổi PHẢI vẽ như 45–55** — khán giả tự nhận mình trẻ (`今の65歳は40代に見える人も多い`).
2. **CẤM tóc bạc trắng + lưng còng + đồ tối màu kiểu "ông bà già"** — bị gọi là `昭和の描き方` = lỗi thời.
3. **Trang phục phải hiện đại, có gu** — `服のセンスも見るに耐えない` (144👍).

> ⚠️ **Chốt với lane:** luật #5 mục 5 (CẤM nhân vật **trẻ hơn** khán giả) áp cho **kịch bản**;
> 3 luật này áp cho **hình vẽ**. Hai tầng khác nhau — đừng hiểu lệch thành "vẽ nhân vật già".

### 🎯 Định hướng nội dung: bàn nhiều ≠ tạo like cao
| Nhóm | Số BL | Like cao nhất |
|---|---|---|
| LÀM VIỆC | 167 (25,8%) | 236 |
| TIỀN / TÀI CHÍNH | 110 (17,0%) | 177 |
| **GIA ĐÌNH / CHỒNG VỢ** | 64 (9,9%) | **447** |
| **CHÊ HÌNH VẼ GIÀ** | 18 (2,8%) | **446** |

⇒ **Đánh vào GIA ĐÌNH/CHỒNG VỢ (cảm xúc cực mạnh), không phải LÀM VIỆC (thảo luận nhiều, like thấp).**

### ⚠️ RỦI RO SỐ 1 CỦA LANE: **SỐ LIỆU TIỀN PHẢI ĐÚNG**
Khán giả 60+ bắt lỗi kiến thức 3 lần: `年金は手続きしないと振り込まれません` (43👍) ·
`年金600万円？300万円で天井` (34👍) · `年金15万で小遣い5万円て非現実的` (9👍).
Còn cảnh báo sức khoẻ: `２万歩…私は3か月で膝を壊し、２年間リハビリ` (32👍) ⇒ **≤10.000 bước**.
**⇒ Thêm 1 bước vào quy trình: kiểm tra số liệu lương hưu/thủ tục với nguồn thật TRƯỚC khi dựng.**

⚠️ Giới hạn: API trả tối đa 100 BL/video theo độ liên quan (#1–#3 chạm trần); **reply chưa gom**.

---

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
- Tựa theo IDEA_GORO §1: 【漫画】{2 lựa chọn hưu trí}…{5年後}…とは？ (hook: theo luật 21/10 bám sát cấu trúc hook video gốc — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`).
- Topic vàng chưa lane nào làm: 熟年離婚 VS 家庭内別居 どっちが幸せ (810k) — ưu tiên tập đầu.
- Số liệu thật có nguồn; QC giọng trước render.
- Hồ sơ nghiên cứu MỎNG (không handoff 14 mục) → gate PHẢI đo từ 8 VIDEO_ANALYSIS + transcript `_raw`, không suy từ F/G.

## 6. CỘT SHEET TAB `teinengo-fuufu` (A→K, giống Lane E §1b)
A STT (= số ep) · B NỘI DUNG · C FOLDER · D KỊCH BẢN (`done` = kịch bản QC + giọng QC + prompt ảnh; mốc tạm F/G là
`script-qc-done`) · E TITLE-DESCRIPTION · F TAGS (không làm marker) · G THUMBNAIL · H STATUS-IMG (1 ô, 2 dòng, path không
`h2dev\`) · I VIDEO · J LIST · K GHI CHÚ.
