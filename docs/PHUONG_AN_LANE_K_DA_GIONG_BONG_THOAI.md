# PHƯƠNG ÁN LANE K (`yakkyoku-sukatto`) — ĐA GIỌNG · KHOÁ MẶT N NHÂN VẬT · BÓNG THOẠI CÓ ĐUÔI

Viết 2026-09-24. Người đọc: anh (duyệt) + tab/agent code theo. Căn cứ đo thật:
`E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\yakkyoku-sukatto\GIONG_VAI.md` (giọng↔vai 4 video gốc) ·
bản thử bóng thoại `C:\Users\admin\AppData\Local\Temp\claude\e--CLAUDE-YOUTUBE-h2dev\e9f51844-8687-403e-a78f-395c363c47ba\scratchpad\demo_trai.png`.

## 0. Anh đã chốt
| # | Quyết định |
|---|---|
| Q1 | Đa giọng ĐÚNG như kênh gốc, dùng VOICEVOX (0đ). Giọng không có trong VOICEVOX thì **không clone, không cài thêm** — thay bằng giọng VOICEVOX mà kênh gốc cũng dùng cho cùng vai (店長 → 雀松朱司, đúng như video 3 gốc) |
| Q2 | Khoá mặt theo TỪNG TẬP: mỗi vai có thoại hoặc xuất hiện ≥2 cảnh = 1 ảnh khoá mặt. Flow Tool: **1 ảnh khoá tối đa 3 nhân vật** |
| Q3 | Lời thoại = BÓNG THOẠI chữ dọc, có đuôi chỉ về người nói, **máy vẽ** (ảnh AI cấm có chữ). Lời kể = hộp trắng chữ dọc |
| Q4 | Hook = clip Grok ở đầu video (luật chung). Shorts làm sau |

Vì sao không clone 阿井田茂 (Aida Shigeru, giọng AivisSpeech ở video 1–2): (1) đó là giọng của một diễn viên lồng tiếng thật
(CV 古山キリヲ) — clone giọng người thật sang ElevenLabs không có phép là rủi ro bản quyền, skill `openspeaker_voice_clone.md`
chỉ cho phép để TEST; (2) trộn 1 giọng ElevenLabs vào 10 giọng VOICEVOX sẽ lệch chất âm rõ tai; (3) chính kênh gốc ở
video 3 cũng dùng 雀松朱司 cho 店長 → vẫn đúng chuẩn kênh gốc.

## 1. Nguồn chân lý mới: `characters.json` mở rộng (mỗi tập 1 file, máy 1 viết ở bước 1)
```json
{"characters": [
  {"id": "shu",   "name": "主人公", "vai": "nhân vật chính", "age": 38, "gender": "M", "look": "...",
   "ref": true,  "voice": {"speaker": "黒沢冴白", "style": "ノーマル"}},
  {"id": "tencho","name": "店長",   "age": 45, "gender": "M", "look": "...", "ref": true,
   "voice": {"speaker": "雀松朱司", "style": "ノーマル"}},
  {"id": "jimu",  "name": "事務さん","age": 30, "gender": "F", "look": "...", "ref": true,
   "voice": {"speaker": "波音リツ", "style": "ノーマル"}},
  {"id": "kanja", "name": "患者の老人", "age": 78, "gender": "M", "look": "...", "ref": false,
   "voice": {"speaker": "ちび式じい", "style": "ノーマル"}}
]}
```
- Người kể KHÔNG nằm trong file này: khai cố định ở profile `voice.narrator = {"speaker":"玄野武宏","style":"ノーマル"}`.
- 3 vai cố định (người kể 玄野武宏 · nhân vật chính 黒沢冴白 · 事務さん 波音リツ) lấy giọng từ profile `voice.fixed_cast`;
  vai phụ tập nào tập nấy chọn theo bảng §3 của `GIONG_VAI.md`.
- `ref: true` → có ảnh khoá mặt riêng `_ref_<id>/001.png`. Luật chọn ref (máy kiểm): mọi vai có ≥1 câu thoại, hoặc có mặt
  ≥2 ảnh, PHẢI `ref: true`.
- Tương thích ngược: file cũ dùng `ref_marker: "@REF"/"@REF2"` vẫn đọc được (lane F/G không đổi gì).

## 2. Bốn phần code

### C1 — Kịch bản viết sẵn để gắn vai (máy 1, bước 1)
- Luật viết nhồi vào prompt của model VIẾT qua `script.structure_block` + `script_qc.lane_rules` của profile (không sửa code
  chung): **mỗi câu thoại đứng riêng 1 câu 「…」**, không dính lời dẫn 「…」と彼は言った trong cùng câu; độc thoại nội tâm
  「俺…」 viết thành câu riêng, không ngoặc (đúng văn phong gốc).
