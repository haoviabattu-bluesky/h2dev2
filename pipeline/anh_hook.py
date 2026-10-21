r"""anh_hook.py — ẢNH HOOK mọi lane: Google Flow (Nano Banana Pro, tài khoản Ultra) → 9router → gpti2 (anh chốt 16/10/2026).

Thứ tự nguồn (thay `gen_images.py` / `_gen_ima2.py` riêng từng tập cho ẢNH HOOK):
  1. GOOGLE FLOW trên Chrome Ultra TUAN_PROFILE (cổng 9350 — cùng tài khoản làm clip Vids). 0 tín dụng/ảnh (đo 16/10).
     Khoá mặt = tải master `_ref_<id>\001.png` lên dự án Flow rồi "Thêm vào câu lệnh" (giữ mặt rất sát, cả cảnh 2 người).
     ⛔ Các tập KHÔNG chạy profile song song: giữ khoá `khoa_ultra` suốt lúc dùng. Khoá bận (tập khác đang dùng
     profile — ảnh hoặc clip Vids) hoặc cổng chết → KHÔNG chờ, đi thẳng 9router.
  2. 9ROUTER (Codex, 0đ, `img_9router.py`) — cho ảnh Google lỗi/bị từ chối, hoặc khi cổng bận.
  3. GPTI2 (`gpti2_edit` có ref / `gpti2_gen`) — khi 9router cũng lỗi. Dòng @GROK (trẻ em) cuối cùng đi Grok thay gpti2.

Cú pháp dòng prompt y hệt gen_images.py: `@CAST:id1,id2 <prompt>` (master `<cast-root>\_ref_<id>\001.png`),
`@REF`/`@REF2`/`@REF12` (dùng --ref/--ref2), `@GROK`, dòng thường. Ra `<out>\NNN.png` (PNG 2560x1440 với ảnh Google),
chạy lại = resume (bỏ ảnh đã có). Nhật ký `<out>\_anh_hook_log.csv`, `<out>\manifest.json` ghi thêm `nguon`.

    py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\anh_hook.py <thư mục hook TUYỆT ĐỐI> [--chi 1,5] [--tabs 2] [--dry]
    (mặc định --prompts <hook>\img_prompts_hook.txt · --out <hook>\img · --cast-root <thư mục tập>)
    --nguon google|9router|gpti2  ép bắt đầu từ 1 nguồn (google ép = CHỜ khoá thay vì sang 9router)
    --lam-lai  vẽ lại cả ảnh đã có (ảnh cũ chuyển sang <out>\_cu_<giờ>\, không xoá)
Hướng dẫn: E:\CLAUDE\YOUTUBE\h2dev\docs\QUY_TRINH_ANH_HOOK_GOOGLE_FLOW.md
"""
import argparse
import csv
import io
import json
import queue
import re
import shutil
import sys
import threading
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_images   # noqa: E402  parse_prompts (cùng cú pháp marker)
import khoa_ultra   # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
_in = threading.Lock()


def log(*a):
    with _in:
        print(*a, flush=True)


def _nfc(s):
    return unicodedata.normalize("NFC", s or "")


def _gon(s):
    return " ".join(_nfc(s).split())


# ======================================================================= GOOGLE FLOW (giao diện đo thật 16/10/2026)
FLOW = "https://flow.google.com/"
UUIDS = r"""() => [...new Set([...document.querySelectorAll('img')].map(i =>
  (i.src.match(/flow-content\.google\/image\/([0-9a-f-]{36})/) || [])[1]).filter(Boolean))]"""
