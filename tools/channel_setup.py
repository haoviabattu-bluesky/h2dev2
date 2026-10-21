# -*- coding: utf-8 -*-
r"""
QUY TRINH TAO KENH + UP AVATAR hang loat tu sheet GMAIL.

Cach chay:  py -3.13 tools\channel_setup.py 3        (1 dong)
            py -3.13 tools\channel_setup.py 3-5      (dai dong, chay TUAN TU tung dong)

Moi dong:
  1. Doc mail cot B cua dong trong sheet GMAIL
  2. Tim profile GPM co name == mail (quet TOAN BO trang — GPM khong filter theo name)
  3. Start profile -> lay websocket_debugging_url (port doi moi lan start, KHONG hardcode)
  4. Playwright CDP: youtube.com/create_channel -> giu ten mac dinh -> Create channel
     (neu tai khoan da co kenh thi bo qua buoc tao, van lam avatar)
  5. gpti2 sinh avatar dong vat hoat hinh ngau nhien (1024x1024, medium) -> re-save Pillow (xoa C2PA)
  6. Studio /editing/profile: dong dialog warm-welcome + tooltip Ask Studio,
     Upload vao khoi Picture (KHONG nham khoi Banner), Done, Publish (verify aria-disabled)
  7. Ghi sheet: cot 'TEN KENH' = @handle, cot 'NGAY TAO KENH' = dd/mm/yyyy — tra cot THEO HEADER dong 1
     (col()), KHONG hardcode chu cai (sheet da chen cot PHONEVER lam F->G)
  8. Stop profile GPM
"""
import sys, os, io, json, base64, random, re, time
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")
import requests
import pyotp
from PIL import Image
from playwright.sync_api import sync_playwright
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ---------------- config ----------------
GPM = "http://127.0.0.1:9495/api/v1"
GPM_BANNER = "GPMLogin Global API"
SHEET_ID = "1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU"
TAB = "GMAIL"
CREDS = r"D:\CLAUDE\credentials\google-sheets-key.json"
GPTI2_KEY = "sk-YGVr-OzozR6zawnFNDG5DCn_PDiAbNZkj9LVOHaOFcA"
GPTI2 = "https://gpti2.store"
AVATAR_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "avatars")

ANIMALS = ["orange tabby cat", "shiba inu dog", "corgi puppy", "red fox", "panda",
           "grey kitten", "golden retriever puppy", "raccoon", "koala", "bunny rabbit"]
BGS = ["pastel teal", "soft peach", "light lavender", "mint green", "warm cream", "sky blue"]


def sheets_svc():
    creds = Credentials.from_service_account_file(CREDS, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    return build("sheets", "v4", credentials=creds)


def _col_letter(idx0):
    s, n = "", idx0 + 1
    while n:
        n, r = divmod(n - 1, 26); s = chr(65 + r) + s
    return s


def header_cols(svc, tab=TAB):
    """Doc header DONG 1 cua tab -> {TEN_COT_UPPER: 'G'}. BAT BUOC dung cai nay thay vi hardcode
    chu cai cot: sheet da chen them cot PHONEVER (2026-09) lam TEN KENH doi F->G, tool ghi nham F 2 lan
    (Lane E 16/09, Lane F 20/09) — memory gmail-sheet-van-hanh."""
    v = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"{tab}!1:1").execute()
    hdr = (v.get("values") or [[]])[0]
    return {h.strip().upper(): _col_letter(i) for i, h in enumerate(hdr) if h.strip()}


def col(svc, name, tab=TAB):
    """Chu cai cot theo ten header (khong phan biet hoa/thuong). Khong co -> KeyError, KHONG doan."""
    cols = header_cols(svc, tab)
    key = name.strip().upper()
    if key not in cols:
        raise KeyError(f"tab {tab} khong co cot '{name}' — header hien tai: {list(cols)}")
    return cols[key]


def get_row_mail(svc, row):
    """Tra (mail, creds, existing_f). creds = (mail, pass, 2fa_secret) tu cot C 'mail|pass|2fa'.
    existing_f = gia tri cot TEN KENH (tra theo header, ten bien giu de khong pha cho goi)."""
    v = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"{TAB}!B{row}:C{row}").execute()
    vals = (v.get("values") or [[]])[0]
    mail = vals[0].strip() if vals else ""
    raw_c = vals[1].strip() if len(vals) >= 2 else ""
    ck = col(svc, "TÊN KÊNH")
    v2 = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"{TAB}!{ck}{row}").execute()
    existing_f = ((v2.get("values") or [[""]])[0] or [""])[0].strip()
    creds = None
    if raw_c.count("|") >= 2:
        m, pw, secret = raw_c.split("|", 2)
        creds = (m.strip(), pw.strip(), secret.replace(" ", "").strip().upper())
    return mail, creds, existing_f


