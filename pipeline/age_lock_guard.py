"""AGE LOCK guard (anh chốt 01/10/2026): `look` trong characters.json phải tả ĐÚNG tuổi, cấm làm trẻ.
Mọi lane, mọi tập: chặn các cụm "66 but looks early 50s", "youthful", "younger-looking"... trước khi sinh prompt ảnh.
Luật gốc: docs/QUY_TAC_REF_NHAN_VAT_TUOI_CAM_XUC.md §12-§17."""
import re

_CAM = [
    (r"\bbut\s+looks?\b", "'N but looks M' (làm trẻ)"),
    (r"\blooks?\s+(like\s+)?(early|mid|late|around|about|in\s+(his|her|their))\b", "'looks early/mid/around …' (khai tuổi nhìn thấy khác tuổi script)"),
    (r"\byounger[- ]looking\b|\blooks?\s+younger\b|\byoung[- ]looking\b", "'younger-looking'"),
    (r"\byouthful\b|\bde-?aged?\b(?!\s*(or|the character))|\bageless\b|\bflawless\b", "'youthful/ageless/flawless'"),
    (r"\b(early|mid|late)[- ]?(20|30|40|50)s\b", "khai tuổi thập niên khác tuổi script"),
]


def kiem(chars):
    """Trả list lỗi (rỗng = sạch). chars = characters.json['characters']."""
    loi = []
    for c in chars or []:
        look = str(c.get("look") or "")
        ten = c.get("id") or c.get("name") or "?"
        for pat, ten_loi in _CAM:
            if re.search(pat, look, re.I):
                loi.append(f"{ten}: look chứa {ten_loi} — AGE LOCK: chỉ ghi đúng tuổi script + dấu hiệu tuổi (% tóc bạc, nếp nhăn), cấm làm trẻ")
                break
        m = re.search(r"\b(\d{2})[- ]?(?:years?[- ]old|yo)\b|\b[A-Za-z ]*,\s*(\d{2})\b", look)
        age = c.get("age")
        for g in (m.groups() if m else ()):
            if g and age and abs(int(g) - int(age)) > 1:
                loi.append(f"{ten}: look ghi tuổi {g} ≠ age={age}")
    return loi


def chan(chars, noi="characters.json"):
    loi = kiem(chars)
    if loi:
        raise SystemExit(f"✗ AGE LOCK ({noi}): " + " | ".join(loi))
