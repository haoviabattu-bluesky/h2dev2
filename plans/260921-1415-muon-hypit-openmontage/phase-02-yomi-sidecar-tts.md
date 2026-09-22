---
phase: 2
title: "M4 — yomi.txt sidecar: TTS đọc theo cách đọc chỉ định, caption giữ kanji"
status: completed
completed: 2026-09-21
priority: P1
effort: "0.5d"
dependencies: []
smoke_test: "PASS — unit: 3 mục/他人様×3+満州×1 → thay đúng, mục thừa đếm 0 · thật: openspeaker enishi 40 chữ 51 credit 7s, log [yomi] 3 mục · thay 2 lần · ⚠️ 幻の語; STT server ghi 人様 (=ひとさま, chứng tỏ đọc đúng); srt_from_script trả caption về kanji, phủ 97.2% · không có yomi.txt → 0 dòng [yomi]"
---

## Overview
Ý tưởng Dual Text `<表示|読み>` của hypit, thu về dạng sidecar để không đụng 39 file đang đọc
`script.txt`. `yomi.txt` đặt cạnh `script.txt`, mỗi dòng `表示=読み`; `tts.py` thay trước khi gửi
provider. Phụ đề vẫn ra kanji vì B4a `srt_from_script.py` bám `script.txt` (make_video.py:886).

## Context Links
- brainstorm §4 (M4-a bị loại vì 39 consumer), §10 mục 4
- Hook: `pipeline/tts.py:363` (`text = clean(...)`), B4 `make_video.py:861` (không cần sửa — tts.py tự tìm yomi.txt cạnh script)

## Requirements
1. `ap_yomi(text, path) -> (text, thong_ke)`; dòng trống/`#` bỏ qua; thay TOÀN CỤC theo thứ tự dòng (mục dài đặt trước mục ngắn để tránh cắt chữ: sort theo len(表示) giảm dần).
2. `--yomi` tuỳ chọn; mặc định `<script>.parent/yomi.txt` nếu tồn tại; không có file → im lặng.
3. Log: `[yomi] N mục · thay M lần` và liệt kê mục 0 lần thay (chữ không có trong script = mục thừa/sai chính tả) — cảnh báo, không dừng.
4. Áp cho cả 2 provider (openspeaker/edge) vì hook trước nhánh rẽ.
Non-functional: ≤ 40 dòng; không đổi `script.txt`; không đổi chữ ký hàm khác.

## Related Code Files
- Modify: `pipeline/tts.py`

## Acceptance Criteria
- [x] script chứa 他人様 ×3, yomi `他人様=ひとさま` → text gửi provider chứa ひとさま ×3, log "1 mục · thay 3 lần".
- [x] yomi có mục không xuất hiện → log cảnh báo "0 lần: …", vẫn chạy.
- [x] Không có yomi.txt → hành vi y hệt cũ.
- [x] Chạy TTS thật 1 câu ngắn qua openspeaker để nghe đúng cách đọc (tốn ~60 credit).

## Smoke Test
Unit: gọi `ap_yomi()` trực tiếp bằng `py -3.13 -c`. Thật: `tts.py --script <tmp>/script.txt --out <tmp>/v.mp3 --provider openspeaker --voice <giọng lane>`.

## Ghi nhận khi test
- `srt_from_script.py` làm rơi chữ đầu cue khi STT bỏ sót ký tự đầu (STT nghe 人様, script 他人様 → caption ra 人様). Lỗi có sẵn của difflib reflow, không do phase này; sẽ được thay khi làm phase 4 (align ký tự WhisperX).
