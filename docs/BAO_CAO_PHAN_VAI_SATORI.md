# BÁO CÁO PHÂN VAI — lane `satori-jp-obaa` (tab `Lopezzapa68`)

Lập 2026-09-13 00:10 · phạm vi: chỉ dự án `h2dev`, chỉ lane này · mục đích: anh phân vai lại.
Mọi dòng tra từ code thật (`brain_channel.py` · `brain_steps.py` · `chay_phan_chu.py` ·
`render_engine.py` · `llm_client.py` · `profiles/profiles/satori-jp-obaa.json`), không gõ theo trí nhớ.

## 0. Bức tranh — 3 bước, 3 tay

| Bước | Ai đang làm | Bộ não | Vào | Ra |
|---|---|---|---|---|
| **1 — Chữ + master** | Máy 1, tab này (Claude Code VS Code) | `claude -p --model opus` (quota gói Max, không hoá đơn) | URL video simbot2 | `script.txt` · `img_prompts.txt` · `characters.json` · `img_doan.txt` · ảnh master `_ref/` · đơn ảnh trên Drive · cột E/F |
| **2 — Vẽ ảnh** | Máy 2 (người + Google Flow) | Nano Banana trong Flow (gói Ultra, 0đ) | đơn ảnh + `REF_*_master.png` | 100–134 ảnh/tập → Drive → cột F `Img done` |
| **3 — Render + giao** | DeepSeek (agent) chạy `render_engine.py` | gemini-3.8-flash (ramclouds) + ElevenLabs + ffmpeg | ảnh + chữ | `final.mp4` · thumbnail · gói đăng → `CHANEL\Lopezzapa68\epNN-slug` · cột G |

## 1. Bước 1 — chi tiết từng việc (máy 1, tab này)

| # | Việc | File | Model / engine | Chi phí | Cổng kiểm | Tình trạng |
|---|---|---|---|---|---|---|
| 1.1 | Quét kênh, chọn video theo view | `brain_channel.py --limit` | máy (yt-dlp) | 0 | — | ổn |
| 1.2 | Cào transcript đối thủ | `fetch_script.py` | yt-dlp + faster-whisper (local) | 0 | — | ổn, có retry đổi player_client |
| 1.3 | Chọn giọng khớp người kể | `detect_voice` → `voice.json` | gemini-3.8-flash | ~0 | — | ổn |
| 1.4 | **NHỊP 0** tra dữ kiện thật (tiền tệ, địa danh, năm…) | `brain_steps.py` | **Opus** (`claude -p`, web search) | quota | `docs/SO_LIEU_THAT_JP.md` phải tăng dòng | mới có từ 12/09; ep19 +15, ep06 +13 dòng |
| 1.5 | NHỊP 1 dàn ý → NHỊP 2 kịch bản 70/30 | `brain_steps.py` → `dan_y.txt`, `script.txt` | **Opus** | quota | — | ổn |
| 1.6 | **NHỊP 2b** khai `img_doan.txt` (ảnh ↔ số đoạn) | `brain_steps.py` | **Opus** | quota | `sinh_neo.py` đọc | luật mới 12/09 — **ep11/19 chạy trước luật nên không có** |
| 1.7 | NHỊP 3 nén/cắt cho đúng char-rate 270 | `gate_check.py` (đo) + `fix_gate.py` (nắn) | máy + gemini-3.8-flash (`task=script`) | ~0 | `gate_check.py` | ổn — Opus tự cắt 26′ thất bại, máy 2,4′ xong |
| 1.8 | B3Q tầng 1 — nhất quán, lặp, lỗi nặng | `qc_script.py` | gemini-3.8-flash | ~0 | chặn lỗi NẶNG | ổn |
| 1.9 | B3Q tầng 2 — giám khảo độc lập | `qc_claude.py` | **Opus** phiên mới | quota | `CHAN` chặn · `GOPY` không chặn | ổn sau khi tách mức; 3 vòng sửa tại chỗ |
| 1.10 | Viết `characters.json` + `img_prompts.txt` + `master_prompts` + `thumb_text.txt` | `brain_steps.py` | **Opus** | quota | `qc_can_anh.py` | ổn |
| 1.11 | Sinh ảnh **master** REF-LOCK (chính + phụ) | `chay_phan_chu.py` → `gen_images.py` | **gpti2** (gpt-image-2, VND) low | 50–110đ/ảnh, 1–2 ảnh/tập | `qc_can_anh.py` | ổn. `ima2` (0đ) đã verify tương đương nhưng **chưa wire** |
| 1.12 | Cổng cân ảnh trước giao | `qc_can_anh.py` | máy | 0 | marker ↔ master | ổn |
| 1.13 | Đẩy đơn lên Drive + tự chứng minh | `drive_handoff.py upload-job` / `verify-job` | Google Drive API | 0 | `verify-job` | ổn sau khi vá 3 lỗi câm |
| 1.14 | Ghi cột E (folder) + F (`Xong nội dung - cần ảnh`) | `quet_dong_can_anh.py` + MCP gsheets | máy | 0 | — | ổn |

