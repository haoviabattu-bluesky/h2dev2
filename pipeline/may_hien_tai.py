r"""Máy nào đang chạy code — một chỗ DUY NHẤT trả lời "đây có phải máy 2 không".

Anh chốt 2026-10-21: TỪ NAY MÁY 2 LÀM 100% A→Z (kịch bản → hook → giọng → ảnh → dựng → giao), không còn
"máy 1 chạy kịch bản rồi đóng gói giao máy 2". Máy 2 chạy thẳng từ checkout git `E:\CLAUDE\YOUTUBE\h2dev`
(không qua cây bundle `buoc2_3_tool`), nên các cổng cũ kiểu "đang ở bundle mới là máy 2" không còn nhận ra máy 2.

Cách đánh dấu máy 2 (chọn 1, KHÔNG commit lên git):
  1. file `E:\CLAUDE\YOUTUBE\h2dev\MAY.local` chứa đúng chữ `2`      ← cách chính, làm 1 lần
  2. biến môi trường `H2DEV_MAY=2`
Máy 1 không có file/biến này → hành vi cũ giữ nguyên.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE_DANH_DAU = ROOT / "MAY.local"


def so_may():
    """'2' / '1' … theo env H2DEV_MAY, rồi tới file MAY.local; không có gì → '1'."""
    v = (os.environ.get("H2DEV_MAY") or "").strip()
    if not v and FILE_DANH_DAU.exists():
        v = FILE_DANH_DAU.read_text(encoding="utf-8", errors="ignore").strip()
    return v or "1"


def la_may2():
    return so_may() == "2" or "buoc2_3_tool" in str(Path(__file__).resolve())


if __name__ == "__main__":
    print(f"máy {so_may()} · la_may2={la_may2()} · file đánh dấu: {FILE_DANH_DAU} ({'có' if FILE_DANH_DAU.exists() else 'không có'})")
