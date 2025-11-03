import tkinter as tk
from tkinter import ttk, messagebox, font
import datetime
from typing import Dict, List, Tuple
import swisseph as swe

class BirthChartCalculator:
    def create_context_menu(self):
        self.context_menu = tk.Menu(self.toplevel, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_to_clipboard)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.context_menu.grab_release()

    
    def copy_to_clipboard(self):
        text = self.output_text.get("1.0", "end-1c")  # Text widget မှ စာသားတိုက်ခတ် grab
        self.toplevel.clipboard_clear()
        self.toplevel.clipboard_append(text)
        messagebox.showinfo("Copy", "ဇာတာရလဒ်များ Clipboard သို့ ကူးယူပြီးပါပြီ။")
    def __init__(self):
        swe.set_ephe_path(None)
        
        # အာယန စနစ်သတ်မှတ်ခြင်း (Lahiri အာယန)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        self.planet_names = {
            swe.SUN: "၁-နွေ",
            swe.MOON: "၁-လာ",
            swe.MERCURY: "၄-ဟူး",
            swe.VENUS: "၆-ကြာ",
            swe.MARS: "၃-ဂါ",
            swe.JUPITER: "၅-တေး",
            swe.SATURN: "၀-နေ",
            swe.URANUS: "U",
            swe.NEPTUNE: "N",
            swe.PLUTO: "P",
            swe.MEAN_NODE: "၈-ရာ",
            swe.TRUE_NODE: "ရာဟု (မှန်)",
            swe.CHIRON: "ခိုင်ရွန်"
        }
        
        self.zodiac_signs = [
            "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်",
            "သိဟ်",  "ကန်", "တူ","ဗြိစ္ဆာ",
            "ဓနု", "မကာရ", "ကုမ်", "မိန်"
        ]
        
        self.bhava_names = [
            "ပဌမဘာဝ", "ဒုတိယဘာဝ", "တတိယဘာဝ", "စတုတ္ထဘာဝ",
            "ပဉ္စမဘာဝ", "ဆဋ္ဌမဘာဝ", "သတ္တမဘာဝ", "အဋ္ဌမဘာဝ",
            "နဝမဘာဝ", "ဒသမဘာဝ", "ဧကာဒသမဘာဝ", "ဒွါဒသမဘာဝ"
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
        
        # ဂြိုဟ်များ၏ နေရာများ တွက်ချက်ခြင်း (အာယနထည့်သွင်း)
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
        self.toplevel = toplevel
        self.toplevel.title("မွေးနေ့ဇာတာတွက်ချက်ခြင်း")
        self.toplevel.geometry("1024x800")
        self.toplevel.resizable(False, False)
        
        # မြန်မာစာဖောင့်များ
        self.setup_myanmar_fonts()
        
        # အရောင်များ
        self.bg_color = "#f0f0f0"
        self.frame_color = "#e0e0e0"
        self.button_color = "#4CAF50"
        self.button_hover = "#45a049"
        
        self.toplevel.configure(bg=self.bg_color)
        
        # ဘယ်ဘက်အကွက် (အဝင်အချက်များ)
        self.left_frame = tk.Frame(toplevel, width=350, bg=self.frame_color, relief="raised", bd=2)
        self.left_frame.pack(side="left", fill="both", expand=False)
        self.left_frame.pack_propagate(False)
        
        # ညာဘက်အကွက် (ရလဒ်များ)
        self.right_frame = tk.Frame(toplevel, bg="white", relief="sunken", bd=2)
        self.right_frame.pack(side="right", fill="both", expand=True)
        
        
        # တည်ဆောက်ခြင်း
        self.create_input_widgets()
        self.create_output_widgets()
        
        # Calculator instance
        self.calculator = BirthChartCalculator()
    
    def setup_myanmar_fonts(self):
        """မြန်မာစာဖောင့်များ စီစဉ်ခြင်း"""
        try:
            # မြန်မာစာဖောင့်များရှာဖွေခြင်း
            available_fonts = font.families()
            self.mm_font = None
            
            # ဦးစားပေးဖောင့်များ
            preferred_fonts = [
                "Pyidaungsu",
                "Myanmar Text", 
                "Zawgyi-One",
                "Masterpiece Uni Sans",
                "Noto Sans Myanmar"
            ]
            
            for font_name in preferred_fonts:
                if font_name in available_fonts:
                    self.mm_font = font_name
                    break
            
            # မရှိပါက default ဖောင့်သုံးမည်
            if self.mm_font is None:
                self.mm_font = "TkDefaultFont"
                
        except Exception as e:
            print(f"Font setup error: {e}")
            self.mm_font = "TkDefaultFont"
    
    def create_input_widgets(self):
        
       
        # ခေါင်းစဉ်
        header = tk.Label(self.left_frame, text="မွေးနေ့ဇာတာအချက်အလက်များ", 
                         font=(self.mm_font, 14, "bold"), bg=self.frame_color, fg="#333")
        header.pack(pady=15)
        
        # User Name
        tk.Label(self.left_frame, text="အမည်   :", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=20, pady=(10,0))
        self.user_name = tk.Entry(self.left_frame, font=(self.mm_font, 10), width=30)
        self.user_name.pack(padx=20, pady=(0,10), fill="x")
        
        # Birth Date
        tk.Label(self.left_frame, text="မွေးသက္ကရာဇ် (YYYY-MM-DD)  :", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=20, pady=(10,0))
        self.birth_date = tk.Entry(self.left_frame, font=(self.mm_font, 10), width=30)
        self.birth_date.pack(padx=20, pady=(0,10), fill="x")
        self.birth_date.insert(0, "1990-05-15")
        
        # Birth Time
        tk.Label(self.left_frame, text="မွေးချိန် (HH:MM)   :", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=20, pady=(10,0))
        self.birth_time = tk.Entry(self.left_frame, font=(self.mm_font, 10), width=30)
        self.birth_time.pack(padx=20, pady=(0,10), fill="x")
        self.birth_time.insert(0, "08:30")
        
        # Birth Place
        tk.Label(self.left_frame, text="မွေးရာဒေသ   :", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=20, pady=(10,0))
        self.birth_place = tk.Entry(self.left_frame, font=(self.mm_font, 10), width=30)
        self.birth_place.pack(padx=20, pady=(0,10), fill="x")
        self.birth_place.insert(0, "ရန်ကုန်မြို့")
        
        # Latitude
        tk.Label(self.left_frame, text="လတ္တီကျုဒ် (Latitude)  :", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=20, pady=(10,0))
        self.latitude = tk.Entry(self.left_frame, font=(self.mm_font, 10), width=30)
        self.latitude.pack(padx=20, pady=(0,10), fill="x")
        self.latitude.insert(0, "16.8661")
        
        # Longitude
        tk.Label(self.left_frame, text="လောင်ဂျီကျုဒ် (Longitude)   :", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=20, pady=(10,0))
        self.longitude = tk.Entry(self.left_frame, font=(self.mm_font, 10), width=30)
        self.longitude.pack(padx=20, pady=(0,10), fill="x")
        self.longitude.insert(0, "96.1951")
        
        # Timezone
        tk.Label(self.left_frame, text="အချိန်ဇုန် (Timezone)   :", font=(self.mm_font, 10), bg=self.frame_color).pack(anchor="w", padx=20, pady=(10,0))
        self.timezone = tk.Entry(self.left_frame, font=(self.mm_font, 10), width=30)
        self.timezone.pack(padx=20, pady=(0,10), fill="x")
        self.timezone.insert(0, "+6.5")
        
      
        
        # Calculate Button
        self.calculate_btn = tk.Button(
            self.left_frame, text="တွက်ချက်မည်", 
            font=(self.mm_font, 12, "bold"), 
            bg=self.button_color, 
            fg="white",
            activebackground=self.button_hover,
            activeforeground="white",
            relief="raised",
            bd=3,
            padx=20,
            pady=10,
            command=self.calculate_chart
        )
        self.calculate_btn.pack(pady=20, padx=20, fill="x")
       
        # အကူအညွှန်း
        help_text = "အကူအညွှန်း:\n- ရက်စွဲနှင့်အချိန်ကို မှန်ကန်စွာဖြည့်ပါ\n- Latitude/Longitude ကို decimal format ဖြင့်ဖြည့်ပါ\n- Myanmar အတွက် Timezone = +6.5"
        help_label = tk.Label(self.left_frame, text=help_text, font=(self.mm_font, 9), 
                             bg=self.frame_color, fg="#666", justify="left")
        help_label.pack(pady=10, padx=20, anchor="w")
    
       

    def create_output_widgets(self):
        # ခေါင်းစဉ်
        header = tk.Label(self.right_frame, text="မွေးနေ့ဇာတာရလဒ်", 
                         font=(self.mm_font, 16, "bold"), bg="white", fg="#333")
        header.pack(pady=15)
        
        # ရလဒ်ပြရန် Text Widget
        self.output_text = tk.Text(
            self.right_frame, 
            wrap="word", 
            font=(self.mm_font, 11),
            bg="white",
            fg="#333",
            relief="flat",
            padx=20,
            pady=20,
            spacing1=5,
            spacing2=5,
            spacing3=5
        )
        self.output_text.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        
        
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
                house_system='P'
            )
            
            # ရလဒ်ပြသခြင်း
            self.display_results(user_name, birth_place, chart_data)
            
        except ValueError as e:
            messagebox.showerror("အမှား", f"အချက်အလက်ပုံစံမှားယွင်းနေသည်: {str(e)}")
        except Exception as e:
            messagebox.showerror("အမှား", f"တွက်ချက်ခြင်းမအောင်မြင်: {str(e)}")
    
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