OPTS = r"() => [...document.querySelectorAll('[role=option]')].map(e => e.innerText.trim().replace(/\s+/g, ' '))"
# chữ tiếng Việt trong DOM Flow có chỗ lưu dạng tổ hợp (NFD) → mọi so khớp chữ đều normalize NFC trong JS
JS_BAM = r"""([t, kieu]) => { const n = s => (s || '').replace(/\s+/g, ' ').trim().normalize('NFC'); const t2 = n(t);
  const sel = kieu === 'radio' ? '[role=radio]' : 'button,[role=button],[role=menuitem],[role=radio]';
  const b = [...document.querySelectorAll(sel)].filter(e => {
    const r = e.getBoundingClientRect(); const s = n(e.innerText || e.getAttribute('aria-label'));
    return r.width > 0 && (kieu === 'het' ? s.endsWith(t2) : kieu === 'dau' ? s.startsWith(t2) : s === t2); });
  if (!b.length) return false; b[b.length - 1].click(); return true; }"""
JS_ANH_O_SOAN = r"""() => { const t = document.querySelector('[role=textbox]'); if (!t) return -1; let c = t;
  for (let i = 0; i < 4 && c.parentElement; i++) c = c.parentElement; return c.querySelectorAll('img').length; }"""
JS_NUT_TILE = r"""(u) => { const i = [...document.querySelectorAll('img')].find(x => x.src.includes(u)); if (!i) return false;
  const t = i.closest('flow-image-tile') || i.parentElement; i.scrollIntoView({block: 'center'});
  const b = [...t.querySelectorAll('button')].find(e => (e.getAttribute('aria-label') || e.innerText || '').normalize('NFC')
    .match(/Tuỳ chọn khác|Tùy chọn khác|more_vert|More options/)); if (!b) return false; b.click(); return true; }"""
RE_LOI = re.compile(r"không thể tạo|không tạo được|thất bại|vi phạm|chính sách|đã xảy ra lỗi|failed|unable to generate|"
                    r"violat|policy|something went wrong|thử lại sau|too fast|quá nhanh", re.I)
KHOA_GUI = threading.Lock()     # chuẩn bị + bấm Tạo lần lượt từng tab (chống cướp focus, giãn nhịp gửi)


class FlowLoi(RuntimeError):
    pass


def _cho_het_lop_phu(pg, n=15):
    for _ in range(n):
        if pg.locator(".cdk-overlay-backdrop").count() == 0:
            return True
        pg.keyboard.press("Escape"); time.sleep(0.3)
    return pg.locator(".cdk-overlay-backdrop").count() == 0


def _bam(pg, chu, kieu="bang"):
    return pg.evaluate(JS_BAM, [chu, kieu])


