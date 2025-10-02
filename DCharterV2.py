import tkinter as tk
import math

class BurmeseGrid:
    def __init__(self, parent, width=300, height=300, bg="lightgray"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = min(width, height) // 15 # ပိုမိုကောင်းမွန်သော cell size calculation

        self.zodiac_names = [
            "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
            "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
        ]
        
        # ရာသီအလိုက် ဂြိုဟ်များ ရေးမည့်နေရာများ (အသစ်ပြင်ဆင်ထားသော coordinates)
        self.planet_positions = {
            "မိဿ": self.calculate_position(174, 13),    # အပေါ်ဆုံး
            "ပြိဿ": self.calculate_position(95, 8),   # 30 degrees
            "မေထုန်": self.calculate_position(8, 55),  # 60 degrees
            "ကရကဋ်": self.calculate_position(9, 176),  # 90 degrees (ညာဘက်)
            "သိဟ်": self.calculate_position(12, 354),  # 120 degrees
            "ကန်": self.calculate_position(98, 410),  # 150 degrees
            "တူ": self.calculate_position(178, 354),    # 180 degrees (အောက်ခြေ)
            "ဗြိစ္ဆာ": self.calculate_position(374, 400), # 210 degrees
            "ဓနု": self.calculate_position(424, 349),  # 240 degrees
            "မကာရ": self.calculate_position(352, 169), # 270 degrees (ဘယ်ဘက်)
            "ကုမ်": self.calculate_position(442, 68),  # 300 degrees
            "မိန်": self.calculate_position(352, 14)   # 330 degrees
        }
        
        # ဂြိုဟ်သင်္ကေတများ
        self.planet_symbols = {
            "Sun": "၁",
            "Moon": "၂",
            "Mars": "၃",
            "Mercury": "၄",
            "Jupiter": "၅",
            "Venus": "၆",
            "Saturn": "၀",
            "Uranus": "U",
            "Neptune": "N",
            "Pluto": "P",
            "Lagna": "L"
        }
        
        # ဂြိုဟ်များအတွက် text positions များ သိမ်းဆည်းရန်
        self.planet_text_positions = {zodiac: [] for zodiac in self.zodiac_names}

    def calculate_position(self, angle_degrees, radius_factor):
        """ထောင့်နှင့် အကွာအဝေးအရ position calculate လုပ်သည်"""
        angle_rad = math.radians(angle_degrees)
        radius = self.cell_size * 4 * radius_factor
        x = self.center_x + radius * math.cos(angle_rad)
        y = self.center_y - radius * math.sin(angle_rad)  # Canvas y coordinates are inverted
        return x, y

    def draw_grid(self, label_text="ရာသီ"):
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size

        # Grid lines
        self.canvas.create_line(c_x - cell, c_y - 2.5*cell, c_x - cell, c_y + 2.5*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y - 2.5*cell, c_x + cell, c_y + 2.5*cell, fill="black", width=1)
        self.canvas.create_line(c_x - 2.5*cell, c_y - cell, c_x + 2.5*cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - 2.5*cell, c_y + cell, c_x + 2.5*cell, c_y + cell, fill="black", width=1)
        self.canvas.create_line(c_x - 2.5*cell, c_y - 2.5*cell, c_x - cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x + 2.5*cell, c_y - 2.5*cell, c_x + cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - cell, c_y + cell, c_x - 2.5*cell, c_y + 2.5*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y + cell, c_x + 2.5*cell, c_y + 2.5*cell, fill="black", width=1)

        # Center label
        self.canvas.create_text(c_x, c_y, text=label_text, font=("Myanmar Text", 11, "bold"), fill="black")

        # Zodiac labels
       # self.draw_zodiac_labels()

        return self
        # Zodiac labels
       # self.draw_zodiac_labels()

        #return self

    def draw_zodiac_labels(self):
        """ရာသီခွင်အမည်များ ရေးသားခြင်း"""
        for zodiac, (x, y) in self.planet_positions.items():
            self.canvas.create_text(x, y, text=zodiac, 
                                  font=("Myanmar Text", 10, "bold"), 
                                  fill="darkblue")

    def write_planet(self, zodiac_name, planet_name, degree_str):
        """
        ဂြိုဟ်တစ်ခုကို ရာသီအတွင်းရေးသားပါ
        """
        # ရာသီအမည်နှင့် ကိုက်ညီမှုရှာပါ
        matched_zodiac = None
        for zodiac in self.zodiac_names:
            if zodiac == zodiac_name:
                matched_zodiac = zodiac
                break
        
        if not matched_zodiac:
            print(f"Error: {zodiac_name} အတွက် နေရာများ သတ်မှတ်ထားခြင်း မရှိပါ")
            return False
        
        base_x, base_y = self.planet_positions[matched_zodiac]
        
        # ဂြိုဟ်သင်္ကေတရယူပါ
        symbol = self.planet_symbols.get(planet_name, planet_name)
        
        # ရာသီအမည်ရဲ့ အောက်မှာ စပြီးရေးသားရန်
        start_y = base_y + 20
        
        # လက်ရှိနေရာမှာ ရှိပြီးသား text များ၏ y coordinates များ
        existing_y_positions = self.planet_text_positions[matched_zodiac]
        
        if existing_y_positions:
            # ရှိပြီးသား y positions များထဲမှ အမြင့်ဆုံးကို ရှာပါ
            last_y = max(existing_y_positions)
            new_y = last_y + 100  # 25 pixels spacing
        else:
            new_y = start_y
        
        # symbol နှင့် degree ကို ရေးသားပါ
        text_id1 = self.canvas.create_text(base_x, new_y, text=symbol, 
                                        font=("Myanmar Text", 12, "bold"),
                                        fill="darkred")
        
        text_id2 = self.canvas.create_text(base_x + 20, new_y, text=degree_str, 
                                        font=("Myanmar Text", 8),
                                        fill="darkred")
        
        # y position ကို မှတ်သားထားပါ
        self.planet_text_positions[matched_zodiac].append(new_y)
        
        print(f"{planet_name} ({ symbol} { degree_str}) ကို {matched_zodiac} ရာသီတွင် ရေးသားပြီး")
        return True

    def write_planets(self, planet_data):
        """
        ဂြိုဟ်များအားလုံးကို ရေးသားပါ
        """
        for planet_name, data in planet_data.items():
            if "zodiac" in data and "degree" in data:
                self.write_planet(data["zodiac"], planet_name, data["degree"])

def main():
    root = tk.Tk()
    root.title("မြန်မာဗေဒင် Grid Viewer")
    root.geometry("400x400")

    grid_frame = tk.Frame(root)
    grid_frame.pack(padx=20, pady=20)

    grid = BurmeseGrid(grid_frame, width=400, height=400)
    grid.draw_grid()
    grid.canvas.pack()
    
    # သင့်ရဲ့ ဂြိုဟ်တွေရဲ့ တည်နေရာဒေတာများ
    planet_data = {
        "Lagna": {"zodiac": "သိဟ်", "degree": "8°47'"},
        "Sun": {"zodiac": "ကန်", "degree": "7°24'"},
        "Moon": {"zodiac": "ဓနု", "degree": "29°17'"},
        "Mercury": {"zodiac": "သိဟ်", "degree": "24°19'"},
        "Venus": {"zodiac": "သိဟ်", "degree": "5°47'"},
        "Mars": {"zodiac": "သိဟ်", "degree": "14°57'"},
        "Jupiter": {"zodiac": "ကရကဋ်", "degree": "17°36' R"},
        "Saturn": {"zodiac": "မိဿ", "degree": "0°07' R"},
        "Uranus": {"zodiac": "မိဿ", "degree": "1°26'"},
        "Neptune": {"zodiac": "ပြိဿ", "degree": "1°23'"},
        "Pluto": {"zodiac": "မကာရ", "degree": "1°48' R"}
    }
    
    # ဂြိုဟ်များကို ရေးသားပါ
    grid.write_planets(planet_data)

    root.mainloop()

if __name__ == "__main__":
    main()