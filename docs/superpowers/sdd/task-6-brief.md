# TASK 6 BRIEF — tài liệu hoá P0 (KHÔNG đổi logic production)

Phạm vi (anh chốt 2026-09-18): CHỈ cập nhật tài liệu + memory + số đo. Cấm sửa `.py` trừ lỗi chính tả trong docstring/comment. Cấm chạy lại LLM/regression (số đo lấy từ report đã có).

## Nguồn số liệu thật (đọc, không bịa)
- `docs/superpowers/sdd/progress.md` (ledger 5 task), `task-2-report.md`, `task-3-report.md`, `task-4-report.md`, `task-5-report.md`.
- `docs/superpowers/plans/2026-09-18-p0-buoc1-gates.md` mục "Số đo thật".
- Code thật để đối chiếu khi viết lệnh/điều kiện: `pipeline/brain_channel.py` (`make_video_one`, dòng ~419-670), `pipeline/brain_steps.py` (`NEED_BY_PHASE`, `phase`), `pipeline/hybrid_chuan_bi.py` (khối rào trước "E. anchors"), `pipeline/gate_common.py`, `pipeline/qc_transcript.py`, `pipeline/qc_prompt_consistency.py`, `pipeline/qc_img_doan.py`.

## 7 việc phải ghi (đúng thứ tự anh yêu cầu)

1. **Cập nhật SOP/CLONE_BRAIN/memory** — file cụ thể ở mục "File sửa" dưới.
2. **Thứ tự pipeline mới** (chép đúng từ `task-5-report.md` §1):
   `competitor.txt → B2Q → pha SCRIPT (claude -p phase="script", chỉ khi thiếu script.txt) → cổng số → B3Q (≤3 vòng, không hội tụ → ESCALATION_REPORT.md) → pha ASSETS (phase="assets", chỉ khi thiếu asset, ≤2 lượt, cấm sửa script) → stamp fingerprint artifact_meta.json → STALE-check → REF-LOCK → B5P → B55 mapping → ⏸ dừng trước render → giao máy 2 (ảnh) → Hermes (ghép)`.
3. **Điều kiện PASS/WARN/FAIL/SKIPPED** từng cổng mới:
   - B2Q: PASS; WARN (coverage 80-92%, gap>45s, cpm<120, không có thời lượng); FAIL (coverage<80%, duplicate>15%, transcript rỗng, sidecar hỏng); SKIPPED (không có `competitor.segments.json`).
   - STALE: FAIL khi sha256(script.txt) ≠ `generated_from_script_sha256` của img_prompts/img_doan; WARN khi artifact sửa tay sau stamp (script không đổi) hoặc chưa có meta mà mtime hợp lệ; FAIL khi chưa có meta VÀ mtime script mới hơn artifact >2s.
   - B5P: FAIL cơ học (số prompt ≠ số dòng img_doan, @REF/@REF2 thiếu nhân vật, prompt rỗng, STALE, LLM lỗi hạ tầng); WARN (PROMPT_CONFLICT hoặc AMBIGUOUS — mode warn); PASS. `--mode fail` chỉ dùng hồi quy, CHƯA bật production.
   - B55 mapping: FAIL cơ học (malformed, ≠ số prompt, thiếu/thừa/trùng ID, đoạn ngoài 1..N, giảm thứ tự, STALE, thiếu img_doan.txt, LLM lỗi hạ tầng); WARN (SUSPICIOUS chia đều/lệch bất thường; semantic ≤2 — mode warn; `--no-llm` khi SUSPICIOUS); PASS.
   - `would_block` (B5P/B55) = số ca sẽ bị chặn NẾU bật `--mode fail` — đọc ở `logs/<gate>_latest.json → metrics.semantic`; sau 2 tập mới quyết bật.
