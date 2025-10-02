import tkinter as tk
from tkinter import messagebox, filedialog
import swisseph as swe
from datetime import datetime
import os

class VedicAstrologyCalculator:
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.setup_ephemeris_path()
    
    def setup_ephemeris_path(self):
        """Ephemeris file path ကို သတ်မှတ်ခြင်း"""
        possible_paths = [
            r"C:\sweph\ephe",
            r"D:\sweph\ephe", 
            r"E:\sweph\ephe",
            "./ephe",
            "../ephe",
            os.path.join(os.path.dirname(__file__), "ephe"),
            "/usr/share/swissephemeris/ephe",
            "/usr/local/share/swissephemeris/ephe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                if any(fname.endswith('.se1') for fname in os.listdir(path)):
                    swe.set_ephe_path(path)
                    print(f"Ephemeris path set to: {path}")
                    return
        
        self.ask_ephemeris_path()
    
    def ask_ephemeris_path(self):
        """User ကို ephemeris path ရွေးခိုင်းခြင်း"""
        if self.parent_window:
            messagebox.showinfo("Ephemeris Path", 
                              "Please select the folder containing Swiss Ephemeris files (usually named 'ephe')",
                              parent=self.parent_window)
            
            ephe_path = filedialog.askdirectory(
                title="Select Ephemeris Files Folder",
                parent=self.parent_window
            )
        else:
            root = tk.Tk()
            root.withdraw()
            
            messagebox.showinfo("Ephemeris Path", 
                              "Please select the folder containing Swiss Ephemeris files (usually named 'ephe')")
            
            ephe_path = filedialog.askdirectory(title="Select Ephemeris Files Folder")
            root.destroy()
        
        if ephe_path:
            swe.set_ephe_path(ephe_path)
            messagebox.showinfo("Success", f"Ephemeris path set to: {ephe_path}", parent=self.parent_window)
        else:
            messagebox.showerror("Error", "Ephemeris path is required.", parent=self.parent_window)
            exit()
    
    def calculate_vedic_chart(self, name, birth_datetime, lat, lon):
        """
        Vehlow Equal + True Rahu + Sidereal စနစ်ဖြင့် တွက်ချက်ခြင်း
        """
        try:
            # Julian Day Number သို့ ပြောင်းလဲခြင်း
            jd = swe.julday(birth_datetime.year, 
                          birth_datetime.month, 
                          birth_datetime.day,
                          birth_datetime.hour + birth_datetime.minute/60.0 + birth_datetime.second/3600.0)
            
            # Lahiri ayanamsa ဖြင့် Sidereal mode သတ်မှတ်ခြင်း
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            ayanamsa = swe.get_ayanamsa(jd)
            
            # Vehlow Equal House စနစ်ဖြင့် အိမ်ထောင့်များ တွက်ချက်ခြင်း
            hsys = b'V'  # Vehlow Equal House system
            cusps, ascmc = swe.houses(jd, lat, lon, hsys)
            
            # ဂြိုဟ်များ၏ နေရာများ တွက်ချက်ခြင်း
            planets = []
            planet_ids = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
                         swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO,
                         swe.TRUE_NODE, swe.MEAN_NODE]
            
            print("\n=== Calculating Planetary Positions ===")
            print(f"Julian Day: {jd}")
            print(f"Ayanamsa: {ayanamsa:.6f}°")
            
            for planet_id in planet_ids:
                try:
                    if planet_id == swe.TRUE_NODE:
                        flags = swe.FLG_SIDEREAL | swe.FLG_TRUEPOS
                    else:
                        flags = swe.FLG_SIDEREAL
                    
                    xx, retflags = swe.calc_ut(jd, planet_id, flags)
                    if retflags == -1:
                        continue
                    
                    longitude = xx[0] % 360
                    house_num = self.find_house_safe(longitude, cusps)
                    
                    # Get planet name and handle decode error
                    planet_name_bytes = swe.get_planet_name(planet_id)
                    if isinstance(planet_name_bytes, bytes):
                        planet_name = planet_name_bytes.decode()
                    else:
                        planet_name = planet_name_bytes
                    
                    print(f"{planet_name}: Longitude={longitude:.6f}°, House={house_num}")
                    
                    planets.append({
                        'name': planet_name,
                        'longitude': longitude,
                        'sign': self.get_zodiac_sign(longitude),
                        'house': house_num
                    })
                    
                except Exception as e:
                    print(f"Error calculating planet {planet_id}: {str(e)}")
                    continue
            
            # ရလဒ်များ ပြင်ဆင်ခြင်း
            results = {
                'name': name,
                'birth_datetime': birth_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'location': f"Lat: {lat}, Lon: {lon}",
                'ayanamsa': ayanamsa,
                'houses': self.prepare_houses_data(cusps),
                'ascendant': {
                    'longitude': ascmc[0],
                    'sign': self.get_zodiac_sign(ascmc[0])
                },
                'mc': {
                    'longitude': ascmc[1],
                    'sign': self.get_zodiac_sign(ascmc[1])
                },
                'planets': planets,
                'calculation_method': "Vehlow Equal House + True Rahu + Sidereal (Lahiri)"
            }
            
            return results
            
        except Exception as e:
            raise Exception(f"Calculation error: {str(e)}")
    
    def get_zodiac_sign(self, longitude):
        """ဒီဂရီကို ရာသီခွင်အမည်သို့ ပြောင်းလဲခြင်း"""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        sign_index = int(longitude // 30)
        degrees_in_sign = longitude % 30
        return f"{signs[sign_index]} {degrees_in_sign:.2f}°"
    
    def find_house_safe(self, longitude, cusps):
        """အိမ်ရှာခြင်း"""
        try:
            norm_long = longitude % 360
            
            for i in range(1, 13):
                start_cusp = cusps[i] % 360
                end_cusp = cusps[i + 1] % 360 if i < 12 else (cusps[1] % 360) + 360
                
                if end_cusp < start_cusp:
                    end_cusp += 360
                
                if start_cusp <= norm_long < end_cusp:
                    return i
                    
            return 1
            
        except (IndexError, TypeError):
            return 1
    
    def prepare_houses_data(self, cusps):
        """အိမ်ထောင့်များကို စနစ်တကျပြင်ဆင်ခြင်း"""
        houses = []
        try:
            for i in range(1, 13):
                if i < len(cusps):
                    houses.append({
                        'house': i,
                        'cusp': cusps[i],
                        'sign': self.get_zodiac_sign(cusps[i])
                    })
            return houses
        except (IndexError, TypeError):
            return [{'house': i, 'cusp': 0.0, 'sign': "Error"} for i in range(1, 13)]

class BurmeseGrid:
    def __init__(self, parent, width=300, height=300, bg="lightgray"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = min(width, height) // 8
        
        # ရာသီခွင်အမည်များ
        self.zodiac_names = [
            "မိဿ", "ပြိဿ", "မေထုန်", "ကြကဋ်", "သိဟ်", "ကန်",
            "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
        ]
        
        # ရာသီခွင်များ၏ တည်နေရာများ
        self.zodiac_positions = {
            "မိဿ": (104, 9),
            "ပြိဿ": (46, 7),
            "မေထုန်": (6, 40),
            "ကြကဋ်": (12, 95),
            "သိဟ်": (6, 174),
            "ကန်": (45, 211),
            "တူ": (108, 168),
            "ဗြိစ္ဆာ": (171, 206),
            "ဓနု": (208, 91),
            "မကာရ": (188, 91),
            "ကုမ်": (215, 44),
            "မိန်": (178, 8)
        }
        
        # ဂြိုဟ်များ၏ မြန်မာအမည်များ
        self.planet_names = {
            "Sun": "နေ",
            "Moon": "လ",
            "Mercury": "ဗုဒ္ဓဟူး",
            "Venus": "ကြာသပတေး",
            "Mars": "အင်္ဂါ",
            "Jupiter": "သောကြာ",
            "Saturn": "စနေ",
            "Uranus": "ယူရေးနပ်စ်",
            "Neptune": "နက်ပကျွန်း",
            "Pluto": "ပလူတို",
            "True Node": "ရာဟု"
        }
        
        # ရာသီခွင်နှင့် ဂြိုဟ်များ၏ အရာဝတ္ထုများကို သိမ်းဆည်းရန်
        self.zodiac_objects = {}
        self.planet_objects = {}
        
        # Mouse click event ကို ချိတ်ဆက်ခြင်း
        self.canvas.bind("<Button-1>", self.on_click)
        
        # ဂြိုဟ်များ၏ တည်နေရာများကို သိမ်းဆည်းရန်
        self.planet_positions = {}
        self.house_positions = {}
    
    def draw_grid(self, label_text="ရာသီ"):
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size
        
        # Clear canvas
        self.canvas.delete("all")
        self.zodiac_objects = {}  # Clear zodiac objects
        self.planet_objects = {}  # Clear planet objects
        
        # Grid lines
        self.canvas.create_line(c_x - cell, c_y - 3*cell, c_x - cell, c_y + 3*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y - 3*cell, c_x + cell, c_y + 3*cell, fill="black", width=1)
        self.canvas.create_line(c_x - 3*cell, c_y - cell, c_x + 3*cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - 3*cell, c_y + cell, c_x + 3*cell, c_y + cell, fill="black", width=1)
        
        self.canvas.create_line(c_x - 3*cell, c_y - 3*cell, c_x - cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x + 3*cell, c_y - 3*cell, c_x + cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - cell, c_y + cell, c_x - 3*cell, c_y + 3*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y + cell, c_x + 3*cell, c_y + 3*cell, fill="black", width=1)
        
        # Center label
        self.canvas.create_text(c_x, c_y, text=label_text, font=("Pyidaungsu", 10, "bold"), fill="black")
        
        # Draw zodiac labels
        self.draw_zodiac_labels()
        
        # Draw planets if available
        self.draw_planets()
        
        return self
    
    def draw_zodiac_labels(self):
        # Draw zodiac signs at their specified positions
        for sign_name, (x, y) in self.zodiac_positions.items():
            zodiac_obj = self.canvas.create_text(
                x, y, 
                text=sign_name, 
                font=("Pyidaungsu", 8, "bold"), 
                fill="black"
            )
            self.zodiac_objects[sign_name] = zodiac_obj
    
    def update_planet_positions(self, planets, houses):
        # Store planet positions
        self.planet_positions = {}
        for planet in planets:
            self.planet_positions[planet['name']] = planet
        
        # Store house positions
        self.house_positions = {}
        for house in houses:
            self.house_positions[house['house']] = house
        
        # Debug print
        print("\n=== Updating Planet Positions ===")
        for planet_name, planet_data in self.planet_positions.items():
            print(f"Planet: {planet_name}, House: {planet_data.get('house', 'N/A')}")
        
        # Redraw the grid with planets
        self.draw_grid()
    
    def draw_planets(self):
        if not self.planet_positions:
            return
        
        print("\n=== Drawing Planets ===")
        
        # ရာသီခွင်အလိုက် ဂြိုဟ်များစုစည်းခြင်း
        planets_by_sign = {}
        for planet_name, planet_data in self.planet_positions.items():
            # ရာသီခွင်အမည်ကို ထုတ်ယူခြင်း
            sign_str = planet_data['sign']
            sign_english = sign_str.split()[0]
            
            # အင်္ဂလိပ်အမည်မှ မြန်မာအမည်သို့ ပြောင်းလဲခြင်း
            sign_myanmar = None
            if sign_english == "Aries":
                sign_myanmar = "မိဿ"
            elif sign_english == "Taurus":
                sign_myanmar = "ပြိဿ"
            elif sign_english == "Gemini":
                sign_myanmar = "မေထုန်"
            elif sign_english == "Cancer":
                sign_myanmar = "ကြကဋ်"
            elif sign_english == "Leo":
                sign_myanmar = "သိဟ်"
            elif sign_english == "Virgo":
                sign_myanmar = "ကန်"
            elif sign_english == "Libra":
                sign_myanmar = "တူ"
            elif sign_english == "Scorpio":
                sign_myanmar = "ဗြိစ္ဆာ"
            elif sign_english == "Sagittarius":
                sign_myanmar = "ဓနု"
            elif sign_english == "Capricorn":
                sign_myanmar = "မကာရ"
            elif sign_english == "Aquarius":
                sign_myanmar = "ကုမ်"
            elif sign_english == "Pisces":
                sign_myanmar = "မိန်"
            
            if sign_myanmar is None:
                continue
                
            if sign_myanmar not in planets_by_sign:
                planets_by_sign[sign_myanmar] = []
            planets_by_sign[sign_myanmar].append(planet_data)
        
        # ရာသီခွင်တစ်ခုစီတွင် ဂြိုဟ်များကို ဖော်ပြခြင်း
        for sign_myanmar, planets in planets_by_sign.items():
            if sign_myanmar not in self.zodiac_positions:
                continue
                
            base_x, base_y = self.zodiac_positions[sign_myanmar]
            
            # ပထမဂြိုဟ်အတွက် အောက်ခြေစာကလေးကို စတင်ခြင်း
            y_offset = 15
            
            for planet in planets:
                # ဂြိုဟ်၏ မြန်မာအမည်
                display_name = self.planet_names.get(planet['name'], planet['name'])
                
                # ဒီဂရီနှင့် မိနစ်များကို ရယူခြင်း
                longitude = planet['longitude']
                degrees = int(longitude)
                minutes = int((longitude - degrees) * 60)
                
                # ဖော်ပြစာကို ဖွဲ့စည်းခြင်း
                text = f"{display_name} {degrees}°{minutes}'"
                
                # ဂြိုဟ်ကို ရေးဆွဲခြင်း
                planet_obj = self.canvas.create_text(
                    base_x, base_y + y_offset, 
                    text=text, 
                    font=("Pyidaungsu", 7), 
                    fill="blue"
                )
                
                # ဂြိုဟ်အရာဝတ္ထုကို သိမ်းဆည်းခြင်း
                self.planet_objects[planet['name']] = planet_obj
                
                # နောက်ဂြိုဟ်အတွက် အောက်ခြေသို့ ရွှေ့ခြင်း
                y_offset += 10
                
                print(f"Drawing planet {display_name} in {sign_myanmar} at position ({base_x}, {base_y + y_offset})")
    
    def on_click(self, event):
        print(f"Mouse clicked at ({event.x}, {event.y})")

class AstrologyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehlow Equal + True Rahu + Sidereal Calculator")
        self.root.geometry("1000x700")
        
        self.calculator = VedicAstrologyCalculator(parent_window=root)
        self.create_widgets()
    
    def create_widgets(self):
        # Main Frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Frame for Inputs
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Input Frame
        input_frame = tk.LabelFrame(left_frame, text="Birth Information", font=("Pyidaungsu", 12, "bold"))
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Name
        tk.Label(input_frame, text="Name:", font=("Pyidaungsu", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame, width=30, font=("Pyidaungsu", 10))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.insert(0, "Test User")
        
        # Birth Date
        tk.Label(input_frame, text="Birth Date (YYYY-MM-DD):", font=("Pyidaungsu", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame, width=20, font=("Pyidaungsu", 10))
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.date_entry.insert(0, "1990-01-01")
        
        # Birth Time
        tk.Label(input_frame, text="Time (HH:MM:SS):", font=("Pyidaungsu", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.time_entry = tk.Entry(input_frame, width=20, font=("Pyidaungsu", 10))
        self.time_entry.grid(row=2, column=1, padx=5, pady=5)
        self.time_entry.insert(0, "12:00:00")
        
        # Location
        tk.Label(input_frame, text="Latitude:", font=("Pyidaungsu", 10)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.lat_entry = tk.Entry(input_frame, width=15, font=("Pyidaungsu", 10))
        self.lat_entry.grid(row=3, column=1, padx=5, pady=5)
        self.lat_entry.insert(0, "16.7967")
        
        tk.Label(input_frame, text="Longitude:", font=("Pyidaungsu", 10)).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.lon_entry = tk.Entry(input_frame, width=15, font=("Pyidaungsu", 10))
        self.lon_entry.grid(row=4, column=1, padx=5, pady=5)
        self.lon_entry.insert(0, "96.1608")
        
        # Calculate Button
        self.calc_button = tk.Button(input_frame, text="Calculate Chart", 
                                   command=self.calculate_chart, 
                                   bg="#4CAF50", fg="white", 
                                   font=("Pyidaungsu", 12, "bold"), 
                                   padx=20, pady=5)
        self.calc_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Results Frame
        result_frame = tk.LabelFrame(left_frame, text="Chart Results", font=("Pyidaungsu", 12, "bold"))
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results Text Area with Scrollbar
        text_frame = tk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_text = tk.Text(text_frame, height=20, width=60, font=("Courier New", 10))
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right Frame for Chart
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        
        # Chart Frame
        chart_frame = tk.LabelFrame(right_frame, text="Burmese Astrology Chart", font=("Pyidaungsu", 12, "bold"))
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Burmese Grid
        self.burmese_grid = BurmeseGrid(chart_frame, width=300, height=300)
        self.burmese_grid.canvas.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.burmese_grid.draw_grid()
    
    def calculate_chart(self):
        try:
            # Get input values
            name = self.name_entry.get().strip()
            birth_date = self.date_entry.get().strip()
            birth_time = self.time_entry.get().strip()
            lat = self.lat_entry.get().strip()
            lon = self.lon_entry.get().strip()
            
            # Validation
            if not all([name, birth_date, birth_time, lat, lon]):
                messagebox.showerror("Input Error", "Please fill in all fields")
                return
            
            # Parse values
            try:
                birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
                lat_float = float(lat)
                lon_float = float(lon)
            except ValueError:
                messagebox.showerror("Input Error", "Please check your input format:\n"
                                                 "Date: YYYY-MM-DD\n"
                                                 "Time: HH:MM:SS\n"
                                                 "Lat/Lon: numbers only")
                return
            
            # Calculate chart
            results = self.calculator.calculate_vedic_chart(name, birth_datetime, lat_float, lon_float)
            
            # Display results
            self.display_results(results)
            
            # Update chart
            self.burmese_grid.update_planet_positions(results['planets'], results['houses'])
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def display_results(self, results):
        self.result_text.delete(1.0, tk.END)
        
        # Basic info
        self.result_text.insert(tk.END, f"NAME: {results['name']}\n")
        self.result_text.insert(tk.END, f"BIRTH: {results['birth_datetime']}\n")
        self.result_text.insert(tk.END, f"LOCATION: {results['location']}\n")
        self.result_text.insert(tk.END, f"AYANAMSA: {results['ayanamsa']:.6f}° (Lahiri)\n")
        self.result_text.insert(tk.END, f"METHOD: {results['calculation_method']}\n")
        self.result_text.insert(tk.END, "=" * 70 + "\n\n")
        
        # Ascendant and MC
        self.result_text.insert(tk.END, f"ASCENDANT : {results['ascendant']['sign']}\n")
        self.result_text.insert(tk.END, f"MC        : {results['mc']['sign']}\n\n")
        
        # Houses
        self.result_text.insert(tk.END, "HOUSE CUSPS (Vehlow Equal):\n")
        for house in results['houses']:
            self.result_text.insert(tk.END, f"House {house['house']:2}: {house['sign']}\n")
        self.result_text.insert(tk.END, "\n")
        
        # Planets
        self.result_text.insert(tk.END, "PLANETARY POSITIONS:\n")
        for planet in results['planets']:
            house_info = f" in House {planet['house']}" if planet.get('house') else ""
            self.result_text.insert(tk.END, f"{planet['name']:12}: {planet['sign']}{house_info}\n")

def main():
    root = tk.Tk()
    app = AstrologyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()