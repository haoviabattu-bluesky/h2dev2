@echo off
REM ============================================================================
REM  build_exe.bat - dong goi tool lam video Satori thanh .exe (PyInstaller --onedir)
REM  Theo skill tao_tool_exe.md. Chay: build_exe.bat   (tu thu muc pipeline\)
REM
REM  Sau khi build:
REM    <out>\"Youtube Clone-Gemini"\"Youtube Clone-Gemini.exe"                -> mo giao dien
REM    <out>\"Youtube Clone-Gemini"\"Youtube Clone-Gemini.exe" --selftest     -> ghi selftest.log CANH exe
REM    <out>\"Youtube Clone-Gemini"\"Youtube Clone-Gemini.exe" --selftest --ping  -> kiem ca ket noi LLM
REM  Doi API key o may khac: sua keys.json DAT CANH exe, khong can build lai.
REM
REM  BAY WINDOWS da dinh: KHONG the xoa/doi ten thu muc dang la CWD cua tien trinh khac.
REM  Chi can 1 cua so cmd/bash dung trong dist\"Youtube Clone-Gemini" la PyInstaller bao
REM  "PermissionError WinError 32" va build hong. Script tu chuyen sang dist_new khi gap.
REM ============================================================================
setlocal enabledelayedexpansion
cd /d "%~dp0"
REM  Ten co DAU CACH -> moi cho dung %APP% deu PHAI boc nhay kep, ke ca `if exist` va `rmdir`,
REM  khong thi batch cat ten lam doi va lenh chay nham thu muc.
set "APP=Youtube Clone-Gemini"

echo [1/5] Kiem xem tool co dang chay khong
REM  ⛔ TUYET DOI KHONG `taskkill` o day. Ban cu dang chay CO THE DANG LAM VIDEO DO:
REM  giet no la mat ca luot chay (da xay ra that 2026-09-09 - giet dung luc user dang
REM  lam video, may man chua toi buoc ve anh nen chua mat tien).
REM  Thay vi tu tien giet, DUNG LAI va bao user tu dong.
tasklist /FI "IMAGENAME eq %APP%.exe" 2>nul | find /I "%APP%.exe" >nul
if not errorlevel 1 (
  echo.
  echo ****************************************************************************
  echo  DUNG BUILD: "%APP%.exe" DANG CHAY.
  echo  No co the dang lam video - build se lam hong luot chay do.
  echo  Hay DONG tool roi chay lai build_exe.bat.
  echo ****************************************************************************
  exit /b 2
)

echo [2/5] Don ban build cu
REM  ⚠ KHONG con phai "cat giu roi tra lai" du lieu nguoi dung: tu 2026-09-09 du lieu (ho so kenh,
REM  keys.json, cai dat, video da lam) nam NGOAI thu muc cai — mac dinh Documents\YoutubeCloneGemini,
REM  doi duoc trong tab 3, nho o %APPDATA%\YoutubeCloneGemini\config.json. Xem paths.py.
REM  Cach cu chi cuu duoc luc build tren may nay; user tu thay ban moi la van mat sach.
if exist build rmdir /s /q build
if exist "dist\%APP%" rmdir /s /q "dist\%APP%" >nul 2>&1
set "OUTDIR=dist"
if exist "dist\%APP%" (
  REM  Xoa khong het = ban cu DANG CHAY (hoac 1 cua so dang dung trong do). PyInstaller build
  REM  sang dist_new, nhung cai con lai o dist la MOT CAI VO RONG VAN CO FILE EXE — bam vao la
  REM  "Failed to load Python DLL python313.dll". User da bam nham that 2026-09-09.
  REM  => VO HIEU HOA no ngay: xoa exe + de bien bao, khong de ai bam duoc nua.
  REM  Dau ngoac trong echo PHAI thoat bang ^ khi nam trong khoi if ^(...^), khong thi no dong
  REM  khoi som va batch bao "- was unexpected at this time".
  echo    ^>^> dist\%APP% dang bi KHOA ^(ban cu dang chay?^) - build sang dist_new
  call :vo_hieu_hoa
  set "OUTDIR=dist_new"
  if exist "dist_new\%APP%" rmdir /s /q "dist_new\%APP%" >nul 2>&1
)

