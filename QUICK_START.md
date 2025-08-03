# 🐱 MeowDown Quick Start Guide

## 🚀 Super Easy Setup (Windows)

### Step 1: First Time Setup
Double-click: **`setup_and_run.bat`**

This will:
- Install all required Python packages
- Launch MeowDown in your browser
- Open at `http://localhost:8501`

### Step 2: Next Time (After Setup)
Double-click: **`run_streamlit.bat`**

Or manually run:
```bash
streamlit run app.py
```

## 🐛 If Something Goes Wrong

### Error: "stqdm not found" or similar import errors
**Solution**: Run `setup_and_run.bat` - it installs all dependencies

### Error: "Python not found"
**Solution**: Install Python 3.8+ from https://python.org

### Error: "Web page won't load"
**Solutions**:
1. Make sure you go to: `http://localhost:8501`
2. Wait 30 seconds for startup
3. Try refreshing the page
4. Check if another app is using port 8501

### Error: "pip install failed"
**Solutions**:
1. Run as Administrator
2. Try: `python -m pip install --user streamlit yt-dlp requests`
3. Update pip: `python -m pip install --upgrade pip`

## 🎯 What You'll See

When working correctly, you'll see:
- A beautiful gradient-animated title: "🐱 MeowDown"
- URL input box with placeholder text
- Format selector (MP4/MP3)
- Download folder selection
- Cute cat statistics cards
- Purple-themed interface with rounded corners

## 🐱 Features

- **Smart URL Detection**: Paste any video URL
- **Format Selection**: Choose MP4 (video) or MP3 (audio)
- **Progress Tracking**: Real-time progress with cat messages
- **Auto-Setup**: Downloads FFmpeg and yt-dlp automatically
- **Celebration**: Balloons when download completes!

## 📁 File Structure

```
MeowDown/
├── app.py                 # Main Streamlit app
├── setup_and_run.bat      # First-time setup & launch
├── run_streamlit.bat      # Quick launcher
├── test_streamlit.bat     # Test components
└── requirements.txt       # Python dependencies
```

## 🎉 Enjoy Your Cute Video Downloader!

Made with ❤️ and lots of purrs 🐾