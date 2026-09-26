r"""nghiemthu_flow_tool.py — cong nghiem thu ZIP do app "Create Tool" cua Google Flow xuat ra,
roi (neu DAT) giao anh ve thu muc img\ cua tap.

    py -3.13 pipeline\nghiemthu_flow_tool.py <file.zip> --bo3 <thu muc bo 3> [--giao "<thu muc tap>\img"]

Khac `D:\CLAUDE\RENDER_IMG\flow_tool_nghiemthu.py`: ban do khoa cung dai 028..045 va so 18
(`CAN = [f"{n:03d}" for n in range(28, 46)]`) nen lo khac se bao TRUOT OAN. Ban nay doc dai NNN
va TAG tu chinh `flow_batch_prompts.txt` cua lo do, nen dung cho moi lo.

7 phep (theo GIAO_VIEC_H2DEV.md):
  1 du so anh · 2 GIU DUNG NNN goc · 3 md5 khac nhau doi mot · 4 kich thuoc dong nhat 1376x768
  5 manifest.csv du dong + attempts khong phai hang so vo nghia
  6 strategy=a cho MOI dong co nhan vat (tut xuong b = chi giu 1 mat trong canh 2 nguoi)
  7 failed_prompts.txt rong
Phep thu 8 (mo 5-6 anh so mat voi _ref_upload/) la viec cua NGUOI — tool chi nhac, khong thay the.
"""
import argparse
import csv
import hashlib
import shutil
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

try:
    from PIL import Image
except ImportError:
    Image = None

KT_CHUAN = (1376, 768)
HEADER_CHUAN = ["nnn", "tag", "state", "strategy", "attempts", "size_bytes", "seconds"]
HEADER_PLAIN = ["nnn", "tag", "state", "attempts", "size_bytes", "seconds"]  # bien the (b)
ANH = (".png", ".jpg", ".jpeg")


def doc_don(bo3):
    """flow_batch_prompts.txt -> {NNN: TAG}. Day la NGUON CHAN LY cua lo, khong gia dinh 028..045."""
    f = Path(bo3) / "flow_batch_prompts.txt"
    if not f.is_file():
        sys.exit(f"LOI: khong thay {f} — --bo3 phai tro vao thu muc bo 3 do don_flow_tool.py sinh")
    don = {}
    for d in f.read_text(encoding="utf-8").splitlines():
        if d.strip():
            nnn, tag, _ = d.split("|", 2)
            don[nnn] = tag
    return don


def kiem(giai, don):
    """Tra (danh sach loi, danh sach file anh)."""
    loi = []
    anh = sorted(x for x in giai.rglob("*") if x.suffix.lower() in ANH)
    ten = [x.stem for x in anh]

    print(f"1. So anh: {len(anh)}/{len(don)}", "OK" if len(anh) == len(don) else "LOI")
    if len(anh) != len(don):
        loi.append(f"so anh {len(anh)} (can {len(don)})")

    thieu = sorted(n for n in don if n not in ten)
    la = sorted(n for n in ten if n not in don)
    print(f"2. NNN goc {min(don)}..{max(don)}: thieu={thieu or 'khong'} | la={la or 'khong'}",
          "OK" if not thieu and not la else "LOI")
    if thieu:
        loi.append(f"thieu NNN: {','.join(thieu)}")
    if la:
        loi.append(f"NNN la (app tu danh so lai?): {','.join(la)}")

    h = [hashlib.md5(x.read_bytes()).hexdigest() for x in anh]
    trung = [k for k, v in Counter(h).items() if v > 1]
    print(f"3. md5: {len(set(h))}/{len(h)} khac nhau", "OK" if not trung else f"LOI trung {len(trung)}")
    if trung:
        loi.append(f"{len(trung)} anh trung md5 (ZIP gom ban cu?)")

    if Image is None:
        print("4. Kich thuoc: BO QUA (khong co PIL)")
    elif anh:
        kt = Counter(Image.open(x).size for x in anh)
        ok = list(kt) == [KT_CHUAN]
        print(f"4. Kich thuoc: {dict(kt)}", "OK" if ok else "KHAC THUONG")
        if not ok:
            loi.append(f"kich thuoc la: {dict(kt)}")
    return loi, anh


