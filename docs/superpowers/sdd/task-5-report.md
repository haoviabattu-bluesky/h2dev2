# TASK 5 REPORT — wire 3 cổng QC vào orchestrator + tách 2 pha bộ não (2026-09-18)

Trạng thái: **DONE_WITH_CONCERNS** (concern là hành vi mode WARN / thời gian chạy, không phải lỗi code).
Test: `py -3.13 -m pytest tests -q` → **41 passed** (38 cũ + 3 mới). Hồi quy (a)(b)(c) đều chạy thật, kết quả ở mục 5.

---

## 1. Thứ tự pipeline mới thực tế

`brain_channel.make_video_one` (`pipeline/brain_channel.py`, hàm bắt đầu dòng 419) — thứ tự đúng như code đã viết,
số dòng là của file hiện tại:

| # | Bước | Vị trí (dòng) | Ghi chú |
|---|---|---|---|
| 0 | prepare (B2 cào + giọng, nếu `do_prepare`) · kiểm `competitor.txt` · resume nếu có `final.mp4` · HÀNG RÀO 1 (`gate_declared`) · `ensure_char_rate` | 439–457 | **giữ nguyên** |
| 1 | **B2Q** `_run(_pycmd("qc_transcript.py","--slug",d))` — exit≠0 → `✗ … return False`; SKIPPED/WARN (exit 0) → tiếp | 458–463 | MỚI |
| 2 | **PHA script**: chỉ khi `script.txt` thiếu hoặc <50 byte → `run_creative(..., phase="script")` (+ đo sổ số liệu, khoá/khôi phục profile); không ra script → `return False` | 464–475 | MỚI (thay khối 1-lượt cũ) |
| 3 | HÀNG RÀO 2 cổng số: `check_gate` → `fix_gate.py` (máy) → `run_creative(phase="script")` (bộ não nắn 1 lượt) → còn lệch → `return False` | 476–515 | giữ nguyên, **thêm `phase="script"`** vào lượt nắn |
| 4 | **B3Q** `check_b3q` (qc_script tầng 0/1 + qc_claude tầng 2) → vòng `VONG_SUA_B3Q`=3 sửa tại chỗ (`run_creative(phase="script")`) với chốt không-hội-tụ → khi thoát mà chưa đạt: `gate_common.viet_escalation_report(d,"B3Q",lich_su_b3q)` → `return False` | 516–570 | giữ nguyên + **lịch sử từng lượt + escalation** |
| 5 | **PHA assets**: `need_assets=[characters.json, img_prompts.txt, img_doan.txt, thumb_text.txt, TIEU_DE_MO_TA.txt]`; thiếu → `run_creative(phase="assets")` tối đa 2 lượt (lượt 2 có extra_prompt "làm nốt"); `BRAIN_BLOCKED` → `return False`; vẫn thiếu sau 2 lượt → `return False` | 572–598 | MỚI |
| 6 | **Fingerprint**: `ghi_fingerprint(d)` CHỈ khi (chưa có `artifact_meta.json`) hoặc (vừa sinh asset ở bước 5, `thieu_truoc_khi_chay`) → **`kiem_stale(d)`**: warning → in `⚠`; blocking (hash script ≠ hash lúc sinh, hoặc mtime fallback khi thiếu meta) → `✗ … return False` (bỏ qua nếu `force_lane`) | 600–619 | MỚI |
| 7 | REF-LOCK `check_reflock` → sửa 1 lượt `run_creative(phase="assets")` → còn hỏng → `return False` | 621–646 | giữ nguyên, **thêm `phase="assets"`** |
| 8 | **B5P** `_run(_pycmd("qc_prompt_consistency.py","--slug",d))` (mode warn mặc định) → exit≠0 → `✗ … return False` | 648–654 | MỚI |
| 9 | **B55 mapping** `_run(_pycmd("qc_img_doan.py","--slug",d))` (mode warn mặc định) → exit≠0 → `✗ … return False` | 648–654 (cùng vòng for) | MỚI |
| 10 | `stop_before_render` → `⏸ DỪNG TRƯỚC RENDER … return True` | 656–663 | giữ nguyên |
| 11 | `render_engine.py` (chỉ khi `stop_before_render=False` — test/non-hybrid cũ) | 664–670 | **giữ nguyên nguyên văn** |

