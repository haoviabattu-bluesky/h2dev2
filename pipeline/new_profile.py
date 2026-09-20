"""new_profile.py — WIZARD lập kênh/nhân vật mới. Tả bằng tiếng Việt → ra file profile chạy được.

Đây là thứ biến tool từ "1 kênh" thành "mọi kênh": mọi tham số riêng của kênh nằm trong
`profiles/<id>.json`, nên lập kênh mới = chạy wizard này, không phải sửa code.

5 bước:
  1. GỢI Ý GIỌNG   — `voice_bank.suggest()` lọc 69 giọng OpenSpeaker theo mô tả tiếng Việt.
  2. NGHE THỬ      — `--preview` phát 1 câu bằng giọng + fx + tốc độ đã chọn (bỏ qua được).
  3. LLM DỰNG HỒ SƠ— sinh narrator/character_sheet/style_suffix/gate/thumbnail theo NGÔN NGỮ ĐÍCH.
  4. GHI PROFILE   — `profiles/<id>.json`, trỏ sang 3 skill của ngách.
  5. ĐO CHAR-RATE  — `calibrate.py` đọc thật rồi ghi lại char_rate (BẮT BUỘC, đừng đoán).

⚠️ char_rate PHẢI đo, không được chép của kênh khác: nó phụ thuộc giọng + tốc độ + fx + ngôn ngữ.
   Và vì tool có bước GIÃN NHỊP (pace_audio) làm video dài thêm ~15%, char_rate đo ở đây chỉ là mốc
   ban đầu — `make_video` sẽ tự hiệu chỉnh lại theo bản ĐÃ GIÃN sau mỗi lần chạy.

Dùng:
  py -3.13 new_profile.py --find "chang trai manh me an to noi lon"        # xem gợi ý giọng
  py -3.13 new_profile.py --id samurai-jp --niche "võ tướng kể chuyện" \\
      --market JP --lang ja --minutes 30 --persona "võ tướng 50 tuổi, ăn to nói lớn" \\
      --voice "Ryu - Characters" --fx boom --speed 1.0 --yes
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import profiles
import voice_bank
from paths import res
from llm_client import chat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
def _pycmd(script, *args):
    """Lệnh chạy script con — CHẠY ĐƯỢC CẢ khi đã đóng thành .exe.

    Khi frozen, `sys.executable` LÀ chính exe (không phải python.exe) và file .py nằm trong
    `_internal`. Gọi `[sys.executable, "…/calibrate.py"]` thì exe không hiểu, rơi vào nhánh mở
    giao diện → bước đo char-rate IM LẶNG không chạy, hồ sơ giữ số tạm 300 "CHƯA ĐO".
    Đo thật 2026-09-09: hồ sơ Lopezzapa68 vì lỗi này mà hỏng nguyên một lượt làm video.
    Phải dùng nhánh tự-gọi-lại: `exe --child calibrate.py …`.
    """
    if getattr(sys, "frozen", False):
        return [sys.executable, "--child", script] + [str(a) for a in args]
    return [sys.executable, str(HERE / script)] + [str(a) for a in args]


LANG_NAME = {"ja": "tiếng Nhật", "ko": "tiếng Hàn", "en": "tiếng Anh", "vi": "tiếng Việt"}

SCHEMA = """{
 "narrator": {"gender":"male|female","age_band":"","persona":"","point_of_view":"","register":""},
 "character_sheet": "",
 "style_suffix": "",
 "gate": {"comma_per_sentence":[0,0],"chars_per_breath":[0,0],"dialogue_ratio_max":0.0},
 "seconds_per_image": 0,
 "thumbnail_banner": "",
 "blocklist": [""]
}"""


# Skill CHUNG (tổng quát, ngách là tham số) — dùng cho mọi kênh. Chỉ trỏ sang bản RIÊNG khi
# bản đó THẬT SỰ tồn tại, chứ không ghi một đường dẫn ma rồi bắt tool cảnh báo mỗi lần chạy.
_SKILL_CHUNG = {"script": "skills/youtube-script/SKILL.md",
                "image": "skills/youtube-image-prompts/SKILL.md",
                "thumbnail": "skills/youtube-thumbnail/SKILL.md"}


def _skill_path(key, suffix):
    """Có bản skill RIÊNG cho ngách thì dùng, không thì dùng bản chung.

    Phải dò bằng `paths.res()` chứ không phải `ROOT / ...`: khi đóng gói, skills nằm trong
    `_internal/skills`, còn `ROOT` trỏ ra cạnh exe → kiểm kiểu cũ luôn báo THIẾU dù có đủ file.
    """
    ten = {"script": "youtube-script", "image": "youtube-image", "thumbnail": "youtube-thumbnail"}[key]
    rieng = f"skills/{ten}-{suffix}/SKILL.md"
    return rieng if res(rieng).exists() else _SKILL_CHUNG[key]

def _chu_ky_giong(prof):
    """Bộ 4 thứ QUYẾT ĐỊNH tốc độ đọc. Đổi một trong bốn là char_rate cũ vô nghĩa."""
    v = (prof or {}).get("voice", {}) or {}
    return (v.get("id", ""), float(v.get("speed") or 0), v.get("fx", ""),
            (prof or {}).get("language", ""))


def _giu_char_rate(moi, cu):
    """Cập nhật kênh: GIỮ char_rate đã đo nếu giọng/tốc độ/hiệu ứng/ngôn ngữ không đổi.

    Vì sao cần: đổi ngách hay đổi mô tả người kể KHÔNG làm giọng đọc nhanh chậm đi, nhưng bản cũ
    ghi đè hồ sơ là char_rate về lại mốc tạm 300 "CHƯA ĐO" — vứt mất số đo từ video thật, rồi
    video kế tiếp lại lệch độ dài đúng như đã dính với hồ sơ Lopezzapa68.
    Ngược lại, ĐỔI GIỌNG thì số cũ sai hẳn → phải bỏ để đo lại.
    """
    if not cu:
        return moi, False
    vc, vm = cu.get("voice", {}) or {}, moi["voice"]
    # CHỈ giữ khi hồ sơ cũ thật sự ĐÃ ĐO. Hồ sơ cũ còn mang mốc tạm 300 "CHƯA ĐO" mà giữ lại là
    # bê nguyên con số giả sang bản mới VÀ xoá luôn nhãn cảnh báo — đúng kiểu lỗi đã làm hỏng một
    # lượt làm video, chỉ khác là lần này còn khó thấy hơn.
    da_do = bool(vc.get("char_rate_measured_at")) and not vc.get("char_rate_note")
    if not (da_do and vc.get("char_rate")) or _chu_ky_giong(cu) != _chu_ky_giong(moi):
        return moi, False
    for k in ("char_rate", "char_rate_speed", "char_rate_measured_at", "char_rate_from"):
        if vc.get(k) is not None:
            vm[k] = vc[k]
    vm.pop("char_rate_note", None)
    return moi, True


def design(niche, market, lang, persona, minutes):
    """Nhờ LLM dựng phần SÁNG TẠO của hồ sơ. Nhịp/hội thoại là THAM SỐ theo nhân vật, không cố định."""
    ask = "\n".join([
        f"Thiết kế hồ sơ nhân vật cho một kênh YouTube kể chuyện (faceless).",
        f"NGÁCH: {niche} · THỊ TRƯỜNG: {market} · NGÔN NGỮ LỜI KỂ: {LANG_NAME.get(lang, lang)} · "
        f"ĐỘ DÀI MỖI VIDEO: {minutes} phút",
        f"MÔ TẢ NGƯỜI KỂ (tiếng Việt): {persona}",
        "",
        "Trả về JSON đúng khuôn dưới đây, không thêm chữ nào:",
        "· narrator.persona: 1 câu tiếng Việt, gọn.",
        "· narrator.point_of_view + register: viết bằng CHÍNH ngôn ngữ đích (vd 一人称 私 / "
        "です・ます体), vì chúng được dán thẳng vào prompt.",
        "· character_sheet: mô tả ngoại hình bằng TIẾNG ANH, 15-30 từ, có 2-3 đặc điểm ĐỘC NHẤT "
        "(kính, nốt ruồi, kiểu tóc, màu áo) để khoá khuôn mặt qua mọi cảnh.",
        "· style_suffix: đuôi phong cách ảnh bằng TIẾNG ANH, kết thúc bằng '16:9, no text'.",
        "· gate: ngưỡng NHỊP hợp với nhân vật này — người già kể chậm thì nhiều dấu phẩy, câu ngắn "
        "(vd 2.5-6.0 phẩy/câu, 4.5-9.0 chữ/nhịp thở); người trẻ/hào sảng thì ít phẩy, câu dài hơn "
        "(vd 0.8-1.8 và 8-16). dialogue_ratio_max: 0.10-0.35 tuỳ kiểu kể.",
        "· seconds_per_image: 12-17.",
        "· thumbnail_banner: 1 câu phụ đề đáy thumbnail bằng ngôn ngữ đích.",
        "· blocklist: các thứ KHÔNG được vẽ (luôn có baby/infant/newborn/naked/blood/gore).",
        "", SCHEMA])
    r = chat(ask, task="short", max_tokens=1500, min_chars=120)
    m = re.search(r"\{.*\}", r.text, re.DOTALL)
    if not m:
        raise SystemExit(f"LLM không trả JSON:\n{r.text[:300]}")
    return json.loads(m.group(0))


def build(args, voice, d):
    g = d.get("gate") or {}
    n = d.get("narrator") or {}
    bl = [b for b in (d.get("blocklist") or []) if b]
    for must in ("baby", "infant", "newborn", "naked", "blood", "gore"):
        if must not in bl:
            bl.append(must)
    return {
        "id": args.id,
        "market": args.market,
        "language": args.lang,
        "niche": args.niche,
        "competitor": args.competitor,
        "slug_dir": args.slug_dir,
        "narrator": {
            "gender": n.get("gender") or args.gender or "female",
            "age_band": n.get("age_band", ""),
            "persona": n.get("persona") or args.persona,
            "point_of_view": n.get("point_of_view", ""),
            "register": n.get("register", ""),
        },
        "voice": {
            "id": voice["voice_id"],
            "name": voice.get("name", ""),
            "speed": args.speed,
            "fx": args.fx,
            # Mốc tạm; bước 5 (calibrate) sẽ ghi đè bằng số ĐO THẬT.
            "char_rate": 300.0,
            "char_rate_note": "CHƯA ĐO — chạy calibrate.py trước khi làm video",
            "pace": True,
        },
        "script": {
            "skill": _skill_path("script", args.skill_suffix),
            "target_minutes": args.minutes,
            "two_pass": True,
            "gate": {
                "comma_per_sentence": g.get("comma_per_sentence", [2.5, 6.0]),
                "chars_per_breath": g.get("chars_per_breath", [4.5, 9.0]),
                "dialogue_ratio_max": g.get("dialogue_ratio_max", 0.15),
                "require_next_ep_teaser": True,
            },
        },
        "image": {
            "skill": _skill_path("image", args.skill_suffix),
            "character_sheet": d.get("character_sheet", ""),
            "style_suffix": d.get("style_suffix", ""),
            "seconds_per_image": int(d.get("seconds_per_image") or 15),
            "ref_lock": True,
            "ref_quality": "low",
            "workers": 24,
            "qc_sample": 12,
        },
        "thumbnail": {
            "skill": _skill_path("thumbnail", args.skill_suffix),
            "palette": ["WHITE", "YELLOW", "RED"],
            "banner": d.get("thumbnail_banner", ""),
            "dedicated_bg": True,
            # Phong cách NỀN ảnh thumbnail, CỐ ĐỊNH cho cả kênh — user chốt 2026-09-10: "mỗi kênh
            # 1 phong cách thumbnail, chỉ thay ảnh và text". Rỗng = giữ hành vi cũ (photoreal điện
            # ảnh) để không phá kênh đang chạy. Đổi trong make_video.py b7_thumb().
            "art_style": args.thumb_style or "",
        },
        "assemble": {"zoom": 1.12, "transition": "xfade", "xfade": 0.6, "qc_sample": 12},
        "blocklist": bl,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--find", default="", help="chỉ TÌM GIỌNG theo mô tả tiếng Việt rồi thoát")
    ap.add_argument("--preview", default="", help="nghe thử 1 giọng rồi thoát")
    ap.add_argument("--id", default="", help="id profile, vd samurai-history-jp")
    ap.add_argument("--niche", default="")
    ap.add_argument("--market", default="JP")
    ap.add_argument("--lang", default="ja")
    ap.add_argument("--minutes", type=float, default=30)
    ap.add_argument("--persona", default="", help="mô tả người kể bằng tiếng Việt")
    ap.add_argument("--gender", default="")
    ap.add_argument("--voice", default="", help="tên/voice_id; bỏ trống = lấy gợi ý số 1")
    ap.add_argument("--fx", default="none")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--competitor", default="")
    ap.add_argument("--slug-dir", dest="slug_dir", default="assets/out")
    ap.add_argument("--skill-suffix", dest="skill_suffix", default="",
                    help="hậu tố skill, mặc định = id")
    ap.add_argument("--thumb-style", dest="thumb_style", default="",
                    help="phong cách NỀN thumbnail cố định cho cả kênh, vd 'Japanese manga/anime "
                        "illustration, cel-shaded flat colors, bold clean line art'. Bỏ trống = "
                        "giữ nguyên photoreal điện ảnh cũ (hoặc GIỮ giá trị đã có nếu đang --update)")
    ap.add_argument("--no-calibrate", action="store_true", help="bỏ bước đo char-rate (KHÔNG nên)")
    ap.add_argument("--yes", action="store_true", help="không hỏi lại, ghi đè nếu trùng id")
    ap.add_argument("--update", action="store_true",
                    help="CẬP NHẬT hồ sơ đã có: đổi ngách/người kể/giọng, GIỮ char-rate đã đo "
                         "nếu giọng-tốc độ-hiệu ứng-ngôn ngữ không đổi")
    a = ap.parse_args()

    if a.preview:
        return subprocess.call(_pycmd("voice_bank.py", "--preview", a.preview,
                                      "--fx", a.fx, "--speed", str(a.speed)))
    if a.find and not a.id:
        for i, item in enumerate(voice_bank.suggest(a.find, a.gender, limit=8), 1):
            sc, v = item if isinstance(item, tuple) else (0, item)   # suggest trả (điểm, giọng)
            print(f"{i:2d}. [{sc:4.1f}] {v.get('name','?'):36s} {v.get('gender','?'):7s} "
                  f"{v['voice_id']}")
        print("\n→ chọn 1 tên rồi chạy lại kèm --id --niche --persona --voice ... để tạo profile.")
        return 0

    for need in ("id", "niche", "persona"):
        if not getattr(a, need):
            raise SystemExit(f"Thiếu --{need}. Xem `--find \"<mô tả>\"` để chọn giọng trước.")
    a.skill_suffix = a.skill_suffix or a.id
    # Ghi vào NƠI GHI ĐƯỢC (cạnh exe), KHÔNG phải thư mục module: khi đóng gói, `HERE` là
    # `_internal` — thư mục bị xoá sạch mỗi lần build, và ở Program Files thì không ghi được.
    # Dùng chung một chỗ với profiles.py để tool đọc lại thấy ngay hồ sơ vừa lập.
    out = profiles.DIR / f"{a.id}.json"
    cu = None
    if out.exists():
        if not (a.yes or a.update):
            raise SystemExit(f"Đã có {out.name} — thêm --update để CẬP NHẬT (giữ char-rate đã đo) "
                             f"hoặc --yes để ghi đè hẳn.")
        if a.update:
            try:
                cu = json.loads(out.read_text(encoding="utf-8"))
                print(f"[0] CẬP NHẬT hồ sơ có sẵn '{a.id}' (giữ số đo tốc độ đọc nếu giọng không đổi)")
            except Exception as e:
                print(f"[0] không đọc được hồ sơ cũ ({e}) → tạo mới")

    # 1-2. giọng
    if a.voice:
        vid = voice_bank.resolve(a.voice)          # resolve() trả về voice_id (chuỗi)
        if isinstance(vid, tuple):
            vid = vid[1]
        if isinstance(vid, dict):
            v = vid
        else:
            v = next((x for x in voice_bank.load() if x.get("voice_id") == vid),
                     {"voice_id": vid, "name": a.voice})
        if not v.get("voice_id"):
            raise SystemExit(f"Không tìm ra giọng '{a.voice}'")
    else:
        cand = voice_bank.suggest(a.find or a.persona, a.gender, limit=1)
        if not cand:
            raise SystemExit("Không gợi ý được giọng nào — truyền --voice tường minh.")
        v = cand[0][1] if isinstance(cand[0], tuple) else cand[0]
    print(f"[1] Giọng: {v.get('name','?')} ({v['voice_id']}) · fx={a.fx} · speed={a.speed}")

    # 3. LLM dựng hồ sơ
    print("[2] Đang dựng hồ sơ nhân vật bằng LLM …")
    d = design(a.niche, a.market, a.lang, a.persona, a.minutes)
    prof = build(a, v, d)
    # Cập nhật kênh mà KHÔNG gõ lại --thumb-style → GIỮ phong cách cũ, đừng âm thầm xoá về rỗng
    # (cùng bài học với char_rate: build() luôn dựng dict MỚI TỪ ĐẦU, không tự merge).
    if not a.thumb_style and cu:
        cu_style = ((cu.get("thumbnail") or {}).get("art_style") or "").strip()
        if cu_style:
            prof["thumbnail"]["art_style"] = cu_style
            print(f"    (giữ phong cách thumbnail cũ: {cu_style[:60]}…)")

    # 4. ghi
    prof, giu = _giu_char_rate(prof, cu)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(prof, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[3] Đã ghi {out}")
    print(f"    người kể : {prof['narrator']['persona']}")
    print(f"    sheet    : {prof['image']['character_sheet'][:90]}")
    print(f"    gate     : {prof['script']['gate']['comma_per_sentence']} phẩy/câu · "
          f"hội thoại ≤{prof['script']['gate']['dialogue_ratio_max']:.0%}")

    dung_chung = [k for k in ("script", "image", "thumbnail")
                  if prof[k]["skill"] == _SKILL_CHUNG[k]]
    if dung_chung:
        print(f"    skill    : dùng bản CHUNG cho {', '.join(dung_chung)} — đầy đủ luật, ngách "
              f"lấy từ hồ sơ này. Chỉ cần viết skill riêng khi muốn tinh chỉnh sâu cho ngách.")
    thieu = [k for k in ("script", "image", "thumbnail") if not res(prof[k]["skill"]).exists()]
    if thieu:
        print(f"    ⚠️ KHÔNG tìm thấy file skill cho {', '.join(thieu)} — kiểm lại thư mục skills/")

    # 5. đo char-rate
    if a.no_calibrate:
        print("[4] BỎ QUA đo char-rate — nhớ chạy `calibrate.py --profile "
              f"{a.id}` trước khi làm video.")
        return 0
    if giu:
        print(f"[4] GIỮ char-rate đã đo: {prof['voice']['char_rate']} "
              f"(giọng/tốc độ/hiệu ứng/ngôn ngữ không đổi) — không cần đo lại.")
        print(f"\n✓ XONG. Làm video: py -3.13 make_video.py --profile {a.id} "
              f"--slug ep01 --competitor <video_id>")
        return 0
    print("[4] Đang đo char-rate thật (đọc thử 1 đoạn) …")
    rc = subprocess.call(_pycmd("calibrate.py", "--profile", a.id))
    if rc != 0:
        print("    ⚠️ đo không thành — chạy lại `calibrate.py --profile " + a.id + "`")
    else:
        print(f"    char_rate = {profiles.char_rate(profiles.load(a.id))}")
    print(f"\n✓ XONG. Làm video: py -3.13 make_video.py --profile {a.id} "
          f"--slug ep01 --competitor <video_id>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
