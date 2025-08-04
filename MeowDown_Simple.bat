@echo off
title MeowDown - Simple Launcher
echo.
echo Starting MeowDown...
echo.
echo This will open in your browser at: http://localhost:8501
echo.
echo To stop MeowDown, close this window or press Ctrl+C
echo.

REM Navigate to the script directory
cd /d "%~dp0"

REM Run streamlit directly
python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

echo.
echo MeowDown stopped.
pause