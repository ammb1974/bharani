import tkinter as tk

class BurmeseGrid:
    def __init__(self, parent, width=300, height=300, bg="lightgray", mode="zodiac"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        # ဇာတာအိမ် ၁၂ အိမ် နေရာချဖို့အတွက် cell_size ကို ၄ ပိုင်းခွဲဖို့ တွက်ထားတယ်
        self.cell_size = (min(width, height) // 4) 
        self.mode = mode  # "zodiac", "bhava", "navamsa"

        # ဂြိုဟ်ဒေတာ
        self.planets = [
            {"name": "Sun",     "symbol": "☉", "zodiac": 0,  "degree": 1, "minute": 19, "second": 30, "type": "zodiac"},  # မိဿ (Aries)
            {"name": "Moon",    "symbol": "☽", "zodiac": 4,  "degree": 15, "minute": 30, "second": 0, "type": "bhava"},  # သိဟ် (Leo)
            {"name": "Mars",    "symbol": "♂", "zodiac": 6,  "degree": 29, "minute": 59, "second": 59, "type": "navamsa"},# တူ (Libra)
            {"name": "Mercury", "symbol": "☿", "zodiac": 1,  "degree": 10, "minute": 45, "second": 20, "type": "zodiac"}, # ပြိဿ (Taurus)
            {"name": "Jupiter", "symbol": "♃", "zodiac": 8,  "degree": 5, "minute": 10, "second": 0, "type": "bhava"},  # ဓနု (Sagittarius)
            {"name": "Venus",   "symbol": "♀", "zodiac": 3,  "degree": 7, "minute": 22, "second": 15, "type": "navamsa"},# ကရကဋ် (Cancer)
            {"name": "Saturn",  "symbol": "♄", "zodiac": 10, "degree": 12, "minute": 5, "second": 0, "type": "zodiac"}, # ကုမ် (Aquarius)
        ]

        # ဇာတာအမည်များ
        self.zodiac_names = [
            "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
            "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
        ]
        self.navamsa_names = [f"နဝင်း {i+1}" for i in range(12)] # ၁၂ ခုလုံးကို နေရာချဖို့အတွက်
        self.bhava_names = [f"ဘာဝ {i+1}" for i in range(12)]    # ၁၂ ခုလုံးကို နေရာချဖို့အတွက်
        
        # Mouse click အတွက်
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_grid(self, label_text=None):
        if label_text is None:
            label_text = {"zodiac": "ရာသီ", "bhava": "ဘာဝ", "navamsa": "နဝင်း"}.get(self.mode, "ဇာတာ")

        self.canvas.delete("all")  # ရှင်းပါ
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size

        # အပြင်ဘက် လေးထောင့်
        self.canvas.create_rectangle(c_x - 2 * cell, c_y - 2 * cell, c_x + 2 * cell, c_y + 2 * cell, outline="black", width=2)
        # အတွင်းဘက် လေးထောင့်
        self.canvas.create_rectangle(c_x - cell, c_y - cell, c_x + cell, c_y + cell, outline="black", width=2)
        
        # ထောင့်ဖြတ်မျဉ်းများ (Diamond ပုံစံ)
        self.canvas.create_line(c_x - 2 * cell, c_y, c_x + 2 * cell, c_y, fill="black", width=1) # အလျားလိုက် အပြင်
        self.canvas.create_line(c_x, c_y - 2 * cell, c_x, c_y + 2 * cell, fill="black", width=1) # ဒေါင်လိုက် အပြင်
        self.canvas.create_line(c_x - cell, c_y, c_x + cell, c_y, fill="black", width=1)        # အလျားလိုက် အတွင်း
        self.canvas.create_line(c_x, c_y - cell, c_x, c_y + cell, fill="black", width=1)        # ဒေါင်လိုက် အတွင်း
        
        # ၄၅ ဒီဂရီ ထောင့်ဖြတ်မျဉ်းများ
        self.canvas.create_line(c_x - 2 * cell, c_y - 2 * cell, c_x + 2 * cell, c_y + 2 * cell, fill="black", width=1)
        self.canvas.create_line(c_x + 2 * cell, c_y - 2 * cell, c_x - 2 * cell, c_y + 2 * cell, fill="black", width=1)
        
        # Center label
        self.canvas.create_text(c_x, c_y, text=label_text, font=("Myanmar Text", 14, "bold"), fill="black")

        # Labels (ရာသီ/ဘာဝ/နဝင်း အမည်များ)
        self.draw_labels_for_mode()

        # သက်ဆိုင်ရာ mode နဲ့ ကိုက်ညီတဲ့ ဂြိုဟ်တွေကို ဆွဲပါ
        for planet in self.planets:
            if planet["type"] == self.mode:
                self.draw_planet(planet)

        return self

    def draw_labels_for_mode(self):
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size
        
        if self.mode == "zodiac":
            names = self.zodiac_names
            color = "darkgreen"
        elif self.mode == "navamsa":
            names = self.navamsa_names
            color = "purple"
        elif self.mode == "bhava":
            names = self.bhava_names
            color = "brown"
        else:
            return
            
        # အိမ် ၁၂ အိမ်ရဲ့ အမည်တွေကို နေရာချခြင်း
        # (ရာသီ 0 ကို အမြဲတမ်း အိမ် 1 မှာထားဖို့ ဇာတာပုံမှာ ပြင်ထားပါတယ်)
        house_coords = [
            (c_x, c_y + 1.5 * cell),    # အိမ် ၁: အောက် အလယ် (0)
            (c_x + 1.5 * cell, c_y + cell), # အိမ် ၂: ညာ အောက်
            (c_x + 1.5 * cell, c_y - cell), # အိမ် ၃: ညာ အပေါ်
            (c_x, c_y - 1.5 * cell),    # အိမ် ၄: အပေါ် အလယ်
            (c_x - 1.5 * cell, c_y - cell), # အိမ် ၅: ဘယ် အပေါ်
            (c_x - 1.5 * cell, c_y + cell), # အိမ် ၆: ဘယ် အောက်
            
            (c_x + cell, c_y + 0.5 * cell), # အိမ် ၇: အတွင်း ညာ အောက် (7)
            (c_x + cell, c_y - 0.5 * cell), # အိမ် ၈: အတွင်း ညာ အပေါ်
            (c_x - cell, c_y - 0.5 * cell), # အိမ် ၉: အတွင်း ဘယ် အပေါ်
            (c_x - cell, c_y + 0.5 * cell), # အိမ် ၁၀: အတွင်း ဘယ် အောက်

            (c_x + 0.5 * cell, c_y + 0.5 * cell), # အိမ် ၁၁: အလယ် အောက်ညာ (11)
            (c_x - 0.5 * cell, c_y + 0.5 * cell), # အိမ် ၁၂: အလယ် အောက်ဘယ်
        ]

        # မြန်မာဗေဒင် (အိန္ဒိယဗေဒင်) ရဲ့ ဇာတာပုံမှာ အိမ်တွေရဲ့ အမည်နေရာချပုံက ပုံစံရှိပါတယ်
        # House 1 နေရာမှာ Aries/မိဿ 0 ကို စပြီး နေရာချခြင်း
        # ဇာတာအိမ်နံပါတ် (1 to 12) နဲ့ ရာသီနံပါတ် (0 to 11) ကိုက်ညီအောင် လုပ်ထားပါတယ်
        
        # ဇာတာအိမ် နံပါတ် 1 မှ 12 အလိုက် အမည်များကို နေရာချမည်
        # (House 1 - House 12) 
        # (မိဿ/Aries - မိန်/Pisces)

        house_index_to_zodiac = [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1] 
        # [House 1: 0 (မိဿ), House 2: 11 (မိန်), ..., House 12: 1 (ပြိဿ)]

        # ဇာတာပုံရဲ့ အိမ်နံပါတ် ၁၂ ခုရဲ့ တည်နေရာကို စက်ဝိုင်းပုံစံ ပြန်ညှိမည်
        # (1) Bottom, (2) Bottom Right, (3) Right, (4) Top Right, (5) Top, (6) Top Left, (7) Left, (8) Bottom Left, (9) Center Right, (10) Center Top, (11) Center Left, (12) Center Bottom
        
        # House Index (1-12) -> Coordinates (approximate center of the house)
        house_coords_new = [
            (c_x, c_y + 1.5 * cell), # 1
            (c_x + 1.5 * cell, c_y + 1.5 * cell), # 2
            (c_x + 2 * cell, c_y), # 3
            (c_x + 1.5 * cell, c_y - 1.5 * cell), # 4
            (c_x, c_y - 2 * cell), # 5
            (c_x - 1.5 * cell, c_y - 1.5 * cell), # 6
            (c_x - 2 * cell, c_y), # 7
            (c_x - 1.5 * cell, c_y + 1.5 * cell), # 8
            (c_x + 0.5 * cell, c_y + 0.5 * cell), # 9 (Inner SE)
            (c_x + 0.5 * cell, c_y - 0.5 * cell), # 10 (Inner NE)
            (c_x - 0.5 * cell, c_y - 0.5 * cell), # 11 (Inner NW)
            (c_x - 0.5 * cell, c_y + 0.5 * cell), # 12 (Inner SW)
        ]

        # မြန်မာဗေဒင်ပုံစံအတိုင်း ရာသီအိမ် 1 (မိဿ) ကနေ 12 (မိန်) အထိ အစဉ်လိုက်နေရာချဖို့အတွက်
        # ရာသီအိမ် 0 (မိဿ) ကနေစပြီး clockwise လည်ပတ်ပုံစံနဲ့ နေရာချရပါမယ်။ 
        # House 1 = Zodiac 0 (မိဿ), House 2 = Zodiac 1 (ပြိဿ), ...
        
        house_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] # ရာသီနံပါတ် 0-11 ကို အိမ် 1-12 မှာ အစဉ်အတိုင်း ထားရန်

        # ဇာတာအိမ် အမည်များ (House Labels)
        for i in range(12):
            x, y = self._get_house_center(i) # ဇာတာအိမ် နံပါတ် i ရဲ့ အလယ်မှတ်
            
            # ဂြိုဟ်အမည် နေရာနဲ့ မတိုက်အောင် အမည်ကို အနည်းငယ် ရွှေ့ခြင်း
            if i in [0, 3, 6, 9]: # ထောင့်အိမ် (1, 4, 7, 10) အနီး
                text_y_offset = -15 if i in [3, 9] else 15
                text_x_offset = -15 if i in [6, 9] else 15
            else:
                text_y_offset = 0
                text_x_offset = 0

            self.canvas.create_text(
                x + text_x_offset, y + text_y_offset,
                text=names[i], 
                font=("Myanmar Text", 8), 
                fill=color,
                tags=f"house_{i}_label"
            )


    def _get_house_center(self, zodiac_index):
        """
        ရာသီနံပါတ် (0-11) ကို ဇာတာအိမ်ရဲ့ အလယ်မှတ် (x, y) အဖြစ် ပြန်ပေးသည်။
        House 1 (မိဿ) သည် အိမ်နံပါတ် 0 ဖြင့် စသည်။
        """
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size
        
        # ရာသီအိမ် ၁၂ အိမ်၏ အလယ်ဗဟို နေရာများ (1 = မိဿ, 2 = ပြိဿ, ...)
        # ရာသီအိမ် 0 = House 1 (Right-Middle)
        # ရာသီအိမ် 1 = House 2 (Top-Right)
        # ...
        
        # ဗေဒင်ဇာတာပုံစံ (Square/Diamond)
        house_coords = {
            0: (c_x + cell, c_y - cell), # 1: Right-Top (မိဿ)
            1: (c_x + 2 * cell, c_y),    # 2: Right-Middle (ပြိဿ)
            2: (c_x + cell, c_y + cell), # 3: Right-Bottom (မေထုန်)
            3: (c_x, c_y + 2 * cell),    # 4: Bottom-Middle (ကရကဋ်)
            4: (c_x - cell, c_y + cell), # 5: Left-Bottom (သိဟ်)
            5: (c_x - 2 * cell, c_y),    # 6: Left-Middle (ကန်)
            6: (c_x - cell, c_y - cell), # 7: Left-Top (တူ)
            7: (c_x, c_y - 2 * cell),    # 8: Top-Middle (ဗြိစ္ဆာ)
            
            8: (c_x + cell * 0.5, c_y - cell * 0.5), # 9: Center-Right-Top (ဓနု)
            9: (c_x + cell * 0.5, c_y + cell * 0.5), # 10: Center-Right-Bottom (မကာရ)
            10: (c_x - cell * 0.5, c_y + cell * 0.5), # 11: Center-Left-Bottom (ကုမ်)
            11: (c_x - cell * 0.5, c_y - cell * 0.5), # 12: Center-Left-Top (မိန်)
        }
        
        # ရာသီအိမ်အလိုက် နေရာချထားခြင်း (House 1 = Zodiac 0)
        return house_coords.get(zodiac_index, (c_x, c_y))

    def draw_planet(self, planet_data):
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size

        zodiac_index = planet_data["zodiac"] # 0 to 11
        
        # ဂြိုဟ် နေရာချမည့် အိမ်ရဲ့ အလယ်မှတ်ကို ရှာပါ
        house_x, house_y = self._get_house_center(zodiac_index)
        
        # ဂြိုဟ်တွေ အိမ်တစ်အိမ်တည်းမှာ စုပြုံမနေစေဖို့ (ဥပမာ: ၄ လုံးထက်မပိုစေရန်)
        # အိမ်တစ်အိမ်မှာ ဂြိုဟ်ဘယ်နှစ်လုံးရှိပြီလဲဆိုတာ စစ်ဆေးပြီး နေရာ ရွှေ့ပါ
        
        planets_in_house = [p for p in self.planets if p["zodiac"] == zodiac_index and p["type"] == self.mode]
        planet_index_in_house = planets_in_house.index(planet_data)
        
        # တစ်အိမ်တည်းမှာ ဂြိုဟ်များပြားပါက ဒေါင်လိုက် ရွှေ့ပေးခြင်း
        planet_x = house_x
        planet_y = house_y + (planet_index_in_house - (len(planets_in_house) - 1) / 2) * 10 
        # 10 pixel စီ ခြားပြီး အပေါ်အောက် ခွဲချသည်။

        # ဖော်ပြမည့် စာသား
        total_minutes = planet_data["minute"] + planet_data["second"] / 60
        display_text = f'{planet_data["symbol"]} {planet_data["degree"]}° {int(total_minutes)}′'

        # ဂြိုဟ်ကို ဆွဲပါ
        self.canvas.create_text(
            planet_x, planet_y,
            text=display_text,
            font=("Myanmar Text", 9, "bold"),
            fill="blue"
        )

    def on_click(self, event):
        print(f"[{self.mode}] Mouse clicked at ({event.x}, {event.y})")


def main():
    root = tk.Tk()
    root.title("မြန်မာဗေဒင် Grid Viewer")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # ရာသီ Grid (zodiac)
    grid_zodiac = BurmeseGrid(frame, width=300, height=300, bg="lightyellow", mode="zodiac")
    grid_zodiac.draw_grid()
    grid_zodiac.canvas.pack(side="left", padx=5)

    # ဘာဝ Grid (bhava)
    grid_bhava = BurmeseGrid(frame, width=300, height=300, bg="lightblue", mode="bhava")
    grid_bhava.draw_grid()
    grid_bhava.canvas.pack(side="left", padx=5)

    # နဝင်း Grid (navamsa)
    grid_navamsa = BurmeseGrid(frame, width=300, height=300, bg="lightpink", mode="navamsa")
    grid_navamsa.draw_grid()
    grid_navamsa.canvas.pack(side="left", padx=5)

    root.mainloop()


if __name__ == "__main__":
    main()