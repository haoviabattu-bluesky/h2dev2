#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""kiem_hook_goc.py — CỔNG "CÓ HOOK GỐC MỚI ĐƯỢC DỰNG" (anh chốt 2026-10-21, mọi lane).

Vì sao: Lane L ep23 — YouTube chặn tải phụ đề video gốc (429) → máy không có cấu trúc hook gốc → hook_stage viết TỰ DO →
hook về 佐野稔 51 tuổi bảo vệ, không theo nhịp gốc, họ 佐野 đã dùng ở ep04. Từ nay:
  1. Không có lời 0–150s của video gốc (→ không tách được cấu trúc hook) = KHÔNG viết hook, KHÔNG dựng tập.
  2. Kiểm TRƯỚC khi chạy (chay_lo_tap.py gọi ở bước chuẩn bị) — tập thiếu hook gốc bị loại khỏi lô, không mở claude -p.
  3. Hook đã khoá mà không có cấu trúc gốc / dùng lại họ tên nhân vật tập trước → chặn ở chặng hook/giao máy 2.

Nguồn lời gốc (theo thứ tự, dừng ở nguồn đầu tiên đủ): competitor.segments.json của tập → hook\source_segments.json →
TRENDING-RESEARCH\data\**\transcripts\<id>.json → cache dự án data\loi_goc\<id>.json → mạng (youtube-transcript-api →
phụ đề yt-dlp → whisper nghe 30MB audio, đường whisper không dính 429). Tải được từ mạng thì lưu cache data\loi_goc.

Dùng:
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kiem_hook_goc.py --tap <thư mục tập tuyệt đối>
  py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\kiem_hook_goc.py --profile shakai_no_naze --tu 23 --den 26
  ... --khong-mang      chỉ xét nguồn có sẵn ở máy (không gọi YouTube)
  ... --khong-whisper   không dùng đường whisper (nhanh hơn, dễ trượt khi 429)
Mã thoát: 0 = mọi tập đủ hook gốc · 2 = có tập thiếu (tập đó CẤM chạy kịch bản/hook).
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
TRENDING_DATA = Path(r"E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data")
CACHE = ROOT / "data" / "loi_goc"
GIAY_LOI_GOC = 150.0
# Lời gốc "đủ" để tách cấu trúc hook: có lời bắt đầu trong 15s đầu, phủ tới ≥ 30s, ≥ 5 đoạn.
GIAY_BAT_DAU_TOI_DA = 15.0
GIAY_PHU_TOI_THIEU = 30.0
SO_DOAN_TOI_THIEU = 5
# Nhân vật có mặt ở ≥ ngần này tập = vai cố định của lane (người dẫn…) → được dùng lại.
SO_TAP_VAI_CO_DINH = 3
# Vai (không phải tên riêng) trong characters.json: 同僚 / 営業部長 / 婚姻届を出す若い男 / 男性客・店員 / 看護師 / 班長 / 長女…
VAI_TRO = re.compile(r"[のをがに]|たち|マン|[員官師客者僚職]|部下|部長|社員|社長|担当|入居|会員|^(男性|女性|新人|若手|家族|元)"
                     r"|^.{1,2}[長女男娘母父]$")
ID_PAT = re.compile(r"(?:v=|/shorts/|/embed/|youtu\.be/)([A-Za-z0-9_-]{11})")


# ── lời video gốc ───────────────────────────────────────────────────────────
def id_video(tap=None, *chu):
    """Mã video gốc: video_goc.json của tập trước, rồi URL YouTube trong các chuỗi `chu` (cột K/B sheet). Không có → ''."""
    if tap:
        try:
            v = json.loads((Path(tap) / "video_goc.json").read_text(encoding="utf-8")).get("video_goc") or {}
            if (v.get("id") or "").strip():
                return v["id"].strip()
        except (OSError, ValueError, AttributeError):
            pass
    for s in chu:
        m = ID_PAT.search(s or "")
        if m:
            return m.group(1)
    return ""


