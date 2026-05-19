from os import path
import unittest

from libs.tools.documents import copy_file, read_document_file_text_content


local_dir = path.dirname(__file__)
assets_dir = path.join(local_dir, "./assets")


class TestDocumentsTools(unittest.TestCase):
    # Copyfile
    def test_copyfile_dst_does_not_exist(self):
        not_exist_dir = path.join(assets_dir, "does_not_exist")
        # We catch the FileNotFoundError in the middleware, so we should not have it here, but a string content instead
        with self.assertRaises(FileNotFoundError) as err:
            copy_res = copy_file.invoke(
                {"filepath": "./foo.py", "new_directory_or_filepath": not_exist_dir})
        # self.assertTrue(copy_res.startswith("Warning"))
