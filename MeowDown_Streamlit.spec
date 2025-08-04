# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Streamlit and other data files
added_files = [
    ('bin', 'bin'),  # Include FFmpeg binary
    ('app.py', '.'),  # Include main app script
]

# Get streamlit path
import streamlit
streamlit_path = streamlit.__path__[0]

a = Analysis(
    ['run_meowdown.py'],
    pathex=[],
    binaries=[],
    datas=added_files + [
        (streamlit_path + "/static", "./streamlit/static"),
        (streamlit_path + "/runtime", "./streamlit/runtime"),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.runtime.state',
        'streamlit.components.v1.components',
        'yt_dlp',
        'requests',
        'urllib3',
        'certifi',
        'stqdm',
        'extra_streamlit_components',
        'streamlit_option_menu',
        'streamlit_lottie',
        'altair',
        'plotly',
        'pandas',
        'numpy',
        'PIL',
        'toml',
        'validators',
        'multiprocessing',
        'multiprocessing.pool',
        'multiprocessing.spawn',
        'watchdog',
        'tornado',
        'packaging',
        'importlib_metadata',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'sklearn',
        'tensorflow',
        'torch',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MeowDown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console for now to see any errors
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
