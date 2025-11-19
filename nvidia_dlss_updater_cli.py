#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NVIDIA DLSS Updater - Command Line Interface Version
Updates NVIDIA App's DLSS source files with custom DLL versions
"""

import os
import sys
import shutil
import argparse
import ctypes
import re
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Back, Style

# Initialize colorama for Windows color support
init(autoreset=True)

# Constants
NVIDIA_BASE_PATH = r"C:\ProgramData\NVIDIA\NGX\models"
MODEL_MAP = {
    "nvngx_dlss.dll": "dlss",
    "nvngx_dlssg.dll": "dlssg",
    "nvngx_dlssd.dll": "dlssd"
}

class NvidiaDLSSUpdaterCLI:
    def __init__(self):
        self.is_admin = self.check_admin()
        
    def check_admin(self):
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def print_header(self):
        """Print application header"""
        print("\n" + "="*70)
        print(Fore.GREEN + Style.BRIGHT + "   NVIDIA DLSS Updater v1.0 - CLI Version")
        print(Fore.CYAN + "   Updates NVIDIA App's DLSS source files")
        print("="*70 + "\n")
    
    def print_status(self, message, status="INFO"):
        """Print formatted status message"""
        if status == "SUCCESS":
            print(f"{Fore.GREEN}[✓] {message}")
        elif status == "ERROR":
            print(f"{Fore.RED}[✗] {message}")
        elif status == "WARNING":
            print(f"{Fore.YELLOW}[⚠] {message}")
        elif status == "INFO":
            print(f"{Fore.CYAN}[i] {message}")
        else:
            print(f"    {message}")
    
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
    
    def update_single_dll(self, dll_name, source_path, create_backup=True):
        """Update a single DLL file"""
        model_name = MODEL_MAP[dll_name]
        
        print(f"\n{Fore.CYAN}{'='*50}")
        self.print_status(f"Processing: {dll_name}", "INFO")
        
        # Check if source file exists
        if not os.path.exists(source_path):
            self.print_status(f"Source file not found: {source_path}", "ERROR")
            return False
        
        self.print_status(f"Source: {source_path}", "")
        
        # Construct versions path
        versions_path = os.path.join(NVIDIA_BASE_PATH, model_name, "versions")
        
        if not os.path.exists(versions_path):
            self.print_status(f"Versions directory not found: {versions_path}", "ERROR")
            return False
        
        # Find latest version
        latest_version_path = self.find_latest_version(versions_path)
        
        if not latest_version_path:
            self.print_status("No valid version found", "ERROR")
            return False
        
        version_name = os.path.basename(latest_version_path)
        self.print_status(f"Latest version: {version_name}", "")
        
        # Construct files path
        files_path = os.path.join(latest_version_path, "files")
        
        if not os.path.exists(files_path):
            self.print_status("Files directory not found", "ERROR")
            return False
        
        # Find .bin file
        bin_files = [f for f in os.listdir(files_path) if f.endswith('.bin')]
        
        if not bin_files:
            self.print_status("No .bin file found", "ERROR")
            return False
        
        bin_file = bin_files[0]
        bin_file_path = os.path.join(files_path, bin_file)
        
        self.print_status(f"Target: {bin_file_path}", "")
        
        # Create backup if requested
        if create_backup:
            try:
                backup_path = f"{bin_file_path}.bak"
                backup_path_dated = f"{bin_file_path}.bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Create dated backup
                shutil.copy2(bin_file_path, backup_path_dated)
                # Create simple backup (for easy restore)
                shutil.copy2(bin_file_path, backup_path)
                
                self.print_status(f"Backup created: {os.path.basename(backup_path)}", "SUCCESS")
            except Exception as e:
                self.print_status(f"Backup failed: {str(e)}", "ERROR")
                return False
        
        # Replace file
        try:
            shutil.copy2(source_path, bin_file_path)
            self.print_status("File replaced successfully!", "SUCCESS")
            return True
        except Exception as e:
            self.print_status(f"Replacement failed: {str(e)}", "ERROR")
            return False
    
    def auto_detect_dlls(self, directory=None):
        """Auto-detect DLL files in specified or current directory"""
        if directory is None:
            directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        
        found_dlls = {}
        
        self.print_status(f"Scanning directory: {directory}", "INFO")
        
        for dll_name in MODEL_MAP.keys():
            dll_path = os.path.join(directory, dll_name)
            if os.path.exists(dll_path):
                found_dlls[dll_name] = dll_path
                self.print_status(f"Found: {dll_name}", "SUCCESS")
        
        return found_dlls
    
    def restore_backups(self):
        """Restore all files from backup"""
        self.print_status("Starting backup restoration...", "INFO")
        
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
                        self.print_status(f"Restored: {os.path.basename(original_path)}", "SUCCESS")
                        restored_count += 1
                    except Exception as e:
                        self.print_status(f"Restore failed: {os.path.basename(original_path)} - {str(e)}", "ERROR")
        
        return restored_count
    
    def run_interactive(self):
        """Run in interactive mode"""
        self.print_header()
        
        # Check admin privileges
        if not self.is_admin:
            self.print_status("Administrator privileges required!", "WARNING")
            self.print_status("Please run this program as Administrator.", "WARNING")
            print(f"\n{Fore.YELLOW}Right-click the program and select 'Run as administrator'")
            input("\nPress Enter to exit...")
            return 1
        
        self.print_status("Running with Administrator privileges", "SUCCESS")
        
        while True:
            print(f"\n{Fore.CYAN}Menu:")
            print("1. Auto-detect and update DLLs from current directory")
            print("2. Select specific DLL files to update")
            print("3. Restore from backup")
            print("4. Exit")
            
            choice = input(f"\n{Fore.GREEN}Select option (1-4): ").strip()
            
            if choice == '1':
                # Auto-detect and update
                found_dlls = self.auto_detect_dlls()
                if found_dlls:
                    print(f"\n{Fore.YELLOW}Found {len(found_dlls)} DLL file(s).")
                    confirm = input("Proceed with update? (y/n): ").strip().lower()
                    if confirm == 'y':
                        success_count = 0
                        for dll_name, dll_path in found_dlls.items():
                            if self.update_single_dll(dll_name, dll_path):
                                success_count += 1
                        
                        print(f"\n{Fore.GREEN}Update complete: {success_count}/{len(found_dlls)} successful")
                else:
                    self.print_status("No DLL files found in current directory", "WARNING")
            
            elif choice == '2':
                # Manual selection
                dll_files = {}
                for dll_name in MODEL_MAP.keys():
                    path = input(f"\nPath to {dll_name} (or press Enter to skip): ").strip()
                    if path and os.path.exists(path):
                        dll_files[dll_name] = path
                
                if dll_files:
                    success_count = 0
                    for dll_name, dll_path in dll_files.items():
                        if self.update_single_dll(dll_name, dll_path):
                            success_count += 1
                    
                    print(f"\n{Fore.GREEN}Update complete: {success_count}/{len(dll_files)} successful")
                else:
                    self.print_status("No valid files specified", "WARNING")
            
            elif choice == '3':
                # Restore backup
                confirm = input(f"\n{Fore.YELLOW}Restore all files from backup? (y/n): ").strip().lower()
                if confirm == 'y':
                    restored = self.restore_backups()
                    if restored > 0:
                        self.print_status(f"Restored {restored} file(s)", "SUCCESS")
                    else:
                        self.print_status("No backup files found", "WARNING")
            
            elif choice == '4':
                print(f"\n{Fore.CYAN}Goodbye!")
                break
            
            else:
                self.print_status("Invalid option", "ERROR")
        
        return 0
    
    def run_cli(self, args):
        """Run with command line arguments"""
        self.print_header()
        
        # Check admin privileges
        if not self.is_admin:
            self.print_status("Administrator privileges required!", "ERROR")
            return 1
        
        if args.restore:
            # Restore mode
            restored = self.restore_backups()
            if restored > 0:
                self.print_status(f"Restored {restored} file(s)", "SUCCESS")
                return 0
            else:
                self.print_status("No backup files found", "ERROR")
                return 1
        
        # Update mode
        dll_files = {}
        
        if args.auto:
            # Auto-detect mode
            dll_files = self.auto_detect_dlls(args.directory)
            if not dll_files:
                self.print_status("No DLL files found", "ERROR")
                return 1
        else:
            # Manual specification
            if args.dlss and os.path.exists(args.dlss):
                dll_files["nvngx_dlss.dll"] = args.dlss
            if args.dlssg and os.path.exists(args.dlssg):
                dll_files["nvngx_dlssg.dll"] = args.dlssg
            if args.dlssd and os.path.exists(args.dlssd):
                dll_files["nvngx_dlssd.dll"] = args.dlssd
        
        if not dll_files:
            self.print_status("No valid DLL files specified", "ERROR")
            return 1
        
        # Perform update
        success_count = 0
        for dll_name, dll_path in dll_files.items():
            if self.update_single_dll(dll_name, dll_path, not args.no_backup):
                success_count += 1
        
        if success_count == len(dll_files):
            self.print_status(f"All updates successful ({success_count}/{len(dll_files)})", "SUCCESS")
            return 0
        elif success_count > 0:
            self.print_status(f"Partial success ({success_count}/{len(dll_files)})", "WARNING")
            return 2
        else:
            self.print_status("All updates failed", "ERROR")
            return 1

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='NVIDIA DLSS Updater - Update NVIDIA App DLSS source files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --auto                     # Auto-detect DLLs in current directory
  %(prog)s --auto -d C:\\path\\to\\dlls  # Auto-detect DLLs in specified directory
  %(prog)s --dlss nvngx_dlss.dll      # Update specific DLL
  %(prog)s --restore                  # Restore from backup
  %(prog)s                            # Interactive mode
        """
    )
    
    parser.add_argument('--auto', '-a', action='store_true',
                       help='Auto-detect DLL files in directory')
    parser.add_argument('--directory', '-d', type=str,
                       help='Directory to search for DLLs (with --auto)')
    parser.add_argument('--dlss', type=str,
                       help='Path to nvngx_dlss.dll')
    parser.add_argument('--dlssg', type=str,
                       help='Path to nvngx_dlssg.dll')
    parser.add_argument('--dlssd', type=str,
                       help='Path to nvngx_dlssd.dll')
    parser.add_argument('--no-backup', action='store_true',
                       help='Do not create backup files')
    parser.add_argument('--restore', '-r', action='store_true',
                       help='Restore files from backup')
    
    args = parser.parse_args()
    
    updater = NvidiaDLSSUpdaterCLI()
    
    # If no arguments provided, run interactive mode
    if len(sys.argv) == 1:
        return updater.run_interactive()
    else:
        return updater.run_cli(args)

if __name__ == "__main__":
    sys.exit(main())