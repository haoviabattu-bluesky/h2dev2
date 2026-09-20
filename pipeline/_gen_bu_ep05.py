# -*- coding: utf-8 -*-
"""Gen bù 23 ảnh thiếu ep05-bermuda-triangle bằng gpti2 (low, 2560x1440)."""
import json, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep05-bermuda-triangle\img_ai")

import gpti2_gen  # noqa: E402  (cần cwd = pipeline)

plan = json.loads((BASE / "_gen_bu_plan.json").read_text(encoding="utf-8"))

ok, fail = [], []
for i, item in enumerate(plan, 1):
    fname, prompt = item["file"], item["prompt"]
    out = BASE / fname
    if out.exists():
        ok.append(f"{fname} (có sẵn)")
        continue
    try:
        data = gpti2_gen.generate(prompt, orientation="landscape",
                                  quality=gpti2_gen.QUALITY_DEFAULT)
        out.write_bytes(data)
        ok.append(f"{fname} ({len(data)//1024}KB)")
        print(f"[{i}/{len(plan)}] OK {fname}", flush=True)
    except Exception as e:
        fail.append(f"{fname}: {e}")
        print(f"[{i}/{len(plan)}] FAIL {fname}: {e}", flush=True)
    time.sleep(1)

print("\n=== KẾT QUẢ ===")
print("OK:", len(ok))
print("FAIL:", len(fail))
for f in fail:
    print("  ", f)