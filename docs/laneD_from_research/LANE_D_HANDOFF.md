# BÀN GIAO SANG h2dev — Lane D: ảnh chiến tranh THẬT được AI tô màu (JP)

> ✅ **ĐÃ DUYỆT bởi user — 2026-09-10.** Xem trước đầy đủ (số liệu xác minh, toàn bộ 15 tập,
> transcript/comment thật, điều tra nguồn ảnh tư liệu, quy trình sản xuất, đặt tên/SEO):
> `https://claude.ai/code/artifact/001a8505-22de-4cd9-a460-dc65a9b8bab0`
>
> **Ranh giới dự án:** `TRENDING-RESEARCH` chỉ NGHIÊN CỨU. `h2dev` LÀM VIDEO.
> File này tự chứa. Nguồn: quét mở rộng 4 ngách (vũ trụ/huyền bí/vụ án/lịch sử) 2026-09-10,
> đào sâu API thật + transcript + comment + 15/15 thumbnail của kênh được chọn, điều tra
> nguồn ảnh tư liệu bằng web search thật (không suy diễn).

---

## 0. Kênh được CHỌN

# **色でたどる戦争の記録**
`youtube.com/channel/UCaj1dslbibbHEnOAOh0tyYw` — 15 ngày tuổi · 877 sub · 15 video · **trend 1,57 (đang lên)**

Mỗi tập là **1 bức ảnh đen trắng có thật** từ Thế chiến 2 được AI ước đoán màu và tô lại, kể chuyện
23–29 phút xoay quanh đúng khoảnh khắc trong ảnh đó — không phải "top 10 sự kiện", mà là chân dung
1 người/1 nhóm cụ thể, gắn số liệu chính xác.

**3 tập bứt phá đã xác nhận (76% tổng view của cả kênh đến từ 3/15 tập này):**
| Tuổi | View | Tiêu đề |
|--:|--:|---|
| 11 ngày | **45.918** | 【特攻】出撃2時間前、17歳は子犬を抱いて笑っていた |
| 8 ngày | **53.320** | 【昭和21年 上野駅】疎開から帰ると家も親もなかった |
| 6 ngày | **41.290** | 【沖縄戦】島の人の85%が柵の中にいた |

---

## 1. Vì sao chọn kênh này trên 4 ứng viên đã soi (quét mở rộng 4 ngách)

| Kênh | Tuổi | Sub | Trend | Kết luận |
|---|--:|--:|--:|---|
| **色でたどる戦争の記録** | 15d | 877 | **1,57 lên** | ✅ **CHỌN** — định dạng hoàn toàn mới, chưa đụng hàng Lane A/C |
| AIと人間の未来【ゆっくり解説】 (`UCPARPfCT78W3DhRYOkF67aA`) | 38d | 1.940 | 1,32 lên | Dự phòng — ngách vũ trụ/khoa học, an toàn hơn nhưng không có cú hit lớn nào |
| しんりゅうの日本紀行 (`UCgCJNufm5rhL86xpiRAPyTw`) | 135d | 12.800 | ~0,91 chững | View tuyệt đối rất cao (78k–137k/video) nhưng không còn mới, tranh vẽ minh hoạ chứ không phải ảnh tô màu thật |
| ゆっくり事件アーカイブ (`UCZ0rY8HfoWgfp8FnYGcRa5w`) | 505d | 10.900 | 1,31 lên | Ngách vụ án hình sự đã BÃO HOÀ (có kênh tới 797k sub) — quét 2 lượt ~12 từ khoá không tìm được kênh nào <200 ngày tuổi lọt sàng |
| ノリタケのミステリー解説 / 少しゾクッとする話をあなたに (huyền bí) | — | — | 0,17–0,23 **chết** | ❌ LOẠI — bẫy "1 video viral 266k–825k view che giấu kênh đã chết", xem [[bay-do-kenh-dang-chet]] |

**Link cả 4 ứng viên còn sống (bấm xem trực tiếp):**
- 色でたどる戦争の記録 (CHỌN): https://www.youtube.com/channel/UCaj1dslbibbHEnOAOh0tyYw
- AIと人間の未来 (dự phòng): https://www.youtube.com/channel/UCPARPfCT78W3DhRYOkF67aA
- しんりゅうの日本紀行 (dự phòng): https://www.youtube.com/channel/UCgCJNufm5rhL86xpiRAPyTw
- ゆっくり事件アーカイブ (thị trường bão hoà, không khuyến nghị): https://www.youtube.com/channel/UCZ0rY8HfoWgfp8FnYGcRa5w

