# 📬 LANE INBOX — `teinengo-fuufu` (Lane J) · DNA kênh mẫu đã có

**Từ:** TRENDING-RESEARCH · **Ngày:** 2026-09-28 · **Trạng thái:** ✅ **SẴN SÀNG bắt đầu giai đoạn 2**

---

## 1. VIỆC CẦN LÀM NGAY

Hồ sơ nghiên cứu Lane J từ nay **KHÔNG còn mỏng**. Trước đây chỉ có **8 video** (Channel Analyzer K1+K2).
Nay đã có **47/47 video (100% kênh)**. Mở phiên mới cho Lane J:

1. **Đọc trước tiên:** `docs\nghien_cuu_lane_ban_da_kiem\channel_analysis_golo__teinengo-fuufu.json`
   (schema h2dev 22 khoá, 47 video, `ch_mult=2.65`, `trend=0.85`, `hit_rate=0.319`).
2. **DNA 11 mục:** `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\CHANNEL_DNA_GOLO.md`
3. **15 video ưu tiên:** `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\ORDER_15_VIDEO_UU_TIEN.md`
4. **15 hồ sơ video:** `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\VIDEO_ANALYSIS_GOLO\*.json`
5. Cập nhật `docs\BAT_DAU_LANE\teinengo-fuufu.md` mục 2 + 2b + 3 (đã làm 28/09).

