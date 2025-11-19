#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script specifically for creating proper Windows x64 executables
This script should be run on a Windows system
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def check_environment():
    """Check if running on Windows"""
    system = platform.system()
    arch = platform.machine()
    
    print(f"System: {system}")
    print(f"Architecture: {arch}")
    print(f"Python: {sys.version}")
    print(f"Python Architecture: {platform.architecture()[0]}")
    
    if system != "Windows":
        print("\n⚠️ WARNING: This script should be run on Windows for proper executable creation!")
        print("Executables created on Linux will not work on Windows.")
        return False
    
    if "64" not in platform.architecture()[0]:
        print("\n⚠️ WARNING: Using 32-bit Python. Please use 64-bit Python for 64-bit executables!")
        return False
    
    return True

def install_requirements():
    """Install required packages"""
    requirements = [
        "pyinstaller>=6.0.0",
        "pillow>=10.0.0",
        "colorama>=0.4.6"
    ]
    
    print("\nInstalling requirements...")
    for req in requirements:
        subprocess.run([sys.executable, "-m", "pip", "install", req], 
                      capture_output=True)
    print("✓ Requirements installed")

def create_spec_file_gui():
    """Create a proper spec file for GUI executable"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['nvidia_dlss_updater.py'],
    pathex=[],
    binaries=[],
    datas=[('README.md', '.')],
    hiddenimports=['tkinter', 'ctypes', 'shutil', 'pathlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NvidiaDLSSUpdater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='x86_64',
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon='nvidia_dlss_updater.ico' if os.path.exists('nvidia_dlss_updater.ico') else None
)
"""
    
    with open('nvidia_dlss_updater.spec', 'w') as f:
        f.write(spec_content)
    print("Created GUI spec file")

def create_spec_file_cli():
    """Create a proper spec file for CLI executable"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['nvidia_dlss_updater_cli.py'],
    pathex=[],
    binaries=[],
    datas=[('README.md', '.')],
    hiddenimports=['colorama', 'ctypes', 'shutil', 'pathlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NvidiaDLSSUpdaterCLI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='x86_64',
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon='nvidia_dlss_updater.ico' if os.path.exists('nvidia_dlss_updater.ico') else None
)
"""
    
    with open('nvidia_dlss_updater_cli.spec', 'w') as f:
        f.write(spec_content)
    print("Created CLI spec file")

def build_executables():
    """Build the executables using the spec files"""
    print("\nBuilding GUI executable...")
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "nvidia_dlss_updater.spec",
        "--clean",
        "--noconfirm"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"GUI build failed: {result.stderr}")
        return False
    print("✓ GUI executable built")
    
    print("\nBuilding CLI executable...")
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "nvidia_dlss_updater_cli.spec",
        "--clean",
        "--noconfirm"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"CLI build failed: {result.stderr}")
        return False
    print("✓ CLI executable built")
    
    return True

def verify_executables():
    """Verify that executables are 64-bit Windows PE files"""
    import struct
    
    exe_files = [
        'dist/NvidiaDLSSUpdater.exe',
        'dist/NvidiaDLSSUpdaterCLI.exe'
    ]
    
    for exe_path in exe_files:
        if not os.path.exists(exe_path):
            print(f"✗ {exe_path} not found")
            continue
        
        with open(exe_path, 'rb') as f:
            # Check DOS header
            dos_header = f.read(2)
            if dos_header != b'MZ':
                print(f"✗ {exe_path} is not a valid Windows executable")
                continue
            
            # Get PE header offset
            f.seek(0x3C)
            pe_offset = struct.unpack('<I', f.read(4))[0]
            
            # Check PE signature
            f.seek(pe_offset)
            pe_sig = f.read(4)
            if pe_sig != b'PE\x00\x00':
                print(f"✗ {exe_path} has invalid PE signature")
                continue
            
            # Check machine type (0x8664 = AMD64)
            machine = struct.unpack('<H', f.read(2))[0]
            if machine == 0x8664:
                print(f"✓ {exe_path} is a valid 64-bit Windows executable")
            elif machine == 0x014c:
                print(f"⚠️ {exe_path} is a 32-bit executable (not recommended)")
            else:
                print(f"✗ {exe_path} has unknown architecture: {hex(machine)}")

def main():
    print("="*60)
    print("NVIDIA DLSS Updater - Windows x64 Build")
    print("="*60)
    
    # Check environment
    if not check_environment():
        print("\nPlease run this script on a 64-bit Windows system with 64-bit Python!")
        return 1
    
    # Install requirements
    install_requirements()
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    for path in ['build', 'dist', '*.spec']:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    
    # Create spec files
    print("\nCreating spec files...")
    create_spec_file_gui()
    create_spec_file_cli()
    
    # Build executables
    if not build_executables():
        print("\n✗ Build failed!")
        return 1
    
    # Verify executables
    print("\nVerifying executables...")
    verify_executables()
    
    # Create release package
    print("\nCreating release package...")
    os.makedirs('release', exist_ok=True)
    
    files_to_copy = [
        ('dist/NvidiaDLSSUpdater.exe', 'release/NvidiaDLSSUpdater.exe'),
        ('dist/NvidiaDLSSUpdaterCLI.exe', 'release/NvidiaDLSSUpdaterCLI.exe'),
        ('README.md', 'release/README.md'),
        ('README_EXE.md', 'release/README_EXE.md')
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {dst}")
    
    # Create RunAsAdmin.bat
    with open('release/RunAsAdmin.bat', 'w') as f:
        f.write('@echo off\n')
        f.write(':: Auto-run as Administrator\n')
        f.write('cd /d "%~dp0"\n')
        f.write('NvidiaDLSSUpdater.exe\n')
    
    print("\n" + "="*60)
    print("✓ Build complete!")
    print("="*60)
    print("\nOutput files in 'release' folder:")
    print("  - NvidiaDLSSUpdater.exe (64-bit)")
    print("  - NvidiaDLSSUpdaterCLI.exe (64-bit)")
    print("  - RunAsAdmin.bat")
    print("\nThese executables are properly built for 64-bit Windows.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())