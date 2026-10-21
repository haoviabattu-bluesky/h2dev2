# -*- coding: utf-8 -*-
r"""
XÁC MINH KÊNH MỚI — Studio → Settings → Channel → Feature eligibility (anh chốt 2026-10-08).

  2. Intermediate features → "Verify phone number" → tab youtube.com/verify → thuê số US TinOTP
     ("Google, Gmail, Youtube - United States (virtual) 1", category 1004, service_id 1119) → nhập mã → đóng tab.
  3. Advanced features → "Access features" → chọn "Build history as you grow" (= Channel history) → Next → Done.

Chạy (sau channel_branding.py, profile GPM tên = mail, đã login sẵn):
  py -3.13 tools\xac_minh_kenh.py --mail moonierwescott384@gmail.com
  py -3.13 tools\xac_minh_kenh.py --mail ... --chi-xem          (chỉ đọc trạng thái 3 cấp, không thuê số)

Đo thật 2026-10-08 (kênh Lane G 定年後のしごと帖, mail moonierwescott384): thuê số 1.951đ, OTP về sau ~8s, "Phone number verified".
Bẫy đã dính:
- TinOTP API: `?api_key=` BỊ TẮT → phải gửi header `X-Api-Key`. `/services/rent` giờ là **POST** (GET trả 405).
- Bấm chữ "2. Intermediate features" KHÔNG mở khung → phải bấm `ytcp-icon-button[aria-label=Expand]` trong
  `yt-trust-tiers-home-level` thứ 2; nút "Verify phone number" nằm sẵn trong DOM nhưng ẩn tới khi mở.
- Chọn Channel history xong, nhãn cấp 3 VẪN là "Eligible" (đang tích lịch sử ~2 tháng) — đó là đúng, không phải lỗi.
- Google từ chối số / không sang step 2 → tool HUỶ số (hoàn tiền vì chưa nhận OTP) rồi thử số khác (tối đa --so-lan).
"""
import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from playwright.sync_api import sync_playwright  # noqa: E402

from channel_setup import find_gpm_profile, gpm_start, gpm_stop  # noqa: E402

TINOTP = "https://tinotp.site/api"
TINOTP_KEY = "tinotp_sk_18d4e046a87b6319eb3429901248f868"     # tk thankhanhduy4627@gmail.com
SERVICE_US1, CATEGORY_GOOGLE = "1119", "1004"
LOG = Path(__file__).resolve().parent.parent / "docs" / "_log_xac_minh_kenh.jsonl"

RX_CHANNEL = re.compile(r"^(Channel|Kênh)$")
RX_FEATURE = re.compile(r"^(Feature eligibility|Điều kiện sử dụng tính năng)$")
RX_NEXT = re.compile(r"^(NEXT|Next|TIẾP|Tiếp)$")
RX_SUBMIT = re.compile(r"^(SUBMIT|Submit|GỬI|Gửi)$")
RX_ACCESS = re.compile(r"^(Access features|Truy cập tính năng)$")
RX_HISTORY = re.compile(r"^(Build history as you grow|Xây dựng lịch sử.*)$")
RX_DONE = re.compile(r"^(Done|Xong)$")
RX_ENABLED = re.compile(r"\b(Enabled|Đã bật)\b")


def tin(method, path, **params):
    r = requests.request(method, f"{TINOTP}{path}", headers={"X-Api-Key": TINOTP_KEY},
                         params=params, timeout=60)
    if r.status_code == 405:                         # API đổi method → thử method kia
        r = requests.request("POST" if method == "GET" else "GET", f"{TINOTP}{path}",
                             headers={"X-Api-Key": TINOTP_KEY}, params=params, timeout=60)
    return r.json()


def log(rec):
    rec["ts"] = datetime.now().isoformat(timespec="seconds")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def open_feature_tab(page):
    # hộp "Welcome to YouTube Studio" ở kênh mới tinh: backdrop chặn click → bấm Continue trước
    for b in page.get_by_role("button", name=re.compile(r"^(Continue|Tiếp tục|Got it|Đã hiểu)$")).all():
        try:
            if b.is_visible():
                b.click(); page.wait_for_timeout(1500)
        except Exception:
            pass
    page.keyboard.press("Escape")
    page.locator("ytcp-navigation-drawer #settings-item").first.click()
    page.wait_for_timeout(3000)
    dlg = page.locator("ytcp-settings-dialog").first
    [t for t in dlg.get_by_text(RX_CHANNEL, exact=True).all() if t.is_visible()][-1].click()
    page.wait_for_timeout(1500)
    dlg.get_by_text(RX_FEATURE).first.click()
    page.wait_for_timeout(3000)
    lv = page.locator("yt-trust-tiers-home-level")
    lv.nth(2).locator(".feature-level-bar").wait_for(state="visible", timeout=20000)
    return lv


