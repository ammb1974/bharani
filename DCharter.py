import tkinter as tk
import json

zodiac_signs = [
    "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
    "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
]

class BurmeseGrid:
    """
    မြန်မာဗေဒင်ကွက်ဆွဲရန် custom component
    Note: ဤ class သည် tk.Canvas ကို inherit မလုပ်ထားသောကြောင့်
    layout method (pack, grid) များကို self.canvas ပေါ်တွင် ခေါ်ရမည်။
    """
    def __init__(self, parent, width=300, height=300, bg="lightgray"):
        # ဤ self.canvas သည် နေရာချရမည့် widget အစစ်အမှန်ဖြစ်သည်။
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg) 
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = (min(width, height) // 5) - 10

        self.zodiac_names = zodiac_signs

        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.on_click)

    def get_canvas(self):
        """အပြင်ဘက်မှ နေရာချရန်အတွက် အတွင်းမှ Canvas object ကို ပြန်ပေးသည်။"""
        return self.canvas

    def draw_grid(self, label_text="ရာသီ"):
        """ဗေဒင်ကွက်ပုံစံကို canvas ပေါ်တွင် ဆွဲသည်။"""
        self.canvas.delete("all") # အရင်ဆွဲထားတာတွေကို ရှင်းပစ်ပါ။
        
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

        # Zodiac labels
        self.draw_zodiac_labels()

        return self # BurmeseGrid object ကို ပြန်ပေးသည်။

    def draw_zodiac_labels(self):
        # ဇာတာခွင် ၁၂ ရာသီ အမည်များ ထည့်သွင်းရန်
        pass

    def on_click(self, event):
        print(f"Mouse clicked at ({event.x}, {event.y})")