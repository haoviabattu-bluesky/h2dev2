# -*- coding: utf-8 -*-
"""sheet_tab.py — tên tab trang tính của từng lane. MỘT nguồn chân lý: `profile.publish.sheet_tab`.

QUY ƯỚC TÊN TAB (anh chốt 2026-09-24): `{Lane}-{tên kênh}`, vd
    A-shinya_shiryoshitsu · Satori-Lopezzapa68 · E-70dai-kenko · F-teinengo-real · G-teinengo-tanoshimi
`{tên kênh}` = tên thư mục giao hàng `CHANEL\\<kênh>` / handle, KHÔNG phải mã lane.

Tên tab ≠ tên thư mục kênh ≠ mã lane — ba thứ khác nhau, đừng suy cái này từ cái kia:
    mã lane      = profile `id`                    (toshi-densetsu-jp)
    thư mục kênh = `publish.upload_channel`        (shinya_shiryoshitsu → E:\\CLAUDE\\YOUTUBE\\CHANEL\\...)
    tên tab      = `publish.sheet_tab`             (A-shinya_shiryoshitsu)

`tab_that(ten)` nhận BẤT KỲ tên nào trong 3 thứ trên (kể cả tên tab CŨ trước khi đổi, tức tên bỏ
tiền tố `X-`) và trả tên tab THẬT — để lệnh cũ trong tài liệu (`--tab shinya_shiryoshitsu`) vẫn chạy
đúng thay vì gọi Sheets API với tên tab không còn tồn tại.
"""
import json
from pathlib import Path

PROFILES = Path(__file__).resolve().parent.parent / "profiles" / "profiles"


def _profiles():
    for f in sorted(PROFILES.glob("*.json")):
        if f.name.startswith("_") or ".bak" in f.name:
            continue
        try:
            yield json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue


def _ten_goi(p):
    """Mọi tên dùng để gọi lane này: tab thật, tab cũ (bỏ tiền tố), thư mục kênh, mã lane."""
    pub = p.get("publish") or {}
    tab = pub.get("sheet_tab") or ""
    ten = {tab, pub.get("upload_channel") or "", p.get("id") or ""}
    if "-" in tab:
        ten.add(tab.split("-", 1)[1])
    return {t for t in ten if t}


def lane_theo_tab(ten):
    """Profile của lane ứng với `ten`. Chỉ xét profile có khai `publish` (upload_channel/sheet_tab).
    Khớp >1 profile → dừng (không đoán)."""
    ten = (ten or "").strip()
    hit = [p for p in _profiles()
           if ((p.get("publish") or {}).get("sheet_tab") or (p.get("publish") or {}).get("upload_channel"))
           and ten in _ten_goi(p)]
    if len(hit) > 1:
        raise SystemExit(f"✗ tên '{ten}' khớp {len(hit)} lane: {[p.get('id') for p in hit]} — dùng tên tab đầy đủ")
    return hit[0] if hit else None


def tab_that(ten):
    """Tên tab thật trên trang tính. Không tra được lane thì trả nguyên `ten` (tab không thuộc lane nào)."""
    p = lane_theo_tab(ten)
    if not p:
        return ten
    pub = p.get("publish") or {}
    return pub.get("sheet_tab") or pub.get("upload_channel") or ten


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for p in _profiles():
        pub = p.get("publish") or {}
        if pub.get("sheet_tab") or pub.get("upload_channel"):
            print(f"{p['id']:22} tab={pub.get('sheet_tab') or '(chưa khai → ' + str(pub.get('upload_channel')) + ')'}"
                  f"  kênh={pub.get('upload_channel')}")