**色でたどる戦争の記録 thắng vì 4 lý do:**
1. **Định dạng hoàn toàn mới** — chưa dùng ở Lane A (clip stock)/B (anime)/C (manga AI); pipeline hình ảnh thứ 3
2. **Công thức tiêu đề đã giải mã bằng bằng chứng thật:** 1 nhân vật cụ thể + số liệu chính xác → 41k–53k view; chủ đề trừu tượng/thể chế → 362–650 view (xem §3)
3. **Nguồn tư liệu ảnh đã điều tra thật, không suy diễn** (xem §7) — không phải kênh "chắc là clone được" mà đã kiểm chứng cụ thể 1 case
4. **Kịch bản mở đầu gần như copy-paste nguyên văn qua mọi tập** — có sẵn template tái dùng ngay (xem §3)

---

## 2. Định dạng nội dung — khác cả Lane A/B/C

| | Satori (đang chạy) | Lane A | Lane C | **Lane D (mới)** |
|---|---|---|---|---|
| Hình | Ảnh AI photorealistic | Clip stock | Tranh manga AI | **Ảnh THẬT lịch sử, AI tô màu lại** |
| Nhân vật | Cụ bà ngôi 1, lặp lại | Không | Người mới mỗi video | **Người có thật trong ảnh**, không lặp lại |
| Độ dài | 25–30 phút | 25–30 phút | ~18 phút | **23–29 phút** (dài nhất trong 4 lane) |
| Mật độ lời thoại | ~309 ký tự/phút | — | ~318 ký tự/phút | **~260 ký tự/phút** — CHẬM hơn hẳn, nhiều khoảng lặng nhạc nền |
| Chủ đề | Đời sống + triết lý | Bí ẩn/vũ trụ | Nghề nghiệp có thật | **Lịch sử Thế chiến 2 có thật** |
| Rủi ro riêng | Thấp | Chính sách trung bình | Thấp | **Chính trị/dân tộc chủ nghĩa** (xem §8) + **bản quyền ảnh** (xem §7) |

**Điểm khác biệt lớn nhất với mọi lane trước:** đây là lane DUY NHẤT phụ thuộc vào ảnh tư liệu **có thật**,
không sinh được bằng AI từ đầu — nên §7 (nguồn ảnh) là phần bắt buộc đọc kỹ nhất, quan trọng hơn cả kịch bản.

---

## 3. Cấu trúc kịch bản — kịch bản mở đầu gần như copy-paste nguyên văn qua mọi tập

Đọc transcript thật của 4 tập (kể cả 3 tập hit lẫn 1 tập vừa), đoạn "khai báo miễn trừ trách nhiệm AI tô màu"
xuất hiện gần như y hệt từng chữ ở phút đầu mỗi tập:

```
「まずこの1枚の白黒写真を見ていただけるだろうか？」
  → mô tả TỈ MỈ từng chi tiết trong đúng 1 bức ảnh (ai đứng đâu, cầm gì, mặc gì)

「この動画では当時の白黒写真をAIで補正し、色を推定して再現している。当時カラーカメラで
取られていたらこう映っていたかもしれない姿だ。細部の色は実際と異なる場合がある。注目して
欲しいのは色の性格さではなく、写真に映る人々の表情とその時代の空気だ。」
  (Dịch: "Video này dùng AI phục chế màu cho ảnh đen trắng thời đó — đây có thể là hình ảnh
  nếu khi ấy chụp bằng máy ảnh màu. Màu chi tiết có thể khác thực tế. Điều đáng chú ý không
  phải độ chính xác màu sắc, mà là biểu cảm con người trong ảnh và không khí thời đại đó.")

  → vào bối cảnh lịch sử + số phận nhân vật, đóng bằng số liệu chính xác
```

**Công thức lõi:** 1 ảnh thật + mô tả chi tiết ảnh (hook) → miễn trừ trách nhiệm AI tô màu (khối cố định,
tái dùng được) → bối cảnh lịch sử → số phận **1 người/1 nhóm cụ thể** → số liệu chính xác đóng lại.

