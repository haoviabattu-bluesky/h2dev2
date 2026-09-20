# H2Dev Video Render — tool .exe render 1-click (TỔNG QUÁT mọi ngách)

GUI render 1-click cho pipeline video YouTube faceless — **TỔNG QUÁT** mọi ngách/thị trường/ngôn ngữ (Satori JP, WW2 EN, Hàn…). Niche/market/language = tham số. **Claude soạn nội dung** (script, prompt ảnh, bible, masters); **exe render cơ học** 9 bước.

## Cách dùng
1. Claude (trong Claude Code) chuẩn bị 1 thư mục slug `assets/satori_jp/<slug>/` có đủ:
   `script.txt` · `characters.json` · `img_prompts.txt` · `thumb_text.txt` · masters `_ref/001.png` (+ `_ref_<char>/001.png` nếu 2 nhân vật).
2. Mở **`H2Dev Render.exe`** → bấm **Chọn slug…** → trỏ tới thư mục slug đó.
3. (tuỳ chọn) Đổi **Profile giọng** (mặc định `satori-jp-obaa` = cụ bà) · bật/tắt **Giãn nhịp**.
4. Bấm **▶ RENDER TẤT CẢ** → xem tiến độ 9 bước + log. Xong có `final.mp4` + `thumb_final.png` trong thư mục slug.
5. Nút **■ DỪNG** cắt được giữa chừng (giết cả cây tiến trình — quan trọng vì gen ảnh tốn tiền). **📂 Mở thư mục** xem kết quả.

## TỔNG QUÁT mọi ngách — dùng cho kênh khác
Tool KHÔNG khoá Satori. Để làm ngách khác (WW2 English, Hàn, tiền/hưu…):
- Đặt slug ở `assets/<market>/<slug>` (bất kỳ).
- Dùng **profile giọng** tương ứng (`profiles/<id>.json`) — điền vào ô "Profile giọng".
- **Nhạc nền:** để file `_bgm/*.mp3` trong slug hoặc thư mục cha (engine tự dò; không có thì bỏ BGM).
- **QC ảnh sát ngách:** thêm field `"world"` vào `characters.json` (vd `"world": "WWII archival, 1940s Europe"`); thiếu thì dùng world tổng quát.
- Ngách KHÔNG khoá mặt (WW2 tư liệu): `characters.json` để `"characters": []` → engine gen ảnh plain, không cần master.

## 9 bước engine chạy (resume: bỏ bước đã có output)
B4 giọng → B4.1 sửa phụ đề khớp script → B4Q QC giọng → B4.2 giãn nhịp → B5 gen ảnh (REF-LOCK) → B5Q QC ảnh → B7 thumbnail → B8 ghép video → B8Q QC video.

## Cấu hình — `satori_gui_config.json` (cạnh exe, sửa được)
```json
{ "project_root": "E:\\CLAUDE\\YOUTUBE\\h2dev", "python_cmd": ["py", "-3.13"], "profile": "satori-jp-obaa" }
```
- `project_root`: gốc dự án (chứa `pipeline/` + `assets/`). GUI gọi `pipeline/render_engine.py`.
- `python_cmd`: lệnh chạy Python **có sẵn deps pipeline** (requests, numpy, Pillow, imageio-ffmpeg, faster-whisper…). Máy đích PHẢI có py-3.13 này (exe chỉ chứa GUI, KHÔNG chứa deps nặng).

## Kiến trúc
`Satori Render.exe` (PySide6, mỏng) --Popen--> `py -3.13 pipeline/render_engine.py --slug <abs>` --subprocess--> từng script pipeline (tts/srt_from_script/qc_visual/pace_audio/gen_images/thumbnail_text/assemble).

## Build lại
`build_satori_gui.bat` (PyInstaller --onedir --windowed). Kiểm bản build: `"Satori Render.exe" --selftest` → đọc `selftest.log` cạnh exe.

## Giới hạn (Out of Scope)
Không tự viết script/prompt/master bằng LLM (Claude làm) · không upload YouTube · không sửa Google Sheet · không bundle API key.
