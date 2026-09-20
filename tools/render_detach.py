#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_detach.py — khởi động make_video TÁCH RỜI khỏi session gọi.

Vì sao: cron/deleg session bị giới hạn ~25 phút và khi kết thúc Hermes kill toàn bộ
process con (kể cả terminal background) → make_video --from B8 (30-50 phút) bị SIGTERM
giữa chừng. Script này Popen make_video với DETACHED_PROCESS + CREATE_NEW_PROCESS_GROUP,
ghi log ra tools/render_<slug>_<ts>.log rồi THOÁT NGAY — process render sống độc lập.

Dùng: env -u PYTHONPATH py -3.13 -X utf8 tools/render_detach.py --slug ep02-walton --from B8Q
      (mọi cờ sau --from được truyền nguyên cho make_video)
Kết quả: worker theo dõi state.json (monitor) — khi B8Q/B9... cập nhật xong thì đọc báo cáo.
"""
import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

H2DEV = Path(r"E:\CLAUDE\YOUTUBE\h2dev")
TOOLS = H2DEV / "tools"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--from", dest="tu_buoc", default="B8")
    args, du = ap.parse_known_args()

    cmd = ["py", "-3.13", "-X", "utf8", "pipeline/make_video.py",
           "--profile", "toshi-densetsu-jp", "--slug", args.slug,
           "--from", args.tu_buoc] + du
    ts = datetime.now().strftime("%H%M%S")
    logf = TOOLS / f"render_{args.slug}_{ts}.log"
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    DETACHED_PROCESS = 0x00000008
    with open(logf, "w", encoding="utf-8") as out:
        p = subprocess.Popen(cmd, cwd=str(H2DEV), env=env,
                             stdout=out, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL,
                             creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
    print(f"RENDER_DETACHED pid={p.pid} log={logf}")
    # thoát ngay — process con sống độc lập


if __name__ == "__main__":
    main()
