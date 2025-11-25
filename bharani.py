import tkinter as tk
from tkinter import font as tkfont, messagebox
import pyswisseph as swe  # <-- YOUR CORRECT IMPORT LINE
import datetime
import os

# --- အချက်အလက်များ စိစစ်ခြင်း ---

# ဂြိုဟ်များ၏ သင်္ကေတများ (Unicode Symbols)
PLANETS = {
    swe.SE_SUN: 'sun', # ☉',     # နေ
    swe.SE_MOON: 'moon', # ☽',    # လ
    swe.SE_MARS: 'mars', #  ♂',    # အင်္ဂါ
    swe.SE_MERCURY: 'mercury',  # ☿', # ဗုဒ္ဓဟူး
    swe.SE_JUPITER: 'jupiter', #♃', # ဂျူပီတာ (သိုး)
    swe.SE_VENUS: 'venus', #♀',   # ကြာ
    swe.SE_SATURN: 'saturn',  # ♄',  # စနေ
    swe.SE_TRUE_NODE: 'north_node', # ☋', # ကိတ် (South Node)
    swe.SE_MEAN_NODE: 'south_node' #☊', # ရာဟု (North Node)
}

# ရာသီ (၁၂) မျိုး
RASI_NAMES_MY = [
    "မိဿ", "ဖာတိုး", "မေထုန်", "ကရကဋ်",
    "စိန်", "ကန်", "သို့", "ကန်ညီ",
    "တူ", "မြောက်", "ဓနု", "ငါး"
]

# ဝိလိတ္တာ (ဆုတ်နစ်/ရှေ့သွား)
RETROGRADE_TEXT = {
    True: "R",
    False: "ရှေ့သွား"
}

# --- ဂြိုဟ်တွေရဲ့ တည်နေရာ တွက်ချက်တဲ့ အပိုင်း ---
def calculate_planetary_positions(date_time=None):
    try:
        if date_time is None:
            now = datetime.datetime.now()
        else:
            now = date_time
            
        jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)
        results = []
        rahu_data = {}
        
        for p_id, p_symbol in PLANETS.items():
            if p_id == swe.SE_MEAN_NODE:
                ret, flags = swe.calc_ut(jd, p_id)
                rahu_data = {
                    "symbol": p_symbol,
                    "longitude": ret[0],
                    "speed": ret[3],
                    "is_retrograde": bool(flags & swe.RETROGRADE)
                }
                continue

            ret, flags = swe.calc_ut(jd, p_id)
            longitude = ret[0]
            speed = ret[3]
            is_retrograde = bool(flags & swe.RETROGRADE)

            rasi_index = int(longitude / 30)
            rasi_name = RASI_NAMES_MY[rasi_index]

            amsa_deg = longitude % 30
            deg = int(amsa_deg)
            mins = int((amsa_deg - deg) * 60)
            secs = round(((amsa_deg - deg) * 60 - mins) * 60)
            amsa_str = f"{deg}° {mins}' {secs}\""

            speed_str = f"{speed:.4f}"
            vilitta_str = RETROGRADE_TEXT[is_retrograde]

            results.append({
                "symbol": p_symbol,
                "rasi": rasi_name,
                "amsa": amsa_str,
                "speed": speed_str,
                "vilitta": vilitta_str
            })

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

            ketu_longitude = (longitude + 180) % 360
            ketu_rasi_index = int(ketu_longitude / 30)
            ketu_rasi_name = RASI_NAMES_MY[ketu_rasi_index]
            ketu_amsa_deg = ketu_longitude % 30
            ketu_deg = int(ketu_amsa_deg)
            ketu_mins = int((ketu_amsa_deg - ketu_deg) * 60)
            ketu_secs = round(((ketu_amsa_deg - ketu_deg) * 60 - ketu_mins) * 60)
            ketu_amsa_str = f"{ketu_deg}° {ketu_mins}' {ketu_secs}\""
            ketu_speed_str = f"{-rahu_data['speed']:.4f}"
            ketu_vilitta_str = RETROGRADE_TEXT[not rahu_data['is_retrograde']]

            results.append({
                "symbol": '☋', # ကိတ်သင်္ကေတ
                "rasi": ketu_rasi_name,
                "amsa": ketu_amsa_str,
                "speed": ketu_speed_str,
                "vilitta": ketu_vilitta_str
            })

        return results
    except Exception as e:
        messagebox.showerror("Error", f"Error calculating planetary positions: {str(e)}")
        return []