class FlowTab:
    """1 tab = 1 dự án Flow MỚI (mỗi tab tải ref riêng → ảnh mới của tab không lẫn tab khác)."""

    def __init__(self, br, ten, orient, ref_dir):
        self.br, self.ten, self.orient, self.ref_dir = br, ten, orient, ref_dir
        self.pg, self.da_tai = None, set()

    def mo(self):
        pg = self.br.contexts[0].new_page()
        try:
            with KHOA_GUI:   # tab nền không vẽ ô soạn → mở dự án lúc tab đang ở trước
                pg.bring_to_front()
                pg.goto(FLOW, wait_until="domcontentloaded", timeout=120000)
                for _ in range(30):
                    time.sleep(1)
                    if _bam(pg, "Dự án mới", "het"):
                        break
                else:
                    raise FlowLoi("không thấy nút 'Dự án mới'")
                for _ in range(45):
                    time.sleep(1)
                    # pg.url là bản ĐỆM chỉ cập nhật khi có lệnh gọi trình duyệt → đọc thẳng location.href
                    if "/project/" in pg.evaluate("location.href") and pg.query_selector("[role=textbox]"):
                        break
                else:
                    raise FlowLoi(f"không vào được dự án mới ({pg.url}, ô soạn {bool(pg.query_selector('[role=textbox]'))})")
                time.sleep(2)
                self.pg = pg
                self.cai_dat()
        except Exception:
            self.pg = None
            try:
                pg.close()   # tab mình vừa mở — không để sót
            except Exception:
                pass
            raise
        log(f"  [{self.ten}] Flow dự án {pg.url.rsplit('/', 1)[-1][:8]}… · Nano Banana Pro · x1 · {self.orient}")

    def cai_dat(self):
        """Hình ảnh · 16:9 (hoặc 9:16) · Nano Banana Pro · x1 — model TỰ TRÔI về mặc định mỗi dự án mới (skill veo3 §11.1b)."""
        pg, ti = self.pg, ("crop_16_9 16:9" if self.orient == "landscape" else "crop_9_16 9:16")
        for _ in range(3):
            _cho_het_lop_phu(pg)
            nut = pg.locator("button", has_text="Nano Banana").first
            nut.click(); time.sleep(1.2)
            _bam(pg, "image Hình ảnh", "radio"); time.sleep(0.5)
            _bam(pg, ti, "radio"); time.sleep(0.5)
            if "Nano Banana Pro" not in (pg.locator("button", has_text="arrow_drop_down").first.inner_text() or ""):
                pg.locator("button", has_text="arrow_drop_down").first.click(); time.sleep(1)
                pg.locator("[role=menuitem]", has_text="Nano Banana Pro").first.click(); time.sleep(1)
            _bam(pg, "x1", "radio"); time.sleep(0.5)
            pg.keyboard.press("Escape"); time.sleep(0.8)
            nhan = pg.locator("button", has_text="Nano Banana").first.inner_text()
            if "Nano Banana Pro" in nhan and "x1" in nhan and ti.split()[0] in nhan:
                break
        else:
            raise FlowLoi(f"không đặt được Nano Banana Pro/x1/{ti}: {nhan!r}")
        tac_nhan = pg.locator("button.agent-mode-chip")
        if tac_nhan.count() and tac_nhan.first.get_attribute("aria-pressed") == "true":
            tac_nhan.first.click(); time.sleep(0.8)   # chế độ Tác nhân gộp prompt, sinh ảnh thừa (skill veo3 §11.3e)

    def _mo_bo_chon(self):
        pg = self.pg
        _cho_het_lop_phu(pg)
        pg.locator("button", has_text=re.compile(r"^\s*add\s*$")).last.click(); time.sleep(1.5)
        if not pg.locator(".cdk-overlay-pane input").count():
            raise FlowLoi("không mở được bảng chọn thành phần (+)")

    def them_ref(self, rid, path, thu_tu):
        """Ảnh master → ô soạn. Lần đầu trong dự án: tải lên với tên ref_<id>.png; lần sau: tìm theo tên trong bảng chọn."""
        pg, ten = self.pg, f"ref_{rid}.png"
        f = self.ref_dir / ten
        if not f.exists() or f.stat().st_size != Path(path).stat().st_size:
            shutil.copyfile(path, f)
        self._mo_bo_chon()
        if rid not in self.da_tai:
            with pg.expect_file_chooser(timeout=15000) as fc:
                pg.locator(".cdk-overlay-pane button", has_text=re.compile(r"^\s*upload")).first.click()
            fc.value.set_files(str(f))
        tim = pg.locator(".cdk-overlay-pane input").first
        tim.fill(f"ref_{rid}"); time.sleep(1.5)
        for _ in range(60):
            o = [x for x in pg.evaluate(OPTS) if ten in x]
            if o and not any("Đang" in _nfc(x) for x in o):
                break
            time.sleep(1)
        else:
            raise FlowLoi(f"{ten} không lên bảng chọn sau 60s")
        self.da_tai.add(rid)
        pg.locator("[role=option]", has_text=ten).first.click(); time.sleep(1.2)
        if pg.locator(".cdk-overlay-backdrop").count():
            _bam(pg, "Thêm vào câu lệnh", "het"); time.sleep(1.2)
        _cho_het_lop_phu(pg)
        for _ in range(40):   # ảnh vừa tải lên còn xử lý → ô soạn hiện biểu tượng chờ, chưa có <img> (đo 16/10)
            if pg.evaluate(JS_ANH_O_SOAN) == thu_tu:
                return
            time.sleep(1)
        if pg.evaluate(JS_ANH_O_SOAN) != thu_tu:
            raise FlowLoi(f"ô soạn có {pg.evaluate(JS_ANH_O_SOAN)} ảnh, cần {thu_tu} sau khi thêm {ten}")

    def sinh(self, prompt, refs, timeout):
        """refs = [(id, path)] → bytes PNG. Lỗi/từ chối/quá giờ → FlowLoi (ảnh đó sang 9router)."""
        pg = self.pg
        with KHOA_GUI:
            pg.bring_to_front()
            _cho_het_lop_phu(pg)
            if pg.evaluate(JS_ANH_O_SOAN) != 0:
                raise FlowLoi("ô soạn còn ảnh cũ")
            for k, (rid, path) in enumerate(refs, 1):
                self.them_ref(rid, path, k)
            if refs:
                prompt = ("Attached reference images, in order: " + ", ".join(f"{k} = {rid}" for k, (rid, _) in enumerate(refs, 1))
                          + ". Use them ONLY to lock each person's face, hairstyle and age (clothing and scene come from the "
                            "text below). Draw a NEW scene: " + prompt)
            o = pg.locator("[role=textbox]").first
            o.click(); o.fill(prompt); time.sleep(0.8)
            if _gon(o.inner_text()) != _gon(prompt):
                raise FlowLoi("prompt trong ô soạn không khớp (bị cắt/nối)")
            if pg.evaluate(JS_ANH_O_SOAN) != len(refs):
                raise FlowLoi("số ảnh ref trong ô soạn bị đổi trước khi bấm Tạo")
            cu = set(pg.evaluate(UUIDS))
            chu_cu = set(pg.evaluate("() => document.body.innerText").splitlines())
            pg.locator("button", has_text="arrow_forward").first.click()
            time.sleep(4)   # giãn nhịp gửi giữa các tab ("You are asking too fast")
        t0 = time.time()
        while time.time() - t0 < timeout:
            moi = set(pg.evaluate(UUIDS)) - cu
            if moi:
                return self.tai(sorted(moi)[0])
            dong_moi = [d for d in pg.evaluate("() => document.body.innerText").splitlines() if d not in chu_cu]
            loi = [d for d in dong_moi if RE_LOI.search(d) and len(d) < 300]
            if loi:
                raise FlowLoi(f"Flow báo: {loi[0][:150]}")
            time.sleep(3)
        raise FlowLoi(f"quá {timeout}s chưa ra ảnh")

    def tai(self, uuid):
        """Ưu tiên bản 2K (Flow tự tăng độ phân giải, ~15s); hỏng thì lấy bản gốc 1376x768 từ src."""
        pg = self.pg
        time.sleep(2)
        try:
            with KHOA_GUI:
                pg.bring_to_front()   # tab nền tải 2K ra file 0 byte (đo 16/10, 2/2 lần ở tab không đứng trước)
                _cho_het_lop_phu(pg)
                if not pg.evaluate(JS_NUT_TILE, uuid):
                    raise FlowLoi("không thấy nút menu của ảnh")
                time.sleep(1)
                pg.locator("[role=menuitem]", has_text="download").first.hover(); time.sleep(1)
                with pg.expect_download(timeout=120000) as d:
                    pg.locator("[role=menuitem]", has_text="2K").first.click()
            tam = self.ref_dir / f"_tai_{uuid[:8]}.jpg"   # CDP: file tải nằm ở trình duyệt → save_as, không dùng path()
            d.value.save_as(str(tam))
            b = tam.read_bytes()
            try:
                png = chuan_hoa(b, self.orient)
            except Exception:
                tam.replace(self.ref_dir / f"_hong_{uuid[:8]}.bin")   # giữ lại để soi
                raise FlowLoi(f"file 2K không phải ảnh ({len(b)} byte, {d.value.suggested_filename})")
            tam.unlink(missing_ok=True)
            return png
        except Exception as e:  # noqa: BLE001
            log(f"  [{self.ten}] tải 2K hỏng ({str(e).splitlines()[0][:120]}) → lấy bản gốc")
            _cho_het_lop_phu(pg)
            src = next(s for s in pg.evaluate("() => [...document.querySelectorAll('img')].map(i => i.src)") if uuid in s)
            return chuan_hoa(pg.request.get(src).body(), self.orient)


