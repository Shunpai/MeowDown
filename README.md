# 🐱 MeowDown v3.0.0 - Streamlit Edition

A beautiful web-based video downloader with the cutest cat theme ever! Download videos from YouTube, TikTok, and 1000+ other platforms through a stunning, responsive web interface.

![MeowDown Interface](https://via.placeholder.com/800x500/667eea/FFFFFF?text=🐱+MeowDown+Web+Interface)

## ✨ Features

- 🌐 **Modern Web Interface**: Beautiful, responsive design that works in any browser
- 🎬 **Video Downloads**: Download from YouTube, TikTok, and 1000+ other sites
- 🎵 **Audio Extraction**: Convert videos to MP3 format with high quality
- 🐾 **Cute Cat Theme**: Adorable animations, emojis, and purr-fect messages
- 🎨 **Gradient Animations**: Stunning visual effects and smooth transitions
- 🔧 **Auto-Setup**: Automatically downloads and configures FFmpeg and yt-dlp
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- 📊 **Real-time Progress**: Live progress bars with cute status updates
- 🖥️ **Standalone Executable**: Runs as a web app without installation
- 💜 **Beautiful Themes**: Gradient colors and modern card-based layout

## 🚀 Quick Start

### Option 1: Web App (Easiest) 🌐
```bash
# Windows - Double click
run_streamlit.bat

# Or manually
pip install streamlit yt-dlp requests
streamlit run app.py
```
Then open `http://localhost:8501` in your browser!

### Option 2: Download Pre-built Executable
1. Download the latest release from the [Releases](../../releases) page
2. Extract the zip file
3. Run `MeowDown.exe` - it will open in your browser!
4. Paste a video URL and click "Download Meow!" 🐱

### Option 3: Build from Source
```bash
# Clone the repository
git clone https://github.com/yourusername/MeowDown.git
cd MeowDown

# Quick build (Windows)
build_streamlit.bat

# Or manually:
python build_streamlit.py
```

## 🛠️ Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

# Or use the old DearPyGUI version
python main.py
```

## 📦 Building Executable

### Streamlit Edition (Recommended) 🌐
```bash
# Windows
build_streamlit.bat

# Or cross-platform
python build_streamlit.py
```

### Classic Desktop Edition
```bash
# Windows
build.bat

# Or cross-platform
python build.py
```

Both will:
- Install all Python dependencies
- Download FFmpeg automatically
- Create a PyInstaller spec file
- Build the standalone executable
- Package everything into a distribution zip

### Manual Build
```bash
# Install dependencies
pip install -r requirements.txt

# Build Streamlit version
python build_streamlit.py

# Or build classic version
python build.py
```

## 🎯 Supported Platforms

- ✅ **Windows 10/11** (64-bit) - Fully supported
- ✅ **Web Browser** - Works on any modern browser
- 🔄 **macOS** - Coming soon
- 🔄 **Linux** - Coming soon

## 📋 Dependencies

### Python Dependencies (Auto-installed)
- `streamlit` - Modern web framework for the UI
- `yt-dlp` - Video downloading engine
- `requests` - HTTP requests
- `stqdm` - Progress bars for Streamlit
- `extra-streamlit-components` - Additional UI components
- `pyinstaller` - Executable building

### External Dependencies (Auto-downloaded)
- `FFmpeg` - Video/audio processing

## 🎨 Interface Preview

The beautiful web interface includes:
- 🌐 **Modern Design**: Gradient animations and card-based layout
- 🔗 **Smart URL Input**: Auto-validation with helpful hints
- 📁 **Easy Folder Selection**: Choose download location with one click
- 🎭 **Format Selection**: Beautiful MP4/MP3 selector with icons
- 📊 **Live Progress**: Real-time progress bars with cute messages
- 🎉 **Celebration Effects**: Balloons and success animations
- 📱 **Responsive**: Perfect on any screen size
- 🐾 **Cat Stats**: System info and cute cat status indicators

## 🐱 Cat Messages

MeowDown includes adorable cat-themed status messages:
- "🐱 Starting download... *excited purr*"
- "😸 Making progress... 45.2% *happy meow*"  
- "🎉 Download complete! *victory purr* 🎉"
- "😻 Found video! *excited purr*"

## 🔧 Technical Details

### Architecture
- **Web Interface**: Streamlit for modern, responsive web UI
- **Classic GUI**: DearPyGUI for desktop application (legacy)
- **Download Engine**: yt-dlp (successor to youtube-dl)
- **Video Processing**: FFmpeg for format conversion
- **Build System**: PyInstaller for standalone executables

### File Structure
```
MeowDown/
├── app.py                 # Streamlit web application (NEW!)
├── main.py                # Classic DearPyGUI application
├── build_streamlit.py     # Streamlit build script
├── build.py               # Classic build script
├── run_streamlit.bat      # Windows launcher for web app
├── build_streamlit.bat    # Windows build helper for web app
├── requirements.txt       # Python dependencies
├── bin/                   # FFmpeg binaries (auto-created)
├── dist/                  # Built executables
└── README.md              # This file
```

## 🚨 Security & Safety

MeowDown is designed for **defensive/legitimate use only**:
- Downloads videos for personal use, education, or backup
- Respects website terms of service
- Does not bypass DRM or circumvent protections
- Open source for transparency

**Please respect content creators' rights and platform terms of service.**

## 🐛 Troubleshooting

### Common Issues

**"Web page won't load"**
- Make sure you're going to `http://localhost:8501`
- Try refreshing the page or restarting the app
- Check if another app is using port 8501

**"FFmpeg not found"**
- The app should auto-download FFmpeg on first run
- If it fails, manually download FFmpeg and place in `bin/` folder

**"yt-dlp not found"** 
- Run: `pip install yt-dlp`
- Or let the app auto-install on first download

**Download fails**
- Check your internet connection
- Verify the URL is correct and public
- Some videos may be region-locked or private

**Build fails**
- Ensure Python 3.8+ is installed
- Try: `pip install --upgrade pip setuptools wheel`
- Run `python build_streamlit.py` with admin privileges if needed

**Streamlit issues**
- Update Streamlit: `pip install --upgrade streamlit`
- Clear browser cache and refresh
- Try a different browser

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **yt-dlp team** - Amazing video downloading library
- **Streamlit team** - Beautiful and modern web framework
- **DearPyGUI team** - Fast GUI framework (classic version)  
- **FFmpeg team** - Powerful multimedia processing
- **Cat emoji creators** - For making everything cuter! 🐾

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](../../issues)
- 💡 **Feature Requests**: [GitHub Discussions](../../discussions)
- 📧 **Contact**: Create an issue for any questions

---

Made with ❤️ and lots of purrs 🐾

*Remember: Always respect content creators and platform terms of service!*