# burmese_calendar.py
import swisseph as swe
import math
from datetime import datetime, timedelta
import zconstants # ဒီနေရာမှာ constants.py ကို import လုပ်ထားပါတယ်

# Myanmar Era (ME) စတဲ့ ရက်စွဲ (Gregorian Date: 638 March 21)
# ဒါကို Julian Day Number (JDN) နဲ့ ဖော်ပြလို့ရပါတယ်။
# JDN ဆိုတာ နေ့ရက်တွေကို ဂဏန်းတစ်ခုတည်းနဲ့ ကိုင်တွယ်တဲ့ စနစ်ပါ။
ME_START_JDN = 1954168.050623

def gregorian_to_jdn(year, month, day):
    """Convert Gregorian date to Julian Day Number."""
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    jdn = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5
    return jdn

def calculate_new_moon(jdn):
    """
    Calculate the Julian Day Number of the new moon closest to the given JDN.
    ဒီနေရာမှာ ပိုမိုတိကျတဲ့ swe.find_moon_phase() ကို သုံးပါမယ်။
    """
    # swe.find_moon_phase() ကိုသုံးပြီး လဆန်းညကို တိုက်ရိုက်ရှာပါတယ်။
    # swe.NEW_MOON ဆိုတာ လဆန်းညကို ရည်ညွှန်းတဲ့ constant ဖြစ်ပါတယ်။
    # ဒီ function က (jdn_of_phase, retcode) ဆိုပြီး tuple တစ်ခုပြန်ပေးမှာ ဖြစ်တဲ့အတွက် 
    # ပထမဆုံး value ဖြစ်တဲ့ jdn ကိုပဲ ယူပါမယ်။
    jdn_of_new_moon, retcode = swe.find_moon_phase(jdn, swe.NEW_MOON)
    print("new moon is fine")
    return jdn_of_new_moon

class BurmeseDate:
    def __init__(self, year, month, day, is_wat_htat=False, is_yat_ngan=False):
        self.year = year
        self.month = month
        self.day = day
        self.is_wat_htat = is_wat_htat
        self.is_yat_ngan = is_yat_ngan

    def __str__(self):
        month_name = zconstants.MYANMAR_MONTHS[self.month - 1]
        wat_htat_str = " (ဝါထပ်)" if self.is_wat_htat else ""
        yat_ngan_str = " (ရက်ငင်)" if self.is_yat_ngan else ""
        return f"{self.year} ခုနှစ်၊ {month_name}{wat_htat_str}လဆန်း {self.day} ရက်{yat_ngan_str}"

