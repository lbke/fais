from datetime import date
from typing import Tuple

from langchain.tools import tool


def intersection(i1: Tuple[date, date], i2: Tuple[date, date]) -> Tuple[date, date]:
    # Interval 1 ends before interval 2
    (d1, d2) = i1
    (d3, d4) = i2
    if d2 < d3:
        return False
    # interval 1 starts after interval 2
    if d1 > d4:
        return False
    return (d3, d2)
