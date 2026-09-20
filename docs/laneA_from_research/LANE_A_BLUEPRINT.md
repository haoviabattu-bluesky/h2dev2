# Lane A — Bản thiết kế sản xuất: ngách 都市伝説 / vũ trụ / bí ẩn

> Bóc từ 4 video top của **今夜も都市伝説** (`UCoFEha9rNMFqUio-4GQITfw`, 27 ngày tuổi,
> 6.300 sub, 666.347 view). Đo thật 2026-09-09: transcript đầy đủ + phát hiện cảnh bằng ffmpeg.

## 0. Ba phát hiện làm thay đổi cách làm

### 0.1 Tư liệu đến từ TIẾNG ANH, không phải tự nghĩ
7/8 đề tài của kênh mẫu là chuyện gốc phương Tây (Nibiru/Sitchin, Roswell, Boriska, Fátima,
Dienach, Thiaoouba, Edgar Cayce, Nikola Tesla). Nguồn cung tiếng Nhật chỉ **0–8 video/tháng**
trong khi view vẫn 3.000–68.000. **Mô hình kinh doanh = dịch & kể lại chuyện đã nổi bằng
tiếng Anh sang tiếng Nhật.** Tư liệu công khai, miễn phí, vô tận.

### 0.2 KHÔNG dùng ảnh AI — dùng video stock cắt nhanh
Trích khung hình thật từ 2 video top: toàn bộ là **clip stock/tư liệu lưu trữ** (người trong
văn phòng, tường gạch, trang Kinh Thánh, phóng tên lửa, mặt trăng, sóng âm trên màn hình),
cắt **12–16 lần/phút** (mỗi clip 3,7–5,0 giây), phụ đề tiếng Nhật cháy sẵn ở dưới, watermark
nhỏ góc trên phải. Hình ảnh chỉ là **B-roll trang trí**, không minh hoạ đúng nội dung đang kể.

> **❗ ĐÍNH CHÍNH 2026-09-10:** điều trên chỉ đúng với **THÂN video**. Soi 12 thumbnail top thì
> **thumbnail LÀ ẢNH AI** (UFO trên Trái Đất, người ngoài hành tinh đối thoại, Tesla dưới đĩa bay).
> → Thân video dùng stock rẻ, **thumbnail phải đầu tư ảnh AI**. Xem `LANE_A_NICHE_KIT.md` §3.

→ **Hệ quả lớn nhất: ở ngách này hình ảnh THÂN VIDEO không phải yếu tố cạnh tranh. Kịch bản mới là.**
Chi phí phần nhìn gần như bằng 0 (Pexels/Pixabay miễn phí). Pipeline ảnh AI của anh trở
thành **lợi thế nâng cấp**, không phải điều kiện bắt buộc.

### 0.3 Video dài = 2 câu chuyện ghép lại
Đánh số chương khởi động lại giữa video (`第1章` xuất hiện ở 3%, rồi lại ở 52–73%), và outro
xuất hiện 2 lần. Video 51–75 phút thực chất là **2 câu chuyện độc lập, mỗi cái 25–35 phút,
mỗi cái 5 chương**.

→ Anh chỉ cần làm được **1 câu chuyện 25–30 phút** (đúng năng lực hiện tại). Ghép 2 cái lại
là chuyện của khâu `assemble.py`.

## 1. Số đo kịch bản

| Chỉ số | Đo được | So với satori của anh |
|---|--:|---|
| Tốc độ đọc | **356–383 ký tự/phút** | 309 → **đọc nhanh hơn ~20%** |
| Kịch bản 1 câu chuyện 30 phút | **~10.700–11.500 ký tự** | 9.000–9.500 |
| Số chương/câu chuyện | **5** | — |
| Câu đảo chiều (しかし/ですが/ところが) | **34–54 lần/video** | — |
| Câu hỏi tu từ | 0,3–1,7 /phút | — |
| **Mốc năm cụ thể (1947年, 2004年…)** | **27–64 lần/video** (0,5–1,2/phút) | — |
| Gọi thẳng khán giả (あなた/皆さん) | 1–39 lần | — |

**Mốc năm là thứ tạo cảm giác "đã nghiên cứu kỹ".** Cứ ~1 phút một lần neo vào một năm,
một địa danh, hoặc một con số có đơn vị.

## 2. Khung 5 chương (bám đúng kênh mẫu)

