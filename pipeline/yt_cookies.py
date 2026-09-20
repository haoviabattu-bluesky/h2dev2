"""yt_cookies.py — lấy cookie YouTube từ Chrome ĐANG CHẠY qua CDP, xuất file Netscape cho yt-dlp.

Vì sao không dùng `yt-dlp --cookies-from-browser`: trên Windows, Chrome 127+ mã hoá cookie bằng
App-Bound Encryption nên đọc thẳng file cookie hay hỏng; và profile đang mở thì DB bị khoá.
Đọc qua CDP thì Chrome tự giải mã hộ, KHÔNG cần đóng trình duyệt (dự án này CẤM kill Chrome).

Dùng:
  py -3.13 yt_cookies.py --port 9333 --out yt_cookies.txt
  set YTDLP_COOKIES=<đường dẫn>   (fetch_script.py tự dùng)
"""
import argparse
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DOMAINS = (".youtube.com", "youtube.com", ".google.com", ".googlevideo.com")


def grab(port):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        out = []
        for ctx in b.contexts:
            for c in ctx.cookies():
                if any(c["domain"].endswith(d.lstrip(".")) for d in DOMAINS):
                    out.append(c)
        b.close()
    # bỏ trùng theo (domain, name)
    seen, uniq = set(), []
    for c in out:
        k = (c["domain"], c["name"])
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    return uniq


def to_netscape(cookies):
    lines = ["# Netscape HTTP Cookie File", "# sinh bởi yt_cookies.py (CDP)"]
    for c in cookies:
        dom = c["domain"]
        flag = "TRUE" if dom.startswith(".") else "FALSE"
        exp = int(c.get("expires") or 0)
        if exp <= 0:
            exp = int(time.time()) + 86400 * 7      # cookie phiên → cho hạn 7 ngày
        lines.append("\t".join([dom, flag, c.get("path", "/"),
                                "TRUE" if c.get("secure") else "FALSE",
                                str(exp), c["name"], c["value"]]))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9333)
    ap.add_argument("--out", default="yt_cookies.txt")
    a = ap.parse_args()
    cs = grab(a.port)
    names = sorted({c["name"] for c in cs})
    logged = any(n in names for n in ("SID", "__Secure-1PSID", "__Secure-3PSID", "LOGIN_INFO"))
    Path(a.out).write_text(to_netscape(cs), encoding="utf-8")
    print(f"✓ {len(cs)} cookie → {a.out} · đăng nhập Google: {'CÓ' if logged else 'KHÔNG'}")
    print("  tên:", ", ".join(names[:14]) + (" …" if len(names) > 14 else ""))


if __name__ == "__main__":
    main()