def levels_status(lv):
    return [lv.nth(i).locator(".feature-level-bar").inner_text().replace("\n", " | ")
            for i in range(lv.count())]


def expand(page, level):
    exp = level.locator('ytcp-icon-button[aria-label="Expand"]')
    if exp.count() and exp.first.is_visible():
        exp.first.click(); page.wait_for_timeout(2000)


def verify_phone(ctx, page, lv, mail, max_price, so_lan):
    lvl = lv.nth(1)
    expand(page, lvl)
    btn = lvl.locator('button[aria-label="Verify phone number"], button[aria-label="Xác minh số điện thoại"]')
    if not btn.count() or not btn.first.is_visible():
        raise RuntimeError("không thấy nút Verify phone number trong 2. Intermediate features")
    with ctx.expect_page(timeout=20000) as np:
        btn.first.click()
    v = np.value
    v.wait_for_load_state("domcontentloaded"); v.wait_for_timeout(5000)
    try:
        for lan in range(1, so_lan + 1):
            # quốc gia nằm trong VALUE của ô readonly, inner_text không chứa (bẫy dính 08/10 kênh J/N)
            qg = " ".join(i.input_value() for i in v.locator("input[readonly]").all())
            if "United States" not in qg and "Hoa Kỳ" not in qg:
                raise RuntimeError("trang verify không để sẵn quốc gia United States → chọn tay rồi chạy lại")
            r = tin("POST", "/services/rent", service_id=SERVICE_US1, category=CATEGORY_GOOGLE, max_price=max_price)
            d = r.get("data") or {}
            rid, phone = d.get("rental_id"), str(d.get("phone_number") or "")
            if not rid or not phone:
                raise RuntimeError(f"thuê số thất bại: {r}")
            so = re.sub(r"\D", "", phone)
            so = so[1:] if len(so) == 11 and so.startswith("1") else so
            print(f"    lượt {lan}: thuê số {phone} (rental {rid}, {d.get('price')}đ)")
            inp = v.locator('input[placeholder="(201) 555-5555"]')
            if not inp.count():
                inp = v.locator('input[type="text"]:not([readonly])')
            inp.first.click(); inp.first.fill(so); v.wait_for_timeout(1000)
            v.get_by_text(RX_NEXT).first.click(); v.wait_for_timeout(6000)
            if not re.search(r"step 2|bước 2", v.inner_text("body"), re.I):
                print("    Google không nhận số →", v.inner_text("body")[:200].replace("\n", " "))
                print("    huỷ số:", tin("POST", "/services/cancel", rental_id=rid).get("message"))
                log({"mail": mail, "rental": rid, "phone": phone, "ket_qua": "google_tu_choi"})
                v.reload(); v.wait_for_timeout(5000)
                continue
            code, t0 = None, time.time()
            while time.time() - t0 < 300:
                c = (tin("GET", "/services/check", rental_id=rid).get("data") or {})
                if str(c.get("status")) == "1" and c.get("code"):
                    code = re.search(r"\d{6}", str(c["code"])).group(0); break
                if str(c.get("status")) == "-1":
                    break
                time.sleep(4)
            if not code:
                print("    hết 5 phút không có OTP → huỷ:", tin("POST", "/services/cancel", rental_id=rid).get("message"))
                log({"mail": mail, "rental": rid, "phone": phone, "ket_qua": "khong_co_otp"})
                v.reload(); v.wait_for_timeout(5000)
                continue
            print(f"    OTP {code}")
            ci = [i for i in v.locator("input").all() if i.is_visible() and i.get_attribute("readonly") is None]
            ci[0].click(); ci[0].fill(code); v.wait_for_timeout(1000)
            v.get_by_text(RX_SUBMIT).first.click(); v.wait_for_timeout(7000)
            ok = re.search(r"Phone number verified|đã được xác minh", v.inner_text("body"), re.I)
            log({"mail": mail, "rental": rid, "phone": phone, "ket_qua": "verified" if ok else "submit_khong_ro"})
            if not ok:
                raise RuntimeError("đã nhập OTP nhưng không thấy 'Phone number verified': " + v.inner_text("body")[:200])
            print(f"    OK Phone number verified ({phone})")
            return phone
        raise RuntimeError(f"thử {so_lan} số vẫn không verify được")
    finally:
        try:
            v.close()                                   # đóng tab điền phone (bước anh yêu cầu)
        except Exception:
            pass


