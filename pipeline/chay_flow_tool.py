r"""chay_flow_tool.py — chay MOT LO anh bang "Create Tool" cua Google Flow, tu bo 3 file
do `don_flow_tool.py` sinh ra.

    py -3.14 pipeline\chay_flow_tool.py --bo3 "assets\_flow_tool_mau\<ten>" [--port 9337] [--parallel 6]
    py -3.14 pipeline\chay_flow_tool.py --bo3 ... --kiem     ← chi kiem bo 3 file, KHONG mo Chrome

⚠️ PHAI DUNG py -3.14 (may nay chi ban 3.14 co playwright).
⚠️ KHONG PHAI "chay nen khong ai trong". Kiem chung that 2026-09-23: 3 luot thi 2 luot tu dong
   trot lot, 1 luot phai cuu tay. Luon co nguoi ngo tren man hinh khi no chay.

Port tu `D:\CLAUDE\RENDER_IMG\flow_tool_trial.py` (ban da chay duoc), bo phan do dac cua thu nghiem
va TONG QUAT hoa: so o ref / ten o / so dong / ten project deu doc tu bo 3 file, khong khoa cung.
BO HAN buoc `pg.reload()` cuoi cua ban trial: do la phep DO do ben, con chay that thi reload chinh
la thu lam mat sach anh (iframe doi origin moi lan tai trang).

3 kieu hong khi dang chay — deu da cai san (GIAO_VIEC_H2DEV.md):
  1. Treo vinh vien o RUNNING (app loi JS, dong khong bao gio sang FAILED) -> phat hien DUNG HINH
     qua `--dung-hinh` giay roi bam nut "Sua loi" cua Flow.
  2. Va xong app dung LAI SACH TRON (mat ref, mat don, Generate All khoa) -> tu nap lai toan bo
     roi bam Generate All lan nua.
  3. App reset bang dem ve 0 + ban ZIP rong NHUNG anh con trong RAM -> doc "images in memory",
     coi la xong, bam lai nut ZIP. CAM ket luan "mat lo" truoc khi lam hai viec do.
"""
import argparse
import json
import os
import re
import sys
import time
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
RENDER_IMG = r"D:\CLAUDE\RENDER_IMG"
MOC_DAU, MOC_CUOI = "=== DAN TU DAY ===", "=== DAN DEN DAY ==="


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)


# ---------------------------------------------------------------- doc bo 3 file
def doc_bo3(bo3):
    """-> dict(prompt, dong, so_dong, slots, ref{slot:path}, ten). Khong khoa cung gi."""
    d = Path(bo3)
    hd, don = d / "flow_create_tool_prompt.txt", d / "flow_batch_prompts.txt"
    for f in (hd, don):
        if not f.is_file():
            sys.exit(f"LOI: thieu {f} — --bo3 phai tro vao thu muc do don_flow_tool.py sinh")
    txt = hd.read_text(encoding="utf-8")
    if MOC_DAU not in txt or MOC_CUOI not in txt:
        sys.exit(f"LOI: {hd.name} khong co cap moc {MOC_DAU} / {MOC_CUOI}")
    prompt = txt.split(MOC_DAU, 1)[1].split(MOC_CUOI, 1)[0].strip()
    for phai_co in ("Interface contract - these exact names",
                    "Do NOT rely on IndexedDB or localStorage",
                    "must be the real number of image-generation calls actually made"):
        if phai_co not in prompt:
            sys.exit(f"LOI: khoi prompt thieu khoi bat buoc: {phai_co[:50]}... — dung khuon _va3")
    dong = don.read_text(encoding="utf-8").strip()
    rows = [x for x in dong.splitlines() if x.strip()]
    slots = []
    for r in rows:
        for t in r.split("|")[1].split("+"):
            if t != "PLAIN" and t not in slots:
                slots.append(t)
    ref = {}
    for s in slots:
        pp = d / "_ref_upload" / f"{s}.png"
        if not pp.is_file():
            sys.exit(f"LOI: thieu anh ref {pp} (don co TAG {s})")
        ref[s] = pp
    # slots rong = BIEN THE (b): lo toan PLAIN, app dung ra khong co o upload nao
    m = re.search(r"Project name:\s*(\S+)", txt)
    return {"prompt": prompt, "dong": dong, "so_dong": len(rows), "slots": slots,
            "ref": ref, "ten": m.group(1) if m else d.name}


