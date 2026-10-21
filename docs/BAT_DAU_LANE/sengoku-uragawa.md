# BẮT ĐẦU LANE I — `sengoku-uragawa` · 戦国の裏側

> Anh nói **"thực hiện lane sengoku-uragawa"** (hoặc "LANE I") → tab này ĐỌC HẾT file này trước, mở đầu báo cáo bằng
> `@lane:sengoku-uragawa`, rồi làm ĐÚNG THỨ TỰ mục 4. Không tìm hiểu lại từ đầu, không đoán. File này là "cửa vào";
> chi tiết vận hành nằm ở SOP (mục 4 giai đoạn 2 sẽ viết). Cập nhật mục 2 mỗi khi trạng thái đổi.

## ⚡ ĐỌC NHANH — "làm tập tiếp theo" (lane đã setup xong, mục 2 TRẠNG THÁI đã ✅ hạ tầng)
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
| Mã lane / profile id | `sengoku-uragawa` (thư mục `assets/sengoku-uragawa/`; tab sheet hiện `sengoku-uragawa`, theo quy ước 24/09 sẽ là `I-sengoku-uragawa`) |
| Kênh thật | 戦国の裏側 · `@sengoku-uragawa` · `UCxBOdUsVT8g8WnpvJ8SdjyQ` |
| Mail (GMAIL dòng 10) | `AldenorRodrigues626@gmail.com` — profile GPMLogin cùng tên, anh login tay |
| Kênh mẫu (clone) | どっこい日本史 `https://www.youtube.com/channel/UCxXV78OIGchz13GAA7RGbEQ` |
| NOTE | dòng 6 (STT 5) — cột L đã ghi `@sengoku-uragawa` = kênh đã setup |
| Tab sheet sản xuất | **`sengoku-uragawa`** (header A→K, mục 6) |
| Thư mục làm việc | `E:\CLAUDE\YOUTUBE\h2dev\assets\sengoku-uragawa\` (branding đã có; tập = `ep<NN>-<slug>\`) |
| Giao hàng bước 3 | `E:\CLAUDE\YOUTUBE\CHANEL\sengoku-uragawa\ep<NN>-<slug>\` |
| Format | **Manga seinen/anime lịch sử NGHIÊM TÚC** (KHÔNG phải chibi — đã soi 21/21 thumbnail thật 2026-09-23, xem `docs\channel_dna\dokkoi-nihonshi\THUMBNAIL_PATTERNS.md`) + narration NAM. Mỗi tập 1 NHÂN VẬT Chiến quốc nổi tiếng có game/anime → lật huyền thoại bằng TÀI LIỆU GỐC (nhật ký, thư, sử liệu) → câu chuyện chi tiết → nối về hình ảnh game/anime |
| Giọng | Nam, kể tài liệu có nhịp tò mò (gần toshi-densetsu-jp hơn satori) — CHƯA CHỐT: hỏi anh clone kênh mẫu hay giọng kho |
| Khác lane nào | Khác hẳn mọi lane người già: khán giả nam 30–60, tài liệu lịch sử thật (documentary), ảnh manga chibi |

## 2. TRẠNG THÁI (cập nhật mỗi lần đổi)
- ✅ 2026-09-13 nghiên cứu kênh (TRENDING-RESEARCH, anh duyệt danh sách NOTE).
- ✅ 2026-09-16 Channel Analyzer (K1+K2) lần 1: 8 video (bản lưu `results\channel_dna\dokkoi-nihonshi`).
- ✅ 2026-09-23 **DNA đã MỞ RỘNG + COPY về `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\dokkoi-nihonshi\`**
  (= xong việc #1 của giai đoạn 2). Đủ **21/21 video** của kênh mẫu · tiêu đề GỐC tiếng Nhật (lần 1 phân
  tích nhầm trên tiêu đề YouTube tự dịch sang tiếng Anh) · `TAG_STATS.json` có thêm `channel_keywords` ·
  thêm `THUMBNAIL_PATTERNS.md` (đo 21 thumbnail thật) + `_raw\thumbs\`. Bản 8 video giữ lại ở
  `CHANNEL_DNA_8video_2026-09-17.md.bak`.
- ✅ 2026-09-20 setup kênh A+B xong bằng `tools/channel_branding.py` (branding gpti2 + 6 mục settings, verify
  reload), sheet GMAIL/NOTE đã ghi, tab sheet + header đã tạo. Tên/handle/mô tả/hashtag do em đề xuất, anh duyệt nguyên.
- 📤 2026-09-23 đã gửi đơn đổi vai (Phương án A) sang dự án nghiên cứu: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\YEU_CAU_TU_H2DEV_2026-09-23.md`
  — bên đó sửa `lane_profile.yaml` (ghi sai "chibi"), đo `thumb_dna.json` cho lane, và TỪ NAY KHÔNG làm CHANNEL_DNA nữa (h2dev tự chạy). Chờ trả lời ở `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\BAO_CAO_TRENDING_2026-09-23.md`.
