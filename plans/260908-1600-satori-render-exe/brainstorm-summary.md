---
title: Satori Render Engine — tool .exe render 1-click cho pipeline video Satori JP
date: 2026-09-08
status: approved
type: brainstorm
next: /ck:plan
---

## 1. Problem Statement
Pipeline sản xuất video Satori JP (`pipeline/`) gồm ~9 bước cơ học (giọng→reflow→giãn nhịp→gen ảnh→QC→thumbnail→ghép→QC) hiện phải gõ tay từng lệnh trong Claude Code. Cần 1 tool .exe để render 1-click 1 slug đã chuẩn bị, không cần Claude ngồi gõ lệnh, chạy trên máy có sẵn py -3.13.

## 2. Requirements (Approved)
- **Functional:** nhận 1 thư mục slug đã có `script.txt + characters.json + img_prompts.txt + thumb_text.txt + masters (_ref/…)`; chạy tuần tự B4 voice → B4.1 reflow → B4Q → B4.2 pace → B5 gen ảnh → B5Q → B7 thumbnail → B8 ghép → B8Q; hiện tiến độ (step i/N) + log realtime + kết quả QC; nút DỪNG cắt được (taskkill cây, ảnh tốn tiền). Resume: bỏ qua bước đã có output.
- **Non-Functional:** GUI PySide6 dark theme; exe standalone (không cần Python cho GUI), nhưng GỌI py -3.13 của máy cho pipeline (không bundle whisper/numpy/torch); an toàn — không xoá dữ liệu; key/API không nằm trong exe (pipeline scripts giữ key, không bundle chúng vào exe).

## 3. Tech Stack (Approved)
- GUI: **PySide6** (QThread + subprocess), đóng gói **PyInstaller --onedir --windowed**.
- Engine: **`pipeline/render_engine.py`** — orchestrator CLI thuần (subprocess gọi các script pipeline bằng `sys.executable`/py-3.13), KHÔNG import deps nặng.
- Bridge pattern (skill tao_tool_exe #23): GUI(.exe) → Popen `py -3.13 render_engine.py --slug <abs>` → từng script pipeline.

## 4. Evaluated Approaches
| Approach | Pros | Cons | Decision |
|---|---|---|---|
| **A. Render-engine 1-click** (Claude soạn script/prompt/bible/master; exe render cơ học) | Chất lượng cao (Claude viết văn/prompt), engine tất định ổn định, exe mỏng | Vẫn cần Claude cho phần sáng tác | ✅ **SELECTED** (user chốt) |
| B. Toàn tự động (exe tự gọi LLM viết script+prompt) | Standalone hẳn | Chất lượng script/prompt thấp, rủi ro lỗi logic/nhất quán cao | ❌ Rejected |
| C. Hộp công cụ từng nút rời | Linh hoạt | Không 1-click, thao tác nhiều | ❌ Rejected |
| GUI bundle cả pipeline deps | 1 exe chứa hết | ~1-2GB, whisper/torch khổng lồ, build lâu | ❌ Rejected → GUI gọi py-3.13 ngoài |

## 5. Final Architecture
```
[Satori Render.exe  (PySide6, mong)]
  slug picker + options + ▶RENDER + progress + log + STOP
        │ Popen  py -3.13 pipeline/render_engine.py --slug <abs> [--no-pace ...]
        ▼
[render_engine.py  (orchestrator CLI, thuan subprocess)]
  in "[STEP i/9] ten"  ->  goi tung script:
    tts.py · srt_from_script.py · qc_visual.py voice · pace_audio.py
    · gen_images.py (--ref/--ref2 doc tu characters.json) · qc_visual.py images
    · thumbnail_text.py · assemble.py · qc_visual.py video
  resume: bo qua buoc da co output. Doc characters.json -> master paths.
config.json (canh exe): { project_root, python_cmd }
```

## 6. Project Structure
```
pipeline/render_engine.py        ← engine CLI (MỚI)
tools/satori_render_gui.py       ← GUI PySide6 (MỚI)
tools/build_satori_gui.bat       ← build exe (MỚI)
tools/satori_gui_config.json     ← project_root + python_cmd (MỚI, mẫu)
plans/260908-1600-satori-render-exe/  ← docs
```

## 7. Implementation Phasing
| Phase | Deliverable |
|---|---|
| 1 (P1 PROBE/FOUND) | `render_engine.py` CLI: orchestrate 9 bước, resume, --dry-run, in STEP i/N. Smoke: render 1 slug ra final.mp4 |
| 2 (P1 MVP) | GUI PySide6 gọi engine qua subprocess: slug picker, progress, log, STOP taskkill-tree |
| 3 (P1 SHIP) | Build .exe (PyInstaller), --selftest, config.json cạnh exe |
| 4 (P2 POLISH) | Toggle từng bước, nút mở thư mục output, README |

## 8. Risks & Mitigations
| Risk | Mitigation |
|---|---|
| Gen ảnh tốn tiền, DỪNG không cắt cháu | taskkill /F /T cả cây (#24) |
| Rebuild exe xoá dữ liệu output nằm trong dist\ | data/slug NẰM NGOÀI dist\ (assets/), config trỏ project_root ngoài (#29) |
| exe --windowed nuốt lỗi | nhánh --selftest ghi selftest.log (#20) |
| py -3.13 không tìm thấy | config.json python_cmd + dò `py -3.13`/`python` |
| Bước lỗi giữa chừng | engine dừng + in lỗi rõ; GUI hiện đỏ; resume chạy lại bỏ bước đã xong |

## 9. Success Criteria (đo được)
- `render_engine.py --slug <slug đã chuẩn bị>` → tạo `final.mp4` + `thumb_final.png`, in đủ 9 STEP, exit 0, QC in kết quả.
- GUI: bấm RENDER → progress chạy 1→9, log realtime; bấm STOP giữa gen ảnh → tiến trình py con chết trong ≤3s (đếm không sinh thêm ảnh).
- `.exe --selftest` → selftest.log ghi BASE/frozen/python_cmd/project_root OK.

## 10. Decisions Locked
1. Phạm vi = **render-engine 1-click** (Claude soạn nội dung, exe render cơ học). KHÔNG tự viết script/prompt bằng LLM trong exe.
2. GUI **PySide6 → .exe --onedir --windowed**.
3. Engine gọi **py -3.13 ngoài** (không bundle deps pipeline). GUI exe chỉ chứa PySide6.
4. Input slug = thư mục `assets/satori_jp/<slug>/` đã có script/characters/img_prompts/thumb_text + masters `_ref*`.
5. Resume theo output tồn tại. DỪNG = taskkill cây.
6. config.json (project_root + python_cmd) cạnh exe.

## 11. Out of Scope
- KHÔNG viết script/prompt/bible bằng LLM trong exe (Claude làm).
- KHÔNG gen/QC master trong exe (Claude gen+QC+đặt masters trước) — engine chỉ dùng masters có sẵn (Phase 1); có thể thêm sau.
- KHÔNG upload YouTube, KHÔNG sửa Google Sheet.
- KHÔNG bundle key/credentials vào exe.

## 12. Next Step
`/ck:plan` → viết plan.md → code phase 1 (render_engine.py).
