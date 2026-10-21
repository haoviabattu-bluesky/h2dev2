# -*- coding: utf-8 -*-
r"""ghi_sheet_da_thay_thumb.py — sau khi đã thay tiêu đề + thumbnail trên Studio, ghi sheet cho 1 dòng tập (18/10/2026).
  · tab lane, dòng <row>: E dòng 1 = tiêu đề mới (giữ nguyên mô tả), G = link thumb mới, K = "ĐÃ THAY TIÊU ĐỀ + THUMB dd/mm/yyyy",
    tô nền xanh #D9EAD3 cột A→<den> (giống các dòng xanh khác của tab)
  · tab TONGHOP: cột có dòng 1 = tên tab lane × dòng có cột A = EpNN → "ĐÃ THAY THUMB"
Không xoá gì; giá trị cũ E→K lưu vào <tập>\thumb_v2\sheet_truoc_<ngày>.json trước khi ghi.
    py -3.13 -X utf8 tools\ghi_sheet_da_thay_thumb.py --tab L-shakai-no-naze --row 6 --ep 5 --tap <thư mục tập> --den S
"""
import argparse, datetime, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
import dong_goi_may2 as dg  # noqa: E402

XANH = {"red": 0.8509804, "green": 0.91764706, "blue": 0.827451}

ap = argparse.ArgumentParser()
ap.add_argument("--tab", required=True)
ap.add_argument("--row", type=int, required=True)
ap.add_argument("--ep", type=int, required=True)
ap.add_argument("--tap", required=True)
ap.add_argument("--den", default="L", help="cột cuối tô xanh")
a = ap.parse_args()

tap = Path(a.tap)
spec = json.loads((tap / "thumb_v2" / "SPEC.json").read_text(encoding="utf-8"))
url = (tap / "thumb_v2" / "thumb_url.txt").read_text(encoding="utf-8").strip()
hom_nay = datetime.date.today().strftime("%d/%m/%Y")
s = dg.svc(doc_thoi=False)
v = s.values()
ID = dg.SHEET_ID

cu = v.get(spreadsheetId=ID, range=f"'{a.tab}'!E{a.row}:K{a.row}").execute().get("values", [[]])[0]
(tap / "thumb_v2" / f"sheet_truoc_{datetime.date.today():%Y%m%d}.json").write_text(
    json.dumps({"tab": a.tab, "row": a.row, "E_to_K": cu}, ensure_ascii=False, indent=1), encoding="utf-8")
dong = (cu[0] if cu else "").split("\n")
dong[0] = spec["title"]
for o, val in ((f"E{a.row}", "\n".join(dong)), (f"G{a.row}", url), (f"K{a.row}", f"ĐÃ THAY TIÊU ĐỀ + THUMB {hom_nay}")):
    v.update(spreadsheetId=ID, range=f"'{a.tab}'!{o}", valueInputOption="RAW", body={"values": [[val]]}).execute()

meta = s.get(spreadsheetId=ID, fields="sheets(properties(sheetId,title))").execute()
sid = {x["properties"]["title"]: x["properties"]["sheetId"] for x in meta["sheets"]}
den = ord(a.den.upper()) - 64
s.batchUpdate(spreadsheetId=ID, body={"requests": [{"repeatCell": {
    "range": {"sheetId": sid[a.tab], "startRowIndex": a.row - 1, "endRowIndex": a.row, "startColumnIndex": 0, "endColumnIndex": den},
    "cell": {"userEnteredFormat": {"backgroundColor": XANH}}, "fields": "userEnteredFormat.backgroundColor"}}]}).execute()

hang1 = [str(x).strip() for x in (v.get(spreadsheetId=ID, range="TONGHOP!1:1").execute().get("values") or [[]])[0]]
cot_a = [str(r[0]).strip() if r else "" for r in v.get(spreadsheetId=ID, range="TONGHOP!A1:A200").execute().get("values", [])]
ep = f"Ep{a.ep:02d}"
if a.tab in hang1 and ep in cot_a:
    ci, ri = hang1.index(a.tab), cot_a.index(ep) + 1
    col = ""
    n = ci + 1
    while n:
        n, r = divmod(n - 1, 26)
        col = chr(65 + r) + col
    o = f"TONGHOP!{col}{ri}"
    old = (v.get(spreadsheetId=ID, range=o).execute().get("values") or [[""]])[0]
    v.update(spreadsheetId=ID, range=o, valueInputOption="RAW", body={"values": [["ĐÃ THAY THUMB"]]}).execute()
    print(f"✓ {o}: {old[0] if old else ''} → ĐÃ THAY THUMB")
else:
    print(f"⚠️ TONGHOP: không thấy cột '{a.tab}' hoặc dòng {ep}")
print(f"✓ {a.tab} dòng {a.row}: E tiêu đề mới, G {url}, K ĐÃ THAY TIÊU ĐỀ + THUMB {hom_nay}, tô xanh A→{a.den}")
