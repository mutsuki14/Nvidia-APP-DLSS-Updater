@echo off
REM Windows native build script for NVIDIA DLSS Updater
REM This script must be run on a Windows system with Python installed

echo ============================================
echo NVIDIA DLSS Updater - Windows Native Build
echo ============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/7] Installing required packages...
python -m pip install --upgrade pip
python -m pip install pyinstaller>=6.0.0 pillow>=10.0.0 colorama>=0.4.6

echo.
echo [2/7] Creating application icon...
python -c "from PIL import Image, ImageDraw; size=256; img=Image.new('RGBA',(size,size),(0,0,0,0)); draw=ImageDraw.Draw(img); [draw.rectangle([0,i,size,i+1],fill=(0,int(76+(200-76)*(i/size)),0,255)) for i in range(size)]; draw.rectangle([0,0,size-1,size-1],outline=(255,255,255,128),width=3); draw.ellipse([60,80,120,176],fill=(255,255,255,255)); draw.rectangle([60,80,90,176],fill=(255,255,255,255)); draw.ellipse([70,90,110,166],fill=(0,150,0,255)); draw.rectangle([70,90,90,166],fill=(0,150,0,255)); draw.rectangle([136,80,156,156],fill=(255,255,255,255)); draw.rectangle([176,80,196,156],fill=(255,255,255,255)); draw.ellipse([136,136,196,176],fill=(255,255,255,255)); draw.ellipse([146,146,186,166],fill=(0,150,0,255)); img.save('nvidia_dlss_updater.ico','ICO',sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)]); print('Icon created successfully')" 2>nul || echo Icon creation skipped

echo.
echo [3/7] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

echo.
echo [4/7] Building GUI executable (64-bit)...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name=NvidiaDLSSUpdater ^
    --icon=nvidia_dlss_updater.ico ^
    --add-data="README.md;." ^
    --hidden-import=tkinter ^
    --hidden-import=ctypes ^
    --hidden-import=shutil ^
    --hidden-import=pathlib ^
    --uac-admin ^
    --target-arch=x86_64 ^
    nvidia_dlss_updater.py

if %errorlevel% neq 0 (
    echo ERROR: Failed to build GUI executable
    pause
    exit /b 1
)

echo.
echo [5/7] Building CLI executable (64-bit)...
pyinstaller ^
    --onefile ^
    --console ^
    --name=NvidiaDLSSUpdaterCLI ^
    --icon=nvidia_dlss_updater.ico ^
    --add-data="README.md;." ^
    --hidden-import=colorama ^
    --hidden-import=ctypes ^
    --hidden-import=shutil ^
    --hidden-import=pathlib ^
    --uac-admin ^
    --target-arch=x86_64 ^
    nvidia_dlss_updater_cli.py

if %errorlevel% neq 0 (
    echo ERROR: Failed to build CLI executable
    pause
    exit /b 1
)

echo.
echo [6/7] Creating release folder...
if not exist release mkdir release
copy /y dist\NvidiaDLSSUpdater.exe release\
copy /y dist\NvidiaDLSSUpdaterCLI.exe release\
copy /y README.md release\
copy /y README_EXE.md release\

REM Create RunAsAdmin.bat in release folder
echo @echo off > release\RunAsAdmin.bat
echo :: Auto-run as Administrator >> release\RunAsAdmin.bat
echo cd /d "%%~dp0" >> release\RunAsAdmin.bat
echo NvidiaDLSSUpdater.exe >> release\RunAsAdmin.bat

echo.
echo [7/7] Creating release archive...
cd release
powershell -Command "Compress-Archive -Path '*' -DestinationPath '../NvidiaDLSSUpdater_v1.0.0_Win64.zip' -Force"
cd ..

echo.
echo ============================================
echo Build Complete!
echo ============================================
echo.
echo Output files (64-bit Windows):
echo   - release\NvidiaDLSSUpdater.exe
echo   - release\NvidiaDLSSUpdaterCLI.exe
echo   - release\RunAsAdmin.bat
echo   - NvidiaDLSSUpdater_v1.0.0_Win64.zip
echo.
echo The executables are now properly compiled for 64-bit Windows.
echo.
pause