#!/usr/bin/env python3
"""
MeowDown Launcher
Launches the Streamlit app with proper configuration.
"""

import subprocess
import sys
import os
import multiprocessing
import time
import webbrowser
from pathlib import Path

def main():
    """Launch the Streamlit app."""
    print("Starting MeowDown...")
    
    # Prevent multiple instances using process detection
    import tempfile
    
    # Check for running streamlit processes
    try:
        result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe"], 
                              capture_output=True, text=True)
        if "streamlit" in result.stdout.lower():
            print("MeowDown may already be running!")
            print("Check your browser for http://localhost:8501")
            print("If not working, close any Python/Streamlit processes first.")
            input("Press Enter to exit...")
            return
    except:
        pass  # Continue if process check fails
    
    # Create simple lock file as backup
    lock_file = Path(tempfile.gettempdir()) / "meowdown.lock" 
    try:
        # Clean up any old lock files first
        if lock_file.exists():
            lock_file.unlink()
        lock_file.write_text("running")
    except:
        pass  # Continue even if lock file fails
    
    # Get the directory where this script is located  
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        app_dir = Path(sys._MEIPASS)
        print(f"Running from PyInstaller bundle: {app_dir}")
    else:
        # Running as script
        app_dir = Path(__file__).parent
        print(f"Running from script directory: {app_dir}")
    
    app_script = app_dir / "app.py"
    
    if not app_script.exists():
        print("Error: app.py not found!")
        print(f"Looking in: {app_dir}")
        try:
            print(f"Available files: {list(app_dir.glob('*'))}")
        except:
            print("Could not list directory contents")
        input("Press Enter to exit...")
        return
    
    print(f"Found app.py at: {app_script}")
    
    # Launch Streamlit with EXACT SAME parameters as working batch file
    cmd = [
        "streamlit", "run", str(app_script),
        "--server.port", "8501", 
        "--browser.gatherUsageStats", "false",
        "--theme.base", "light",
        "--theme.primaryColor", "#667eea"
    ]
    
    print(f"Command: {' '.join(cmd)}")
    
    try:
        print("Launching Streamlit server...")
        print("This will open in your browser at http://localhost:8501")
        print("Only ONE tab will open!")
        
        # Start Streamlit normally (let it handle browser opening)
        process = subprocess.Popen(
            cmd,
            text=True,
            creationflags=0 if sys.platform != "win32" else 0
        )
        
        print("MeowDown is running!")
        print("Close this window to stop the server.")
        print("Press Ctrl+C to stop...")
        
        # Wait for the process to complete or be interrupted
        try:
            process.wait()
        except KeyboardInterrupt:
            print("Stopping MeowDown...")
            process.terminate()
            process.wait()
            
    except FileNotFoundError:
        print("Error: Streamlit not found!")
        print("Make sure Streamlit is installed: pip install streamlit")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"Error starting MeowDown: {e}")
        input("Press Enter to exit...")
        
    # Clean up lock file
    try:
        if 'lock_file' in locals() and lock_file.exists():
            lock_file.unlink()
    except:
        pass

if __name__ == "__main__":
    # Critical fix for PyInstaller multiprocessing issues
    multiprocessing.freeze_support()
    main()
