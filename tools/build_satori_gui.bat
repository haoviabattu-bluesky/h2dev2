@echo off
REM Build "H2Dev Render.exe" (PySide6 --onedir --windowed). GUI mong: goi py-3.13 pipeline ben ngoai.
cd /d "%~dp0"
taskkill /F /IM "H2Dev Render.exe" >nul 2>&1
timeout /t 1 >nul

py -3.13 -m PyInstaller --onedir --windowed --name "H2Dev Render" ^
  --exclude-module PySide6.QtNetwork --exclude-module PySide6.QtQml --exclude-module PySide6.QtQuick ^
  --exclude-module PySide6.QtWebEngineCore --exclude-module PySide6.QtWebEngineWidgets ^
  --exclude-module PySide6.QtMultimedia --exclude-module PySide6.QtMultimediaWidgets ^
  --exclude-module PySide6.QtCharts --exclude-module PySide6.QtPdf --exclude-module PySide6.QtPdfWidgets ^
  --exclude-module PySide6.Qt3DCore --exclude-module PySide6.QtDataVisualization ^
  --exclude-module PySide6.QtPositioning --exclude-module PySide6.QtBluetooth ^
  --exclude-module PySide6.QtSerialPort --exclude-module PySide6.QtSql ^
  --exclude-module numpy --exclude-module matplotlib --exclude-module tkinter --exclude-module scipy ^
  --noconfirm --clean satori_render_gui.py

REM config.json phai NAM CANH exe (BASE=dirname(exe)), khong bundle vao _internal
copy /Y satori_gui_config.json "dist\H2Dev Render\satori_gui_config.json"
echo === BUILD XONG: dist\H2Dev Render\H2Dev Render.exe ===
