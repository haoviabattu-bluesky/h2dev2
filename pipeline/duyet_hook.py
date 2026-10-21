# -*- coding: utf-8 -*-
r"""duyet_hook.py — chặng "ANH DUYỆT CLIP HOOK" chen giữa hình hook (máy 1) và giao máy 2 (anh chốt 2026-10-02).

Máy 1 làm xong ảnh + clip Grok hook → dựng BẢN XEM THỬ hook đầy đủ (clip + giọng ai33 theo vai + nhạc nền + phụ đề
Nhật/Việt từng câu) bằng `tools\hook_lane_g\xem_thu_hook_giong.py` → anh xem → duyệt rồi mới giao máy 2.

Luồng:
  `--gui`   : kiểm bản xem thử có và MỚI HƠN hook (hook_locked.txt, hook_timeline.json, clip\) → ghi duyet_hook.json
              state=cho + dấu vân hook → cột D = "Chờ duyệt hook" + dòng 2 = đường dẫn video. DỪNG lượt.
  anh xem   : được → đổi dòng đầu ô D = "Đã duyệt hook", báo tab "anh duyệt hook <lane> <tập>".
              chưa được → báo tab chỗ cần sửa (tab sửa, dựng lại bản xem thử, `--gui` lại).
  `--nhan`  : kiểm D = "Đã duyệt hook" (hoặc `--force` khi anh duyệt ngay trong chat) + hook không đổi sau khi gửi
              → state=duyet.
  `cong()`  : dong_goi_may2 --job gọi trước khi đóng gói — chưa duyệt / hook đổi sau khi duyệt → DỪNG.
              Job đã giao trước đây (có _BANGIAO.txt) = đóng gói SỬA → chỉ cảnh báo.

Field: áp cho lane bật soát máy 3 (`script.review_may3`, vắng = BẬT) và bật hook (`script.hook.enabled`).

  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\duyet_hook.py --gui  --profile <lane> --slug <tập>
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\duyet_hook.py --nhan --profile <lane> --slug <tập> [--force]
"""
import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import profiles      # noqa: E402
import review_may3   # noqa: E402
import tong_hop      # noqa: E402

MARKER = "duyet_hook.json"                       # trong thư mục tập
VIDEO = "XEM_THU_hook_giong_phude_VI.mp4"        # tên do xem_thu_hook_giong.py đặt
TRANG_THAI_CHO = "Chờ duyệt hook"
TRANG_THAI_DUYET = "Đã duyệt hook"
TOOL_XEM = HERE.parent / "tools" / "hook_lane_g" / "xem_thu_hook_giong.py"


def ap_dung(prof):
    hook = ((prof.get("script") or {}).get("hook") or {})
    return review_may3.is_enabled(prof) and bool(hook.get("enabled"))


def _file_hook(d):
    hd = Path(d) / "hook"
    fs = [hd / "hook_locked.txt", hd / "hook_timeline.json", hd / "phu_de_vi.json", Path(d) / "vai.txt"]
    fs += sorted((hd / "clip").glob("*")) if (hd / "clip").is_dir() else []
    return [f for f in fs if f.is_file()]


def dau_van(d):
    """Dấu vân của hook: nội dung lời hook + timeline + phụ đề + vai + từng clip. Đổi 1 thứ = phải duyệt lại."""
    h = hashlib.sha256()
    for f in _file_hook(d):
        h.update(f.name.encode("utf-8"))
        h.update(hashlib.sha256(f.read_bytes()).digest())
    return h.hexdigest()


def doc_marker(d):
    p = Path(d) / MARKER
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except Exception:
        return {}


