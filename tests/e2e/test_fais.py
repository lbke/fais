from os import path
import unittest
from libs.fais import fais
from libs.utils import xmlzip


class TestFais(unittest.TestCase):
    def test_intersect(self):
        res = fais(
            ["Intersection 01 mars 2026/03 mars 2026  et 02 mars 2026/05 mars 2026. Output format: DD/MM/YYYY-DD/MM/YYYY. Your answer should only output the response."])
        print(res)
        self.assertTrue("02/03/2026-03/03/2026" in res[-1].content)

    def test_parallel_tools(self):
        """
        TODO: not finalized but should open 2 files in parallel and print results correctly
        """
        res = fais(
            ["Ouvre deux fichiers en même temps"])
        print(res)

    def test_errors(self):
        res = fais("Ouvre le fichier ./fake-test.txt")
        print(res)
