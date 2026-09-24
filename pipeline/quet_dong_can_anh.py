r"""quet_dong_can_anh.py — doc trang tinh, tra ve DANH SACH JOB CAN SINH ANH theo DONG.

Vi sao co file nay (anh chot 2026-09-11): giao viec bang slug (`chay job simbot2-11-DXXwIxhcfF0`)
la bat nguoi doc va go mot chuoi dai vo nghia. Cach giao viec CHUAN cua du an la theo DONG:

    "vao tab Satori-Lopezzapa68, chay job tao anh cho dong 11"
    "vao tab A-shinya_shiryoshitsu, chay job tao anh cho dong 2-8"

Dong -> slug do MAY tra, khong phai nguoi nho. Slug lay tu doan cuoi duong dan o cot E (FOLDER),
khong co thi lay o cot F sau dau `|`.

Dai dong (`--dong 5-12`) thi chi lay nhung dong co cot F = "Xong noi dung - can anh", chay LAN LUOT
TU TREN XUONG. Dong da `Dang tao anh` / `Img done` / `LOI:` deu bo qua (in ra de biet, khong chay).

CHI DOC, KHONG GHI — dung chung cho MOI tab/lane. Ghi cot F la viec cua lenh khac.

  py -3.13 quet_dong_can_anh.py --tab Satori-Lopezzapa68 --dong 11
  py -3.13 quet_dong_can_anh.py --tab A-shinya_shiryoshitsu --dong 2-8
  py -3.13 quet_dong_can_anh.py --tab Satori-Lopezzapa68 --dong 11 --lenh      (in san lenh download-job)

exit 0 = co it nhat 1 job can chay · exit 1 = khong co dong nao can anh trong dai do.

LUU Y --dong la SO THU TU o cot A (STT), KHONG phai so dong cua Google Sheet: STT 11 nam o dong 12
cua trang tinh vi dong 1 la tieu de. Script tu cong bu, nguoi dung cu noi theo STT.
"""
import argparse
import re
import sys
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import sheet_tab  # noqa: E402  (tên tab {Lane}-{kênh} — nguồn: profile.publish.sheet_tab)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SHEET_ID = "1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU"
CREDS = r"D:\CLAUDE\credentials\google-sheets-key.json"
CAN_ANH = "xong nội dung - cần ảnh"
# Trang thai may 2 ghi khi da ve xong — dau vao cua BUOC 3 (ghep video).
IMG_DONE = "img done"


