"""profiles.py — hồ sơ NHÂN VẬT/KÊNH: 1 nguồn chân lý cho cả 7 bước sản xuất.

Mỗi kênh = 1 file `pipeline/profiles/<id>.json` (schema ở `docs/PROFILE_ARCHITECTURE.md`).
Đọc được CẢ `channels.json` cũ (tự quy đổi) để lệnh/script cũ không vỡ.

Dùng:
  py -3.13 profiles.py --list
  py -3.13 profiles.py --show satori-jp-obaa

Import:
  import profiles
  p = profiles.load("satori-jp-obaa")
  voice, fx, speed = profiles.voice_conf(p)
  n_chars = profiles.target_chars(p)              # số chữ cần cho target_minutes theo char_rate ĐÃ ĐO
"""
import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent

# Tách NƠI ĐỌC khỏi NƠI GHI. Khi đóng exe, `HERE` là `_internal/` — thư mục BỊ XOÁ SẠCH mỗi lần
# build lại. Trước đây cả đọc lẫn ghi đều trỏ vào đó, nên: char_rate tool tự đo được sau mỗi video
# và profile người dùng tự tạo đều bay hết sau một lần build (đo thật 2026-09-09: exe học được
# char_rate 275.8 nhưng nằm trong bundle). Chưa kể máy khách cài vào Program Files thì thư mục đó
# không ghi được.
#   BUNDLED — bản đi kèm, CHỈ ĐỌC.
#   DIR     — bản ghi được, CẠNH exe; trùng tên thì bản này thắng.
# Lúc chạy từ mã nguồn hai đường này là MỘT (pipeline/profiles) nên hành vi không đổi.
from paths import res, DATA_DIR
BUNDLED = res("profiles")
DIR = DATA_DIR / "profiles"
LEGACY = HERE / "channels.json"


def _find(pid):
    """File profile của pid: ưu tiên bản ghi được cạnh exe, rồi tới bản đi kèm."""
    for d in (DIR, BUNDLED):
        f = d / f"{pid}.json"
        if f.exists():
            return f
    return None
DEFAULT_CHAR_RATE = 309.0        # chỉ dùng khi profile chưa đo — LUÔN nên đo bằng calibrate.py

# Ngưỡng nhịp văn mặc định (kiểu tâm tình/người già). Kênh khác PHẢI ghi gate riêng trong profile.
DEFAULT_GATE = {
    "comma_per_sentence": [2.5, 6.0],
    "chars_per_breath": [4.5, 9.0],
    "dialogue_ratio_max": 0.15,
    "require_next_ep_teaser": True,
}


def list_ids():
    ids = set()
    for d in (BUNDLED, DIR):                 # gộp bản đi kèm + bản người dùng thêm cạnh exe
        if d.exists():
            ids |= {p.stem for p in d.glob("*.json")}
    ids = sorted(ids)
    if LEGACY.exists():
        legacy = json.loads(LEGACY.read_text(encoding="utf-8"))
        ids += [k for k in legacy if not k.startswith("_") and k not in ids]
    return ids


def _from_legacy(cid, raw):
    """channels.json (phẳng: voice/age/speed) → schema profile mới."""
    return {
        "id": cid,
        "market": raw.get("market", ""),
        "language": raw.get("language", "ja"),
        "niche": raw.get("niche", ""),
        "competitor": raw.get("competitor", ""),
        "narrator": {"persona": raw.get("narrator", ""), "gender": "", "age_band": ""},
        "voice": {"id": raw.get("voice", ""), "speed": raw.get("speed", 0.95),
                  "fx": raw.get("age", "none"), "char_rate": raw.get("char_rate", 0)},
        "script": {"skill": raw.get("skill", "skills/youtube-script/SKILL.md"),
                   "target_minutes": raw.get("target_minutes", 30), "gate": dict(DEFAULT_GATE)},
        "image": {}, "thumbnail": {},
        "assemble": {"bgm": raw.get("bgm", "")},
        "blocklist": [],
        "_legacy": True,
        "slug_dir": raw.get("slug_dir", ""),
    }