def _chuan_strategy(v):
    import re as _re
    tok = _re.sub(r"[^a-z]+", " ", (v or "").lower()).split()
    return "a" if tok and tok[0] in ("a", "all") else (v or "").lower().strip()


def kiem_manifest(giai, don, loi):
    man = list(giai.rglob("manifest.csv"))
    if not man:
        print("5. manifest.csv: KHONG CO -> LOI")
        loi.append("thieu manifest.csv")
        return
    rows = list(csv.reader(man[0].read_text(encoding="utf-8", errors="replace").splitlines()))
    rows = [r for r in rows if any(c.strip() for c in r)]
    cols = [c.strip().lower() for c in rows[0]]
    data = rows[1:]
    print(f"5. manifest.csv: {len(data)} dong | cot={cols}")
    chuan = HEADER_CHUAN if any(tag != "PLAIN" for tag in don.values()) else HEADER_PLAIN
    if cols != chuan:
        print(f"   header khac khe uoc (can {chuan})")
        loi.append("header manifest sai khe uoc")
    if len(data) != len(don):
        loi.append(f"manifest {len(data)} dong (can {len(don)})")

    lay = lambda r, k: r[cols.index(k)].strip() if k in cols and len(r) > cols.index(k) else ""
    if "attempts" in cols:
        v = [lay(r, "attempts") for r in data]
        dem = Counter(v)
        hang_so = len(dem) == 1
        if hang_so and v and v[0] != "1":
            print(f"   attempts: {dict(dem)} LOI (hang so {v[0]} — cot vo nghia)")
            loi.append(f"attempts la hang so {v[0]}")
        else:
            print(f"   attempts: {dict(dem)}", "OK")
    if "state" in cols:
        print(f"   state: {dict(Counter(lay(r, 'state') for r in data))}")
    if "strategy" in cols:
        # 2026-09-25 (vá theo YEU_CAU_MAY1_..._thieu_hook_promise.md §BỔ SUNG 11:32): app ghi strategy
        # "toàn A" một kiểu khác nhau mỗi lần dựng — "(a)" / "(a) all references" / "all" / "a" — so
        # thẳng == "a" báo TỤT OAN cho các biến thể đó. Chuẩn hoá: bất kỳ token đầu là a/all → "a".
        st = {lay(r, "nnn"): _chuan_strategy(lay(r, "strategy")) for r in data}
        print(f"6. strategy: {dict(Counter(st.values()))}")
        # chi tinh la TUT khi dong CO trong manifest ma strategy khac 'a'; dong thieu han da bi
        # phep dem dong bat roi — gop vao day se bao "chi khoa duoc 1 mat" cho mot dong khong ton tai.
        tut = sorted(n for n, tag in don.items()
                     if tag != "PLAIN" and n in st and st[n] not in ("a", ""))
        if tut:
            print(f"   LOI: {len(tut)} dong co nhan vat tut xuong '{st.get(tut[0])}': {','.join(tut)}")
            loi.append(f"{len(tut)} dong chi khoa duoc 1 mat (strategy != a) -> LAM LAI CA LO")
        else:
            print("   moi dong co nhan vat deu strategy=a", "OK")
    elif any(tag != "PLAIN" for tag in don.values()):
        print("6. strategy: KHONG CO COT -> khong chung minh duoc da khoa du mat")
        loi.append("manifest thieu cot strategy")
    else:
        print("6. strategy: lo toan PLAIN (bien the b) -> khuon da cat cot nay, khong doi")