# ---------------------------------------------------------------- tien ich UI (giu nguyen tu ban trial)
def app_frame(pg, tu_mo=True):
    """Tim iframe cua app theo SRC, KHONG theo kich thuoc: co ban dung Flow de khung xem truoc
    rong 0px (panel 'Trinh tao cong cu' chiem cho), loc theo width>300 se tuong app chua dung xong."""
    ds = pg.evaluate(
        "() => [...document.querySelectorAll('iframe')]"
        ".map(e => ({src: e.src || '', w: Math.round(e.getBoundingClientRect().width)}))"
        ".filter(o => o.src && !o.src.includes('recaptcha') && !o.src.includes('accounts.google'))")
    if not ds:
        return None
    o = ds[0]
    if o["w"] < 300 and tu_mo:
        pg.evaluate(
            "() => { for (const e of document.querySelectorAll('button,div,span')) {"
            " const t = (e.innerText || '').trim();"
            " if ((t === 'Xem trước' || t === 'Preview') && e.getBoundingClientRect().width > 0)"
            " { e.click(); return true; } } return false; }")
        pg.wait_for_timeout(5000)
        return app_frame(pg, False)
    return pg.frame_locator("iframe[src*='" + o["src"].split("//")[1][:24] + "']")


def cho_app(pg, giay=180):
    """Lay lai frame SAU khi Flow va loi: app duoc dung LAI TU DAU voi iframe src MOI, va iframe co mat
    TRUOC khi app render xong. Doi cung 6s roi dien ngay = `Locator.fill` timeout vi chua co textarea
    (da dinh that 2026-09-24). Cho toi khi app that su co >=3 nut VA co textarea."""
    t0 = time.time()
    while time.time() - t0 < giay:
        fl = app_frame(pg)
        if fl:
            try:
                if fl.locator("button").count() >= 3 and fl.locator("textarea").count():
                    log(f"  app da render lai sau {int(time.time()-t0)}s")
                    return fl
            except Exception:
                pass
        pg.wait_for_timeout(5000)
    return None


JS_XONG = r"""(n) => {
  const rows = (document.body.innerText || '').split(String.fromCharCode(10))
      .map(s => s.trim()).filter(Boolean);
  const LAB = ['TOTAL','DONE','RUNNING','FAILED','PENDING','REMAINING'];
  const doc = (buoc) => { const d = {};
    for (const k of LAB) { const i = rows.indexOf(k); if (i < 0) continue;
      const j = i + buoc;
      if (j >= 0 && j < rows.length && /^[0-9]+$/.test(rows[j])) d[k] = +rows[j]; }
    return d; };
  const ung = [doc(1), doc(-1)].filter(d => Object.keys(d).length);
  if (ung.length) {
    ung.sort((a, b) => ((b.TOTAL === n) - (a.TOTAL === n))
                       || (Object.keys(b).length - Object.keys(a).length));
    const d = ung[0];
    if ((d.DONE || 0) + (d.FAILED || 0) >= n) return true;
  }
  const m = (document.body.innerText || '')
      .match(/([0-9]+)\s*images? in memory|in memory[:\s]*([0-9]+)/i);
  if (m) { const v = parseInt(m[1] || m[2], 10); if (v >= n) return true; }
  return false;
}"""


def khung_that(pg):
    """Frame THAT cua app (khac frame_locator): can de goi wait_for_function — cho TRONG TRINH DUYET,
    dieu kien dung la bat ra NGAY, khong phai ngoi doi het mot nhip poll 20s roi moi biet."""
    for f in pg.frames:
        u = f.url or ""
        if u and "recaptcha" not in u and "accounts.google" not in u and f != pg.main_frame:
            return f
    return None