def load(pid):
    """Nạp profile theo id — bản cạnh exe trước, rồi bản đi kèm, sau cùng channels.json cũ."""
    f = _find(pid)
    if f:
        p = json.loads(f.read_text(encoding="utf-8"))
        p.setdefault("id", pid)
        sc = p.setdefault("script", {})
        if not sc.get("gate"):
            # Đánh dấu là ĐI MƯỢN, để B3 biết mà chặn — xem gate_declared().
            sc["gate"] = dict(DEFAULT_GATE)
            sc["_gate_inherited"] = True
        return p
    if LEGACY.exists():
        legacy = json.loads(LEGACY.read_text(encoding="utf-8"))
        if pid in legacy:
            print(f"[profiles] '{pid}' còn ở channels.json (định dạng cũ) → nên chuyển sang profiles/{pid}.json")
            return _from_legacy(pid, legacy[pid])
    raise SystemExit(f"Không có profile '{pid}'. Có: {list_ids()}")


def save(prof):
    DIR.mkdir(parents=True, exist_ok=True)
    prof.pop("_legacy", None)
    # `ep_speed` chỉ đúng cho MỘT tập — ghi vào hồ sơ kênh là các tập sau tính sai độ dài.
    (prof.get("voice") or {}).pop("ep_speed", None)
    f = DIR / f"{prof['id']}.json"
    f.write_text(json.dumps(prof, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ Ghi profile: {f}")
    return f


DA_GIONG_PROVIDERS = ("voicevox", "ai33")


def da_giong(prof):
    """Lane ĐA GIỌNG (mỗi câu một giọng theo vai.txt → tts_voicevox.chay): voice.provider = "voicevox" (Lane K,
    engine local) hoặc "ai33" (Lane L 2026-09-24, OpenSpeaker/MiniMax — kênh mẫu không phải VOICEVOX).
    Lane một giọng không khai provider → False, đường tts.py cũ y nguyên."""
    return ((prof.get("voice") or {}).get("provider") or "") in DA_GIONG_PROVIDERS


def voice_conf(prof):
    v = prof.get("voice", {}) or {}
    return v.get("id", ""), v.get("fx", "none"), float(v.get("speed", 0.95) or 0.95)


def char_rate(prof):
    r = float((prof.get("voice", {}) or {}).get("char_rate", 0) or 0)
    if r <= 0:
        print(f"⚠️ profile '{prof.get('id')}' CHƯA đo char-rate → tạm dùng {DEFAULT_CHAR_RATE}. "
              f"Chạy: py -3.13 calibrate.py --profile {prof.get('id')}")
        return DEFAULT_CHAR_RATE
    return r


# ---------------------------------------------------------------- hàng rào ĐA KÊNH
# Từ khi dự án chạy NHIỀU NGÁCH cùng lúc (satori người già + 都市伝説), hai giá trị mặc định
# dưới đây trở thành BẪY SAI CÂM LẶNG: kênh mới quên khai thì vẫn chạy trơn tru rồi ra kịch bản
# mang nhịp văn và độ dài của kênh CŨ. Đo thật ở satori: dùng nhầm char_rate lệch 20% = kịch bản
# "30 phút" ra 44 phút, phải viết lại (mất 1 lượt B3 + 1 lượt TTS ~1.400đ).
#   · char_rate  : mỗi giọng một số, chênh tới 39% giữa các giọng (docs/PROFILE_ARCHITECTURE.md §1)
#   · gate       : DEFAULT_GATE là nhịp TÂM TÌNH (cụ bà), ngách kể tài liệu cần nhịp DỒN
# Hai hàm này để nơi gọi (make_video B1/B3) CHẶN CỨNG thay vì lặng lẽ mượn số của kênh khác.

def rate_measured(prof):
    """char_rate đã ĐO THẬT cho chính giọng này chưa (≠ số tạm mặc định)."""
    v = prof.get("voice", {}) or {}
    return bool(v.get("char_rate_measured_at")) and float(v.get("char_rate", 0) or 0) > 0


def gate_declared(prof):
    """Profile có tự khai ngưỡng nhịp văn riêng chưa (≠ mượn DEFAULT_GATE của satori)."""
    sc = prof.get("script", {}) or {}
    return bool(sc.get("gate")) and not sc.get("_gate_inherited")


def target_minutes(prof):
    return float((prof.get("script", {}) or {}).get("target_minutes", 30))


def char_rate_speed(prof):
    """Tốc độ đọc mà char_rate được ĐO Ở ĐÓ (mặc định: tốc độ ghi trong hồ sơ)."""
    v = prof.get("voice", {}) or {}
    return float(v.get("char_rate_speed") or v.get("speed") or 0.95)


def char_rate_at(prof, speed=None):
    """char_rate quy đổi sang TỐC ĐỌC THẬT của tập này.

    Số chữ đọc được mỗi phút tỉ lệ thuận với tốc độ. Từ khi mỗi tập tự chọn giọng theo tuổi
    người kể, tốc độ chạy từ 0.90 (cụ già) tới 1.00 (người trẻ) — chênh 11%. Dùng chung một
    char_rate đo ở 0.92 thì tập giọng nhanh bị viết THIẾU ~8% chữ, ra video ngắn hơn video gốc.
    """
    r = char_rate(prof)
    # `ep_speed` do make_video gắn vào BẢN SAO hồ sơ của tập; nhờ vậy mọi chỗ gọi target_chars()
    # tự lấy đúng tốc độ của tập mà không phải sửa từng lời gọi.
    # 2026-10-01: lane đổi voice.speed (vd kênh người già 0.95→0.90) mà giữ char_rate đo ở tốc độ cũ → cũng quy đổi.
    v = prof.get("voice", {}) or {}
    speed = speed or v.get("ep_speed") or v.get("speed")
    if not speed:
        return r
    goc = char_rate_speed(prof)
    return round(r * (float(speed) / goc), 1) if goc else r


def target_chars(prof, minutes=None, speed=None):
    """Số chữ (không tính space/xuống dòng) cần để đọc đủ số phút — theo giọng VÀ tốc độ tập này."""
    return int(round(char_rate_at(prof, speed) * (minutes or target_minutes(prof))))


def gate(prof):
    g = dict(DEFAULT_GATE)
    g.update((prof.get("script", {}) or {}).get("gate", {}) or {})
    return g


ASSETS_MAC_DINH = ["characters.json", "img_prompts.txt", "img_doan.txt",
                   "thumb_text.txt", "TIEU_DE_MO_TA.txt"]


def assets_need(prof):
    """File asset BẮT BUỘC của pha "assets" cho lane này.

    `profile.assets.skip` = danh sách file KHÔNG phải làm ở lane đó (vd lane satori 2026-09-19: tiêu đề/
    mô tả + thumbnail do dự án khác lo ⇒ skip `TIEU_DE_MO_TA.txt` + `thumb_text.txt`). Không khai =
    giữ nguyên như cũ. Khai ở PROFILE chứ không `if profile_id` — xem hàng rào chống lẫn lane #2."""
    skip = set((prof.get("assets") or {}).get("skip") or [])
    return [f for f in ASSETS_MAC_DINH if f not in skip]


def narrator_line(prof):
    n = prof.get("narrator", {}) or {}
    bits = [n.get("persona", ""), n.get("gender", ""), n.get("age_band", ""), n.get("register", "")]
    return " · ".join(b for b in bits if b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--show", default="")
    args = ap.parse_args()
    if args.show:
        p = load(args.show)
        print(json.dumps(p, ensure_ascii=False, indent=2))
        print(f"\n→ char_rate={char_rate(p)} · target {target_minutes(p)}' = {target_chars(p)} chữ")
        return
    for pid in list_ids():
        p = load(pid)
        v, fx, sp = voice_conf(p)
        print(f"{pid:22s} {p.get('language','?'):3s} voice={v[:34]:34s} fx={fx:9s} speed={sp} "
              f"rate={(p.get('voice',{}) or {}).get('char_rate') or '(chưa đo)'} · {narrator_line(p)[:40]}")


if __name__ == "__main__":
    main()