echo [3/5] Build vao !OUTDIR!\%APP% ...
REM  --onedir : khoi dong ~2s, it bi antivirus bao dong (KHONG dung --onefile)
REM  --windowed: khong console -> BAT BUOC co nhanh --selftest de doc loi
REM  --add-data: bundle CA .py cua pipeline vi exe TU GOI LAI CHINH NO (--child) chay script con
REM  --hidden-import: module chi duoc import DONG (importlib) nen PyInstaller khong thay
REM  --collect-submodules yt_dlp: yt_dlp nap extractor DONG qua danh sach lazy; thieu co nay thi
REM     ban frozen bao "no suitable extractor" du import yt_dlp thanh cong.
REM  KHONG chen dong REM giua cac dong noi ^ ben duoi - batch se truyen "REM ..." thanh tham so.
pyinstaller --noconfirm --clean --onedir --windowed --name "%APP%" ^
  --distpath "!OUTDIR!" ^
  --icon "assets\youtube-logo.ico" ^
  --add-data "assets\youtube-logo.png;assets" ^
  --add-data "assets\tick-white.png;assets" ^
  --paths "." ^
  --add-data "make_video.py;." ^
  --add-data "ai_steps.py;." ^
  --add-data "qc_script.py;." ^
  --add-data "qc_visual.py;." ^
  --add-data "qc_audio.py;." ^
  --add-data "srt_from_script.py;." ^
  --add-data "qc_character.py;." ^
  --add-data "storyboard.py;." ^
  --add-data "pace_audio.py;." ^
  --add-data "profiles.py;." ^
  --add-data "paths.py;." ^
  --add-data "keys.py;." ^
  --add-data "selftest_extra.py;." ^
  --add-data "channel_scan.py;." ^
  --add-data "detect_voice.py;." ^
  --add-data "llm_client.py;." ^
  --add-data "voice_bank.py;." ^
  --add-data "calibrate.py;." ^
  --add-data "new_profile.py;." ^
  --add-data "tts.py;." ^
  --add-data "openspeaker_tts.py;." ^
  --add-data "fetch_script.py;." ^
  --add-data "gen_images.py;." ^
  --add-data "gpti2_gen.py;." ^
  --add-data "gpti2_edit.py;." ^
  --add-data "grok_gen.py;." ^
  --add-data "assemble.py;." ^
  --add-data "thumbnail_text.py;." ^
  --add-data "profiles;profiles" ^
  --add-data "..\skills;skills" ^
  --add-data "..\assets\voice_bank.json;assets" ^
  --hidden-import make_video --hidden-import ai_steps --hidden-import qc_script ^
  --hidden-import paths --hidden-import qc_visual --hidden-import qc_character ^
  --hidden-import storyboard --hidden-import pace_audio --hidden-import profiles ^
  --hidden-import llm_client --hidden-import voice_bank --hidden-import calibrate ^
  --hidden-import new_profile --hidden-import tts --hidden-import openspeaker_tts ^
  --hidden-import fetch_script --hidden-import gen_images --hidden-import gpti2_gen ^
  --hidden-import gpti2_edit --hidden-import grok_gen --hidden-import assemble ^
  --hidden-import thumbnail_text --hidden-import keys --hidden-import selftest_extra ^
  --hidden-import channel_scan --hidden-import detect_voice ^
  --hidden-import youtube_comment_downloader --hidden-import youtube_comment_downloader.downloader ^
  --collect-data imageio_ffmpeg ^
  --collect-submodules yt_dlp ^
  --add-data "models;models" ^
  --collect-all faster_whisper ^
  --collect-binaries ctranslate2 ^
  --collect-binaries onnxruntime ^
  --hidden-import faster_whisper --hidden-import ctranslate2 --hidden-import onnxruntime ^
  --hidden-import av --hidden-import tokenizers ^
  --exclude-module tkinter --exclude-module matplotlib --exclude-module scipy ^
  --exclude-module pandas --exclude-module notebook --exclude-module IPython ^
  --exclude-module torch ^
  --exclude-module numba --exclude-module llvmlite --exclude-module pyarrow ^
  --exclude-module datasets --exclude-module transformers --exclude-module onnxruntime.transformers ^
  --exclude-module PySide6.QtWebEngineCore --exclude-module PySide6.Qt3DCore ^
  --exclude-module PySide6.QtCharts --exclude-module PySide6.QtQuick3D ^
  gui_video.py
