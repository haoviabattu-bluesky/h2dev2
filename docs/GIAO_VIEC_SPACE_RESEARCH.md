# QUY TRÌNH GIAO VIỆC CHO DỰ ÁN NGHIÊN CỨU — áp dụng cho MỌI lane

> Dựng 2026-09-10 sau tập đầu tiên nhận hàng thật từ `SPACE_RESEARCH`.
> Đây là quy trình **chung cho mọi kênh** sẽ mở trong dự án này, không riêng Lane A.
> Hợp đồng cụ thể của từng lane nằm ở **`profile.research`**, không nằm trong file này.

---

## 0. BÀI HỌC ĐẺ RA QUY TRÌNH NÀY

Dự án **đã có** hợp đồng bằng chữ từ đầu (`docs/KHUON_HO_SO_DE_TAI.md`). Hồ sơ đầu tiên vẫn sai 6
chỗ. Không phải bên kia ẩu — mà vì **không có gì kiểm hợp đồng đó**, nên mọi sai lệch chỉ lộ ra
sau khi đã tiêu tiền:

| Sai | Lộ ra ở đâu | Đã tiêu gì rồi |
|---|---|---|
| Tiêu đề 47 ký tự (ngưỡng 30–45) | B10, cuối cùng | giọng đọc + dựng xong video |
| `competitor.txt` 8,5′ cho video 28′ | không ai biết | cả lượt sinh kịch bản theo sai nhịp |
| 20 từ khoá hình không có hàng | sau 24 phút tải | 24 phút, ra 0 file dùng được |
| Tư liệu nói nửa chừng → model bịa | B3F | một lượt sinh kịch bản |

Và chỗ đau nhất: **khuôn của chính dự án này dạy sai.** `KHUON_HO_SO_DE_TAI.md` ghi mẫu
`TIÊU ĐỀ ĐÃ CHỐT (không đổi):` — bên research làm **đúng mẫu**, và mẫu đó tự tay tước quyền chỉnh
tiêu đề của bên làm video. Hợp đồng bằng chữ mà không có cổng thì đến lỗi của chính hợp đồng cũng
không ai phát hiện.

> **Luật rút ra:** giao việc ra ngoài thì mỗi điều khoản phải có **một phép đo**. Điều khoản nào
> không đo được thì đừng viết vào hợp đồng — viết vào cũng không ai giữ.

---

## 1. RANH GIỚI HAI BÊN — không được lấn

| | Dự án NGHIÊN CỨU | Dự án LÀM VIDEO (h2dev) |
|---|---|---|
| Chọn đề tài, đo cung/cầu | ✅ | ❌ |
| Tra nguồn, kiểm chứng dữ kiện | ✅ | ❌ (chỉ kiểm lại bằng cổng) |
| Khung chương, hook, CTA | ✅ | ❌ |
| **Đề xuất** tiêu đề | ✅ (3 phương án) | — |
| **Chốt** tiêu đề | ❌ | ✅ (còn phải khớp thumbnail) |
| Tải kho b-roll + ảnh bằng chứng | ✅ | bổ sung phần thiếu sau khi có kịch bản |
| Viết kịch bản | ❌ | ✅ |
| Giọng, ảnh, dựng, thumbnail, file đăng | ❌ | ✅ |

Nguyên tắc gốc: **bên đó CHỈ nghiên cứu, bên này CHỈ làm video.** Đừng viết kịch bản ở đó, đừng
đào tư liệu ở đây.

---

## 2. VÒNG ĐỜI MỘT ĐỀ TÀI

Trang tính điều phối: tab `gid=612920013`, cột **A** STT · **B** ĐỀ TÀI · **C** NỘI DUNG ·
**D** TÌNH TRẠNG · **E** FOLDER.

