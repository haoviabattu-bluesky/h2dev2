---
title: Mượn 5 mảnh từ hypit + OpenMontage cho pipeline h2dev
date: 2026-09-21
status: approved
type: brainstorm
next: plan.md
---

# 1. Problem Statement
Đọc 2 repo `hypit-ai/hypit` và `calesthio/OpenMontage` (2026-09-21) thấy 5 mảnh mượn được cho
pipeline h2dev (mọi lane). Không dùng nguyên repo nào: hypit là DSL cho UGC 20 giây có A-roll,
OpenMontage là khung agent-first 700 skill — cả hai lệch với video Nhật 25–30′ narration + ảnh tĩnh.
Chỉ port từng ý tưởng/hàm vào code hiện có, không thêm dependency nặng ở các mảnh ưu tiên đầu.

# 2. Requirements (Approved)
Functional (theo thứ tự anh chốt 2026-09-21):
- M3 QC hậu render: kiểm ÂM THANH BẢN GHÉP CUỐI (`final.mp4` sau amix BGM) — clipping, quá nhỏ,
  im lặng bất thường giữa video, BGM lấn giọng. **Phần còn lại của M3 trong báo cáo (ffprobe, khung
  đen, lệch độ dài, phụ đề) đã có sẵn ở B8Q `qc_visual.qc_video` → không làm lại.**
- M4 Dual Text: từ kanji dễ đọc sai có cách đọc riêng cho TTS, caption vẫn hiện kanji.
- M1 Adapter nguồn tư liệu: NARA, LOC (Lane D), JAXA, ESA, NOAA (Lane A) vào `stock_sources.py`.
- M6+M5 WhisperX align ký tự + marker `@{id!}` trong script → mốc đổi cảnh chính xác. **Điều kiện: có máy GPU rảnh.**
- M2 Corpus CLIP cho Lane A. **Điều kiện: Lane A ≥1 tập/tuần.**
Non-functional: mỗi mảnh ≤ 200 dòng/file · không phá contract file đang có (`script.txt`,
`manifest.jsonl`, `qc_video.json`) · QC tất định, không gọi model · fail hạ tầng ném lỗi, không nuốt.

# 3. Tech Stack (Approved)
Python 3.13 (`py -3.13`), ffmpeg qua `imageio_ffmpeg` (đã có), `requests` (đã có).
M6: `whisperx` + model align ja (mới, ~1.2 GB). M2: `torch` + `transformers` CLIP ViT-B/32 (mới, 350 MB).

# 4. Evaluated Approaches
| Approach | Pros | Cons | Decision |
|---|---|---|---|
| A. Cài nguyên OpenMontage, chạy pipeline của nó | có sẵn mọi thứ | agent-first 700 skill, không có SOP lane, tiếng Nhật không phải ưu tiên, trùng 80% với make_video.py | Rejected |
| B. Cài hypit skill + viết SVML cho video Nhật | timing neo từ rất đúng | cần A-roll/WhisperX cho mọi tập, render Chromium nặng, DSL mới cho toàn bộ lane | Rejected |
| C. Port từng hàm/ý tưởng vào pipeline h2dev hiện có | không đổi contract, mỗi mảnh ≤1 ngày, đo được | phải tự viết lại, không hưởng update upstream | **Selected** |
| M4-a. Inline `<表示\|読み>` trong `script.txt` (như hypit) | chính xác từng lần xuất hiện | **39 file** đọc `script.txt` (gate đếm chữ, qc, publish…) phải hiểu cú pháp mới | Rejected |
| M4-b. Sidecar `yomi.txt` (`表示=読み` mỗi dòng), chỉ `tts.py` áp | đụng 1 file, script.txt giữ nguyên | thay toàn cục, không phân biệt 2 cách đọc cùng chữ trong 1 tập | **Selected** (truyện 1 tập cùng chữ cùng đọc ~99%) |
| M3-a. Viết `qc_render.py` mới | tách bạch | thêm bước B mới + state mới, trùng B8Q | Rejected |
| M3-b. Thêm khối kiểm tiếng vào `qc_visual.qc_video` (B8Q) | tái dùng `qc_audio.do_muc`/`khoang_lang`, report đã có | qc_visual.py dài thêm ~50 dòng | **Selected** |

# 5. Final Architecture
```
B4  tts.py ──(đọc yomi.txt → thay 表示→読み trước khi gửi OpenSpeaker)──▶ voice.mp3 + voice.srt   [M4]
B5  stockfetch.py --sources nasa,commons,nara,loc,jaxa,esa,noaa ──▶ kho + manifest.jsonl          [M1]
B8  assemble.py ──▶ final.mp4
B8Q qc_visual.qc_video ── + kiem_tieng_ghep(final.mp4, voice.mp3) ──▶ qc_video.json problems[]     [M3]
      ├ max_volume > -0.5 dB        → "VỠ TIẾNG bản ghép"
      ├ mean_volume < -30 dB        → "tiếng quá nhỏ"
      ├ khoảng lặng ≥ 8 s ở giữa    → "mất tiếng từ t1→t2"
      └ mean(final) − mean(voice) > +3 dB → "BGM lấn giọng"
(sau) B4  whisperx align ja → char timing ──▶ align script @{id!} ──▶ timeline.json → assemble    [M6+M5]
(sau) B5  corpus CLIP: embed kho 1 lần → rank_for_slot/diversify theo câu script                  [M2]
```

