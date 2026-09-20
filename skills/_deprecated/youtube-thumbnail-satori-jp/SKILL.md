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
   BANNER|<sub: "sự thật ... người X tiết lộ">
   ```
   Chữ theo NGÔN NGỮ market (Nhật/Hàn/Anh); font đậm hỗ trợ ngôn ngữ đó (vd YuGothB cho JP). Ngắn, gây tò mò.
3. **Render:** `py -3.13 pipeline/thumbnail_text.py --bg <nền.png> --text <slug>/thumb_text.txt --out <slug>/thumbnail_final.png`
   → PIL overlay (model gen KHÔNG render chữ CJK chuẩn nên PHẢI overlay).

## Kiểu B — CINEMATIC KHÔNG CHỮ / tiêu đề tiếng Anh (ngách tư liệu: WW2/lịch sử)
Prompt 1 ảnh cinematic 16:9 bắt khoảnh khắc/căng thẳng/cảm xúc, đúng style niche (vd WW2: archival B&W, 1940s,
LIFE/Signal Corps, sáng-rõ-có chiều sâu). Kèm gợi ý tiêu đề (theo archetype của ngách) + SEO tags/hashtag market.

## GOLDEN
- Nền = mặt/khoảnh khắc cảm xúc nhất, KHÔNG cảnh trống. Chữ to đọc được trên mobile, tương phản cao.
- Ngôn ngữ chữ + tiêu đề + SEO theo MARKET. Có thể tái dùng 1 ảnh đã gen trong img/ làm nền.
Tool: `pipeline/thumbnail_text.py` (impl: e:\CLAUDE\YOUTUBE\h2dev\pipeline). Chuẩn "giống bản gốc": xem
memory [[uu-tien-lam-giong-ban-goc]].
