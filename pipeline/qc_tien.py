"""Cổng TIỀN — bắt DẤU VẾT QUY ĐỔI của bản gốc bằng MÁY, không dùng LLM.

Lỗi hệ thống đã đo (2026-09-11 và cả các tập cũ từ trước): khi nhân bản kịch bản Hàn → Nhật, bộ não
quy đổi con số tiền theo tỉ giá thô — thường là CHIA 10 — rồi giữ nguyên cấu trúc số:

    130만원  → 十三万円      ·  82만원  → 八万二千円  ·  3.000만원 → 三百万円
    500만원  → 五十万円      ·  20만원  → 二万円      ·  3.000원   → 三百円

Đây là DẤU VÂN TAY của việc sao chép, nặng hơn dịch sát câu chữ: khán giả bản xứ nhìn mức lương hưu /
viện phí là biết ngay không phải chuyện của nước mình. Gemini (tầng 1) MÙ HOÀN TOÀN với lỗi này —
hai lượt liền báo ĐẠT. Giám khảo Claude (tầng 2) bắt được nhưng mất ~10 phút và không tất định.

Con số là thứ ĐONG ĐẾM ĐƯỢC ⇒ để MÁY bắt: chạy 1 giây, 0 đồng, không dao động. Đúng nguyên tắc
"Claude viết · máy đo" của `docs/SOP_CLONE_BRAIN.md`.

  py -3.13 qc_tien.py --script <script.txt> --competitor <competitor.txt> [--ti-le 10 100]

exit 0 = sạch · exit 1 = có dấu vết quy đổi.
"""
import argparse
import re
import sys
from pathlib import Path


def _ensure_std():
    """xem channel_scan.py._ensure_std — bẫy sys.stdout=None trong .exe --windowed."""
    for name in ("stdout", "stderr"):
        st = getattr(sys, name, None)
        if st is None:
            continue
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_SO = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
       "六": 6, "七": 7, "八": 8, "九": 9}
_NHO = {"十": 10, "百": 100, "千": 1000}
_LON = [("億", 10 ** 8), ("万", 10 ** 4)]
_CHU_SO = "〇零一二三四五六七八九0-9０-９"


def _doc_cum_nho(s):
    """Đọc cụm dưới 万: 三百七十 → 370 · 二千三百 → 2300 · 十 → 10."""
    tong, hien = 0, 0
    for ch in s:
        if ch in _SO:
            hien = _SO[ch]
        elif ch in _NHO:
            tong += (hien or 1) * _NHO[ch]
            hien = 0
        elif ch.isdigit():
            hien = hien * 10 + int(ch)
    return tong + hien


def doc_so(s):
    """Đọc số Hán-Nhật → int. Trả None nếu không đọc được.

    Xử cả kiểu BẤT QUY TẮC `一三万` (đọc từng chữ số = 13万) — bộ não có viết kiểu này."""
    s = s.strip()
    if not s:
        return None
    if re.fullmatch(r"[0-9０-９,，]+", s):
        return int(re.sub(r"[,，]", "", s.translate(str.maketrans("０１２３４５６７８９", "0123456789"))))
    # tách theo 億 rồi 万
    tong, con = 0, s
    for ky, he in _LON:
        if ky in con:
            trai, con = con.split(ky, 1)
            # `一三` không có 十/百/千 ⇒ đọc như dãy chữ số
            if trai and not any(c in _NHO for c in trai) and len(trai) > 1:
                v = int("".join(str(_SO[c]) if c in _SO else c for c in trai if c in _SO or c.isdigit()))
            else:
                v = _doc_cum_nho(trai) if trai else 1
            tong += v * he
    tong += _doc_cum_nho(con) if con else 0
    return tong or None


def tien_nhat(text):
    """[(chuỗi gốc, giá trị yên)] — bắt cả 円 và 万円."""
    ra = []
    for m in re.finditer(rf"([{_CHU_SO}十百千万億]{{1,16}})\s*円", text):
        v = doc_so(m.group(1))
        if v:
            ra.append((m.group(0), v))
    return ra


_HAN_LON = (("억", 10 ** 8), ("만", 10 ** 4))
_HAN_NHO = (("천", 1000), ("백", 100), ("십", 10))


