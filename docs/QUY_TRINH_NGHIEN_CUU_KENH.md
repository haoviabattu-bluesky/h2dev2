# QUY TRÌNH NGHIÊN CỨU/PHÂN TÍCH 1 KÊNH — áp dụng cho MỌI lane, MỌI tab

> **⚡ TRIGGER:** anh nói *"nghiên cứu/phân tích kênh <tên hoặc URL>"* (hoặc câu tương đương: "tìm
> hiểu kênh này", "phân tích công thức kênh X") ở BẤT KỲ tab lane nào → làm ĐÚNG THEO file này,
> theo thứ tự, không bỏ bước, không tự nghĩ ra cách khác. Nếu không rõ mình đang ở lane nào, xem
> `docs/DANH_BA_LANE.md` trước.

Có **2 việc dễ nhầm lẫn với nhau**, file này tách rõ:
- **Nghiên cứu KÊNH** (chủ đề của file này) = nắm công thức/DNA của 1 kênh đối thủ cụ thể.
- **Nghiên cứu ĐỀ TÀI** (không phải file này — xem `docs/GIAO_VIEC_SPACE_RESEARCH.md` +
  `docs/KHUON_HO_SO_DE_TAI.md`) = tìm dữ kiện/tư liệu cho 1 TẬP VIDEO cụ thể sắp viết.

---

## BƯỚC 0 — KIỂM TRA ĐÃ CÓ NGHIÊN CỨU CHƯA (bắt buộc, làm trước khi tốn công/tiền)

Một kênh có thể đã được nghiên cứu ở 1 trong 4 chỗ sau — tìm hết cả 4 trước khi làm gì mới:

```
docs/channel_dna/<slug>/CHANNEL_DNA.md                          ← Phương án A (tool tự động, xem dưới)
docs/laneX_from_research/LANE_X_HANDOFF.md                      ← Phương án B, bản CŨ (trước Syncthing)
FlowHandoff_local/results/laneX_from_research/LANE_X_HANDOFF.md ← Phương án B, bản MỚI (qua Syncthing)
docs/DANH_BA_LANE.md                                             ← tra xem lane/kênh này đã có ai đụng chưa
```
Grep nhanh tên kênh hoặc slug trong cả 2 thư mục `docs/` và `FlowHandoff_local/results/`. **Tìm thấy
rồi thì DÙNG LUÔN, báo lại 1 dòng cho user, DỪNG Ở ĐÂY** — đừng chạy lại tốn tiền Gemini hoặc tốn
công dự án research làm lại.

---

## BƯỚC 1 — CHƯA CÓ THÌ CHỌN PHƯƠNG ÁN NÀO

| | **Phương án A — Channel Analyzer** | **Phương án B — SPACE_RESEARCH/TRENDING-RESEARCH** |
|---|---|---|
| Làm bằng gì | `pipeline/channel_analyzer.py` (Gemini, qua máy 2) | Dự án nghiên cứu riêng (máy khác), người/AI khác làm |
| Tốc độ | ~2-3 phút / kênh | Vài giờ đến 1 ngày |
| Độ sâu | N video top-view (mặc định 8), KHÔNG đọc comment | Toàn kênh (comment, A/B test, HIT/MISS từng video, thumbnail) |
| Chi phí | Vài trăm-nghìn đồng (Gemini qua ramcloud) | Công sức 1 dự án khác |
| Dùng khi | Kênh ĐÃ CHỌN rồi, cần nắm nhanh công thức để viết script | Đang CHỌN kênh trong nhiều ứng viên, hoặc mở LANE MỚI hẳn (cần độ tin cậy cao trước khi đầu tư sản xuất) |
| Output | `docs/channel_dna/<slug>/CHANNEL_DNA.md` + `VIDEO_ANALYSIS/*.json` (đúng schema `retrieve_videos.py` đọc được) | `LANE_X_HANDOFF.md` + đôi khi `channel_analysis_*.json` (schema RIÊNG, `retrieve_videos.py` KHÔNG đọc được thẳng) |

**Quy tắc chọn nhanh:**
- Lane đã có sẵn kênh mẫu, chỉ cần bắt đầu viết script → **Phương án A**.
- Đang cân nhắc mở 1 lane/ngách hoàn toàn mới, cần biết kênh có ăn khách thật không trước khi đầu tư
  → **Phương án B** trước (nhờ user chuyển yêu cầu sang SPACE_RESEARCH/TRENDING-RESEARCH theo đúng
  `docs/GIAO_VIEC_SPACE_RESEARCH.md`), Phương án A có thể chạy THÊM sau đó nếu cần
  `VIDEO_ANALYSIS/*.json` cho `retrieve_videos.py`.
- Không chắc → hỏi user, đừng tự chọn khi việc tốn tiền/thời gian đáng kể.

---

## BƯỚC 2A — LÀM PHƯƠNG ÁN A (Channel Analyzer)

Việc này **KHÔNG do Claude tự làm** — giao máy 2 chạy qua Syncthing. Các bước:

1. Xác định `slug` (tên thư mục không dấu, viết thường) cho kênh — vd kênh `シニア元気` → slug
   `senior-genki`.
2. Báo lại cho user ĐÚNG 1 đoạn (user sẽ dán sang chat với máy 2 — Claude không tự gửi được sang máy
   khác):
   ```
   <Tên/URL kênh>, <mô tả ngắn ngách viết ĐÚNG NGÔN NGỮ của kênh đó>
   ```
   (Máy 2 đã đọc + ghi nhớ toàn bộ quy trình ở `FlowHandoff_local/shared/GIAO_VIEC_MAY2_CHANNEL_
   ANALYZER.md` — không cần giải thích lại từng bước, chỉ cần đưa đúng 2 thông tin trên.)
3. Chờ user báo đã gửi + máy 2 chạy xong (Syncthing tự đưa kết quả về
   `FlowHandoff_local/results/channel_dna/<slug>/`, mất ~2-3 phút cho 8 video, có thể lâu hơn nếu
   dính 429 phải rơi vào whisper — xem mục "SỰ CỐ 429" trong file GIAO_VIEC nói trên).
4. Copy `FlowHandoff_local/results/channel_dna/<slug>/` → `docs/channel_dna/<slug>/` (thư mục chuẩn
   dùng cho mọi lane đọc).
5. Đọc nhanh `CHANNEL_DNA.md`, kiểm dòng cuối `run_log.txt` có `✓ TỔNG` không, kiểm số video phân
   tích được ≥70%. Có cảnh báo thì báo lại user, không tự ý bỏ qua.

**Nếu Claude đang chạy trong tab CHÍNH LÀ máy 2** (tức là bạn đang là agent máy 2, không phải lane
trên máy 1) — bỏ qua bước 2-3, chạy thẳng lệnh trong `GIAO_VIEC_MAY2_CHANNEL_ANALYZER.md`.

---

## BƯỚC 2B — LÀM PHƯƠNG ÁN B (SPACE_RESEARCH/TRENDING-RESEARCH)

KHÔNG lặp lại ở đây — làm đúng theo `docs/GIAO_VIEC_SPACE_RESEARCH.md` mục "5. MỞ LANE MỚI THÌ LÀM
GÌ" (sinh đơn đặt hàng bằng `pipeline/don_dat_hang.py`, gửi 1 đường dẫn duy nhất cho user chuyển
sang dự án research). Đợi hàng trả về ở `FlowHandoff_local/results/laneX_from_research/` hoặc
`docs/laneX_from_research/`, đọc theo mục 6 "TRẢ HÀNG LẠI" của file đó khi cần phản hồi lỗi.