**Bằng chứng công thức tiêu đề (từ toàn bộ 15/15 tập, không phải suy diễn):**
- **Thắng lớn** (41k–53k view): 【特攻】cậu bé 17 tuổi ôm chó con trước giờ cảm tử · 【上野駅】trẻ mồ côi 123.511 người · 【沖縄戦】85% dân bị dồn vào hàng rào kẽm gai — đều có **1 nhân vật/nhóm cụ thể + số liệu chính xác**
- **Thua đậm** (362–650 view): 【講和条約】lễ ký hoà ước (chủ đề thể chế) · 【風船爆弾】bom bóng bay (chủ đề kỹ thuật) — không có nhân vật cụ thể để đồng cảm

---

## 4. Định lượng bắt buộc

| Chỉ số | Đo thật (4 video top, API + transcript thật 2026-09-10) |
|---|---|
| Độ dài | **23–29 phút** (1.396–1.714 giây) — DÀI NHẤT trong 4 lane |
| Kịch bản | **~6.500–7.200 ký tự** — ÍT hơn độ dài gợi ý rất nhiều |
| Tốc độ đọc | **~260 ký tự/phút** — CHẬM hơn hẳn satori (309)/Lane C (318). **KHÔNG tái dùng thẳng tham số giọng cũ** — cần đo lại nhịp mới, nhiều khoảng lặng cho nhạc nền + ảnh tĩnh "thở" |
| Ảnh tĩnh/video | Ước lượng 1 ảnh chính + vài ảnh phụ minh hoạ bối cảnh, giữ lâu (Ken Burns pan/zoom bù cho ít ảnh) |
| Giọng | Giọng dẫn chuyện điềm tĩnh, trầm — có thể tái dùng hạ tầng TTS tiếng Nhật sẵn có, nhưng PHẢI đo lại char-rate vì nhịp chậm hẳn |

---

## 5. Thumbnail — template cố định, dễ sao chép khung

Đã tải + xem trực tiếp toàn bộ 15/15 thumbnail thật (`data/laneD_scan/thumbs_all/` +
`thumbsheet_all.png`). Template **giống hệt nhau tuyệt đối** qua mọi tập:

- Nền **đen**
- Dải **đỏ dọc bên trái** ghi "カラーでよみがえる" (Sống lại bằng màu sắc)
- **Ảnh tô màu** ở giữa/bên trái
- Tiêu đề **chữ trắng/vàng đậm** bên phải, kèm phụ đề số liệu màu khác bên dưới

**Kênh mới KHÔNG copy nguyên văn dải chữ "カラーでよみがえる"** (tránh trùng thương hiệu) — đổi
sang tagline riêng, ví dụ **「その色を見た者はいない」** hoặc **「AIが蘇らせた記憶」**, giữ nguyên
bố cục nền đen + dải màu dọc + ảnh giữa + chữ đậm bên phải.

---

## 6. Từ khoá & tiêu đề

**Công thức tiêu đề** (100% của 15/15 tập dùng đúng cấu trúc):
`【chủ đề ngoặc】{mô tả cụ thể 1 khoảnh khắc/nhân vật}——{twist/hệ quả}｜{số liệu chính xác}｜{tagline cố định}`

Ví dụ thật: `【特攻】出撃2時間前、17歳は子犬を抱いて笑っていた——翌朝、この写真に写る全員が帰らなかった｜残された最後の一枚｜実際の写真をAIフルカラー復元`

**Tagline cố định của kênh gốc là `実際の写真をAIフルカラー復元` — kênh mới KHÔNG copy nguyên văn**,
dùng tagline riêng đã đề xuất ở §10 (mô tả kênh).

**Từ khoá lõi:** tên sự kiện lịch sử cụ thể + số liệu (tuổi, số người, tỉ lệ %, ngày giờ chính xác) +
`実際の写真` / `AIカラー化` / `白黒写真 復元`

---

## 7. Nguồn ảnh tư liệu — điều tra thật, KHÔNG được bịa (phần quan trọng nhất file này)

Kênh lịch sử không được bịa ảnh. Đã bóc đúng tập hit #1 (【特攻】) để truy nguồn thật — không suy diễn.