def chuan_hoa(b, orient):
    """JPEG Flow (2752x1536 ≈ 16:9) → cắt giữa đúng 16:9 → PNG 2560x1440 (cỡ chuẩn ảnh hook gpti2 cũ)."""
    from PIL import Image
    im = Image.open(io.BytesIO(b)).convert("RGB")
    W, H = (2560, 1440) if orient == "landscape" else (1440, 2560)
    w, h = im.size
    if w / h > W / H:
        nw = round(h * W / H); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = round(w * H / W); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    out = io.BytesIO()
    im.resize((W, H), Image.LANCZOS).save(out, "PNG")
    return out.getvalue()


def chay_google(viec, a, out, ghi):
    """Chạy hết `viec` trên Flow; trả list việc HỎNG (để sang 9router)."""
    from playwright.sync_api import sync_playwright
    q = queue.Queue()
    for v in viec:
        q.put(v)
    hong, ref_dir = [], out / "_flow_ref"
    ref_dir.mkdir(exist_ok=True)

    def luong(ten):
        with sync_playwright() as p:
            br = p.chromium.connect_over_cdp(a.cdp)
            tab = None
            while True:
                try:
                    v = q.get_nowait()
                except queue.Empty:
                    break
                t = time.time()
                try:
                    if tab is None:
                        tab = FlowTab(br, ten, a.orient, ref_dir); tab.mo()
                    png = tab.sinh(v["prompt"], v["refs"], a.timeout)
                    ghi(v, png, "google", f"{time.time() - t:.0f}s")
                except Exception as e:  # noqa: BLE001
                    ly_do = str(e).splitlines()[0][:200] if str(e) else type(e).__name__
                    log(f"  [{ten}] ✗ {v['name']} Google: {ly_do} → để 9router")
                    hong.append(v)
                    if tab and tab.pg:   # trạng thái ô soạn không rõ → bỏ tab, việc sau mở dự án mới
                        try:
                            tab.pg.screenshot(path=str(out / f"_flow_loi_{Path(v['name']).stem}.png"))
                            tab.pg.close()
                        except Exception:
                            pass
                    tab = None
            if tab and tab.pg:
                tab.pg.close()   # chỉ đóng tab mình mở, KHÔNG đóng trình duyệt

    so_tab = max(1, min(a.tabs, len(viec)))
    ds = [threading.Thread(target=luong, args=(f"tab{k + 1}",)) for k in range(so_tab)]
    for k, th in enumerate(ds):
        th.start(); time.sleep(3 if k < so_tab - 1 else 0)
    for th in ds:
        th.join()
    return hong


