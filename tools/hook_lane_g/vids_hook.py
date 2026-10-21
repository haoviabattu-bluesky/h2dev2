# -*- coding: utf-8 -*-
"""Sinh clip hook bằng GOOGLE VIDS Omni (tài khoản Ultra) — ẢNH hook → video, thay grok_da_luong.py (anh chốt 16/10).

Mỗi ảnh hook (<hook>/img/NNN.png, đã chèn chữ đạo cụ nếu có) được tải lên chế độ "Tạo ảnh động" của Vids: ảnh = KHUNG ĐẦU
clip (đo thật: lệch 1,4 → mặt/áo/nét anime giữ nguyên như REF-LOCK). Prompt = chỉ CHUYỂN ĐỘNG (rút từ prompt Grok trong
grok_jobs.csv). Số giây mỗi clip KHỚP lời đọc của shot (hook_timeline.json, ước bằng voice.char_rate của profile):
giây = ceil(lời + nghỉ + 0,5) kẹp 3–10; shot có thẻ tên ≥ dur_s thẻ (6s); không có timeline → cột duration của csv.
Hậu kỳ: bỏ tiếng (hook chỉ nhạc nền), che sao Gemini góc phải dưới bằng AVATAR KÊNH cắt tròn (<lane>/branding/avatar_raw.png).
QC từng clip: đủ giây, khung đầu khớp ảnh (lệch ≤ 15 như Grok), không bị Omni tự cắt cảnh → hỏng thì sinh lại (--vong).

    py -3.13 -X utf8 E:\\CLAUDE\\YOUTUBE\\h2dev\\tools\\hook_lane_g\\vids_hook.py <thư mục hook TUYỆT ĐỐI> [--tabs 5] [--only clip_01,clip_05] [--ra <thư mục>] [--dry]

Chrome Ultra: E:\\CLAUDE\\YOUTUBE\\TUAN_PROFILE cổng 9350 (mở bằng E:\\CLAUDE\\YOUTUBE\\GROK_VIDEO\\open_tuan_profile.bat). Không kill Chrome.
⛔ (16/10) Các tập KHÔNG chạy profile song song: tool giữ khoá pipeline\\khoa_ultra.py suốt lúc chạy; tập khác đang giữ
(ảnh hook anh_hook.py / clip Vids tập khác) → CHỜ tới lượt (--cho-khoa phút), không mở tab chen vào.
Ra: <ra>/<clip_id>.mp4 (đã che + câm) · bản gốc <ra>/_vids_goc/ · clip hỏng <ra>/_sai/ · nhật ký <ra>/_vids_log.csv
Hướng dẫn: E:\\CLAUDE\\YOUTUBE\\h2dev\\docs\\QUY_TRINH_CLIP_HOOK_GOOGLE_VIDS.md
"""
import argparse, csv, json, math, queue, re, subprocess, sys, threading, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GV = Path(r"E:\CLAUDE\YOUTUBE\GROK_VIDEO\tools\google_vids")
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(GV)); sys.path.insert(0, str(ROOT / "pipeline"))
import grok_1tk_lib as L      # noqa: E402  lech_anh (khung đầu ↔ ảnh gốc)
import vids_omni as vo        # noqa: E402
import vids_nhieu_tab as vn   # noqa: E402
import che_logo               # noqa: E402
import soat_muot              # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
FF = soat_muot.FF

# ---------- giao diện Vids (đo 16/10/2026) ----------
FILE_IN = "input[type=file][accept*='image']"
THUMB = "img.inputPreviewItemPreview"
NUT_CAI_DAT = "button[aria-label^='Cài đặt tạo video']"
# aria-label "Thời lượng video" lưu Unicode dạng tổ hợp → selector theo aria-label KHÔNG khớp; chọn theo class.
SLIDER = "[class*=MenubuttonSlider] input[type=range]"
JS_BTN = """(t) => [...document.querySelectorAll('button,[role=button]')].filter(e => {
  const r = e.getBoundingClientRect(); const s = ((e.innerText || e.getAttribute('aria-label') || '').trim()).normalize('NFC');
  return r.width > 5 && s === t.normalize('NFC'); }).map(e => { const r = e.getBoundingClientRect();
  return {x: r.x, y: r.y, width: r.width, height: r.height}; })"""
