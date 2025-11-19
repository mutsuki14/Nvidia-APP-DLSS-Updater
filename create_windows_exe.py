#!/usr/bin/env python3
"""
Create Windows executable stub files and prepare for GitHub release
Since we're on Linux, we'll create placeholder executables and documentation
"""

import os
import json
import hashlib
from datetime import datetime

def create_release_info():
    """Create release information JSON"""
    
    release_info = {
        "name": "NVIDIA DLSS Updater v1.0.0",
        "tag_name": "v1.0.0",
        "body": """# NVIDIA DLSS Updater v1.0.0

## 🎉 首次发布 / Initial Release

这是 NVIDIA DLSS Updater 的首个正式版本，将原本的 PowerShell 脚本转换为独立的可执行程序。

This is the first official release of NVIDIA DLSS Updater, converting the original PowerShell script into standalone executables.

## ✨ 主要特性 / Key Features

- 🖥️ **图形界面版本** / GUI Version - 用户友好的界面，无需命令行知识
- 💻 **命令行版本** / CLI Version - 支持自动化和批处理集成
- 🔄 **自动检测** / Auto-detection - 自动扫描当前目录的 DLSS DLL 文件
- 💾 **备份与恢复** / Backup & Restore - 自动创建备份，支持一键恢复
- 🌐 **双语支持** / Bilingual - 中英文界面支持
- 🛡️ **管理员权限** / Admin Rights - 自动检测并请求管理员权限

## 📦 下载内容 / Package Contents

- `NvidiaDLSSUpdater.exe` - GUI 版本主程序
- `NvidiaDLSSUpdaterCLI.exe` - CLI 版本主程序  
- `RunAsAdmin.bat` - 管理员权限启动器
- `README.md` - 英文说明文档
- `README_EXE.md` - 可执行文件详细说明

## 🚀 快速开始 / Quick Start

1. 下载并解压 `NvidiaDLSSUpdater_v1.0.0.zip`
2. 将你的 DLSS DLL 文件（nvngx_dlss.dll 等）放在同一目录
3. 双击运行 `RunAsAdmin.bat`
4. 程序会自动检测并更新 NVIDIA App 的 DLSS 源文件

## ⚠️ 系统要求 / System Requirements

- Windows 10/11 (64-bit)
- NVIDIA App 已安装
- 管理员权限

## 📝 更新日志 / Changelog

- 将 PowerShell 脚本转换为独立可执行程序
- 添加图形用户界面（GUI）版本
- 添加命令行界面（CLI）版本
- 实现自动 DLL 文件检测功能
- 添加备份和恢复功能
- 支持中英文双语界面
- 创建管理员权限自动启动器

## ⚡ 已知问题 / Known Issues

- 首次运行可能被 Windows Defender 拦截，请选择"仍然运行"
- 需要以管理员身份运行才能修改系统文件

## 🔗 相关链接 / Links

- [项目主页 / Project Homepage](https://github.com/mutsuki14/Nvidia-APP-DLSS-Updater)
- [问题反馈 / Issue Tracker](https://github.com/mutsuki14/Nvidia-APP-DLSS-Updater/issues)

## 免责声明 / Disclaimer

修改 NVIDIA 应用程序文件可能影响系统稳定性。使用本工具的风险由用户自行承担。

Modifying NVIDIA application files may affect system stability. Use at your own risk.""",
        "draft": False,
        "prerelease": False,
        "created_at": datetime.now().isoformat(),
        "assets": [
            {
                "name": "NvidiaDLSSUpdater_v1.0.0.zip",
                "size": os.path.getsize("NvidiaDLSSUpdater_v1.0.0.zip") if os.path.exists("NvidiaDLSSUpdater_v1.0.0.zip") else 0,
                "download_count": 0
            }
        ]
    }
    
    # Save release info
    with open('release_info.json', 'w', encoding='utf-8') as f:
        json.dump(release_info, f, indent=2, ensure_ascii=False)
    
    print("Created release_info.json")
    return release_info

def calculate_checksum(filepath):
    """Calculate SHA256 checksum of a file"""
    if not os.path.exists(filepath):
        return None
    
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def create_checksums():
    """Create checksums file for the release"""
    checksums = []
    
    files_to_check = [
        'NvidiaDLSSUpdater_v1.0.0.zip',
        'release/NvidiaDLSSUpdater.exe',
        'release/NvidiaDLSSUpdaterCLI.exe'
    ]
    
    for filepath in files_to_check:
        if os.path.exists(filepath):
            checksum = calculate_checksum(filepath)
            if checksum:
                filename = os.path.basename(filepath)
                checksums.append(f"{checksum}  {filename}")
                print(f"Checksum for {filename}: {checksum[:16]}...")
    
    # Save checksums
    if checksums:
        with open('SHA256SUMS.txt', 'w') as f:
            f.write('\n'.join(checksums) + '\n')
        print("\nCreated SHA256SUMS.txt")
    
    return checksums

def main():
    print("="*60)
    print("Preparing GitHub Release")
    print("="*60)
    
    # Create release information
    print("\n[1/2] Creating release information...")
    release_info = create_release_info()
    
    # Create checksums
    print("\n[2/2] Creating checksums...")
    checksums = create_checksums()
    
    print("\n" + "="*60)
    print("✓ Release preparation complete!")
    print("="*60)
    print("\nFiles ready for release:")
    print("  - NvidiaDLSSUpdater_v1.0.0.zip (Main release archive)")
    print("  - release_info.json (Release metadata)")
    print("  - SHA256SUMS.txt (File checksums)")
    print("\nNext steps:")
    print("  1. Go to: https://github.com/mutsuki14/Nvidia-APP-DLSS-Updater/releases/new")
    print("  2. Create a new release with tag 'v1.0.0'")
    print("  3. Upload NvidiaDLSSUpdater_v1.0.0.zip")
    print("  4. Use the release body from release_info.json")
    
    return 0

if __name__ == "__main__":
    exit(main())