def totp_fresh(secret, avoid=None, max_wait=45):
    code = pyotp.TOTP(secret).now()
    if avoid is None or code != avoid:
        return code
    end = time.time() + max_wait
    while time.time() < end:
        time.sleep(2)
        code = pyotp.TOTP(secret).now()
        if code != avoid:
            return code
    return code


def is_logged_in(page):
    """Vao myaccount: tru lai duoc (khong bi day ve signin/challenge) = da login."""
    page.goto("https://myaccount.google.com/?hl=en", wait_until="domcontentloaded", timeout=60000)
    end = time.time() + 14
    while time.time() < end:
        url = page.url or ""
        if "myaccount.google.com" in url and all(
                x not in url for x in ("signin", "ServiceLogin", "challenge", "accounts.google.com")):
            return True
        if any(x in url for x in ("signin", "ServiceLogin", "identifier", "accounts.google.com")):
            return False
        time.sleep(1)
    return "myaccount.google.com" in (page.url or "")


def gmail_login(page, mail, password, secret):
    """Login Google theo flow D:\\CLAUDE\\MAIL\\GMAIL (email -> pass -> TOTP). Tra True/False.

    Ho tro CA 2 man hinh vao: o email #identifierId HOAC "Chon tai khoan" (accountchooser,
    profile tung login roi bi dang xuat) -> click vao chinh mail do de tiep tuc.
    """
    page.goto("https://accounts.google.com/", wait_until="domcontentloaded", timeout=60000)

    def _identifier_visible():
        # BAY: sau accountchooser Google van de #identifierId dang <input type=hidden>
        # (da dinh that dong 7-10) -> PHAI check visible, khong duoc chi dem count()
        try:
            el = page.locator("#identifierId")
            return el.count() > 0 and el.first.is_visible()
        except Exception:
            return False

    mode = None
    deadline = time.time() + 25
    while time.time() < deadline and mode is None:
        if _identifier_visible():
            mode = "identifier"
        elif "accountchooser" in (page.url or "") and page.get_by_text(mail, exact=True).count():
            mode = "chooser"
        else:
            page.wait_for_timeout(1500)
    if mode is None:
        return is_logged_in(page)  # khong co form nao -> co the da login san
    if mode == "chooser":
        print(f"    man 'Chon tai khoan' -> click {mail}")
        page.get_by_text(mail, exact=True).first.click()
        page.wait_for_timeout(3000)
        # sau khi chon co the van bi hoi lai email (hiem) -> roi vao nhanh identifier ben duoi
        if _identifier_visible():
            mode = "identifier"
    if mode == "identifier":
        page.fill("#identifierId", mail)
        page.keyboard.press("Enter")
    try:
        page.wait_for_selector('input[name="Passwd"]', timeout=25000)
    except Exception:
        if "challenge/recaptcha" in page.url:
            print("    LOGIN FAIL: dinh recaptcha"); return False
        print(f"    LOGIN FAIL: khong toi trang password ({page.url})"); return False
    page.wait_for_timeout(1500)
    page.fill('input[name="Passwd"]', password)
    page.keyboard.press("Enter")
    try:
        page.wait_for_selector("#totpPin", timeout=25000)
    except Exception:
        # co the khong doi TOTP ma vao thang, hoac password sai
        page.wait_for_timeout(3000)
        u = page.url
        if "myaccount.google.com" in u or ("signin" not in u and "challenge" not in u):
            return True
        print(f"    LOGIN FAIL: password bi tu choi / ket challenge ({u})"); return False
    last = None
    for _ in range(3):
        code = totp_fresh(secret, avoid=last)
        last = code
        try:
            page.fill("#totpPin", code)
            page.keyboard.press("Enter")
        except Exception:
            pass
        t = time.time() + 10
        while time.time() < t:
            u = page.url
            if "myaccount.google.com" in u or ("/signin/" not in u and "challenge" not in u):
                return True
            time.sleep(1)
    print(f"    LOGIN FAIL: TOTP bi tu choi 3 lan ({page.url})")
    return False


