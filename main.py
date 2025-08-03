import dearpygui.dearpygui as dpg
import threading
import subprocess
import os
import sys
import pyperclip
import re
import urllib.parse
from pathlib import Path
import time
import requests
import zipfile
import shutil
import json
import platform
from typing import Optional
import tempfile

# ------------ CONFIG ------------
APP_NAME = "MeowDown"
VERSION = "2.0.0"
WINDOW_WIDTH, WINDOW_HEIGHT = 650, 500
CAT_EMOJIS = ["🐱", "😸", "😺", "🙀", "😻", "🐾", "🎵", "📹"]
THEME_COLOR = (128, 70, 240, 230)  # Modern purple
SUCCESS_COLOR = (100, 200, 100, 255)
ERROR_COLOR = (255, 100, 100, 255)
WARNING_COLOR = (255, 200, 100, 255)

# Dependency URLs
FFMPEG_URLS = {
    "Windows": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
    "Darwin": "https://evermeet.cx/ffmpeg/getrelease/zip",
    "Linux": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
}
# ---------------------------------

def is_valid_url(url):
    """Validate if the given string is a valid URL."""
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def get_app_dir():
    """Get application directory for storing binaries."""
    if getattr(sys, 'frozen', False):
        # Running as executable
        app_dir = Path(sys.executable).parent
    else:
        # Running as script
        app_dir = Path(__file__).parent
    
    bin_dir = app_dir / "bin"
    bin_dir.mkdir(exist_ok=True)
    return bin_dir

