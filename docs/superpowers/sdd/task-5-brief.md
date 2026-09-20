# TASK 5 BRIEF (trich tu plan 2026-09-18-p0-buoc1-gates.md)

## Global Constraints

- Dự án KHÔNG có git → mỗi task kết thúc bằng chạy pytest + 1 lệnh chạy thật trên tập STT3 (`E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-03-Kmxva85WKec`) thay cho commit. Trước khi sửa file có sẵn: copy `<file>` → `pipeline/_bak_<file>_<HHMM>` (theo lệ `_bak_stock_sources_1551.py` đã có).
- Chế độ cổng (anh chốt 2026-09-18): chỉ **PHÁN XÉT SEMANTIC** (B5P conflict, mapping mismatch) chạy **WARN-only** (`--mode warn` mặc định) trên 2 tập đầu để đo false-positive. **Invariant/lỗi cơ học chắc chắn FAIL ngay từ tập đầu:** số đoạn không tồn tại; mapping vi phạm ràng buộc bắt buộc (không giảm theo thứ tự); thiếu/trùng ID; **artifact STALE** (hash script khác hash nguồn đã ghi); output malformed; thiếu artifact bắt buộc.
- **Histogram chia đều (2,3,2,3…) KHÔNG phải FAIL cơ học** — chỉ đánh dấu `SUSPICIOUS` (WARN) và **bắt buộc chạy semantic QC** cho tập đó (không được `--no-llm` khi suspicious). FAIL của bản `img_doan` cũ STT3 trong hồi quy phải đến từ semantic mismatch (`--mode fail`) hoặc invariant thật, không phải vì "đều quá".
- **Fingerprint thay vì mtime:** khi sinh xong B5/B5.5, ghi `<slug>/artifact_meta.json` = `{"script_sha256": <sha>, "artifacts": {"img_prompts.txt": {"generated_from_script_sha256": <sha>, "sha256": <sha_file>}, "img_doan.txt": {...}}}`. Cổng `kiem_stale`: sha256(script.txt) hiện tại ≠ `generated_from_script_sha256` → **STALE = FAIL, chặn handoff**. mtime chỉ là fast-check phụ trợ (chưa có meta → dùng mtime + WARN "chưa có fingerprint").
- LLM: **không** làm ma trận 130×50. Facts: 1 lời gọi/10 đoạn; kiểm prompt: 1 lời gọi/15 prompt kèm facts của dải đoạn liên quan; mapping semantic: 1 lời gọi/8 đoạn kèm prompt đã map. ≈20 lời gọi/tập là **mục tiêu ban đầu, không phải trần cứng**. Mọi cổng ghi vào `metrics.llm` = `{"calls", "tokens_in", "tokens_out", "latency_s", "errors"}` (từ `gate_common.LLM_STATS`) để sau 2 tập có số thật rồi tối ưu.
- Mọi lời gọi LLM qua `gate_common.goi_llm_json` (task `"analysis"`, `temperature=0`, `tries_per_model=2`). Lỗi hạ tầng ném `QcError` → cổng báo `status="FAIL"` với `infra=True`, KHÔNG được coi là "0 lỗi" (bẫy 503 im lặng, memory `cong-b3q-phai-verify-bang-may`).
- Đường dẫn tuyệt đối: `E:\CLAUDE\YOUTUBE\h2dev\pipeline\` (gọi tắt `pipeline/`). Chạy test: `cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests -q`.
- Mọi script mới: đầu file `sys.stdout.reconfigure(encoding="utf-8")` trong try/except (Windows cp1252), đặt trong `pipeline/`, có docstring tiếng Việt không dấu hoặc có dấu nhất quán với file, CLI `--slug`, exit 1 khi FAIL, ghi JSON kết quả vào `<slug>/logs/`.
- Không sửa `render_engine.py`, `assemble.py`, `chay_buoc3.py`, `qc_visual.py`, `qc_script.py`.
- Định dạng kết quả cổng (dùng chung): `{"gate": str, "status": "PASS|WARN|FAIL|SKIPPED|ESCALATED", "attempt": int, "blocking_issues": [str], "warnings": [str], "metrics": {}, "infra": bool, "timestamp": ISO}`.

---


### Task 5: Tách phase trong `brain_steps` + đổi thứ tự trong `brain_channel` + rào trong `hybrid_chuan_bi`

**Files:**
- Modify: `pipeline/brain_steps.py:58` (`creative_prompt` thêm `phase`), `:346` (`run_creative` thêm `phase`) — backup trước
- Modify: `pipeline/brain_channel.py:448-605` (`make_video_one`) — backup trước
- Modify: `pipeline/hybrid_chuan_bi.py` (trước mục E `sinh_neo.py`)
- Create: `pipeline/tests/test_brain_phase.py`

**Interfaces:**
- `creative_prompt(slug_dir, profile_id, minutes, competitor_name="competitor.txt", phase="all") -> str` — `phase="script"`: chỉ mục 1) B3 + khối 70/30 + cổng số + B3Q (bỏ 2/2b/3/4, đổi câu kết "đủ 4 file" thành "xong script.txt đạt gate_check + qc_script"); `phase="assets"`: bỏ mục 1) và khối 70/30, thêm dòng đầu "`script.txt` ĐÃ ĐẠT mọi cổng — TUYỆT ĐỐI KHÔNG sửa script.txt lượt này; nếu thấy script cần sửa thì in BRAIN_BLOCKED <lý do>"; `phase="all"` = như cũ (giữ cho `brain_toshi.py` và CLI cũ).
- `run_creative(..., phase="all")` truyền xuống `creative_prompt`.
- `brain_channel.make_video_one`: thứ tự mới
  1. competitor.txt → **B2Q** (`qc_transcript.py`, FAIL → return False; SKIPPED/WARN → tiếp)
  2. thiếu `script.txt` → `run_creative(phase="script")`
  3. cổng số (`check_gate`/`fix_gate`) như cũ
  4. B3Q loop như cũ (VONG_SUA_B3Q) → khi thoát vòng mà chưa đạt: `gate_common.viet_escalation_report(d, "B3Q", attempts)` rồi return False
  5. thiếu bất kỳ file trong `need_assets = ["characters.json","img_prompts.txt","img_doan.txt","thumb_text.txt","TIEU_DE_MO_TA.txt"]` → `run_creative(phase="assets")` (+1 lượt gọi lại nếu bỏ dở, giữ logic cũ)
  6. **stamp fingerprint** `gate_common.ghi_fingerprint(d)` ngay khi pha asset xong (orchestrator tính hash, KHÔNG tin bộ não tự khai) → **rào STALE** `gate_common.kiem_stale(d)` → blocking → emit + return False (FAIL ngay; mtime chỉ là phụ trợ khi thiếu meta)
  7. REF-LOCK như cũ
  8. **B5P**: `_run(_pycmd("qc_prompt_consistency.py","--slug",d))` — mode warn; exit 1 (= cơ học/infra FAIL) → return False
  9. **mapping**: `_run(_pycmd("qc_img_doan.py","--slug",d))` — exit 1 → return False
  10. `stop_before_render` → return True (mặc định của orchestrator KHÔNG đổi; `render_engine` chỉ chạy khi gọi tường minh `stop_before_render=False` — giữ nguyên cho test/non-hybrid cũ)
- `hybrid_chuan_bi.py`: trước mục E, gọi `gate_common.kiem_stale(slug)` (blocking → in + `sys.exit(1)`; warning "chua co fingerprint" → in hướng dẫn `--stamp`, không chặn) và `qc_img_doan.main(["--slug", str(slug), "--no-llm"])` (≠0 = invariant/STALE → `sys.exit(1)`; nếu log báo SUSPICIOUS → in nhắc chạy `qc_img_doan.py` có LLM trước khi giao, không chặn ở mode warn).


**Ghi chú chốt từ code thật (phiên chính đọc trước khi giao, 2026-09-18):**
- `brain_channel._run(cmd, on_line) -> bool` đã stream log; dùng `_run(_pycmd("qc_transcript.py", "--slug", str(d)), on_line)` thay cho `subprocess.call` ở mọi chỗ gọi cổng mới (B2Q/B5P/mapping). `_pycmd` trả list lệnh sẵn.
- `brain_steps.creative_prompt`: `return "
".join([` ở dòng ~144 → đổi thành `parts = [`; dấu `])` đóng ở dòng ~343 → `]`, rồi thêm khối lọc `khoa_pha`/`pha_note` và `return "
".join(parts)`. `run_creative` gọi `creative_prompt(slug_dir, profile_id, minutes, competitor_name)` ở dòng ~359 → thêm `phase=phase`.
- Các phần tử `parts` là chuỗi f-string nhiều dòng; khoá theo **chữ đầu chuỗi** ("  1) B3:", "  2) B5:", "  2b) B5", "  3) B7:", "  4) TIÊU ĐỀ", "⚖️ 70/30", "LÀM ĐÚNG 4 BƯỚC", "   1. Liệt kê", "   2. Chốt", "   3. Với 7", "   💴", "      → PHẢI", "   🔎", "   ⚠️ NẾU QC", "   4. Mọi lời thoại", "Mục tiêu: ĐẠT B3Q") — in `repr(s[:20])` của từng phần tử để khớp đúng trước khi viết `khoa_pha`, không đoán. `thumb_bg_note` là biến riêng: pha "script" phải loại nó (so sánh `s is thumb_bg_note` hoặc `startswith("  4) THUMBNAIL")`).
- `hybrid_chuan_bi.py`: chèn rào ngay TRƯỚC dòng `# ---- E. anchors.txt` (~dòng 188); import `gate_common`, `qc_img_doan` cạnh các import đầu file.
- Hồi quy (mục 5 báo cáo anh yêu cầu): (a) **flow B smoke** trên bản copy STT3 (`scratch_analysis/_regress_stt3_flowB`, copy toàn bộ trừ `img/`, `stock/`, `voice*`, `logs/`) với `do_prepare=False, stop_before_render=True` — đủ file nên KHÔNG gọi `run_creative`; sẽ chạy thật B2Q(SKIPPED) → cổng số → B3Q (qc_script + qc_claude ≈10 phút, chấp nhận) → stamp/STALE → REF-LOCK → B5P → mapping → dừng; (b) **hybrid**: `hybrid_chuan_bi.py` trên STT3 THẬT vẫn ra `>> DU DIEU KIEN GIAO BUOC 3`; (c) **tập cũ non-hybrid** `simbot2-07-TISOm_7M_vM` (đã giao hàng, KHÔNG có `img_doan.txt`): chỉ chạy 3 cổng standalone trên bản copy để ghi nhận hành vi (B2Q SKIPPED · B5P chạy được không có img_doan · mapping FAIL "thieu required artifact") — KHÔNG chạy `make_video_one` trên tập này (sẽ gọi `claude -p` viết img_doan mới cho tập đã giao).
- Không đụng `render_engine.py`/`assemble.py`; `stop_before_render` mặc định giữ nguyên False trong chữ ký (callers hiện tại truyền tường minh) — nhưng docstring/`main()` phải ghi rõ: production = dừng trước render, `render_engine` chỉ cho test/non-hybrid cũ.