def svc():
    creds = Credentials.from_service_account_file(
        CREDS, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    return build("sheets", "v4", credentials=creds).spreadsheets()


def doc_dai(s):
    """'11' -> [11] · '5-12' -> [5..12] · '3,7,9' -> [3,7,9]."""
    ra = []
    for phan in str(s).split(","):
        phan = phan.strip()
        if not phan:
            continue
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", phan)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            ra += list(range(min(a, b), max(a, b) + 1))
        else:
            ra.append(int(phan))
    return sorted(set(ra))


def slug_tu_dong(cot_e, cot_f):
    """Doan cuoi duong dan = slug. **COT F TRUOC**, khong co thi lay cot E.

    Vi sao F truoc (sua 2026-09-12, ban cu uu tien E va no SAI cho lane toshi-densetsu-jp):
    hai cot la HAI KHONG GIAN TEN KHAC NHAU.
      · Cot E = duong dan HO SO NGHIEN CUU do du an SPACE_RESEARCH dat: `..._READY\\02-walton\\`
      · Cot F = duong dan THU MUC TAP do may 1 tu dat khi giao viec: `...\\ep02-walton`
        (so tap phai co tien to `ep` theo luat danh so trong CLAUDE.md)
    Slug tren Drive lay theo THU MUC TAP, nen doc cot E se ra `02-walton` — mot job KHONG TON TAI,
    va `download-job` cua may 2 bao "khong thay job" du may 1 da up day du. Cot F con dung hon ve
    ban chat: no do chinh may 1 ghi DUNG LUC giao viec, con cot E co the tro ho so goc da doi cho.
    """
    for nguon in ((cot_f.split("|", 1)[1] if "|" in cot_f else ""), cot_e):
        p = (nguon or "").strip().strip('"').rstrip("\\/")
        if p:
            ten = Path(p).name
            if ten:
                return ten
    return ""


ASSETS = Path(__file__).resolve().parent.parent / "assets"


def thu_muc_lane(tab):
    """Tim `slug_dir` cua lane co `publish.upload_channel` == ten tab.

    Tra ve (duong_dan_slug_dir, profile_dict) — can ca profile de doc `folder_pattern`
    (sua 2026-09-12, xem docs/GIAO_VIEC_VIET_CHAY_BUOC3.md VIỆC 0). So tap danh RIENG
    TUNG LANE, nen quet `assets/*/ep<nn>-*` la SAI: `ep02-*` khop ca
    `toshi-densetsu-jp/ep02-walton` lan `irogatatarukioku/ep02-kuribayashi-iwojima` => hai ket qua,
    khong chon duoc cai nao. Ten tab chinh la `publish.upload_channel` trong profile, nen tra nguoc
    duoc ma khong phai hardcode bang tab->lane o day (dung luat: khac biet lane = field profile).
    """
    p = sheet_tab.lane_theo_tab(tab)          # 2026-09-24: tab {Lane}-{kênh}, tên cũ vẫn tra được
    if p:
        return ASSETS.parent / (p.get("slug_dir") or "assets"), p
    return None, None


def slug_tu_dia(stt, tab):
    """Tra slug bang THU MUC TAP tren dia: `<slug_dir cua lane>/<folder_pattern>` voi nn = STT.

    Vi sao can duong nay: cot F cua trang tinh la O DUNG CHUNG hai ben. May 1 ghi vao do
    'Xong noi dung - can anh | <duong dan>', nhung khi may 2 ve xong no GHI DE thanh
    'Img done - 300/300 anh (...)' — va duong dan bien mat. Den luot buoc 3 doc thi chi con cot E,
    ma cot E la ho so nghien cuu (`_READY\\02-walton`) chu khong phai thu muc tap (`ep02-walton`)
    => tra ra mot slug khong ton tai. Da dinh that 2026-09-12.
    Dia moi la nguon chan ly: luat danh so cua du an ghi ro **so tap = STT cot A**, nen glob
    theo `folder_pattern` cua profile la duy nhat va truy nguoc duoc (sua 2026-09-12, VIỆC 0 —
    lane satori dung `simbot2-{nn:02d}-*` chu khong phai `ep{nn:02d}-*`). Khong doan, khong ghep chuoi.
    """
    goc, prof = thu_muc_lane(tab)
    if not goc or not goc.is_dir():
        return ""
    mau = (prof or {}).get("folder_pattern") or "ep{nn:02d}-*"
    m = sorted(p for p in goc.glob(mau.format(nn=stt)) if p.is_dir())
    return m[0].name if len(m) == 1 else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tab", required=True, help="ten tab kenh trong trang tinh")
    ap.add_argument("--dong", required=True,
                    help="STT o cot A: '11' hoac dai '5-12' hoac '3,7,9'. BAT BUOC — "
                         "khong co thi khong chay (cam chay ca tab)")
    ap.add_argument("--lenh", action="store_true", help="in san lenh de copy")
    # BUOC 3 (ghep video) can dung danh sach NGUOC LAI voi buoc 2: no tim dong may 2 da ve XONG.
    # Ban dau script chi phuc vu may 2 nen dong `Img done` bi xep vao "bo qua" va ham tra exit 1 —
    # agent buoc 3 chay theo tai lieu se khong lay duoc slug nao. Cung mot script, doi moi bo loc.
    ap.add_argument("--cho-ghep", action="store_true",
                    help="BUOC 3: liet ke dong may 2 DA VE XONG (cot F 'Img done') va cot G con "
                         "trong — tuc la dang cho ghep video")
    a = ap.parse_args()
    a.tab = sheet_tab.tab_that(a.tab)

    stt_list = doc_dai(a.dong)
    if not stt_list:
        print("✗ --dong khong doc duoc")
        return 1

    # STT n nam o dong n+1 cua trang tinh (dong 1 la tieu de)
    d1, d2 = min(stt_list) + 1, max(stt_list) + 1
    res = svc().values().get(spreadsheetId=SHEET_ID,
                             range=f"{a.tab}!A{d1}:H{d2}").execute()
    rows = res.get("values", [])

    def o(r, i):
        return (r[i] if i < len(r) else "").strip()

    can, bo_qua = [], []
    for stt in stt_list:
        idx = stt + 1 - d1
        r = rows[idx] if 0 <= idx < len(rows) else []
        de_tai, folder, status, video = o(r, 1), o(r, 4), o(r, 5), o(r, 6)
        slug = slug_tu_dong(folder, status)
        if a.cho_ghep:
            # Buoc 3 uu tien THU MUC TAP tren dia (xem docstring slug_tu_dia), cot E/F chi la du phong.
            slug = slug_tu_dia(stt, a.tab) or slug
            if not status.lower().startswith(IMG_DONE):
                bo_qua.append((stt, f"chưa vẽ xong ảnh — cột F: {status or '(trống)'}", slug))
            elif video:
                bo_qua.append((stt, f"đã giao video rồi — cột G: {video}", slug))
            elif not slug:
                bo_qua.append((stt, "cột F báo Img done NHƯNG không dò được slug", ""))
            else:
                can.append((stt, slug, de_tai))
        elif status.lower().startswith(CAN_ANH):
            if not slug:
                bo_qua.append((stt, "cột F báo cần ảnh NHƯNG không dò được slug (cột E trống)", ""))
            else:
                can.append((stt, slug, de_tai))
        else:
            bo_qua.append((stt, status or "(cột STATUS-IMG trống)", slug))

    print(f"=== tab {a.tab} · STT {a.dong} ===")
    for stt, ly_do, slug in bo_qua:
        print(f"  – STT {stt}: bỏ qua — {ly_do}")
    if not can:
        print("\n✗ Không có dòng nào ở trạng thái "
              + ("'Img done' + cột G trống" if a.cho_ghep else "'Xong nội dung - cần ảnh'")
              + " trong dải này.")
        return 1

    print(f"\n✓ {len(can)} job {'chờ ghép video' if a.cho_ghep else 'cần sinh ảnh'} — "
          f"chạy LẦN LƯỢT TỪ TRÊN XUỐNG:")
    for i, (stt, slug, de_tai) in enumerate(can, 1):
        print(f"  {i}. STT {stt} · {slug}")
        if de_tai:
            print(f"       {de_tai[:70]}")
        if a.lenh and a.cho_ghep:
            print(f'       py -3.13 drive_handoff.py download-result {slug} '
                  f'"<thư mục tập>\\{slug}\\img_ai"')
        elif a.lenh:
            print(f'       py -3.13 drive_handoff.py download-job {slug} "<thư mục tạm>\\{slug}"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
