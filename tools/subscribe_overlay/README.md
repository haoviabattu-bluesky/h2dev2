# subscribe_overlay — nút đăng ký kênh chèn vào video

Hiệu ứng: 「(avatar) ▶ チャンネル登録」 → con trỏ click (nút lún 92%) → 「▶ 登録済み 🔔」 → click chuông → "ting" + chuông rung
→ chữ đổi thành 「ありがとうございます」 → mờ dần.
Overlay RGBA trong suốt (VP9 alpha), KHÔNG green screen, KHÔNG GUI. Icon tự vẽ bằng Pillow, không tải mạng.

Thư mục này làm để copy NGUYÊN SI sang `E:\CLAUDE\YOUTUBE\h2dev\tools\subscribe_overlay\`.

## Chạy

```powershell
$env:PYTHONIOENCODING="utf-8"
# Chèn vào 1 video (overlay lấy từ cache nếu đã có)
py -3.12 subscribe_overlay.py --input video.mp4 --output video_final.mp4 --start 15 --language ja --position bottom_center
# Hiện 20 giây trước khi hết video
py -3.12 subscribe_overlay.py --input video.mp4 --output video_final.mp4 --start -20
# Chỉ xuất overlay trong suốt (dùng lại ở chỗ khác)
py -3.12 subscribe_overlay.py --generate-overlay --output subscribe_overlay.webm --size 1080p   # 720p|1440p|4k|vertical|WxH
py -3.12 subscribe_overlay.py --generate-overlay --output ov.mov --format mov                   # ProRes 4444 nếu webm alpha không hợp
py -3.12 subscribe_overlay.py --generate-overlay --output ov_png --format png                   # chuỗi PNG RGBA
# Render sẵn bộ master (1080p ja/en, 720p ja, vertical ja)
py -3.12 subscribe_overlay.py --masters
# Chọn cách ghép: segment (mặc định, chỉ encode lại đoạn có nút) | full (encode lại cả video)
py -3.12 subscribe_overlay.py --input video.mp4 --output out.mp4 --sound --mode full
# Test (14 test, ≈3 phút)
py -3.12 -m pytest tests -q -p no:cacheprovider
```

Cờ khác: `--has-subs` (đẩy nút lên trên vùng phụ đề), `--sound/--no-sound`, `--encoder auto|libx264|h264_nvenc`,
`--duration`, `--config <file>`, `--force` (bỏ cache, render lại).

## Cấu hình — `subscribe_config.json`

- `start_time`: giây xuất hiện; số âm = tính từ cuối video. `--start` ghi đè.
- `language`: `ja` (mặc định) | `en` | `vi`. Muốn chữ khác thì ghi `subscribe_text` / `subscribed_text`.
- `position`: `bottom_center` | `bottom_left` | `bottom_right` | `center`.
- `avatar_path`: avatar kênh (tròn, bên trái logo) — MỖI KÊNH 1 ẢNH. Đã tải sẵn 800×800 (2026-09-30) ở
  `assets/avatars/<profile_id>.png`: teinengo-real, teinengo-tanoshimi, yakkyoku-sukatto, shakai_no_naze, teinengo-anaba.
  Mẫu dự phòng: `assets/avatar_mau.png` (gấu mèo).
- `start_times`: `[180, -120]` = phút 3 + 2 phút trước khi hết (anh chốt). Âm = tính từ cuối.
- `compose_mode`: `segment` (mặc định) | `full` — xem mục "Cách ghép".
- `thanks_text`: lời cảm ơn sau khi bấm chuông (null = theo ngôn ngữ, "" = tắt).
- `overlay_width_ratio` 0.38 (ngang), `overlay_width_ratio_vertical` 0.80 (9:16).
- `bottom_margin_ratio` 0.035 (gần mép dưới, không sát), `bottom_margin_ratio_vertical` 0.24 (Shorts tránh vùng UI YouTube).
- `timeline`: mọi mốc animation (giây tính từ lúc nút hiện) — sai thứ tự sẽ bị chặn ngay khi đọc config.
- `enable_cursor / enable_bell / enable_card / enable_sound`, `fade_in / fade_out`, `press_scale`, `bell_angles`.
- `video_crf` 18 / `video_preset` medium: chất lượng encode lại video.

## Cách ghép (`compose_mode`)

- `segment` (mặc định, `so_segment.py`): chỉ encode lại các GOP có nút, phần còn lại stream-copy.
  - Các bước: quét keyframe → cắt `.ts` (mốc lùi 0,015 s) → **kiểm độ dài từng đoạn** → encode lại đoạn có nút (giữ `pix_fmt` / `color_range` / profile của nguồn) → concat copy.
  - Audio: trộn âm nút trên toàn track rồi AAC 192k.
  - Đo trên ep06 21:54: **71 s** (full mất 278 s); 39443/39443 khung; khung ngoài đoạn giống gốc từng bit (md5); decode 0 lỗi; đỉnh −1,8 dB.
  - Cắt lệch, nguồn không phải h264 yuv(j)420p, hoặc thời lượng lệch quá 0,1 s thì **tự rơi về `full`** và ghi vào `warnings`.
- `full` (`so_compose.compose`): encode lại cả video bằng `video_encoder` / `video_crf`.

## Cache

`cache/subscribe/subscribe_<size>_<lang>_<sha12>.webm` (+ `.json` meta: canvas, vị trí thẻ, fps, font).
Khoá SHA256 = bề rộng px + dọc/ngang + fps + chữ + font + timeline + style + `RENDER_VERSION`.
Đổi `start_time` / `position` / âm thanh / encoder KHÔNG render lại. Đổi chỗ cache: env `SUBSCRIBE_CACHE_DIR`
hoặc `cache_dir` trong config. Sửa code vẽ → tăng `RENDER_VERSION` trong `so_config.py`.

## Âm thanh

Bỏ `pop.wav`, `click.wav`, `bell.wav` của anh vào `sounds/` là tool dùng. Đang có `sounds/pop.wav` = 05_lap_lanh_3_not (anh chọn); chuông = "ting" bản 1 (anh chốt). Thiếu file nào thì tự tổng hợp
(sine có bao âm mềm, không bản quyền) vào `cache/subscribe/sounds_synth_v3/`. Âm được ép theo đúng layout/sample rate
audio gốc (không hạ stereo → mono). Không bật âm → audio gốc được `copy` nguyên vẹn.

## File

| File | Việc |
|---|---|
| `subscribe_overlay.py` | CLI + API `apply_to_video()` / `get_overlay()` |
| `so_config.py` | mặc định, đọc JSON, kiểm timeline, khoá cache |
| `so_fonts.py` | `find_font()` — dò Noto Sans JP → Yu Gothic → Meiryo…, kiểm glyph THẬT |
| `so_layout.py` | hình học theo đơn vị + trạng thái animation tại giây t |
| `so_icons.py` | logo play, chuông, con trỏ, bóng đổ (vẽ bằng mặt nạ, không quầng) |
| `so_renderer.py` | vẽ khung supersample 4x → LANCZOS → encode webm/mov/png; chặn nếu hình chạm mép |
| `so_compose.py` | đặt vị trí, `resolve_starts`, filter overlay / trộn âm dùng chung, mode `full` |
| `so_segment.py` | mode `segment`: chỉ encode lại GOP có nút |
| `so_sounds.py` | âm pop/click/chuông |
| `so_bells.py` | 5 kiểu chuông riêng từng lane (`bell_style`: 1_ting · 2_tram_am · 3_hai_not · 4_chuong_gio · 5_kim_loai) |
| `so_moc.py` | chọn giây hiện nút ±60s: tiếng nút vào khoảng nghỉ (sóng âm), đúng lúc chuyển ảnh, tránh bóng thoại trắng ở vùng nút |
| `so_ffmpeg.py` | tìm ffmpeg (imageio_ffmpeg như h2dev), probe, dò NVENC |

## Pitfall đã gặp

- Decode webm alpha PHẢI ép `-c:v libvpx-vp9` trước `-i` — decoder vp9 gốc của ffmpeg bỏ mất kênh alpha (nút ra nền đen).
- Vẽ chữ trực tiếp lên ảnh RGBA trong suốt → viền chữ bị pha đen khi thu nhỏ. Vẽ vào mặt nạ L rồi tô màu.
- Hoà 2 chữ cùng lúc lúc đổi trạng thái → nhoè; chữ cũ tắt hẳn rồi chữ mới mới hiện.
- `-segment_times 177.800000` > pts thật 177.7999 → muxer cắt sang GOP SAU, nút lệch 8 s mà thời lượng / số khung vẫn đúng. Phải lùi mốc 0,015 s VÀ kiểm độ dài từng đoạn.
- alimiter 0.97 vượt ngưỡng QC −0,5 dB → dùng 0.891 như `assemble.py:531`.
- Máy này GPU GeForce 210 → không NVENC; `auto` tự rơi về libx264.

## Gắn vào h2dev (2026-09-30)

B8n = `pipeline/nut_dang_ky.py`, gọi cuối B8 (sau ghép hook) khi profile có `assemble.subscribe.enabled`. CHỈ lớp phủ: số khung + thời lượng phải = gốc, sai thì giữ file gốc. Chống phủ 2 lần bằng `<video>.subscribe.json`. Phủ tay 1 tập: `py -3.13 nut_dang_ky.py --profile <lane> --slug <tập>`.
