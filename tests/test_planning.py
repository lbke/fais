import unittest

from libs.utils.textdates import TextDate, TextDateInterval, intersection


class TestPlanning(unittest.TestCase):
    def test_interval(self):
        d1 = TextDate("1", "3", "2026")
        d2 = TextDate("3", "3", "2026")
        d3 = TextDate("2", "3", "2026")
        d4 = TextDate("4", "3", "2026")
        i1 = TextDateInterval(d1, d2)
        i2 = TextDateInterval(d3, d4)
        (start, end) = intersection(i1, i2)
        self.assetEqual(start.day, "3")
        self.assetEqual(start.month, "3")
        self.assetEqual(start.year, "2026")
        self.assetEqual(end.day, "3")
        self.assetEqual(end.month, "3")
        self.assetEqual(end.year, "2026")
