# BẮT ĐẦU LANE L — `shakai_no_naze` · 社会のなぜ研究室 (Shakai no Naze Kenkyūshitsu, dịch: "Phòng nghiên cứu Vì sao của xã hội")

> Anh nói **"thực hiện lane shakai_no_naze"** (hoặc "LANE L") → tab này ĐỌC HẾT file này trước, mở đầu báo cáo
> bằng `@lane:shakai_no_naze`, rồi làm ĐÚNG THỨ TỰ mục 4. Không tìm hiểu lại từ đầu, không đoán. File này là
> "cửa vào"; chi tiết vận hành nằm ở SOP (mục 4 giai đoạn 2 sẽ viết). Cập nhật mục 2 mỗi khi trạng thái đổi.

## ⚡ ĐỌC NHANH — "làm tập tiếp theo" (lane đã setup xong, mục 2 TRẠNG THÁI đã ✅ hạ tầng)
> ⭐ **2026-09-30 anh chốt — THẮNG mọi chỉ dẫn soát ChatGPT web bên dưới:** hook = Fable 5.1 viết 2 phương án theo luật hook 21/10 (bám sát cấu trúc hook video gốc: `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`);
> `make_video --den B3G` khoá xong là DỪNG, tự giao máy 3/anh soát (D=`Chờ kiểm tra kịch bản`). Anh sửa xong (D=`Đã sửa kịch bản`) →
> đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\NHAN_KICH_BAN_MAY3.md` để nhận + làm hook/ảnh/giao máy 2.

> ⭐ **21/10: lô tập 23–26 (sheet dòng 24–27) đã có hồ sơ + HƯỚNG DẪN RIÊNG từng tập** — anh dán "Lane L tập X đọc <thư mục tập>\HUONG_DAN_TAP.md và thực hiện" (= cột K); mục lục `E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\HUONG_DAN_TAP23-26.md`. Tập 23 = tập mẫu luật hook 21/10.

> ⭐ **14/10: lô tập 18–21 (sheet dòng 19–22) đã có hồ sơ + kế hoạch** — anh nói "làm tập X" (18…21) → đọc `E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\KE_HOACH_TAP18-21.md` mục 2 + `<thư mục tập>\KE_HOACH_TAP.md`, không đọc lại research.

> ✅ **01/10: tập 8 `ep08-nengajou-jimai` đã giao máy 2** (D9=Done, 122 ảnh). Tập kế = STT 9 (転勤 — chuyển công tác), đọc `assets\shakai_no_naze\HUONG_DAN_TAP_TIEP_THEO.md`.

CHỈ cần đọc: mục 4 **Giai đoạn 3** (lệnh chạy đúng thứ tự) + đúng file mục 4 tự trỏ tới (thường chỉ
`COMMENT_INSIGHT.md`). KHÔNG cần mở lại toàn bộ mục 3 TÀI LIỆU, SOP đầy đủ, `CHANNEL_DNA.md`,
`profile.json` — các file đó là cho **Giai đoạn 2 (setup 1 LẦN)** hoặc được chính `pipeline\*.py` tự
đọc khi chạy lệnh, không phải để Claude nạp vào context mỗi tập. Chỉ mở thêm khi lệnh báo lỗi cần
quyết định thủ công (thiếu context, xung đột dữ liệu...).

## 1. ĐỊNH DANH (không đổi)
| Mục | Giá trị |
|---|---|
| Mã lane / profile id | `shakai_no_naze` (thư mục `assets/shakai_no_naze/`; tab sheet = **`L-shakai-no-naze`**) |
| Kênh thật | 社会のなぜ研究室 · `@shakai-no-naze` · `UCjy5fWoigvtCfduJDJ3jTbg` |
| Mail (GMAIL dòng 13) | `SyedualiBajwa92@gmail.com` — profile GPMLogin cùng tên, anh login tay |
| Kênh mẫu (clone) | 社会のウラガワ (dịch: "Mặt sau xã hội") `@社会のウラガワ` `https://www.youtube.com/channel/UCFWFKb3Yr_1SrAT0kcvwFdw` |
| NOTE | dòng 9 (STT 8) — cột L đã ghi `@shakai-no-naze` = kênh đã setup |
| Tab sheet sản xuất | **`L-shakai-no-naze`** (header A→K, mục 6) |
| Thư mục làm việc | `E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\` (branding đã có; tập = `ep<NN>-<slug>\`) |
| Giao hàng bước 3 | `FlowHandoff_local\results\video_render\shakai_no_naze\<slug>\` (quy tắc 24/09 — KHÔNG dùng tên tab) |
| Format | Giải thích HIỆN TƯỢNG XÃ HỘI thật (tuyển dụng Gen Z, hôn nhân, công nghệ, tâm lý xã hội...) qua khuôn
  「なぜ〜のか」(vì sao lại...) — KHÔNG PHẢI kể chuyện 1 nhân vật cố định như F/G/K, mà là: đặt câu hỏi lớn →
  xung đột kịch tính minh hoạ → phân tích bằng số liệu/thuật ngữ thật (感情労働=lao động cảm xúc, 35歳転職限界説=
  giả thuyết giới hạn chuyển việc tuổi 35...) → hậu quả/đảo chiều → thông điệp an ủi. **Nhân vật xuyên suốt
  さくら (Sakura)** đóng vai người hỏi thay khán giả ở MỌI tập, vai trò khác nhau mỗi tập (nhân viên nhân sự,
  đồng nghiệp, cháu gái, khách hàng...) — câu hỏi kiểu Socratic lặp lại 「えっ、どういうことですか？」 |
| Giọng | **Anh chốt 24/09: y như kênh gốc** = ĐA GIỌNG (người kể nữ · Sakura · nhân vật nam), **ai33/MiniMax, KHÔNG
  VOICEVOX** (đo: kênh gốc không phải VOICEVOX). Ứng viên: người kể Kind Lady/Cold Queen · nam Gentle Butler · Sakura
  Graceful Maiden/Yuna — chờ anh nghe `assets\shakai_no_naze\_research\kenh_mau\nghe\SO_GIONG.html`. Chi tiết
  `docs\channel_dna\shakai-no-naze\DO_THUC_TE_2026-09-24.md` §3 |
| Khoá mặt | **Anh chốt 24/09: khoá TOÀN BỘ** — 1 ảnh ref gốc Sakura (tóc đen buộc đuôi ngựa, như 4/5 video gốc) dùng cho MỌI tập |
| Slide số liệu | **Anh chốt 24/09: BỎ** (kênh gốc có 1–5 slide/video nhưng AI vẽ số không chuẩn); số liệu vẫn tra có nguồn,
  nằm trong lời kể/hộp chữ máy vẽ |
| Nguồn số liệu | **Anh chốt 24/09: tab lane L tự tra** ở S1, ghi `series_ctx.txt` [Dn] kèm URL |
| Khác lane nào | KHÁC MỌI LANE Ở CẤU TRÚC NỘI DUNG: không kể chuyện 1-2 nhân vật đối lập (F/H/J/K) không phải
  list N選 (E/G), không phải documentary lịch sử (I) — mà là ESSAY GIẢI THÍCH có nhân vật MC xuyên suốt xuất
  hiện lại mỗi tập với vai trò khác. ⚠️ Sửa 24/09 (đo video thật): thân video là **manga anime kể chuyện liền mạch**
  ~7–8 ảnh/phút (~150 ảnh/tập), hộp chữ dọc + bóng thoại oval KHÔNG đuôi trên mọi cảnh, 2–5 slide số liệu/tập;
  Sakura cùng tên nhưng **khác mặt giữa các tập**. Khuôn kỹ thuật gần nhất = **Lane K**, không phải F |

## 2. TRẠNG THÁI (cập nhật mỗi lần đổi)
- ✅ 2026-09-24 nghiên cứu kênh xong bởi TRENDING-RESEARCH (ứng viên tự phát hiện khi quét ngách iyaku_labo,
  KHÔNG cùng ngách — báo cáo cảnh báo rõ điều này). Có sẵn `CHANNEL_DNA.md` chuẩn K1+K2 (8 video, QC 11/11 đạt)
  + 5 hook đã nạp HOOK_LIBRARY.
- ✅ 2026-09-24 anh chốt qua hội thoại: NOTE dòng 9 (STT 8) → Lane L (đúng gợi ý cột J sẵn có), kênh mẫu chưa
  có handle công khai nên em tự đặt `shakai-no-naze`.
- ✅ 2026-09-24 setup kênh A+B xong bằng `tools/channel_branding.py`, 1 lượt sạch 22/22, verify reload khớp.
  Tên/handle/mô tả/hashtag/keywords do em đề xuất dựa theo văn phong + hashtag suy luận từ kênh mẫu (kênh mẫu
  không có tag thật rõ trong dữ liệu đã đọc — **cần soi lại `TAG_STATS.json` nếu Channel Analyzer trả về
  channel_keywords thật, có thể phải sửa 9 keyword hiện tại**). Sheet GMAIL dòng 13 + NOTE dòng 9 đã ghi, tab
  `L-shakai-no-naze` + header đã tạo.
- ✅ 2026-09-24 đo thật 2 video + 11 transcript → `docs\channel_dna\shakai-no-naze\DO_THUC_TE_2026-09-24.md`;
  DNA đã chép sang `docs\channel_dna\shakai-no-naze\` (bước GĐ2.1 xong). Bước GĐ2.3 (đối chiếu keywords) ĐÓNG: kênh
  mẫu chỉ gắn tag 1/11 video, không có channel_keywords → giữ nguyên `KENH.json`.
- ✅ 2026-09-24 **GIAI ĐOẠN 2 XONG** (anh chốt 4 điểm + "lấy top 1 máy chọn"):
  profile `profiles\profiles\shakai_no_naze.json` (lean, hook video_sinh+sfx, goi_dang, gate đo) · code nhánh đa giọng
  ai33 (`profiles.da_giong`, `tts_voicevox.py` provider ai33, test `pipeline\tests\test_lane_l_da_giong_ai33.py`) ·
  bóng thoại không đuôi (`assemble.bubble.tail`) · khoá Sakura xuyên tập (`image.fixed_refs`, ảnh gốc
  `assets\shakai_no_naze\_ref_kenh\sakura\001.png`, QC 22/F đạt) · char_rate đo 311,5 chữ/phút · SOP `docs\SOP_LANE_L.md` ·
  router CLAUDE.md + DANH_BA · 10 tập đầu ghi sheet A2:B11. **Tiếp theo = giai đoạn 3, chờ anh "cho làm tập X".**
- ✅ 2026-09-24 **TẬP 1 XONG TRỌN (ngoại lệ anh cho: máy 1 làm cả ảnh + dựng video)**:
  `assets\shakai_no_naze\ep01-shusse-shitakunai\final_with_hook.mp4` (20,1', bóng thoại + hook clip Grok) → đã chép sang
  `FlowHandoff_local\results\video_render\shakai_no_naze\ep01-shusse-shitakunai\`; sheet dòng 2 D=Done. Bundle máy 2 đã
  làm mới (`--profile-list shakai_no_naze`). Chờ dự án TITLE làm tiêu đề/mô tả/tags/thumbnail. Từ tập 2 theo luồng thường
  (máy 1 bước 1 → máy 2). Bài học tập 1: SOP §9–§10.
- ⚠️ 2026-09-30 **Thư mục `ep07-taishoku-daikou` · `ep08-nenshu-no-kabe` · `ep09-reskilling-boom` · `ep10-ohitorisama-kyuzou` KHÔNG khớp sheet** (sheet STT 7–10 = 車離れ/年賀状/転勤/燃え尽き; 退職代行 còn vi phạm §5 luật 5). Tập N = dòng STT N của sheet. Tập 7 = `ep07-kuruma-banare` (viết 30/09, hook cao trào — `script.hook.cao_trao` bật cho L từ ngày này), đã gửi máy 3, D8 = `Chờ kiểm tra kịch bản`.
- ✅ 2026-10-01 **TẬP 7 `ep07-kuruma-banare` GIAO MÁY 2**: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\L-shakai-no-naze\ep07-kuruma-banare` (145 ảnh ≈ 14.750đ, D8=Done, H8=cần ảnh). Bản anh sửa 5.593 chữ ≈ 18,1'.
  Hook DÀI tới hết cao trào = 13 dòng/16 câu ≈ 55s (`_khoa_hook13.py`, profile `script.hook.den_cao_trao: true`), 14 clip Grok, CHỈ nhạc nền `hook\sfx\99_nhac_cang.mp3` (22s lặp).
  REF 7 vai khoá tuổi theo `docs\QUY_TAC_REF_NHAN_VAT_TUOI_CAM_XUC.md` (prompt tự viết `_ve_ref.py` — code mặc định ép "Neutral calm expression" trái luật cảm xúc; biên bản `REF_AGE_QC.md`).
  Bẫy mới: (1) gan_vai bắt mọi 「」 là thoại → biển hiệu/chữ trích bị gán nhân vật, sửa tay về `ke` (bản gốc `vai.gan_vai_goc.txt`); (2) gpti2 hay ra ảnh gần như ảnh thật cho nam vest → STYLE phải nhấn "flat 2D TV-anime"; (3) Sol chấm hook FAIL oan "họp sáng phải ở phòng họp" khi kịch bản là 朝礼 trong showroom; (4) nhạc nền ai33 AUTO chỉ 1,54s → `sfx.py ...|1|22`; (5) grok_1tk thiếu `GROK_SHEET_ID` → đã vá setdefault.