def doc_so_han(s):
    """Đọc số tiền Hàn kiểu HỖN HỢP chữ số + đơn vị: `4천만` → 40.000.000 · `2,300만` → 23.000.000
    · `1억 5천만` → 150.000.000 · `3천` → 3.000.

    Bản đầu chỉ đọc được `<chữ số>만|억`, nên **bỏ sót hẳn** `4천만 원` / `7천만 원` / `3천 원` có
    thật trong bản gốc (đo 2026-09-11: sót 3/18 chuỗi tiền). Sót ở VẾ BẢN GỐC thì mọi phép đối
    chiếu phía sau đều mù với con số đó — lỗi câm, cổng vẫn báo SẠCH."""
    s = re.sub(r"[,\.\s]", "", s)
    if not s:
        return None
    tong = 0
    for ky, he in _HAN_LON:                     # tách 억 rồi 만
        if ky in s:
            trai, s = s.split(ky, 1)
            tong += (_doc_cum_han(trai) if trai else 1) * he
    tong += _doc_cum_han(s) if s else 0
    return tong or None


def _doc_cum_han(s):
    """Cụm dưới 만: `4천` → 4000 · `2300` → 2300 · `5백` → 500 · `천` → 1000."""
    tong, hien = 0, 0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch.isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            hien = int(s[i:j])
            i = j
            continue
        don = dict(_HAN_NHO).get(ch)
        if don:
            tong += (hien or 1) * don
            hien = 0
        i += 1
    return tong + hien


def tien_han(text):
    """[(chuỗi gốc, giá trị won)] — 원 · 만원 · 억원 · và dạng hỗn hợp `4천만 원`."""
    ra = []
    # chuỗi NHIỀU cụm `<số><đơn vị>` liên tiếp: `1억 5천만 원` phải ăn CẢ `1억` lẫn `5천만`,
    # bắt mỗi cụm cuối là đọc thiếu một bậc (150.000.000 → 50.000.000) mà không báo gì.
    for m in re.finditer(r"([0-9][0-9,\.]*(?:\s*(?:[0-9][0-9,\.]*|[억만천백십]))*)\s*원", text):
        v = doc_so_han(m.group(1))
        if v:
            ra.append((m.group(0).strip(), v))
    return ra


def soi(script, competitor, ti_le=(10,), san=100):
    """Trả danh sách dấu vết: mỗi cái là (số_nhật, số_hàn, tỉ_lệ)."""
    jp = tien_nhat(script)
    kr = tien_han(competitor)
    kr_val = {}
    for s, v in kr:
        kr_val.setdefault(v, s)
    ra, da_bao = [], set()
    for s_jp, v_jp in jp:
        # SÀN chống báo động giả: 「一円」/「十円」 là THÀNH NGỮ ("không một xu nào"), trùng tỉ lệ với
        # 「10원」 chỉ là ngẫu nhiên. Và chỉ soi tỉ lệ 10 — đúng kiểu lỗi hệ thống đã đo; mở rộng sang
        # 100/1000 thì số trùng ngẫu nhiên nhiều hơn số lỗi thật (đo: 19 báo → 5 trong đó là trùng hú hoạ).
        if v_jp < san or s_jp in da_bao:
            continue
        for t in ti_le:
            if v_jp * t in kr_val:
                ra.append((s_jp, v_jp, kr_val[v_jp * t], v_jp * t, t))
                da_bao.add(s_jp)
                break
    return ra, jp, kr


def main():
    _ensure_std()
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--competitor", required=True)
    ap.add_argument("--ti-le", nargs="*", type=int, default=[10])
    ap.add_argument("--san", type=int, default=100, help="bỏ qua số tiền nhỏ hơn (chống thành ngữ 一円)")
    a = ap.parse_args()

    script = Path(a.script).read_text(encoding="utf-8")
    comp = Path(a.competitor).read_text(encoding="utf-8")
    ra, jp, kr = soi(script, comp, a.ti_le, a.san)
    print(f"=== CỔNG TIỀN: {len(jp)} số tiền trong kịch bản · {len(kr)} trong bản gốc ===")
    if not ra:
        print("=== SẠCH — không thấy con số nào là bản quy đổi thô của bản gốc ===")
        return 0
    print(f"=== {len(ra)} DẤU VẾT QUY ĐỔI ===")
    for s_jp, v_jp, s_kr, v_kr, t in ra:
        print(f"   ✗ 「{s_jp}」 = {v_jp:,} ← đúng bằng 「{s_kr}」 ({v_kr:,}) ÷ {t} của bản gốc")
    print("   → Thay bằng MỨC THẬT của nước sở tại cho hạng mục đó, đừng quy đổi theo tỉ giá.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
