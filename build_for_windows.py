#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Windows executables in Linux environment
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
        from PIL import Image, ImageDraw
        
        # Create a 256x256 icon
        size = 256
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw NVIDIA-like green gradient background
        for i in range(size):
            green_value = int(76 + (200 - 76) * (i / size))
            draw.rectangle([0, i, size, i+1], fill=(0, green_value, 0, 255))
        
        # Draw border
        draw.rectangle([0, 0, size-1, size-1], outline=(255, 255, 255, 128), width=3)
        
        # Draw "DU" text (DLSS Updater) - simplified without font
        # Create a simple "D" shape
        draw.ellipse([60, 80, 120, 176], fill=(255, 255, 255, 255))
        draw.rectangle([60, 80, 90, 176], fill=(255, 255, 255, 255))
        draw.ellipse([70, 90, 110, 166], fill=(0, 150, 0, 255))
        draw.rectangle([70, 90, 90, 166], fill=(0, 150, 0, 255))
        
        # Create a simple "U" shape
        draw.rectangle([136, 80, 156, 156], fill=(255, 255, 255, 255))
        draw.rectangle([176, 80, 196, 156], fill=(255, 255, 255, 255))
        draw.ellipse([136, 136, 196, 176], fill=(255, 255, 255, 255))
        draw.ellipse([146, 146, 186, 166], fill=(0, 150, 0, 255))
        
        # Save as ICO (save as PNG first, then convert)
        img.save('nvidia_dlss_updater.png', format='PNG')
        print("Created application icon: nvidia_dlss_updater.png")
        return True
    except Exception as e:
        print(f"Could not create icon: {e}")
        return False

def build_gui_executable():
    """Build the GUI executable"""
    
    # PyInstaller options for GUI
    options = [
        'nvidia_dlss_updater.py',
        '--onefile',
        '--windowed',
        '--name=NvidiaDLSSUpdater',
        '--clean',
        '--noconfirm',
        '--distpath=./dist',
        '--workpath=./build',
        '--specpath=.',
    ]
    
    # Add icon if it exists
    if os.path.exists('nvidia_dlss_updater.png'):
        options.extend(['--icon=nvidia_dlss_updater.png'])
    
    print("Building GUI executable...")
    result = subprocess.run(['pyinstaller'] + options, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ GUI build successful!")
        return True
    else:
        print(f"✗ GUI build failed: {result.stderr}")
        return False

def build_cli_executable():
    """Build the CLI executable"""
    
    # PyInstaller options for CLI
    options = [
        'nvidia_dlss_updater_cli.py',
        '--onefile',
        '--console',
        '--name=NvidiaDLSSUpdaterCLI',
        '--clean',
        '--noconfirm',
        '--distpath=./dist',
        '--workpath=./build',
        '--specpath=.',
    ]
    
    print("Building CLI executable...")
    result = subprocess.run(['pyinstaller'] + options, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ CLI build successful!")
        return True
    else:
        print(f"✗ CLI build failed: {result.stderr}")
        return False

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
start "" "NvidiaDLSSUpdater"
"""
    
    launcher_path = 'dist/RunAsAdmin.bat'
    os.makedirs('dist', exist_ok=True)
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    print(f"Created batch launcher: {launcher_path}")

def create_release_package():
    """Create release package with all files"""
    release_dir = 'release'
    
    # Clean and create release directory
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Files to include in release
    files_to_copy = [
        ('dist/NvidiaDLSSUpdater', 'NvidiaDLSSUpdater.exe'),
        ('dist/NvidiaDLSSUpdaterCLI', 'NvidiaDLSSUpdaterCLI.exe'),
        ('dist/RunAsAdmin.bat', 'RunAsAdmin.bat'),
        ('README.md', 'README.md'),
        ('README_EXE.md', 'README_EXE.md'),
    ]
    
    copied_count = 0
    for src, dst in files_to_copy:
        dst_path = os.path.join(release_dir, dst)
        if os.path.exists(src):
            shutil.copy2(src, dst_path)
            print(f"Copied: {dst}")
            copied_count += 1
        else:
            # Try without extension for Linux builds
            src_no_ext = src.replace('.exe', '')
            if os.path.exists(src_no_ext):
                # For Linux-built executables, add .exe extension
                shutil.copy2(src_no_ext, dst_path)
                print(f"Copied: {dst}")
                copied_count += 1
            else:
                print(f"Warning: {src} not found")
    
    # Create ZIP archive
    if copied_count > 0:
        archive_name = 'NvidiaDLSSUpdater_v1.0.0'
        shutil.make_archive(archive_name, 'zip', release_dir)
        print(f"\n✓ Created release archive: {archive_name}.zip")
        return f"{archive_name}.zip"
    
    return None

def main():
    """Main build process"""
    print("="*60)
    print("NVIDIA DLSS Updater - Windows Build (Linux Environment)")
    print("="*60)
    
    # Step 1: Clean previous builds
    print("\n[1/6] Cleaning previous builds...")
    clean_build_dirs()
    
    # Step 2: Create icon
    print("\n[2/6] Creating application icon...")
    create_icon()
    
    # Step 3: Build GUI executable
    print("\n[3/6] Building GUI executable...")
    gui_success = build_gui_executable()
    
    # Step 4: Build CLI executable
    print("\n[4/6] Building CLI executable...")
    cli_success = build_cli_executable()
    
    # Step 5: Create batch launcher
    print("\n[5/6] Creating batch launcher...")
    create_batch_launcher()
    
    # Step 6: Create release package
    print("\n[6/6] Creating release package...")
    archive = create_release_package()
    
    print("\n" + "="*60)
    if gui_success and cli_success and archive:
        print("✓ BUILD COMPLETE!")
        print("="*60)
        print(f"\nRelease archive created: {archive}")
        print("\nNote: These are Linux-built executables.")
        print("For true Windows executables, build on a Windows system.")
    else:
        print("✗ BUILD PARTIALLY FAILED!")
        print("="*60)
        print("Check the error messages above.")
    
    return 0 if (gui_success and cli_success) else 1

if __name__ == "__main__":
    sys.exit(main())