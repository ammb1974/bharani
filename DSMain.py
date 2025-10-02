import tkinter as tk
from tkinter import ttk
import math
from DChart import BurmeseGrid  # Burm

class BurmeseAstrologyGrid:
    def __init__(self, parent, width=600, height=600, bg="white", rotation_angle =15):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.radius = min(width, height) * 0.4  # Chart radius
        
        # 12 zodiac signs in Burmese
        self.zodiac_signs = ["မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", 
                            "သိဟ်", "ကန်", "တူ", "ဗြိစ္ဆာ", 
                            "ဓနု", "မကာရ", "ကုမ်", "မိန်"]
        
        # Planet symbols
        self.planet_symbols = {
            "Lagna": "လ",
            "Sun": "၁",
            "Moon": "၂",
            "Mars": "၃",
            "Mercury": "၄",
            "Jupiter": "၅",
            "Venus": "၆",
            "Saturn": "၀",
            "Rahu": "၈",
            "Ketu": "၉",
            "Uranus": "U",
            "Neptune": "N",
            "Pluto": "P"
        }
        
        # Planet positions (degree, minute, second, retrograde)
        self.planet_positions = {}
        
    def draw_grid(self):
        # Draw outer circle
        self.canvas.create_oval(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            outline="black",
            width=2
        )
        
        # Draw zodiac signs
        for i in range(12):
            angle = math.radians(i * 30 - 90)  # Start from top, anticlockwise
            x = self.center_x + (self.radius - 20) * math.cos(angle)
            y = self.center_y + (self.radius - 20) * math.sin(angle)
            
            # Draw zodiac sign
            self.canvas.create_text(x, y, text=self.zodiac_signs[i], 
                                   font=("Myanmar Text", 12, "bold"))
            
            # Draw division lines
            inner_x = self.center_x + (self.radius - 50) * math.cos(angle)
            inner_y = self.center_y + (self.radius - 50) * math.sin(angle)
            self.canvas.create_line(self.center_x, self.center_y, inner_x, inner_y, 
                                   fill="gray", width=10)
        
        # Draw inner circles
        for r in [self.radius * 0.7, self.radius * 0.5, self.radius * 0.3]:
            self.canvas.create_oval(
                self.center_x - r,
                self.center_y - r,
                self.center_x + r,
                self.center_y + r,
                outline="gray",
                width=1
                
            )
        
        # Draw center point
        self.canvas.create_oval(
            self.center_x - 5,
            self.center_y - 5,
            self.center_x + 5,
            self.center_y + 5,
            fill="black"
        )
        
        return self
    
    def set_planet_position(self, planet, degree, minute=0, second=0, retrograde=False):
        """Set planet position in degrees (0-360)"""
        self.planet_positions[planet] = {
            'degree': degree,
            'minute': minute,
            'second': second,
            'retrograde': retrograde
        }
    
    def draw_planets(self):
        """Draw all planets on the chart"""
        for planet, pos in self.planet_positions.items():
            # Calculate angle (anticlockwise from right, 0-360 degrees)
            angle_rad = math.radians(pos['degree'] - 90)  # Adjust for starting from top
            
            # Calculate position (middle circle)
            r = self.radius * 0.6
            x = self.center_x + r * math.cos(angle_rad)
            y = self.center_y + r * math.sin(angle_rad)
            
            # Draw planet symbol
            symbol = self.planet_symbols.get(planet, planet)
            if pos['retrograde']:
                symbol += "R"
            
            # Create planet text with degree details
            degree_text = f"{pos['degree']}°{pos['minute']}'{pos['second']}\""
            
            # Draw planet
            self.canvas.create_text(x, y, text=symbol, 
                                   font=("Pyidaungsu", 14, "bold"), fill="blue")
            
            # Draw degree details below planet
            self.canvas.create_text(x, y + 20, text=degree_text, 
                                   font=("Pyidaungsu", 8), fill="darkblue")
    
    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)
        return self
    
    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)
        return self

