# -*- coding: utf-8 -*-
r"""so_lieu_dong.py — sinh + nghiệm thu `so_lieu_dong.json` (số liệu động hiện TRÊN ảnh nền của tập).

Anh chốt 2026-10-06 (dự án E:\CLAUDE\MOTION GRAPHICS, mẫu Lane L ep03): ở câu kịch bản có số liệu thật,
máy 2 thay hộp chữ bằng con số đếm lên đặt thẳng trên ảnh gpti2/Flow của chính câu đó (màn hình laptop,
đồ thị, tờ giấy, ô trống). Cách dựng: skill `motion_graphics` (bản cho máy 2 ở
`FlowHandoff_local\shared\motion_graphics\HUONG_DAN_MAY2.md`).

CHIA VIỆC (anh chốt 2026-10-07: CHUYỂN HẲN SANG MÁY 2 — trước đây máy 1 duyệt tay ở bước 1, tập làm tập
không nên QC không đều; nay mọi tập của lane bật đi đúng một đường ở máy 2, sau khi đã có final.mp4):
  · MÁY rút phần TẤT ĐỊNH — số nào trong `SỐ ĐƯỢC PHÉP` của series_ctx.txt thật sự xuất hiện trong
    script.txt, nằm ở câu nào, đơn vị gì, nguồn [Dn] nào chứa nó.
  · CLAUDE MÁY 2 duyệt theo luật cố định ở `shared\motion_graphics\HUONG_DAN_MAY2.md` §2 bước 0 — bỏ số
    không đáng hiện, điền `nhan`/`nguon`, đặt `"trang_thai": "da_duyet"`, `--kiem` phải PASS.
  · Máy 1 KHÔNG chạy file này nữa; dong_goi_may2 không chặn, chỉ ghi mục SỐ LIỆU ĐỘNG vào _BANGIAO.txt.

Bật theo lane bằng field profile `mg.so_lieu_dong: true` (KHÔNG rẽ nhánh theo profile_id).

Dùng (máy 2, đứng ở shared\buoc2_3_tool\pipeline):
  py -3.13 -X utf8 so_lieu_dong.py --profile shakai_no_naze --slug ep03-...           # sinh bản nháp
  py -3.13 -X utf8 so_lieu_dong.py --profile shakai_no_naze --slug ep03-... --kiem    # nghiệm thu
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import profiles  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TEN = "so_lieu_dong.json"
DA_DUYET = "da_duyet"
NHAP = "nhap_may"
DON_VI = ["万人", "万円", "%", "人", "倍", "件", "社", "年", "歳", "円", "割", "位", "時間", "日", "回", "代"]


def bat(prof):
    return bool((prof.get("mg") or {}).get("so_lieu_dong"))


def _so_duoc_phep(ctx):
    m = re.search(r"SỐ ĐƯỢC PHÉP:\s*(.+)", ctx)
    return [x.strip() for x in m.group(1).split("·") if x.strip()] if m else []


def _cau(script):
    """Tách câu theo 。！？ và giữ cả phần trong 「」 — đủ để tìm `cau_chua` trong voice.srt (srt cắt theo câu)."""
    return [c.strip() for c in re.split(r"(?<=[。！？])", script.replace("\n", "")) if c.strip()]


def _cac_nguon(ctx):
    """[(Dn, tên tổ chức, dòng)] — dòng bắt đầu bằng 同調査/同社 thì mượn tên của [D] liền trước."""
    ra, truoc = [], ""
    for dong in ctx.splitlines():
        m = re.match(r"\[(D\d+)\]\s*(.*)", dong)
        if not m:
            continue
        than = m.group(2)
        ten = "" if than.startswith(("同調査", "同社", "同じ調査")) else re.split(r"[「『（(、]|の\d|の調査|が", than)[0].strip()
        ten = ten or truoc
        truoc = ten
        ra.append((m.group(1), ten, dong))
    return ra


def _nguon(nguon, so, ngu_canh):
    """Nguồn = tổ chức được nêu GẦN con số nhất trong câu/3 câu trước (kịch bản luôn nói ai khảo sát);
    cùng tổ chức thì ưu tiên dòng [D] chứa đúng con số. Không ai được nêu → [D] đầu tiên chứa con số."""
    ung = [(ngu_canh.rfind(ten[:6]), so in dong, dn, ten) for dn, ten, dong in nguon if ten and ten[:6] in ngu_canh]
    if ung:
        _, _, dn, ten = max(ung)
        return dn, ten
    for dn, ten, dong in nguon:
        if so in dong:
            return dn, ten
    return "", ""


def _don_vi(so):
    if not re.fullmatch(r"[\d.,]+\D{0,3}", so):     # vd 5社に1社 → giữ nguyên cụm, máy 2 hiện như chữ số
        return so, ""
    for dv in DON_VI:
        if so.endswith(dv):
            return so[: -len(dv)], dv
    return so, ""


def _cat_quanh(cau, so, rong=20):
    """Đoạn ≤ ~45 ký tự quanh con số, cắt ở ranh giới dấu câu nếu có (để không cắt ngang số khác)."""
    if len(cau) <= 45:
        return cau
    i = cau.find(so)
    a, b = max(0, i - rong), min(len(cau), i + len(so) + rong)
    while b < len(cau) and re.match(r"[\d.,%]", cau[b]):
        b += 1
    while a > 0 and re.match(r"[\d.,]", cau[a - 1]):
        a -= 1
    return cau[a:b]


def sinh(slug, profile_id, ghi_de=False):
    prof = profiles.load(profile_id)
    tap = ROOT / prof["slug_dir"] / slug
    out = tap / TEN
    if out.exists() and not ghi_de:
        raise SystemExit(f"✗ {out} đã có (có thể đã sửa tay) — thêm --ghi-de nếu chắc muốn viết lại")
    ctx = (tap / "series_ctx.txt").read_text(encoding="utf-8")
    script = (tap / "script.txt").read_text(encoding="utf-8")
    cau = _cau(script)
    nguon = _cac_nguon(ctx)
    ds, da_co = [], set()
    for so in _so_duoc_phep(ctx):
        for k, c in enumerate(cau):
            if so in c and (so, k) not in da_co:
                da_co.add((so, k))
                gia_tri, dv = _don_vi(so)
                dn, ten = _nguon(nguon, so, "".join(cau[max(0, k - 3): k + 1]))
                ds.append({"cau_chua": _cat_quanh(c, so), "so": gia_tri, "don_vi": dv,
                           "loai": "nam" if dv == "年" else "so", "nhan": "", "nguon": ten, "dn": dn,
                           "goi_y_cho": "", "_k": k})
    ds.sort(key=lambda x: (x["_k"], cau[x["_k"]].find(x["so"])))
    for x in ds:
        del x["_k"]
    data = {"_doc": "Máy 2 duyệt theo shared\\motion_graphics\\HUONG_DAN_MAY2.md §2 bước 0: xoá mục không đáng hiện, "
                    "điền nhan, sửa nguon, đặt trang_thai=da_duyet rồi chạy --kiem.",
            "tap": slug, "trang_thai": NHAP, "so": ds}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    khong_thay = [s for s in _so_duoc_phep(ctx) if not any(s in c for c in cau)]
    return out, len(ds), khong_thay


def kiem(tap: Path):
    loi = []
    f = tap / TEN
    if not f.exists():
        return [f"thiếu {TEN} (chạy so_lieu_dong.py --profile ... --slug ... rồi duyệt)"]
    d = json.loads(f.read_text(encoding="utf-8"))
    if d.get("trang_thai") != DA_DUYET:
        loi.append(f"trang_thai = {d.get('trang_thai')!r}, chưa '{DA_DUYET}' (chưa duyệt bản nháp máy — HUONG_DAN_MAY2.md §2 bước 0)")
    script = (tap / "script.txt").read_text(encoding="utf-8") if (tap / "script.txt").exists() else ""
    flat = script.replace("\n", "")
    for i, x in enumerate(d.get("so") or [], 1):
        if x.get("cau_chua") and x["cau_chua"] not in flat:
            loi.append(f"mục {i}: cau_chua không có trong script.txt → máy 2 không tìm được câu: {x['cau_chua']}")
        if len(x.get("nhan") or "") > 6:
            loi.append(f"mục {i}: nhan quá dài ({x['nhan']}) — chỉ số + nhãn ngắn, anh chốt bỏ chữ")
    return loi


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sinh/nghiệm thu so_lieu_dong.json (số liệu động trên ảnh)")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--ghi-de", action="store_true")
    ap.add_argument("--kiem", action="store_true")
    a = ap.parse_args(argv)
    prof = profiles.load(a.profile)
    tap = ROOT / prof["slug_dir"] / a.slug
    if a.kiem:
        loi = kiem(tap)
        for x in loi:
            print("  ✗", x)
        print("=== SO_LIEU_DONG:", "FAIL" if loi else "PASS")
        return 1 if loi else 0
    out, n, khong_thay = sinh(a.slug, a.profile, ghi_de=a.ghi_de)
    print(f"=== {out}  ({n} mục, trang_thai={NHAP})")
    if khong_thay:
        print("  ⚠ số được phép nhưng không thấy nguyên văn trong script (có thể viết bằng chữ Hán):", " · ".join(khong_thay))
    print("→ Duyệt theo shared\\motion_graphics\\HUONG_DAN_MAY2.md §2 bước 0, đặt trang_thai=da_duyet, rồi --kiem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
