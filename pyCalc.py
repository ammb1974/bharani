# လိုအပ်တဲ့ libraries တွေကို import လုပ်ပါ
from mycal import MyanmarDate
from datetime import datetime

# --- ဥပမာ ၁: လက်ရှိရက်စွဲကို မြန်မာပြက္ခဒိန်ပြောင်းခြင်း ---

# လက်ရှိရက်စွဲကို ရယူပါ
now_gregorian = datetime.now()

# ဂျော်ဂျီယံရက်စွဲကို မြန်မာပြက္ခဒိန် object အဖြစ် ပြောင်းလဲပါ
myanmar_date_now = MyanmarDate(now_gregorian)

# ရလဒ်တွေကို ပုံစံလိုက် ထုတ်ပြပါ
print("--- လက်ရှိရက်စွဲ ---")
print(f"ပြည့်စုံတဲ့ အချက်အလက်: {myanmar_date_now}")
print(f"မြန်မာနှစ်: {myanmar_date_now.year}")
print(f"မြန်မာလ: {myanmar_date_now.month_name}")
print(f"မြန်မာရက်: {myanmar_date_now.day}")
print(f"နေ့ရက်: {myanmar_date_now.weekday_name}")
print(f"ပွဲတော်/ရုပ်ရှင်: {myanmar_date_now.holiday if myanmar_date_now.holiday else 'မရှိ'}")
print("-" * 20)


# --- ဥပမာ ၂: သတ်မှတ်ထားတဲ့ ရက်စွဲတစ်ခုကို ပြောင်းခြင်း ---
# ဥပမာ - ၂၀၂၄ ခုနှစ်၊ ဧပြီလ ၁၇ ရက် (နှစ်သစ်ကူးနေ့)

# သတ်မှတ်ထားတဲ့ ရက်စွဲ
specific_gregorian_date = datetime(2024, 4, 17)

# မြန်မာပြက္ခဒိန် object အဖြစ် ပြောင်းလဲပါ
myanmar_date_specific = MyanmarDate(specific_gregorian_date)

# ရလဒ်တွေကို ပုံစံလိုက် ထုတ်ပြပါ
print("--- သတ်မှတ်ရက်စွဲ (၂၀၂၄-ဧပြီ-၁၇) ---")
print(f"ပြည့်စုံတဲ့ အချက်အလက်: {myanmar_date_specific}")
print(f"မြန်မာနှစ်: {myanmar_date_specific.year}")
print(f"မြန်မာလ: {myanmar_date_specific.month_name}")
print(f"မြန်မာရက်: {myanmar_date_specific.day}")
print(f"နေ့ရက်: {myanmar_date_specific.weekday_name}")
print(f"ပွဲတော်/ရုပ်ရှင်: {myanmar_date_specific.holiday if myanmar_date_specific.holiday else 'မရှိ'}")
print("-" * 20)

# --- ဥပမာ ၃: ဝါထပ်လ စစ်ဆေးခြင်း ---
# ၁၃၈၅ ခုနှစ်မှာ ဒုတိယ ဝါဆို ဝါထပ်တယ်
watat_date = datetime(2023, 7, 29) # ဒုတိယ ဝါဆိုလဆန်း ၁ ရက်
myanmar_watat_date = MyanmarDate(watat_date)

print("--- ဝါထပ်လ စစ်ဆေးမှု ---")
print(f"ရက်စွဲ: {watat_date.strftime('%Y-%m-%d')}")
print(f"မြန်မာပြက္ခဒိန်: {myanmar_watat_date}")
# ဝါထပ်လမှန်း သိရန် intercalary_month နဲ့ intercalary_day တွေကို စစ်ဆေးနိုင်ပါတယ်
print(f"ဝါထပ်လလား? {'ဟုတ်' if myanmar_watat_date.intercalary_month else 'မဟုတ်'}")
print(f"ဝါထပ်ရက်လား? {'ဟုတ်' if myanmar_watat_date.intercalary_day else 'မဟုတ်'}")
print("-" * 20)