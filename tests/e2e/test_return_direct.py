import unittest

from libs.fais import fais


class TestReturnDirect(unittest.TestCase):
    res = fais(
        ["demo the return_direct tool : call it alongside the list files tool for current folder"])
    print(res)
