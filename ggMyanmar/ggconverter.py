from ggcalendar_core import calculate_myanmar_date
from ggtypes import MyanmarDate

def convert_to_myanmar(year: int, month: int, day: int) -> MyanmarDate:
    return calculate_myanmar_date(year, month, day)
