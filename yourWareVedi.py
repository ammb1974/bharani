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
    def __init__(self, parent, width=400, height=400, bg="lightgray"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = min(width, height) // 8
        # ရာသီခွင် icon မလိုတော့တာကြောင့် ဖျက်ပစ်နိုင်ပါတယ်
        # self.zodiac_names = [...] မလိုတော့ပါ

        # ဂြိုဟ်များ၏ မြန်မာအမည်များ (သင့်အတိုင်း ထားပါမယ်)
        self.planet_names = {
            "Sun": "☉",
            "Moon": "☽",
            "Mercury": "☿",
            "Venus": "♃",  # Note: သင့်မှာ Venus ကို ♃ (Jupiter သင်္ကေတ) ထားတာ မှားနိုင်ပါတယ်
            "Mars": "♂",
            "Jupiter": "♀",  # ဒါလည်း မှားနေနိုင်ပါတယ်
            "Saturn": "♄",
            "Uranus": "♅",
            "Neptune": "♆",
            "Pluto": "♇",
            "True Node": "H",
            "Mean Node": "M"  # Added for Mean Node
        }

        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.on_click)
        # Store planet positions
        self.planet_positions = {}
        # Store house positions (now we need house positions, not zodiac)
        self.house_positions = {}  # Key: house number (1-12), Value: (x, y)
        # Store planet objects for easy access
        self.planet_objects = {}

        # Initialize house positions (for 12 houses in Burmese grid layout)
        self.init_house_positions()

    def init_house_positions(self):
        """Define positions for 12 houses in Burmese grid (clockwise, starting from top)"""
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size

        # Define house positions (House 1 to 12) — အားလုံး (x, y) tuple ဖြစ်အောင် သေချာသတ်မှတ်ပါ
        self.house_positions = {
            1: (c_x, c_y - 2 * cell),
            2: (c_x + cell, c_y - int(1.5 * cell)),
            3: (c_x + 2 * cell, c_y),
            4: (c_x + cell, c_y + int(1.5 * cell)),
            5: (c_x, c_y + 2 * cell),
            6: (c_x - cell, c_y + int(1.5 * cell)),
            7: (c_x - 2 * cell, c_y),
            8: (c_x - cell, c_y - int(1.5 * cell)),
            9: (c_x + int(1.5 * cell), c_y - 2 * cell),
            10: (c_x + int(1.5 * cell), c_y + 2 * cell),
            11: (c_x - int(1.5 * cell), c_y + 2 * cell),
            12: (c_x - int(1.5 * cell), c_y - 2 * cell),
        }

    def draw_grid(self, label_text="ရာသီ"):
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size

        # Clear canvas
        self.canvas.delete("all")
        self.planet_objects = {}

        # Grid lines
        self.canvas.create_line(c_x - cell, c_y - 3*cell, c_x - cell, c_y + 3*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y - 3*cell, c_x + cell, c_y + 3*cell, fill="black", width=1)
        self.canvas.create_line(c_x - 3*cell, c_y - cell, c_x + 3*cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - 3*cell, c_y + cell, c_x + 3*cell, c_y + cell, fill="black", width=1)

        self.canvas.create_line(c_x - 3*cell, c_y - 3*cell, c_x - cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x + 3*cell, c_y - 3*cell, c_x + cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - cell, c_y + cell, c_x - 3*cell, c_y + 3*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y + cell, c_x + 3*cell, c_y + 3*cell, fill="black", width=1)

        # Center label - Myanmar Text, 11pt
        self.canvas.create_text(c_x, c_y, text=label_text, font=("Myanmar Text", 11, "bold"), fill="black")

        # DO NOT draw zodiac labels (as requested)

        # Draw planets if available
        self.draw_planets()

        return self

    def update_planet_positions(self, planets, houses):
        # Store planet positions
        self.planet_positions = {}
        for planet in planets:
            self.planet_positions[planet['name']] = planet

        # We don't need house data from 'houses' parameter for drawing,
        # because we have fixed house positions in self.house_positions
        # But if you want to show house cusps later, you can store it
        # self.house_cusps = {h['house']: h for h in houses}

        # Debug print
        print("\n=== Updating Planet Positions ===")
        for planet_name, planet_data in self.planet_positions.items():
            print(f"Planet: {planet_name}, House: {planet_data.get('house', 'N/A')}")

        # Redraw the grid with planets
        self.draw_grid()

        def draw_planets(self):
            if not self.planet_positions:
                return

        print("\n=== HOUSE POSITIONS DEBUG ===")
        for h, pos in self.house_positions.items():
            print(f"House {h}: {pos} (type: {type(pos)})")

        print("\n=== Drawing Planets ===")

        # Group planets by house
        house_planets = {}
        for planet_name, planet_data in self.planet_positions.items():
            house = planet_data.get('house', 1)
            if house not in house_planets:
                house_planets[house] = []
            house_planets[house].append(planet_name)

        # For each house, draw planets vertically stacked
        for house, planet_names in house_planets.items():
            if house not in self.house_positions:
                print(f"House {house} position not defined!")
                continue

            pos = self.house_positions[house]
            if not isinstance(pos, tuple) or len(pos) != 2:
                print(f"ERROR: Invalid position for house {house}: {pos}")
                continue

            base_x, base_y = pos

            # Determine horizontal offset (left/right/center)
            if house in [3, 4, 5, 10]:      # right side houses
                offset_x = -18  # နည်းနည်းပိုဝေးအောင် (ဂြိုဟ်+ဒီဂရီ နေရာယူမှာမို့)
            elif house in [7, 8, 9, 12]:    # left side houses
                offset_x = 18
            else:                           # center column houses
                offset_x = 0

            # Vertical spacing between planets in same house
            vertical_spacing = 20  # နည်းနည်းပိုကြီးအောင် (ဒီဂရီဖော်ပြမှာမို့)
            num_planets = len(planet_names)
            start_y = base_y - ((num_planets - 1) * vertical_spacing) // 2

            for i, planet_name in enumerate(planet_names):
                # Get symbol
                display_symbol = self.planet_names.get(planet_name, planet_name[:1])

                # Get longitude (in degrees)
                longitude = self.planet_positions[planet_name].get('longitude', 0.0)

                # Convert to degrees and minutes
                deg = int(longitude)
                minutes = int((longitude - deg) * 60)

                # Format as "☉ 12°30′"
                display_text = f"{display_symbol} {deg}°{minutes:02d}′"

                planet_y = start_y + i * vertical_spacing
                planet_x = base_x + offset_x

                # Draw planet with degree & minute - Myanmar Text, 11pt
                planet_obj = self.canvas.create_text(
                    planet_x, planet_y,
                    text=display_text,
                    font=("Myanmar Text", 11, "bold"),
                    fill="blue"
                )

                self.planet_objects[planet_name] = planet_obj
                print(f"Drawing planet {display_text} in HOUSE {house} at ({planet_x}, {planet_y})")

    def on_click(self, event):
        print(f"Mouse clicked at ({event.x}, {event.y})")
        
    def __init__(self, parent, width=400, height=400, bg="lightgray"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        # 400x400 အတွက် cell_size ကို ပြောင်းလဲခြင်း
        self.cell_size = min(width, height) // 8  # 400/8 = 50
        self.zodiac_names = [
            "♈︎", "♉︎", "♊︎", "♋︎", "♌︎", "♍︎",
            "♎︎", "♏︎", "♐︎", "♑︎", "♒︎", "♓︎"
        ]
        # ဂြိုဟ်များ၏ မြန်မာအမည်များ
        self.planet_names = {
            "Sun": "☉",
            "Moon": "☽",
            "Mercury": "☿",
            "Venus": "♀",   # Fixed
            "Mars": "♂",
            "Jupiter": "♃", # Fixed
            "Saturn": "♄",
            "Uranus": "♅",
            "Neptune": "♆",
            "Pluto": "♇",
            "True Node": "H",
            "Mean Node": "M"  # Added
}
        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.on_click)
        # Store planet positions
        self.planet_positions = {}
        # Store house positions
        self.house_positions = {}
        # Store zodiac positions
        self.zodiac_positions = {}
        # Store planet objects for easy access
        self.planet_objects = {}

    def draw_grid(self, label_text="ရာသီ"):
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size
        
        # Clear canvas
        self.canvas.delete("all")
        self.planet_objects = {}  # Clear planet objects
        
        # Grid lines - 400x400 အတွက် ပြင်ဆင်ခြင်း
        # အလယ်က စတဲ့ မျဉ်းကြောင်းများ
        self.canvas.create_line(c_x - cell, c_y - 3*cell, c_x - cell, c_y + 3*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y - 3*cell, c_x + cell, c_y + 3*cell, fill="black", width=1)
        self.canvas.create_line(c_x - 3*cell, c_y - cell, c_x + 3*cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - 3*cell, c_y + cell, c_x + 3*cell, c_y + cell, fill="black", width=1)
        
        # ထောင့်များမှ စတဲ့ မျဉ်းကြောင်းများ
        self.canvas.create_line(c_x - 3*cell, c_y - 3*cell, c_x - cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x + 3*cell, c_y - 3*cell, c_x + cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - cell, c_y + cell, c_x - 3*cell, c_y + 3*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y + cell, c_x + 3*cell, c_y + 3*cell, fill="black", width=1)
        
        # Center label
        self.canvas.create_text(c_x, c_y, text=label_text, font=("Myanmar Text", 10, "bold"), fill="black")
        
        # Draw zodiac labels
        self.draw_zodiac_labels()
        
        # Draw planets if available
        self.draw_planets()
        
        return self
    
    def draw_zodiac_labels(self):
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size
        
        # Define positions for each zodiac sign - 400x400 အတွက် ပြင်ဆင်ခြင်း
        positions = [
            (c_x, c_y - 2*cell),  # မိဿ (Aries) - top
            (c_x + cell, c_y - 1.5*cell),  # ပြိဿ (Taurus) - top-right
            (c_x + 2*cell, c_y),  # မေထုန် (Gemini) - right
            (c_x + cell, c_y + 1.5*cell),  # ကရကဋ် (Cancer) - bottom-right
            (c_x, c_y + 2*cell),  # သိဟ် (Leo) - bottom
            (c_x - cell, c_y + 1.5*cell),  # ကန် (Virgo) - bottom-left
            (c_x - 2*cell, c_y),  # တူ (Libra) - left
            (c_x - cell, c_y - 1.5*cell),  # ဗြိစ္ဆာ (Scorpio) - top-left
        ]
        
        # Draw the 8 main zodiac signs
        for i, (x, y) in enumerate(positions):
            self.zodiac_positions[i+1] = (x, y)  # Store position for house 1-8
            self.canvas.create_text(x, y, text=self.zodiac_names[i], font=("Pyidaungsu", 12, "bold"), fill="black")
        
        # Draw the remaining 4 zodiac signs in the corners
        # ဓနု (Sagittarius) - top-right corner
        x, y = c_x + 1.5*cell, c_y - 2*cell
        self.zodiac_positions[9] = (x, y)
        self.canvas.create_text(x, y, text=self.zodiac_names[8], font=("Pyidaungsu", 12, "bold"), fill="black")
        
        # မကာရ (Capricorn) - bottom-right corner
        x, y = c_x + 1.5*cell, c_y + 2*cell
        self.zodiac_positions[10] = (x, y)
        self.canvas.create_text(x, y, text=self.zodiac_names[9], font=("Pyidaungsu", 12, "bold"), fill="black")
        
        # ကုမ် (Aquarius) - bottom-left corner
        x, y = c_x - 1.5*cell, c_y + 2*cell
        self.zodiac_positions[11] = (x, y)
        self.canvas.create_text(x, y, text=self.zodiac_names[10], font=("Pyidaungsu", 12, "bold"), fill="black")
        
        # မိန် (Pisces) - top-left corner
        x, y = c_x - 1.5*cell, c_y - 2*cell
        self.zodiac_positions[12] = (x, y)
        self.canvas.create_text(x, y, text=self.zodiac_names[11], font=("Pyidaungsu", 12, "bold"), fill="black")
    
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
        
        # For each planet, find its house and draw it
        for planet_name, planet_data in self.planet_positions.items():
            house = planet_data.get('house', 1)
            
            # Get the position of this house
            if house in self.zodiac_positions:
                x, y = self.zodiac_positions[house]
                
                # Use Myanmar name if available
                display_name = self.planet_names.get(planet_name, planet_name)
                
                # 400x400 အတွက် ဂြိုဟ်များ၏ တည်နေရာကို ပြင်ဆင်ခြင်း
                # အပေါ်ဘက်ရှိ ရာသီများအတွက် အောက်ဘက်သို့၊ အောက်ဘက်ရှိ ရာသီများအတွက် အပေါ်ဘက်သို့ ရွှေ့ခြင်း
                if house in [1, 2, 3, 9, 10, 11]:  # အပေါ်ဘက်ရှိ အိမ်များ
                    planet_y = y + 8
                else:  # အောက်ဘက်ရှိ အိမ်များ
                    planet_y = y - 8
                
                # ဘယ်ညာဘက်ရှိ ရာသီများအတွက် တည်နေရာပြောင်းလဲခြင်း
                if house in [3, 4, 5, 10]:  # ညာဘက်ရှိ အိမ်များ
                    planet_x = x - 10
                elif house in [7, 8, 9, 12]:  # ဘယ်ဘက်ရှိ အိမ်များ
                    planet_x = x + 10
                else:  # အလယ်ရှိ အိမ်များ
                    planet_x = x
                
                # Draw planet at the calculated position
                planet_obj = self.canvas.create_text(
                    planet_x, planet_y, 
                    text=display_name, 
                    font=("Pyidaungsu", 14, "bold"), 
                    fill="blue"
                )
                
                # Store the planet object for later reference
                self.planet_objects[planet_name] = planet_obj
                
                print(f"Drawing planet {display_name} in house {house} at position ({planet_x}, {planet_y})")
            else:
                print(f"House {house} not found in zodiac_positions")
    
    def on_click(self, event):
        print(f"Mouse clicked at ({event.x}, {event.y})")

class AstrologyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehlow Equal + True Rahu + Sidereal Calculator")
        self.root.geometry("1000x700")  # 400x400 ဇယားအတွက် window size ကို ပြောင်းလဲခြင်း
        
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
        
        # Create Burmese Grid - 400x400 အရွယ်အစား
        self.burmese_grid = BurmeseGrid(chart_frame, width=400, height=400)
        self.burmese_grid.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
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