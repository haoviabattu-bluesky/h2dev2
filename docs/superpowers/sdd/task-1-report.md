# Task 1 Report — gate_common.py

## Files created

- `pipeline/gate_common.py` — 242 lines
- `pipeline/tests/__init__.py` — 0 lines (empty, as specified)
- `pipeline/tests/test_gate_common.py` — 134 lines

No existing file was modified (task only creates new files; `llm_client.py` was read-only,
not touched).

## Step 2 — pytest before implementation existed

Command:
```
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests/test_gate_common.py -q
```
Output:
```
ModuleNotFoundError: No module named 'gate_common'
```
Matches expected.

## Step 4 — pytest after implementation

Command:
```
cd E:\CLAUDE\YOUTUBE\h2dev\pipeline && py -3.13 -m pytest tests/test_gate_common.py -q
```
First run (with brief's `phan_bo_xen_ke` code transcribed verbatim) FAILED:
```
.......F....                                                             [100%]
FAILED tests/test_gate_common.py::test_phan_bo_xen_ke - assert False is True
1 failed, 11 passed in 0.17s
```

After fixing the implementation (see Deviation below), final run:
```
............                                                             [100%]
12 passed in 0.12s
```

## Step 5 — real-data check on STT3

All commands run from `E:\CLAUDE\YOUTUBE\h2dev\pipeline`, `PYTHONIOENCODING=utf-8`.

Command 1 (first `--check`, before stamping):
```
py -3.13 gate_common.py --slug "../assets/satori_jp/simbot2-03-Kmxva85WKec" --check
```
Output:
```
  ⚠ chua co artifact_meta.json (fingerprint) — chay `py -3.13 gate_common.py --slug <tap> --stamp` sau khi xong B5/B5.5
=== STALE-CHECK: WARN
```
Matches expected exactly (1 warning line, WARN status).

Command 2 (`--stamp`):
```
py -3.13 gate_common.py --slug "../assets/satori_jp/simbot2-03-Kmxva85WKec" --stamp
```
Output:
```
✓ stamp ..\assets\satori_jp\simbot2-03-Kmxva85WKec\artifact_meta.json
```

Command 3 (`--check` again, after stamping):
```
py -3.13 gate_common.py --slug "../assets/satori_jp/simbot2-03-Kmxva85WKec" --check
```
Output:
```
=== STALE-CHECK: PASS
```
Matches expected.

Only `artifact_meta.json` was created inside the episode folder
(`E:\CLAUDE\YOUTUBE\h2dev\assets\satori_jp\simbot2-03-Kmxva85WKec\`); no other file in that
folder was read-modified or deleted. Content:
```json
{
 "artifacts": {
  "img_prompts.txt": {
   "generated_from_script_sha256": "e07ff6854f4d1e07ceb3d78c83d4439cb2df57e1fe4bd36d2c2ab185f687c132",
   "sha256": "b460fcf9e7dc6a6fe94811f695497795bef502170c028d68e255cda82f27af9f"
  },
  "img_doan.txt": {
   "generated_from_script_sha256": "e07ff6854f4d1e07ceb3d78c83d4439cb2df57e1fe4bd36d2c2ab185f687c132",
   "sha256": "c9781c7af9fbce215a5cfdbc57c618e37cd227077f52050d83960bc4b6f46091"
  }
 },
 "script_sha256": "e07ff6854f4d1e07ceb3d78c83d4439cb2df57e1fe4bd36d2c2ab185f687c132",
 "stamped_at": "2026-09-18T11:10:46"
}
```

Note on an operational pitfall hit while running this (not a code issue): invoking the CLI
from the Bash (git-bash/POSIX) tool with an **unquoted** Windows-style backslash path
(`--slug ..\assets\satori_jp\...`) silently mangles the path — bash strips the backslashes
in an unquoted argument, so the script sees a nonexistent directory, `kiem_stale` hits its
early `if not s.exists(): return [], []` guard, and the CLI prints a false `PASS` with zero
output lines. Using a quoted forward-slash path (`--slug "../assets/satori_jp/..."`) avoids
this. This is purely a shell-quoting issue in how the check was invoked, not a bug in
`gate_common.py` — flagging it because a silent false-PASS is exactly the kind of failure
mode this module exists to prevent, and it would be easy for a future caller (e.g.
`brain_channel.py`) to hit the same trap if it ever builds the `--slug` argument as an
unquoted backslash path in a POSIX shell context.

## Deviation from the brief (and why)

**`phan_bo_xen_ke`** — the Step 3 code transcribed verbatim from the brief contained a bug
relative to the brief's own Step-1 test. The original code was:

```python
vals = sorted(set(c))
if len(vals) == 1:
    return True
if len(vals) != 2 or vals[1] - vals[0] != 1:
    return False
xen = sum(1 for a, b in zip(c, c[1:]) if a != b)
return xen / (len(c) - 1) >= nguong
```

This rejects any list with more than 2 distinct values or where the two distinct values
aren't adjacent integers. But `test_phan_bo_xen_ke` asserts:
```python
assert G.phan_bo_xen_ke([3, 2] * 10 + [5, 3]) is True     # 20/22 cap xen ke
```
This list has **3** distinct values (`{2, 3, 5}`), so the `len(vals) != 2` guard forces an
early `return False`, contradicting the expected `True`. The comment on that test line
("20/22 cap xen ke") makes clear the intended rule is purely about the *fraction of
alternating adjacent pairs*, not the count of distinct values present.

Fix applied (implementation only, test left untouched): removed the
`len(vals) != 2 or vals[1] - vals[0] != 1` early-exit, keeping only the "all-equal ⇒ True"
special case and the alternating-fraction threshold check for everything else:

```python
vals = sorted(set(c))
if len(vals) == 1:
    return True
xen = sum(1 for a, b in zip(c, c[1:]) if a != b)
return xen / (len(c) - 1) >= nguong
```

Re-verified by hand against all 5 assertions in `test_phan_bo_xen_ke` (including the
`False`-expected case with values `{2,3,4,5}`, which now correctly returns `False` because
its alternating fraction is 17/21 ≈ 0.81 < 0.9) and by running pytest (12/12 pass). Also
updated the function's docstring to describe the corrected rule and documented the reason
for the change inline in the docstring itself, so a future reader of `gate_common.py` sees
why it differs from the brief's literal listing.

No other part of the Step 3 code was changed from the brief's verbatim listing.

## Self-review checklist

- [x] Every function/name under "Interfaces → Produces" exists with the exact name/signature:
      `STATUS`, `QcError`, `ket_qua`, `ghi_log`, `goi_llm_json`, `viet_escalation_report`,
      `LLM_STATS`, `llm_stats_snapshot`, `sha256_file`, `ghi_fingerprint`, `kiem_stale`,
      `kiem_mtime_script_vs_prompts`, `phan_bo_xen_ke`, plus the `--stamp`/`--check` CLI.
- [x] `ghi_log` never overwrites an attempt file — it globs existing `<gate>_attempt_*.json`,
      increments the count, and writes a new zero-padded file each call (verified by
      `test_ghi_log_khong_ghi_de`: two calls produce `_001` then `_002`).
- [x] `goi_llm_json` increments `LLM_STATS["errors"]` on both infra failure (`LLMError`/other
      exception from `llm_client.chat`) and non-JSON output (`_boc_json` raising `QcError`,
      caught and re-raised after incrementing) — verified by `test_llm_stats_cong_don`.
- [x] `kiem_stale` without an `artifact_meta.json` falls back to
      `kiem_mtime_script_vs_prompts` (verified by `test_stale_chua_co_meta_dung_mtime` and the
      real STT3 run, which had no meta file and correctly fell back to the mtime check,
      returning WARN since STT3's script.txt is older than its artifacts).
- [x] No extra features added beyond the brief (YAGNI) — implementation matches the Step 3
      listing verbatim except for the one documented bugfix in `phan_bo_xen_ke`.

## Concerns

- The `phan_bo_xen_ke` deviation above is the only substantive concern — it's a bug in the
  brief's own Step 3 code (contradicts its own Step 1 test), fixed per the task instructions
  ("fix the implementation, not the test... report any such deviation"). Downstream tasks
  that call `phan_bo_xen_ke` should be aware the "chỉ 1-2 giá trị khác nhau" phrasing in the
  original design intent is *not* enforced — a list with any number of distinct values will
  be flagged `True` (SUSPICIOUS/WARN) if ≥90% of adjacent pairs differ, per the test's own
  20/22-example.
- No other concerns; all 12 tests pass, the real-data STT3 check matches the brief's expected
  WARN → stamp → PASS sequence exactly, and no file other than the newly-created
  `artifact_meta.json` was touched in the STT3 episode folder.
