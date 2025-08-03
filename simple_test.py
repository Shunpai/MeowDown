#!/usr/bin/env python3
"""
MeowDown Simple Debug Test
Run this to test functionality with console output.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import time

def debug_print(message, level="INFO"):
    """Print debug messages."""
    timestamp = time.strftime("%H:%M:%S")
    if level == "ERROR":
        print(f"[{timestamp}] ERROR: {message}")
    elif level == "SUCCESS":
        print(f"[{timestamp}] SUCCESS: {message}")
    elif level == "WARNING":
        print(f"[{timestamp}] WARNING: {message}")
    else:
        print(f"[{timestamp}] INFO: {message}")

def test_folder_opening():
    """Test different methods of opening folders."""
    print("\n=== FOLDER OPENING TEST ===")
    
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
            ("Method 1 - explorer", ["explorer", test_folder]),
            ("Method 2 - cmd start", ["cmd", "/c", "start", test_folder]),
        ]
        
        for method_name, cmd in methods:
            try:
                debug_print(f"Trying: {method_name}")
                debug_print(f"Command: {' '.join(cmd)}")
                
                result = subprocess.run(cmd, check=True, capture_output=True, timeout=5)
                debug_print(f"SUCCESS: {method_name} worked!", "SUCCESS")
                debug_print(f"Return code: {result.returncode}")
                return True
                
            except subprocess.TimeoutExpired:
                debug_print(f"TIMEOUT: {method_name} took too long", "WARNING")
            except subprocess.CalledProcessError as e:
                debug_print(f"PROCESS ERROR: {method_name} failed: {e}", "ERROR")
                debug_print(f"Return code: {e.returncode}")
                if e.stderr:
                    debug_print(f"Stderr: {e.stderr.decode()}")
            except Exception as e:
                debug_print(f"EXCEPTION: {method_name} failed: {str(e)}", "ERROR")
                debug_print(f"Exception type: {type(e).__name__}")
        
        # Try os.startfile as backup
        try:
            debug_print("Trying: Method 3 - os.startfile")
            os.startfile(test_folder)
            debug_print("SUCCESS: os.startfile worked!", "SUCCESS")
            return True
        except Exception as e:
            debug_print(f"EXCEPTION: os.startfile failed: {str(e)}", "ERROR")
    
    return False

def test_imports():
    """Test importing required modules."""
    print("\n=== IMPORT TEST ===")
    
    modules = [
        "streamlit",
        "yt_dlp", 
        "requests"
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            __import__(module)
            debug_print(f"OK: {module}")
        except ImportError as e:
            debug_print(f"FAILED: {module} - {e}", "ERROR")
            failed_imports.append(module)
    
    if failed_imports:
        debug_print(f"Missing modules: {', '.join(failed_imports)}", "ERROR")
        return False
    else:
        debug_print("All imports successful!", "SUCCESS")
        return True

def test_app_loading():
    """Test if the main app can be imported."""
    print("\n=== APP LOADING TEST ===")
    
    try:
        # Check if app.py exists
        if not Path("app.py").exists():
            debug_print("app.py file not found!", "ERROR")
            return False
        
        debug_print("app.py file exists")
        
        # Try to import
        import app
        debug_print("app.py imported successfully!", "SUCCESS")
        
        # Test some key functions exist
        functions = ['show_floating_cats', 'get_default_download_folder']
        
        for func_name in functions:
            if hasattr(app, func_name):
                debug_print(f"Function {func_name} exists")
            else:
                debug_print(f"Function {func_name} missing", "ERROR")
        
        return True
        
    except Exception as e:
        debug_print(f"Failed to import app.py: {str(e)}", "ERROR")
        debug_print(f"Exception type: {type(e).__name__}")
        return False

def main():
    """Run all debug tests."""
    print("MeowDown Debug Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("App Loading Test", test_app_loading),
        ("Folder Opening Test", test_folder_opening)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                debug_print(f"PASSED: {test_name}", "SUCCESS")
                passed += 1
            else:
                debug_print(f"FAILED: {test_name}", "ERROR")
        except Exception as e:
            debug_print(f"CRASHED: {test_name} - {e}", "ERROR")
    
    print(f"\n{'='*40}")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! MeowDown should work!")
    else:
        print("Some tests failed. Check errors above.")

if __name__ == "__main__":
    main()