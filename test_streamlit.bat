@echo off
title MeowDown Test 🐱

echo.
echo     🐱 Testing MeowDown Components...
echo     ================================
echo.

REM Test Python imports
echo     Testing Python imports...
python -c "import streamlit; print('✅ Streamlit: OK')" || echo "❌ Streamlit: FAILED"
python -c "import yt_dlp; print('✅ yt-dlp: OK')" || echo "❌ yt-dlp: FAILED" 
python -c "import requests; print('✅ requests: OK')" || echo "❌ requests: FAILED"
python -c "import app; print('✅ app.py: OK')" || echo "❌ app.py: FAILED"

echo.
echo     🐱 All tests completed!
echo     If you see any FAILED messages above, run setup_and_run.bat first.
echo.
pause