- ❌ CHƯA: profile JSON · giọng · char-rate · SOP · danh sách tập · bất kỳ kịch bản nào. Anh mới duyệt SETUP KÊNH,
  chưa ra lệnh giai đoạn 2 — tab mở phiên mới phải HỎI trước khi bắt đầu mục 4.

## 3. TÀI LIỆU — đọc theo thứ tự này, đường dẫn thật trên máy 1
1. `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\GIAO_VIEC_LANE_I.md` — tóm tắt việc + công thức thắng + hard rules.
2. Hồ sơ nghiên cứu: FlowHandoff_local\shared\laneI_dokkoi\channel_analysis_どっこい日本史.json (KHÔNG có LANE_I_HANDOFF.md 14 mục — chỉ JSON).
3. **`E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\dokkoi-nihonshi\`** (bản CHÍNH, đọc bản này) — `CHANNEL_DNA.md` + `VIDEO_ANALYSIS/*.json`
   (21 video) + `TAG_STATS.json` (có `channel_keywords`) + `THUMBNAIL_PATTERNS.md` + `_raw\` (transcript +
   21 thumbnail). Bản 8 video ở `FlowHandoff_local\results\channel_dna\dokkoi-nihonshi\` chỉ còn giá trị lịch sử.
4. `assets\sengoku-uragawa\branding\KENH.json` — tên/handle/mô tả/keywords/hashtag đã lên kênh (nguồn chân lý branding).
5. Khuôn để chép: lane gần nhất đã đi hết giai đoạn 2 — `docs\SOP_LANE_F.md` + `profiles\profiles\teinengo-real.json`
   (fiction_facts + structure_block + Fable viết/B3R) và `docs\SOP_LANE_G.md` + `teinengo-tanoshimi.json`; `SOP_LANE_E.md`
   cho lane không REF-LOCK.
6. Luật toàn dự án: `CLAUDE.md` (router + ⛔ Claude chỉ làm BƯỚC 1, không render, không tự upload-job lần đầu) ·
   `docs\QUY_TRINH_SETUP_KENH.md` (đã làm, chỉ đọc khi cần sửa kênh).

⚠️ Hook bắt buộc khoá trước S2 — Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn), dài ≈ hook gốc — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá.

## 4. QUY TRÌNH — làm bước nào trước
### Giai đoạn 2 — dựng hạ tầng lane (1 LẦN, đúng thứ tự, xong mới sang giai đoạn 3)
1. ~~**Copy DNA**~~ ✅ XONG 2026-09-23 — đã copy VÀ mở rộng lên 21 video (xem mục 2).
2. **Profile** `profiles\profiles\sengoku-uragawa.json` (chép khuôn teinengo-real/teinengo-tanoshimi, sửa từng field):
   `id/slug_dir/competitor/channel_dossier/channel_dna_dir` · `narrator` theo Format mục 1 · documentary: nhân vật/sự kiện CÓ THẬT — mọi dữ kiện (năm, tên tài liệu, nơi lưu trữ) phải kiểm chứng, tách rõ 'truyền thuyết' vs 'sử liệu' ·
   script.structure = 'hook tên quen + lật huyền thoại → bằng chứng gốc → chuyện → nối game/anime' (khai structure_block; gần chapters5 của toshi nhưng 1 nhân vật) · `body.mode=ai_images` · ref_lock=true cho NHÂN VẬT CHÍNH của tập (1 võ tướng chibi lặp suốt tập; phụ không khoá); không xuyên tập · `image.style_suffix` theo Format ·
   `thumbnail` = chibi nhân vật + chữ lớn, màu truyền thống (đỏ/vàng/đen) · `publish.sheet_tab=<tên tab thật, quy ước I-sengoku-uragawa>` · `script.brain_model` Fable như F/G nếu anh giữ chủ trương đó.
   **`script.gate` PHẢI ĐO** từ transcript thật trong `_raw/` (title_len, hook_chars, comma/breath) — không chép số lane khác.
3. **Giọng**: Nam, kể tài liệu có nhịp tò mò (gần toshi-densetsu-jp hơn satori) — CHƯA CHỐT: hỏi anh clone kênh mẫu hay giọng kho. Nếu clone: tách 20–30s sạch từ 1 video kênh mẫu → `POST /voice-clone` (skill `openspeaker_voice_clone.md`)
   → nghe A/B → **HỎI ANH trước khi giữ voice_id** (giọng người thật). Ghi `voice.id`.
4. **Char-rate**: `py -3.13 pipeline\calibrate.py --profile sengoku-uragawa` (`calib_style` theo văn phong) → ghi `voice.char_rate`.
5. **SOP** `docs\SOP_LANE_I.md` theo khuôn `SOP_LANE_F.md`: §0 bảng delta, **§0b Channel Analyzer** (bắt buộc),
   §1 quyết định, §1b danh sách 10 tập + quy tắc cột sheet, §2 lệnh chạy, §3 gate, §5b phân vai.
6. **Router**: 1 dòng bảng lane `CLAUDE.md` (đã có sẵn dòng cửa vào, chỉ cập nhật cột SOP) + `docs\DANH_BA_LANE.md` + mục 2 file này.
7. **Danh sách 10 tập** vào tab `sengoku-uragawa` cột A/B (bám HIT của kênh mẫu, tránh trùng tựa hit). Tập 1 đề xuất: 1 võ tướng nổi tiếng chưa bị kênh mẫu đốt (đề xuất 伊達政宗 hoặc 真田幸村) — HOOK: 'bạn biết hắn qua game, nhưng bức thư tay 400 năm cho thấy…'.

### Giai đoạn 3 — sản xuất 1 tập (CHỈ tập anh chỉ định "cho làm tập X")
1. Tạo `assets\sengoku-uragawa\ep<NN>-<slug>\`, ghi cột C.
2. Hồ sơ đề tài: `competitor.txt` (1 transcript thật cùng dạng qua `retrieve_videos.py --dna-dir docs\channel_dna\dokkoi-nihonshi
   --topic "..."`) + `series_ctx.txt` (dữ kiện CÓ NGUỒN — cấm bịa).
3. `py -3.13 -X utf8 pipeline\make_video.py --profile sengoku-uragawa --slug ep<NN>-<slug>` — chạy tới mốc anh cho phép (F/G hiện
   dừng ở kịch bản + QC `--den B3R`); đủ bước 1 = B3 + gate → B3Q/B3F/B3S → B4 giọng + B4Q → B5W/B5P prompt ảnh →
   master REF-LOCK (nếu có) → `TIEU_DE_MO_TA.txt` + `thumb_text.txt`.
4. Ghi cột D + K → **DỪNG**. KHÔNG tự `upload-job` lần đầu — chỉ khi anh nói "giao sang máy 2".
5. Anh bảo giao → job `FlowHandoff_local\jobs\<slug>\`, cột H 1 ô 2 dòng, path KHÔNG `h2dev\`.
6. Bước 3 = agent khác (`docs\QUY_TRINH_RENDER_VIDEO.md`); xong ghi cột I (CHANEL) + G. Claude Code KHÔNG render.

## 5. LUẬT CỨNG RIÊNG LANE
- LUÔN gắn nhân vật NỔI TIẾNG có phiên bản game/anime (前田慶次 712k, 柴田勝家 465k…); sự kiện không tên tuổi chết 3,3k.
- Bằng chứng gốc là 'gia vị' bắt buộc: nhật ký/tài liệu/số liệu thật, ghi rõ nguồn lưu trữ.
- Không bịa lịch sử; luôn nói rõ huyền thoại vs tài liệu gốc.
- Kênh mẫu ĐÃ làm (soi ĐỦ 21/21 video 2026-09-23; danh sách cũ chỉ có 7/21): 前田慶次 · 柴田勝家(×2) · 徳川家康 ·
  武田勝頼 · 今川義元 · 千利休 · 小早川秀秋 · 今川氏真 · 明智光秀 · お市の方 · 前田利家 · 石田三成 · 春日局 ·
  豊臣秀長 · 黒田官兵衛 · 近藤勇 · 松永久秀 · ジョン万次郎 · 寧々 · 備中高松城 → TRÁNH.
- Vẫn CÒN TRỐNG (không video nào trong 21 chạm tới): 織田信長 / 豊臣秀吉 / 伊達政宗 / 真田幸村 / 上杉謙信 /
  武田信玄 — đúng như đề xuất cũ, nay đã kiểm chứng trên TOÀN kênh chứ không phải 8 video.
- Tử huyệt của kênh mẫu (tránh lặp lại): nhân vật NỮ + ngoài Chiến quốc — 春日局 10k · 寧々 4,4k ·
  近藤勇 6,4k · ジョン万次郎 5,1k, trong khi võ tướng hệ 織田 ăn 142k–771k.
- Khán giả nam 30–60 (KHÔNG phải người già như E/F/G/H) → nhịp nhanh hơn, không cần giãn nhịp.

## 6. CỘT SHEET TAB `sengoku-uragawa` (A→K, giống Lane E §1b)
A STT (= số ep) · B NỘI DUNG · C FOLDER · D KỊCH BẢN (`done` = kịch bản QC + giọng QC + prompt ảnh; mốc tạm F/G là
`script-qc-done`) · E TITLE-DESCRIPTION · F TAGS (không làm marker) · G THUMBNAIL · H STATUS-IMG (1 ô, 2 dòng, path không
`h2dev\`) · I VIDEO · J LIST · K GHI CHÚ.
