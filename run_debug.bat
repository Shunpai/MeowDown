@echo off
title MeowDown Debug Console 🐱🔧

echo.
echo     🐱🔧 MeowDown Debug Mode 🔧🐱
echo     ===============================
echo.
echo     Debug messages will appear below!
echo     Browser will open to: http://localhost:8501
echo.
echo     Try the test buttons to see debug output!
echo.

streamlit run app_debug.py --server.port 8501 --browser.gatherUsageStats false

echo.
echo     Thanks for testing MeowDown! 🐱
pause