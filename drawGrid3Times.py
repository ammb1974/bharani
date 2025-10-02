import tkinter as tk

class BurmeseGrid:
    def __init__(self, parent, width=300, height=300, bg="lightgray", mode="zodiac"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = (min(width, height) // 5) - 10
        self.mode = mode  # "zodiac", "bhava", "navamsa"

        # ဂြိုဟ်ဒေတာ
        self.planets = [
            {"name": "Sun",     "symbol": "☉", "zodiac": 0,  "degree": 1, "minute": 19, "second": 30, "type": "zodiac"},
            {"name": "Moon",    "symbol": "☽", "zodiac": 4,  "degree": 15, "minute": 30, "second": 0, "type": "bhava"},
            {"name": "Mars",    "symbol": "♂", "zodiac": 6,  "degree": 29, "minute": 59, "second": 59, "type": "navamsa"},
            {"name": "Mercury", "symbol": "☿", "zodiac": 1,  "degree": 10, "minute": 45, "second": 20, "type": "zodiac"},
            {"name": "Jupiter", "symbol": "♃", "zodiac": 8,  "degree": 5, "minute": 10, "second": 0, "type": "bhava"},
            {"name": "Venus",   "symbol": "♀", "zodiac": 3,  "degree": 7, "minute": 22, "second": 15, "type": "navamsa"},
        ]

        # ဇာတာအမည်များ
        self.zodiac_names = [
            "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
            "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
        ]
        self.navamsa_names = ["ပထမ", "ဒုတိယ", "တတိယ", "စတုတ္ထ", "ပဉ္စမ", "ဆဋ္ဌမ", "သတ္တမ", "အဋ္ဌမ", "နဝမ"]
        self.bhava_names = self.navamsa_names.copy()

        # Mouse click အတွက်
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_grid(self, label_text=None):
        if label_text is None:
            label_text = {"zodiac": "ရာသီ", "bhava": "ဘာဝ", "navamsa": "နဝင်း"}.get(self.mode, "ဇာတာ")

        self.canvas.delete("all")  # ရှင်းပါ
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size

        # Grid lines
        self.canvas.create_line(c_x - cell, c_y - 5*cell, c_x - cell, c_y + 5*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y - 5*cell, c_x + cell, c_y + 5*cell, fill="black", width=1)
        self.canvas.create_line(c_x - 5*cell, c_y - cell, c_x + 5*cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - 5*cell, c_y + cell, c_x + 5*cell, c_y + cell, fill="black", width=1)
        self.canvas.create_line(c_x - 5*cell, c_y - 5*cell, c_x - cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x + 5*cell, c_y - 5*cell, c_x + cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - cell, c_y + cell, c_x - 5*cell, c_y + 5*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y + cell, c_x + 5*cell, c_y + 5*cell, fill="black", width=1)

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
            y_offset = -2 * cell - 20
        elif self.mode == "navamsa":
            names = self.navamsa_names
            y_offset = 20
        elif self.mode == "bhava":
            names = self.bhava_names
            y_offset = 2 * cell + 20
        else:
            return

        # ဘယ်၊ အလယ်၊ ညာ အကွက် ၃ ခုအတွက် အမည်ဆွဲ
        for i in range(3):
            x = c_x + (i - 1) * 2 * cell
            y = c_y + y_offset
            name = names[i]
            color = {"zodiac": "darkgreen", "bhava": "brown", "navamsa": "purple"}.get(self.mode, "black")
            self.canvas.create_text(x, y, text=name, font=("Myanmar Text", 10), fill=color)

    def draw_planet(self, planet_data):
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size

        # သီးသန့် grid ဖြစ်လို့ အလယ်တန်းမှာပဲ ဆွဲမယ်
        row_offset = 0
        col_index = planet_data["zodiac"] % 3
        col_offset = (col_index - 1) * 2 * cell

        # ဘယ်ဘက်ကို 10px ရွေ့ပါ
        planet_x = c_x + col_offset - 10
        planet_y = c_y + row_offset

        # ဖော်ပြမည့် စာသား
        total_minutes = planet_data["minute"] + planet_data["second"] / 60
        display_text = f'{planet_data["symbol"]} {planet_data["degree"]}° {int(total_minutes)}′'

        # ဂြိုဟ်ကို ဆွဲပါ
        self.canvas.create_text(
            planet_x, planet_y,
            text=display_text,
            font=("Myanmar Text", 12, "bold"),
            fill="blue"
        )

    def on_click(self, event):
        print(f"[{self.mode}] Mouse clicked at ({event.x}, {event.y})")


def main():
    root = tk.Tk()
    root.title("မြန်မာဗေဒင် Grid Viewer")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # ရာသီ Grid
    grid_zodiac = BurmeseGrid(frame, width=200, height=200, bg="lightyellow", mode="zodiac")
    grid_zodiac.draw_grid()
    grid_zodiac.canvas.pack(side="left", padx=5)

    # ဘာဝ Grid
    grid_bhava = BurmeseGrid(frame, width=200, height=200, bg="lightblue", mode="bhava")
    grid_bhava.draw_grid()
    grid_bhava.canvas.pack(side="left", padx=5)

    # နဝင်း Grid
    grid_navamsa = BurmeseGrid(frame, width=200, height=200, bg="lightpink", mode="navamsa")
    grid_navamsa.draw_grid()
    grid_navamsa.canvas.pack(side="left", padx=5)

    root.mainloop()


if __name__ == "__main__":
    main()