- [ ] **Step 1: Viết test thất bại (prompt theo phase, thuần chuỗi — không gọi claude)**

```python
# pipeline/tests/test_brain_phase.py
from pathlib import Path
import brain_steps as B


def _mk(tmp_path):
    (tmp_path / "competitor.txt").write_text("x" * 100, encoding="utf-8")
    return tmp_path


def test_phase_script_chi_co_b3(tmp_path):
    p = B.creative_prompt(_mk(tmp_path), "satori-jp-obaa", 30, phase="script")
    assert "1) B3" in p and "70/30" in p
    assert "img_doan.txt" not in p and "thumb_text.txt" not in p and "TIEU_DE_MO_TA" not in p
    assert "BRAIN_DONE" in p


def test_phase_assets_khong_sua_script(tmp_path):
    (tmp_path / "script.txt").write_text("s" * 200, encoding="utf-8")
    p = B.creative_prompt(_mk(tmp_path), "satori-jp-obaa", 30, phase="assets")
    assert "KHÔNG sửa script.txt" in p or "KHONG sua script.txt" in p
    assert "img_doan.txt" in p and "TIEU_DE_MO_TA" in p and "thumb_text.txt" in p
    assert "1) B3: viết `script.txt`" not in p


def test_phase_all_giu_nguyen(tmp_path):
    p = B.creative_prompt(_mk(tmp_path), "satori-jp-obaa", 30)
    assert "1) B3" in p and "img_doan.txt" in p and "TIEU_DE_MO_TA" in p
```

