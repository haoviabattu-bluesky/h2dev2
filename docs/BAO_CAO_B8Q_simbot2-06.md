# BÁO CÁO B8Q — ẢNH LỆCH LỜI TẬP simbot2-06-sYRr33eHYSM (STT 6)

> Ngày: 2026-09-12 · Người render: Hermes (bước 3, lane satori-jp-obaa)
> Log đầy đủ: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-06-sYRr33eHYSM\_render_06.log`

---

## 1. HIỆN TƯỢNG (đọc từ log, nguyên văn)

B8Q QC video:

```
=== VIDEO: 7 VẤN ĐỀ
   ✗ ẢNH LỆCH LỜI: trung bình 2.9/5, 6/14 mốc ≤2
   ✗   73s (2/5): The image shows a hospital corridor, not the mentioned closi | lời: 店を綺麗に畳んで、一人だけで、
   ✗   367s (2/5): A television morning news broadcast does not depict the wife | lời: 妻は六年前に、胃の重い癌を患い、
   ✗   508s (2/5): Shows a woman holding a parcel at an entrance, not items on  | lời: 縁側の板には、黄ばんだ型紙と、絹糸の
   ✗   1094s (2/5): Shows two people in a garden, not arranging flowers at an al | lời: 仏壇の花を、活け替えていて、
   ✗   1386s (2/5): Shows writing with a pen, not a swinging wall clock pendulum | lời: 柱時計の振り子が、狂ったように、揺れ始めました。
   ✗   1530s (2/5): Hospital room does not match narration about sharing home en | lời: 玄関の暗証番号を、互いに知っておき、
```

TÓM TẮT cuối log:

```
8. B7.5 neo ảnh↔lời: LỖI [0.0′]
10. B8Q QC video: OK [0.9′] === VIDEO: 7 VẤN ĐỀ
```

Các mốc khác (B4Q QC giọng, B10 nghiệm thu) đều ĐẠT. Video vẫn ra `final.mp4` (831 MB · 34 phút · 1920×1080).

---

## 2. NGUYÊN NHÂN GỐC (đã xác định, không phải đoán)

**Thiếu `img_doan.txt` → không sinh được `anchors.txt` → `assemble.py` chạy chế độ cũ (chia ảnh theo SỐ ĐẾM, chỉ hút về ranh giới câu theo THỜI GIAN) → ảnh trôi dần so với lời.**

Chuỗi bằng chứng trong log:

B7.5 (nguyên văn):
```
[STEP 8/13] B7.5 neo ảnh↔lời
  $ --slug E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-06-sYRr33eHYSM
    ✗ CHUA sinh duoc anchors.txt:
       - khong co img_doan.txt (bo nao chua ghi o buoc B5)
       → render se QUAY VE che do cu (chia theo so dem). Video van ra, chi la anh co the
         troi so voi loi ke. Sua img_doan.txt roi chay lai lenh nay.
  ⚠️ B7.5 neo ảnh↔lời lỗi nhưng KHÔNG chặn (bổ trợ) — video chính vẫn dùng được.
```

B8 ghép video (nguyên văn — chứng minh chế độ cũ, không có `--anchors`):
```
$ assemble.py --img ... --audio ... --srt voice_paced.srt --bgm ... --size 1920x1080 --out final.mp4
Audio 2040s / 133 ảnh · sync theo RANH GIỚI CÂU (SRT) · transition=xfade
```

B5 (nguyên văn — lý do bộ não không viết img_doan.txt):
```
[STEP 5/13] B5 gen ảnh (REF-LOCK)
  ⏭ đã có output — bỏ qua (resume)
