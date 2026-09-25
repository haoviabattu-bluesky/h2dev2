r"""don_flow_tool.py — mot lenh ra BO 3 FILE de sinh anh bang "Create Tool" cua Google Flow.

    py -3.13 pipeline\don_flow_tool.py --job <slug> --dong 28-45

Ra trong assets\_flow_tool_mau\<ten>\ :
    flow_create_tool_prompt.txt   huong dan + khoi tieng Anh dan vao Create Tool
    flow_batch_prompts.txt        cac dong NNN|TAG|description (giu NGUYEN NNN goc)
    _ref_upload\<SLOT>.png        anh master da QC mat, ten file trung ten o trong app (da resize <=1600px)

Khoi tieng Anh KHONG viet trong file nay — nap tu `flow_tool_template_va3.txt` (khuon da verify
that 2026-09-23: 18 anh/90s, 0 tin dung). Doi khuon = sua file .txt do, khong sua code.
Ba khoi BAT BUOC nam trong khuon va duoc kiem lai truoc khi ghi: Interface contract ·
cam IndexedDB + tu tai ZIP + banner cam reload · attempts la so lan goi THAT.

2026-09-25 (yeu cau lane K, ep02-mae-no-mise — 8 nhan vat/tap, khuon chi co 5 o): them marker
`@CAST:id1,id2[,id3] <mo ta>` doc THANG tu `characters.json` (khop theo `id`, KHONG theo `name`).
O anh goc gio tinh THEO LO — chi gom nhan vat XUAT HIEN trong cac dong --dong da chon (>5 nguoi/lo
la dung, bao danh sach id + goi y tach dai dong), KHONG con nap ca 8 nhan vat cua tap nhu truoc.
Ten o = id viet HOA ASCII (vd SHU, TENCHO), KHONG con MAIN/FRIEND/THIRD... Job KHONG co dong nao
`@CAST:` van chay dung y het ban cu (@REF/@REF2/@REF12...), khong hoi quy.

Chi tiet ky thuat + bang bay: C:\Users\xxx\.claude\skills\google-flow-tool.md
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

JOBS = Path(r"E:\CLAUDE\YOUTUBE\FlowHandoff_local\jobs")
OUT_ROOT = Path(__file__).resolve().parent.parent / "assets" / "_flow_tool_mau"
KHUON_REF = Path(__file__).resolve().parent / "flow_tool_template_va3.txt"      # (a) job CO nhan vat
KHUON_PLAIN = Path(__file__).resolve().parent / "flow_tool_template_plain.txt"  # (b) job KHONG nhan vat
NGHIEMTHU = r"D:\CLAUDE\RENDER_IMG\flow_tool_nghiemthu.py"
SLOT_MAC_DINH = ["MAIN", "FRIEND", "THIRD", "FOURTH", "FIFTH"]
SO_CHU = {1: ("ONE", "one"), 2: ("TWO", "two"), 3: ("THREE", "three"), 4: ("FOUR", "four"), 5: ("FIVE", "five")}
CANH_DAI_REF = 1600     # px — resize _ref_upload/ (KHONG dung anh master goc) de picker Flow khong ket
# 3 khoi bat buoc — moi khoi mot cau moc phai con nguyen trong khuon
MOC = {
    "Interface contract": "Interface contract - these exact names and element types are read by an",
    "cam IndexedDB": "Do NOT rely on IndexedDB or localStorage to keep finished images",
    "tu tai ZIP": "the app must build the ZIP and start its download on its own",
    "banner cam reload": "Do not reload this page - reloading destroys all finished",
    "attempts that": '"attempts" must be the real number of image-generation calls actually made',
}


def tim_job(ten):
    """slug -> duong dan job. Truoc 2026-09-25 jobs\\ phang (JOBS/slug). Tu 2026-09-25 chia theo
    ten tab (JOBS/<tab>/slug, xem dong_goi_may2.py). Tim kieu cu truoc (khong pha job cu), khong
    thay thi do duoi MOI thu muc tab — khop DUNG 1 thi dung, khop >1 hoac 0 thi dung, khong doan."""
    p = JOBS / ten
    if p.is_dir():
        return p
    hit = [d for d in JOBS.glob(f"*/{ten}") if d.is_dir()]
    if len(hit) == 1:
        return hit[0]
    if len(hit) > 1:
        sys.exit(f"LOI: slug {ten!r} khop {len(hit)} tab: {[h.parent.name for h in hit]} — dung duong dan day du --job")
    sys.exit(f"LOI: khong thay job {ten!r} trong {JOBS} (da thu ca kieu phang lan jobs/<tab>/{ten})")


def nap_nhan_vat(job):
    """marker -> (ten nhan vat, tuoi, duong dan master, mo ta trang phuc).
    Nguon: _BANGIAO.txt neu co dong "@REF = Ten"; khong co thi lay characters[] CO master, dung thu tu.
    Nhan vat khong co master = khong khoa mat = khong co marker (vd 千恵子 trong ep01-fuufu).
    Bien the CU (@REF/@REF2/@REF12...) — dung nguyen, KHONG doi de khong hoi quy job dang chay."""
    cf = job / "characters.json"
    if not cf.is_file():                               # job kieu lane E: khong co file nay = khong nhan vat
        print("khong co characters.json -> job khong nhan vat")
        return {}
    chars = json.loads(cf.read_text(encoding="utf-8")).get("characters", [])
    theo_ten = {c.get("name"): c for c in chars}
    cap = []
    bg = job / "_BANGIAO.txt"
    if bg.exists():
        for d in bg.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"\s*(@REF\d*)\s*=\s*(\S+)", d)
            if m and m.group(2) in theo_ten:
                cap.append((m.group(1), theo_ten[m.group(2)]))
    nguon = "_BANGIAO.txt"
    if not cap:                                        # nhieu job _BANGIAO rong hoac khuon khac
        co_master = [c for c in chars if (c.get("master") or "").strip()]
        cap = [("@REF" if i == 0 else f"@REF{i + 1}", c) for i, c in enumerate(co_master)]
        nguon = "characters.json (thu tu nhan vat CO master)"
    ra = {}
    for marker, c in cap:
        p = job / (c.get("master") or "")
        if not p.is_file():
            sys.exit(f"LOI: master cua {marker} khong ton tai: {p}")
        ra[marker] = (c.get("name", "?"), c.get("age", "?"), p, trang_phuc(c.get("look", "")))
    print(f"nhan vat khoa mat: {nguon} -> " + ", ".join(f"{k}={v[0]}" for k, v in ra.items()))
    return ra


def nap_toan_bo_nhan_vat(job):
    """id -> (ten, tuoi, duong dan master hoac None, mo ta trang phuc). TOAN BO nhan vat trong
    characters.json theo THU TU trong file, dung cho marker @CAST:id1,id2 — o ref chi loc theo LO
    o cho goi (doc_prompts_cast), KHONG loc o day."""
    cf = job / "characters.json"
    if not cf.is_file():
        return {}
    chars = json.loads(cf.read_text(encoding="utf-8")).get("characters", [])
    ra = {}
    for c in chars:
        cid = c.get("id")
        if not cid:
            continue
        master = (c.get("master") or "").strip()
        p = (job / master) if master else None
        ra[cid] = (c.get("name", "?"), c.get("age", "?"), p, trang_phuc(c.get("look", "")))
    return ra


def trang_phuc(look, n=70):
    """Rut cum trang phuc trong `look` de nhac anh biet anh nao vao o nao (chi la ghi chu tieng Viet)."""
    t = look
    m = re.search(r"\bwearing\b(.*)", look, re.S)
    if m:
        t = m.group(1).strip()
        m2 = re.search(r"\bsuch as\b(.*)", t, re.S)
        if m2:
            t = m2.group(1).strip()
    return " ".join(t.split())[:n]


def chon_dong(dong, tong):
    """"28-45" | "28-45,60-70" | "all" -> tap chi so 1-based."""
    if dong.strip().lower() in ("all", "tat-ca"):
        return set(range(1, tong + 1))
    ra = set()
    for khoi in dong.split(","):
        m = re.fullmatch(r"\s*(\d+)\s*-\s*(\d+)\s*", khoi) or re.fullmatch(r"\s*(\d+)\s*", khoi)
        if not m:
            sys.exit(f"LOI: --dong khong hieu khoi {khoi!r} (dung 28-45 hoac 28-45,60-70 hoac all)")
        a = int(m.group(1)); b = int(m.group(2)) if m.lastindex == 2 else a
        if a > b or a < 1:
            sys.exit(f"LOI: khoang {khoi!r} khong hop le")
        ra |= set(range(a, min(b, tong) + 1))
    if not ra:
        sys.exit("LOI: --dong khong chon duoc dong nao")
    return ra


def bang_marker(thu_tu_marker, slot_cua_mk):
    """marker -> danh sach chi so nhan vat. Ba kieu marker dang ton tai trong cac job:
       @REF/@REF1 = nhan vat 1 · @REF2 = nhan vat 2 · @REF12 = CA HAI (quy uoc lane F, xem
       flow_batch_laneF.MARKER_ORDER) · "@REF @REF2 " nhieu marker roi o dau dong (quy uoc simbot2).
    Sinh luon moi to hop >=2 (@REF12, @REF13, @REF23, @REF123...) roi khop DAI TRUOC."""
    from itertools import combinations
    n = len(thu_tu_marker)
    b = {"@REF": [0], "@REF1": [0]}
    for i in range(1, n):
        b[f"@REF{i + 1}"] = [i]
    for k in range(2, n + 1):
        for cb in combinations(range(n), k):
            b["@REF" + "".join(str(i + 1) for i in cb)] = list(cb)
    return {mk: v for mk, v in b.items() if all(i < n for i in v)}


def duoi_chung(mo_ta, toi_thieu=8):
    """Style suffix = duoi DAI NHAT giong nhau o MOI dong, cat ve ranh gioi ', ' cho sach clause.
    Nhieu job KHONG co duoi chung (moi dong tu mang style rieng) -> tra ve None, goi y --suffix-them."""
    chung = mo_ta[0]
    for t in mo_ta[1:]:
        while chung and not t.endswith(chung):
            chung = chung[1:]
    i = chung.find(", ")
    chung = chung[i + 2:] if i >= 0 else chung.lstrip(", ")
    return chung if len(chung) >= toi_thieu else None


def _cat_suffix_va_kiem(tho, suffix_tay, suffix_them):
    """Dung chung cho ca 2 bien the: quyet dinh suffix CAT hay NOI THEM, roi cat tung dong.
    `tho` = list (i, tags, line_tho). Tra ve (rows theo tag da lam san, suffix, cat)."""
    if suffix_them:
        return suffix_them, False
    suffix = suffix_tay or duoi_chung([t[2] for t in tho])
    if not suffix:
        print("\nLOI: cac dong nay KHONG co duoi chung nao de lam style suffix (moi dong tu mang style rieng).")
        for i, _, t in tho[:3]:
            print(f"   dong {i}: ...{t[-80:]}")
        sys.exit('  -> chon mot trong hai: --suffix "<duoi CO SAN o moi dong, tool se cat>"\n'
                 '                      hoac --suffix-them "16:9, no text"  (app noi them, khong cat gi)')
    return suffix, True


def doc_prompts(job, dong, thu_tu_marker, slot_cua_mk, ten_cua_mk, suffix_tay, suffix_them):
    """BIEN THE CU: @REF/@REF2/@REF12... nap toan bo tu nap_nhan_vat() (khong loc theo lo).
    Boc marker o dau dong -> TAG, cat style suffix -> description. Giu NGUYEN so dong goc lam NNN."""
    lines = (job / "img_prompts.txt").read_text(encoding="utf-8").splitlines()
    chon = chon_dong(dong, len(lines))
    bang = bang_marker(thu_tu_marker, slot_cua_mk)
    markers = sorted(bang, key=len, reverse=True)               # @REF12 truoc @REF2 truoc @REF
    tho = []
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or i not in chon:
            continue
        idx = []
        while True:
            for mk in markers:
                if line == mk or line.startswith(mk + " "):
                    idx += bang[mk]; line = line[len(mk):].lstrip(); break
            else:
                break
        idx = sorted(set(idx))                                   # thu tu chuan theo o ref, khong theo thu tu go
        for j in idx:                                            # ten nhan vat lap lai ngay sau marker
            ten = ten_cua_mk[thu_tu_marker[j]]
            if ten and line.startswith(ten + " "):
                line = line[len(ten) + 1:].lstrip()
        if line.startswith("@"):
            sys.exit(f"LOI dong {i}: con marker la {line.split()[0]} — chua co trong bang {sorted(bang)}.\n"
                     "  Job dung marker la thi phai them vao bang_marker(), dung doan.")
        tho.append((i, [slot_cua_mk[thu_tu_marker[j]] for j in idx], line))
    if not tho:
        sys.exit("LOI: khong co dong nao trong khoang da chon")

    suffix, cat = _cat_suffix_va_kiem(tho, suffix_tay, suffix_them)
    rows, dem = [], {}
    for i, tags, line in tho:
        if cat:
            if not line.endswith(suffix):
                sys.exit(f"LOI dong {i}: khong ket thuc bang style suffix -> khong cat duoc.\n"
                         f"  suffix: ...{suffix[-60:]}\n  dong  : ...{line[-60:]}")
            desc = line[: -len(suffix)].rstrip().rstrip(",").rstrip()
        else:
            desc = line
        if len(desc) < 40:
            sys.exit(f"LOI dong {i}: description con {len(desc)} ky tu sau khi cat suffix — nghi cat qua tay")
        tag = "+".join(tags) if tags else "PLAIN"
        dem[tag] = dem.get(tag, 0) + 1
        rows.append(f"{i:03d}|{tag}|{desc}")
    return rows, suffix, dem, cat


def doc_prompts_cast(job, dong, toan_bo_nv, suffix_tay, suffix_them):
    """BIEN THE MOI 2026-09-25: marker `@CAST:id1,id2[,id3] <mo ta>` khop THANG theo `id` trong
    characters.json (khong qua @REF/thu tu master). O anh goc tinh THEO LO: chi gom id XUAT HIEN
    trong cac dong --dong DA CHON, sap theo thu tu trong characters.json — job 8 nhan vat/tap nhung
    moi lo chi dung <=5 nguoi van chay duoc, khong con nap ca 8 nguoi lam tran khuon 5 o.
    Dong khong co @CAST -> PLAIN (canh vat, giu nguyen quy uoc cu)."""
    lines = (job / "img_prompts.txt").read_text(encoding="utf-8").splitlines()
    chon = chon_dong(dong, len(lines))
    tho = []            # (i, [id,...], mo_ta_tho)
    dung_id = set()
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or i not in chon:
            continue
        if line.startswith("@CAST:"):
            m = re.match(r"@CAST:([a-zA-Z0-9_,]+)\s+(.*)", line)
            if not m:
                sys.exit(f"LOI dong {i}: @CAST sai cu phap (dung @CAST:id1,id2 <mo ta>): {line[:70]!r}")
            ids = [x.strip() for x in m.group(1).split(",") if x.strip()]
            for cid in ids:
                if cid not in toan_bo_nv:
                    sys.exit(f"LOI dong {i}: @CAST dung id {cid!r} khong co trong characters.json.\n"
                             f"  Id hop le: {sorted(toan_bo_nv)}")
                if not toan_bo_nv[cid][2] or not toan_bo_nv[cid][2].is_file():
                    sys.exit(f"LOI dong {i}: nhan vat id={cid!r} khong co master (khong khoa mat) — "
                             f"khong dung duoc trong @CAST (chi nhan vat co 'ref':true/master moi dung).")
            dung_id.update(ids)
            desc = m.group(2).strip()
        elif line.startswith("@"):
            sys.exit(f"LOI dong {i}: marker la {line.split()[0]} nhung job nay dung kieu @CAST — "
                     f"dung '@CAST:id1,id2 <mo ta>' cho canh co nhan vat, hoac bo han marker cho canh vat.")
        else:
            ids, desc = [], line
        tho.append((i, ids, desc))
    if not tho:
        sys.exit("LOI: khong co dong nao trong khoang da chon")

    thu_tu_id = [cid for cid in toan_bo_nv if cid in dung_id]      # dung thu tu characters.json
    if len(thu_tu_id) > 5:
        dong_theo_id = {}
        for i, ids, _ in tho:
            for cid in ids:
                dong_theo_id.setdefault(cid, []).append(i)
        chi_tiet = "; ".join(f"{cid} (dong {min(dong_theo_id[cid])}-{max(dong_theo_id[cid])})" for cid in thu_tu_id)
        sys.exit(f"LOI: lo nay co {len(thu_tu_id)} nhan vat nhung khuon Create Tool chi co 5 o: {chi_tiet}\n"
                 f"  Tach --dong thanh nhieu lo nho hon (vd tach doan doi nhan vat).")

    slot_cua_id = {}
    for cid in thu_tu_id:
        slot = cid.upper()
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", slot):
            sys.exit(f"LOI: id {cid!r} -> ten o {slot!r} khong hop le (id phai chu+so+_ , bat dau bang chu cai)")
        slot_cua_id[cid] = slot
    if len(set(slot_cua_id.values())) != len(slot_cua_id):
        sys.exit(f"LOI: trung ten o sau khi viet HOA id: {slot_cua_id}")

    suffix, cat = _cat_suffix_va_kiem(tho, suffix_tay, suffix_them)
    rows, dem = [], {}
    for i, ids, line in tho:
        if cat:
            if not line.endswith(suffix):
                sys.exit(f"LOI dong {i}: khong ket thuc bang style suffix -> khong cat duoc.\n"
                         f"  suffix: ...{suffix[-60:]}\n  dong  : ...{line[-60:]}")
            desc = line[: -len(suffix)].rstrip().rstrip(",").rstrip()
        else:
            desc = line
        if len(desc) < 40:
            sys.exit(f"LOI dong {i}: description con {len(desc)} ky tu sau khi cat suffix — nghi cat qua tay")
        tags = [slot_cua_id[cid] for cid in thu_tu_id if cid in ids]
        tag = "+".join(tags) if tags else "PLAIN"
        dem[tag] = dem.get(tag, 0) + 1
        rows.append(f"{i:03d}|{tag}|{desc}")

    nv = {cid: toan_bo_nv[cid] for cid in thu_tu_id}
    return rows, suffix, dem, cat, nv, thu_tu_id, slot_cua_id


def dung_khoi_anh(slots, suffix, nnn_a, nnn_b):
    """Dien placeholder vao khuon. HAI BIEN THE:
       (a) job CO nhan vat  -> flow_tool_template_va3.txt   (o ref + thang fallback + cot strategy)
       (b) job KHONG nhan vat -> flow_tool_template_plain.txt (cat het 3 thu do, moi dong TAG PLAIN)
    Ban (b) on dinh hon vi phan lon su co da gap deu nam o khoi ref. Ca hai GIU 3 khoi bat buoc —
    kiem lai truoc khi tra ve, thieu la dung."""
    khuon = KHUON_REF if slots else KHUON_PLAIN
    if not khuon.is_file():
        sys.exit(f"LOI: thieu khuon {khuon}")
    body = khuon.read_text(encoding="utf-8")
    thieu = [k for k, v in MOC.items() if v not in body]
    if thieu:
        sys.exit(f"LOI: khuon {khuon.name} thieu khoi bat buoc: {thieu}")
    thay = [("SUFFIX", suffix), ("NNN_A", nnn_a), ("NNN_B", nnn_b)]
    if slots:
        n = len(slots)
        if n not in SO_CHU:
            sys.exit(f"LOI: khuon (a) chi ho tro 1-5 o ref, job nay co {n}")
        ds = ", ".join('"' + s + '"' for s in slots)
        # 1 o (2026-09-24, kenko ep02: 1 nhan vat): khong co "A and B" — chi 'exactly "MAIN"'
        nut = (", ".join('exactly "' + s + '"' for s in slots[:-1]) + f' and exactly "{slots[-1]}"'
               if n > 1 else f'exactly "{slots[0]}"')
        thay += [("N_WORD", SO_CHU[n][0]), ("N_WORD_LOW", SO_CHU[n][1]),
                 ("SLOT_LIST", ds), ("SLOT_A", slots[0]), ("SLOT_B", slots[1] if n > 1 else slots[0]),
                 ("SLOT_BUTTONS", nut)]
    for k, v in thay:
        body = body.replace("{" + k + "}", v)
    con = sorted(set(re.findall(r"\{[A-Z_]+\}", body)))
    if con:
        sys.exit(f"LOI: khuon con placeholder chua dien: {con}")
    return body


def dung_huong_dan(ten, job, dong, rows, dem, nv, slots, khoi_anh, slot_cua_mk, cat):
    nnn = [r.split("|")[0] for r in rows]
    co_tag = len([r for r in rows if r.split("|")[1] != "PLAIN"])
    L = ["=" * 72,
         f"PROMPT TAO TOOL cho Google Flow > Create Tool   —   {ten}",
         "=" * 72, "",
         f"Nguon: {job}",
         f"Khoi prompt: dong {dong} cua img_prompts.txt ({len(rows)} anh) — "
         + " · ".join(f"{k}={dem[k]}" for k in sorted(dem)),
         f"Khuon: {(KHUON_REF if slots else KHUON_PLAIN).name} — bien the "
         + ("(a) CO nhan vat" if slots else "(b) KHONG nhan vat, moi dong PLAIN")
         + " (da verify that: 18 anh/90s, 0 tin dung)", "",
         (f"1. UPLOAD {len(slots)} ANH REF — lay trong _ref_upload/, ten file TRUNG ten o:" if slots
          else "1. KHONG CO ANH REF — lo nay khong nhan vat nao lap lai, bo qua buoc upload."), ""]
    for mk, (ten_nv, tuoi, _, tp) in nv.items():
        slot = slot_cua_mk[mk]
        L.append(f'   O "{slot}"' + " " * max(1, 10 - len(slot)) + f"→ _ref_upload/{slot}.png   "
                 + f"{ten_nv} {tuoi} · {tp}")
    L += ["",
          ("   ⚠️ CHI upload file trong _ref_upload/ — do la anh master SACH da qua QC mat (da resize\n"
           f"      <={CANH_DAI_REF}px canh dai cho Flow tai nhanh), dung lay anh trong img/ cua tap "
           "(anh canh, mat nho, sai goc)." if slots
           else "   App dung ra se KHONG co o upload nao — dung di tim. Moi dong deu TAG PLAIN."), "",
          "2. DAN KHOI TIENG ANH duoi day vao o mo ta cua Create Tool:",
          ("   (style suffix duoi day DA duoc cat khoi tung dong trong flow_batch_prompts.txt — app noi lai)"
           if cat else
           "   (cac dong tu mang style rieng, khong cat gi; app CHI noi them style suffix duoi day)"), "",
          "=== DAN TU DAY ===", khoi_anh.rstrip("\n"), "=== DAN DEN DAY ===", "",
          ("3. Chon MOT model ho tro nhieu anh tham chieu (Nano Banana Pro) · Concurrency 6-8" if slots
           else "3. Chon model Nano Banana Pro · Concurrency 6-8 (khong can model ho tro anh tham chieu)"),
          f"   · Project name: {ten}",
          '   · dan flow_batch_prompts.txt · bam "Generate All"',
          "   · mot so ban dung co nut \"Parse Lines\" — phai bam TRUOC khi Generate All", "",
          "4. BA KHOI BAT BUOC trong khoi tieng Anh (tool da kiem, dung go khi sua tay):",
          "   · Interface contract — thieu la moi lan dung ra mot app khac, khong tu dong hoa noi",
          "   · Cam IndexedDB + tu tai ZIP + banner do cam reload — iframe doi ORIGIN moi lan tai trang",
          "     nen moi luu tru trinh duyet chet theo; day la loi giai vu \"dung cam o 46/85, mat sach anh\"",
          "   · attempts la so lan goi THAT (1 neu an ngay) — ban thieu cau nay ghi attempts=4 ca 18 dong", "",
          "   Va 3 diem da chot tu truoc: bo han nhanh (c) \"het cach thi ve khong ref\" (anh dep nhung",
          "   SAI MAT, chi lo ra luc ghep video) · co manifest.csv trong ZIP · ep xoa kho cu khi doi ten project.", "",
          "5. BA LUAT VAN HANH khi chay lo — khong lam du la mat hang:",
          "   (1) TUYET DOI khong reload/F5 khi dang chay. Tai ZIP xong moi duoc dung vao trang.",
          "   (2) LUON tu bam \"Download ZIP\" roi DEM anh trong file. ZIP tu dong da 2 lan ban luc moi",
          "       xong 12/18 va ra file 830 byte chi co manifest, khong mot anh nao.",
          "   (3) Lo dai thi bam Download ZIP giua chung vai lan (nut nay tai duoc phan da xong bat cu luc nao).", "",
          "6. NGHIEM THU — bat buoc chay, dung mat bang mat:",
          f"   py -3.13 {NGHIEMTHU} <file.zip>",
          f"   Kiem: du {len(rows)} anh · giu NGUYEN NNN {min(nnn)}..{max(nnn)} (KHONG duoc danh lai 001...) ·",
          "   md5 khac nhau doi mot · 1376×768 · manifest du dong, attempts khong phai hang so ·",
          ("   strategy=a cho MOI dong co nhan vat (tut xuong b = chi giu 1 mat trong canh 2 nguoi "
           "⇒ lam lai ca lo) ·" if slots else "   (bien the b: manifest KHONG co cot strategy) ·"),
          "   failed_prompts.txt rong",
          (f"   Roi mo {min(co_tag, 6)} anh co TAG so mat voi _ref_upload/ — sai 1 anh la hong ca lo."
           if slots else "   Lo nay khong co mat nhan vat nen khong phai so mat."), ""]
    return "\n".join(L)


def luu_anh_ref(src, dst, canh_dai=CANH_DAI_REF):
    """Copy anh master vao _ref_upload/, THU NHO neu canh dai > canh_dai px — anh master GOC
    (_ref_<id>\\001.png) KHONG bi dong den. Ly do: PNG 2-4MB lam picker Flow ket "Dang tai len"
    (do that 2026-09-24: 2 lan lien khong xong sau 90s); ban ~1600px ~1,8MB len trong ~20s."""
    from PIL import Image
    im = Image.open(src)
    w, h = im.size
    if max(w, h) <= canh_dai:
        shutil.copy2(src, dst)
        return
    ti_le = canh_dai / max(w, h)
    if im.mode not in ("RGB", "RGBA", "L"):
        im = im.convert("RGB")
    im = im.resize((max(1, round(w * ti_le)), max(1, round(h * ti_le))), Image.LANCZOS)
    im.save(dst, "PNG")


def main():
    ap = argparse.ArgumentParser(description="Sinh bo 3 file cho Google Flow > Create Tool")
    ap.add_argument("--job", required=True, help="slug trong FlowHandoff_local\\jobs (phang hoac jobs\\<tab>\\slug) hoac duong dan day du")
    ap.add_argument("--dong", required=True, help="28-45 | 28-45,60-70 | all")
    ap.add_argument("--ten", help="project name (mac dinh = slug)")
    ap.add_argument("--out", help="thu muc ra (mac dinh assets\\_flow_tool_mau\\<ten>)")
    ap.add_argument("--slot", action="append", default=[], metavar="@REF=MAIN",
                    help="doi ten o ref cho job kieu @REF cu (lap lai duoc); khong dung duoc cho job @CAST")
    ap.add_argument("--suffix", help="style suffix CO SAN o cuoi moi dong -> tool cat, app noi lai "
                                     "(mac dinh: tu do duoi chung)")
    ap.add_argument("--suffix-them", dest="suffix_them",
                    help="style suffix app NOI THEM, khong cat gi — dung cho job moi dong tu mang style rieng")
    ap.add_argument("--khong-ref", action="store_true", dest="khong_ref",
                    help="ep dung bien the (b) — moi dong PLAIN, khong o ref (chi dung cho job kieu @REF cu)")
    ap.add_argument("--kiem", action="store_true", help="chi in ke hoach, KHONG ghi file")
    ap.add_argument("--ghi-de", action="store_true", dest="ghi_de", help="cho ghi de thu muc ra da co file")
    a = ap.parse_args()

    job = Path(a.job) if Path(a.job).is_absolute() else tim_job(a.job)
    if not (job / "img_prompts.txt").is_file():
        sys.exit(f"LOI: {job} khong co img_prompts.txt")
    # characters.json KHONG bat buoc: thieu = job khong nhan vat = bien the (b)
    ten = a.ten or job.name
    out = Path(a.out) if a.out else OUT_ROOT / ten

    if a.suffix and a.suffix_them:
        sys.exit("LOI: --suffix va --suffix-them loai tru nhau (mot cai CAT, mot cai NOI THEM)")

    dong_goc = (job / "img_prompts.txt").read_text(encoding="utf-8").splitlines()
    co_cast = any(l.strip().startswith("@CAST:") for l in dong_goc)

    if co_cast:
        # ---------- BIEN THE MOI: @CAST:id1,id2 — o ref tinh THEO LO --------------------------
        if a.khong_ref:
            sys.exit("LOI: --khong-ref khong dung cho job kieu @CAST (dong khong @CAST tu nhien la PLAIN)")
        if a.slot:
            sys.exit("LOI: --slot khong dung cho job kieu @CAST (ten o = id nhan vat viet HOA, co dinh)")
        toan_bo_nv = nap_toan_bo_nhan_vat(job)
        if not toan_bo_nv:
            sys.exit("LOI: job co marker @CAST nhung khong doc duoc characters.json (hoac file rong)")
        print(f"job kieu @CAST — {len(toan_bo_nv)} nhan vat trong characters.json, o ref tinh rieng theo lo")
        rows, suffix, dem, cat, nv, thu_tu, slot_cua_mk = doc_prompts_cast(
            job, a.dong, toan_bo_nv, a.suffix, a.suffix_them)
    else:
        # ---------- BIEN THE CU: @REF/@REF2/@REF12... (khong doi, khong hoi quy) --------------
        nv = {} if a.khong_ref else nap_nhan_vat(job)
        if a.khong_ref:
            print("--khong-ref: ep bien the (b), bo qua nhan vat cua job")
        if not nv:
            print("job KHONG co nhan vat co anh master -> BIEN THE (b): moi dong TAG PLAIN, khong o ref")
        thu_tu = list(nv)                                            # @REF, @REF2, ... theo thu tu nhan vat
        slot_cua_mk = {mk: (SLOT_MAC_DINH[i] if i < len(SLOT_MAC_DINH) else f"SLOT{i + 1}")
                       for i, mk in enumerate(thu_tu)}
        if a.slot and not nv:
            sys.exit("LOI: --slot khong dung duoc cho job khong co nhan vat")
        for d in a.slot:
            mk, _, s = d.partition("=")
            if mk.strip() not in nv or not s.strip():
                sys.exit(f"LOI: --slot {d!r} — marker phai la mot trong {thu_tu}")
            slot_cua_mk[mk.strip()] = s.strip()
        if any(not re.fullmatch(r"[A-Z][A-Z0-9_]*", slot_cua_mk[mk]) for mk in thu_tu):
            sys.exit(f"LOI: ten o ref phai CHU IN ASCII (app doc dung text nut nay): "
                     f"{[slot_cua_mk[mk] for mk in thu_tu]}")
        if len(set(slot_cua_mk[mk] for mk in thu_tu)) != len(thu_tu):
            sys.exit(f"LOI: ten o ref trung nhau: {[slot_cua_mk[mk] for mk in thu_tu]}")

        ten_cua_mk = {mk: nv[mk][0] for mk in thu_tu}
        rows, suffix, dem, cat = doc_prompts(job, a.dong, thu_tu, slot_cua_mk, ten_cua_mk,
                                             a.suffix, a.suffix_them)

    slots = [slot_cua_mk[mk] for mk in thu_tu]
    nnn = [r.split("|")[0] for r in rows]
    khoi = dung_khoi_anh(slots, suffix, nnn[0], nnn[1] if len(nnn) > 1 else nnn[0])
    hd = dung_huong_dan(ten, job, a.dong, rows, dem, nv, slots, khoi, slot_cua_mk, cat)

    print(f"\nproject : {ten}")
    print(f"ra      : {out}")
    print("o ref   : " + " · ".join(f"{slot_cua_mk[mk]}={nv[mk][0]} ({nv[mk][2].name})" for mk in thu_tu))
    print(f"anh     : {len(rows)} dong, NNN {min(nnn)}..{max(nnn)} — "
          + " · ".join(f"{k}={dem[k]}" for k in sorted(dem)))
    print(f"suffix  : [{'CAT khoi tung dong' if cat else 'chi NOI THEM'}] "
          f"{suffix[:80]}{'...' if len(suffix) > 80 else ''}")
    if a.kiem:
        print("\n--kiem: KHONG ghi file nao.")
        return
    if out.exists() and any(out.iterdir()) and not a.ghi_de:
        sys.exit(f"\nLOI: {out} da co file. Xem lai roi chay lai kem --ghi-de neu chac.")
    out.mkdir(parents=True, exist_ok=True)
    if nv:
        (out / "_ref_upload").mkdir(parents=True, exist_ok=True)
        for mk in nv:
            luu_anh_ref(nv[mk][2], out / "_ref_upload" / f"{slot_cua_mk[mk]}.png")
    (out / "flow_batch_prompts.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (out / "flow_create_tool_prompt.txt").write_text(hd, encoding="utf-8")
    print(f"\nDA GHI 3 thu vao {out}:")
    print(f"  flow_create_tool_prompt.txt   {len(hd)} ky tu")
    print(f"  flow_batch_prompts.txt        {len(rows)} dong")
    print("  _ref_upload\\                  "
          + (", ".join(f"{slot_cua_mk[mk]}.png" for mk in nv) if nv else "(khong co — bien the b)"))


if __name__ == "__main__":
    main()
