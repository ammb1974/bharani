import swisseph as swe

# Swiss Ephemeris စတင်ပါ
swe.set_ephe_path()  # Ephemeris files ရှိရာ folder (သို့မဟုတ် မထားရင် default)

# မွေးနေ့၊ အချိန်၊ နေရာ ထည့်ပါ
year, month, day = 1990, 4, 15  # ဥပမာ: ဧပြီ ၁၅၊ ၁၉၉၀
hour = 6.0 + 5.5  # မွေးချိန် (ဥပမာ: 6:30 AM IST) → UTC+5:30 ဖြစ်လို့ UTC ကို 5.5 နဲ့ နုတ်ပါ (hour = 1.0)
lat = 22.5726  # Kolkata (East India)
lon = 88.3639
tz = 5.5  # အိန္ဒိယ အချိန် (UTC+5:30)

# UTC အချိန်ကို Julian Day အဖြစ်ပြောင်းပါ
jd = swe.julday(year, month, day, hour - tz)  # UTC အချိန်ကိုသုံးပါ

# 🌟 Vedic အတွက် Ayanamsa: Lahiri (Chitrapaksha)
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Ascendant (Lagna) တွက်ပါ
house_system = b'P'  # Placidus နဲ့ တွက်မယ် (Ascendant အတွက်)
cusps, ascmc = swe.houses(jd, lat, lon, house_system)
asc_deg = ascmc[0]  # Ascendant ဒီဂရီ

# ရာသီနာမည် (Sanskrit နဲ့ အင်္ဂလိပ်)
rasi_names = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# ဂြိုဟ်အမည်များ
planet_names = [
    'Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
    'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Rahu'
]
planet_ids = [
    swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
    swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO
]

print("=== VEDIC ASTROLOGY CHART (East Indian Style) ===")
print(f"Date: {day}/{month}/{year}, Time: {hour - tz:.2f} UTC ({hour:.2f} IST)")
print(f"Location: Lat {lat}, Lon {lon}")
print(f"Ascendant (Lagna): {rasi_names[int(asc_deg/30)]} {(asc_deg % 30):.2f}°")
print("\n--- ဂြိုဟ်တိုင်း၏ ရာသီနှင့် ဘာဝ (Whole Sign System) ---")

# ဘာဝ ၁ ကို Lagna ရာသီအဖြစ်သတ်မှတ်ပါ
lagna_rasi = int(asc_deg / 30)

# ဂြိုဟ်တိုင်းအတွက်
for i, planet_id in enumerate(planet_ids):
    p = swe.calc(jd, planet_id)
    lon = p[0][0]  # Sidereal longitude (Lahiri ကြောင့်)

    rasi_num = int(lon / 30)
    pos_in_rasi = lon % 30

    # ဘာဝတွက် (Whole Sign)
    house = (rasi_num - lagna_rasi) % 12 + 1

    print(f"{planet_names[i]}: {rasi_names[rasi_num]} {pos_in_rasi:.2f}° | ဘာဝ: {house}")

# Rahu ကို အထူးတွက်ပါ (Mean Node)
rahu = swe.calc(jd, swe.MEAN_NODE)
rahu_lon = rahu[0][0]
rasi_num = int(rahu_lon / 30)
house = (rasi_num - lagna_rasi) % 12 + 1
print(f"Rahu: {rasi_names[rasi_num]} {(rahu_lon % 30):.2f}° | ဘာဝ: {house}")

# Ketu က Rahu နဲ့ 180° ပြောင်း
ketu_lon = (rahu_lon + 180) % 360
rasi_num = int(ketu_lon / 30)
house = (rasi_num - lagna_rasi) % 12 + 1
print(f"Ketu: {rasi_names[rasi_num]} {(ketu_lon % 30):.2f}° | ဘာဝ: {house}")

