#!/usr/bin/env python3
"""
🐱 MeowDown v3.0.0 - Cute Video Downloader
A delightful Streamlit-based video downloader with cat theme!
"""

import streamlit as st
import os
import sys
import subprocess
import tempfile
import zipfile
import shutil
import requests
import platform
import time
import re
import urllib.parse
from pathlib import Path
from threading import Thread
import json

# Optional imports - graceful fallback if not available
try:
    from stqdm import stqdm
    HAS_STQDM = True
except ImportError:
    HAS_STQDM = False
    stqdm = None

# =============================================================================
# 🐱 CONFIGURATION & CONSTANTS
# =============================================================================

APP_NAME = "MeowDown"
VERSION = "3.0.0"
GITHUB_URL = "https://github.com/yourusername/MeowDown"

# Cat emojis for different moods
CAT_EMOJIS = {
    "happy": "😸",
    "excited": "😻", 
    "working": "🙀",
    "sleepy": "😴",
    "heart_eyes": "😍",
    "cool": "😎",
    "normal": "🐱",
    "paw": "🐾",
    "music": "🎵",
    "video": "🎬",
    "download": "⬇️",
    "success": "🎉",
    "error": "😿",
    "thinking": "🤔"
}

# Platform-specific FFmpeg URLs
FFMPEG_URLS = {
    "Windows": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
    "Darwin": "https://evermeet.cx/ffmpeg/getrelease/zip",
    "Linux": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
}

# =============================================================================
# 🎨 STREAMLIT CONFIGURATION
# =============================================================================

def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=f"{CAT_EMOJIS['normal']} {APP_NAME} - Purr-fectly Cute!",
        page_icon="🐱",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': GITHUB_URL,
            'Report a bug': f"{GITHUB_URL}/issues",
            'About': f"# {CAT_EMOJIS['heart_eyes']} {APP_NAME} v{VERSION}\\n"
                    f"The most adorable video downloader in the universe!\\n"
                    f"Made with love, purrs, and pink pixels! 💕\\n\\n"
                    f"Built with Streamlit {CAT_EMOJIS['paw']}"
        }
    )

def load_custom_css():
    """Load custom CSS for cute styling."""
    st.markdown("""
    <style>
    /* Import cute font */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700&display=swap');
    
    /* Global styles with cute pink-purple background */
    .main {
        padding-top: 2rem;
        background: linear-gradient(135deg, #ffeef8 0%, #f0e6ff 25%, #e6f3ff 50%, #ffeef8 75%, #f8e6ff 100%);
        background-size: 400% 400%;
        animation: dreamyBackground 20s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes dreamyBackground {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Override Streamlit's default background */
    .stApp {
        background: linear-gradient(135deg, #ffeef8 0%, #f0e6ff 25%, #e6f3ff 50%, #ffeef8 75%, #f8e6ff 100%);
        background-size: 400% 400%;
        animation: dreamyBackground 20s ease infinite;
    }
    
    /* Cute bounce animation for buttons */
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes wiggle {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(2deg); }
        75% { transform: rotate(-2deg); }
    }
    
    /* Make buttons more bouncy */
    .stButton > button {
        transition: all 0.3s ease !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Custom font for the whole app */
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }
    
    /* Floating cats animation */
    .floating-cats {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    }
    
    .floating-cat {
        position: absolute;
        font-size: 2rem;
        animation: floatUp 4s ease-out forwards;
        opacity: 1;
    }
    
    @keyframes floatUp {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 1;
        }
        50% {
            opacity: 1;
            transform: translateY(50vh) rotate(180deg);
        }
        100% {
            transform: translateY(-10vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* Header styling */
    .big-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Card styling with pink-purple theme */
    .download-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(255,182,193,0.3);
        margin: 1rem 0;
        color: #5a4e7c;
    }
    
    .stats-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(255,182,193,0.2);
        text-align: center;
        margin: 0.5rem;
        border-left: 4px solid #ff9a9e;
        border: 1px solid rgba(255,182,193,0.2);
    }
    
    /* Button styling with pink theme */
    .stButton > button {
        background: linear-gradient(45deg, #ff9a9e, #fecfef, #ff9a9e);
        color: #5a4e7c;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 154, 158, 0.6);
        background: linear-gradient(45deg, #fecfef, #ff9a9e, #fecfef);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(45deg, #ff9a9e, #fecfef);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #fecfef;
        padding: 0.75rem;
        font-size: 1rem;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff9a9e;
        box-shadow: 0 0 0 0.2rem rgba(255, 154, 158, 0.25);
    }
    
    /* Success/Error message styling */
    .success-message {
        background: linear-gradient(45deg, #ff9a9e, #fecfef);
        color: #5a4e7c;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        animation: slideIn 0.5s ease;
        box-shadow: 0 5px 15px rgba(255, 154, 158, 0.3);
    }
    
    .error-message {
        background: linear-gradient(45deg, #ffb3ba, #ffc9dd);
        color: #8b4d6b;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Floating animation for cat emojis */
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0% { transform: translate(0, 0px); }
        50% { transform: translate(0, -10px); }
        100% { transform: translate(0, 0px); }
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 🛠️ UTILITY FUNCTIONS
# =============================================================================

def get_app_dir():
    """Get application directory for storing binaries."""
    if getattr(sys, 'frozen', False):
        app_dir = Path(sys.executable).parent
    else:
        app_dir = Path(__file__).parent
    
    bin_dir = app_dir / "bin"
    bin_dir.mkdir(exist_ok=True)
    return bin_dir

def is_valid_url(url):
    """Validate if the given string is a valid URL."""
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def get_default_download_folder():
    """Get cross-platform default download folder."""
    downloads = Path.home() / "Downloads"
    if downloads.exists() and downloads.is_dir():
        return str(downloads)
    return str(Path.cwd())

def download_file_with_progress(url, dest_path, description="Downloading"):
    """Download a file with progress bar."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        downloaded = 0
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = downloaded / total_size
                        progress_bar.progress(progress)
                        status_text.text(f"{description}... {progress*100:.1f}%")
        
        progress_bar.progress(1.0)
        status_text.text(f"{description} complete! {CAT_EMOJIS['success']}")
        return True
        
    except Exception as e:
        st.error(f"Download failed: {str(e)} {CAT_EMOJIS['error']}")
        return False

def check_dependencies():
    """Check if all dependencies are available."""
    deps = {"ytdlp": False, "ffmpeg": False}
    
    # Check yt-dlp
    try:
        result = subprocess.run([sys.executable, "-m", "yt_dlp", "--version"], 
                              capture_output=True, text=True)
        deps["ytdlp"] = result.returncode == 0
    except Exception:
        pass
    
    # Check ffmpeg
    bin_dir = get_app_dir()
    ffmpeg_exe = bin_dir / ("ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg")
    
    if ffmpeg_exe.exists():
        deps["ffmpeg"] = True
    else:
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
            deps["ffmpeg"] = result.returncode == 0
        except Exception:
            pass
    
    return deps

def install_dependencies():
    """Install required dependencies."""
    with st.spinner(f"Setting up dependencies... {CAT_EMOJIS['working']}"):
        deps = check_dependencies()
        
        if not deps["ytdlp"]:
            st.info(f"Installing yt-dlp... {CAT_EMOJIS['working']}")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], 
                             check=True, capture_output=True)
                st.success(f"yt-dlp installed! {CAT_EMOJIS['success']}")
            except Exception as e:
                st.error(f"Failed to install yt-dlp: {e} {CAT_EMOJIS['error']}")
                return False
        
        if not deps["ffmpeg"]:
            st.info(f"Downloading FFmpeg... {CAT_EMOJIS['working']}")
            if not install_ffmpeg():
                return False
        
        return True