# --- Tkinter GUI အပိုင်း ---
class PlanetaryPositionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ယနေ့ ဂြိုဟ်စင် (Today's Planetary Positions)")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')

        if not os.path.exists('./ephe'):
            messagebox.showwarning("Warning", "Ephemeris files not found in './ephe' directory. Please download and place them there.")
        
        swe.set_ephe_path('./ephe')

        try:
            self.display_font = tkfont.Font(family="Pyidaungsu", size=12)
            self.header_font = tkfont.Font(family="Pyidaungsu", size=12, weight="bold")
        except:
            self.display_font = tkfont.Font(family="Courier New", size=12)
            self.header_font = tkfont.Font(family="Courier New", size=12, weight="bold")

        main_frame = tk.Frame(root, bg='#f0f0f0', padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        date_frame = tk.Frame(main_frame, bg='#f0f0f0')
        date_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(date_frame, text="ရက်စွဲ:", bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        
        self.date_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = tk.Entry(date_frame, textvariable=self.date_var, width=12)
        self.date_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(date_frame, text="အချိန်:", bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        
        self.time_var = tk.StringVar(value=datetime.datetime.now().strftime("%H:%M"))
        self.time_entry = tk.Entry(date_frame, textvariable=self.time_var, width=8)
        self.time_entry.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(date_frame, text="ပြန်လည်တွက်ချက်", command=self.update_display)
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        today_btn = tk.Button(date_frame, text="ယနေ့", command=self.set_today)
        today_btn.pack(side=tk.LEFT)

        self.text_widget = tk.Text(main_frame, font=self.display_font, wrap="none", bg="white", relief=tk.SUNKEN, bd=2)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(main_frame, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=scrollbar.set)

        self.update_display()
    
    def set_today(self):
        now = datetime.datetime.now()
        self.date_var.set(now.strftime("%Y-%m-%d"))
        self.time_var.set(now.strftime("%H:%M"))
        self.update_display()

    def update_display(self):
        try:
            date_str = self.date_var.get()
            time_str = self.time_var.get()
            
            date_parts = date_str.split('-')
            year = int(date_parts[0])
            month = int(date_parts[1])
            day = int(date_parts[2])
            
            time_parts = time_str.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            
            selected_datetime = datetime.datetime(year, month, day, hour, minute)
            
            self.text_widget.config(state="normal")
            self.text_widget.delete("1.0", tk.END)

            date_header = f"ရက်စွဲ: {selected_datetime.strftime('%Y-%m-%d %H:%M')}\n"
            self.text_widget.insert(tk.END, date_header, "date_header")
            
            header = f"{'ဂြိုဟ်':<6} {'ရာသီ':<10} {'အံသာ':<15} {'လိတ္တာ':<12} {'ဝိလိတ္တာ':<10}\n"
            self.text_widget.insert(tk.END, header, "header")
            self.text_widget.insert(tk.END, "-" * 65 + "\n")

            planetary_data = calculate_planetary_positions(selected_datetime)

            for data in planetary_data:
                line = f"{data['symbol']:<6} {data['rasi']:<10} {data['amsa']:<15} {data['speed']:<12} {data['vilitta']:<10}\n"
                self.text_widget.insert(tk.END, line)
            
            self.text_widget.config(state="disabled")
            
            self.text_widget.tag_config("header", font=self.header_font, foreground="#005a9c")
            self.text_widget.tag_config("date_header", font=self.header_font, foreground="#d9534f")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating display: {str(e)}")


# --- Program ကို Run ခြင်း ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PlanetaryPositionApp(root)
    root.mainloop()