# BÀN GIAO SANG h2dev — Lane A: ngách 都市伝説 / vũ trụ / bí ẩn (JP)

> **Ranh giới dự án:** `TRENDING-RESEARCH` chỉ NGHIÊN CỨU. `h2dev` LÀM VIDEO.
> File này tự chứa — h2dev không cần mở lại dự án research để làm video đầu tiên.
> Nguồn số liệu: 63 tiêu đề + 4 transcript đầy đủ + 190 comment + 12 thumbnail của 4 kênh
> Nhật đang lên, đo thật 2026-09-09/10.

---

## 1. Quyết định đã chốt (đừng bàn lại)

| | |
|---|---|
| Thị trường | **Nhật Bản** (user chốt) |
| Ngách | 都市伝説 / vũ trụ / bí ẩn — kể chuyện tài liệu 1 giọng dẫn |
| Kênh mẫu | **今夜も都市伝説** `youtube.com/channel/UCoFEha9rNMFqUio-4GQITfw` — 27 ngày tuổi, 6.300 sub, 25 video, **666.347 view** |
| Mô hình | Lấy chuyện đã nổi bằng **tiếng Anh** → kể lại tiếng Nhật → **luôn móc về Nhật Bản** |
| Video đầu tiên | **多元宇宙 (Multiverse)** — chỉ **1** video tiếng Nhật trong tháng qua mà được **31.694 view** |
| Nhân vật lặp lại | **KHÔNG CÓ** → bỏ REF-LOCK, bỏ cổng QC B5RQ |

**Vì sao chọn ngách này:** khảo sát 11 ngách / 4.000+ video. Ngách này có 9 kênh mới (<180 ngày) đang sống được, `median ch_mult` 3,0, và **không có nhân vật lặp lại** nên bỏ được khâu đắt + hay lỗi nhất của pipeline satori (khoá khuôn mặt).

---

## 2. Khác gì với SOP satori hiện tại — bảng delta

| Khâu | Satori JP (đang chạy) | **Lane A (mới)** |
|---|---|---|
| Người kể | Cụ bà ngôi 1 kể đời mình | **Người dẫn tài liệu ngôi 3**, nam trầm điềm tĩnh |
| Giọng | `ado` + age med + speed 0.92 | **giọng nam trầm** — phải chọn + **đo lại char-rate** |
| Tốc độ đọc | 309 ký tự/phút | **356–383 ký tự/phút** (nhanh hơn ~20%) |
| Kịch bản 30 phút | 9.000–9.500 ký tự | **10.700–11.500 ký tự** |
| Cấu trúc | mở cảnh → 伏線 → cao trào → 悟り | **5 chương đánh số 第◯章** |
| Hình thân video | Ảnh AI khoá nhân vật | **Clip stock/tư liệu**, cắt 12–16 lần/phút |
| Thumbnail | Ảnh nền + chữ to | **Ảnh AI** + 2 tầng chữ (xem §6) |
| REF-LOCK + QC B5RQ | Bắt buộc | ❌ **BỎ** — không có nhân vật lặp |
| QC B3Q (kịch bản) | Bắt buộc | ✅ **Giữ** + thêm kiểm SỐ HỌC (xem §9) |
| Nguồn nội dung | Bóc kênh Hàn simbot2 | **Wikipedia EN + kênh YouTube Anh ngữ** |

**Entry mới cho `pipeline/channels.json`:**
```json
"toshi-densetsu-jp": {
  "market": "JP", "language": "ja",
  "niche": "都市伝説/宇宙/ミステリー — kể chuyện tài liệu ngôi 3",
  "competitor": "https://www.youtube.com/channel/UCoFEha9rNMFqUio-4GQITfw",
  "narrator": "nam 40-50 tuổi, trầm, điềm tĩnh, nhịp đều — giọng dẫn phim tài liệu",
  "voice": "<CHỌN + ĐO LẠI char-rate>", "age": "med", "speed": 1.0,
  "note": "Không có nhân vật lặp lại giữa các video → KHÔNG dùng REF-LOCK, KHÔNG chạy QC B5RQ. Char-rate mục tiêu 356-383 ký tự/phút."
}
```
⚠️ **Bắt buộc đo char-rate của giọng mới 1 lần trước khi viết kịch bản** (bài học EP4 satori: viết 13.700 chữ ra 44 phút, phải viết lại).

