@echo off
title MeowDown Setup & Launch 🐱💕

echo.
echo     🐱💕 MeowDown - Pink Edition Setup 🌸
echo     =====================================
echo.
echo     Get ready for the CUTEST video downloader ever!
echo     🌸 Pink dreamy background
echo     🐱 Floating cats celebration  
echo     💕 Meow sound effects
echo     ✨ Maximum adorableness activated!
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo     😿 Python not found! Please install Python 3.8+ first.
    echo     Download from: https://python.org
    echo.
    pause
    exit /b 1
)

echo     🐱 Installing Python packages...
echo     This may take a few minutes on first run.
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install core packages
python -m pip install streamlit
python -m pip install yt-dlp
python -m pip install requests

echo.
echo     🐱 Checking installation...

REM Test imports
python -c "import streamlit; print('✅ Streamlit OK')"
python -c "import yt_dlp; print('✅ yt-dlp OK')" 
python -c "import requests; print('✅ requests OK')"

echo.
echo     🐱 Launching MeowDown web interface...
echo     🌐 This will open in your browser at http://localhost:8501
echo.

REM Run the app
streamlit run app.py --server.port 8501 --browser.gatherUsageStats false --theme.base light --theme.primaryColor "#667eea"

echo.
echo     Thanks for using MeowDown! 🐱
pause