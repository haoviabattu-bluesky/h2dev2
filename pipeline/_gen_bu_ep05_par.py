# -*- coding: utf-8 -*-
"""Gen bù 23 ảnh thiếu ep05-bermuda-triangle bằng gpti2 — ĐA LUỒNG 12 workers.
Resume an toàn: bỏ qua file đã tồn tại; gpti2_gen.generate() tự retry transient."""
import json, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"E:\CLAUDE\YOUTUBE\h2dev\assets\toshi-densetsu-jp\ep05-bermuda-triangle\img_ai")

import gpti2_gen  # noqa: E402  (cần cwd = pipeline)

plan = json.loads((BASE / "_gen_bu_plan.json").read_text(encoding="utf-8"))
# chỉ giữ file chưa có
todo = [it for it in plan if not (BASE / it["file"]).exists()]
print(f"Tổng 23 · đã có: {23 - len(todo)} · cần gen: {len(todo)}", flush=True)

def lam(it):
    fname, prompt = it["file"], it["prompt"]
    out = BASE / fname
    try:
        data = gpti2_gen.generate(prompt, orientation="landscape",
                                  quality=gpti2_gen.QUALITY_DEFAULT)
        out.write_bytes(data)
        return f"OK {fname} ({len(data)//1024}KB)"
    except Exception as e:
        return f"FAIL {fname}: {e}"

ok = fail = 0
t0 = time.time()
with ThreadPoolExecutor(max_workers=12) as ex:
    futs = {ex.submit(lam, it): it["file"] for it in todo}
    for i, fut in enumerate(as_completed(futs), 1):
        r = fut.result()
        print(f"[{i}/{len(todo)}] {r}", flush=True)
        if r.startswith("OK"):
            ok += 1
        else:
            fail += 1

print(f"\n=== XONG sau {time.time()-t0:.0f}s · OK {ok} · FAIL {fail} ===", flush=True)