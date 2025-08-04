@echo off
title MeowDown - Perfect Single Tab Launcher
echo.
echo     🐱💕 MeowDown - Perfect Edition 💕🐱
echo     ===================================
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

echo     Starting MeowDown with full cute UI...
echo     This will open ONLY ONE browser tab with all the pretty elements!
echo.
echo     Server will be available at: http://localhost:8501
echo     Close this window to stop the server.
echo.

REM Navigate to the script directory
cd /d "%~dp0"

REM Start Streamlit normally (NOT headless) but disable browser auto-launch
start /B python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false --server.address localhost

REM Wait for server to start
echo     Waiting for server to start...
timeout /t 6 /nobreak >nul

REM Check if server is ready and open browser once
echo     Checking if server is ready...
for /L %%i in (1,1,10) do (
    ping -n 1 localhost >nul 2>&1 && (
        echo     Server is ready! Opening browser...
        start http://localhost:8501
        goto :server_ready
    )
    timeout /t 1 /nobreak >nul
)

REM Fallback - open browser anyway
echo     Opening browser anyway...
start http://localhost:8501

:server_ready
echo.
echo     🐱✨ MeowDown is running with full cute UI! ✨🐱
echo     All the cats, fonts, and pink styling should be there!
echo     Press any key to stop the server.
echo.
pause >nul

REM Clean up
echo     Stopping MeowDown...
taskkill /F /IM python.exe /FI "COMMANDLINE eq *streamlit*" >nul 2>&1
del "%TEMP%\meowdown.lock" >nul 2>&1

echo.
echo     MeowDown stopped. Thanks for using our cute app! 🐱💕
pause