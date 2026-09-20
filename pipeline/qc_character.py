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
AGE_TOL = 12                                  # lệch quá 12 tuổi so thiết kế = flag


def _chat(model, prompt, img_b64):
    body = json.dumps({"model": model, "stream": False, "max_tokens": 120,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + img_b64}}]}]}).encode()
    req = urllib.request.Request(BASE_URL + "/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {API_KEY}", "User-Agent": _UA,
                 "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


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
            d = _parse_json(_chat(m, prompt, b64))
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
    if exp_age is not None and abs(age - exp_age) > AGE_TOL:
        flags.append(f"AGE lệch: nhìn ~{age}, thiết kế {exp_age} (>±{AGE_TOL})")
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
        if args.age and age and abs(age - args.age) > AGE_TOL:
            print(f"  ⚠ lệch tuổi so thiết kế {args.age}"); lech = True
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
