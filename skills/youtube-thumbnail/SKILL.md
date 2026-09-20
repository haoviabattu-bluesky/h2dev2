---
name: youtube-thumbnail
description: Tạo THUMBNAIL cho video YouTube faceless — TỔNG QUÁT mọi ngách/thị trường/ngôn ngữ. Chọn ảnh nền cảm xúc + phủ CHỮ TO tương phản cao (overlay bằng PIL, KHÔNG nhờ model render chữ) HOẶC prompt thumbnail cinematic. Trigger: "thumbnail", "thumb <ngách>", "ảnh bìa video", "サムネ", "thumbnail prompt". Input: topic/cảnh cao trào + market/language + (ảnh nền). Áp dụng mọi dự án YouTube.
---

> **NGÁCH CHỐT CHO PROFILE NÀY:** niche=satori-elderly · market=JP · language=tiếng Nhật · narrator=cụ bà 70-80 ngôi 1, です・ます+ございます. Mọi tham số còn lại lấy từ  (char_rate, gate nhịp, character_sheet, style_suffix).

# YouTube Thumbnail (tổng quát — mọi ngách/thị trường)

2 kiểu, chọn theo NICHE/market:

## Kiểu A — CHỮ TO PHỦ (mặc định cho ngách kể chuyện/tư vấn: satori, tiền, quan hệ...)
Bắt chước thumbnail clickbait cảm xúc: nền ảnh mờ/tối + chữ TO tương phản (trắng/vàng/đỏ) + banner đỏ dưới.
1. **Nền:** chọn 1 ảnh trong `img/` có **KHUÔN MẶT cảm xúc mạnh / cảnh biểu tượng** (tool tự blur+darken làm nền).
2. **Config** `<slug>/thumb_text.txt` (mỗi dòng `MÀU|nội dung`, dòng cuối `BANNER|...`; MÀU = WHITE/YELLOW/RED):
   ```
   WHITE|<hook dòng 1>
   YELLOW|<hook dòng 2>
   RED|<câu hỏi/keyword gây sốc>
   RED|<đẩy thêm 1 nhịp — xem CẤU TRÚC 4+1 bên dưới>
   BANNER|<sub: "sự thật ... người X tiết lộ">
   ```
   Chữ theo NGÔN NGỮ market (Nhật/Hàn/Anh); font đậm hỗ trợ ngôn ngữ đó (vd YuGothB cho JP). Ngắn, gây tò mò.

   **⭐ CẤU TRÚC 4+1 (chốt 2026-09-17, áp dụng CHO MỌI tập của lane satori-jp-obaa từ nay):**
   đúng **4 dòng tiêu đề** (WHITE/YELLOW/RED, tuỳ ý lặp màu — KHÔNG tính dòng banner) + **1 dòng
   BANNER riêng** = 5 dòng hiển thị tổng cộng. Không phải "4 dòng gồm cả banner". Mỗi dòng tiêu đề
   PHẢI ngắn (4-7 ký tự CJK) để tự nhiên nằm gọn 1 hàng ở cỡ chữ to — dài hơn sẽ bị `--wrap` bẻ
   xuống thành 2 hàng, biến 4 dòng thành 5-6 hàng nhìn rối. Nếu kịch bản gốc chỉ có 3 ý, THÊM 1
   nhịp đẩy kịch tính (câu hỏi ngắn, từ khoá gây tò mò) làm dòng thứ 4 trước khi tới banner — banner
   giữ vai trò "chốt hạ" riêng, không lặp lại đúng ý đã có ở 1 trong 4 dòng trên.
3. **Render:** `py -3.13 pipeline/thumbnail_text.py --bg <nền.png> --text <slug>/thumb_text.txt --out <slug>/thumbnail_final.png --side left --wrap`
   → PIL overlay (model gen KHÔNG render chữ CJK chuẩn nên PHẢI overlay).

