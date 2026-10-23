# ĐỘ DÀI HOOK = HOOK GỐC · CHỈ NHẠC NỀN · KIỂM BỐI CẢNH CẢNH (§2 §3 anh chốt 01/10/2026, Lane J ep02 · §1 sửa 17/10/2026)

## 1. Độ dài hook = độ dài hook video gốc (17/10/2026)
- Độ dài hook = độ dài hook video gốc, kẹp trong `script.hook.giay` của lane; storyboard 3–22 cảnh / 12–120s
  (`pipeline\hook_storyboard.py`). Luật viết: `E:\CLAUDE\YOUTUBE\h2dev\docs\HOOK_CAU_TRUC\00_CHUNG.md`. (Luật cũ "mặc định 20–30s /
  dài tới hết cao trào `den_cao_trao`" đã xoá.)
- **Số cảnh video hook = đủ số cảnh của hook đã khoá** (khoá N câu đầu bằng `hook_stage.khoa`, mẫu: `assets\J-teinengo-fuufu\ep02-sotsukon\_khoa_hook26.py`).
  Không được cắt bớt hook đã khoá. **Ranh giới cảnh PHẢI trùng ranh giới câu** (1 câu không bị cắt đôi giữa 2 clip) — `_mk_hook.py` ghi `shots[].cau=[a,b]`.
- Mỗi cảnh 3–6,5s = 1 clip Grok 6s. Tài khoản Grok nhiều → làm CẨN THẬN: QC từng ảnh (`qc_hook_clip.py --anh N`) rồi từng clip (`--clip N`); FAIL → sửa prompt + chạy lại ngay bằng profile khác.

## 2. Âm thanh hook = CHỈ NHẠC NỀN (MỌI lane)
- CẤM mọi hiệu ứng âm thanh đồ vật (chuông cửa, máy khâu, bước chân, tiếng giấy…). Cảnh buồn → nhạc buồn, không có tiếng máy khâu.
- Profile: `script.hook.sfx: false` + `script.hook.nhac_nen: true` (cổng `qc_goi_dang.cong_truoc_khi_viet` chặn nếu sai). Body video: `assemble.sfx.enabled: false`.
- `hook_timeline.json`: `"sfx": []` + `"nen": {"file":"sfx/99_nhac_buon.mp3","loai":"nhac",...}`. `ghep_hook_noi_truoc.py` và `tools\hook_lane_g\xem_thu_hook.py` BỎ QUA mọi `sfx[]` còn sót ở tập cũ.
- Sinh nhạc: **CẤM dùng `sfx.py` (sound-effect) làm nhạc nền** — ra đoạn 1,54s lặp "ting tong" gây đau đầu (anh chê ep02 Lane J, 01/10).
  ⛔ **(23/10) CẤM Suno** (`openspeaker_tts.generate_music()` đã khoá, `tao_nhac_hook.py` bỏ). Nhạc hook = cắt 1 đoạn liền ≥ độ dài hook
  (không lặp), fade-in 2s, −16 LUFS từ **bài Thư viện âm thanh YouTube của lane**: `py -3.13 -X utf8 pipeline\nhac_hook_tu_thu_vien.py
  --tap <tập> --lane <mã lane> --giay <độ dài hook>` → `hook\sfx\99_nhac_piano.mp3` (+ `.nguon.json`). Luật đầy đủ: `docs/QUY_TAC_NHAC_NEN.md`.

## 3. TRƯỚC KHI lập storyboard: kiểm bối cảnh thật của từng câu
- Đọc kịch bản xác định cảnh là **gọi điện thoại** hay **gặp mặt**. Gọi điện → mỗi cảnh chỉ MỘT người, có điện thoại trong tay, hai người ở hai nơi, KHÔNG chung khung hình.
- Ghi bối cảnh vào `<tập>\hook\ghi_chu_canh.txt` (storyboard tự đọc và bắt buộc tuân theo). Sai bối cảnh = làm lại cảnh (bài học ep02 Lane J: máy 1 dựng thành cuộc nói chuyện trực tiếp trong tiệm sửa đồ trong khi kịch bản là gọi điện).
- Câu thoại mà kịch bản đòi cảm xúc cụ thể (vd vợ nói 「まだ分かってないのね」) phải có cảnh **cận mắt** thể hiện đúng (đăm chiêu, khó hiểu — không cười, không giận).
