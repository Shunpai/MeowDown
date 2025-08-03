@echo off
title MeowDown with Debug Output 🐱

echo.
echo     🐱 MeowDown - Debug Mode 🔧
echo     ============================
echo.
echo     This will show debug messages in this window
echo     while the app runs in your browser!
echo.
echo     🌐 Browser will open to: http://localhost:8501
echo     📋 Debug messages will appear here
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo     😿 Python not found! Please install Python first.
    pause
    exit /b 1
)

echo     🐱 Starting MeowDown with debug output...
echo.

REM Run with python directly so we can see print statements
python -c "
import subprocess
import sys
import os

print('🚀 Launching Streamlit...')
os.environ['PYTHONIOENCODING'] = 'utf-8'
subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.port', '8501', '--browser.gatherUsageStats', 'false'])
"

echo.
echo     Thanks for using MeowDown! 🐱
pause