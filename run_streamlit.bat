@echo off
title MeowDown - Cute Video Downloader 🐱

echo.
echo     🐱 MeowDown - Streamlit Edition 🐾
echo     ==================================
echo.
echo     Starting the web interface...
echo     This will open in your browser! 🌐
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo     😿 Python not found! Please install Python first.
    echo     Download from: https://python.org
    pause
    exit /b 1
)

REM Install essential dependencies
echo     🐱 Installing essential dependencies...
pip install --upgrade pip
pip install streamlit yt-dlp requests

REM Check if streamlit was installed successfully
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo     😿 Failed to install Streamlit! Trying alternative method...
    pip install --user streamlit yt-dlp requests
)

REM Run the app
echo     🐱 Launching MeowDown...
echo     🌐 Opening http://localhost:8501 in your browser...
echo.
streamlit run app.py --server.port 8501 --browser.gatherUsageStats false --theme.base light --theme.primaryColor "#667eea"

echo.
echo     Thanks for using MeowDown! 🐱
pause