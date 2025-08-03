#!/usr/bin/env python3
"""
Quick test script for MeowDown functionality
"""

import sys
import importlib.util
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    required_modules = [
        'dearpygui.dearpygui',
        'yt_dlp', 
        'requests',
        'pyperclip',
        'urllib.parse',
        'threading',
        'subprocess',
        'pathlib'
    ]
    
    failed = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  OK {module}")
        except ImportError as e:
            print(f"  FAIL {module}: {e}")
            failed.append(module)
    
    return len(failed) == 0

def test_main_script():
    """Test that main script can be imported."""
    print("\nTesting main script...")
    try:
        import main
        print("  OK main.py imports successfully")
        
        # Test some key functions exist
        functions_to_check = [
            'is_valid_url',
            'get_default_download_folder', 
            'setup_dependencies',
            'download_video',
            'launch_meowdown'
        ]
        
        for func_name in functions_to_check:
            if hasattr(main, func_name):
                print(f"  OK Function {func_name} exists")
            else:
                print(f"  FAIL Function {func_name} missing")
                return False
        
        return True
    except Exception as e:
        print(f"  FAIL Failed to import main.py: {e}")
        return False

def test_url_validation():
    """Test URL validation function."""
    print("\nTesting URL validation...")
    try:
        import main
        
        test_cases = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
            ("https://youtu.be/dQw4w9WgXcQ", True),
            ("not a url", False),
            ("", False),
            ("ftp://example.com", True),  # Valid URL but not http(s)
        ]
        
        all_passed = True
        for url, expected in test_cases:
            result = main.is_valid_url(url)
            if result == expected:
                print(f"  OK '{url}' -> {result}")
            else:
                print(f"  FAIL '{url}' -> {result} (expected {expected})")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"  FAIL URL validation test failed: {e}")
        return False

def main_test():
    """Run all tests."""
    print("MeowDown Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Main Script Test", test_main_script), 
        ("URL Validation Test", test_url_validation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        try:
            if test_func():
                print(f"PASS {test_name}")
                passed += 1
            else:
                print(f"FAIL {test_name}")
        except Exception as e:
            print(f"CRASH {test_name}: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("All tests passed! MeowDown is ready!")
        return True
    else:
        print("Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main_test()
    sys.exit(0 if success else 1)