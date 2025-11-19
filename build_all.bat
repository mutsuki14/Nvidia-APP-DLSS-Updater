@echo off
REM Build script for NVIDIA DLSS Updater
REM Builds both GUI and CLI versions

echo ========================================
echo NVIDIA DLSS Updater - Build Script
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/5] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo [2/5] Running build script...
python build_exe.py

echo.
echo [3/5] Building CLI version...
pyinstaller nvidia_dlss_updater_cli.py ^
    --onefile ^
    --console ^
    --name=NvidiaDLSSUpdaterCLI ^
    --clean ^
    --noconfirm ^
    --add-data="README.md;."

echo.
echo [4/5] Organizing output files...
if not exist "release" mkdir release
if exist "dist\NvidiaDLSSUpdater.exe" (
    copy "dist\NvidiaDLSSUpdater.exe" "release\NvidiaDLSSUpdater.exe"
)
if exist "dist\NvidiaDLSSUpdaterCLI.exe" (
    copy "dist\NvidiaDLSSUpdaterCLI.exe" "release\NvidiaDLSSUpdaterCLI.exe"
)
if exist "dist\RunAsAdmin.bat" (
    copy "dist\RunAsAdmin.bat" "release\RunAsAdmin.bat"
)
if exist "README.md" (
    copy "README.md" "release\README.md"
)

echo.
echo [5/5] Creating release archive...
if exist "release" (
    powershell -Command "Compress-Archive -Path 'release\*' -DestinationPath 'NvidiaDLSSUpdater_v1.0.zip' -Force"
    echo Created release archive: NvidiaDLSSUpdater_v1.0.zip
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Output files:
echo   - release\NvidiaDLSSUpdater.exe     (GUI version)
echo   - release\NvidiaDLSSUpdaterCLI.exe  (CLI version)
echo   - release\RunAsAdmin.bat            (Admin launcher)
echo   - NvidiaDLSSUpdater_v1.0.zip        (Complete package)
echo.
echo To use:
echo   1. Extract NvidiaDLSSUpdater_v1.0.zip
echo   2. Copy your DLSS .dll files to the same folder
echo   3. Run RunAsAdmin.bat or run exe as administrator
echo.
pause