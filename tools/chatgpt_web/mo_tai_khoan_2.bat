@echo off
REM ============================================================
REM  Mo Chrome profile RIENG cho TAI KHOAN ChatGPT THU 2 (acc2) - dang nhap tay 1 lan
REM  - user-data-dir rieng  : E:\CLAUDE\YOUTUBE\CHATGPT_PROFILE_2
REM  - remote debugging port: 9336  (acc1 = 9335, Veo3 9333, Grok 9334)
REM  Dang nhap xong thi DONG cua so nay lai - tool pipeline\gptweb_pool.py tu mo/dong cong khi can.
REM ============================================================
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --user-data-dir=E:\CLAUDE\YOUTUBE\CHATGPT_PROFILE_2 ^
  --remote-debugging-port=9336 ^
  --no-first-run ^
  --no-default-browser-check ^
  --new-window https://chatgpt.com/
