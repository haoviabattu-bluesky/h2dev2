# HẠ TẦNG TTS — AI33.PRO / OPENSPEAKER (dọn từ CLAUDE.md 2026-09-29)

ai33.pro = **OpenSpeaker** (openspeaker.ai) — proxy ElevenLabs/MiniMax/Fish/Vbee giá $5/1.000.000
credit. Đã mua gói, tài khoản ~1.003.209 credit. Voice trả phí CHÍNH cho satori (chất ElevenLabs);
edge-tts free trong `pipeline/tts.py` giữ làm fallback. API mechanics đầy đủ (endpoint, poll pattern,
voice-clone, pitfall UTF-8/curl) đã đóng gói ở skill dùng chung mọi dự án:
`C:\Users\admin\.claude\skills\openspeaker_voice_clone.md`.

- **API key:** `AI33_API_KEY=sk_vdplz671t7nq190rwxrwd52lj30z1giekav30rh0mkaqzleo` (header `xi-api-key`,
  KHÔNG có prefix Bearer). Base: `https://api.openspeaker.ai`.
- **HAI TÀI KHOẢN CHẠY ĐAN XEN (anh chốt 2026-09-27)** — `AI33_API_KEY_2` (khoá `openspeaker2`).
  ai33 chặn **theo TÀI KHOẢN**: `queue_limit_exceeded` "You have too many tasks in queue (10/10)".
  Đo thật: ép khoá 1 đầy rồi bắn khoá 2 từ CÙNG máy, cùng lúc → khoá 1 chặn 199 lần, khoá 2 qua 5/5.
  Thêm khoá của CÙNG tài khoản thì vô ích. `pipeline/openspeaker_tts.py` nay tự xoay vòng 2 khoá và
  đổi khoá ngay khi bị chặn (không nằm chờ); `poll()` tự hỏi đúng khoá đã gửi. Nghiệm thu: 18 task
  liên tiếp chia đều 9/9, 4,9 giây, 0 lỗi; khoá 1 đầy thì 4/4 lượt sau tự sang khoá 2 trong 0,5 giây.
  Giọng clone DÙNG CHUNG được giữa 2 tài khoản (clone nằm ở tầng MiniMax) — đã verify ra mp3 nghe được.
- **Chi phí đo thật:** 49 chữ Nhật = 62 credit. Video 30' ~10k chữ ≈ 13k credit → gói $5 ≈ 75–90 video
  30' (~1.500đ/video). Task fail tự hoàn credit.
- Giọng đang dùng cho `satori-jp-obaa`: xem `docs/SOP_SATORI_JP.md` §B4 (hệ thống `channels.json`
  per-kênh — KHÔNG chép giọng cụ thể vào tài liệu chung, dễ lệch khi đổi kênh/giọng mà quên sửa 2 chỗ).
