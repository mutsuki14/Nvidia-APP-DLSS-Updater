# Build Instructions for Windows Executables

## ⚠️ Important Notice

The executables in the v1.0.0 release were built on Linux and are **NOT compatible with Windows**. Please follow these instructions to build proper Windows executables.

## 🛠️ Prerequisites

1. **Windows 10/11 (64-bit)**
2. **Python 3.8+ (64-bit version)**
   - Download from: https://www.python.org/downloads/
   - **IMPORTANT**: Make sure to download the **64-bit** version
   - During installation, check "Add Python to PATH"
3. **Git** (optional, for cloning the repository)
   - Download from: https://git-scm.com/download/win

## 📋 Build Instructions

### Method 1: Automated Build (Recommended)

1. **Clone or download the repository**
   ```cmd
   git clone https://github.com/mutsuki14/Nvidia-APP-DLSS-Updater.git
   cd Nvidia-APP-DLSS-Updater
   ```
   Or download the source code ZIP from GitHub and extract it.

2. **Run the Windows build script**
   ```cmd
   build_windows.bat
   ```
   This will:
   - Install required Python packages
   - Create application icon
   - Build both GUI and CLI executables (64-bit)
   - Create release folder with all files
   - Generate a ZIP archive

### Method 2: Python Build Script

1. **Open Command Prompt or PowerShell**

2. **Navigate to the project directory**
   ```cmd
   cd path\to\Nvidia-APP-DLSS-Updater
   ```

3. **Run the Python build script**
   ```cmd
   python build_windows_fixed.py
   ```

### Method 3: Manual Build

1. **Install required packages**
   ```cmd
   pip install pyinstaller>=6.0.0 pillow>=10.0.0 colorama>=0.4.6
   ```

2. **Build GUI executable**
   ```cmd
   pyinstaller --onefile --windowed --name=NvidiaDLSSUpdater --uac-admin --target-arch=x86_64 nvidia_dlss_updater.py
   ```

3. **Build CLI executable**
   ```cmd
   pyinstaller --onefile --console --name=NvidiaDLSSUpdaterCLI --uac-admin --target-arch=x86_64 nvidia_dlss_updater_cli.py
   ```

## ✅ Verification

After building, verify the executables are 64-bit:

1. Right-click on the `.exe` file
2. Select "Properties"
3. Go to "Compatibility" tab
4. It should NOT show "Run this program in compatibility mode for Windows XP" or any 32-bit options

Or use PowerShell:
```powershell
[System.Reflection.AssemblyName]::GetAssemblyName(".\dist\NvidiaDLSSUpdater.exe") | Select-Object ProcessorArchitecture
```
Should output: `Amd64` (for 64-bit)

## 📦 Output Files

After successful build, you'll find:

```
release/
├── NvidiaDLSSUpdater.exe      # GUI version (64-bit)
├── NvidiaDLSSUpdaterCLI.exe   # CLI version (64-bit)
├── RunAsAdmin.bat             # Administrator launcher
├── README.md                  # Documentation
└── README_EXE.md             # Executable documentation

NvidiaDLSSUpdater_v1.0.0_Win64.zip  # Complete package
```

## 🐛 Troubleshooting

### "Not a valid Win32 application" error
- The executable was built on Linux. Build it on Windows instead.

### "This app can't run on your PC" error
- Make sure you're using 64-bit Python on 64-bit Windows
- Rebuild using the instructions above

### Python not found
- Ensure Python is installed and added to PATH
- Try using `py` instead of `python`: `py build_windows_fixed.py`

### PyInstaller not found
- Install it: `pip install pyinstaller`

### Build fails with "target-arch" error
- Use an older version of PyInstaller: `pip install pyinstaller==5.13.2`

## 🔧 Advanced Options

### Building for specific Windows versions

Add to PyInstaller command:
- `--target-arch=x86_64` - Force 64-bit build
- `--version-file=version_info.txt` - Add version information
- `--manifest=app.manifest` - Custom manifest for Windows compatibility

### Creating a universal installer

Consider using:
- **NSIS**: https://nsis.sourceforge.io/
- **Inno Setup**: https://jrsoftware.org/isinfo.php
- **WiX Toolset**: https://wixtoolset.org/

## 📝 Notes for Developers

1. **Always build on the target platform**: Windows executables should be built on Windows
2. **Use virtual environments**: `python -m venv venv` to isolate dependencies
3. **Test on clean systems**: Verify executables work without Python installed
4. **Code signing**: Consider signing executables to avoid Windows Defender warnings

## 🆘 Getting Help

If you encounter issues:

1. Check the [Issues](https://github.com/mutsuki14/Nvidia-APP-DLSS-Updater/issues) page
2. Create a new issue with:
   - Your Windows version
   - Python version (`python --version`)
   - Error messages
   - Build log output

## 📄 License

This build process is part of the NVIDIA DLSS Updater project. See LICENSE file for details.