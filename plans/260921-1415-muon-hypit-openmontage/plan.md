---
title: Mượn 5 mảnh từ hypit + OpenMontage
status: in-progress
priority: P1
created: 2026-09-21
type: implementation
source: brainstorm-summary.md
---

Port 5 ý tưởng/hàm từ 2 repo vào pipeline h2dev hiện có, theo thứ tự anh chốt. 3 phase đầu làm ngay
(≤1 ngày mỗi phase, 0 dependency mới); 2 phase sau chờ điều kiện (GPU / nhịp sản xuất Lane A).

## Context Links
- Brainstorm: ./brainstorm-summary.md
- Repo đã clone để đối chiếu: scratchpad `.../hypit` (packages/speech-alignment, services/whisperx),
  `.../OpenMontage` (tools/video/stock_sources/, tools/video/video_compose.py:2311-2500, lib/corpus.py, lib/clip_embedder.py)
- Code h2dev đụng tới: `pipeline/qc_visual.py:336` (qc_video), `pipeline/qc_audio.py:101,113` (do_muc, khoang_lang),
  `pipeline/tts.py:304` (run_openspeaker), `pipeline/stock_sources.py`, `pipeline/stockfetch.py:141`

## Phases
| # | Phase | Status | Priority | Effort | Depends On |
|---|---|---|---|---|---|
| 1 | M3 — kiểm tiếng bản ghép trong B8Q | completed | P1 | 0.5d | — |
| 2 | M4 — `yomi.txt` sidecar + tts.py áp cách đọc | completed | P1 | 0.5d | — |
| 3 | M1 — adapter NARA (LOC/JAXA/ESA/NOAA đã probe và loại, xem phase-03) | blocked (chờ NARA_API_KEY) | P2 | 0.5d | — |
| 4 | M6+M5 — WhisperX align ja + marker `@{id!}` → timeline.json | blocked (chờ GPU) | P2 | 2d | — |
| 5 | M2 — corpus CLIP cho Lane A | blocked (chờ Lane A ≥1 tập/tuần) | P3 | 1.5d | 3 |

Phase 1/2/3 độc lập nhau — có thể chạy song song ở 3 tab.

## Key Dependencies
- Python 3.13, ffmpeg (imageio_ffmpeg), requests — đã có.
- Phase 4: `whisperx` + align model ja, GPU. Phase 5: `torch`, `transformers` (CLIP ViT-B/32).
- API key: LOC/NARA/JAXA/ESA/NOAA đều không cần key.

## Decisions Locked (từ brainstorm §10)
1. Port từng mảnh, không cài repo. 2. Thứ tự M3→M4→M1→M6+5→M2. 3. M3 cắm vào B8Q, không bước mới.
4. M4 = sidecar yomi.txt. 5. M1 = thêm hàm + dispatch, chọn qua profile. 6. QC tất định, infra ≠ PASS.

## Out of Scope
Không Remotion/HyperFrames/Backlot/Piper; không sửa assemble mix; không sửa prompt Fable ở phase 2.

## Success Criteria (Plan-Level)
- [x] Phase 1: file cố ý vỡ tiếng bị B8Q chặn; tập thật đã giao qua sạch.
- [x] Phase 2: TTS đọc theo yomi, caption giữ kanji, log số lần thay.
- [ ] Phase 3: dry-run 5 nguồn ra item thật, manifest đủ license/source_url.
- [ ] Phase 4/5: chỉ khi điều kiện mở.

## Next Step
Duyệt `phase-01-qc-tieng-ban-ghep.md` → code.
