# LỖI ẢNH LỆCH LỜI — vì sao xảy ra và xử lý thế nào

> Viết 2026-09-12 sau khi soi tập `simbot2-04-Fgc8IQvQVj8` (B8Q chấm **3,1/5**, **5/14 mốc ≤ 2**).
> Đây **không phải lỗi của máy 2 sinh ảnh**, cũng không phải lỗi của AI chạy render. Nguyên nhân
> nằm ở khâu ghép, và nó là **lỗi đã biết, đã có cách chữa ở lane khác, chỉ là lane satori chưa bật**.

---

## 1. KẾT LUẬN NGẮN

`assemble.py` có **ba chế độ** gán thời điểm cho ảnh:

| Chế độ | Điều kiện | Cách chia | Độ chính xác |
|---|---|---|---|
| A | có `--anchors` **và** `--srt` | mỗi ảnh neo vào **đúng một câu** trong kịch bản | chính xác |
| B | chỉ có `--srt` | đổi cảnh rơi đúng **ranh giới câu**, nhưng **ảnh nào vào câu nào thì chia theo SỐ ĐẾM** | **trôi dần** |
| C | không có gì | chia đều theo độ dài audio | tệ nhất |

**Lane satori đang chạy chế độ B.** `render_engine.py` (dòng 249) gọi `assemble.py` với `--img`,
`--audio`, `--srt` — **không có `--anchors`**.

Chế độ B **không cắt giữa câu** (nên nghe không bị nấc), nhưng nó **không biết ảnh nào ứng với đoạn
nào**. Ảnh thứ k trong tổng N được đặt vào ranh giới câu ở khoảng k/N thời lượng audio. Còn **nội
dung** của ảnh thứ k là do bộ não vẽ storyboard ở khoảng k/N của **kịch bản**. Hai cái đó chỉ trùng
nhau khi mọi đoạn kể dài bằng nhau — điều không bao giờ đúng.

Chính chú thích trong `assemble.py` đã ghi (dòng 134–140):

> *"chia đều theo số đếm sẽ TRÔI dần về cuối video nếu các đoạn trước đó dài/ngắn không đều — đo
> thật (2026-09-11, ep01-ushijima-mitsuru): phục hồi đủ N ảnh KHÔNG sửa được trôi, vì gốc rễ là
> thiếu neo theo NỘI DUNG chứ không phải thiếu ảnh."*

---

## 2. BẰNG CHỨNG TỪ TẬP 04

| Số đo | Giá trị |
|---|---|
| Ảnh | 119 |
| Câu trong kịch bản | 251 |
| Trung bình | **2,1 câu mỗi ảnh** · **16,2 giây mỗi ảnh** |
| Sổ ghép ảnh ↔ lời (`img_meta.json`) | **không có** |
| File neo (`anchors`) | **không có** |
| B8Q khớp hình–lời | **3,1/5**, 5/14 mốc ≤ 2 |

**Phân bố các mốc lệch — dấu vân tay của lỗi trôi:**

`12:35` · `14:56` · `26:25` · `28:40` · `31:01` trên video dài ~32 phút.

**Ba trong năm mốc nằm sau phút 26**, tức dồn về cuối. Đúng đặc trưng của sai số tích luỹ: đầu video
lệch ít, càng về sau càng lệch nhiều. Nếu là lỗi ngẫu nhiên của người viết prompt thì các mốc phải
rải đều khắp video.

**Yếu tố làm nặng thêm:** `pace_audio.py` chèn khoảng nghỉ ở cuối câu, chỗ nhiều chỗ ít. Việc đó kéo
giãn một số vùng audio nhiều hơn vùng khác, làm phép chia theo số đếm càng lệch.

---

## 3. VÌ SAO KHÔNG PHẢI LỖI CỦA AI KHÁC

- **Không phải máy 2:** ảnh sinh ra đúng nội dung prompt. Kiểm 119/119 tấm: không trùng, không hỏng,
  đều do Flow sinh, không tấm nào phải vá.
- **Không phải AI chạy render:** nó gọi đúng lệnh trong quy trình. Lệnh đó vốn không có `--anchors`.
- **Không phải bộ não viết prompt:** prompt được viết khi **chưa có file giọng đọc**, nên không thể
  biết câu nào rơi vào giây thứ mấy. Prompt trong hồ sơ ghi rõ: *"voice.srt CHƯA có ở bước này là
  BÌNH THƯỜNG — cứ rải đều theo mạch kịch bản"*.

Nói cách khác: **cả ba khâu đều làm đúng phần việc của mình, nhưng không ai giữ mối nối giữa ảnh và
câu.** Thông tin đó chưa từng được ghi ra file nào.

---

## 4. LANE KHÁC ĐÃ CHỮA THẾ NÀO

| Lane | Cách chữa | Kết quả đo thật |
|---|---|---|
| **Lane D** (`irogatatarukioku`) | Thêm `--anchors` vào `assemble.py`: mỗi ảnh khai một **câu neo** trong kịch bản | B8Q **2,9/5 → 3,8/5**, hết mốc lệch |
| **Lane A** (`toshi-densetsu-jp`) | `khop_hinh.py` (B5K) chia lời thành đoạn ~15s, sinh `img_meta.json` ghi `t0`/`t1` cho từng ảnh | trước đó **43/141 cảnh (30%) lạc lời** mà B8Q vẫn báo 0 vấn đề |

Cả hai lane đều đã đi qua đúng vũng lầy này. **Lane satori là lane duy nhất chưa bật cơ chế neo.**

---

## 5. BA HƯỚNG XỬ LÝ

