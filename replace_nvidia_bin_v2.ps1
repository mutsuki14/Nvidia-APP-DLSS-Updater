# PowerShell Script to replace NVIDIA's .bin files with custom DLLs. (v3 - Patched)
#
# Description:
# This script performs a reverse replacement. It takes a custom DLL file
# (e.g., nvngx_dlss.dll) from the script's directory and uses it to overwrite
# the latest .bin file found in the corresponding NVIDIA NGX model's 'files' directory.
# This version is patched to correctly sort version folders that use plain numbers
# instead of standard version formats (e.g., Major.Minor.Build).
#
# Instructions:
# 1. Place your custom DLLs (nvngx_dlss.dll, nvngx_dlssg.dll, nvngx_dlssd.dll)
#    in the same folder as this script.
# 2. You MUST run this script as an Administrator because it writes to the
#    C:\ProgramData directory. Right-click the .ps1 file and choose
#    "Run with PowerShell as Administrator".

# --- SCRIPT START ---

# Get the directory where the script is located.
$scriptPath = $PSScriptRoot

# Base path for NVIDIA NGX models
$nvidiaBasePath = "C:\ProgramData\NVIDIA\NGX\models"

# A map defining the source DLL files and their corresponding model folders
$modelMap = @{
    "nvngx_dlss.dll"  = "dlss";
    "nvngx_dlssg.dll" = "dlssg";
    "nvngx_dlssd.dll" = "dlssd";
}

Write-Host "--- NVIDIA .bin �ļ������滻�ű� (v3-���޸�) ---" -ForegroundColor Yellow
Write-Host "��Ҫ��ʾ: ��ȷ������ʹ�ù���Ա������д˽ű���" -ForegroundColor Red
Write-Host "�ű�����Ŀ¼: $scriptPath"
Write-Host ""

# Iterate over each source DLL defined in the map
foreach ($sourceDll in $modelMap.Keys) {
    $modelName = $modelMap[$sourceDll]
    $sourceFileFullPath = Join-Path $scriptPath $sourceDll

    Write-Host "���ڴ���Դ�ļ�: $sourceDll" -ForegroundColor Cyan

    # Check if the source DLL file exists in the script's directory.
    if (-not (Test-Path -Path $sourceFileFullPath)) {
        Write-Host "  [����] �ű�Ŀ¼��δ�ҵ�Դ�ļ�: $sourceDll" -ForegroundColor Gray
        Write-Host ""
        Continue # Move to the next file
    }

    # Construct the path to the versions folder for the current model
    $versionsPath = Join-Path $nvidiaBasePath "$modelName\versions"

    if (-not (Test-Path -Path $versionsPath -PathType Container)) {
        Write-Host "  [����] δ�ҵ� '$modelName' �� versions Ŀ¼: $versionsPath" -ForegroundColor Red
        Write-Host ""
        Continue
    }

    # --- FIX START ---
    # Find the latest version directory by sorting folder names numerically.
    # This correctly handles folder names that are large integers.
    $latestVersion = Get-ChildItem -Path $versionsPath -Directory |
        Where-Object { $_.Name -match '^\d+$' } | # Filter for directories with all-digit names
        Sort-Object -Property @{Expression={[long]$_.Name}} -Descending | # Sort them as numbers
        Select-Object -First 1
    # --- FIX END ---

    if (-not $latestVersion) {
        Write-Host "  [����] δ�ҵ� '$modelName' ����Ч�汾�ļ��С����� '$versionsPath' ���Ƿ���ڴ������������ļ��С�" -ForegroundColor Red
        Write-Host ""
        Continue
    }

    # Construct the path to the 'files' folder inside the latest version
    $destinationFilesPath = Join-Path $latestVersion.FullName "files"

    if (-not (Test-Path -Path $destinationFilesPath -PathType Container)) {
        Write-Host "  [����] �ڰ汾 $($latestVersion.Name) ��δ�ҵ� 'files' Ŀ¼��" -ForegroundColor Red
        Write-Host ""
        Continue
    }
    
    # Find the first .bin file in the destination directory
    $destinationBinFile = Get-ChildItem -Path $destinationFilesPath -Filter "*.bin" | Select-Object -First 1

    if (-not $destinationBinFile) {
        Write-Host "  [����] ��Ŀ¼��δ�ҵ�Ŀ�� .bin �ļ�: $destinationFilesPath" -ForegroundColor Red
        Write-Host ""
        Continue
    }

    Write-Host "  > Դ�ļ�: $sourceFileFullPath"
    Write-Host "  > Ŀ���ļ�: $($destinationBinFile.FullName)"
    
    # Perform the replacement: Copy the source DLL to the destination, overwriting the .bin file.
    try {
        # Create a backup of the original file
        $backupFile = "$($destinationBinFile.FullName).bak"
        Write-Host "  > ���ڱ���ԭʼ�ļ���: $backupFile"
        Copy-Item -Path $destinationBinFile.FullName -Destination $backupFile -Force -ErrorAction Stop

        # Copy the new file
        Copy-Item -Path $sourceFileFullPath -Destination $destinationBinFile.FullName -Force -ErrorAction Stop
        Write-Host "  [�ɹ�] ��ʹ�� '$sourceDll' �ɹ����� '$($destinationBinFile.Name)'��" -ForegroundColor Green
    }
    catch {
        Write-Host "  [��������] д���ļ�ʧ�ܡ���ȷ�����Ƿ���ʹ�ù���Ա������нű���" -ForegroundColor Red
        Write-Host "  ������Ϣ: $_" -ForegroundColor Red
    }
    finally{
        Write-Host "" # Add a blank line for better readability
    }
}

Write-Host "--- �ű�ִ����� ---" -ForegroundColor Yellow
# Keep the window open for 10 seconds to allow the user to read the output
Start-Sleep -Seconds 10