- S3 (máy đo) thêm 1 phép kiểm tất định: câu chứa 「」 lẫn chữ ngoài ngoặc → VIỆC (patch tách câu). Khai bằng field
  `script.gate.dialogue_own_sentence: true` — lane khác không khai = không đổi.

### C2 — Gắn vai từng câu: `pipeline/gan_vai.py` (MỚI, máy 1, sau LOCK, trước B5W)
- Vào: `script.txt` (LOCK PASS) + `characters.json`. Ra: `vai.txt` — mỗi dòng `số_câu|id_vai|câu nguyên văn`
  (`id_vai` = `ke` cho người kể hoặc `id` trong characters.json).
- Model: `script.patch_model` (Opus) qua `claude_p_bridge` — đọc hiểu nội dung, **KHÔNG chạm script.txt**.
- Máy kiểm (thiếu = hỏi lại 1 lượt rồi BLOCK): đủ số câu, đúng thứ tự, chữ từng câu khớp script 100% · câu 「…」 không được
  gán `ke` · câu nội tâm 「俺…」 ngoài ngoặc phải gán nhân vật chính · mọi id có trong characters.json · vai có thoại mà
  `ref:false` → báo lỗi characters.json.
- Chép thêm `vai.txt` vào `JOB_FILES` của `dong_goi_may2.py` (máy 2 cần để lồng tiếng + vẽ bóng thoại).

### C3 — Lồng tiếng đa giọng VOICEVOX: `pipeline/tts_voicevox.py` (MỚI, chạy ở MÁY 2)
- Profile khai `voice.provider = "voicevox"` → `make_video.b4_voice` rẽ sang file này (ngã rẽ bằng field, không `if profile_id`).
- Mỗi dòng `vai.txt` → `POST /audio_query` + `/synthesis` với speaker/style của vai (engine local `:50021`) → WAV từng câu →
  nối lại, chèn nghỉ giữa câu (ms, khai `voice.pause_sentence_ms`/`pause_para_ms`, ĐO từ tiếng gốc trước khi chốt) →
  `voice.mp3` (chuẩn hoá −16 LUFS như `tts.py`).
- **SRT viết thẳng từ độ dài từng WAV** → mốc chính xác tuyệt đối, chữ đúng 100% (không qua STT) ⇒ bỏ được B4a nắn phụ đề;
  kèm `voice_roles.json` (cue → id_vai) cho C4.
- Cổng giữ nguyên tinh thần `kiem_phu_chu`: tổng chữ SRT = tổng chữ script; câu nào WAV < 0,3s → DỪNG.
- Ghi khối ▼素材 (tư liệu) = danh sách 「VOICEVOX:<tên>」 thật đã dùng → file `credits_giong.txt` cho dự án tiêu đề chép vào mô tả
  (điều khoản 14 giọng bắt buộc ghi tên).
