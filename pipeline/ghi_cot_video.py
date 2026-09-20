# -*- coding: utf-8 -*-
"""ghi_cot_video.py — ghi ĐÚNG MỘT Ô cột G (VIDEO) sau khi đã giao hàng xong.

    py -3.13 ghi_cot_video.py --tab shinya_shiryoshitsu --dong 2

VÌ SAO CÓ FILE NÀY
------------------------------------------------------------------------------------------------
Bước 3 (ghép video + giao hàng) nay do một agent riêng chạy, và việc cuối cùng của nó là ghi đường
dẫn thư mục giao hàng vào cột G. Trước đây việc này làm bằng tay qua MCP Google Sheets — nghĩa là
toàn bộ luật an toàn chỉ tồn tại dưới dạng CHỮ trong tài liệu:

  · "chỉ ghi cột G, cột VIDEO đã đổi từ F sang G ngày 2026-09-12, đọc header trước khi ghi"
  · "chỉ ghi khi B11 đã giao xong thật, chưa giao mà ghi là chỉ người ta vào thư mục rỗng"
  · "ghi đường dẫn thuần, không kèm dung lượng/thời lượng"
  · "TUYỆT ĐỐI không xoá dòng/cột/dữ liệu của bất kỳ trang tính nào"

Luật bằng chữ thì không ai giữ. File này biến bốn luật đó thành rào chắn chạy được:
  1. **Chỉ ghi được cột G.** Cột đích cố định trong code, không có tham số nào đổi được. Không có
     đường nào từ file này chạm tới ô khác, dòng khác, hay lệnh xoá.
  2. **Đọc lại dòng tiêu đề thật** và dừng nếu cột G không phải "VIDEO" — chống đúng cái bẫy cột
     đổi chỗ (ghi nhầm vào F là đè mất trạng thái ảnh của máy 2, không khôi phục được).
  3. **Đối chiếu đĩa trước khi ghi**: thư mục giao hàng phải tồn tại và có đủ 3 file
     (`final.mp4`, `thumbnail.png`, `listting.txt`). Thiếu một file là chưa giao xong ⇒ không ghi.
  4. **Không đè ô đã có sẵn** trừ khi truyền `--ghi-de` (in ra giá trị cũ trước khi đè).

Slug + thư mục giao hàng đều tra từ profile của lane (`publish.upload_dir`/`upload_channel`) và từ
thư mục tập trên đĩa, không nhận đường dẫn gõ tay — gõ tay là chỗ sai chính tả lọt vào trang tính.
"""
import argparse
import json
import sys
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GOC_KENH = r"E:\CLAUDE\YOUTUBE\CHANEL"      # cùng mặc định với giao_hang.py (profile thiếu upload_dir)
SHEET_ID = "1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU"
CREDS = r"D:\CLAUDE\credentials\google-sheets-key.json"

COT = "G"                 # CỐ ĐỊNH — không tham số hoá, xem docstring
TIEU_DE_COT = "VIDEO"     # dòng 1 của cột G phải là chữ này
CAN_CO = ("final.mp4", "thumbnail.png", "listting.txt")


def svc(doc_thoi=True):
    scope = "spreadsheets.readonly" if doc_thoi else "spreadsheets"
    creds = Credentials.from_service_account_file(
        CREDS, scopes=[f"https://www.googleapis.com/auth/{scope}"])
    return build("sheets", "v4", credentials=creds).spreadsheets()


def lane_theo_tab(tab):
    """Profile nào khai `publish.upload_channel` == tab thì đó là lane của tab này.

    `publish.sheet_tab` (tuỳ chọn) GHI ĐÈ tên tab khi tên tab trang tính KHÁC tên thư mục kênh
    trong CHANEL — vd Lane E: `upload_channel="kenko-chiebukuro"` (đúng tên thư mục CHANEL\\...) nhưng
    tab trang tính lại là `70dai-kenko` (đúng handle YouTube @70dai-kenko). Không khai thì mặc định
    = `upload_channel` như cũ (mọi lane khác không đổi hành vi)."""
    for f in sorted((ROOT / "profiles" / "profiles").glob("*.json")):
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        pub = p.get("publish") or {}
        if (pub.get("sheet_tab") or pub.get("upload_channel") or "") == tab:
            return p
    return None


