"""qc_character.py — QC nhân vật bằng AI vision (ramclouds) TRƯỚC khi gen cả loạt ảnh.

LÝ DO (user chốt 2026-09-08): master nhân vật phải KHỚP tuổi/giới đã thiết kế, và các nhân vật có
QUAN HỆ phải hợp lý (mẹ 73 → con 20-50, KHÔNG để con nhìn 10 tuổi hay ngang tuổi mẹ). Text-to-image
hay ra tuổi lệch → QC master trước, lệch thì gen lại, đỡ hỏng cả 80 ảnh.

Đọc characters.json:
  {"characters":[{"name":"Fumi","age":73,"gender":"F","master":"_ref/001.png"},
                 {"name":"Son","age":47,"gender":"M","master":"_ref_son/001.png"}],
   "relationships":[{"a":"Fumi","b":"Son","min_gap":18,"max_gap":50}]}
Mỗi master: vision ước lượng apparent_age/gender (trung bình nhiều model), flag nếu |Δtuổi|>TOL hoặc
sai giới hoặc (cần người lớn mà nhìn trẻ con). Quan hệ: flag nếu chênh tuổi thật ngoài [min_gap,max_gap].

Dùng: py -3.13 qc_character.py --bible ../assets/satori_jp/<slug>/characters.json
      py -3.13 qc_character.py --img a.png --age 47 --gender M   (QC 1 ảnh nhanh)
"""
import argparse
import sys
import base64
import json
import re
import statistics
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "https://ramclouds.me"
API_KEY = "sk-ue0LE9lhUveoGFrt3Ah2SFJb82nPD9FVoe7jiihO3n6RnMeJ"
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
MODELS = ["gemini-3.8-flash", "grok-4.6"]   # gemini-3.8-flash = QC chính (user chốt); grok cross-check
AGE_TOL = 12                                  # CŨ — chỉ còn dùng làm dung sai so CHÊNH quan hệ, KHÔNG dùng cho tuổi 1 nhân vật


def age_tol(age):
    """AGE LOCK (anh chốt 01/10/2026, docs/QUY_TAC_REF_NHAN_VAT_TUOI_CAM_XUC.md §12): dung sai tuổi NHÌN THẤY.
    <=59: ±4 · 60–69: ±4 · 70–79: ±5 · >=80: ±5. Thay cho ±12 cũ (cho lọt REF trẻ hơn 10 tuổi)."""
    return 4 if int(age) < 70 else 5


def phan_loai_tuoi(seen, exp):
    """PASS (trong dung sai) · BORDERLINE (lệch thêm <=3 → chỉ cảnh báo) · FAIL (→ REGENERATE).
    VD script 67: PASS 63–71 theo ±4; luật gốc ghi PASS 64–70, BORDERLINE 61–63/71–73, FAIL ≥ lệch 8+."""
    d = abs(int(seen) - int(exp))
    tol = age_tol(exp)
    return "PASS" if d <= tol else ("BORDERLINE" if d <= tol + 3 else "FAIL")


