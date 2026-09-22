---
phase: 4
title: "M6+M5 — WhisperX align ký tự + marker @{id!} trong script → timeline.json"
status: blocked
priority: P2
effort: "2d"
dependencies: []
smoke_test: ""
---

## Điều kiện mở phase
Máy GPU rảnh (WhisperX ja: faster-whisper + align model wav2vec2-ja ~1.2 GB; CPU cho audio 30′ ước ~10–15′/tập → không hợp nhịp sản xuất).

## Overview
Thay chuỗi vá hiện tại (`srt_from_script.py` difflib → `pace_audio.py` dò sóng → `qc_audio.py`) bằng
timing ký tự thật: WhisperX `load_align_model(language_code="ja")` cho từng ký tự Han/Kana một mốc
thời gian → align với `script.txt` bằng DP đơn điệu M:N (port từ hypit
`packages/speech-alignment/src/align.ts` 259 dòng + `locate.ts` 473 dòng: chấp nhận exact/split/merge/
replace/omission/insertion; token thiếu timing nội suy theo trọng số giữa 2 láng giềng đã đo).

Marker: script (bản Fable viết) chèn `@{img07!}` ngay trước từ đổi ảnh; `tts.py` strip marker (zero-width)
trước khi gửi; sau align xuất `timeline.json` `{img07: 412.36}` → `assemble.py` đọc thay vì
`do_thoi_luong_neo.py`. Bản `script.txt` khoá SHA256 hiện tại KHÔNG chứa marker — cần quyết định
marker nằm ở file riêng (`script.marked.txt`) hay đổi contract; chưa chốt, hỏi anh khi mở phase.

## Việc cụ thể khi mở
1. `pipeline/align_whisperx.py`: audio → {char, t0, t1} (dùng service pattern của hypit `services/whisperx`, chạy local, cache model).
2. `pipeline/align_script.py`: DP align script ↔ evidence → SRT theo câu thật (ranh giới 。！？) + mốc marker.
3. So với SRT hiện tại trên 3 tập đã giao: đo % cue kết thúc đúng câu (mục tiêu ≥ 95%, hiện ~37% theo narration_audio_pacing_qc.md).
4. Cổng: sửa luôn lỗi ghi nhận ở phase-02 (rơi chữ đầu cue khi STT bỏ sót).
