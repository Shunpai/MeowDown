#!/usr/bin/env python3
"""
🐱 MeowDown Streamlit Build Script
Creates a standalone executable for the Streamlit version.
"""

import os
import sys
import subprocess
import shutil
import tempfile
import zipfile
import requests
from pathlib import Path
import platform

# Build configuration
APP_NAME = "MeowDown"
VERSION = "3.0.0"
MAIN_SCRIPT = "app.py"

def print_cat(message):
    """Print with cute cat emoji."""
    print(f"🐱 {message}")

def print_error(message):
    """Print error with sad cat."""
    print(f"😿 ERROR: {message}")

def print_success(message):
    """Print success with happy cat."""
    print(f"😸 SUCCESS: {message}")

def run_command(cmd, check=True):
    """Run a command and return the result."""
    print_cat(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def install_dependencies():
    """Install all required dependencies."""
    print_cat("Installing Python dependencies...")
    
    # Upgrade pip first
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install requirements
    if Path("requirements.txt").exists():
        run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        # Install individual packages if requirements.txt doesn't exist
        packages = [
            "streamlit>=1.28.0",
            "yt-dlp>=2023.12.30", 
            "requests>=2.31.0",
            "pyinstaller>=6.0.0",
            "stqdm>=0.0.5",
            "streamlit-option-menu>=0.3.6",
            "streamlit-lottie>=0.0.5",
            "extra-streamlit-components>=0.1.60"
        ]
        for package in packages:
            run_command([sys.executable, "-m", "pip", "install", package])

def download_ffmpeg():
    """Download FFmpeg binary for the current platform."""
    print_cat("Downloading FFmpeg...")
    
    system = platform.system()
    ffmpeg_urls = {
        "Windows": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
        "Darwin": "https://evermeet.cx/ffmpeg/getrelease/zip",
        "Linux": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
    }
    
    if system not in ffmpeg_urls:
        print_error(f"Unsupported platform: {system}")
        return False
    
    # Create bin directory
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)
    
    ffmpeg_exe = bin_dir / ("ffmpeg.exe" if system == "Windows" else "ffmpeg")
    
    if ffmpeg_exe.exists():
        print_cat("FFmpeg already exists, skipping download")
        return True
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            archive_path = temp_path / "ffmpeg_archive"
            
            print_cat("Downloading FFmpeg archive...")
            response = requests.get(ffmpeg_urls[system], stream=True)
            response.raise_for_status()
            
            with open(archive_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print_cat("Extracting FFmpeg...")
            
            if system == "Windows":
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                
                for root, dirs, files in os.walk(temp_path):
                    if "ffmpeg.exe" in files:
                        src_path = Path(root) / "ffmpeg.exe"
                        shutil.copy2(src_path, ffmpeg_exe)
                        break
            
            if ffmpeg_exe.exists():
                print_success("FFmpeg downloaded successfully!")
                return True
            else:
                print_error("Failed to extract FFmpeg")
                return False
                
    except Exception as e:
        print_error(f"Failed to download FFmpeg: {e}")
        return False

def create_launcher_script():
    """Create a launcher script for the Streamlit app."""
    print_cat("Creating launcher script...")
    
    launcher_content = f'''#!/usr/bin/env python3
"""
MeowDown Launcher
Launches the Streamlit app with proper configuration.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Streamlit app."""
    # Get the directory where this script is located
    app_dir = Path(__file__).parent
    app_script = app_dir / "app.py"
    
    if not app_script.exists():
        print("😿 Error: app.py not found!")
        input("Press Enter to exit...")
        return
    
    # Launch Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", str(app_script),
        "--server.port", "8501",
        "--server.address", "localhost",
        "--browser.serverAddress", "localhost",
        "--browser.gatherUsageStats", "false",
        "--theme.base", "light",
        "--theme.primaryColor", "#667eea",
        "--theme.backgroundColor", "#ffffff",
        "--theme.secondaryBackgroundColor", "#f0f2f6"
    ]
    
    try:
        print("🐱 Starting MeowDown...")
        print("🌐 Opening in your browser...")
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\\n🐱 MeowDown stopped. Goodbye!")
    except Exception as e:
        print(f"😿 Error starting MeowDown: {{e}}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''
    
    with open("run_meowdown.py", "w", encoding='utf-8') as f:
        f.write(launcher_content)
    
    print_success("Launcher script created!")

def create_spec_file():
    """Create PyInstaller spec file for Streamlit app."""
    print_cat("Creating PyInstaller spec file...")
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Streamlit and other data files
added_files = [
    ('bin', 'bin'),  # Include FFmpeg binary
]

# Get streamlit path
import streamlit
streamlit_path = streamlit.__path__[0]

a = Analysis(
    ['run_meowdown.py'],
    pathex=[],
    binaries=[],
    datas=added_files + [
        (streamlit_path + "/static", "./streamlit/static"),
        (streamlit_path + "/runtime", "./streamlit/runtime"),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.runtime.state',
        'streamlit.components.v1.components',
        'yt_dlp',
        'requests',
        'urllib3',
        'certifi',
        'stqdm',
        'extra_streamlit_components',
        'streamlit_option_menu',
        'streamlit_lottie',
        'altair',
        'plotly',
        'pandas',
        'numpy',
        'PIL',
        'toml',
        'validators',
        'watchdog',
        'tornado',
        'packaging',
        'importlib_metadata',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'sklearn',
        'tensorflow',
        'torch',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console for now to see any errors
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
'''
    
    with open(f"{APP_NAME}_Streamlit.spec", "w", encoding='utf-8') as f:
        f.write(spec_content)
    
    print_success("Spec file created!")

def build_executable():
    """Build the executable using PyInstaller."""
    print_cat("Building executable with PyInstaller...")
    
    # Clean previous builds
    for dir_name in ["build", "dist"]:
        if Path(dir_name).exists():
            print_cat(f"Cleaning {dir_name} directory...")
            shutil.rmtree(dir_name)
    
    # Build using spec file
    spec_file = f"{APP_NAME}_Streamlit.spec"
    run_command([sys.executable, "-m", "PyInstaller", "--clean", spec_file])
    
    # Check if build succeeded
    exe_name = f"{APP_NAME}.exe" if platform.system() == "Windows" else APP_NAME
    exe_path = Path("dist") / exe_name
    
    if exe_path.exists():
        print_success(f"Executable created: {exe_path}")
        print_cat(f"File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        return True
    else:
        print_error("Executable not found after build")
        return False

def create_distribution():
    """Create a distribution package."""
    print_cat("Creating distribution package...")
    
    dist_name = f"{APP_NAME}-Streamlit-v{VERSION}-{platform.system().lower()}"
    dist_dir = Path("dist") / dist_name
    dist_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_name = f"{APP_NAME}.exe" if platform.system() == "Windows" else APP_NAME
    exe_src = Path("dist") / exe_name
    exe_dst = dist_dir / exe_name
    
    if exe_src.exists():
        shutil.copy2(exe_src, exe_dst)
    
    # Copy app.py for reference
    if Path("app.py").exists():
        shutil.copy2("app.py", dist_dir / "app.py")
    
    # Create README for distribution
    readme_content = f"""
# 🐱 {APP_NAME} v{VERSION} - Streamlit Edition

A beautiful web-based video downloader with a cute cat theme!

## ✨ Features
- 🌐 **Modern Web Interface** - Beautiful, responsive design
- 🎬 **Video Downloads** - YouTube, TikTok, and 1000+ sites
- 🎵 **Audio Extraction** - Convert to MP3 format
- 🐾 **Cute Cat Theme** - Adorable interface with animations
- 🔧 **Auto-Setup** - Automatically downloads FFmpeg and yt-dlp
- 📱 **Responsive** - Works great on any screen size

## 🚀 How to Use

### Option 1: Run the Executable (Easiest)
1. Double-click `{exe_name}`
2. Wait for the web interface to open in your browser
3. Paste a video URL and click "Download Meow!"

### Option 2: Run with Python
```bash
# Install dependencies
pip install streamlit yt-dlp requests

# Run the app
streamlit run app.py
```

## 🌐 Web Interface
The app runs as a web application in your browser at `http://localhost:8501`

## 📋 System Requirements
- Windows 10/11 (64-bit)
- Internet connection for downloads
- Modern web browser

## 🎨 Features
- Gradient animations
- Real-time progress tracking
- Cute cat emojis and messages
- Beautiful color scheme
- Responsive design
- Auto-dependency management

## 🐛 Troubleshooting
- If the web page doesn't open automatically, go to `http://localhost:8501`
- If downloads fail, check your internet connection
- The app may take a moment to start on first run (downloading dependencies)

## 📞 Support
Create an issue on GitHub if you encounter any problems!

---
Made with ❤️ and lots of purrs 🐾

*Always respect content creators and platform terms of service!*
"""
    
    with open(dist_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Create zip archive
    zip_path = Path("dist") / f"{dist_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dist_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(dist_dir.parent)
                zipf.write(file_path, arcname)
    
    print_success(f"Distribution package created: {zip_path}")
    return zip_path

def main():
    """Main build process."""
    print_cat(f"Building {APP_NAME} v{VERSION} - Streamlit Edition 🐾")
    print_cat(f"Platform: {platform.system()} {platform.machine()}")
    print_cat("=" * 60)
    
    if not Path(MAIN_SCRIPT).exists():
        print_error(f"Main script {MAIN_SCRIPT} not found!")
        sys.exit(1)
    
    try:
        # Step 1: Install dependencies
        install_dependencies()
        
        # Step 2: Download FFmpeg
        if not download_ffmpeg():
            print_error("Failed to setup FFmpeg")
            sys.exit(1)
        
        # Step 3: Create launcher script
        create_launcher_script()
        
        # Step 4: Create spec file
        create_spec_file()
        
        # Step 5: Build executable
        if not build_executable():
            print_error("Failed to build executable")
            sys.exit(1)
        
        # Step 6: Create distribution
        zip_path = create_distribution()
        
        print_cat("=" * 60)
        print_success("Build completed successfully! 🎉")
        print_cat(f"Your beautiful MeowDown Streamlit app is ready!")
        print_cat(f"Distribution package: {zip_path}")
        print_cat("The app will open in your web browser when you run it! 🌐")
        print_cat("Share the purr-fect video downloader! 🐾")
        
    except KeyboardInterrupt:
        print_cat("Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()