**Case thật:** nhân vật là **荒木幸雄** (Araki Yukio), 17 tuổi, phi đội Cảm tử số 72. Ảnh chụp bởi phóng
viên Asahi Shimbun ngày 26/5/1945 tại sân bay Bansei (Kagoshima). Ảnh + di vật gốc lưu tại
**万世特攻平和祈念館** (bảo tàng thật, Minamisatsuma, Kagoshima — liên hệ được).

**Phát hiện pháp lý quan trọng:** Luật Bản quyền CŨ của Nhật (trước 1971) chỉ bảo hộ ảnh 13 năm kể từ
khi công bố. Hiệp hội Nhiếp ảnh gia Nhật Bản (JPS) xác nhận: **mọi ảnh công bố trước 1956 tại Nhật đã
hết hạn bản quyền** — tức phần lớn ảnh báo chí WWII Nhật về lý thuyết đã public domain. **KHÔNG chắc
chắn 100% cho mọi case** (ảnh chưa từng công bố, hoặc bảo tàng vẫn coi là tài sản riêng dù luật đã hết
hạn) — **bắt buộc xác nhận lại với người hiểu luật SHTT trước khi dùng ảnh nổi tiếng/nhạy cảm ở quy mô
sản xuất lớn.**

**6 nguồn ảnh đã kiểm chứng thật (đọc trang, xác nhận điều khoản, không đoán):**

| Nguồn | Chi phí | Cần xin phép? | Phù hợp chủ đề |
|---|---|---|---|
| **PICRYL.com / GetArchive.net** (gộp từ NARA — kiểm thật: search "Peleliu"/"Saipan" ra hàng nghìn ảnh USMC) | Miễn phí | Không | Trận đánh Mỹ-Nhật, tàu chiến, quân đội Mỹ |
| **沖縄県公文書館** (Okinawa Pref. Archives) | Miễn phí | Không (chỉ ghi nguồn "沖縄県公文書館所蔵") | 22.131 ảnh chiến tranh Okinawa đã số hoá — khớp thẳng chủ đề 沖縄戦 |
| **Thư viện Quốc hội Mỹ** (LOC) | Miễn phí | Không | Trại giam Manzanar (ảnh Dorothea Lange, chụp cho cơ quan liên bang) |
| **国立国会図書館デジタルコレクション** (NDL) | Miễn phí (mục "保護期間満了") | Không | ~336.000 tư liệu Nhật đã hết hạn bản quyền — dự phòng cho đề tài dân sự Nhật |
| **昭和館デジタルアーカイブ** (Showakan) | Miễn phí XEM, ảnh gốc "貸出不可" | **CÓ** — gọi 03-3222-2574 xin phép | Đời thường dân hậu chiến — xác nhận có đúng ảnh khớp chủ đề 上野駅 |
| Getty / AP / Kyodo / 毎日フォトバンク | Có phí (chưa rõ giá, phải liên hệ) | Không cần xin, chỉ cần mua | Phương án cuối khi 2 nhóm trên không đủ |

**Chia 15 chủ đề của kênh gốc ra 2 nhóm — tỉ lệ tìm ảnh khác hẳn nhau:**
- **Nhóm A (9/15 tập)** — chủ đề Mỹ-Nhật trên chiến trường (降伏調印, 沖縄戦, 戦艦大和, マンザナー,
  サイパン, ペリリュー島, 第442連隊...) → quân đội Mỹ chụp CÓ HỆ THỐNG, đã số hoá, public domain
  xác nhận. **Tỉ lệ tìm được ảnh: RẤT CAO.**
- **Nhóm B (6/15 tập)** — đời thường dân Nhật thuần tuý (特攻, 岸壁の母, 学童疎開, 上野駅...) →
  nguồn hẹp hơn, cần thời gian xin phép bảo tàng (chậm nhưng miễn phí) hoặc dò may rủi trong NDL.
  **Tỉ lệ tìm được: TRUNG BÌNH, cần thời gian.**
- **Trớ trêu:** 2/3 tập hit lớn nhất của kênh gốc (特攻, 上野駅) rơi đúng vào Nhóm B khó nguồn hơn —
  đánh đổi thật giữa "câu chuyện ăn khách nhất" và "nguồn dễ tìm nhất".

