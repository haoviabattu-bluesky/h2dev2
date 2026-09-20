# TRAO ĐỔI — HYBRID STOCK + AI, TẬP simbot2-21-HD-ADEBz5oM (retrofit thử nghiệm)

Ngày: 2026-09-16 · Người làm: Claude Code (Sonnet) · Mức độ: PHA 1 (phân loại + tải asset + nghiệm thu),
CHƯA dựng compositor.

## 1. Phạm vi & an toàn dữ liệu

Chỉ đọc `script.txt`/`img_prompts.txt`/`img_doan.txt`/`anchors.txt`/`img/`/`characters.json`/`final.mp4`
để tham chiếu — **không sửa/xoá file nào trong số đó**. Mọi thứ mới nằm ở:
- `assets/satori_jp/simbot2-21-HD-ADEBz5oM/stock/` (asset thật + `manifest.csv`)
- `scratch_analysis/stock_hybrid_simbot2-21-HD-ADEBz5oM/` (3 script + plan + log + báo cáo)

**Hash SHA-256 trước/sau của các file được bảo vệ (`pipeline/assemble.py`, `render_engine.py`,
`chay_buoc3.py`, `final.mp4`, `img_doan.txt`, `anchors.txt`, `img_prompts.txt`, `script.txt`):
KHÔNG ĐỔI** — verify bằng `hashes.py before` (lúc bắt đầu) và `hashes.py after` (vừa xong), in
`HASH KHONG DOI`.

## 2. VIỆC 1 — Phân loại (`phan_loai_stock.py`)

126 dòng `img_prompts.txt` → 3 lần gọi lô 25 dòng, `deepseek-v4-flash` qua ramclouds, 1,9 phút:

| Nhóm | Số dòng |
|---|---|
| AI — marker `@REF`/`@REF2`/`@GROK` (cứng, không hỏi LLM) | 60 |
| AI — LLM xác định có người/bộ phận cơ thể | 43 |
| **STOCK** — thuần cảnh/đồ vật | **23** (22 hiện đại, 1 lịch sử) |

Output: `stock_plan.tsv`.

## 3. VIỆC 2 — Tải asset (`stock_fetch.py`)

Với 23 dòng STOCK: Pexels video trước → ảnh sau (Commons thử trước cho 1 dòng lịch sử nhưng không ra
kết quả, rơi về Pexels). `deepseek-v4-flash` chấm điểm khớp 0–10 trên tối đa 8 ứng viên mỗi lần, nhận
ngưỡng ≥5 (nới lỏng theo yêu cầu — cảnh phong cảnh không cần khớp tuyệt đối). Kết quả (9,4 phút, 34
lượt gọi LLM, 0 lỗi API):

| | Video | Ảnh | Không tìm được |
|---|---|---|---|
| 23 dòng STOCK | 21 | 2 | 0 |

Cộng thêm **8 ảnh filler** thiên nhiên chung (mây, mưa, lá thu, nước, vườn đá...) vào `stock/_filler/`
để dùng sau này khi 2 clip stock đứng liền nhau (theo đúng ý anh — ảnh filler không cần khớp cảnh).

## 4. VIỆC 3 — Nghiệm thu nới lỏng (`audit_stock.py`)

Kiểm cơ học (file tồn tại, decode ffmpeg, kích thước khớp manifest, license đầy đủ, `prompt_line`
không trùng dòng `@REF`) **+ vision `gemini-3.8-flash`** (1–2 khung/video, 1 khung/ảnh, 52 lượt gọi,
6,2 phút) — chỉ loại khi **thấy MẶT NGƯỜI rõ** hoặc **CHỮ/LOGO to** (đúng tinh thần "nới lỏng": tay,
lưng, bóng người KHÔNG bị loại).

Kết quả sau nghiệm thu, `manifest.csv` đã cập nhật cột `status`:

| status | video | image |
|---|---:|---:|
| **OK** (dùng được) | 13 | 1 |
| REJECT_TEXT (chữ viết tay/lịch/thẻ hiện rõ trong khung) | 7 | 1 |
| REJECT_FACE (mặt người xuất hiện rõ) | 1 | — |
| FILLER (dùng được) | — | 8 |

