#!/bin/bash
# restart_login.sh — graceful restart Chrome dự án + tự đăng nhập lại (khi grab degradation).
# An toàn vì có do_login.py tự auth lại. Dùng khi grab_one fail nhiều.
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
echo "=== graceful close ==="
py -3.13 -c "
from playwright.sync_api import sync_playwright
try:
    with sync_playwright() as p:
        b=p.chromium.connect_over_cdp('http://127.0.0.1:9345'); b.new_browser_cdp_session().send('Browser.close'); print('closed')
except Exception as e: print('close err',e)
" 2>/dev/null
for i in $(seq 1 15); do
  n=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"name='chrome.exe'\" | Where-Object { \$_.CommandLine -like '*h2dev*chrome_profile*' }).ProcessId" 2>/dev/null | grep -cE "[0-9]")
  [ "$n" -eq 0 ] && { echo "closed ${i}s"; break; }; sleep 1
done
echo "=== relaunch ==="
"$CHROME" --user-data-dir=E:\\CLAUDE\\YOUTUBE\\h2dev\\chrome_profile --profile-directory=Default --remote-debugging-port=9345 --disk-cache-size=1 --media-cache-size=1 --new-window https://h2dev.vn/learn/study/1 >/dev/null 2>&1 &
sleep 13
echo "=== login ==="
py -3.13 /e/CLAUDE/YOUTUBE/h2dev/tools/do_login.py