---

## 3. Template kịch bản (bám đúng kênh mẫu)

```
[HOOK 0-30s]   Nói thẳng KẾT LUẬN gây sốc + neo NGÀY/NƠI/NGƯỜI cụ thể
               Mẫu thật: "1987年6月26日、オーストラリアの…58歳の牧場主が眠りから目を覚ました"
[ĐẶT KÈO 30-75s]  Leo thang + HỨA phần thưởng
               Mẫu thật: "この謎を追いかけていくと、思いもよらない場所へたどり着きます"
第1章  Sự kiện gốc — tường thuật, dày mốc năm
第2章  Nhân vật / tài liệu trung tâm — lai lịch, vì sao đáng tin
第3章  Bằng chứng + phản bác chính thống ("しかし…")
第4章  ⭐ MÓC VỀ NHẬT BẢN  (BẮT BUỘC — có ở 4/4 video kênh mẫu)
第5章  Diễn giải lớn: điều này nghĩa gì với hôm nay
[KẾT 90s]  Khung triết lý + nói thẳng với người xem
               Mẫu thật: "選ぶのはあなた自身だ" → outro CTA cố định
```

**Định lượng bắt buộc cho 1 video 25–30 phút:**
- 8.900–11.500 ký tự · 5 chương
- **`しかし / だが / ところが` mỗi ≤90 giây** — đo thật: 3–10 lần mỗi 5–7 phút, **chưa khoảng nào dưới 2**
- **~1 mốc năm hoặc số có đơn vị mỗi phút** (27–64 lần/video) — đây là thứ tạo cảm giác "đã nghiên cứu kỹ"
- Gọi `あなた` **chỉ ở đầu và cuối**, giữa video thì không

**Chiêu móc về Nhật (chương 4) — mẫu thật của kênh:**
| Chuyện gốc | Móc về Nhật |
|---|---|
| Thiaoouba (Úc/Pháp) | 和の精神, 4 mảng kiến tạo |
| Edgar Cayce (Mỹ) | 青森県戸来村 "mộ Chúa Jesus" |
| Nikola Tesla (Mỹ) | công nghệ Nhật thời hậu chiến |
| Bí mật mặt trăng (NASA) | tàu かぐや + 竹取物語 |

---

## 4. Khán giả — viết cho ai

190 comment gốc, 3 nhóm cùng ngồi một chỗ và **cãi nhau** (đó chính là động cơ tương tác):
- **Người TIN** (~35%, tâm linh + yêu nước): *"涙が溢れます…日本浄化の時ですね"* (87👍)
- **Người PHẢN BIỆN** (~6% nhưng like rất cao): *"その写真をアップロードしてください"* (86👍)
- **Người TƯ DUY** (~40%): *"全て地球基準なんだよね。前提が変わると可否も変わる"* (41👍)

**Nỗi đau khiến họ click:** cảm giác *có một sự thật lớn đang bị giấu khỏi mình*.

**⚠️ 0/190 comment nhắc "nghe khi ngủ / làm nền"** — khác hẳn ngách người già. Khán giả ở đây **xem chủ động**, nên nhịp phải chặt.

---

## 5. Tiêu đề — 8 công thức + số đo quyết định

