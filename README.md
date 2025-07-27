# NVIDIA App DLSS Source Updater
A PowerShell script to update the source DLSS files used by the **NVIDIA App**.

This tool ensures that when you use the NVIDIA App to manage game profiles, the DLSS version it applies is the latest one you provide, not the potentially outdated version bundled with the app.

---

## The Problem
The new NVIDIA App is a great tool for managing game settings and driver profiles. One of its features is the ability to apply or update DLSS profiles for your games. However, the DLSS files that the NVIDIA App uses internally are not always the absolute latest versions available. This means when you use the app to "update" a game's DLSS, you might not be getting the best possible version.

## The Solution
This script solves that problem. It directly updates the source `.bin` files within the NVIDIA App's own model database (`C:\ProgramData\NVIDIA\NGX\models`) with the newer `.dll` files that you provide.

**The result:** After running this script, the next time you use the NVIDIA App to manage a game's DLSS profile, it will install the new, updated version you just supplied. This effectively keeps your NVIDIA App's DLSS library up-to-date.

## Features
- **Targets the NVIDIA App**: Specifically designed to update the source files for the NVIDIA App's profile management feature.
- **Automatic Version Detection**: Automatically finds the correct destination folder for `dlss`, `dlssg`, and `dlssd` models.
- **Safe Replacement**: Creates a `.bak` backup of the original `.bin` file before overwriting it.
- **Simple to Use**: Just place your new DLLs next to the script and run it as an admin.

## How to Use
1.  **Download**: Get the latest `nvngx_dlss.dll` (and/or `dlssg`, `dlssd`) files you want to use.
2.  **Prepare Files**: Place the downloaded DLL(s) and the `replace_nvidia_bin.ps1` script in the same folder.
3.  **Run as Administrator**: Right-click on `replace_nvidia_bin.ps1` and select **"Run with PowerShell as Administrator"**. This is mandatory.
4.  **Verify**: The script will confirm the replacement. Now, open the NVIDIA App and apply the DLSS profile to your desired game. The app will now use your updated file.

## Disclaimer
Modifying application or driver files comes with risks. This script is provided as-is. The author is not responsible for any potential issues with your system, the NVIDIA App, drivers, or games that may arise from its use. Please use it at your own risk.

---
---

# NVIDIA App DLSS 源文件更新工具
一个专门用于更新 **NVIDIA App** 自身所使用的 DLSS 文件的 PowerShell 脚本。

本工具确保当您使用 NVIDIA App 管理游戏配置时，它所应用的 DLSS 版本是您提供的最新版，而非其自带的、可能过时的版本。

---

## 问题所在
全新的 NVIDIA App 是管理游戏设置和驱动配置的强大工具，其功能之一就是为您的游戏应用或更新 DLSS 配置。然而，NVIDIA App 内部使用的 DLSS 文件库并不总是保持在最新的版本。这意味着，当您使用该应用为游戏“更新”DLSS 时，您得到的可能并非当前最好的版本。

## 解决方案
这个脚本解决了上述问题。它会直接将您提供的、更新的 `.dll` 文件，覆盖到 NVIDIA App 自己的模型数据库（位于 `C:\ProgramData\NVIDIA\NGX\models`）中的源 `.bin` 文件。

**最终效果：** 运行此脚本后，当您再次使用 NVIDIA App 管理任何游戏的 DLSS 配置时，它所应用的将是您刚刚提供的那个更新、更强的版本。这能有效保持您的 NVIDIA App 的 DLSS 文件库始终处于最新状态。

## 功能
- **精准定位 NVIDIA App**：专门为更新 NVIDIA App 配置文件管理功能所使用的源文件而设计。
- **自动版本检测**：自动为 `dlss`、`dlssg` 和 `dlssd` 模型找到正确的目标文件夹。
- **安全替换**：在覆盖原始的 `.bin` 文件之前，会自动创建一个 `.bak` 备份文件。
- **使用简单**：只需将您下载的新 DLL 文件和脚本放在一起，然后以管理员身份运行即可。

## 如何使用
1.  **下载**：获取您想使用的最新版 `nvngx_dlss.dll`（以及/或者 `dlssg`, `dlssd`）文件。
2.  **准备文件**：将下载好的 DLL 文件与 `replace_nvidia_bin.ps1` 脚本放在同一个文件夹里。
3.  **以管理员身份运行**：右键点击 `replace_nvidia_bin.ps1` 文件，然后选择 **“使用 PowerShell 管理员身份运行”**。这是必须步骤。
4.  **验证**：脚本会提示替换成功。现在，打开 NVIDIA App 并为您想更新的游戏应用 DLSS 配置，应用此时使用的就是您更新后的文件了。

## 免责声明
修改应用程序或驱动程序文件存在风险。本脚本按“原样”提供。对于因使用此脚本而可能导致的任何系统、NVIDIA App、驱动程序或游戏问题，作者概不负责。请自行承担使用风险。
