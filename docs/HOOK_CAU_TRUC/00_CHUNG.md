# LUẬT HOOK DUY NHẤT — BÁM SÁT CẤU TRÚC HOOK CỦA VIDEO GỐC (anh chốt 21/10/2026, mọi lane)

> Thay luật 17/10 ("động cơ chính + bám sườn + khuôn từng lane") và MỌI luật viết hook cũ trước đó (mở đầu bằng hội thoại,
> cao trào/kịch tính, cảnh nhục, 6 thành phần Lane M, narrative intro Lane N, mở đầu giới thiệu Lane L, 4 nhịp A–E,
> 20–30 giây, kho kiểu hook HOOK_LIBRARY, câu để ngỏ…) — tất cả đã BỎ.
> Khuôn hook riêng từng lane (F/L/M/N/O) cũ cất ở `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\_DA_BO_20261021\` — chỉ để tra, KHÔNG dùng.

## 1. Luật (chỉ 1 điều)
**Hook tập mình bám sát cấu trúc hook của video gốc: gốc làm thế nào mình làm thế ấy.** Được thay đổi một chút để hợp tập
mình hơn hoặc hay hơn.

- Giữ như gốc: cách mở giây 0, các nhịp theo thứ tự + vai trò từng nhịp, độ dài ≈ hook gốc.
- Đổi theo hồ sơ tập mình: tên họ, tuổi, công việc/ngành nghề, câu thoại, chi tiết, số.
- **Lý do không bị tính trùng lặp nội dung:** tên họ, nghề, câu thoại đã khác thì kịch bản đã khác; giữ cấu trúc hook gốc
  là được phép, không phải lỗi "sử dụng lại nội dung".
- Không có yêu cầu nào khác. Gốc mở bằng thoại thì mình mở bằng thoại; gốc không có cao trào thì mình không thêm cao trào.

## 2. Máy làm thế nào (`E:\CLAUDE\YOUTUBE\h2dev\pipeline\hook_stage.py`)
- H1–H3 `phan_tich_cau_truc()`: đọc lời 0–150 giây của video gốc (`video_goc.json`) → ghi `cau_truc_hook` vào
  `<tập>\hook\source.json`: cách mở, các nhịp, giây hook kết thúc. Chỉ mô tả gốc, không phân loại, không xếp khuôn.
- H4: Fable 5.1 viết `script.hook.so_ung_vien` phương án (mặc định 2), cùng 1 cấu trúc gốc.
- Máy đo (chỉ kỹ thuật): độ dài ≈ giây hook gốc × char_rate ±25%, không marker, không xin đăng ký, số có trong tư liệu,
  thoại tách câu riêng (lane đa giọng, cho TTS).
- Sol chấm 3 ô: BAM_CAU_TRUC (lệch nhẹ vẫn PASS) · STORY_TRUTH (người/sự kiện khớp hồ sơ tập) · DOI_CHI_TIET (đã đổi tên/
  nghề/câu thoại, không chép nguyên câu gốc). FIX → Opus 5 vá tại chỗ. Rồi khoá SHA256 như cũ.
- ⛔ (21/10, sự cố Lane L ep23 佐野稔 (Sano Minoru) — 429 chặn phụ đề, máy viết tự do) Tập KHÔNG có lời/cấu trúc hook gốc → **CẤM viết hook, CẤM dựng**: `ensure_locked` dừng (`hook_qc.json` state `NO_HOOK_GOC`), `khoa()` từ chối khoá (kể cả khoá tay), `make_video` chặn lock từ 21/10 không có `so_nhip_goc`. Bước chuẩn bị `tools\chay_lo_tap.py` kiểm trước khi mở `claude -p` (`pipeline\kiem_hook_goc.py`). Nguồn lời: competitor.segments.json → hook\source_segments.json → TRENDING transcripts → `data\loi_goc\<id>.json` → mạng (api → yt-dlp → whisper). `<tập>\hook_goc.json` do TRENDING-RESEARCH giao (đơn `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\YEU_CAU_TU_H2DEV_2026-10-21_HOOK_GOC_BAT_BUOC.md`) được dùng thẳng làm cấu trúc.
- Họ nhân vật đã dùng ở tập khác cùng lane (characters.json, trừ vai cố định có mặt ≥3 tập) → máy đo đánh trượt hook.
- Field profile `script.hook.huong_dan_cau_truc` đã bỏ (còn khai thì máy bỏ qua).

## 3. Không đổi (luật DỰNG hook, không phải luật viết)
Hình hook máy 1 làm (Google Flow/Vids), thẻ tên động, block giới thiệu, chữ trên đạo cụ, ký ức đen trắng, CHỈ nhạc nền (cấm SFX),
kiểm bối cảnh gọi điện/gặp mặt, clip hook xem thử + duyệt trước khi giao máy 2, HOOK_TAP.md — giữ nguyên như CLAUDE.md.