def _chuan(segs):
    out = []
    for s in segs or []:
        txt = re.sub(r"\s+", " ", str(s.get("text", ""))).strip()
        if not txt:
            continue
        st = float(s.get("start", 0))
        du = float(s.get("duration", float(s.get("end", st)) - st))
        out.append({"start": st, "duration": max(0.0, du), "text": txt})
    return out


def danh_gia(segs):
    """Lời gốc có đủ để tách cấu trúc hook không. Trả (ok, mô tả)."""
    segs = [s for s in _chuan(segs) if s["start"] < GIAY_LOI_GOC]
    if not segs:
        return False, "không có đoạn lời nào trong 0–150s"
    dau, cuoi = segs[0]["start"], segs[-1]["start"] + segs[-1]["duration"]
    if dau > GIAY_BAT_DAU_TOI_DA:
        return False, f"lời bắt đầu muộn ở {dau:.0f}s (thiếu phần mở hook)"
    if cuoi < GIAY_PHU_TOI_THIEU or len(segs) < SO_DOAN_TOI_THIEU:
        return False, f"lời quá ngắn ({len(segs)} đoạn, tới {cuoi:.0f}s)"
    return True, f"{len(segs)} đoạn, {dau:.0f}–{cuoi:.0f}s"


def _doc_segs(p):
    j = json.loads(Path(p).read_text(encoding="utf-8"))
    return j if isinstance(j, list) else (j.get("segments") or [])


def tim_loi(vid, tap=None, proxy=None, tai_mang=True, whisper=True):
    """Tìm lời 0–150s video gốc. Trả (segments, nguồn) — không có thì ([], lý do các đường đã thử). Không bao giờ ném."""
    thu = []
    ung_vien = []
    if tap:
        ung_vien += [(Path(tap) / "competitor.segments.json", "competitor.segments.json"),
                     (Path(tap) / "hook" / "source_segments.json", "hook\\source_segments.json")]
    if vid:
        ung_vien += [(f, f"TRENDING:{f.parent.parent.name}") for f in sorted(TRENDING_DATA.glob(f"**/transcripts/{vid}.json"))]
        ung_vien.append((CACHE / f"{vid}.json", "cache data\\loi_goc"))
    for p, ten in ung_vien:
        if not p.exists():
            continue
        try:
            segs = _doc_segs(p)
        except (OSError, ValueError) as e:
            thu.append(f"{ten} hỏng ({type(e).__name__})")
            continue
        ok, mo_ta = danh_gia(segs)
        if ok:
            return _chuan(segs), ten
        thu.append(f"{ten}: {mo_ta}")
    if not vid:
        return [], "không có mã video gốc (video_goc.json / URL ở cột K)"
    if not tai_mang:
        return [], " · ".join(thu) or "không có lời gốc ở máy (đã tắt tải mạng)"
    import fetch_script
    duong = [("api", lambda: fetch_script.via_api(vid, ["ja", "ja-JP", "en"], proxy=proxy)),
             ("ytdlp", lambda: fetch_script.via_ytdlp_subs(vid, ["ja", "en"], Path(tempfile.mkdtemp(prefix="hookgoc_")),
                                                           proxy=proxy))]
    if whisper:
        duong.append(("whisper", lambda: fetch_script.via_whisper(vid, ["ja"], Path(tempfile.mkdtemp(prefix="hookgoc_")),
                                                                  proxy=proxy)))
    for ten, ham in duong:
        try:
            segs = ham()
        except BaseException as e:   # noqa: BLE001 — via_* có thể SystemExit; cổng không được chết theo
            thu.append(f"{ten}: {type(e).__name__} {' '.join(str(e).split())[:80]}")
            continue
        ok, mo_ta = danh_gia(segs)
        if ok:
            segs = [s for s in _chuan(segs) if s["start"] < GIAY_LOI_GOC]
            CACHE.mkdir(parents=True, exist_ok=True)
            (CACHE / f"{vid}.json").write_text(json.dumps({"video_id": vid, "source": ten, "segments": segs},
                                                          ensure_ascii=False, indent=1), encoding="utf-8")
            return segs, ten
        thu.append(f"{ten}: {mo_ta}")
    return [], " · ".join(thu)