# ======================================================================= 9ROUTER / GPTI2
def chay_9router(viec, a, ghi):
    import img_9router

    def lam(v):
        for lan in range(1, 3):
            t = time.time()
            try:
                b = img_9router.generate(v["prompt"], [p for _, p in v["refs"]], a.orient, a.quality)
                ghi(v, b, "9router", f"{time.time() - t:.0f}s")
                return None
            except Exception as e:  # noqa: BLE001
                log(f"  ! {v['name']} 9router lần {lan}: {str(e)[:160]}")
                time.sleep(20 if "reset after" in str(e) else 5)
        return v

    with ThreadPoolExecutor(a.workers) as ex:
        return [v for v in ex.map(lam, viec) if v]


def chay_gpti2(viec, a, ghi):
    import gpti2_edit
    import gpti2_gen
    import grok_gen

    def lam(v):
        t = time.time()
        try:
            if v["tag"] == "grok":   # trẻ em: gpti2 chặn mọi minor → Grok như gen_images.py
                b, nguon = grok_gen.generate(v["prompt"], orientation=a.orient), "grok"
            elif v["refs"]:
                b, nguon = gpti2_edit.edit(v["prompt"], [(Path(p).read_bytes(), Path(p).name) for _, p in v["refs"]],
                                           orientation=a.orient, quality=a.quality), "gpti2"
            else:
                b, nguon = gpti2_gen.generate(v["prompt"], orientation=a.orient, quality=a.quality), "gpti2"
            ghi(v, b, nguon, f"{time.time() - t:.0f}s")
            return None
        except Exception as e:  # noqa: BLE001
            log(f"  ✗ {v['name']} gpti2: {str(e)[:200]}")
            return v

    with ThreadPoolExecutor(a.workers) as ex:
        return [v for v in ex.map(lam, viec) if v]