def ov_buttons(pg):
    return pg.evaluate(
        "() => [...document.querySelectorAll('.cdk-overlay-container button')]"
        ".map(b => ({t:(b.innerText||'').trim().split(String.fromCharCode(10)).join(' '),"
        " x:Math.round(b.getBoundingClientRect().x+b.getBoundingClientRect().width/2),"
        " y:Math.round(b.getBoundingClientRect().y+b.getBoundingClientRect().height/2)}))")


JS_SET = """(el, v) => {
     const proto = el.tagName === 'TEXTAREA'
         ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
     Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, v);
     el.dispatchEvent(new Event('input', {bubbles: true}));
     el.dispatchEvent(new Event('change', {bubbles: true})); }"""


def dat_chu(loc, v):
    """fill() cua Playwright CHI doi value trong DOM: co ban dung van thay du 4.706 ky tu trong
    textarea nhung state React van rong -> Generate All khoa vinh vien. Phai goi native setter."""
    loc.fill(v)
    loc.evaluate(JS_SET, v)


def dat_so(fl, v):
    for kieu in ("number", "range"):                 # ban khac dung thanh truot thay o so
        loc = fl.locator(f"input[type={kieu}]")
        if loc.count():
            if kieu == "number":
                loc.first.fill(str(v))
            else:
                loc.first.evaluate(JS_SET, str(v))
            return kieu
    return None


def bam_chu(fl, chu):
    """Uu tien the <button>: ban dung hay dat tieu de trung chu voi nut ('CHARACTER REF: MAIN'
    vs nut 'MAIN') — bam nham tieu de thi khong co gi xay ra."""
    rx = re.compile(chu, re.I)
    nut = fl.locator("button").filter(has_text=rx)
    loc = nut.first if nut.count() else fl.get_by_text(rx).first
    loc.scroll_into_view_if_needed()
    loc.click()


def dat_ref(pg, fl, slot, path, cho_upload=90):
    """HAI kieu tuy ban dung: (1) input file thuong, (2) media picker cua Flow.
    Thu (1) truoc voi timeout ngan, khong thi cho overlay — khong do ca hai se ngoi cho mot cai
    overlay khong bao gio hien. Thu vien media RIENG theo project nen project moi luon upload lai."""
    try:
        with pg.expect_file_chooser(timeout=9000) as fc:
            bam_chu(fl, r"\b" + slot + r"\b")
        fc.value.set_files(str(path))
        pg.wait_for_timeout(4000)
        log(f"  {slot}: nap thang qua input file")
        return
    except Exception:
        pass
    t_mo = time.time()
    while time.time() - t_mo < 30 and not ov_buttons(pg):   # picker co the mat ~15s moi hien
        pg.wait_for_timeout(2000)
    btns = ov_buttons(pg)
    if not btns:
        raise RuntimeError(f"{slot}: picker khong mo sau 30s")
    ten = path.name
    san = [b for b in btns if ten in b["t"] and "ang t" not in b["t"]]   # 'Dang tai len' = chua xong
    if not san:
        up = [b for b in btns if b["t"].lower().startswith("upload")]
        if not up:
            raise RuntimeError(f"{slot}: khong thay nut upload: {[b['t'][:30] for b in btns]}")
        with pg.expect_file_chooser(timeout=30000) as fc:
            pg.mouse.click(up[0]["x"], up[0]["y"])
        fc.value.set_files(str(path))
        t0 = time.time()
        while time.time() - t0 < cho_upload and not san:
            pg.wait_for_timeout(3000)
            san = [b for b in ov_buttons(pg) if ten in b["t"] and "ang t" not in b["t"]]
        if not san:
            raise RuntimeError(f"{slot}: upload {ten} khong xong sau {cho_upload}s")
        log(f"  {slot}: upload xong sau {int(time.time()-t0)}s")
    pg.mouse.click(san[0]["x"], san[0]["y"])           # bam khi con 'Dang tai len' la ket dialog
    pg.wait_for_timeout(3000)
    con = ov_buttons(pg)
    if con:
        pg.mouse.click(con[-1]["x"], con[-1]["y"])
        pg.wait_for_timeout(3000)
    if pg.locator(".cdk-overlay-backdrop").count():
        raise RuntimeError(f"{slot}: picker khong dong")


