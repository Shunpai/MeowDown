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
        initial_sidebar_state="collapsed",
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

def download_video(url, dest_folder, format_type, progress_container):
    """Download video with real-time progress updates."""
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
        
        # Build command
        cmd = [sys.executable, "-m", "yt_dlp", url, "--newline"]
        
        if ffmpeg_path.exists():
            cmd.extend(["--ffmpeg-location", str(ffmpeg_path)])
        
        if format_type == "mp3":
            cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
            output_template = str(dest_path / "🎵%(title)s.%(ext)s")
        else:
            cmd.extend(["-f", "best[ext=mp4]/best"])
            output_template = str(dest_path / "🎬%(title)s.%(ext)s")
        
        cmd.extend(["-o", output_template])
        
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT, text=True)
            
            for line in proc.stdout:
                if "[download]" in line:
                    if "Destination:" in line:
                        status_text.success(f"Found video! {CAT_EMOJIS['excited']}")
                    elif "has already been downloaded" in line:
                        status_text.info(f"Already downloaded! {CAT_EMOJIS['sleepy']}")
                        progress_bar.progress(1.0)
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
            
            proc.wait()
            
            if proc.returncode == 0:
                status_text.success(f"Download complete! {CAT_EMOJIS['success']}")
                progress_bar.progress(1.0)
                return True
            else:
                status_text.error(f"Download failed! {CAT_EMOJIS['error']}")
                return False
                
        except Exception as e:
            st.error(f"Download error: {e} {CAT_EMOJIS['error']}")
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
    
    # URL Input
    st.markdown(f"### {CAT_EMOJIS['normal']} Paste your video URL")
    url = st.text_input(
        "Video URL",
        placeholder="https://youtube.com/watch?v=... or any supported site!",
        help="Paste a video URL from YouTube, TikTok, or 1000+ other sites!",
        label_visibility="collapsed"
    )
    
    # Format and folder selection
    col1, col2 = st.columns(2)
    
    with col1:
        format_choice = st.selectbox(
            f"{CAT_EMOJIS['thinking']} Choose format",
            [f"{CAT_EMOJIS['video']} MP4 (Video) - *purr-fect quality*", f"{CAT_EMOJIS['music']} MP3 (Audio) - *meow-sical*"],
            help="MP4 for videos, MP3 for audio only - both are pawsome!"
        )
        format_type = "mp3" if "MP3" in format_choice else "mp4"
    
    with col2:
        download_folder = st.text_input(
            f"{CAT_EMOJIS['paw']} Download folder",
            value=get_default_download_folder(),
            help="Where to save your downloads"
        )
    
    # Download button with extra cuteness
    st.markdown("<div style='text-align: center; margin: 1rem 0;'><small style='color: #ff9a9e;'>Ready to pounce on that video? 🐾</small></div>", unsafe_allow_html=True)
    
    # Create columns to center the button better
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button(f"{CAT_EMOJIS['download']} Download Meow! 💕", type="primary", use_container_width=True):
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
            
            # Download
            progress_container = st.empty()
            success = download_video(url, download_folder, format_type, progress_container)
            
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
                
                # Create columns for better button layout
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    # Open folder button with working method from debug version
                    if st.button(f"{CAT_EMOJIS['paw']} Open Downloads Folder", type="secondary", use_container_width=True, key="open_folder_success"):
                        success = False
                        
                        try:
                            # Make sure folder exists
                            folder = Path(download_folder)
                            if not folder.exists():
                                st.info("Created downloads folder!")
                                folder.mkdir(parents=True, exist_ok=True)
                            
                            if platform.system() == "Windows":
                                # Use the method that worked in our test: cmd /c start
                                try:
                                    result = subprocess.run(
                                        ["cmd", "/c", "start", str(folder)], 
                                        check=True, 
                                        capture_output=True, 
                                        timeout=5
                                    )
                                    st.success("Opening your downloads folder! 😸")
                                    success = True
                                    
                                except subprocess.CalledProcessError as e:
                                    pass
                                        
                                except subprocess.TimeoutExpired:
                                    st.success("Opening folder (command timed out but likely worked)")
                                    success = True
                                    
                                except Exception as e:
                                    pass
                                
                                # Backup method: os.startfile
                                if not success:
                                    try:
                                        os.startfile(str(folder))
                                        st.success("Opening your downloads folder! 😸")
                                        success = True
                                    except Exception as e:
                                        pass
                            
                            else:
                                # Non-Windows platforms
                                if platform.system() == "Darwin":
                                    result = subprocess.run(["open", str(folder)], check=True, capture_output=True)
                                    success = True
                                else:
                                    result = subprocess.run(["xdg-open", str(folder)], check=True, capture_output=True)
                                    success = True
                                st.success("Opening your downloads folder! 😸")
                            
                            if not success:
                                st.error("Couldn't open folder automatically 😿")
                            
                        except Exception as e:
                            st.error(f"Error: {e}")
                        
                        # Always show manual path
                        st.info(f"**Manual path:** `{download_folder}`")
                        st.markdown("*Copy this path to your file explorer if the button didn't work*")

