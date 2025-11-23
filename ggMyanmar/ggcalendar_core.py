from ggtypes import MyanmarDate, MonthType
from ggjulian import gregorian_to_jdn
from ggastro import get_moon_phase

def calculate_myanmar_date(year: int, month: int, day: int) -> MyanmarDate:
    """Basic Myanmar calendar calculation"""
    jdn = gregorian_to_jdn(year, month, day)
    moon_phase = get_moon_phase(jdn)
    waxing = moon_phase in ("New", "Waxing")

    # Simple intercalary month placeholder (second Waso every 3 years)
    if month == 4 and year % 3 == 0:
        month_type = MonthType.INTERCALARY_BIG
    else:
        month_type = MonthType.NORMAL

    day_in_month = (jdn % 30) + 1  # Approximate lunar day
    myanmar_month = ((month - 1) % 12) + 1

    return MyanmarDate(
        year=year,
        month=myanmar_month,
        day=day_in_month,
        waxing=waxing,
        month_type=month_type,
        moon_phase=moon_phase
    )
