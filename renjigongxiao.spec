# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['renjigongxiao.py',
    'Ui_renjigongxiao.py',
    'memory_pic.py',
    'testredata.py',
    'MatplotlibWidget.py',
    'pic2py.py',
    'pic_rc.py',
    'globalvar.py'
    ],
    pathex=['D:\\testpyqt5\\renjigongxiao'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='renjigongxiao',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='renjigongxiao',
)