JS_XOA_ANH = """() => { const b = [...document.querySelectorAll('button,[role=button]')].filter(e =>
  (e.getAttribute('aria-label') || '').normalize('NFC') === 'Xoá hình ảnh'.normalize('NFC')); b.forEach(e => e.click()); return b.length; }"""


def _nhan(page):
    return page.get_attribute(NUT_CAI_DAT, "aria-label") or ""


JS_DAT_GIAY = """(v) => { const e = document.querySelector('[class*=MenubuttonSlider] input[type=range]');
  Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(e, String(v));
  e.dispatchEvent(new Event('input', {bubbles: true})); e.dispatchEvent(new Event('change', {bubbles: true})); return e.value; }"""


def mo_o_soan(page):
    """Sau mỗi clip / khi popup còn mở, ô soạn THU GỌN: mất nút Cài đặt + ô tải ảnh → Escape rồi bấm vào ô prompt cho mở ra."""
    page.keyboard.press("Escape"); time.sleep(0.5)
    for _ in range(4):
        if page.query_selector(NUT_CAI_DAT):
            return
        o = page.query_selector(vo.PROMPT_BOX)
        if o and o.bounding_box():
            vo._click(page, o)
        time.sleep(1.5)
    raise RuntimeError("không mở được ô soạn (thiếu nút Cài đặt)")


def tab_anh_dong(page):
    mo_o_soan(page)
    for _ in range(3):
        if page.query_selector(FILE_IN) or page.query_selector(THUMB):
            return
        nut = page.evaluate(JS_BTN, "Tạo ảnh động")
        if nut:
            vo._click(page, nut[0]); time.sleep(1.5)
        mo_o_soan(page)
    if not (page.query_selector(FILE_IN) or page.query_selector(THUMB)):
        raise RuntimeError("không vào được chế độ 'Tạo ảnh động'")


def dat_anh(page, img):
    """Xoá ảnh cũ còn sót → tải đúng 1 ảnh → chờ ảnh xem trước hiện."""
    for _ in range(3):
        if not page.query_selector_all(THUMB):
            break
        page.evaluate(JS_XOA_ANH); time.sleep(1)
    if page.query_selector_all(THUMB):
        raise RuntimeError("không xoá được ảnh cũ trong ô Tạo ảnh động")
    page.set_input_files(FILE_IN, str(img))
    for _ in range(30):
        time.sleep(0.5)
        if len(page.query_selector_all(THUMB)) == 1:
            return
    raise RuntimeError("ảnh không lên ô Tạo ảnh động sau 15s")


def chon_giay(page, giay):
    """Thanh 'Thời lượng video' (3–10, bước 1) nằm trong popup Cài đặt; popup đóng là bị gỡ khỏi DOM → mở ra rồi mới đặt.
    Đặt giá trị, đóng popup, ĐỌC LẠI nhãn nút phải ghi '<giay> giây'."""
    for _ in range(3):
        if page.query_selector(SLIDER):
            break
        if page.get_attribute(NUT_CAI_DAT, "aria-expanded") != "true":
            vo._click(page, page.query_selector(vo.PROMPT_BOX)); time.sleep(1)
            vo._click(page, page.query_selector(NUT_CAI_DAT))
        for _ in range(10):
            time.sleep(0.5)
            if page.query_selector(SLIDER):
                break
    if not page.query_selector(SLIDER):
        raise RuntimeError("không mở được popup cài đặt (thanh thời lượng)")
    # Đặt bằng JS (setter gốc + input/change): phím mũi tên KHÔNG ăn ở tab nền khi chạy 5 tab (đo 16/10: 4/5 tab giữ 10s).
    page.evaluate(JS_DAT_GIAY, giay); time.sleep(0.4)
    page.keyboard.press("Escape"); time.sleep(0.8)
    if f", {giay} giây" not in _nhan(page):
        raise RuntimeError(f"đặt {giay}s thất bại: {_nhan(page)}")


RE_TU_CHOI = re.compile(r"vi phạm các điều khoản|violates? (our|the) (terms|policies)", re.I)


class TuChoi(RuntimeError):
    """Vids báo 'Có vẻ như yêu cầu đó vi phạm các điều khoản của chúng tôi' (đo 16/10: 4/18 ảnh ep11 Lane N, cả 3 lần)."""