- [ ] **Step 2: Chạy test để thấy fail**

Run: `py -3.13 -m pytest tests/test_brain_phase.py -q`
Expected: `TypeError: creative_prompt() got an unexpected keyword argument 'phase'`

- [ ] **Step 3: Backup + sửa `brain_steps.py`**

Backup: `Copy-Item brain_steps.py ("_bak_brain_steps_" + (Get-Date -Format HHmm) + ".py")`.

(a) Chữ ký: `def creative_prompt(slug_dir, profile_id, minutes, competitor_name="competitor.txt", phase="all"):`

(b) Ngay trước `return "\n".join([` (dòng ~144), thêm:

```python
    # Tach 2 pha (P0 2026-09-18): pha "script" chi viet script.txt + qua cong so/B3Q; pha "assets"
    # viet characters/img_prompts/img_doan/thumb/TIEU_DE_MO_TA tren script DA CHOT. Truoc day viet
    # tat ca trong 1 luot roi vong B3Q sua script.txt SAU -> prompt/img_doan bam ban script cu
    # (bang chung STT3: img_prompts 18:36 < script 20:45, 3 anh mau thuan cot truyen).
    khoa_pha = {
        "script": ("  2) B5:", "  2b) B5", "  3) B7:", thumb_bg_note[:20] if thumb_bg_note else "\x00", "  4) TIÊU ĐỀ"),
        "assets": ("  1) B3:", "⚖️ 70/30", "LÀM ĐÚNG 4 BƯỚC", "   1. Liệt kê 10 nhịp", "   2. Chốt bằng chữ",
                   "   3. Với 7 nhịp", "   💴 CON SỐ TIỀN", "      → PHẢI DÙNG", "   🔎 TIỀN CHỈ", "   ⚠️ NẾU QC",
                   "   4. Mọi lời thoại", "Mục tiêu: ĐẠT B3Q"),
    }.get(phase, ())
    pha_note = {
        "script": "\n- PHA NÀY CHỈ LÀM `script.txt` (B3) tới khi ĐẠT gate_check.py + qc_script.py. KHÔNG viết "
                  "characters/img_prompts/img_doan/thumb/TIEU_DE_MO_TA — pha sau làm. Xong in BRAIN_DONE.",
        "assets": "\n- `script.txt` ĐÃ ĐẠT mọi cổng. TUYỆT ĐỐI KHÔNG sửa script.txt lượt này (sửa là lệch "
                  "prompt/img_doan với script — đúng lỗi STT3). Nếu thấy script BUỘC phải sửa: in "
                  "BRAIN_BLOCKED <lý do> và dừng. Chỉ viết các file asset còn thiếu.",
    }.get(phase, "")
```