- ✅ 2026-10-01 **TẬP 8 `ep08-nengajou-jimai` GIAO MÁY 2**: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\jobs\L-shakai-no-naze\ep08-nengajou-jimai` (122 ảnh ≈ 12.280đ, D9=Done). Bản anh sửa 4.710 chữ ≈ 15,2' (dưới ngân sách, chỉ cảnh báo). Hook 17 câu ≈ 64s (`_khoa_hook.py`), 14 clip Grok, nhạc Suno `_bgm\HOOK_PIANO_LANE_L.mp3`. 7 REF khoá tuổi (`REF_AGE_QC.md`). Bài học: `assets\shakai_no_naze\HUONG_DAN_TAP_TIEP_THEO.md`.
- (lịch sử, đã xong ở GĐ2) CHƯA: đọc kỹ `CHANNEL_DNA.md` chuẩn đã có sẵn (mục 3) · profile JSON · giọng (nghi vấn mục 1) · char-rate ·
  SOP · danh sách tập · bất kỳ kịch bản nào. Anh mới duyệt SETUP KÊNH, chưa ra lệnh giai đoạn 2 — tab mở phiên
  mới phải HỎI trước khi bắt đầu mục 4.
- ⚠️ **Rủi ro đã ghi trong hồ sơ gốc, đọc trước khi đầu tư sâu**: kênh mẫu chỉ 66 ngày tuổi, MỘT video đạt
  431k view (chủ đề nóng Z世代 tuyển dụng) trong khi 10/11 video còn lại chỉ 1k–59k — kém ổn định hơn Lane K
  (iyaku_labo có 4/4 video full đều mạnh). Không phải outlier chắc chắn bền, cân nhắc khi chọn tập đầu.

## 3. TÀI LIỆU — đọc theo thứ tự này, đường dẫn thật trên máy 1
1. `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\GIAO_VIEC_SHAKAI_NO_URAGAWA_2026-09-24.md` — hồ sơ giao việc gốc
   (cảnh báo phân loại, 11 video, còn treo).
2. **`E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\channel_dna\shakai_no_uragawa\CHANNEL_DNA.md`** — DNA CHUẨN
   (K1+K2, cùng tool đã chạy cho Lane K), QC 11/11 đạt, kèm `VIDEO_ANALYSIS\*.json` cho 8 video. **Đọc bản
   này TRƯỚC** khi viết profile — phát hiện quan trọng: nhân vật さくら (Sakura), CTA cố định 6/7 video, câu
   chuyển cảnh cố định 「その答えは〜に隠されていた。時は少し遡る——」(dịch: "câu trả lời ẩn trong câu chuyện
   của.../ hãy lùi lại một chút thời gian—"), nhịp twist mỗi 60–90 giây.
3. `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\SHAKAI_NO_URAGAWA_CHANNEL_REPORT.html` — báo cáo đọc bằng mắt:
   công thức tiêu đề (なぜ〜のか/〜の理由/〜の末路とは, luôn có 【漫画】 — độ dài đo lại 21–35), công thức mô tả, hook
   0–30s của 5 video (2 kiểu: scene giấu lý do / stat_reversal), cấu trúc thumbnail (băng đen 3 màu vàng/đỏ/
   trắng, chữ thumbnail VIẾT LẠI không chép nguyên tiêu đề — khác iyaku_labo). Artifact online:
   `https://claude.ai/artifact/P7H4y3cuHM6XFd2fdv6dAP`.