| # | Chặng (bên nghiên cứu) | Hình ảnh | Cột D |
|---|---|---|---|
| 1 | Sàng lọc nhiều đề tài ứng viên | **CHỈ DÒ API đếm kết quả — không tải file nào** | (trống) |
| 2 | Chốt 1 đề tài, viết hồ sơ | — | `DOING` |
| 3 | Hồ sơ xong | **TẢI** b-roll + ảnh bằng chứng vào `stock/` | `DOING` |
| 4 | Tự nghiệm thu đủ checklist | — | ghi **`DONE-READY`** |
| 5 | h2dev thấy `DONE-READY` → chạy **cổng B0** | | |
| 6 | B0 ĐẠT → sản xuất | | |
| 6' | B0 TRƯỢT → trả lại kèm danh sách | | về `DOING` |
| 7 | Đăng xong → chuyển thư mục sang `_DONE\` | | `PUBLISHED` |

**Cấm tải ở chặng 1.** Chặng đó có nhiều đề tài ứng viên; tải đến đâu thì 9 đề tài bị loại vẫn để
lại ~1,8 GB mỗi cái nằm chết trên ổ.

### ⚠️ `DONE-READY` từ nay mang nghĩa NẶNG HƠN
- **Trước:** "đã viết xong hồ sơ".
- **Nay:** "hồ sơ + kho hình đã sẵn sàng, bên kia cắm vào dựng được ngay."

Đây không phải chuyện chữ nghĩa. Cờ này là **thứ duy nhất báo bên kia đã ghi xong**. Đã dính thật:
chạy B0 lúc bên kia còn tải dở, thư mục có 9 file `.mp4` nhưng nạp được **1** — 8 file kia viết dở
nên ffprobe đọc không ra, bị loại lặng lẽ. Cổng in "kho gánh được 6 cảnh / cần 392", một con số
hoàn toàn sai mà nhìn y như kết luận thật. Chạy lại sau 2 phút: 9/9 bình thường.
→ `qc_hoso.py` nay tự cảnh báo nếu file mới nhất vừa ghi dưới 120 giây, nhưng **cờ vẫn là cửa
chính** — đừng vào lấy hàng chỉ vì "thấy có thư mục".

---

## 3. HỢP ĐỒNG NẰM Ở ĐÂU — `profile.research`

Giống hệt luật `body.mode` của phần dựng: **khác biệt giữa các lane là FIELD trong profile, không
phải nhánh `if` trong code.** Cổng B0 (`pipeline/qc_hoso.py`) đọc thẳng khối này làm ngưỡng.

```jsonc
"research": {
  "nguon": "SPACE_RESEARCH",
  "files_required": ["series_ctx.txt", "competitor.txt", "stock_queries.txt"],
  "competitor_ratio": [0.85, 1.30],      // × script.target_minutes
  "title_options_min": 3,
  "source_coverage_min": 0.90,           // tỉ lệ khối dữ kiện có 〔出典〕
  "blocks_required": ["【CHƯA KIỂM CHỨNG", "懐疑論", "MÓC VỀ"],
  "stock_queries_min": 12,
  "stock_by_chapter": true,
  "deliver_stock": true,
  "deliver_evidence": true,
  "evidence_min": 8
}
```

**Lane không khai `research` ⇒ lane đó không nhận hàng nghiên cứu**, B0 báo và thoát êm. (Ví dụ
lane `Lopezzapa68` satori: chuyện kể cảm xúc, không có dữ kiện cần kiểm chứng, không cần nguồn
ngoài.)

> Sửa hợp đồng = sửa JSON. **Không sửa `qc_hoso.py`.** Ngày nào phải mở code cổng ra để thêm luật
> cho một lane cụ thể là ngày hợp đồng bắt đầu rơi trở lại thành lời hứa suông.

---

## 4. CỔNG B0 — `pipeline/qc_hoso.py`

```
py -3.13 qc_hoso.py --folder "<...>\_READY\<nn>-<slug>" --profile <lane>
```

Chạy **trước khi copy hồ sơ vào thư mục tập**, ngay khi thấy `DONE-READY`.

| Kiểm | Vì sao chết người |
|---|---|
| Đủ file bắt buộc | thiếu là pipeline dừng giữa chừng |
| `competitor.txt` đúng dải phút | dạy sai nhịp ⇒ mất mốc chương, không cổng nào sau đó bắt được |
| ≥N phương án tiêu đề, ≥1 nằm trong `gate.title_len` | lệch dải ⇒ view thấp hơn 2,4 lần |
| Cảnh báo nếu hồ sơ ghi "ĐÃ CHỐT / không đổi" | tước quyền chỉnh tiêu đề của bên làm video |
| Đủ khối bắt buộc (`blocks_required`) | thiếu khối ⇒ chương đó không có nguyên liệu ⇒ model bịa |
| Đủ mốc chương `gate.chapter_markers` | pipeline không tự nghĩ ra khung chương |
| Độ phủ 〔出典〕 ≥ ngưỡng | khối không nguồn = không truy ngược được khi bị khiếu nại |
| Từ khoá hình đủ số, **chia theo chương** | danh sách phẳng dồn hết vào chương 1, đếm TỔNG vẫn "đủ" |
| **Kho gánh được ≥ số cảnh cần** | kho mỏng = lặp hình thấy rõ |
| `evidence.json` đủ mục, đủ 4 trường, **chỉ PD** | ảnh cháy màn hình sai giấy phép là rủi ro thật |
| Thư mục vừa được ghi < 120s | bên kia còn đang tải ⇒ mọi số bên dưới có thể sai |

**Cổng gọi chính code sản xuất.** Phần kiểm kho gọi thẳng `stock_cut.nap_kho()` + `suc_chua()` —
đúng hai hàm B5/B8 dùng. Nên "kho đủ" ở B0 nghĩa đúng là "B8 dựng được", không phải một phép đếm
gần đúng viết riêng cho cổng. Đây là điều kiện để cổng đáng tin.

---

## 5. MỞ LANE MỚI THÌ LÀM GÌ

1. Thêm khối `research` vào profile của lane. Ngưỡng lấy từ **đo thật kênh đối thủ**, không chép
   từ lane khác — xem `docs/` bài học "ngưỡng gate phải đo từ dữ liệu".
2. Thêm 1 dòng vào bảng ROUTER LANE ở `CLAUDE.md`.
3. **Sinh đơn đặt hàng** rồi bảo bên đó đọc đúng một file:
   ```
   py -3.13 pipeline\don_dat_hang.py --profile <lane>
   → E:\CLAUDE\YOUTUBE\SPACE_RESEARCH\DON_DAT_HANG_<lane>.md
   ```
   Đơn **sinh ra từ profile**, nên ngưỡng trong đơn và ngưỡng cổng B0 đọc **cùng một khối JSON** —
   không thể lệch nhau. Lỗi kinh điển của hợp đồng viết tay là bản gửi đi một đằng, bản đem ra
   chấm một nẻo. Sửa hợp đồng thì **sinh lại đơn**, đừng sửa tay vào file `.md`.
   Lane chưa khai `research` ⇒ đơn ra rỗng ngưỡng và tự cảnh báo — đó là đúng, không phải lỗi.
4. **Không sửa `qc_hoso.py`.** Nếu thấy cần sửa, nghĩa là điều khoản mới chưa được diễn đạt thành
   field — làm thành field trước.
5. Lane không cần nguồn ngoài thì **đừng khai `research`**. Không phải kênh nào cũng cần dự án
   nghiên cứu; kênh kể chuyện cảm xúc thì hồ sơ dữ kiện là gánh nặng vô ích.
6. **Lane thứ hai trở đi:** `CLAUDE.md` bên nghiên cứu hiện viết cho một kênh duy nhất (số liệu
   ngách, khung chương, giọng văn đều đóng cứng). Bảo họ **thêm mục lane riêng + bảng router**,
   đừng sửa đè — đúng cách h2dev đã làm. Mục 8 của đơn đặt hàng đã ghi sẵn dặn dò này.

---

## 6. TRẢ HÀNG LẠI — quy cách phản hồi

Trượt B0 thì **không tự sửa hộ**. Tự sửa hộ là bên kia không bao giờ biết mình sai, và tập sau sai
y hệt. Viết một file phản hồi đặt thẳng vào thư mục dự án bên đó:

```
<DỰ ÁN NGHIÊN CỨU>\PHAN_HOI_TU_H2DEV_<nn>-<slug>.txt
```

Mỗi lỗi viết đủ 4 phần, thiếu phần nào là phản hồi đó vô dụng:

1. **Số đo thật** — "22 phút/từ khoá, 0 file dùng được", không phải "hơi chậm".
2. **Hậu quả cụ thể ở sản phẩm cuối** — "thân video sẽ là thiên hà chạy dưới lời kể về chiếc
   Cessna", không phải "không phù hợp".
3. **Phải sửa thành gì** — câu lệnh, ngưỡng, khuôn file.
4. **Vì sao ngưỡng đó** — số đo hoặc lần dính thật. Ngưỡng không giải thích thì lần sau bị bỏ qua.

Kèm mục **ĐIỂM LÀM TỐT — GIỮ NGUYÊN**. Phản hồi chỉ toàn lỗi thì lần sau bên kia sửa luôn cả thứ
đang đúng. (Thật: cách trích nguyên văn kèm nguồn theo từng khối của họ chính là thứ giúp bắt được
lỗi bịa — nếu không nói rõ "giữ nguyên", rất dễ bị đổi mất.)

---

## 7. SỔ LỖI ĐÃ GẶP — đọc trước khi giao lane mới

| Lỗi | Gốc rễ | Nay chặn ở đâu |
|---|---|---|
| Tiêu đề 47 ký tự | **khuôn của mình dạy** "ĐÃ CHỐT (không đổi)" | B0 `tieu_de_ngoai_dai` + `tieu_de_khoa_cung` |
| `competitor.txt` 8,5′ | khuôn không nói độ dài | B0 `khung_ke_lech_do_dai` |
| Đề tài không có tư liệu hình | không ai dò trước khi chốt đề tài | cổng khả thi hình ảnh (bên đó) + B0 `kho_hinh_khong_du` |
| Từ khoá toàn ra ảnh CC BY-SA | không lọc giấy phép lúc TÌM | `_license_ok()` trong `stock_sources.py` |
| Tư liệu nói nửa chừng → model bịa năm/tên | thiếu luật "ghi đủ hoặc ghi thẳng là không có" | B3F + B0 `tu_lieu_thieu_nguon` |
| Thiếu khối phản bác | khung có chương mà tư liệu không có nguyên liệu | B0 `thieu_khoi_bat_buoc` |
| Chạy cổng lúc bên kia còn tải dở | không có mốc "xong" | cờ `DONE-READY` + B0 `ho_so_vua_moi_ghi` |
| Clip NASA 320×180 làm video nhoè | `rank` ưu tiên `mobile` | `stock_sources.py` — **đừng để ai đảo lại** |

---

## 8. LIÊN QUAN
- `docs/KHUON_HO_SO_DE_TAI.md` — khuôn từng file (nội dung hợp đồng)
- `pipeline/qc_hoso.py` — cổng B0 (phép đo của hợp đồng)
- `docs/SOP_TOSHI_DENSETSU_JP.md` — runbook lane A, bước 0 là chạy B0
- `CLAUDE.md` mục ROUTER LANE — chốt lane trước mọi việc