if errorlevel 1 goto :fail

echo [4/5] Cat DLL GPU khong dung + chep file de CANH exe cho user sua duoc
REM  Tool chay whisper o device="cpu" nen KHONG dung mot DLL GPU nao. PyInstaller keo ve rat nhieu:
REM  do that lan dau (2026-09-09) la 1.009 MB rieng 3 file toan hoc CUDA o goc _internal
REM  (cublasLt64_12 638MB + cufft64_11 274MB + cublas64_12 98MB) cong 306MB provider CUDA cua
REM  onnxruntime -> thu muc gui di phong len 1,8 GB. Cat het con ~600 MB.
REM  PyInstaller KHONG co co bo mot DLL le (--exclude-module chi an voi module Python) nen phai
REM  xoa sau khi build. Cat xong PHAI chay lai phep thu nghe that (buoc 5) keo cat lo ma khong biet.
set "GPUDLL=cublasLt64_12.dll cufft64_11.dll cublas64_12.dll cudnn64_9.dll cudart64_12.dll"
set "GPUDLL=!GPUDLL! cudnn_ops64_9.dll cudnn_cnn64_9.dll cudnn_adv64_9.dll nvrtc64_120_0.dll"
set "GPUDLL=!GPUDLL! onnxruntime_providers_cuda.dll onnxruntime_providers_tensorrt.dll"
for %%D in (!GPUDLL!) do (
  for %%P in ("_internal" "_internal\onnxruntime\capi" "_internal\ctranslate2") do (
    if exist "!OUTDIR!\%APP%\%%~P\%%D" (
      del /f /q "!OUTDIR!\%APP%\%%~P\%%D" >nul 2>&1
      echo    ^>^> da cat %%D
    )
  )
)

REM  keys.json CANH exe = cach doi API key o may khac ma KHONG build lai.
REM  Uu tien ban that (keys.json) neu co; khong thi phat ban mau da dien san key hien tai.
if exist keys.json (
  copy /y keys.json "!OUTDIR!\%APP%\keys.json" >nul
) else (
  if exist keys.sample.json copy /y keys.sample.json "!OUTDIR!\%APP%\keys.json" >nul
)
> "!OUTDIR!\%APP%\DOC-TRUOC.txt" (
  echo YOUTUBE CLONE-GEMINI - huong dan nhanh
  echo.
  echo 1^) Mo "Youtube Clone-Gemini.exe"
  echo 2^) Tab 1 "Quet kenh - chay hang loat" - dung tab nay la du:
  echo      - Nhap ten kenh doi thu ^(vd simbot2^) hoac dan URL kenh, bam QUET VIDEO
  echo      - Bang hien ra: ten video, so view, thoi luong, o tich chon
  echo      - Tich cac video muon lam ^(hoac bam Tich tat ca^), sua ten tap neu can
  echo      - Bat "Nhan nguoi ke theo tung video" neu kenh co nhieu nguoi ke khac nhau
  echo        ^(tool doc loi video goc -^> viet dung ngoi ke + ve dung mat + chon dung giong^)
  echo      - Bam "Chay cac video DA TICH" hoac "Chay TAT CA video"
  echo    Chay lan luot tung video. Tap nao loi thi bo tap do, lam tiep tap sau.
  echo 3^) Tab 2 "Lam 1 video": khi chi muon lam dung 1 video da biet id.
  echo 4^) Tab 3 "Lap kenh moi": ta nhan vat bang tieng Viet -^> tool tu chon giong,
  echo    dung ho so, va DO char-rate that. Bam "Tao profile tu kenh nay" o Tab 1
  echo    la dien san ID kenh vao day.
  echo.
  echo Neu exe khong mo duoc: chay lenh sau roi doc selftest.log cung thu muc
  echo    "Youtube Clone-Gemini.exe" --selftest
  echo Doi API key: sua keys.json trong thu muc nay, KHONG can build lai.
  echo.
  echo LUU Y: buoc bong transcript can mang; buoc tao anh TON TIEN that.
  echo Tool tu dung o buoc nao khong dat QC de khong tieu tien oan.
  echo Video xuat ra nam o: assets\satori_jp\^<ten tap^>\final.mp4
)

