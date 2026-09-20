"""qc_can_anh.py — cong kiem truoc khi ghi cot STATUS-IMG = "Xong noi dung - can anh"
(xem docs/GIAO_VIEC_MAY2_ANH.md muc 3). Dam bao ho so du de may 2 chay qua Flow ma khong bi
bay da biet, cho CA HAI loai job dang co trong du an:

  Loai A (REF-LOCK, vd Lopezzapa68/satori): <folder>/img_prompts.txt + characters.json +
          _ref/001.png (+ _ref2/001.png) — cau thieu mention nhan vat -> Flow bia nguoi la.
  Loai B (plain prompt, vd toshi-densetsu-jp): <folder>/img_ai/prompts.txt (dong dang
          "<ten file>\\t<prompt>") + img_ai/img_meta.json — khong Character, chi can ten file
          lien tuc 001..NNN khop dung so dong.

Tu dong nhan dien: co img_ai/prompts.txt -> Loai B, khong thi tim img_prompts.txt -> Loai A.

Dung:
  py -3.13 pipeline\\qc_can_anh.py --folder "assets/satori_jp/<slug>"
  py -3.13 pipeline\\qc_can_anh.py --folder "assets/toshi-densetsu-jp/<slug>"
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

_HEADER = re.compile(r"^\s*(═══|▶|✅|#|//)")
_MARK_RE = re.compile(r"^\s*@(REF2|REF)\b", re.IGNORECASE)
_MARK_MOI = re.compile(r"@(REF2|REF)\b", re.IGNORECASE)   # marker ở BẤT KỲ đâu trong dòng
_FNAME_RE = re.compile(r"^(\d{3,})\.png$", re.IGNORECASE)


def load_prompts(path):
    """Tra ve list (lineno, tag, text, tags) — tag la marker DAU DONG ('REF'/'REF2'/None),
    tags la TAT CA marker xuat hien tren dong do.

    Vi sao can `tags`: dong viet "@REF and @REF2 two elderly women..." khop _MARK_RE thanh 'REF',
    con "@REF2" nam lai trong text nen bi dem nham la canh MOT nguoi — dung canh 2 nguoi ma cong
    im lang bo qua (do that simbot2-11: 3 dong 46/74/115). `gen_images.py` cung chi doc marker dau
    dong nen neu phai va bang gpti2 thi chi khoa mat nhan vat 1 => Flow/gpti2 bia nguoi la (§11.3c)."""
    out = []
    for i, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        s = line.strip()
        if not s or _HEADER.match(s):
            continue
        m = _MARK_RE.match(s)
        tag = m.group(1).upper() if m else None
        text = s[m.end():].strip() if m else s
        tags = [g.upper() for g in _MARK_MOI.findall(s)]
        out.append((i, tag, text, tags))
    return out


def masters_tu_characters(folder, characters):
    """[(marker, ten, Path master hoac None)] theo THU TU trong characters.json.

    NGUON CHAN LY la truong `master` — dung thu ma render_engine.py dung (dong 141-149):
        masters = [S / c["master"] for c in chars if c.get("master")]
        --ref masters[0] ... --ref2 masters[1]
    Cong cu doan cung ten thu muc `_ref2/001.png` nen chan oan tap dat thu muc theo ten nhan vat
    (vd `_ref_kyoko`), trong khi render_engine chay binh thuong."""
    ra = []
    for i, c in enumerate(characters[:2]):
        mk = "REF" if i == 0 else "REF2"
        m = c.get("master")
        ra.append((mk, c.get("name", "?"), (folder / m) if m else None))
    return ra


def load_characters(path):
    if not Path(path).exists():
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    chars = list(data.get("characters", []))
    return chars


def check_loai_b(folder):
    """Job Loai B: <folder>/img_ai/prompts.txt (ten_file<TAB>prompt) + img_ai/img_meta.json.
    Khong REF-LOCK, khong Character — chi can ten file lien tuc 001..NNN khop so dong."""
    errors, warnings = [], []
    prompts_file = folder / "img_ai" / "prompts.txt"
    lines = [l for l in Path(prompts_file).read_text(encoding="utf-8").splitlines() if l.strip()]
    if not lines:
        errors.append("img_ai/prompts.txt rỗng")

    rows = []  # (fname, prompt)
    for i, line in enumerate(lines, start=1):
        parts = line.split("\t", 1)
        if len(parts) != 2:
            errors.append(f"dòng {i}: không đúng dạng '<tên file>TAB<prompt>' (thiếu tab)")
            continue
        fname, prompt = parts[0].strip(), parts[1].strip()
        if not _FNAME_RE.match(fname):
            errors.append(f"dòng {i}: tên file '{fname}' không đúng dạng NNN.png")
        if not prompt:
            errors.append(f"dòng {i}: prompt rỗng (file {fname})")
        rows.append((fname, prompt))

    nums = sorted(int(_FNAME_RE.match(f).group(1)) for f, _ in rows if _FNAME_RE.match(f))
    expected = list(range(1, len(nums) + 1))
    if nums != expected:
        missing = sorted(set(expected) - set(nums))
        dup_or_extra = sorted(set(nums) - set(expected))
        if missing:
            errors.append(f"thiếu số thứ tự trong tên file: {missing[:20]}{'...' if len(missing)>20 else ''}")
        if dup_or_extra:
            errors.append(f"số thứ tự thừa/trùng/nhảy cóc: {dup_or_extra[:20]}{'...' if len(dup_or_extra)>20 else ''}")

    meta_file = folder / "img_ai" / "img_meta.json"
    if not meta_file.exists():
        errors.append("thiếu img_ai/img_meta.json (sổ ghép ảnh↔đoạn lời)")
    else:
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            meta_list = meta if isinstance(meta, list) else list(meta.values())
            if len(meta_list) != len(rows):
                warnings.append(f"img_meta.json có {len(meta_list)} bản ghi, khác {len(rows)} dòng prompts.txt")
        except Exception as e:
            errors.append(f"img_meta.json không đọc được: {e}")

    print(f"Hồ sơ (Loại B — plain prompt, không REF-LOCK): {folder}")
    print(f"Tổng ảnh cần vẽ: {len(rows)} | tên file: {rows[0][0] if rows else '?'} → {rows[-1][0] if rows else '?'}")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=True, help="thu muc tap")
    ap.add_argument("--profile", default=None, help="chua dung, de danh cho sau nay")
    args = ap.parse_args()

    folder = Path(args.folder)

    if (folder / "img_ai" / "prompts.txt").exists():
        errors, warnings = check_loai_b(folder)
        print()
        if warnings:
            print(f"⚠ {len(warnings)} CẢNH BÁO:")
            for w in warnings:
                print("  -", w)
            print()
        if errors:
            print(f"✗ TRƯỢT — {len(errors)} lỗi chặn:")
            for e in errors:
                print("  -", e)
            sys.exit(1)
        print("✓ ĐẠT — đủ điều kiện ghi cột STATUS-IMG = 'Xong nội dung - cần ảnh' và upload-job lên Drive.")
        return

    errors = []
    warnings = []

    prompts_file = folder / "img_prompts.txt"
    if not prompts_file.exists():
        print(f"TRƯỢT: không thấy {prompts_file} (cũng không thấy img_ai/prompts.txt)")
        sys.exit(1)

    prompts = load_prompts(prompts_file)
    if not prompts:
        errors.append("img_prompts.txt rỗng (không có dòng prompt nào sau khi bỏ header)")

    chars_file = folder / "characters.json"
    characters = load_characters(chars_file)
    char_names = [c["name"] for c in characters if "name" in c]

    use_ref = any("REF" in tags for *_, tags in prompts)
    use_ref2 = any("REF2" in tags for *_, tags in prompts)

    # LUAT (anh chot 2026-09-11): may 1 PHAI gen xong toan bo anh master REF-LOCK bang gpti2 roi
    # moi ban giao — may 2 chi Upload len Flow, khong tu tao master (docs/GIAO_VIEC_MAY2_ANH.md §0).
    can = {"REF": use_ref, "REF2": use_ref2}
    co_master = {}
    for mk, ten, path_master in masters_tu_characters(folder, characters):
        co_master[mk] = (ten, path_master)
    for mk, dung in can.items():
        if not dung:
            continue
        if mk not in co_master:
            errors.append(f"có dòng @{mk} nhưng characters.json KHÔNG khai nhân vật tương ứng "
                          f"(cần ít nhất {2 if mk == 'REF2' else 1} nhân vật trong mảng 'characters')")
            continue
        ten, path_master = co_master[mk]
        if path_master is None:
            errors.append(f"có dòng @{mk} ({ten}) nhưng characters.json thiếu trường 'master'")
        elif not path_master.exists():
            errors.append(f"có dòng @{mk} ({ten}) nhưng CHƯA CÓ ảnh master {path_master} — "
                          f"máy 1 phải gen bằng gpti2 TRƯỚC khi bàn giao, máy 2 không tự tạo master")

    # canh NHIEU marker tren cung 1 dong: dung cho Flow (mention duoc 2 Character) nhung
    # gen_images.py chi doc marker DAU DONG => neu sau nay va bang gpti2 thi chi khoa mat nhan vat 1.
    da_canh = [(ln, tags) for ln, _t, _x, tags in prompts if len(set(tags)) > 1]
    if da_canh:
        ds = ", ".join(str(ln) for ln, _ in da_canh[:10])
        warnings.append(
            f"{len(da_canh)} cảnh có NHIỀU nhân vật trên một dòng (dòng {ds}) — ĐÚNG cho máy 2 chạy "
            f"Flow (mention được cả 2 Character), nhưng `gen_images.py` chỉ đọc marker ĐẦU DÒNG nên "
            f"nếu phải vá bằng gpti2 thì chỉ khoá mặt nhân vật thứ nhất. Dặn máy 2 mention đủ.")

    if (use_ref or use_ref2) and not char_names:
        warnings.append("có REF-LOCK nhưng characters.json thiếu/không có 'characters' — không dò được tên nhân vật để kiểm mention thiếu")

    # do cau nhieu nhan vat nhung thieu mention (bug da dinh that o simbot2-11 anh 006)
    suspect = []
    for lineno, tag, text, _tags in prompts:
        if tag is None or not char_names:
            continue
        # dong da co CA HAI marker (vd '@REF and @REF2 ...') thi KHONG phai thieu mention —
        # bao o day la bao dong gia, ma cong keu oan thi lan sau nguoi ta bo qua ca canh bao that.
        if len(set(_tags)) > 1:
            continue
        marked_name = None
        # doan ten nhan vat ung voi marker: @REF = nhan vat dau tien trong list, @REF2 = nhan vat thu 2
        # (dung quy uoc cua gen_images.py / characters.json da co trong du an)
        idx = 0 if tag == "REF" else 1
        if idx < len(char_names):
            marked_name = char_names[idx]
        for name in char_names:
            if name == marked_name:
                continue
            if re.search(rf"\b{re.escape(name)}\b", text, re.IGNORECASE):
                suspect.append((lineno, tag, name, text[:80]))

    for lineno, tag, other_name, snippet in suspect:
        warnings.append(
            f"dòng {lineno}: có @{tag} nhưng CŨNG nhắc tên '{other_name}' trong câu chữ "
            f"(không có @-mention riêng) — nghi cảnh 2 người, dễ bị Flow bịa người lạ (xem §11.3c). "
            f'Câu: "{snippet}..."'
        )

    empty_lines = [i for i, (_, _, text, _t) in enumerate(prompts, start=1) if not text.strip()]
    if empty_lines:
        errors.append(f"có {len(empty_lines)} dòng prompt rỗng sau khi bỏ marker")

    print(f"Hồ sơ: {folder}")
    n_ref = sum(1 for *_, tg in prompts if "REF" in tg)
    n_ref2 = sum(1 for *_, tg in prompts if "REF2" in tg)
    n_doi = sum(1 for *_, tg in prompts if len(set(tg)) > 1)
    print(f"Tổng dòng prompt: {len(prompts)} | có @REF: {n_ref} | có @REF2: {n_ref2} | "
          f"cảnh 2 nhân vật: {n_doi} | thường: {sum(1 for *_, tg in prompts if not tg)}")
    for mk, ten, pm in masters_tu_characters(folder, characters):
        if can.get(mk):
            print(f"   @{mk} = {ten} → {pm}  [{'có' if pm and pm.exists() else 'THIẾU'}]")
    print(f"Nhân vật trong characters.json: {char_names or '(không có)'}")
    print()

    if warnings:
        print(f"⚠ {len(warnings)} CẢNH BÁO (không chặn, nhưng nên soát lại trước khi gửi máy 2):")
        for w in warnings:
            print("  -", w)
        print()

    if errors:
        print(f"✗ TRƯỢT — {len(errors)} lỗi chặn:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    print("✓ ĐẠT — đủ điều kiện ghi cột STATUS-IMG = 'Xong nội dung - cần ảnh' và upload-job lên Drive.")


if __name__ == "__main__":
    main()