def doc_hook_goc_json(tap, vid=""):
    """`<tập>/hook_goc.json` do TRENDING-RESEARCH giao (đơn YEU_CAU_TU_H2DEV_2026-10-21_HOOK_GOC_BAT_BUOC.md) — cùng khuôn
    cau_truc_hook của hook_stage. Hợp lệ (khớp mã video, ≥2 nhịp, mỗi nhịp có tu/den/vai_tro/cau_goc) → dict, ngược lại None."""
    if not tap:
        return None
    try:
        j = json.loads((Path(tap) / "hook_goc.json").read_text(encoding="utf-8"))
        ct = j.get("cau_truc_hook") or j
        nhip = ct.get("nhip") or []
        if vid and j.get("video_id") and j["video_id"] != vid:
            return None
        if (len(nhip) >= 2 and str(ct.get("mo_dau", "")).strip() and float(ct.get("giay_ket_hook") or 0) > 0
                and all(str(n.get("vai_tro", "")).strip() and str(n.get("cau_goc", "")).strip()
                        and float(n.get("den", 0)) > float(n.get("tu", 0)) for n in nhip)):
            return ct
    except (OSError, ValueError, AttributeError, TypeError):
        pass
    return None


# ── họ tên nhân vật đã dùng ─────────────────────────────────────────────────
def _ho(ten):
    """Họ (hoặc tên kanji) để so trùng: 「佐野 稔」/「佐野稔」→ 佐野. Tên toàn kana (さくら) / 1 chữ → None."""
    ten = re.sub(r"[（(].*?[）)]", "", str(ten or "")).strip()
    if VAI_TRO.search(ten):
        return None
    dau = re.split(r"[\s　・]", ten)[0]
    m = re.match(r"[\u4e00-\u9fff々]{2,}", dau)
    if not m or re.fullmatch(r"[一二三四五六七八九十百千万]+", m.group(0)[:2]):   # 五十嵐 → '五十' khớp nhầm 五十一歳
        return None
    return m.group(0)[:2]


def ho_da_dung(tap, slug_dir=None):
    """{họ: [tập đã dùng]} của các tập KHÁC cùng lane (characters.json), bỏ vai cố định (có mặt ≥ SO_TAP_VAI_CO_DINH tập)."""
    tap = Path(tap) if tap else None
    sd = Path(slug_dir) if slug_dir else (tap.parent if tap else None)
    if not sd or not sd.exists():
        return {}
    dem = {}
    for f in sorted(sd.glob("*/characters.json")):
        try:
            cs = json.loads(f.read_text(encoding="utf-8")).get("characters", [])
        except (OSError, ValueError, AttributeError):
            continue
        ep = f.parent.name.split("-")[0]
        for c in cs if isinstance(cs, list) else []:
            h = _ho((c or {}).get("name"))
            if h:
                dem.setdefault(h, set()).add((f.parent, ep))
    out = {}
    for h, s in dem.items():
        if len(s) >= SO_TAP_VAI_CO_DINH:
            continue
        khac = sorted(ep for p, ep in s if not tap or p.resolve() != tap.resolve())
        if khac:
            out[h] = khac
    return out


def ho_trung(text, cam):
    """Các họ trong `cam` xuất hiện trong text → list chuỗi mô tả."""
    return [f"{h} (đã dùng ở {','.join(e)})" for h, e in sorted(cam.items()) if h in (text or "")]


# ── cổng ─────────────────────────────────────────────────────────────────────
def kiem_nguon(tap=None, *chu, proxy=None, tai_mang=True, whisper=True):
    """Bước chuẩn bị (trước chặng kịch bản): tập có lời hook gốc đủ để tách cấu trúc không."""
    vid = id_video(tap, *chu)
    if doc_hook_goc_json(tap, vid):
        return {"ok": True, "video_id": vid, "nguon": "hook_goc.json (TRENDING-RESEARCH)", "ly_do": "",
                "so_doan": len(doc_hook_goc_json(tap, vid)["nhip"])}
    segs, nguon = tim_loi(vid, tap, proxy=proxy, tai_mang=tai_mang, whisper=whisper)
    return {"ok": bool(segs), "video_id": vid, "nguon": nguon if segs else "",
            "ly_do": "" if segs else f"KHÔNG CÓ HOOK GỐC — {nguon}", "so_doan": len(segs)}


