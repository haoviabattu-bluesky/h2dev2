# -*- coding: utf-8 -*-
r"""cau_vai.py — MỘT luật cắt câu dùng chung cho lane đa giọng (Lane K `yakkyoku-sukatto`, 2026-09-24).

Vì sao có file này: ba bước cùng phải nói về "câu thứ i" của script.txt — gán vai (gan_vai.py, máy 1),
lồng tiếng từng câu bằng đúng giọng (tts_voicevox.py, máy 2) và vẽ bóng thoại (tate_text.py, máy 2).
Nếu mỗi bước tự cắt câu một kiểu thì câu 57 của bước này là câu 58 của bước kia → giọng/bóng thoại
lệch người nói mà không cổng nào báo. Cả ba chỉ được gọi `tach_cau()` ở đây.

Luật cắt:
- Mỗi dòng không rỗng của script.txt = 1 đoạn (para).
- Trong đoạn: khối 「…」 (kể cả 『』 lồng trong) là MỘT đơn vị, dù bên trong có 。 — lời thoại đọc
  bằng giọng nhân vật, không được xé đôi. Chữ ngoài ngoặc cắt sau 。！？.
- Khối 「」 dính chữ ngoài ngoặc trong cùng câu (「…」と彼は言った。) vẫn bị tách thành 2 đơn vị;
  luật viết của lane cấm kiểu này (S3 `dialogue_own_sentence` bắt) nhưng cắt vẫn phải tất định.

Định dạng vai.txt (gan_vai.py ghi, tts_voicevox.py / tate_text.py đọc): mỗi dòng `n|id_vai|câu nguyên văn`,
n từ 1, id_vai = "ke" (người kể) hoặc `id` trong characters.json.
"""
import re
from pathlib import Path

KE = "ke"                     # id vai của người kể (giọng lấy từ profile voice.narrator)
_END = "。！？!?"
_MO, _DONG = "「『", "」』"


def _chuan(s):
    return re.sub(r"\s+", "", s or "")


def tach_cau(text):
    """→ list dict {i, para, text} theo đúng thứ tự đọc."""
    out = []
    # khoi = số thứ tự KHỐI giữa các dòng trống (= cảnh). 2026-10-04: kịch bản viết mỗi câu một dòng, dòng
    # trống chỉ khi đổi cảnh → nghỉ dài (tts_voicevox) phải theo khoi, không theo dòng (para).
    dong_khoi, khoi, trong = [], 1, False
    for ln in text.splitlines():
        if not ln.strip():
            trong = bool(dong_khoi)
            continue
        if trong:
            khoi, trong = khoi + 1, False
        dong_khoi.append((ln.strip(), khoi))
    for p, (dong, kh) in enumerate(dong_khoi, 1):
        buf, sau = "", 0          # sau = độ sâu ngoặc
        for ch in dong:
            if ch in _MO and sau == 0 and ch == "「" and _chuan(buf):
                out.append(buf)       # chữ ngoài ngoặc đứng trước 「 thành câu riêng
                buf = ""
            buf += ch
            if ch in _MO:
                sau += 1
            elif ch in _DONG:
                sau = max(0, sau - 1)
                if sau == 0 and ch == "」":
                    out.append(buf)
                    buf = ""
            elif ch in _END and sau == 0:
                out.append(buf)
                buf = ""
        if _chuan(buf):
            out.append(buf)
        # gắn số đoạn cho các câu vừa thêm
        for k in range(len(out)):
            if isinstance(out[k], str):
                out[k] = {"para": p, "khoi": kh, "text": out[k].strip()}
    res = [c for c in out if _chuan(c["text"]) and _chuan(c["text"]) not in ("、", "。")]
    for i, c in enumerate(res, 1):
        c["i"] = i
    return res


def la_thoai(cau):
    """Câu là lời trong ngoặc 「」 (thoại) — bỏ khoảng trắng rồi xét đầu/cuối."""
    s = _chuan(cau)
    return s.startswith("「") and s.endswith("」")


def bo_ngoac(cau):
    """Chữ hiển thị trong bóng thoại / gửi TTS: bỏ 「」 bọc ngoài (kênh mẫu không in ngoặc trong bóng)."""
    s = cau.strip()
    if s.startswith("「") and s.endswith("」"):
        s = s[1:-1]
    return s.strip()


# 2026-10-06 (Lane O ep04, anh: clip hook "chưa có dừng nghỉ hoặc nghỉ quá ngắn"): MỘT luật khoảng lặng giữa câu
# cho cả giọng thân máy 2 (tts_voicevox) lẫn clip hook xem thử (xem_thu_hook_giong) — nghe thử sao, video thật vậy.
# Sàn = luật 03/10 (câu ≥0,5s, đoạn ≥1,0s; ghim 0,5/1,1 như pipeline/pace_audio.py).
SAN_NGHI_CAU, SAN_NGHI_DOAN = 0.5, 1.1
KHE_MANH = 0.2      # mảnh câu (「昔、」「代わりは…」「が口ぐせ…」cùng 1 câu) — chỉ hơi ngắt như dấu phẩy


def khe_nghi(c, n, nghi_cau, nghi_doan, khoa="khoi", doan_them=()):
    """Khoảng lặng (s) sau câu c, câu kế là n (None = hết). c/n = dict của tach_cau().
    doan_them = tập số câu `i` phải nghỉ ĐOẠN dù cùng khối (hook_timeline.json `nghi_doan_sau`: đổi cảnh/thời gian)."""
    nghi_cau, nghi_doan = max(nghi_cau, SAN_NGHI_CAU), max(nghi_doan, SAN_NGHI_DOAN)
    if n is None:
        return nghi_cau
    t = c["text"].rstrip()
    t0 = t.rstrip(_DONG)
    # mảnh: không có dấu hết câu (xuống dòng giữa câu), hoặc 「…」 không 。 mà câu còn tiếp trên cùng dòng
    if not t.endswith(tuple(_END + _DONG)) or (t != t0 and not t0.endswith(tuple(_END)) and n["para"] == c["para"]):
        return KHE_MANH
    if n[khoa] != c[khoa] or c["i"] in doan_them:
        return nghi_doan
    return nghi_cau