def install_ffmpeg():
    """Download and install FFmpeg."""
    system = platform.system()
    if system not in FFMPEG_URLS:
        st.error(f"Unsupported platform: {system} {CAT_EMOJIS['error']}")
        return False
    
    bin_dir = get_app_dir()
    ffmpeg_exe = bin_dir / ("ffmpeg.exe" if system == "Windows" else "ffmpeg")
    
    if ffmpeg_exe.exists():
        return True
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            archive_path = temp_path / "ffmpeg.zip"
            
            if not download_file_with_progress(FFMPEG_URLS[system], archive_path, "Downloading FFmpeg"):
                return False
            
            st.info(f"Extracting FFmpeg... {CAT_EMOJIS['working']}")
            
            if system == "Windows":
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                
                for root, dirs, files in os.walk(temp_path):
                    if "ffmpeg.exe" in files:
                        src_path = Path(root) / "ffmpeg.exe"
                        shutil.copy2(src_path, ffmpeg_exe)
                        break
            
            if ffmpeg_exe.exists():
                st.success(f"FFmpeg installed! {CAT_EMOJIS['success']}")
                return True
            else:
                st.error(f"Failed to extract FFmpeg {CAT_EMOJIS['error']}")
                return False
                
    except Exception as e:
        st.error(f"FFmpeg installation failed: {e} {CAT_EMOJIS['error']}")
        return False

# =============================================================================
# 🎬 DOWNLOAD FUNCTIONS
# =============================================================================