`brain_steps.py`:
- `creative_prompt(slug_dir, profile_id, minutes, competitor_name="competitor.txt", phase="all")` (dòng 58): dựng `parts`
  như cũ → lọc theo `khoa_pha[phase]` (prefix chuỗi) → chèn `pha_note` sau dòng đầu tiên (`parts.index("")`) → join
  (dòng 147–167 khối `khoa_pha`/`pha_note`, dòng 364–369 khối lọc + return).
- `NEED_BY_PHASE` (dòng 372–376): `script` → `["script.txt"]`; `assets` → 5 file asset (kể cả `img_doan.txt`);
  `all` → 5 file như cũ (không có img_doan — giữ y hệt hành vi cũ).
- `run_creative(..., extra_prompt="", phase="all")` (dòng 379): truyền `phase` xuống `creative_prompt`; kiểm tầng hai
  dùng `NEED_BY_PHASE[phase]` (dòng 437–441).

## 2. Gate nào tự chạy ở đâu

| Cổng | Gọi ở đâu | Cách gọi / mode | Ghi gì |
|---|---|---|---|
| **B2Q** transcript | `make_video_one` bước 1 (`brain_channel.py:461`) | subprocess `qc_transcript.py --slug <d>` (không có mode; SKIPPED khi không có sidecar) | `<slug>/logs/B2Q_attempt_NNN.json` + `B2Q_latest.json` |
| **Cổng số** | bước 3 (`check_gate`, `fix_gate.py`) | in-process `ai_steps.check` | không ghi file (như cũ) |
| **B3Q** nội dung | bước 4 (`check_b3q`) | subprocess `qc_script.py` (tầng 0/1) + in-process `qc_claude.cham` (tầng 2, gọi `claude -p` phiên mới làm giám khảo, **không phải run_creative**) | `_qc_claude.json` (như cũ); **không hội tụ → `<slug>/ESCALATION_REPORT.md`** (mới) |
| **Fingerprint / STALE** | bước 6 (`brain_channel.py:605–619`) | in-process `gate_common.ghi_fingerprint` (điều kiện) + `gate_common.kiem_stale` | `<slug>/artifact_meta.json` (chỉ khi stamp) |
| **REF-LOCK** | bước 7 | in-process `check_reflock` | không ghi file (như cũ) |
| **B5P** prompt↔script | bước 8 (`brain_channel.py:651–654`) | subprocess `qc_prompt_consistency.py --slug <d>` → mode **warn** (mặc định của tool), có LLM | `logs/B5P_attempt_NNN.json` + `B5P_latest.json` (metrics.llm) |
| **B55 mapping** img_doan | bước 9 (`brain_channel.py:651–654`) | subprocess `qc_img_doan.py --slug <d>` → mode **warn**, có LLM (semantic chạy khi không có blocking cơ học) | `logs/B55_mapping_attempt_NNN.json` + `B55_mapping_latest.json` |
| **STALE + mapping (hybrid)** | `hybrid_chuan_bi.py` ngay TRƯỚC mục E `sinh_neo.py` (dòng 191–211) | in-process `gate_common.kiem_stale(slug)` + `qc_img_doan.main(["--slug",slug,"--no-llm"])` | `logs/B55_mapping_attempt_NNN.json` trong tập thật; đọc lại `B55_mapping_latest.json` để nhắc SUSPICIOUS |

