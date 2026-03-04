from datetime import date
import dateutil
from typing import NamedTuple

from langchain.tools import tool

from libs.utils.dates import intersection


class TextDate(NamedTuple):
    dd: str
    mm: str
    yyyy: str

    def to_date(self):
        return dateutil.parse(self.to_str(), "%DD/%MM/%YYYY")

    def to_str(self):
        return f"{self.dd}/{self.mm}/{self.yyyy}"


class TextDateInterval(NamedTuple):
    start: TextDate
    end: TextDate

    def to_dates(self) -> tuple[date, date]:
        if self.start.to_date() > self.end.to_date():
            raise ValueError("Start date is after end date, not possible")
        return (self.start.to_date(), self.end.to_date())


@tool
def planning_intersection(i1: TextDateInterval, i2: TextDateInterval) -> tuple[date, date]:
    """
    Compute the intersection between two date intervals
    Output the intersection interval as two dates
    Output false if impossible to obtain 
    """
    return intersection(i1, i2)


TOOLS=[planning_intersection]