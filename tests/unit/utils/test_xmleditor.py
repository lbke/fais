from os import path
import unittest

from libs.utils import xmlzip
from libs.utils.xmleditor import edit_xml_node_text, xml_file_to_selectable_text_map


class TextXmlEditor(unittest.TestCase):
    def test_parse(self):
        asset = path.join(path.dirname(__file__), "assets",
                          "xmleditor", "foobar.docx")
        xml_content = xmlzip.extract_content_xml_from_zip(asset)
        tm = xml_file_to_selectable_text_map(
            xml_content)
        self.assertDictEqual(tm, {"/w:document/w:body/w:p/w:r/w:t": "Hello"})

    def test_update(self):
        asset = path.join(path.dirname(__file__), "assets",
                          "xmleditor", "foobar.docx")
        xml_content = xmlzip.extract_content_xml_from_zip(asset)
        updated = edit_xml_node_text(
            "/w:document/w:body/w:p/w:r/w:t", "EDITED", xml_content)
        updated_text_map = xml_file_to_selectable_text_map(updated)
        self.assertDictEqual(
            updated_text_map,
            {"/w:document/w:body/w:p/w:r/w:t": "EDITED"},
        )
