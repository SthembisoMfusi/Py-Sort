#!/usr/bin/env python3
"""
Test suite for the File Organizer tool.

This test suite ensures that the file organizer works correctly
and handles edge cases properly.
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add the parent directory to the path so we can import py_sort
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_sort import (
    load_sorting_rules,
    get_default_sorting_rules,
    get_file_extension,
    find_target_folder,
    organize_files
)


class TestFileOrganizer(unittest.TestCase):
    """Test cases for the file organizer functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
    def tearDown(self):
        """Clean up after each test method."""
        shutil.rmtree(self.test_dir)

    def test_get_default_sorting_rules(self):
        """Test that default sorting rules are returned correctly."""
        rules = get_default_sorting_rules()
        
        # Check that we have expected categories
        expected_categories = ["Images", "Documents", "Videos", "Audio", "Archives", "Code"]
        for category in expected_categories:
            self.assertIn(category, rules)
        
        # Check that Images category has expected extensions
        self.assertIn(".jpg", rules["Images"])
        self.assertIn(".png", rules["Images"])
        
        # Check that Documents category has expected extensions
        self.assertIn(".pdf", rules["Documents"])
        self.assertIn(".txt", rules["Documents"])

    def test_load_sorting_rules_with_valid_config(self):
        """Test loading sorting rules from a valid config file."""
        config_data = {
            "TestImages": [".test1", ".test2"],
            "TestDocs": [".test3"]
        }
        
        config_path = self.test_path / "test_config.json"
        with open(config_path, 'w') as f:
            json.dump(config_data, f)
        
        rules = load_sorting_rules(str(config_path))
        self.assertEqual(rules, config_data)

    def test_load_sorting_rules_with_missing_file(self):
        """Test loading sorting rules when config file doesn't exist."""
        rules = load_sorting_rules("nonexistent_config.json")
        default_rules = get_default_sorting_rules()
        self.assertEqual(rules, default_rules)

    def test_load_sorting_rules_with_invalid_json(self):
        """Test loading sorting rules with invalid JSON."""
        config_path = self.test_path / "invalid_config.json"
        with open(config_path, 'w') as f:
            f.write("invalid json content")
        
        rules = load_sorting_rules(str(config_path))
        default_rules = get_default_sorting_rules()
        self.assertEqual(rules, default_rules)

    def test_get_file_extension(self):
        """Test getting file extensions."""
        test_cases = [
            ("test.jpg", ".jpg"),
            ("document.PDF", ".pdf"),
            ("file.TXT", ".txt"),
            ("noextension", ""),
            (".hidden", ""),
            ("multiple.dots.in.name.txt", ".txt")
        ]
        
        for filename, expected_ext in test_cases:
            file_path = Path(filename)
            result = get_file_extension(file_path)
            self.assertEqual(result, expected_ext, f"Failed for {filename}")

    def test_find_target_folder(self):
        """Test finding target folder for file extensions."""
        sorting_rules = {
            "Images": [".jpg", ".png"],
            "Documents": [".pdf", ".txt"],
            "Other": []
        }
        
        test_cases = [
            (".jpg", "Images"),
            (".png", "Images"),
            (".pdf", "Documents"),
            (".txt", "Documents"),
            (".unknown", "Other")
        ]
        
        for extension, expected_folder in test_cases:
            result = find_target_folder(extension, sorting_rules)
            self.assertEqual(result, expected_folder, f"Failed for {extension}")

    def test_organize_files_basic(self):
        """Test basic file organization functionality."""
        # Create test files
        test_files = [
            "image1.jpg",
            "document1.pdf",
            "text1.txt",
            "unknown.xyz"
        ]
        
        for filename in test_files:
            (self.test_path / filename).touch()
        
        # Organize files
        organize_files(self.test_dir)
        
        # Check that folders were created
        self.assertTrue((self.test_path / "Images").exists())
        self.assertTrue((self.test_path / "Documents").exists())
        self.assertTrue((self.test_path / "Other").exists())
        
        # Check that files were moved
        self.assertTrue((self.test_path / "Images" / "image1.jpg").exists())
        self.assertTrue((self.test_path / "Documents" / "document1.pdf").exists())
        self.assertTrue((self.test_path / "Documents" / "text1.txt").exists())
        self.assertTrue((self.test_path / "Other" / "unknown.xyz").exists())

    def test_organize_files_dry_run(self):
        """Test dry run mode doesn't actually move files."""
        # Create test files
        test_files = ["test.jpg", "test.pdf"]
        for filename in test_files:
            (self.test_path / filename).touch()
        
        # Run in dry run mode
        with patch('builtins.print') as mock_print:
            organize_files(self.test_dir, dry_run=True)
        
        # Check that files are still in the original location
        for filename in test_files:
            self.assertTrue((self.test_path / filename).exists())
        
        # Check that no folders were created
        self.assertFalse((self.test_path / "Images").exists())
        self.assertFalse((self.test_path / "Documents").exists())

    def test_organize_files_nonexistent_directory(self):
        """Test organizing files in a nonexistent directory."""
        with patch('builtins.print') as mock_print:
            organize_files("/nonexistent/directory")
        
        # Should print an error message
        mock_print.assert_called_with("Error: Directory '/nonexistent/directory' does not exist.")

    def test_organize_files_empty_directory(self):
        """Test organizing files in an empty directory."""
        with patch('builtins.print') as mock_print:
            organize_files(self.test_dir)
        
        # Should print a message about no files found
        mock_print.assert_called_with("No files found to organize.")

    def test_organize_files_duplicate_names(self):
        """Test handling of duplicate file names."""
        # Create a file in a subdirectory first
        subdir = self.test_path / "Images"
        subdir.mkdir()
        (subdir / "test.jpg").touch()
        
        # Create a file with the same name in the main directory
        (self.test_path / "test.jpg").touch()
        
        # Organize files
        with patch('builtins.print') as mock_print:
            organize_files(self.test_dir)
        
        # Should skip the duplicate file
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        skip_message = any("Skipped 'test.jpg'" in call for call in print_calls)
        self.assertTrue(skip_message, "Should have skipped duplicate file")

    def test_organize_files_with_custom_config(self):
        """Test organizing files with a custom configuration."""
        # Create custom config
        custom_config = {
            "CustomImages": [".jpg"],
            "CustomDocs": [".pdf"]
        }
        
        config_path = self.test_path / "custom_config.json"
        with open(config_path, 'w') as f:
            json.dump(custom_config, f)
        
        # Create test files
        (self.test_path / "test.jpg").touch()
        (self.test_path / "test.pdf").touch()
        
        # Organize with custom config
        organize_files(self.test_dir, config_path=str(config_path))
        
        # Check that custom folders were created
        self.assertTrue((self.test_path / "CustomImages").exists())
        self.assertTrue((self.test_path / "CustomDocs").exists())
        
        # Check that files were moved to custom folders
        self.assertTrue((self.test_path / "CustomImages" / "test.jpg").exists())
        self.assertTrue((self.test_path / "CustomDocs" / "test.pdf").exists())


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete file organizer workflow."""

    def setUp(self):
        """Set up test fixtures for integration tests."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)

    def tearDown(self):
        """Clean up after integration tests."""
        shutil.rmtree(self.test_dir)

    def test_complete_workflow(self):
        """Test the complete workflow from start to finish."""
        # Create a variety of test files
        test_files = [
            "vacation.jpg",
            "report.pdf",
            "notes.txt",
            "presentation.pptx",
            "music.mp3",
            "video.mp4",
            "archive.zip",
            "script.py",
            "data.csv",
            "unknown.xyz"
        ]
        
        for filename in test_files:
            (self.test_path / filename).touch()
        
        # Run the organizer
        organize_files(self.test_dir)
        
        # Verify all expected folders were created
        expected_folders = [
            "Images", "Documents", "Presentations", "Audio", 
            "Videos", "Archives", "Code", "Spreadsheets", "Other"
        ]
        
        for folder in expected_folders:
            self.assertTrue((self.test_path / folder).exists(), f"Folder {folder} should exist")
        
        # Verify files were moved to correct folders
        expected_moves = [
            ("vacation.jpg", "Images"),
            ("report.pdf", "Documents"),
            ("notes.txt", "Documents"),
            ("presentation.pptx", "Presentations"),
            ("music.mp3", "Audio"),
            ("video.mp4", "Videos"),
            ("archive.zip", "Archives"),
            ("script.py", "Code"),
            ("data.csv", "Spreadsheets"),
            ("unknown.xyz", "Other")
        ]
        
        for filename, expected_folder in expected_moves:
            file_path = self.test_path / expected_folder / filename
            self.assertTrue(file_path.exists(), f"{filename} should be in {expected_folder}")
        
        # Verify no files remain in the root directory
        remaining_files = [f for f in self.test_path.iterdir() if f.is_file()]
        self.assertEqual(len(remaining_files), 0, "No files should remain in root directory")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
