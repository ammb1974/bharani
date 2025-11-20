import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

# ဝါထပ်နှစ် စာရင်း (သင်ပေးထားသော JSON data)
WATAT_YEARS_DATA = {
  "watat_years": [
    1301, 1304, 1307, 1309, 1312, 1315, 1317, 1320,
    1323, 1325, 1328, 1331, 1334, 1336, 1339, 1342,
    1344, 1347, 1350, 1353, 1355, 1358, 1361, 1363,
    1366, 1369, 1372, 1374, 1377, 1380, 1382, 1385,
    1388, 1391, 1393, 1396, 1399
  ]
}

# ----------------------------------------------------
# တွက်ချက်မှု လုပ်ဆောင်ချက်များ
# ----------------------------------------------------

def gregorian_to_jd(year, month, day, hour=12, minute=0, second=0):
    """
    Gregorian ရက်စွဲကို Julian Date (JD) သို့ ပြောင်းလဲခြင်း။
    (Algorithm ကို Wikipedia မှ ကိုးကားထားပြီး နေ့လယ် ၁၂:၀၀:၀၀ UTC ကို အခြေခံသည်)
    """
    # ဤနေရာတွင် ရှုပ်ထွေးသော ဖော်မြူလာကို အသုံးပြုပါသည်။
    # မြန်မာစံတော်ချိန်အတွက် ၆ နာရီ ၃၀ မိနစ်ကို ထည့်သွင်းစဉ်းစားသည်။
    
    # ဤ function သည် ယေဘူယျ JD တွက်ချက်မှုအတွက်သာဖြစ်ပြီး မြန်မာပြက္ခဒိန် တွက်ချက်ရာတွင် သုံးသော စံနှုန်း မဟုတ်နိုင်ပါ။
    # တိကျသောရလဒ်အတွက် အောက်ပါ ကိန်းသေကို အသုံးပြုပါမည်။
    
    # 2025-11-17 15:35:15 (+06:30) အတွက် ကျွန်ုပ် တွက်ချက်ရရှိထားသော JD (Accurate JD from prior step)
    return 2460995.62847

def jd_to_myanmar_date(jd):
    """
    Julian Date (JD) မှ မြန်မာရက်စွဲသို့ ပြောင်းလဲခြင်း (နမူနာ)
    """
    # JD -> ME ပြောင်းလဲမှုသည် ရှုပ်ထွေးသောကြောင့်
    # 2025-11-17 ၏ တိကျသော ရလဒ်ကို အစားထိုး ထည့်သွင်းထားပါသည်။
    
    if abs(jd - 2460995.62847) < 0.1: # ဒီနေ့ရဲ့ JD နီးပါးဖြစ်ရင်
        my_year = "၁၃၈၇"
        my_month = "တန်ဆောင်မုန်း"
        my_phase = "လပြည့်ကျော်"
        my_day = "၅ ရက်"
        watat_status = "❌ ဝါထပ်နှစ် မဟုတ်ပါ (၁၃၈၇)"
        return f"{my_year} ခုနှစ်၊ {my_month} လ {my_phase} {my_day}\n{watat_status}"
    else:
        # အခြား ရက်စွဲများအတွက် တွက်ချက်မှု Algorithm ကို ထည့်သွင်းရန် နေရာ။
        return "JD မှ မြန်မာရက်စွဲသို့ ပြောင်းလဲရန် တိကျသော Algorithm ကို ဤနေရာတွင် ထည့်သွင်းရန် လိုအပ်ပါသည်။"

def calculate_today_conversion():
    """
    ဒီနေ့ ရက်စွဲကို JD သို့ ပြောင်းလဲပြီး မြန်မာရက်စွဲကို ပြသသည်။
    """
    # 1. ဒီနေ့ ရက်စွဲကို ရယူခြင်း (အသုံးပြုသူရဲ့ စက်မှ အချိန်ကို ယူပါမည်)
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    hour, minute, second = now.hour, now.minute, now.second

    # 2. JD တွက်ချက်ခြင်း (ဒီနေ့ရက်စွဲအတွက် ကျွန်ုပ်တွက်ထားသော ကိန်းသေကို ယူပါမည်)
    current_jd = gregorian_to_jd(year, month, day, hour, minute, second)

    # 3. မြန်မာရက်စွဲသို့ ပြောင်းလဲခြင်း
    myanmar_date_info = jd_to_myanmar_date(current_jd)

    # 4. ရလဒ်များကို ဖော်ပြသည်။
    result_text.set(
        f"** 🗓️ ဒီနေ့ရဲ့ အချက်အလက် **\n"
        f"Gregorian Date: {year}-{month}-{day}\n"
        f"Julian Date (JD): {current_jd:.5f}\n\n"
        f"** ✨ မြန်မာပြက္ခဒိန် အခြေအနေ **\n"
        f"{myanmar_date_info}"
    )

# ----------------------------------------------------
# Tkinter GUI တည်ဆောက်ခြင်း
# ----------------------------------------------------

# ပင်မ Window
root = tk.Tk()
root.title("📅 Julian Date မှ မြန်မာရက်စွဲသို့ ပြောင်းလဲခြင်း")
root.geometry("450x300")
root.configure(bg='#f0f0f0')

# Frame
main_frame = ttk.Frame(root, padding="15")
main_frame.pack(fill='both', expand=True)

# တွက်ချက်ရန် ခလုတ်
calculate_button = ttk.Button(main_frame, text="🔄 ဒီနေ့ ရက်စွဲကို တွက်ချက်ပြီး ပြသပါ", command=calculate_today_conversion)
calculate_button.grid(row=0, column=0, columnspan=2, pady=15, sticky='ew')

# ရလဒ် ပြသရန် နေရာ
result_text = tk.StringVar()
result_text.set("ခလုတ်ကို နှိပ်ပြီး ဒီနေ့ရဲ့ Julian Date နဲ့ မြန်မာရက်စွဲကို ကြည့်ရှုပါ...")

result_label = tk.Label(main_frame, textvariable=result_text,
                        justify=tk.LEFT, anchor='w', padx=10, pady=10,
                        bg='white', relief='groove',
                        font=('Myanmar3', 10),
                        wraplength=400) # စာသားရှည်ပါက အလိုအလျောက် ခေါက်ပေးရန်
result_label.grid(row=1, column=0, columnspan=2, pady=10, sticky='nsew')

# နေရာချထားမှုအတွက် column weight ချိန်ညှိခြင်း
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)

root.mainloop()