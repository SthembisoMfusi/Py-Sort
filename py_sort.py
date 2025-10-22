#!/usr/bin/env python3
"""
File Organizer - A simple tool to sort files into folders by type.

This script helps organize messy directories by automatically moving files
into subdirectories based on their file extensions.

Author: Sthembiso Mfusi
License: MIT
"""

import argparse
import json
import os
import shutil
import sys
import logging
from pathlib import Path
from typing import Dict, List
from assets import color

# Logging setup

logging.basicConfig(
    filename="py_sort.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# Retry prompt helper

def prompt_retry(action_desc: str) -> bool:
    """Ask the user if they want to retry an action that failed."""
    while True:
        response = input(f"{action_desc} - Retry? (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("Please enter 'y' or 'n'.")


# Sorting rules

def load_sorting_rules(config_path: str = "config.json") -> Dict[str, List[str]]:
    """
    Load sorting rules from a JSON configuration file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary mapping folder names to lists of file extensions
    """
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        color.print_yellow(f"Warning: Config file '{config_path}' not found. Using default rules.")
        return get_default_sorting_rules()
    except json.JSONDecodeError as e:
        color.print_red(f"Error: Invalid JSON in config file: {e}")
        logger.exception("JSON decode error")
        return get_default_sorting_rules()
    except Exception as e:
        color.print_red(f"Unexpected error loading config: {e}")
        logger.exception("Unexpected error loading config")
        return get_default_sorting_rules()

def get_default_sorting_rules() -> Dict[str, List[str]]:
    return {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico", ".raw", 
                   ".heic", ".heif", ".cr2", ".nef", ".arw", ".dng", ".psd"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages", ".md", ".tex",
                      ".epub", ".mobi", ".azw", ".azw3", ".log"],
        "Videos": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mkv", ".m4v", ".3gp",
                   ".mpg", ".mpeg", ".vob", ".ogv"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".opus", ".aiff",
                  ".au", ".mid", ".midi"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tar.gz", ".tar.bz2",
                     ".cab", ".iso", ".img"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb", ".go", 
                 ".rs", ".ts", ".jsx", ".tsx", ".swift", ".kt", ".scala", ".sh", ".bash",
                 ".json", ".xml", ".yaml", ".yml", ".sql"],
        "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods", ".numbers", ".tsv", ".xlsm"],
        "Presentations": [".ppt", ".pptx", ".odp", ".key", ".pps", ".ppsx"],
        "Executables": [".exe", ".msi", ".deb", ".rpm", ".dmg", ".app", ".apk", ".jar"]
    }

# File utilities

def create_folder_if_not_exists(folder_path: Path) -> None:
    """
    Create a folder if it doesn't already exist.
    
    Args:
        folder_path: Path to the folder to create
    """
    
    while True:
        try:
            if not folder_path.exists():
                folder_path.mkdir(parents=True, exist_ok=True)
                color.print_green(f"Created folder: {folder_path.name}/")
            return  # success
        except PermissionError:
            logger.exception(f"Permission denied creating folder {folder_path}")
            color.print_red(f"Permission denied: cannot create folder '{folder_path}'")
            if not prompt_retry(f"Cannot create folder '{folder_path}'"):
                return
        except OSError as e:
            logger.exception(f"OS error creating folder {folder_path}")
            color.print_red(f"System error creating folder '{folder_path}': {e}")
            if not prompt_retry(f"Cannot create folder '{folder_path}'"):
                return
        except Exception as e:
            logger.exception(f"Unexpected error creating folder {folder_path}")
            color.print_red(f"Unexpected error creating folder '{folder_path}': {e}")
            if not prompt_retry(f"Cannot create folder '{folder_path}'"):
                return

def get_file_extension(file_path: Path) -> str:
     """
    Get the file extension in lowercase.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension including the dot (e.g., '.jpg')
    """
    return file_path.suffix.lower()

