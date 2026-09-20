# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all

datas = [('assets\\youtube-logo.png', 'assets'), ('assets\\tick-white.png', 'assets'), ('make_video.py', '.'), ('ai_steps.py', '.'), ('qc_script.py', '.'), ('qc_visual.py', '.'), ('qc_audio.py', '.'), ('srt_from_script.py', '.'), ('qc_character.py', '.'), ('storyboard.py', '.'), ('pace_audio.py', '.'), ('profiles.py', '.'), ('paths.py', '.'), ('keys.py', '.'), ('selftest_extra.py', '.'), ('channel_scan.py', '.'), ('detect_voice.py', '.'), ('llm_client.py', '.'), ('voice_bank.py', '.'), ('calibrate.py', '.'), ('new_profile.py', '.'), ('tts.py', '.'), ('openspeaker_tts.py', '.'), ('fetch_script.py', '.'), ('gen_images.py', '.'), ('gpti2_gen.py', '.'), ('gpti2_edit.py', '.'), ('grok_gen.py', '.'), ('assemble.py', '.'), ('thumbnail_text.py', '.'), ('profiles', 'profiles'), ('..\\skills', 'skills'), ('..\\assets\\voice_bank.json', 'assets'), ('models', 'models')]
binaries = []
hiddenimports = ['make_video', 'ai_steps', 'qc_script', 'paths', 'qc_visual', 'qc_character', 'storyboard', 'pace_audio', 'profiles', 'llm_client', 'voice_bank', 'calibrate', 'new_profile', 'tts', 'openspeaker_tts', 'fetch_script', 'gen_images', 'gpti2_gen', 'gpti2_edit', 'grok_gen', 'assemble', 'thumbnail_text', 'keys', 'selftest_extra', 'channel_scan', 'detect_voice', 'youtube_comment_downloader', 'youtube_comment_downloader.downloader', 'faster_whisper', 'ctranslate2', 'onnxruntime', 'av', 'tokenizers']
datas += collect_data_files('imageio_ffmpeg')
binaries += collect_dynamic_libs('ctranslate2')
binaries += collect_dynamic_libs('onnxruntime')
hiddenimports += collect_submodules('yt_dlp')
tmp_ret = collect_all('faster_whisper')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['gui_video.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'scipy', 'pandas', 'notebook', 'IPython', 'torch', 'numba', 'llvmlite', 'pyarrow', 'datasets', 'transformers', 'onnxruntime.transformers', 'PySide6.QtWebEngineCore', 'PySide6.Qt3DCore', 'PySide6.QtCharts', 'PySide6.QtQuick3D'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Youtube Clone-Gemini',
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
    icon=['assets\\youtube-logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Youtube Clone-Gemini',
)