4. `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\shakai_no_uragawa\` — dữ liệu thô: `channel.json`, `thumbs\*.jpg`,
   `transcripts\*.json` (11/11 video có transcript qua proxy).
5. `assets\shakai_no_naze\branding\KENH.json` — tên/handle/mô tả/keywords/hashtag đã lên kênh (nguồn chân lý
   branding — **keywords/hashtag hiện là em SUY LUẬN, chưa đối chiếu `channel_keywords` thật của kênh mẫu**).
6. Khuôn để chép (sửa 24/09 sau khi xem video thật): **`docs\SOP_LANE_K.md` + `profiles\profiles\yakkyoku-sukatto.json`**
   (đa giọng, N vai/tập, hộp chữ dọc + bóng thoại máy vẽ). `structure_block` vẫn viết MỚI theo 5 giai đoạn ở mục 1.
7. Luật toàn dự án: `CLAUDE.md` (router + ⛔ Claude chỉ làm BƯỚC 1, không render, không tự upload-job lần đầu;
   toàn bộ mục HOOK 2026-09-23/24 + "XONG TẬP = GHI SHEET NGAY") · `docs\QUY_TRINH_SETUP_KENH.md` (đã làm) ·
   `docs\QUY_TRINH_TAO_KICH_BAN_MOI_LANE.md` (luồng lean, hook bắt buộc, cổng S1L) — lane L nên khai
   `flow="lean"` ngay từ đầu như mọi lane mới sau 20/09.

⚠️ Hook bắt buộc khoá trước S2 (video sinh) — Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn), dài ≈ hook gốc —
`E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. Luật hook cũ đã xoá. Cổng S1L (hook+gói đăng+promise.txt) chặn CỨNG trước khi viết.

