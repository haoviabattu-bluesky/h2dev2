# TASK 6 REPORT — tài liệu hoá P0 (2026-09-18)

Trạng thái: **DONE**. Không đụng file `.py` nào (kể cả docstring). Không chạy LLM/regression — mọi số đo chép từ
`task-2/3/4/5-report.md` + `progress.md`.

## 1. File sửa + số dòng

| File | Chỗ sửa | Dòng thêm/bớt |
|---|---|---|
| `docs/SOP_SATORI_JP.md` | bảng "CỔNG QC BẮT BUỘC" +3 dòng (B2Q / B5P / B55); mục B2 +1 lệnh `qc_transcript.py` + 4 dòng quy tắc SKIPPED; mục B5 (ngay sau đoạn hybrid) +14 dòng: 3 lệnh `gate_common.py --stamp` → `qc_prompt_consistency.py` → `qc_img_doan.py`, `would_block`, migration | +22 / −0 (297→319) |
| `docs/SOP_CLONE_BRAIN.md` | THẺ CHẠY bước 2: thay đoạn "Bốn cổng" (8 dòng) bằng thứ tự pipeline mới + bảng 8 cổng + `would_block` + mục nhỏ "Migration tập cũ chưa stamp" + "Production = dừng trước render" (39 dòng); bảng §2 +5 dòng (B2Q, 2 pha, Stamp+STALE, B5P, B55) | +36 / −0 (382→418) |
| `docs/QUY_TRINH_BUOC1_SATORI_JP_TOAN_DIEN.md` | mục 3: B2 +1 dòng B2Q (output thêm sidecar), B5.5 +5 dòng (stamp / B5P / B55 / would_block); mục 4 bảng +3 dòng; mục 6 viết lại đoạn mở đầu thành 2 pha + thứ tự đầy đủ + bảng cổng 8 dòng + khối "Số đo thật 2026-09-18"; mục 8 đánh dấu ✅ 3 ý đã làm | +31 / −0 (240→271) |
| `docs/GIAO_VIEC_HYBRID_COMPOSITOR.md` | §3c bảng phân việc +1 dòng "Rào STALE + mapping invariant \| Bước 1 \| `hybrid_chuan_bi.py` (trước `sinh_neo.py`)" | +1 / −0 (262→263) |
| `docs/superpowers/plans/2026-09-18-p0-buoc1-gates.md` | "Số đo thật": thay dòng trống "smoke flow B: … phút" bằng 5 dòng (B2Q Task 4, flow B smoke Task 5 chi tiết từng khúc, hybrid STT3, STT7, Task 6); tick `- [x]` 34/35 step Task 1-6 (giữ `- [ ]` Step 4 Task 6 "xoá `_regress_*`" — chưa xoá, kèm ghi chú) | +5 / −1 |
| `C:\Users\admin\.claude\projects\e--CLAUDE-YOUTUBE-h2dev\memory\p0-buoc1-gates-2026-09-18.md` | MỚI, frontmatter `name/description/metadata.type: project`, nội dung = mục 2/3(rút gọn)/4/5/7 + đường dẫn log + "chưa bật --mode fail, đo 2 tập đầu" + số đo | +53 |
| `...\memory\MEMORY.md` | +1 dòng cuối (99→100) | +1 / −0 |

## 2. Trích đoạn đã chèn

**SOP_SATORI_JP.md — mục B5 (sau đoạn hybrid):**
```
- ⭐ **3 lệnh BẮT BUỘC ngay sau khi viết xong `img_prompts.txt` + `img_doan.txt` (P0, 2026-09-18)** — stamp
  fingerprint rồi chạy 2 cổng, đọc `would_block` (= số ca sẽ bị chặn NẾU bật `--mode fail`; sau 2 tập mới quyết bật):
  py -3.13 gate_common.py --slug ../assets/satori_jp/$SLUG --stamp
  py -3.13 qc_prompt_consistency.py --slug ../assets/satori_jp/$SLUG        # B5P → logs/B5P_latest.json
  py -3.13 qc_img_doan.py --slug ../assets/satori_jp/$SLUG                  # B55 → logs/B55_mapping_latest.json
  Tập cũ chưa có `artifact_meta.json`: chạy 2 cổng QC TRƯỚC ... RỒI MỚI `--stamp` — cấm stamp mù (STT7: script 07:58 mới hơn prompt 07:35).
```

**SOP_SATORI_JP.md — mục B2:**
```
- **B2Q `SKIPPED` chỉ được đi tiếp khi `competitor.txt` bóc TRƯỚC P0 (2026-09-18, không có sidecar
  `competitor.segments.json`).** `fetch_script.py` từ 2026-09-18 LUÔN ghi sidecar — tập mới mà B2Q báo SKIPPED là lỗi
  pipeline (fetch không ghi sidecar), phải xem lại, KHÔNG coi là qua. Đo thật Kmxva85WKec: nguồn api, 694 đoạn, coverage 1.0, cpm 341.9 → PASS.
```

