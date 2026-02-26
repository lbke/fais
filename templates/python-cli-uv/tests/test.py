import unittest
from main import echo
from packages.math import sum


class TestMethods(unittest.TestCase):
    def test_echo(self):
        self.assertEqual(echo("hello"), "hello")

    def test_sum(self):
        self.assertEqual(sum(2, 2), 4)


if __name__ == '__main__':
    unittest.main()
