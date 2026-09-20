"""voice_bank.py — kho giọng OpenSpeaker: hút danh sách, TÌM giọng theo mô tả nhân vật, nghe thử.

Vì sao cần: tool phải làm được MỌI nhân vật (cụ bà tâm tình, trai trẻ ầm vang, nữ sắc sảo...), không
đóng đinh 12 giọng calm/deep như `tts.py._OS_VOICES` cũ. Xem `docs/PROFILE_ARCHITECTURE.md`.

Dùng:
  py -3.13 voice_bank.py --refresh                          # hút lại /v3/voices → assets/voice_bank.json
  py -3.13 voice_bank.py --find "trai tre manh me an to noi lon"
  py -3.13 voice_bank.py --find "cu ba tam tinh" --gender female --age middle_aged
  py -3.13 voice_bank.py --preview elevenlabs_D3L9PtKnIVJXdgK444Ey --fx boom   # đọc thử 1 câu
  py -3.13 voice_bank.py --list-fx

Import:
  from voice_bank import load, suggest, resolve
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from paths import res, DATA_DIR
# ĐỌC: bản bundle trong exe. GHI (--refresh): ra cạnh exe để lần sau đọc được bản mới.
BANK = res("assets/voice_bank.json")
BANK_WRITE = DATA_DIR / "assets" / "voice_bank.json"
PROVIDERS = ("elevenlabs", "minimax", "fish", "vbee", "edge")

# Mô tả nhân vật (tiếng Việt anh hay gõ) → từ khoá trong description/descriptives của giọng.
PERSONA_KEYWORDS = {
    "manh me": ["powerful", "dominant", "deep", "dramatic", "serious", "commander"],
    "am vang": ["deep", "powerful", "resonance", "dramatic", "bass"],
    "an to noi lon": ["powerful", "dominant", "energetic", "dramatic"],
    "du doi": ["powerful", "dramatic", "serious", "samurai"],
    "hung": ["powerful", "deep", "dramatic", "samurai", "commander"],
    "tre": ["young", "youthful", "cheerful", "energetic", "fresh"],
    "nhiet": ["cheerful", "energetic", "hyped", "high-energy", "fast-paced"],
    "noi nhanh": ["fast-paced", "energetic", "hyped"],
    "tram": ["deep", "calm", "mature", "grounded", "low"],
    "am ap": ["warm", "soothing", "gentle", "kind"],
    "gia": ["mature", "senior", "wise", "grounded"],
    "cu ba": ["mature", "soothing", "calm", "gentle"],
    "cu ong": ["deep", "mature", "wise", "grounded"],
    "tam tinh": ["soothing", "calm", "warm", "intimate"],
    "sac sao": ["sharp", "assertive", "self-assured", "decisive"],
    "gat": ["sharp", "assertive", "cold", "serious"],
    "nghiem": ["serious", "professional", "commander", "confident"],
    "tin cay": ["trustworthy", "confident", "professional", "business"],
    "ke chuyen": ["narrator", "narration", "storyteller", "audiobook"],
    "de thuong": ["cute", "playful", "sweet", "bright"],
    "thieu nien": ["boy", "young", "student", "innocent"],
}
GENDER_VN = {"nam": "male", "trai": "male", "ong": "male", "nu": "female", "gai": "female",
             "ba": "female", "chi": "female"}


# ---------------------------------------------------------------- hút / nạp
def refresh(save=True):
    """Hút toàn bộ /v3/voices của mọi provider → list dict (mỗi giọng có _prov)."""
    import requests
    import openspeaker_tts as osp
    headers = osp._headers()
    out, seen = [], set()
    for prov in PROVIDERS:
        for lang in ("Japanese", ""):
            params = {"provider": prov}
            if lang:
                params["language"] = lang
            try:
                r = requests.get(f"{osp.BASE}/v3/voices", headers=headers, params=params, timeout=60)
            except Exception as e:
                print(f"  ! {prov}: {type(e).__name__} {e}")
                break
            if r.status_code != 200:
                continue
            d = r.json()
            items = d.get("data") or d.get("voices") or (d if isinstance(d, list) else [])
            if isinstance(items, dict):
                items = items.get("voices", [])
            if not items:
                continue
            for v in items:
                vid = str(v.get("voice_id") or v.get("id") or "")
                if not vid or vid in seen:
                    continue
                seen.add(vid)
                v["_prov"] = prov
                out.append(v)
            break     # provider này đã ra kết quả, khỏi thử query khác
        print(f"  {prov}: tổng {len(out)} giọng")
    if save and out:
        BANK_WRITE.parent.mkdir(parents=True, exist_ok=True)
        BANK_WRITE.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"✓ Lưu {len(out)} giọng → {BANK_WRITE}")
    return out


def load():
    if not BANK.exists():
        print(f"⚠️ Chưa có {BANK} → chạy: py -3.13 voice_bank.py --refresh")
        return refresh()
    return json.loads(BANK.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- tìm giọng
def _text_of(v):
    return " ".join(str(x) for x in (v.get("name"), v.get("description"),
                                     v.get("descriptives"), v.get("category"),
                                     v.get("use_cases"), v.get("tags"))).lower()


def _keywords(query):
    """Mô tả tiếng Việt/Anh → tập từ khoá tìm kiếm."""
    q = re.sub(r"[^a-z0-9\s]", " ", (query or "").lower())
    kws = []
    for phrase, words in PERSONA_KEYWORDS.items():
        if phrase in q:
            kws += words
    # từ tiếng Anh gõ trực tiếp cũng dùng luôn
    kws += [w for w in q.split() if len(w) > 3 and w.isascii()]
    return list(dict.fromkeys(kws))


def suggest(query="", gender="", age="", limit=8, voices=None):
    """Trả list (điểm, giọng) khớp nhất.

    gender/age truyền TAY = lọc CỨNG. Còn giới/tuổi đoán được từ câu mô tả chỉ CỘNG ĐIỂM —
    nếu lọc cứng theo suy đoán thì gõ "trai trẻ mạnh mẽ" sẽ loại mất Ryu-Characters / Dominant Man
    (đều middle_aged) tức là mất đúng mấy giọng ầm vang nhất.
    """
    voices = voices if voices is not None else load()
    q = (query or "").lower()
    hard_gender, hard_age = gender.lower(), age.lower().replace(" ", "_")
    soft_gender = soft_age = ""
    if not hard_gender:
        for vn, en in GENDER_VN.items():
            if re.search(rf"\b{vn}\b", q):
                soft_gender = en
                break
    if not hard_age and re.search(r"\btre\b|\byoung\b|thieu nien", q):
        soft_age = "young"
    kws = _keywords(query)
    scored = []
    for v in voices:
        g = str(v.get("gender") or "").lower()
        a = str(v.get("age") or "").lower().replace(" ", "_")
        if hard_gender and g and g != hard_gender:
            continue
        if hard_age and a and hard_age not in a:
            continue
        text = _text_of(v)
        name = str(v.get("name") or "").lower()
        desc = str(v.get("descriptives") or "").lower()
        score = 0.0
        for k in kws:
            if k in desc:
                score += 3           # descriptives = nhãn chính thức của giọng
            elif k in name:
                score += 2           # tên giọng cũng là tín hiệu mạnh (Dominant Man, Serious Commander)
            elif k in text:
                score += 1
        if soft_gender and g:
            score += 1.5 if g == soft_gender else -2.5   # gõ "nữ" thì giọng nam phải tụt hạng
        if soft_age and a and soft_age in a:
            score += 1.5
        if v.get("description"):
            score += 0.5             # có mô tả rõ → dễ chọn đúng
        if score > 0 or not kws:
            scored.append((round(score, 1), v))
    scored.sort(key=lambda t: -t[0])
    return scored[:limit]


def resolve(name_or_id, voices=None):
    """'ado' / 'Ryu - Characters' / 'elevenlabs_xxx' → voice_id thật."""
    s = str(name_or_id or "").strip()
    if not s:
        return ""
    if re.match(r"^(elevenlabs|minimax|fish|vbee|edge|clone)_", s):
        return s
    voices = voices if voices is not None else load()
    low = s.lower()
    for v in voices:                                   # khớp tên chính xác trước
        if str(v.get("name", "")).lower() == low:
            return v["voice_id"]
    for v in voices:                                   # rồi khớp tiền tố tên
        if str(v.get("name", "")).lower().startswith(low):
            return v["voice_id"]
    for v in voices:                                   # cuối cùng khớp chứa
        if low in str(v.get("name", "")).lower():
            return v["voice_id"]
    return s                                           # để tts.py tự báo lỗi nếu sai


# ---------------------------------------------------------------- CLI
SAMPLE_JA = "私が、この村に、戻ってまいりましたのは、去年の、秋のことでございます。"


def _preview(voice_id, fx, speed, text):
    import openspeaker_tts as osp
    from tts import apply_fx, mp3_seconds
    outdir = DATA_DIR / "_voice_test"
    outdir.mkdir(parents=True, exist_ok=True)
    p = outdir / f"preview_{voice_id[-8:]}_{fx}.mp3"
    audio, _ = osp.synthesize(text, voice_id=voice_id, speed=speed,
                              with_transcript=False, file_name=p.stem)
    p.write_bytes(audio)
    apply_fx(p, fx)
    print(f"✓ Nghe thử: {p} ({mp3_seconds(p):.1f}s)")
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="hút lại danh sách giọng từ server")
    ap.add_argument("--find", default="", help='mô tả nhân vật, vd "trai tre manh me an to noi lon"')
    ap.add_argument("--gender", default="", help="male/female (không truyền = tự đoán từ --find)")
    ap.add_argument("--age", default="", help="young/middle_aged")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--preview", default="", help="voice_id hoặc tên giọng → đọc thử 1 câu")
    ap.add_argument("--fx", default="none", help="none/young/boom/punch/old-mild/old-med/old-frail")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--text", default=SAMPLE_JA, help="câu đọc thử")
    ap.add_argument("--list-fx", action="store_true")
    args = ap.parse_args()

    if args.list_fx:
        from tts import VOICE_FX
        for k, v in VOICE_FX.items():
            print(f"{k:10s} {v or '(giữ nguyên)'}")
        return
    if args.refresh:
        refresh()
        return
    if args.preview:
        _preview(resolve(args.preview), args.fx, args.speed, args.text)
        return
    voices = load()
    if not args.find and not args.gender and not args.age:
        print(f"Kho có {len(voices)} giọng "
              f"({sum(1 for v in voices if str(v.get('gender')).lower()=='male')} nam / "
              f"{sum(1 for v in voices if str(v.get('gender')).lower()=='female')} nữ). "
              f"Dùng --find \"<mô tả nhân vật>\".")
        return
    hits = suggest(args.find, args.gender, args.age, args.limit, voices)
    if not hits:
        print("Không tìm thấy giọng khớp — thử bỏ --gender/--age hoặc đổi từ khoá.")
        return
    print(f"Từ khoá tìm: {_keywords(args.find) or '(không)'}\n")
    for score, v in hits:
        print(f"[{score:4.1f}] {v['voice_id']:38s} {str(v.get('name'))[:34]:34s} "
              f"{str(v.get('gender') or '?')[:6]:6s} {str(v.get('age') or '?')[:11]:11s} "
              f"{str(v.get('description') or v.get('descriptives'))[:70]}")
    print(f"\n→ Nghe thử: py -3.13 voice_bank.py --preview {hits[0][1]['voice_id']} --fx boom")


if __name__ == "__main__":
    main()