def download_file(url: str, dest_path: Path, progress_callback=None) -> bool:
    """Download a file with progress tracking."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total_size > 0:
                        progress_callback(downloaded / total_size)
        
        return True
    except Exception as e:
        if dest_path.exists():
            dest_path.unlink()
        return False

def install_ffmpeg() -> bool:
    """Download and install FFmpeg."""
    bin_dir = get_app_dir()
    ffmpeg_exe = bin_dir / ("ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg")
    
    if ffmpeg_exe.exists():
        return True
    
    system = platform.system()
    if system not in FFMPEG_URLS:
        return False
    
    set_status("🐱 Downloading FFmpeg... (this might take a moment)")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            archive_path = temp_path / "ffmpeg.zip"
            
            def progress_cb(progress):
                set_progress(progress * 0.7)  # 70% for download
            
            if not download_file(FFMPEG_URLS[system], archive_path, progress_cb):
                return False
            
            set_status("🐱 Extracting FFmpeg...")
            set_progress(0.8)
            
            # Extract archive
            if system == "Windows":
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                
                # Find ffmpeg.exe in extracted files
                for root, dirs, files in os.walk(temp_path):
                    if "ffmpeg.exe" in files:
                        src_path = Path(root) / "ffmpeg.exe"
                        shutil.copy2(src_path, ffmpeg_exe)
                        break
            
            set_progress(1.0)
            return ffmpeg_exe.exists()
    
    except Exception as e:
        set_status(f"😿 Failed to install FFmpeg: {str(e)}")
        return False

def install_ytdlp() -> bool:
    """Install yt-dlp using pip."""
    try:
        set_status("🐱 Installing yt-dlp...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def check_dependencies() -> dict:
    """Check if all dependencies are available."""
    deps = {
        "ytdlp": False,
        "ffmpeg": False
    }
    
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
        # Check system PATH
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
            deps["ffmpeg"] = result.returncode == 0
        except Exception:
            pass
    
    return deps

def setup_dependencies():
    """Setup all required dependencies."""
    deps = check_dependencies()
    
    if not deps["ytdlp"]:
        if not install_ytdlp():
            set_status("😿 Failed to install yt-dlp")
            return False
    
    if not deps["ffmpeg"]:
        if not install_ffmpeg():
            set_status("😿 Failed to install FFmpeg")
            return False
    
    set_status("😸 All dependencies ready!")
    return True

def get_default_download_folder():
    """Get cross-platform default download folder."""
    downloads = Path.home() / "Downloads"
    if downloads.exists() and downloads.is_dir():
        return str(downloads)
    return str(Path.cwd())

# -------- State --------
state = {
    "url": "",
    "destination": get_default_download_folder(),
    "format": "mp4",
    "downloading": False,
    "progress": 0,
    "status": "",
    "current_cat": 0,
    "dependencies_checked": False,
}

def set_status(msg):
    """Thread-safe status update with cute cat rotation."""
    try:
        # Rotate cat emoji for fun
        if "🐱" in msg or "😸" in msg or "😺" in msg:
            state["current_cat"] = (state["current_cat"] + 1) % len(CAT_EMOJIS)
        
        dpg.set_value("status_text", msg)
        dpg.configure_item("status_text", show=True)
        
        # Update title cat too
        current_title = dpg.get_viewport_title()
        if current_title:
            new_title = f"{CAT_EMOJIS[state['current_cat']]} {APP_NAME} v{VERSION}"
            dpg.set_viewport_title(new_title)
    except Exception:
        pass

def set_progress(p):
    """Thread-safe progress update."""
    try:
        dpg.set_value("progress_bar", p)
    except Exception:
        pass

def enable_download_button(enable=True):
    """Thread-safe button enable/disable with cute label updates."""
    try:
        dpg.configure_item("download_btn", enabled=enable)
        if enable and not state["downloading"]:
            dpg.configure_item("download_btn", label="😸 Download Meow!")
        elif state["downloading"]:
            dpg.configure_item("download_btn", label="😻 Downloading...")
    except Exception:
        pass

# ---- Download Logic ----
def download_video(url, dest_folder, format_type):
    set_status("🐱 Fetching video info... *purr*")
    set_progress(0.05)
    
    # Validate destination folder
    dest_path = Path(dest_folder)
    if not dest_path.exists():
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            set_status(f"😿 Meow! Cannot create folder: {str(e)}")
            return
    
    if not os.access(dest_path, os.W_OK):
        set_status("😿 Meow! Folder is not writable")
        return
    
    # Get FFmpeg path
    bin_dir = get_app_dir()
    ffmpeg_path = bin_dir / ("ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg")
    
    # Build command based on format
    cmd = [sys.executable, "-m", "yt_dlp", url, "--newline"]
    
    # Add FFmpeg location if we have it
    if ffmpeg_path.exists():
        cmd.extend(["--ffmpeg-location", str(ffmpeg_path)])
    
    if format_type == "mp3":
        cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
        output_template = os.path.join(dest_folder, "🐱%(title)s.%(ext)s")
        set_status("🎵 Converting to MP3... *meow meow*")
    elif format_type == "mp4":
        cmd.extend(["-f", "best[ext=mp4]/best"])
        output_template = os.path.join(dest_folder, "📹%(title)s.%(ext)s")
        set_status("📹 Downloading video... *pounce*")
    else:
        output_template = os.path.join(dest_folder, "🐱%(title)s.%(ext)s")
    
    cmd.extend(["-o", output_template])
    
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in proc.stdout:
            if "[download]" in line:
                if "Destination:" in line:
                    set_status("😸 Found the video! Starting download...")
                elif "has already been downloaded" in line:
                    set_status("😺 Already have this one! *happy purr*")
                    set_progress(1.0)
                else:
                    match = re.search(r'(\d{1,3}(?:\.\d+)?)%', line)
                    if match:
                        percent = float(match.group(1)) / 100.0
                        set_progress(percent)
                        
                        # Fun status messages based on progress
                        if percent < 0.25:
                            set_status(f"🐱 Downloading... {percent*100:.1f}% *curious meow*")
                        elif percent < 0.5:
                            set_status(f"😺 Getting there... {percent*100:.1f}% *excited purr*")
                        elif percent < 0.75:
                            set_status(f"😸 Almost done... {percent*100:.1f}% *happy meow*")
                        else:
                            set_status(f"😻 So close... {percent*100:.1f}% *anticipating purr*")
                    elif "100%" in line:
                        set_progress(1.0)
            elif "[ffmpeg]" in line:
                set_status("🎵 Converting with FFmpeg... *technical meow*")
        
        proc.wait()
        
        if proc.returncode == 0:
            set_status("🎉 Download complete! *victory purr* 🎉")
            dpg.configure_item("open_folder_btn", show=True)
            # Add a little celebration
            for i in range(3):
                time.sleep(0.2)
                dpg.set_value("status_text", f"🎉 Success! {CAT_EMOJIS[i % len(CAT_EMOJIS)]} *happy dance* 🎉")
        else:
            set_status("😿 Meow! Something went wrong. Check your URL!")
            
    except FileNotFoundError:
        set_status("😿 Meow! yt-dlp not found. Installing now...")
        if install_ytdlp():
            set_status("😸 Installed yt-dlp! Try again!")
        else:
            set_status("😿 Failed to install yt-dlp")
    except Exception as e:
        set_status(f"😿 Unexpected error: {str(e)}")
    finally:
        state["downloading"] = False
        enable_download_button(True)

def on_download(sender, app_data, user_data):
    url = dpg.get_value("url_input").strip()
    dest = state["destination"]
    format_type = state["format"]
    
    if not url:
        set_status("🙀 Meow! Please paste a URL first!")
        return
    
    if not is_valid_url(url):
        set_status("😿 That doesn't look like a URL! *confused meow*")
        return
    
    # Check dependencies first
    if not state["dependencies_checked"]:
        set_status("🐱 Checking dependencies...")
        if not setup_dependencies():
            return
        state["dependencies_checked"] = True
    
    enable_download_button(False)
    set_status("😸 Starting download... *excited purr*")
    state["downloading"] = True
    dpg.configure_item("open_folder_btn", show=False)
    set_progress(0)
    
    def download_with_callbacks():
        download_video(url, dest, format_type)
    
    threading.Thread(target=download_with_callbacks, daemon=True).start()

def on_open_folder(sender, app_data):
    try:
        if sys.platform == "win32":
            os.startfile(state["destination"])
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", state["destination"]])
        else:  # Linux
            subprocess.run(["xdg-open", state["destination"]])
        set_status("😸 Opening your downloads! *happy meow*")
    except Exception as e:
        set_status(f"😿 Error opening folder: {str(e)}")

def on_url_input(sender, app_data):
    url = dpg.get_value("url_input").strip()
    is_valid = bool(url) and is_valid_url(url) and not state["downloading"]
    enable_download_button(is_valid)
    
    if url and is_valid_url(url):
        set_status("😸 Valid URL detected! *excited meow*")
        dpg.set_value("progress_bar", 0)
        dpg.configure_item("progress_bar", overlay="Ready to download! 😸")
    elif url:
        set_status("🙀 That doesn't look like a valid URL *confused meow*")
    else:
        dpg.configure_item("status_text", show=False)
        dpg.configure_item("progress_bar", overlay="Ready to pounce! 🐾")

def on_clipboard_paste(sender, app_data, user_data):
    try:
        clip = pyperclip.paste()
        if clip and clip.strip():
            dpg.set_value("url_input", clip.strip())
            set_status("😸 Pasted! *happy meow*")
            on_url_input(None, None)  # Trigger validation
        else:
            set_status("🙀 Clipboard is empty *sad meow*")
    except pyperclip.PyperclipException as e:
        set_status(f"😿 Clipboard error: {str(e)}")
    except Exception as e:
        set_status(f"😿 Unexpected clipboard error: {str(e)}")

def on_folder_select(sender, app_data):
    folder = app_data['file_path_name'] if app_data else None
    if folder and os.path.isdir(folder):
        state["destination"] = folder
        dpg.set_value("dest_input", folder)
        set_status("😸 New download spot selected! *purr*")

def on_format_change(sender, app_data):
    state["format"] = app_data
    if app_data == "mp3":
        set_status("🎵 Audio mode selected! *musical meow*")
    else:
        set_status("📹 Video mode selected! *cinematic purr*")

def setup_theme():
    with dpg.theme() as theme_id:
        with dpg.theme_component(dpg.mvAll):
            # Main colors - cute purple theme
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 20, 35, 245), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, THEME_COLOR, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (158, 90, 250, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (98, 30, 200, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (55, 45, 85, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (75, 60, 140, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (85, 70, 150, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (0,0,0,80), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (245, 240, 255, 255), category=dpg.mvThemeCat_Core)
            
            # Progress bar colors
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (150, 100, 250, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, (170, 120, 255, 255), category=dpg.mvThemeCat_Core)
            
            # Cute rounded corners
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 20, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 25, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 30, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 10, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 12, category=dpg.mvThemeCat_Core)
    return theme_id

def add_cute_separator():
    """Add a cute separator with cat paws."""
    dpg.add_text("  🐾 • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • 🐾", color=(180, 140, 255, 150))

def check_for_updates():
    """Check if dependencies are ready and show startup status."""
    def startup_check():
        set_status("🐱 Starting up... *yawn*")
        time.sleep(0.5)
        
        deps = check_dependencies()
        if not deps["ytdlp"] or not deps["ffmpeg"]:
            set_status("🐱 First time setup... preparing dependencies!")
            setup_dependencies()
        else:
            set_status("😸 Ready to download! *happy purr*")
        
        state["dependencies_checked"] = True
    
    threading.Thread(target=startup_check, daemon=True).start()

def launch_meowdown():
    dpg.create_context()
    theme_id = setup_theme()
    dpg.create_viewport(title=f"{CAT_EMOJIS[0]} {APP_NAME} v{VERSION}", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, resizable=False)
    dpg.setup_dearpygui()

    # Create file dialog for folder selection
    with dpg.file_dialog(
        directory_selector=True, 
        show=False, 
        callback=on_folder_select, 
        tag="folder_picker", 
        width=600, 
        height=450, 
        modal=True
    ):
        dpg.add_file_extension("", color=(255, 255, 255, 255))

    with dpg.window(label="", tag="main_window", no_title_bar=True, no_resize=True, no_move=True, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        # Header with cute title
        dpg.add_spacer(height=15)
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_text(f"🐱 MeowDown v{VERSION}", color=(255, 220, 255, 255))
            dpg.add_spacer(width=150)
            dpg.add_text("*purr*", color=(200, 150, 255, 150))
        
        add_cute_separator()
        dpg.add_spacer(height=15)
        
        # URL Input Section with cute styling
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_text("🔗 Video URL:", color=(200, 170, 255))
        dpg.add_spacer(height=8)
        
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_input_text(tag="url_input", hint="https://youtube.com/watch?v=... *meow*", width=430, callback=on_url_input, on_enter=True)
            dpg.add_button(label="📋 Paste", callback=on_clipboard_paste, width=90)
        
        dpg.add_spacer(height=18)
        
        # Destination Folder Section
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_text("📁 Download to:", color=(200, 170, 255))
        dpg.add_spacer(height=8)
        
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_input_text(tag="dest_input", default_value=state["destination"], width=430, enabled=False)
            dpg.add_button(label="📂 Browse", callback=lambda: dpg.show_item("folder_picker"), width=90)
        
        dpg.add_spacer(height=18)
        
        # Format Selection with cute icons
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_text("🎚️ Format:", color=(200, 170, 255))
        dpg.add_spacer(height=8)
        
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_combo(
                items=["📹 mp4 (Video)", "🎵 mp3 (Audio)"], 
                default_value="📹 mp4 (Video)", 
                width=250, 
                callback=lambda s, a: on_format_change(s, a.split()[1] if len(a.split()) > 1 else "mp4"),
                tag="format_combo"
            )
        
        dpg.add_spacer(height=25)
        
        # Download Button - centered and cute
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=225)
            dpg.add_button(label="😸 Download Meow!", tag="download_btn", callback=on_download, width=200, height=35, enabled=False)
        
        dpg.add_spacer(height=20)
        
        # Progress Bar with cute styling
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=75)
            dpg.add_progress_bar(tag="progress_bar", default_value=0.0, overlay="Ready to pounce! 🐾", width=500, height=28)
        
        dpg.add_spacer(height=15)
        
        # Status Text - centered
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=50)
            dpg.add_text("", tag="status_text", color=(255, 200, 240), show=False, wrap=550)
        
        dpg.add_spacer(height=15)
        
        # Open Folder Button - centered
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=225)
            dpg.add_button(label="📁 Open Downloads", tag="open_folder_btn", callback=on_open_folder, show=False, width=200, height=30)
        
        dpg.add_spacer(height=10)
        
        # Footer with cute message
        add_cute_separator()
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=200)
            dpg.add_text("🐾 Made with ♥ and lots of purrs 🐾", color=(180, 140, 255, 120))

    dpg.bind_theme(theme_id)
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    
    # Start dependency check
    check_for_updates()
    
    dpg.start_dearpygui()
    dpg.destroy_context()

# -- Run It! --
if __name__ == "__main__":
    launch_meowdown()
