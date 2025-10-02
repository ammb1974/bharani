import tkinter as tk
from tkinter import ttk
import math

class BurmeseGrid:
    def __init__(self, parent, width=300, height=300, bg="lightgray"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = (min(width, height) // 5) - 10
        self.points = []
        self.planets = {}  # Store planet positions

    def draw_grid(self, label_text="မြန်မာ"):
        c_x, c_y = self.center_x, self.center_y 
        cell = self.cell_size

        # Vertical lines
        self.canvas.create_line(c_x - cell, c_y - (5*cell), c_x - cell, c_y + (5*cell), fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y - 5*cell, c_x + cell, c_y + 5*cell, fill="black", width=1)

        # Horizontal lines
        self.canvas.create_line(c_x - 5*cell, c_y - cell, c_x + 5*cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - 5*cell, c_y + cell, c_x + 5*cell, c_y + cell, fill="black", width=1)

        # Diagonal lines
        self.canvas.create_line(c_x - 5*cell, c_y - 5*cell, c_x - cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x + 5*cell, c_y - 5*cell, c_x + cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - cell, c_y + cell, c_x - 5*cell, c_y + 5*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y + cell, c_x + 5*cell, c_y + 5*cell, fill="black", width=1)

        # Draw zodiac signs (counter-clockwise)
        zodiac_signs = ["မိန်", "ကုမ်", "မကာရ", "ဓနု", "ဗြိစ္ဆာ", "တူ", 
                       "ကန်", "သိဟ်", "ကရကဋ်", "မေထုန်", "ပြိဿ", "မိဿ"]
        
        zodiac_positions = []
        for i in range(12):
            angle = math.radians(i * 30 - 90)  # Start from top, counter-clockwise
            radius = 4.5 * cell
            x = c_x + radius * math.cos(angle)
            y = c_y + radius * math.sin(angle)
            zodiac_positions.append((x, y))
            self.canvas.create_text(x, y, text=zodiac_signs[i], font=("Myanmar Text", 8), fill="darkblue")

        # Center label
        self.canvas.create_text(c_x, c_y, text=label_text, font=("Myanmar Text", 14, "bold"), fill="black")

        return self

    def add_planet(self, planet_number, house_number):
        """Add a planet to a specific house (1-12)"""
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size
        
        # Planet symbols mapping
        planet_symbols = {
            "၁": "Sun", "၂": "Moon", "၃": "Mars", "၄": "Mercury",
            "၅": "Jupiter", "၆": "Venus", "၀": "Saturn", 
            "၈": "Rahu", "၉": "Ketu"
        }
        
        # Calculate position in the house (counter-clockwise from top)
        angle = math.radians((house_number - 1) * 30 - 90)  # Start from top, counter-clockwise
        radius = 3.5 * cell
        
        x = c_x + radius * math.cos(angle)
        y = c_y + radius * math.sin(angle)
        
        # Draw planet
        planet_text = f"{planet_number}"
        planet_id = self.canvas.create_text(x, y, text=planet_text, 
                                          font=("Myanmar Text", 12, "bold"), 
                                          fill="red")
        
        # Add planet name below
        name_id = self.canvas.create_text(x, y+20, text=planet_symbols.get(planet_number, ""), 
                                        font=("Myanmar Text", 8), fill="darkred")
        
        self.planets[planet_number] = (house_number, planet_id, name_id)
        return planet_id, name_id

    def calculate_stretch_status(self, x, y):
        """Calculate if the point stretches the grid or not"""
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size
        
        # Calculate distance from center
        dx = x - c_x
        dy = y - c_y
        
        # Check if point is within the inner square
        within_inner_square = (abs(dx) <= cell and abs(dy) <= cell)
        
        # Check if point is within the outer boundary
        within_outer_boundary = (abs(dx) <= 5*cell and abs(dy) <= 5*cell)
        
        # Check if point is on any of the grid lines (with some tolerance)
        on_vertical_line = (abs(abs(dx) - cell) < 5) or (abs(dx) < 5)
        on_horizontal_line = (abs(abs(dy) - cell) < 5) or (abs(dy) < 5)
        on_diagonal = False
        
        # Check diagonal lines (with tolerance)
        for i in range(1, 6):
            if abs(abs(dx) - i*cell) < 5 and abs(abs(dy) - i*cell) < 5:
                on_diagonal = True
                break
        
        # Determine stretch status
        if within_inner_square:
            return "အတွင်းအကွက်", "green"
        elif within_outer_boundary and not within_inner_square:
            if on_vertical_line or on_horizontal_line or on_diagonal:
                return "အကွက်ဆန့်", "red"
            else:
                return "အပြင်အကွက်", "orange"
        else:
            return "အကွက်ပြင်ပ", "purple"

    def add_point(self, x, y):
        """Add a point to the canvas and store its coordinates"""
        # Draw a small circle at the clicked position
        stretch_status, color = self.calculate_stretch_status(x, y)
        point_id = self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=color, outline="")
        
        # Add text near the point showing coordinates
        text_id = self.canvas.create_text(x+15, y-15, text=f"({x}, {y})", 
                                         font=("Myanmar Text", 8), fill=color)
        
        self.points.append((x, y, point_id, text_id, stretch_status))
        return point_id, text_id, stretch_status

    def clear_points(self):
        """Remove all points from the canvas"""
        for x, y, point_id, text_id, status in self.points:
            self.canvas.delete(point_id)
            self.canvas.delete(text_id)
        self.points = []

class App:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("မြန်မာ့ဇာတာခွင်နှင့် ဂြိုဟ်တွေ")
        
        # Create main frame
        main_frame = ttk.Frame(toplevel, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create grid
        self.grid = BurmeseGrid(main_frame, width=500, height=500)
        self.grid.canvas.grid(row=0, column=0, padx=5, pady=5)
        
        # Create info panel
        info_frame = ttk.LabelFrame(main_frame, text="အချက်အလက်များ", padding="5")
        info_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.N, tk.S))
        
        # Create listbox to display coordinates with stretch info
        self.coord_list = tk.Listbox(info_frame, width=35, height=20, font=("Myanmar Text", 10))
        self.coord_list.grid(row=0, column=0, padx=5, pady=5)
        
        # Add scrollbar to listbox
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.coord_list.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.coord_list.configure(yscrollcommand=scrollbar.set)
        
        # Planet control frame
        planet_frame = ttk.LabelFrame(info_frame, text="ဂြိုဟ်ထည့်သွင်းခြင်း", padding="5")
        planet_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Planet selection
        ttk.Label(planet_frame, text="ဂြိုဟ်:").grid(row=0, column=0, sticky=tk.W)
        self.planet_var = tk.StringVar()
        planet_combo = ttk.Combobox(planet_frame, textvariable=self.planet_var, width=10)
        planet_combo['values'] = ('၁ - Sun', '၂ - Moon', '၃ - Mars', '၄ - Mercury', 
                                 '၅ - Jupiter', '၆ - Venus', '၀ - Saturn', '၈ - Rahu', '၉ - Ketu')
        planet_combo.grid(row=0, column=1, padx=5)
        planet_combo.current(0)
        
        # House selection
        ttk.Label(planet_frame, text="ရာသီအိမ်:").grid(row=1, column=0, sticky=tk.W)
        self.house_var = tk.StringVar()
        house_combo = ttk.Combobox(planet_frame, textvariable=self.house_var, width=10)
        house_combo['values'] = tuple(f"{i} - {house}" for i, house in enumerate([
            "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်", 
            "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
        ], 1))
        house_combo.grid(row=1, column=1, padx=5, pady=5)
        house_combo.current(0)
        
        # Add planet button
        add_planet_btn = ttk.Button(planet_frame, text="ဂြိုဟ်ထည့်မည်", command=self.add_planet)
        add_planet_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Add clear button
        clear_btn = ttk.Button(info_frame, text="အစက်အားလုံးဖျက်မည်", command=self.clear_points)
        clear_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Add legend frame
        legend_frame = ttk.LabelFrame(info_frame, text="အရောင်အဓိပ္ပါယ်များ", padding="5")
        legend_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Add legend items
        ttk.Label(legend_frame, text="• အနီ - အကွက်ဆန့်", foreground="red").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(legend_frame, text="• အနက် - အတွင်းအကွက်", foreground="green").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(legend_frame, text="• လိမ္မော် - အပြင်အကွက်", foreground="orange").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(legend_frame, text="• ခရမ်း - အကွက်ပြင်ပ", foreground="purple").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(legend_frame, text="• အနီ/ကြီး - ဂြိုဟ်များ", foreground="red", font=("Myanmar Text", 9, "bold")).grid(row=4, column=0, sticky=tk.W)
        ttk.Label(legend_frame, text="• အပြာ - ရာသီခွင်", foreground="darkblue").grid(row=5, column=0, sticky=tk.W)
        
        # Bind mouse click event
        self.grid.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Draw the grid
        self.grid.draw_grid()
        
    def add_planet(self):
        """Add a planet to the grid"""
        planet_str = self.planet_var.get()
        house_str = self.house_var.get()
        
        if planet_str and house_str:
            planet_num = planet_str.split(' - ')[0]
            house_num = int(house_str.split(' - ')[0])
            
            # Add planet to the grid (this will make it appear on the canvas)
            self.grid.add_planet(planet_num, house_num)
            
            # Add to listbox
            planet_names = {
                "၁": "Sun", "၂": "Moon", "၃": "Mars", "၄": "Mercury",
                "၅": "Jupiter", "၆": "Venus", "၀": "Saturn", 
                "၈": "Rahu", "၉": "Ketu"
            }
            
            zodiac_names = [
                "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်", 
                "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
            ]
            
            display_text = f"{planet_names.get(planet_num, '')} ({planet_num}) in {zodiac_names[house_num-1]}"
            self.coord_list.insert(tk.END, display_text)
            self.coord_list.itemconfig(tk.END, fg="red")
            self.coord_list.see(tk.END)
        
    def on_canvas_click(self, event):
        """Handle mouse click on canvas"""
        x, y = event.x, event.y
        
        # Add point to grid
        point_id, text_id, stretch_status = self.grid.add_point(x, y)
        
        # Add coordinates and stretch status to listbox
        display_text = f"({x}, {y}) - {stretch_status}"
        self.coord_list.insert(tk.END, display_text)
        
        # Color the list item based on stretch status
        color_map = {
            "အတွင်းအကွက်": "green",
            "အကွက်ဆန့်": "red",
            "အပြင်အကွက်": "orange", 
            "အကွက်ပြင်ပ": "purple"
        }
        self.coord_list.itemconfig(tk.END, fg=color_map[stretch_status])
        
        # Auto-scroll to the bottom
        self.coord_list.see(tk.END)
    
    def clear_points(self):
        """Clear all points from grid and listbox"""
        self.grid.clear_points()
        self.coord_list.delete(0, tk.END)

if __name__ == "__main__":
    toplevel = tk.Tk()
    app = App(toplevel)
    toplevel.mainloop()