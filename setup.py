#!/usr/bin/env python3
"""
MeowDown Setup Script 🐱
Quick setup for development or building.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_cat(message):
    """Print with cute cat emoji.""" 
    print(f"🐱 {message}")

def run_command(cmd):
    """Run a command safely."""
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"😿 Error running command: {e}")
        return False

def setup_development():
    """Setup for development."""
    print_cat("Setting up MeowDown for development...")
    
    # Install dependencies
    print_cat("Installing Python dependencies...")
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]):
        print("😿 Failed to install requirements. Trying individual packages...")
        packages = ["dearpygui", "yt-dlp", "pyperclip", "requests", "pyinstaller"]
        for package in packages:
            run_command([sys.executable, "-m", "pip", "install", package])
    
    print_cat("Development setup complete! Run 'python main.py' to start.")

def build_executable():
    """Build the executable."""
    print_cat("Building MeowDown executable...")
    if not run_command([sys.executable, "build.py"]):
        print("😿 Build failed!")
        return False
    return True

def main():
    """Main setup function."""
    print_cat("MeowDown Setup 🐾")
    print("What would you like to do?")
    print("1. Setup for development")
    print("2. Build executable")
    print("3. Both")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
    except KeyboardInterrupt:
        print("\n🐱 Bye!")
        return
    
    if choice == "1":
        setup_development()
    elif choice == "2":
        build_executable()
    elif choice == "3":
        setup_development()
        print_cat("Now building executable...")
        build_executable()
    else:
        print("😿 Invalid choice!")

if __name__ == "__main__":
    main()