- `calibrate.py` đo char-rate bằng chính engine này (hàng rào #1).
- Máy 2 phải cài VOICEVOX engine 0.25.2 (1,9 GB, miễn phí) — giao việc cài 1 lần, kèm lệnh chạy `run.exe --port 50021`.

### C4 — Khoá mặt N nhân vật (máy 1 vẽ master, máy 2 vẽ cảnh bằng Flow Tool)
- `prompt_doan.py`: thay tag cố định MAIN/MENTOR/BOTH bằng **danh sách id nhân vật thấy mặt** trong ảnh, dạng
  `<đoạn>|shu,tencho|<prompt>` (hoặc `NONE`/`CHILD`). Máy kiểm: ≤3 id/ảnh (Flow Tool) · id phải `ref:true` · tỉ lệ ảnh thấy
  mặt ≤50% như cũ. Dòng ghi ra `img_prompts.txt`: `@CAST:shu,tencho <prompt>` (marker mới; `@REF/@REF2/@REF12` vẫn chạy cho lane cũ).
- `make_video.masters_from_bible`: vẽ master cho MỌI nhân vật `ref:true` (song song), QC tuổi/giới bằng `qc_character.py`
  như hiện tại → `_ref_<id>/001.png`.
- `dong_goi_may2.py`: gói mọi `_ref_<id>/`; `_BANGIAO.txt` hướng dẫn máy 2 tạo 1 Character Flow cho mỗi id trong CÙNG 1 project
  rồi mention đúng các `@id` ghi ở đầu dòng prompt.
- `gen_images.py` (dự phòng gpti2): hiểu `@CAST:` → gửi tối đa 3 ảnh master tương ứng (gpti2 nhận tới 8).
- Prompt ảnh BẮT BUỘC: không chữ, không bóng thoại, chừa khoảng trống quanh người nói (câu dặn thêm khi profile có
  `assemble.bubble`).

### C5 — Bóng thoại + hộp lời kể: nâng `pipeline/tate_text.py` (chạy ở MÁY 2, bước ghép)
- Vào: `voice.srt` + `voice_roles.json` + dòng thời gian ảnh (cùng hàm `anchor_durations` của `assemble.py`) +
  `img_faces.json`.
- `img_faces.json` (MỚI, `pipeline/do_mat.py`): với mỗi ảnh có câu thoại chạy qua, gọi vision (`sol_client`, lớp QC có sẵn)
  kèm `look` các nhân vật trong `@CAST` của ảnh → trả `{id, mat:[x1,y1,x2,y2], mieng:[x,y]}` theo tỉ lệ. Chỉ ảnh có thoại mới
  gọi (~40–60% số ảnh).
- Vẽ: câu người kể → hộp trắng chữ dọc (như Lane F hiện có). Câu thoại → bóng trắng bo tròn viền đen, chữ dọc phải→trái,
  đuôi tam giác chỉ về MIỆNG người nói; vị trí = chỗ trống gần người nói nhất, không đè mặt ai. Người nói không có trong ảnh →
  đuôi chỉ ra mép khung phía gần nhất (quy ước manga "lời từ ngoài khung").
- Sửa 3 lỗi của bản thử: chữ nhỏ ゃゅょっ lệch lên-phải · ー、。「」 xoay/đặt đúng kiểu dọc · ngắt cột theo cụm từ (không cắt
  「辞めま/す」).
- `assemble.py` thêm `--bubble` (song song `--tate`), overlay 1 track trong suốt như cách `--tate` đang làm.

## 3. Thứ tự làm + ước lượng
| Bước | Việc | Ai chạy | Ước lượng |
|---|---|---|---|
| 1 | Profile `profiles\profiles\yakkyoku-sukatto.json` (lean, hook video_sinh+sfx, goi_dang, gate ĐO từ 4 transcript, voice VOICEVOX, `fixed_cast`) + đo nghỉ giữa câu từ tiếng gốc | máy 1 | 1–1,5h |
| 2 | C1 + C2 `gan_vai.py` + test trên 1 transcript gốc (máy gắn vai, so với kết quả đo giọng) | máy 1 | 2h |
| 3 | C3 `tts_voicevox.py` + `calibrate` → char-rate | máy 1 test, máy 2 chạy thật | 2h |
| 4 | C4 N ref (`prompt_doan`, `masters_from_bible`, `dong_goi_may2`, `gen_images`) + test hồi quy lane F/G | máy 1 | 2–3h |
| 5 | C5 `do_mat.py` + nâng `tate_text.py` + `assemble --bubble`; test offline 10 ảnh cũ + SRT giả | máy 1 test | 3h |
| 6 | `SOP_LANE_K.md` (§0b DNA, §0c giọng, bảng cột sheet) + router + giao máy 2 cài VOICEVOX | máy 1 | 1h |
| 7 | Tập 1 chạy thật tới hết bước 1 → vẽ thử 5 ảnh trước loạt (luật dự án) → giao máy 2 | máy 1 → 2 | theo tập |

Chi phí mới: 0đ cho giọng (VOICEVOX) · vision `do_mat.py` ~40–60 lượt sol/tập · Character Flow tạo thêm theo số nhân vật.

## 4. Rủi ro đã thấy trước
| Rủi ro | Chặn bằng |
|---|---|
| Model gắn vai sai người nói | máy kiểm §C2 + đối chiếu: câu 「」 không bao giờ là người kể; lớp 3 đọc `vai.txt` lướt 5 phút |
| Vision xác định nhầm ai là ai khi 2 người cùng giới/tuổi | `look` phải khác nhau rõ (áo/tóc/kính) — máy kiểm characters.json trùng look; ảnh ≤3 người |
| Bóng thoại che mặt người thứ 3 | vị trí bóng tránh MỌI hộp mặt trong ảnh, không chỉ người nói; không tìm được chỗ → thu nhỏ chữ 1 nấc rồi đặt góc trên |
| Máy 2 chưa cài VOICEVOX | `tts_voicevox.py` kiểm `/version` đầu tiên → DỪNG kèm lệnh cài |
| Tổng chữ SRT lệch script (nuốt câu) | không thể xảy ra với VOICEVOX từng câu, nhưng cổng vẫn giữ |
