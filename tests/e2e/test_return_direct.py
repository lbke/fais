import unittest

from libs.fais import fais


class TestReturnDirect(unittest.TestCase):
    def test_return_direct(self):
        res = fais(
            ["demo the return_direct tool : call it alongside the list files tool for current folder"])
        self.assertTrue("Output of tool list_files:" in res[-1].content)
