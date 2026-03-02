from datetime import date
from typing import Tuple, TypedDict

from langchain.tools import tool


class TextDate(TypedDict):
    dd: str
    mm: str
    yyyy: str

    def to_date(self):
        return date(self.yyyy, self.mm, self.dd)


class TextDateInterval(TypedDict):
    start: TextDate
    end: TextDate

    def __init__(start: TextDate, end: TextDate):
        if start.to_date() > end.to_date():
            raise ValueError("Start date is after end date, not possible")

    def to_dates(self) -> Tuple[date, date]:
        return (self.dstart.to_date(), self.dend.to_date())


def intersection(i1: TextDateInterval, i2: TextDateInterval) -> Tuple[date, date]:
    (ds1, de1) = i1.to_dates()
    (ds2, de2) = i2.to_dates()
    # Interval 1 ends before interval 2
    if de1 < ds2:
        return False
    # interval 1 starts after interval 2
    if ds1 > de2:
        return False
    return (ds2, de1)
