#!/usr/bin/env python3
"""
Demo build script to test the executable creation process
This creates a simplified version for demonstration
"""

import sys
import os

def main():
    print("="*60)
    print("NVIDIA DLSS Updater - Demo Build")
    print("="*60)
    print()
    
    # Check if required files exist
    required_files = [
        'nvidia_dlss_updater.py',
        'nvidia_dlss_updater_cli.py',
        'build_exe.py',
        'requirements.txt'
    ]
    
    print("Checking required files...")
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - NOT FOUND")
            all_present = False
    
    if not all_present:
        print("\nError: Not all required files are present!")
        return 1
    
    print("\nAll required files are present!")
    print()
    print("To build the executable on Windows:")
    print("1. Install Python 3.8 or higher")
    print("2. Open Command Prompt as Administrator")
    print("3. Navigate to this directory")
    print("4. Run: pip install -r requirements.txt")
    print("5. Run: python build_exe.py")
    print("   OR")
    print("   Run: build_all.bat")
    print()
    print("The executable files will be created in the 'dist' folder")
    print()
    
    # Test import of main modules
    print("Testing Python modules...")
    try:
        import tkinter
        print("  ✓ tkinter (GUI support) - Available")
    except ImportError:
        print("  ✗ tkinter - Not available (GUI will not work)")
    
    try:
        import nvidia_dlss_updater
        print("  ✓ nvidia_dlss_updater module - OK")
    except Exception as e:
        print(f"  ✗ nvidia_dlss_updater module - Error: {e}")
    
    try:
        import nvidia_dlss_updater_cli
        print("  ✓ nvidia_dlss_updater_cli module - OK")
    except Exception as e:
        print(f"  ✗ nvidia_dlss_updater_cli module - Error: {e}")
    
    print()
    print("Demo complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())