def sua_loi_neu_can(pg, cho=240):
    """KIEU HONG 1: app Flow tu sinh co the tham chieu bien khong ton tai -> moi lenh sinh anh loi
    ngam, dong nam mai o RUNNING, KHONG BAO GIO sang FAILED. Flow hien thanh do + nut 'Sua loi'."""
    if not pg.evaluate(
            "() => { for (const b of document.querySelectorAll('button')) {"
            " const t = (b.innerText || '').trim().toLowerCase();"
            " if ((t === 'sửa lỗi' || t === 'fix error' || t === 'fix')"
            "     && b.getBoundingClientRect().width > 0) { b.click(); return true; } } return false; }"):
        return False
    log("  app loi JavaScript -> bam 'Sua loi', cho Flow va lai")
    t0 = time.time()
    while time.time() - t0 < cho:
        pg.wait_for_timeout(15000)
        if not pg.evaluate(
                "() => [...document.querySelectorAll('button')].some(b =>"
                " ['sửa lỗi','fix error','fix'].includes((b.innerText||'').trim().toLowerCase())"
                " && b.getBoundingClientRect().width > 0)"):
            log(f"  va xong sau {int(time.time()-t0)}s")
            return True
    log("  van con loi sau khi bam 'Sua loi'")
    return True


NHAN = ("TOTAL", "DONE", "RUNNING", "FAILED", "PENDING", "REMAINING")


def doc_so(rows, so_dong):
    """Ban nay de so TRUOC nhan ('18 / DONE'), ban kia de SAU ('DONE / 18'). Doc nham chieu thi
    TOTAL bi doc thanh DONE -> tuong xong ngay giay thu 20, hoac nguoc lai tuong DONE=0 mai ->
    bao dung hinh oan roi bam 'Sua loi' lam app dung lai tu dau (mat ca lo dang chay).

    CHOT CHIEU: 'TOTAL == so dong' KHONG du de phan xu — lo ma DONE cung bang TOTAL (luc xong,
    hoac lo nho) thi CA HAI chieu deu cho TOTAL dung (do that: lo 6 dong, chieu sai van ra
    TOTAL=6 nhung DONE=0). Nen phai cong them: chieu nao doc duoc NHIEU nhan hon va khong pha
    rang buoc DONE+RUNNING+FAILED <= TOTAL thi chieu do moi dung."""
    ung = []
    for buoc in (1, -1):
        d = {}
        for k in NHAN:
            if k in rows:
                j = rows.index(k) + buoc
                if 0 <= j < len(rows) and re.fullmatch(r"\d+", rows[j]):
                    d[k] = int(rows[j])
        if d:
            hop_le = sum(d.get(k, 0) for k in ("DONE", "RUNNING", "FAILED")) <= d.get("TOTAL", 10 ** 9)
            ung.append((d.get("TOTAL") == so_dong, hop_le, len(d), d))
    if not ung:
        return {}
    return max(ung, key=lambda x: (x[0], x[1], x[2]))[3]


def than(fl):
    return [x.strip() for x in fl.locator("body").inner_text().split("\n") if x.strip()]


# ---------------------------------------------------------------- chay
def nap_du_lieu(pg, fl, bo):
    """KIEU HONG 2 dung ham nay: moi lan Flow va loi xong, app dung LAI SACH TRON -> goi lai het."""
    for s in bo["slots"]:                    # bien the (b): rong -> khong nap ref gi ca
        dat_ref(pg, fl, s, bo["ref"][s])
    dat_chu(fl.locator("textarea").first, bo["dong"])
    if fl.locator("input[type=text]").count():
        dat_chu(fl.locator("input[type=text]").first, bo["ten"])
    dat_so(fl, bo["parallel"])
    pg.wait_for_timeout(1500)
    log(f"  da nap {len(bo['slots'])} ref + {bo['so_dong']} dong, parallel={bo['parallel']}")


