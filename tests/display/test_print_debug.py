import unittest
from libs.display.print_debug import print_debug


class TestPrintDebug(unittest.TestCase):
    def test_print_debug(self):
        print("\n***** Testing print_debug function:\n")
        print_debug("This is a debug message")
