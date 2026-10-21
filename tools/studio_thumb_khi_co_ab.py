# -*- coding: utf-8 -*-
r"""studio_thumb_khi_co_ab.py — video đang chạy A/B test thumbnail (khối "Running…"): Options → Upload file → Continue
(YouTube xoá thí nghiệm) → chọn file → Save. Dùng sau studio_thay_tieu_de_thumb.py khi thumbnail không đổi.
    py -3.13 -X utf8 tools\studio_thumb_khi_co_ab.py --cdp http://127.0.0.1:<port> --video <id> --thumb <png> [--shot <png>]
"""
import argparse, asyncio, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")


async def main(a):
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp(a.cdp)
        pg = await b.contexts[0].new_page()
        await pg.goto(f"https://studio.youtube.com/video/{a.video}/edit", wait_until="domcontentloaded")
        await pg.wait_for_selector("#title-textarea #textbox", timeout=60000)
        await pg.wait_for_timeout(4000)
        ed = pg.locator("ytcp-thumbnails-experiment-editor#thumbnail-experiment-editor")
        if not await ed.count():
            print("KHONG_CO_AB")
            return
        await ed.scroll_into_view_if_needed(); await ed.hover(); await pg.wait_for_timeout(800)
        await ed.locator("[aria-label=Options]").click(); await pg.wait_for_timeout(1200)
        await pg.locator("tp-yt-paper-item:visible", has_text="Upload file").first.click()
        await pg.wait_for_timeout(2500)
        async with pg.expect_file_chooser(timeout=20000) as fc:
            await pg.locator("ytcp-button:visible, button:visible", has_text="Continue").last.click()
        await (await fc.value).set_files(a.thumb)
        await pg.wait_for_timeout(7000)
        await pg.locator("ytcp-button#save").click()
        await pg.wait_for_timeout(8000)
        await pg.reload(wait_until="domcontentloaded")
        await pg.wait_for_selector("#title-textarea #textbox", timeout=60000)
        await pg.wait_for_timeout(5000)
        print("CON_AB:", await pg.locator("ytcp-thumbnails-experiment-editor#thumbnail-experiment-editor").count())
        if a.shot:
            sec = pg.locator("ytcp-video-thumbnail-editor").first
            await sec.scroll_into_view_if_needed()
            await pg.screenshot(path=a.shot)
        await pg.close()


ap = argparse.ArgumentParser()
for k in ("--cdp", "--video", "--thumb"):
    ap.add_argument(k, required=True)
ap.add_argument("--shot", default="")
asyncio.run(main(ap.parse_args()))