def format_size(size_bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def find_target_folder(file_extension: str, sorting_rules: Dict[str, List[str]]) -> str:
     """
    Find the target folder for a given file extension.
    
    Args:
        file_extension: The file extension to look up
        sorting_rules: Dictionary mapping folder names to extensions
        
    Returns:
        The name of the target folder, or 'Other' if no match found
    """
    
    for folder_name, extensions in sorting_rules.items():
        if file_extension in extensions:
            return folder_name
    return "Other"

# Core organizer

def organize_files(directory_path: str, dry_run: bool = False, config_path: str = "config.json", 
                   show_stats: bool = True) -> None:
    """
    Organize files in the specified directory.
    
    Args:
        directory_path: Path to the directory to organize
        dry_run: If True, only show what would be moved without actually moving files
        config_path: Path to the configuration file
    """

    directory = Path(directory_path)
    
    if not directory.exists():
        color.print_red(f"Error: Directory '{directory_path}' does not exist.")
        return
    if not directory.is_dir():
        color.print_red(f"Error: '{directory_path}' is not a directory.")
        return
    
    sorting_rules = load_sorting_rules(config_path)
    files_to_organize = [f for f in directory.iterdir() if f.is_file()]
    
    if not files_to_organize:
        color.print_red("No files found to organize.")
        return
    
    color.print_red(f"Found {len(files_to_organize)} files to organize...")
    if dry_run:
        color.print_red("DRY RUN MODE - No files will actually be moved\n")
    
    moved_count = 0
    skipped_count = 0
    total_size = 0
    category_stats = {}
    
    for file_path in files_to_organize:
        try:
            file_extension = get_file_extension(file_path)
            target_folder = find_target_folder(file_extension, sorting_rules)
            file_size = os.path.getsize(file_path)
            target_dir = directory / target_folder
            if not dry_run:
                create_folder_if_not_exists(target_dir)
            target_file_path = target_dir / file_path.name
            
            if target_file_path.exists():
                print(f"Skipped '{file_path.name}' - file already exists in {target_folder}/")
                skipped_count += 1
                continue
            
            if dry_run:
                print(f"[DRY RUN] Would move '{file_path.name}' to '{target_folder}/'")
            else:
                while True:
                    try:
                        shutil.move(str(file_path), str(target_file_path))
                        print(f"Moved '{file_path.name}' to '{target_folder}/'")
                        moved_count += 1
                        total_size += file_size
                        if target_folder not in category_stats:
                            category_stats[target_folder] = {'count': 0, 'size': 0}
                        category_stats[target_folder]['count'] += 1
                        category_stats[target_folder]['size'] += file_size
                        break  # success
                    except PermissionError:
                        logger.exception(f"Permission denied moving {file_path}")
                        color.print_red(f"Permission denied: cannot move '{file_path.name}'")
                        if not prompt_retry(f"Cannot move '{file_path.name}'"):
                            skipped_count += 1
                            break
                    except OSError as e:
                        logger.exception(f"OS error moving {file_path}")
                        color.print_red(f"System error moving '{file_path.name}': {e}")
                        if not prompt_retry(f"Cannot move '{file_path.name}'"):
                            skipped_count += 1
                            break
                    except Exception as e:
                        logger.exception(f"Unexpected error moving {file_path}")
                        color.print_red(f"Unexpected error moving '{file_path.name}': {e}")
                        if not prompt_retry(f"Cannot move '{file_path.name}'"):
                            skipped_count += 1
                            break
        except Exception as e:
            color.print_red(f"Error processing '{file_path.name}': {e}")
            logger.exception(f"Error processing {file_path}")
            skipped_count += 1
    
    # Summary
    print(f"\n{'='*50}")
    if dry_run:
        print(f"DRY RUN COMPLETE: Would move {len(files_to_organize)} files")
    else:
        color.print_green(f"ORGANIZATION COMPLETE!")
        color.print_green(f"Files moved: {moved_count}")
        if skipped_count > 0:
            print(f"Files skipped: {skipped_count}")
        
        if show_stats and moved_count > 0:
            print(f"\n{'='*50}")
            print("STATISTICS")
            print(f"{'='*50}")
            print(f"Total files organized: {moved_count}")
            print(f"Total size: {format_size(total_size)}")
            print(f"\nFiles by category:")
            sorted_categories = sorted(category_stats.items(), key=lambda x: x[1]['count'], reverse=True)
            for category, stats in sorted_categories:
                print(f"  {category}: {stats['count']} files ({format_size(stats['size'])})")
            print(f"{'='*50}")
            color.print_yellow(f"Files skipped: {skipped_count}")

# CLI

def main():
    """Main function to handle command line arguments and run the organizer."""

    parser = argparse.ArgumentParser(
        description="Organize files in a directory by moving them into subdirectories based on file type.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python py_sort.py ~/Downloads
  python py_sort.py ~/Downloads --dry-run
  python py_sort.py ~/Downloads --config my_rules.json
        """
    )
    
    parser.add_argument("directory", help="Path to the directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved without actually moving files")
    parser.add_argument("--config", default="config.json", help="Path to the JSON configuration file (default: config.json)")
    parser.add_argument("--no-stats", action="store_true", help="Disable detailed statistics at the end")
    
    args = parser.parse_args()
    
    try:
        organize_files(args.directory, args.dry_run, args.config, not args.no_stats)
    except KeyboardInterrupt:
        color.print_red("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        color.print_red(f"Unexpected error: {e}")
        logger.exception("Unexpected error in main")
        sys.exit(1)

if __name__ == "__main__":
    main()