(c) Đổi `return "\n".join([` thành `parts = [` ; sau list đóng `])` → `]` rồi thêm:

```python
    if khoa_pha:
        parts = [s for s in parts if not any(str(s).startswith(k) for k in khoa_pha)]
    if pha_note:
        parts.insert(parts.index("") if "" in parts else 0, pha_note)
    return "\n".join(parts)
```

(d) `run_creative(..., extra_prompt="", phase="all")` và chỗ gọi `creative_prompt(...)` bên trong thêm `phase=phase`.

- [ ] **Step 4: Chạy test phase**

Run: `py -3.13 -m pytest tests/test_brain_phase.py -q`
Expected: `3 passed`. Nếu test 1 fail vì chuỗi mục 2/3/4 vẫn lọt → in `khoa_pha` và các phần tử `parts` bắt đầu bằng "  2)"/"  3)"/"  4)" để khớp ĐÚNG chữ đầu dòng thật trong file (không đoán), sửa key.

- [ ] **Step 5: Backup + sửa `brain_channel.make_video_one`**

Backup: `Copy-Item brain_channel.py ("_bak_brain_channel_" + (Get-Date -Format HHmm) + ".py")`. Thêm `import gate_common` cạnh `import brain_steps` (dòng 426).

Thay khối từ `# 🧠 bộ não Claude viết phần sáng tạo` (dòng 448) đến hết `if not ok: emit(... "vẫn chưa xong") return False` (dòng 494) bằng:

