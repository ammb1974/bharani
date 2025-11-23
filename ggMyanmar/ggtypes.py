from dataclasses import dataclass
from enum import Enum

@dataclass
class MyanmarDate:
    year: int
    month: int
    day: int
    waxing: bool           # True = Waxing, False = Waning
    month_type: 'MonthType'
    moon_phase: str        # "New", "Waxing", "Full", "Waning"

class MonthType(Enum):
    NORMAL = 0
    INTERCALARY_BIG = 1    # ဝါကြီး
    INTERCALARY_SMALL = 2  # ဝါငယ်