```
HOOK 0-30s     Nói thẳng KẾT LUẬN gây sốc + neo vào ngày/nơi/người cụ thể
               vd: "1987年6月26日、オーストラリアの…58歳の牧場主が眠りから目を覚ました"
30-75s         Leo thang + HỨA phần thưởng
               vd: "この謎を追いかけていくと思いもよらない場所へたどり着きます"
第1章          Sự kiện gốc — kể như tường thuật, dày mốc năm
第2章          Nhân vật/tài liệu trung tâm — lai lịch, vì sao đáng tin
第3章          Bằng chứng + phản bác chính thống ("しかし…")
第4章          ⭐ MÓC NỐI VỀ NHẬT BẢN  (xem §3)
第5章          Diễn giải lớn: điều này nghĩa gì với hôm nay
KẾT 90s        Kéo về khung triết lý + nói thẳng với người xem
               vd: "選ぶのはあなた自身だ" → outro CTA cố định
```

## 3. ⭐ Chiêu bản địa hoá: LUÔN móc câu chuyện phương Tây về Nhật Bản

Có ở **cả 4/4 video**:

| Chuyện gốc (phương Tây) | Móc về Nhật |
|---|---|
| Thiaoouba (Úc/Pháp) | 和の精神, 4 mảng kiến tạo, "hòn đảo này là trung tâm" |
| Edgar Cayce (Mỹ) | 青森県戸来村 "mộ Chúa Jesus", 東の島 |
| Nikola Tesla (Mỹ/Serbia) | công nghệ Nhật, chiến hậu |
| Bí mật mặt trăng (NASA) | tàu かぐや, 竹取物語, "dân tộc kể chuyện về mặt trăng suốt ngàn năm" |

**Đây là giá trị gia tăng thật sự** — không phải bản dịch, mà là bản diễn giải cho người Nhật.
Đồng thời là chốt chặn chống bị nhận ra là nội dung dịch máy.

## 4. Số đo phần hình

| | Đo được | Ý nghĩa cho anh |
|---|--:|---|
| Nhịp cắt | 12–16 lần/phút | video 30 phút ≈ **360–480 cảnh** |
| Mỗi cảnh giữ | 3,7–5,0 giây | |
| Loại | clip stock + tư liệu lưu trữ | **KHÔNG cần ảnh AI** |
| Phụ đề | cháy sẵn, trắng viền đen, dưới giữa | `assemble.py` đã làm được |

**Hai lựa chọn cho anh:**
- **Rẻ & nhanh (giống kênh mẫu):** kho clip Pexels/Pixabay, tái dùng chéo video. Chi phí ~0.
- **Khác biệt (dùng lợi thế sẵn có):** ảnh AI minh hoạ ĐÚNG nội dung đang kể. Đắt hơn nhưng
  hơn hẳn về độ khớp — clip stock của họ chỉ là bức tường gạch trong khi lời kể nói về
  "tiền đề 2000 năm không ai nghi ngờ".
- **Khuyến nghị: bắt đầu theo cách rẻ.** Nếu kịch bản không giữ chân được người xem thì ảnh
  đẹp cũng không cứu; mà nếu kịch bản tốt thì stock đã đủ (145.972 view chứng minh).

## 5. Việc phải chuẩn bị

| Việc | Trạng thái |
|---|---|
| `fetch_script.py` bóc transcript **kênh Anh ngữ** làm nguồn tư liệu | ✅ dùng lại nguyên |
| Giọng nam trầm điềm tĩnh trong `channels.json` | ⬜ tạo mới + **đo lại char-rate** |
| Kho clip stock (Pexels/Pixabay) + script tự ghép theo timestamp | ⬜ làm mới (nhẹ) |
| Phụ đề cháy | ✅ `assemble.py` |
| Thumbnail chữ to | ✅ `thumbnail_text.py` |
| `topic_gap.py` chọn đề tài | ✅ đã dựng |
| Cổng QC B5RQ (khuôn mặt nhân vật) | ❌ **bỏ được** — không có nhân vật lặp |

## 6. An toàn nội dung

Ngách này dễ bị gắn cờ nếu viết như tin tức thật. Bám đúng mẫu câu của kênh mẫu:
`〜という説がある` · `〜とされています` · `〜かもしれません` · `もし本当だったら？`
(chính tiêu đề video 62k view của 極秘接触 dùng cụm cuối). Kênh mẫu dùng
`かもしれません` 8–23 lần/video — đó là lá chắn, không phải văn phong yếu.

## 7. Nguồn tư liệu

- Wikipedia EN: mục *Unexplained disappearances*, *UFO sightings*, *Unsolved deaths*, *Fringe science*
- Sách hết hạn bản quyền (Project Gutenberg, archive.org)
- Hồ sơ giải mật: CIA Reading Room, Project Blue Book (đã công khai)
- Kênh YouTube Anh ngữ cùng đề tài → `fetch_script.py` bóc transcript làm tư liệu thô
- Kiểm khoảng trống tiếng Nhật bằng `py -3.13 -X utf8 src/topic_gap.py`