**SOP_CLONE_BRAIN.md — THẺ CHẠY bước 2:**
```
**Thứ tự thật trong `make_video_one` (P0, 2026-09-18 — 2 pha bộ não + 3 cổng mới, `brain_channel.py:419-670`):**
`competitor.txt → B2Q → pha SCRIPT (claude -p phase="script", chỉ khi thiếu script.txt) → cổng số → B3Q (≤3 vòng,
không hội tụ → ESCALATION_REPORT.md) → pha ASSETS (phase="assets", chỉ khi thiếu asset, ≤2 lượt, cấm sửa script) →
stamp fingerprint artifact_meta.json → STALE-check → REF-LOCK → B5P → B55 mapping → ⏸ dừng trước render → giao máy 2
(ảnh) → Hermes (ghép)`.
...
#### Production = dừng trước render
Sản xuất luôn gọi `make_video_one(..., stop_before_render=True)` (`chay_phan_chu.py` đã truyền tường minh). Nhánh
`render_engine.py` ở cuối hàm chỉ cho test / tập non-hybrid cũ; handoff thật = máy 2 vẽ ảnh → Hermes ghép (không đổi).
```

**QUY_TRINH_BUOC1 — mục 6 "Số đo thật 2026-09-18":**
```
- B55 mapping: 7 lời gọi, tok_in 20.077 / tok_out 4.883, 86s (bản gán tay: WARN 16/128, would_block 16); bản lỗi 2-3-2-3 `--mode fail`: FAIL 108/125, 6/6 ảnh mục tiêu bị bắt, 110s.
- B5P: 14 lời gọi (5 facts + 9 batch), tok_in ≈39-40k / tok_out ≈10.8k, 190-235s; hồi quy prompt cũ 5/5 (022/028/112/113/114) ở cả 3 run; bản sửa 4/5 sạch, 113 flag 1/3 run có lý do; 8 lỗi prompt thật mới phát hiện (002/027/074/081/082/111/118/125).
- Flow B smoke: 23,7 phút (B3Q tầng 2 12,1'; B5P 7,2'; mapping 3,4'; 21 lời gọi LLM), 0 ✗, không gọi `claude -p` viết.
- B2Q trên Kmxva85WKec: nguồn api, 694 đoạn, coverage 1.0, cpm 341.9, PASS.
- Chi phí thêm/tập ≈10,6 phút + 21 lời gọi gemini-3.8-flash.
```

**GIAO_VIEC_HYBRID_COMPOSITOR.md §3c:**
```
| Rào STALE + mapping invariant (mới 2026-09-18) | **Bước 1** | `hybrid_chuan_bi.py` (ngay TRƯỚC `sinh_neo.py`): `gate_common.kiem_stale` (... → exit 1) + `qc_img_doan --no-llm` (... → exit 1); SUSPICIOUS chỉ nhắc chạy có LLM, không chặn |
```

## 3. Kiểm sau khi sửa

- `cd pipeline && py -3.13 -m pytest tests -q` → `41 passed in 0.27s` (không đụng code).
- `grep -n "qc_transcript\|qc_prompt_consistency\|qc_img_doan\|--stamp" docs/SOP_SATORI_JP.md docs/SOP_CLONE_BRAIN.md docs/QUY_TRINH_BUOC1_SATORI_JP_TOAN_DIEN.md | wc -l` → **29** (≥ 8): SOP_SATORI_JP 9 · SOP_CLONE_BRAIN 8 · QUY_TRINH 12.
- Memory file: frontmatter hợp lệ (`name` / `description` / `metadata.type: project`; hệ thống memory đã tự bổ sung `originSessionId` + `modified` ISO khi lưu). `MEMORY.md` 99 → 100 dòng, đúng 1 dòng mới.
- Không file nào bị thêm BOM (kiểm byte đầu `SOP_SATORI_JP.md` = `# S`; plan file BOM=False sau khi ghi bằng UTF8Encoding(false)).

## 4. Lệch so với brief

1. Dòng MEMORY.md dùng **nguyên văn** brief (169 ký tự) dù brief ghi "≤150 ký tự" — giữ nguyên văn vì đó là chuỗi anh chỉ định, ưu tiên khớp text hơn khớp số.
2. Plan Step 4 Task 6 ("xoá `scratch_analysis/_regress_*`") **không tick** — chưa xoá (brief nói "giữ nếu anh muốn đối chiếu"), ghi chú ngay cạnh để anh quyết.
3. Mục 8 QUY_TRINH: ý "mapping QC" đánh dấu "ĐÃ LÀM, một phần" vì gợi ý gốc là "gợi ý ứng viên TRƯỚC khi gán" còn tool P0 chỉ kiểm SAU khi gán.

## 5. Concerns

- Bảng cổng ở 3 doc nay có 2-3 chỗ mô tả cùng điều kiện PASS/WARN/FAIL (SOP_SATORI_JP bảng đầu, SOP_CLONE_BRAIN bảng THẺ CHẠY + bảng §2, QUY_TRINH mục 3 + 4 + 6) — nếu sau này bật `--mode fail` phải sửa đồng bộ cả 3 file (đã ghi rõ "chưa bật" ở mọi chỗ để dễ grep `--mode fail`).
- `SOP_CLONE_BRAIN.md` bảng "Thời gian & chi phí thật một tập" (18-20 phút phần chữ) và "TRẠNG THÁI CHỨNG NHẬN" (4 cổng) là số cũ trước P0 — không sửa vì brief không yêu cầu; bảng THẺ CHẠY mới đã ghi 23,7' + ≈10,6' thêm/tập ngay phía trên nên người đọc thấy cả hai.
