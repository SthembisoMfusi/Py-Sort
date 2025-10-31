#!/usr/bin/env python3
"""
Menu-based JSON configuration editor for Py-Sort.

Allows users to view and modify sorting categories and extensions
in the configuration JSON file. Changes can be saved back to disk
or discarded.
"""

import json
import os
import sys

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def load_config():
    """
    Load configuration from the JSON file.

    Returns:
        dict: Dictionary containing categories as keys and lists of
              extensions as values. Returns an empty dict if the file
              doesn't exist or contains invalid JSON.
    """
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file not found: {CONFIG_FILE}")
        return {}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format. Starting with empty config.")
        return {}


def save_config(config):
    """
    Save the configuration dictionary back to the JSON file.

    Args:
        config (dict): Configuration dictionary to save.
    """
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration saved to {CONFIG_FILE}")
    except Exception as e:
        print(f"Error saving configuration: {e}")


def view_categories(config):
    """
    Display all current categories and their associated file extensions.

    Args:
        config (dict): Configuration dictionary.
    """
    if not config:
        print("No categories defined.")
        return
    for category, extensions in config.items():
        print(f"\n{category}:")
        print(", ".join(extensions) if extensions else "  (no extensions)")


def add_category(config):
    """
    Prompt the user to add a new category to the configuration.

    Args:
        config (dict): Configuration dictionary.
    """
    name = input("Enter new category name: ").strip()
    if not name:
        print("Category name cannot be empty.")
        return
    if name in config:
        print("Category already exists.")
        return
    config[name] = []
    print(f"Added category '{name}'.")


def remove_category(config):
    """
    Prompt the user to remove an existing category from the configuration.

    Args:
        config (dict): Configuration dictionary.
    """
    name = input("Enter category name to remove: ").strip()
    if name not in config:
        print("Category not found.")
        return
    del config[name]
    print(f"Removed category '{name}'.")


def add_extension(config):
    """
    Prompt the user to add a new extension to a specific category.

    Args:
        config (dict): Configuration dictionary.
    """
    category = input("Enter category name: ").strip()
    if category not in config:
        print("Category not found.")
        return
    ext = input("Enter new extension (include the dot, e.g. .xyz): ").strip().lower()
    if not ext.startswith("."):
        print("Invalid format. Extension must start with '.'")
        return
    if ext in config[category]:
        print("Extension already exists in this category.")
        return
    config[category].append(ext)
    print(f"Added '{ext}' to '{category}'.")


def remove_extension(config):
    """
    Prompt the user to remove an extension from a specific category.

    Args:
        config (dict): Configuration dictionary.
    """
    category = input("Enter category name: ").strip()
    if category not in config:
        print("Category not found.")
        return
    ext = input("Enter extension to remove (include the dot): ").strip().lower()
    if ext not in config[category]:
        print("Extension not found in this category.")
        return
    config[category].remove(ext)
    print(f"Removed '{ext}' from '{category}'.")


def menu():
    """
    Main interactive menu loop.

    Displays options to view, add, remove categories or extensions,
    and allows saving or discarding changes.
    """
    config = load_config()

    while True:
        print("\n==== CONFIG EDITOR ====")
        print("1. View current categories")
        print("2. Add a new category")
        print("3. Remove a category")
        print("4. Add extension to category")
        print("5. Remove extension from category")
        print("6. Save and exit")
        print("7. Exit without saving")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            view_categories(config)
        elif choice == "2":
            add_category(config)
        elif choice == "3":
            remove_category(config)
        elif choice == "4":
            add_extension(config)
        elif choice == "5":
            remove_extension(config)
        elif choice == "6":
            save_config(config)
            break
        elif choice == "7":
            print("Exiting without saving changes.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nExited by user.")
        sys.exit(0)
