# -*- coding: utf-8 -*-
"""qc_numbers.py — CỔNG KIỂM SỐ HỌC cho kịch bản (tầng máy móc, miễn phí, tất định).

Vì sao có file này: khán giả ngách kể tài liệu (都市伝説 / vũ trụ / lịch sử) SOI SỐ RẤT KỸ.
Comment 44👍 dưới video của kênh mẫu bắt đúng một lỗi nhân:
    「東京ドームの60倍が日本列島より大きい？200mの60倍は12kmだろが！」
Một phép tính sai xoá sạch cái uy "đã nghiên cứu kỹ" mà cả video xây lên — và nó nằm ở comment
nổi nhất, ai vào cũng đọc. Vì vậy mọi phép tính / đơn vị / quy đổi phải qua cổng này TRƯỚC khi
tiêu tiền giọng + hình.

Nguyên tắc: **chỉ báo khi CHẮC**. Chỉ kiểm những phép mà chính kịch bản đã viết đủ hai vế
(có số vào, có số ra). Báo động giả làm người ta tắt cổng, mà tắt cổng thì mất luôn tác dụng.
Phần cần kiến thức đời thực (con số này có hợp lý không) là việc của tầng LLM trong qc_script.py.

Dùng độc lập:
  py -3.13 qc_numbers.py --script <file>
"""
import re

_SO_KANJI = {"〇": "0", "零": "0", "一": "1", "二": "2", "三": "3", "四": "4", "五": "5",
             "六": "6", "七": "7", "八": "8", "九": "9"}
_DON_VI = {"万": 10 ** 4, "億": 10 ** 8, "兆": 10 ** 12}

# Thước so sánh hay bị dùng, kèm giá trị THẬT. Sai số cho phép rộng (±35%) vì mỗi nguồn viết một
# kiểu; mục tiêu là bắt LỆCH BẬC (10×, 100×), không bắt lỗi làm tròn.
HANG_SO = {
    "1 năm ánh sáng": (9.46e12, "km", ["1光年", "一光年"]),
    "chiều cao Phú Sĩ": (3776.0, "m", ["富士山の高さ"]),
    "đỉnh Everest": (8849.0, "m", ["エベレストの高さ"]),
    "đường kính Trái Đất": (12742.0, "km", ["地球の直径"]),
    "khoảng cách tới Mặt Trăng": (384400.0, "km", ["月までの距離", "地球から月まで"]),
    "khoảng cách tới Mặt Trời": (1.496e8, "km", ["太陽までの距離", "地球から太陽まで"]),
}

# Đơn vị độ dài → mét
DV_DAI = {"ミリ": 1e-3, "センチ": 1e-2, "メートル": 1.0, "キロ": 1e3, "km": 1e3, "m": 1.0}

_NUM = r"[一二三四五六七八九〇\d,\.兆億万]+"


def to_num(txt):
    """'9兆5000億' · '38万' · '12,742' · '3.5' · '三' → float. None nếu không đọc được."""
    t = str(txt).replace(",", "").replace("，", "").strip()
    if not t:
        return None
    for k, v in _SO_KANJI.items():
        t = t.replace(k, v)
    tong, con = 0.0, t
    for dv in ("兆", "億", "万"):
        if dv in con:
            trai, _, con = con.partition(dv)
            try:
                tong += float(trai or 1) * _DON_VI[dv]
            except ValueError:
                return None
    if con:
        try:
            tong += float(con)
        except ValueError:
            return tong if tong else None
    return tong


def lech(a, b, tol=0.02):
    if a is None or b is None:
        return False
    m = max(abs(a), abs(b))
    return m > 0 and abs(a - b) / m > tol


def khoang_nam(body):
    """「1947年から1969年までの22年間」→ 1969-1947 = 22."""
    out = []
    for m in re.finditer(r"(\d{3,4})\s*年から\s*(\d{3,4})\s*年(?:まで)?の\s*(" + _NUM + r")\s*年間", body):
        a, b, c = int(m.group(1)), int(m.group(2)), to_num(m.group(3))
        if c is None or b <= a:
            continue
        if abs((b - a) - c) > 1:
            out.append({"kind": "so_hoc_khoang_nam", "sev": "cao",
                        "msg": f"「{m.group(0)}」→ {b}−{a} = {b - a} năm, kịch bản ghi {c:g}"})
    return out


def khoang_thang(body):
    """「2月から11月までの9か月間」→ 9 tháng."""
    out = []
    for m in re.finditer(r"(\d{1,2})\s*月から\s*(\d{1,2})\s*月(?:まで)?の\s*(" + _NUM +
                         r")\s*(?:か月|ヶ月|カ月)間", body):
        a, b, c = int(m.group(1)), int(m.group(2)), to_num(m.group(3))
        if c is None or not (1 <= a <= 12 and 1 <= b <= 12):
            continue
        dung = (b - a) % 12
        if abs(dung - c) > 1:
            out.append({"kind": "so_hoc_khoang_thang", "sev": "vua",
                        "msg": f"「{m.group(0)}」→ {a}月→{b}月 là {dung} tháng, kịch bản ghi {c:g}"})
    return out