| # | Công thức | Đo được | Mẫu thật |
|---|---|--:|---|
| 1 | Kết bằng **？** | **62%** | `なぜ他の文明は絶対に地球へ来られないのか？` (377k) |
| 2 | Bỏ lửng **…** | **51%** | `宇宙最大級の銀河がヤバすぎる…想像を超える驚きの大きさ` |
| 3 | Phủ định điều ai cũng tin | — | `UFOは宇宙人じゃない。答えは100年前に出ていた…` |
| 4 | Đặc quyền quốc gia | — | `日本だけが知っていた？「月の秘密」がついにバレ始めている` |
| 5 | Lời trăng trối nhân chứng | — | `予言者ケイシーが死の直前に残した一言の意味を読み解く` |
| 6 | Che giấu (`秘密/隠/封印/機密`) | 13% | `日本に隠されたキリスト宇宙人説の真相` |
| 7 | Giả định `もし〜だったら？` | 2% | `宇宙人が地球に墜落…もし本当だったら？` |
| 8 | Khối tag `【…】` cuối câu | — | `…【都市伝説 ミステリー 怖い話】` |

> ### ⭐ ĐỘ DÀI TIÊU ĐỀ — số đo quan trọng nhất
> | Độ dài | Số video | Median view |
> |---|--:|--:|
> | 0–30 ký tự | 16 | 17.371 |
> | **30–45 ký tự** | 11 | **34.288** ← nhắm khoảng này |
> | 45–60 ký tự | 18 | 14.056 ← **tệ nhất, tránh** |
> | 60+ ký tự | 18 | 25.886 |

**Khối tag SEO chuẩn của ngách:** `【都市伝説 ミステリー 怖い話】` (9/63 video dùng).

---

## 6. Thumbnail — 9 quy tắc + prompt ảnh AI

**❗ Thumbnail LÀ ẢNH AI** (khác thân video dùng stock). Đây là chỗ dùng `gpti2_gen.py`.

| # | Quy tắc | Tần suất |
|---|---|---|
| 1 | **2 tầng chữ**: trên nhỏ (tiền đề, vàng/trắng) + dưới TO NHẤT (cú sốc, đỏ/trắng viền đen dày) | 10/12 |
| 2 | Chữ chiếm **30–50% khung** | 12/12 |
| 3 | Nền **tối** (vũ trụ đen, xanh navy) | 12/12 |
| 4 | **●● che đáp án**: `核兵器ではなく●●だった` | 2/12 |
| 5 | **「」 trích lời**: `「月の裏側に鳥居がある」` | 4/12 |
| 6 | **Mũi tên đỏ** chỉ chi tiết | 3/12 |
| 7 | Ảnh AI cinematic, **không mặt người thật** | 11/12 |
| 8 | Chỉ 3 màu chữ: **đỏ + vàng + trắng** | 12/12 |
| 9 | Chữ overlay bằng PIL (`thumbnail_text.py`), **KHÔNG nhờ model render chữ** | — |

**Prompt ảnh nền mẫu (gpti2, size landscape 3:2):**
```
Cinematic dark space scene, dramatic volumetric lighting, deep navy and black
background with subtle nebula glow, high contrast, photorealistic, 8k,
[CHỦ THỂ: vd "two identical silhouettes facing each other across a mirrored
cosmic divide"], empty space on upper-left and lower-half for text overlay,
no text, no watermark, no people's faces in focus
```
⚠️ Chừa **khoảng trống** ở trên và nửa dưới cho chữ — model không biết chữ sẽ đè lên đâu.

---

## 7. Hình thân video — clip stock, KHÔNG phải ảnh AI

Trích khung hình thật từ 2 video top: toàn bộ là **clip stock/tư liệu lưu trữ**, cắt **12–16 lần/phút** (mỗi clip 3,7–5,0 giây). Hình chỉ là B-roll trang trí, **không minh hoạ đúng lời đang kể**.

→ Video 30 phút ≈ **360–480 cảnh**, nhưng chỉ cần **80–120 clip khác nhau** (mỗi clip cắt nhiều đoạn, tái dùng chéo video).

**Công cụ đã dựng sẵn ở dự án research** — copy sang h2dev nếu cần:
```
TRENDING-RESEARCH/src/stockfetch.py + stock_sources.py
py -3.13 -X utf8 src/stockfetch.py --q "black hole galaxy deep space" --n 8 --sources nasa,commons
```

