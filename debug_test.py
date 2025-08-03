#!/usr/bin/env python3
"""
🐱 MeowDown Debug Test Script
Run this to test functionality with detailed console output.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import time

def debug_print(message, level="INFO"):
    """Print debug messages with cat emojis."""
    timestamp = time.strftime("%H:%M:%S")
    if level == "ERROR":
        print(f"[{timestamp}] 😿 ERROR: {message}")
    elif level == "SUCCESS":
        print(f"[{timestamp}] 😸 SUCCESS: {message}")
    elif level == "WARNING":
        print(f"[{timestamp}] 😼 WARNING: {message}")
    else:
        print(f"[{timestamp}] 🐱 INFO: {message}")

def test_folder_opening():
    """Test different methods of opening folders."""
    debug_print("🧪 Testing folder opening methods...")
    
    # Get default downloads folder
    downloads = Path.home() / "Downloads"
    if downloads.exists():
        test_folder = str(downloads)
    else:
        test_folder = str(Path.cwd())
    
    debug_print(f"Test folder: {test_folder}")
    debug_print(f"Folder exists: {Path(test_folder).exists()}")
    debug_print(f"Platform: {platform.system()}")
    
    if platform.system() == "Windows":
        methods = [
            ("explorer", lambda path: subprocess.run(["explorer", path], check=True, capture_output=True, timeout=5)),
            ("cmd start", lambda path: subprocess.run(["cmd", "/c", "start", path], check=True, capture_output=True, timeout=5)),
            ("os.startfile", lambda path: os.startfile(path))
        ]
        
        for method_name, method_func in methods:
            try:
                debug_print(f"Trying method: {method_name}")
                method_func(test_folder)
                debug_print(f"✅ {method_name} succeeded!", "SUCCESS")
                return True
            except Exception as e:
                debug_print(f"❌ {method_name} failed: {str(e)}", "ERROR")
                debug_print(f"Exception type: {type(e).__name__}")
    
    return False

def test_imports():
    """Test importing required modules."""
    debug_print("🧪 Testing imports...")
    
    modules = [
        "streamlit",
        "yt_dlp", 
        "requests",
        "pathlib",
        "subprocess",
        "platform"
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            __import__(module)
            debug_print(f"✅ {module} - OK")
        except ImportError as e:
            debug_print(f"❌ {module} - FAILED: {e}", "ERROR")
            failed_imports.append(module)
    
    if failed_imports:
        debug_print(f"Missing modules: {', '.join(failed_imports)}", "ERROR")
        return False
    else:
        debug_print("All imports successful!", "SUCCESS")
        return True

def test_app_loading():
    """Test if the main app can be imported."""
    debug_print("🧪 Testing app.py import...")
    
    try:
        # Try to import the main app
        import app
        debug_print("✅ app.py imported successfully!", "SUCCESS")
        
        # Test some key functions exist
        functions_to_check = [
            'show_floating_cats',
            'play_meow_sound', 
            'get_default_download_folder',
            'check_dependencies'
        ]
        
        for func_name in functions_to_check:
            if hasattr(app, func_name):
                debug_print(f"✅ Function {func_name} exists")
            else:
                debug_print(f"❌ Function {func_name} missing", "ERROR")
        
        return True
        
    except Exception as e:
        debug_print(f"❌ Failed to import app.py: {str(e)}", "ERROR")
        debug_print(f"Exception type: {type(e).__name__}")
        return False

def test_streamlit_launch():
    """Test if Streamlit can launch the app."""
    debug_print("🧪 Testing Streamlit launch...")
    
    try:
        # Try to run streamlit --help to see if it works
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            debug_print("✅ Streamlit command works", "SUCCESS")
            
            # Try to validate the app file
            if Path("app.py").exists():
                debug_print("✅ app.py file exists")
                
                # Test streamlit config check (non-blocking)
                try:
                    result = subprocess.run([
                        sys.executable, "-c", 
                        "import streamlit as st; import app; print('Streamlit app validation OK')"
                    ], capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        debug_print("✅ Streamlit app validation passed", "SUCCESS")
                        debug_print("🎉 Ready to run: streamlit run app.py")
                        return True
                    else:
                        debug_print(f"❌ App validation failed: {result.stderr}", "ERROR")
                        
                except Exception as e:
                    debug_print(f"❌ App validation error: {e}", "ERROR")
            else:
                debug_print("❌ app.py file not found", "ERROR")
        else:
            debug_print(f"❌ Streamlit command failed: {result.stderr}", "ERROR")
            
    except Exception as e:
        debug_print(f"❌ Streamlit test failed: {str(e)}", "ERROR")
    
    return False

def main():
    """Run all debug tests."""
    print("🐱💕 MeowDown Debug Test Suite 💕🐱")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("App Loading Test", test_app_loading),
        ("Folder Opening Test", test_folder_opening),
        ("Streamlit Launch Test", test_streamlit_launch)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                debug_print(f"✅ {test_name} PASSED", "SUCCESS")
                passed += 1
            else:
                debug_print(f"❌ {test_name} FAILED", "ERROR")
        except Exception as e:
            debug_print(f"💥 {test_name} CRASHED: {e}", "ERROR")
    
    print(f"\n{'='*50}")
    print(f"🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MeowDown should work perfectly! 🐱")
        print("\n🚀 To run the app:")
        print("   setup_and_run.bat")
        print("   OR")
        print("   streamlit run app.py")
    else:
        print("😿 Some tests failed. Check the errors above.")
        print("\n🔧 Try running setup_and_run.bat to fix dependencies.")

if __name__ == "__main__":
    main()