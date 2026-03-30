#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NVIDIA DLSS Updater - Shared Core Module
Common logic for both GUI and CLI applications.
"""

import os
import shutil
import re
from datetime import datetime

# Constants
NVIDIA_BASE_PATH = r"C:\ProgramData\NVIDIA\NGX\models"
MODEL_MAP = {
    "nvngx_dlss.dll": "dlss",
    "nvngx_dlssg.dll": "dlssg",
    "nvngx_dlssd.dll": "dlssd",
}


def check_admin():
    """Check if running as administrator (Windows only)."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def find_latest_version(versions_path):
    """Find the latest (highest-numbered) version directory.

    Uses os.scandir + max() instead of listdir + sort for fewer syscalls
    and O(n) instead of O(n log n) traversal.
    """
    if not os.path.isdir(versions_path):
        return None

    best = None
    with os.scandir(versions_path) as entries:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False) and re.fullmatch(r'\d+', entry.name):
                num = int(entry.name)
                if best is None or num > best[0]:
                    best = (num, entry.path)

    return best[1] if best else None


def resolve_target(model_name):
    """Resolve the target .bin file path for a given model.

    Returns (bin_file_path, files_path, error_message).
    On success error_message is None; on failure bin_file_path is None.
    """
    versions_path = os.path.join(NVIDIA_BASE_PATH, model_name, "versions")

    if not os.path.isdir(versions_path):
        return None, None, f"Versions directory not found: {versions_path}"

    latest = find_latest_version(versions_path)
    if not latest:
        return None, None, "No valid version found"

    files_path = os.path.join(latest, "files")
    if not os.path.isdir(files_path):
        return None, None, "Files directory not found"

    # Find the first .bin file using scandir (avoids listing everything)
    bin_file = None
    with os.scandir(files_path) as entries:
        for entry in entries:
            if entry.is_file(follow_symlinks=False) and entry.name.endswith('.bin'):
                bin_file = entry.path
                break

    if not bin_file:
        return None, files_path, "No .bin file found"

    return bin_file, files_path, None


def create_backup(bin_file_path):
    """Create backup of the target file.

    Creates a timestamped backup first, then a simple .bak via hard-link
    (falling back to copy) to avoid redundant file I/O.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dated = f"{bin_file_path}.bak.{timestamp}"
    backup_simple = f"{bin_file_path}.bak"

    # Primary copy — timestamped backup
    shutil.copy2(bin_file_path, backup_dated)

    # Simple backup via hard-link (same data, no extra I/O)
    try:
        if os.path.exists(backup_simple):
            os.remove(backup_simple)
        os.link(backup_dated, backup_simple)
    except OSError:
        # Hard-links not supported (cross-device, FAT32, etc.) — fall back to copy
        shutil.copy2(bin_file_path, backup_simple)

    return backup_simple


def replace_file(source_path, target_path):
    """Replace target file with source file, preserving metadata."""
    shutil.copy2(source_path, target_path)


def find_backup_files(files_path):
    """Yield (backup_path, original_path) pairs found in files_path."""
    with os.scandir(files_path) as entries:
        for entry in entries:
            if entry.is_file(follow_symlinks=False) and entry.name.endswith('.bin.bak'):
                yield entry.path, entry.path[:-4]  # strip .bak


def restore_model_backups(model_name):
    """Restore backups for a single model.

    Yields (original_path, error) tuples.
    error is None on success, str on failure.
    """
    versions_path = os.path.join(NVIDIA_BASE_PATH, model_name, "versions")
    if not os.path.isdir(versions_path):
        return

    latest = find_latest_version(versions_path)
    if not latest:
        return

    files_path = os.path.join(latest, "files")
    if not os.path.isdir(files_path):
        return

    for backup_path, original_path in find_backup_files(files_path):
        try:
            shutil.copy2(backup_path, original_path)
            yield original_path, None
        except Exception as e:
            yield original_path, str(e)
