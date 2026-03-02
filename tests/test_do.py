from os import path
import unittest
from libs.fais import run
from libs.utils import xmlzip


class TestDo(unittest.TestCase):
    def test_changefile(self):
        fixture = path.join(path.dirname(__file__), "./assets/champ.docx")
        print(fixture)
        fixturecopy = path.join(path.dirname(__file__),
                                "./assets/champ_copy.docx")
        run(["Remplace [[champ]] par 'valeur'", fixture])
        updatedcontent = xmlzip.extract_content_xml_from_zip(fixturecopy)
        self.assertTrue(updatedcontent.find("valeur") > -1)
        self.assertTrue(updatedcontent.find("[[champ]]") == -1)