**Nếu không tìm được đúng câu chuyện gốc:** đây là kênh CLONE/REUP, không bắt buộc kể đúng y hệt
Araki Yukio hay đúng trẻ mồ côi ga Ueno. Giữ nguyên CÔNG THỨC ở §3 (1 ảnh thật + 1 người/nhóm cụ thể
+ số liệu chính xác), tìm **câu chuyện khác** cùng chủ đề có ảnh xác nhận sạch bản quyền trong 6 nguồn
trên — kho NARA/PICRYL riêng đã có hàng chục nghìn ảnh lính trẻ/tù binh/trẻ em thời chiến tương đương
về cảm xúc. Hết cả 5 nguồn miễn phí mới tính mua Getty/Kyodo.

**KHÔNG được làm:** tự sinh ảnh AI giả làm "ảnh lịch sử thật" — phá đúng thứ khiến kênh đáng tin, và
đã có 1 comment thật nghi ngờ nội dung là AI (§8) — thêm ảnh giả sẽ làm rủi ro mất lòng tin tăng gấp bội.

---

## 8. Quy trình sản xuất — đánh dấu rõ bước MỚI vs TÁI DÙNG

| # | Bước | Trạng thái |
|---|---|---|
| 1 | Tìm ảnh tư liệu gốc đen trắng có bản quyền sạch (theo §7) | **MỞ RỘNG** — Nhóm A tái dùng `stockfetch.py`, Nhóm B cần thêm NDL + quy trình xin phép Showakan vào tool |
| 2 | **AI tô màu ảnh** | **MỚI HOÀN TOÀN — CHƯA THỬ NGHIỆM.** Cần khác hẳn "sinh ảnh mới" — đây là tô màu GIỮ NGUYÊN 100% bố cục/chi tiết ảnh gốc. Ứng viên cần thử trước khi chốt: dịch vụ tô màu chuyên dụng (Palette.fm, MyHeritage Photo Colorization) HOẶC gpti2/imgstudio edit với prompt "colorize keep everything identical" (rủi ro: các model gen ảnh thường VẼ LẠI thay vì tô màu thuần, xem bẫy tương tự đã ghi trong skill `gpti2.md` — quality cao dễ làm mờ/sai chi tiết khi giữ nguyên ảnh gốc) |
| 3 | Viết kịch bản (theo §3) | **MỚI** — văn phong riêng ngách này (mô tả ảnh tỉ mỉ + miễn trừ trách nhiệm cố định + số liệu chính xác) |
| 4 | Giọng đọc tiếng Nhật (TTS) | **TÁI DÙNG** hạ tầng TTS + giãn nhịp đã có, nhưng **PHẢI đo lại char-rate** (§4 — nhịp chậm hơn hẳn Satori/Lane C) |
| 5 | Dựng video: ảnh tĩnh tô màu + Ken Burns pan/zoom + nhạc nền | **TÁI DÙNG** `assemble.py` — đơn giản hơn Lane A/C vì ảnh tĩnh là đủ, không cần animate/clip AI |
| 6 | Thumbnail | **MỚI nhưng đơn giản** — copy khung (nền đen + dải màu dọc + ảnh + chữ đậm), không cần ảnh AI sinh nhân vật, đổi tagline riêng (§5) |

**Rủi ro lớn nhất của cả pipeline nằm ở Bước 2 (tô màu) — chưa render thử lần nào.** Bắt buộc thử
nghiệm 3–5 ảnh mẫu trước khi cam kết lịch sản xuất 1 tập/ngày như kênh gốc.

---

## 9. Khán giả & rủi ro — trích nguyên văn comment thật

79 comment gốc (4 tập top). Khán giả là người Nhật trung niên/cao tuổi **có liên hệ gia đình thật với
chiến tranh** — xem để đối chiếu ký ức cha mẹ/ông bà, không phải xem giải trí đơn thuần.

> 「第二次世界大戦終戦後の話は、先日亡くなった父から何度も聞かされていました。…上野駅の戦争孤児の
> 話はよく聞かされていました。」(66👍, tập 上野駅)

**⚠️ Rủi ro 1 — vùng bình luận chính trị nhạy cảm:** một phần đáng kể comment lái sang chính trị/dân
tộc chủ nghĩa hiện đại (Mỹ chiếm đóng hậu chiến, căn cứ Okinawa hiện tại, quan hệ Nhật-Trung) — đặc
điểm CỐ HỮU của ngách lịch sử chiến tranh Nhật, không phải lỗi của kênh gốc. Kênh mới cần cân nhắc
khoá bình luận hoặc lọc kỹ nếu đứng tên khác.