# ---------------------------------------------------------------- THANG DỰ PHÒNG VISION
# Chốt 2026-09-26 sau khi đo 15 model ở 3 proxy trên CÙNG 2 tấm ảnh thật (xem
# docs/FALLBACK_GEMINI_SANG_SOL.md §đo model rẻ). Mốc so sánh là chính gemini-3.8-flash: 52/M và
# 70/F. Ba bậc dưới đây đều đoán sát mốc đó, và mỗi bậc đổi sang một NHÀ khác — hỏng cùng lúc cả
# ba là chuyện khó xảy ra hơn nhiều so với hỏng một nhà.
#
# Vì sao KHÔNG chọn mấy cái tưởng ngon:
#   · `grok-4.5`/`grok-4.6` ở ramclouds: 503 kéo dài, một lượt treo 250 giây rồi mới báo lỗi.
#   · `qwen3.8-flash` ở ramclouds: đọc ảnh 2 ra 30 tuổi trong khi mọi model khác đọc 70–80 — sai
#     tới mức cổng QC sẽ đánh trượt oan ảnh đúng.
#   · `deepseek-v4.1-flash` ở RAMCLOUDS: trả rỗng khi có ảnh (chỉ bản ở ns24 mới nhìn được ảnh).
#     Cùng tên model, khác nhà, khác hẳn khả năng — đừng suy từ nhà này sang nhà kia.
#
# ⚠️ BẪY ĐÃ DÍNH KHI ĐO: `glm-5.3-flash` và `kimi-k3` là model CÓ SUY NGHĨ TRƯỚC — phần suy nghĩ ăn
# vào chính hạn `max_tokens`, nên cho hạn nhỏ (80–120 như bản ramclouds đang dùng) thì trả về RỖNG
# mà HTTP vẫn 200, trông y hệt "model không đọc được ảnh". Vì vậy mọi bậc dự phòng ở đây dùng hạn
# rộng `_MAX_TOKENS_DP` chứ không dùng lại 120 của đường chính.
_MAX_TOKENS_DP = 700
THANG_DU_PHONG = [
    ("ns24", "deepseek-v4.1-flash"),    # khớp mốc (55/M 75/F) và NHANH nhất: 7 giây cho cả 2 ảnh
    ("hhtech", "glm-5.3-flash"),        # khớp mốc (55/M 75/F), đổi hẳn nhà thứ ba
]
_PROXY = {
    "ramclouds": ("https://ramclouds.me/v1", API_KEY),
    "ns24": ("https://api.ns24.io/v1", "sk-up-0ef5398f1893e50f6a8d9055c7b9e7cb4f847dac7601d09f"),
    "hhtech": ("https://hhtechapi.net/v1", "sk-d4108f8b284a42b48df72bf4"),
}


def _chat(model, prompt, img_b64, cho_phep_sol=True):
    """Lõi VISION dùng chung. ramclouds trước; hỏng thì lần lượt xuống `THANG_DU_PHONG` rồi sol.

    VÌ SAO (2026-09-26): hàm này là lõi vision của `qc_character` (QC master nhân vật), `qc_canh.py`
    (soi từng cảnh), `soi_kho.py` (chấm kho tư liệu → `tim_anh_that.py` gọi tiếp) và `audit_stock.py`.
    Trước đây nó gọi THẲNG ramclouds, không lưới đỡ: ramclouds/gemini hỏng là cả 4 bước chết cùng
    lúc. Quan trọng nhất, mấy bước này chạy Ở MÁY 2 (vẽ ảnh + dựng video) — nơi KHÔNG có 9router,
    nên lưới phải là model chạy được từ xa, không phải proxy nội bộ của máy 1.

    Thứ tự: ramclouds → ns24 → hhtech → sol. Sol xếp cuối vì đắt hơn và chậm hơn ba bậc trên.
    `cho_phep_sol=False` cho người gọi ĐÃ CÓ lưới sol ở tầng trên (`qc_visual._vision`), khỏi chờ
    sol hai lần chồng nhau.
    """
    loi = []
    try:
        return _chat_ramclouds(model, prompt, img_b64)
    except Exception as e:
        loi.append(f"ramclouds({model}): {type(e).__name__} {str(e)[:80]}")
    for nha, mod in THANG_DU_PHONG:
        try:
            return _chat_proxy(nha, mod, prompt, img_b64)
        except Exception as e:
            loi.append(f"{nha}({mod}): {type(e).__name__} {str(e)[:80]}")
    if not cho_phep_sol:
        raise RuntimeError("vision hỏng mọi bậc (sol để tầng trên lo): " + " | ".join(loi))
    import sol_client
    import tempfile
    # sol_client nhận ĐƯỜNG DẪN ảnh (nó tự đọc + base64), còn ở đây ảnh đã ở dạng b64 → ghi ra file
    # tạm thay vì sửa chữ ký sol_client (file đó đang được 5 chỗ khác gọi theo đúng chữ ký cũ).
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(base64.b64decode(img_b64))
        tam = f.name
    try:
        text, _usage = sol_client.chat(prompt, image_path=tam, max_tokens=_MAX_TOKENS_DP, timeout=120)
        return text
    except Exception as e:
        loi.append(f"sol: {type(e).__name__} {str(e)[:100]}")
        raise RuntimeError("vision hỏng MỌI đường: " + " | ".join(loi)) from None
    finally:
        Path(tam).unlink(missing_ok=True)


