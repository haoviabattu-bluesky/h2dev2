# -*- coding: utf-8 -*-
"""ghi_cot_anh.py — ghi ĐÚNG MỘT Ô cột F (STATUS-IMG) sau khi đã gói + gửi job cho máy 2.

    py -3.13 ghi_cot_anh.py --tab shinya_shiryoshitsu --dong 8 --trang-thai "Da gui may 2 | jobs/ep08"

Cùng khuôn an toàn với `ghi_cot_video.py` (cột G): chỉ ghi được đúng cột F cố định trong code, đọc
lại tiêu đề thật trước khi ghi, không đè ô đã có sẵn trừ khi `--ghi-de`. Khác `ghi_cot_video.py`:
không đối chiếu đĩa (không có "đủ 3 file" để kiểm ở bước này) — người gọi (`goi_buoc2_3.py` hoặc
người dùng) tự chịu trách nhiệm nội dung `--trang-thai` đúng sự thật, vì trạng thái ảnh vốn đến từ
NHIỀU nguồn khác nhau (máy 2 Flow, gpti2, upload-job cũ) không có một tín hiệu đĩa chung để máy tự đo.
"""
import argparse
import sys
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SHEET_ID = "1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU"
CREDS = r"D:\CLAUDE\credentials\google-sheets-key.json"
COT = "F"
TIEU_DE_COT = "STATUS-IMG"


def svc(doc_thoi=True):
    scope = "spreadsheets.readonly" if doc_thoi else "spreadsheets"
    creds = Credentials.from_service_account_file(
        CREDS, scopes=[f"https://www.googleapis.com/auth/{scope}"])
    return build("sheets", "v4", credentials=creds).spreadsheets()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tab", required=True)
    ap.add_argument("--dong", required=True, type=int, help="STT ở cột A (KHÔNG phải số dòng sheet)")
    ap.add_argument("--trang-thai", required=True, help="nội dung ghi vào ô F")
    ap.add_argument("--ghi-de", action="store_true")
    ap.add_argument("--thu", action="store_true")
    a = ap.parse_args()

    dong_sheet = a.dong + 1
    s = svc(doc_thoi=True)

    hd = s.values().get(spreadsheetId=SHEET_ID,
                        range=f"{a.tab}!{COT}1").execute().get("values", [[""]])
    ten_cot = (hd[0][0] if hd and hd[0] else "").strip().upper()
    if ten_cot != TIEU_DE_COT:
        raise SystemExit(f"✗ cột {COT} dòng 1 đang là '{ten_cot or '(trống)'}', không phải "
                         f"'{TIEU_DE_COT}' → cột đã đổi chỗ, DỪNG.")

    cur = s.values().get(spreadsheetId=SHEET_ID,
                         range=f"{a.tab}!A{dong_sheet}:{COT}{dong_sheet}").execute().get("values", [[]])
    hang = cur[0] if cur else []
    stt_that = (hang[0] if hang else "").strip()
    de_tai = (hang[1] if len(hang) > 1 else "").strip()
    cu = (hang[5] if len(hang) > 5 else "").strip()

    if stt_that != str(a.dong):
        raise SystemExit(f"✗ dòng {dong_sheet} có STT = '{stt_that}', không phải {a.dong} "
                         f"→ trang tính đã xê dịch, DỪNG.")

    print(f"tab {a.tab} · STT {a.dong} (dòng {dong_sheet}) · {de_tai[:50]}")

    if cu and not a.ghi_de:
        print(f"  ô {COT}{dong_sheet} ĐÃ CÓ: {cu}")
        raise SystemExit("✗ không đè ô đã có. Đúng rồi thì thôi; cần đổi thì thêm --ghi-de.")
    if cu:
        print(f"  ⚠️ đè lên giá trị cũ: {cu}")

    if a.thu:
        print(f"  (--thu) sẽ ghi {COT}{dong_sheet} = {a.trang_thai} — chưa ghi gì cả")
        return 0

    svc(doc_thoi=False).values().update(
        spreadsheetId=SHEET_ID, range=f"{a.tab}!{COT}{dong_sheet}",
        valueInputOption="USER_ENTERED", body={"values": [[a.trang_thai]]}).execute()
    print(f"✓ đã ghi {COT}{dong_sheet} = {a.trang_thai}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
