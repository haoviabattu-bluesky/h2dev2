# -*- coding: utf-8 -*-
"""
GRAB 1 LESSON — bọc learn_grab.grab() với: bounce sang bài AN TOÀN (đã học) + mute + retry 3 lần.
KHÔNG lồng sync_playwright: bounce mở/đóng phiên riêng, rồi LG.grab() mở phiên riêng của nó.

Dùng: py -3.13 grab_lesson.py "<needle bài đích>" "<slug_hint>" "<out_prefix>"
"""
import sys, time, os, subprocess
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
import learn_grab as LG

CDP = LG.CDP
SAFE_NEEDLE = "TỰ TRAIN PROMPT VÀ PHÂN TÍCH KÊNH"
SAFE_SLUG = "tu-train-prompt-va-phan-tich"

CLICK_JS = """(needle)=>{const els=[...document.querySelectorAll('*')].filter(e=>e.children.length===0&&e.tagName!=='SCRIPT'&&e.tagName!=='STYLE'&&(e.textContent||'').includes(needle)); if(!els.length)return false; let n=els[0]; for(let i=0;i<10&&n;i++){const c=n.className?n.className.toString():''; if(c.includes('cursor-pointer'))break; n=n.parentElement;} (n||els[0]).click(); return true;}"""
MUTE_JS = "()=>{document.querySelectorAll('video,audio').forEach(v=>{v.muted=true;v.volume=0;});}"

def bounce_to_safe():
    """Mở phiên Playwright riêng: RELOAD tab (reset frame/CDP như relaunch, không kill Chrome),
    rồi click sang bài an toàn, mute, đóng."""
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(CDP)
        ctx = b.contexts[0]; ctx.add_init_script(LG.HOOK)
        pg = ctx.pages[0]; pg.bring_to_front()
        # RELOAD để trang tươi (chống thoái hoá OOPIF/CDP sau nhiều lần điều hướng SPA)
        try:
            pg.reload(wait_until="commit", timeout=60000)
            print("reloaded", flush=True)
        except Exception as e:
            print("reload err:", e, flush=True)
        time.sleep(9)
        for fr in pg.frames:
            try: fr.evaluate(MUTE_JS)
            except Exception: pass
        pg.evaluate(CLICK_JS, SAFE_NEEDLE)
        for _ in range(18):
            time.sleep(1)
            for fr in pg.frames:
                try: fr.evaluate(MUTE_JS)
                except Exception: pass
            if SAFE_SLUG in pg.url: break
        print("bounced to safe:", SAFE_SLUG in pg.url, flush=True)

def main(needle, slug, out):
    for attempt in range(1, 2):   # 1 attempt; outer bash `timeout`+retry chống hang
        print(f"[attempt {attempt}]", flush=True)
        try:
            bounce_to_safe()
        except Exception as e:
            print("bounce err:", e, flush=True)
        time.sleep(2)
        a = None
        try:
            a = LG.grab(needle, slug, out)   # phiên Playwright riêng của grab
        except Exception as e:
            print("grab err:", e, flush=True)
        if a:
            wav = out + ".wav"
            try: LG.split_and_decode(a, wav)
            except Exception: pass
            if not (os.path.exists(wav) and os.path.getsize(wav) > 1500000):
                ff = LG.ffmpeg()
                subprocess.run([ff, "-y", "-i", a, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav], capture_output=True)
            if os.path.exists(wav) and os.path.getsize(wav) > 1500000:
                print("WAV OK:", wav, os.path.getsize(wav), flush=True); return
        print(f"[attempt {attempt}] failed", flush=True)
    print("GIVE UP after 3 attempts", flush=True)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