def channel_history(page, lv):
    lvl = lv.nth(2)
    expand(page, lvl)
    # ngay sau verify phone + reload, khung cấp 3 render chậm → chờ nút/ô thật thay vì sleep cố định
    acc = lvl.get_by_role("button", name=RX_ACCESS).first
    try:
        acc.wait_for(state="visible", timeout=15000)
    except Exception:
        # Kênh đã chọn Channel history từ trước (Lane J 08/10, kênh cũ 戦国の裏側): khung Requirements chỉ còn
        # "AND · Channel history", KHÔNG có nút Access features → coi như đã đăng ký.
        if re.search(r"AND\s*Channel history\s*$", lvl.inner_text().strip()):
            print("    OK Channel history đã đăng ký từ trước (không còn nút Access features)"); return
        raise
    acc.click()
    opt = page.get_by_text("Build history as you grow", exact=True)
    if not opt.count():
        page.wait_for_timeout(3000)
    if not opt.count():
        opt = page.get_by_text(RX_HISTORY)
    opt.first.wait_for(state="visible", timeout=20000); opt.first.click(); page.wait_for_timeout(1500)
    nxt = [x for x in page.get_by_role("button", name=RX_NEXT).all() if x.is_visible()]
    if not nxt:
        raise RuntimeError("không thấy nút Next ở hộp Get advanced features")
    nxt[-1].click(); page.wait_for_timeout(5000)
    txt = " ".join(d.inner_text() for d in page.locator("tp-yt-paper-dialog, ytcp-dialog").all() if d.is_visible())
    ok = re.search(r"channel history is being established|lịch sử kênh", txt, re.I)
    done = [x for x in page.get_by_role("button", name=RX_DONE).all() if x.is_visible()]
    if done:
        done[-1].click(); page.wait_for_timeout(2000)
    if not ok:
        raise RuntimeError("không thấy xác nhận 'Your channel history is being established'")
    print("    OK Channel history: đang tích lịch sử (~2 tháng), nhãn cấp 3 vẫn 'Eligible' là đúng")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mail", required=True, help="tên profile GPM = mail kênh")
    ap.add_argument("--max-price", type=int, default=2500, help="giá trần thuê số (VNĐ)")
    ap.add_argument("--so-lan", type=int, default=3, help="số lần thử số khác nếu Google từ chối")
    ap.add_argument("--chi-xem", action="store_true")
    ap.add_argument("--keep-open", action="store_true")
    a = ap.parse_args()

    pid = find_gpm_profile(a.mail)
    if not pid:
        print("DỪNG: không thấy profile GPM tên =", a.mail); return 2
    ws = gpm_start(pid)
    rc = 0
    try:
        with sync_playwright() as p:
            ctx = p.chromium.connect_over_cdp(ws).contexts[0]
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)
            if "/channel/" not in page.url:
                print("DỪNG: Studio không vào được kênh:", page.url); return 2
            print(f"== XÁC MINH {a.mail} — {page.url}")
            lv = open_feature_tab(page)
            st = levels_status(lv)
            for s in st:
                print("   ", s)
            if a.chi_xem:
                return 0
            if RX_ENABLED.search(st[1]):
                print("    2. Intermediate đã Enabled → bỏ qua verify phone")
            else:
                verify_phone(ctx, page, lv, a.mail, a.max_price, a.so_lan)
                page.bring_to_front(); page.reload(wait_until="domcontentloaded"); page.wait_for_timeout(6000)
                lv = open_feature_tab(page)
            if RX_ENABLED.search(levels_status(lv)[2]):
                print("    3. Advanced đã Enabled → bỏ qua")
            else:
                channel_history(page, lv)
            print("== SAU:")
            for s in levels_status(lv):
                print("   ", s)
            page.keyboard.press("Escape")
    except Exception as e:
        print("!! LỖI:", e); rc = 1
    finally:
        if not a.keep_open:
            gpm_stop(pid); print("    profile GPM đã đóng")
    return rc


if __name__ == "__main__":
    sys.exit(main())
