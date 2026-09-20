# -*- coding: utf-8 -*-
r"""
SETUP BRANDING kenh Lane D (色が語る記憶) — dong 5 sheet GMAIL, mail AmmarHilham@gmail.com,
kenh da co san "irogatatarukioku" (tao 06/09/2026). Khong tao kenh moi — chi:
  1. Doi TEN kenh hien thi -> 色が語る記憶 (giu nguyen handle @irogatatarukioku)
  2. Up avatar (Picture) + banner (Banner) trong Studio Branding
  3. Dien Description + Channel keywords trong Studio Basic info

Chay:  py -3.13 tools\channel_branding_laneD.py
Yeu cau: mail da LOGIN SAN trong profile GPM (script khong tu login, giong channel_setup.py).
"""
import os
import re
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright

from channel_setup import (
    sheets_svc, SHEET_ID, TAB, find_gpm_profile, gpm_start, gpm_stop,
    is_logged_in, is_violated, mark_violated,
    RX_CONT, RX_CLOSE, RX_DONE, RX_PUBLISH, RX_UPLOAD, RX_CHANGE,
)

ROW = 5
MAIL = "AmmarHilham@gmail.com"
CHANNEL_NAME = "色が語る記憶"
DESCRIPTION = (
    "当時の白黒写真をAIで色付けし、その一枚に写る一人ひとりの物語を追います。\n"
    "戦争・戦後・引き揚げ・収容所——教科書には載らない、名もなき人々の記録です。\n"
    "色の正確さより、その時代の空気を伝えることを大切にしています。毎日更新。"
)
KEYWORDS = ["戦争 写真", "AI カラー化", "白黒写真 復元", "昭和史", "太平洋戦争", "実話 歴史",
            "特攻隊", "戦争体験", "歴史ドキュメンタリー", "AIフルカラー復元"]

BRANDING_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "assets", "laneD", "branding")
AVATAR_PATH = os.path.join(BRANDING_DIR, "avatar_raw.png")
BANNER_PATH = os.path.join(BRANDING_DIR, "banner_final.png")

RX_NAME_TAB = re.compile(r"^(Basic info|Thông tin cơ bản)$", re.I)
RX_BRANDING_TAB = re.compile(r"^(Branding|Thương hiệu)$", re.I)
RX_SAVE = re.compile(r"^(Save|Lưu)$", re.I)


def upload_branding_images(page):
    """Trang Branding (Picture + Banner). Tra ve True neu ca 2 upload xong."""
    page.wait_for_timeout(3000)
    dlg = page.locator("ytcp-warm-welcome-dialog")
    if dlg.count():
        b = dlg.get_by_role("button", name=RX_CONT)
        if not b.count():
            b = dlg.get_by_role("button", name=RX_CLOSE)
        if b.count():
            b.first.click()
        page.wait_for_timeout(2000)
    page.keyboard.press("Escape")
    close = page.get_by_role("button", name=RX_CLOSE)
    if close.count():
        try:
            close.first.click(); page.wait_for_timeout(1000)
        except Exception:
            pass

    for label, path in (("PICTURE", AVATAR_PATH), ("BANNER", BANNER_PATH)):
        upload_btn = None
        for b in page.get_by_role("button", name=RX_UPLOAD).all():
            where = b.evaluate("""el => { let n = el;
                for (let i=0;i<8 && n;i++){ n = n.parentElement;
                  var t = (n && n.innerText) ? n.innerText.toLowerCase() : '';
                  if (t && (t.includes('profile picture')||t.includes('ảnh hồ sơ'))) return 'PICTURE';
                  if (t && (t.includes('top of your channel')||t.includes('đầu kênh')||t.includes('banner'))) return 'BANNER'; }
                return 'UNKNOWN'; }""")
            if where == label:
                upload_btn = b
                break
        if upload_btn is None:
            # da co san anh -> nut la Change, phan biet bang cung logic tren khoi cha cua Change
            for b in page.get_by_role("button", name=RX_CHANGE).all():
                where = b.evaluate("""el => { let n = el;
                    for (let i=0;i<8 && n;i++){ n = n.parentElement;
                      var t = (n && n.innerText) ? n.innerText.toLowerCase() : '';
                      if (t && (t.includes('profile picture')||t.includes('ảnh hồ sơ'))) return 'PICTURE';
                      if (t && (t.includes('top of your channel')||t.includes('đầu kênh')||t.includes('banner'))) return 'BANNER'; }
                    return 'UNKNOWN'; }""")
                if where == label:
                    upload_btn = b
                    break
        if upload_btn is None:
            print(f"    ! khong tim thay nut Upload/Change cho {label} -> bo qua")
            continue
        with page.expect_file_chooser(timeout=15000) as fc:
            upload_btn.click()
        fc.value.set_files(path)
        page.wait_for_timeout(6000)
        done = page.get_by_role("button", name=RX_DONE)
        if done.count():
            done.first.click(); page.wait_for_timeout(3000)
        print(f"    {label} da chon file: {os.path.basename(path)}")

    pub = page.get_by_role("button", name=RX_PUBLISH).first
    if pub.count() and pub.get_attribute("aria-disabled") != "true":
        pub.click()
        page.wait_for_timeout(7000)
    ok = (not pub.count()) or pub.get_attribute("aria-disabled") == "true"
    print(f"    publish branding: {'OK' if ok else 'CHUA XAC NHAN - kiem tra tay'}")
    return ok


