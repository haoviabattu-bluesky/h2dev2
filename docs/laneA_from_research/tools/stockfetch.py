# -*- coding: utf-8 -*-
"""Kho tư liệu hình cho Lane A — chỉ lấy nguồn AN TOÀN BẢN QUYỀN, ghi sổ từng file.

Kênh mẫu 今夜も都市伝説 dựng hình bằng clip stock cắt nhanh (12–16 lần/phút), không phải
ảnh AI. File này lấy tư liệu tương đương từ nguồn công cộng, và **ghi lại giấy phép của
TỪNG file** vào `manifest.jsonl` để sau này có bị khiếu nại còn truy ngược được.

⚠️ CẠM BẪY ĐÃ GẶP THẬT: tìm "apollo" trên Internet Archive trả về cả bản ghi truyền hình
CÓ BẢN QUYỀN (CSPAN2, FOXNEWS...). Dùng nhầm là vi phạm. Vì vậy nhánh Internet Archive
ở đây BẮT BUỘC lọc `licenseurl` chứa publicdomain/creativecommons — không có giấy phép
rõ ràng thì bỏ, không đoán.

  py -3.13 -X utf8 src/stockfetch.py --q "moon far side" --n 12 --out assets/stock
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path

import requests

from stock_sources import UA, TIMEOUT, archive, commons, nasa, pexels

UA = {"User-Agent": "Mozilla/5.0 (compatible; stock-research/1.0)"}
TIMEOUT = 45

# Trần dung lượng mỗi file. Tư liệu dựng nền chỉ cần 1080p vài chục MB; bản ~orig của
# NASA có thể tới hàng GB và hoàn toàn vô dụng cho việc này.
MAX_BYTES = 250 * 1024 * 1024
MIN_BPS = 200 * 1024        # dưới 200 KB/s kéo dài ⇒ bỏ file
STALL_AFTER_S = 20          # chỉ bắt đầu xét tốc độ sau 20s (tránh oan lúc khởi động)
MAX_FILE_S = 90             # trần tuyệt đối cho 1 file


def download(items: list[dict], out_dir: Path) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    man = out_dir / "manifest.jsonl"
    done = set()
    if man.exists():
        done = {json.loads(l)["url"] for l in man.open(encoding="utf-8") if l.strip()}
    saved = []
    with man.open("a", encoding="utf-8") as mf:
        for it in items:
            if it["url"] in done:
                continue
            ext = os.path.splitext(it["url"].split("?")[0])[1][:5] or ".bin"
            safe = re.sub(r"[^A-Za-z0-9_-]", "_", f"{it['src']}_{it['id']}")[:70]
            dest = out_dir / f"{safe}{ext}"
            try:
                h = requests.head(it["url"], headers=UA, timeout=TIMEOUT, allow_redirects=True)
                size = int(h.headers.get("content-length") or 0)
                if size > MAX_BYTES:
                    print(f"  ⤫ bỏ {it['id'][:34]} — {size // 1024 // 1024} MB > trần "
                          f"{MAX_BYTES // 1024 // 1024} MB")
                    continue
                got, t0 = 0, time.time()
                with requests.get(it["url"], headers=UA, timeout=TIMEOUT, stream=True) as r:
                    r.raise_for_status()
                    with dest.open("wb") as f:
                        for chunk in r.iter_content(1 << 16):
                            got += len(chunk)
                            if got > MAX_BYTES:      # server không khai content-length
                                raise IOError(f"vượt trần khi đang tải ({got // 1024 // 1024} MB)")
                            el = time.time() - t0
                            # Chốt tốc độ: Internet Archive đo thật chỉ ~2,5 MB/phút —
                            # 1 file ngốn 20 phút. Bỏ sớm còn hơn treo cả lượt chạy.
                            if el > STALL_AFTER_S and got / el < MIN_BPS:
                                raise IOError(f"quá chậm ({got / el / 1024:.0f} KB/s sau "
                                              f"{el:.0f}s)")
                            if el > MAX_FILE_S:
                                raise IOError(f"quá {MAX_FILE_S}s cho 1 file")
                            f.write(chunk)
            except Exception as e:
                dest.unlink(missing_ok=True)
                print(f"  ! bỏ {it['id'][:30]}: {type(e).__name__} {str(e)[:60]}")
                continue
            rec = {**it, "file": dest.name, "bytes": dest.stat().st_size}
            mf.write(json.dumps(rec, ensure_ascii=False) + "\n")
            # Flush NGAY. Sổ giấy phép là lý do tồn tại của file này — để buffer thì lượt
            # chạy bị ngắt giữa chừng sẽ còn lại một đống file KHÔNG BIẾT nguồn gốc,
            # tức là không dùng được. Đã dính thật khi phải kill một lượt tải 5,4 GB.
            mf.flush()
            os.fsync(mf.fileno())
            saved.append(rec)
            print(f"  ✓ {dest.name[:52]:<54} {rec['bytes']//1024:>7} KB  [{it['license'][:26]}]")
    return saved


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True, help="từ khoá TIẾNG ANH")
    ap.add_argument("--n", type=int, default=8, help="số file mỗi nguồn")
    ap.add_argument("--out", default="assets/stock")
    ap.add_argument("--sources", default="nasa,commons,archive")
    ap.add_argument("--dry-run", action="store_true", help="chỉ liệt kê, không tải")
    args = ap.parse_args()

    srcs = [s.strip() for s in args.sources.split(",")]
    items: list[dict] = []
    for s in srcs:
        try:
            if s == "nasa":
                items += nasa(args.q, args.n, "video") + nasa(args.q, max(args.n // 2, 2), "image")
            elif s == "commons":
                items += commons(args.q, args.n)
            elif s == "archive":
                items += archive(args.q, max(args.n // 2, 2))
            elif s == "pexels":
                items += pexels(args.q, args.n, os.getenv("PEXELS_API_KEY", ""))
        except Exception as e:
            print(f"  ! nguồn {s}: {type(e).__name__} {e}")
    print(f"[{args.q}] tìm được {len(items)} tư liệu "
          f"({ {s: sum(1 for i in items if i['src'] == s) for s in srcs} })")
    if args.dry_run:
        for it in items:
            print(f"   [{it['src']:<8}] {it['license'][:30]:<32} {it['title'][:44]}")
        return 0
    saved = download(items, Path(args.out))
    print(f"[xong] tải {len(saved)} file → {args.out}/ (sổ giấy phép: manifest.jsonl)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