**⚠️ Rủi ro 2 — nghi ngờ nội dung là AI (dù chỉ 1/79 comment, vẫn là tín hiệu QC thật):**
> 「服が何色か、男の子が立っているだとかいちいち解説しなくてもいいことをAIに読ませるだけの動画で
> 再生回数稼ぐとか、、」("Cứ diễn giải vặt vãnh... video kiểu này chỉ để AI đọc kịch bản câu view")

→ Kịch bản mô tả ảnh không nên quá thẳng/máy móc — cần văn phong biên tập viên thật, tránh liệt kê
chi tiết vô cảm.

**⚠️ Rủi ro 3 — tỉ lệ chuyển đổi subscriber rất thấp** (877/184.737 view ≈ 0,47%) — người xem đến rồi
đi, chưa giữ chân thành subscriber trung thành như Lane C.

**⚠️ Rủi ro 4 — nhịp sản xuất 1 tập/ngày liên tục 15 ngày không nghỉ** của kênh gốc là RẤT nặng —
h2dev cần đặt nhịp thận trọng hơn (2–3 tập/tuần) cho tới khi Bước 2 (tô màu) và Bước 4 (TTS nhịp mới)
ổn định.

---

## 10. QC & an toàn nội dung

**QC THÊM (bắt buộc, riêng cho Lane D — khác mọi lane trước):**
1. **Kiểm nguồn ảnh trước khi dùng** — mọi ảnh phải trích được nguồn cụ thể (bảo tàng/kho lưu trữ nào,
   theo bảng §7), không dùng ảnh không rõ gốc gác
2. **Kiểm tính xác thực lịch sử** — số liệu (số người, ngày giờ, tỉ lệ %) phải khớp nguồn sử liệu thật,
   không bịa cho "ấn tượng" — đây là kênh dễ bị fact-check nhất trong 4 lane vì chủ đề nhạy cảm lịch sử
3. **Kiểm nội dung chính trị** — tránh đưa quan điểm chính trị hiện đại vào kịch bản/mô tả video (dù
   bình luận khán giả có thể lái sang đó, KÊNH không nên chủ động khơi mào)
4. **Kiểm văn phong mô tả ảnh** — tránh liệt kê chi tiết máy móc gây cảm giác "AI đọc kịch bản" (§9 rủi ro 2)

**An toàn:** rủi ro chính sách CAO HƠN Lane C (đời thường) nhưng khác loại rủi ro so với Lane A (bí ẩn/
siêu nhiên) — đây là rủi ro **bản quyền ảnh + nhạy cảm lịch sử-chính trị**, không phải rủi ro nội dung
giả/tuyên bố sai sự thật.

---

## 11. Đặt tên & SEO cho kênh mới

**3 phương án tên, đề xuất chính là #1:**

| # | Tên | Lý do |
|---|---|---|
| **1 (đề xuất)** | **色が語る記憶** | "Ký ức mà màu sắc kể lại" — gần tinh thần tên gốc nhưng không trùng, giữ từ khoá `色`/`記憶` |
| 2 | 白黒からよみがえる記憶 | "Ký ức hồi sinh từ đen trắng" — nhấn mạnh hành động phục chế, dài hơn nhưng rõ nghĩa |
| 3 | あの日の色 - AI復元記録 | "Màu sắc của ngày hôm đó" — ngắn, dễ nhớ, cần tag phụ làm rõ chủ đề lịch sử |

**Mô tả kênh (dán thẳng vào YouTube Studio):**
```
当時の白黒写真をAIで色付けし、その一枚に写る一人ひとりの物語を追います。
戦争・戦後・引き揚げ・収容所——教科書には載らない、名もなき人々の記録です。
色の正確さより、その時代の空気を伝えることを大切にしています。毎日更新。
```

**5 hashtag:** `#戦争の記録` `#AIカラー化` `#白黒写真` `#昭和史` `#実話`

**10 tag SEO:** `戦争 写真` `AI カラー化` `白黒写真 復元` `昭和史` `太平洋戦争` `実話 歴史`
`特攻隊` `戦争体験` `歴史ドキュメンタリー` `AIフルカラー復元`

Mỗi video khi đăng, thêm riêng 2–3 tag đúng sự kiện/nhân vật của video đó.

---

