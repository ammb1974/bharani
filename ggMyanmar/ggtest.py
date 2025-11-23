# examples/test.py
from .ggconverter import convert_to_myanmar

date = convert_to_myanmar(2025, 11, 20)
print(f"Myanmar Date: {date.year}-{date.month}-{date.day}")
print(f"Waxing: {date.waxing}, Moon Phase: {date.moon_phase}, Month Type: {date.month_type.name}")
