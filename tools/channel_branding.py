# -*- coding: utf-8 -*-
r"""
SETUP KÊNH THẬT (A. Branding + B. 6 mục Settings) — THAM SỐ HOÁ, đọc 1 file KENH.json.

Thay cho channel_branding_laneD.py / channel_branding_laneE.py (hardcode 1 kênh). Quy trình gốc:
docs/QUY_TRINH_SETUP_KENH.md mục "⭐ QUY TRÌNH SETUP KÊNH ĐẦY ĐỦ" + memory channel-settings-checklist.

Chạy:
  py -3.13 tools\channel_branding.py --config assets\<lane>\branding\KENH.json            (làm hết A+B)
  py -3.13 tools\channel_branding.py --config ... --steps profile                          (chỉ A: avatar/banner/tên/handle/mô tả/links/email)
  py -3.13 tools\channel_branding.py --config ... --steps settings                         (chỉ B: currency/audience/upload defaults/keywords/country)
  py -3.13 tools\channel_branding.py --config ... --check-only                             (KHÔNG sửa gì, chỉ reload + báo trạng thái hiện tại)
  py -3.13 tools\channel_branding.py --config ... --no-sheet                               (không ghi sheet)

Yêu cầu: GPMLogin đang mở + mail đã LOGIN SẴN trong profile GPM (tool không tự login).
Nguyên tắc: mỗi mục RELOAD trang thật để đọc trạng thái trước, đã đúng thì KHÔNG ghi đè.
Không tìm thấy phần tử → chụp màn hình vào branding_dir/_s_*.png rồi báo, KHÔNG đoán.
UI Studio đổi ngôn ngữ theo tài khoản → mọi selector theo tên là regex SONG NGỮ Anh/Việt.
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright

from channel_setup import (
    sheets_svc, SHEET_ID, TAB, find_gpm_profile, gpm_start, gpm_stop,
    is_logged_in, is_violated, get_row_mail, totp_fresh, col,
)

# ---------------- regex song ngữ ----------------
RX_CONT = re.compile(r"^(Continue|Tiếp tục|Got it|Đã hiểu)$", re.I)
RX_CLOSE = re.compile(r"^(Close|Đóng)$", re.I)
RX_DONE = re.compile(r"^(Done|Xong)$", re.I)
RX_PUBLISH = re.compile(r"^(Publish|Xuất bản|Đăng)$", re.I)
RX_UPLOAD = re.compile(r"^(Upload|Tải lên)$", re.I)
RX_CHANGE = re.compile(r"^(Change|Thay đổi)$", re.I)
RX_SAVE = re.compile(r"^(Save|Lưu)$", re.I)
RX_NAME_PH = re.compile(r"channel name|tên kênh", re.I)
RX_HANDLE_PH = re.compile(r"handle|tên người dùng", re.I)
RX_SETTINGS = re.compile(r"^(Settings|Cài đặt)$", re.I)
RX_TAB_GENERAL = re.compile(r"^(General|Chung)$", re.I)
RX_TAB_CHANNEL = re.compile(r"^(Channel|Kênh)$", re.I)
RX_TAB_UPLOAD = re.compile(r"^(Upload defaults|Chế độ cài đặt mặc định cho video tải lên|.*mặc định.*tải lên.*)$", re.I)
RX_SUB_BASIC = re.compile(r"^(Basic info|Thông tin cơ bản)$", re.I)
RX_SUB_ADV = re.compile(r"^(Advanced settings|Cài đặt nâng cao)$", re.I)
RX_VIDEO_DESC_PH = re.compile(r"Tell viewers about your video|Giới thiệu cho người xem", re.I)
RX_ADD_LINK = re.compile(r"^(Add link|Thêm đường liên kết|Thêm liên kết)$", re.I)
RX_NOT_KIDS = re.compile(r"(No, set this channel as not made for kids|Không, đặt kênh này là không dành cho trẻ em)", re.I)

CURRENCY_LABEL = {"VND": r"VND\s*[—-]\s*(Vietnamese Dong|Đồng Việt Nam)"}
LANG_LABEL = {"Japanese": r"^(Japanese|Tiếng Nhật)$", "Korean": r"^(Korean|Tiếng Hàn)$", "English": r"^(English|Tiếng Anh)"}
COUNTRY_LABEL = {"Japan": r"^(Japan|Nhật Bản)$", "Vietnam": r"^(Vietnam|Việt Nam)$"}


class Ctx:
    def __init__(self, page, cfg, bdir, check_only):
        self.page, self.cfg, self.bdir, self.check_only = page, cfg, bdir, check_only
        self.report = []

    def shot(self, name):
        p = os.path.join(self.bdir, f"_s_{name}.png")
        try:
            self.page.screenshot(path=p)
        except Exception:
            pass
        return p

    def log(self, msg, ok=None):
        tag = {True: "OK ", False: "!! ", None: "   "}[ok]
        print(f"    {tag}{msg}")
        self.report.append((ok, msg))


RX_VERIFY = re.compile(r"Verify it.s you|Xác minh đó là bạn|Xác minh danh tính", re.I)
RX_NEXT = re.compile(r"^(Next|Tiếp theo)$", re.I)
CREDS = None   # (mail, pass, 2fa_secret) đọc từ cột C — set trong main()


def handle_verify(page):
    """Hộp "Verify it's you" của Google (hiện khi sửa tên/handle). Next -> mật khẩu -> TOTP.
    Dùng credential cột C (đã có sẵn trong sheet, cùng tài khoản). Màn lạ -> chụp ảnh, trả False."""
    body = page.locator("body").inner_text()
    if not RX_VERIFY.search(body):
        return True
    print("    hộp Verify it's you -> xử lý bằng mật khẩu + TOTP cột C")
    if not CREDS:
        print("    !! không có credential cột C -> anh xác minh tay"); return False
    _, pw, secret = CREDS
    nb = page.get_by_role("button", name=RX_NEXT)
    n_before = len(page.context.pages)
    if nb.count():
        nb.first.click()
    page.wait_for_timeout(5000)
    # Đo thật Lane I 2026-09-20: bấm Next KHÔNG đổi tab hiện tại — Google mở POPUP accounts.google.com
    # trong cùng context -> phải tìm trang đó rồi thao tác ở đó.
    vp = None
    for pg in page.context.pages:
        if "accounts.google.com" in (pg.url or ""):
            vp = pg; break
    if vp is None and len(page.context.pages) > n_before:
        vp = page.context.pages[-1]
    if vp is None:
        vp = page
    try:
        vp.wait_for_selector('input[name="Passwd"], input[type="password"]', timeout=20000)
        vp.wait_for_timeout(1200)
        vp.locator('input[name="Passwd"], input[type="password"]').first.fill(pw)
        vp.keyboard.press("Enter")
    except Exception:
        vp.screenshot(path="_verify_no_password.png")
        print(f"    !! không tới màn mật khẩu (popup={vp is not page}, {vp.url})"); return False
    try:
        vp.wait_for_selector("#totpPin", timeout=20000)
    except Exception:
        vp.wait_for_timeout(3000)
        if vp.is_closed() or "accounts.google.com" not in (vp.url or ""):
            return True
        print(f"    !! sau mật khẩu không ra TOTP ({vp.url})"); return False
    last = None
    for _ in range(3):
        code = totp_fresh(secret, avoid=last); last = code
        try:
            vp.fill("#totpPin", code); vp.keyboard.press("Enter")
        except Exception:
            pass
        t = time.time() + 12
        while time.time() < t:
            if vp.is_closed() or "accounts.google.com" not in (vp.url or "") or "challenge" not in (vp.url or ""):
                page.wait_for_timeout(3000); return True
            time.sleep(1)
    print(f"    !! TOTP bị từ chối 3 lần ({vp.url})"); return False


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
            close.first.click(); page.wait_for_timeout(800)
        except Exception:
            pass
    handle_verify(page)


def where_button(b):
    """PICTURE / BANNER / UNKNOWN — phân biệt nút Upload/Change bằng innerText tổ tiên."""
    return b.evaluate("""el => { let n = el;
        for (let i=0;i<8 && n;i++){ n = n.parentElement;
          var t = (n && n.innerText) ? n.innerText.toLowerCase() : '';
          if (t && (t.includes('profile picture')||t.includes('ảnh hồ sơ'))) return 'PICTURE';
          if (t && (t.includes('top of your channel')||t.includes('đầu kênh')||t.includes('banner')||t.includes('ảnh bìa'))) return 'BANNER'; }
        return 'UNKNOWN'; }""")


def find_upload_button(page, kind):
    for rx in (RX_CHANGE, RX_UPLOAD):
        for b in page.get_by_role("button", name=rx).all():
            if not b.is_visible():
                continue
            if where_button(b) == kind:
                return b
    return None


def upload_image(page, btn, path, label, c):
    with page.expect_file_chooser(timeout=15000) as fc:
        btn.click()
    fc.value.set_files(path)
    page.wait_for_timeout(6000)
    done = page.get_by_role("button", name=RX_DONE)
    if done.count():
        done.first.click(); page.wait_for_timeout(3000)
    c.log(f"{label}: đã chọn {os.path.basename(path)}", True)


def type_into(page, loc, text):
    loc.click()
    page.keyboard.press("Control+a")
    page.keyboard.type(text, delay=12)
    page.wait_for_timeout(400)


# ======================= A. PROFILE PAGE =======================
def goto_profile(page, cid):
    page.goto(f"https://studio.youtube.com/channel/{cid}/editing/profile",
              wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(5000)
    dismiss_dialogs(page)


def read_profile_state(page):
    st = {}
    n = page.get_by_placeholder(RX_NAME_PH)
    st["name"] = n.first.input_value() if n.count() else None
    h = page.get_by_placeholder(RX_HANDLE_PH)
    st["handle"] = h.first.input_value().lstrip("@") if h.count() else None
    d = page.locator('div[contenteditable="true"]#textbox')
    st["description"] = d.first.inner_text().strip() if d.count() else None
    body = page.locator("body").inner_text()
    st["has_banner"] = find_upload_button(page, "BANNER") is not None and \
        any(b.is_visible() for b in page.get_by_role("button", name=RX_CHANGE).all())
    st["body"] = body
    return st


def step_profile(c: Ctx, cid):
    page, cfg = c.page, c.cfg
    goto_profile(page, cid)
    st = read_profile_state(page)
    c.log(f"hiện tại: tên={st['name']!r} handle=@{st['handle']} mô tả={len(st['description'] or '')} ký tự")
    c.shot("profile_before")
    if c.check_only:
        return st

    avatar = os.path.join(c.bdir, cfg["avatar"])
    banner = os.path.join(c.bdir, cfg["banner"])
    for kind, path, label in (("BANNER", banner, "BANNER"), ("PICTURE", avatar, "AVATAR")):
        if not os.path.exists(path):
            c.log(f"{label}: thiếu file {path} -> bỏ qua", False); continue
        btn = find_upload_button(page, kind)
        if btn is None:
            c.shot(f"no_{label.lower()}_button")
            c.log(f"{label}: không thấy nút Upload/Change -> bỏ qua, soi tay", False); continue
        upload_image(page, btn, path, label, c)
        page.wait_for_timeout(1500)

    if st["name"] != cfg["channel_name"]:
        n = page.get_by_placeholder(RX_NAME_PH)
        if n.count():
            type_into(page, n.first, cfg["channel_name"]); c.log(f"tên kênh -> {cfg['channel_name']}", True)
        else:
            c.log("không tìm thấy ô Tên kênh", False)
    else:
        c.log("tên kênh đã đúng sẵn", True)

    if st["handle"] != cfg["handle"]:
        h = page.get_by_placeholder(RX_HANDLE_PH)
        if h.count():
            type_into(page, h.first, cfg["handle"]); page.wait_for_timeout(3500)
            # YouTube kiểm handle NGAY khi gõ: "This handle isn't available. Here's one available: @xxx"
            # (đo thật Lane H 2026-09-20: Publish vẫn bấm được, mọi thứ khác lưu, RIÊNG handle bị bỏ qua
            # im lặng) -> phải đọc khối cha của ô handle, không tin "đã gõ = đã đổi".
            msg = h.first.evaluate("""el => { let n = el; for (let i=0;i<10 && n;i++){ n = n.parentElement;
                if (n && n.innerText && /available|không|invalid|không hợp lệ|taken/i.test(n.innerText)) return n.innerText.slice(0,300); }
                return ''; }""")
            if re.search(r"isn.t available|not available|không có sẵn|đã được sử dụng|invalid|không hợp lệ", msg, re.I):
                sug = re.search(r"@([\w.-]+)", msg.split("available:")[-1]) if "available:" in msg else None
                c.log(f"HANDLE @{cfg['handle']} BỊ TỪ CHỐI: {msg.strip()[:160]}" + (f" | gợi ý YouTube: @{sug.group(1)}" if sug else ""), False)
                type_into(page, h.first, st["handle"] or "")      # trả lại handle cũ để không chặn Publish
                page.wait_for_timeout(1500)
            else:
                c.log(f"handle -> @{cfg['handle']} (giới hạn 2 lần/14 ngày)", True)
        else:
            c.log("không tìm thấy ô Handle", False)
    else:
        c.log("handle đã đúng sẵn", True)

    want_desc = cfg["description"].strip()
    if (st["description"] or "").replace("\r", "") != want_desc:
        d = page.locator('div[contenteditable="true"]#textbox')
        if d.count():
            d.first.click(); page.keyboard.press("Control+a"); page.keyboard.type(want_desc, delay=6)
            c.log("mô tả đã điền", True)
        else:
            c.log("không tìm thấy ô Description (contenteditable #textbox)", False)
    else:
        c.log("mô tả đã đúng sẵn", True)

    # Contact email: chỉ điền nếu trống
    email = cfg.get("contact_email") or cfg["mail"]
    em = page.locator('input[type="email"], input[placeholder*="mail" i]')
    filled = False
    for i in range(em.count()):
        e = em.nth(i)
        if not e.is_visible():
            continue
        cur = e.input_value().strip()
        if cur.lower() == email.lower():
            c.log("contact email đã đúng sẵn", True); filled = True; break
        if not cur:
            type_into(page, e, email); c.log(f"contact email -> {email}", True); filled = True; break
        c.log(f"contact email hiện là {cur!r} (khác), KHÔNG ghi đè", None); filled = True; break
    if not filled:
        c.log("không thấy ô Contact email (có thể đã có sẵn dạng khác) -> soi ảnh", False)

    # Links: chỉ báo, Studio thường tự điền sẵn Youtube link
    body = page.locator("body").inner_text()
    if f"youtube.com/channel/{cid}" in body or "youtube.com/@" in body:
        c.log("Links: đã thấy URL kênh trong trang (tự điền sẵn)", True)
    else:
        al = page.get_by_role("button", name=RX_ADD_LINK)
        if al.count():
            al.first.click(); page.wait_for_timeout(2000); c.log("Links: đã bấm Add link 1 lần (Studio tự điền Youtube)", True)
        else:
            c.log("Links: không thấy nút Add link -> soi tay", False)

    c.shot("profile_before_publish")
    pub = page.get_by_role("button", name=RX_PUBLISH).first
    if pub.count() and pub.get_attribute("aria-disabled") != "true":
        pub.click(); page.wait_for_timeout(8000)
        c.log("đã bấm Publish (Profile)", True)
    ok = (not pub.count()) or pub.get_attribute("aria-disabled") == "true"
    c.log(f"Publish xác nhận: {'OK' if ok else 'CHƯA — kiểm tra tay'}", ok)
    c.shot("profile_after_publish")
    return st


# ======================= B. SETTINGS MODAL =======================
# Bản đồ DOM đo thật 2026-09-20 (Studio EN, kênh VirgiliTraino): modal = <ytcp-settings-dialog>,
# tab trái + tab con là CHỮ THƯỜNG (không role=tab) -> get_by_text(exact).last trong dialog;
# Currency = nút chữ "USD — US Dollar"; Country = nút "Select"; Keywords placeholder
# "Enter comma-separated values"; Upload/Advanced: "Video language" + "Title and description language"
# đều là nút "Select" (Category là "None"). Save riêng từng tab, lưu ngay.
RX_SELECT = re.compile(r"^(Select|Chọn)$", re.I)
RX_KW_PH = re.compile(r"comma-separated|keyword|từ khóa|từ khoá|dấu phẩy", re.I)


def open_settings(page, c: Ctx):
    page.keyboard.press("Escape")
    link = page.locator("ytcp-navigation-drawer #settings-item")     # icon bánh răng, sống cả khi sidebar thu gọn
    if not link.count():
        link = page.get_by_text(RX_SETTINGS, exact=True)
    if not link.count():
        c.shot("no_settings_link"); raise RuntimeError("không thấy Settings (#settings-item) ở sidebar")
    link.first.click(); page.wait_for_timeout(3000)
    dlg = page.locator("ytcp-settings-dialog")
    if not dlg.count():
        c.shot("no_settings_dialog"); raise RuntimeError("bấm Settings nhưng không thấy ytcp-settings-dialog")
    return dlg.first


def click_tab(dlg, page, rx, c: Ctx, label):
    vis = [t for t in dlg.get_by_text(rx, exact=True).all() if t.is_visible()]
    if not vis:
        c.shot(f"no_tab_{label}"); c.log(f"không thấy tab {label}", False); return False
    vis[-1].click(); page.wait_for_timeout(1500); return True


def dropdown(dlg, label_rx):
    """Dropdown Studio = <ytcp-dropdown-trigger role=button> chứa nhãn + giá trị (đo thật 2026-09-20).
    Trả (locator, text hiện tại) — text gồm 'Nhãn|Giá trị'."""
    loc = dlg.locator("ytcp-dropdown-trigger").filter(has_text=label_rx)
    vis = [x for x in loc.all() if x.is_visible()]
    if not vis:
        return None, ""
    return vis[0], vis[0].inner_text().replace("\n", "|")


def save_settings(dlg, page, c: Ctx, label):
    save = dlg.get_by_role("button", name=RX_SAVE)
    if save.count() and save.first.get_attribute("aria-disabled") != "true" and save.first.is_enabled():
        save.first.click(); page.wait_for_timeout(3500); c.log(f"Save ({label})", True); return True
    c.log(f"Save ({label}): nút disabled = không có thay đổi", None); return False


def close_settings(page):
    page.keyboard.press("Escape"); page.wait_for_timeout(800)


def pick_option(page, rx, c: Ctx, label):
    """Sau khi bấm nút dropdown: chọn option theo text trong menu vừa bung."""
    page.wait_for_timeout(1200)
    opt = page.locator("tp-yt-paper-item, [role='option']").filter(has_text=rx)
    vis = [o for o in opt.all() if o.is_visible()]
    if not vis:
        vis = [o for o in page.get_by_text(rx).all() if o.is_visible()]
    if not vis:
        c.shot(f"no_option_{label}"); page.keyboard.press("Escape"); c.log(f"{label}: không thấy option", False); return False
    vis[-1].click(); page.wait_for_timeout(1000); return True


def settings_currency(c: Ctx, cid):
    page, cfg = c.page, c.cfg
    want = cfg.get("currency", "VND")
    goto_profile(page, cid)
    dlg = open_settings(page, c)
    click_tab(dlg, page, RX_TAB_GENERAL, c, "General")
    body = dlg.inner_text()
    if re.search(CURRENCY_LABEL[want], body):
        c.log(f"Currency đã là {want} sẵn", True); c.shot("currency_ok"); close_settings(page); return
    c.shot("currency_before")
    if c.check_only:
        c.log(f"Currency CHƯA phải {want}", False); close_settings(page); return
    dd, _ = dropdown(dlg, re.compile(r"Currency|Đơn vị tiền", re.I))
    if dd is None:
        c.shot("currency_no_trigger"); c.log("Currency: không thấy dropdown", False); close_settings(page); return
    dd.click()
    if pick_option(page, re.compile(CURRENCY_LABEL[want], re.I), c, "Currency"):
        c.log(f"Currency -> {want}", True)
        save_settings(dlg, page, c, "Currency")
    c.shot("currency_saved")
    close_settings(page)


def settings_channel(c: Ctx, cid):
    """Channel > Basic info (Country, Keywords) rồi Advanced settings (Audience). Save riêng từng tab con."""
    page, cfg = c.page, c.cfg
    goto_profile(page, cid)
    dlg = open_settings(page, c)
    if not click_tab(dlg, page, RX_TAB_CHANNEL, c, "Channel"):
        close_settings(page); return
    click_tab(dlg, page, RX_SUB_BASIC, c, "Basic info")
    c.shot("channel_basic")
    body = dlg.inner_text()
    # --- Country ---
    want_c = cfg.get("country")
    if want_c:
        if re.search(COUNTRY_LABEL.get(want_c, want_c).strip("^$"), body):
            c.log(f"Country đã là {want_c}", True)
        elif c.check_only:
            c.log(f"Country CHƯA phải {want_c}", False)
        else:
            dd, txt = dropdown(dlg, re.compile(r"Country of residence|Quốc gia", re.I))
            if dd is not None:
                dd.click()
                if pick_option(page, re.compile(COUNTRY_LABEL.get(want_c, want_c), re.I), c, "Country"):
                    c.log(f"Country -> {want_c} (trước: {txt})", True)
            else:
                c.log("Country: không thấy dropdown -> soi ảnh", False)
    # --- Keywords ---
    kws = cfg.get("keywords") or []
    have = [k for k in kws if k in body]
    if kws and len(have) == len(kws):
        c.log(f"Keywords đã đủ {len(kws)}/{len(kws)}", True)
    elif kws and c.check_only:
        c.log(f"Keywords mới có {len(have)}/{len(kws)}", False)
    elif kws:
        box = dlg.get_by_placeholder(RX_KW_PH)
        if box.count():
            missing = [k for k in kws if k not in body]
            box.first.click()
            for kw in missing:
                page.keyboard.type(kw, delay=15); page.keyboard.press("Enter"); page.wait_for_timeout(200)
            c.log(f"Keywords thêm {len(missing)} (đã có {len(have)})", True)
        else:
            c.shot("no_keywords_box"); c.log("không thấy ô Keywords", False)
    saved = False
    if not c.check_only:
        c.shot("channel_basic_filled")
        saved = save_settings(dlg, page, c, "Channel/Basic info")
    # --- Audience (Advanced settings) — Save ở trên làm modal TỰ ĐÓNG (toast "Settings saved",
    # đo thật 2026-09-20) -> phải mở lại modal + tab Channel rồi mới sang tab con ---
    if saved:
        page.wait_for_timeout(1500)
        dlg = open_settings(page, c)
        click_tab(dlg, page, RX_TAB_CHANNEL, c, "Channel")
    click_tab(dlg, page, RX_SUB_ADV, c, "Advanced settings")
    c.shot("channel_adv")
    radio = dlg.locator("tp-yt-paper-radio-button, [role='radio']").filter(has_text=RX_NOT_KIDS)
    vis = [r for r in radio.all() if r.is_visible()]
    if not vis:
        c.log("Audience: không thấy radio 'not made for kids' -> soi ảnh", False)
    else:
        checked = vis[0].get_attribute("aria-checked") == "true"
        if checked:
            c.log("Audience đã là 'not made for kids'", True)
        elif c.check_only:
            c.log("Audience CHƯA đặt 'not made for kids'", False)
        else:
            vis[0].click(); page.wait_for_timeout(800)
            c.log("Audience -> not made for kids", True)
            save_settings(dlg, page, c, "Channel/Advanced")
    c.shot("channel_adv_after")
    close_settings(page)


def settings_upload_defaults(c: Ctx, cid):
    page, cfg = c.page, c.cfg
    goto_profile(page, cid)
    dlg = open_settings(page, c)
    if not click_tab(dlg, page, RX_TAB_UPLOAD, c, "Upload defaults"):
        close_settings(page); return
    click_tab(dlg, page, RX_SUB_BASIC, c, "Basic info")
    c.shot("upload_basic")
    want = cfg.get("upload_default_description", "")
    ta = dlg.get_by_placeholder(RX_VIDEO_DESC_PH)
    if not ta.count():
        ta = dlg.locator("textarea")
    vis = [t for t in ta.all() if t.is_visible()]
    cur = vis[0].input_value().strip() if vis else None
    if cur is None:
        c.log("Upload defaults: không thấy ô Description", False)
    elif cur == want:
        c.log("Upload defaults Description đã đúng", True)
    elif c.check_only:
        c.log(f"Upload defaults Description hiện {cur!r}", False)
    else:
        type_into(page, vis[0], want); c.log(f"Upload defaults Description -> {want}", True)
    # Advanced: Video language + Title/description language (2 nút "Select")
    click_tab(dlg, page, RX_SUB_ADV, c, "Advanced settings")
    c.shot("upload_adv")
    lang = cfg.get("video_language", "Japanese")
    rx_lang = re.compile(LANG_LABEL.get(lang, f"^{lang}$"), re.I)
    body = dlg.inner_text()
    n_have = len(re.findall(LANG_LABEL.get(lang, lang).strip("^$"), body))
    if n_have >= 2:
        c.log(f"Video language + Title/description language đã là {lang} (thấy {n_have})", True)
    elif c.check_only:
        c.log(f"Ngôn ngữ mới thấy {n_have}/2 chỗ là {lang}", False)
    else:
        done = 0
        for lab in (re.compile(r"Video language|Ngôn ngữ video", re.I),
                    re.compile(r"Title and description language|Ngôn ngữ tiêu đề", re.I)):
            dd, txt = dropdown(dlg, lab)
            if dd is None:
                c.log(f"không thấy dropdown {lab.pattern}", False); continue
            if rx_lang.search(txt.split("|")[-1].strip()):
                done += 1; continue
            dd.click()
            if pick_option(page, rx_lang, c, "Language"):
                done += 1
        c.log(f"Ngôn ngữ {lang}: {done}/2 chỗ", done >= 2)
    if not c.check_only:
        c.shot("upload_adv_filled")
        save_settings(dlg, page, c, "Upload defaults")
    c.shot("upload_saved")
    close_settings(page)


# ======================= VERIFY (reload thật) =======================
def verify_profile(c: Ctx, cid):
    """Reload thật. YouTube cập nhật tên/handle/mô tả TRỄ ~10-30s sau Publish (đo thật 2026-09-20:
    reload ngay ra giá trị cũ dù đã lưu) -> chờ rồi thử tối đa 3 lần."""
    page, cfg = c.page, c.cfg
    st = None
    for i in range(3):
        page.wait_for_timeout(15000 if i == 0 else 10000)
        goto_profile(page, cid)
        st = read_profile_state(page)
        if st["name"] == cfg["channel_name"] and st["handle"] == cfg["handle"]:
            break
    c.log(f"[RELOAD] tên={st['name']!r} {'✓' if st['name']==cfg['channel_name'] else '✗'}", st["name"] == cfg["channel_name"])
    c.log(f"[RELOAD] handle=@{st['handle']} {'✓' if st['handle']==cfg['handle'] else '✗'}", st["handle"] == cfg["handle"])
    ok_d = (st["description"] or "").replace("\r", "") == cfg["description"].strip()
    c.log(f"[RELOAD] mô tả {'khớp' if ok_d else 'KHÁC'}", ok_d)
    c.shot("verify_profile")
    return st


def safe_gpm_start(pid):
    """GPM có lúc trả success nhưng websocket RỖNG (profile đang đóng dở) — mỗi lần gọi start
    là mở thêm 1 cửa sổ. Tối đa 2 lượt, giữa 2 lượt stop + chờ; vẫn rỗng thì DỪNG, không lặp."""
    for attempt in (1, 2):
        try:
            ws = gpm_start(pid)
        except Exception as e:
            ws = ""; print(f"    GPM start lượt {attempt}: {e}")
        if ws and ws.startswith("ws"):
            return ws
        print(f"    GPM start lượt {attempt}: websocket rỗng -> stop + chờ 12s")
        gpm_stop(pid); time.sleep(12)
    raise RuntimeError("GPM không trả websocket sau 2 lượt -> anh kiểm tra cửa sổ profile đang mở dở rồi chạy lại")


def write_sheets(cfg, cid):
    """Ghi sheet theo TÊN CỘT (tra header dòng 1 ngay lúc ghi — memory gmail-sheet-van-hanh).
    GMAIL: TÊN KÊNH=@handle · NGÁCH · THỊ TRƯỜNG · KÊNH_CLONE.  NOTE: NHẬN KÊNH · MAIL · HANDLE · KÊNH."""
    svc = sheets_svc()
    row = cfg["sheet_row"]
    handle = f"@{cfg['handle']}"
    data = [{"range": f"{TAB}!{col(svc, 'TÊN KÊNH')}{row}", "values": [[handle]]}]
    for key, hdr in (("niche", "NGÁCH"), ("market", "THỊ TRƯỜNG"), ("clone_channel", "KÊNH_CLONE")):
        if cfg.get(key):
            data.append({"range": f"{TAB}!{col(svc, hdr)}{row}", "values": [[cfg[key]]]})
    svc.spreadsheets().values().batchUpdate(
        spreadsheetId=SHEET_ID, body={"valueInputOption": "USER_ENTERED", "data": data}).execute()
    for d in data:
        print(f"    sheet {d['range']} <- {d['values'][0][0]}")
    ns = cfg.get("note_sheet")
    if ns:
        tab, r = ns["tab"], ns["row"]
        data = [
            {"range": f"{tab}!{col(svc, 'NHẬN KÊNH', tab)}{r}", "values": [["Đã nhận kênh"]]},
            {"range": f"{tab}!{col(svc, 'MAIL', tab)}{r}", "values": [[cfg["mail"]]]},
            {"range": f"{tab}!{col(svc, 'HANDLE', tab)}{r}", "values": [[cfg["handle"]]]},
            {"range": f"{tab}!{col(svc, 'KÊNH', tab)}{r}", "values": [[handle]]},
        ]
        svc.spreadsheets().values().batchUpdate(
            spreadsheetId=SHEET_ID, body={"valueInputOption": "USER_ENTERED", "data": data}).execute()
        for d in data:
            print(f"    sheet {d['range']} <- {d['values'][0][0]}")


LANE_TAB_HEADER = ["STT", None, "FOLDER", "KỊCH BẢN", "TITLE-DESCREPTION", "TAGS", "THUMBNAIL",
                   "STATUS-IMG", "VIDEO", "LIST", "GHI CHÚ"]     # None = ô B ghép từ lane_label + niche


def ensure_lane_tab(cfg):
    """Sau setup kênh: tạo tab sản xuất riêng tên = lane_id, dòng 1 header A→K giống tab 70dai-kenko
    (anh chốt 2026-09-20). Tab đã có / dòng 1 đã có dữ liệu -> không đụng."""
    svc = sheets_svc()
    tab = cfg["lane_id"]
    meta = svc.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    have = {sh["properties"]["title"] for sh in meta["sheets"]}
    if tab not in have:
        svc.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID,
            body={"requests": [{"addSheet": {"properties": {"title": tab}}}]}).execute()
        print(f"    tạo tab {tab}")
    cur = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"{tab}!A1:K1").execute().get("values")
    if cur and any(cur[0]):
        print(f"    tab {tab}: dòng 1 đã có dữ liệu, giữ nguyên"); return
    b = f"NỘI DUNG - {cfg.get('lane_label', tab)}" + chr(10) + cfg.get('niche', '')
    row = [b if h is None else h for h in LANE_TAB_HEADER]
    svc.spreadsheets().values().update(spreadsheetId=SHEET_ID, range=f"{tab}!A1:K1",
        valueInputOption="USER_ENTERED", body={"values": [row]}).execute()
    print(f"    tab {tab}: header A1:K1 OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--steps", default="profile,settings", help="profile,settings (phẩy)")
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--no-sheet", action="store_true")
    ap.add_argument("--keep-open", action="store_true", help="không stop profile GPM khi xong")
    a = ap.parse_args()

    cfg = json.load(open(a.config, encoding="utf-8"))
    bdir = os.path.dirname(os.path.abspath(a.config))
    steps = [s.strip() for s in a.steps.split(",") if s.strip()]

    svc = sheets_svc()
    row = cfg["sheet_row"]
    v = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"{TAB}!B{row}").execute()
    mail = ((v.get("values") or [[""]])[0] or [""])[0].strip()
    if mail.lower() != cfg["mail"].lower():
        print(f"DỪNG: dòng {row} sheet GMAIL là {mail!r}, config ghi {cfg['mail']!r}"); return 2
    if not a.check_only and not a.no_sheet:
        for hdr in ("TÊN KÊNH", "NGÁCH", "THỊ TRƯỜNG", "KÊNH_CLONE"):
            col(svc, hdr)                      # header đổi thì DỪNG trước khi động vào kênh
    print(f"== {'KIỂM TRA' if a.check_only else 'SETUP'} kênh {cfg['channel_name']} (@{cfg['handle']}) — dòng {row} {mail} ==")

    global CREDS
    _, CREDS, _ = get_row_mail(svc, row)
    pid = find_gpm_profile(mail)
    if not pid:
        print("DỪNG: không tìm thấy profile GPM tên =", mail); return 2
    ws = safe_gpm_start(pid)
    rc = 0
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(ws)
            ctx = browser.contexts[0]
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.on("dialog", lambda d: d.accept())
            if not is_logged_in(page):
                print("DỪNG: CHƯA LOGIN -> anh login tay trong GPM rồi chạy lại"); return 2
            print("    đã login sẵn")
            page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)
            if is_violated(page):
                print("DỪNG: kênh vi phạm"); return 2
            m = re.search(r"/channel/(UC[\w-]+)", page.url)
            if not m:
                raise RuntimeError(f"không lấy được channel id từ {page.url}")
            cid = m.group(1)
            print(f"    channel id: {cid}")
            c = Ctx(page, cfg, bdir, a.check_only)

            if "profile" in steps:
                print("--- A. Profile (branding) ---")
                step_profile(c, cid)
            if "settings" in steps:
                print("--- B. Settings ---")
                for fn in (settings_currency, settings_channel, settings_upload_defaults):
                    try:
                        fn(c, cid)
                    except Exception as e:
                        c.shot(f"err_{fn.__name__}"); c.log(f"{fn.__name__}: LỖI {e}", False)
                        try:
                            page.keyboard.press("Escape")
                        except Exception:
                            pass
            if not a.check_only and "profile" in steps:
                print("--- VERIFY (reload) ---")
                verify_profile(c, cid)

            bad = [m for ok, m in c.report if ok is False]
            print(f"\n== TỔNG: {len([1 for ok,_ in c.report if ok])} OK · {len(bad)} cần soi tay ==")
            for m in bad:
                print("   -", m)
            if not a.check_only and not a.no_sheet and "profile" in steps:
                write_sheets(cfg, cid)
                ensure_lane_tab(cfg)
                print(f"    -> viết docs/BAT_DAU_LANE/{cfg['lane_id']}.md (khuôn: teinengo-real.md) nếu chưa có")
            print(f"    Kiểm tra tay: https://studio.youtube.com/channel/{cid}/editing/profile")
            rc = 1 if bad else 0
            try:
                page.evaluate("window.onbeforeunload = null")
                page.goto("https://www.youtube.com/", wait_until="domcontentloaded", timeout=30000)
            except Exception:
                pass
    finally:
        if not a.keep_open:
            gpm_stop(pid); print("    profile GPM đã đóng")
    return rc


if __name__ == "__main__":
    sys.exit(main())