def ghi_marker(d, **kv):
    m = doc_marker(d)
    m.update(kv, at=_dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
    (Path(d) / MARKER).write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


def gui(prof, slug, dry=False):
    d = review_may3.thu_muc_tap(prof, slug)
    review_may3.cong(prof, d, "duyet_hook --gui")
    # 2026-10-10 (anh chốt): nhân vật chính phải có THẺ TÊN ĐỘNG (sửa 14/10: lời hook ĐƯỢC đọc tên-tuổi song song)
    import the_ten_hook
    the_ten_hook.cong(prof, d, "duyet_hook --gui")
    # 2026-10-10 (anh chốt): đạo cụ mang chữ trọng tâm (giấy tờ/biển/màn hình) phải được chèn chữ bằng code hoặc ghi bo_qua
    import chu_dao_cu
    chu_dao_cu.cong(prof, d, "duyet_hook --gui")
    v = d / VIDEO
    if not v.exists():
        raise SystemExit(f"✗ chưa có bản xem thử {v}\n  → py -3.13 -X utf8 {TOOL_XEM} --profile {prof['id']} --hook {d / 'hook'}")
    cu = [f.name for f in _file_hook(d) if f.stat().st_mtime > v.stat().st_mtime]
    cu += [f.name for f in (d / "hook" / "the_ten").glob("*.webm") if f.stat().st_mtime > v.stat().st_mtime]
    if cu:
        raise SystemExit(f"✗ bản xem thử CŨ hơn {cu} → dựng lại: py -3.13 -X utf8 {TOOL_XEM} --profile {prof['id']} --hook {d / 'hook'}")
    o_d = f"{TRANG_THAI_CHO}\n{v}"
    if dry:
        print(f"[dry] sẽ ghi marker state=cho + ô D = {o_d!r}")
        return
    ghi_marker(d, state="cho", van=dau_van(d), video=str(v))
    try:
        dg, tab, dong = review_may3._sheet(prof, slug)
        o = review_may3._doc_d(dg, tab, dong)
        dau = review_may3.dong_dau(o)
        if dau in ("", review_may3.TRANG_THAI_DA_SUA, review_may3.TRANG_THAI_DANG_HOOK, TRANG_THAI_CHO, TRANG_THAI_DUYET):
            review_may3._ghi_d(dg, tab, dong, o_d)
        else:
            print(f"  ⚠️ ô {tab}!D{dong} đang '{o}' → KHÔNG đè, anh xem lại")
    except SystemExit as e:
        print(f"  ⚠️ chưa ghi được cột D: {e}")
    tong_hop.ghi(prof, slug, tong_hop.CHO_HOOK)
    print(f"⏸ DỪNG — chờ anh duyệt clip hook: {v}\n"
          f"  Anh duyệt → ô D = '{TRANG_THAI_DUYET}' → tab: py -3.13 -X utf8 {HERE / 'duyet_hook.py'} --nhan --profile {prof['id']} --slug {slug}\n"
          f"  rồi: py -3.13 -X utf8 {HERE / 'dong_goi_may2.py'} --job {prof['id']} {slug}")


def nhan(prof, slug, force=False):
    d = review_may3.thu_muc_tap(prof, slug)
    m = doc_marker(d)
    if m.get("state") not in ("cho", "duyet"):
        raise SystemExit(f"✗ tập {slug} chưa gửi duyệt hook (chạy --gui trước)")
    if m.get("van") != dau_van(d):
        raise SystemExit("✗ hook đã đổi SAU khi gửi anh xem (lời/clip/phụ đề/vai) → dựng lại bản xem thử rồi --gui lại")
    if not force:
        dg, tab, dong = review_may3._sheet(prof, slug)
        dau = review_may3.dong_dau(review_may3._doc_d(dg, tab, dong))
        if dau != TRANG_THAI_DUYET:
            raise SystemExit(f"✗ ô {tab}!D{dong} = '{dau}', chưa phải '{TRANG_THAI_DUYET}' "
                             f"(anh duyệt trong chat thì chạy lại với --force)")
    else:
        # anh duyệt trong chat: ô D còn "Chờ duyệt hook" thì dong_goi_may2 không dám đè → đổi luôn ở đây
        try:
            dg, tab, dong = review_may3._sheet(prof, slug)
            if review_may3.dong_dau(review_may3._doc_d(dg, tab, dong)) == TRANG_THAI_CHO:
                review_may3._ghi_d(dg, tab, dong, TRANG_THAI_DUYET)
                print(f"  ✓ ô {tab}!D{dong} = {TRANG_THAI_DUYET}")
        except SystemExit as e:
            print(f"  ⚠️ chưa ghi được cột D: {e}")
    ghi_marker(d, state="duyet", nguon="force" if force else "cot_D")
    print(f"  ✓ {MARKER} = duyet → giao máy 2: py -3.13 -X utf8 {HERE / 'dong_goi_may2.py'} --job {prof['id']} {slug}")


def cong(prof, d, buoc, dst=None):
    """Gọi trước khi đóng gói giao máy 2. Chưa duyệt / hook đổi sau khi duyệt → DỪNG."""
    if not ap_dung(prof):
        return
    d = Path(d)
    m = doc_marker(d)
    if m.get("state") == "duyet" and m.get("van") == dau_van(d):
        return
    if dst and (Path(dst) / "_BANGIAO.txt").exists():
        print(f"  ⚠ {buoc}: hook chưa có duyệt khớp bản hiện tại, nhưng job đã giao trước đây → đóng gói SỬA, cho qua")
        return
    ly_do = "đã đổi sau khi anh duyệt" if m.get("state") == "duyet" else f"chưa duyệt (đang '{m.get('state') or 'chua'}')"
    raise SystemExit(f"✗ {buoc}: clip hook {ly_do} → dựng bản xem thử ({TOOL_XEM}) → "
                     f"py -3.13 -X utf8 {HERE / 'duyet_hook.py'} --gui --profile {prof['id']} --slug {d.name} → chờ anh duyệt → --nhan")


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--slug", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--gui", action="store_true")
    g.add_argument("--nhan", action="store_true")
    ap.add_argument("--force", action="store_true", help="--nhan: anh duyệt trong chat, không cần ô D")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args(argv)
    prof = profiles.load(a.profile)
    if a.gui:
        gui(prof, a.slug, dry=a.dry)
    else:
        nhan(prof, a.slug, force=a.force)


if __name__ == "__main__":
    main()
