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
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import re
import unicodedata
import re
import unicodedata

from assets import color

def rename_file(file_path: Path, pattern: str, existing_names: set) -> str:
    """
    Return a new filename based on pattern, ensuring uniqueness in existing_names.
    Supports {date}, {clean}, {lower}. Appends counter if needed.
    """
    name = file_path.stem
    ext = file_path.suffix

    # clean version
    clean_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    clean_name = re.sub(r'[^\w\s-]', '', clean_name).replace(' ', '_').lower()

    new_name = pattern
    new_name = new_name.replace("{date}", datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    new_name = new_name.replace("{clean}", clean_name)
    new_name = new_name.replace("{lower}", name.lower())

    candidate = f"{new_name}{ext}"
    counter = 1
    while candidate in existing_names:
        candidate = f"{new_name}_{counter}{ext}"
        counter += 1

    existing_names.add(candidate)
    return candidate

def rename_file(file_path: Path, pattern: str, existing_names: set) -> str:
    """
    Return a new filename based on pattern, ensuring uniqueness in existing_names.
    Supports {date}, {clean}, {lower}. Appends counter if needed.
    """
    name = file_path.stem
    ext = file_path.suffix

    # clean version
    clean_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    clean_name = re.sub(r'[^\w\s-]', '', clean_name).replace(' ', '_').lower()

    new_name = pattern
    new_name = new_name.replace("{date}", datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    new_name = new_name.replace("{clean}", clean_name)
    new_name = new_name.replace("{lower}", name.lower())

    candidate = f"{new_name}{ext}"
    counter = 1
    while candidate in existing_names:
        candidate = f"{new_name}_{counter}{ext}"
        counter += 1

    existing_names.add(candidate)
    return candidate

# Logging setup
logging.basicConfig(
    filename="py_sort.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def prompt_retry(action_desc: str) -> bool:
    """
    Ask the user if they want to retry an action that failed.
     This function presents a yes/no prompt to the user and ensures a valid
    'y' or 'n' response. It's used to give the user control over repeating
    operations that encountered transient errors (e.g., permission issues).
    Args:
        action_desc (str): A description of the action that failed, to be
                           included in the retry prompt.
    Returns:
        bool: True if the user chooses to retry (enters 'y' or 'yes'),
              False otherwise (enters 'n' or 'no').
    """
    while True:
        response = input(f"{action_desc} - Retry? (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("Please enter 'y' or 'n'.")


def load_sorting_rules(config_path: str = "config.json") -> Dict[str, List[str]]:
    """
    Load sorting rules from a JSON configuration file.
    This function attempts to read a JSON file specified by `config_path`.
    The JSON file is expected to contain a dictionary where keys are folder
    names (e.g., "Images") and values are lists of file extensions (e.g.,
    [".jpg", ".png"]). If the file is not found, or if there's an error
    parsing the JSON, default sorting rules are returned, and a warning/error
    is printed and logged.
    Args:
        config_path (str): Path to the configuration file (default: "config.json").
    Returns:
        Dict[str, List[str]]: A dictionary mapping folder names to lists of
                              file extensions. Returns default rules on error.
    """
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        color.print_yellow(f"Warning: Config file '{config_path}' not found. Using default rules.")
        return get_default_sorting_rules()
    except json.JSONDecodeError as e:
        color.print_red(f"Error: Invalid JSON in config file '{config_path}': {e}")
        logger.exception("JSON decode error in config file")
        return get_default_sorting_rules()
    except Exception as e:
        color.print_red(f"Unexpected error loading config file '{config_path}': {e}")
        logger.exception("Unexpected error loading config file")
        return get_default_sorting_rules()


def get_default_sorting_rules() -> Dict[str, List[str]]:
    """
    Provides a dictionary of default file sorting rules.
    This function defines a hardcoded set of common file types mapped to
    logical folder names. This acts as a fallback if no custom configuration
    file is provided or if the custom file is invalid.
    Returns:
        Dict[str, List[str]]: A dictionary where keys are target folder names
                              and values are lists of associated file extensions.
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
    Create a folder if it doesn't already exist, handling permissions and OS errors.
    This function attempts to create the specified `folder_path` (including any
    necessary parent directories) if it does not already exist. It incorporates
    a retry mechanism using `prompt_retry` for `PermissionError` and other
    `OSError` types, making the folder creation more robust.
    Args:
        folder_path (Path): Path to the folder to create.
    """
    while True:
        try:
            if not folder_path.exists():
                folder_path.mkdir(parents=True, exist_ok=True)
                color.print_green(f"Created folder: {folder_path.name}/")
            return
            return
        except PermissionError:
            logger.exception(f"Permission denied creating folder {folder_path}")
            color.print_red(f"Permission denied: cannot create folder '{folder_path}'")
            if not prompt_retry(f"Cannot create folder '{folder_path}'"):
                return
                return
        except OSError as e:
            logger.exception(f"OS error creating folder {folder_path}")
            color.print_red(f"System error creating folder '{folder_path}': {e}")
            if not prompt_retry(f"Cannot create folder '{folder_path}'"):
                return
                return
        except Exception as e:
            logger.exception(f"Unexpected error creating folder {folder_path}")
            color.print_red(f"Unexpected error creating folder '{folder_path}': {e}")
            if not prompt_retry(f"Cannot create folder '{folder_path}'"):
                return
                return


def get_file_extension(file_path: Path) -> str:
    """
    Get the file extension in lowercase.
    This function extracts the file extension from a `pathlib.Path` object.
    It returns the extension including the leading dot (e.g., '.jpg') and
    converts it to lowercase for consistent matching against sorting rules.
    Args:
        file_path (Path): Path to the file.
    Returns:
        str: The file extension, including the dot, in lowercase.
             Returns an empty string if the file has no extension.
    """
    return file_path.suffix.lower()


def format_size(size_bytes: int) -> str:
    """
    Formats a file size in bytes into a human-readable string (e.g., KB, MB, GB).
    This function converts a raw byte count into a more understandable format
    by applying appropriate units (B, KB, MB, GB, TB).
    Args:
        size_bytes (int): The size of the file in bytes.
    Returns:
        str: A formatted string representing the file size with units
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def find_target_folder(file_extension: str, sorting_rules: Dict[str, List[str]]) -> str:
    """
    Find the target folder for a given file extension based on sorting rules.
    This function iterates through the provided `sorting_rules` to find which
    category (folder name) the `file_extension` belongs to. If a match is found,
    the corresponding folder name is returned. If no matching rule is found,
    the default folder name "Other" is returned.
    Args:
        file_extension (str): The file extension to look up (e.g., '.pdf').
        sorting_rules (Dict[str, List[str]]): A dictionary mapping folder names
                                               to lists of file extensions.
    Returns:
        str: The name of the target folder (e.g., "Documents"), or "Other"
    """
    for folder_name, extensions in sorting_rules.items():
        if file_extension in extensions:
            return folder_name
    return "Other"


def log_move(directory: Path, original_path: Path, new_path: Path) -> None:
    """
    Log a file move operation to a JSON log file.
    This function appends details of a file move (timestamp, original path, new path)
    to a JSON file named `py_sort_moves.json` located in the `directory` being organized.
    This log is crucial for the undo functionality. The log is a list of dictionaries.
    Args:
        directory (Path): The root directory where the log file is stored.
        original_path (Path): The original full path of the file before moving.
        new_path (Path): The new full path of the file after moving.
    """
    log_file = directory / "py_sort_moves.json"
    moves = []
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                moves = json.load(f)
            if not isinstance(moves, list):
            if not isinstance(moves, list):
                moves = []
                color.print_yellow(f"Warning: Move log '{log_file.name}' was malformed. Starting a new log.")
        except json.JSONDecodeError:
            moves = []
            color.print_yellow(f"Warning: Move log '{log_file.name}' is corrupted. Starting a new log.")
        except Exception as e:
            logger.exception(f"Error reading move log {log_file}")
            color.print_red(f"Error reading move log '{log_file.name}': {e}. Starting a new log.")
            moves = []

    moves.append({
        "timestamp": datetime.now().isoformat(),
        "original": str(original_path),
        "new": str(new_path)
    })
    try:
        with open(log_file, 'w') as f:
            json.dump(moves, f, indent=4)
    except Exception as e:
        logger.exception(f"Error writing to move log {log_file}")
        color.print_red(f"Error writing to move log '{log_file.name}': {e}")


def organize_files(directory_path: str, dry_run: bool = False, config_path: str = "config.json",
                   show_stats: bool = True) -> None:
    """
    Organize files in the specified directory into subfolders by type.
    This is the core function for organizing files. It sc  ans the target directory,
    determines the correct destination for each file based on its extension and
    the sorting rules, and then (if not in dry-run mode) moves the files. It
    provides progress updates, handles potential errors during file operations
    with a retry mechanism, and collects statistics about the organization process.
    Args:
        directory_path (str): The path to the directory whose files are to be organized.
        dry_run (bool, optional): If True, files will not actually be moved;
                                  the script will only show what *would* happen.
                                  Defaults to False.
        config_path (str, optional): Path to the JSON configuration file containing
                                     custom sorting rules. Defaults to "config.json".
        show_stats (bool, optional): If True, detailed statistics about the
                                     organization (files moved, total size,
                                     category breakdown) will be displayed.
                                     Defaults to True.
    """
    directory = Path(directory_path)

    if not directory.exists():
        color.print_red(f"Error: Directory '{directory_path}' does not exist.")
        return
    if not directory.is_dir():
        color.print_red(f"Error: '{directory_path}' is not a directory.")
        return

    sorting_rules = load_sorting_rules(config_path)

    files_to_organize = [
        f for f in directory.iterdir()
        if f.is_file() and f.name not in ["py_sort.log", "py_sort_moves.json"]
    ]

    if not files_to_organize:
        color.print_yellow("No files found to organize in the specified directory.")
        return

    color.print_yellow(f"Found {len(files_to_organize)} files to consider for organization...")
    if dry_run:
        color.print_yellow("DRY RUN MODE - No files will actually be moved\n")

    moved_count = 0
    skipped_count = 0
    total_size = 0
    category_stats: Dict[str, Dict[str, int]] = {}
    category_stats: Dict[str, Dict[str, int]] = {}

    for file_path in files_to_organize:
        try:
            file_extension = get_file_extension(file_path)
            target_folder = find_target_folder(file_extension, sorting_rules)
            file_size = file_path.stat().st_size
            file_size = file_path.stat().st_size
            target_dir = directory / target_folder
            target_file_path = target_dir / file_path.name

            if target_file_path.exists():
                color.print_yellow(f"Skipped '{file_path.name}' - file already exists in '{target_folder}/'")
                skipped_count += 1
                continue
                continue

            if not dry_run:
                create_folder_if_not_exists(target_dir)

            if dry_run:
                print(f"[DRY RUN] Would move '{file_path.name}' to '{target_folder}/'")
                moved_count += 1 
                total_size += file_size
                category_stats.setdefault(target_folder, {'count': 0, 'size': 0})
                category_stats[target_folder]['count'] += 1
                category_stats[target_folder]['size'] += file_size
            else:
                while True:
                    try:
                        shutil.move(str(file_path), str(target_file_path))
                        color.print_green(f"Moved '{file_path.name}' to '{target_folder}/'")
                        moved_count += 1
                        total_size += file_size
                        log_move(directory, file_path, target_file_path)
                        category_stats.setdefault(target_folder, {'count': 0, 'size': 0})
                        category_stats[target_folder]['count'] += 1
                        category_stats[target_folder]['size'] += file_size
                        break
                        break
                    except PermissionError:
                        logger.exception(f"Permission denied moving {file_path}")
                        color.print_red(f"Permission denied: cannot move '{file_path.name}'")
                        if not prompt_retry(f"Cannot move '{file_path.name}'"):
                            skipped_count += 1
                            break
                            break
                    except OSError as e:
                        logger.exception(f"OS error moving {file_path}")
                        color.print_red(f"System error moving '{file_path.name}': {e}")
                        if not prompt_retry(f"Cannot move '{file_path.name}'"):
                            skipped_count += 1
                            break
                            break
                    except Exception as e:
                        logger.exception(f"Unexpected error moving {file_path}")
                        color.print_red(f"Unexpected error moving '{file_path.name}': {e}")
                        if not prompt_retry(f"Cannot move '{file_path.name}'"):
                            skipped_count += 1
                            break
                            break
        except Exception as e:
            color.print_red(f"Error processing '{file_path.name}': {e}")
            logger.exception(f"Error processing {file_path}")
            skipped_count += 1

    print(f"\n{'='*50}")
    if dry_run:
        color.print_yellow(f"DRY RUN COMPLETE: Would have attempted to organize {len(files_to_organize)} files.")
        print(f"  Would move: {moved_count} files")
        print(f"  Would skip: {skipped_count} files")
        print(f"  Would skip: {skipped_count} files")
    else:
        color.print_green(f"ORGANIZATION COMPLETE!")
        color.print_green(f"Files successfully moved: {moved_count}")
        if skipped_count > 0:
            color.print_yellow(f"Files skipped due to errors or existing duplicates: {skipped_count}")

        if show_stats and moved_count > 0:
            print(f"\n{'='*50}")
            print("STATISTICS")
            print(f"{'='*50}")
            print(f"Total files organized: {moved_count}")
            print(f"Total size moved: {format_size(total_size)}")
            print(f"\nFiles by category:")
            sorted_categories = sorted(category_stats.items(), key=lambda x: x[1]['count'], reverse=True)
            for category, stats in sorted_categories:
                print(f"  {category}: {stats['count']} files ({format_size(stats['size'])})")
            print(f"{'='*50}")
    print(f"{'='*50}")


def undo_organization(directory_path: str) -> None:
    """
    Undo the last organization operation for a given directory.
    
    This function attempts to revert the file moves performed by the
    `organize_files` function by reading the `py_sort_moves.json` log file
    located in the target `directory`. It moves files from their new locations
    back to their recorded original paths. The undo operation is performed
    in reverse order of the original moves to minimize conflicts.
    After a successful undo, the move log is cleared.
    Args:
        directory_path (str): Path to the directory for which organization
                              needs to be undone.
    """
    directory = Path(directory_path)

    if not directory.exists():
        color.print_red(f"Error: Directory '{directory_path}' does not exist.")
        return

    if not directory.is_dir():
        color.print_red(f"Error: '{directory_path}' is not a directory.")
        return

    log_file = directory / "py_sort_moves.json"

    if not log_file.exists():
        color.print_red("No move log found for this directory. Nothing to undo.")
        return

    try:
        with open(log_file, 'r') as f:
            moves = json.load(f)
        if not isinstance(moves, list) or not all(isinstance(m, dict) for m in moves):
            color.print_red("Error reading move log. Log file may be corrupted or malformed.")
            return
    except json.JSONDecodeError:
        color.print_red("Error reading move log. Log file is not valid JSON.")
        return
    except Exception as e:
        logger.exception(f"Unexpected error loading move log {log_file}")
        color.print_red(f"Unexpected error loading move log '{log_file.name}': {e}")
        return

    if not moves:
        color.print_red("No moves recorded in the log file for this directory. Nothing to undo.")
        return

    color.print_yellow("\nThis will attempt to undo the last organization by moving files back to their original locations.")
    confirm = input("Are you sure you want to proceed? (y/N): ").strip().lower()
    if confirm != 'y':
        color.print_red("Undo cancelled by user.")
        return

    restored_count = 0
    skipped_count = 0

    for move in reversed(moves):
        original_path = Path(move.get('original', ''))
        new_path = Path(move.get('new', ''))

        if not original_path.is_absolute() or not new_path.is_absolute():
            color.print_red(f"Skipped '{new_path.name}' - invalid path in log. Log entry: {move}")
            skipped_count += 1
            continue

        if new_path.exists():
            if original_path.exists():
                color.print_yellow(f"Skipped '{new_path.name}' - original location '{original_path.parent}' "
                                   f"already has a file named '{original_path.name}'.")
                skipped_count += 1
                continue

            if not original_path.parent.exists():
                color.print_yellow(f"Warning: Creating original parent directory '{original_path.parent}/' for '{new_path.name}'.")
                try:
                    original_path.parent.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    color.print_red(f"Error creating parent directory '{original_path.parent}': {e}. Skipping '{new_path.name}'.")
                    skipped_count += 1
                    continue

            while True:
                try:
                    shutil.move(str(new_path), str(original_path))
                    color.print_green(f"Restored '{new_path.name}' to '{original_path.parent}/'")
                    restored_count += 1
                    break
                    break
                except PermissionError:
                    logger.exception(f"Permission denied restoring {new_path}")
                    color.print_red(f"Permission denied: cannot restore '{new_path.name}'")
                    if not prompt_retry(f"Cannot restore '{new_path.name}'"):
                        skipped_count += 1
                        break
                        break
                except OSError as e:
                    logger.exception(f"OS error restoring {new_path}")
                    color.print_red(f"System error restoring '{new_path.name}': {e}")
                    if not prompt_retry(f"Cannot restore '{new_path.name}'"):
                        skipped_count += 1
                        break
                        break
                except Exception as e:
                    logger.exception(f"Unexpected error restoring {new_path}")
                    color.print_red(f"Unexpected error restoring '{new_path.name}': {e}")
                    if not prompt_retry(f"Cannot restore '{new_path.name}'"):
                        skipped_count += 1
                        break
                        break
        else:
            color.print_yellow(f"Skipped '{new_path.name}' - file not found at expected location.")
            color.print_yellow(f"Skipped '{new_path.name}' - file not found at expected location.")
            skipped_count += 1

    color.print_green(f"\nUndo complete. Files restored: {restored_count}")
    if skipped_count:
        color.print_yellow(f"Files skipped: {skipped_count}")
    color.print_green(f"\nUndo complete. Files restored: {restored_count}")
    if skipped_count:
        color.print_yellow(f"Files skipped: {skipped_count}")


def main():
    """
    Command-line interface for the File Organizer.
    Main function to handle command-line arguments and run the file organizer.
    This function serves as the entry point for the PyDex script. It configures
    the command-line argument parser, interprets user input, and dispatches
    control to either `organize_files` or `undo_organization` based on the
    provided arguments. It also includes global error handling for `KeyboardInterrupt`
    and other unexpected exceptions.
    """
    parser = argparse.ArgumentParser(description="File Organizer - Sort files into folders by type.")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to organize (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--config", default="config.json", help="Path to JSON config file with sorting rules")
    parser.add_argument("--undo", action="store_true", help="Undo the last organization operation")
    parser.add_argument("--no-stats", action="store_true", help="Do not show detailed statistics after organizing")
    parser = argparse.ArgumentParser(description="File Organizer - Sort files into folders by type.")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to organize (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--config", default="config.json", help="Path to JSON config file with sorting rules")
    parser.add_argument("--undo", action="store_true", help="Undo the last organization operation")
    parser.add_argument("--no-stats", action="store_true", help="Do not show detailed statistics after organizing")

    args = parser.parse_args()

    directory = args.directory
    dry_run = args.dry_run
    config_path = args.config
    show_stats = not args.no_stats
    undo = args.undo

    if undo:
        undo_organization(directory)
    else:
        organize_files(directory, dry_run=dry_run, config_path=config_path, show_stats=show_stats)
    directory = args.directory
    dry_run = args.dry_run
    config_path = args.config
    show_stats = not args.no_stats
    undo = args.undo

    if undo:
        undo_organization(directory)
    else:
        organize_files(directory, dry_run=dry_run, config_path=config_path, show_stats=show_stats)


if __name__ == "__main__":
    main()

