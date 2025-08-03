#!/usr/bin/env python3
"""
MeowDown Build Script 🐱
Creates a standalone executable with all dependencies bundled.
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
VERSION = "2.0.0"
MAIN_SCRIPT = "main.py"

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
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
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
            "dearpygui>=1.10.0",
            "yt-dlp>=2023.12.30", 
            "pyperclip>=1.8.2",
            "requests>=2.31.0",
            "pyinstaller>=6.0.0"
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
                
                # Find ffmpeg.exe in extracted files
                for root, dirs, files in os.walk(temp_path):
                    if "ffmpeg.exe" in files:
                        src_path = Path(root) / "ffmpeg.exe"
                        shutil.copy2(src_path, ffmpeg_exe)
                        break
            else:
                # For Linux/Mac, we'd need different extraction logic
                print_error("Linux/Mac FFmpeg extraction not implemented yet")
                return False
            
            if ffmpeg_exe.exists():
                print_success("FFmpeg downloaded successfully!")
                return True
            else:
                print_error("Failed to extract FFmpeg")
                return False
                
    except Exception as e:
        print_error(f"Failed to download FFmpeg: {e}")
        return False

def create_spec_file():
    """Create PyInstaller spec file with proper configuration."""
    print_cat("Creating PyInstaller spec file...")
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Include all necessary data files
added_files = [
    ('bin', 'bin'),  # Include FFmpeg binary
]

a = Analysis(
    ['{MAIN_SCRIPT}'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'dearpygui.dearpygui',
        'yt_dlp',
        'requests',
        'pyperclip',
        'urllib3',
        'certifi',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
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
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
'''
    
    with open(f"{APP_NAME}.spec", "w") as f:
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
    spec_file = f"{APP_NAME}.spec"
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
    
    dist_name = f"{APP_NAME}-v{VERSION}-{platform.system().lower()}"
    dist_dir = Path("dist") / dist_name
    dist_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_name = f"{APP_NAME}.exe" if platform.system() == "Windows" else APP_NAME
    exe_src = Path("dist") / exe_name
    exe_dst = dist_dir / exe_name
    
    if exe_src.exists():
        shutil.copy2(exe_src, exe_dst)
    
    # Create README for distribution
    readme_content = f"""
# {APP_NAME} v{VERSION} 🐱

A cute video downloader with a cat theme!

## Features
- Download videos from YouTube and other platforms
- Convert to MP3 or keep as MP4
- Cute cat-themed interface
- Auto-installs dependencies (yt-dlp, FFmpeg)
- Easy-to-use GUI

## How to Use
1. Run {exe_name}
2. Paste a video URL
3. Choose your download folder
4. Select format (MP4 video or MP3 audio)
5. Click "Download Meow!" 
6. Wait for the cute progress messages! 🐾

## System Requirements
- Windows 10/11 (64-bit)
- Internet connection for downloads

## Support
If you find any bugs or have suggestions, please create an issue!

Made with ❤️ and lots of purrs 🐾
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
    print_cat(f"Building {APP_NAME} v{VERSION} 🐾")
    print_cat(f"Platform: {platform.system()} {platform.machine()}")
    print_cat("=" * 50)
    
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
        
        # Step 3: Create spec file
        create_spec_file()
        
        # Step 4: Build executable
        if not build_executable():
            print_error("Failed to build executable")
            sys.exit(1)
        
        # Step 5: Create distribution
        zip_path = create_distribution()
        
        print_cat("=" * 50)
        print_success("Build completed successfully! 🎉")
        print_cat(f"Your cute MeowDown executable is ready!")
        print_cat(f"Distribution package: {zip_path}")
        print_cat("Share the purr-fect video downloader! 🐾")
        
    except KeyboardInterrupt:
        print_cat("Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()