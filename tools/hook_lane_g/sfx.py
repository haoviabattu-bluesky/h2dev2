# -*- coding: utf-8 -*-
"""Sinh hiệu ứng âm thanh hook qua ai33 (duration AUTO — memory sfx-ai33-mac-dinh-auto).

    py -3.13 sfx.py <thư mục hook> <file.mp3>|<mô tả tiếng Anh>|<loop 0/1>[|<giây>] [...]
01/10/2026: NHẠC NỀN phải ghi <giây> (vd 22) — AUTO trả nhạc chỉ 1,54s (đo thật ep07 Lane L + ep02 Lane J), lặp nghe giật.
"""
import sys, time, requests
from pathlib import Path

KEY = "sk_vdplz671t7nq190rwxrwd52lj30z1giekav30rh0mkaqzleo"
BASE = "https://api.openspeaker.ai"
OUT = Path(sys.argv[1]) / "sfx"; OUT.mkdir(parents=True, exist_ok=True)
H = {"xi-api-key": KEY}
for arg in sys.argv[2:]:
    fn, txt, loop, *dur = arg.split("|")
    if (OUT / fn).exists():
        continue
    r = requests.post(f"{BASE}/v1/task/sound-effect", headers=H,
                      json={"text": txt, "prompt_influence": 0.3, "loop": loop == "1", **({"duration_seconds": float(dur[0])} if dur else {})}, timeout=60).json()
    tid = r.get("task_id"); assert tid, r
    for _ in range(60):
        time.sleep(3)
        t = requests.get(f"{BASE}/v1/task/{tid}", headers=H, timeout=30).json()
        d = t.get("data") if isinstance(t.get("data"), dict) else t
        if d.get("status") == "done":
            (OUT / fn).write_bytes(requests.get((d.get("metadata") or {}).get("audio_url"), timeout=60).content)
            print("✓", fn, "· credit còn", r.get("ec_remain_credits")); break
        if d.get("status") in ("failed", "error"):
            print("✗", fn, d); break
