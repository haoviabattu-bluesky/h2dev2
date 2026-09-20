---
title: Satori Render Engine .exe
status: completed
priority: P1
created: 2026-09-08
type: implementation
source: brainstorm-summary.md
---

Tool .exe render 1-click cho pipeline video Satori JP. GUI PySide6 gọi `render_engine.py` (orchestrator py-3.13) chạy 9 bước cơ học từ 1 slug đã chuẩn bị.

## Context Links
- Brainstorm: ./brainstorm-summary.md
- Pipeline: `pipeline/` (tts.py, srt_from_script.py, pace_audio.py, gen_images.py, qc_visual.py, thumbnail_text.py, assemble.py)
- Runbook: `docs/SOP_SATORI_JP.md`
- Skill exe: `C:\Users\admin\.claude\skills\tao_tool_exe.md`

## Phases
| # | Phase | Status | Priority | Effort | Depends On |
|---|---|---|---|---|---|
| 1 | render_engine.py (orchestrator CLI + resume + dry-run) | completed | P1 | 0.5d | — |
| 2 | GUI PySide6 (subprocess bridge, progress, log, STOP) | completed | P1 | 1d | 1 |
| 3 | Build .exe (PyInstaller + selftest + config.json) | completed | P1 | 0.5d | 2 |
| 4 | Polish (toggle bước, mở output, README) | completed | P2 | 0.5d | 3 |

**Smoke tests:**
- Phase 1: `render_engine --slug tsucho-kotae` → resume skip 6 bước nặng, chạy thật 3 QC (B4Q phủ 1.0/655cue · B5Q · B8Q ĐẠT), exit 0, in ✅XONG + TÓM TẮT.
- Phase 2: headless offscreen → MainWindow dựng OK, config load, cmd build đúng, regex STEP parse `[STEP 5/9]`→(5,9,name).
- Phase 3: `Satori Render.exe --selftest` → BASE/frozen=True/config/project_root/render_engine.py/PySide6 OK; launch exe → GUI mở không crash. exe 1MB, total 108MB.
- Phase 4: nút "📂 Mở thư mục" + toggle "Giãn nhịp" (--no-pace) đã có trong GUI.

## Key Dependencies
- Python: **py -3.13** (đã có deps pipeline: requests, numpy, Pillow, imageio-ffmpeg, faster-whisper…).
- GUI build: PySide6 + pyinstaller + pillow (cài cho python build GUI).
- Không cần API key mới (pipeline scripts giữ key sẵn).

## Decisions Locked (từ brainstorm §10)
1. Render-engine 1-click; exe KHÔNG viết script/prompt/master.
2. PySide6 → exe --onedir --windowed.
3. Engine gọi py-3.13 ngoài, không bundle deps pipeline.
4. Input = slug folder đã có script/characters/img_prompts/thumb_text + masters.
5. Resume theo output; STOP = taskkill cây.
6. config.json (project_root + python_cmd) cạnh exe.

## Out of Scope
LLM viết script/prompt/master trong exe · upload YouTube · sửa Sheet · bundle key.

## Success Criteria (Plan-Level)
- [ ] render_engine.py render 1 slug → final.mp4 + QC, exit 0.
- [ ] GUI RENDER chạy 1→9 + STOP cắt py con ≤3s.
- [ ] .exe --selftest → selftest.log OK.

## Next Step
Code phase 1 → smoke test → phase 2.
