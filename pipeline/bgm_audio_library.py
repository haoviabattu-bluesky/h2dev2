"""NHẠC NỀN TỪ THƯ VIỆN ÂM THANH YOUTUBE STUDIO (Audio Library) — thay Suno/ai33 (anh chốt 2026-10-23).

Lý do: nhạc Suno qua ai33 không có chứng từ giấy phép (tài khoản Suno là của bên bán lại) → bị claim không kháng được.
Audio Library: YouTube cam kết bài tải từ thư viện "won't be claimed through Content ID", video vẫn kiếm tiền.
CHỈ lấy bài giấy phép YOUTUBE (không cần ghi công) — bỏ hẳn CC-BY. Mỗi đích bài riêng (đích khác không lấy lại).
Tải bằng Chrome đã đăng nhập YouTube (studio_audio_library.py — mở thêm 1 tab, không chuyển kênh).

Đích:
  h2dev    : assets/_bgm_kenh/<lane>/piano_nen.mp3 = 2 bài piano nối mờ 5s + loudnorm −20 LUFS (y chuẩn bản Suno cũ,
             ghep_hook_noi_truoc.py đọc như cũ) + nguon.json (chứng từ kháng claim). Bản Suno → piano_nen_suno_bak.mp3
  MG lane X: MG_STUDIO/assets/nhac/x/al_hook.mp3 + al_than_{1,2}.mp3 + nguon.json; lanes/x/lane.json "nhac" trỏ sang
             (nhac_file.py tự cân mức theo giọng). Lane P/Q nhạc do code tự tổng hợp → không đụng.

  py -3.13 -X utf8 bgm_audio_library.py --dry-run            # chỉ in bài sẽ chọn
  py -3.13 -X utf8 bgm_audio_library.py                      # mọi đích chưa có nguon.json
  py -3.13 -X utf8 bgm_audio_library.py --only teinengo-real --force
"""
import argparse, hashlib, json, shutil, subprocess, sys, time
from datetime import date
from pathlib import Path

import numpy as np

import studio_audio_library as sal

KHO = Path(__file__).resolve().parent.parent / "assets" / "_bgm_kenh"     # cùng chỗ ghep_hook_noi_truoc.py đọc
CACHE = KHO / "_audio_library"
MG = Path(r"E:\CLAUDE\YOUTUBE\MG_STUDIO")
PIANO = dict(can={"PIANO"}, cam={"DRUMS", "SYNTH", "ELECTRIC_GUITAR", "BASS", "TRUMPET", "ORGAN"}, n=2)
LE = ("birthday", "christmas", "xmas", "holiday", "halloween", "santa", "jingle", "wedding")   # bài theo dịp — lạc màu
# Thứ tự moods/genres = ưu tiên. Màu nhạc theo PHONG_CACH cũ của gen_bgm_kenh.py (bản Suno). Kênh mới: thêm 1 dòng.
DICH = {
    "teinengo-real":   dict(PIANO, moods=["DRAMATIC", "SAD", "DARK"], genres=["CINEMATIC", "CLASSICAL"]),
    "shakai_no_naze":  dict(PIANO, moods=["CALM", "INSPIRATIONAL", "BRIGHT"], genres=["CLASSICAL", "AMBIENT", "CINEMATIC"]),
    "teinengo-anaba":  dict(PIANO, moods=["CALM", "INSPIRATIONAL", "ROMANTIC"], genres=["CLASSICAL", "AMBIENT", "CINEMATIC"]),
    "senior_korekara": dict(PIANO, moods=["INSPIRATIONAL", "BRIGHT", "HAPPY"], genres=["CLASSICAL", "CINEMATIC", "AMBIENT"]),
    "kaigo-sukatto":   dict(PIANO, moods=["INSPIRATIONAL", "CALM", "HAPPY"], genres=["CLASSICAL", "CINEMATIC", "AMBIENT"]),
    # Lane X: hook phải mạnh như video gốc (trống + dây), thân trầm bí ẩn.
    "x/hook": dict(can={"DRUMS", "STRINGS"}, cam={"SYNTH", "ELECTRIC_GUITAR"}, n=1, moods=["DRAMATIC", "DARK"], genres=["CINEMATIC"]),
    "x/than": dict(can=set(), cam={"DRUMS", "ELECTRIC_GUITAR", "BASS", "TRUMPET", "SYNTH"}, n=2,
                   moods=["DARK", "CALM"], genres=["AMBIENT", "CINEMATIC"]),
}


def _bo(x, tien_to):
    return {s.replace(tien_to, "") for s in x}