def doan_hook(tap, cau):
    """Số câu nghỉ đoạn trong hook (`hook/hook_timeline.json` → `nghi_doan_sau`), CHỈ khi hook nằm đầu script
    (số câu hook = số câu script). Hook nối trước (giọng riêng) → set() để không nghỉ nhầm câu thân."""
    tl, hk = Path(tap) / "hook" / "hook_timeline.json", Path(tap) / "hook" / "hook_locked.txt"
    if not (tl.exists() and hk.exists()):
        return set()
    import json
    so = [int(x) for x in json.loads(tl.read_text(encoding="utf-8")).get("nghi_doan_sau") or []]
    bo = lambda x: _chuan(x).replace("。", "")      # tach_cau bỏ 。 sau 」
    h = bo(hk.read_text(encoding="utf-8"))
    return set(so) if so and bo("".join(c["text"] for c in cau)).startswith(h) else set()


def lang_tu_timeline(tl):
    """2026-10-12 (anh duyệt hook Lane L ep15: cảnh mở đầu KHÔNG lời — chỉ motion gõ ngày/bệnh viện, cảnh 経理課 chỉ chữ
    địa điểm, dừng ngắn giữ mặt nhân vật cho thẻ tên). Shot LẶNG = shot không có `cau`, khai `lang_s` (giây). Shot có lời
    khai thêm `nghi_sau_s` = giữ hình sau câu cuối của shot. Trả {số câu i: giây lặng THÊM sau câu i}; i = 0 = trước câu 1."""
    out, b = {}, 0
    for s in tl.get("shots") or []:
        if "cau" in s:
            b = int(s["cau"][1])
            if s.get("nghi_sau_s"):
                out[b] = out.get(b, 0.0) + float(s["nghi_sau_s"])
        elif s.get("lang_s"):
            out[b] = out.get(b, 0.0) + float(s["lang_s"])
    return out


def lang_hook(tap, cau):
    """Giây lặng thêm của hook (shot lặng `lang_s` + `nghi_sau_s`, xem lang_tu_timeline) để máy 2 chèn vào GIỌNG THÂN —
    CHỈ khi hook nằm đầu script (cùng điều kiện doan_hook). {} nếu không có."""
    tl, hk = Path(tap) / "hook" / "hook_timeline.json", Path(tap) / "hook" / "hook_locked.txt"
    if not (tl.exists() and hk.exists()):
        return {}
    import json
    out = lang_tu_timeline(json.loads(tl.read_text(encoding="utf-8")))
    bo = lambda x: _chuan(x).replace("。", "")
    return out if out and bo("".join(c["text"] for c in cau)).startswith(bo(hk.read_text(encoding="utf-8"))) else {}


def nghi_the_ten(tap, cau):
    """2026-10-11 (anh chốt Lane L ep14): thẻ tên động ở THÂN bài — nhân vật không tự giới thiệu bằng lời, máy 2 chồng
    thẻ lúc nhân vật hiện lần đầu và giọng NGHỈ THÊM 1–2s sau câu neo để người xem kịp đọc thẻ.
    File `<tập>/the_ten_than.json` = [{"id", "ten", "kana", "tuoi", "nghe", "cau_neo", "nghi_s"}]. Không có file → {}.
    Trả {số câu i: giây nghỉ tối thiểu}. Câu neo không tìm thấy → báo lỗi (thẻ treo không neo là thẻ sai chỗ)."""
    f = Path(tap) / "the_ten_than.json"
    if not f.exists():
        return {}
    import json
    out = {}
    for t in json.loads(f.read_text(encoding="utf-8")):
        neo = _chuan(t.get("cau_neo") or "").replace("。", "")
        hit = [c["i"] for c in cau if neo and neo in _chuan(c["text"]).replace("。", "")]
        if not hit:
            raise SystemExit(f"✗ the_ten_than.json: không thấy câu neo của {t.get('id')}: {t.get('cau_neo')}")
        out[hit[0]] = max(out.get(hit[0], 0.0), float(t.get("nghi_s") or 1.5))
    return out


def doc_vai(path):
    """vai.txt → list dict {i, id, text}."""
    rows = []
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        n, _, rest = ln.partition("|")
        vid, _, txt = rest.partition("|")
        rows.append({"i": int(n), "id": vid.strip(), "text": txt.strip()})
    return rows


def ghi_vai(path, cau, ids):
    Path(path).write_text("".join(f"{c['i']}|{v}|{c['text']}\n" for c, v in zip(cau, ids)), encoding="utf-8")


def khop_vai(cau, vai_rows):
    """Gán id vai cho từng câu của MỘT script (có thể chỉ là đoạn hook) bằng cách dò tuần tự theo chữ
    trong vai.txt của cả tập. Trả list id; câu không khớp → SystemExit (không đoán)."""
    ids, j = [], 0
    for c in cau:
        t = _chuan(c["text"])
        k = j
        while k < len(vai_rows) and _chuan(vai_rows[k]["text"]) != t:
            k += 1
        if k >= len(vai_rows):
            raise SystemExit(f"✗ câu không có trong vai.txt (script đã đổi sau khi gắn vai?): {c['text'][:40]}")
        ids.append(vai_rows[k]["id"])
        j = k + 1
    return ids
