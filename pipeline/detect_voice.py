"""detect_voice.py — PHÂN TÍCH giọng người kể của 1 video nguồn → chọn giọng khớp trong kho.

Vì sao (user chốt 2026-09-09): một kênh có nhiều video, NGƯỜI KỂ khác nhau (video này bà cụ tâm tình,
video kia ông cụ trầm, video khác người dẫn trung tính) → KHÔNG được đọc tất cả bằng 1 giọng. Sau khi
bóc transcript (B2), LLM đọc lời kể suy ra: giới tính · độ tuổi · sắc thái → khớp `voice_bank` chọn giọng
+ hiệu ứng (fx) + tốc độ phù hợp. Giọng này OVERRIDE giọng mặc định của kênh cho RIÊNG video đó.

Chỉ cần transcript nguồn (tiếng Hàn/Nhật/Anh) — KHÔNG cần nghe audio. LLM phán đoán theo ngôi kể, cách
xưng hô, nội dung. Nếu LLM hỏng (hạ tầng) → trả None (caller giữ giọng mặc định của profile).

Dùng:
  py -3.13 detect_voice.py --transcript <slug>/competitor.txt --json
  py -3.13 detect_voice.py --transcript comp.txt --prefer-gender female   # ép giới (khớp ngách)

Import: from detect_voice import detect  ->  dict {gender,age_band,tone,voice_id,voice_name,fx,speed,reason}
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


def _ensure_std():
    """xem channel_scan.py._ensure_std — bẫy sys.stdout=None trong .exe --windowed."""
    for name in ("stdout", "stderr"):
        st = getattr(sys, name, None)
        if st is None:
            setattr(sys, name, open(os.devnull, "w", encoding="utf-8", errors="replace"))
            continue
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_ensure_std()

import voice_bank
from llm_client import chat

# tuổi → hiệu ứng giọng + tốc độ mặc định (khớp VOICE_FX của tts.py)
_FX_BY_AGE = {"old": "old-med", "elderly": "old-med", "senior": "old-med",
              "middle": "none", "middle_aged": "none", "adult": "none",
              "young": "young", "teen": "young"}
_SPEED_BY_AGE = {"old": 0.92, "elderly": 0.92, "senior": 0.93,
                 "middle": 0.98, "middle_aged": 0.98, "adult": 1.0, "young": 1.0, "teen": 1.02}

_SCHEMA = """{"gender":"male|female","age_band":"young|middle_aged|old",
 "tone":"3-6 từ tiếng Việt tả sắc thái giọng, vd: trầm ấm chậm rãi tâm tình",
 "confidence":"cao|vừa|thấp","reason":"1 câu vì sao"}"""


def _classify(transcript, lang=""):
    """LLM đọc lời kể → JSON {gender, age_band, tone, ...}. Trả None nếu không parse được."""
    sample = transcript.strip()[:4000]     # đủ để nhận giọng kể; khỏi gửi cả bài cho rẻ+nhanh
    ask = "\n".join([
        "Đây là TRANSCRIPT lời kể (voiceover) của một video kể chuyện faceless.",
        "Hãy suy ra NGƯỜI KỂ (ngôi thứ nhất nếu có) là ai để chọn giọng đọc phù hợp.",
        "Căn cứ: ngôi kể, cách xưng hô, nội dung trải nghiệm, giọng điệu.",
        "",
        "Trả về DUY NHẤT JSON đúng khuôn (không thêm chữ nào):",
        _SCHEMA,
        "",
        "TRANSCRIPT:",
        sample,
    ])
    try:
        r = chat(ask, task="short", max_tokens=400, min_chars=20, verbose=False)
    except Exception as e:
        print(f"  (detect_voice: LLM lỗi {type(e).__name__} {e})")
        return None
    m = re.search(r"\{.*\}", r.text, re.DOTALL)
    if not m:
        print(f"  (detect_voice: LLM không trả JSON: {r.text[:120]})")
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def detect(transcript, lang="", prefer_gender="", voices=None):
    """Phân tích + chọn giọng. prefer_gender ('male'/'female') = ÉP theo ngách (khớp ảnh/kịch bản)."""
    d = _classify(transcript, lang)
    if not d:
        return None
    gender = (prefer_gender or d.get("gender") or "").lower()
    age = str(d.get("age_band") or "middle_aged").lower().replace(" ", "_")
    tone = d.get("tone") or ""
    age_key = "old" if "old" in age or "eld" in age or "senior" in age else \
              ("young" if "young" in age or "teen" in age else "middle_aged")
    # Khớp kho giọng qua QUERY (cộng điểm mềm), KHÔNG lọc cứng age: nhiều giọng "mature" bị gán nhãn
    # middle_aged (xem docstring voice_bank.suggest) → lọc cứng age='old' sẽ loại nhầm. Thay vào đó
    # nhồi từ tuổi vào query để PERSONA_KEYWORDS bắt: gia→mature/senior/wise, tre→young/youthful.
    age_word = {"old": "gia", "young": "tre"}.get(age_key, "")
    gender_word = "cu ba" if gender == "female" and age_key == "old" else \
                  ("cu ong" if gender == "male" and age_key == "old" else "")
    query = f"{tone} {age_word} {gender_word}".strip()
    hits = voice_bank.suggest(query or tone, gender=gender, age="", limit=5, voices=voices)
    if not hits:                            # nới lỏng: bỏ lọc giới
        hits = voice_bank.suggest(tone or "ke chuyen", limit=5, voices=voices)
    if not hits:
        return None
    v = hits[0][1]
    fx = _FX_BY_AGE.get(age_key, "none")
    speed = _SPEED_BY_AGE.get(age_key, 0.98)
    return {
        "gender": gender or v.get("gender") or "",
        "age_band": age_key,
        "tone": tone,
        "confidence": d.get("confidence", ""),
        "voice_id": v.get("voice_id"),
        "voice_name": v.get("name", ""),
        "fx": fx,
        "speed": speed,
        "reason": d.get("reason", ""),
        "alts": [{"voice_id": x[1].get("voice_id"), "name": x[1].get("name", "")} for x in hits[1:4]],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True, help="file competitor.txt (lời kể nguồn)")
    ap.add_argument("--lang", default="")
    ap.add_argument("--prefer-gender", dest="prefer_gender", default="",
                    help="male/female — ép giới cho khớp ngách (ảnh + kịch bản)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    txt = Path(a.transcript).read_text(encoding="utf-8", errors="replace")
    r = detect(txt, a.lang, a.prefer_gender)
    if not r:
        print(json.dumps({"error": "khong phan tich duoc"}) if a.json
              else "✗ Không phân tích được giọng (LLM lỗi / transcript rỗng).")
        return 1
    if a.json:
        print(json.dumps(r, ensure_ascii=False))
        return 0
    print(f"Người kể : {r['gender']} · {r['age_band']} · {r['tone']} (tin cậy {r['confidence']})")
    print(f"→ Giọng  : {r['voice_name']}  [{r['voice_id']}]")
    print(f"  fx={r['fx']} speed={r['speed']} · vì: {r['reason']}")
    if r.get("alts"):
        print("  giọng thay thế: " + ", ".join(f"{x['name']}" for x in r["alts"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