Thời gian đo thật một tập bước 1: **~25–40 phút** máy chạy, phần lớn là Opus viết + 2 tầng QC.

## 2. Bước 2 — máy 2 (ngoài phạm vi code, chỉ ghi để đủ bức tranh)

| Việc | Cách | Chi phí | Cổng |
|---|---|---|---|
| Đọc cột F, tải đơn từ Drive | `drive_handoff.py download-job` | 0 | — |
| Vẽ ảnh Flow, REF-LOCK qua Character chung project | tay + Flow Nano Banana | 0 (Ultra) | — |
| Trả ảnh về Drive, đổi cột F `Img done - n/m` | `drive_handoff.py upload-result` | 0 | máy 1 `verify-result` |

Ảnh ra **1376×768**, được phóng ~1,4× lên 1080p ở B8 — **đòn bẩy chất lượng chưa động tới.**

## 3. Bước 3 — chi tiết 14 bước `render_engine.py` (DeepSeek chạy)

| # | Bước | File | Model / engine | Chi phí | Chặn? | Tình trạng |
|---|---|---|---|---|---|---|
| 3.0 | Tải ảnh về, đếm đủ | `drive_handoff.py download-result` | Drive API | 0 | tay | ổn |
| 3.0b | **Sinh `img_doan.txt` cho tập cũ** | `sinh_img_doan.py` | gemini-3.8-flash (`task=short`) | ~0 | — | ❌ **HỎNG — lỗi A**: đoán được cảnh, không đếm được; 17/52 đoạn trống |
| B4 | Giọng đọc | `tts.py --provider openspeaker` | **ElevenLabs** `Ado - Mature & Soothing` · speed 0,92 · fx `old-med` | ~1.500đ/tập (~13k credit) | có | ổn |
| B4.1 | Phụ đề khớp script (STT nghe nhầm) | `srt_from_script.py` | máy (difflib) | 0 | có | ổn |
| B4.2 | Giãn nhịp lời người già | `pace_audio.py` | máy (sóng âm) | 0 | có | ổn; còn bug undershoot chưa sửa |
| B4Q | QC giọng + phụ đề + nghe | `qc_visual.py` + `qc_audio.py` | gemini-3.8-flash + máy | ~0 | có | ổn |
| B5 | Gen ảnh | `gen_images.py` | gpti2 | **~8.000đ/tập nếu lỡ chạy** | có | ⚠ bị bỏ qua khi đủ ảnh; **thiếu 1 tấm là tự vẽ lại toàn bộ** |
| B5Q | QC ảnh (mẫu 20) | `qc_visual.py images` | gemini-3.8-flash | ~0 | có | ổn; biển hiệu tiếng Nhật hay bị báo nhầm |
| B7 | Thumbnail | `gen_images.py` (nền) + `thumbnail_text.py` (chữ PIL) | gpti2 + máy | ~50–110đ | có | ổn |
| B7.5 | Neo ảnh ↔ lời | `sinh_neo.py` | máy | 0 | **không** | ❌ **lỗi B**: dồn ảnh về đầu đoạn; cổng chỉ kiểm ≥1s, không kiểm "đứng 4 phút" |
| B8 | Ghép video (Ken Burns, xfade) | `assemble.py` | ffmpeg CPU | 0 | có | ổn; rớt B7.5 thì rơi về chia theo số đếm → **ảnh trôi** |
| B8Q | QC video (mẫu 14 mốc) | `qc_visual.py video` | gemini-3.8-flash | ~0 | có | ổn nhưng **4 tập đều 2,9–3,1/5** vì B8 chưa có neo |
| B8V | Bản duyệt phụ đề Việt | `sub_vi.py` | gemini-3.8-flash (`task=script`) | ~0 | không | ổn |
| B9 | Gói đăng tải | `publish_kit.py` | máy | 0 | không | ổn |
| B10 | Nghiệm thu toàn tập | `qc_final.py` | máy | 0 | có | ổn |
| B11 | Giao hàng 3 file + ghi cột G | `giao_hang.py` + `ghi_cot_video.py` | máy | 0 | — | ổn sau khi vá tên file + số 2 chữ số |

Thời gian đo thật: **~27 phút/tập** cả giọng, **~20 phút** khi ghép lại không tốn giọng.

## 4. Bảng model — ai đang gánh việc gì

