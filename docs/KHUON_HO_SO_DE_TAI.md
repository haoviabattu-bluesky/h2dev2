# KHUÔN HỒ SƠ ĐỀ TÀI — thứ dự án research giao cho pipeline

> Đây là **hợp đồng giữa hai bên**: dự án research đưa RA đúng khuôn này, pipeline làm video ĐƯỢC
> ngay, không phải hỏi lại. Mỗi đề tài = 1 thư mục.
>
> ⚠️ **Khuôn này là NỘI DUNG hợp đồng. PHÉP ĐO của nó là `pipeline/qc_hoso.py` (cổng B0), ngưỡng
> khai ở `profile.research`.** Quy trình giao–nhận đầy đủ: `docs/GIAO_VIEC_SPACE_RESEARCH.md`.
> Sửa khuôn này mà không sửa cổng thì điều khoản mới sẽ không ai giữ — đã dính thật một lần: bản
> cũ của chính file này ghi mẫu "TIÊU ĐỀ ĐÃ CHỐT (không đổi)", bên research làm đúng mẫu, và mẫu
> đó tự tay tước quyền chỉnh tiêu đề của bên làm video. Không cổng nào phát hiện, tới B10 mới lộ.

## Vì sao phải có khuôn

Ở chế độ `script.mode = documentary`, mô hình **bị cấm tự nghĩ ra tên người, năm, địa danh, số
liệu** — nó chỉ được dùng thứ có trong tư liệu. Hệ quả trực tiếp: **tư liệu thiếu chỗ nào, mô hình
sẽ tự điền chỗ đó.**

Đo thật (video 多元宇宙, 2026-09-10): hồ sơ quên ghi phòng thí nghiệm của 外村彰 nằm ở đâu → kịch bản
đặt nó ở **埼玉県** trong chương 1 và **東京の西** trong chương 4. QC bắt được, nhưng phải chạy lại một
lượt sửa. Một dòng tư liệu thiếu = một lượt viết lại.

---

## 3 FILE MỖI ĐỀ TÀI

```
<slug>/
  competitor.txt   ← KHUNG KỂ  (transcript 1 video hay của kênh tham chiếu)
  series_ctx.txt   ← TƯ LIỆU SỰ THẬT (file chính, theo khuôn dưới)
  stock_queries.txt← từ khoá TIẾNG ANH để tải tư liệu hình
```

⚠️ **Hai file đầu KHÁC VAI TRÒ, đừng gộp.** `competitor.txt` dạy **nhịp và thứ tự dẫn dắt** —
không phải nguồn nội dung, và có thể là đề tài hoàn toàn khác. `series_ctx.txt` mới là nội dung.
Video dài của đối thủ thường là **2 câu chuyện nối nhau** (mốc chương khởi động lại ở giữa) → cắt
lấy MỘT câu chuyện.

---

## KHUÔN `series_ctx.txt`

```
ĐỀ TÀI: <tên đề tài>   (kèm số đo cung/cầu: bao nhiêu video cùng đề tài trong tháng qua, view trung vị)

TIÊU ĐỀ — 3 PHƯƠNG ÁN (đã đếm ký tự, GỒM CẢ khối tag 【】):
① <phương án 1>  (NN ký tự)
② <phương án 2>  (NN ký tự)
③ <phương án 3>  (NN ký tự)
→ Đề xuất mặc định: ①

HOOK 30 GIÂY ĐẦU:
<1-2 câu, nói thẳng kết luận gây sốc, neo vào NGÀY/NƠI/NGƯỜI cụ thể>

KHUNG N CHƯƠNG:
第1章 <...>
...
第4章 ⭐ MÓC VỀ <nước sở tại> — bắt buộc
第5章 <...>

CTA KẾT:
<câu hỏi ngỏ cho người xem>

======================================================================
TƯ LIỆU SỰ THẬT — CHỈ ĐƯỢC DÙNG NHỮNG DỮ KIỆN DƯỚI ĐÂY.
Tên người, năm, con số nào không có trong danh sách này thì KHÔNG ĐƯỢC VIẾT RA.
Chỗ nào không chắc thì diễn đạt định tính, tuyệt đối không bịa số.
======================================================================

【<Nhóm dữ kiện 1>】
・<năm>年<tháng>月<ngày>日、<nơi>で、<ai>が<làm gì>。<con số + đơn vị>。
・...

【<Nhóm dữ kiện 2>】
・...

【PHÍA PHẢN BÁC】
・<lập luận chính thống phản đối, ai nói, khi nào>

【MÓC VỀ <NƯỚC SỞ TẠI>】
・<khái niệm/sự kiện/nhân vật bản địa>, <năm/thời kỳ>, <nơi>
・<ranh giới>: chỗ nào chỉ được nói "giống nhau về hình thức", KHÔNG được nói "là một"

======================================================================
LƯU Ý VIẾT (bắt buộc)
======================================================================
・Mẫu câu lá chắn phải có ở mỗi chương: <liệt kê cụ thể theo ngôn ngữ>
・Gọi thẳng người xem CHỈ ở đầu và cuối
・Số liệu chỉ lấy từ hồ sơ này. Muốn nhân/chia/đổi đơn vị → viết cách khác để khỏi phải tính
・Điều CẤM nói: <tôn giáo/chính trị/y tế... tuỳ đề tài>
・Không viết teaser tập sau (nếu kênh làm video độc lập)
```