Mọi cổng con đều gọi qua `_run(_pycmd(...), on_line)` (stream log thẳng ra `on_line`, không dùng `subprocess.call` như
khối code mẫu trong brief — theo "Ghi chú chốt từ code thật").

## 3. Điều kiện nào chặn cứng

`make_video_one` trả **False** khi (theo thứ tự gặp):
1. thiếu `competitor.txt` (cũ) · hồ sơ chưa khai `script.gate` và không `force_lane` (cũ).
2. **B2Q exit≠0** = `qc_transcript.py` FAIL (transcript cụt/lặp). SKIPPED/WARN không chặn.
3. Pha script: `run_creative` không ok hoặc không tạo `script.txt`.
4. Cổng số còn lệch sau máy nắn + bộ não nắn (không `force_lane`) (cũ).
5. **B3Q** không đạt sau vòng sửa (không `force_lane`) — nay kèm ghi `ESCALATION_REPORT.md`.
6. Pha assets: bộ não in `BRAIN_BLOCKED` (script cần sửa) · hoặc vẫn thiếu file asset sau 2 lượt.
7. **STALE blocking** (không `force_lane`): `artifact_meta.json` có và `generated_from_script_sha256` ≠ sha256(script.txt) hiện tại;
   HOẶC chưa có meta và mtime(script.txt) − mtime(img_prompts/img_doan) > 2s (fallback mtime của `kiem_stale`).
   Warning (chưa có fingerprint / artifact sửa tay sau stamp) chỉ in `⚠`.
8. REF-LOCK còn hỏng sau 1 lượt sửa (cũ).
9. **B5P exit 1** (không `force_lane`): ở mode warn chỉ xảy ra khi lỗi cơ học chắc chắn (thiếu artifact bắt buộc, STALE/mtime
   trong chính tool, output malformed) hoặc **LLM không chấm được (`infra=True`)**. Semantic conflict → WARN, không chặn.
10. **B55 mapping exit 1** (không `force_lane`): thiếu `img_doan.txt` · dòng malformed · số đoạn không tồn tại · không giảm theo thứ
    tự · thiếu/trùng ID · STALE · LLM infra. SUSPICIOUS (chia đều) chỉ WARN.
11. Render không ra `final.mp4` (chỉ khi `stop_before_render=False`, cũ).

`hybrid_chuan_bi.py` **exit 1** thêm 2 chỗ (ngoài các exit 1 cũ A–D): STALE blocking (`[E] !! …`) · `qc_img_doan --no-llm` trả ≠0
(`[E] !! img_doan.txt rot invariant …`). SUSPICIOUS chỉ in nhắc chạy có LLM, không chặn.

`run_creative` trả `(False, "thiếu file: …")` khi thiếu file của **đúng pha** (`NEED_BY_PHASE`) — pha script không còn đòi asset.

## 4. Flow hybrid có bị ảnh hưởng không

**Có, đúng 1 chỗ và chỉ thêm rào, không đổi luồng A–E:** `pipeline/hybrid_chuan_bi.py` +25 dòng / −0:
- import (dòng 45–47): `sys.path.insert(0, HERE)`, `import gate_common`, `import qc_img_doan`.
- ngay TRƯỚC `# ---- E. anchors.txt` (dòng 191–211): `kiem_stale(slug)` → warning in `[E] ⚠` (+ gợi ý lệnh `--stamp` khi chưa có
  fingerprint) · blocking in `[E] !!` + `sys.exit(1)`; `qc_img_doan.main(["--slug",slug,"--no-llm"])` ≠0 → `sys.exit(1)`; đọc
  `logs/B55_mapping_latest.json` → `metrics.suspicious` → in nhắc chạy có LLM (không chặn).
- `render_engine.py`, `assemble.py`, `chay_buoc3.py`, `sinh_neo.py` **không đụng**.