def diem(t, k, ten):
    """Điểm chọn bài (thấp = tốt) hoặc None nếu loại."""
    a = t.get("attributes") or {}
    ins, moods, gen = (_bo(a.get(f, []), "CREATOR_MUSIC_" + p) for f, p in
                       (("instruments", "INSTRUMENT_"), ("moods", "MOOD_"), ("genres", "GENRE_")))
    dur = int((t.get("duration") or {}).get("seconds", 0))
    if t.get("licenseType") != "CREATOR_MUSIC_LICENSE_TYPE_YOUTUBE" or dur < 150 or not k["can"] <= ins or ins & k["cam"]:
        return None
    hang = [i for i, m in enumerate(k["moods"]) if m in moods]
    if not hang:
        return None
    g = [i for i, x in enumerate(k["genres"]) if x in gen]
    if not g or any(w in t.get("title", "").lower() for w in LE):
        return None
    g = min(g)
    lech = int(hashlib.md5(f"{ten}{t['trackId']}".encode()).hexdigest()[:4], 16) / 65536   # khác giữa đích, cố định giữa lần chạy
    return hang[0] * 10 + g * 2 + len(ins - k["can"]) * 1.5 - min(dur, 300) / 150 + lech


def qc(f):
    """-> (đạt?, giây nhạc bắt đầu mạnh, lý do). Loại bài có lỗ im > 3s giữa bài (nhạc nền 'tắt' giữa video)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "8000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    y = np.frombuffer(raw, np.float32)
    rms = np.sqrt(np.convolve(y ** 2, np.ones(8000) / 8000, "valid")[::2000] + 1e-12)     # cửa sổ 1s, bước 0,25s
    db = 20 * np.log10(rms / (np.percentile(rms, 90) + 1e-9))
    im = run = 0
    for v in db[16:-24] < -35:                                                           # bỏ 4s đầu, 6s cuối
        run = run + 1 if v else 0
        im = max(im, run)
    return im * .25 <= 3, max(0.0, float(np.argmax(db > -6)) * .25 - 0.5), f"lỗ im dài nhất {im * .25:.1f}s"


def lufs(f):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(f), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    return float([x for x in r.splitlines() if x.strip().startswith("I:")][-1].split()[1])


def _nguon(ten):
    return MG / "assets" / "nhac" / ten.split("/")[0] / "nguon.json" if "/" in ten else KHO / ten / "nguon.json"


def _doc(nf):
    return json.loads(nf.read_text(encoding="utf-8")) if nf.exists() else {}


def xong(ten):
    j = _doc(_nguon(ten))
    return ten in j if "/" in ten else bool(j)


def _kenh(ten):
    """Tên kênh trong sổ đăng ký chung (shared/nhac_audio_library/so_dang_ky_bai.json)."""
    return f"MG/{ten}" if "/" in ten else f"h2dev/{ten}"


def da_dung():
    """trackId -> đích đang dùng."""
    m = {}
    for ten in DICH:
        j = _doc(_nguon(ten))
        m.update({b["trackId"]: ten for b in ((j.get(ten) or {}) if "/" in ten else j).get("bai", [])})
    return m


def ghi(ten, ds, files, cid, tu):
    meta = {"nguon": "YouTube Studio Audio Library", "ngay_tai": str(date.today()), "kenh_tai": cid,
            "giay_phep": "YouTube Audio Library license — không cần ghi công; YouTube cam kết không bị Content ID claim",
            "tu_manh_giay": round(tu, 1),
            "bai": [{"trackId": t["trackId"], "title": t["title"], "artist": (t.get("artist") or {}).get("name"),
                     "licenseType": t["licenseType"], "giay": int(t["duration"]["seconds"]), "attributes": t.get("attributes")}
                    for t in ds]}
    nf = _nguon(ten)
    d = nf.parent
    d.mkdir(parents=True, exist_ok=True)
    if "/" in ten:                                                    # MG_STUDIO
        ra = [d / (f"al_{ten.split('/')[1]}" + (f"_{i}" if len(files) > 1 else "") + ".mp3") for i in range(1, len(files) + 1)]
        for f, o in zip(files, ra):
            shutil.copy2(f, o)
        nf.write_text(json.dumps(_doc(nf) | {ten: meta | {"file": [o.name for o in ra]}}, ensure_ascii=False, indent=1),
                      encoding="utf-8")
        return ra
    out = d / "piano_nen.mp3"
    if out.exists() and not nf.exists() and not (d / "piano_nen_suno_bak.mp3").exists():
        out.rename(d / "piano_nen_suno_bak.mp3")                    # giữ bản Suno, không xoá
    ins = sum((["-i", str(f)] for f in files), [])
    fc = ("[0][1]acrossfade=d=5:c1=tri:c2=tri," if len(files) == 2 else "") + "loudnorm=I=-20:TP=-2:LRA=11"
    tam = d / "_tam.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *ins, "-filter_complex", fc, "-ar", "48000", str(tam)],
                   check=True)
    bu = -20 - lufs(tam)            # loudnorm 1 lượt lệch tới +1,8 dB ở bài dài (đo 23/10) → bù cho đúng −20 như bản Suno
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(tam), "-af", f"volume={bu:.2f}dB",
                    "-b:a", "192k", str(out)], check=True)
    tam.unlink()
    print(f"    {lufs(out):.1f} LUFS (bù {bu:+.1f} dB)")
    nf.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return [out]


def lane_x():
    """Trỏ MG lane x sang file Audio Library (bản cũ → lane.truoc_<ngày>-audiolib.json). Gọi khi đủ hook + thân."""
    f = MG / "lanes" / "x" / "lane.json"
    j = json.loads(f.read_text(encoding="utf-8"))
    bak = f.with_name(f"lane.truoc_{date.today():%Y%m%d}-audiolib.json")
    if not bak.exists():
        shutil.copy2(f, bak)
    ng = _doc(_nguon("x/hook"))
    nh = j["nhac"]
    nh["_khac"]["file"] = [f"assets/nhac/x/{n}" for n in ng["x/than"]["file"]]
    nh["_hook"].update({"file": f"assets/nhac/x/{ng['x/hook']['file'][0]}", "tu": ng["x/hook"]["tu_manh_giay"], "toc": 1.0})
    nh["_doc_audiolib"] = (f"{date.today()}: bỏ Suno (không chứng từ giấy phép) → YouTube Audio Library giấy phép YouTube; "
                           "chứng từ assets/nhac/x/nguon.json; tool h2dev/pipeline/bgm_audio_library.py; hook 'tu' = giây nhạc bắt đầu mạnh")
    f.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  lane x: lane.json → al_*.mp3 (hook tu {nh['_hook']['tu']}s) — bản cũ {bak.name}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help=f"đích: {' '.join(DICH)}")
    ap.add_argument("--force", action="store_true", help="chọn lại cả đích đã có nguon.json")
    ap.add_argument("--dry-run", action="store_true", help="chỉ in bài sẽ chọn, không tải/ghi")
    ap.add_argument("--lam-moi", action="store_true", help="tải lại danh mục (mặc định dùng cache)")
    ap.add_argument("--port", type=int, default=9339, help="Chrome đã đăng nhập YouTube (mặc định hoangletran6868 / chrome_profile_gemini2)")
    a = ap.parse_args()
    if bad := [d for d in (a.only or []) if d not in DICH]:
        raise SystemExit(f"✗ chưa khai đích {bad} — thêm vào DICH")
    ds_dich = [d for d in (a.only or DICH) if a.force or a.dry_run or not xong(d)]
    if not ds_dich:
        return print("mọi đích đã có nguon.json (--force để chọn lại)")
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    with sync_playwright() as p:
        pg, cid = sal.mo_tab(p, a.port)
        try:
            cat = sal.danh_muc(pg, cid, CACHE / "catalog.json", a.lam_moi)
            cua_minh = {_kenh(d) for d in ds_dich}
            dung = {k: v for k, v in (sal.kenh_dung() | da_dung()).items() if v not in ds_dich and v not in cua_minh}
            for ten in ds_dich:
                k = DICH[ten]
                ung = sorted((s, t["trackId"], t) for t in cat if t["trackId"] not in dung and (s := diem(t, k, ten)) is not None)
                print(f"[{ten}] {len(ung)} bài đạt lọc")
                chon, files, tu = [], [], None
                for _, _, t in ung:
                    if len(chon) == k["n"]:
                        break
                    s = int(t["duration"]["seconds"])
                    tag = f"{t['title']} — {(t.get('artist') or {}).get('name')} ({s // 60}:{s % 60:02d})"
                    if a.dry_run:
                        print(f"    + {tag}")
                        chon.append(t); dung[t["trackId"]] = ten
                        continue
                    try:
                        f = sal.tai(pg, cid, t, CACHE / "goc")
                    except Exception as e:
                        print(f"    ✗ {tag}: {e}")
                        continue
                    dat, manh, ly = qc(f)
                    print(f"    {'+' if dat else '✗'} {tag} · {ly}")
                    if dat:
                        chon.append(t); files.append(f); dung[t["trackId"]] = ten
                        tu = manh if tu is None else tu
                if len(chon) < k["n"]:
                    raise SystemExit(f"✗ {ten}: chỉ được {len(chon)}/{k['n']} bài — nới moods/genres trong DICH")
                if not a.dry_run:
                    print("    →", ", ".join(str(o) for o in ghi(ten, chon, files, cid, tu)))
                    sal.dang_ky(chon, _kenh(ten), "MG_STUDIO" if "/" in ten else "h2dev")
        finally:
            pg.close()                      # chỉ đóng tab của mình — Chrome dùng chung Flow/Vids
    if not a.dry_run and any(d.startswith("x/") for d in ds_dich) and xong("x/hook") and xong("x/than"):
        lane_x()
    print(f"xong {len(ds_dich)} đích trong {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