# ======================================================================= main
def lap_viec(a, out):
    """→ list việc {i, name, tag, prompt, refs:[(id, path)]} cho các ảnh còn thiếu (đúng route của gen_images.py)."""
    dong = gen_images.parse_prompts(a.prompts)
    chi = {int(x) for x in a.chi.split(",") if x.strip()}
    ref1 = [(f"nv1_{k}" if k else "nv1", r) for k, r in enumerate(a.ref)]
    ref2 = [(f"nv2_{k}" if k else "nv2", r) for k, r in enumerate(a.ref2)]
    co_dau = any(t in ("ref", "ref2", "ref12") for t, _ in dong)
    viec, thieu = [], []
    for i, (tag, p) in enumerate(dong, 1):
        name = f"{i:03d}.png"
        if (chi and i not in chi) or ((out / name).exists() and not a.lam_lai):
            continue
        if tag.startswith("cast:"):
            refs = [(x, Path(a.cast_root) / f"_ref_{x}" / "001.png") for x in tag[5:].split(",")]
        elif tag == "ref12":
            refs = ref1 + ref2
        elif tag == "ref2":
            refs = ref2
        elif tag == "ref" or (ref1 and not co_dau and tag == "plain"):
            refs = ref1
        else:
            refs = []
        mat = [str(r) for _, r in refs if not Path(r).exists()]
        if mat:
            thieu.append(f"{name}: thiếu master {mat}")
            continue
        viec.append({"i": i, "name": name, "tag": tag, "prompt": p, "refs": [(x, Path(r)) for x, r in refs]})
    return viec, thieu


