# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['tkinter']
hiddenimports += collect_submodules('gmaps')


a = Analysis(
    ['src/gmaps/gmaps_gui_main.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/cemkarahan/Library/Caches/pypoetry/virtualenvs/gmaps-scraper-*/lib/python3.10/site-packages/dateparser/data', 'dateparser/data')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='gmaps_gui',
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
    name='gmaps_gui',
)
app = BUNDLE(
    coll,
    name='gmaps_gui.app',
    icon=None,
    bundle_identifier='com.cemkarahan.gmaps',
)
