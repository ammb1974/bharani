import tkinter as tk
from tkinter import font as tkfont
import pyswisseph as swe
import datetime

# --- အချက်အလက်များ စိစစ်ခြင်း ---

# ဂြိုဟ်များ၏ သင်္ကေတများ (Unicode Symbols)
# SE_SUN, SE_MOON စသည်တို့ကို pysweph မှ ပေးထားတဲ့ ID များဖြစ်သည်။
PLANETS = {
    swe.SE_SUN: '☉',     # နေ
    swe.SE_MOON: '☽',    # လ
    swe.SE_MARS: '♂',    # အင်္ဂါ
    swe.SE_MERCURY: '☿', # ဗုဒ္ဓဟူး
    swe.SE_JUPITER: '♃', # ဂျူပီတာ (သိုး)
    swe.SE_VENUS: '♀',   # ကြာ
    swe.SE_SATURN: '♄',  # စနေ
    swe.SE_MEAN_NODE: '☊', # ရာဟု (North Node)
    # Ketu ကို Rahu နဲ့ ဆန့်ကျင်ဘက်မှာ ရှိတယ်ဆိုတာသိပြီး တွက်ချက်မယ်။
}

# ရာသီ (၁၂) မျိုး
RASI_NAMES_MY = [
    "မိဿ", "ဖာတိုး", "မေထုန်", "ကရကဋ်",
    "စိန်", "ကန်", "သို့", "ကန်ညီ",
    "တူ", "မြောက်", "ဓနု", "ငါး"
]

# ဝိလိတ္တာ (ဆုတ်နစ်/ရှေ့သွား)
RETROGRADE_TEXT = {
    True: "ဆုတ်နစ်",
    False: "ရှေ့သွား"
}

# --- ဂြိုဟ်တွေရဲ့ တည်နေရာ တွက်ချက်တဲ့ အပိုင်း ---
def calculate_planetary_positions():
    """
    �နေ့ရက်စွဲအတွက် ဂြိုဟ်တွေရဲ့ တည်နေရာကို တွက်ချက်ပြီး
    လိုအပ်တဲ့ အချက်အလက်တွေကို ပြန်ပေးမယ်။
    """
    # ယနေ့ရက်စွဲနဲ့ အချိန်ကို ရယူခြင်း
    now = datetime.datetime.now()
    # pysweph ကို သုံးဖို့ Julian Day အချိန်ကို ပြောင်းခြင်း
    jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)

    results = []
    # ရာဟုကို သီးသန့်တွက်ချက်မယ်။ Ketu ကိုတော့ နောက်မှာ ထည့်မယ်။
    rahu_data = {}
    
    # စဉ်ဆက်မပြတ် ဂြိုဟ်တွေကို တွက်ချက်ခြင်း
    for p_id, p_symbol in PLANETS.items():
        if p_id == swe.SE_MEAN_NODE:
            # ရာဟုကို ခဏထားပြီး နောက်ဆုံးမှာ ထည့်မယ်
            ret, flags = swe.calc_ut(jd, p_id)
            rahu_data = {
                "symbol": p_symbol,
                "longitude": ret[0],
                "speed": ret[3],
                "is_retrograde": bool(flags & swe.RETROGRADE)
            }
            continue

        # ဂြိုဟ်တစ်ခုချင်းစီရဲ့ တည်နေရာကို တွက်ချက်ခြင်း
        # swe.calc_ut က longitude (ဒီဂရီ), speed (အရှိန်နှုန်း), နဲ့ retrograde flag တွေပေးမယ်
        ret, flags = swe.calc_ut(jd, p_id)
        longitude = ret[0]
        speed = ret[3]
        is_retrograde = bool(flags & swe.RETROGRADE)

        # ရာသီကို ရှာခြင်း (ဥပမာ - 30.5 ဒီဂရီဆိုရင် ဖာတိုးရာသီ)
        rasi_index = int(longitude / 30)
        rasi_name = RASI_NAMES_MY[rasi_index]

        # အံသာ (ဒီဂရီ, မိနစ်, စက္ကန့်) ကို ရှာခြင်း
        amsa_deg = longitude % 30
        deg = int(amsa_deg)
        mins = int((amsa_deg - deg) * 60)
        secs = round(((amsa_deg - deg) * 60 - mins) * 60)
        amsa_str = f"{deg}° {mins}' {secs}\""

        # လိတ္တာ (အရှိန်နှုန်း) ကို ပုံစံပြောင်းခြင်း
        speed_str = f"{speed:.4f}"

        # ဝိလိတ္တာ (ဆုတ်နစ်/ရှေ့သွား)
        vilitta_str = RETROGRADE_TEXT[is_retrograde]

        results.append({
            "symbol": p_symbol,
            "rasi": rasi_name,
            "amsa": amsa_str,
            "speed": speed_str,
            "vilitta": vilitta_str
        })

    # ရာဟုကို နောက်ဆုံးမှာ ထည့်ခြင်း
    if rahu_data:
        longitude = rahu_data['longitude']
        rasi_index = int(longitude / 30)
        rasi_name = RASI_NAMES_MY[rasi_index]
        amsa_deg = longitude % 30
        deg = int(amsa_deg)
        mins = int((amsa_deg - deg) * 60)
        secs = round(((amsa_deg - deg) * 60 - mins) * 60)
        amsa_str = f"{deg}° {mins}' {secs}\""
        speed_str = f"{rahu_data['speed']:.4f}"
        vilitta_str = RETROGRADE_TEXT[rahu_data['is_retrograde']]
        
        results.append({
            "symbol": rahu_data['symbol'],
            "rasi": rasi_name,
            "amsa": amsa_str,
            "speed": speed_str,
            "vilitta": vilitta_str
        })

        # ကိတ်ကို ထည့်ခြင်း (ရာဟုနဲ့ ၁၈၀ ကွာပြီး ဆန့်ကျင်ဘက်မှာ ရှိတယ်)
        ketu_longitude = (longitude + 180) % 360
        ketu_rasi_index = int(ketu_longitude / 30)
        ketu_rasi_name = RASI_NAMES_MY[ketu_rasi_index]
        ketu_amsa_deg = ketu_longitude % 30
        ketu_deg = int(ketu_amsa_deg)
        ketu_mins = int((ketu_amsa_deg - ketu_deg) * 60)
        ketu_secs = round(((ketu_amsa_deg - ketu_deg) * 60 - ketu_mins) * 60)
        ketu_amsa_str = f"{ketu_deg}° {ketu_mins}' {ketu_secs}\""
        # ကိတ်ရဲ့ အရှိန်နှုန်းက ရာဟုနဲ့ ဆန့်ကျင်ဘက်
        ketu_speed_str = f"{-rahu_data['speed']:.4f}"
        # ကိတ်ရဲ့ ဝိလိတ္တာလဲ ရာဟုနဲ့ ဆန့်ကျင်ဘက်
        ketu_vilitta_str = RETROGRADE_TEXT[not rahu_data['is_retrograde']]

        results.append({
            "symbol": '☋', # ကိတ်သင်္ကေတ
            "rasi": ketu_rasi_name,
            "amsa": ketu_amsa_str,
            "speed": ketu_speed_str,
            "vilitta": ketu_vilitta_str
        })

    return results

