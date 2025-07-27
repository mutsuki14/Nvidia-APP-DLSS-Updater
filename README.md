NVIDIA DLSS File Replacer
A PowerShell script to easily replace NVIDIA's DLSS/DLSSG/DLSSD model files with your custom DLLs.
This tool automates the process of finding the latest version of the DLSS model files located in the C:\ProgramData\NVIDIA\NGX\models directory and overwriting them with the nvngx_dlss.dll, nvngx_dlssg.dll, or nvngx_dlssd.dll files you provide.
What is this?
For gamers and developers who want to use a specific version of NVIDIA's DLSS, DLSS-G (Frame Generation), or DLSSD files, this script provides a convenient way to perform the replacement. Instead of manually navigating through system folders, finding the correct version, and renaming files, this script handles everything for you.
Features
Automatic Version Detection: Automatically finds the latest version folder for dlss, dlssg, and dlssd.
Safe Replacement: Creates a .bak backup of the original .bin file before overwriting it.
Simple to Use: Just place your DLLs next to the script and run it.
Informative Output: Provides clear feedback in the console about what it's doing.
How to Use
Download: Download the replace_nvidia_bin.ps1 script from this repository.
Prepare Files: Place the script in a folder along with the custom DLL files you want to use (e.g., nvngx_dlss.dll).
Run as Administrator: Right-click on replace_nvidia_bin.ps1 and select "Run with PowerShell as Administrator". This is mandatory as the script needs to write to the protected C:\ProgramData directory.
Done: The script will find the target files and replace them with yours. Check the console output to confirm the operation was successful.
Disclaimer
Modifying driver or system files comes with risks. This script is provided as-is. The author is not responsible for any potential issues with your system, drivers, or games that may arise from its use. Please use it at your own risk.
NVIDIA DLSS 文件替换工具
一个能轻松将您自定义的 DLL 文件替换掉 NVIDIA 官方 DLSS/DLSSG/DLSSD 模型文件的 PowerShell 脚本。
本工具可以自动在 C:\ProgramData\NVIDIA\NGX\models 目录中查找最新版本的 DLSS 模型文件，并用您提供的 nvngx_dlss.dll, nvngx_dlssg.dll, 或 nvngx_dlssd.dll 文件进行覆盖。
这是什么？
对于希望使用特定版本 NVIDIA DLSS、DLSS-G（帧生成）或 DLSSD 文件的游戏玩家和开发者来说，这个脚本提供了一种便捷的替换方式。您无需再手动浏览系统文件夹、寻找正确的版本号、重命名和替换文件，脚本会为您完成所有操作。
功能
自动版本检测：自动为 dlss、dlssg 和 dlssd 查找版本号最高的文件夹。
安全替换：在覆盖原始的 .bin 文件之前，会自动创建一个 .bak 备份文件。
使用简单：只需将您的 DLL 文件和脚本放在一起运行即可。
信息清晰：在控制台中提供清晰的操作过程反馈。
如何使用
下载：从本仓库下载 replace_nvidia_bin.ps1 脚本文件。
准备文件：将脚本与您想要使用的自定义 DLL 文件（例如 nvngx_dlss.dll）放在同一个文件夹里。
以管理员身份运行：右键点击 replace_nvidia_bin.ps1 文件，然后选择 “使用 PowerShell 管理员身份运行”。这是必须的，因为脚本需要写入受系统保护的 C:\ProgramData 目录。
完成：脚本会自动查找目标文件并进行替换。您可以查看控制台的输出来确认操作是否成功。
免责声明
修改驱动或系统文件存在风险。本脚本按“原样”提供。对于因使用此脚本而可能导致的任何系统、驱动程序或游戏问题，作者概不负责。请自行承担使用风险。
