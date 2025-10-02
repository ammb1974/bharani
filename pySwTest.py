import swisseph as swe
import datetime
from typing import Dict, List, Tuple

class BirthChartCalculator:
    def __init__(self):
        """Swiss Ephemeris စာရင်းအင်းဖိုင်များ အစပျိုးခြင်း"""
        swe.set_ephe_path(None)  # အလိုအလျောက်ရှာဖွေခြင်း
        
        # ဂြိုဟ်များ၏ အမည်များ
        self.planet_names = {
            swe.SUN: "Sun",
            swe.MOON: "Moon",
            swe.MERCURY: "Mercury",
            swe.VENUS: "Venus",
            swe.MARS: "Mars",
            swe.JUPITER: "Jupiter",
            swe.SATURN: "Saturn",
            swe.URANUS: "Uranus",
            swe.NEPTUNE: "Neptune",
            swe.PLUTO: "Pluto",
            swe.MEAN_NODE: "North Node"
        }
        
        # ရာသီခွင်များ
        self.zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", 
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
    
    def calculate_birth_chart(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        latitude: float,
        longitude: float,
        timezone: float = 0.0,
        house_system: str = 'P'
    ) -> Dict:
        """
        မွေးနေ့ဇာတာ တွက်ချက်ခြင်း
        """
        # Local time ကို UTC သို့ ပြောင်းခြင်း
        utc_hour = hour - timezone
        if utc_hour < 0:
            utc_hour += 24
            day -= 1
        elif utc_hour >= 24:
            utc_hour -= 24
            day += 1
        
        # ပြင်ဆင်ချက်: UTC time ကို decimal hours အဖြစ် ပြောင်းလဲခြင်း
        decimal_hours = utc_hour + minute / 60.0
        
        # Julian Day တွက်ချက်ခြင်း (swe.julday ကိုအသုံးပြု)
        jd = swe.julday(year, month, day, decimal_hours)
        
        # ဇာတာအိမ်များ တွက်ချက်ခြင်း
        houses = swe.houses(jd, latitude, longitude, house_system.encode())
        
        # ဂြိုဟ်များ၏ နေရာများ တွက်ချက်ခြင်း
        planets = {}
        for planet_id in self.planet_names.keys():
            try:
                position = swe.calc_ut(jd, planet_id, swe.FLG_SWIEPH)[0]
                planets[planet_id] = {
                    "longitude": position[0],
                    "latitude": position[1],
                    "distance": position[2],
                    "speed": position[3],
                    "sign": self.get_zodiac_sign(position[0]),
                    "sign_degree": position[0] % 30,
                    "house": self.get_planet_house(position[0], houses[0])
                }
            except Exception as e:
                print(f"Error calculating planet {planet_id}: {e}")
                planets[planet_id] = None
        
        return {
            "birth_info": {
                "date": f"{year}-{month:02d}-{day:02d}",
                "time": f"{hour:02d}:{minute:02d}",
                "location": f"{latitude:.4f}, {longitude:.4f}",
                "timezone": timezone,
                "julian_day": jd
            },
            "houses": {
                "cusps": houses[0],
                "ascendant": houses[1][0],
                "mc": houses[1][1],
                "armc": houses[1][2],
                "vertex": houses[1][3]
            },
            "planets": planets,
            "angles": {
                "ascendant": {
                    "longitude": houses[1][0],
                    "sign": self.get_zodiac_sign(houses[1][0]),
                    "sign_degree": houses[1][0] % 30
                },
                "mc": {
                    "longitude": houses[1][1],
                    "sign": self.get_zodiac_sign(houses[1][1]),
                    "sign_degree": houses[1][1] % 30
                }
            }
        }
    
    def get_zodiac_sign(self, longitude: float) -> str:
        """လောင်ဂျီကျုဒ်ကို ရာသီခွင်အဖြစ် ပြောင်းလဲခြင်း"""
        return self.zodiac_signs[int(longitude / 30) % 12]
    
    def get_planet_house(self, planet_longitude: float, house_cusps: List[float]) -> int:
        """ဂြိုဟ်တစ်ခု ရှိရာ ဇာတာအိမ်ကို ဆုံးဖြတ်ခြင်း"""
        for i in range(12):
            next_house = (i + 1) % 12
            if house_cusps[i] <= planet_longitude < house_cusps[next_house]:
                return i + 1
        return 12  # နောက်ဆုံးအိမ်

    def print_birth_chart(self, chart_data: Dict):
        """မွေးနေ့ဇာတာကို ဖတ်ရှုလွယ်ကူစွာ ပုံစံဖော်ပြခြင်း"""
        print("\n" + "="*50)
        print("🌟 BIRTH CHART 🌟")
        print("="*50)
        
        # မွေးချိန်နှင့်နေရာ
        birth_info = chart_data["birth_info"]
        print(f"\n📅 Birth Date: {birth_info['date']}")
        print(f"⏰ Birth Time: {birth_info['time']}")
        print(f"📍 Location: {birth_info['location']}")
        print(f"🌍 Timezone: UTC{birth_info['timezone']:+.1f}")
        
        # ဇာတာအိမ်များ
        print("\n🏠 HOUSE CUSPS:")
        houses = chart_data["houses"]
        for i, cusp in enumerate(houses["cusps"]):
            sign = self.get_zodiac_sign(cusp)
            degree = cusp % 30
            print(f"  House {i+1:2d}: {sign} {degree:5.2f}°")
        
        # အဓိကထောင့်များ
        print("\n📐 ANGLES:")
        angles = chart_data["angles"]
        ascendant = angles["ascendant"]
        mc = angles["mc"]
        print(f"  Ascendant: {ascendant['sign']} {ascendant['sign_degree']:5.2f}°")
        print(f"  MC:         {mc['sign']} {mc['sign_degree']:5.2f}°")
        
        # ဂြိုဟ်များ
        print("\n🪐 PLANETS:")
        planets = chart_data["planets"]
        for planet_id, planet_data in planets.items():
            if planet_data:
                name = self.planet_names[planet_id]
                sign = planet_data["sign"]
                degree = planet_data["sign_degree"]
                house = planet_data["house"]
                retrograde = "R" if planet_data["speed"] < 0 else ""
                print(f"  {name:10s}: {sign:10s} {degree:5.2f}° (House {house}) {retrograde}")
        
        print("\n" + "="*50)

# အသုံးပြုပုံဥပမာ
if __name__ == "__main__":
    # ဇာတာတွက်ချက်ကိရိယာ ဖန်တီးခြင်း
    calculator = BirthChartCalculator()
    
    # မွေးနေ့ဇာတာ တွက်ချက်ခြင်း (ဥပမာ: ရန်ကုန်မြို့ ၁၉၉၀ ခုနှစ် မေလ ၁၅ ရက် နံနက် ၈:၃၀)
    birth_chart = calculator.calculate_birth_chart(
        year=1990,
        month=5,
        day=15,
        hour=8,
        minute=30,
        latitude=16.8661,  # ရန်ကုန်မြို့ လတ္တီကျုဒ်
        longitude=96.1951,  # ရန်ကုန်မြို့ လောင်ဂျီကျုဒ်
        timezone=6.5,  # မြန်မာစံတော်ချိန်
        house_system='P'  # Placidus စနစ်
    )
    
    # ရလဒ်ကို ပုံနှိပ်ခြင်း
    calculator.print_birth_chart(birth_chart)