def kiem_failed(giai, loi):
    fp = list(giai.rglob("failed_prompts.txt"))
    if not fp:
        print("7. failed_prompts.txt: khong co", "OK")
        return
    nd = [l for l in fp[0].read_text(encoding="utf-8", errors="replace").splitlines()
          if l.strip() and not l.startswith("-") and "NNN" not in l]
    print(f"7. failed_prompts.txt: {len(nd)} dong loi", "OK" if not nd else "CO LOI")
    if nd:
        loi.append(f"{len(nd)} dong that bai")


def main():
    ap = argparse.ArgumentParser(description="Nghiem thu ZIP cua Flow Create Tool + giao anh ve tap")
    ap.add_argument("zip", help="file ZIP tai ve tu app")
    ap.add_argument("--bo3", required=True, help="thu muc bo 3 file (co flow_batch_prompts.txt)")
    ap.add_argument("--giao", help=r"thu muc anh cua tap de chep vao khi DAT (vd <tap>\img)")
    ap.add_argument("--ghi-de", action="store_true", dest="ghi_de", help="cho de len anh cung ten da co")
    a = ap.parse_args()

    zp = Path(a.zip)
    if not zp.is_file():
        sys.exit(f"LOI: khong thay {zp}")
    don = doc_don(a.bo3)
    giai = zp.with_suffix("") / "giai_nen"
    if giai.exists():
        shutil.rmtree(giai)
    giai.mkdir(parents=True)
    try:
        zipfile.ZipFile(zp).extractall(giai)
    except zipfile.BadZipFile as e:
        sys.exit(f"LOI: ZIP hong ({e}). DUNG reload trang — anh con trong RAM, bam lai 'Download ZIP'.")
    print(f"ZIP: {zp}  ({zp.stat().st_size} bytes) -> {giai}")
    print(f"Don: {len(don)} dong, NNN {min(don)}..{max(don)}, "
          f"{len([1 for t in don.values() if t != 'PLAIN'])} dong co nhan vat\n")

    loi, anh = kiem(giai, don)
    kiem_manifest(giai, don, loi)
    kiem_failed(giai, loi)

    print("\n=> KET LUAN:", "DAT" if not loi else "KHONG DAT: " + " | ".join(loi))
    if loi:
        print("   ⚠️ CHUA duoc reload trang Flow — anh co the con trong RAM, bam lai 'Download ZIP'.")
        return 1
    if a.giao:
        # 2026-09-25 (vá theo YEU_CAU_MAY1_..._thieu_hook_promise.md §BỔ SUNG 11:32): app ZIP lúc xuất
        # .png lúc .jpg/.jpeg tuỳ lô — pipeline (assemble.py/gen_images.py/make_video.py B5) chỉ nhận
        # diện NNN.png, thiếu .png là bị coi là chưa vẽ rồi TỰ VẼ LẠI bằng gpti2 (tốn tiền). LUÔN ghi
        # ra .png bất kể đuôi gốc.
        d = Path(a.giao)
        d.mkdir(parents=True, exist_ok=True)
        dich = [d / f"{x.stem}.png" for x in anh]
        de = [p for p in dich if p.exists()]
        if de and not a.ghi_de:
            sys.exit(f"\nLOI: {len(de)} anh da co trong {d} (vd {de[0].name}). "
                     "Xem lai roi chay lai kem --ghi-de neu chac.")
        from PIL import Image as _Image
        for x, p in zip(anh, dich):
            if x.suffix.lower() == ".png":
                shutil.copy2(x, p)
            else:
                _Image.open(x).convert("RGB").save(p)
        print(f"\nDA GIAO {len(anh)} anh -> {d} (deu .png)")
    co_tag = len([1 for t in don.values() if t != "PLAIN"])
    if co_tag:
        print(f"\nCON MOT PHEP NUA, TOOL KHONG LAM THAY: mo {min(6, co_tag)} anh co TAG "
              f"so mat voi {Path(a.bo3) / '_ref_upload'} — sai 1 anh la hong ca lo.")
    else:
        print("\nLo toan PLAIN (bien the b): khong co mat nhan vat nen khong phai so mat.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