def show_sidebar():
    """Show sidebar with additional options."""
    with st.sidebar:
        st.markdown(f"## {CAT_EMOJIS['normal']} MeowDown")
        st.markdown(f"Version {VERSION}")
        
        # Test button for animations
        st.markdown("---")
        st.markdown(f"### {CAT_EMOJIS['excited']} Test Zone")
        if st.button("🎉 Test Cat Animation!", help="See the floating cats without downloading"):
            st.success("Activating cat celebration! 🐱✨")
            play_meow_sound()
            show_floating_cats()
            
        # Test folder opening
        if st.button("📁 Test Folder Opening", help="Test if folder opening works"):
            test_folder = get_default_download_folder()
            st.info(f"Testing folder: {test_folder}")
            
            success = False
            
            try:
                if platform.system() == "Windows":
                    # Use the proven cmd /c start method
                    try:
                        result = subprocess.run(
                            ["cmd", "/c", "start", test_folder], 
                            check=True, 
                            capture_output=True, 
                            timeout=5
                        )
                        st.success("Folder opened successfully! 😸")
                        success = True
                    except subprocess.TimeoutExpired:
                        st.success("Folder likely opened (timed out)")
                        success = True
                    except:
                        # Backup method
                        try:
                            os.startfile(test_folder)
                            st.success("Folder opened with backup method! 😸")
                            success = True
                        except Exception as e:
                            st.error(f"Failed to open folder: {e}")
                else:
                    st.info("This test is optimized for Windows")
                    
                if not success and platform.system() == "Windows":
                    st.error("All folder opening methods failed")
                    
            except Exception as e:
                st.error(f"Unexpected error: {e}")
        
        st.markdown("---")
        
        st.markdown(f"### {CAT_EMOJIS['paw']} About This Cutie")
        st.markdown("""
        💕 A purr-fectly adorable video downloader that supports:
        - 📱 YouTube, TikTok, Instagram
        - 🌍 1000+ other sites  
        - 🎥 MP4 video downloads
        - 🎵 MP3 audio extraction
        - 🤖 Automatic dependency management
        - 🐱 100% cat-approved cuteness!
        """)
        
        st.markdown("---")
        
        if st.button(f"{CAT_EMOJIS['heart_eyes']} Give Us Some Love!"):
            st.markdown(f"[⭐ Star on GitHub]({GITHUB_URL})")
            st.markdown("💕 Thank you for supporting our purr-oject!")
        
        st.markdown("---")
        
        st.markdown(f"### {CAT_EMOJIS['cool']} Paw-some System Info")
        deps = check_dependencies()
        
        st.write(f"😸 **yt-dlp:** {'✅ Ready to pounce!' if deps['ytdlp'] else '❌ Needs setup'}")
        st.write(f"🎬 **FFmpeg:** {'✅ Purr-fect!' if deps['ffmpeg'] else '❌ Downloading...'}")
        st.write(f"💻 **Platform:** {platform.system()} *meow*")
        
        if st.button("🔄 Refresh Paw-some Status"):
            st.session_state.deps_checked = False
            st.rerun()
        
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