def thu_muc_tap(prof, stt):
    """`<slug_dir>/<folder_pattern>` với nn = STT. Số tập đánh riêng từng lane nên phải khoanh theo lane.

    Pattern lấy từ profile (`folder_pattern`), mặc định `ep{nn:02d}-*` giữ hành vi cũ. Lane satori đặt
    tên kiểu `simbot2-{nn:02d}-*` — không hardcode theo lane, đọc field profile (sửa 2026-09-12, xem
    docs/GIAO_VIEC_VIET_CHAY_BUOC3.md VIỆC 0)."""
    goc = ROOT / (prof.get("slug_dir") or "assets")
    mau = prof.get("folder_pattern") or "ep{nn:02d}-*"
    m = sorted(p for p in goc.glob(mau.format(nn=stt)) if p.is_dir())
    if len(m) == 1:
        return m[0]
    if not m:
        raise SystemExit(f"✗ không thấy thư mục tập {mau.format(nn=stt)} trong {goc}")
    raise SystemExit(f"✗ có {len(m)} thư mục cùng số tập {mau.format(nn=stt)}: "
                     + ", ".join(p.name for p in m) + " → sửa tên trước khi ghi")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tab", required=True, help="ten tab kenh trong trang tinh")
    ap.add_argument("--dong", required=True, type=int, help="STT o cot A (KHONG phai so dong sheet)")
    ap.add_argument("--ghi-de", action="store_true", help="cho phep de len o G da co san")
    ap.add_argument("--thu", action="store_true", help="chi kiem va in ra, KHONG ghi")
    a = ap.parse_args()

    prof = lane_theo_tab(a.tab)
    if not prof:
        raise SystemExit(f"✗ không profile nào khai publish.upload_channel = '{a.tab}'")
    tap = thu_muc_tap(prof, a.dong)

    pub = prof.get("publish") or {}
    # giao_hang.py dùng `GOC_KENH` làm mặc định khi profile thiếu publish.upload_dir (lane satori
    # CHỈ khai upload_channel) — phải đọc CÙNG mặc định, nếu không sẽ tìm nhầm trong cwd (rỗng).
    goc_kenh = Path(pub.get("upload_dir") or GOC_KENH) / str(pub.get("upload_channel"))
    # giao_hang.py LUÔN đặt thư mục giao hàng dạng ep<nn>-<tên> (prefix "ep" + số tập + tên đề tài/slug),
    # còn tap.name (thư mục LÀM VIỆC) có thể KHÔNG có prefix "ep" (lane satori: simbot2-11-...).
    # Đừng tự ghép tên theo trí nhớ — TÌM TRÊN ĐĨA theo ep<nn>-*: đúng 1 → dùng; 0 → fallback tap.name;
    # >1 → báo lỗi (trùng, cần người dọn). Sửa 2026-09-13 (vòng 3) sau khi vấp: giao_hang tạo ep11-...
    # còn ghi_cot_video tìm simbot2-11-... → "chưa có thư mục giao hàng" dù đã giao xong.
    thu_muc_giao = sorted(p for p in goc_kenh.glob(f"ep{a.dong:02d}-*") if p.is_dir())
    if len(thu_muc_giao) == 1:
        giao = thu_muc_giao[0]
    elif not thu_muc_giao:
        giao = goc_kenh / tap.name          # lane không dùng prefix "ep" — giữ hành vi cũ
    else:
        raise SystemExit("✗ có " + str(len(thu_muc_giao)) + f" thư mục giao hàng ep{a.dong:02d}-* trong "
                         + str(goc_kenh) + ": " + ", ".join(p.name for p in thu_muc_giao)
                         + " → dọn bớt trước khi ghi")

    # --- rào 3: đĩa phải chứng minh đã giao xong -------------------------------------------------
    if not giao.is_dir():
        raise SystemExit(f"✗ chưa có thư mục giao hàng: {giao}\n"
                         f"  → chạy B11 (make_video.py --from B8) cho xong rồi hãy ghi.")
    thieu = [t for t in CAN_CO if not (giao / t).exists()]
    if thieu:
        raise SystemExit(f"✗ thư mục giao hàng thiếu {len(thieu)} file: {', '.join(thieu)}\n"
                         f"  {giao}\n  → chưa giao xong, KHÔNG ghi cột {COT}.")

    dong_sheet = a.dong + 1          # STT n nằm ở dòng n+1 (dòng 1 là tiêu đề)
    s = svc(doc_thoi=True)

    # --- rào 2: đọc lại tiêu đề thật, không tin trí nhớ ------------------------------------------
    hd = s.values().get(spreadsheetId=SHEET_ID,
                        range=f"{a.tab}!{COT}1").execute().get("values", [[""]])
    ten_cot = (hd[0][0] if hd and hd[0] else "").strip().upper()
    if ten_cot != TIEU_DE_COT:
        raise SystemExit(f"✗ cột {COT} dòng 1 đang là '{ten_cot or '(trống)'}', không phải "
                         f"'{TIEU_DE_COT}' → cột đã đổi chỗ, DỪNG (ghi tiếp là đè nhầm cột khác).")

    cur = s.values().get(spreadsheetId=SHEET_ID,
                         range=f"{a.tab}!A{dong_sheet}:{COT}{dong_sheet}").execute().get("values", [[]])
    hang = cur[0] if cur else []
    stt_that = (hang[0] if hang else "").strip()
    de_tai = (hang[1] if len(hang) > 1 else "").strip()
    cu = (hang[6] if len(hang) > 6 else "").strip()

    if stt_that != str(a.dong):
        raise SystemExit(f"✗ dòng {dong_sheet} có STT = '{stt_that}', không phải {a.dong} "
                         f"→ trang tính đã xê dịch, DỪNG.")

    print(f"tab {a.tab} · STT {a.dong} (dòng {dong_sheet}) · {de_tai[:50]}")
    print(f"  thư mục giao hàng: {giao}  ({', '.join(CAN_CO)} đủ)")

    # --- rào 4: không đè im lặng -----------------------------------------------------------------
    if cu and not a.ghi_de:
        print(f"  ô {COT}{dong_sheet} ĐÃ CÓ: {cu}")
        raise SystemExit(f"✗ không đè ô đã có. Đúng rồi thì thôi; cần đổi thì thêm --ghi-de.")
    if cu:
        print(f"  ⚠️ đè lên giá trị cũ: {cu}")

    if a.thu:
        print(f"  (--thu) sẽ ghi {COT}{dong_sheet} = {giao}  — chưa ghi gì cả")
        return 0

    svc(doc_thoi=False).values().update(
        spreadsheetId=SHEET_ID, range=f"{a.tab}!{COT}{dong_sheet}",
        valueInputOption="USER_ENTERED", body={"values": [[str(giao)]]}).execute()
    print(f"✓ đã ghi {COT}{dong_sheet} = {giao}")
    print(f"\nĐưa đường dẫn này cho chủ dự án:\n  {giao}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
