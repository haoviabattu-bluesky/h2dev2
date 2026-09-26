# BẮT ĐẦU LANE M — `teinengo-anaba` · 定年後の穴場ノート【漫画】 (Sổ tay chỗ hay ít người biết sau nghỉ hưu)

> Anh nói **"thực hiện lane teinengo-anaba"** (hoặc "LANE M", "M-teinengo-anaba") → tab này ĐỌC HẾT file này trước, mở đầu
> báo cáo bằng `@lane:teinengo-anaba`, rồi làm ĐÚNG THỨ TỰ mục 4. File này là "cửa vào"; chi tiết vận hành nằm ở SOP
> (`docs\SOP_LANE_M.md`, đã viết 2026-09-26). Cập nhật mục 2 mỗi khi trạng thái đổi.

## 1. ĐỊNH DANH (không đổi)
| Mục | Giá trị |
|---|---|
| Mã lane / profile id | `teinengo-anaba` (profile `profiles\profiles\teinengo-anaba.json`) |
| **Tên thư mục = tên tab = `M-teinengo-anaba`** | anh chốt 2026-09-26: thư mục làm việc theo tên kênh có tiền tố lane |
| Thư mục làm việc (`slug_dir`) | `E:\CLAUDE\YOUTUBE\h2dev\assets\M-teinengo-anaba\` (branding đã có; tập = `ep<NN>-<slug>\`) |
| Tab sheet sản xuất | **`M-teinengo-anaba`** — header A→S (mục 6) |
| Giao hàng bước 3 | `E:\CLAUDE\YOUTUBE\CHANEL\M-teinengo-anaba\ep<NN>-<slug>\` (tra bằng `pipeline\duong_ket_qua.py`) |
| Kênh thật | 定年後の穴場ノート【漫画】 · `@teinengo-anaba` — **anh TỰ cài thông số + tự upload ảnh**, Claude KHÔNG chạy `channel_branding.py` |
| Mail | `haoviabattu@gmail.com` (kênh thứ 2 của mail này; GMAIL dòng 3 là Lane A → chỉ ghi chú ở ô L3, không ghi đè) |
| NOTE | dòng 10 (STT 9) — G `Đã nhận kênh` · H mail · L `@teinengo-anaba` |
| Kênh mẫu (clone) | 大人の盲点【漫画でわかる人生の裏側】 (Điểm mù của người lớn) `@otonanomouten` `UCsWLzQF-6knOsQlHYBNtvwg` |
| Format kênh mẫu | Manga chibi AI + giọng máy, 28–40 phút, đếm ngược N選 (N lựa chọn), nhân vật cố định 高瀬健一 64 tuổi cựu 信用金庫 (quỹ tín dụng) + vợ 恵子, câu chốt 「盲点だった。」 (đúng là điểm mù) |
| Lane M làm gì | **CHỈ trụ cột VIỆC LÀM tuổi 60**: アルバイト・パート (việc làm thêm), 再就職 (tái tuyển dụng), thu nhập sau hưu, việc 穴場 (ít người biết). Nhân vật chính RIÊNG (ông tóc muối tiêu, kính mảnh, áo len vàng mù tạt, sổ tay xanh — xem avatar), KHÔNG dùng 高瀬 |
| Không làm | Sở thích/dạo bộ/du lịch 0円/thư viện (= Lane G) · kịch tính tiền mất (= Lane F) · vợ chồng (= Lane J) |

## 2. TRẠNG THÁI
- ✅ 2026-09-26 nghiên cứu kênh (TRENDING-RESEARCH): DNA K1+K2 6 video, báo cáo + hồ sơ giao việc.
- ✅ 2026-09-26 anh duyệt mở Lane M riêng; anh tự setup kênh; em làm avatar + cover (anh tự upload):
  `E:\CLAUDE\YOUTUBE\h2dev\assets\M-teinengo-anaba\branding\{avatar_raw.png, banner_final.png, banner_bg_raw.png}`.
- ✅ 2026-09-26 sheet: NOTE dòng 10 G/H/L · GMAIL L3 ghi chú · tab `M-teinengo-anaba` header A→S.
- ✅ 2026-09-26 DNA copy về `docs\channel_dna\otonanomouten\` + bình luận: `COMMENTS_TOP.md` (53 bình luận) + `COMMENT_INSIGHT.md` (khối ĐƯA VÀO PROMPT).
- ✅ 2026-09-26 GIAI ĐOẠN 2 (trừ giọng):
  - Profile `E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\teinengo-anaba.json` — gate/budget/goi_dang ĐO từ 6 transcript `_raw` (có `_nguon`), `structure_block` xếp hạng 第7位→第1位.
  - Nhân vật 田島誠 (たじま まこと, 63) + vợ 田島春江 (はるえ, 61) — ảnh gốc lane `E:\CLAUDE\YOUTUBE\h2dev\assets\M-teinengo-anaba\_ref_kenh\{makoto,harue}\001.png` (`image.fixed_refs`), 5 ảnh thử ≈2.070đ.
  - SOP `E:\CLAUDE\YOUTUBE\h2dev\docs\SOP_LANE_M.md` (§0b Channel Analyzer, K1–K12 chép nguyên).
  - 10 tập ghi tab `M-teinengo-anaba` A2:B11 + video gốc ở K2:K11.
- ✅ 2026-09-26 GIỌNG: ĐA GIỌNG — 7 giọng clone từ video gốc tập 1 (anh duyệt cả 7), xem SOP §0c.
- ❌ CHƯA: char-rate · kịch bản · đo `seconds_per_image` kênh mẫu. (`claude -p` Fable + Opus thử lại 26/09 chiều: chạy được.)

## 3. TÀI LIỆU — đọc theo thứ tự
1. `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\GIAO_VIEC_OTONANOMOUTEN_2026-09-26.md` — hồ sơ giao việc (công thức thắng, hard rules).
2. `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\OTONANOMOUTEN_CHANNEL_REPORT.html` — báo cáo đầy đủ.
3. `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\otonanomouten\` — `CHANNEL_DNA.md` + `VIDEO_ANALYSIS\*.json` + `TAG_STATS.json` + `_raw\`.
4. ⭐ `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\otonanomouten\COMMENT_INSIGHT.md` — **đọc TRƯỚC khi viết bất kỳ tập nào** (mục 5).
5. Dữ liệu thô: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\otonanomouten\` (`comments.json` · `transcripts\` · `thumbs\` · `competitors.json`).
6. Khuôn chép: `docs\SOP_LANE_G.md` + `profiles\profiles\teinengo-tanoshimi.json` (manga list N選, REF-LOCK nhân vật chính) ·
   `docs\SOP_LANE_L.md` + `shakai_no_naze.json` (nhân vật khoá XUYÊN TẬP bằng `image.fixed_refs`, `outro_line`).
7. Luật toàn dự án: `CLAUDE.md` · `docs\QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` §2a (bình luận) · §2b (hook) · §2c (cung cảm xúc + kết cảm ơn) · §4c (máy 3 soát).

## 4. QUY TRÌNH
### Giai đoạn 2 — hạ tầng lane (1 LẦN, đúng thứ tự)
1. **Profile** `profiles\profiles\teinengo-anaba.json` (chép khuôn teinengo-tanoshimi): `id=teinengo-anaba` ·
   `slug_dir=assets/M-teinengo-anaba` · `channel_dna_dir=docs/channel_dna/otonanomouten` (để lean nhồi COMMENT_INSIGHT) ·
   `publish.sheet_tab=M-teinengo-anaba` · `publish.upload_channel=M-teinengo-anaba` · `body.mode=ai_images` ·
   nhân vật chính khoá XUYÊN TẬP (1 ảnh gốc lane từ avatar, như Sakura Lane L) + vợ ·
   `script.outro_line` = 1 câu CTA riêng của kênh có đủ **cảm ơn xem hết + 高評価 (thích) + チャンネル登録 (đăng ký)** ·
   `script.cung_cam_xuc` để vắng (= bật) · `script.review_may3` để vắng (= bật) · hook `video_sinh` + `sfx: true` · `goi_dang.enabled`.
   **`script.gate` + budget PHẢI ĐO** từ `_raw\` transcript thật (độ dài, vị trí mục đầu, marker 第N位).
2. **Giọng**: kênh mẫu dùng giọng máy nam (bị chê đọc sai tên 「シンリコさん」). Chọn giọng kho ai33 nam 60 tuổi ấm — hoặc clone thì
   **HỎI ANH trước khi giữ voice_id**. KHÔNG dùng chung voice_id với F/G. Ghi `voice.id` → `pipeline\calibrate.py` đo char-rate.
3. **SOP** `docs\SOP_LANE_M.md` theo khuôn `SOP_LANE_G.md` (§0 delta, §0b Channel Analyzer bắt buộc, §1b 10 tập + cột sheet, §2 lệnh).
4. **Danh sách 10 tập** vào tab `M-teinengo-anaba` cột A/B — chỉ trụ cột việc làm, bám hit 92k (7 việc làm thêm thoải mái),
   thêm móc tiết kiệm/0 vốn mà kênh mẫu chưa dùng; tránh trùng tựa kênh mẫu và tựa Lane G.

### Giai đoạn 3 — 1 tập (CHỈ tập anh chỉ định)
1. Đọc `COMMENT_INSIGHT.md` + bình luận của đúng video gốc trong `COMMENTS_TOP.md` → lỗi dữ kiện khán giả bắt ghi vào QUY ƯỚC `series_ctx.txt`.
2. Tạo `assets\M-teinengo-anaba\ep<NN>-<slug>\`, ghi cột C. Hồ sơ đề tài: `competitor.txt` (`retrieve_videos.py --dna-dir docs\channel_dna\otonanomouten`) + `series_ctx.txt` (lương giờ/chế độ/giới hạn tuổi CÓ NGUỒN) + `promise.txt`.
3. `py -3.13 -X utf8 pipeline\make_video.py --profile teinengo-anaba --slug ep<NN>-<slug> --den B3G` → tự dừng sau LOCK (cột D = `Cần check kịch bản`).
   ⭐ **Anh chốt 2026-09-26: Lane M KHÔNG chờ máy 3** — tab lane tự soát bằng ChatGPT web (`pipeline\soat_kb_gptweb.py`, hội thoại ở `profile.script.soat_gptweb.url`) → viec_tay → Opus → Sol ×2 → `BAO_CAO_SUA.md` + D = `Đã sửa kịch bản` → `review_may3.py --nhan`. Chi tiết `docs\SOP_LANE_M.md` §1e + §2.
4. Nhận bản soát → gan_vai → B5W/B5P (`--only`) → hook → `dong_goi_may2.py --job` (tự ghi D=`Done` + H=`cần ảnh`) → `HOOK_TAP.md` → giao máy 2. Claude Code KHÔNG render.

## 5. ⛔ LUẬT KHOÁ CỨNG LANE M (anh chốt 2026-09-26 — vi phạm 1 điều = DỪNG, không tự "linh hoạt")
**K1 — Tên:** thư mục làm việc = tên tab = thư mục giao hàng = `M-teinengo-anaba` (`assets\M-teinengo-anaba\`,
tab `M-teinengo-anaba`, `CHANEL\M-teinengo-anaba\`). Mã lane/profile id = `teinengo-anaba`. Cấm tạo thư mục `assets\teinengo-anaba\`.
**K2 — Kênh:** anh TỰ setup kênh + tự upload avatar/cover. Cấm chạy `tools\channel_branding.py`, cấm mở GPM vào YouTube Studio kênh này.
**K3 — Sheet:** mail `haoviabattu@gmail.com` là kênh thứ 2 của mail (GMAIL dòng 3 = Lane A) → cấm ghi đè GMAIL dòng 3 (chỉ ô ghi chú L3).
Tab `M-teinengo-anaba` header A→S cố định (mục 6), cấm đổi/xoá cột; cấm xoá dữ liệu bất kỳ sheet nào.
**K4 — Phạm vi đề tài:** CHỈ việc làm tuổi 60 — アルバイト・パート (việc làm thêm), 再就職 (tái tuyển dụng), 再雇用 (tuyển lại sau hưu),
thu nhập đi làm vs 年金 (lương hưu). Cấm sở thích/du lịch/0円 vui chơi (Lane G), cấm drama mất tiền (Lane F), cấm trục vợ chồng (Lane J).
**K5 — Bình luận trước khi viết:** mỗi tập đọc `docs\channel_dna\otonanomouten\COMMENT_INSIGHT.md` + bình luận của đúng video gốc trong
`COMMENTS_TOP.md`; lỗi dữ kiện khán giả đã bắt ghi thành QUY ƯỚC trong `series_ctx.txt`. Hai ví dụ phải nhớ:
「初月はシフト18日でしたが、次の月は11日でした」 (tháng đầu 18 ca, tháng sau 11 ca — không đủ sống) = nỗi lo thật → cú KÍCH;
「5キロの荷物を2人で持つことはない」 (không ai 2 người khiêng 5 kg) = chi tiết gốc phi thực tế → kiểm lại mọi con số trước khi clone.
**K6 — Cung cảm xúc:** KÍCH (quản lý cắt ca tuỳ tiện / nơi tuyển coi người 60 là đồ bỏ / đồng nghiệp cũ bám chức danh, leo thang ≥3 nấc)
→ GIẢI TOẢ bằng sự thật + chế độ thật → VỊ THA + 1 câu đạo lý đáng chép. Cấm viết nhẹ nhàng khô khan. Profile KHÔNG được khai `cung_cam_xuc: false`.
**K7 — Kết bắt buộc:** cảm ơn người xem đã quan tâm xem hết video + xin 1 lượt 高評価 (thích) + チャンネル登録 (đăng ký).
`script.outro_line` của lane phải chứa đủ 3 ý; máy kiểm `KẾT THIẾU`. Profile KHÔNG được khai `cam_on_cuoi: false`.
**K8 — Cấu trúc:** mục xếp hạng đầu tiên TRƯỚC phút 4 (khán giả kênh mẫu chê "nửa đầu chỉ kể chuyện"); truyện đan xen giữa các mục;
mỗi mục = ưu điểm + cái bẫy + con số (giờ, lương giờ, ca/tuần, sức nặng) + ai hợp/không hợp. Hạng 1 để cuối, giấu trên thumbnail.
**K9 — Sự thật:** lương giờ, chế độ 在職老齢年金 (lương hưu bị trừ khi đi làm), giới hạn tuổi, bảo hiểm, luật cắt ca → CÓ NGUỒN trong
`series_ctx.txt` [Dn] và nói rõ điều kiện; không nguồn thì nói định tính. Nhân vật/tình tiết hư cấu được, số chế độ thì cấm bịa.
**K10 — Nhân vật:** ông chính RIÊNG của lane (tóc muối tiêu, kính gọng mảnh, áo len vàng mù tạt, sổ tay xanh — theo `branding\avatar_raw.png`),
khoá mặt XUYÊN TẬP bằng 1 ảnh gốc lane (như Sakura Lane L). Vợ có chính kiến, chồng không quát/nói trống không với vợ.
Cấm dùng 高瀬健一 / 恵子 / câu chốt 「盲点だった。」 / tên kênh mẫu. Nét chibi dễ thương, soát lỗi ảnh AI (tóc, tay).
**K11 — Giọng:** không dùng chung voice_id với lane nào; clone giọng người thật → HỎI ANH trước khi giữ voice_id; mọi tên riêng
phải nghe thử qua TTS (kênh mẫu bị chê đọc sai 「シンリコさん」); nhạc nền không được "ngớ ngẩn" (bị chê 12 like).
**K12 — Luật dự án chung vẫn áp:** Claude chỉ làm BƯỚC 1 (không render); hook 20–30s là video sinh + SFX (cổng S1L); máy 3 soát kịch bản
sau LOCK; xong tập ghi D=`Done` + H=`cần ảnh`; mọi chữ Nhật trong báo cáo kèm dịch tiếng Việt; báo cáo ghi đường dẫn tuyệt đối.

## 6. CỘT SHEET TAB `M-teinengo-anaba` (A→S)
A STT (= số ep) · B NỘI DUNG (tựa tập + dịch) · C FOLDER · D KỊCH BẢN (`Cần check kịch bản` → `Đã sửa kịch bản` → `Done`) ·
E TITLE-DESCREPTION · F TAGS · G THUMBNAIL · H STATUS-IMG (`cần ảnh (N ảnh, ~Xđ)`) · I VIDEO · J LIST · K GHI CHÚ ·
L ID KÊNH · M LINK KÊNH · N SỐ NGÀY LIST · O VIEW · P CTR TỔNG · Q CTR 24H · R VIEW CŨ · S CTR 24H CŨ (L→S theo dõi sau khi đăng).