| Model / engine | Việc đang gánh | Trả bằng | Nhận xét để phân vai |
|---|---|---|---|
| **Claude Opus** (`claude -p`, gói Max) | NHỊP 0–2b viết; B3Q tầng 2 chấm; 3 vòng sửa tại chỗ | quota tuần | Đúng chỗ: sáng tác + phán xét. **Đừng** đưa việc đếm/cắt cho nó (đã chứng minh 4 vòng thất bại) |
| **gemini-3.8-flash** (ramclouds → ns24 → gpt-5.6-luna) | `fix_gate` nén · `qc_script` · `qc_visual` B4Q/B5Q/B8Q · `sub_vi` · `detect_voice` · **`sinh_img_doan`** | API rẻ | Tốt việc chấm/nén/dịch. **Không dùng được** cho việc ghép nội dung có ràng buộc số lượng (lỗi A) |
| **gpti2** gpt-image-2 | master REF-LOCK · nền thumbnail · (B5 dự phòng) | VND | 1–3 ảnh/tập, rẻ. `ima2` 0đ đã verify ngang bằng, chưa wire |
| **Google Flow** Nano Banana | 100–134 ảnh thân video | 0 (Ultra) | Máy 2. Giới hạn 1376×768 |
| **ElevenLabs** qua OpenSpeaker | giọng Ado | credit ~1.500đ/tập | ổn, không đổi |
| **ffmpeg / Python thuần** | srt reflow · pace · neo · ghép · QC nghe · gói · giao hàng | 0 | Phần "máy đo và nắn" — nơi đáng đổ thêm việc |
| **DeepSeek** (agent ngoài) | vận hành bước 3, đọc cột H, báo cáo file .txt | quota bên đó | Làm đúng lệnh, tự đo được thời lượng (đã tự viết `do_thoi_luong_neo.py`). **Không** giao việc sửa thuật toán |

## 5. Trạng thái 8 tập trên đĩa (đo 2026-09-13 00:05)

| Tập | Chữ | Master | Ảnh | Giọng | Video | Giao hàng / cột G | Ghi chú |
|---|---|---|---|---|---|---|---|
| 02 (thử) | ✓ | 1 | 90/90 | ✓ | ✓ | — | tập nháp đầu, không trên trang tính |
| 04 | ✓ | 1 | 119/119 | ✓ | ✓ | ✓ `ep04-roujin-home-88` | B8Q **3,1** — chế độ cũ, không neo |
| 06 | ✓ | 1 | 133/133 | ✓ | ✓ | ✓ `ep06-oita-onna` | B8Q **2,9**; có `img_doan` nhưng `013.png` đứng 97s — DeepSeek chờ anh quyết |
| 07 | ✓ | 1 | 128/128 | ✓ | ✓ | ✓ `ep07-yokin-yuigon` | 3 mốc 2/5 sau phút 19 |
| 11 | ✓ | 1 | 121/121 | ✓ | ✓ (không neo) | ✗ | B8Q 3,1; `anchors.txt` mới **tệ hơn không neo** — ĐANG DỪNG |
| 19 | ✓ | 1 | 134/134 | ✗ | ✗ | ✗ | `img_doan.txt` sinh bằng tool hỏng — ĐANG DỪNG |
| 21 | ✓ (rớt cổng) | 1 | 0/126 | ✗ | ✗ | ✗ | 3 lỗi chặn (2 SAO_CHÉP + 1 lặp), chưa sửa, chưa giao máy 2 |
| vU5PWT2zLDs (cũ) | ✓ | 1 | 124/124 | ✓ | ✓ | — | bản cũ trùng video 02 |

## 6. Việc đang treo — theo thứ tự chặn nhau

1. **Lỗi A + B (neo ảnh)** → chặn 11, 19, và mọi tập cũ muốn ghép lại. Đề xuất đã gửi DeepSeek
   (`CLAUDE-DEEPSEEK-satori.TXT` mục 5): phương án B (chấm điểm + quy hoạch động) + trải đều neo.
   Đây là việc **sửa thuật toán** → máy 1.
2. **Tập 21** rớt cổng chữ → sửa tại chỗ bằng Opus (máy 1), rồi mới giao máy 2 vẽ.
3. **Tập 06** `013.png` 97 giây — anh quyết giữ hay ghép lại (20 phút, 0đ giọng).
4. **Cổng B7.5** phải đo phân bố thời lượng, không chỉ cận dưới — máy 1 sửa `sinh_neo.py`.
5. Đòn bẩy chưa động: ảnh 1376×768 phóng lên 1080p; `ima2` 0đ thay gpti2 cho master.

## 7. Ranh giới hiện tại (để anh cân nhắc khi phân vai)

- Máy 1 = **viết + phán xét + sửa code**. Chỉ Opus mới làm được 1.4–1.10.
- Bước 3 = **chạy lệnh theo đơn + đo + báo**. Không cần Opus; DeepSeek đang làm tốt, và có thể
  giao thêm cho nó việc **kiểm số đo** (đã tự viết tool đo thời lượng) — nhưng **không** giao việc sửa
  `sinh_img_doan.py`/`sinh_neo.py`, vì lỗi nằm ở thiết kế thuật toán chứ không ở vận hành.
- Việc **chấm điểm ngữ nghĩa** trong phương án B là việc gemini-3.8-flash làm được (chấm từng cặp
  0–3), còn **quy hoạch động** là máy — không cần Opus cho khâu này sau khi viết xong.
