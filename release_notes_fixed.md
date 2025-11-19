# NVIDIA DLSS Updater v1.0.0

## ⚠️ 重要提示 / IMPORTANT NOTICE

**当前发布的可执行文件是在Linux环境下构建的，不兼容Windows系统。请按照以下说明在Windows上重新构建。**

**The executables in this release were built on Linux and are NOT compatible with Windows. Please follow the instructions below to rebuild on Windows.**

## 🔧 如何修复 / How to Fix

1. 下载源代码 / Download source code
2. 在Windows系统上运行 / Run on Windows system:
   ```cmd
   build_windows.bat
   ```
3. 使用生成的 release 文件夹中的可执行文件 / Use executables from the generated release folder

详细说明 / Detailed instructions: [BUILD_INSTRUCTIONS.md](https://github.com/mutsuki14/Nvidia-APP-DLSS-Updater/blob/main/BUILD_INSTRUCTIONS.md)

---

## 🎉 首次发布 / Initial Release

这是 NVIDIA DLSS Updater 的首个正式版本，将原本的 PowerShell 脚本转换为独立的可执行程序。

This is the first official release of NVIDIA DLSS Updater, converting the original PowerShell script into standalone executables.

## ✨ 主要特性 / Key Features

- 🖥️ **图形界面版本** / GUI Version - 用户友好的界面
- 💻 **命令行版本** / CLI Version - 支持自动化
- 🔄 **自动检测** / Auto-detection - 自动扫描DLL文件
- 💾 **备份与恢复** / Backup & Restore - 安全更新
- 🌐 **双语支持** / Bilingual - 中英文界面
- 🛡️ **管理员权限** / Admin Rights - 自动提权

## 📦 源代码构建 / Build from Source

由于兼容性问题，请从源代码构建：

**Due to compatibility issues, please build from source:**

### Windows构建步骤 / Windows Build Steps:

1. **安装 Python 3.8+ (64-bit)** / Install Python 3.8+ (64-bit)
   - https://www.python.org/downloads/

2. **克隆仓库** / Clone repository:
   ```cmd
   git clone https://github.com/mutsuki14/Nvidia-APP-DLSS-Updater.git
   cd Nvidia-APP-DLSS-Updater
   ```

3. **运行构建脚本** / Run build script:
   ```cmd
   build_windows.bat
   ```

4. **获取可执行文件** / Get executables:
   - `release\NvidiaDLSSUpdater.exe` (GUI版本)
   - `release\NvidiaDLSSUpdaterCLI.exe` (CLI版本)

## 🚀 使用方法 / Usage

1. 将DLSS DLL文件放在exe同目录
2. 运行 `RunAsAdmin.bat` 或以管理员身份运行exe
3. 程序会自动更新NVIDIA App的DLSS源文件

## ⚠️ 系统要求 / System Requirements

- Windows 10/11 (64-bit)
- NVIDIA App 已安装
- 管理员权限

## 📝 已知问题 / Known Issues

- ❌ **v1.0.0发布的exe文件不兼容Windows** - 请从源代码构建
- ⚠️ 首次运行可能被Windows Defender拦截 - 选择"仍然运行"

## 🔗 相关链接 / Links

- [构建说明 / Build Instructions](https://github.com/mutsuki14/Nvidia-APP-DLSS-Updater/blob/main/BUILD_INSTRUCTIONS.md)
- [项目主页 / Project Homepage](https://github.com/mutsuki14/Nvidia-APP-DLSS-Updater)
- [问题反馈 / Issue Tracker](https://github.com/mutsuki14/Nvidia-APP-DLSS-Updater/issues)

## 免责声明 / Disclaimer

修改NVIDIA应用程序文件可能影响系统稳定性。使用本工具的风险由用户自行承担。

Modifying NVIDIA application files may affect system stability. Use at your own risk.