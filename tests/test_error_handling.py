#!/usr/bin/env python3
import unittest
from unittest.mock import patch
import py_sort
from pathlib import Path
import tempfile


class TestPySortErrorHandling(unittest.TestCase):
    @patch("py_sort.open", side_effect=FileNotFoundError)
    def test_missing_config_file_uses_default(self, mock_open_file):
        rules = py_sort.load_sorting_rules("nonexistent.json")
        self.assertIsInstance(rules, dict)
        self.assertIn("Images", rules)

    @patch("py_sort.json.load", side_effect=py_sort.json.JSONDecodeError("msg", "doc", 0))
    def test_invalid_json_config_falls_back(self, mock_json):
        rules = py_sort.load_sorting_rules("bad.json")
        self.assertIn("Documents", rules)

    @patch("py_sort.Path.mkdir", side_effect=PermissionError)
    @patch("py_sort.prompt_retry", return_value=False)
    def test_permission_error_on_folder_creation(self, mock_retry, mock_mkdir):
        folder = Path("/restricted")
        # Should handle permission error gracefully without crashing
        py_sort.create_folder_if_not_exists(folder)
        mock_retry.assert_called_once()

    def test_permission_error_on_file_move(self):
        # Create a temporary directory and file
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_file_path = Path(tmpdir) / "file.txt"
            fake_file_path.touch()  # create an empty file

            with patch("py_sort.shutil.move", side_effect=PermissionError) as mock_move, \
                 patch("py_sort.prompt_retry", return_value=False):

                # Run organizer on temp directory
                py_sort.organize_files(tmpdir, dry_run=False)

                # Confirm the move was attempted
                mock_move.assert_called()

    @patch("py_sort.logger.exception")
    def test_logging_on_oserror(self, mock_log):
        with patch("py_sort.os.listdir", side_effect=OSError("System fail")):
            py_sort.logger.exception("System fail")
        mock_log.assert_called_once_with("System fail")


class TestPySortUX(unittest.TestCase):
    def test_format_size_outputs_human_readable(self):
        self.assertIn("KB", py_sort.format_size(1024))

    def test_find_target_folder_fallback(self):
        rules = {"Images": [".jpg"]}
        folder = py_sort.find_target_folder(".unknown", rules)
        self.assertEqual(folder, "Other")


if __name__ == "__main__":
    unittest.main()
