@echo off
chcp 65001 >nul
title MeowDown - Single Tab Edition

echo.
echo     MeowDown - Single Tab Edition
echo     ============================
echo.
echo     Get ready for the CUTEST video downloader ever!
echo     Pink dreamy background
echo     Floating cats celebration  
echo     Meow sound effects
echo     Maximum adorableness activated!
echo     Single tab protection enabled!
echo.

REM Clean up any old lock files first
del "%TEMP%\meowdown.lock" >nul 2>&1

REM Check if already running by checking for streamlit process
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *streamlit*" 2>nul | find /I "python.exe" >nul
if %ERRORLEVEL%==0 (
    echo     MeowDown may already be running!
    echo     Check your browser for http://localhost:8501
    echo     If not working, close any Python/Streamlit processes first.
    echo.
    pause
    exit /b
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo     Python not found! Please install Python 3.8+ first.
    echo     Download from: https://python.org
    echo.
    pause
    exit /b 1
)

echo     Checking Python packages...
echo.

REM Quick check if packages are installed
python -c "import streamlit, yt_dlp, requests" >nul 2>&1
if errorlevel 1 (
    echo     Installing missing packages...
    python -m pip install streamlit yt-dlp requests
)

echo.
echo     Launching MeowDown web interface...
echo     This will open in your browser at http://localhost:8501
echo     Only ONE tab will open!
echo.

REM Navigate to the script directory
cd /d "%~dp0"

REM Run the app with EXACT same parameters as setup_and_run.bat
streamlit run app.py --server.port 8501 --browser.gatherUsageStats false --theme.base light --theme.primaryColor "#667eea"

echo.
echo     Thanks for using MeowDown!
pause