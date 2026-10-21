---
title: Nút đăng ký kênh (subscribe overlay) cho h2dev
created: 2026-09-30
status: phase2_completed
smoke_test: "2026-09-30: pytest 8/8 (102s). 1080p 60s: overlay cache 0.1s + ghép 20.9-25.7s, lệch thời lượng 0.000s. Render overlay mới: 1080p 30.6s, 720p 23.9s, 9:16 74.1s. webm 92-148KB, alpha_mode=1, alpha góc=0 / thẻ=255, viền canvas alpha max=0."
---

# Brainstorm (tóm tắt — nguồn: spec anh dán 2026-09-30)

- Mục tiêu: chèn animation nút đăng ký (JA mặc định: チャンネル登録 → 登録済み + chuông) vào video bằng
  Python + FFmpeg, overlay RGBA trong suốt, KHÔNG green screen, KHÔNG GUI, KHÔNG CapCut.
- Render 1 lần / cấu hình → cache `cache/subscribe/`; mỗi tập chỉ còn bước FFmpeg overlay.

# Quyết định khớp h2dev (khảo sát 2026-09-30)

| Điểm | h2dev đang làm | Tool này làm |
|---|---|---|
| ffmpeg | `imageio_ffmpeg.get_ffmpeg_exe()` (assemble.py:36) | giống, fallback PATH |
| encode cuối | libx264 medium crf 20, aac 192k, +faststart | libx264 medium crf 18 (config), audio `copy` khi không bật âm |
| khung | 1920x1080 @30fps | tự đọc kích thước/fps video, scale overlay theo chiều rộng |
| overlay | track `.mov` + `overlay=eof_action=pass` | webm VP9 alpha + cùng filter |
| font JP | tate_text.load_font / YuGothB.ttc cứng | `find_font()` dò nhiều thư mục + kiểm glyph thật |
| cấu hình lane | `profile.assemble.{tate,bubble,sfx}` | sau này thêm `assemble.subscribe` (cùng key với subscribe_config.json) |
| file ship | `final_with_hook.mp4` ưu tiên hơn `final.mp4` | ghép nút SAU hook (bước cuối B8) |
| GPU | GeForce 210 — không NVENC | encoder `auto` dò NVENC thật, rơi về libx264 |

# Phases

1. Phase 1 (rủi ro nhất): render frame Pillow → webm VP9 alpha, font JP, compose 1 video 1080p — kiểm alpha thật.
2. Phase 2: cache SHA256, 3 độ phân giải, âm thanh tự tổng hợp, CLI đầy đủ, test tự động.
2b. Góp ý bản 1 (2026-09-30): hạ nút gần đáy (bottom_margin_ratio 0.035), âm v2 bỏ nhiễu (pop/click/ting sine
   có bao âm mềm), avatar kênh bên trái logo (`avatar_path`), 登録済み → ありがとうございます sau chuông
   (`thanks_text`, timeline.thanks 4.1, duration 6.0). pytest 9/9 (121s). RENDER_VERSION 2.
3. Phase 3 (CHƯA làm — chờ anh duyệt): copy vào `h2dev/tools/subscribe_overlay/`, thêm field
   `assemble.subscribe` vào profile + gọi `apply_to_video()` cuối B8 trên `giao_hang.chon_video_nguon()`.