def bam_generate(pg, fl):
    """Mot so ban dung bat bam 'Parse Lines' truoc, chua parse thi Generate All bi khoa."""
    p = fl.locator("button").filter(has_text=re.compile(r"parse", re.I))
    if p.count():
        p.first.click()
        pg.wait_for_timeout(4000)
        log("  da bam 'Parse Lines'")
    nut = fl.locator("button").filter(has_text=re.compile(r"generate\s*all", re.I)).first
    for _ in range(15):
        if not nut.is_disabled():
            break
        pg.wait_for_timeout(2000)
    if nut.is_disabled():
        raise RuntimeError("nut Generate All van bi khoa sau 30s")
    nut.click()
    return nut


def retry_failed(pg, fl, so_dong, vong=2):
    """Bam nut "Retry Failed" cua app de ve lai CHI nhung dong FAILED, roi cho lai.
    Khe uoc giao dien bat app phai co nut nay; khong co thi bao ro chu khong im lang bo qua.
    Tra ve (so_lan_bam, dem_cuoi)."""
    lan = 0
    for _ in range(vong):
        so = doc_so(than(fl), so_dong)
        if so.get("FAILED", 0) <= 0:
            break
        nut = fl.locator("button").filter(has_text=re.compile(r"retry", re.I))
        if not nut.count():
            co = [fl.locator("button").nth(i).inner_text().strip()
                  for i in range(fl.locator("button").count())]
            log(f"  CO {so.get('FAILED')} dong FAILED nhung app KHONG co nut Retry — cac nut: {co}")
            break
        log(f"  {so.get('FAILED')} dong FAILED -> bam 'Retry Failed' (vong {lan + 1})")
        nut.first.click()
        lan += 1
        t0 = time.time()
        while time.time() - t0 < 900:
            kt = khung_that(pg)
            try:
                if kt:
                    kt.wait_for_function(JS_XONG, arg=so_dong, timeout=30000)
                    break
                pg.wait_for_timeout(5000)
            except Exception:
                pass
        moi_so = doc_so(than(fl), so_dong)
        log(f"  sau retry: {moi_so}")
        if moi_so.get("FAILED", 0) <= 0:
            break
    return lan, doc_so(than(fl), so_dong)


def tai_zip(pg, fl, dich, so_dong):
    """ZIP tu dong KHONG dang tin: do that no ban luc moi xong 12/18, ra file 830 byte chi co
    manifest. Luon tu bam nut roi DEM anh; thieu thi bam lai lan 2."""
    nut = fl.locator("button").filter(has_text=re.compile(r"zip", re.I))
    if not nut.count():
        co = [fl.locator("button").nth(i).inner_text().strip() for i in range(fl.locator("button").count())]
        raise RuntimeError("KHONG THAY NUT TAI ZIP — dung lai, DUNG reload. Cac nut: " + str(co))
    for lan in (1, 2):
        with pg.expect_download(timeout=180000) as dl:
            nut.first.click()
        d = dl.value
        p = dich / f"lo_thu{lan}_{d.suggested_filename or 'batch.zip'}"
        d.save_as(str(p))
        try:
            n = len([x for x in zipfile.ZipFile(p).namelist() if x.lower().endswith((".png", ".jpg", ".jpeg"))])
        except Exception as e:
            n = -1
            log(f"  ZIP hong: {str(e)[:60]}")
        log(f"  ZIP lan {lan}: {p.stat().st_size} bytes, {n} anh")
        if n >= so_dong:
            return p
        pg.wait_for_timeout(10000)
    raise RuntimeError("ZIP thieu anh sau 2 lan bam — DUNG reload, anh con trong RAM, bam tay them lan nua")


