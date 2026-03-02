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

    def test_intersect(self):
        res = run(
            ["Intersection 01 mars 2026/03 mars 2026  et 02 mars 2026/05 mars 2026. Output format: DD/MM/YYYY-DD/MM/YYYY. Your answer should only output the response."])
        print(res)
        self.assertEqual(res.content, "02/03/2026-03/03/2026")
