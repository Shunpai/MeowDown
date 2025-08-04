@echo off
title MeowDown - Single Tab Edition 🐱💕

echo.
echo     🐱💕 MeowDown - Single Tab Edition 🌸
echo     ====================================
echo.
echo     Get ready for the CUTEST video downloader ever!
echo     🌸 Pink dreamy background
echo     🐱 Floating cats celebration  
echo     💕 Meow sound effects
echo     ✨ Maximum adorableness activated!
echo     🔒 Single tab protection enabled!
echo.

REM Check if already running
if exist "%TEMP%\meowdown.lock" (
    echo     🐱 MeowDown is already running!
    echo     Check your browser for the existing window.
    echo     Close the other instance first if you want to restart.
    echo.
    pause
    exit /b
)

REM Create lock file
echo running > "%TEMP%\meowdown.lock"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo     😿 Python not found! Please install Python 3.8+ first.
    echo     Download from: https://python.org
    echo.
    del "%TEMP%\meowdown.lock" >nul 2>&1
    pause
    exit /b 1
)

echo     🐱 Checking Python packages...
echo.

REM Quick check if packages are installed (simplified)
python -c "import streamlit, yt_dlp, requests" >nul 2>&1
if errorlevel 1 (
    echo     Installing missing packages...
    python -m pip install streamlit yt-dlp requests
)

echo.
echo     🐱 Launching MeowDown web interface...
echo     🌐 This will open in your browser at http://localhost:8501
echo     🔒 Only ONE tab will open!
echo.

REM Navigate to the script directory
cd /d "%~dp0"

REM Run the app with EXACT same parameters as setup_and_run.bat
streamlit run app.py --server.port 8501 --browser.gatherUsageStats false --theme.base light --theme.primaryColor "#667eea"

echo.
echo     Thanks for using MeowDown! 🐱

REM Clean up lock file
del "%TEMP%\meowdown.lock" >nul 2>&1

pause