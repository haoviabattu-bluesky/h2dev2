# -*- coding: utf-8 -*-
"""ghi_cot_video_goc.py — ghi LINK VIDEO GỐC của tập vào ĐÚNG MỘT Ô cột T (VIDEO GỐC).

    py -3.13 ghi_cot_video_goc.py --tap E:\\CLAUDE\\YOUTUBE\\h2dev\\assets\\shakai_no_naze\\ep22-izakaya-hitode
    py -3.13 ghi_cot_video_goc.py --tab L-shakai-no-naze --stt 22
    py -3.13 ghi_cot_video_goc.py --profile senior_korekara --stt 16 --thu      # chỉ in, không ghi

VÌ SAO CÓ FILE NÀY
------------------------------------------------------------------------------------------------
Anh chốt 2026-10-19: **bất kỳ tập nào chạy kịch bản thì link video gốc (nếu có) PHẢI lên trang tính
cột T (VIDEO GỐC)** — để nhìn 1 dòng là biết tập đó clone từ video nào, khỏi mở `video_goc.json`.

Nguồn dữ liệu DUY NHẤT là `<thư mục tập>\\video_goc.json` (B2 tự ghi qua `pipeline\\video_goc.py`).
File này KHÔNG đi tìm video, KHÔNG đoán ID — không có thì báo "không có" và không ghi gì.

Rào chắn (cùng khuôn `ghi_cot_video.py` cột G / `ghi_cot_anh.py` cột F):
  1. **Chỉ ghi được cột T** — cột đích cố định trong code, không tham số nào đổi được.
  2. **Đọc lại dòng tiêu đề thật**, dừng nếu T1 không phải "VIDEO GỐC" (cột đã đổi chỗ).
  3. **Khoanh đúng dòng** bằng thư mục tập ở cột C (FOLDER) — không tin số dòng nhớ tay; đối chiếu
     lại STT ở cột A trước khi ghi.
  4. **Không đè ô đã có** trừ khi `--ghi-de` (in giá trị cũ trước khi đè).

TỰ ĐỘNG: `video_goc.ghi_video_goc()` gọi hàm `ghi_tu_ep()` ngay sau khi ghi `video_goc.json` (B2 mọi
lane), nên tập nào chạy kịch bản là cột T có link luôn. `dong_goi_may2.py --job` gọi lại lần nữa lúc
đóng gói (idempotent — ô đã đúng thì thôi). Hỏng/không có credentials chỉ in cảnh báo, KHÔNG chặn tập.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SHEET_ID = "1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU"
CREDS = r"D:\CLAUDE\credentials\google-sheets-key.json"

COT = "T"                    # CỐ ĐỊNH — không tham số hoá
TIEU_DE_COT = "VIDEO GỐC"
COT_FOLDER = "C"


def svc(doc_thoi=True):
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    scope = "spreadsheets.readonly" if doc_thoi else "spreadsheets"
    creds = Credentials.from_service_account_file(
        CREDS, scopes=[f"https://www.googleapis.com/auth/{scope}"])
    return build("sheets", "v4", credentials=creds).spreadsheets()


def _chuan(s):
    return str(s or "").strip().replace("\\", "/").rstrip("/").lower()


def tab_cua_lane(prof):
    pub = prof.get("publish") or {}
    return pub.get("sheet_tab") or pub.get("upload_channel") or ""


_CACHE_TAB = {}


def _tab_that_su(s, tab):
    """Tên tab CÓ THẬT trên trang tính. Profile có thể khai `G-teinengo-tanoshimi` trong khi tab đã
    được đặt tên ngắn `G` (Lane G, kiểm 19/10) → thử: tên nguyên văn → phần sau dấu '-' đầu tiên →
    tên nào bắt đầu bằng tên khai. Không khớp gì thì trả nguyên văn (để tầng gọi báo lỗi rõ ràng).
    Danh sách tab CACHE lại: backfill nhiều tập mà gọi metadata mỗi tập là ăn 429 của Sheets."""
    if tab in _CACHE_TAB:
        return _CACHE_TAB[tab]
    try:
        md = s.get(spreadsheetId=SHEET_ID, fields="sheets.properties.title").execute()
        co = [x["properties"]["title"] for x in md.get("sheets", [])]
    except Exception:
        return tab
    ket = tab
    if tab in co:
        ket = tab
    else:
        duoi = tab.split("-", 1)[1] if "-" in tab else ""
        ung_vien = ([duoi] if duoi else []) + [c for c in co if c.lower().startswith(tab.lower())] \
            + [c for c in co if len(c) >= 2 and tab.lower().startswith(c.lower())] \
            + [c for c in co if len(c) == 1 and tab.lower().startswith(c.lower() + "-")]
        for ung in ung_vien:
            if ung and ung in co:
                ket = ung
                break
    _CACHE_TAB[tab] = ket
    return ket


def lane_theo_slug_dir(slug_dir):
    """Profile có `slug_dir` trùng (so theo đuôi đường dẫn, chịu được \\ vs /)."""
    import profiles
    want = _chuan(slug_dir)
    for pid in profiles.list_ids():
        try:
            p = profiles.load(pid)
        except BaseException:
            continue
        if _chuan(p.get("slug_dir")) == want:
            return p
    return None


def doc_link(ep_dir):
    """(url, nguon) từ `<ep_dir>\\video_goc.json`. Không có → (None, lý do)."""
    f = Path(ep_dir) / "video_goc.json"
    if not f.exists():
        return None, f"không có {f}"
    try:
        doc = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        return None, f"{f.name} hỏng ({type(e).__name__})"
    v = doc.get("video_goc") or {}
    if not v:
        ly_do = doc.get("ly_do") or "video_goc = null (lane/tập không clone 1 video cụ thể)"
        return None, f"video_goc.json không có video gốc — {ly_do}"
    url = v.get("url") or (f"https://www.youtube.com/watch?v={v['id']}" if v.get("id") else "")
    if not url:
        return None, "video_goc.json có mục nhưng thiếu id/url"
    return url, v.get("id") or ""


def tim_dong(s, tab, ten_thu_muc):
    """Dòng sheet (1-based) có cột C (FOLDER) chứa `ten_thu_muc`. Trả (dong, stt) hoặc (None, None)."""
    rows = s.values().get(spreadsheetId=SHEET_ID,
                          range=f"'{tab}'!A2:{COT_FOLDER}400").execute().get("values", [])
    hit = []
    for i, r in enumerate(rows, start=2):
        folder = _chuan(r[2] if len(r) > 2 else "")
        if folder and folder.rstrip("/").endswith("/" + _chuan(ten_thu_muc)):
            hit.append((i, (r[0] if r else "").strip()))
    if len(hit) > 1:
        raise SystemExit(f"✗ có {len(hit)} dòng cùng trỏ tới '{ten_thu_muc}' trong tab {tab} "
                         f"(dòng {[h[0] for h in hit]}) → dọn trùng trước khi ghi")
    return hit[0] if hit else (None, None)


def ghi_tu_ep(ep_dir, tab=None, stt=None, ghi_de=False, thu=False):
    """Ghi link video gốc của tập `ep_dir` vào cột T. Trả dict {ok, ly_do, url, tab, dong}.

    Không ném SystemExit khi gọi từ pipeline (dùng `thu=False`, đọc `ok`/`ly_do`). Lỗi cấu hình
    (thiếu credentials, tab không có cột VIDEO GỐC) trả ok=False kèm lý do để nơi gọi tự in.
    """
    ep_dir = Path(ep_dir)
    url, info = doc_link(ep_dir)
    if not url:
        return {"ok": False, "ly_do": info, "url": None, "tab": tab, "dong": None}

    if tab is None:
        prof = lane_theo_slug_dir(ep_dir.parent.relative_to(ROOT) if ep_dir.is_absolute() else ep_dir.parent)
        if not prof:
            return {"ok": False, "ly_do": f"không profile nào khai slug_dir = {ep_dir.parent}",
                    "url": url, "tab": None, "dong": None}
        tab = tab_cua_lane(prof)
        if not tab:
            return {"ok": False, "ly_do": f"profile '{prof.get('id')}' không khai publish.sheet_tab",
                    "url": url, "tab": None, "dong": None}

    try:
        s = svc(doc_thoi=True)
        tab = _tab_that_su(s, tab)
        hd = s.values().get(spreadsheetId=SHEET_ID,
                            range=f"'{tab}'!{COT}1").execute().get("values", [[""]])
        ten_cot = (hd[0][0] if hd and hd[0] else "").strip().upper()
        # Cột T1 trống = lane chưa dán nhãn cột (vd Lane F) — vẫn ghi được, chỉ cảnh báo. Có nhãn KHÁC
        # 'VIDEO GỐC' = cột đã bị đổi chỗ → DỪNG (ghi tiếp là đè nhầm cột của người khác).
        if ten_cot and ten_cot != TIEU_DE_COT:
            return {"ok": False, "ly_do": f"cột {COT}1 của tab {tab} đang là "
                                          f"'{ten_cot}', không phải '{TIEU_DE_COT}' → cột đã đổi chỗ",
                    "url": url, "tab": tab, "dong": None}
        canh_bao = "" if ten_cot else f" (lưu ý: {COT}1 của tab {tab} đang TRỐNG nhãn)"

        if stt is not None:
            dong = int(stt) + 1
        else:
            dong, _ = tim_dong(s, tab, ep_dir.name)
            if not dong:
                return {"ok": False, "ly_do": f"không dòng nào ở tab {tab} có FOLDER (cột C) chứa "
                                              f"'{ep_dir.name}'", "url": url, "tab": tab, "dong": None}

        cur = s.values().get(spreadsheetId=SHEET_ID,
                             range=f"'{tab}'!A{dong}:{COT}{dong}").execute().get("values", [[]])
        hang = cur[0] if cur else []
        stt_that = (hang[0] if hang else "").strip()
        if not stt_that.isdigit():
            return {"ok": False, "ly_do": f"dòng {dong} của tab {tab} không có STT (cột A trống) "
                                          f"→ trang tính đã xê dịch", "url": url, "tab": tab, "dong": dong}
        cu = (hang[19] if len(hang) > 19 else "").strip()
        if cu and not ghi_de:
            if cu.strip() == url.strip():
                return {"ok": True, "ly_do": f"ô {COT}{dong} đã đúng link này{canh_bao}", "url": url,
                        "tab": tab, "dong": dong}
            return {"ok": False, "ly_do": f"ô {COT}{dong} ĐÃ CÓ '{cu}' khác link mới '{url}' "
                                          f"→ thêm --ghi-de nếu muốn đè", "url": url,
                    "tab": tab, "dong": dong}
        if thu:
            return {"ok": True, "ly_do": f"(--thu) sẽ ghi {COT}{dong} = {url}{canh_bao}", "url": url,
                    "tab": tab, "dong": dong}

        svc(doc_thoi=False).values().update(
            spreadsheetId=SHEET_ID, range=f"'{tab}'!{COT}{dong}",
            valueInputOption="USER_ENTERED", body={"values": [[url]]}).execute()
        return {"ok": True, "ly_do": f"✓ ghi {tab}!{COT}{dong} = {url}{canh_bao}", "url": url,
                "tab": tab, "dong": dong}
    except SystemExit as e:
        return {"ok": False, "ly_do": str(e), "url": url, "tab": tab, "dong": None}
    except Exception as e:
        return {"ok": False, "ly_do": f"{type(e).__name__}: {e}", "url": url, "tab": tab, "dong": None}


def quet_lane(pid, thu=False, ghi_de=False):
    """Backfill cả lane: mọi tập có `video_goc.json` mà ô T còn TRỐNG → điền link.

    Đọc trang tính ĐÚNG 1 LẦN (A2:T400) rồi ghi 1 lệnh `batchUpdate` → không ăn 429 khi lane
    có 20+ tập. KHÔNG đè ô đã có link khác (báo ra để anh quyết), trừ khi `ghi_de=True`.
    Trả dict {ok, tab, ghi, da_co, khac, khong_link, chi_tiet}.
    """
    import profiles
    prof = profiles.load(pid)
    sd = ROOT / prof["slug_dir"]
    tab = tab_cua_lane(prof)
    ket = {"ok": False, "tab": tab, "ghi": [], "da_co": [], "khac": [], "khong_link": [], "chi_tiet": ""}
    if not tab:
        ket["chi_tiet"] = f"profile '{pid}' không khai publish.sheet_tab"
        return ket
    eps = sorted(d for d in sd.glob("ep*") if d.is_dir() and (d / "video_goc.json").exists())
    if not eps:
        ket["ok"] = True
        ket["chi_tiet"] = f"{sd} không có tập nào kèm video_goc.json"
        return ket
    try:
        s = svc(doc_thoi=True)
        tab = _tab_that_su(s, tab)
        ket["tab"] = tab
        hd = s.values().get(spreadsheetId=SHEET_ID,
                            range=f"'{tab}'!{COT}1").execute().get("values", [[""]])
        ten_cot = (hd[0][0] if hd and hd[0] else "").strip().upper()
        if ten_cot and ten_cot != TIEU_DE_COT:
            ket["chi_tiet"] = f"cột {COT}1 của tab {tab} đang là '{ten_cot}', không phải '{TIEU_DE_COT}'"
            return ket
        rows = s.values().get(spreadsheetId=SHEET_ID,
                              range=f"'{tab}'!A2:{COT}400").execute().get("values", [])
        o = {}
        for i, r in enumerate(rows, start=2):
            f = _chuan(r[2] if len(r) > 2 else "").rstrip("/")
            if f:
                o[f.split("/")[-1]] = (i, (r[19] if len(r) > 19 else "").strip())

        can_ghi, lenh = [], []
        for d in eps:
            url, info = doc_link(d)
            if not url:
                ket["khong_link"].append(f"{d.name}: {info}")
                continue
            if d.name.lower() not in o:
                ket["khac"].append(f"{d.name}: KHÔNG có dòng nào trong tab {tab} (cột C)")
                continue
            dong, cu = o[d.name.lower()]
            if cu and cu.strip() == url.strip():
                ket["da_co"].append(d.name)
            elif cu and not ghi_de:
                ket["khac"].append(f"{d.name}: ô T{dong} đã có '{cu}' (khác link mới)")
            else:
                can_ghi.append(d.name)
                lenh.append({"range": f"'{tab}'!{COT}{dong}", "values": [[url]]})

        if can_ghi and not thu:
            # PHẢI service quyền GHI: service ở trên là `readonly` (đọc), dùng lại sẽ 403
            # ACCESS_TOKEN_SCOPE_INSUFFICIENT ở `values:batchUpdate`.
            svc(doc_thoi=False).values().batchUpdate(
                spreadsheetId=SHEET_ID,
                body={"valueInputOption": "USER_ENTERED", "data": lenh}).execute()
        ket["ghi"] = can_ghi
        ket["ok"] = True
        ket["chi_tiet"] = (f"tab {tab}: {len(can_ghi)} tập "
                           f"{'(sẽ)' if thu else 'ĐÃ'} ghi cột {COT}, {len(ket['da_co'])} đã có sẵn, "
                           f"{len(ket['khac'])} cần xem tay, {len(ket['khong_link'])} không có video gốc")
    except SystemExit as e:
        ket["chi_tiet"] = str(e)
    except Exception as e:
        ket["chi_tiet"] = f"{type(e).__name__}: {e}"
    return ket


def main():
    ap = argparse.ArgumentParser(description="Ghi link video gốc của tập vào cột T (VIDEO GỐC)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--tap", help="thư mục tập (có video_goc.json)")
    g.add_argument("--profile", help="mã lane — dùng với --stt")
    g.add_argument("--tab", help="tên tab trang tính — dùng với --stt")
    g.add_argument("--lane", help="BACKFILL cả lane: mọi tập có video_goc.json mà ô T còn trống")
    ap.add_argument("--stt", type=int, help="số tập (cột A)")
    ap.add_argument("--ghi-de", action="store_true", help="cho phép đè ô T đã có sẵn")
    ap.add_argument("--thu", action="store_true", help="chỉ kiểm và in ra, KHÔNG ghi")
    a = ap.parse_args()

    if a.lane:
        r = quet_lane(a.lane, thu=a.thu, ghi_de=a.ghi_de)
        print(f"lane {a.lane} · tab {r['tab']}")
        print(f"  {r['chi_tiet']}")
        for k, nhan in (("ghi", "sẽ ghi" if a.thu else "đã ghi"), ("khac", "CẦN XEM TAY"),
                        ("khong_link", "KHÔNG có video gốc")):
            if r[k]:
                print(f"  {nhan} ({len(r[k])}):")
                for x in r[k]:
                    print(f"    - {x}")
        return 0 if r["ok"] else 2

    if a.tap:
        ep = Path(a.tap)
    else:
        import profiles
        prof = profiles.load(a.profile) if a.profile else None
        if prof is None:
            raise SystemExit("✗ --tab cần đi kèm --stt và phải dùng --tap (không suy được thư mục tập)")
        if a.stt is None:
            raise SystemExit("✗ --profile cần --stt")
        mau = prof.get("folder_pattern") or "ep{nn:02d}-*"
        ds = sorted(p for p in (ROOT / prof["slug_dir"]).glob(mau.format(nn=a.stt)) if p.is_dir())
        if len(ds) != 1:
            raise SystemExit(f"✗ cần đúng 1 thư mục {mau.format(nn=a.stt)} trong "
                             f"{ROOT / prof['slug_dir']}, thấy {len(ds)}")
        ep = ds[0]

    r = ghi_tu_ep(ep, tab=a.tab, stt=a.stt, ghi_de=a.ghi_de, thu=a.thu)
    print(f"tập: {ep}")
    print(f"  {r['ly_do']}")
    return 0 if r["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