echo [5/5] Kiem tra ban vua build (selftest)
"!OUTDIR!\%APP%\%APP%.exe" --selftest
if exist "!OUTDIR!\%APP%\selftest.log" (
  echo ---------- selftest.log ----------
  type "!OUTDIR!\%APP%\selftest.log"
  echo.
  echo ----------------------------------
) else (
  echo ^>^> KHONG thay selftest.log - exe co the chet ngay khi khoi dong.
)

echo [5b/5] Kiem key + module front-end + NGHE THAT bang whisper trong exe
"!OUTDIR!\%APP%\%APP%.exe" --child selftest_extra.py
if exist "_selftest_audio.mp3" (
  "!OUTDIR!\%APP%\%APP%.exe" --child selftest_extra.py --audio "_selftest_audio.mp3"
) else (
  echo    ^>^> khong co _selftest_audio.mp3 canh build_exe.bat - BO QUA phep thu nghe that.
  echo    ^>^> Nen tao: ffmpeg -ss 30 -t 12 -i ^<voice.mp3 bat ky^> _selftest_audio.mp3
)

echo.
if /i "!OUTDIR!"=="dist_new" (
  echo ****************************************************************************
  echo  CHU Y: ban cu dang chay nen phai build sang dist_new.
  echo  DUNG ban o:  dist_new\%APP%\%APP%.exe
  echo  Thu muc dist\%APP% chi con vo rong - da xoa exe trong do de khong bam nham.
  echo ****************************************************************************
)
echo XONG. Thu muc gui di: !OUTDIR!\%APP%\
for /f %%S in ('powershell -nop -c "[math]::Round((Get-ChildItem '!OUTDIR!\%APP%' -Recurse -File ^| Measure-Object Length -Sum).Sum/1MB)"') do echo Dung luong: %%S MB
goto :eof

:vo_hieu_hoa
REM  Vo hieu hoa cai VO RONG con lai o dist khi khong xoa duoc: bo file exe di + de bien bao.
REM  Khong lam thi no van "bam duoc" va bao "Failed to load Python DLL python313.dll"
REM  (user da bam nham that 2026-09-09). Viet bang nhieu dong echo >> chu KHONG dung khoi
REM  ngoac long trong `if (...)` - batch bao "- was unexpected at this time".
del /f /q "dist\%APP%\%APP%.exe" >nul 2>&1
set "BB=dist\%APP%\HONG-DUNG-DUNG.txt"
echo THU MUC NAY HONG - DUNG CHAY.> "%BB%"
echo.>> "%BB%"
echo Luc build, ban cu dang chay nen khong xoa duoc, chi con lai cai vo rong.>> "%BB%"
echo File exe trong day da bi go bo de khong ai bam nham.>> "%BB%"
echo.>> "%BB%"
echo Ban dung duoc nam o:  dist_new\%APP%\%APP%.exe>> "%BB%"
echo Dong het cua so tool roi build lai la thu muc nay tu bien mat.>> "%BB%"
goto :eof

:fail
echo.
echo ^>^> BUILD LOI. Doc log PyInstaller ben tren.
exit /b 1