```

---

## 3. TẠI SAO B5 SKIP (gốc rễ thật sự — lỗi QUY TRÌNH, không phải lỗi ngẫu nhiên)

`render_engine.py` dòng ~241: điều kiện "B5 xong" là

```python
("B5 gen ảnh (REF-LOCK)", len(list((S / "img").glob("*.png"))) >= n_prompt, ...)
```

Tập này ảnh đến từ **máy 2 (Flow) đã đủ 133/133** (drive_handoff download-result) → B5 bị đánh dấu "đã xong" → **bỏ qua hoàn toàn** → `gen_images.py` không chạy → **bộ não không bao giờ được gọi để viết `img_doan.txt`**.

Mà `img_doan.txt` lại CHÍNH LÀ sản phẩm phụ của bước B5 (prompt B5 trong `brain_steps.py` dòng ~257-265 dặn bộ não viết `<tên ảnh>|<số đoạn>` ngay lúc sinh ảnh). Khi ảnh có sẵn từ máy 2, khâu đó bị bỏ qua → không ai viết file → B7.5 chết non → B8 về chế độ cũ.

**Hệ quả:** MỌI tập có ảnh đến từ máy 2 (không phải render_engine tự gen) đều sẽ dính lỗi này. Tập simbot2-04 và simbot2-07 trước đây cũng từng lệch vì cùng cơ chế (04: 3,1/5 — chính là ca đã thúc đẩy sinh `sinh_neo.py`), nhưng lúc đó chưa có `sinh_neo.py`. Giờ có công cụ nhưng quy trình vẫn không gọi được vì B5 skip.

---

## 4. DỮ KIỆN LIÊN QUAN (để kiểm tra/xử lý)

- Ảnh: `E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-06-sYRr33eHYSM\img\` — 133 PNG (001..133)
- Prompt ảnh: `img_prompts.txt` — 133 dòng
- Script lời kể: `script.txt` (đoạn = khối chữ cách nhau dòng trống)
- Bộ sinh neo: `pipeline\sinh_neo.py` (đọc `img_doan.txt` + `script.txt` → `anchors.txt`; exit 1 = không ghi)
- Bước B7.5/B8: `pipeline\render_engine.py` (~dòng 241-256)
- Prompt B5 viết img_doan: `pipeline\brain_steps.py` (~dòng 257-265)
- Không có `img_doan.txt` / `anchors.txt` trong thư mục tập (đã kiểm tra).

---

## 5. ĐỀ XUẤT XỬ LÝ (2 hướng — cần chủ dự án chốt)

### Hướng A — Vá tập này (~15-20 phút, 0đ, không tốn TTS)
1. Viết thủ công `img_doan.txt`: map 133 ảnh ↔ số đoạn của `script.txt` (chỉ ghi CON SỐ, không chép trích đoạn — theo đúng thiết kế của `sinh_neo.py`).
2. Chạy `py -3.13 sinh_neo.py --slug "E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-06-sYRr33eHYSM"` → sinh `anchors.txt` (kiểm 5 điều tự động).
3. Chạy lại render (resume): B8 sẽ tự thêm `--anchors`, log B8 phải in `sync theo NEO NỘI DUNG (--anchors...)`.
4. Chạy lại B8Q → kiểm tra mốc lệch còn không.

### Hướng B — Sửa gốc pipeline (để mọi tập máy 2 sau này không dính)
`render_engine.py`: tách điều kiện B5 thành 2 phần — "đủ ảnh để gen" (skip gen ảnh) ≠ "đã có `img_doan.txt`" (bộ não vẫn phải được gọi để viết img_doan dù ảnh có sẵn). Gợi ý:
- Nếu `img/*.png` đủ nhưng THIẾU `img_doan.txt` → chạy một bước "B5b chỉ viết img_doan.txt" (gọi bộ não với prompt rút gọn: đọc `img_prompts.txt` + `script.txt`, CHỈ ghi số đoạn) trước B7.5.
- Hoặc thêm bước riêng sau B5: nếu thiếu `img_doan.txt` thì chạy `sinh_neo.py`-style brain call.

Lưu ý thiết kế đã chốt (khắc cốt): bộ não CHỈ ghi con số đoạn, MÁY tự cắt chuỗi neo — đừng bắt bộ não chép trích đoạn nguyên văn.

---

## 6. GHI CHÚ PHỤ (B5Q — không chặn, chỉ thông tin)

B5Q báo `11/20 ảnh mẫu có vấn đề` — đã soi 5 tấm bị nêu tên (008, 015, 022, 050, 057):
- `008` — chữ thật "緊急連絡先カード" trên biểu mẫu quầy tiếp tân → hợp cảnh, bỏ qua
- `050` — biển hiệu thật "洋服店" → hợp cảnh, bỏ qua
- `057` — name tag thật "スーパーマネージャー" → hợp cảnh, bỏ qua
- `015` — thư pháp treo tường hành lang, chữ AI-bịa nhưng là tranh trang trí nền nhỏ, mặt không nhoè → lỗi nhẹ, khó thấy
- `022` — chữ địa chỉ vô nghĩa trên phong bì thư (prop cảnh, chữ nhỏ) → lỗi nhẹ

Không có tấm nào nhoè mặt nặng, không watermark. B10: 1 phát hiện không nặng (chưa chạy B3F kiểm dữ kiện cho tập này).

---
*File do Hermes tạo 2026-09-12 để Claude Code đọc + xử lý theo yêu cầu chủ dự án.*
