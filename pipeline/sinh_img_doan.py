r"""sinh_img_doan.py — sinh `img_doan.txt` (anh <-> so doan loi) bang LLM, cho tap CHUA CO file do.

VI SAO CO FILE NAY
------------------
`img_doan.txt` cho biet moi anh minh hoa cho DOAN THU MAY cua `script.txt`. Thieu no thi khau ghep
chia anh theo SO DEM => anh TROI dan so voi loi, nang dan ve cuoi video. Do that: tap 04 khop
hinh-loi 3,1/5 · tap 06 2,9/5 · tap 07 co 3 moc 2/5 deu nam sau phut 19. Xem docs/LOI_ANH_LECH_LOI.md.

Tu 2026-09-12 bo nao TU VIET file nay o buoc B5 (pha chu). File nay danh cho:
  1. Cac tap chay pha chu TRUOC khi co luat do (04, 06, 07, 11, 19, 21) — vet cu.
  2. Luoi an toan neu bo nao quen khai.

VI SAO PHAI DUNG LLM, KHONG TINH DUOC BANG MAY
-----------------------------------------------
Anh nao ung doan nao la chuyen NOI DUNG: phai doc prompt ("ba cu ngoi ben giuong benh") roi tim doan
loi ke ve canh do. Chia theo ti le la quay lai dung cach lam sinh ra loi. Nhung day la viec GHEP NOI
(co dap an dung/sai, kiem duoc) chu khong phai SANG TAC — nen dung duoc model re, khong can Opus.

  py -3.13 sinh_img_doan.py --slug <thu muc tap>
  py -3.13 sinh_img_doan.py --slug <thu muc tap> --lo 30      # so anh moi lan hoi (mac dinh 30)

exit 0 = da ghi img_doan.txt · exit 1 = that bai (khong ghi file hong).
Sau lenh nay chay tiep: py -3.13 sinh_neo.py --slug <thu muc tap>
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from llm_client import chat          # noqa: E402

DAI_TOM = 70                          # moi doan trich bao nhieu ky tu dau lam muc luc cho LLM


def doc_doan(p):
    return [x.strip() for x in re.split(r"\n\s*\n", Path(p).read_text(encoding="utf-8")) if x.strip()]


def doc_prompt(p):
    """[(ten_anh, prompt_da_bo_marker)] — dong thu k ung voi anh {k:03d}.png (quy uoc gen_images)."""
    ra = []
    for i, ln in enumerate([l for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()], 1):
        txt = re.sub(r"@(REF2|REF|GROK)\b", "", ln).strip(" ,")
        ra.append((f"{i:03d}.png", txt))
    return ra


def muc_luc(doan):
    return "\n".join(f"{i}. {d[:DAI_TOM]}" for i, d in enumerate(doan, 1))


def doan_trung_tam(S, doan, N):
    """[so_doan_trung_tam moi anh, 1..N]. Dung TY LE THOI GIAN THAT cua tung doan (khong phai
    ty le theo SO LUONG doan) — anh thu i (0-based) nam o vi tri i/N trong toan bo audio.

    Phương án B (2026-09-13): thay cho viec chia theo index, vi doan dai ngan khac nhau
    lam lech vi tri thuc te cua anh so voi loi ke."""
    import sinh_neo as sn
    f = sn.tim_srt(S)
    P = len(doan)
    if not f:
        # khong co SRT (chua chay TTS) — uoc theo do dai doan, cung tot hon chia deu theo SO LUONG
        do_dai = [len(d) for d in doan]
        tong = sum(do_dai)
        cong = [0]
        for d in do_dai:
            cong.append(cong[-1] + d)
    else:
        cues = sn.parse_srt_cues(f)
        dai = sn.dai_cue_cua_doan(doan, cues)
        het = cues[-1][0]
        tg = []
        for i2, j2 in dai:
            t0 = cues[i2][0]
            t1 = cues[j2 + 1][0] if j2 + 1 < len(cues) else het
            tg.append(max(0.1, t1 - t0))
        tong = sum(tg)
        cong = [0]
        for t in tg:
            cong.append(cong[-1] + t)
    ra = []
    for i in range(N):
        pos = (i + 0.5) / N * tong          # vi tri thoi gian mong muon cua anh thu i
        p = next((k for k in range(1, P + 1) if cong[k] >= pos), P)
        ra.append(p)
    return ra


def cua_so(trung_tam, P, K):
    return [max(1, trung_tam - K), min(P, trung_tam + K)]


def hoi_mot_lo(doan, lo, trung_tam_lo, K):
    """lo: [(ten_anh, prompt)]. trung_tam_lo: {ten_anh: so_doan_trung_tam}.
    Tra {ten_anh: so_doan} — MOI ANH mot lua chon, LAY TU CUA SO RIENG cua no.

    Phương án B (2026-09-13): khong hoi "may anh thuoc doan nay" (LLM khong dem duoc — do that
    3 lan ho said nho nhat), khong dua muc luc 52 doan cat cut (bão hoa → don het ve doan cuoi).
    Hoi MULTIPLE-CHOICE cuc hep: anh NAY khớp doan NAO trong {8-10} doan ung vien quanh vi tri
    thoi gian that cua no. Viet day du doan, KHONG cat cut."""
    cau = []
    for ten, txt in lo:
        tt = trung_tam_lo[ten]
        lo_min, lo_max = cua_so(tt, len(doan), K)
        ds_doan = "\n".join(f"    {p}. {doan[p-1][:200]}" for p in range(lo_min, lo_max + 1))
        cau.append(f"ANH {ten}: {txt[:180]}\n  CAC DOAN UNG VIEN (chon DUNG MOT so trong day):\n{ds_doan}")
    ask = ("Voi MOI anh duoi day, chon DUNG MOT doan trong danh sach ung vien rieng cua no — "
               "doan nao ta dung noi dung/canh vat/hanh dong ma anh do the hien nhat. KHONG duoc chon "
               "so ngoai danh sach ung vien cua chinh anh do.\n\n" + "\n\n".join(cau) +
               "\n\nTra ve DUNG moi dong mot cho moi anh, dinh dang `<ten anh>|<so doan>`, "
               "khong giai thich, khong markdown.")
    kq = chat(ask, task="short", max_tokens=4000, temperature=0.1, verbose=False)
    kq = getattr(kq, "text", kq) or ""
    ra = {}
    for ln in kq.splitlines():
        # LLM hay lặp lại đúng dòng đề bài ("ANH 001.png|1") thay vì bỏ prefix — chấp nhận cả 2
        m = re.match(r"\s*(?:ANH\s+)?([0-9]{3}\.png)\s*\|\s*(\d+)", ln.strip(), re.IGNORECASE)
        if m:
            ra[m.group(1)] = int(m.group(2))
    return ra


def suc_chua(S, doan):
    """[so cue toi da moi doan]. Co SRT thi dem cue that; khong co thi uoc theo do dai doan.

    Vi sao can: `sinh_neo.py` doi moi anh MOT CUE RIENG. Doan 12 cue ma bi gan 28 anh thi khong dat
    neo duoc — cong chan, khau ghep quay ve che do cu, anh troi. Producer phai biet rang buoc cua
    consumer, dung de consumer chan roi moi biet."""
    try:
        import sinh_neo as sn
        f = sn.tim_srt(S)
        if f:
            cues = sn.parse_srt_cues(f)
            ra = []
            for i, j in sn.dai_cue_cua_doan(doan, cues):
                # Dem so cho THUC SU dat duoc: cue ke nhau ma cach < 1 giay thi khong dung duoc 2
                # neo. Dem "so cue" tho la SAI — do that tap 11: doan 12 cue van ra 2 anh < 1s.
                n_cho, moc = 0, -10.0
                for t in range(i, j + 1):
                    if cues[t][0] - moc >= sn.TOI_THIEU_GIAY:
                        n_cho += 1
                        moc = cues[t][0]
                ra.append(max(1, n_cho))
            return ra
    except Exception:
        pass
    return [max(1, len(d) // 30) for d in doan]


def can_bang(de_xuat, chua):
    """Ep day so doan thanh KHONG GIAM va KHONG VUOT SUC CHUA, lech it nhat so voi de xuat.

    Cach lam: voi anh thu i, tinh khoang doan KHA THI [som_nhat, muon_nhat] roi kep de_xuat vao do,
    cuoi cung chay max don de day khong giam.
      som_nhat[i] = doan nho nhat ma tong suc chua tu dau den do >= i+1
      muon_nhat[i] = doan lon nhat ma tong suc chua tu do den cuoi >= so anh con lai
    Chung minh khong tran: anh nao co chi so >= tong-suc-chua-den-doan-p thi som_nhat > p, nen so anh
    duoc gan vao cac doan <= p khong bao gio vuot tong suc chua den p.

    Ban dau viet kieu tham lam "day toi khi gap doan con cho, het cho thi lui lai" — LUI LAI pha vo
    tinh khong giam (test bat duoc: [1,1,5,5,5,4,4,4,3,3])."""
    n, N = len(chua), len(de_xuat)
    if sum(chua) < N:
        return None                              # khong the xep vua — nguoi goi phai bao loi

    cong = [0]
    for c in chua:
        cong.append(cong[-1] + c)                # cong[p] = tong suc chua cua p doan dau

    con = list(chua)                             # suc chua con lai tung doan
    ra, cur = [], 1
    for i, v in enumerate(de_xuat):
        som = next(p for p in range(1, n + 1) if cong[p] >= i + 1)
        muon = max(p for p in range(1, n + 1) if cong[n] - cong[p - 1] >= N - i)
        k = max(cur, som, min(v, muon))          # kep de xuat vao [som, muon], khong lui
        while k < n and con[k - 1] <= 0:         # doan day roi thi day sang doan sau
            k += 1
        con[k - 1] -= 1
        ra.append(k)
        cur = k

    # TU KIEM truoc khi tra — hai lan truoc thuat toan sai ma van tra ket qua trong im lang
    from collections import Counter
    dem = Counter(ra)
    if any(ra[i] > ra[i + 1] for i in range(len(ra) - 1)) or any(dem[p] > chua[p - 1] for p in dem):
        return None
    return ra



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--lo", type=int, default=30, help="so anh moi lan hoi LLM")
    a = ap.parse_args()

    S = Path(a.slug)
    f_script, f_prompt = S / "script.txt", S / "img_prompts.txt"
    for f in (f_script, f_prompt):
        if not f.exists():
            print(f"✗ thieu {f.name}")
            return 1
    if (S / "img_doan.txt").exists():
        print("✓ da co img_doan.txt — khong lam gi (xoa file do neu muon sinh lai)")
        return 0

    doan = doc_doan(f_script)
    prompts = doc_prompt(f_prompt)
    n_anh = len(list((S / "img").glob("*.png"))) if (S / "img").exists() else 0
    print(f"=== {S.name}: {len(prompts)} prompt · {len(doan)} doan · {n_anh} anh tren dia ===")
    if n_anh and n_anh != len(prompts):
        print(f"⚠ so anh ({n_anh}) KHAC so prompt ({len(prompts)}) — img_doan sinh theo PROMPT")

    chua = suc_chua(S, doan)
    print(f"   suc chua: {sum(chua)} cue cho {len(prompts)} anh"
          f" (doan chat nhat {min(chua)} cue)")
    # --- Phương án B: trung tâm theo TỈ LỆ THỜI GIAN THẬT + multiple-choice cửa sổ hẹp riêng
    # từng ảnh. Nới K 4 -> 6 -> 9 nếu can_bang() không xếp vừa; giữ nguyên can_bang() làm lưới
    # an toàn cuối (đã test 200 ca ngẫu nhiên, KHÔNG viết lại).
    N = len(prompts)
    K = 4
    cuoi = None
    for lan_thu in range(3):
        trung_tam = dict(zip((t for t, _ in prompts), doan_trung_tam(S, doan, N)))
        ket = {}
        for i in range(0, N, a.lo):
            lo = prompts[i:i + a.lo]
            try:
                tra = hoi_mot_lo(doan, lo, trung_tam, K)
            except Exception as e:
                print(f"✗ lo {i//a.lo + 1} loi LLM: {type(e).__name__} {e}")
                return 1
            # KEP CUNG vao cua so rieng cua TUNG anh — LLM co the lo mo chon ngoai du da dan
            for ten, _ in lo:
                if ten in tra:
                    lo_min, lo_max = cua_so(trung_tam[ten], len(doan), K)
                    tra[ten] = max(lo_min, min(tra[ten], lo_max))
            ket.update(tra)
            print(f"  lo {i//a.lo + 1}: {len(tra)}/{len(lo)} anh (K={K})")

        # --- VA MAY MOC: LLM co the thieu dong hoac tra so giam. Va bang cach MANG THEO gia tri
        # truoc do (an toan nhat: anh khong co dap an se dung chung doan voi anh lien truoc).
        so_bu = sum(1 for ten, _ in prompts if ten not in ket)
        truoc, de_xuat = 1, []
        for ten, _ in prompts:
            v = max(1, min(ket.get(ten, truoc), len(doan)))
            de_xuat.append(v)
            truoc = v
        cuoi = can_bang(de_xuat, chua)            # GIU NGUYEN ham cu, da test 200 ca
        if cuoi is not None:
            break
        print(f"  K={K} khong xep vua, noi rong cua so...")
        K += 2 if K < 8 else 5                    # 4 -> 6 -> 9 (lan thu 3 het)
    if cuoi is None:
        print(f"✗ khong xep vua sau 3 lan noi cua so (K toi da {K}): kich ban qua ngan so voi so anh.")
        print("   → giam so anh trong img_prompts.txt, hoac chap nhan chay khong neo (anh se troi).")
        return 1
    so_doi = sum(1 for x, y in zip(de_xuat, cuoi) if x != y)
    ra = [(ten, v) for (ten, _), v in zip(prompts, cuoi)]

    (S / "img_doan.txt").write_text("\n".join(f"{t}|{v}" for t, v in ra) + "\n", encoding="utf-8")
    phu = len({v for _, v in ra})
    print(f"\n✓ ghi {S / 'img_doan.txt'} — {len(ra)} dong")
    dn = max((cuoi.count(v), v) for v in set(cuoi))
    print(f"   phu {phu}/{len(doan)} doan · bu thieu {so_bu} dong · can bang doi {so_doi} dong"
          f" · dong nhat: doan {dn[1]} co {dn[0]} anh (suc chua {chua[dn[1]-1]})")
    if so_bu + so_doi > len(ra) * 0.15:
        print("   ⚠ tren 15% dong phai va — nen xem lai truoc khi ghep, hoac chay lai voi --lo nho hon")
    print(f"   → chay tiep: py -3.13 sinh_neo.py --slug \"{S}\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
