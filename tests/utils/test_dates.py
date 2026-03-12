from datetime import date
import unittest

from libs.utils.dates import intersection


class TestPlanning(unittest.TestCase):
    # def test_interval(self):
    #    d1 = TextDate("1", "3", "2026")
    #    d2 = TextDate("3", "3", "2026")
    #    d3 = TextDate("2", "3", "2026")
    #    d4 = TextDate("4", "3", "2026")
    #    i1 = TextDateInterval(d1, d2)
    #    i2 = TextDateInterval(d3, d4)
    #    (start, end) = intersection(i1, i2)
    #    self.assertEqual(start.day, "3")
    #    self.assertEqual(start.month, "3")
    #    self.assertEqual(start.year, "2026")
    #    self.assertEqual(end.day, "3")
    #    self.assertEqual(end.month, "3")
    #    self.assertEqual(end.year, "2026")
    def test_interval(self):
        d1 = date(day=1, month=3, year=2026)
        d2 = date(day=3, month=3, year=2026)
        d3 = date(day=2, month=3, year=2026)
        d4 = date(day=5, month=3, year=2026)
        i1 = (d1, d2)
        i2 = (d3, d4)
        (start, end) = intersection(i1, i2)
        self.assertEqual(start.day, 2)
        self.assertEqual(start.month, 3)
        self.assertEqual(start.year, 2026)
        self.assertEqual(end.day, 3)
        self.assertEqual(end.month, 3)
        self.assertEqual(end.year, 2026)