```python
    # B2Q — transcript co du khong (P0). FAIL = transcript cut/lap -> viet tren nua cau chuyen.
    rc = subprocess.call(_pycmd("qc_transcript.py", "--slug", str(d)), cwd=str(HERE))
    if rc != 0:
        emit("✗ B2Q transcript RỚT (xem logs/B2Q_latest.json) → thử --method khác/proxy rồi chạy lại"); return False
    # PHA 1 — chi script.txt (P0 2026-09-18: tach khoi asset de B3Q sua script XONG roi moi viet prompt)
    if not (d / "script.txt").exists() or (d / "script.txt").stat().st_size < 50:
        _bang0 = _dem_bang_so_lieu()
        _kh = _khoa_profile(prof["id"])
        ok, last = brain_steps.run_creative(d, prof["id"], mn, on_line=on_line, phase="script",
                                            permission_mode=permission_mode, budget_usd=budget_usd)
        _bao_bang_so_lieu(_bang0, on_line)
        _kiem_profile(_kh, on_line)
        if not ok or not (d / "script.txt").exists():
            emit(f"✗ bộ não chưa ra script.txt ({last}) → dừng {d.name}"); return False
```

Giữ nguyên các khối HÀNG RÀO 2 (cổng số) và B3Q loop. Trong B3Q loop, ngay sau `emit("  ⏹ số lỗi chặn KHÔNG GIẢM ...")` và ở nhánh `if not dat_b3q and not force_lane:` (dòng ~567) thêm trước `return False`:

```python
        gate_common.viet_escalation_report(
            d, "B3Q", [{"attempt": i + 1, "status": "FAIL", "blocking_issues": loi_b3q} for i in range(luot)],
            goi_y="Sửa tay script.txt đúng các dòng trên rồi chạy lại; KHÔNG viết lại cả bài.")
        emit(f"  → đã ghi {d / 'ESCALATION_REPORT.md'}")
```
(`luot` là biến vòng for đã có; nếu vòng không chạy vì `dat_b3q` True thì nhánh này không vào.)

Ngay SAU khối B3Q (trước `# CỔNG REF-LOCK`), thêm PHA 2:

```python
    # PHA 2 — asset tren script DA CHOT
    need_assets = ["characters.json", "img_prompts.txt", "img_doan.txt", "thumb_text.txt", "TIEU_DE_MO_TA.txt"]
    thieu = [f for f in need_assets if not (d / f).exists()]
    for lan in (1, 2):
        if not thieu:
            break
        _kh = _khoa_profile(prof["id"])
        extra = "" if lan == 1 else (
            "⛔ LƯỢT TRƯỚC BẠN DỪNG LẠI BÁO CÁO THAY VÌ LÀM XONG. Chế độ không người giám sát — "
            f"làm nốt NGAY: {', '.join(thieu)}. Cấm dừng để xin ý kiến. Xong in BRAIN_DONE.")
        ok, last = brain_steps.run_creative(d, prof["id"], mn, on_line=on_line, phase="assets",
                                            permission_mode=permission_mode, budget_usd=budget_usd,
                                            extra_prompt=extra)
        _kiem_profile(_kh, on_line)
        thieu = [f for f in need_assets if not (d / f).exists()]
        if not ok and "BRAIN_BLOCKED" in str(last):
            emit(f"✗ bộ não báo script cần sửa ở pha asset ({last}) → quay về sửa script rồi chạy lại"); return False
    if thieu:
        emit(f"✗ vẫn thiếu {', '.join(thieu)} sau 2 lượt → dừng {d.name}"); return False
    # FINGERPRINT (anh chốt 2026-09-18): orchestrator tự tính hash script lúc asset vừa sinh xong —
    # không tin bộ não tự khai. Sau đó rào STALE (hash) chặn cứng; mtime chỉ phụ trợ khi thiếu meta.
    if not (d / gate_common.META_NAME).exists() or thieu_truoc_khi_chay:
        gate_common.ghi_fingerprint(d)
    b_stale, w_stale = gate_common.kiem_stale(d)
    for v in w_stale:
        emit(f"  ⚠ {v}")
    if b_stale and not force_lane:
        for v in b_stale:
            emit(f"✗ {v}")
        emit("  → asset bám bản script CŨ: viết lại img_prompts/img_doan theo script hiện tại rồi "
             f"`py -3.13 gate_common.py --slug {d} --stamp`")
        return False
```
(`thieu_truoc_khi_chay` = giá trị `thieu` đo TRƯỚC vòng `for lan` — lưu `thieu_truoc_khi_chay = bool(thieu)` ngay sau dòng `thieu = [...]` đầu tiên. Ý: chỉ stamp lại khi vừa sinh asset mới hoặc chưa có meta; tập đã stamp mà chỉ chạy lại kiểm thì giữ meta cũ để rào STALE có tác dụng.)

