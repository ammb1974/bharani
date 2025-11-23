def gregorian_to_jdn(year: int, month: int, day: int) -> int:
    """Convert Gregorian date to Julian Day Number"""
    if month <= 2:
        year -= 1
        month += 12
    A = year // 100
    B = 2 - A + (A // 4)
    jdn = int(365.25*(year + 4716)) + int(30.6001*(month + 1)) + day + B - 1524
    return jdn
