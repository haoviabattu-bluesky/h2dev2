r"""sinh_neo.py — dung `img_doan.txt` (anh <-> so doan) de sinh `anchors.txt` cho assemble.py.

VI SAO CO FILE NAY
------------------
`assemble.py` co 3 che do chia thoi luong anh. Khong co `--anchors` thi no chia theo SO DEM => anh
TROI dan so voi loi, nang dan ve cuoi video (do that: tap 04 khop hinh-loi 3,1/5 · tap 06 2,9/5 ·
tap 07 co 3 moc 2/5 deu sau phut 19). Xem docs/LOI_ANH_LECH_LOI.md.

Chia viec: **bo nao ghi MOT CON SO** (anh nay thuoc doan thu may cua script.txt) → **may tu dat neo
chinh xac**. Bat bo nao chep nguyen van 100+ trich doan dung thu tu la loai viec no lam khong noi.

NEO LA MOT CUE CO THAT TRONG PHU DE — KHONG PHAI LAT CHU TU CAT
---------------------------------------------------------------
Ban dau file nay cat doan van thanh cac lat deu nhau lam neo, va KHONG HE DOC FILE PHU DE. Hau qua
(do that 2026-09-12, tap 06): doan 30 dai 179 ky tu ma `img_doan.txt` gan 8 anh => moi lat ~22 ky
tu, hai neo ke nhau roi vao CUNG MOT CUE => `anchor_durations` tinh ra thoi luong **0.0 giay** =>
`SystemExit` giua buoc ghep. Ma cong nay van bao "133 neo hop le", vi no chi kiem "tim duoc dung
thu tu" — **kiem sai thu ma khau sau doi hoi**.

Nay: moi neo la NGUYEN VAN MOT CUE, va cac anh trong cung mot doan duoc trai ra CAC CUE KHAC NHAU.
Cuoi cung mo phong dung phep tinh cua `anchor_durations` de chac moi anh duoc >= 1 giay.

  py -3.13 sinh_neo.py --slug <thu muc tap>
  py -3.13 sinh_neo.py --slug <thu muc tap> --kiem       # chi kiem, khong ghi

exit 0 = xong/hop le · exit 1 = khong dung duoc (render se quay ve che do cu, KHONG chet).
"""
import argparse
import collections
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TOI_THIEU_GIAY = 1.0        # assemble.py coi thoi luong < 1s la loi cung — phai kiem TRUOC o day


def parse_srt_cues(srt_path):
    """(thoi diem bat dau, loi) tung cue. Chep tu assemble.py de khong phu thuoc import cheo."""
    txt = Path(srt_path).read_text(encoding="utf-8")
    out = []
    for blk in re.split(r"\n\s*\n", txt.strip()):
        L = blk.splitlines()
        tl = next((x for x in L if "-->" in x), None)
        if not tl:
            continue
        m = re.match(r"\s*(\d\d):(\d\d):(\d\d)[,.](\d\d\d)", tl)
        if not m:
            continue
        h, mn, s, ms = map(int, m.groups())
        out.append((h * 3600 + mn * 60 + s + ms / 1000,
                    "".join(L[L.index(tl) + 1:]).strip()))
    return out


def doc_doan(script_path):
    t = Path(script_path).read_text(encoding="utf-8")
    return [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip()]


def doc_img_doan(path):
    ra = {}
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#") or "|" not in ln:
            continue
        ten, so = ln.split("|", 1)
        if so.strip().isdigit():
            ra[ten.strip()] = int(so.strip())
    return ra


def tim_srt(slug):
    for t in ("voice_paced.srt", "voice.srt"):
        if (slug / t).exists():
            return slug / t
    return None


def _chuan(s):
    """Bo khoang trang/dau cau de gong hai ban text (script vs cue) — cue co the da bi reflow."""
    return re.sub(r"[\s、。！？「」…・]", "", s)


def dai_cue_cua_doan(doan, cues):
    """[(cue_dau, cue_cuoi)] cho tung doan — gong doan van vao day cue theo thu tu.

    Khong dung `find` tren toan van vi cue co the them/bot dau cau; dung do dai da chuan hoa."""
    do_cue = [len(_chuan(t)) for _, t in cues]
    cong = [0]
    for d in do_cue:
        cong.append(cong[-1] + d)          # cong[i] = so ky tu truoc cue i
    ra, moc = [], 0
    for d in doan:
        het = moc + len(_chuan(d))
        i = max(0, next((k for k in range(len(cues)) if cong[k + 1] > moc), 0))
        j = next((k for k in range(i, len(cues)) if cong[k + 1] >= het), len(cues) - 1)
        ra.append((i, max(i, j)))
        moc = het
    return ra


