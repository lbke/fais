from os import path
import unittest

from libs.tools.documents import copy_file, read_document_file_text_content


local_dir = path.dirname(__file__)
assets_dir = path.join(local_dir, "./assets")


class TestDocumentsTools(unittest.TestCase):
    def test_read_document_file_text_content(self):
        filepath = path.join(assets_dir, "./foo.odt")
        content = read_document_file_text_content.invoke(filepath)
        self.assertTrue(content.find("foo") > -1)
        # No XML left
        self.assertFalse(content.find("<") > -1)

    def test_copyfile_dst_does_not_exist(self):
        not_exist_dir = path.join(assets_dir, "does_not_exist")
        copy_res = copy_file.invoke(
            {"filepath": "./foo.py", "new_directory_or_filepath": not_exist_dir})
        self.assertTrue(copy_res.startswith("Warning"))
