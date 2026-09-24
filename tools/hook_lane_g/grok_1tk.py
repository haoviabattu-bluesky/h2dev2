# -*- coding: utf-8 -*-
"""Sinh clip hook bằng tài khoản Grok FREE trong GPM (tab GROK): 1 tài khoản = 1 clip (1 lượt/24h).

Mỗi lượt: gpm_grok_mo.py --pick → xoá cache mã chống bot cũ → grok_batch.py --only <clip còn thiếu> →
LUÔN gpm_grok_mo.py --close <PID> <ROW> (tắt profile ngay + ghi cột E), kể cả khi lỗi.
Danh sách clip cần = shots trong <hook>/hook_timeline.json.

    py -3.13 grok_1tk.py <thư mục hook> [số lượt tối đa]
"""
import json, os, re, subprocess, sys
from pathlib import Path

GV = Path(r"E:\CLAUDE\YOUTUBE\GROK_VIDEO")
HOOK = Path(sys.argv[1]); LAN = int(sys.argv[2]) if len(sys.argv) > 2 else 12
PY = ["py", "-3.13", "-X", "utf8"]
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def run(cmd, env=ENV, timeout=900):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=GV, timeout=timeout)
    return (r.stdout or "") + (r.stderr or "")


def thieu():
    ids = [f"clip_{s['n']:02d}" for s in json.loads((HOOK / "hook_timeline.json").read_text(encoding="utf-8"))["shots"]]
    return [i for i in ids if not ((HOOK / "clip" / f"{i}.mp4").exists() and (HOOK / "clip" / f"{i}.mp4").stat().st_size > 10240)]


for _ in range(LAN):
    t = thieu()
    if not t:
        print("✓ đủ clip"); break
    out = run(PY + [str(GV / "gpm_grok_mo.py"), "--pick"], timeout=300)
    m = re.search(r"PORT=(\d+) VIDEO_CON=(\d+) PID=(\S+) ROW=(\d+)", out)
    print(next((l for l in out.splitlines() if l.startswith("tai khoan")), out[-300:]), flush=True)
    if not m:
        print("✗ không mở được tài khoản:", out[-500:]); break
    port, con, pid, row = m.groups()
    try:
        if int(con) < 1:
            print(f"  dòng {row}: 0 lượt → bỏ"); continue
        (GV / "grok_headers.json").unlink(missing_ok=True)      # mã chống bot của tài khoản khác → không dùng lại
        o = run(PY + [str(GV / "grok_batch.py"), "--jobs", str(HOOK / "grok_jobs.csv"), "--out", str(HOOK / "clip"),
                      "--no-audio", "--gap", "5", "--retry", "0", "--only", t[0]], env=dict(ENV, GROK_CDP=f"http://127.0.0.1:{port}"))
        print("  " + "\n  ".join(l for l in o.splitlines() if re.search(r"OK |QUOTA|REJECT|FAIL|TỤT|XONG", l))[-800:], flush=True)
    finally:
        print("  " + run(PY + [str(GV / "gpm_grok_mo.py"), "--close", pid, row], timeout=120).strip().splitlines()[-1], flush=True)
print("còn thiếu:", thieu())