def sinh(slug):
    """Tra (dong_anchors, loi)."""
    slug = Path(slug)
    anh = sorted((slug / "img").glob("*.png"))
    f_doan, f_script = slug / "img_doan.txt", slug / "script.txt"
    f_srt = tim_srt(slug)

    if not anh:
        return [], ["khong co anh nao trong img/"]
    if not f_doan.exists():
        return [], ["khong co img_doan.txt (chay sinh_img_doan.py truoc)"]
    if not f_script.exists():
        return [], ["khong co script.txt"]
    if not f_srt:
        return [], ["khong co voice_paced.srt / voice.srt — phai chay TTS truoc khi dat neo"]

    doan = doc_doan(f_script)
    m = doc_img_doan(f_doan)
    cues = parse_srt_cues(f_srt)
    loi = []

    thieu = [p.name for p in anh if p.name not in m]
    if thieu:
        loi.append(f"{len(thieu)} anh khong co so doan: {thieu[:8]}{'...' if len(thieu) > 8 else ''}")
    ngoai = sorted({v for v in m.values() if not 1 <= v <= len(doan)})
    if ngoai:
        loi.append(f"so doan ngoai khoang 1..{len(doan)}: {ngoai[:8]}")
    day = [m.get(p.name, 0) for p in anh]
    lui = [(anh[i].name, day[i - 1], day[i]) for i in range(1, len(day)) if day[i] < day[i - 1]]
    if lui:
        loi.append(f"{len(lui)} cho so doan GIAM (neo lui) — vd {lui[:3]}")
    if loi:
        return [], loi

    dai = dai_cue_cua_doan(doan, cues)

    # moi doan: trai cac anh cua no ra CAC CUE KHAC NHAU trong dai cue cua doan do
    nhom = {}
    for p in anh:
        nhom.setdefault(m[p.name], []).append(p.name)

    # CHON NEO TRAI DEU THEO THOI GIAN trong dai cue cua doan (Phương án B, 2026-09-13).
    # Ban cu lay cue SOM NHAT con cach neo truoc >= 1s => moi anh trong cung doan don het ve DAU
    # doan, de trong phan sau (do that: max 45,0s va 17 anh < 3s). Nay: moi anh co mot MOC THOI
    # GIAN MONG MUON trai deu trong doan (t0 + (t1-t0)*k/n), chon cue HOP LE gan moc nhat.
    chon, cue_truoc = {}, -10.0
    da_dat = collections.Counter()
    for p in anh:
        so_doan = m[p.name]
        i, j = dai[so_doan - 1]
        n_trong_doan = len(nhom[so_doan])
        k_thu = da_dat[so_doan]                 # anh nay la anh thu may (0-based) trong doan
        da_dat[so_doan] += 1
        t0 = cues[i][0]
        t1 = cues[j + 1][0] if j + 1 < len(cues) else cues[-1][0] + 1.0
        muc = t0 + (t1 - t0) * k_thu / n_trong_doan       # moc thoi gian mong muon, trai deu
        ung = [t for t in range(i, j + 1) if cues[t][0] - cue_truoc >= TOI_THIEU_GIAY]
        if not ung:
            loi.append(f"doan {so_doan} khong con cho cho {p.name} (cac cue con lai cach neo "
                       f"truoc < {TOI_THIEU_GIAY}s) — bot anh o doan nay trong img_doan.txt")
            break
        k = min(ung, key=lambda t: abs(cues[t][0] - muc))  # cue GAN MOC NHAT trong so con hop le
        chon[p.name] = k
        cue_truoc = cues[k][0]
    if loi:
        return [], loi

    # neo = NGUYEN VAN cue do; cue rong thi lui dan sang cue ben canh con chu
    ra = []
    for p in anh:
        ci = chon[p.name]
        while ci < len(cues) - 1 and len(cues[ci][1].strip()) < 4:
            ci += 1
        ra.append((p.name, cues[ci][1].strip()))

    # --- MO PHONG DUNG PHEP TINH CUA assemble.anchor_durations ---
    # Day la phep kiem QUAN TRONG NHAT: cong phai kiem dung thu khau sau doi hoi. Ban truoc bo qua
    # buoc nay nen bao "hop le" cho bo neo lam assemble chet giua chung.
    full, spans, pos = [], [], 0
    for i, (_, t) in enumerate(cues):
        spans.append((pos, i))
        full.append(t)
        pos += len(t)
    full_text = "".join(full)

    starts, tim, xau = [], 0, []
    for ten, neo in ra:
        idx = full_text.find(neo, tim)
        if idx == -1:
            idx = full_text.find(neo)
        if idx == -1:
            xau.append(f"{ten}: khong tra nguoc duoc neo {neo[:20]!r}")
            continue
        ci = 0
        for start_ch, k in spans:
            if start_ch <= idx:
                ci = k
            else:
                break
        starts.append((ten, cues[ci][0]))
        tim = idx + len(neo)
    if xau:
        return [], xau[:6]

    ngan = [(starts[i][0], round(starts[i + 1][1] - starts[i][1], 2))
            for i in range(len(starts) - 1)
            if starts[i + 1][1] - starts[i][1] < TOI_THIEU_GIAY]
    if ngan:
        return [], [f"{len(ngan)} anh duoc < {TOI_THIEU_GIAY}s (assemble se bao loi cung) — vd {ngan[:5]}",
                    "→ giam so anh dung chung mot doan trong img_doan.txt, hoac tang so doan"]

    return [f"{t}|{n}" for t, n in ra], []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--kiem", action="store_true")
    a = ap.parse_args()

    dong, loi = sinh(a.slug)
    if loi:
        print("✗ CHUA sinh duoc anchors.txt:")
        for l in loi:
            print("   -", l)
        print("   → render se QUAY VE che do cu (chia theo so dem). Video van ra, chi la anh co the troi.")
        return 1

    out = Path(a.slug) / "anchors.txt"
    print(f"✓ {len(dong)} neo hop le — moi neo la mot cue CO THAT, moi anh duoc >= {TOI_THIEU_GIAY}s")
    if a.kiem:
        print("   (--kiem: khong ghi file)")
        return 0
    out.write_text("\n".join(dong) + "\n", encoding="utf-8")
    print(f"✓ ghi {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
