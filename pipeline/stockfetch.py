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

from stock_sources import UA, TIMEOUT, archive, commons, nasa, pexels, nara

# Wikimedia đòi User-Agent MÔ TẢ ĐƯỢC + có cách liên hệ; UA trình duyệt giả bị siết sớm hơn.
UA = {"User-Agent": "h2dev-stockfetch/1.1 (YouTube documentary b-roll; contact via project owner)"}
TIMEOUT = 45


def _load_dotenv() -> None:
    """Đọc tools/.env, chỉ set biến CHƯA có sẵn trong environment — không có
    python-dotenv trong dự án nên tự đọc tối giản. Không ghi đè PEXELS_API_KEY
    nếu người dùng đã tự export tay (env thật luôn ưu tiên hơn .env)."""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"'))


_load_dotenv()

# Chống 429 của Wikimedia. Đo thật 2026-09-10: tải dồn ~40 file liên tiếp là mọi request sau đó
# trả 429 hàng loạt, cả một lượt B5 tải về 0 file mà KHÔNG hề báo hỏng — kho vẫn "đủ" nhờ file cũ
# nên lỗi này im lặng làm nghèo kho tư liệu qua từng tập.
NGHI_GIUA_FILE = 0.5        # giây, giữa hai lượt tải
RETRY_429 = 3               # số lần thử lại
CHO_429 = (5, 15, 40)       # giãn dần

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
            time.sleep(NGHI_GIUA_FILE)
            try:
                h = None
                for lan in range(RETRY_429 + 1):
                    h = requests.head(it["url"], headers=UA, timeout=TIMEOUT, allow_redirects=True)
                    if h.status_code != 429:
                        break
                    if lan == RETRY_429:
                        raise IOError("429 sau khi đã chờ — nguồn đang siết, dừng file này")
                    cho = int(h.headers.get("Retry-After") or CHO_429[min(lan, len(CHO_429) - 1)])
                    print(f"  … 429, chờ {cho}s rồi thử lại ({lan+1}/{RETRY_429})")
                    time.sleep(cho)
                size = int(h.headers.get("content-length") or 0)
                if size > MAX_BYTES:
                    print(f"  ⤫ bỏ {it['id'][:34]} — {size // 1024 // 1024} MB > trần "
                          f"{MAX_BYTES // 1024 // 1024} MB")
                    continue
                got, t0 = 0, time.time()
                # 429 rơi vào CẢ lượt GET chứ không chỉ HEAD — bản chỉ vá HEAD vẫn mất file
                # (đo thật: 1/3 file vẫn hỏng). Thử lại ngay trong vòng lặp file này.
                for lan in range(RETRY_429 + 1):
                    r0 = requests.get(it["url"], headers=UA, timeout=TIMEOUT, stream=True)
                    if r0.status_code != 429:
                        break
                    r0.close()
                    if lan == RETRY_429:
                        raise IOError("429 ở lượt tải — nguồn đang siết")
                    cho = int(r0.headers.get("Retry-After") or CHO_429[min(lan, len(CHO_429) - 1)])
                    print(f"  … 429 khi tải, chờ {cho}s ({lan+1}/{RETRY_429})")
                    time.sleep(cho)
                with r0 as r:
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
    ap.add_argument("--sources", default="nasa,commons,pexels,archive")
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
            elif s == "nara":
                items += nara(args.q, args.n, "image") + nara(args.q, max(args.n // 2, 2), "video")
            elif s == "pexels":
                # KHÔNG truyền key ở đây: để `pexels()` tự xoay vòng mọi key PEXELS_API_KEY*
                # trong .env. Truyền một key cụ thể là khoá cứng vào đúng hạn mức của key đó.
                items += pexels(args.q, args.n)
        except Exception as e:
            print(f"  ! nguồn {s}: {type(e).__name__} {e}")
    # `nap_kho()`/`chia_theo_cau()` (stock_cut.py) đọc `manifest["query"]` để biết file này tải về
    # bằng từ khoá nào — đó là sợi dây DUY NHẤT nối 1 file trong kho với 1 đoạn lời cụ thể. File
    # này quên gắn field đó vào từng item trước khi `download()` ghi manifest, nên MỌI file do
    # chính `stockfetch.py` tải (khác với file do hồ sơ nghiên cứu tải sẵn, vốn có gắn sẵn) đều có
    # `query=""` trong manifest.jsonl — không lỗi rành rành (vẫn tải được, vẫn xem được), chỉ lặng
    # lẽ làm `chon_nguon()` không bao giờ chọn ĐÚNG các file này cho đúng đoạn, phải rơi vào nhánh
    # "mượn cả kho, bỏ ràng buộc chương". Đo thật ep06-mandela-effect: 64/274 file (23%) trong
    # manifest.jsonl thiếu query vì lý do này.
    for it in items:
        it.setdefault("query", args.q)
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
