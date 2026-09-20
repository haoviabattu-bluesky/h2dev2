# -*- coding: utf-8 -*-
"""Tự đăng nhập h2dev qua Playwright CDP (khi mất phiên). In LOGIN_OK / LOGIN_FAIL."""
import sys, time
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

EMAIL = "hduongwwork@gmail.com"
PASSWORD = "duonghoang123"
CDP = "http://127.0.0.1:9345"

def is_logged_in(pg):
    try:
        t = pg.evaluate("()=>document.body?document.body.innerText:''")
        return ('Đăng nhập' not in t) and ('/study/' in pg.url)
    except Exception:
        return False

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp(CDP)
    pg = b.contexts[0].pages[0]
    pg.goto("https://h2dev.vn/learn/study/1", wait_until="commit", timeout=60000); time.sleep(7)
    if is_logged_in(pg):
        print("LOGIN_OK (already)"); sys.exit(0)
    # open login modal from /learn
    pg.goto("https://h2dev.vn/learn", wait_until="commit", timeout=60000); time.sleep(5)
    pg.evaluate("""()=>{const el=[...document.querySelectorAll('*')].find(e=>e.children.length===0&&(e.textContent||'').trim()==='Đăng nhập'); if(el){let n=el;for(let i=0;i<6&&n;i++){if((n.className||'').toString().includes('cursor'))break;n=n.parentElement;}(n||el).click();}}""")
    time.sleep(3)
    try:
        pg.fill("input[name='email']", EMAIL)
        pg.fill("input[name='password']", PASSWORD)
        try: pg.check("input[name='isRemember']")
        except Exception: pass
        time.sleep(1)
        # click submit button in the form (type=submit)
        pg.evaluate("""()=>{const pw=document.querySelector("input[name='password']");const f=pw.closest('form');const bs=[...f.querySelectorAll('button')];const sb=bs.find(b=>b.type==='submit')||bs[bs.length-1]; if(sb)sb.click(); else f.requestSubmit&&f.requestSubmit();}""")
    except Exception as e:
        print("fill err:", e)
    # wait for login
    for _ in range(20):
        time.sleep(1)
        try:
            if '/study/' in pg.url or 'token' in [c['name'] for c in b.contexts[0].cookies('https://h2dev.vn')]:
                break
        except Exception: pass
    time.sleep(2)
    pg.goto("https://h2dev.vn/learn/study/1", wait_until="commit", timeout=60000); time.sleep=7
    time.sleep(6)
    if is_logged_in(pg):
        print("LOGIN_OK")
    else:
        cks=[c['name'] for c in b.contexts[0].cookies('https://h2dev.vn')]
        print("LOGIN_FAIL url=",pg.url[:60],"cookies=",cks)
