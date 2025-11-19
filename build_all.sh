#!/bin/bash

# Build script for NVIDIA DLSS Updater
# For building Windows executables on Linux/Mac using Wine

echo "========================================"
echo "NVIDIA DLSS Updater - Build Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Install dependencies
echo "[1/5] Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "[2/5] Running build script..."
python3 build_exe.py

echo ""
echo "[3/5] Building CLI version..."
python3 -m PyInstaller nvidia_dlss_updater_cli.py \
    --onefile \
    --console \
    --name=NvidiaDLSSUpdaterCLI \
    --clean \
    --noconfirm \
    --add-data="README.md:."

echo ""
echo "[4/5] Organizing output files..."
mkdir -p release
[ -f "dist/NvidiaDLSSUpdater.exe" ] && cp "dist/NvidiaDLSSUpdater.exe" "release/"
[ -f "dist/NvidiaDLSSUpdaterCLI.exe" ] && cp "dist/NvidiaDLSSUpdaterCLI.exe" "release/"
[ -f "dist/RunAsAdmin.bat" ] && cp "dist/RunAsAdmin.bat" "release/"
[ -f "README.md" ] && cp "README.md" "release/"

echo ""
echo "[5/5] Creating release archive..."
if [ -d "release" ]; then
    zip -r "NvidiaDLSSUpdater_v1.0.zip" release/
    echo "Created release archive: NvidiaDLSSUpdater_v1.0.zip"
fi

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Output files:"
echo "  - release/NvidiaDLSSUpdater.exe     (GUI version)"
echo "  - release/NvidiaDLSSUpdaterCLI.exe  (CLI version)"
echo "  - release/RunAsAdmin.bat            (Admin launcher)"
echo "  - NvidiaDLSSUpdater_v1.0.zip        (Complete package)"
echo ""
echo "To use:"
echo "  1. Extract NvidiaDLSSUpdater_v1.0.zip"
echo "  2. Copy your DLSS .dll files to the same folder"
echo "  3. Run RunAsAdmin.bat or run exe as administrator"
echo ""