# --- Tkinter GUI အပိုင်း ---
class PlanetaryPositionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ယနေ့ ဂြိုဟ်စင် (Today's Planetary Positions)")
        self.root.geometry("500x450")
        self.root.configure(bg='#f0f0f0')

        # Swiss Ephemeris ဖိုင်တွေရှိတဲ့ path ကို ညွှန်ကြားခြင်း
        # 'ephe' folder ကို script နဲ့အတူ ထားရမယ်
        swe.set_ephe_path('./ephe')

        # Font ကို စိစစ်ခြင်း (စာလုံးတွေ အလှည့်ကျနေအောင် Monospace Font သုံးမယ်)
        self.display_font = tkfont.Font(family="Pyidaungsu", size=12)
        self.header_font = tkfont.Font(family="Pyidaungsu", size=12, weight="bold")

        # အဓိက Frame
        main_frame = tk.Frame(root, bg='#f0f0f0', padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ရလဒ်ကို ပြသမယ့် Text Widget
        self.text_widget = tk.Text(main_frame, font=self.display_font, wrap="none", bg="white", relief=tk.SUNKEN, bd=2)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(main_frame, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=scrollbar.set)

        # ရလဒ်တွေကို ဖော်ပြခြင်း
        self.update_display()

    def update_display(self):
        """Text Widget ထဲမှာ ဂြိုဟ်စင်ရလဒ်တွေကို အပ်ဒိတ်လုပ်ခြင်း"""
        # အဟောင်းကို ရှင်းလင်းခြင်း
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", tk.END)

        # ခေါင်းစဉ်ထည့်ခြင်း
        header = f"{'ဂြိုဟ်':<6} {'ရာသီ':<10} {'အံသာ':<15} {'လိတ္တာ':<12} {'ဝိလိတ္တာ':<10}\n"
        self.text_widget.insert(tk.END, header, "header")
        self.text_widget.insert(tk.END, "-" * 65 + "\n")

        # ဂြိုဟ်စင်ရလဒ်တွေကို ရယူခြင်း
        planetary_data = calculate_planetary_positions()

        # ရလဒ်တွေကို စာကြောင်းလိုက် ထည့်ခြင်း
        for data in planetary_data:
            line = f"{data['symbol']:<6} {data['rasi']:<10} {data['amsa']:<15} {data['speed']:<12} {data['vilitta']:<10}\n"
            self.text_widget.insert(tk.END, line)
        
        # Text Widget ကို ဖတ်ရေးပိတ်ခြင်း
        self.text_widget.config(state="disabled")
        
        # Header ကို အစိမ်းရောင်ပေးခြင်း
        self.text_widget.tag_config("header", font=self.header_font, foreground="#005a9c")


# --- Program ကို Run ခြင်း ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PlanetaryPositionApp(root)
    root.mainloop()