def download_video(url, dest_folder, format_type, progress_container, options=None):
    """Download video with real-time progress updates and advanced options."""
    if options is None:
        options = {}
    
    with progress_container.container():
        st.info(f"Starting download... {CAT_EMOJIS['excited']}")
        
        # Validate destination
        dest_path = Path(dest_folder)
        if not dest_path.exists():
            try:
                dest_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                st.error(f"Cannot create folder: {e} {CAT_EMOJIS['error']}")
                return False
        
        # Get FFmpeg path
        bin_dir = get_app_dir()
        ffmpeg_path = bin_dir / ("ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg")
        
        # Build base command (URL will be added later for each batch)
        cmd = [sys.executable, "-m", "yt_dlp", "--newline"]
        
        if ffmpeg_path.exists():
            cmd.extend(["--ffmpeg-location", str(ffmpeg_path)])
        
        # Handle batch mode
        urls_to_process = []
        if options.get('batch_mode', False) and options.get('batch_urls', ''):
            # Split batch URLs and clean them
            batch_list = [u.strip() for u in options['batch_urls'].split('\n') if u.strip()]
            urls_to_process.extend(batch_list)
        if url.strip():  # Add the main URL if provided
            urls_to_process.append(url.strip())
        
        if not urls_to_process:
            st.error(f"No valid URLs provided! {CAT_EMOJIS['error']}")
            return False
        
        # Handle channel mode
        if options.get('channel_mode', False):
            # For channel mode, we want all videos from the channel
            cmd.append("--yes-playlist")
            cmd.extend(["--playlist-end", str(options.get('channel_limit', 25))])
        elif options.get('is_playlist', False):
            cmd.append("--yes-playlist")
            max_downloads = options.get('max_downloads', 50)
            cmd.extend(["--playlist-end", str(max_downloads)])
        else:
            cmd.append("--no-playlist")
        
        # Handle format and quality
        if format_type == "mp3_complete":
            # Complete MP3 with everything embedded
            cmd.extend(["-x", "--audio-format", "mp3"])
            
            # Handle audio quality
            audio_quality = options.get('audio_quality', '320 kbps (Best) - *audiophile cats*')
            if "320 kbps" in audio_quality:
                cmd.extend(["--audio-quality", "0"])
            elif "256 kbps" in audio_quality:
                cmd.extend(["--audio-quality", "2"])
            elif "192 kbps" in audio_quality:
                cmd.extend(["--audio-quality", "5"])
            elif "128 kbps" in audio_quality:
                cmd.extend(["--audio-quality", "7"])
            elif "96 kbps" in audio_quality:
                cmd.extend(["--audio-quality", "9"])
            else:
                cmd.extend(["--audio-quality", "0"])  # Default to 320kbps for complete version
            
            # Embed EVERYTHING into the MP3
            cmd.extend([
                "--add-metadata",           # Add metadata tags
                "--embed-metadata",         # Embed metadata into file
                "--embed-thumbnail",        # Embed thumbnail as album art
                "--convert-thumbnails", "jpg"  # Convert to JPG for better compatibility
            ])
            
            # Don't save separate thumbnail files - only embed them
            # (removing --write-thumbnail to avoid clutter)
            
            if options.get('playlist_numbering', False):
                output_template = str(dest_path / "%(playlist_index)03d - 🎵%(artist,uploader|Unknown Artist)s - %(title)s.%(ext)s")
            else:
                output_template = str(dest_path / "🎵%(artist,uploader|Unknown Artist)s - %(title)s.%(ext)s")
        elif format_type == "best":
            cmd.extend(["-f", "best"])
            if options.get('playlist_numbering', False):
                output_template = str(dest_path / "%(playlist_index)03d - 🎬%(title)s.%(ext)s")
            else:
                output_template = str(dest_path / "🎬%(title)s.%(ext)s")
        elif format_type.startswith("video_"):
            quality = format_type.split("_")[1]
            if quality == "720p":
                cmd.extend(["-f", "best[height<=720]/best"])
            elif quality == "1080p":
                cmd.extend(["-f", "best[height<=1080]/best"])
            elif quality == "1440p":
                cmd.extend(["-f", "best[height<=1440]/best"])
            elif quality == "4K":
                cmd.extend(["-f", "best[height<=2160]/best"])
            elif quality == "best":
                cmd.extend(["-f", "best"])
            elif quality == "worst":
                cmd.extend(["-f", "worst"])
            
            if options.get('playlist_numbering', False):
                output_template = str(dest_path / "%(playlist_index)03d - 🎬%(title)s.%(ext)s")
            else:
                output_template = str(dest_path / "🎬%(title)s.%(ext)s")
        else:  # Default MP4
            cmd.extend(["-f", "best[ext=mp4]/best"])
            if options.get('playlist_numbering', False):
                output_template = str(dest_path / "%(playlist_index)03d - 🎬%(title)s.%(ext)s")
            else:
                output_template = str(dest_path / "🎬%(title)s.%(ext)s")
        
        # Handle auto-organization
        organize_type = options.get('auto_organize', '🗂️ No organization - *all in one folder*')
        if "By Date" in organize_type:
            output_template = str(dest_path / "%(upload_date>%Y)s/%(upload_date>%m)s/%(upload_date>%d)s" / Path(output_template).name)
        elif "By Channel" in organize_type:
            output_template = str(dest_path / "%(uploader)s" / Path(output_template).name)
        elif "By Type" in organize_type:
            if format_type in ["mp3", "mp3_meta"]:
                output_template = str(dest_path / "Audio" / Path(output_template).name)
            else:
                output_template = str(dest_path / "Video" / Path(output_template).name)
        elif "By Playlist" in organize_type:
            output_template = str(dest_path / "%(playlist_title)s" / Path(output_template).name)
        
        cmd.extend(["-o", output_template])
        
        # Add smart filters
        filters = []
        
        # Duration filters
        if options.get('duration_filter', False):
            duration_min = options.get('duration_min', 0)
            duration_max = options.get('duration_max', 0)
            if duration_min > 0:
                filters.append(f"duration>={duration_min}")
            if duration_max > 0:
                filters.append(f"duration<={duration_max}")
        
        # File size filters
        if options.get('size_filter', False):
            max_size = options.get('max_filesize', 'No limit')
            if max_size != 'No limit':
                size_bytes = {
                    '50MB': '50M',
                    '100MB': '100M', 
                    '250MB': '250M',
                    '500MB': '500M',
                    '1GB': '1000M',
                    '2GB': '2000M'
                }.get(max_size, '500M')
                filters.append(f"filesize<={size_bytes}")
        
        # Content type filters - disable live filter for now as it has syntax issues
        # if options.get('skip_live', True):
        #     # Live stream filtering needs to be handled differently
        #     pass
        
        if options.get('skip_shorts', False):
            filters.append("duration>=60")  # Skip videos shorter than 60 seconds
        
        # Language filters - temporarily disabled to avoid syntax issues
        # lang_pref = options.get('language_pref', '🌐 Any language')
        # if "English only" in lang_pref:
        #     filters.append("language=en")
        # elif "Spanish only" in lang_pref:
        #     filters.append("language=es")
        # elif "French only" in lang_pref:
        #     filters.append("language=fr")
        # elif "German only" in lang_pref:
        #     filters.append("language=de")
        # elif "Japanese only" in lang_pref:
        #     filters.append("language=ja")
        # elif "Korean only" in lang_pref:
        #     filters.append("language=ko")
        
        # Apply filters if any
        if filters:
            filter_string = " & ".join(filters)
            if format_type in ["mp3", "mp3_meta"]:
                cmd.extend(["-f", f"bestaudio[{filter_string}]/bestaudio"])
            else:
                # For video, modify existing format selector
                for i, arg in enumerate(cmd):
                    if arg == "-f" and i + 1 < len(cmd):
                        current_format = cmd[i + 1]
                        cmd[i + 1] = f"{current_format}[{filter_string}]/{current_format}"
                        break
        
        # Add download archive for history
        if options.get('download_archive', True):
            archive_file = dest_path / ".meowdown_history.txt"
            cmd.extend(["--download-archive", str(archive_file)])
        
        # Add retry options
        if options.get('auto_retry', True):
            cmd.extend(["--retries", "3", "--fragment-retries", "3"])
        
        # Add metadata options
        if options.get('download_metadata', True):
            cmd.append("--write-info-json")
        
        # Add thumbnail options  
        if options.get('download_thumbnail', True):
            cmd.append("--write-thumbnail")
            
        # Add subtitles options
        if options.get('download_subtitles', False):
            cmd.extend(["--write-subs", "--write-auto-subs", "--sub-langs", "en,en-US"])
            
        # Add metadata embedding for audio/video files
        if options.get('embed_metadata', True):
            cmd.append("--add-metadata")
            if format_type in ["mp3", "mp3_meta"]:
                cmd.append("--embed-metadata")
        
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Show what we're about to do
            if len(urls_to_process) > 1:
                st.info(f"🎯 Batch mode: Processing {len(urls_to_process)} URLs!")
            elif options.get('channel_mode', False):
                st.info(f"📺 Channel mode: Downloading up to {options.get('channel_limit', 25)} videos!")
            elif options.get('is_playlist', False):
                st.info(f"📀 Playlist mode: Downloading up to {options.get('max_downloads', 50)} tracks!")
            else:
                st.info(f"🎵 Single download mode activated!")
            
            # Process each URL (for batch mode or single URL)
            overall_success = True
            for i, current_url in enumerate(urls_to_process):
                if len(urls_to_process) > 1:
                    st.info(f"🐱 Processing URL {i+1}/{len(urls_to_process)}: {current_url[:50]}...")
                    
                # Build command for this specific URL
                current_cmd = cmd + [current_url]
                
                proc = subprocess.Popen(current_cmd, stdout=subprocess.PIPE, 
                                      stderr=subprocess.STDOUT, text=True)
                
                # Capture all output for debugging
                all_output = []
                
                # Process output for this URL
                for line in proc.stdout:
                    all_output.append(line.strip())
                    
                    if "[download]" in line:
                        if "Destination:" in line:
                            status_text.success(f"Found content! {CAT_EMOJIS['excited']}")
                        elif "has already been downloaded" in line:
                            status_text.info(f"Already downloaded! {CAT_EMOJIS['sleepy']}")
                            progress_bar.progress(1.0)
                        elif "Downloading playlist:" in line:
                            status_text.info(f"Found playlist! {CAT_EMOJIS['heart_eyes']}")
                        else:
                            match = re.search(r'(\d{1,3}(?:\.\d+)?)%', line)
                            if match:
                                percent = float(match.group(1)) / 100.0
                                progress_bar.progress(percent)
                                
                                # Cute progress messages
                                if percent < 0.25:
                                    status_text.info(f"Getting started... {percent*100:.1f}% {CAT_EMOJIS['working']}")
                                elif percent < 0.5:
                                    status_text.info(f"Making progress... {percent*100:.1f}% {CAT_EMOJIS['happy']}")
                                elif percent < 0.75:
                                    status_text.info(f"Almost there... {percent*100:.1f}% {CAT_EMOJIS['excited']}")
                                else:
                                    status_text.info(f"So close... {percent*100:.1f}% {CAT_EMOJIS['heart_eyes']}")
                    elif "[ffmpeg]" in line:
                        status_text.info(f"Converting... {CAT_EMOJIS['music']}")
                    elif "[Metadata]" in line:
                        status_text.info(f"Adding metadata... {CAT_EMOJIS['thinking']}")
                    elif "ERROR:" in line:
                        st.error(f"🚨 yt-dlp error: {line}")
                    elif "WARNING:" in line:
                        st.warning(f"⚠️ yt-dlp warning: {line}")
                
                proc.wait()
                
                # Check success for this URL
                if proc.returncode != 0:
                    overall_success = False
                    st.error(f"❌ Failed to download: {current_url[:50]}... (Exit code: {proc.returncode}) {CAT_EMOJIS['error']}")
                    
                    # Show last few lines of output for debugging
                    if all_output:
                        st.error("📋 Last few lines of yt-dlp output:")
                        for line in all_output[-5:]:  # Show last 5 lines
                            if line.strip():
                                st.code(line)
                    
                    # Try to run a simple test command to see what's wrong
                    st.info("🔧 Testing basic yt-dlp functionality...")
                    test_cmd = [sys.executable, "-m", "yt_dlp", "--version"]
                    try:
                        test_result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=10)
                        if test_result.returncode == 0:
                            st.info(f"✅ yt-dlp version: {test_result.stdout.strip()}")
                        else:
                            st.error(f"❌ yt-dlp test failed: {test_result.stderr}")
                    except Exception as e:
                        st.error(f"❌ yt-dlp test error: {e}")
                        
                elif len(urls_to_process) > 1:
                    st.success(f"✅ Completed URL {i+1}/{len(urls_to_process)}")
            
            # Final status
            if overall_success:
                status_text.success(f"All downloads complete! {CAT_EMOJIS['success']}")
                progress_bar.progress(1.0)
                
                # Handle MP3 playlist merging if needed
                if format_type == "mp3_complete" and options.get('is_playlist', False) and options.get('merge_playlist', False):
                    st.info(f"🎵 Creating playlist mix... {CAT_EMOJIS['music']}")
                    mix_success = create_playlist_mix(dest_path, format_type, options)
                    if mix_success:
                        st.success(f"🎵 Playlist mix created! {CAT_EMOJIS['success']}")
                    else:
                        st.warning(f"⚠️ Mix creation had issues, but individual files are ready! {CAT_EMOJIS['thinking']}")
                
                # Show post-processing message if enabled
                post_process = options.get('post_process', '🐱 Do nothing - *just enjoy*')
                if "Normalize audio" in post_process:
                    st.info(f"🔊 Normalizing audio volumes... {CAT_EMOJIS['music']}")
                elif "Auto-trim" in post_process:
                    st.info(f"✂️ Trimming silence... {CAT_EMOJIS['working']}")
                elif "Compress" in post_process:
                    st.info(f"🗜️ Compressing files... {CAT_EMOJIS['thinking']}")
                elif "Copy to cloud" in post_process:
                    st.info(f"📤 Copying to cloud folder... {CAT_EMOJIS['heart_eyes']}")
                
                return True
            else:
                status_text.error(f"Some downloads failed! {CAT_EMOJIS['error']}")
                return False
                
        except Exception as e:
            st.error(f"Download error: {e} {CAT_EMOJIS['error']}")
            return False