Hồi quy (b) trên tập THẬT `assets/satori_jp/simbot2-03-Kmxva85WKec` (exit 0, 0,9 s — mọi bước A–D đã xong từ trước, qc_audio chạy lại nhanh):
```
=== QC NGHE: ĐẠT
  seconds          1952.4 … pause_misplaced 0 · dropouts 0 · srt_drift 0.17
[A] Khong co dong nao can doi nhom (da xong tu truoc, hoac tap khong co stock bi loai).
[B] Copy 0 anh moi tu E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\simbot2-03-Kmxva85WKec vao img/.
=== img/: co 120, can 120 (AI+AI_FALLBACK) — 8 dong STOCK that KHONG can nam o day ===
[D] voice_paced.wav/srt da co san, bo qua B4.
=== B55_mapping: PASS · 128 anh / 50 doan · semantic checked=0 warn=0 would_block=0 · llm calls=0 tok_in=0 tok_out=0 latency=0s err=0
[E] anchors.txt da co san, bo qua.
=== DU DIEU KIEN GIAO BUOC 3 (compositor hybrid, xem GIAO_VIEC_HYBRID_COMPOSITOR.md muc 1) ===
  img/*.png : 120 · voice_paced.wav OK · voice_paced.srt OK · anchors.txt OK
```
Không có dòng `[E] ⚠` (tập đã có `artifact_meta.json` stamp 11:10, hash khớp) và không SUSPICIOUS. Ghi thêm
`logs/B55_mapping_attempt_002.json` vào tập thật (đúng thiết kế ghi-không-đè).

## 5. Regression trên các tập cũ

### (a) Flow-B smoke — bản copy STT3 · `RETURN = True` · **23,7 phút** · 0 dòng `✗` · **không gọi run_creative**

Cách trỏ vào bản copy: `video_dir(prof, handle, idx, vid)` = `OUT_ROOT / prof["slug_dir"] / f"{handle}-{idx:02d}-{vid}"`
(`brain_channel.py:82–84`). Với `handle="simbot2", idx=3` nó trỏ thẳng vào tập THẬT, nên tôi copy tập vào
`scratch_analysis/_regress_stt3_flowB/simbot2-03-Kmxva85WKec/` (mọi thứ trừ `img/`, `stock/`, `voice*`, `logs/`) và **chỉ đổi
`prof["slug_dir"] = "scratch_analysis/_regress_stt3_flowB"` trên dict trong bộ nhớ** (không ghi file profile) — `video_dir` thật
được dùng nguyên, resolve ra đúng thư mục copy (assert `exists()` trước khi chạy). Driver: scratchpad `regress_a.py`; log đầy đủ
`scratch_analysis/_regress_stt3_flowB/_flowB_run.log` (70 dòng). Các dòng chốt, đúng thứ tự:
```
[    0.0s] [B2Q] kiểm transcript …
[    0.1s]     === B2Q: SKIPPED (khong co sidecar)
[   60.5s]     === QC NỘI DUNG: DAT ===
[   60.5s]     — bám gốc 70/30 (ramclouds:gemini-3.8-flash): giữ 75% nhịp · DAT
[   60.5s]     [tầng 2] giám khảo Claude (phiên mới) …
[  789.0s]     [tầng 2] 0 lỗi CHẶN · 12 góp ý (không chặn) · 12.1 phút
[  789.0s]   ✓ STALE-check: asset khớp hash script hiện tại
[  789.0s] [B5P] qc_prompt_consistency.py …
[ 1219.6s]     === B5P: WARN · 128 prompt / 50 doan · checked=128 warn=28 would_block=12 ambiguous=16 · llm calls=14 tok_in=41018 tok_out=10867 latency=431s err=0
[ 1219.7s] [B55 mapping] qc_img_doan.py …
[ 1423.8s]     === B55_mapping: WARN · 128 anh / 50 doan · semantic checked=128 warn=18 would_block=18 · llm calls=7 tok_in=20077 tok_out=4844 latency=204s err=0
[ 1423.8s] ⏸ DỪNG TRƯỚC RENDER theo yêu cầu — phần chữ đã xong & qua cổng: …\_regress_stt3_flowB\simbot2-03-Kmxva85WKec
[ 1423.8s] RETURN = True · total 23.7 min
```
Thời gian từng khúc: B2Q 0,1 s · cổng số + qc_script tầng 1 ≈ 60 s · qc_claude tầng 2 12,1 phút · STALE 0 s · B5P 7,2 phút
(14 lời gọi LLM, latency 431 s) · B55 mapping 3,4 phút (7 lời gọi, 204 s).