## 12. VIDEO ĐẦU TIÊN — checklist

| # | Mục | Nội dung |
|---|---|---|
| 1 | Chủ đề nhóm ưu tiên | Chọn từ **Nhóm A** (§7) trước — nguồn ảnh chắc chắn nhất để làm quen pipeline, vd 1 câu chuyện cụ thể trong trận Okinawa (nguồn 沖縄県公文書館 đã xác nhận có 22.131 ảnh) |
| 2 | Thử nghiệm Bước 2 (tô màu) TRƯỚC | Bắt buộc — chọn 3–5 ảnh NARA/Okinawa Archives thật, thử tô màu bằng 1–2 công cụ ứng viên (§8), so sánh chất lượng trước khi viết kịch bản đầu tiên |
| 3 | Tiêu đề mẫu | `【沖縄戦】{mô tả 1 người/nhóm cụ thể tìm được trong ảnh}——{twist}｜{số liệu chính xác}｜{tagline riêng, KHÔNG copy nguyên văn kênh gốc}` |
| 4 | Kịch bản | Theo khung §3 — hook mô tả ảnh tỉ mỉ → khối miễn trừ trách nhiệm (viết lại bằng văn phong riêng, KHÔNG copy nguyên văn) → bối cảnh → số phận nhân vật → số liệu đóng |
| 5 | Giọng đọc | Đo lại char-rate theo nhịp ~260 ký tự/phút (§4), KHÔNG dùng thẳng tham số Satori/Lane C |
| 6 | Thumbnail | Nền đen + dải màu dọc + ảnh tô màu + chữ đậm, tagline riêng (§5, §11) |
| 7 | Độ dài mục tiêu | 20–25 phút cho tập đầu (ngắn hơn kênh gốc 1 chút để giảm rủi ro trong lúc pipeline tô màu chưa ổn định) |
| 8 | Nguồn ảnh phải trích dẫn | Ghi rõ trong ghi chú sản xuất: ảnh lấy từ đâu (bảng §7), để tra soát lại nếu có khiếu nại |
| 9 | Chỉ số cần đạt | ≥5.000 view/7 ngày (thận trọng — kênh gốc mới 15 ngày, mẫu nhỏ, median thật chỉ 3.836) |

---

## 13. Dữ liệu gốc kèm theo

`E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\laneD_scan\`
- `channel_full.json` — toàn bộ 15/15 video (title/views/likes/comments/duration) lấy trực tiếp API 2026-09-10
- `deepdive_top4.json` — transcript đầy đủ + 79 comment gốc của 4 tập top
- `thumbs_all/` + `thumbsheet_all.png` — toàn bộ 15 thumbnail thật
- `prep_stats.json` — số liệu đã tính (trend, ch_mult, top3_share, sub_conv...)

Công cụ đi kèm: `deepdive.py`, `ytapi.py`, `innertube.py`, `stockfetch.py`, `stock_sources.py`
(copy từ dự án research — `stockfetch.py`/`stock_sources.py` cần bổ sung 3 nguồn Nhật mới ở §7
trước khi dùng cho Nhóm B).

---

## 14. Việc CHƯA làm — nói rõ để không tưởng đã đủ

- **Bước AI tô màu ảnh (§8 bước 2) CHƯA thử nghiệm lần nào** — đây là rủi ro kỹ thuật lớn nhất, bắt
  buộc thử trước khi cam kết lịch sản xuất
- **Chưa đo lại char-rate giọng đọc** cho nhịp chậm ~260 ký tự/phút
- **Chưa xin phép 昭和館** hay bất kỳ kho lưu trữ nào cần permission (Nhóm B, §7) — nếu chọn đề tài
  Nhóm B phải chủ động liên hệ trước, không giả định được duyệt
- **Chưa có xác nhận pháp lý chính thức** về việc ảnh báo chí Nhật trước 1956 đã hết hạn bản quyền áp
  dụng đúng cho từng case cụ thể — khuyến nghị hỏi người hiểu luật SHTT trước khi sản xuất quy mô lớn
- Mọi số liệu trong file này là **quan sát từ 1 kênh 15 ngày tuổi, 15 video** — mẫu rất nhỏ, cần theo
  dõi thêm sau khi kênh gốc chạy thêm vài tuần và sau khi h2dev ra 3–5 video đầu của chính mình
