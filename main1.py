import swisseph as swe

# Set ephemeris path (adjust if needed)
swe.set_ephe_path(".")

# 📋 Input birth data
year, month, day = 2001, 12, 25
hour, minute = 7, 45
latitude = 21.9588   # Mandalay
longitude = 96.0891
timezone = 6.5       # Myanmar Time

# 🧭 Set sidereal mode to Lahiri
swe.set_sid_mode(swe.SIDM_LAHIRI)

# 📅 Julian Day
ut = hour + minute / 60.0
jd = swe.julday(year, month, day, ut - timezone)

# 🌟 Planetary positions (sidereal)
print("🌟 Planetary Positions (Sidereal - Lahiri)")
planets = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
           swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO]

for planet in planets:
    lon, _ = swe.calc(jd, planet)
    sidereal_lon = lon % 360  # Optional: only needed if lon > 360
    rāśi = int(sidereal_lon // 30)
    deg = int(sidereal_lon % 30)
    min = int((sidereal_lon % 1) * 60)
    sec = int((((sidereal_lon % 1) * 60) % 1) * 60)
    print(f"{swe.get_planet_name(planet)}: Rāśi {rāśi + 1}, {deg}°{min}'{sec}\"")

# 🧭 Ascendant & 🏠 House cusps
print("\n🧭 Ascendant & House Cusps (Sidereal - Lahiri)")
cusps, ascmc = swe.houses(jd, latitude, longitude, b'A')  # Placidus system

# Ascendant
ayanamsa = swe.get_ayanamsa(jd)
asc_sidereal = (ascmc[0] - ayanamsa) % 360
asc_rasi = int(asc_sidereal // 30)
asc_deg = int(asc_sidereal % 30)
asc_min = int((asc_sidereal % 1) * 60)
asc_sec = int((((asc_sidereal % 1) * 60) % 1) * 60)
print(f"Ascendant: Rāśi {asc_rasi + 1}, {asc_deg}°{asc_min}'{asc_sec}\"")

# House cusps
for i, cusp in enumerate(cusps[:12], start=1):
    cusp_sidereal = (cusp - ayanamsa) % 360
    rasi = int(cusp_sidereal // 30)
    deg = int(cusp_sidereal % 30)
    min = int((cusp_sidereal % 1) * 60)
    sec = int((((cusp_sidereal % 1) * 60) % 1) * 60)
    print(f"House {i}: Rāśi {rasi + 1}, {deg}°{min}'{sec}\"")