def _so_tu_choi(page):
    return len(RE_TU_CHOI.findall(page.evaluate("() => document.body.innerText")))


def sinh(page, img, prompt, giay, res, timeout):
    with vo.KHOA_GUI:   # nhập + bấm Tạo lần lượt từng tab (chống cướp focus — bẫy 2 của HUONG_DAN_GOOGLE_VIDS.md)
        page.bring_to_front()
        tab_anh_dong(page)
        cu = set(page.evaluate(vo.JS_SRC))
        tc = _so_tu_choi(page)
        dat_anh(page, img)
        vo.dat_prompt(page, prompt)
        chon_giay(page, giay)
        if res not in _nhan(page):
            raise RuntimeError(f"độ phân giải không phải {res}: {_nhan(page)}")
        if len(page.query_selector_all(THUMB)) != 1 or vo._gon(page.locator(vo.PROMPT_BOX).first.inner_text()) != vo._gon(prompt):
            raise RuntimeError("ảnh/prompt bị đổi ngay trước khi bấm Tạo")
        nut = [b for b in page.evaluate(vo.JS_NUT_GUI) if not b["disabled"]]
        if not nut:
            raise RuntimeError("nút Tạo còn khoá")
        vo._click(page, nut[-1])
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(4)
        moi = set(page.evaluate(vo.JS_SRC)) - cu
        if moi:
            return sorted(moi)[0], round(time.time() - t0)
        if vo.RE_HET_HAN_MUC.search(page.evaluate("() => document.body.innerText")):
            raise vo.HetHanMuc("Vids báo hết hạn mức")
        if _so_tu_choi(page) > tc:
            raise TuChoi("Vids TỪ CHỐI (vi phạm điều khoản)")
    raise TimeoutError(f"quá {timeout}s chưa ra video")


# ---------- prompt: Grok (tả cảnh + chuyển động) → Vids ảnh động (CHỈ chuyển động) ----------
KHOA = r"SUBJECT|LOCATION|ACTION|EMOTION|CAMERA|MOVEMENT|DURATION|CONTINUITY|NEGATIVE|LIGHTING|STYLE|KEEP TEXT"


def lam_prompt(p, gon=False):
    """gon=True (lần sinh lại sau khi Vids TỪ CHỐI): chỉ còn chuyển động, bỏ câu 'giữ nguyên mặt' + cảm xúc."""
    p = " ".join((p or "").split())
    truong = {k: v.strip() for k, v in re.findall(rf"\b({KHOA}):\s*(.*?)(?=\s*\b(?:{KHOA}):|$)", p)}
    if truong.get("ACTION") or truong.get("MOVEMENT"):
        dong = [truong.get(k) for k in ("ACTION", "MOVEMENT", "CAMERA", "EMOTION") if truong.get(k)]
    else:   # prompt văn xuôi (vd Lane F) → bỏ câu DURATION / cấm chữ / giữ nét — phần đầu prompt Vids đã nói
        cau = re.split(r"(?<=[.;])\s+", re.sub(rf"\b({KHOA}):", "", p))
        dong = [c for c in cau if not re.search(r"duration|\bno text|subtitle|keep the .*style|distorted|extra fingers", c, re.I)]
        if truong.get("SUBJECT"):
            dong = [" ".join(truong["SUBJECT"].split()[:45])] + dong
    if gon:
        dong = [truong.get("MOVEMENT") or truong.get("ACTION") or (dong[0] if dong else "")]
    giua = " ".join(d.rstrip(".") + "." for d in dong if d)
    co_chu = "KEEP TEXT" in truong or "KEEP TEXT" in p
    duoi = ("Keep every piece of writing on paper, signs and screens exactly as in the image; do not add, change or blur any text; "
            "camera nearly still. " if co_chu else "No subtitles, no on-screen text. ")
    dau = ("Single continuous shot, no cuts. Animate this image. " if gon else
           "Single continuous shot, no cuts. Animate this exact image as the opening frame; keep the art style, every face, "
           "hair, clothing, props and background exactly as shown, no new people. ")
    return (dau + giua + " " + duoi
            + "Audio: quiet ambient room tone. No dialogue, no music.")