⚠️ **Hồ sơ cũ `results\channel_dna\rougo-no-goro\` (8 video) vẫn dùng được nhưng MỎNG HƠN.** Vẫn phải copy
sang `docs\channel_dna\rougo-no-goro\` theo mục 4 giai đoạn 2 — nhưng khi mâu thuẫn thì **lấy bản 47 video**.

---

## 2. ⛔ BÁC BỎ KẾT LUẬN CŨ "KHÔNG THỂ CLONE"

> Lý do cũ: *"trend 0,42 < 0,6; ch_mult 2,65 < 3,0; median lệch Mean 4×; top3 chiếm 43,8%"*

| Chỉ số cũ | Số thật (tái lập 28/09) | Phán quyết |
|---|---|---|
| `ch_mult` **2,65 < 3,0** | `ch_mult = median_view ÷ subs = 28.881 ÷ 10.900 = **2,65**`. Ngưỡng **đúng cho lane là 2,0** (`src/find_lane_similar.py:71 CH_MULT_MIN = 2.0`). Số 3,0 là `CONSISTENT` của `explore_niches.py` — ngưỡng cho **luồng khám phá ngách mới**, KHÔNG phải thẩm định lane đã chọn | ✅ **ĐẠT** |
| `trend` **0,42 < 0,6** | **Không tái lập được với bất kỳ định nghĩa nào.** Theo định nghĩa h2dev (`median_recent_longform_views ÷ baseline`, xem `channel_analysis_rougo-no-kurashi__teinengo-real.json`): **trend = 0,85** (≤90 ngày, n=28). Theo VPD cùng cửa sổ ≤90 ngày: **+1,11** (n=28); còn ≤30 ngày thì **+3,75** (n=13) | ✅ **ĐẠT** |
| `median lệch Mean 4×` | mean/median = **4,05×**. Kênh ngách 60+ dạng "1 video nổ + đuôi dài" thì **2–5× là BÌNH THƯỜNG** — dấu hiệu **có video đột biến = bài học copy được** | ✅ **BÌNH THƯỜNG** |
| `top3 chiếm 43,8%` | top3 = **43,8%**. Kênh có **công thức lặp lại** thì phân bố lệch là **điều kiện để nhân bản**, không phải để loại | ✅ **BÌNH THƯỜNG** |

**Bằng chứng cộng thêm:**
- Cấu trúc **6 giai đoạn** giống nhau ở **47/47 video**
- `【漫画】` **47/47 (100%)** — định dạng đồng nhất tuyệt đối
- **4 nguyên nhân nổ/tụt ĐO ĐƯỢC trên 46 hook** (3,18× / 2,09× / 13,5× / 3,7×) → công thức kiểm soát được
- **1 narrator, 1 định dạng ảnh** (100% AI sinh manga anime) xuyên **7 tháng** → quy trình ổn định
- `hit_rate` **31,9%** (15/47 video ≥100k)

**→ Kết luận: CLONE ĐƯỢC. Không còn lý do kỹ thuật nào để hoãn giai đoạn 2.**

---

## 3. 4 LUẬT CỨNG MỚI (đã kiểm chứng trên 46 hook — dùng làm gate tập)

| # | Luật | Bằng chứng | Mức |
|---|---|---|---|
| 1 | **Mở bằng CẢNH**, không thuyết minh | nổ 4/5 = 0 câu thuyết minh; VPD median **905 vs 285 = 3,18×** | BẮT BUỘC |
| 2 | **BẮT BUỘC có ĐỐI CHỨNG** (同期/同じ日/隣/あいつ) | nổ 3/5, tụt 0/5; VPD median **1.098 vs 526 = 2,09×** | BẮT BUỘC |
| 3 | **Ngôi `俺`, CẤM `彼`** trong 150 ký tự đầu | VPD **65 vs 878 = 13,5×** | ⛔ TUYỆT ĐỐI |
| 4 | **CẤM chủ ngữ chung chung** (`男性`/`方々`/`高齢者`/`多くの人`) | tụt 3/5, nổ 0/5; chuẩn hoá **0,13 vs 0,48 = 3,7×** | ⛔ TUYỆT ĐỐI |
| 5 | **CẤM nhân vật trẻ hơn khán giả** | video `8xEY-fMffys` (58 tuổi) rel_VPD **0,10** dù rel_ENG **2,00** cao nhất | ⛔ TUYỆT ĐỐI |

**6 yếu tố ĐÃ ĐO và ĐÃ LOẠI** (không phải nguyên nhân): ngôi `俺` (6,9 vs 6,7), số tuổi (3,8 vs 4,1),
câu hỏi (6,0 vs 4,8 — TỤT còn nhiều hơn), số tiền cụ thể (3/5 vs 3/5), độ dài hook, thẻ định danh.

---

## 4. 💬 BÌNH LUẬN 15 VIDEO — ĐÃ GOM VÀ PHÂN TÍCH XONG (648 bình luận)

**Nguồn:** YouTube Data API v3 `commentThreads`, `order=relevance` · **phủ 15/15 video (100%)**
· **648 bình luận** · gom 28/09. Tài liệu: `scratch_golo\PHAN_TICH_BINH_LUAN_15VIDEO.md`
· dữ liệu thô: `scratch_golo\comments_15videos.json`.

### 4.1 🚨 PHÁT HIỆN QUYẾT ĐỊNH — KHÁN GIẢ **CHÊ HÌNH VẼ GIÀ** RẤT NẶNG

6/20 bình luận like cao nhất là **chê nhân vật vẽ già**:

| Like | Bình luận | Dịch |
|---|---|---|
| **446** | この絵は80歳ですね | "Hình này là 80 tuổi rồi" |
| **384** | この話しを作った人は、60代の人間は相当老人に見えてるんでしょうねー | "Tác giả nghĩ 60 tuổi là già lắm rồi" |
| **323** | いい話だけど老けすぎてない？ | "Chuyện hay nhưng vẽ già quá phải không?" |
| **252** | 今の60代 こんな昭和な感じの描き方は違うと思う | "60 tuổi bây giờ không vẽ kiểu Showa thế này" |

**3 LUẬT CỨNG MỚI cho khâu dựng hình (rút từ bình luận):**
1. **Nhân vật 60–65 tuổi PHẢI vẽ như 45–55.** Khán giả tự nhận mình trẻ
   (`今の65歳は40代に見える人も多い` = "65 tuổi nhiều người trông như 40").
2. **CẤM tóc bạc trắng + lưng còng + quần áo tối màu kiểu "ông bà già"** — bị gọi là `昭和の描き方`
   (kiểu vẽ thời Showa) = **lỗi thời, không thật**.
3. **Trang phục phải hiện đại, có gu** — bình luận 144👍: `服のセンスも見るに耐えない` (gu ăn mặc không nhìn nổi).

> ⚠️ **MÂU THUẪN CẦN LANE J CHỐT:** luật #5 ở mục 3 (CẤM nhân vật trẻ hơn khán giả) nói về **kịch bản**;
> phát hiện này nói về **hình vẽ**. Hai luật áp cho hai tầng khác nhau — nhưng cần chốt rõ để tránh
> người dựng hiểu lệch thành "vẽ nhân vật già".

### 4.2 🎯 CHỦ ĐỀ BÀN NHIỀU ≠ CHỦ ĐỀ TẠO LIKE CAO

| Nhóm chủ đề | Số BL | Tỷ lệ | Like cao nhất |
|---|---|---|---|
| LÀM VIỆC (tiếp tục hay nghỉ) | 167 | 25,8% | 236 |
| TIỀN / TÀI CHÍNH | 110 | 17,0% | 177 |
| MONG MUỐN / LỜI KHUYÊN | 86 | 13,3% | 231 |
| THÓI QUEN TỐT | 67 | 10,3% | 177 |
| **GIA ĐÌNH / CHỒNG VỢ** | 64 | 9,9% | **447** |
| "TÔI CŨNG VẬY" (đồng cảm) | 58 | 9,0% | 93 |
| CON CÁI / CHA MẸ | 36 | 5,6% | 134 |
| **CHÊ HÌNH VẼ GIÀ** | 18 | 2,8% | **446** |
| CÔ ĐƠN | 18 | 2,8% | 447 |

**⇒ Định hướng: đánh vào GIA ĐÌNH/CHỒNG VỢ (cảm xúc cực mạnh, like 447), KHÔNG phải LÀM VIỆC
(thảo luận nhiều nhưng like thấp).**

### 4.3 ⚠️ RỦI RO SỐ 1 CỦA LANE: **SỐ LIỆU TIỀN PHẢI ĐÚNG**

Khán giả 60+ **bắt lỗi kiến thức 3 lần** trên cùng 1 video:
- `年金は手続きしないと振り込まれません` (43👍) — **phải làm thủ tục mới nhận lương hưu**.
- `年金600万円？300万円で天井` (34👍) — **không thể có 600 man**.
- `年金15万で小遣い5万円て非現実的では` (9👍) — 15 man lương hưu, cho 5 man tiêu vặt: **vô lý**.

Còn 1 cảnh báo sức khoẻ: `２万歩って、10kmを軽く超えます…私は3か月で膝を壊し、２年間リハビリ` (32👍)
⇒ **đừng đưa con số vận động phi thực tế** (≤10.000 bước).

**⇒ Quy trình Lane J phải thêm bước: kiểm tra số liệu lương hưu/thủ tục với nguồn thật trước khi dựng.**

### 4.4 NGUYÊN LIỆU KỊCH BẢN SẴN DÙNG (bình luận thật, like cao)

| # | Nguyên liệu | Dùng vào |
|---|---|---|
| 1 | "Tôi bị cúm, chồng không giúp gì, suýt chết vẫn phải nấu ăn. **Tôi muốn sống một mình.**" (447👍) | **Hook** — chi tiết cụ thể, đau, ngôi "tôi" |
| 2 | "Chồng tôi **nói cảm ơn suông, nhưng không làm gì cả.**" (93👍) | **Đối chứng** — lời nói vs hành động |
| 3 | "**Thuê người làm việc nhà tốn bao nhiêu?** Vợ tôi làm không lương." (116👍) | **Con số** quy đổi công sức |
| 4 | "**'Tao nuôi mày'** ⇒ vợ chồng hết." (62👍) | **Câu chốt** gây phẫn nộ |
| 5 | "Làm đến khi không làm được, **coi như được trả tiền để tập thể dục**." (177👍) | **Góc nhìn tích cực** |
| 6 | "66 tuổi, làm hợp đồng, **cuối tuần vui như trẻ con**." (96👍) | **Kết bài** |
| 7 | "**Được người ta cần = ý nghĩa sống.**" (30👍) | **Thông điệp** |

**⚠️ Giới hạn:** API trả **tối đa 100 BL/video theo độ liên quan**, KHÔNG phải toàn bộ; video #1–#3
chạm trần 100. **Bình luận trả lời (reply) chưa gom.**

---

## 5. HỎI LANE J

1. **Giọng** — clone giọng kênh mẫu hay giọng kho? (chưa chốt ở `BAT_DAU_LANE` mục 1)
2. **Tập đầu** — đề xuất ep01 = `r4jNE1oTv8Q` (rel_VPD **17,33×**, dùng **4/4** tiêu chí hook) thay vì
   熟年離婚 VS 家庭内別居 như dự kiến cũ? Lý do: `r4jNE1oTv8Q` là **mẫu vàng đầy đủ nhất**, dùng được làm chuẩn
   cho các tập sau; còn 熟年離婚 đã được lane F phủ một phần.
3. **TRENDING-RESEARCH có cần thêm gì không?** (vd: bóc khung hình đo tỉ lệ slide/giây, lấy comment video hạng 5–10)

---

## 6. ⚠️ GIỚI HẠN TRUNG THỰC (đừng coi là bằng chứng tuyệt đối)

- **CHƯA đo được `retention`** — InnerTube API không trả. Nguyên nhân tụt **giữa** video chưa kiểm chứng.
- **CHƯA kiểm soát biến thời điểm** — 2/5 cặp đối chứng đăng cách nhau hàng tháng.
- **1/47 video** (`D39bUfMK4jQ`) không lấy được hook — bị chặn IP.
- Transcript qua proxy còn nhiễu STT (`豪華客戦`←`豪華客船`; `丁年`←`定年`).
- Thumbnail **KHÔNG** phân biệt được nhóm nổ vs nhóm tụt (đã đo).

---

## 7. FILE BÀN GIAO

| Vai trò | Đường dẫn |
|---|---|
| Hồ sơ phân tích kênh (schema h2dev) | `E:\CLAUDE\YOUTUBE\h2dev\docs\nghien_cuu_lane_ban_da_kiem\channel_analysis_golo__teinengo-fuufu.json` |
| Cửa vào Lane J (đã cập nhật) | `E:\CLAUDE\YOUTUBE\h2dev\docs\BAT_DAU_LANE\teinengo-fuufu.md` |
| DNA 11 mục | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\CHANNEL_DNA_GOLO.md` |
| 15 video ưu tiên | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\ORDER_15_VIDEO_UU_TIEN.md` |
| 15 hồ sơ video | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\VIDEO_ANALYSIS_GOLO\` |
| title_intel (đã nâng 47 video) | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\title_intel\teinengo-fuufu.json` |
| Giao việc YT-TITLE-RESEARCH | `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\docs\GIAO_VIEC_LANEJ_GOLO_2026-09-28.md` |
| **648 bình luận 15 video (thô)** | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\comments_15videos.json` |
| **Phân tích bình luận** | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\PHAN_TICH_BINH_LUAN_15VIDEO.md` |
| Script gom bình luận | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\scratch_golo\fetch_comments_15.py` |


## 📬 2026-10-01 — từ tab Lane F: KÊNH NGƯỜI GIÀ ĐỌC CHẬM + NGHỈ, ẢNH KHỚP TUỔI (anh chốt)
Anh chốt: kênh người già cho giọng đọc chậm lại một chút để có nghe và ngừng nghỉ, tránh nhọc; ảnh phải khớp tuổi.
Profile lane này đang `voice.speed`=1.0, `voice.pace`=false. Việc cho tab lane: đổi `voice.speed` → ~0.90 (GIỮ `char_rate_speed` = tốc độ lúc đo để `profiles.char_rate_at` tự quy đổi; chưa có thì ghi `char_rate_speed: 1.0`) + `voice.pace: true` (pace_audio nghỉ đúng chỗ dứt câu), sửa cả bản bundle máy 2 `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\buoc2_3_tool\profiles\teinengo-fuufu.json`. Video sẽ dài thêm ~15–20% → tính lại ngân sách phút tập mới. Ảnh REF: `E:\CLAUDE\YOUTUBE\h2dev\docs\QUY_TAC_REF_NHAN_VAT_TUOI_CAM_XUC.md`. Mẫu đã làm: Lane F `E:\CLAUDE\YOUTUBE\h2dev\profiles\profiles\teinengo-real.json` (`_pace_speed_note`).