Ngay SAU khối REF-LOCK (trước `# CHỐT KIỂM TRA TRƯỚC KHI TIÊU TIỀN`), thêm:

```python
    # B5P + mapping QC (P0). Mode WARN: chi exit 1 khi loi CO HOC chac chan hoac LLM khong cham duoc.
    for tool, ten in (("qc_prompt_consistency.py", "B5P"), ("qc_img_doan.py", "B55 mapping")):
        rc = subprocess.call(_pycmd(tool, "--slug", str(d)), cwd=str(HERE))
        if rc != 0 and not force_lane:
            emit(f"✗ {ten} RỚT (xem {d / 'logs'}) → sửa rồi chạy lại"); return False
```

Xoá `need` cũ (dòng 449-458) nếu không còn dùng; `grep -n "need\b" brain_channel.py` để chắc không còn tham chiếu.

- [ ] **Step 6: Kiểm cú pháp + import**

Run: `py -3.13 -c "import ast;ast.parse(open('brain_channel.py',encoding='utf-8').read());ast.parse(open('brain_steps.py',encoding='utf-8').read());import brain_channel,brain_steps;print('OK')"`
Expected: `OK`

- [ ] **Step 7: Sửa `hybrid_chuan_bi.py` — rào trước mục E**

Thêm `import gate_common` + `import qc_img_doan` cạnh các import; ngay trước `# ---- E. anchors.txt` chèn:

```python
    # RAO INVARIANT (P0 2026-09-18): STALE (hash script khac luc sinh asset) -> FAIL; mapping vi pham
    # invariant -> FAIL. Chia deu chi la SUSPICIOUS (warn) — nhac chay semantic QC truoc khi giao.
    b_stale, w_stale = gate_common.kiem_stale(slug)
    for v in w_stale:
        print("[E] ⚠", v)
    if b_stale:
        for v in b_stale:
            print("[E] !!", v)
        sys.exit(1)
    if qc_img_doan.main(["--slug", str(slug), "--no-llm"]) != 0:
        print("[E] !! img_doan.txt rot invariant (xem logs/B55_mapping_latest.json) — sua roi chay lai"); sys.exit(1)
```

Run: `py -3.13 hybrid_chuan_bi.py --slug ..\assets\satori_jp\simbot2-03-Kmxva85WKec --profile satori-jp-obaa`
Expected: vẫn `>> DU DIEU KIEN GIAO BUOC 3`, có thêm dòng `=== B55_mapping: PASS`.

- [ ] **Step 8: Chạy toàn bộ test + smoke flow B không tốn tiền**

Run: `py -3.13 -m pytest tests -q` → Expected: `35 passed` (12+9+5+6+3).
Smoke (dry, không gọi claude): trong `py -3.13 -c`, import `brain_channel`, gọi `make_video_one` với `do_prepare=False` trên **bản copy** STT3 (`scratch_analysis/_regress_stt3_flowB` = copy toàn bộ thư mục trừ `img/`, `stock/`, `voice*`), `stop_before_render=True`, `force_lane=False`. Vì đủ file → phải đi qua B2Q(SKIPPED) → cổng số → B3Q (gọi qc_script + qc_claude thật ~10 phút, chấp nhận) → không gọi `run_creative` (đủ file) → rào mtime → REF-LOCK → B5P → mapping → `⏸ DỪNG TRƯỚC RENDER`. Expected: return True, không dòng `✗`. Nếu B3Q rớt trên STT3 (script đã đạt trước đó) → xem lỗi thật, không chỉnh test.

---