# ---------- số giây khớp lời đọc ----------
def tim_profile(hook):
    for f in sorted((ROOT / "profiles" / "profiles").glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        sd = p.get("slug_dir")
        if sd and str(hook).lower().startswith(str((ROOT / sd).resolve()).lower()):
            return p
    return None


def _dai_mp3(f):
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", soat_muot.chay(["-i", str(f)]))
    return int(m.group(2)) * 60 + float(m.group(3)) if m else None


def _loi_that(tap, voice):
    """Giây lời THẬT của 1 shot từ cache giọng xem thử (<tập>/_xem_thu_giong/cau_NN_<giọng>_<speed>_<md5 câu>.mp3 —
    xem_thu_hook_giong.py đã đọc rồi) + nghỉ 0,5s/câu. Thiếu câu nào → None (dùng ước lượng)."""
    import hashlib
    import cau_vai
    t = 0.0
    for c in cau_vai.tach_cau(voice):
        h = hashlib.md5(c["text"].encode("utf-8")).hexdigest()[:8]
        fs = sorted((tap / "_xem_thu_giong").glob(f"cau_*_{h}.mp3"), key=lambda f: f.stat().st_mtime)
        d = _dai_mp3(fs[-1]) if fs else None
        if d is None:
            return None
        t += d + 0.5
    return t


def tinh_giay(hook, jobs, prof):
    """{clip_id: (giây xin Vids, giây lời, ghi chú)} — clip phải DÀI HƠN lời (dư thì cắt bớt, thiếu thì bị giãn chậm).
    Lời THẬT (cache giọng xem thử) → giây = ceil(lời + 0,5). Chưa có giọng → ước số chữ ÷ char_rate × 60 + 0,5s/câu,
    nhưng ước hụt tới 30% ở câu có số (64歳, 1150円 — đo ep11 Lane N) → giây = ceil(ước × 1,2 + 1).
    Shot có thẻ tên ≥ dur_s thẻ (6s, luật 16). Kẹp 3–10 (giới hạn thanh Vids); lời > 10s → giãn chậm clip 10s."""
    rate = float(((prof or {}).get("voice") or {}).get("char_rate") or 0)
    dur_the = float((((prof or {}).get("script") or {}).get("hook") or {}).get("the_ten", {}).get("dur_s") or 6)
    tl = hook / "hook_timeline.json"
    can = {}
    if tl.exists():
        for s in json.loads(tl.read_text(encoding="utf-8")).get("shots", []):
            cid = Path(s.get("clip", "")).stem
            them = float(s.get("nghi_sau_s") or 0)
            if s.get("lang_s") and not s.get("voice"):
                dai = float(s["lang_s"]); gay, ghi = math.ceil(dai), "shot lặng"
            elif (that := _loi_that(hook.parent, s.get("voice", ""))) is not None:
                dai = that + them; gay, ghi = math.ceil(dai + 0.5), "giọng thật"
            elif rate:
                chu = re.sub(r"[\s「」『』（）()、。！？!?…・]", "", s.get("voice", ""))
                so_cau = max(1, len(re.findall(r"[。！？!?]", s.get("voice", ""))))
                dai = len(chu) / rate * 60 + 0.5 * so_cau + them
                gay, ghi = math.ceil(dai * 1.2 + 1), f"ước {len(chu)} chữ"
            else:
                continue
            if s.get("the_ten"):
                gay, ghi = max(gay, math.ceil(dur_the)), ghi + " · thẻ tên"
            if dai > 10:
                ghi += f" · lời {dai:.1f}s > 10s → giãn chậm clip x{dai / 10:.2f}"
            moi = (min(10, max(3, gay)), round(dai, 1), ghi)
            can[cid] = max(can[cid], moi) if cid in can else moi
    for j in jobs:
        if j["id"] not in can:
            g = int(float(j.get("duration") or 6))
            can[j["id"]] = (min(10, max(3, g)), None, "theo cột duration csv (chưa có hook_timeline.json)")
    return can


# ---------- hậu kỳ + QC ----------
def hau_ky(goc, avatar, dich, duong_kinh=72, vien=2):
    w, _ = che_logo.kich_thuoc(goc)
    s = w / che_logo.GOC_W
    d = round(duong_kinh * s)
    png = dich.parent / "_vids_goc" / f"_avatar_{d}.png"
    if not png.exists():
        che_logo.avatar_tron(avatar, d, png, round(vien * s))
    x, y = round(che_logo.TAM_X * s - d / 2), round(che_logo.TAM_Y * s - d / 2)
    subprocess.run([FF, "-v", "error", "-y", "-i", str(goc), "-i", str(png), "-filter_complex",
                    f"[0:v:0][1:v]overlay={x}:{y}[v]", "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "18",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dich)], check=True)


def qc(goc, img, giay):
    m = soat_muot.do_clip(goc)
    loi = []
    if abs(m["giay"] - giay) > 0.4:
        loi.append(f"dài {m['giay']}s ≠ {giay}s")
    lech = L.lech_anh(img, goc)
    if lech > 15:
        loi.append(f"khung đầu lệch ảnh {lech:.0f} > 15")
    if m["cat_canh_tai"]:
        loi.append(f"Omni tự cắt cảnh tại {m['cat_canh_tai']}s")
    return loi, lech, m


def main():
    ap = argparse.ArgumentParser(description="Clip hook bằng Google Vids (ảnh → video)")
    ap.add_argument("hook")
    ap.add_argument("--tabs", type=int, default=5)
    ap.add_argument("--only", default="", help="clip_01,clip_05 …")
    ap.add_argument("--ra", default="", help="thư mục ra (mặc định <hook>/clip)")
    ap.add_argument("--avatar", default="", help="mặc định <lane>/branding/avatar_raw.png")
    ap.add_argument("--cdp", default="http://127.0.0.1:9350")
    ap.add_argument("--res", default="720p", choices=["720p", "1080p"])
    ap.add_argument("--vong", type=int, default=3, help="số lần sinh tối đa mỗi clip")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--lam-lai", action="store_true", help="sinh cả clip đã có trong <ra>")
    ap.add_argument("--bo-kiem-chu", action="store_true", help="bỏ cổng chữ trên đạo cụ (chỉ khi anh cho phép)")
    ap.add_argument("--dry", action="store_true", help="chỉ in kế hoạch giây + prompt")
    ap.add_argument("--cho-khoa", type=int, default=360, help="phút chờ khi tập khác đang dùng profile Ultra")
    a = ap.parse_args()
    hook = Path(a.hook).resolve()
    ra = Path(a.ra).resolve() if a.ra else hook / "clip"
    (ra / "_vids_goc").mkdir(parents=True, exist_ok=True)
    prof = tim_profile(hook)
    avatar = Path(a.avatar) if a.avatar else (ROOT / prof["slug_dir"] / "branding" / "avatar_raw.png" if prof else None)
    if not avatar or not avatar.exists():
        raise SystemExit(f"✗ không thấy avatar kênh ({avatar}) — truyền --avatar <ảnh avatar kênh>")
    if not a.bo_kiem_chu:
        import chu_dao_cu
        chu_dao_cu.cong(prof or {}, hook.parent, "vids_hook (trước khi sinh clip)", sau_grok=False)

    with (hook / "grok_jobs.csv").open(encoding="utf-8-sig") as f:
        jobs = list(csv.DictReader(f))
    if a.only:
        chon = {x.strip() for x in a.only.split(",")}
        jobs = [j for j in jobs if j["id"] in chon]
    giay = tinh_giay(hook, jobs, prof)
    viec = queue.Queue()
    print(f"Profile: {(prof or {}).get('id', '?')} · char_rate {((prof or {}).get('voice') or {}).get('char_rate')} · avatar {avatar}")
    for j in jobs:
        img = Path(j["image"]) if Path(j["image"]).is_absolute() else hook.parent / j["image"]
        g, dai, ghi = giay[j["id"]]
        pr = lam_prompt(j["prompt"])
        co = (ra / f"{j['id']}.mp4").exists()
        print(f"  {j['id']}: {g}s (lời {dai}s · {ghi}){' · ĐÃ CÓ → bỏ' if co and not a.lam_lai else ''}")
        if a.dry:
            print("     " + pr)
        if not (co and not a.lam_lai):
            viec.put((j["id"], img, j["prompt"], g, 1))
    if a.dry or viec.empty():
        return
    import khoa_ultra
    khoa_profile = khoa_ultra.Khoa("vids_hook", hook.parent, cho_s=a.cho_khoa * 60)
    if not khoa_profile.thu():
        raise SystemExit(f"✗ profile Ultra vẫn bận sau {a.cho_khoa} phút: {khoa_ultra.ai_dang_giu()} — chạy lại sau")
    tong = viec.qsize()
    so_tab = max(1, min(a.tabs, tong))
    print(f"Sinh {tong} clip · {so_tab} tab · {a.res} → {ra}")
    log_f = (ra / "_vids_log.csv").open("a", encoding="utf-8-sig", newline="")
    w = csv.writer(log_f)
    khoa = threading.Lock()
    kq = {}
    bi_tu_choi = set()   # clip bị Vids từ chối → lần sau prompt gọn; vẫn hỏng → Grok (grok_da_luong.py)

    def luong(ten, url_san):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            br = p.chromium.connect_over_cdp(a.cdp)
            tu_tao, page = url_san is None, None
            with vn.KHOA_MO:
                if url_san:
                    page = next((x for x in br.contexts[0].pages if x.url.startswith(url_san)), None)
                    try:
                        page and (page.bring_to_front(), vo.mo_panel_ai(page))
                    except Exception:
                        page = None
                if page is None:
                    tu_tao, page = True, vn._mo_editor_moi(br, ten, a)
            if page is None:
                return
            while not vn.DUNG.is_set():
                try:
                    cid, img, pr_goc, g, lan = viec.get_nowait()
                except queue.Empty:
                    break
                goc = ra / "_vids_goc" / f"{cid}_lan{lan}.mp4"
                pr = lam_prompt(pr_goc, gon=cid in bi_tu_choi)
                trang = ""
                try:
                    src, s = sinh(page, img, pr, g, a.res, a.timeout)
                    vo.tai_clip(page, src, goc)
                    loi, lech, m = qc(goc, img, g)
                    if loi:
                        (ra / "_sai").mkdir(exist_ok=True)
                        goc.replace(ra / "_sai" / goc.name)
                        trang = "SAI: " + "; ".join(loi)
                    else:
                        hau_ky(goc, avatar, ra / f"{cid}.mp4")
                        trang = f"OK {s}s sinh · {m['giay']}s · lệch {lech:.1f}"
                        kq[cid] = True
                except TuChoi as e:
                    trang = f"TỪ CHỐI{' (prompt gọn)' if cid in bi_tu_choi else ''}: {e}"
                    bi_tu_choi.add(cid)
                except vo.HetHanMuc as e:
                    trang = f"HẾT HẠN MỨC: {e}"
                    vn.DUNG.set()
                except Exception as e:  # noqa: BLE001
                    trang = f"LỖI: {str(e).splitlines()[0][:200]}"
                    try:
                        page.screenshot(path=str(ra / "_vids_goc" / f"loi_{cid}_lan{lan}.png"))
                    except Exception:
                        pass
                print(f"[{ten}] {cid} lần {lan} ({g}s): {trang}")
                with khoa:
                    w.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), cid, lan, g, trang, img.name, pr]); log_f.flush()
                if not kq.get(cid) and lan < a.vong and not vn.DUNG.is_set():
                    viec.put((cid, img, pr_goc, g, lan + 1))
            if tu_tao:
                page.close()   # chỉ đóng tab mình tạo, KHÔNG đóng trình duyệt

    t0 = time.time()
    san = vn.editor_dang_mo(a.cdp)
    ds = [threading.Thread(target=luong, args=(f"tab{k + 1}", san[k] if k < len(san) else None)) for k in range(so_tab)]
    for t in ds:
        t.start()
    for t in ds:
        t.join()
    khoa_profile.nha()
    log_f.close()
    hong = [j["id"] for j in jobs if j["id"] not in kq and not ((ra / f"{j['id']}.mp4").exists() and not a.lam_lai)]
    print(f"XONG {len(kq)}/{tong} clip trong {time.time() - t0:.0f}s → {ra}" + (f" · HỎNG: {', '.join(hong)}" if hong else ""))
    if hong:
        print(f"→ clip hỏng chạy dự phòng Grok: py -3.13 -X utf8 {HERE / 'grok_da_luong.py'} {hook}"
              + ("" if ra == hook / "clip" else f"  (Grok ghi vào {hook / 'clip'})"))
    if kq:
        subprocess.run([sys.executable, "-X", "utf8", str(GV / "soat_muot.py"), str(ra)], check=False)
    sys.exit(1 if hong else 0)


if __name__ == "__main__":
    main()