| | **A — Bỏ qua** | **B — Vá tay vài cảnh** | **C — Bật cơ chế neo** |
|---|---|---|---|
| **Làm gì** | Chấp nhận lệch, đăng luôn | Đổi chỗ / thay vài tấm ảnh ở đúng mốc bị nêu | Bộ não khai câu neo cho từng ảnh → `render_engine` truyền `--anchors` |
| **Mạnh** | 0 công, 0 tiền. Khán giả xem chuyện kể ít soi hình có khớp từng câu | Sửa đúng chỗ đau, không đụng code, ~15–30 phút/tập | Chữa gốc. Mọi tập sau tự khớp, không phải vá nữa |
| **Yếu** | Lỗi còn nguyên ở mọi tập sau, và **nặng dần về cuối video** — đúng đoạn cao trào | Chỉ chữa tập này. Tập sau lặp lại y hệt | Phải sửa prompt bộ não (thêm việc khai neo) + sửa `render_engine.py`. Tốn một lượt chạy thử để đo lại |
| **Rủi ro** | Cảnh cao trào chiếu nhầm hình làm hụt cảm xúc — thứ khán giả cảm được dù không chỉ ra được | Vá xong phải render lại phần ghép (~15 phút) | `render_engine.py` là file của riêng lane này nên không đụng lane khác; rủi ro thấp |
| **Chi phí** | 0 | ~15–30 phút/tập, không tốn quota bộ não | Một lần sửa code + prompt, cộng ~1 lượt chạy thử |

**Khuyến nghị: C, nhưng chưa vội.** Lý do: lỗi này **nặng dần theo số tập** — càng làm nhiều tập
càng phải vá nhiều. Chữa gốc một lần rẻ hơn vá mãi. Nhưng nó cần sửa prompt của bộ não, mà việc đó
nên làm khi có quota rảnh, không phải lúc đang gấp.

**Trước mắt cho tập 04 và 07: chọn A.** Mức 3,1/5 là "có liên quan nhưng lệch", không phải chiếu
nhầm hẳn sang chuyện khác. Xem `review-vi.mp4` rồi quyết — nếu xem thấy không gợn thì đăng.

---

## 6. CÁCH ĐỌC CẢNH BÁO QC CHO ĐÚNG

Hai cổng hay bị hiểu nhầm, cả hai đều **không chặn render**:

**B5Q "N/20 ảnh mẫu có vấn đề — có chữ đọc được".** Phần lớn là **báo động giả**: cổng cấm chữ để
chặn chú thích AI bịa, nhưng nó bắt nhầm cả chữ có thật trong cảnh (biển số xe, chữ trên thân xe cứu
thương, số phòng). Cách xử đúng: **mở đúng tấm bị nêu ra nhìn.**

| Thấy gì | Kết luận |
|---|---|
| Biển hiệu, biển số, số phòng **bằng tiếng Nhật** | không phải lỗi, bỏ qua |
| Chữ **tiếng Anh** trong bối cảnh Nhật (vd biển `Room 302`) | **lỗi thật** — sai tính bản xứ |
| Dòng chú thích lơ lửng, watermark, chữ nguệch ngoạc chồng hình | **lỗi thật** |
| **Mặt người nhoè bệt thành mảng** | **lỗi nặng nhất** |

**B8Q "khớp hình–lời N/5".** Đây chính là lỗi đang bàn trong file này. Thang điểm:

- **≥ 4,0** — tốt, đăng được
- **3,0 – 3,9** — có lệch nhưng còn liên quan; xem bản duyệt rồi quyết
- **< 3,0** — lệch nặng, nên vá trước khi đăng

---

## 7. ĐÍNH CHÍNH BÁO CÁO CỦA AI CHẠY RENDER TẬP 04

Em soi lại thực tế trên đĩa, có hai chỗ báo cáo ghi khác thực tế — **thực tế thì đúng, báo cáo ghi sai**:

- Báo cáo ghi *"Thư mục giao hàng: `E:\...\assets\satori_jp\simbot2-04-...`"*. Đó là thư mục **làm
  việc**, không phải thư mục giao hàng. Thực tế trên đĩa thì **đúng**:
  `E:\CLAUDE\YOUTUBE\CHANEL\Lopezzapa68\ep04-roujin-home-88\` — đủ 7 file (`final.mp4` 695 MB ·
  `review-vi.mp4` 347 MB · `thumbnail.png` · `listting.txt` · `listting.parsed.json` · `phude.srt` ·
  `tomtat.txt`). Cột G trong trang tính cũng đã ghi đúng đường dẫn này.
- Báo cáo kết luận cả 3 cảnh báo B5Q đều là báo động giả. Kết luận đó **có thể đúng**, nhưng cần
  soi theo bảng ở mục 6 — riêng **số phòng viết bằng tiếng Anh** thì là lỗi thật, không phải giả.

---

## 8. LIÊN QUAN

- `docs/QUY_TRINH_RENDER_VIDEO.md` — quy trình bước 3, giao cho AI khác chạy
- `pipeline/assemble.py` — ba chế độ chia thời lượng (`sync_durations` · `anchor_durations`)
- `pipeline/render_engine.py` dòng ~249 — chỗ gọi `assemble.py`, hiện thiếu `--anchors`
- `pipeline/khop_hinh.py` — cách Lane A giải bài toán này (sinh `img_meta.json`)
- memory `lane-d-anchor-sync-fix` — Lane D vá bằng `--anchors`, số đo trước/sau
- memory `cong-bo-qua-phep-kiem-quan-trong` — bài học B8Q từng tắt phép kiểm khớp lời, 30% cảnh lạc
  mà vẫn báo 0 vấn đề