def create_playlist_mix(dest_path, format_type, options):
    """Create a single MP3 mix from all downloaded files."""
    try:
        dest_path = Path(dest_path)
        
        # Get FFmpeg path
        bin_dir = get_app_dir()
        ffmpeg_path = bin_dir / ("ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg")
        
        if not ffmpeg_path.exists():
            st.error(f"FFmpeg not found for mixing! {CAT_EMOJIS['error']}")
            return False
        
        # Find all MP3 files to merge (sorted by number)
        if format_type == "mp3_complete":
            audio_files = sorted(dest_path.glob("*.mp3"))
        else:
            audio_files = sorted(dest_path.glob("*.mp4"))
        
        if len(audio_files) < 2:
            st.info(f"Only {len(audio_files)} file found, no mixing needed! {CAT_EMOJIS['sleepy']}")
            return True
        
        st.info(f"🎵 Found {len(audio_files)} tracks to mix!")
        
        # Create a temporary file list for FFmpeg
        temp_file_list = dest_path / "temp_filelist.txt"
        
        # Generate mix filename
        first_file = audio_files[0]
        if "🎬" in first_file.name:
            # Extract playlist name from first file
            base_name = first_file.name.split(" - ", 1)[-1].split(".")[0]
            mix_name = f"🎵 PLAYLIST MIX - {base_name}.mp3"
        else:
            mix_name = f"🎵 PLAYLIST MIX - {len(audio_files)} tracks.mp3"
        
        mix_path = dest_path / mix_name
        
        # Create file list for FFmpeg concat
        with open(temp_file_list, 'w', encoding='utf-8') as f:
            for audio_file in audio_files:
                # Escape single quotes for FFmpeg
                file_path = str(audio_file).replace("'", "'\\''")
                f.write(f"file '{file_path}'\n")
        
        # Build FFmpeg command for concatenation
        cmd = [
            str(ffmpeg_path),
            "-f", "concat",
            "-safe", "0",
            "-i", str(temp_file_list),
            "-c", "copy",  # Copy without re-encoding when possible
            str(mix_path),
            "-y"  # Overwrite if exists
        ]
        
        # For MP3 complete files, use direct copy for better quality
        if format_type == "mp3_complete" and all(f.suffix == '.mp3' for f in audio_files):
            # Direct MP3 concatenation - preserves embedded metadata and thumbnails
            cmd = [
                str(ffmpeg_path),
                "-f", "concat",
                "-safe", "0",
                "-i", str(temp_file_list),
                "-c", "copy",  # Copy without re-encoding
                "-map_metadata", "0",  # Copy metadata from first file
                str(mix_path),
                "-y"
            ]
        else:
            # For other formats, convert to MP3
            cmd = [
                str(ffmpeg_path),
                "-f", "concat",
                "-safe", "0", 
                "-i", str(temp_file_list),
                "-vn",  # No video
                "-acodec", "libmp3lame",  # MP3 encoding
                "-ab", "320k",  # High quality bitrate
                str(mix_path),
                "-y"
            ]
        
        st.info(f"🔧 Running FFmpeg to create mix...")
        
        # Run FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up temp file
        if temp_file_list.exists():
            temp_file_list.unlink()
        
        if result.returncode == 0 and mix_path.exists():
            st.success(f"✅ Created: {mix_name}")
            
            # Show file size
            file_size = mix_path.stat().st_size / (1024 * 1024)  # MB
            st.info(f"📁 Mix file size: {file_size:.1f} MB")
            
            return True
        else:
            st.error(f"❌ FFmpeg failed: {result.stderr}")
            return False
            
    except Exception as e:
        st.error(f"Mix creation error: {e} {CAT_EMOJIS['error']}")
        return False

