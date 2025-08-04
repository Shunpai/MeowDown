@echo off
title MeowDown - Fixed Single Tab Launcher
echo.
echo     🐱 MeowDown - Single Tab Fix 🐱
echo     ================================
echo.

REM Check if already running
if exist "%TEMP%\meowdown.lock" (
    echo     MeowDown is already running!
    echo     Check your browser for the existing window.
    echo.
    pause
    exit /b
)

REM Create lock file
echo running > "%TEMP%\meowdown.lock"

echo     Starting MeowDown...
echo     This will open ONLY ONE browser tab.
echo.
echo     Server will be available at: http://localhost:8501
echo     Close this window to stop the server.
echo.

REM Navigate to the script directory
cd /d "%~dp0"

REM Start Streamlit in the background without auto-opening browser
start /B python -m streamlit run app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false

REM Wait for server to start
echo     Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Open browser once
echo     Opening browser...
start http://localhost:8501

echo.
echo     🐱 MeowDown is running!
echo     Press any key to stop the server.
echo.
pause >nul

REM Clean up
taskkill /F /IM python.exe /FI "WINDOWTITLE eq streamlit*" >nul 2>&1
del "%TEMP%\meowdown.lock" >nul 2>&1

echo.
echo     MeowDown stopped. Goodbye! 🐱
pause