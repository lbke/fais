from os import path
import unittest

from libs.tools.documents import read_document_file_text_content


class TestDocumentsTools(unittest.TestCase):
    def test_read_document_file_text_content(self):
        dir = path.dirname(__file__)
        filepath = path.join(dir, "./assets/foo.odt")
        content = read_document_file_text_content.invoke(filepath)
        self.assertTrue(content.find("foo") > -1)
        # No XML left
        self.assertFalse(content.find("<") > -1)