def main():
    ap = argparse.ArgumentParser(description="Chay 1 lo anh bang Google Flow Create Tool")
    ap.add_argument("--bo3", required=True, help="thu muc bo 3 file cua don_flow_tool.py")
    ap.add_argument("--port", default="9337", help="cong CDP cua Chrome Flow (9333 | 9337)")
    ap.add_argument("--parallel", default="6")
    ap.add_argument("--timeout", type=int, default=2400, help="tran giay cho ca lo")
    ap.add_argument("--dung-hinh", type=int, default=300, dest="dung_hinh",
                    help="bao nhieu giay khong doi so thi coi la treo roi bam 'Sua loi'")
    ap.add_argument("--out", help="thu muc luu ZIP (mac dinh <bo3>\\_ket_qua)")
    ap.add_argument("--kiem", action="store_true", help="chi kiem bo 3 file, KHONG mo Chrome")
    a = ap.parse_args()

    bo = doc_bo3(a.bo3)
    bo["parallel"] = a.parallel
    print(f"bo 3   : {Path(a.bo3)}")
    print(f"project: {bo['ten']}")
    print(f"don    : {bo['so_dong']} dong | o ref: " + " · ".join(
        f"{s}={bo['ref'][s].name}" for s in bo["slots"]))
    print(f"prompt : {len(bo['prompt'])} ky tu (du 3 khoi bat buoc)")
    if a.kiem:
        print("\n--kiem: bo 3 file HOP LE, khong mo Chrome.")
        return 0

    dich = Path(a.out) if a.out else Path(a.bo3) / "_ket_qua"
    dich.mkdir(parents=True, exist_ok=True)
    os.environ["FLOW_CDP"] = f"http://127.0.0.1:{a.port}"
    sys.path.insert(0, RENDER_IMG)
    try:
        from flow_lib import Flow
    except ImportError:
        sys.exit(f"LOI: khong import duoc flow_lib tu {RENDER_IMG} (can playwright -> py -3.14)")

    kq = {"bo3": str(a.bo3), "port": a.port, "parallel": a.parallel, "so_dong": bo["so_dong"],
          "bat_dau": time.strftime("%Y-%m-%d %H:%M:%S"), "va_giua_chung": 0}
    f = Flow()
    pg = f.pg
    try:
        pg.goto("https://flow.google.com/")
        pg.wait_for_timeout(8000)
        f.wait_no_overlay()
        if not pg.evaluate(
                "() => { for (const e of document.querySelectorAll('button,div,a')) {"
                " const t=(e.innerText||'').trim();"
                " if ((t.includes('New project')||t.includes('n mới')) && t.length<24"
                "     && e.getBoundingClientRect().width>0) { e.click(); return true; } } return false; }"):
            raise RuntimeError("khong bam duoc nut tao project moi")
        pg.wait_for_timeout(11000)
        f.wait_no_overlay()
        proj = pg.url.rstrip("/")
        kq["project"] = proj.rsplit("/", 1)[-1]
        log(f"project moi: {kq['project']}")

        pg.goto(proj + "/create-tool")
        pg.wait_for_timeout(8000)
        f.wait_no_overlay()
        ed = pg.locator(".base-prompt-box .ProseMirror").first
        f.click_xy(ed)
        pg.wait_for_timeout(500)
        pg.keyboard.insert_text(bo["prompt"])
        pg.wait_for_timeout(1500)
        da = pg.evaluate("() => document.querySelector('.base-prompt-box .ProseMirror').innerText")
        if abs(len(da) - len(bo["prompt"])) > 300:
            raise RuntimeError(f"prompt dan thieu: {len(da)}/{len(bo['prompt'])}")
        t0 = time.time()
        nut = pg.locator('button[aria-label="Bắt đầu tạo"]')
        if not nut.count():
            nut = pg.locator(".create-applet-prompt-box-wrapper button, .base-prompt-box button").last
        f.click_xy(nut.first if nut.count() else nut)
        pg.wait_for_timeout(20000)
        if "/tool/" not in pg.url:
            raise RuntimeError(f"bam submit khong an, van o {pg.url[-40:]}")

        # iframe co mat TRUOC khi app render xong; Flow con dung loi TAM THOI ('Da xay ra loi'
        # + nut Thu lai) — cung mot prompt luc loi luc dung, phai tu thu lai chu dung ket luan
        # tai khoan hong.
        fl, thu_lai = None, 0
        while time.time() - t0 < 900:
            fl = app_frame(pg)
            if fl:
                try:
                    if fl.locator("button").count() >= 3 and fl.locator("textarea").count():
                        break
                except Exception:
                    pass
            fl = None
            if thu_lai < 3:
                bam = pg.evaluate(
                    "() => { const ds=[...document.querySelectorAll('button')]"
                    "  .filter(b=>b.getBoundingClientRect().width>0 && !b.disabled);"
                    " for (const b of ds) { const t=(b.innerText||'').trim().toLowerCase();"
                    "   if (t==='thử lại'||t==='retry'||t==='try again') { b.click(); return t; } }"
                    " const co=document.body.innerText.includes('xảy ra lỗi')"
                    "   || document.body.innerText.toLowerCase().includes('went wrong');"
                    " if (co) { for (const b of ds) { if ((b.innerText||'').trim()==='arrow_forward')"
                    "   { b.click(); return 'gui lai'; } } } return null; }")
                if bam:
                    thu_lai += 1
                    log(f"  Flow bao loi dung app -> '{bam}' (lan {thu_lai})")
            pg.wait_for_timeout(15000)
        if sua_loi_neu_can(pg):
            fl = cho_app(pg) or fl
        if not fl:
            raise RuntimeError(f"Flow khong dung xong app trong 900s (da thu lai {thu_lai} lan)")
        kq["giay_dung_app"] = int(time.time() - t0)
        kq["thu_lai_dung_app"] = thu_lai
        kq["tool"] = pg.url.split("/tool/")[-1].split("?")[0]
        log(f"app dung xong sau {kq['giay_dung_app']}s, tool={kq['tool']}")
        pg.wait_for_timeout(5000)

        # khe uoc giao dien: moi lan dung ra mot app khac nhau -> kiem truoc khi nap
        tx = fl.locator("body").inner_text().upper()
        thieu = [s for s in bo["slots"] if s not in tx] + (["GENERATE"] if "GENERATE" not in tx else [])
        # bien the (b) khong co o ref -> chi doi nut Generate + o dan prompt
        if thieu or not fl.locator("textarea").count():
            nut_co = [fl.locator("button").nth(i).inner_text().strip()
                      for i in range(fl.locator("button").count())]
            raise RuntimeError(f"giao dien thieu thanh phan {thieu} | nut={nut_co}")

        nut_co = [" ".join(fl.locator("button").nth(i).inner_text().split())
                  for i in range(fl.locator("button").count())]
        kq["nut_app"] = nut_co
        thieu_nut = [x for x in ("generate all", "retry", "download") if
                     not any(x in n.lower() for n in nut_co)]
        log(f"  app co {len(nut_co)} nut: {nut_co}")
        if thieu_nut:                                 # khe uoc giao dien doi du 6 nut
            log(f"  ⚠️ THIEU nut theo khe uoc: {thieu_nut} — retry/tai ZIP co the khong bam duoc")
        nap_du_lieu(pg, fl, bo)
        t0 = time.time()
        bam_generate(pg, fl)

        # bam Generate All co lan KHONG AN -> de nguyen thi ngoi het gio khong co anh nao
        pg.wait_for_timeout(30000)
        s0 = doc_so(than(fl), bo["so_dong"])
        if sum(s0.get(k, 0) for k in ("DONE", "RUNNING", "FAILED")) == 0:
            log("  hang doi chua chay sau 30s -> thu va loi roi bam lai")
            if sua_loi_neu_can(pg):
                fl2 = cho_app(pg)
                if not fl2:
                    raise RuntimeError("va loi xong nhung app khong render lai trong 180s")
                fl = fl2
                nap_du_lieu(pg, fl, bo)
            bam_generate(pg, fl)
            pg.wait_for_timeout(30000)
            if sum(doc_so(than(fl), bo["so_dong"]).get(k, 0) for k in ("DONE", "RUNNING", "FAILED")) == 0:
                raise RuntimeError("bam Generate All 2 lan van khong chay — dung lai kiem tra tay")

        cuoi, t_doi = {}, time.time()
        while time.time() - t0 < a.timeout:
            # CHO TRONG TRINH DUYET: xong la bat ra ngay (do that: phat hien trong <1s thay vi <=20s).
            # Cat thanh tung lat 30s de van con nhip kiem DUNG HINH o duoi.
            kt = khung_that(pg)
            try:
                if kt:
                    kt.wait_for_function(JS_XONG, arg=bo["so_dong"], timeout=30000)
                else:
                    pg.wait_for_timeout(5000)
            except Exception:
                pass                                  # het lat 30s ma chua xong -> xuong doc bang dem
            rows = than(fl)
            so = doc_so(rows, bo["so_dong"])
            if so != cuoi:
                log(f"  [{int(time.time()-t0)}s] {so}")
                cuoi, t_doi = so, time.time()
            if so.get("DONE", 0) + so.get("FAILED", 0) >= bo["so_dong"]:
                break
            # KIEU HONG 3: bang dem tu reset ve 0 + ZIP rong, nhung anh VAN con trong RAM
            m = re.search(r"(\d+)\s*images? in memory|in memory[:\s]*(\d+)", "\n".join(rows), re.I)
            if m:
                n_ram = int(next(g for g in m.groups() if g))
                if n_ram >= bo["so_dong"]:
                    log(f"  bang dem bi reset nhung con {n_ram} anh trong RAM -> coi nhu xong")
                    cuoi = {"TOTAL": bo["so_dong"], "DONE": n_ram, "RUNNING": 0, "FAILED": 0}
                    break
            # KIEU HONG 1: dung hinh, dong nam mai o RUNNING
            if time.time() - t_doi > a.dung_hinh:
                log(f"  dung hinh {int(time.time()-t_doi)}s -> kiem thanh loi cua Flow")
                if kq["va_giua_chung"] < 2 and sua_loi_neu_can(pg):
                    kq["va_giua_chung"] += 1
                    fl2 = cho_app(pg)
                    if not fl2:
                        raise RuntimeError("va loi xong nhung app khong render lai trong 180s")
                    fl = fl2
                    nap_du_lieu(pg, fl, bo)       # KIEU HONG 2: va xong app sach tron
                    bam_generate(pg, fl)
                    cuoi, t_doi = {}, time.time()
                else:
                    raise RuntimeError(f"app dung hinh, khong co nut 'Sua loi' de va: {so}")
        kq["giay_chay"] = int(time.time() - t0)
        kq["dem_cuoi"] = cuoi
        log(f"chay xong sau {kq['giay_chay']}s: {cuoi}")
        if cuoi.get("FAILED", 0) > 0:                 # ve lai CHI cac dong hong, truoc khi tai ZIP
            kq["retry_lan"], cuoi = retry_failed(pg, fl, bo["so_dong"])
            kq["dem_sau_retry"] = cuoi
        if cuoi.get("DONE", 0) < bo["so_dong"]:
            raise RuntimeError(f"chua du anh khi het gio: {cuoi} — DUNG reload, anh con trong RAM")

        zp = tai_zip(pg, fl, dich, bo["so_dong"])
        kq["zip"] = str(zp)
        kq["zip_bytes"] = zp.stat().st_size
        log(f"DA TAI ZIP: {zp}")
        print("\nBUOC TIEP THEO (tool nay KHONG tu lam — nghiem thu roi moi giao anh):")
        print(f'  py -3.13 pipeline\\nghiemthu_flow_tool.py "{zp}" --bo3 "{a.bo3}" '
              f'--giao "<thu muc tap>\\img"')
        print("  ⚠️ CHUA nghiem thu xong thi DUNG reload/dong tab Flow — anh con trong RAM.")
        # DONG TAB APP ngay sau khi co ZIP: app tu tai ZIP moi khi re-render, ban thieu chot mot-lan
        # se tai LAP VO HAN chung nao tab con mo (do that 2026-09-24: 5.120 file / 12,4 GB trong 15
        # phut vao thu muc Downloads). Da co ZIP roi thi khong con ly do giu tab.
        try:
            pg.close()
            log("  da dong tab app (chan vong tai ZIP lap)")
        except Exception as e:
            log(f"  khong dong duoc tab app: {str(e)[:70]}")
    finally:
        kq["ket_thuc"] = time.strftime("%Y-%m-%d %H:%M:%S")
        (dich / "ket_qua.json").write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
        try:
            f.shot("chay_flow_tool")
        except Exception:
            pass
        f.stop()                                   # chi ngat playwright, KHONG dong Chrome
    return 0


if __name__ == "__main__":
    sys.exit(main())
