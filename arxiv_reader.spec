# arxiv_reader.spec
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from pathlib import Path

block_cipher = None

hiddenimports = []
hiddenimports += collect_submodules("streamlit")
hiddenimports += collect_submodules("scrapy")
hiddenimports += collect_submodules("lxml")
hiddenimports += collect_submodules("requests")
hiddenimports += ["streamlit.web.bootstrap"]

datas = []
datas += [("ui_arxiv_reader.py", ".")]
datas += [("arxiv_scraper", "arxiv_scraper")]
datas += [("runs", "runs")]
datas += [("assets", "assets")]

a = Analysis(
    ["desktop_app.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    a.binaries,
    a.datas,
    [],
    name="arxiv_reader",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # no console window
    #icon=str(Path("assets") / "arxiv_reader.ico"),
    icon=None,
)