def convert(gregorian_date):
    """
    Convert a Gregorian date to a Burmese date.
    This is a simplified version for demonstration.
    """
    jdn = gregorian_to_jdn(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    
    # 1. မြန်မာနှစ်ကို ရှာပါမယ်။
    # တစ်နှစ်မှာ ရက် ၃၅၄ ရက် သို့မဟုတ် ၃၈၄ ရက် (ဝါထပ်နှစ်) ရှိတယ်။
    # ဒီကိန်းက ပျမ်းမျှအားဖြင့် နှစ်ပေါင်း ၁၉ နှစ်မှာ ဝါထပ် ၇ ကြိမ်ထပ်တယ်။
    year_diff = (jdn - ME_START_JDN) / 354.36708614
    myanmar_year = int(year_diff) + 1
    
    # 2. လဆန်းညတွေကို စဉ်ဆက်မပြတ် ရှာပါမယ်။
    # ဒီနေရာမှာတော့ ရှုပ်ထွေးတဲ့ တွက်ချက်မှုတွေပါဝင်ပါတယ်။
    # ရိုးရှင်းအောင် လက်ရှိရက်ရဲ့ အရင်က လဆန်းညကို ရှာမယ်။
    # ဒါဆိုရင် လက်ရှိလဆန်းညနဲ့ အရင်လဆန်းညကြားမှာ ကျွန်တော်တို့ရဲ့ ရက်စွဲရှိနေမယ်။
    # ဒီ logic က အရမ်းရိုးရှင်းပြီး အမှားပါနိုင်ပါတယ်။ တကယ့်အသုံးချမှုအတွက် ပိုပြီးရှုပ်ထွေးတဲ့ Algorithm လိုပါတယ်။
    # ဥပမာ - တန်ခူးလဆန်းည၊ ကဆုန်လဆန်းည စသဖြင့် တစ်နှစ်စာလုံးကို ရှာရပါမယ်။
    
    # ဒီဥပမာအတွက် ရိုးရှင်းတဲ့ တွက်နည်းလမ်းတစ်ခုကို သုံးပါမယ်။
    # လဆန်းညကို ရှာပြီး နောက်လဆန်းညကို ရှာပါမယ်။ ကြားက ရက်တွေက ဒီလမှာရှိတယ်။
    # ဒီနည်းလမ်းက လက်ရှိလကိုပဲ ရှာတာမို့ တကယ့်ပြက္ခဒိန်အတိုင်း မရပါဘူး။
    # သို့ပေမယ့် သဘောပေါက်ဖို့အတွက် လုံလောက်ပါတယ်။
    
    # လက်ရှိလဆန်းည
    current_new_moon_jdn = calculate_new_moon(jdn)
    # အရင်လဆန်းည
    previous_new_moon_jdn = calculate_new_moon(current_new_moon_jdn - 25)
    
    # လဆန်း ၁ ရက်နေ့ကို ရှာပါမယ်။
    day_of_month = int(jdn - previous_new_moon_jdn) + 1
    
    # လကို ခန့်မှန်းရပါမယ်။ ဒါက အရမ်းရှုပ်ထွေးပါတယ်။
    # ဒီနေရာမှာတော့ ရိုးရှင်းတဲ့ ခန့်မှန်းချက်တစ်ခုကို သုံးပါမယ်။
    # တန်ခူးလက မတ်လ/ဧပြီလလေးတွေမှာ ရှိတယ်။
    # ဒီဟာက တိကျတဲ့ နည်းလမ်းမဟုတ်ပါဘူး။
    month_index = (gregorian_date.month - 3 + 12) % 12
    
    # ဝါထပ် (Intercalary Month) နဲ့ ရက်ငင် (Intercalary Day) တွေကို စစ်ဆေးရပါမယ်။
    # ဒါကလည်း အရမ်းရှုပ်ထွေးတဲ့ တွက်ချက်မှုတွေလိုပါတယ်။
    # ဒီဥပမာမှာ အလွယ်တကူ ထည့်သွင်းထားပါတယ်။
    is_wat_htat = False # ဒီနေရာမှာ ဝါထပ်ကို စစ်ဆေးရမယ်။
    is_yat_ngan = False # ဒီနေရာမှာ ရက်ငင်ကို စစ်ဆေးရမယ်။
    
    # ဥပုသ်နေ့နဲ့ ရက်ရာဇာ
    sabbath = False
    yatyaza = False
    if day_of_month in [8, 15, 23]:
        sabbath = True
    
    # ရက်ရာဇာက တနင်္ဂနွေ၊ အင်္ဂါ၊ ဗုဒ္ဓဟူး၊ စနေတို့မှာ ပါဝင်တတ်ပြီး
    # လဆန်း ၁ ရက်နေ့က အဲဒီတနင်္ဂနွေရက်တွေထဲက တစ်ခုဖြစ်ရင် အဲဒီလရဲ့ ရက်ရာဇာကို ရှာရမယ်။
    # ဒါကလည်း ရှုပ်ထွေးတဲ့ စည်းမျဉ်းတွေရှိပါတယ်။
    
    return BurmeseDate(myanmar_year, month_index, day_of_month, is_wat_htat, is_yat_ngan)