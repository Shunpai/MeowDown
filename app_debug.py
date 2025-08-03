#!/usr/bin/env python3
"""
🐱 MeowDown v3.0.0 - Debug Version
A delightful Streamlit-based video downloader with debug output!
"""

import streamlit as st
import os
import sys
import subprocess
import platform
import time
from pathlib import Path

# Debug output to console
def debug_print(message, level="INFO"):
    """Print debug messages to console."""
    timestamp = time.strftime("%H:%M:%S")
    try:
        if level == "ERROR":
            print(f"[{timestamp}] ERROR: {message}")
        elif level == "SUCCESS":
            print(f"[{timestamp}] SUCCESS: {message}")
        else:
            print(f"[{timestamp}] INFO: {message}")
    except UnicodeEncodeError:
        # Fallback for Windows console
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        if level == "ERROR":
            print(f"[{timestamp}] ERROR: {safe_message}")
        elif level == "SUCCESS":
            print(f"[{timestamp}] SUCCESS: {safe_message}")
        else:
            print(f"[{timestamp}] INFO: {safe_message}")

def get_default_download_folder():
    """Get cross-platform default download folder."""
    downloads = Path.home() / "Downloads"
    if downloads.exists() and downloads.is_dir():
        return str(downloads)
    return str(Path.cwd())

def show_floating_cats():
    """Display floating cats animation."""
    debug_print("Showing floating cats animation")
    
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
        
        debug_print("Floating cats animation completed successfully!", "SUCCESS")
        
    except Exception as e:
        debug_print(f"Error showing floating cats: {e}", "ERROR")
        st.markdown("### 🐱 CATS ARE CELEBRATING! 🎉")

def open_folder_button(folder_path):
    """Create a button to open folder with debug output."""
    if st.button("🐾 Open Downloads Folder", type="secondary", use_container_width=True):
        debug_print(f"User clicked Open Folder button for: {folder_path}")
        
        success = False
        
        try:
            # Make sure folder exists
            folder = Path(folder_path)
            if not folder.exists():
                debug_print(f"Folder doesn't exist, creating: {folder}")
                folder.mkdir(parents=True, exist_ok=True)
                st.info("Created downloads folder!")
            
            debug_print(f"Folder exists: {folder.exists()}")
            debug_print(f"Platform: {platform.system()}")
            
            if platform.system() == "Windows":
                # Use the method that worked in our test: cmd /c start
                try:
                    debug_print("Trying: cmd /c start method")
                    result = subprocess.run(
                        ["cmd", "/c", "start", str(folder)], 
                        check=True, 
                        capture_output=True, 
                        timeout=5
                    )
                    debug_print(f"Command succeeded! Return code: {result.returncode}", "SUCCESS")
                    st.success("Opening your downloads folder! 😸")
                    success = True
                    
                except subprocess.CalledProcessError as e:
                    debug_print(f"cmd start failed: return code {e.returncode}", "ERROR")
                    if e.stderr:
                        debug_print(f"Error output: {e.stderr.decode()}")
                        
                except subprocess.TimeoutExpired:
                    debug_print("Command timed out (but folder probably opened)", "SUCCESS")
                    st.success("Opening folder (command timed out but likely worked)")
                    success = True
                    
                except Exception as e:
                    debug_print(f"cmd start exception: {type(e).__name__}: {e}", "ERROR")
                
                # Backup method: os.startfile
                if not success:
                    try:
                        debug_print("Trying backup method: os.startfile")
                        os.startfile(str(folder))
                        debug_print("os.startfile succeeded!", "SUCCESS")
                        st.success("Opening your downloads folder! 😸")
                        success = True
                    except Exception as e:
                        debug_print(f"os.startfile failed: {type(e).__name__}: {e}", "ERROR")
            
            else:
                # Non-Windows platforms
                debug_print(f"Non-Windows platform: {platform.system()}")
                st.info("Folder opening test is currently Windows-only")
            
            if not success:
                st.error("Couldn't open folder automatically 😿")
                debug_print("All folder opening methods failed", "ERROR")
            
        except Exception as e:
            debug_print(f"Unexpected error in folder opening: {type(e).__name__}: {e}", "ERROR")
            st.error(f"Error: {e}")
        
        # Always show manual path
        st.info(f"**Manual path:** `{folder_path}`")
        st.markdown("*Copy this path to your file explorer if the button didn't work*")

def main():
    """Main application function."""
    debug_print("Starting MeowDown Debug Version...")
    
    # Page config
    st.set_page_config(
        page_title="🐱 MeowDown - Debug Mode",
        page_icon="🐱",
        layout="centered"
    )
    
    # Simple CSS
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #ffeef8 0%, #f0e6ff 50%, #e6f3ff 100%);
        min-height: 100vh;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("# 🐱💕 MeowDown - Debug Mode 💕🐱")
    st.markdown("*Debug messages will appear in your command window!*")
    
    st.markdown("---")
    
    # Test Section
    st.markdown("## 🧪 Test Zone")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎉 Test Cat Animation!", use_container_width=True):
            debug_print("🧪 User clicked Test Cat Animation")
            show_floating_cats()
    
    with col2:
        default_folder = get_default_download_folder()
        st.write(f"**Download folder:** `{default_folder}`")
        open_folder_button(default_folder)
    
    st.markdown("---")
    
    # Info section
    st.markdown("## 📋 Debug Info")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.write(f"**Platform:** {platform.system()}")
        st.write(f"**Python:** {sys.version.split()[0]}")
        
    with info_col2:
        folder = Path(get_default_download_folder())
        st.write(f"**Folder Exists:** {folder.exists()}")
        st.write(f"**Folder Path:** `{folder}`")
    
    st.markdown("---")
    
    # URL test section
    st.markdown("## 🔗 Quick URL Test")
    
    url = st.text_input(
        "Test URL (paste any video URL):",
        placeholder="https://youtube.com/watch?v=...",
        help="This won't actually download, just tests the interface"
    )
    
    if url:
        if "youtube.com" in url or "youtu.be" in url:
            st.success("✅ Valid YouTube URL detected!")
            debug_print(f"User entered valid YouTube URL: {url[:50]}...")
        elif "http" in url:
            st.info("🔗 URL detected (non-YouTube)")
            debug_print(f"User entered URL: {url[:50]}...")
        else:
            st.warning("⚠️ That doesn't look like a URL")
    
    if st.button("🐱 Simulate Download Success!", type="primary"):
        debug_print("🧪 User clicked Simulate Download Success")
        st.success("🎉 Simulated download complete!")
        show_floating_cats()
        
        # Show the folder button after "download"
        st.markdown("### 📁 Your download is ready!")
        open_folder_button(get_default_download_folder())
    
    st.markdown("---")
    st.markdown("*Check your command window for detailed debug messages!* 🔧")

if __name__ == "__main__":
    debug_print("MeowDown Debug Version starting...")
    main()