def tuoi_theo_nam_sinh(body):
    """「1930年生まれ」… 「1975年、45歳」→ 45 phải khớp 1975−1930."""
    out = []
    sinh = {int(m.group(1)) for m in re.finditer(r"(\d{4})\s*年\s*(?:に)?生まれ", body)}
    if len(sinh) != 1:                      # nhiều mốc sinh ⇒ nhiều nhân vật, không kết luận được
        return out
    y0 = sinh.pop()
    # (?!\s*(?:に)?生まれ): bỏ qua chính mốc SINH. Không loại thì regex bám vào "1930年…50歳",
    # tính ra 0 tuổi rồi im lặng cho qua — cặp năm-tuổi thật sự cần kiểm nằm ngay sau đó.
    for m in re.finditer(r"(\d{4})\s*年(?!\s*(?:に)?生まれ)[^。]{0,40}?(\d{1,3})\s*歳", body):
        y, tuoi = int(m.group(1)), int(m.group(2))
        dung = y - y0
        if 0 < dung < 130 and abs(dung - tuoi) > 1:
            out.append({"kind": "so_hoc_tuoi_nam", "sev": "cao",
                        "msg": f"sinh năm {y0} → {y}年 phải ~{dung} tuổi, kịch bản ghi {tuoi}歳 "
                               f"(「{m.group(0)[:34]}」)"})
    return out


def phep_nhan(body):
    """「200メートルの60倍は12キロ」→ 200×60 = 12.000m = 12km. Đây chính là lỗi kênh mẫu bị bắt."""
    out = []
    dv = "|".join(re.escape(k) for k in DV_DAI)
    pat = (r"(" + _NUM + r")\s*(" + dv + r")[^。]{0,14}?の\s*(" + _NUM + r")\s*倍"
           r"[^。]{0,16}?(" + _NUM + r")\s*(" + dv + r")")
    for m in re.finditer(pat, body):
        a, k, c = to_num(m.group(1)), to_num(m.group(3)), to_num(m.group(4))
        if None in (a, k, c):
            continue
        trai = a * DV_DAI[m.group(2)] * k
        phai = c * DV_DAI[m.group(5)]
        if lech(trai, phai, 0.10):
            out.append({"kind": "so_hoc_phep_nhan", "sev": "cao",
                        "msg": f"「{m.group(0)[:48]}」→ {a:g}×{k:g} = {trai:g}m, "
                               f"kịch bản ghi {c:g}{m.group(5)} ({phai:g}m)"})
    return out


def hang_so(body):
    """Thước so sánh quen thuộc bị ghi lệch bậc."""
    out = []
    for ten, (that, dv, keys) in HANG_SO.items():
        that_m = that * (1e3 if dv == "km" else 1.0)
        for key in keys:
            pat = (re.escape(key) + r"は?[^。]{0,12}?(?:約|およそ)?\s*(" + _NUM +
                   r")\s*(キロ|km|メートル|m)")
            for m in re.finditer(pat, body):
                v = to_num(m.group(1))
                if v is None:
                    continue
                v_m = v * (1e3 if m.group(2) in ("キロ", "km") else 1.0)
                if lech(v_m, that_m, 0.35):
                    out.append({"kind": "so_hoc_hang_so", "sev": "vua",
                                "msg": f"「{m.group(0)[:42]}」→ {ten} thực tế ≈ {that:g}{dv}"})
    return out


def phan_tram(body):
    """Các phần trăm của cùng một tổng cộng lại vượt 100."""
    out = []
    for cau in re.split(r"[。\n]", body):
        if not ("それぞれ" in cau or "うち" in cau or "残り" in cau):
            continue
        ps = [float(x) for x in re.findall(r"(\d{1,3}(?:\.\d+)?)\s*(?:%|パーセント)", cau)]
        if len(ps) >= 2 and 100.5 < sum(ps) < 400:
            out.append({"kind": "so_hoc_phan_tram", "sev": "vua",
                        "msg": f"tổng % = {sum(ps):g} > 100 trong 「{cau[:44]}」"})
    return out


def arithmetic(text):
    """Tất cả phép kiểm số học tất định. Trả list {kind, sev, msg} — cùng khuôn với mechanical()."""
    body = text.replace("\n", "")
    out = []
    for f in (khoang_nam, khoang_thang, tuoi_theo_nam_sinh, phep_nhan, hang_so, phan_tram):
        try:
            out += f(body)
        except Exception as e:                 # một mẫu hỏng không được làm chết cả cổng QC
            out.append({"kind": "so_hoc_loi_kiem", "sev": "thap",
                        "msg": f"{f.__name__}: {type(e).__name__} {e}"})
    return out


def main():
    import argparse
    import sys
    from pathlib import Path
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    a = ap.parse_args()
    hits = arithmetic(Path(a.script).read_text(encoding="utf-8"))
    if not hits:
        print("✓ không thấy lỗi số học tất định nào")
        return 0
    for h in hits:
        print(f"  [{h['sev']}] {h['kind']}: {h['msg']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