---

## 5 LUẬT KHI VIẾT TƯ LIỆU

1. **Mỗi dòng dữ kiện phải đủ 5 ô**: chuyện gì — năm — nơi — ai — số liệu. Thiếu ô nào, mô hình
   điền ô đó.
2. **Ghi cả cái mình KHÔNG biết.** Viết thẳng "không rõ địa điểm" còn hơn để trống — để trống là
   mời mô hình sáng tác.
3. **Kèm phía phản bác.** Ngách bí ẩn mà chỉ kể một chiều thì vừa dở vừa dễ bị gắn cờ. Chương
   "bằng chứng vs phản bác" cần nguyên liệu thật.
4. **Ranh giới của phần móc bản địa.** Nói rõ chỗ nào chỉ là "giống về hình thức" — nếu không,
   kịch bản sẽ tuyên bố hai thứ là một, và đó là câu bị bắt lỗi nhiều nhất.
5. **Số nào cũng phải tự kiểm được.** Cổng `qc_numbers.py` tính lại khoảng năm, khoảng tháng, tuổi
   theo năm sinh, phép nhân có đơn vị, hằng số quen thuộc, phần trăm. Sai là chặn ở B3Q.

## `stock_queries.txt`
Mỗi dòng một từ khoá **tiếng Anh** để tải tư liệu hình. Cần ~12–18 dòng cho một video 30 phút.

**CHIA THEO CHƯƠNG** bằng dòng `# 第N章 — <tên chương>`, mỗi chương ≥20 clip. Danh sách phẳng có
thể dồn hết vào chương 1 mà chương 4 trống trơn — đếm TỔNG vẫn thấy "đủ", chỉ khi dựng mới lộ.

**Phải DÒ THỬ API trước khi ghi vào hồ sơ**, đừng viết bằng suy luận. Đo thật: 20 từ khoá viết
bằng suy luận cho một đề tài hàng không → NASA 0, Commons chỉ ra ảnh tĩnh CC BY-SA (bị loại),
tốn 24 phút ra 0 file dùng được. Cùng bộ từ khoá đó qua Pexels: 6/6 clip HD, 24 giây/từ khoá.

## `evidence.json` (nếu lane bật `research.deliver_evidence`)
Ảnh cháy lên màn hình kèm chú thích nguồn. Ràng buộc CỨNG, khác hẳn b-roll:
**chỉ Public Domain / CC0** — không nhận CC BY, không nhận Pexels.

```json
[{"file": "ev01_vh-dsj.jpg", "caption": "セスナ182L（VH-DSJ）",
  "source": "https://…", "license": "Public domain",
  "accessed": "2026-09-10", "chapter": 1}]
```

## `stock/` (nếu lane bật `research.deliver_stock`)
Kho clip đã tải, kèm `manifest.jsonl` — **sổ giấy phép, mỗi file một dòng**. File nào không có
dòng trong manifest thì pipeline BỎ HẲN (không đoán bản quyền), nên đừng chép file vào bằng tay.
Ưu tiên từ khoá tả **CẢNH** (nebula timelapse, old laboratory, temple interior) hơn là tả **KHÁI
NIỆM** (multiverse, consciousness) — thư viện công cộng không có ảnh cho khái niệm, và tìm theo tên
riêng dễ ra thứ trùng chữ mà sai nghĩa (đã dính: tìm "Hugh Everett" ra tấm biển đường
"Everett Square, Massachusetts").
