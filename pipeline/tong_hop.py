# -*- coding: utf-8 -*-
r"""tong_hop.py — ghi trạng thái tập vào tab TONGHOP (bảng tổng quan mọi lane, anh chốt 2026-10-04).

Bố cục tab TONGHOP: dòng 1 = tên tab lane (`publish.sheet_tab`, vd `L-shakai-no-naze`, `Lane-J`) · cột A = `Ep01`, `Ep02`…
Ô giao (tập, lane) = 1 chữ trong dropdown. Tool chỉ ghi 5 chữ đầu; 3 chữ sau do máy 2 / anh:
  Chạy kịch bản        make_video bắt đầu chặng 1          (review_may3.bat_dau_b1)
  Chờ duyệt kịch bản   kịch bản khoá, gửi máy 3/anh sửa    (review_may3.share)
  Chạy Hook            nhận bản anh sửa, đi làm hook       (review_may3.nhan)
  Chờ duyệt Hook       clip hook xem thử gửi anh           (duyet_hook.gui)
  Giao máy 2           đóng gói giao máy 2 xong            (dong_goi_may2.cmd_job)
  Chạy ảnh + video · Done · Listed  → tool KHÔNG đè.
Lane chưa có cột → tool thêm tên tab vào ô trống đầu tiên dòng 1. Tập chưa có dòng → thêm `EpNN` nối tiếp cột A.
Lỗi sheet KHÔNG chặn bước chính (chỉ in cảnh báo). Không xoá gì.

Dùng tay: py -3.13 -X utf8 pipeline\tong_hop.py --profile <lane> --slug <tập> --trang-thai "Chạy Hook"
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

TAB = "TONGHOP"
CHAY_KB = "Chạy kịch bản"
CHO_KB = "Chờ duyệt kịch bản"
CHAY_HOOK = "Chạy Hook"
CHO_HOOK = "Chờ duyệt Hook"
GIAO_MAY2 = "Giao máy 2"
CHAY_VIDEO = "Chạy ảnh + video"   # 21/10 máy 2 làm A→Z: chặng dựng cũng do tool ghi (pipeline\xong_video.py)
VIDEO_XONG = "Done"
CUA_TOOL = (CHAY_KB, CHO_KB, CHAY_HOOK, CHO_HOOK, GIAO_MAY2, CHAY_VIDEO, VIDEO_XONG)


def _cot(i):
    """0 → A, 25 → Z, 26 → AA."""
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def ghi(prof, slug, trang_thai):
    if "buoc2_3_tool" in str(HERE):          # bản pipeline chạy ở máy 2 → không ghi
        return
    try:
        import dong_goi_may2 as dg
        import review_may3
        m = re.match(r"ep(\d+)", slug, re.I)
        tab = review_may3.tab_cua(prof)
        if not m or not tab:
            print(f"  ⚠️ TONGHOP: không rút được số tập/tab từ '{slug}' → bỏ qua")
            return
        ep = f"Ep{int(m.group(1)):02d}"
        s = dg.svc(doc_thoi=False)
        v = s.values()
        hang1 = (v.get(spreadsheetId=dg.SHEET_ID, range=f"{TAB}!1:1").execute().get("values") or [[]])[0]
        hang1 = [str(x).strip() for x in hang1]
        if tab in hang1:
            ci = hang1.index(tab)
        else:
            ci = next((i for i in range(1, len(hang1)) if not hang1[i]), max(len(hang1), 1))
            v.update(spreadsheetId=dg.SHEET_ID, range=f"{TAB}!{_cot(ci)}1", valueInputOption="RAW",
                     body={"values": [[tab]]}).execute()
            print(f"  ✓ TONGHOP: thêm cột {_cot(ci)} = {tab}")
        cot_a = [str(r[0]).strip() if r else "" for r in
                 v.get(spreadsheetId=dg.SHEET_ID, range=f"{TAB}!A1:A1000").execute().get("values", [])]
        so = {c.lower(): i + 1 for i, c in enumerate(cot_a) if re.fullmatch(r"(?i)ep\d+", c)}
        if ep.lower() not in so:
            cuoi = max(so.values()) if so else 3
            n_cuoi = max((int(k[2:]) for k in so), default=0)
            them = [f"Ep{n:02d}" for n in range(n_cuoi + 1, int(m.group(1)) + 1)] or [ep]
            v.update(spreadsheetId=dg.SHEET_ID, range=f"{TAB}!A{cuoi + 1}", valueInputOption="RAW",
                     body={"values": [[x] for x in them]}).execute()
            so.update({x.lower(): cuoi + 1 + i for i, x in enumerate(them)})
            print(f"  ✓ TONGHOP: thêm {', '.join(them)} ở cột A")
        o = f"{TAB}!{_cot(ci)}{so[ep.lower()]}"
        cu = (v.get(spreadsheetId=dg.SHEET_ID, range=o).execute().get("values") or [[""]])[0]
        cu = str(cu[0]).strip() if cu else ""
        if cu == trang_thai:
            return
        if cu and cu not in CUA_TOOL:
            print(f"  ⚠️ TONGHOP {o} đang '{cu}' (máy 2/anh ghi) → KHÔNG đè thành '{trang_thai}'")
            return
        v.update(spreadsheetId=dg.SHEET_ID, range=o, valueInputOption="USER_ENTERED",
                 body={"values": [[trang_thai]]}).execute()
        print(f"  ✓ TONGHOP {o} ({tab} {ep}) = {trang_thai}")
    except BaseException as e:  # noqa: BLE001 — bảng tổng quan, không phải cổng
        print(f"  ⚠️ chưa ghi được TONGHOP ({trang_thai}): {e}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--trang-thai", required=True, choices=CUA_TOOL)
    a = ap.parse_args(argv)
    import profiles
    ghi(profiles.load(a.profile), a.slug, a.trang_thai)


if __name__ == "__main__":
    main()