| Nguồn | Giấy phép | Trữ lượng đo thật | Tốc độ |
|---|---|---|---|
| **NASA Image & Video Library** | **Public Domain** | `mars surface` 113 video/3.383 ảnh · `galaxy` 136/1.741 · `saturn` 114/4.237 | ✅ nhanh |
| **Wikimedia Commons** | PD/CC (ghi rõ từng file) | `moon surface` 16.372 ảnh · `nikola tesla` 8.950 | ✅ nhanh |
| Internet Archive | PD/CC (**phải lọc**) | 6.786 mục có giấy phép rõ | ❌ ~2,5 MB/phút, quá chậm |
| Pexels / Pixabay | Free commercial | clip đời thường (văn phòng, bàn tay gõ máy) | cần API key miễn phí |

**⚠️ Cạm bẫy bản quyền:** tìm `apollo` trên Internet Archive trả về **bản ghi truyền hình CÓ BẢN QUYỀN** (CSPAN2, FOXNEWS). Tool đã bắt buộc lọc `licenseurl`. **Mục nào không ghi rõ giấy phép thì bỏ, không đoán.** Mỗi file tải về ghi sổ `manifest.jsonl` (nguồn + giấy phép + tác giả) để truy ngược khi bị khiếu nại.

---

## 8. Nguồn tư liệu nội dung

**7/8 đề tài của kênh mẫu là chuyện gốc phương Tây**, cung tiếng Nhật chỉ 0–8 video/tháng.

- Wikipedia **EN**: *Unexplained disappearances* · *UFO sightings* · *Unsolved deaths* · *Fringe science*
- Sách hết hạn bản quyền: Project Gutenberg, archive.org
- Hồ sơ giải mật: CIA Reading Room, Project Blue Book
- **Kênh YouTube Anh ngữ cùng đề tài** → `fetch_script.py` bóc transcript làm tư liệu thô (tool này bóc kênh tiếng Anh tốt như tiếng Nhật)

**Kiểm khoảng trống trước khi chọn đề tài:**
`TRENDING-RESEARCH/src/topic_gap.py --topics config/topics_cases.yaml`

---

## 9. An toàn nội dung + QC

**Mẫu câu lá chắn (bắt buộc, kênh mẫu dùng 8–23 lần/video):**
`〜という説がある` · `〜とされています` · `〜かもしれません` · `もし本当だったら？`

**QC giữ lại từ SOP satori:** B3Q (kịch bản) · B4Q (giọng) · B5Q (loạt ảnh) · B8Q (video)
**QC BỎ:** B5RQ (khuôn mặt nhân vật) — không có nhân vật lặp

**⚠️ THÊM cổng kiểm SỐ HỌC vào B3Q.** Một comment **44👍** của kênh mẫu bắt lỗi sai phép nhân:
*"東京ドームの60倍が日本列島より大きい？200mの60倍は12kmだろが！"*
Ngách này khán giả soi số rất kỹ. Mọi phép tính, đơn vị, quy đổi trong kịch bản phải kiểm tay.

**⭐ Cơ hội vượt kênh mẫu:** 2 comment nhiều like nhất trong nhóm phản biện đều **đòi tấm ảnh mà video đã hứa** (*"かぐや chụp được cái torii đó — đưa ảnh ra đây"* 86👍 · *"không đưa được thì đừng gọi là chương trình"* 55👍). Kênh mẫu nói mà không đưa được bằng chứng hình. **Dùng `stockfetch.py` đưa ảnh NASA/Wikimedia thật kèm chú thích nguồn ngay trong video** → thắng đúng chỗ họ bị chê.

---

## 10. VIDEO 1 — 多元宇宙 (Multiverse) — checklist 12 mục