class AstrologyApp:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("မြန်မာ့ဇာတာဖွဲ့စည်းပုံ")
        self.toplevel.geometry("1000x800")
        
        # Create main frame
        main_frame = ttk.Frame(toplevel, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create astrology grid
        self.grid = BurmeseAstrologyGrid(main_frame, width=600, height=600)
        self.grid.draw_grid().pack(side=tk.LEFT, padx=10, pady=10)
        
        # Create control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(control_frame, text="ဂြိုဟ်တွေထည့်သွင်းရန်", 
                 font=("Myanmar Text", 14, "bold")).pack(pady=10)
        
        # Planet selection
        ttk.Label(control_frame, text="ဂြိုဟ်ရွေးပါ:").pack(anchor=tk.W, pady=5)
        self.planet_var = tk.StringVar()
        planet_combo = ttk.Combobox(control_frame, textvariable=self.planet_var,
                                   values=list(self.grid.planet_symbols.keys()))
        planet_combo.pack(fill=tk.X, pady=5)
        planet_combo.set("Sun")
        
        # Degree input
        ttk.Label(control_frame, text="ဒီဂရီ (0-360):").pack(anchor=tk.W, pady=5)
        self.degree_var = tk.StringVar(value="0")
        degree_entry = ttk.Entry(control_frame, textvariable=self.degree_var)
        degree_entry.pack(fill=tk.X, pady=5)
        
        # Minute input
        ttk.Label(control_frame, text="မိနစ် (0-59):").pack(anchor=tk.W, pady=5)
        self.minute_var = tk.StringVar(value="0")
        minute_entry = ttk.Entry(control_frame, textvariable=self.minute_var)
        minute_entry.pack(fill=tk.X, pady=5)
        
        # Second input
        ttk.Label(control_frame, text="စက္ကန့် (0-59):").pack(anchor=tk.W, pady=5)
        self.second_var = tk.StringVar(value="0")
        second_entry = ttk.Entry(control_frame, textvariable=self.second_var)
        second_entry.pack(fill=tk.X, pady=5)
        
        # Retrograde checkbox
        self.retro_var = tk.BooleanVar()
        retro_check = ttk.Checkbutton(control_frame, text="Retrograde (နောက်ပြန်)", 
                                     variable=self.retro_var)
        retro_check.pack(anchor=tk.W, pady=10)
        
        # Add planet button
        add_btn = ttk.Button(control_frame, text="ဂြိုဟ်ထည့်ပါ", command=self.add_planet)
        add_btn.pack(pady=10)
        
        # Clear button
        clear_btn = ttk.Button(control_frame, text="အားလုံးဖျက်ပါ", command=self.clear_planets)
        clear_btn.pack(pady=5)
        
        # Sample data button
        sample_btn = ttk.Button(control_frame, text="နမူနာဒေတာထည့်ပါ", command=self.add_sample_data)
        sample_btn.pack(pady=10)
        
        # Information display
        info_frame = ttk.LabelFrame(control_frame, text="အချက်အလက်")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = """
ဂြိုဟ်သင်္ကေတများ:
လ = Lagna
၁ = Sun
၂ = Moon
၃ = Mars
၄ = Mercury
၅ = Jupiter
၆ = Venus
၀ = Saturn
၈ = Rahu
၉ = Ketu
U = Uranus
N = Neptune
P = Pluto
R = Retrograde
        """
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(padx=5, pady=5)
    
    def add_planet(self):
        try:
            planet = self.planet_var.get()
            degree = float(self.degree_var.get())
            minute = int(self.minute_var.get())
            second = int(self.second_var.get())
            retro = self.retro_var.get()
            
            if not 0 <= degree < 360:
                tk.messagebox.showerror("Error", "Degree must be between 0 and 360")
                return
            
            self.grid.set_planet_position(planet, degree, minute, second, retro)
            self.redraw_chart()
            
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numbers")
    
    def clear_planets(self):
        self.grid.planet_positions = {}
        self.redraw_chart()
    
    def add_sample_data(self):
        # Sample planetary positions
        sample_data = [
            ("Lagna", 45, 30, 15, False),
            ("Sun", 120, 15, 0, False),
            ("Moon", 210, 45, 30, False),
            ("Mars", 300, 20, 10, True),
            ("Mercury", 75, 10, 5, False),
            ("Jupiter", 150, 35, 20, False),
            ("Venus", 225, 50, 40, False),
            ("Saturn", 30, 5, 0, True)
        ]
        
        for planet, deg, min, sec, retro in sample_data:
            self.grid.set_planet_position(planet, deg, min, sec, retro)
        
        self.redraw_chart()
    
    def redraw_chart(self):
        self.grid.canvas.delete("all")
        self.grid.draw_grid()
        self.grid.draw_planets()

if __name__ == "__main__":
    toplevel = tk.Tk()
    app = AstrologyApp(toplevel)
    toplevel.mainloop()