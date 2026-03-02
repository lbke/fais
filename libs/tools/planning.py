from ast import Tuple
from datetime import date

from langchain.tools import tool

from libs.utils.textdates import TextDateInterval, intersection


@tool
def planning_intersection(i1: TextDateInterval, i2: TextDateInterval) -> Tuple[date, date]:
    """
    Compute the intersection between two date intervals
    Output the intersection interval as two dates
    Output false if impossible to obtain 
    """
    return intersection(i1, i2)