4. **Migration tập cũ chưa stamp**: (a) tập chưa có `artifact_meta.json` → chạy `py -3.13 qc_prompt_consistency.py --slug <d>` + `qc_img_doan.py --slug <d>` xem prompt/mapping còn khớp script hiện tại không, RỒI MỚI `py -3.13 gate_common.py --slug <d> --stamp`; cấm stamp mù cho tập biết là stale (STT7: script 07:58 mới hơn prompt 07:35 → phải rà prompt trước). (b) Tập đã giao hàng (ep01/04/06/07…) KHÔNG cần stamp trừ khi làm lại. (c) STT3 đã stamp (Task 1); STT8/STT2/STT5 chưa — stamp khi đụng tới.
5. **B2Q `SKIPPED` được đi tiếp khi nào**: CHỈ khi `competitor.txt` được bóc TRƯỚC P0 (không có sidecar `competitor.segments.json`). Tập bóc bằng `fetch_script.py` từ 2026-09-18 trở đi LUÔN có sidecar — nếu tập mới mà B2Q báo SKIPPED thì là lỗi pipeline (fetch không ghi sidecar), phải xem lại, không được coi là qua.
6. **Số đo thật** (chép đúng số từ report, ghi kèm ngày 2026-09-18, tập STT3 128 prompt/50 đoạn):
   - B55 mapping: 7 lời gọi, tok_in 20.077 / tok_out 4.883, 86s (bản gán tay: WARN 16/128, would_block 16); bản lỗi 2-3-2-3 `--mode fail`: FAIL 108/125, 6/6 ảnh mục tiêu, 110s.
   - B5P: 14 lời gọi (5 facts + 9 batch), tok_in ≈39-40k / tok_out ≈10.8k, 190-235s; hồi quy prompt cũ 5/5 (022/028/112/113/114) ở cả 3 run; bản sửa 4/5 sạch, 113 flag 1/3 run có lý do; 8 lỗi prompt thật mới phát hiện (002/027/074/081/082/111/118/125).
   - Flow B smoke STT3 copy: 23,7 phút (B3Q tầng 2 12,1'; B5P 7,2'; mapping 3,4'; 21 lời gọi LLM), 0 ✗, không gọi `claude -p` viết.
   - B2Q trên Kmxva85WKec: nguồn api, 694 đoạn, coverage 1.0, cpm 341.9, PASS.
   - Chi phí thêm/tập ≈10,6 phút + 21 lời gọi gemini-3.8-flash.
7. **Production flow = dừng trước render**: `make_video_one(..., stop_before_render=True)`; nhánh `render_engine.py` cuối hàm chỉ cho test/tập non-hybrid cũ; handoff = máy 2 vẽ ảnh → Hermes ghép (không đổi).

## File sửa (mỗi chỗ ngắn, có lệnh copy-paste; KHÔNG viết lại cả file)
- `docs/SOP_SATORI_JP.md`: bảng "CỔNG QC BẮT BUỘC" thêm 3 dòng B2Q / B5P / B55 (lệnh + PASS khi); mục B2 thêm 1 dòng chạy `qc_transcript.py` + quy tắc SKIPPED (mục 5); mục B5 sau đoạn hybrid thêm 3 dòng: sau khi viết `img_prompts.txt`+`img_doan.txt` → `gate_common.py --stamp` → `qc_prompt_consistency.py` → `qc_img_doan.py`, đọc `would_block`.
- `docs/SOP_CLONE_BRAIN.md`: "THẺ CHẠY" bước 2 đổi thành thứ tự mục 2 (2 pha + 3 cổng mới), bảng cổng thêm 3 dòng; thêm mục nhỏ "Migration tập cũ" (mục 4) và "Production = dừng trước render" (mục 7); giữ nguyên phần còn lại.
- `docs/QUY_TRINH_BUOC1_SATORI_JP_TOAN_DIEN.md`: mục 3 thêm B2Q (sau B2), B5P + B5.5-QC (sau B5.5), ghi 2 pha ở mục 6; mục 4 bảng cổng thêm 3 dòng; mục 8 "Gợi ý tối ưu" đánh dấu 3 ý đã làm (thứ tự B3Q→B5, cổng prompt-vs-script, mapping QC) + ghi số đo mục 6.
- `docs/GIAO_VIEC_HYBRID_COMPOSITOR.md` §3c bảng phân việc: thêm dòng "Rào STALE + mapping invariant | Bước 1 | `hybrid_chuan_bi.py` (trước `sinh_neo.py`)".
- `docs/superpowers/plans/2026-09-18-p0-buoc1-gates.md`: mục "Số đo thật" bổ sung dòng Task 4/5 (B2Q, flow B smoke) nếu chưa có; tick `- [x]` các task 1-6.
- Memory: tạo `C:\Users\admin\.claude\projects\e--CLAUDE-YOUTUBE-h2dev\memory\p0-buoc1-gates-2026-09-18.md` (frontmatter `name/description/metadata.type: project`), nội dung = mục 2, 3 (rút gọn), 4, 5, 7 + đường dẫn log (`<slug>/logs/<gate>_latest.json`, `ESCALATION_REPORT.md`, `artifact_meta.json`) + "chưa bật --mode fail, đo 2 tập đầu". Thêm 1 dòng vào `MEMORY.md` (≤150 ký tự): `- [★ P0 cổng bước 1 đã nối flow](p0-buoc1-gates-2026-09-18.md) — B2Q/B5P/B55 tự chạy, 2 pha script→assets, STALE chặn cứng, WARN-only 2 tập, production dừng trước render`.

## Kiểm sau khi sửa
- `py -3.13 -m pytest tests -q` vẫn 41 passed (không đụng code).
- `grep -n "qc_transcript\|qc_prompt_consistency\|qc_img_doan\|--stamp" docs/SOP_SATORI_JP.md docs/SOP_CLONE_BRAIN.md docs/QUY_TRINH_BUOC1_SATORI_JP_TOAN_DIEN.md` ra ≥ 8 dòng.
- Memory file có frontmatter hợp lệ; MEMORY.md có đúng 1 dòng mới.

## Báo cáo
Ghi `docs/superpowers/sdd/task-6-report.md`: file sửa + số dòng thêm/bớt, trích 3-5 đoạn đã chèn, kết quả grep + pytest. Trả về đây CHỈ: status, 1 dòng tóm tắt file đã sửa, concerns.