### ⭐ BỐ CỤC BẮT BUỘC (chốt 2026-09-17, sau khi so ảnh mẫu kênh gốc): 1 bên MẶT nét, 1 bên CHỮ TO HẾT KHUNG
Ảnh nền phải chừa nguyên **1/3 khung cho mặt SẮC NÉT** (prompt bg dùng cụm `RIGHT THIRD`/`LEFT THIRD` +
"the other two-thirds is completely empty out-of-focus background, no part of hair/body/hands visible
there" — đừng để mặt/tay lấn sang phía chữ). **2/3 khung còn lại dành cho chữ, và chữ phải PHỦ GẦN HẾT
cả bề ngang lẫn bề dọc của phần khung đó** (từ sát mép trên tới sát banner), KHÔNG chỉ vừa-đọc-được-là-xong.
Nếu có dòng banner dưới cùng, banner **cũng phải to hết bề ngang khung dưới**; KHÔNG có banner thì bỏ, không
cần cố nhét cho có.
- Gọi `--side left`/`--side right` khớp đúng bên mặt đã gen trong ảnh nền (`--side` = bên CHỮ, đối
  diện bên mặt), luôn kèm `--wrap` để chữ được ngắt dòng thay vì tự co nhỏ.
- **Bài học lỗi thật (ep1, 2026-09-17):** bản `thumbnail_text.py` cũ chỉ so BỀ NGANG của dòng dài nhất
  với 1 trần cỡ chữ cố định thấp (92px) rồi dừng — không bao giờ thử to hơn dù còn thừa cả khung ngang
  lẫn khung dọc (đo thật: hụt ~200px giữa khối chữ và banner), và banner ăn theo tỉ lệ cỡ chữ tiêu đề
  nên luôn dư lề 2 bên. Đã sửa: `fit_font()` giờ tối đa hoá cỡ chữ theo CẢ bề ngang lẫn tổng chiều cao
  khối (`--max-size` mặc định nâng lên 160), và banner có `fit_banner_font()` riêng tối đa hoá theo đúng
  bề ngang khung banner của chính nó — không lệ thuộc cỡ chữ tiêu đề nữa.
- Nếu `thumb_text.txt` thiếu dấu `|` (định dạng cũ chỉ có text trần, không có tiền tố MÀU) thì
  `thumbnail_text.py` ÂM THẦM bỏ qua toàn bộ dòng đó — ra ảnh nền đẹp nhưng KHÔNG CÓ CHỮ nào, không báo
  lỗi gì (đã dính thật ở 1 tập cũ). Luôn kiểm output có chữ thật trước khi coi là xong, đừng chỉ tin
  dòng log "✓ Thumbnail: ...".
- **Viền chữ MỎNG cố định (chốt 2026-09-17, vòng 2):** viền dày/scale theo cỡ chữ làm chữ "phồng" —
  `STROKE_W = 2` (px, cố định, không nhân theo size) cho cả viền đen (trắng/vàng) lẫn viền trắng (đỏ).
  To ra là THÂN chữ to, không phải viền dày ra.
- **`--side-width` mặc định 0.60** (trước 0.56) để thân chữ to hơn nữa, và **vùng LÀM MỜ nền phải
  khoá theo đúng `--side-width`** (`keep_sharp = side_width + 0.04`, wire thẳng trong `main()`) — trước
  đây 2 số này độc lập nhau (`keep_sharp` cũ cố định 0.44 bất kể `--side-width` truyền gì), chữ to ra là
  lấn vào đúng vùng ảnh NÉT phía sau, nhìn lởm chởm. Đổi 1 trong 2 số thì luôn đổi theo cặp.
- ⚠️ **ĐỪNG "giả đậm" chữ bằng cách vẽ 2 lớp `stroke_width` chồng nhau (silhouette to + lõi trong)**
  — đã thử (`BOLD_GROW`) rồi TỰ BỎ ngay trong ngày 2026-09-17: ở cỡ chữ lớn, kanji nhiều nét (電/話/朝...)
  bị 2 lớp viền chồng đè GÃY NÉT, đặc bệt mất khoảng trắng bên trong chữ (nhìn như lỗi font, nhưng
  không phải lỗi font — do kỹ thuật vẽ). Hiện tại CHỈ dùng đúng **1 lớp `stroke_width=STROKE_W=2`**
  trong `draw_line()`. Muốn chữ "mập" hơn thì đổi FONT (vd font Black thay vì Bold) hoặc tăng cỡ chữ,
  đừng quay lại kỹ thuật 2 lớp.

## Kiểu B — CINEMATIC KHÔNG CHỮ / tiêu đề tiếng Anh (ngách tư liệu: WW2/lịch sử)
Prompt 1 ảnh cinematic 16:9 bắt khoảnh khắc/căng thẳng/cảm xúc, đúng style niche (vd WW2: archival B&W, 1940s,
LIFE/Signal Corps, sáng-rõ-có chiều sâu). Kèm gợi ý tiêu đề (theo archetype của ngách) + SEO tags/hashtag market.

## GOLDEN
- Nền = mặt/khoảnh khắc cảm xúc nhất, KHÔNG cảnh trống. Chữ to ĐẦY KHUNG (không chỉ "đọc được") ở bên
  đối diện mặt, tương phản cao — xem mục BỐ CỤC BẮT BUỘC ở trên.
- Ngôn ngữ chữ + tiêu đề + SEO theo MARKET. Có thể tái dùng 1 ảnh đã gen trong img/ làm nền.
Tool: `pipeline/thumbnail_text.py` (impl: e:\CLAUDE\YOUTUBE\h2dev\pipeline). Chuẩn "giống bản gốc": xem
memory [[uu-tien-lam-giong-ban-goc]].