def main():
    ap = argparse.ArgumentParser(description="Ảnh hook: Google Flow (Ultra) → 9router → gpti2")
    ap.add_argument("hook", help="thư mục hook TUYỆT ĐỐI (<tập>\\hook)")
    ap.add_argument("--prompts", default="", help="mặc định <hook>\\img_prompts_hook.txt")
    ap.add_argument("--out", default="", help="mặc định <hook>\\img")
    ap.add_argument("--cast-root", default="", help="mặc định thư mục tập (cha của hook)")
    ap.add_argument("--ref", action="append", default=[], help="master nhân vật 1 cho dòng @REF (như gen_images.py)")
    ap.add_argument("--ref2", action="append", default=[], help="master nhân vật 2 cho dòng @REF2")
    ap.add_argument("--chi", default="", help="chỉ vẽ các số này, vd 1,5,7")
    ap.add_argument("--nguon", default="auto", choices=["auto", "google", "9router", "gpti2"])
    ap.add_argument("--tabs", type=int, default=2, help="số tab Flow (mỗi tab 1 dự án riêng) — trong CÙNG 1 tập")
    ap.add_argument("--workers", type=int, default=4, help="số luồng 9router/gpti2")
    ap.add_argument("--orient", default="landscape", choices=["landscape", "portrait"])
    ap.add_argument("--quality", default="low", choices=["low", "medium", "high"], help="9router/gpti2")
    ap.add_argument("--timeout", type=int, default=240, help="giây chờ 1 ảnh Flow")
    ap.add_argument("--cdp", default=khoa_ultra.CDP)
    ap.add_argument("--lam-lai", action="store_true")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    hook = Path(a.hook).resolve()
    a.prompts = a.prompts or str(hook / "img_prompts_hook.txt")
    a.cast_root = a.cast_root or str(hook.parent)
    out = Path(a.out).resolve() if a.out else hook / "img"
    if not Path(a.prompts).exists():
        raise SystemExit(f"✗ thiếu {a.prompts}")
    out.mkdir(parents=True, exist_ok=True)

    viec, thieu = lap_viec(a, out)
    for t in thieu:
        log(f"  ✗ {t}")
    log(f"Ảnh hook {hook.parent.name}: cần vẽ {len(viec)} · nguồn {a.nguon} · ra {out}")
    for v in viec:
        log(f"  {v['name']} [{v['tag']}] ref: {', '.join(x for x, _ in v['refs']) or '-'}")
    if a.dry or not viec:
        return
    if a.lam_lai:
        cu = [out / v["name"] for v in viec if (out / v["name"]).exists()]
        if cu:
            bak = out / f"_cu_{time.strftime('%Y%m%d-%H%M%S')}"
            bak.mkdir()
            for f in cu:
                f.replace(bak / f.name)
            log(f"  ảnh cũ ({len(cu)}) chuyển sang {bak}")

    mf = out / "manifest.json"
    done = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {}
    log_f = (out / "_anh_hook_log.csv").open("a", encoding="utf-8-sig", newline="")
    w = csv.writer(log_f)
    dem = {}

    def ghi(v, b, nguon, ghi_chu=""):
        (out / v["name"]).write_bytes(b)
        with _in:
            done[v["name"]] = {"idx": v["i"], "prompt": v["prompt"], "nguon": nguon}
            mf.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")
            w.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), v["name"], nguon, ghi_chu, len(v["refs"])]); log_f.flush()
            dem[nguon] = dem.get(nguon, 0) + 1
            print(f"  ✓ {v['name']} ← {nguon} ({len(b) // 1024}KB, {ghi_chu}, ref {len(v['refs'])}) "
                  f"[{sum(dem.values())}/{len(viec)}]", flush=True)

    t0 = time.time()
    con = viec
    if a.nguon in ("auto", "google"):
        if not khoa_ultra.mo_neu_chet(a.cdp):
            log(f"  ⚠ cổng {a.cdp} không sống → bỏ Google, sang 9router")
        else:
            k = khoa_ultra.Khoa("anh_hook", hook.parent, cho_s=(6 * 3600 if a.nguon == "google" else 0))
            if k.thu():
                try:
                    con = chay_google(con, a, out, ghi)
                finally:
                    k.nha()
            else:
                g = khoa_ultra.ai_dang_giu()
                log(f"  ⚠ CỔNG BẬN: profile Ultra đang được {g.get('tool', '?')} · {g.get('tap', '?')} dùng → sang 9router")
    if con and a.nguon != "gpti2":
        log(f"→ 9router: {len(con)} ảnh")
        con = chay_9router(con, a, ghi)
    if con:
        log(f"→ gpti2: {len(con)} ảnh (9router lỗi)")
        con = chay_gpti2(con, a, ghi)
    log_f.close()
    log(f"\nXONG {sum(dem.values())}/{len(viec)} ảnh trong {time.time() - t0:.0f}s · "
        + " · ".join(f"{k} {n}" for k, n in dem.items())
        + (f" · HỎNG: {', '.join(v['name'] for v in con)} — chạy lại lệnh cũ để thử tiếp" if con else ""))
    sys.exit(1 if con or thieu else 0)


if __name__ == "__main__":
    main()
