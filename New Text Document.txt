@echo off
setlocal

echo ===============================
echo   arXiv Reader - Launcher
echo ===============================
echo.

REM --- Check Python ---
where python >nul 2>&1
if errorlevel 1 (
    echo Python not found.
    echo Trying to install Python via winget...
    echo.

    where winget >nul 2>&1
    if errorlevel 1 (
        echo ERROR: winget not available.
        echo Please install Python manually from https://python.org
        pause
        exit /b 1
    )

    winget install -e --id Python.Python.3 --source winget
    if errorlevel 1 (
        echo ERROR: Python installation failed.
        pause
        exit /b 1
    )

    echo Python installed. Please RESTART this script.
    pause
    exit /b 0
)

REM --- Check pip ---
where pip >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip not found.
    pause
    exit /b 1
)

REM --- Install dependencies once ---
if not exist ".deps_installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
    echo ok > .deps_installed
)

echo.
echo Launching arXiv Reader...
echo.

python -m streamlit run ui_arxiv_reader.py ^
  --server.headless=false ^
  --browser.gatherUsageStats=false

pause
endlocal