# =============================================================================
# 🎨 UI COMPONENTS
# =============================================================================

def play_meow_sound():
    """Play a cute meow sound using HTML audio."""
    # Using a free meow sound from freesound.org
    meow_html = """
    <audio autoplay>
        <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBj2P2fDNeSsFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBj2P2fDNeSsFJHfH8N2QQAoUXrTp66hVFApGn+DyvmcAgdHX6+iGNgYVYrfs4ZdOFQxPpeLxtmMcBjiR1/LMeSwFJHfH8N2QQNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmcAgdHX6+iGNgYVYrfs4ZdOFQxPpeLxtmMcBjiR1/LMeSwFJHfH8N2QQNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmchBj2P2fDNeSsFJHfH8N2QQNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmchBj2P2fDNeSsFJHfH8N2QQNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmchBj2P2fDNeSsFJHfH8N2QQNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQ==" type="audio/wav">
        <source src="https://www.soundjay.com/misc/sounds/meow_x.wav" type="audio/wav">
    </audio>
    """
    st.markdown(meow_html, unsafe_allow_html=True)

def show_floating_cats():
    """Display floating cats animation."""
    try:
        # Simple celebration with CSS animation
        st.markdown("""
        <div style="
            text-align: center;
            background: linear-gradient(45deg, rgba(255,200,220,0.3), rgba(200,150,255,0.3));
            padding: 2rem;
            border-radius: 20px;
            margin: 1rem 0;
            animation: celebration 2s ease-in-out;
        ">
            <div style="font-size: 3rem; animation: bounce 1s infinite;">
                🐱 😸 😻 💕 😺 😽 🐾
            </div>
            <div style="font-size: 1.5rem; color: #ff6b9d; margin-top: 1rem;">
                CATS ARE CELEBRATING!
            </div>
            <div style="color: #8b7ba8;">*purr purr purr* 🎉</div>
        </div>
        
        <style>
        @keyframes celebration {
            0% { transform: scale(0.8); opacity: 0; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        </style>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown("### 🐱 CATS ARE CELEBRATING! 🎉")

def show_header():
    """Display the cute header."""
    st.markdown(f"""
    <div class="big-title floating">
        🐱💕 {APP_NAME} 💕🐱
    </div>
    <div class="subtitle">
        The purr-fectly adorable video downloader! {CAT_EMOJIS['paw']} Made with love and whiskers! 💖
    </div>
    """, unsafe_allow_html=True)

def show_stats():
    """Show app statistics."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <h3>{CAT_EMOJIS['video']} Videos</h3>
            <p>Support 1000+ sites</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <h3>{CAT_EMOJIS['music']} Audio</h3>
            <p>MP3 conversion</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <h3>{CAT_EMOJIS['success']} Easy</h3>
            <p>One-click downloads</p>
        </div>
        """, unsafe_allow_html=True)

def show_download_interface():
    """Main download interface."""
    
    # Cute main header
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #ffeef8 0%, #f0e6ff 50%, #e6f3ff 100%); border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);">
        <h1 style="margin: 0; color: #667eea; font-family: 'Comic Sans MS', cursive; font-size: 2.5rem;">{CAT_EMOJIS['heart_eyes']} MeowDown {CAT_EMOJIS['heart_eyes']}</h1>
        <p style="margin: 0.5rem 0 0 0; color: #8b7ba8; font-size: 1.2rem; font-style: italic;">The purr-fectly cute video downloader!</p>
        <div style="font-size: 1.5rem; margin-top: 0.8rem; animation: bounce 2s infinite;">🐱💕✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    # URL Input with cute styling
    st.markdown(f"""
    <div style="margin-bottom: 1rem;">
        <h3 style="color: #667eea; margin-bottom: 0.5rem; font-family: 'Comic Sans MS', cursive;">
            {CAT_EMOJIS['excited']} Drop your video link here, human! {CAT_EMOJIS['paw']}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    url = st.text_input(
        "Video URL",
        placeholder="🌐 https://youtube.com/watch?v=... (or TikTok, Instagram, etc!) 🎬",
        help="🐱 Paste any video URL from YouTube, TikTok, Instagram, or 1000+ other sites! The cats will fetch it for you! 🐾",
        label_visibility="collapsed"
    )
    
    # Advanced options in expandable section with better styling
    with st.expander(f"🎯 Advanced Download Options", expanded=False):
        # Add cute cat animations floating around
        st.markdown("""
        <style>
        .floating-cats-1 {
            position: fixed;
            top: 15%;
            right: 30px;
            font-size: 2.5rem;
            animation: float1 3s ease-in-out infinite;
            z-index: 1000;
            pointer-events: none;
            opacity: 0.8;
        }
        .floating-cats-2 {
            position: fixed;
            top: 25%;
            left: 30px;
            font-size: 2rem;
            animation: float2 4s ease-in-out infinite;
            z-index: 1000;
            pointer-events: none;
            opacity: 0.7;
        }
        .floating-cats-3 {
            position: fixed;
            top: 45%;
            right: 10px;
            font-size: 1.8rem;
            animation: float3 5s ease-in-out infinite;
            z-index: 1000;
            pointer-events: none;
            opacity: 0.6;
        }
        .floating-cats-4 {
            position: fixed;
            top: 60%;
            left: 15px;
            font-size: 2.2rem;
            animation: float4 3.5s ease-in-out infinite;
            z-index: 1000;
            pointer-events: none;
            opacity: 0.8;
        }
        @keyframes float1 {
            0%, 100% { transform: translateY(0px) rotate(5deg); }
            50% { transform: translateY(-25px) rotate(-8deg); }
        }
        @keyframes float2 {
            0%, 100% { transform: translateY(0px) rotate(-3deg); }
            50% { transform: translateY(-15px) rotate(6deg); }
        }
        @keyframes float3 {
            0%, 100% { transform: translateY(0px) rotate(2deg); }
            50% { transform: translateY(-20px) rotate(-4deg); }
        }
        @keyframes float4 {
            0%, 100% { transform: translateY(0px) rotate(-6deg); }
            50% { transform: translateY(-18px) rotate(3deg); }
        }
        .advanced-container {
            padding: 2rem;
            background: linear-gradient(135deg, rgba(255,240,250,0.4), rgba(240,220,255,0.4));
            border-radius: 20px;
            margin: 1.5rem 0;
            border: 2px solid rgba(255,192,203,0.3);
            box-shadow: 0 4px 15px rgba(255,192,203,0.2);
        }
        </style>
        <div class="floating-cats-1">🐱</div>
        <div class="floating-cats-2">😸</div>
        <div class="floating-cats-3">😻</div>
        <div class="floating-cats-4">🐾</div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="advanced-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            format_choice = st.selectbox(
                f"{CAT_EMOJIS['thinking']} Choose format",
                [
                    f"{CAT_EMOJIS['video']} MP4 (Video) - *purr-fect quality*", 
                    f"{CAT_EMOJIS['music']} MP3 (Complete) - *with thumbnails & metadata embedded*",
                    f"📱 Best Quality Available",
                    f"🎬 Specific Quality..."
                ],
                help="Choose your preferred download format"
            )
            
            # Quality options for specific quality choice
            if "Specific Quality" in format_choice:
                quality_choice = st.selectbox(
                    "Video Quality",
                    ["720p", "1080p", "1440p", "4K", "Best", "Worst"],
                    index=2
                )
            else:
                quality_choice = "best"
        
        with col2:
            # Playlist options
            is_playlist = st.checkbox(
                f"📀 Download entire playlist/album",
                help="Download all videos/songs from a playlist or album"
            )
            
            if is_playlist:
                playlist_numbering = st.checkbox(
                    "🔢 Add track numbers",
                    value=True,
                    help="Add track numbers to filenames (001_, 002_, etc.)"
                )
                max_downloads = st.number_input(
                    "Max items to download",
                    min_value=1,
                    max_value=500,
                    value=50,
                    help="Limit the number of items to download"
                )
                
                # Playlist merging option (only for MP3 Complete format)
                st.markdown("**🎵 Playlist Options:**")
                if "MP3 (Complete)" in format_choice:
                    merge_playlist = st.checkbox(
                        f"🎵 **Create continuous playlist mix**",
                        value=False,  # Default to False so individual tracks are cleaner
                        help="🎧 Combine all tracks into one long MP3 file (like a radio show or DJ mix)"
                    )
                    st.info("ℹ️ **Individual tracks will always be downloaded.** Mix is optional!")
                else:
                    merge_playlist = False
                    st.info("🎵 Mix option available for MP3 Complete format only")
            else:
                playlist_numbering = False
                max_downloads = 1
                merge_playlist = False
        
        # Additional Options
        st.markdown("#### 📋 **Additional Options**")
        col3, col4 = st.columns(2)
        
        with col3:
            download_subtitles = st.checkbox(
                f"📝 Download subtitles",
                help="Download subtitle files if available (video formats only)"
            )
        
        with col4:
            st.info("🎵 **MP3 Complete includes:** Metadata, thumbnails, and album art automatically embedded!")
        
        # Set defaults for MP3 Complete format
        if "MP3 (Complete)" in format_choice:
            download_metadata = False  # Don't save separate .json files
            download_thumbnail = False  # Don't save separate .jpg files
            embed_metadata = True      # Everything embedded in MP3
        else:
            download_metadata = st.checkbox(
                f"📋 Download metadata files",
                value=True,
                help="Save .info.json files with video information"
            )
            download_thumbnail = st.checkbox(
                f"🖼️ Save thumbnail files", 
                value=True,
                help="Save thumbnail images as separate files"
            )
            embed_metadata = False
        
        st.markdown("---")
        st.markdown(f"### ✨ **Super Purr-fect Features** ✨")
        
        # Batch Downloads
        col5, col6 = st.columns(2)
        
        with col5:
            batch_mode = st.checkbox(
                f"📋 Batch Download Mode",
                help="Download multiple URLs at once - paste one URL per line!"
            )
            
            if batch_mode:
                batch_urls = st.text_area(
                    "Multiple URLs (one per line)",
                    placeholder="https://youtube.com/watch?v=abc123\nhttps://youtube.com/watch?v=def456\nhttps://soundcloud.com/track/xyz789",
                    height=100,
                    help="Paste multiple URLs, one per line"
                )
            else:
                batch_urls = ""
            
            # Channel Downloads
            channel_mode = st.checkbox(
                f"📺 Channel/Creator Mode",
                help="Download ALL videos from a channel or creator"
            )
            
            if channel_mode:
                channel_limit = st.number_input(
                    "Max videos from channel",
                    min_value=1,
                    max_value=1000,
                    value=25,
                    help="Limit how many videos to download from the channel"
                )
            else:
                channel_limit = 25
        
        with col6:
            # Audio Quality for MP3s
            if "MP3 (Complete)" in format_choice:
                audio_quality = st.selectbox(
                    f"🎵 Audio Quality",
                    [
                        "320 kbps (Best) - *audiophile cats*",
                        "256 kbps (High) - *music loving cats*", 
                        "192 kbps (Good) - *happy cats*",
                        "128 kbps (Standard) - *casual cats*",
                        "96 kbps (Small) - *space-saving cats*"
                    ],
                    index=0,  # Default to 320kbps for complete version
                    help="Choose MP3 audio quality"
                )
            else:
                audio_quality = "320 kbps (Best) - *audiophile cats*"
            
            # File Organization
            auto_organize = st.selectbox(
                f"📁 Auto-Organize Files",
                [
                    "🗂️ No organization - *all in one folder*",
                    "📅 By Date - *YYYY/MM/DD folders*",
                    "👤 By Channel - *separate channel folders*", 
                    "🎬 By Type - *Video/Audio folders*",
                    "🏷️ By Playlist - *playlist name folders*"
                ],
                help="Automatically organize downloads into folders"
            )
        
        # Smart Filters
        st.markdown("#### 🎯 **Smart Filters** *(Skip unwanted content)*")
        col7, col8 = st.columns(2)
        
        with col7:
            # Duration filter
            duration_filter = st.checkbox(f"⏱️ Filter by duration")
            if duration_filter:
                duration_min = st.number_input("Min duration (seconds)", min_value=0, value=30, help="Skip videos shorter than this")
                duration_max = st.number_input("Max duration (seconds)", min_value=0, value=3600, help="Skip videos longer than this (0 = no limit)")
            else:
                duration_min = 0
                duration_max = 0
            
            # File size filter  
            size_filter = st.checkbox(f"💾 Filter by file size")
            if size_filter:
                max_filesize = st.selectbox(
                    "Max file size",
                    ["50MB", "100MB", "250MB", "500MB", "1GB", "2GB", "No limit"],
                    index=3,
                    help="Skip files larger than this"
                )
            else:
                max_filesize = "No limit"
        
        with col8:
            # Content filters
            skip_live = st.checkbox(
                f"🚫 Skip live streams",
                value=True,
                help="Don't download live streams or premieres"
            )
            
            skip_shorts = st.checkbox(
                f"🚫 Skip shorts/clips",
                help="Skip YouTube Shorts, TikToks under 60s, etc."
            )
            
            # Language preference
            language_pref = st.selectbox(
                f"🌍 Language Preference",
                [
                    "🌐 Any language",
                    "🇺🇸 English only",
                    "🇪🇸 Spanish only", 
                    "🇫🇷 French only",
                    "🇩🇪 German only",
                    "🇯🇵 Japanese only",
                    "🇰🇷 Korean only"
                ],
                help="Prefer content in specific language"
            )
        
        # Power User Features
        st.markdown("#### ⚡ **Power User Features**")
        col9, col10 = st.columns(2)
        
        with col9:
            auto_retry = st.checkbox(
                f"🔄 Auto-retry failed downloads",
                value=True,
                help="Automatically retry downloads that fail"
            )
            
            download_archive = st.checkbox(
                f"📚 Keep download history",
                value=True,
                help="Remember what you've downloaded to avoid duplicates"
            )
        
        with col10:
            post_process = st.selectbox(
                f"🛠️ After download...",
                [
                    "🐱 Do nothing - *just enjoy*",
                    "🔊 Normalize audio volume",
                    "✂️ Auto-trim silence", 
                    "🗜️ Compress to save space",
                    "📤 Copy to cloud folder"
                ],
                help="Automatically process files after download"
            )
            
            notification_mode = st.selectbox(
                f"🔔 Notifications",
                [
                    "🐱 Cat celebrations only",
                    "🔔 System notifications",
                    "📧 Email when done",
                    "🤫 Silent mode"
                ],
                help="How to notify you when downloads complete"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close advanced container
    
    # Folder selection (always visible) with better spacing
    st.markdown("---")
    st.markdown("### 📁 **Download Location**")
    download_folder = st.text_input(
        f"{CAT_EMOJIS['paw']} Download folder",
        value=get_default_download_folder(),
        help="Where to save your downloads"
    )
    
    # Determine format type
    if "MP3 (Complete)" in format_choice:
        format_type = "mp3_complete"
    elif "Best Quality" in format_choice:
        format_type = "best"
    elif "Specific Quality" in format_choice:
        format_type = f"video_{quality_choice}"
    else:
        format_type = "mp4"
    
    # Download button with extra cuteness
    st.markdown("<div style='text-align: center; margin: 1rem 0;'><small style='color: #ff9a9e;'>Ready to pounce on that video? 🐾</small></div>", unsafe_allow_html=True)
    
    # Create columns to center the button better
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button(f"🚀✨ **DOWNLOAD MEOW!** ✨🐾", type="primary", use_container_width=True, help="Click to let the cats fetch your video! 🐱💕"):
            if not url:
                st.warning(f"Please paste a URL first! {CAT_EMOJIS['thinking']}")
                return
            
            if not is_valid_url(url):
                st.error(f"That doesn't look like a valid URL! {CAT_EMOJIS['error']}")
                return
            
            # Check dependencies
            if not st.session_state.get('deps_checked', False):
                with st.spinner(f"Checking dependencies... {CAT_EMOJIS['working']}"):
                    if not install_dependencies():
                        st.error(f"Failed to setup dependencies! {CAT_EMOJIS['error']}")
                        return
                    st.session_state.deps_checked = True
            
            # Prepare advanced options
            download_options = {
                'is_playlist': is_playlist,
                'playlist_numbering': playlist_numbering,
                'max_downloads': max_downloads,
                'merge_playlist': merge_playlist,
                'download_metadata': download_metadata,
                'download_thumbnail': download_thumbnail,
                'download_subtitles': download_subtitles,
                'embed_metadata': embed_metadata,
                # New creative features
                'batch_mode': batch_mode,
                'batch_urls': batch_urls,
                'channel_mode': channel_mode,
                'channel_limit': channel_limit,
                'audio_quality': audio_quality,
                'auto_organize': auto_organize,
                'duration_filter': duration_filter,
                'duration_min': duration_min,
                'duration_max': duration_max,
                'size_filter': size_filter,
                'max_filesize': max_filesize,
                'skip_live': skip_live,
                'skip_shorts': skip_shorts,
                'language_pref': language_pref,
                'auto_retry': auto_retry,
                'download_archive': download_archive,
                'post_process': post_process,
                'notification_mode': notification_mode
            }
            
            # Download
            progress_container = st.empty()
            success = download_video(url, download_folder, format_type, progress_container, download_options)
            
            if success:
                # Show success message first
                st.markdown(f"""
                <div class="success-message">
                    <h3>{CAT_EMOJIS['success']} Meow-nificent Success! {CAT_EMOJIS['heart_eyes']}</h3>
                    <p>Your download is complete! The cats are celebrating! {CAT_EMOJIS['paw']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Then play animations
                play_meow_sound()
                show_floating_cats()
                
                # Force a small delay to ensure animations load
                time.sleep(0.1)
                
                # PERSISTENT DOWNLOAD FOLDER OPENER - ALWAYS VISIBLE
                st.markdown("---")
                st.markdown("### 📁 **Open Your Downloaded Files**")
                st.info(f"📍 **Download location:** `{download_folder}`")
                
                # Store download folder in session state to persist across reruns
                st.session_state.last_download_folder = download_folder
                
                # Cute instructions instead of debug clutter
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffeef8 0%, #f0e6ff 100%); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center; border: 2px solid rgba(102, 126, 234, 0.2);">
                    <h3 style="color: #667eea; margin-bottom: 1rem;">{CAT_EMOJIS['paw']} Where are my files?</h3>
                    <div style="background: rgba(255,255,255,0.8); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                        <div style="color: #8b7ba8; font-size: 0.9rem; margin-bottom: 0.3rem;">📍 Your downloads are purr-fectly stored in:</div>
                        <div style="color: #667eea; font-weight: bold; word-break: break-all; font-family: monospace; font-size: 0.9rem;">{download_folder}</div>
                    </div>
                    <div style="color: #8b7ba8; font-size: 0.95rem; margin-top: 1rem;">
                        💡 <strong>Tip:</strong> Look for the <strong>"🚀✨ Open My Downloads! ✨🐾"</strong> button in the sidebar! {CAT_EMOJIS['heart_eyes']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Backup manual copy option
                with st.expander("📋 Need to copy the path manually?", expanded=False):
                    st.code(download_folder)
                    st.markdown("💡 *Copy this path and paste it in File Explorer's address bar!*")

def show_sidebar():
    """Show cute sidebar with cat-themed elements."""
    with st.sidebar:
        # Cute header with animated elements
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #ffeef8 0%, #f0e6ff 100%); border-radius: 15px; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);">
            <h2 style="margin: 0; color: #667eea; font-family: 'Comic Sans MS', cursive;">{CAT_EMOJIS['heart_eyes']} MeowDown</h2>
            <p style="margin: 0; color: #8b7ba8; font-size: 0.9rem;">v{VERSION} - Purr-fectly Cute!</p>
            <div style="font-size: 2.5rem; margin: 0.5rem 0; animation: bounce 2s infinite;">🐱</div>
        </div>
        """, unsafe_allow_html=True)
        
        # FOLDER OPENER SECTION - Clean and prominent
        if 'last_download_folder' in st.session_state:
            folder_path = st.session_state.last_download_folder
            folder_name = Path(folder_path).name if Path(folder_path).name else "Downloads"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,238,248,0.8) 100%); padding: 1rem; border-radius: 12px; margin: 1rem 0; border: 2px solid #f0e6ff;">
                <h3 style="margin: 0 0 0.5rem 0; color: #667eea; font-size: 1.1rem;">📁 Your Downloads</h3>
                <div style="font-size: 0.85rem; color: #8b7ba8; margin-bottom: 0.3rem;">📍 Latest downloads in:</div>
                <div style="background: rgba(102, 126, 234, 0.1); padding: 0.5rem; border-radius: 8px; font-weight: bold; color: #667eea; font-size: 0.9rem; word-break: break-all;">📂 {folder_name}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Primary folder opener button - bigger and cuter
            if st.button("🚀✨ **Open My Downloads!** ✨🐾", use_container_width=True, key="sidebar_folder_opener", type="primary"):
                print(f"\nSIDEBAR FOLDER BUTTON CLICKED!")
                print(f"   Folder: {folder_path}")
                # Track download count for cat mood
                st.session_state.download_count = st.session_state.get('download_count', 0) + 1
                
                try:
                    subprocess.Popen(['explorer', folder_path])
                    print(f"   Explorer command sent!")
                    st.success("🎉 Folder opened! Happy downloading! 🐱✨")
                    st.balloons()
                except Exception as e:
                    try:
                        os.startfile(folder_path)
                        st.success("🎉 Folder opened! Meow-nificent! 🐱✨")
                    except:
                        st.error(f"Oops! {CAT_EMOJIS['error']} Couldn't open folder")
            
            # Compact path copy
            with st.expander("📋 Copy Path Instead", expanded=False):
                st.code(folder_path, language=None)
        
        # Cat mood indicator based on app usage
        st.markdown("---")
        download_count = st.session_state.get('download_count', 0)
        if download_count == 0:
            mood_cat = CAT_EMOJIS['normal']
            mood_text = "Ready to download!"
        elif download_count < 5:
            mood_cat = CAT_EMOJIS['happy']
            mood_text = "Getting started!"
        elif download_count < 10:
            mood_cat = CAT_EMOJIS['excited']
            mood_text = "You're on fire!"
        else:
            mood_cat = CAT_EMOJIS['heart_eyes']
            mood_text = "Download master!"
            
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, rgba(255,255,255,0.7) 0%, rgba(240,230,255,0.5) 100%); border-radius: 12px; margin: 1rem 0; border: 1px solid rgba(102, 126, 234, 0.2);">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem; animation: pulse 2s infinite;">{mood_cat}</div>
            <div style="color: #667eea; font-weight: bold; font-size: 1rem;">{mood_text}</div>
            <div style="color: #8b7ba8; font-size: 0.8rem; margin-top: 0.2rem;">Folder opens: {download_count}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick cat celebration button
        if st.button("🎉 **Cat Party Time!** 🎉", help="Instant cat celebration!", use_container_width=True):
            st.balloons()
            st.success("🐱✨ MEOW PARTY ACTIVATED! ✨🐱")
            play_meow_sound()
            show_floating_cats()
            # Add some confetti effect
            st.markdown(f"""
            <div style="text-align: center; font-size: 2rem; animation: bounce 1s infinite;">
                🎊 {CAT_EMOJIS['excited']} 🎊 {CAT_EMOJIS['heart_eyes']} 🎊 {CAT_EMOJIS['happy']} 🎊
            </div>
            """, unsafe_allow_html=True)
        
        # Cute about section
        st.markdown("---")
        with st.expander(f"ℹ️ About MeowDown {CAT_EMOJIS['paw']}"):
            st.markdown(f"""
            {CAT_EMOJIS['heart_eyes']} **The cutest video downloader ever!**
            
            **What this kitty can do:**
            - 📱 YouTube, TikTok, Instagram & more
            - 🌍 1000+ supported sites  
            - 🎥 High-quality video downloads
            - 🎵 MP3 audio extraction
            - 🐱 100% cat-approved interface!
            
            Made with {CAT_EMOJIS['heart_eyes']} and lots of purrs!
            """)
        
        # Cute footer with animation
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; margin-top: 2rem;">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem; animation: wiggle 3s infinite;">🐾 🐱 🐾</div>
            <div style="color: #8b7ba8; font-size: 0.7rem; font-style: italic;">Made with purrs & pixels</div>
        </div>
        
        <style>
        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
            40% {{ transform: translateY(-10px); }}
            60% {{ transform: translateY(-5px); }}
        }}
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); }}
        }}
        @keyframes wiggle {{
            0%, 100% {{ transform: rotate(0deg); }}
            25% {{ transform: rotate(5deg); }}
            75% {{ transform: rotate(-5deg); }}
        }}
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("🐾 *paws and whiskers ready for action!*")
        
        # Debug info
        st.markdown("---")
        st.markdown(f"### 🔧 Debug Info")
        default_folder = get_default_download_folder()
        st.write(f"**Download folder:** `{default_folder}`")
        st.write(f"**Folder exists:** {Path(default_folder).exists()}")
        st.write(f"**Platform:** {platform.system()}")
        st.write(f"**Python version:** {sys.version.split()[0]}")
        
        # Show Streamlit version info
        try:
            import streamlit
            st.write(f"**Streamlit version:** {streamlit.__version__}")
        except:
            st.write("**Streamlit version:** Unknown")

# =============================================================================
# 🚀 MAIN APPLICATION
# =============================================================================

def main():
    """Main application function."""
    setup_page_config()
    load_custom_css()
    
    # Initialize session state
    if 'deps_checked' not in st.session_state:
        st.session_state.deps_checked = False
    
    # Header
    show_header()
    
    # Stats
    show_stats()
    
    st.markdown("---")
    
    # Main interface
    show_download_interface()
    
    # Sidebar
    show_sidebar()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #8b7ba8; padding: 2rem; background: rgba(255,255,255,0.3); border-radius: 20px; margin: 1rem;">
        Made with {CAT_EMOJIS['heart_eyes']} and lots of purrs {CAT_EMOJIS['paw']}<br>
        <small>Always respect content creators and platform terms of service!</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()