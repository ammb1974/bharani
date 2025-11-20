import tkinter as tk
from tkinter import messagebox
import json
import os
import math
from datetime import datetime

# === ဝါထပ်နှစ်များ ဖတ်ယူခြင်း ===
def load_watat_years():
    if not os.path.exists("watat_years.json"):
        messagebox.showerror("ဖိုင်မတွေ့ပါ", "watat_years.json ဖိုင်ကို မတွေ့ပါ။\nဖိုင်ကို ဤ program နှင့် အတူတူ ထားပါ။")
        return set()
    try:
        with open("watat_years.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("watat_years", []))
    except Exception as e:
        messagebox.showerror("ဖိုင်ဖတ်ရာတွင် အမှား", str(e))
        return set()

WATAT_YEARS = load_watat_years()

# === အခြေခံ တွက်ချက်မှုများ ===
def gregorian_to_jd(gy, gm, gd):
    a = (14 - gm) // 12
    y = gy + 4800 - a
    m = gm + 12 * a - 3
    return gd + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

def myanmar_new_year_jd(me):
    MO_EPOCH = 1954168.0506
    SY = 365.258756481
    return math.floor(MO_EPOCH + me * SY)

def gregorian_to_myanmar(gy, gm, gd):
    jd = gregorian_to_jd(gy, gm, gd)
    MO_EPOCH = 1954168.0506
    SY = 365.258756481
    me = math.floor((jd - MO_EPOCH) / SY)
    be = me  # ✅ မှန်ကန်: ME ပင် မြန်မာခုနှစ်ဖြစ်ပါသည်

    # နှစ်ညှိရန်
    if jd < myanmar_new_year_jd(me):
        me -= 1
        be -= 1
    elif jd >= myanmar_new_year_jd(me + 1):
        me += 1
        be += 1

    watat = be in WATAT_YEARS
    first_day = myanmar_new_year_jd(me)  # တန်ခူး လစ JD

    # လများကို တစ်လချင်း တည်ဆောက်ပါ
    months = []
    current_jd = first_day
    for i in range(12):
        if i == 11:  # တပေါင်း (လ 12)
            days = 30 if watat else 29
        else:
            days = 30 if (i % 2 == 0) else 29  # 1,3,5,7,9,11 → 30; 2,4,6,8,10 → 29
        months.append((i + 1, current_jd, days))
        current_jd += days

    if watat:
        # ဝါထပ်လကို ဝါဆို (လ 4) နောက်တွင် ထည့်ပါ
        waso_end = months[3][1] + months[3][2]
        months.insert(4, (4, waso_end, 30))

    # မှန်ကန်သော လကို ရှာပါ
    for m_num, m_start, m_len in months:
        if jd < m_start + m_len:
            full_moon_jd = m_start + 14  # လပြည့်နေ့
            if jd <= full_moon_jd:
                day_str = f"လဆန်း {int(jd - m_start + 1)} ရက်"
            else:
                day_str = f"လဆုတ် {int(jd - full_moon_jd)} ရက်"
            is_leap = (m_num == 4 and len(months) > 12 and m_start == waso_end)
            return be, m_num, day_str, is_leap, watat

    return be, 12, f"ရက် {int(jd - first_day + 1)}", False, watat

# === GUI ===
def convert_date():
    try:
        gy = int(year_entry.get())
        gm = int(month_entry.get())
        gd = int(day_entry.get())

        if not (1 <= gm <= 12):
            raise ValueError("လသည် 1 မှ 12 ကြားဖြစ်ရပါမည်")
        if not (1 <= gd <= 31):
            raise ValueError("ရက်သည် 1 မှ 31 ကြားဖြစ်ရပါမည်")

        be, mm, day_str, is_leap, watat = gregorian_to_myanmar(gy, gm, gd)

        months = [
            "တန်ခူး", "ကဆုန်", "နယုန်", "ဝါဆို", "ဝါခေါက်",
            "တော်သလင်း", "သီတင်းကျွတ်", "တန်ဆောင်မုန်း",
            "နတ်တော်", "ပြာသို", "တပို့တွဲ", "တပေါင်း"
        ]

        if is_leap:
            month_name = "ဝါထပ်"
        else:
            month_name = months[mm - 1] if 1 <= mm <= 12 else f"လ {mm}"

        weekdays = ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ကြာသပတေး", "သောကြာ", "စနေ"]
        jd = gregorian_to_jd(gy, gm, gd)
        wd = int((jd + 1) % 7)

        result = f"မြန်မာ ရက်စွဲ:\n"
        result += f"ခုနှစ်: {be}\n"
        result += f"လ: {month_name}\n"
        result += f"ရက်: {day_str}\n"
        result += f"နေ့: {weekdays[wd]}"
        if watat:
            result += "\n(ဝါထပ်နှစ်)"

        result_label.config(text=result, fg="navy")

    except Exception as e:
        messagebox.showerror("အမှား", f"အမှားဖြစ်နေပါသည်:\n{str(e)}")

# === GUI Setup ===
root = tk.Tk()
root.title("မြန်မာ ပြက္ခဒိန် – Yan9a နှင့် ကိုက်ညီ")
root.geometry("470x470")
root.resizable(False, False)
root.configure(bg="#f8f9fa")

tk.Label(root, text="Gregorian → မြန်မာ ပြက္ခဒိန်", 
         font=("pyidaungsu", 11, "bold"), bg="#f8f9fa", fg="#1e3a8a").pack(pady=15)

frame = tk.Frame(root, bg="#f8f9fa")
frame.pack(pady=10)

tk.Label(frame, text="နှစ် (YYYY):", bg="#f8f9fa").grid(row=0, column=0, padx=5, pady=5, sticky="e")
year_entry = tk.Entry(frame, width=12, font=("pyidaungsu", 11))
year_entry.grid(row=0, column=1)

tk.Label(frame, text="လ (MM):", bg="#f8f9fa").grid(row=1, column=0, padx=5, pady=5, sticky="e")
month_entry = tk.Entry(frame, width=12, font=("pyidaungsu", 11))
month_entry.grid(row=1, column=1)

tk.Label(frame, text="ရက် (DD):", bg="#f8f9fa").grid(row=2, column=0, padx=5, pady=5, sticky="e")
day_entry = tk.Entry(frame, width=12, font=("pyidaungsu", 11))
day_entry.grid(row=2, column=1)

today = datetime.today()
year_entry.insert(0, str(today.year))
month_entry.insert(0, str(today.month))
day_entry.insert(0, str(today.day))

tk.Button(root, text="ပြောင်းပြပါ", command=convert_date,
          font=("pyidaungsu", 11, "bold"), bg="#3b82f6", fg="white", padx=20, pady=6).pack(pady=15)

result_label = tk.Label(root, text="", font=("pyidaungsu", 11), bg="#f8f9fa", justify="left")
result_label.pack(pady=15)

tk.Label(root, text="Yan9a နှင့် ကိုက်ညီ | လပြည့်နေ့အပေါ် မူတည်၍ လဆန်း/လဆုတ် ဖော်ပြ", 
         bg="#f8f9fa", fg="gray", font=("Arial", 9)).pack(side="bottom", pady=10)

root.mainloop()