from os import path
import os
import unittest
from unittest.mock import patch

from libs.fais import fais


class TestHIL(unittest.TestCase):
    def test_copy_file(self):
        """
        Copy tool is expected to trigger human in the loop interrupt
        """
        fixture = path.abspath(path.join(path.dirname(__file__),
                                         "./assets/test_hil/file.txt"))
        # TODO: it would be ideal to test an actual "enter" key press in stdin
        # This test is the lazy AI suggestion (but cool to learn unittest patch at least)
        # + ideally we should test the proper prompt options display
        with patch("libs.fais.choice", return_value="approve"):
            fais(
                [f"Copie le fichier {fixture} vers file_copy.txt dans le même dossier"])
        expected = path.abspath(path.join(path.dirname(__file__),
                                          "./assets/test_hil/file_copy.txt"))
        self.assertTrue(path.exists(expected))
        os.unlink(expected)
