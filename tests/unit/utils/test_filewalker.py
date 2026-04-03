import unittest
import os

from libs.utils.filewalker import walk_folder, list_folder_files


class TestFilewalker(unittest.TestCase):
    def setUp(self):
        """Set up test assets path"""
        self.assets_path = os.path.join(os.path.dirname(__file__), "assets/filewalker")

    def test_walk_folder_gets_all_folders(self):
        """Test that walk_folder returns all non-hidden, non-excluded folders"""
        result = walk_folder(self.assets_path)

        # Expected folders (relative paths from assets)
        expected_folders = [
            os.path.join(self.assets_path, "folder1"),
            os.path.join(self.assets_path, "folder2"),
            os.path.join(self.assets_path, "folder1", "subfolder1"),
        ]

        # Sort both lists for consistent comparison
        result_sorted = sorted(result)
        expected_sorted = sorted(expected_folders)

        self.assertEqual(result_sorted, expected_sorted)

    def test_walk_folder_excludes_hidden_folders(self):
        """Test that walk_folder excludes hidden folders (starting with .)"""
        result = walk_folder(self.assets_path)

        # Check that no hidden folders are in the result
        for folder in result:
            folder_name = os.path.basename(folder)
            self.assertFalse(folder_name.startswith('.'),
                             f"Hidden folder {folder_name} should be excluded")

    def test_walk_folder_excludes_pycache(self):
        """Test that walk_folder excludes __pycache__ folders"""
        result = walk_folder(self.assets_path)

        # Check that __pycache__ is not in the result
        for folder in result:
            folder_name = os.path.basename(folder)
            self.assertNotEqual(folder_name, "__pycache__",
                                "__pycache__ folder should be excluded")

    def test_walk_folder_respects_max_depth(self):
        """Test that walk_folder respects max_depth parameter"""
        # With max_depth=1, should only get folder1 and folder2, not subfolder1
        result = walk_folder(self.assets_path, max_depth=1)

        # Should only have first-level folders
        expected_folders = [
            os.path.join(self.assets_path, "folder1"),
            os.path.join(self.assets_path, "folder2"),
        ]

        result_sorted = sorted(result)
        expected_sorted = sorted(expected_folders)

        self.assertEqual(result_sorted, expected_sorted)

    def test_list_folder_files_gets_all_files(self):
        """Test that list_folder_files returns all non-hidden files in a folder"""
        result = list_folder_files(self.assets_path)

        # Expected files in the root assets folder
        expected_files = [
            os.path.join(self.assets_path, "file1.txt"),
            os.path.join(self.assets_path, "file2.txt"),
        ]

        # Sort both lists for consistent comparison
        result_sorted = sorted(result)
        expected_sorted = sorted(expected_files)

        self.assertEqual(result_sorted, expected_sorted)

    def test_list_folder_files_excludes_hidden_files(self):
        """Test that list_folder_files excludes hidden files (starting with .)"""
        result = list_folder_files(self.assets_path)

        # Check that no hidden files are in the result
        for file_path in result:
            file_name = os.path.basename(file_path)
            self.assertFalse(file_name.startswith('.'),
                             f"Hidden file {file_name} should be excluded")

    def test_list_folder_files_in_subfolder(self):
        """Test that list_folder_files works correctly in subfolders"""
        folder1_path = os.path.join(self.assets_path, "folder1")
        result = list_folder_files(folder1_path)

        # Expected only file3.txt, not files from subfolder1
        expected_files = [
            os.path.join(folder1_path, "file3.txt"),
        ]

        self.assertEqual(sorted(result), sorted(expected_files))

    def test_list_folder_files_only_lists_files(self):
        """Test that list_folder_files only returns files, not directories"""
        result = list_folder_files(self.assets_path)

        # All results should be files, not directories
        for path in result:
            self.assertTrue(os.path.isfile(path),
                            f"{path} should be a file, not a directory")
