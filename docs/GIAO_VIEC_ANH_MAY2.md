# GIAO VIỆC VẼ ẢNH CHO MÁY 2 (Google Flow / Ultra) — chi tiết lane `stock_clips`

Máy 1 (h2dev) **ra đơn**, máy 2 **vẽ**, máy 1 **ghép + nghiệm thu**. Máy 1 không gọi gpti2 nữa.

> ⚠️ File này chỉ nói khâu **RA ĐƠN** (mục 1, máy 1 chạy) và **GHÉP LẠI** (mục 4, máy 1 chạy) +
> lý do kỹ thuật của lane `stock_clips`. Quy trình BÀN GIAO thật cho máy 2 (cột STATUS-IMG trên
> trang tính, Drive `jobs/results/shared`, cổng `qc_can_anh.py`, cách máy 2 nhận/trả việc) đã GỘP
> CHUNG cho mọi kênh vào **`docs/GIAO_VIEC_MAY2_ANH.md`** — đọc file đó trước (mục 2 "Loại B",
> mục 4 nhánh 6b/7b), file này chỉ bổ sung phần đặc thù lane. Job `ep01-valentich` (308 ảnh) đã
> qua cổng + đã `upload-job` thật lên Drive theo đúng quy trình đó, xem `GIAO_VIEC_MAY2_ANH.md`
> mục 4b.

---

## 1. Máy 1 ra đơn

```
py -3.13 pipeline\sinh_anh_canh.py --slug <thư mục tập> --chi-don
```

Sinh ra 2 file trong `<thư mục tập>\img_ai\` và **không vẽ tấm nào**:

| File | Nội dung |
|---|---|
| `prompts.txt` | mỗi dòng `<tên file><TAB><prompt tiếng Anh>` |
| `img_meta.json` | sổ ghép: tấm nào thuộc đoạn lời nào (`t0`/`t1` giây) |

Đơn của tập `01-valentich`: **308 ảnh**, đặt tên `001.png` → `308.png`.

## 2. Máy 2 vẽ

**Ba điều bắt buộc, sai là ghép hỏng:**

1. **Tên file phải đúng cột 1 của `prompts.txt`.** `001.png`, `002.png`, … `308.png` — ba chữ
   số, đuôi `.png`. Tên là thứ DUY NHẤT nối tấm ảnh với đoạn lời; máy 1 không đoán theo thứ tự.
2. **Khung ngang 16:9.** Máy 1 sẽ cắt về 1920×1080. Ảnh vuông hoặc dọc sẽ bị cắt mất chủ thể.
   Chiều ngang ≥1280 px.
3. **Thiếu tấm nào cứ báo, đừng đổi tên tấm khác thay vào.** Máy 1 bỏ đúng tấm thiếu, các tấm
   còn lại không bị lệch. Đổi tên để "cho đủ" là làm sai toàn bộ từ chỗ đó trở đi.

**Prompt dùng NGUYÊN VĂN cột 2**, đã gồm sẵn góc máy và phần đuôi phong cách. Đừng thêm chữ vào
ảnh, đừng thêm logo, đừng để lộ mặt người nhận dạng được — phần đuôi prompt đã ghi rõ.

Mỗi đoạn lời có 3–5 tấm cùng nội dung nhưng **khác góc máy** (wide / medium low-angle / close
detail / high angle). Đó là cố ý: một đoạn lời dài ~15 giây phủ 3–4 cảnh, dùng một tấm cho cả
đoạn thì hình đứng chết 15 giây.

## 3. Trả hàng

Chép toàn bộ `.png` vào đúng `<thư mục tập>\img_ai\`. Không cần sửa `img_meta.json`.

## 4. Máy 1 ghép + nghiệm thu

```
py -3.13 pipeline\make_video.py --profile <lane> --slug <tập> --from B8
```

`stock_cut.gan_anh_ai()` đọc `img_meta.json`, ghép **theo tên file**, dán nhãn 「イメージ（再現）」
lên mọi ảnh AI (máy 2 KHÔNG cần tự dán). Rồi `qc_canh.py` chấm **100% số cảnh**: mỗi cảnh một
khung hình + đúng câu đang đọc lúc đó, hỏi model vision xem hình có thuộc về khoảnh khắc đó
không. Trần lạc 3% — quá thì dừng, trả lại danh sách mốc giây cần vẽ lại.

---

## Vì sao chỉ vẽ một phần, không vẽ hết mọi cảnh

Thân video là **clip stock thật** (0đ, có chuyển động). Chỉ những đoạn lời nói tới **vật/nơi/thiết
bị xác định** (`CU_THE`) mới cần vẽ, vì kho stock đời thường không có: `area 51 sign nevada` trả
về phố Las Vegas, `old radio transmitter microphone` trả về micro thu âm hiện đại. Đoạn chỉ cần
không khí (sa mạc, trời đêm, đường vắng) thì clip thật bao giờ cũng hơn ảnh vẽ.

Đo thật 2 tập:

| | ep03-bob-lazar | ep01-valentich |
|---|---|---|
| Kho stock lạc đề tài | 32% | 11% |
| Đoạn `CU_THE` cần vẽ | 75 | 77 |
| Ảnh | 295 | 308 (đơn đang giao) |
| Cảnh lạc sau khi ghép | 277 cảnh ảnh AI → **0 lạc** | — |

## Nhãn 「イメージ（再現）」 là bắt buộc, máy 1 tự dán

Ảnh vẽ trông như ảnh chụp thật, mà nội dung thường là **lời khai chính tập đó bác bỏ**. Phim tài
liệu thật luôn dán chữ "hình dựng lại" lên cảnh dàn dựng; bỏ nhãn là đúng thứ chính sách "nội dung
không trung thực" 2026 của YouTube nhắm tới. Dán cho MỌI ảnh AI, không chọn lọc từng cảnh. Ảnh
**bằng chứng thật** (PD/CC0) không bị đụng tới.