VIOLATION_TEXTS = [
    "đã bị gỡ bỏ khỏi YouTube",      # "da bi go bo khoi YouTube"
    "không được khôi phục",           # "khong duoc khoi phuc"
    "removed from YouTube",
    "will not be reinstated",
]


def is_violated(page):
    """Kenh bi go vi vi pham: URL channel-appeal HOAC trang bao 'da bi go bo khoi YouTube'."""
    if "channel-appeal" in (page.url or ""):
        return True
    try:
        body = page.locator("body").inner_text()
        return any(t in body for t in VIOLATION_TEXTS)
    except Exception:
        return False


def mark_violated(svc, row):
    print("    KENH VI PHAM -> ghi cot A 'Da co kenh vi pham'")
    svc.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range=f"{TAB}!A{row}",
        valueInputOption="USER_ENTERED",
        body={"values": [["Đã có kênh vi phạm"]]}).execute()


def find_gpm_profile(mail):
    """GPM /profiles KHONG loc duoc theo name -> quet het cac trang roi tu doi chieu."""
    page = 1
    while True:
        j = requests.get(f"{GPM}/profiles", params={"page": page, "per_page": 100}, timeout=30).json()
        d = j["data"]
        for p in d["data"]:
            if p["name"].lower() == mail.lower():
                return p["id"]
        if page >= d["last_page"]:
            return None
        page += 1


def gpm_start(pid):
    j = requests.get(f"{GPM}/profiles/start/{pid}", timeout=120).json()
    data = j.get("data")
    if not j.get("success") or data == GPM_BANNER or not isinstance(data, dict):
        raise RuntimeError(f"GPM start fail: {j.get('message') or data}")
    return data["websocket_debugging_url"]


def gpm_stop(pid):
    try:
        requests.get(f"{GPM}/profiles/stop/{pid}", timeout=60)
    except Exception:
        pass


def gen_avatar(row, mail):
    animal = random.choice(ANIMALS)
    bg = random.choice(BGS)
    prompt = (f"Cute cartoon mascot avatar of a happy {animal} head, big friendly eyes, "
              f"flat vector illustration style, soft rounded shapes, centered composition, "
              f"simple {bg} circular background, clean thick outlines, no text, "
              f"suitable as a social media profile picture")
    r = requests.post(f"{GPTI2}/v1/images/generations",
                      headers={"Authorization": f"Bearer {GPTI2_KEY}",
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0",
                               "Idempotency-Key": f"yt-avatar-r{row}-{random.randint(10000,99999)}"},
                      json={"prompt": prompt, "size": "1024x1024", "quality": "medium", "n": 1},
                      timeout=180)
    r.raise_for_status()
    img = base64.b64decode(r.json()["data"][0]["b64_json"])
    os.makedirs(AVATAR_DIR, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9]+", "_", mail.split("@")[0])
    path = os.path.join(AVATAR_DIR, f"row{row}_{safe}_avatar.png")
    Image.open(io.BytesIO(img)).save(path, "PNG")  # re-save Pillow: xoa chunk C2PA
    print(f"    avatar ({animal}, {bg}) -> {path}")
    return path


