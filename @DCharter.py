import tkinter as tk
import json

zodiac_signs = [
    "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
    "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
]

class BurmeseGrid:
    def __init__(self, parent, width=300, height=300, bg="lightgray"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = (min(width, height) // 5) - 10

        self.zodiac_names = [
            "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
            "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
        ]

        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.on_click)



    def draw_grid(self, label_text="ရာသီ"):
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

        return self

    def draw_zodiac_labels(self):
        # Placeholder: You can add zodiac label positions here later
        pass

    def on_click(self, event):
        print(f"Mouse clicked at ({event.x}, {event.y})")

def main():
    toplevel = tk.Tk()
    toplevel.title("မြန်မာဗေဒင် Grid Viewer")

    grid_frame = tk.Frame(toplevel)
    grid_frame.pack(padx=10, pady=10)

    grid = BurmeseGrid(grid_frame)
    grid.draw_grid()
    grid.canvas.pack()
    
   

    toplevel.mainloop()

if __name__ == "__main__":
    main()