`claude -p` có được gọi không: **run_creative KHÔNG được gọi** (0 dòng `🧠 Claude (bộ não) bắt đầu viết`, không có `⟳`/pha nào).
Có ĐÚNG 1 tiến trình `claude -p --permission-mode bypassPermissions --model opus` (PID 32920, 14:18:52) — đó là **giám khảo
`qc_claude.py:100`** trong B3Q tầng 2 (không có `--append-system-prompt`/`--add-dir`/`stream-json` của run_creative), đọc-chỉ, ghi
`_qc_claude.json`. Đây là hành vi cũ của `check_b3q`, không phải bộ não viết.

Kiểm sau chạy: `script.txt`/`img_prompts.txt`/`img_doan.txt`/`characters.json`/`artifact_meta.json` trong copy **không đổi mtime**
(meta có sẵn + không sinh asset → không re-stamp, đúng thiết kế); sha256(script copy) == sha256(script thật); không có
`ESCALATION_REPORT.md`; `logs/` có `B2Q_/B5P_/B55_mapping_attempt_001.json` + `_latest.json`.

B3Q **không rớt** trên script đã đạt trước đó (không phát sinh concern về gate).

### (b) hybrid — xem mục 4: vẫn `>> DU DIEU KIEN GIAO BUOC 3`, có `=== B55_mapping: PASS`, exit 0.

### (c) Tập cũ non-hybrid STT7 `simbot2-07-TISOm_7M_vM` (đã giao, không có `img_doan.txt`) — copy sang
`scratch_analysis/_regress_stt7_gates/` (trừ `img/`, `stock/`, `voice*`, `logs/`, và `final*.mp4` 1,1 GB không liên quan 3 cổng),
**chỉ chạy 3 cổng standalone, KHÔNG chạy make_video_one**:
```
### py -3.13 qc_transcript.py --slug …\_regress_stt7_gates
=== B2Q: SKIPPED (khong co sidecar)                                   exit=0 · 0,1s

### py -3.13 qc_prompt_consistency.py --slug …\_regress_stt7_gates --no-llm
=== B5P: FAIL · 128 prompt / 56 doan · checked=0 warn=0 would_block=0 ambiguous=0 · llm calls=0 …
  ✗ script.txt (09-12 07:58) MOI HON img_prompts.txt (09-12 07:35) — img_prompts.txt dang bam ban script cu, phai ra soat/viet lai img_prompts.txt sau khi sua script
                                                                       exit=1 · 0,1s

### py -3.13 qc_img_doan.py --slug …\_regress_stt7_gates --no-llm
=== B55_mapping: FAIL · thieu img_doan.txt                             exit=1 · 0,1s
```
Ghi nhận: B2Q SKIPPED (đúng brief) · **B5P chạy được không cần img_doan nhưng FAIL vì fallback mtime** (tập cũ không có
`artifact_meta.json`, script sửa 23 phút SAU img_prompts — đúng loại lệch mà P0 nhắm tới; khác dự đoán "chạy được" trong brief
ở chỗ nó rớt cơ học chứ không PASS) · mapping FAIL "thieu required artifact img_doan.txt" (đúng brief). Tập này đã giao hàng,
không sửa gì — chỉ ghi nhận hành vi.

## 6. Có thay đổi nào ngoài Bước 1 hay không

