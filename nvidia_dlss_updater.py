#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NVIDIA DLSS Updater - GUI Application
Updates NVIDIA App's DLSS source files with custom DLL versions
"""

import os
import sys
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import ctypes
import re
from pathlib import Path
from datetime import datetime

# Constants
NVIDIA_BASE_PATH = r"C:\ProgramData\NVIDIA\NGX\models"
MODEL_MAP = {
    "nvngx_dlss.dll": "dlss",
    "nvngx_dlssg.dll": "dlssg",
    "nvngx_dlssd.dll": "dlssd"
}

class NvidiaDLSSUpdater:
    def __init__(self, root):
        self.root = root
        self.root.title("NVIDIA DLSS Updater v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set icon if available
        try:
            self.root.iconbitmap(default='nvidia.ico')
        except:
            pass
        
        # Variables
        self.dll_files = {}
        self.is_admin = self.check_admin()
        
        # Create GUI
        self.create_widgets()
        
        # Check admin status
        if not self.is_admin:
            self.log_message("⚠️ 警告: 请以管理员身份运行此程序！\n", "warning")
            self.log_message("⚠️ WARNING: Please run this program as Administrator!\n", "warning")
            messagebox.showwarning("需要管理员权限", 
                                 "此程序需要管理员权限才能修改系统文件。\n"
                                 "请右键点击程序并选择'以管理员身份运行'。\n\n"
                                 "This program requires Administrator privileges.\n"
                                 "Please right-click and 'Run as Administrator'.")
    
    def check_admin(self):
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="NVIDIA DLSS 源文件更新工具 / NVIDIA DLSS Source Updater",
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="选择 DLL 文件 / Select DLL Files", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(1, weight=1)
        
        # DLSS file selection
        row = 0
        for dll_name, model_name in MODEL_MAP.items():
            label = ttk.Label(file_frame, text=f"{dll_name}:")
            label.grid(row=row, column=0, sticky=tk.W, pady=5)
            
            entry = ttk.Entry(file_frame, width=50)
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=5)
            
            button = ttk.Button(file_frame, text="浏览/Browse", width=12,
                              command=lambda e=entry, d=dll_name: self.browse_file(e, d))
            button.grid(row=row, column=2, pady=5)
            
            self.dll_files[dll_name] = entry
            row += 1
        
        # Auto detect button
        auto_detect_btn = ttk.Button(file_frame, 
                                   text="自动检测当前目录的 DLL 文件 / Auto-detect DLLs in current directory",
                                   command=self.auto_detect_dlls)
        auto_detect_btn.grid(row=row, column=0, columnspan=3, pady=(10, 0))
        
        # Log output frame
        log_frame = ttk.LabelFrame(main_frame, text="操作日志 / Operation Log", padding="10")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text widget with scrollbar
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=70, height=15)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for different message types
        self.log_text.tag_config("info", foreground="black")
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("warning", foreground="orange")
        self.log_text.tag_config("error", foreground="red")
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2)
        
        # Update button
        self.update_btn = ttk.Button(button_frame, 
                                    text="开始更新 / Start Update", 
                                    command=self.start_update,
                                    state=tk.NORMAL if self.is_admin else tk.DISABLED)
        self.update_btn.grid(row=0, column=0, padx=5)
        
        # Restore backup button
        self.restore_btn = ttk.Button(button_frame, 
                                     text="恢复备份 / Restore Backup", 
                                     command=self.restore_backup,
                                     state=tk.NORMAL if self.is_admin else tk.DISABLED)
        self.restore_btn.grid(row=0, column=1, padx=5)
        
        # Exit button
        exit_btn = ttk.Button(button_frame, text="退出 / Exit", command=self.root.quit)
        exit_btn.grid(row=0, column=2, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("就绪 / Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def browse_file(self, entry, dll_name):
        """Browse for DLL file"""
        filename = filedialog.askopenfilename(
            title=f"选择 {dll_name} 文件 / Select {dll_name} file",
            filetypes=[("DLL files", "*.dll"), ("All files", "*.*")]
        )
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)
            self.log_message(f"已选择文件 / File selected: {filename}\n", "info")
    
    def auto_detect_dlls(self):
        """Auto-detect DLL files in current directory"""
        current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        found_count = 0
        
        self.log_message(f"正在扫描目录 / Scanning directory: {current_dir}\n", "info")
        
        for dll_name in MODEL_MAP.keys():
            dll_path = os.path.join(current_dir, dll_name)
            if os.path.exists(dll_path):
                self.dll_files[dll_name].delete(0, tk.END)
                self.dll_files[dll_name].insert(0, dll_path)
                self.log_message(f"✓ 找到 / Found: {dll_name}\n", "success")
                found_count += 1
            else:
                self.log_message(f"✗ 未找到 / Not found: {dll_name}\n", "warning")
        
        if found_count > 0:
            self.log_message(f"\n自动检测完成，找到 {found_count} 个文件。\n", "success")
            self.log_message(f"Auto-detection complete, found {found_count} file(s).\n", "success")
        else:
            self.log_message("\n未找到任何 DLL 文件。\n", "warning")
            self.log_message("No DLL files found.\n", "warning")
    
    def log_message(self, message, msg_type="info"):
        """Add message to log"""
        self.log_text.insert(tk.END, message, msg_type)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def find_latest_version(self, versions_path):
        """Find the latest version directory"""
        if not os.path.exists(versions_path):
            return None
        
        version_dirs = []
        for item in os.listdir(versions_path):
            item_path = os.path.join(versions_path, item)
            if os.path.isdir(item_path):
                # Check if it's a numeric folder name
                if re.match(r'^\d+$', item):
                    version_dirs.append((int(item), item_path))
        
        if not version_dirs:
            return None
        
        # Sort by numeric value and get the latest
        version_dirs.sort(key=lambda x: x[0], reverse=True)
        return version_dirs[0][1]
    
    def update_single_dll(self, dll_name, source_path):
        """Update a single DLL file"""
        model_name = MODEL_MAP[dll_name]
        
        self.log_message(f"\n{'='*50}\n", "info")
        self.log_message(f"处理 / Processing: {dll_name}\n", "info")
        
        # Check if source file exists
        if not os.path.exists(source_path):
            self.log_message(f"✗ 源文件不存在 / Source file not found: {source_path}\n", "error")
            return False
        
        # Construct versions path
        versions_path = os.path.join(NVIDIA_BASE_PATH, model_name, "versions")
        
        if not os.path.exists(versions_path):
            self.log_message(f"✗ 未找到版本目录 / Versions directory not found: {versions_path}\n", "error")
            return False
        
        # Find latest version
        latest_version_path = self.find_latest_version(versions_path)
        
        if not latest_version_path:
            self.log_message(f"✗ 未找到有效版本 / No valid version found\n", "error")
            return False
        
        version_name = os.path.basename(latest_version_path)
        self.log_message(f"找到最新版本 / Found latest version: {version_name}\n", "info")
        
        # Construct files path
        files_path = os.path.join(latest_version_path, "files")
        
        if not os.path.exists(files_path):
            self.log_message(f"✗ 未找到 files 目录 / Files directory not found\n", "error")
            return False
        
        # Find .bin file
        bin_files = [f for f in os.listdir(files_path) if f.endswith('.bin')]
        
        if not bin_files:
            self.log_message(f"✗ 未找到 .bin 文件 / No .bin file found\n", "error")
            return False
        
        bin_file = bin_files[0]
        bin_file_path = os.path.join(files_path, bin_file)
        
        self.log_message(f"目标文件 / Target file: {bin_file_path}\n", "info")
        
        # Create backup
        try:
            backup_path = f"{bin_file_path}.bak"
            backup_path_dated = f"{bin_file_path}.bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create dated backup
            shutil.copy2(bin_file_path, backup_path_dated)
            # Create simple backup (for easy restore)
            shutil.copy2(bin_file_path, backup_path)
            
            self.log_message(f"✓ 已创建备份 / Backup created: {backup_path}\n", "success")
        except Exception as e:
            self.log_message(f"✗ 备份失败 / Backup failed: {str(e)}\n", "error")
            return False
        
        # Replace file
        try:
            shutil.copy2(source_path, bin_file_path)
            self.log_message(f"✓ 成功替换文件 / File replaced successfully!\n", "success")
            return True
        except Exception as e:
            self.log_message(f"✗ 替换失败 / Replacement failed: {str(e)}\n", "error")
            return False
    
    def start_update(self):
        """Start the update process"""
        if not self.is_admin:
            messagebox.showerror("权限错误", "需要管理员权限才能执行此操作！\nAdministrator privileges required!")
            return
        
        # Disable button during update
        self.update_btn.config(state=tk.DISABLED)
        self.status_var.set("正在更新... / Updating...")
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        self.log_message("开始更新过程... / Starting update process...\n\n", "info")
        
        # Run update in thread to prevent GUI freezing
        thread = threading.Thread(target=self.perform_update)
        thread.start()
    
    def perform_update(self):
        """Perform the actual update"""
        success_count = 0
        total_count = 0
        
        for dll_name, entry in self.dll_files.items():
            source_path = entry.get().strip()
            if source_path:
                total_count += 1
                if self.update_single_dll(dll_name, source_path):
                    success_count += 1
        
        # Summary
        self.log_message(f"\n{'='*50}\n", "info")
        if total_count == 0:
            self.log_message("未选择任何文件进行更新。\n", "warning")
            self.log_message("No files selected for update.\n", "warning")
        else:
            self.log_message(f"更新完成: 成功 {success_count}/{total_count}\n", 
                           "success" if success_count == total_count else "warning")
            self.log_message(f"Update complete: Success {success_count}/{total_count}\n",
                           "success" if success_count == total_count else "warning")
            
            if success_count > 0:
                self.log_message("\n现在您可以打开 NVIDIA App 并应用 DLSS 配置到游戏。\n", "info")
                self.log_message("You can now open NVIDIA App and apply DLSS profiles to your games.\n", "info")
        
        # Re-enable button
        self.update_btn.config(state=tk.NORMAL)
        self.status_var.set("就绪 / Ready")
    
    def restore_backup(self):
        """Restore from backup files"""
        if not self.is_admin:
            messagebox.showerror("权限错误", "需要管理员权限才能执行此操作！\nAdministrator privileges required!")
            return
        
        result = messagebox.askyesno("确认恢复", 
                                    "确定要从备份恢复所有文件吗？\n"
                                    "Are you sure you want to restore all files from backup?")
        if not result:
            return
        
        self.log_text.delete(1.0, tk.END)
        self.log_message("开始恢复备份... / Starting backup restoration...\n\n", "info")
        
        restored_count = 0
        
        for model_name in MODEL_MAP.values():
            versions_path = os.path.join(NVIDIA_BASE_PATH, model_name, "versions")
            if not os.path.exists(versions_path):
                continue
            
            latest_version_path = self.find_latest_version(versions_path)
            if not latest_version_path:
                continue
            
            files_path = os.path.join(latest_version_path, "files")
            if not os.path.exists(files_path):
                continue
            
            # Find backup files
            for file_name in os.listdir(files_path):
                if file_name.endswith('.bin.bak'):
                    backup_path = os.path.join(files_path, file_name)
                    original_path = backup_path[:-4]  # Remove .bak
                    
                    try:
                        shutil.copy2(backup_path, original_path)
                        self.log_message(f"✓ 已恢复 / Restored: {original_path}\n", "success")
                        restored_count += 1
                    except Exception as e:
                        self.log_message(f"✗ 恢复失败 / Restore failed: {original_path}\n{str(e)}\n", "error")
        
        if restored_count > 0:
            self.log_message(f"\n恢复完成: 已恢复 {restored_count} 个文件。\n", "success")
            self.log_message(f"Restoration complete: {restored_count} file(s) restored.\n", "success")
        else:
            self.log_message("\n未找到备份文件。\n", "warning")
            self.log_message("No backup files found.\n", "warning")

def main():
    """Main entry point"""
    root = tk.Tk()
    app = NvidiaDLSSUpdater(root)
    root.mainloop()

if __name__ == "__main__":
    main()