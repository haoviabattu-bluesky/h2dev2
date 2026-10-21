# BẮT ĐẦU LANE N — `senior_korekara` · シニアの人生これから

> Anh nói **"thực hiện lane senior_korekara"** (hoặc "LANE N") → tab này ĐỌC HẾT file này trước, mở đầu báo cáo bằng
> `@lane:senior_korekara`, rồi làm ĐÚNG THỨ TỰ mục 4. Không tìm hiểu lại từ đầu, không đoán. File này là "cửa vào";
> chi tiết vận hành nằm ở SOP (mục 4 giai đoạn 2 sẽ viết). Cập nhật mục 2 mỗi khi trạng thái đổi.

> ⭐ **TẬP 2** → tab mới đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\senior_korekara_TAP2.md` (quy trình 30/09 — phần viết hook trong đó đã thay bằng luật 17/10 ở dưới;
> giao máy 3 soát, hook dựng tay theo câu, video hook xem thử phụ đề Việt). Tập 1 đã giao máy 2 lần 2 lúc 30/09 ~18:40 (hook anh viết lại, 18 clip).
> ⭐ **TẬP 1** (đã xong, giữ để tra) → tab mới đọc `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\senior_korekara_TAP1.md` (giao việc trọn gói máy 1 → máy 2,
> soát bằng ChatGPT web, không máy 3). Tên "Lane N" là tạm — anh đổi tên sau.

## ⚡ ĐỌC NHANH — "làm tập tiếp theo" (lane đã setup xong, mục 2 TRẠNG THÁI đã ✅ hạ tầng)
> ⛔ **Hook (21/10/2026): bám sát cấu trúc hook video gốc (gốc thế nào làm thế ấy, được đổi chút cho hợp/hay hơn)** — `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`
> Luật hook cũ đã xoá — THẮNG mọi dòng hook cũ (narrative intro / thoại
> xung đột / cảnh nhục trước / CẢNH XUNG ĐỘT CHO HOOK) còn sót ở file này, `senior_korekara_TAP1.md`, `senior_korekara_TAP2.md` và HUONG_DAN_TAP cũ.
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
| Mã lane / profile id | `senior_korekara` (thư mục `assets/N-senior_korekara/`; tab sheet `Lane-N` — đặt 28/09/2026 theo quy ước Lane M) |
| Kênh mẫu (clone) | シニアの人生これから · `@senior_korekara` · `UCL8PFGotC_jY_UbzfRTnnng` |
| Kênh thật | **03/10/2026: シニア暮らし研究所 · `@senior_kurashi60` · `UCqXxSE88mHQiZMvzCdlmk3w`** (mail `thienduongly7890@gmail.com`, AdsPower `k15wbjoo`; setup: `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\branding\KENH.json` + `E:\CLAUDE\YOUTUBE\h2dev\tools\channel_branding_ads.py`) |
| Format | Manga ảnh AI + slideshow tĩnh + narration ĐA GIỌNG, **6 chương có TÊN chứa số liệu**, ngôi 3 hoặc ngôi 1 theo tập, **mỗi tập một nhân vật mới** 60–70 tuổi sau nghỉ việc (việc làm thêm, hôn nhân tuổi già, chuyển đi, viện dưỡng lão, tiền, cô đơn) → thực tế phũ phàng dần → mất mát không lấy lại → **kết NGHIỆM TÙNG, không quả báo** |
| Giọng | Anh chọn (a) clone 2026-09-30: `clone_2669055` Nam B (dẫn mặc định) ✅ · `clone_2669056` Nữ C (mọi vai nữ) ✅ — anh duyệt 30/09 · `clone_2669111` Nam A (dẫn ngôi 1, bản A3) ✅ (`SOP_LANE_N.md` §0c) |
| Thư mục làm việc | `E:\CLAUDE\YOUTUBE\h2dev\assets\N-senior_korekara\` (tập = `ep<NN>-<slug>\`) |
| Khác lane nào | Bao trùm hơn F (chỉ tiền), G (chỉ vui chơi), J (chỉ vợ chồng), M (chỉ việc làm). Lane N = **toàn cảnh đời sống hậu nghỉ việc**. Khác K (dược sĩ cố định) vì **mỗi tập một nhân vật mới**. Kết **NGHIỆM TÙNG** chứ không cay đắng như F/K. |

## 2. TRẠNG THÁI (cập nhật mỗi lần đổi)

- ✅ 2026-09-28 nghiên cứu kênh xong (TRENDING-RESEARCH, tab nghiên cứu). Đã có:
  `docs\nghien_cuu_lane_ban_da_kiem\channel_analysis_senior_korekara.json` (**schema h2dev 22 khoá**, 28.540 ký tự) ·
  `docs\lane_inbox\senior_korekara.md` (hộp thư bàn giao) ·
  `docs\channel_dna\CHANNEL_DNA_KOREKARA.md` (DNA kênh đầy đủ, 126 dòng) ·
  `docs\nghien_cuu_lane_ban_da_kiem\ORDER_15_VIDEO_UU_TIEN.md` (**15 video xếp ưu tiên**) ·
  `docs\nghien_cuu_lane_ban_da_kiem\PHAN_TICH_BINH_LUAN_15VIDEO.md` (**779 bình luận** + nên/không nên).
- ✅ 2026-09-30 GIAI ĐOẠN 2 (setup nội dung) xong: profile `profiles\profiles\senior_korekara.json` · SOP `docs\SOP_LANE_N.md` ·
  `docs\channel_dna\senior_korekara\` (CHANNEL_DNA + COMMENT_INSIGHT + _raw 15 transcript) · 3 giọng clone (đã duyệt) + char_rate khởi điểm 382,8 ·
  tab sheet `Lane-N` 10 tập (A2:B11 + K2:K11) · file Project soát `CHATGPT_PROJECTS\N-senior_korekara-script\`.
- ✅ 30/09: 3 giọng chốt · kiểu chữ chốt (dọc, góc phải, lời kể ô vuông, thoại elip có đuôi, chữ đậm) · nhịp ảnh 7,5 s + cắt thẳng ĐÃ ĐO. ⏳ CÒN: kênh thật (anh) · cỡ chữ (anh chốt sau ep01).
- Kịch bản: CHƯA tập nào. "chạy tập X" → làm theo `SOP_LANE_N.md` §2.

## 2b. VÌ SAO KÊNH NÀY ĐÁNG LÀM (số liệu, đo 2026-09-28)

| Chỉ số | Giá trị | Ý nghĩa |
|---|---|---|
| Tuổi kênh | **73 ngày** | Cực non |
| Video | **64/64** (khớp `videoCount`) | ~6,1 video/tuần |
| Subscriber | 3.410 | |
| Median view | 6.929 | |
| Mean view | 26.616 | Lệch **3,84×** (`ch_mult`) — cần cẩn thận, Top1 chiếm 26,1% tổng view |
| **`trend_vpd`** | **14,61×** | **Video mới tốt hơn hẳn video cũ ⇒ thuật toán đang đẩy** |
| `ch_mult` | 3,84 | Thành công trải đều |
| Top1 | 443.785 view · VPD **49.309** (**290,7×** median VPD · **64,1×** median view) | |
| Top3 | 61,0% tổng view | |

**Kết luận: kênh ĐANG LÊN, 73 ngày đã có video nổ 443K view. Đáng clone ngay.**

## 2c. ⚠️ KHÁC BIỆT THEN CHỐT SO LANE J — ĐỌC KỸ

| | Lane N (kênh này) | Lane J (老後のゴローさん) |
|---|---|---|
| Bình luận về hình vẽ | **KHEN 27 · CHÊ 6 = 4,5:1** | Bị **6/20 top comment CHÊ hình vẽ già** |
| Kết thúc | NGHIỆM TÙNG 2,8% > quả báo 0,4% (**7,3:1**) | |
| Nhân vật | **Mỗi tập một nhân vật mới** | |

Khán giả khen nguyên văn: *"風景・情景が美しく描かれている！　こんなに綺麗な絵ははじめて！"* (19 like) ·
*"丁寧な作りの動画です"* (19 like).
⇒ **Lane N là kênh được khen VẼ ĐẸP. Nếu vẽ già hơn tuổi sẽ mất điểm mạnh nhất.**

## 2d. ⭐ ANH CHỐT 2026-09-30 + ĐO LẠI (tab lane N) — mục này THẮNG mục 1/2/2b nếu mâu thuẫn

**Luật nội dung (anh chốt):** mọi tập PHẢI ĐỔI NGHỀ NGHIỆP nhân vật chính so với video gốc — cấm dùng lại nghề cũ
(kể cả nghề của vợ/chồng nếu là nhân vật chính thứ hai). Đổi nghề thì đổi luôn chi tiết đi kèm nghề (số năm làm,
dụng cụ, câu thoại nghề). Nghề cấm từng tập ghi ở bảng dưới; khi dựng profile đưa vào `script_qc.lane_rules` +
prompt soát GPT web.

**10 tập đầu = view video gốc giảm dần (×trung vị = view/6.929).** Anh chấp nhận BẺ GÓC #1, #2, #9 (trùng Lane M việc
làm / Lane J tour mai mối) → kể thành truyện đời 1 nhân vật mới, kết nghiệm tùng, KHÔNG làm dạng list/xếp hạng.

| # | Video gốc | View · ×TV | Người dẫn gốc | ⛔ Nghề CẤM dùng lại |
|---|---|---|---|---|
| 1 | `G5kIPGFNKeY` シルバー人材センター | 443.785 · 64,1× | Nam A, ngôi 1 俺 | 電気部品会社の品質管理 38年 (QC linh kiện điện) · vợ パート惣菜 (bán thời gian đồ ăn sẵn) |
| 2 | `BdLooNSganA` 仕事ランキング7選 | 242.757 · 35,0× | Nam A, ngôi 1 俺 | công ty 42 năm (không nêu) · vợ 学校給食パート (bếp ăn trường) |
| 3 | `mbRCAib7xQM` シニア婚活パーティー | 142.953 · 20,6× | Nam B ngôi 3 | 縫製工場ミシン 42年 · 洋服のお直し (thợ may / sửa đồ) |
| 4 | `uUmbugIRmiY` 同窓会 | 109.064 · 15,7× | Nam B ngôi 3 | 自転車店 45年 (tiệm xe đạp) |
| 5 | `yTH_8ls9Jgg` 軽井沢移住 | 87.031 · 12,6× | Nam B ngôi 3 | 食品会社の総務 40年 · vợ 駅前の店パート |
| 6 | `qvUvnZwYR2w` 年金6万 vs 25万 | 76.880 · 11,1× | Nam B ngôi 3 | 大工 45年 (thợ mộc) |
| 7 | `SOIklzU69fg` 老人ホーム体験入居 | 68.984 · 10,0× | **Nữ C ngôi 1 私** | nội trợ, chồng đã mất (gốc không nêu nghề → tự đặt nghề rõ ràng) |
| 8 | `KY8NLrQguo0` 入居金1億円 | 58.557 · 8,5× | Nam B ngôi 3 | 精密部品メーカー元社長 (cựu giám đốc linh kiện chính xác) |
| 9 | `cu_DTPtgYHg` 婚活バスツアー | 44.651 · 6,4× | Nam B ngôi 3 | 工場で鉄を削る 40年 (thợ tiện) |
| 10 | `vfe1rz99eP0` キャンピングカー | 37.398 · 5,4× | Nam B (ngôi 1 私 xen ngôi 3) | 営業一筋 42年 (sales) |

**GIỌNG ĐỌC KÊNH MẪU — đo lại 2026-09-30** (resemblyzer + F0 trên 10 video tải thật; mẫu nghe ở
`E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_korekara\voice10\samples\`, số liệu `voice10\voice_report.json`):
- **Nam A** (F0 ~115 Hz) — dẫn 2 video ngôi 1 nổ nhất (#1, #2; 2 video này giống nhau 0,90, giống Nam B chỉ 0,67–0,78).
- **Nam B** (F0 ~110 Hz) — dẫn 7/10 video ngôi 3 (7 video giống nhau 0,79–0,89 ⇒ cùng 1 người).
- **Nữ C** (F0 ~185–220 Hz) — dẫn #7 (ngôi 1 nữ) VÀ lồng thoại MỌI nhân vật nữ trong 9 video còn lại (~10–25% thời lượng); 28 cụm giọng nữ gom về 1 người.
- Thoại nhân vật nam phụ phần lớn do chính người dẫn đổi giọng (giống 0,78–0,86); vài cụm chỉ giống 0,66–0,70 → có thể có thêm 1 giọng nam phụ, CHƯA chắc.
- ⚠️ Bằng chứng "người thật, jitter 17,56%" ở mục 1/DNA §3 đo trên `Scnn76gZ8E8` = video của kênh Lane J (老後のゴローさん), KHÔNG phải kênh này ⇒ vô hiệu. Người hay TTS: chưa kết luận.
- Người kể: 5/10 ngôi 1 (俺/私), 5/10 ngôi 3 mở bằng 「これは…の物語です」 — DNA ghi "ngôi 3" là sai một nửa. Transcript 15 video ĐÃ CÓ (`scratch_korekara\transcripts15.json`).

## 3. ĐIỀU NÊN / KHÔNG NÊN (tóm — chi tiết ở file bình luận)

**NÊN:** không kết hôn giấy tờ ở chủ đề hôn nhân tuổi già · cài chi phí THẬT · kết nghiệm tùng ấm ·
để nhân vật tự nhận ra · nhân vật là người tốt bị đối xử tệ · chương có tên + số liệu · ngôi 3 gọi tên nhân vật.

**KHÔNG NÊN:** ⛔ vẽ già hơn tuổi · ⛔ tiêu đề chỉ có 末路 mà không nêu tình huống (59,4% nhóm TỤT) ·
⛔ khoe kết quả đã đạt thay vì nêu vấn đề · ⛔ cốt truyện quá đẹp thiếu người xấu · ⛔ giọng đọc sai cảm xúc ·
⛔ để lỗi hình lọt ra · ⛔ nội dung trợ cấp/chính trị.

## 4. THỨ TỰ LÀM (khi anh ra lệnh)

- **Giai đoạn 2 (setup 1 lần)**: ✅ xong 2026-09-30 (mục 2).
- **Giai đoạn 3 — "chạy tập X"**: đọc `docs\SOP_LANE_N.md` §1b (tập X bám video gốc nào, nghề cấm/nghề mới) + §2 (lệnh đúng thứ tự)
  + `docs\channel_dna\senior_korekara\COMMENT_INSIGHT.md`. Tập theo thứ tự tab `Lane-N`; CHỈ tập anh chỉ định.
- Sau khi đăng: đo VPD sau 7 ngày, so median kênh mẫu **170 view/ngày**.
- (Mục cũ "ưu tiên LIST 7選" đã BỎ — anh chốt 30/09 bẻ góc #1 #2 thành truyện đời, không list, để khỏi trùng Lane M.)

## 5. NGUỒN DỮ LIỆU THÔ

Ở `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_korekara\`:
`scored64.json` (64 video + VPD) · `comments15.json` (779 bình luận) ·
`GRID_oZatkpZ0HEc.jpg` + `GRID2_Scnn76gZ8E8.jpg` (**29 khung hình THẬT** — bằng chứng định dạng ảnh) ·
`all_videos_raw.json`.