---

## BƯỚC 3 — SAU KHI CÓ DNA (từ A hoặc B), VIỆC BẮT BUỘC TIẾP THEO

1. **Nếu lane CHƯA có `profile.json`** (kênh/lane hoàn toàn mới): xem CLAUDE.md mục "⭐ QUY TRÌNH
   SETUP KÊNH ĐẦY ĐỦ" + gọi skill global `youtube-produce` — DNA/handoff vừa có chính là "hồ sơ đề
   tài" đầu vào, không cần nghiên cứu lại.
2. **Nếu lane ĐÃ có SOP**: thêm/kiểm mục **§0b CHANNEL ANALYZER** — theo đúng khuôn đã có sẵn ở
   `docs/SOP_TOSHI_DENSETSU_JP.md` và `docs/SOP_SATORI_JP.md`. Lane CHƯA có SOP thì khi viết SOP mới
   PHẢI có mục này, không phải tuỳ chọn.
3. **Nếu có `VIDEO_ANALYSIS/*.json` (chỉ Phương án A có)**: mỗi khi viết 1 tập cụ thể, chạy
   ```
   py -3.13 pipeline\retrieve_videos.py --dna-dir docs\channel_dna\<slug> --topic "<chủ đề tập>"
   ```
   lấy N video liên quan thay vì tự đọc lại nhiều transcript thô.
4. **Nếu chỉ có handoff Phương án B** (không có `VIDEO_ANALYSIS/*.json` đúng schema): đọc thẳng file
   `LANE_X_HANDOFF.md` mỗi lần cần — không dùng được `retrieve_videos.py`. Nếu về sau cần retrieval
   tự động, có thể chạy THÊM Phương án A cho cùng kênh để có `VIDEO_ANALYSIS/*.json`.
5. **Cập nhật `CLAUDE.md`** mục "🧬 CHANNEL ANALYZER" (bảng trạng thái từng lane) nếu lane này chưa
   có dòng trong bảng đó, hoặc trạng thái đã đổi (mới chạy xong Phương án A/B).

---

## LIÊN QUAN
- Thiết kế kỹ thuật đầy đủ Phương án A: `docs/superpowers/specs/2026-09-16-gemini-channel-analyzer-design.md`
- Hướng dẫn máy 2 (Phương án A): `FlowHandoff_local/shared/GIAO_VIEC_MAY2_CHANNEL_ANALYZER.md`
- Nghiên cứu ĐỀ TÀI (khác nghiên cứu KÊNH): `docs/GIAO_VIEC_SPACE_RESEARCH.md`, `docs/KHUON_HO_SO_DE_TAI.md`
- Danh bạ lane: `docs/DANH_BA_LANE.md`