def kiem_hook_da_khoa(tap):
    """Chặng hook/giao máy 2: hook đã khoá phải có cấu trúc gốc (hook\\source.json cau_truc_hook.nhip) và không dùng lại
    họ nhân vật tập khác. Trả list lỗi (rỗng = đạt)."""
    tap = Path(tap)
    loi = []
    try:
        src = json.loads((tap / "hook" / "source.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        src = {}
    if not ((src.get("cau_truc_hook") or {}).get("nhip")):
        loi.append(f"hook đã khoá KHÔNG có cấu trúc hook gốc ({tap / 'hook' / 'source.json'} thiếu cau_truc_hook) "
                   f"→ hook viết tự do, phải chạy lại hook khi có lời gốc")
    hook = ""
    try:
        hook = (tap / "hook" / "hook_locked.txt").read_text(encoding="utf-8")
    except OSError:
        loi.append("chưa có hook\\hook_locked.txt")
    trung = ho_trung(hook, ho_da_dung(tap))
    if trung:
        loi.append("hook dùng lại họ nhân vật tập trước: " + ", ".join(trung))
    return loi


def _thu_muc_tap(folder):
    if not folder:
        return None
    p = Path(folder.replace("/", "\\"))
    return p if p.is_absolute() else ROOT / p


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tap", help="thư mục tập (tuyệt đối)")
    ap.add_argument("--profile")
    ap.add_argument("--tu", type=int)
    ap.add_argument("--den", type=int)
    ap.add_argument("--khong-mang", action="store_true")
    ap.add_argument("--khong-whisper", action="store_true")
    ap.add_argument("--proxy", default="")
    a = ap.parse_args(argv)
    viec = []                                   # (nhãn, thư mục tập, chữ cột K/B)
    if a.tap:
        viec.append((Path(a.tap).name, Path(a.tap), ()))
    elif a.profile and a.tu:
        import dong_goi_may2 as dg
        import profiles
        import review_may3 as rv
        tab = rv.tab_cua(profiles.load(a.profile))
        vals = dg.svc(doc_thoi=True).values().get(spreadsheetId=dg.SHEET_ID, range=f"{tab}!A2:K300").execute().get("values", [])
        for row in vals:
            row = row + [""] * (11 - len(row))
            if row[0].strip().isdigit() and a.tu <= int(row[0]) <= (a.den or a.tu):
                viec.append((f"STT {row[0].strip()}", _thu_muc_tap(row[2].strip()), (row[10], row[1])))
    else:
        ap.error("cần --tap hoặc --profile --tu [--den]")
    thieu = 0
    for nhan, tap, chu in viec:
        k = kiem_nguon(tap, *chu, proxy=a.proxy or None, tai_mang=not a.khong_mang, whisper=not a.khong_whisper)
        if k["ok"]:
            print(f"✓ {nhan}: video gốc {k['video_id']} · lời hook gốc từ {k['nguon']} ({k['so_doan']} đoạn) · {tap}")
        else:
            thieu += 1
            print(f"✗ {nhan}: {k['ly_do']} · video {k['video_id'] or '(không có)'} · {tap or '(chưa có thư mục)'}")
        if tap and (tap / "hook" / "hook_locked.txt").exists():
            for l in kiem_hook_da_khoa(tap):
                print(f"   ✗ hook đã khoá: {l}")
    if thieu:
        print(f"\n{thieu} tập THIẾU hook gốc → CẤM chạy kịch bản/hook. Cách gỡ: nhờ TRENDING-RESEARCH tải lời "
              f"(data\\<kênh>\\transcripts\\<id>.json có mốc giây) hoặc đặt competitor.segments.json vào thư mục tập, rồi chạy lại.")
    return 2 if thieu else 0


if __name__ == "__main__":
    sys.exit(main())
