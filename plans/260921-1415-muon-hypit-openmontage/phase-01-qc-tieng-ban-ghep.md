---
phase: 1
title: "M3 — kiểm tiếng bản ghép cuối trong B8Q"
status: completed
completed: 2026-09-21
priority: P1
effort: "0.5d"
dependencies: []
smoke_test: "PASS — Lane D ep08 final.mp4 (567s) ĐẠT max -1.7/mean -19.5 dB 10.6s · Lane A ep03 có BGM (1654s) ĐẠT max -2.5/mean -19.2 vs voice -19.1, 35s · 3 file cố ý hỏng (90s): amix+9dB → VỠ TIẾNG +0.0 dB & BGM LẤN +8.6 dB · im 30-42s → MẤT TIẾNG 14s 29→43s · -20dB → quá nhỏ -39.7 dB"
---

## Overview
B8Q hiện chỉ kiểm bản ghép có luồng tiếng và độ dài khớp; mọi phép đo âm (`qc_audio`) chạy ở B4Q trên
`voice.mp3` TRƯỚC khi trộn BGM. Lỗ hổng: vỡ tiếng/BGM lấn/mất tiếng sinh ra ở bước amix (`assemble.py:470`)
không cổng nào bắt. Phase này thêm 4 phép đo tất định lên `final.mp4` vào `qc_visual.qc_video`.

## Context Links
- plan.md phase 1 · brainstorm §5 (sơ đồ), §8 (2 rủi ro báo oan)
- Mẫu tham chiếu: OpenMontage `tools/video/video_compose.py:2440-2495` (volumedetect → silence/clipping)
- Tái dùng: `qc_audio.do_muc()` (volumedetect trên file gốc), `qc_audio.khoang_lang()`, `qc_audio.doc_song()`

## Requirements
Functional:
1. `kiem_tieng_ghep(mp4, voice_mp3=None) -> {"problems": [], "infra": [], "max_db", "mean_db", "lang_dai": [...]}`
2. Vỡ tiếng: `max_volume ≥ -0.5 dB` → problem "VỠ TIẾNG bản ghép: đỉnh X dB".
3. Quá nhỏ: `mean_volume < -30 dB` → problem.
4. Mất tiếng: khoảng lặng ≥ 8 s nằm trong [5 s, dur−5 s] → problem kèm t1→t2 (bỏ đầu/cuối vì fade BGM).
5. BGM lấn: nếu có `voice_mp3`, `mean(final) − mean(voice) > +3 dB` → problem (giọng đã chuẩn mực −16 LUFS ở tts.py:113 nên chênh lớn = BGM to).
6. Gọi trong `qc_video()` ngay sau khối probe; gộp `problems`/`infra` vào `out`; ghi số đo vào `out["tieng"]`.
7. `make_video.b8q_qc` truyền `self.voice_audio()` (không đổi chữ ký cũ: thêm tham số `voice=None`).
Non-functional: ≤ 60 dòng thêm vào qc_visual.py; không gọi model; lỗi ffmpeg → `infra[]`.

## Architecture
Không file mới. Sửa `pipeline/qc_visual.py` (+ hàm, + 3 dòng trong qc_video), `pipeline/make_video.py` (1 dòng truyền voice).

## Related Code Files
- Modify: `pipeline/qc_visual.py:336` qc_video · `pipeline/make_video.py:1304` b8q_qc

## Acceptance Criteria
- [x] File thử: ghép voice + BGM `--bgm-volume 3.0` từ 1 tập thật → qc_video trả problem "VỠ TIẾNG" và "BGM lấn".
- [x] File thử: cắt 12 s giữa voice thành im lặng rồi ghép → problem "mất tiếng t1→t2".
- [x] `final.mp4` của 1 tập đã giao (Lane D ep08 hoặc Lane A ep03) → 0 problem tiếng, in số đo.
- [x] `qc_video.json` có khoá `tieng`.

## Smoke Test
```
cd pipeline
py -3.13 qc_visual.py video --mp4 <ep>/final.mp4 --voice <ep>/voice.mp3 --sample 0 --no-sub   # --sample 0 = bỏ vision, chỉ đo tiếng
# file cố ý hỏng dựng bằng ffmpeg (sine 220Hz amix normalize=0 + volume=9dB / volume=0 trong 30-42s / volume=-20dB)
```
Ghi vào frontmatter: max_db/mean_db của tập thật, và dòng problem của file cố ý hỏng.