# 6. Project Structure
```
pipeline/qc_visual.py        (+ kiem_tieng_ghep, gọi trong qc_video)      [M3]
pipeline/tts.py              (+ ap_yomi(text, yomi_path))                  [M4]
pipeline/stock_sources.py    (+ nara, loc, jaxa, esa, noaa)                [M1]
pipeline/stockfetch.py       (+ dispatch 5 nguồn)                          [M1]
pipeline/align_whisperx.py   (mới, sau)                                    [M6]
pipeline/corpus_clip.py      (mới, sau)                                    [M2]
assets/<lane>/<ep>/yomi.txt  (sidecar, tuỳ chọn)                           [M4]
```

# 7. Implementation Phasing
| Phase | Deliverable | Effort |
|---|---|---|
| 1 | M3 — kiểm tiếng bản ghép trong B8Q, bắt được file cố ý làm vỡ tiếng | 0.5d |
| 2 | M4 — `yomi.txt` + `tts.py` áp đọc; QC cảnh báo mục yomi không có trong script | 0.5d |
| 3 | M1 — 5 adapter nguồn + dispatch; `--dry-run` ra kết quả thật từng nguồn | 1d |
| 4 | M6+M5 — WhisperX align ja + marker → timeline.json (**chờ GPU**) | 2d |
| 5 | M2 — corpus CLIP Lane A (**chờ điều kiện ≥1 tập/tuần**) | 1.5d |

# 8. Risks & Mitigations
| Rủi ro | Giảm thiểu |
|---|---|
| M3 báo oan "im lặng" ở đoạn nghỉ cố ý sau pace_audio (nghỉ dài nhất đo ~3 s) | ngưỡng 8 s, chỉ tính khoảng nằm trong [5 s, dur−5 s] |
| M3 "BGM lấn" đo trên mean toàn file bị BGM intro/outro làm lệch | so mean trên đoạn giọng đang nói (lấy cửa sổ 60 s giữa file) |
| M4 thay toàn cục sai chỗ (chữ có 2 cách đọc) | yomi.txt do người/Fable chọn từ; QC in số lần thay mỗi mục để soi |
| M1 API nguồn đổi/chặn (JAXA scrape HTML, LOC JSON) | mỗi nguồn try/except riêng như hiện tại; dry-run smoke từng nguồn |
| M6 WhisperX ja trên CPU 30′ audio quá chậm | chỉ làm khi có GPU; fallback giữ srt_from_script |

# 9. Success Criteria
- P1: file `final.mp4` cố ý ghép BGM volume 3.0 → B8Q báo "VỠ TIẾNG" (max_volume ≥ −0.5 dB); file tập thật đã giao → 0 problem tiếng.
- P2: script chứa 他人様, `yomi.txt` có `他人様=ひとさま` → text gửi OpenSpeaker chứa ひとさま, `voice.srt`/caption vẫn 他人様; log in "yomi: 3 mục, thay 7 lần".
- P3: `stockfetch.py --dry-run --sources nara,loc,jaxa,esa,noaa --q "iwo jima 1945"` liệt kê ≥1 item/nguồn (nguồn nào 0 phải in lý do), manifest có `license` + `source_url`.
- P4/P5: ghi khi mở phase.

# 10. Decisions Locked
1. Port từng mảnh (approach C), không cài repo nào vào h2dev.
2. Thứ tự: M3 → M4 → M1 → M6+M5 (chờ GPU) → M2 (chờ điều kiện).
3. M3 = chỉ phần TIẾNG bản ghép, cắm vào B8Q hiện có; không tạo bước B mới.
4. M4 = sidecar `yomi.txt`, `script.txt` giữ nguyên contract.
5. M1 = thêm hàm vào `stock_sources.py` + dispatch `stockfetch.py`; chọn nguồn qua `profile.body.stock_sources` như hiện tại.
6. Mọi QC mới tất định, 0 đồng; lỗi hạ tầng → `infra[]`, không PASS ảo.

# 11. Out of Scope
- Không dùng Remotion/HyperFrames, Backlot, Piper, caption karaoke, decision_log JSON.
- Không đổi `assemble.py` (mix, loudnorm) — chỉ ĐO, không tự sửa tiếng.
- Không sửa prompt Fable để tự sinh `yomi.txt` ở phase 2 (ghi tay/Claude ghi; tích hợp prompt là việc sau nếu thấy cần).
- Không port `slideshow_risk`, `video-reference-analyst`, research-brief schema (chỉ là checklist, đã ghi trong báo cáo chat).

# 12. Next Step
Viết `plan.md` + `phase-01-qc-tieng-ban-ghep.md` → anh duyệt → code phase 1.
