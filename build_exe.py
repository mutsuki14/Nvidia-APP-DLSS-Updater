#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for creating Windows executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned: {dir_name}")
    
    # Remove .spec file if exists
    spec_files = list(Path('.').glob('*.spec'))
    for spec_file in spec_files:
        spec_file.unlink()
        print(f"Removed: {spec_file}")

def create_icon():
    """Create a simple icon for the application"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a 256x256 icon
        size = 256
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw NVIDIA-like green gradient background
        for i in range(size):
            color_value = int(255 * (1 - i / size))
            green_value = int(118 + (255 - 118) * (i / size))
            draw.rectangle([0, i, size, i+1], fill=(0, green_value, 0, 255))
        
        # Draw "DU" text (DLSS Updater)
        try:
            # Try to use a bold font if available
            font = ImageFont.truetype("arial.ttf", 100)
        except:
            font = ImageFont.load_default()
        
        # Draw white text with shadow
        text = "DU"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        # Shadow
        draw.text((x+3, y+3), text, fill=(0, 0, 0, 128), font=font)
        # Main text
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        
        # Save as ICO
        img.save('nvidia_dlss_updater.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        print("Created application icon: nvidia_dlss_updater.ico")
        return True
    except Exception as e:
        print(f"Could not create icon: {e}")
        return False

def build_executable():
    """Build the executable using PyInstaller"""
    
    # PyInstaller options
    options = [
        'nvidia_dlss_updater.py',  # Main script
        '--onefile',                # Single executable
        '--windowed',               # No console window
        '--name=NvidiaDLSSUpdater', # Executable name
        '--clean',                  # Clean temporary files
        '--noconfirm',             # Don't ask for confirmation
        '--add-data=README.md;.',   # Include README
    ]
    
    # Add icon if it exists
    if os.path.exists('nvidia_dlss_updater.ico'):
        options.extend(['--icon=nvidia_dlss_updater.ico'])
    
    # Add version information
    options.extend([
        '--version-file=version_info.txt'
    ])
    
    # Build command
    cmd = ['pyinstaller'] + options
    
    print("Building executable with PyInstaller...")
    print(f"Command: {' '.join(cmd)}")
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✓ Build successful!")
        print(f"Executable location: dist/NvidiaDLSSUpdater.exe")
        return True
    else:
        print(f"\n✗ Build failed!")
        print(f"Error: {result.stderr}")
        return False

def create_version_info():
    """Create version information file for Windows"""
    version_info = """# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx

VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    OS=0x40004,
    # The general type of file.
    fileType=0x1,
    # The function of the file.
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Open Source'),
        StringStruct(u'FileDescription', u'NVIDIA DLSS Updater - Updates NVIDIA App DLSS source files'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'NvidiaDLSSUpdater'),
        StringStruct(u'LegalCopyright', u'© 2024. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'NvidiaDLSSUpdater.exe'),
        StringStruct(u'ProductName', u'NVIDIA DLSS Updater'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    print("Created version info file: version_info.txt")

def create_batch_launcher():
    """Create a batch file to run the program as administrator"""
    batch_content = r"""@echo off
:: Request administrator privileges
:: Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

:: If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"="
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"

:: Run the program
start "" "NvidiaDLSSUpdater.exe"
"""
    
    with open('RunAsAdmin.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    print("Created batch launcher: RunAsAdmin.bat")

def main():
    """Main build process"""
    print("="*60)
    print("NVIDIA DLSS Updater - Build Script")
    print("="*60)
    
    # Step 1: Clean previous builds
    print("\n[1/6] Cleaning previous builds...")
    clean_build_dirs()
    
    # Step 2: Install dependencies
    print("\n[2/6] Installing dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                   capture_output=True)
    
    # Step 3: Create icon
    print("\n[3/6] Creating application icon...")
    create_icon()
    
    # Step 4: Create version info
    print("\n[4/6] Creating version information...")
    create_version_info()
    
    # Step 5: Build executable
    print("\n[5/6] Building executable...")
    success = build_executable()
    
    # Step 6: Create batch launcher
    if success:
        print("\n[6/6] Creating batch launcher...")
        create_batch_launcher()
        
        # Copy batch file to dist folder
        if os.path.exists('dist'):
            shutil.copy('RunAsAdmin.bat', 'dist/RunAsAdmin.bat')
            print("Copied batch launcher to dist folder")
        
        print("\n" + "="*60)
        print("✓ BUILD COMPLETE!")
        print("="*60)
        print("\nOutput files:")
        print("  - dist/NvidiaDLSSUpdater.exe  (Main executable)")
        print("  - dist/RunAsAdmin.bat         (Administrator launcher)")
        print("\nTo use the program:")
        print("  1. Copy nvngx_dlss.dll files to the same folder as the exe")
        print("  2. Double-click RunAsAdmin.bat to run with administrator privileges")
        print("  3. Or right-click NvidiaDLSSUpdater.exe and 'Run as administrator'")
    else:
        print("\n" + "="*60)
        print("✗ BUILD FAILED!")
        print("="*60)
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()