def fill_basic_info(page):
    """Trang Basic info: doi Name, dien Description, dien Channel keywords."""
    page.wait_for_timeout(3000)
    page.keyboard.press("Escape")

    # --- Name: input dau tien trong khoi co label Name/Ten kenh ---
    name_input = page.locator("#channel-title textarea, #channel-title input").first
    if not name_input.count():
        # fallback: input dau tien visible co gia tri khac rong
        vis = [i for i in page.locator("input, textarea").all() if i.is_visible()]
        name_input = vis[0] if vis else None
    if name_input and (hasattr(name_input, "count") is False or name_input.count() if hasattr(name_input, "count") else True):
        try:
            name_input.click()
            page.keyboard.press("Control+a")
            page.keyboard.type(CHANNEL_NAME, delay=40)
            page.wait_for_timeout(500)
            print(f"    ten kenh -> {CHANNEL_NAME}")
        except Exception as e:
            print(f"    ! khong sua duoc ten kenh: {e!r}")

    # --- Description ---
    desc_box = page.locator("#description-textarea textarea").first
    if not desc_box.count():
        desc_box = page.get_by_label(re.compile("Description|Mô tả", re.I))
    if desc_box.count():
        desc_box.click()
        page.keyboard.press("Control+a")
        page.keyboard.type(DESCRIPTION, delay=15)
        page.wait_for_timeout(500)
        print("    description da dien")
    else:
        print("    ! khong tim thay o Description")

    return True


def fill_keywords(page):
    """Advanced settings co Channel keywords (o cuoi trang Basic info hoac link rieng)."""
    adv = page.get_by_text(re.compile("Advanced settings|Cài đặt nâng cao", re.I))
    if adv.count():
        adv.first.click()
        page.wait_for_timeout(2000)
    kw_input = page.locator("#text-input").filter(has=page.locator("xpath=ancestor::*[contains(., 'keyword') or contains(., 'từ khóa')]"))
    box = page.get_by_placeholder(re.compile("keyword|từ khóa", re.I))
    target = box if box.count() else kw_input
    if target.count():
        target.first.click()
        for kw in KEYWORDS:
            page.keyboard.type(kw, delay=20)
            page.keyboard.press("Enter")
            page.wait_for_timeout(150)
        print(f"    {len(KEYWORDS)} keyword da them")
        return True
    print("    ! khong tim thay o Channel keywords -> bo qua (dien tay sau)")
    return False


def save_basic_info(page):
    pub = page.get_by_role("button", name=RX_PUBLISH).first
    save = page.get_by_role("button", name=RX_SAVE).first
    btn = pub if pub.count() else save
    if btn.count() and btn.get_attribute("aria-disabled") != "true":
        btn.click()
        page.wait_for_timeout(6000)
        print("    da bam Publish/Save cho Basic info")
        return True
    print("    ! khong bam duoc Publish/Save (co the da luu san hoac nut disabled)")
    return False


def main():
    svc = sheets_svc()
    v = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"{TAB}!B{ROW}:H{ROW}").execute()
    vals = (v.get("values") or [[]])[0]
    mail = vals[0].strip() if vals else ""
    if mail.lower() != MAIL.lower():
        print(f"CANH BAO: dong {ROW} hien la mail {mail!r}, khac {MAIL!r} da hardcode -> dung lai kiem tra")
        return
    print(f"== Setup branding Lane D cho dong {ROW} ({mail}) ==")

    pid = find_gpm_profile(mail)
    if not pid:
        print("FAIL: khong tim thay profile GPM"); return
    ws = gpm_start(pid)
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(ws)
            ctx = browser.contexts[0]
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.on("dialog", lambda d: d.accept())

            if not is_logged_in(page):
                print("CHUA LOGIN -> anh login tay roi chay lai"); return
            print("    da login san")

            page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)
            if is_violated(page):
                print("    KENH VI PHAM -> dung lai"); return
            m = re.search(r"/channel/(UC[\w-]+)", page.url)
            if not m:
                raise RuntimeError(f"khong lay duoc channel id tu {page.url}")
            cid = m.group(1)
            print(f"    channel id: {cid}")

            # --- 1. Branding: Picture + Banner ---
            page.goto(f"https://studio.youtube.com/channel/{cid}/editing/profile",
                      wait_until="domcontentloaded", timeout=60000)
            upload_branding_images(page)
            page.wait_for_timeout(2000)

            # --- 2. Basic info: Name + Description ---
            page.goto(f"https://studio.youtube.com/channel/{cid}/editing/basicinfo",
                      wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)
            if "editing/basicinfo" not in page.url:
                # fallback: click tab "Basic info" tu trang editing/profile
                page.goto(f"https://studio.youtube.com/channel/{cid}/editing",
                          wait_until="domcontentloaded", timeout=60000)
                tab = page.get_by_role("tab", name=RX_NAME_TAB)
                if tab.count():
                    tab.first.click(); page.wait_for_timeout(2000)
            fill_basic_info(page)
            fill_keywords(page)
            save_basic_info(page)

            try:
                page.evaluate("window.onbeforeunload = null")
                page.goto("https://www.youtube.com/", wait_until="domcontentloaded", timeout=30000)
            except Exception:
                pass
            print(f"    XONG. Kiem tra tay: https://studio.youtube.com/channel/{cid}/editing")
    finally:
        gpm_stop(pid)
        print("    profile GPM da dong")


if __name__ == "__main__":
    main()