**KHÔNG.** Bằng chứng:
- File sửa: `pipeline/brain_steps.py` (+43/−9, 438→469 dòng) · `pipeline/brain_channel.py` (+108/−47, 618→675) ·
  `pipeline/hybrid_chuan_bi.py` (+25/−0, 173→197). File mới: `pipeline/tests/test_brain_phase.py` (21 dòng).
- Backup trước khi sửa: `pipeline/_bak_brain_steps_1412.py` · `pipeline/_bak_brain_channel_1412.py` ·
  `pipeline/_bak_hybrid_chuan_bi_1412.py`.
- **Không đụng**: `render_engine.py`, `assemble.py`, `chay_buoc3.py`, `qc_visual.py`, `qc_script.py`, `gate_common.py`,
  `qc_transcript.py`, `qc_prompt_consistency.py`, `qc_img_doan.py`, `sinh_neo.py`, `brain_toshi*.py`, profile JSON.
- Nhánh `render_engine.py` cuối `make_video_one` giữ nguyên nguyên văn; `stop_before_render` mặc định vẫn False (chỉ thêm docstring
  + comment ở `main()` nói rõ sản xuất = dừng trước render). Caller sản xuất `chay_phan_chu.py:64` đã truyền
  `stop_before_render=True` tường minh → không đổi hành vi.
- Không chạy render/ghép/TTS/gen ảnh nào trong task này: (a) dừng ở `⏸ DỪNG TRƯỚC RENDER`; (b) mọi bước B4 đã có sẵn nên
  `hybrid_chuan_bi` chỉ chạy qc_audio (đọc) + cổng mới; (c) chỉ 3 cổng đọc.
- `phase="all"` cho prompt y hệt bản cũ (test 3 + kiểm tay: 112 dòng, đủ mục 1/2/2b/3/4/4) → `brain_steps` CLI (`main`,
  dòng 486) và mọi caller cũ không đổi. `brain_toshi.py` dùng `brain_toshi_steps` riêng, không liên quan.

---

## Files changed + backups
| File | Dòng (cũ→mới) | Diff | Backup |
|---|---|---|---|
| `pipeline/brain_steps.py` | 438→469 | +43/−9 | `pipeline/_bak_brain_steps_1412.py` |
| `pipeline/brain_channel.py` | 618→675 | +108/−47 | `pipeline/_bak_brain_channel_1412.py` |
| `pipeline/hybrid_chuan_bi.py` | 173→197 | +25/−0 | `pipeline/_bak_hybrid_chuan_bi_1412.py` |
| `pipeline/tests/test_brain_phase.py` | mới, 21 | — | — |

## Pytest (nguyên văn)
```
> cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests -q
.........................................                                [100%]
41 passed in 0.25s
```
(Bước 2 brief: trước khi sửa `py -3.13 -m pytest tests/test_brain_phase.py -q` → `2 failed, 1 passed` với
`TypeError: creative_prompt() got an unexpected keyword argument 'phase'` — test 3 (`phase="all"`) đã pass sẵn vì không truyền phase.)
Brief Step 8 ghi "35 passed (12+9+5+6+3)" — con số đó lỗi thời; suite thật trước task là 38, sau là 41.

## Deviations so với brief (đều cần thiết, đã kiểm)
1. **`pha_note["script"]` của brief chứa chữ `TIEU_DE_MO_TA`**, trong khi test 1 của chính brief assert `"TIEU_DE_MO_TA" not in p`
   → đổi đúng 1 token thành "tiêu đề+mô tả đăng tải" (nghĩa giữ nguyên). Không đổi test.
2. **`run_creative` kiểm tầng hai theo pha** (`NEED_BY_PHASE`): brief không nói, nhưng nếu giữ `need` 5 file cũ thì pha "script"
   LUÔN trả `(False, "thiếu file: characters.json, …")` dù đã viết xong script → orchestrator dừng ngay ở pha 1 trên mọi tập mới.
   `all` giữ đúng 5 file cũ (không có img_doan) để không đổi hành vi caller cũ.
