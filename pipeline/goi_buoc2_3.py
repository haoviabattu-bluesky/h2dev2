# -*- coding: utf-8 -*-
"""goi_buoc2_3.py — VIỆC 2 (mỗi tập 1 lần): gói TOÀN BỘ dữ liệu bước 1 của 1 tập Lane A
(toshi-densetsu-jp) thành 1 gói tự chứa, đặt vào FlowHandoff_local/jobs_buoc23/<slug>/ để
Syncthing mang sang máy 2 — nơi chạy `docs` (FlowHandoff_local/shared/GIAO_VIEC_MAY2_BUOC2_3.md)
để tự làm Bước 2 (ảnh, gpti2 nếu <50 ảnh) + Bước 3 (ghép video) gộp làm một, KHÔNG cần Claude Code.

Khác `drive_handoff.py upload-job` (chỉ gửi `img_ai/` — dùng cho luồng Google Flow cũ, người vẽ
tay): tool này gửi CẢ THƯ MỤC TẬP (script/giọng/kho hình/đơn ảnh) vì máy 2 giờ tự chạy `make_video.py
--from B8` tại chỗ, cần đủ input y hệt máy 1 có.

    py -3.13 goi_buoc2_3.py --slug ep08-fatima-akita
"""
import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

# Thư mục con/tệp KHÔNG gửi đi — rác trung gian của chính máy 1, máy 2 không cần và gửi chỉ tốn
# băng thông/dung lượng Syncthing (đặc biệt _truoc_khi_sua/_truoc_khi_viet_lai có thể nặng vài chục MB).
BO_QUA = {"__pycache__", "_truoc_khi_sua", "_truoc_khi_viet_lai", ".git"}
BO_QUA_DUOI = {".pyc"}


def _copy_loc(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in BO_QUA or item.suffix in BO_QUA_DUOI:
            continue
        if item.is_dir():
            _copy_loc(item, dst / item.name)
        else:
            shutil.copy2(item, dst / item.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--out-root", default="")
    a = ap.parse_args()

    src = ROOT / "assets" / "toshi-densetsu-jp" / a.slug
    if not src.exists():
        raise SystemExit(f"✗ Không thấy thư mục tập: {src}")
    for can in ("script.txt", "voice.mp3", "voice.srt", "khop_hinh.json"):
        if not (src / can).exists():
            raise SystemExit(f"✗ Thiếu {can} — tập chưa xong hết Bước 1, chưa gói được.")

    # ⚠️ Dùng ĐÚNG "jobs" (không phải "jobs_buoc23") — đây là 1 trong 4 thư mục Syncthing THẬT SỰ
    # đang đồng bộ (FlowHandoff_local\{jobs,results,shared} + CHANEL, xem CLAUDE.md mục Syncthing).
    # Bản đầu tự đặt tên "jobs_buoc23" tưởng vậy cho rõ nghĩa, nhưng KHÔNG có Syncthing folder nào
    # trỏ vào đó nên máy 2 không bao giờ nhận được (đo thật 2026-09-17: máy 2 báo "không thấy
    # jobs_buoc23"). "jobs/<slug>/" trước đây chỉ chứa img_ai/ (từ drive_handoff.py upload-job cho
    # luồng Flow cũ) — gói bước-2-3 nay ĐỔ THÊM vào cùng thư mục đó (không xoá gì có sẵn), thành nơi
    # giao nhận DUY NHẤT cho 1 slug thay vì 2 quy ước khác nhau.
    dst_root = Path(a.out_root) if a.out_root else ROOT / "FlowHandoff_local" / "jobs"
    dst = dst_root / a.slug
    # KHÔNG rmtree trước khi copy: "jobs/<slug>/" có thể đã có sẵn "img_ai/" từ một lượt
    # `drive_handoff.py upload-job` cũ (luồng Flow) — xoá sạch rồi mới copy sẽ mất dữ liệu máy 2 đã
    # nhận. `_copy_loc` chỉ ghi đè file trùng tên + thêm file mới, không đụng file không có trong
    # nguồn.
    _copy_loc(src, dst)

    n_prompts = 0
    pf = dst / "img_ai" / "prompts.txt"
    if pf.exists():
        n_prompts = sum(1 for l in pf.read_text(encoding="utf-8").splitlines() if l.strip())

    print(f"✓ đã gói {a.slug} → {dst}")
    print(f"  ảnh cần vẽ (đọc từ img_ai/prompts.txt): {n_prompts}")
    if n_prompts:
        print(f"  → Lane không REF-LOCK: máy 2 luôn dùng gpti2 vẽ thẳng (bất kể số lượng), không "
              f"còn chờ Google Flow (chốt 2026-09-17).")
    print("  Syncthing sẽ tự đồng bộ thư mục trên sang máy 2. Kết quả trả về ở "
          "FlowHandoff_local/results/video_render/<slug>/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
