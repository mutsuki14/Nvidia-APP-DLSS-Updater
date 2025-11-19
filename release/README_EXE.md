# NVIDIA DLSS Updater - Executable Version

## 简介 / Introduction

这是 NVIDIA DLSS Updater 的可执行文件版本，提供了图形界面（GUI）和命令行界面（CLI）两种使用方式。

This is the executable version of NVIDIA DLSS Updater, providing both GUI and CLI interfaces.

## 版本说明 / Version Information

- **Version**: 1.0.0
- **GUI版本 / GUI Version**: `NvidiaDLSSUpdater.exe`
- **CLI版本 / CLI Version**: `NvidiaDLSSUpdaterCLI.exe`
- **启动器 / Launcher**: `RunAsAdmin.bat`

## 系统要求 / System Requirements

- Windows 10/11 (64-bit)
- 管理员权限 / Administrator privileges
- NVIDIA App 已安装 / NVIDIA App installed

## 功能特性 / Features

### GUI 版本特性 / GUI Features
- ✅ 友好的图形用户界面 / User-friendly graphical interface
- ✅ 自动检测当前目录的 DLL 文件 / Auto-detect DLL files
- ✅ 文件浏览器选择 DLL / File browser for DLL selection
- ✅ 实时操作日志显示 / Real-time operation log
- ✅ 一键恢复备份功能 / One-click backup restoration
- ✅ 中英文双语界面 / Bilingual interface (Chinese/English)

### CLI 版本特性 / CLI Features
- ✅ 命令行参数支持 / Command-line arguments support
- ✅ 批处理脚本集成 / Batch script integration
- ✅ 交互式菜单模式 / Interactive menu mode
- ✅ 彩色输出提示 / Colored output messages
- ✅ 自动化更新支持 / Automation support

## 使用方法 / How to Use

### 方法 1: 使用启动器（推荐）/ Method 1: Using Launcher (Recommended)

1. 将你的 DLSS DLL 文件放在程序同一目录下 / Place your DLSS DLL files in the same directory
2. 双击运行 `RunAsAdmin.bat` / Double-click `RunAsAdmin.bat`
3. 程序会自动以管理员权限启动 / Program will start with admin privileges

### 方法 2: GUI 版本 / Method 2: GUI Version

1. 右键点击 `NvidiaDLSSUpdater.exe`
2. 选择"以管理员身份运行" / Select "Run as administrator"
3. 使用界面操作：
   - 点击"自动检测"扫描当前目录 / Click "Auto-detect" to scan current directory
   - 或点击"浏览"手动选择文件 / Or click "Browse" to manually select files
   - 点击"开始更新"执行替换 / Click "Start Update" to execute replacement

### 方法 3: CLI 版本（交互模式）/ Method 3: CLI Version (Interactive)

```cmd
# 以管理员身份运行命令提示符 / Run Command Prompt as administrator
NvidiaDLSSUpdaterCLI.exe
```

### 方法 4: CLI 版本（命令行模式）/ Method 4: CLI Version (Command-line)

```cmd
# 自动检测并更新当前目录的 DLL / Auto-detect and update DLLs in current directory
NvidiaDLSSUpdaterCLI.exe --auto

# 指定目录自动检测 / Auto-detect in specified directory
NvidiaDLSSUpdaterCLI.exe --auto -d "C:\path\to\dlls"

# 手动指定 DLL 文件 / Manually specify DLL files
NvidiaDLSSUpdaterCLI.exe --dlss nvngx_dlss.dll --dlssg nvngx_dlssg.dll

# 恢复备份 / Restore from backup
NvidiaDLSSUpdaterCLI.exe --restore

# 不创建备份直接更新 / Update without creating backup
NvidiaDLSSUpdaterCLI.exe --auto --no-backup
```

## 文件说明 / File Description

```
NvidiaDLSSUpdater_v1.0.zip
├── NvidiaDLSSUpdater.exe      # GUI版本主程序 / GUI version main program
├── NvidiaDLSSUpdaterCLI.exe   # CLI版本主程序 / CLI version main program
├── RunAsAdmin.bat              # 管理员启动器 / Administrator launcher
└── README.md                   # 说明文档 / Documentation
```

## 更新流程 / Update Process

1. **检测** / Detection: 程序查找 NVIDIA NGX 模型目录
2. **定位** / Location: 找到最新版本的 .bin 文件
3. **备份** / Backup: 创建原始文件的备份（.bak）
4. **替换** / Replace: 用提供的 DLL 覆盖 .bin 文件
5. **验证** / Verify: 确认替换成功

## 备份恢复 / Backup Restoration

程序会自动创建两种备份：
- `.bak` - 简单备份，用于快速恢复
- `.bak.YYYYMMDD_HHMMSS` - 带时间戳的备份

恢复方法 / Restoration methods:
- GUI: 点击"恢复备份"按钮
- CLI: 运行 `NvidiaDLSSUpdaterCLI.exe --restore`

## 常见问题 / FAQ

### Q: 提示需要管理员权限？/ Admin privileges required?
A: 使用 RunAsAdmin.bat 启动，或右键选择"以管理员身份运行"

### Q: 找不到 DLL 文件？/ DLL files not found?
A: 确保 DLL 文件与 exe 在同一目录，或使用"浏览"功能手动选择

### Q: 更新后游戏没有变化？/ No change after update?
A: 需要在 NVIDIA App 中重新应用 DLSS 配置文件

### Q: 如何确认更新成功？/ How to verify successful update?
A: 查看程序日志中的绿色"✓"标记，或检查目标目录的文件修改时间

## 安全提示 / Security Notice

- ⚠️ 始终从可信来源获取 DLSS DLL 文件
- ⚠️ 程序会自动创建备份，但建议手动备份重要文件
- ⚠️ 修改系统文件存在风险，使用需自行承担

## 技术支持 / Support

如遇到问题，请提供以下信息：
- 使用的版本（GUI/CLI）
- 操作系统版本
- NVIDIA App 版本
- 错误日志截图

## 更新日志 / Changelog

### v1.0.0 (2024-11-19)
- ✨ 首次发布 / Initial release
- ✨ GUI 和 CLI 双版本 / Both GUI and CLI versions
- ✨ 自动版本检测 / Automatic version detection
- ✨ 备份和恢复功能 / Backup and restore functionality
- ✨ 中英文双语支持 / Bilingual support

## 开源协议 / License

This project is provided as-is for educational purposes. Use at your own risk.

---

**免责声明 / Disclaimer**: 修改 NVIDIA 应用程序文件可能影响系统稳定性。作者不对使用本工具造成的任何问题负责。请自行承担使用风险。

Modifying NVIDIA application files may affect system stability. The author is not responsible for any issues caused by using this tool. Use at your own risk.