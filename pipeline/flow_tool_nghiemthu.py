r"""flow_tool_nghiemthu.py - nghiem thu ZIP do tool "Create Tool" cua Flow xuat ra.

5 phep: du 18 anh · dung ten 028..045 · md5 khong trung · kich thuoc 1376x768
        · manifest.csv hop le (co du dong, cot attempts KHONG phai hang so)

Dung:  python flow_tool_nghiemthu.py out\_tool_test\lan1\<file>.zip
"""
import hashlib
import sys
import zipfile
from collections import Counter
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

CAN = [f"{n:03d}" for n in range(28, 46)]


def main(zip_path):
    z = zipfile.ZipFile(zip_path)
    giai = Path(zip_path).with_suffix("") / "giai_nen"
    giai.mkdir(parents=True, exist_ok=True)
    z.extractall(giai)
    anh = sorted(x for x in giai.rglob("*") if x.suffix.lower() in (".png", ".jpg", ".jpeg"))
    loi = []

    ten = [x.stem for x in anh]
    print(f"1. So anh: {len(anh)}/18", "OK" if len(anh) == 18 else "LOI")
    if len(anh) != 18:
        loi.append(f"thieu/thua anh: {len(anh)}")

    thieu = [n for n in CAN if n not in ten]
    la = [n for n in ten if n not in CAN]
    print(f"2. Ten 028..045: thieu={thieu or 'khong'} | la={la or 'khong'}",
          "OK" if not thieu and not la else "LOI")
    if thieu or la:
        loi.append(f"ten sai: thieu={thieu} la={la}")

    h = [hashlib.md5(x.read_bytes()).hexdigest() for x in anh]
    trung = [k for k, v in Counter(h).items() if v > 1]
    print(f"3. md5: {len(set(h))}/{len(h)} khac nhau", "OK" if not trung else f"LOI trung {len(trung)}")
    if trung:
        loi.append(f"md5 trung: {len(trung)}")

    if Image:
        kt = Counter(Image.open(x).size for x in anh)
        print(f"4. Kich thuoc: {dict(kt)}", "OK" if list(kt) == [(1376, 768)] else "KHAC THUONG")
        if list(kt) != [(1376, 768)]:
            loi.append(f"kich thuoc la: {dict(kt)}")

    man = [x for x in giai.rglob("manifest.csv")]
    if not man:
        print("5. manifest.csv: KHONG CO -> LOI")
        loi.append("thieu manifest.csv")
    else:
        dong = [l for l in man[0].read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
        header, data = dong[0], dong[1:]
        cols = [c.strip().lower() for c in header.split(",")]
        print(f"5. manifest.csv: {len(data)} dong du lieu | cot={cols}")
        if len(data) != 18:
            loi.append(f"manifest {len(data)} dong (can 18)")
        if "attempts" in cols:
            i = cols.index("attempts")
            vals = [r.split(",")[i].strip() for r in data if len(r.split(",")) > i]
            dem = Counter(vals)
            hang_so = len(dem) == 1
            if hang_so and vals[0] == "1":
                nhan = "OK (khong dong nao phai retry)"
            elif hang_so:
                nhan = f"LOI (hang so {vals[0]} - cot vo nghia)"
            else:
                nhan = "OK (phan anh so lan goi that)"
            print(f"   attempts: {dict(dem)}", nhan)
            if hang_so and vals[0] not in ("1",):
                loi.append(f"attempts la hang so {vals[0]}")
        if "strategy" in cols:
            i = cols.index("strategy")
            print("   strategy:", dict(Counter(r.split(",")[i].strip() for r in data)))
        if "state" in cols:
            i = cols.index("state")
            print("   state:", dict(Counter(r.split(",")[i].strip() for r in data)))

    fp = [x for x in giai.rglob("failed_prompts.txt")]
    if fp:
        noi_dung = [l for l in fp[0].read_text(encoding="utf-8", errors="replace").splitlines()
                    if l.strip() and not l.startswith("-") and "NNN" not in l]
        print(f"6. failed_prompts.txt: {len(noi_dung)} dong loi", "OK" if not noi_dung else "CO LOI")
        if noi_dung:
            loi.append(f"{len(noi_dung)} dong that bai")

    print("\n=> KET LUAN:", "DAT" if not loi else "KHONG DAT: " + " | ".join(loi))
    return 0 if not loi else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
