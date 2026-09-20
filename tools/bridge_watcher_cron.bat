@echo off
REM ============================================================
REM  bridge_watcher_cron.bat — chay moi 3 phut qua Task Scheduler
REM  Task: HermesBridgeWatcher  (tao: schtasks /Create ...)
REM ============================================================
cd /d E:\CLAUDE\YOUTUBE\h2dev
set PYTHONPATH=
py -3.13 -X utf8 tools\bridge_watcher.py --once >> tools\bridge_cron.log 2>&1
