# -*- coding: utf-8 -*-
r"""
SETUP BRANDING kenh Lane E (シニア/70歳からの健康習慣 — sinh hoat khoe manh nguoi gia Nhat)
dong 6 sheet GMAIL, mail normaneileenpm218@gmail.com, kenh da co san "@eileennorman-p8o"
(tao 06/09/2026 boi channel_setup.py, avatar la con vat ngau nhien) — khong tao kenh moi, chi:
  1. Up avatar (Photo) + banner (Banner) trong trang "Tuy chinh kenh" (Ho so)
  2. Doi Ten kenh + Handle
  3. Dien Description (div contenteditable #textbox — UI MOI, khac Lane D dung textarea)
  4. Dien Channel keywords trong modal Cai dat > Kenh (UI MOI da doi cho, khong con o Basic info)

Trang Studio nay dang o GIAO DIEN MOI (gop Branding+BasicInfo lam 1 trang "Ho so", khong con
route /editing/basicinfo rieng — goto thang route do se ra trang loi "Rat tiec da xay ra loi").
Profile GPM nay hien UI TIENG VIET (browser locale vi-VN) — moi selector viet theo text tieng Viet,
kem fallback tieng Anh cho profile khac.

Chay:  py -3.13 tools\channel_branding_laneE.py
Yeu cau: mail da LOGIN SAN trong profile GPM (script khong tu login).
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
)

ROW = 6
MAIL = "normaneileenpm218@gmail.com"
CHANNEL_NAME = "70歳からの健康習慣チャンネル"
HANDLE = "70dai-kenko"
DESCRIPTION = (
    "70代・80代の健康的な生活を、毎日の食事と暮らしの知恵からお届けします。難しい話は抜きにして、\n"
    "「今日からできること」をわかりやすく。監修情報は一般的な健康情報に基づきます。毎日更新。"
)
KEYWORDS = ["健康長寿", "高齢者 食事", "70歳 健康", "シニア 筋トレ", "転倒予防", "夜間頻尿", "老化防止"]

BRANDING_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "assets", "laneE", "branding")
AVATAR_PATH = os.path.join(BRANDING_DIR, "avatar_raw.png")
BANNER_PATH = os.path.join(BRANDING_DIR, "banner_final.png")

RX_CONT    = re.compile(r"^(Continue|Tiếp tục|Got it|Đã hiểu)$", re.I)
RX_CLOSE   = re.compile(r"^(Close|Đóng)$", re.I)
RX_DONE    = re.compile(r"^(Done|Xong)$", re.I)
RX_PUBLISH = re.compile(r"^(Publish|Xuất bản|Đăng)$", re.I)
RX_UPLOAD  = re.compile(r"^(Upload|Tải lên)$", re.I)
RX_CHANGE  = re.compile(r"^(Change|Thay đổi)$", re.I)
RX_SAVE    = re.compile(r"^(Save|Lưu)$", re.I)
RX_NAME_PH = re.compile(r"tên kênh|channel name", re.I)
RX_HANDLE_PH = re.compile(r"tên người dùng|handle", re.I)
RX_SETTINGS = re.compile(r"^(Settings|Cài đặt)$", re.I)
RX_CHANNEL_TAB = re.compile(r"^(Channel|Kênh)$", re.I)
RX_ADV_SETTINGS = re.compile(r"Advanced settings|Cài đặt nâng cao", re.I)
RX_KEYWORDS_PH = re.compile(r"keyword|từ khóa", re.I)


def dismiss_dialogs(page):
    page.wait_for_timeout(1500)
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


def upload_one(page, button_locator, path, label):
    with page.expect_file_chooser(timeout=15000) as fc:
        button_locator.click()
    fc.value.set_files(path)
    page.wait_for_timeout(6000)
    done = page.get_by_role("button", name=RX_DONE)
    if done.count():
        done.first.click(); page.wait_for_timeout(3000)
    print(f"    {label} da chon file: {os.path.basename(path)}")


def main():
    svc = sheets_svc()
    v = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"{TAB}!B{ROW}:H{ROW}").execute()
    vals = (v.get("values") or [[]])[0]
    mail = vals[0].strip() if vals else ""
    if mail.lower() != MAIL.lower():
        print(f"CANH BAO: dong {ROW} hien la mail {mail!r}, khac {MAIL!r} da hardcode -> dung lai"); return
    print(f"== Setup branding Lane E cho dong {ROW} ({mail}) ==")

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

            page.goto(f"https://studio.youtube.com/channel/{cid}/editing/profile",
                      wait_until="domcontentloaded", timeout=60000)
            dismiss_dialogs(page)

            # --- 1. Banner: hien tai TRONG -> nut la "Tai len" (chi 1 nut Upload duy nhat) ---
            up = page.get_by_role("button", name=RX_UPLOAD)
            if up.count():
                upload_one(page, up.first, BANNER_PATH, "BANNER")
            else:
                print("    ! khong thay nut Tai len cho banner -> bo qua (co the da co banner)")
            page.wait_for_timeout(1500)

            # --- 2. Avatar: da co san (con vat ngau nhien) -> nut la "Thay doi" ---
            ch = page.get_by_role("button", name=RX_CHANGE)
            if ch.count():
                upload_one(page, ch.first, AVATAR_PATH, "PICTURE")
            else:
                print("    ! khong thay nut Thay doi cho avatar -> bo qua")
            page.wait_for_timeout(1500)

            # --- 3. Ten kenh ---
            name_input = page.get_by_placeholder(RX_NAME_PH)
            if name_input.count():
                name_input.first.click()
                page.keyboard.press("Control+a")
                page.keyboard.type(CHANNEL_NAME, delay=35)
                page.wait_for_timeout(400)
                print(f"    ten kenh -> {CHANNEL_NAME}")
            else:
                print("    ! khong tim thay o Ten kenh")

            # --- 4. Handle ---
            handle_input = page.get_by_placeholder(RX_HANDLE_PH)
            if handle_input.count():
                handle_input.first.click()
                page.keyboard.press("Control+a")
                page.keyboard.type(HANDLE, delay=35)
                page.wait_for_timeout(600)
                print(f"    handle -> @{HANDLE}")
            else:
                print("    ! khong tim thay o Handle")

            # --- 5. Description (div contenteditable) ---
            desc_box = page.locator('div[contenteditable="true"]#textbox').first
            if desc_box.count():
                desc_box.click()
                page.keyboard.press("Control+a")
                page.keyboard.type(DESCRIPTION, delay=8)
                page.wait_for_timeout(400)
                print("    description da dien")
            else:
                print("    ! khong tim thay o Description (contenteditable)")

            page.wait_for_timeout(1000)
            pub = page.get_by_role("button", name=RX_PUBLISH).first
            if pub.count() and pub.get_attribute("aria-disabled") != "true":
                pub.click()
                page.wait_for_timeout(7000)
                print("    da bam Xuat ban (Ho so)")
            ok = (not pub.count()) or pub.get_attribute("aria-disabled") == "true"
            print(f"    xac nhan Ho so: {'OK' if ok else 'CHUA XAC NHAN - kiem tra tay'}")

            page.screenshot(path=os.path.join(BRANDING_DIR, "_after_profile_save.png"))

            # --- 6. Channel keywords: modal Cai dat > Kenh (UI moi doi cho, khong con o Basic info) ---
            page.wait_for_timeout(1500)
            settings_link = page.get_by_text(RX_SETTINGS, exact=True)
            if settings_link.count():
                settings_link.first.click()
                page.wait_for_timeout(2500)
                ch_tab = page.get_by_role("tab", name=RX_CHANNEL_TAB)
                if not ch_tab.count():
                    ch_tab = page.get_by_text(RX_CHANNEL_TAB, exact=True)
                if ch_tab.count():
                    ch_tab.first.click()
                    page.wait_for_timeout(1500)
                adv = page.get_by_text(RX_ADV_SETTINGS)
                if adv.count():
                    adv.first.click()
                    page.wait_for_timeout(1500)
                page.screenshot(path=os.path.join(BRANDING_DIR, "_settings_channel.png"))
                kw_box = page.get_by_placeholder(RX_KEYWORDS_PH)
                if kw_box.count():
                    kw_box.first.click()
                    for kw in KEYWORDS:
                        page.keyboard.type(kw, delay=20)
                        page.keyboard.press("Enter")
                        page.wait_for_timeout(150)
                    print(f"    {len(KEYWORDS)} keyword da them")
                    save = page.get_by_role("button", name=RX_SAVE)
                    if save.count() and save.first.get_attribute("aria-disabled") != "true":
                        save.first.click(); page.wait_for_timeout(3000)
                        print("    da luu Settings")
                else:
                    print("    ! khong tim thay o Channel keywords trong modal Settings -> can soi tay")
                    page.screenshot(path=os.path.join(BRANDING_DIR, "_settings_no_keywords.png"))
            else:
                print("    ! khong tim thay link Cai dat -> bo qua keywords")

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