3. **Lượt nắn cổng số và vòng sửa B3Q truyền `phase="script"`, lượt sửa REF-LOCK truyền `phase="assets"`** — cùng lý do (2):
   ở thứ tự mới, khi nắn/sửa script thì asset chưa tồn tại. Extra_prompt lượt nắn cổng số đổi câu "characters.json, img_prompts.txt,
   thumb_text.txt ĐÃ ĐẠT" → "các file khác nếu đã có … không viết thêm asset" cho khớp thực tế.
4. **Escalation report ghi lịch sử TỪNG lượt** (`lich_su_b3q`: lượt 1 = kết quả check đầu, lượt k+1 = sau mỗi lần sửa, kể cả lượt bộ não
   bỏ dở) thay vì lặp cùng một `loi_b3q` cho mọi lượt như snippet brief. Bọc try/except để lỗi ghi file không che mất `return False`.
5. Gọi cổng qua `_run(_pycmd(...), on_line)` (stream log) thay `subprocess.call` — theo "Ghi chú chốt từ code thật".
6. Thư mục copy (a) là `scratch_analysis/_regress_stt3_flowB/simbot2-03-Kmxva85WKec/` (thêm 1 cấp) để `video_dir` thật resolve
   được bằng cách chỉ đổi `slug_dir` trong bộ nhớ — mục 5(a) đã nêu.
7. Không thêm `--stop-before-render` vào CLI (brief chỉ yêu cầu docstring/main "ghi rõ") — thêm docstring ở `make_video_one` và
   comment ngay trước lời gọi trong `main()`.
8. (c): loại thêm `final*.mp4` (1,1 GB) khỏi bản copy STT7 — không liên quan 3 cổng.

## Concerns
1. **Mode WARN đang cho qua khá nhiều semantic conflict thật trên STT3**: B5P `would_block=12` (vd 022.png sa mạc Ả Rập vs công
   trường Kawaguchi; 081/082.png "3 sổ tiết kiệm" vs "thư gấp tư dưới bát miso"), B55 `would_block=18/128`. Đúng chủ trương
   "đo false-positive 2 tập đầu", nhưng nghĩa là tập STT3 hiện tại vẫn qua orchestrator với ~12 prompt lệch cốt truyện. Cần người đọc
   `logs/B5P_latest.json` + `B55_mapping_latest.json` của tập thật rồi quyết định khi nào bật `--mode fail` (orchestrator hiện gọi
   không truyền `--mode`, muốn đổi chỉ cần thêm arg ở `brain_channel.py:652`).
2. **Thời gian bước 1 tăng ≈ 10,6 phút/tập** cho 2 cổng LLM mới (B5P 7,2' + mapping 3,4') trên nền B3Q 13'. Chấp nhận được theo
   brief nhưng đáng đo lại sau 2 tập (LLM_STATS đã ghi vào metrics.llm).
3. **qc_claude tầng 2 chạy 12,1 phút** (brief ước "≈10 phút" cho cả B3Q) — không phải do task này, ghi nhận để không nhầm là treo.
4. Tập cũ non-hybrid (STT7) **rớt B5P vì mtime fallback** khi không có fingerprint — nếu sau này ai chạy `make_video_one` lại trên tập
   cũ đã giao (không nên), nó sẽ dừng ở STALE (bước 6) trước cả B5P; đây là hành vi mong muốn nhưng cần biết để không hiểu nhầm là lỗi.
5. Trong (b), `hybrid_chuan_bi` không in dòng `[E] ⚠` nào vì STT3 đã có meta — nhánh "chưa có fingerprint → in gợi ý --stamp" chưa được
   hồi quy trên tập thật (đã kiểm logic bằng đọc `kiem_stale`: message chứa "chua co … fingerprint").
