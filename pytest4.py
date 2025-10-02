import tkinter as tk
from tkinter import ttk, messagebox, font
import datetime
from typing import Dict, List, Tuple
import swisseph as swe
import os

class BirthChartCalculator:
    def __init__(self):
        swe.set_ephe_path(None)

        self.planet_names = {
            swe.SUN: "၁",
            swe.MOON: "၂",
            swe.MERCURY: "၄",
            swe.VENUS: "၆",
            swe.MARS: "၃",
            swe.JUPITER: "၅",
            swe.SATURN: "၀",
            swe.URANUS: "U",
            swe.NEPTUNE: "N",
            swe.PLUTO: "P",
            swe.MEAN_NODE: "၈",
            swe.TRUE_NODE: "ရာဟု (မှန်)",
            swe.CHIRON: "ခိုင်ရွန်"
        }
        
        self.zodiac_signs = [
            "မိဿ", "ပြိဿ","မေထုန်", "ကြရကဋ်",
            "သိဟ်","ကန်", "တူ", "ဗြိစ္ဆာ", 
            "ဓနု", "မကာရ", "ကုမ်", "မိန်"
        ]
        
        self.bhava_names = [
            "တနု ဘာဝ", "ကဋုမ္ပ ဘာဝ", "သဟဇ ဘာဝ", "ဗန္ဓု ဘာဝ",
            "ပုတြရ ဘာဝ", "အာရီ ဘာဝ", "ပထနီ ဘာဝ", "မရဏ ဘာဝ",
            "သုဘ ဘာဝ","ကမ္မ ဘာဝ", "လာဘ ဘာဝ", "ဗျာယ ဘာဝ"
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
        house_system: str = 'P',
        ayanamsa_system: str = 'LAHIRI'
    ) -> Dict:
        # အာယနစနစ်သတ်မှတ်ခြင်း
        ayanamsa_map = {
            'LAHIRI': swe.SIDM_LAHIRI,
            'RAMAN': swe.SIDM_RAMAN,
            'KRISHNAMURTI': swe.SIDM_KRISHNAMURTI,
            'FAGAN_BRADLEY': swe.SIDM_FAGAN_BRADLEY,
            'DELUCE': swe.SIDM_DELUCE
        }
        swe.set_sid_mode(ayanamsa_map[ayanamsa_system])
        
        utc_hour = hour - timezone
        if utc_hour < 0:
            utc_hour += 24
            day -= 1
        elif utc_hour >= 24:
            utc_hour -= 24
            day += 1
        
        decimal_hours = utc_hour + minute / 60.0
        jd = swe.julday(year, month, day, decimal_hours)
        
        # အာယနတွက်ချက်ခြင်း
        ayanamsa = swe.get_ayanamsa(jd)
        
        # ဇာတာအိမ်များ တွက်ချက်ခြင်း
        houses = swe.houses(jd, latitude, longitude, house_system.encode())
        
        # လဂ် (Lagna/Ascendant) တွက်ချက်ခြင်း
        lagna_longitude = houses[1][0]
        lagna_sign = self.get_zodiac_sign(lagna_longitude)
        lagna_degree = lagna_longitude % 30
        
        # ဘာဝများတွက်ချက်ခြင်း
        bhavas = []
        for i in range(12):
            bhava_cusp = houses[0][i]
            bhava_sign = self.get_zodiac_sign(bhava_cusp)
            bhava_degree = bhava_cusp % 30
            bhavas.append({
                "name": self.bhava_names[i],
                "cusp": bhava_cusp,
                "sign": bhava_sign,
                "degree": bhava_degree
            })
        
        # ဂြိုဟ်များ၏ နေရာများ တွက်ချက်ခြင်း
        planets = {}
        for planet_id in self.planet_names.keys():
            try:
                position = swe.calc_ut(jd, planet_id, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0]
                planets[planet_id] = {
                    "longitude": position[0],
                    "latitude": position[1],
                    "distance": position[2],
                    "speed": position[3],
                    "sign": self.get_zodiac_sign(position[0]),
                    "sign_degree": position[0] % 30,
                    "house": self.get_planet_house(position[0], houses[0]),
                    "bhava": self.get_planet_bhava(position[0], houses[0])
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
            "ayanamsa": {
                "system": ayanamsa_system,
                "value": ayanamsa,
                "sign": self.get_zodiac_sign(ayanamsa),
                "degree": ayanamsa % 30
            },
            "lagna": {
                "longitude": lagna_longitude,
                "sign": lagna_sign,
                "degree": lagna_degree
            },
            "bhavas": bhavas,
            "houses": {
                "system": house_system,
                "cusps": list(houses[0]),
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
        return self.zodiac_signs[int(longitude / 30) % 12]
    
    def get_planet_house(self, planet_longitude: float, house_cusps: List[float]) -> int:
        for i in range(12):
            next_house = (i + 1) % 12
            if house_cusps[i] <= planet_longitude < house_cusps[next_house]:
                return i + 1
        return 12
    
    def get_planet_bhava(self, planet_longitude: float, house_cusps: List[float]) -> str:
        for i in range(12):
            next_house = (i + 1) % 12
            if house_cusps[i] <= planet_longitude < house_cusps[next_house]:
                return self.bhava_names[i]
        return self.bhava_names[11]

class BirthChartApp:
    def __init__(self, toplevel):
        width  = toplevel.winfo_screenwidth()
        height = toplevel.winfo_screenheight()
       
        self.toplevel = toplevel
        self.toplevel.title("ဇာတာတွက်ချက်ခြင်း")
        self. toplevel.geometry(f'{width}x{height}')

       # self.toplevel.resizable(true, true)
        
        # မြန်မာစာဖောင့်များ
        self.setup_myanmar_fonts()
        
        # အရောင်များ
        self.bg_color = "#f0f0f0"
        self.frame_color = "#e0e0e0"
        self.button_color = "#4CAF50"
        self.button_hover = "#45a049"
        
        self.toplevel.configure(bg=self.bg_color)
        
        # ဘယ်ဘက်အကွက် (အဝင်အချက်များ) - ပြင်ဆင်ချက်
        self.left_frame = tk.Frame(toplevel, bg=self.frame_color, relief="raised", bd=2)
        self.left_frame.pack(side="left", fill="both", expand=False)
        
        # ညာဘက်အကွက် (ရလဒ်များ)
        self.right_frame = tk.Frame(toplevel, bg="white", relief="sunken", bd=2)
        self.right_frame.pack(side="right", fill="both", expand=True)
        
        # တည်ဆောက်ခြင်း
        self.create_input_widgets()
        self.create_output_widgets()
        
        # Calculator instance
        self.calculator = BirthChartCalculator()
        
        # ဖိုင်မှ ဇာတာများဖတ်ရန်
        self.load_saved_charts()
    
    def setup_myanmar_fonts(self):
        """မြန်မာစာဖောင့်များ စီစဉ်ခြင်း"""
        try:
            available_fonts = font.families()
            self.mm_font = None
            
            preferred_fonts = [
                "Pyidaungsu",
                "Myanmar Text", 
                "Pyidaungsu",
                "Masterpiece Uni Sans",
                "Noto Sans Myanmar"
            ]
            
            for font_name in preferred_fonts:
                if font_name in available_fonts:
                    self.mm_font = font_name
                    break
            
            if self.mm_font is None:
                self.mm_font = "TkDefaultFont"
                
        except Exception as e:
            print(f"Font setup error: {e}")
            self.mm_font = "TkDefaultFont"
    
    def create_input_widgets(self):
        # ဘယ်ဘက် frame အတွက် scrollable canvas ဖန်တီးခြင်း
        self.left_canvas = tk.Canvas(self.left_frame, bg=self.frame_color, highlightthickness=0)
        self.left_scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.left_canvas.yview)
        self.left_scrollable_frame = tk.Frame(self.left_canvas, bg=self.frame_color)
        
        self.left_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))
        )
        
        self.left_canvas.create_window((0, 0), window=self.left_scrollable_frame, anchor="nw")
        self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)
        
        # Canvas နှင့် scrollbar ကို pack လုပ်ခြင်း
        self.left_canvas.pack(side="left", fill="both", expand=True)
        self.left_scrollbar.pack(side="right", fill="y")
        
        # ခေါင်းစဉ်
        header = tk.Label(self.left_scrollable_frame, text="မွေးနေ့ဇာတာအချက်အလက်များ", 
                         font=(self.mm_font, 14, "bold"), bg=self.frame_color, fg="#333")
        header.pack(pady=(15, 10))
        
        # User Name
        tk.Label(self.left_scrollable_frame, text="အမည်:", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=(15, 0), pady=(5, 0))
        self.user_name = tk.Entry(self.left_scrollable_frame, font=(self.mm_font, 10), width=30)
        self.user_name.pack(padx=(15, 15), pady=(0, 8), fill="x")
        
        # Birth Date
        tk.Label(self.left_scrollable_frame, text="မွေးသက္ကရာဇ် (YYYY-MM-DD):", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=(15, 0), pady=(5, 0))
        self.birth_date = tk.Entry(self.left_scrollable_frame, font=(self.mm_font, 10), width=30)
        self.birth_date.pack(padx=(15, 15), pady=(0, 8), fill="x")
        self.birth_date.insert(0, "1990-05-15")
        
        # Birth Time
        tk.Label(self.left_scrollable_frame, text="မွေးချိန် (HH:MM):", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=(15, 0), pady=(5, 0))
        self.birth_time = tk.Entry(self.left_scrollable_frame, font=(self.mm_font, 10), width=30)
        self.birth_time.pack(padx=(15, 15), pady=(0, 8), fill="x")
        self.birth_time.insert(0, "08:30")
        
        # Birth Place
        tk.Label(self.left_scrollable_frame, text="မွေးရာဒေသ:", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=(15, 0), pady=(5, 0))
        self.birth_place = tk.Entry(self.left_scrollable_frame, font=(self.mm_font, 10), width=30)
        self.birth_place.pack(padx=(15, 15), pady=(0, 8), fill="x")
        self.birth_place.insert(0, "ရန်ကုန်မြို့")
        
        # Latitude
        tk.Label(self.left_scrollable_frame, text="လတ္တီကျုဒ် (Latitude):", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=(15, 0), pady=(5, 0))
        self.latitude = tk.Entry(self.left_scrollable_frame, font=(self.mm_font, 10), width=30)
        self.latitude.pack(padx=(15, 15), pady=(0, 8), fill="x")
        self.latitude.insert(0, "16.8661")
        
        # Longitude
        tk.Label(self.left_scrollable_frame, text="လောင်ဂျီကျုဒ် (Longitude):", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=(15, 0), pady=(5, 0))
        self.longitude = tk.Entry(self.left_scrollable_frame, font=(self.mm_font, 10), width=30)
        self.longitude.pack(padx=(15, 15), pady=(0, 8), fill="x")
        self.longitude.insert(0, "96.1951")
        
        # Timezone
        tk.Label(self.left_scrollable_frame, text="အချိန်ဇုန် (Timezone):", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=(15, 0), pady=(5, 0))
        self.timezone = tk.Entry(self.left_scrollable_frame, font=(self.mm_font, 10), width=30)
        self.timezone.pack(padx=(15, 15), pady=(0, 8), fill="x")
        self.timezone.insert(0, "+6.5")
        
        # အာယနစနစ် ရွေးချယ်မှု
        tk.Label(self.left_scrollable_frame, text="အာယနစနစ်:", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=(15, 0), pady=(10, 0))
        self.ayanamsa_var = tk.StringVar(value="LAHIRI")
        ayanamsa_options = [
            ("Lahiri", "LAHIRI"),
            ("Raman", "RAMAN"),
            ("Krishnamurti", "KRISHNAMURTI"),
            ("Fagan-Bradley", "FAGAN_BRADLEY")
        ]
        
        ayanamsa_frame = tk.Frame(self.left_scrollable_frame, bg=self.frame_color)
        ayanamsa_frame.pack(anchor="w", padx=(35, 15))
        
        for text, value in ayanamsa_options:
            tk.Radiobutton(
                ayanamsa_frame,
                text=text,
                variable=self.ayanamsa_var,
                value=value,
                font=(self.mm_font, 9),
                bg=self.frame_color
            ).pack(anchor="w")
        
        # ဇာတာအိမ်စနစ် ရွေးချယ်မှု
        tk.Label(self.left_scrollable_frame, text="ဇာတာအိမ်စနစ်:", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=(15, 0), pady=(10, 0))
        self.house_system_var = tk.StringVar(value="P")
        house_systems = [
            ("Placidus", "P"),
            ("Koch", "K"),
            ("Equal House", "A"),
            ("Sripati", "S")
        ]
        
        house_frame = tk.Frame(self.left_scrollable_frame, bg=self.frame_color)
        house_frame.pack(anchor="w", padx=(35, 15))
        
        for text, value in house_systems:
            tk.Radiobutton(
                house_frame,
                text=text,
                variable=self.house_system_var,
                value=value,
                font=(self.mm_font, 9),
                bg=self.frame_color
            ).pack(anchor="w")
        
        # ခလုတ်များ
        button_frame = tk.Frame(self.left_scrollable_frame, bg=self.frame_color)
        button_frame.pack(pady=(15, 10), padx=(15, 15), fill="x")
        
        self.calculate_btn = tk.Button(
            button_frame, text="တွက်ချက်မည်", 
            font=(self.mm_font, 12, "bold"), 
            bg=self.button_color, 
            fg="white",
            activebackground=self.button_hover,
            activeforeground="white",
            relief="raised",
            bd=3,
            padx=15,
            pady=8,
            command=self.calculate_chart
        )
        self.calculate_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.save_btn = tk.Button(
            button_frame, text="သိမ်းဆည်းမည်", 
            font=(self.mm_font, 12, "bold"), 
            bg="#2196F3", 
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            relief="raised",
            bd=3,
            padx=15,
            pady=8,
            command=self.save_chart
        )
        self.save_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # သိမ်းဆည်းထားသော ဇာတာများ
        tk.Label(self.left_scrollable_frame, text="သိမ်းဆည်းထားသော ဇာတာများ:", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=(15, 0), pady=(15, 5))
        
        self.saved_charts_listbox = tk.Listbox(self.left_scrollable_frame, font=(self.mm_font, 9), height=6)
        self.saved_charts_listbox.pack(padx=(15, 15), pady=(0, 10), fill="x")
        self.saved_charts_listbox.bind('<<ListboxSelect>>', self.load_selected_chart)
        
        # အကူအညွှန်း
        help_text = "အကူအညွှန်း:\n- ရက်စွဲနှင့်အချိန်ကို မှန်ကန်စွာဖြည့်ပါ\n- Latitude/Longitude ကို decimal format ဖြင့်ဖြည့်ပါ\n- Myanmar အတွက် Timezone = +6.5"
        help_label = tk.Label(self.left_scrollable_frame, text=help_text, font=(self.mm_font, 9), 
                             bg=self.frame_color, fg="#666", justify="left")
        help_label.pack(pady=(0, 15), padx=(15, 15), anchor="w")
    
    def create_output_widgets(self):
        # ခေါင်းစဉ်
        header = tk.Label(self.right_frame, text="မွေးနေ့ဇာတာရလဒ်", 
                         font=(self.mm_font, 16, "bold"), bg="white", fg="#333")
        header.pack(pady=(15, 10))
        
        # ရလဒ်ပြရန် Text Widget
        self.output_text = tk.Text(
            self.right_frame, 
            wrap="word", 
            font=(self.mm_font, 11),
            bg="white",
            fg="#333",
            relief="flat",
            padx=15,
            pady=15,
            spacing1=3,
            spacing2=3,
            spacing3=3
        )
        self.output_text.pack(fill="both", expand=True, padx=(15, 15), pady=(0, 15))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.output_text)
        scrollbar.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)
        
        # စာသားညှိနှိုင်းခြင်း
        self.output_text.tag_configure("header", font=(self.mm_font, 12, "bold"), foreground="#2c3e50")
        self.output_text.tag_configure("title", font=(self.mm_font, 14, "bold"), foreground="#e74c3c")
        self.output_text.tag_configure("section", font=(self.mm_font, 11, "bold"), foreground="#3498db")
        self.output_text.tag_configure("planet", font=(self.mm_font, 10))
        self.output_text.tag_configure("info", font=(self.mm_font, 10), foreground="#27ae60")
        self.output_text.tag_configure("highlight", font=(self.mm_font, 11, "bold"), foreground="#e67e22")
    
    def calculate_chart(self):
        try:
            # အချက်အလက်များယူဆောင်ခြင်း
            user_name = self.user_name.get().strip()
            birth_date_str = self.birth_date.get().strip()
            birth_time_str = self.birth_time.get().strip()
            birth_place = self.birth_place.get().strip()
            latitude_str = self.latitude.get().strip()
            longitude_str = self.longitude.get().strip()
            timezone_str = self.timezone.get().strip()
            
            # အချက်အလက်များစစ်ဆေးခြင်း
            if not all([user_name, birth_date_str, birth_time_str, birth_place, latitude_str, longitude_str, timezone_str]):
                messagebox.showerror("အမှား", "အချက်အလက်အားလုံးဖြည့်စွက်ပါ")
                return
            
            # ရက်စွဲနှင့်အချိန်ပြောင်းခြင်း
            birth_date = datetime.datetime.strptime(birth_date_str, "%Y-%m-%d")
            birth_time = datetime.datetime.strptime(birth_time_str, "%H:%M")
            
            latitude = float(latitude_str)
            longitude = float(longitude_str)
            timezone = float(timezone_str.replace('+', ''))
            
            # ဇာတာတွက်ချက်ခြင်း
            chart_data = self.calculator.calculate_birth_chart(
                year=birth_date.year,
                month=birth_date.month,
                day=birth_date.day,
                hour=birth_time.hour,
                minute=birth_time.minute,
                latitude=latitude,
                longitude=longitude,
                timezone=timezone,
                house_system=self.house_system_var.get(),
                ayanamsa_system=self.ayanamsa_var.get()
            )
            
            # လက်ရှိဇာတာကို မှတ်ထားခြင်း
            self.current_chart_data = {
                "name": user_name,
                "data": chart_data
            }
            
            # ရလဒ်ပြသခြင်း
            self.display_results(user_name, birth_place, chart_data)
            
        except ValueError as e:
            messagebox.showerror("အမှား", f"အချက်အလက်ပုံစံမှားယွင်းနေသည်: {str(e)}")
        except Exception as e:
            messagebox.showerror("အမှား", f"တွက်ချက်ခြင်းမအောင်မြင်: {str(e)}")
    
    def save_chart(self):
        try:
            if not hasattr(self, 'current_chart_data'):
                messagebox.showwarning("သတိပေးချက်", "ဇာတာတစ်ခုကို ဦးစွာတွက်ချက်ပါ")
                return
            
            # ဖိုင်ထဲမှာ သိမ်းဆည်းခြင်း
            with open("paymu.txt", "a", encoding="utf-8") as f:
                f.write(f"Name: {self.current_chart_data['name']}\n")
                f.write(f"Date: {self.current_chart_data['data']['birth_info']['date']}\n")
                f.write(f"Time: {self.current_chart_data['data']['birth_info']['time']}\n")
                f.write(f"Place: {self.current_chart_data['data']['birth_info']['location']}\n")
                f.write(f"Ayanamsa: {self.current_chart_data['data']['ayanamsa']['system']}\n")
                f.write(f"House System: {self.current_chart_data['data']['houses']['system']}\n")
                f.write("---\n")
            
            # Listbox ကို ပြန်ဖြည့်ခြင်း
            self.load_saved_charts()
            
            messagebox.showinfo("အောင်မြင်", "ဇာတာကို paymu.txt ဖိုင်ထဲသိမ်းဆည်းပြီးပါပြီ")
            
        except Exception as e:
            messagebox.showerror("အမှား", f"သိမ်းဆည်းခြင်းမအောင်မြင်: {str(e)}")
    
    def load_saved_charts(self):
        try:
            self.saved_charts_listbox.delete(0, tk.END)
            
            if os.path.exists("paymu.txt"):
                with open("paymu.txt", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                charts = []
                current_chart = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("Name:"):
                        if current_chart:
                            charts.append(current_chart)
                        current_chart = {"name": line.split(": ")[1]}
                    elif line.startswith("Date:"):
                        current_chart["date"] = line.split(": ")[1]
                    elif line.startswith("Time:"):
                        current_chart["time"] = line.split(": ")[1]
                    elif line == "---":
                        charts.append(current_chart)
                        current_chart = {}
                
                if current_chart:
                    charts.append(current_chart)
                
                for chart in charts:
                    display_text = f"{chart['name']} ({chart['date']} {chart['time']})"
                    self.saved_charts_listbox.insert(tk.END, display_text)
            
        except Exception as e:
            print(f"Error loading saved charts: {e}")
    
    def load_selected_chart(self, event):
        try:
            selection = self.saved_charts_listbox.curselection()
            if selection:
                index = selection[0]
                
                if os.path.exists("paymu.txt"):
                    with open("paymu.txt", "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    
                    # ရွေးချယ်ထားတဲ့ ဇာတာကို ရှာဖွေခြင်း
                    chart_count = 0
                    current_chart_lines = []
                    
                    for line in lines:
                        if line.strip() == "---":
                            if chart_count == index:
                                break
                            chart_count += 1
                            current_chart_lines = []
                        elif chart_count == index:
                            current_chart_lines.append(line.strip())
                    
                    # ဇာတာအချက်အလက်များကို Entry များထဲ ထည့်သွင်းခြင်း
                    for line in current_chart_lines:
                        if line.startswith("Name:"):
                            self.user_name.delete(0, tk.END)
                            self.user_name.insert(0, line.split(": ")[1])
                        elif line.startswith("Date:"):
                            self.birth_date.delete(0, tk.END)
                            self.birth_date.insert(0, line.split(": ")[1])
                        elif line.startswith("Time:"):
                            self.birth_time.delete(0, tk.END)
                            self.birth_time.insert(0, line.split(": ")[1])
                        elif line.startswith("Place:"):
                            place_data = line.split(": ")[1]
                            # ဒေသနှင့် ကိုဩဒိနိတ်များကို ခွဲခြားခြင်း
                            if "," in place_data:
                                place, coords = place_data.split(", ")
                                self.birth_place.delete(0, tk.END)
                                self.birth_place.insert(0, place)
                                if "," in coords:
                                    lat, lon = coords.split(",")
                                    self.latitude.delete(0, tk.END)
                                    self.latitude.insert(0, lat.strip())
                                    self.longitude.delete(0, tk.END)
                                    self.longitude.insert(0, lon.strip())
                        elif line.startswith("Ayanamsa:"):
                            ayanamsa = line.split(": ")[1]
                            self.ayanamsa_var.set(ayanamsa)
                        elif line.startswith("House System:"):
                            house_system = line.split(": ")[1]
                            self.house_system_var.set(house_system)
        
        except Exception as e:
            print(f"Error loading selected chart: {e}")
    
    def display_results(self, user_name, birth_place, chart_data):
        self.output_text.delete(1.0, tk.END)
        
        # ခေါင်းစဉ်
        self.output_text.insert(tk.END, f"{'='*60}\n", "title")
        self.output_text.insert(tk.END, f"🌟 {user_name} ၏ မွေးနေ့ဇာတာ 🌟\n", "title")
        self.output_text.insert(tk.END, f"{'='*60}\n\n", "title")
        
        # မွေးချိန်နှင့်နေရာ
        birth_info = chart_data["birth_info"]
        self.output_text.insert(tk.END, "📅 မွေးချိန်နှင့်နေရာ\n", "section")
        self.output_text.insert(tk.END, f"  မွေးသက္ကရာဇ်: {birth_info['date']}\n", "info")
        self.output_text.insert(tk.END, f"  မွေးချိန်: {birth_info['time']}\n", "info")
        self.output_text.insert(tk.END, f"  မွေးရာဒေသ: {birth_place}\n", "info")
        self.output_text.insert(tk.END, f"  တည်နေရာ: {birth_info['location']}\n", "info")
        self.output_text.insert(tk.END, f"  အချိန်ဇုန်: UTC{birth_info['timezone']:+.1f}\n\n", "info")
        
        # အာယန
        ayanamsa = chart_data["ayanamsa"]
        self.output_text.insert(tk.END, "🔭 အာယန (Ayanamsa)\n", "section")
        self.output_text.insert(tk.END, f"  စနစ်: {ayanamsa['system']}\n", "info")
        self.output_text.insert(tk.END, f"  အာယနတန်ဖိုး: {ayanamsa['value']:.4f}°\n", "highlight")
        self.output_text.insert(tk.END, f"  ရာသီခွင်: {ayanamsa['sign']} {ayanamsa['degree']:.2f}°\n\n", "info")
        
        # လဂ် (Lagna)
        lagna = chart_data["lagna"]
        self.output_text.insert(tk.END, "⭐ လဂ် (Lagna/Ascendant)\n", "section")
        self.output_text.insert(tk.END, f"  လဂ်ရာသီ: {lagna['sign']}\n", "highlight")
        self.output_text.insert(tk.END, f"  လဂ်ဒီဂရီ: {lagna['degree']:.2f}°\n", "info")
        self.output_text.insert(tk.END, f"  လဂ်လောင်ဂျီကျုဒ်: {lagna['longitude']:.4f}°\n\n", "info")
        
        # ဘာဝများ
        self.output_text.insert(tk.END, "🏠 ဘာဝများ (Bhavas)\n", "section")
        for bhava in chart_data["bhavas"]:
            self.output_text.insert(tk.END, f"  {bhava['name']}: {bhava['sign']} {bhava['degree']:.2f}°\n", "info")
        self.output_text.insert(tk.END, "\n")
        
        # ဇာတာအိမ်များ
        self.output_text.insert(tk.END, "🏛️ ဇာတာအိမ်ခွက်များ\n", "section")
        self.output_text.insert(tk.END, f"  စနစ်: {chart_data['houses']['system']}\n", "info")
        houses = chart_data["houses"]
        for i, cusp in enumerate(houses["cusps"]):
            sign = self.calculator.get_zodiac_sign(cusp)
            degree = cusp % 30
            self.output_text.insert(tk.END, f"  အိမ် {i+1:2d}: {sign} {degree:5.2f}°\n", "info")
        self.output_text.insert(tk.END, "\n")
        
        # အဓိကထောင့်များ
        self.output_text.insert(tk.END, "📐 အဓိကထောင့်များ\n", "section")
        angles = chart_data["angles"]
        ascendant = angles["ascendant"]
        mc = angles["mc"]
        self.output_text.insert(tk.END, f"  အရှေ့ကောင်းကင်: {ascendant['sign']} {ascendant['sign_degree']:5.2f}°\n", "info")
        self.output_text.insert(tk.END, f"  ကောင်းကင်အလယ်: {mc['sign']} {mc['sign_degree']:5.2f}°\n\n", "info")
        
        # ဂြိုဟ်များ
        self.output_text.insert(tk.END, "🪐 ဂြိုဟ်များ၏နေရာ\n", "section")
        planets = chart_data["planets"]
        for planet_id, planet_data in planets.items():
            if planet_data:
                name = self.calculator.planet_names[planet_id]
                sign = planet_data["sign"]
                degree = planet_data["sign_degree"]
                house = planet_data["house"]
                bhava = planet_data["bhava"]
                retrograde = "R" if planet_data["speed"] < 0 else ""
                self.output_text.insert(tk.END, f"  {name:12s}: {sign:10s} {degree:5.2f}° (အိမ် {house}, {bhava}) {retrograde}\n", "planet")
        
        self.output_text.insert(tk.END, f"\n{'='*60}\n", "title")

if __name__ == "__main__":
    toplevel = tk.Tk()
    app = BirthChartApp(toplevel)
    toplevel.mainloop()