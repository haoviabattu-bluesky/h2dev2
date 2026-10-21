# -*- coding: utf-8 -*-
r"""studio_thay_tieu_de_thumb.py — thay TIÊU ĐỀ + THUMBNAIL 1 video trên YouTube Studio qua CDP (profile đã đăng nhập kênh).
Chỉ đụng ô Title + thumbnail rồi Save; không đổi mô tả/tags/hiển thị. In tiêu đề đọc lại sau khi tải lại trang.
    py -3.13 -X utf8 tools\studio_thay_tieu_de_thumb.py --cdp http://127.0.0.1:<port> --video <id> --title "<tiêu đề>" --thumb <png> [--shot <png>]
"""
import argparse, asyncio, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
TB = "#title-textarea #textbox"


async def main(a):
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp(a.cdp)
        pg = await b.contexts[0].new_page()
        url = f"https://studio.youtube.com/video/{a.video}/edit"
        await pg.goto(url, wait_until="domcontentloaded")
        await pg.wait_for_selector(TB, timeout=60000)
        await pg.wait_for_timeout(3000)
        cu = (await pg.inner_text(TB)).strip()
        print("CU:", cu)
        box = pg.locator(TB)
        await box.click()
        await pg.keyboard.press("Control+A")
        await pg.keyboard.press("Delete")
        await pg.keyboard.insert_text(a.title)
        await pg.wait_for_timeout(800)
        # thumbnail: input file ẩn trong khối Thumbnail
        inp = pg.locator("input#file-loader[type=file]").first
        await inp.set_input_files(a.thumb)
        await pg.wait_for_timeout(6000)
        await pg.locator("ytcp-button#save").click()
        await pg.wait_for_timeout(8000)
        if a.shot:
            await pg.screenshot(path=a.shot.replace(".png", "_saved.png"))
        await pg.goto(url, wait_until="domcontentloaded")
        await pg.wait_for_selector(TB, timeout=60000)
        await pg.wait_for_timeout(4000)
        moi = (await pg.inner_text(TB)).strip()
        print("MOI:", moi)
        print("KHOP_TIEU_DE:", moi == a.title)
        if a.shot:
            await pg.screenshot(path=a.shot)
        await pg.close()


ap = argparse.ArgumentParser()
for k in ("--cdp", "--video", "--title", "--thumb"):
    ap.add_argument(k, required=True)
ap.add_argument("--shot", default="")
asyncio.run(main(ap.parse_args()))
