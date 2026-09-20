# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['satori_render_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PySide6.QtNetwork', 'PySide6.QtQml', 'PySide6.QtQuick', 'PySide6.QtWebEngineCore', 'PySide6.QtWebEngineWidgets', 'PySide6.QtMultimedia', 'PySide6.QtMultimediaWidgets', 'PySide6.QtCharts', 'PySide6.QtPdf', 'PySide6.QtPdfWidgets', 'PySide6.Qt3DCore', 'PySide6.QtDataVisualization', 'PySide6.QtPositioning', 'PySide6.QtBluetooth', 'PySide6.QtSerialPort', 'PySide6.QtSql', 'numpy', 'matplotlib', 'tkinter', 'scipy'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Satori Render',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Satori Render',
)