→ **14/23 dòng STOCK có asset dùng được** (61%); 9 dòng bị loại **tự động rơi về ảnh AI hiện tại**
(đúng chính sách "không có stock → giữ ảnh AI", không có tập nào mất hình). Chi tiết từng dòng +
mô tả cảnh do vision trả về: `scratch_analysis/stock_hybrid_simbot2-21-HD-ADEBz5oM/audit_report.md`.

⚠️ Ghi chú chủ quan: một số REJECT_TEXT hơi khắt khe (vd "tay khoanh tròn ngày trên lịch" — chữ viết
tay nhỏ, không phải watermark/logo thật) — vì đây là kiểm ad-hoc tự thiết kế, anh xem lại
`audit_report.md` nếu muốn nới thêm ngưỡng "chữ" ở lượt sau (hiện đang tính mọi chữ đọc được, có thể
đổi thành "chỉ loại khi chữ CHIẾM PHẦN LỚN khung hoặc rõ ràng là watermark/thương hiệu").

## 5. Dung lượng & chi phí

- `stock/` (14 asset dùng được + 8 filler): **172 MB**.
- Chi phí: 0đ (Pexels free API + `deepseek-v4-flash` giá rẻ, quota ramclouds không phải thẻ VNĐ).
- Model dùng: phân loại + chấm điểm = `deepseek-v4-flash`; nghiệm thu vision = `gemini-3.8-flash`
  (đều KHÔNG dùng Claude, đúng yêu cầu tiết kiệm token).

## 6. CHƯA làm — cần anh chốt tiếp

1. **Compositor** theo luật slot mới (video ngắn/dài hơn co giãn ranh giới GIỮA 2 slot, giữ nguyên
   điểm kết thúc của slot phía sau; ảnh filler chèn khi 2 stock liền nhau) — đang chờ anh xác nhận 3
   điểm biên (trần mượn 1 slot, sàn 1,5s bỏ cảnh, mốc đầu=0/mốc cuối=audio cố định) đã hỏi trong chat.
2. Chưa dựng `final_stock_mix.mp4`, chưa preview tiếng Việt, chưa giao hàng, chưa ghi Sheet — đúng
   yêu cầu "chưa thay final.mp4 tới khi người dùng duyệt bản preview".

## 6b. QUYẾT ĐỊNH BIÊN — đã chốt 2026-09-16, bàn giao compositor cho AGENT KHÁC

Claude Code không tự dựng/ghép video (quy tắc mới ghi trong `CLAUDE.md` mục "⛔ CẤM TUYỆT ĐỐI",
2026-09-16) — 3 điểm biên hỏi ở mục 6 đã được suy nghĩ kỹ và CHỐT LẠI (đổi khác đề xuất ban đầu):
`DRIFT_MAX=2,5s` (không phải "mượn trọn slot kế"), `MIN_SLOT=2,5s` + **không bao giờ bỏ slot, luôn
cắt bớt clip stock khi chạm sàn** (bỏ hẳn ngoại lệ `@REF` — không cần nữa), mốc đầu/cuối cố định
tuyệt đối. Toàn bộ thuật toán ghép (kể cả ca chèn filler khi 2 video liền nhau, 4 trường hợp biên
nguy hiểm) đã viết đầy đủ, tự chứa, có công thức từng bước:

**→ `docs/GIAO_VIEC_HYBRID_COMPOSITOR.md`** (mục 7 của file đó áp riêng cho tập này — input đã sẵn
sàng 100%, chỉ còn việc viết code + chạy). Agent bước 3 (Hermes/DeepSeek) đọc file đó để dựng
`scratch_analysis/stock_hybrid_simbot2-21-HD-ADEBz5oM/output/{final_stock_mix.mp4,mixed_timeline.json}`
rồi ghi báo cáo nối vào CUỐI file này.

## 7. File liên quan
- `scratch_analysis/stock_hybrid_simbot2-21-HD-ADEBz5oM/{hashes.py,hashes_before.json,phan_loai_stock.py,stock_plan.tsv,phan_loai_log.txt,stock_fetch.py,fetch_log.txt,audit_stock.py,audit_report.md}`
- `assets/satori_jp/simbot2-21-HD-ADEBz5oM/stock/{*.mp4,*.jpg,_filler/,manifest.csv}`