def _chat_proxy(nha, model, prompt, img_b64, max_tokens=None):
    """Một lượt vision non-stream tới proxy bất kỳ trong `_PROXY` (dùng cho các bậc dự phòng)."""
    base, key = _PROXY[nha]
    body = json.dumps({"model": model, "stream": False,
        "max_tokens": max_tokens or _MAX_TOKENS_DP,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + img_b64}}]}]}).encode()
    req = urllib.request.Request(base + "/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}", "User-Agent": _UA,
                 "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        noi_dung = json.loads(r.read())["choices"][0]["message"]["content"]
    if not (noi_dung or "").strip():
        # Rỗng mà HTTP 200 = model suy nghĩ hết sạch hạn token (xem bẫy ở ghi chú THANG_DU_PHONG).
        raise RuntimeError(f"{nha}:{model} trả RỖNG dù HTTP 200 (nghi hết hạn token vì phần suy nghĩ)")
    return noi_dung


def _chat_ramclouds(model, prompt, img_b64):
    body = json.dumps({"model": model, "stream": False, "max_tokens": 120,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + img_b64}}]}]}).encode()
    req = urllib.request.Request(BASE_URL + "/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {API_KEY}", "User-Agent": _UA,
                 "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        noi_dung = json.loads(r.read())["choices"][0]["message"]["content"]
    if not (noi_dung or "").strip():
        raise RuntimeError(f"ramclouds:{model} trả RỖNG dù HTTP 200")
    return noi_dung


def _parse_json(txt):
    txt = re.sub(r"^```(json)?|```$", "", txt.strip(), flags=re.MULTILINE).strip()
    m = re.search(r"\{.*\}", txt, re.DOTALL)
    return json.loads(m.group(0)) if m else {}


def estimate(path):
    """Trả (avg_age, gender, adult, raw[]) — trung bình các model chạy được."""
    b64 = base64.b64encode(Path(path).read_bytes()).decode()
    prompt = ('You are a strict visual QC for character casting. Look at the MAIN person and estimate. '
              'Reply ONLY compact JSON: {"apparent_age":<int>,"gender":"M"|"F","adult":<true|false>}.')
    ages, genders, adults, raw = [], [], [], []
    for m in MODELS:
        try:
            # Chỉ model ĐẦU được rơi sang sol: ramclouds chết thì cả 2 vòng đều rơi xuống CÙNG một
            # model sol, mất hẳn ý nghĩa cross-check mà tốn gấp đôi thời gian chờ.
            d = _parse_json(_chat(m, prompt, b64, cho_phep_sol=(m == MODELS[0])))
            if "apparent_age" in d:
                ages.append(int(d["apparent_age"])); genders.append(str(d.get("gender", "?")).upper()[:1])
                adults.append(bool(d.get("adult", True))); raw.append(f"{m}={d.get('apparent_age')}/{d.get('gender')}")
        except Exception as e:
            raw.append(f"{m}:ERR {str(e)[:40]}")
    if not ages:
        return None, "?", None, raw
    gender = max(set(genders), key=genders.count)
    return round(statistics.mean(ages)), gender, (sum(adults) >= len(adults) / 2), raw


def qc_char(c, base):
    exp_age, exp_gender = c.get("age"), str(c.get("gender", "")).upper()[:1]
    age, gender, adult, raw = estimate(Path(base) / c["master"])
    flags = []
    if age is None:
        return {"name": c["name"], "flags": ["VISION_FAIL"], "raw": raw}
    if exp_age is not None:
        pl = phan_loai_tuoi(age, exp_age)
        if pl == "FAIL":
            flags.append(f"AGE FAIL → REGENERATE: nhìn ~{age}, script {exp_age} (delta {age - exp_age:+d}, dung sai ±{age_tol(exp_age)})")
        elif pl == "BORDERLINE":
            raw.append(f"BORDERLINE tuổi: nhìn ~{age} vs script {exp_age} (dung sai ±{age_tol(exp_age)})")
    if exp_gender and gender != exp_gender:
        flags.append(f"GIỚI sai: nhìn {gender}, thiết kế {exp_gender}")
    if exp_age is not None and exp_age >= 18 and adult is False:
        flags.append("nhìn TRẺ CON dù nhân vật là người lớn")
    return {"name": c["name"], "seen_age": age, "seen_gender": gender, "exp_age": exp_age,
            "flags": flags, "raw": raw}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bible", help="characters.json")
    ap.add_argument("--img"); ap.add_argument("--age", type=int); ap.add_argument("--gender")
    args = ap.parse_args()

    if args.img:
        age, gender, adult, raw = estimate(args.img)
        print(f"nhìn ~{age} tuổi, giới {gender}, adult={adult}  ({'; '.join(raw)})")
        # exit 2 khi lệch — make_video.masters_from_bible (Lane G, 2026-09-20) đọc mã thoát để quyết vẽ lại master.
        # Trước đây luôn exit 0 (chỉ in cảnh báo) → máy gọi không biết master sai.
        lech = False
        if args.age and age:
            pl = phan_loai_tuoi(age, args.age)
            print(f"  AGE_QC: SCRIPT_AGE={args.age} VISUAL={age} DELTA={age - args.age:+d} → {pl}")
            if pl == "FAIL":
                print(f"  ⚠ AGE FAIL → REGENERATE (dung sai ±{age_tol(args.age)}; cấm tự hợp lý hoá 'người Nhật trông trẻ')"); lech = True
            elif pl == "BORDERLINE":
                print("  ⚠ BORDERLINE — cân nhắc vẽ lại, chưa bắt buộc")
        if args.gender and gender and str(gender)[:1].upper() != str(args.gender)[:1].upper():
            print(f"  ⚠ sai giới so thiết kế {args.gender}"); lech = True
        if args.age and adult is False:
            print("  ⚠ nhìn như trẻ con trong khi thiết kế là người lớn"); lech = True
        sys.exit(2 if lech else 0)

    data = json.loads(Path(args.bible).read_text(encoding="utf-8"))
    base = Path(args.bible).parent
    seen = {}
    ok = True
    print("=== QC NHÂN VẬT ===")
    for c in data.get("characters", []):
        if not c.get("master"):
            print(f"  {c['name']}: (chưa có master, bỏ qua)"); continue
        r = qc_char(c, base)
        seen[c["name"]] = r.get("seen_age")
        status = "✅" if not r["flags"] else "❌"
        print(f"  {status} {r['name']}: nhìn ~{r.get('seen_age')} ({r.get('seen_gender')}), thiết kế {r.get('exp_age')}"
              f"  [{'; '.join(r['raw'])}]")
        for f in r["flags"]:
            print(f"       → {f}"); ok = False
    for rel in data.get("relationships", []):
        a, b = seen.get(rel["a"]), seen.get(rel["b"])
        if a is None or b is None:
            continue
        gap = abs(a - b)
        lo, hi = rel.get("min_gap", 0), rel.get("max_gap", 200)
        if not (lo <= gap <= hi):
            print(f"  ❌ QUAN HỆ {rel['a']}–{rel['b']}: chênh nhìn ~{gap} tuổi, hợp lý [{lo},{hi}]"); ok = False
        else:
            print(f"  ✅ QUAN HỆ {rel['a']}–{rel['b']}: chênh ~{gap} tuổi (OK)")
    print("=== KẾT LUẬN:", "ĐẠT — gen tiếp được" if ok else "CÓ FLAG — sửa master rồi QC lại", "===")


if __name__ == "__main__":
    main()
