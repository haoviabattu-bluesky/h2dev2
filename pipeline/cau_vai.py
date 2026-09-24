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
    for p, dong in enumerate([ln.strip() for ln in text.splitlines() if ln.strip()], 1):
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
                out[k] = {"para": p, "text": out[k].strip()}
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
