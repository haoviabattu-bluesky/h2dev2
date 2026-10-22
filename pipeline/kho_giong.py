# -*- coding: utf-8 -*-
r"""kho_giong.py — chọn giọng nhân vật theo KHO GIỌNG CHUNG (khung tuổi × giới), cấm vai già lấy giọng trẻ.

Vì sao (anh 22/10/2026): tập nào cũng phải đi tìm giọng + bắt anh duyệt lại, cụ bà cứ bị gán giọng trẻ
(Nữ C, もち子さん…) vì cast_bank của lane xếp theo VAI chứ không theo TUỔI. Kho `kho_giong.json` gom mọi giọng đã
làm/anh đã chốt, mỗi giọng khai khoảng tuổi nghe đúng. Máy tự điền/sửa `characters.json[].voice`:
  - vai chưa có voice → lấy từ kho;
  - voice đang khai không hợp tuổi/giới (hoặc nằm ngoài kho, hoặc dính danh sách `cam`) → thay bằng giọng kho;
  - voice hợp → giữ; vai ≥65 chưa khai speed → 0.85.
Giữ nguyên ý anh: voice có `"giu": true` (anh tự chốt giọng ngoài kho) → không đụng, trừ khi dính `cam`.
Người kể `ke` dùng đúng giọng người kể của profile → không đụng (màu kênh).

Ưu tiên khi chọn: giọng lane đang dùng (giữ màu kênh) → anh đã duyệt → đã dùng → dự phòng; chưa ai trong tập dùng;
tuổi gần giữa khoảng. Giọng `chi_khi_tu_khoa` (quát/hách dịch) chỉ chọn khi vai/name chứa từ khoá.

Gọi tự động: gan_vai.py (sau khi viết characters.json), tools\hook_lane_g\xem_thu_hook_giong.py, tts_voicevox.py.
CLI:
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.py --profile <mã lane> --tap <thư mục tập>        # kiểm + sửa
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.py --profile <mã lane> --tap <thư mục tập> --chi-xem
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.py --soat            # quét mọi tập mọi lane, chỉ báo
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.py --bang            # in kho theo khung tuổi
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kho_giong.py --them --ma F_gia_xxx --voice-id clone_123 --gioi F --tuoi 65-90 --ten "..." [--speed 0.85 --fx old-mild --lane <mã> --nguon "..."]
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KHO = HERE / "kho_giong.json"
sys.stdout.reconfigure(encoding="utf-8")

DIEM_DUYET = {"anh": 2.0, "da_dung": 1.0, "du_phong": 0.0}


def nap():
    return json.loads(KHO.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- chuẩn hoá dữ liệu nhân vật
def tuoi_cua(c):
    a = c.get("age")
    if isinstance(a, (int, float)):
        return int(a)
    m = re.search(r"\d+", str(a or ""))
    if not m:
        return None
    n = int(m.group())
    return n + 5 if re.search(r"\d+\s*代", str(a)) else n     # "50代" → 55


def gioi_cua(c):
    g = str(c.get("gender") or "").strip().lower()
    if g in ("m", "male", "nam", "男", "男性"):
        return "M"
    if g in ("f", "female", "nu", "nữ", "女", "女性"):
        return "F"
    return None


def fx_chuoi(fx):
    """'old-mild+punch' → chuỗi lọc ffmpeg thô (characters.json voice.fx là chuỗi thô, tts_voicevox.ap_fx dùng thẳng)."""
    if not fx:
        return ""
    from tts import VOICE_FX
    return ",".join(VOICE_FX[x] for x in fx.split("+") if VOICE_FX.get(x))


def _provider_duoc(prof):
    v = prof.get("voice") or {}
    p = (v.get("provider") or "").lower()
    if p == "voicevox":
        return {"voicevox", "ai33"} if v.get("ai33_cho_vai") else {"voicevox"}
    return {"ai33"} if p == "ai33" else set()


def _khoa(v):
    """voice dict → khoá so sánh: voice_id hoặc speaker/style."""
    if v.get("voice_id"):
        return v["voice_id"]
    return f"VV:{v.get('speaker')}/{v.get('style') or 'ノーマル'}" if v.get("speaker") else ""


def _khoa_kho(e):
    return e["voice_id"] if e["provider"] == "ai33" else f"VV:{e['speaker']}/{e.get('style') or 'ノーマル'}"


def _gioi_hop(e, g):
    return g in e["gioi"]


def _dinh_cam(kho, v, g, t):
    for x in kho.get("cam", []):
        if x.get("voice_id") and x["voice_id"] != v.get("voice_id"):
            continue
        if x.get("speaker") and x["speaker"] != v.get("speaker"):
            continue
        if not (x.get("voice_id") or x.get("speaker")):
            continue
        if x.get("gioi") and x["gioi"] != g:
            continue
        if t < x.get("tu_tuoi", 0) or t > x.get("den_tuoi", 999):
            continue
        return x["ly_do"]
    return ""


def _dung_tuoi(e, t, noi=True):
    """Tuổi t có hợp khoảng tuổi của giọng không. noi=True: dưới 60 cho lệch ±8 (người lớn lệch vài tuổi nghe vẫn đúng),
    từ 60 chỉ ±3 — vai già phải là giọng già thật (lỗi anh chê: cụ bà 72/86/88 bị giọng trẻ)."""
    du = (8 if t < 60 else 3) if noi else 0
    return e["tuoi"][0] - du <= t <= e["tuoi"][1] + du


def _hop_kho(kho, v, g, t):
    """voice đang khai có khớp 1 mục kho đúng tuổi/giới không (mục có fx thì voice phải có fx)."""
    k = _khoa(v)
    for e in kho["giong"]:
        if _khoa_kho(e) != k or not _gioi_hop(e, g):
            continue
        if not _dung_tuoi(e, t):
            continue
        if e.get("fx") and not v.get("fx"):
            continue
        return e
    return None


def chon(kho, prof, c, da_dung=(), loai_tru=(), nai=False):
    """→ mục kho tốt nhất cho nhân vật c (hoặc None). Đúng khoảng tuổi trước; không có mới nới (nai=True)."""
    g, t = gioi_cua(c), tuoi_cua(c)
    pid = prof.get("id", "")
    pv = _provider_duoc(prof)
    chu = f"{c.get('name', '')} {c.get('vai', '')}"
    ke_kenh = _khoa((prof.get("voice") or {}).get("narrator") or {})
    best = None
    for e in kho["giong"]:
        if e["provider"] not in pv or not _gioi_hop(e, g) or not _dung_tuoi(e, t, noi=nai):
            continue
        if _khoa_kho(e) in loai_tru:
            continue
        khop_tk = any(k in chu for k in e.get("tu_khoa", []))
        if e.get("chi_khi_tu_khoa") and not khop_tk:
            continue
        diem = DIEM_DUYET.get(e.get("duyet"), 0)
        diem += 4 if khop_tk else 0
        diem += 3 if pid in e.get("lanes", []) else (0.5 if not e.get("lanes") else 0)
        diem += 1.5 if _khoa_kho(e) not in da_dung else 0
        diem -= abs(t - sum(e["tuoi"]) / 2) / 20
        if c.get("id") != "ke" and _khoa_kho(e) == ke_kenh:
            diem -= 3                 # vai khác trùng giọng người kể → nghe lẫn với lời kể
        if best is None or diem > best[0]:
            best = (diem, e)
    if best is None and not nai:
        return chon(kho, prof, c, da_dung, loai_tru, nai=True)
    return best[1] if best else None


def voice_tu_kho(e, ghi_chu):
    v = {"voice_id": e["voice_id"]} if e["provider"] == "ai33" else {"speaker": e["speaker"], "style": e.get("style") or "ノーマル"}
    if e.get("speed") is not None:
        v["speed"] = e["speed"]
    if e.get("fx"):
        v["fx"] = fx_chuoi(e["fx"])
    v["kho"] = e["ma"]
    v["_note"] = ghi_chu
    return v


def _giong_co_dinh(prof, c):
    """Người kể `ke` = giọng người kể profile, hoặc vai cố định xuyên tập (voice.fixed_cast[id]) đúng giọng khai → màu kênh, không đụng."""
    pv = prof.get("voice") or {}
    k = _khoa(c.get("voice") or {})
    if not k:
        return False
    if c.get("id") == "ke" and k == _khoa(pv.get("narrator") or {}):
        return True
    fc = (pv.get("fixed_cast") or {}).get(c.get("id"))
    return isinstance(fc, dict) and k == _khoa(fc)


# ---------------------------------------------------------------- kiểm + sửa 1 tập
def ap_dung(prof, chars_path, sua=True, in_ra=True):
    """→ (danh sách đổi, danh sách lỗi chặn, danh sách cảnh báo). sua=True thì ghi lại characters.json."""
    import datetime
    kho = nap()
    if not _provider_duoc(prof):
        return [], [], []          # lane 1 giọng: không có giọng vai
    p = Path(chars_path)
    d = json.loads(p.read_text(encoding="utf-8"))
    chars = d.get("characters") or []
    doi, loi, canh = [], [], []
    da_dung = set()
    toc = kho.get("toc_do_gia") or {}
    hom_nay = datetime.date.today().isoformat()
    # lane đã đọc chậm sẵn (voice.speed ≤0.9, vd Lane F) → không tự hạ thêm cho vai già đang có giọng hợp
    cham_lane = float((prof.get("voice") or {}).get("speed") or 1.0) > 0.9
    # lượt 1: giữ chỗ cho giọng đang hợp → lượt 2 chọn giọng cho vai sai sẽ né giọng đã có chủ
    xet = []
    for c in chars:
        v = c.get("voice")
        if not v:
            continue
        g, t = gioi_cua(c), tuoi_cua(c)
        ten = f"{c.get('id')} {c.get('name', '')}".strip()
        if g is None or t is None:
            canh.append(f"{ten}: thiếu age/gender → không kiểm được tuổi giọng (vai nhóm? tách riêng vai già ra để có giọng già)")
            da_dung.add(_khoa(v))
            continue
        cam = _dinh_cam(kho, v, g, t)
        if not cam and (_giong_co_dinh(prof, c) or v.get("giu")):
            da_dung.add(_khoa(v))
            continue
        e = None if cam else _hop_kho(kho, v, g, t)
        if e:
            da_dung.add(_khoa(v))
            if t >= toc.get("tu_tuoi", 999) and "speed" not in v and cham_lane:
                v["speed"] = e.get("speed", toc["speed"])
                doi.append(f"{ten} ({g},{t}): giữ {e['ten']}, thêm speed {v['speed']} (vai ≥{toc['tu_tuoi']})")
            continue
        ly_do = cam or ("giọng ngoài kho" if not any(_khoa_kho(x) == _khoa(v) for x in kho["giong"])
                        else "giọng không hợp tuổi/giới này")
        xet.append((c, g, t, ten, ly_do))
    # người kể ngôi 1 `ke` (name「語り（林房江・一人称）」) và chính nhân vật đó = CÙNG MỘT NGƯỜI → cùng giọng
    by_id = {c.get("id"): c for c in chars}
    ke = by_id.get("ke")
    cung = {}
    if ke:
        for c in chars:
            n = re.sub(r"[（(].*", "", str(c.get("name") or "")).strip()
            if c is not ke and n and n in str(ke.get("name") or ""):
                cung[c.get("id")], cung["ke"] = "ke", c.get("id")
                break
    xet.sort(key=lambda x: x[0].get("id") != "ke")
    for c, g, t, ten, ly_do in xet:
        cu = _khoa(c["voice"])
        ban = by_id.get(cung.get(c.get("id")))
        if ban and ban.get("voice") and not _dinh_cam(kho, ban["voice"], g, t) and _hop_kho(kho, ban["voice"], g, t):
            c["voice"] = dict(ban["voice"], _note=f"{hom_nay} kho_giong: cùng người với {ban.get('id')} → cùng giọng")
            doi.append(f"{ten} ({g},{t}): {cu} → giọng của {ban.get('id')} (cùng một người) — lý do: {ly_do}")
            continue
        e = chon(kho, prof, c, da_dung, loai_tru={cu} if ly_do != "giọng ngoài kho" else set())
        if not e:
            loi.append(f"{ten} ({g},{t}): {cu} sai ({ly_do}) và kho KHÔNG có giọng {g} {t} tuổi cho lane này"
                       + (" — lane VOICEVOX: bật voice.ai33_cho_vai trong profile để dùng giọng già ai33" if "voicevox" in _provider_duoc(prof) and "ai33" not in _provider_duoc(prof) else "")
                       + f" → thêm giọng vào {KHO}")
            continue
        sp = e.get("speed")
        if sp is None and t >= toc.get("tu_tuoi", 999):
            e = dict(e, speed=toc["speed"])
        c["voice"] = voice_tu_kho(e, f"{hom_nay} kho_giong: {cu} bị thay ({ly_do}) → {e['ten']}")
        da_dung.add(_khoa_kho(e))
        doi.append(f"{ten} ({g},{t}): {cu} → {e['ten']} [{e['ma']}] — lý do: {ly_do}")
    if sua and doi:
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if in_ra:
        for x in doi:
            print(f"  [kho_giong] {'ĐỔI' if sua else 'SẼ ĐỔI'} {x}")
        for x in canh:
            print(f"  [kho_giong] ! {x}")
        for x in loi:
            print(f"  [kho_giong] ✗ {x}")
        if not (doi or loi):
            print(f"  [kho_giong] ✓ giọng mọi vai hợp tuổi/giới ({p})")
    return doi, loi, canh


def chan(prof, chars_path):
    """Dùng trong pipeline: sửa tại chỗ; còn vai không có giọng hợp → DỪNG."""
    _, loi, _ = ap_dung(prof, chars_path, sua=True)
    if loi:
        raise SystemExit("✗ kho_giong: còn vai không có giọng hợp tuổi — " + " | ".join(loi))


# ---------------------------------------------------------------- CLI
def _prof(pid):
    import profiles
    return profiles.load(pid)


def _soat():
    import profiles
    tong = 0
    for pid in sorted(profiles.list_ids()):
        if pid.startswith(("zz-", "_")):
            continue
        prof = _prof(pid)
        if not _provider_duoc(prof) or not prof.get("slug_dir"):
            continue
        lane_dir = HERE.parent / prof["slug_dir"]      # slug_dir tương đối gốc dự án
        if not lane_dir.exists():
            continue
        for cf in sorted(lane_dir.glob("ep*/characters.json")):
            doi, loi, _ = ap_dung(prof, cf, sua=False, in_ra=False)
            if doi or loi:
                tong += 1
                print(f"\n{cf}")
                for x in doi + loi:
                    print("   -", x)
    print(f"\n→ {tong} tập có vai lệch tuổi giọng (CHỈ BÁO, chưa sửa).")


def _bang():
    kho = nap()
    for ten, (a, b) in kho["khung_tuoi"].items():
        print(f"\n== {ten} ({a}–{b} tuổi)")
        for g in ("F", "M"):
            ds = [e for e in kho["giong"] if g in e["gioi"] and e["tuoi"][0] <= b and e["tuoi"][1] >= a]
            for e in ds:
                print(f"   {g} {e['provider']:8} {_khoa_kho(e):38} {e['tuoi'][0]}-{e['tuoi'][1]:<3} {e.get('duyet', ''):8} {e['ten']}")


def _them(a):
    kho = nap()
    lo, hi = (int(x) for x in a.tuoi.split("-"))
    e = {"ma": a.ma, "provider": "voicevox" if a.speaker else "ai33", "ten": a.ten, "gioi": a.gioi, "tuoi": [lo, hi],
         "lanes": [a.lane] if a.lane else [], "duyet": a.duyet, "nguon": a.nguon}
    if a.speaker:
        e.update(speaker=a.speaker, style=a.style or "ノーマル")
    else:
        e["voice_id"] = a.voice_id
    if a.speed:
        e["speed"] = a.speed
    if a.fx:
        e["fx"] = a.fx
    kho["giong"] = [x for x in kho["giong"] if x["ma"] != a.ma] + [e]
    KHO.write_text(json.dumps(kho, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ thêm/cập nhật {a.ma} vào {KHO}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile")
    ap.add_argument("--tap", help="thư mục tập (chứa characters.json)")
    ap.add_argument("--chi-xem", action="store_true")
    ap.add_argument("--soat", action="store_true")
    ap.add_argument("--bang", action="store_true")
    ap.add_argument("--them", action="store_true")
    for k in ("ma", "voice_id", "speaker", "style", "gioi", "tuoi", "ten", "fx", "lane", "nguon"):
        ap.add_argument(f"--{k.replace('_', '-')}", default="")
    ap.add_argument("--speed", type=float, default=0)
    ap.add_argument("--duyet", default="anh")
    a = ap.parse_args()
    if a.bang:
        return _bang()
    if a.soat:
        return _soat()
    if a.them:
        if not (a.ma and (a.voice_id or a.speaker) and a.gioi and a.tuoi and a.ten):
            raise SystemExit("--them cần --ma --voice-id|--speaker --gioi --tuoi --ten")
        return _them(a)
    if not (a.profile and a.tap):
        raise SystemExit("cần --profile <mã lane> --tap <thư mục tập> (hoặc --soat / --bang / --them)")
    doi, loi, _ = ap_dung(_prof(a.profile), Path(a.tap) / "characters.json", sua=not a.chi_xem)
    if loi:
        sys.exit(1)


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    main()
