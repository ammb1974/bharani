import tkinter as tk
from tkinter import messagebox, filedialog
import swisseph as swe
import numpy as np
from datetime import datetime
import os

class VedicAstrologyCalculator:
    def __init__(self):
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
                # Check if the path contains at least one ephemeris file
                if any(fname.endswith('.se1') for fname in os.listdir(path)):
                    swe.set_ephe_path(path)
                    print(f"Ephemeris path set to: {path}")
                    return
        
        self.ask_ephemeris_path()
    
    def ask_ephemeris_path(self):
        """User ကို ephemeris path ရွေးခိုင်းခြင်း"""
        toplevel = tk.Tk()
        toplevel.withdraw()
        
        messagebox.showinfo("Ephemeris Path", 
                          "Please select the folder containing Swiss Ephemeris files (usually named 'ephe')")
        
        ephe_path = filedialog.askdirectory(title="Select Ephemeris Files Folder")
        
        if ephe_path:
            swe.set_ephe_path(ephe_path)
            messagebox.showinfo("Success", f"Ephemeris path set to: {ephe_path}")
        else:
            messagebox.showerror("Error", "Ephemeris path is required.")
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
            
            print(f"JD: {jd}")
            
            # Lahiri ayanamsa ဖြင့် Sidereal mode သတ်မှတ်ခြင်း
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            ayanamsa = swe.get_ayanamsa(jd)
            print(f"Ayanamsa: {ayanamsa}")
            
            # Vehlow Equal House စနစ်ဖြင့် အိမ်ထောင့်များ တွက်ချက်ခြင်း
            hsys = b'V'  # Vehlow Equal House system
            cusps, ascmc = swe.houses(jd, lat, lon, hsys)
            
            print(f"Houses calculated successfully")
            print(f"Cusps length: {len(cusps)}")
            print(f"Cusps: {cusps}")
            
            # ဂြိုဟ်များ၏ နေရာများ တွက်ချက်ခြင်း (Sidereal + True Node)
            planets = []
            planet_ids = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
                         swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO,
                         swe.TRUE_NODE]  # True Rahu/Ketu
            
            for planet_id in planet_ids:
                try:
                    # True Node အတွက် special flags
                    if planet_id == swe.TRUE_NODE:
                        flags = swe.FLG_SIDEREAL | swe.FLG_TRUEPOS
                    else:
                        flags = swe.FLG_SIDEREAL
                    
                    # ဂြိုဟ်၏ နေရာ တွက်ချက်ခြင်း
                    xx, retflags = swe.calc_ut(jd, planet_id, flags)
                    if retflags == -1:
                        print(f"Error calculating {swe.get_planet_name(planet_id)}")
                        continue
                    
                    longitude = xx[0] % 360
                    
                    # အိမ်ရှာခြင်း (safe method)
                    house_num = self.find_house_safe(longitude, cusps)
                    
                    planets.append({
                        'name': swe.get_planet_name(planet_id),
                        'longitude': longitude,
                        'sign': self.get_zodiac_sign(longitude),
                        'house': house_num,
                        'position': xx
                    })
                    
                except Exception as e:
                    print(f"Error with planet {planet_id}: {e}")
                    continue
            
            # ရလဒ်များ ပြင်ဆင်ခြင်း
            results = {
                'name': name,
                'birth_datetime': birth_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'location': f"Lat: {lat}, Lon: {lon}",
                'ayanamsa': ayanamsa,
                'houses': self.prepare_houses_data_safe(cusps),
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
            print(f"Detailed error: {str(e)}")
            raise Exception(f"Calculation error: {str(e)}")
    
    def get_zodiac_sign(self, longitude):
        """ဒီဂရီကို ရာသီခွင်အမည်သို့ ပြောင်းလဲခြင်း"""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        sign_index = int(longitude // 30)
        degrees_in_sign = longitude % 30
        return f"{signs[sign_index]} {degrees_in_sign:.2f}°"
    
    def find_house_safe(self, longitude, cusps):
        """အိမ်ရှာခြင်း (safe version)"""
        try:
            # Cusps array ကို check လုပ်ခြင်း
            if len(cusps) < 13:
                print(f"Warning: cusps array too short: {len(cusps)}")
                return 1
                
            for i in range(1, 13):
                start_cusp = cusps[i]
                end_cusp = cusps[i + 1] if i < 12 else 360 + cusps[1]
                
                # Normalize longitudes for comparison
                norm_long = longitude % 360
                norm_start = start_cusp % 360
                norm_end = end_cusp % 360
                
                if norm_end < norm_start:
                    norm_end += 360
                
                if norm_start <= norm_long < norm_end:
                    return i
                    
            return 1  # default to 1st house
            
        except IndexError:
            print("Index error in find_house")
            return 1
    
    def prepare_houses_data_safe(self, cusps):
        """အိမ်ထောင့်များကို စနစ်တကျပြင်ဆင်ခြင်း (safe version)"""
        houses = []
        try:
            for i in range(1, 13):
                if i < len(cusps):
                    houses.append({
                        'house': i,
                        'cusp': cusps[i],
                        'sign': self.get_zodiac_sign(cusps[i])
                    })
                else:
                    houses.append({
                        'house': i,
                        'cusp': 0.0,
                        'sign': "Unknown"
                    })
            return houses
        except IndexError:
            print("Index error in prepare_houses_data")
            return [{'house': i, 'cusp': 0.0, 'sign': "Error"} for i in range(1, 13)]

class AstrologyGUI:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("Vehlow Equal + True Rahu + Sidereal Calculator")
        self.toplevel.geometry("900x700")
        
        self.calculator = VedicAstrologyCalculator()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Input Frame
        input_frame = tk.Frame(self.toplevel)
        input_frame.pack(pady=10)
        
        # Name
        tk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        self.name_entry.insert(0, "Test User")
        
        # Birth Date
        tk.Label(input_frame, text="Birth Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.date_entry = tk.Entry(input_frame, width=20)
        self.date_entry.grid(row=1, column=1, padx=5, pady=2)
        self.date_entry.insert(0, "1990-01-01")
        
        # Birth Time
        tk.Label(input_frame, text="Time (HH:MM:SS):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.time_entry = tk.Entry(input_frame, width=20)
        self.time_entry.grid(row=2, column=1, padx=5, pady=2)
        self.time_entry.insert(0, "12:00:00")
        
        # Location
        tk.Label(input_frame, text="Latitude:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.lat_entry = tk.Entry(input_frame, width=15)
        self.lat_entry.grid(row=3, column=1, padx=5, pady=2)
        self.lat_entry.insert(0, "16.7967")
        
        tk.Label(input_frame, text="Longitude:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.lon_entry = tk.Entry(input_frame, width=15)
        self.lon_entry.grid(row=4, column=1, padx=5, pady=2)
        self.lon_entry.insert(0, "96.1608")
        
        # Calculate Button
        self.calc_button = tk.Button(input_frame, text="Calculate Chart", 
                                   command=self.calculate_chart, bg="lightblue", font=("Arial", 12))
        self.calc_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Results Text Area
        result_frame = tk.Frame(self.toplevel)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(result_frame, text="Results:", font=("Arial", 14, "bold")).pack(anchor="w")
        
        self.result_text = tk.Text(result_frame, height=25, width=100, font=("Courier New", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
    
    def calculate_chart(self):
        try:
            # Get data from entries
            name = self.name_entry.get()
            birth_date = self.date_entry.get()
            birth_time = self.time_entry.get()
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            
            # Parse datetime
            birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
            
            # Calculate chart
            results = self.calculator.calculate_vedic_chart(name, birth_datetime, lat, lon)
            
            # Display results
            self.display_results(results)
            
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Please check your input values:\n{ve}")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred:\n{e}")
    
    def display_results(self, results):
        self.result_text.delete(1.0, tk.END)
        
        # Basic info
        self.result_text.insert(tk.END, f"Name: {results['name']}\n")
        self.result_text.insert(tk.END, f"Birth: {results['birth_datetime']}\n")
        self.result_text.insert(tk.END, f"Location: {results['location']}\n")
        self.result_text.insert(tk.END, f"Ayanamsa (Lahiri): {results['ayanamsa']:.6f}°\n")
        self.result_text.insert(tk.END, f"Method: {results['calculation_method']}\n")
        self.result_text.insert(tk.END, "-" * 70 + "\n\n")
        
        # Ascendant and MC
        self.result_text.insert(tk.END, f"Ascendant : {results['ascendant']['sign']}\n")
        self.result_text.insert(tk.END, f"MC        : {results['mc']['sign']}\n\n")
        
        # Houses (Vehlow Equal)
        self.result_text.insert(tk.END, "HOUSE CUSPS (Vehlow Equal):\n")
        for house in results['houses']:
            self.result_text.insert(tk.END, f"House {house['house']:2}: {house['sign']}\n")
        self.result_text.insert(tk.END, "\n")
        
        # Planets
        self.result_text.insert(tk.END, "PLANETARY POSITIONS (Sidereal + True Rahu):\n")
        for planet in results['planets']:
            house_info = f" in House {planet['house']}" if planet.get('house') else ""
            self.result_text.insert(tk.END, f"{planet['name']:12}: {planet['sign']}{house_info}\n")
        
        self.result_text.insert(tk.END, "\n" + "=" * 70 + "\n")

# Run the application
if __name__ == "__main__":
    toplevel = tk.Tk()
    app = AstrologyGUI(toplevel)
    toplevel.mainloop()