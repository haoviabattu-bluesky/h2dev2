---
title: Phase 3 — nghiên cứu cách ghép nút đăng ký vào h2dev (2 lần / tập)
date: 2026-09-30
status: cho_anh_duyet
smoke_test: "ep06 kenko 21:54.77: encode lại cả video 278s | nguyên mẫu chỉ encode lại 2 đoạn 71.6s (24.7s video); 39443/39443 khung, decode 0 lỗi, md5 khung ngoài đoạn giống hệt gốc, thời lượng lệch 0.000s, đỉnh âm -2.4 dB"
---

# Yêu cầu anh (2026-09-30)
Mỗi tập chèn nút 2 lần: phút 3 (t=180s) và 2 phút trước khi hết (t = cuối − 120s).

# Sự thật đã kiểm (file:dòng trong h2dev/pipeline)
- B8 `make_video.py:2344-2452`: assemble → `final.mp4` → sfx_than ghi đè `final.mp4` tại chỗ → `ghep_hook_noi_truoc` → `final_with_hook.mp4`. `done("B8")` ở cuối (:2452).
- Lane stock (`stock_cut`) **return sớm ở :2375** — không sfx, không hook → phải gắn bước nút ở CẢ nhánh này.
- File được giao = `giao_hang.chon_video_nguon` (:200-220): `final_with_hook.mp4` nếu có, không thì `final.mp4`. B8Q (:1421), B10 qc_final, B11 giao hàng đều đọc theo tên file đó.
- Hook `noi_truoc` dời thân video +T (20-30s) → "phút 3" phải đo trên FILE GIAO (dòng thời gian người xem), không phải `final.mp4`.
- QC phải còn qua: thời lượng ±2-3s; đỉnh âm < −0.5 dBFS (`qc_visual.py:471`); tiếng ghép không to hơn giọng > 3 dB.
- Máy 2 chạy B8; `chan_may2` không chặn file video.
- Lane `teinengo-anaba`, `shakai_no_naze` có câu kết (outro_line) nói チャンネル登録 ở CÂU CUỐI — nằm sau mốc −120s, không trùng.

# 3 phương án
| | Cách | Tốn thêm / tập 22 phút (máy này) | Ghi chú |
|---|---|---|---|
| a | Bước riêng, encode lại CẢ video | 278s | đơn giản, mất chất lượng thêm 1 đời encode toàn bộ |
| b | Gộp vào filter của ghep_hook | ~0s | chỉ lane có hook; sửa file hook đã khoá tay; lane stock/không hook vẫn phải làm (a) |
| c | Bước riêng, CHỈ encode lại GOP chứa nút, còn lại stream-copy | 71.6s (video 6.4s, quét keyframe 11.8s, audio 51.8s) | ngoài 2 đoạn giống hệt gốc từng bit |

# Đề xuất: (c)
1. Tool vào `h2dev/tools/subscribe_overlay/`; hàm `apply_to_video(..., mode="segment")`, tự rơi về (a) nếu kiểm cắt đoạn sai.
2. Gọi 1 chỗ cuối B8 (sau hook, trước `done`) VÀ trước `return` nhánh stock (:2375), trên `giao_hang.chon_video_nguon()`, ghi `.partial` rồi thay đúng tên file → B8Q/B10/B11 không phải sửa.
3. Chống chèn 2 lần khi chạy lại tay: file đánh dấu `<video>.subscribe.json` (sha256 đầu vào + mốc).
4. Profile: `assemble.subscribe {enabled, start_times [180,-120], sub_click_style, avatar_path, thanks_text, language, position}`.
5. Tuỳ chọn: hút mốc về khoảng lặng giữa 2 câu gần nhất (±10s) theo `voice(_with_hook).srt` để "ting" không đè lời.

# Bẫy đã dính khi làm nguyên mẫu
- `-segment_times 177.800000` > pts thật 177.7999 → segment muxer cắt sang GOP SAU, nút lệch 8s mà thời lượng/số khung vẫn đúng. Sửa: lùi mốc cắt nửa khung + kiểm độ dài từng đoạn sau khi cắt (sai → dừng/rơi về a).
- alimiter 0.97 (−0.26 dB) vượt ngưỡng QC −0.5 dB → hạ 0.891 như assemble.py.