| # | Mục | Nội dung |
|---|---|---|
| 1 | Từ khoá chính | `多元宇宙 解説` (1 video/tháng, 31.694 view) |
| 2 | Từ khoá phụ | `パラレルワールド` · `量子力学` · `別の自分` · `都市伝説` |
| 3 | Tiêu đề | `別の宇宙にもう一人の自分がいる…物理学が否定できない理由【都市伝説 ミステリー 怖い話】` |
| 4 | Hook 30s | *「あなたが今下したその選択。別の宇宙では、逆を選んだあなたが生きている——これは空想ではなく、物理学が真剣に議論している話です」* |
| 5 | Thumbnail | Ảnh AI: 2 bóng người giống hệt soi gương qua vực vũ trụ · dòng trên vàng `物理学者が認めた` · dòng dưới đỏ viền đen `「もう一人のあなた」がいる` |
| 6 | Độ dài | 25–28 phút (~9.500 ký tự, kiểm theo char-rate giọng mới) |
| 7 | 5 chương | ①Thí nghiệm khe đôi ②Hugh Everett và diễn giải nhiều thế giới ③Bằng chứng vs phản bác ④**Nhật: 華厳宗 重々無尽 + 唯識** ⑤Nghĩa gì với lựa chọn hôm nay |
| 8 | Móc về Nhật | Tư tưởng 重々無尽 (Hoa Nghiêm) — vô số thế giới lồng nhau, có từ trước vật lý hiện đại hàng nghìn năm |
| 9 | Tư liệu | Wikipedia EN *Many-worlds interpretation*, *Hugh Everett III* · hình: `stockfetch.py --q "galaxy quantum nebula deep space"` |
| 10 | Mẫu câu an toàn | `〜という説がある` · `物理学者の中にはこう考える人もいます` · `もし本当だったら？` |
| 11 | CTA kết | *「あなたはどう思いますか？別の選択をした自分に、会ってみたいですか」* |
| 12 | Chỉ số cần đạt | ≥5.000 view/7 ngày · giữ chân 30s đầu ≥60% · ≥15 comment |

**4 video tiếp theo** (đã nghiên cứu, làm sau khi video 1 có số):
1. `ヴァレンティッチ失踪` — 1 video/tháng, 7.382 view · móc Nhật: 日航1628便 (1986)
2. `トラヴィス・ウォルトン` — 6 video, trần đã chứng minh **111.873** · móc Nhật: 神隠し
3. `ボブ・ラザー / エリア51` — 27 video nhưng **median 16.085**, cầu lớn nhất
4. Video "日本だけが知っていた" tự tạo — bám thế mạnh đặc quyền Nhật (kênh mẫu đạt 101k dạng này)

---

## 11. Dữ liệu gốc (nếu cần đào lại)

`E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\laneA\`
- `titles.json` — 63 tiêu đề + view + thời lượng của 4 kênh
- `transcripts.json` — 4 kịch bản đầy đủ (video 146k/125k/99k/99k view)
- `comments.json` — 190 comment gốc kèm số like
- `thumbs/` — 12 thumbnail top + `thumbsheet.png` (lưới ghép để xem một lượt)

Tài liệu đầy đủ: `docs/LANE_A_BLUEPRINT.md` (cấu trúc sản xuất) · `docs/LANE_A_NICHE_KIT.md` (8 mục nghiên cứu ngách)

## 12. Điều KHÔNG làm được — đừng tốn công thử lại

- **Retention của đối thủ**: đã thử 4 client InnerTube (WEB/ANDROID/TVHTML5/EMBED, cả `/next` lẫn `/player`), trang watch, và **cả phiên Chrome đã đăng nhập** — video kênh mẫu không có biểu đồ "most replayed". Comment cũng 0/190 nhắc mốc thời gian. Chỉ có retention **video của chính mình** trong Studio sau khi đăng.
- **Mọi con số trong file này là quan sát tương quan, chưa phải nhân quả.** Chỉ sau 5 video đầu mới biết công thức nào thật sự có tác dụng.
