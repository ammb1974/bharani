import swisseph as swe

# Set ephemeris file path
swe.set_ephe_path('./ephe')

# Input data
year, month, day = 1937, 6, 15
hour, minute = 23, 00
timezone_offset = -6  # Myanmar Time

# Location0000
latitude = 33.916
longitude = -102.3167

# Convert to Julian Day (Universal Time)
ut = hour + minute / 60.0
jd = swe.julday(year, month, day, ut - timezone_offset)

# Planet IDs
planets = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
    "Ketu": swe.TRUE_NODE
}

# Rāśi names (Burmese zodiac signs)
rasi_names = [
    "♈", "♉", "♊", "♋",
    "♌", "♍", "♎", "♏",
    "♐", "♑", "♒", "♓"
]

# Conversion function
def convert_to_rasi(degree):
    rasi_index = int(degree // 30)
    rasi_name = rasi_names[rasi_index]
    
    rasi_deg = degree % 30
    deg = int(rasi_deg)
    min_float = (rasi_deg - deg) * 60
    minute = int(min_float)
    second = int((min_float - minute) * 60)
    
    return rasi_name, deg, minute, second

# 🪐 Planetary Positions
print("📍 Planetary Positions:")
for name, pid in planets.items():
    pos, _ = swe.calc_ut(jd, pid)
    rasi, deg, minute, second = convert_to_rasi(pos[0])
    print(f"{name}: {rasi} {deg}° {minute}′ {second}″")

# 🏠 House Cusps & Angles
print("\n🏠 House Cusps & Angles:")
# Use Placidus system (default)
cusps, ascmc = swe.houses(jd, latitude, longitude)

# Ascendant & MC
asc_rasi, asc_deg, asc_min, asc_sec = convert_to_rasi(ascmc[0])
mc_rasi, mc_deg, mc_min, mc_sec = convert_to_rasi(ascmc[1])
print(f"Ascendant: {asc_rasi} {asc_deg}° {asc_min}′ {asc_sec}″")
print(f"MC       : {mc_rasi} {mc_deg}° {mc_min}′ {mc_sec}″")

# House Cusps 1–12
for i in range(12):
    cusp_deg = cusps[i]
    rasi, deg, minute, second = convert_to_rasi(cusp_deg)
    print(f"House {i+1}: {rasi} {deg}° {minute}′ {second}″")