@echo off
echo 🐱 MeowDown Streamlit Builder 🐾
echo.
echo This will build MeowDown Streamlit Edition into a standalone executable!
echo The result will be a beautiful web-based app that runs in your browser.
echo.
echo Make sure you have Python installed.
echo.
pause

echo 🐱 Starting build process...
python build_streamlit.py

echo.
echo 🐱 Build complete! Check the dist folder for your executable.
echo When you run it, it will open a web interface in your browser! 🌐
pause