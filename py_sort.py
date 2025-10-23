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
from pathlib import Path
from typing import Dict, List
from assets import color
from tqdm import tqdm
from time import sleep


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
        return get_default_sorting_rules()

def print(message):
    tqdm.write(message)

def get_default_sorting_rules() -> Dict[str, List[str]]:
    """
    Get default sorting rules when no config file is available.
    
    Returns:
        Dictionary mapping folder names to lists of file extensions
    """
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


def create_folder_if_not_exists(folder_path: Path) -> None:
    """
    Create a folder if it doesn't already exist.
    
    Args:
        folder_path: Path to the folder to create
    """
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
        color.print_green(f"Created folder: {folder_path.name}/")


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
    """
    Convert bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable string (e.g., '1.5 MB', '500 KB')
    """
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


def organize_files(directory_path: str, dry_run: bool = False, config_path: str = "config.json", 
                   show_stats: bool = True) -> None:
  
  
    """
    Organize files in the specified directory.
    
    Args:
        directory_path: Path to the directory to organize
        dry_run: If True, only show what would be moved without actually moving files
        config_path: Path to the configuration file
        show_stats: If True, display detailed statistics at the end
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        color.print_red(f"Error: Directory '{directory_path}' does not exist.")
        return
    
    if not directory.is_dir():
        color.print_red(f"Error: '{directory_path}' is not a directory.")
        return
    
    # Load sorting rules
    sorting_rules = load_sorting_rules(config_path)
    
    # Get all files in the directory (not subdirectories)
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
    category_stats = {}  # Track files and size per category
    total=len(files_to_organize)
    
    for itter_cnt,file_path in tqdm(enumerate(files_to_organize),colour="#CEFCAB",total=total,desc="Current Progress in Organizing your folder"):
        #view current progress with a visual progress Bar
        
        file_extension = get_file_extension(file_path)
        target_folder = find_target_folder(file_extension, sorting_rules)
        file_size = os.path.getsize(file_path)
        
        

        # Create target directory
        target_dir = directory / target_folder
        if not dry_run:
            create_folder_if_not_exists(target_dir)
        
        # Move the file
        target_file_path = target_dir / file_path.name
        
        if target_file_path.exists():
            print(f"Skipped '{file_path.name}' - file already exists in {target_folder}/")
            skipped_count += 1
            continue
        
        if dry_run:
            print(f"[DRY RUN] Would move '{file_path.name}' to '{target_folder}/'")
        else:
            try:
                shutil.move(str(file_path), str(target_file_path))
                print(f"Moved '{file_path.name}' to '{target_folder}/'")
                moved_count += 1
                total_size += file_size
                
                # Update category statistics
                if target_folder not in category_stats:
                    category_stats[target_folder] = {'count': 0, 'size': 0}
                category_stats[target_folder]['count'] += 1
                category_stats[target_folder]['size'] += file_size
            except Exception as e:
                color.print_red(f"Error moving '{file_path.name}': {e}")
                skipped_count += 1
      
        
        sleep(0.01)
       
    # Summary
    print(f"\n{'='*50}")
    if dry_run:
        print(f"DRY RUN COMPLETE: Would move {len(files_to_organize)} files")
    else:
        color.print_green(f"ORGANIZATION COMPLETE!")
        color.print_green(f"Files moved: {moved_count}")
        if skipped_count > 0:
            print(f"Files skipped: {skipped_count}")
        
        # Display detailed statistics if enabled
        if show_stats and moved_count > 0:
            print(f"\n{'='*50}")
            print("STATISTICS")
            print(f"{'='*50}")
            print(f"Total files organized: {moved_count}")
            print(f"Total size: {format_size(total_size)}")
            print(f"\nFiles by category:")
            
            # Sort categories by count (descending)
            sorted_categories = sorted(category_stats.items(), 
                                     key=lambda x: x[1]['count'], 
                                     reverse=True)
            
            for category, stats in sorted_categories:
                print(f"  {category}: {stats['count']} files ({format_size(stats['size'])})")
            print(f"{'='*50}")

            color.print_yellow(f"Files skipped: {skipped_count}")
        
    
    


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
    
    parser.add_argument(
        "directory",
        help="Path to the directory to organize"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved without actually moving files"
    )
    
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to the JSON configuration file (default: config.json)"
    )
    
    parser.add_argument(
        "--no-stats",
        action="store_true",
        help="Disable detailed statistics at the end"
    )
    
    args = parser.parse_args()
    
    try:
        organize_files(args.directory, args.dry_run, args.config, not args.no_stats)
    except KeyboardInterrupt:
        color.print_red("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        color.print_red(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    
    main()