## 4. QUY TRÌNH — làm bước nào trước
### Giai đoạn 2 — dựng hạ tầng lane (1 LẦN, đúng thứ tự, xong mới sang giai đoạn 3)
1. **Copy DNA đã có sẵn**: `TRENDING-RESEARCH\docs\channel_dna\shakai_no_uragawa\` → `docs\channel_dna\
   shakai_no_naze\` (đặt tên thư mục theo mã lane cho nhất quán với các lane khác).
2. **HỎI ANH chốt giọng** (nghi vấn mục 1): 1 giọng kể xuyên suốt, hay tách riêng giọng người kể + giọng Sakura
   khi có câu hỏi trực tiếp trong ngoặc kép.
3. **Đối chiếu keywords/hashtag branding với `channel_keywords` thật** trong `TAG_STATS.json` của DNA (nếu K1
   có chạy `yt_tags.py`) — sửa lại `KENH.json` + chạy lại `--steps settings` nếu lệch nhiều so với 9 keyword
   hiện tại (em suy luận, chưa đối chiếu số liệu thật).
4. **Profile** `profiles\profiles\shakai_no_naze.json` (chép khuôn teinengo-real, sửa mạnh cấu trúc):
   `narrator` = kể chuyện + có 1 nhân vật phụ (Sakura) hỏi lặp lại · `script.mode = fiction_facts` (Sakura và
   tình huống cụ thể hư cấu, nhưng SỐ LIỆU/THUẬT NGỮ xã hội phải có nguồn thật — kênh này RỦI RO BỊA SỐ LIỆU
   cao nhất trong mọi lane vì bản chất là "giải thích bằng dữ liệu") · `script.structure` = 5 giai đoạn theo
   mục 1, KHÔNG dùng structure của F/G/K · `body.mode=ai_images` với TỈ LỆ ẢNH THẤP (xác nhận lại số ảnh/phút
   thật từ DNA trước khi đặt `seconds_per_image`) · `image.ref_lock=true` cho Sakura (xuất hiện lại MỌI tập,
   khác F/H/J chỉ khoá trong 1 tập — cần bàn có REF-LOCK XUYÊN TẬP không, giống hệ thống nhân vật xuyên suốt
   của satori/toshi) · `publish.sheet_tab="L-shakai-no-naze"` · `publish.upload_channel="shakai_no_naze"` ·
   `script.flow="lean"` · `script.hook.enabled=true` + `sfx=true` + `visual_kind="video_sinh"`.
   **`script.gate` PHẢI ĐO** từ 11 transcript thật trong `data\shakai_no_uragawa\transcripts\`.
5. **Char-rate**: `py -3.13 pipeline\calibrate.py --profile shakai_no_naze` sau khi chốt giọng ở bước 2.
6. **SOP** `docs\SOP_LANE_L.md` theo khuôn `SOP_LANE_F.md`: §0 bảng delta, **§0b Channel Analyzer** (đã có DNA
   sẵn, chỉ cần copy + ghi lại vào SOP), §0c giọng, §1 quyết định (đặc biệt: có REF-LOCK Sakura xuyên tập hay
   không), §1b danh sách 10 tập + quy tắc cột sheet, §2 lệnh chạy, §3 gate, §5b phân vai.
7. **Router**: 1 dòng bảng lane `CLAUDE.md` + 1 dòng `docs\DANH_BA_LANE.md` + cập nhật mục 2 file này.
8. **Danh sách 10 tập**: bám công thức tiêu đề なぜ〜のか/〜の理由/〜の末路とは + chủ đề xã hội đang nóng THẬT
   (không bịa số liệu — kiểm tra được), tránh trùng 11 tựa đã có của kênh mẫu. Ưu tiên chủ đề gần với video
   431k (Z世代 tuyển dụng) nhưng KHÔNG trùng, vì đây là bằng chứng duy nhất kênh mẫu có outlier thật.

### Giai đoạn 3 — sản xuất 1 tập (CHỈ tập anh chỉ định "cho làm tập X")
1. Tạo `assets\shakai_no_naze\ep<NN>-<slug>\`, ghi cột C.
2. Hồ sơ đề tài: `competitor.txt` (1 transcript thật qua `retrieve_videos.py --dna-dir docs\channel_dna\
   shakai_no_naze --topic "..."`) + `series_ctx.txt` (số liệu/thuật ngữ xã hội Nhật CÓ NGUỒN kiểm chứng được
   — đây là lane RỦI RO BỊA SỐ LIỆU CAO NHẤT, viết hồ sơ đề tài kín trước khi viết, đừng để model tự điền).
3. `py -3.13 -X utf8 pipeline\make_video.py --profile shakai_no_naze --slug ep<NN>-<slug>` — luồng lean, chạy
   tới mốc anh cho phép (mặc định theo lane khác: kịch bản + QC, chưa ảnh/video).
4. Xong tập (phần máy 1) = **GHI SHEET NGAY**: tab `L-shakai-no-naze` cột D = `Đã giao máy 2` (+ K lệnh máy 2), cột H = `cần ảnh (N ảnh,
   ~Xđ)` khi tới lượt giao máy 2 — `pipeline\dong_goi_may2.py --job` tự ghi, KHÔNG hỏi "anh bấm giao".
5. Bước 3 = máy 2 nhận qua `FlowHandoff_local\results\video_render\shakai_no_naze\<slug>\`. Claude Code KHÔNG
   render (trừ hook theo quy tắc 24/09).

## 5. LUẬT CỨNG RIÊNG LANE (từ báo cáo mục 3–5)
- **Số liệu/thuật ngữ xã hội PHẢI có nguồn kiểm chứng được** — đây là ngách rủi ro bịa số liệu cao nhất trong
  mọi lane vì bản chất video là "giải thích bằng dữ liệu thật", khác các lane kể chuyện cảm xúc khác.
- Tiêu đề luôn có 【漫画】 + khuôn なぜ〜のか/〜の理由/〜の末路とは, **21–35 ký tự** (đo 11 video: trung vị 27).
- Slide số liệu có chữ/số trên hình: máy vẽ từ `[Dn]`, KHÔNG để AI vẽ chữ số. Không chèn poster/ảnh có bản quyền.
- CTA cố định cuối video (dịch): "Từ nay kênh vẫn tiếp tục giải thích các câu hỏi 'vì sao' của xã hội qua
  truyện kể, mong mọi người đăng ký kênh và bấm thích."
- Câu nối sau hook 「その答えは…の物語の中にあった」 (câu trả lời nằm trong câu chuyện của…): 7/11 video, giây 56–136 —
  NÊN có nhưng không bắt buộc; 「時は少し遡る」 (hãy lùi lại một chút) chỉ 2/11, không phải luật.
- Thumbnail: chữ VIẾT LẠI súc tích/gây sốc hơn, KHÔNG chép nguyên tiêu đề (khác mọi lane khác copy thẳng).
- Nhân vật Sakura hỏi kiểu Socratic thay khán giả — giữ đúng vai trò "người hỏi", không biến thành nhân vật
  chính có cốt truyện riêng.

## 6. CỘT SHEET TAB `L-shakai-no-naze` (A→K, giống mọi lane khác)
A STT (= số ep) · B NỘI DUNG · C FOLDER · D KỊCH BẢN (tool tự ghi theo docsTRANG_THAI_COT_D_K.md; xong máy 1 = `Đã giao máy 2`) · E TITLE-DESCRIPTION · F TAGS
(không làm marker) · G THUMBNAIL · H STATUS-IMG (`cần ảnh (N ảnh, ~Xđ)` khi tới lượt giao máy 2) · I VIDEO ·
J LIST · K GHI CHÚ.