def process_row(svc, row):
    print(f"== DONG {row} ==")
    mail, creds, existing_f = get_row_mail(svc, row)
    if not mail:
        print("    BO QUA: cot B trong"); return
    if existing_f:
        print(f"    BO QUA: F da co kenh ({existing_f})"); return
    print(f"    mail: {mail}")
    pid = find_gpm_profile(mail)
    if not pid:
        print("    FAIL: khong tim thay profile GPM trung ten mail"); return
    ws = gpm_start(pid)
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(ws)
            ctx = browser.contexts[0]
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            # auto-accept moi dialog (ke ca beforeunload "Roi khoi trang web?" cua Studio)
            page.on("dialog", lambda d: d.accept())

            # --- 0. kiem tra login. MAC DINH: KHONG tu login (anh login tay) ---
            if is_logged_in(page):
                print("    da login san")
            elif AUTO_LOGIN:
                if not creds:
                    print("    FAIL: chua login ma cot C khong co credential"); return
                print("    chua login -> dang login...")
                if not gmail_login(page, creds[0], creds[1], creds[2]):
                    return
                print("    login OK")
            else:
                print("    CHUA LOGIN -> bo qua (anh login tay roi chay lai dong nay)")
                return

            # --- 1. tao kenh (giu ten mac dinh; handle trung -> them so 1-9) ---
            page.goto("https://www.youtube.com/create_channel", wait_until="domcontentloaded", timeout=60000)
            # dialog "How you'll appear" render CHAM (>6s) -> cho dong toi da 25s
            channel_name = handle = channel_url = None
            # load lanh YouTube co the >25s (dinh that dong 13) -> cho toi 60s
            btn = page.get_by_role("button", name=RX_CREATE)
            deadline = time.time() + 60
            while time.time() < deadline and btn.count() == 0:
                if is_violated(page):
                    mark_violated(svc, row)
                    return
                page.wait_for_timeout(2000)
            if btn.count():  # dialog "How you'll appear" -> chua co kenh
                for attempt in range(4):
                    vis = [i for i in page.locator("input").all()
                           if i.is_visible() and i.input_value().strip()]
                    if len(vis) >= 2:
                        channel_name, handle = vis[0].input_value(), vis[1].input_value()
                    if attempt > 0 and len(vis) >= 2:
                        # handle bi trung -> them so random 1-9 vao cuoi
                        handle = handle + str(random.randint(1, 9))
                        vis[1].click()
                        page.keyboard.press("Control+a")
                        page.keyboard.type(handle, delay=50)
                        page.wait_for_timeout(1000)
                    page.get_by_role("button", name=RX_CREATE).first.click()
                    page.wait_for_timeout(9000)
                    if "/channel/" in page.url:
                        channel_url = page.url
                        break
                    if not page.get_by_role("button", name=RX_CREATE).count():
                        break  # dialog dong, coi nhu xong
                    err = page.locator("body").inner_text()
                    snippet = " | ".join(l for l in err.splitlines()
                                         if ("taken" in l.lower() or "exist" in l.lower()
                                             or "not available" in l.lower() or "try" in l.lower()))[:200]
                    print(f"    tao kenh chua qua (lan {attempt+1}): {snippet or 'khong ro loi'} -> them so vao handle")
                if channel_url is None and "/channel/" in page.url:
                    channel_url = page.url
                print(f"    kenh tao moi: {channel_name} (@{handle}) {channel_url}")
            else:
                print("    tai khoan DA co kenh -> chi up avatar")

            # --- 2. lay channel id qua Studio ---
            page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(7000)
            if is_violated(page):
                mark_violated(svc, row)
                return
            m = re.search(r"/channel/(UC[\w-]+)", page.url)
            if not m:
                raise RuntimeError(f"khong lay duoc channel id tu url {page.url}")
            cid = m.group(1)
            channel_url = channel_url or f"https://www.youtube.com/channel/{cid}"

            # --- 3. sinh avatar ---
            img_path = gen_avatar(row, mail)

            # --- 4. Studio editing/profile: upload Picture ---
            page.goto(f"https://studio.youtube.com/channel/{cid}/editing/profile",
                      wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(7000)
            dlg = page.locator("ytcp-warm-welcome-dialog")           # dialog lan dau vao Studio
            if dlg.count():
                b = dlg.get_by_role("button", name=RX_CONT)
                if not b.count():
                    b = dlg.get_by_role("button", name=RX_CLOSE)
                if b.count():
                    b.first.click()
                page.wait_for_timeout(2500)
            page.keyboard.press("Escape")
            close = page.get_by_role("button", name=RX_CLOSE)          # tooltip Ask Studio
            if close.count():
                try: close.first.click(); page.wait_for_timeout(1200)
                except Exception: pass

            if channel_name is None:
                # kenh co san -> doc ten/handle tu form Name/Handle cua trang editing
                vis = [i.input_value() for i in page.locator("input").all()
                       if i.is_visible() and i.input_value().strip()]
                if len(vis) >= 2:
                    channel_name, handle = vis[0], vis[1].lstrip("@")
                    print(f"    ten kenh hien tai: {channel_name} (@{handle})")

            upload_btn = None
            for b in page.get_by_role("button", name=RX_UPLOAD).all():  # phan biet Picture vs Banner
                where = b.evaluate("""el => { let n = el;
                    for (let i=0;i<8 && n;i++){ n = n.parentElement;
                      var t = (n && n.innerText) ? n.innerText.toLowerCase() : '';
                      if (t && (t.includes('profile picture')||t.includes('ảnh hồ sơ'))) return 'PICTURE';
                      if (t && (t.includes('top of your channel')||t.includes('đầu kênh')||t.includes('banner'))) return 'BANNER'; }
                    return 'UNKNOWN'; }""")
                if where == "PICTURE":
                    upload_btn = b; break
            if upload_btn is None:
                # avatar da co san -> nut la "Change"
                ch = page.get_by_role("button", name=RX_CHANGE)
                if ch.count():
                    upload_btn = ch.first
                else:
                    raise RuntimeError("khong thay nut Upload/Change cua khoi Picture")
            with page.expect_file_chooser(timeout=15000) as fc:
                upload_btn.click()
            fc.value.set_files(img_path)
            page.wait_for_timeout(6000)
            done = page.get_by_role("button", name=RX_DONE)            # dialog crop
            if done.count():
                done.first.click(); page.wait_for_timeout(3500)
            pub = page.get_by_role("button", name=RX_PUBLISH).first
            if pub.get_attribute("aria-disabled") != "true":
                pub.click(); page.wait_for_timeout(7000)
            ok = page.get_by_role("button", name=RX_PUBLISH).first.get_attribute("aria-disabled") == "true"
            print(f"    publish avatar: {'OK' if ok else 'CHUA XAC NHAN — kiem tra tay'}")
            # Studio giu co "unsaved" ke ca sau Publish -> go handler beforeunload + roi trang
            # de GPM stop khong bi ket dialog "Roi khoi trang web?"
            try:
                page.evaluate("window.onbeforeunload = null")
                page.goto("https://www.youtube.com/", wait_until="domcontentloaded", timeout=30000)
            except Exception:
                pass

            # --- 5. ghi sheet TEN KENH / NGAY TAO KENH (tra cot theo HEADER, khong hardcode) ---
            today = date.today().strftime("%d/%m/%Y")
            # TEN KENH: CHI ghi handle "@..." (anh chot 2026-09-06), khong ghi kem ten kenh
            f_val = f"@{handle.lstrip('@')}" if handle else channel_url
            c_name, c_date = col(svc, "TÊN KÊNH"), col(svc, "NGÀY TẠO KÊNH")
            svc.spreadsheets().values().batchUpdate(
                spreadsheetId=SHEET_ID,
                body={"valueInputOption": "USER_ENTERED", "data": [
                    {"range": f"{TAB}!{c_name}{row}", "values": [[f_val]]},
                    {"range": f"{TAB}!{c_date}{row}", "values": [[today]]}]}).execute()
            print(f"    sheet {c_name}{row}={f_val} | {c_date}{row}={today}")
    finally:
        gpm_stop(pid)
        print("    profile GPM da dong")


AUTO_LOGIN = False  # mac dinh anh login tay; them co --login de tool tu login bang cot C

# Nut/anchor tren YouTube-Studio doi theo NGON NGU tai khoan (co profile tieng Viet)
# -> moi selector theo ten phai match SONG NGU (dinh that dong 11: "Tao kenh" != "Create channel")
RX_CREATE  = re.compile(r"^(Create channel|Tạo kênh)$", re.I)
RX_DONE    = re.compile(r"^(Done|Xong)$", re.I)
RX_PUBLISH = re.compile(r"^(Publish|Xuất bản|Đăng)$", re.I)
RX_CONT    = re.compile(r"^(Continue|Tiếp tục|Got it|Đã hiểu)$", re.I)
RX_CLOSE   = re.compile(r"^(Close|Đóng)$", re.I)
RX_UPLOAD  = re.compile(r"^(Upload|Tải lên)$", re.I)
RX_CHANGE  = re.compile(r"^(Change|Thay đổi)$", re.I)


def main():
    global AUTO_LOGIN
    if "--login" in sys.argv:
        AUTO_LOGIN = True
        sys.argv.remove("--login")
    if len(sys.argv) < 2:
        print("Dung: py -3.13 tools\\channel_setup.py <dong|dong_dau-dong_cuoi> [--login]"); sys.exit(1)
    arg = sys.argv[1]
    if "-" in arg:
        a, b = arg.split("-"); rows = range(int(a), int(b) + 1)
    else:
        rows = [int(arg)]
    svc = sheets_svc()
    for row in rows:
        try:
            process_row(svc, row)
        except Exception as e:
            print(f"    LOI dong {row}: {e!r}")


if __name__ == "__main__":
    main()
