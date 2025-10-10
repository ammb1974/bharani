import tkinter as tk
import math

# ဂြိုဟ်တို့၏ တည်နေရာများ (degrees)
planets = {
    "Lagna": 10.695277777778,
    "Sun": 100.486912833333,
    "Moon": 26.5020220833333,
    "Mars": 163.196193833333,
    "Jupiter": 126.123213972222,
    "Venus": 96.3435823333333,
    "Saturn": 3.49313661111111,
    "Rahu": 287.268938444444,
    "Ketu": 107.268938444444,
    "Uranus": 44.7123589722222,
    "Neptune": 342.327093833333,
    "Pluto": 281.743067666667
}

# အိမ်များ၏ အမည်များ
house_names = ["၁", "၂", "၃", "၄", "၅", "၆", "၇", "၈", "၉", "၁၀", "၁၁", "၁၂"]

# အရောင်များ
colors = {
    "Lagna": "#FF5733", "Sun": "#FFD700", "Moon": "#C0C0C0", "Mars": "#FF4500",
    "Jupiter": "#FFA500", "Venus": "#32CD32", "Saturn": "#8B4513",
    "Rahu": "#4B0082", "Ketu": "#8A2BE2", "Uranus": "#00FFFF",
    "Neptune": "#0000FF", "Pluto": "#800000"
}

class KPChartApp:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("KP Natal Chart")
        
        # Canvas တည်ဆောက်ခြင်း
        self.canvas = tk.Canvas(toplevel, width=800, height=800, bg="black")
        self.canvas.pack(pady=20)
        
        # Chart ဆွဲခြင်း
        self.draw_chart()
        
        # အိမ်များနှင့် ဂြိုဟ်များ ပြခြင်း
        self.show_house_table()
    
    def draw_chart(self):
        # ဗဟိုနှင့် အချင်း
        center_x, center_y = 400, 400
        radius = 250
        
        # အပြင်ဘက်စက်ဝိုင်း
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline="white", width= 5
        )
        
        # အတွင်းစက်ဝိုင်း
        inner_radius = radius * 0.3
        self.canvas.create_oval(
            center_x - inner_radius, center_y - inner_radius,
            center_x + inner_radius, center_y + inner_radius,
            outline="white", width=1
        )
        
        # အိမ်များကို ခွဲခြမ်းခြင်း (တစ်အိမ်လျှင် 30 degrees)
        lagna_angle = planets["Lagna"]
        
        for i in range(12):
            # အိမ်စတင်မှတ်တိုင်
            lagna_angle= 0
            start_angle = ((lagna_angle + i * 30) % 360)-15
            
            # အိမ်ပိုင်းခြားမျဉ်း
            x1 = center_x + radius * math.cos(math.radians(start_angle))
            y1 = center_y - radius * math.sin(math.radians(start_angle))
            x2 = center_x + inner_radius * math.cos(math.radians(start_angle))
            y2 = center_y - inner_radius * math.sin(math.radians(start_angle))
            
            self.canvas.create_line(x1, y1, x2, y2, fill="white", width=1)
         
            
            # အိမ်နံပါတ်ရေးခြင်း
            label_radius = radius + 30
            label_x = center_x + label_radius * math.cos(math.radians(start_angle))
            label_y = center_y - label_radius * math.sin(math.radians(start_angle))
            
            self.canvas.create_text(
                label_x, label_y, text=house_names[i],
                fill="white", font=("Myanmar Text", 14, "bold")
            )
            
        # ဂြိုဟ်များထည့်ခြင်း
        for planet, angle in planets.items():
            if planet == "Lagna":
                continue
                
            # ဂြိုဟ်၏ တည်နေရာ (Lagna နှင့် နှိုင်းယှဉ်)
            relative_angle = (angle - lagna_angle) % 360
            canvas_angle = (relative_angle - 90) % 360  # ထိပ်မှ စတင်အရှေ့ဘက်သို့
            
            # ဂြိုဟ်၏ တည်နေရာ တွက်ချက်ခြင်း
            planet_radius = radius * 0.7 #0.9
            x = center_x + planet_radius * math.cos(math.radians(canvas_angle))
            y = center_y - planet_radius * math.sin(math.radians(canvas_angle))
            
            # ဂြိုဟ်ဆိုင်းရေးခြင်း
            self.canvas.create_oval(
                x - 8, y - 8, x + 8, y + 8,
                fill=colors[planet], outline="white", width=0.1
            )
            
            # ဂြိုဟ်အမည်ရေးခြင်း
            self.canvas.create_text(
                x+30, y , text=planet,
                fill="white", font=("Pyidaungsu", 9, "bold")
            )
        
        # Lagna ကို အထူးပြခြင်း
        lagna_x = center_x
        lagna_y = center_y - inner_radius
        self.canvas.create_oval(
            lagna_x - 10, lagna_y - 10, lagna_x + 10, lagna_y + 10,
            fill=colors["Lagna"], outline="yellow", width=3
        )
        self.canvas.create_text(
            lagna_x, lagna_y - 25, text="Lagna",
            fill="yellow", font=("Pyidaungsu", 10, "bold")
        )
    
    def show_house_table(self):
        # အိမ်များနှင့် ဂြိုဟ်များ ဇယား
        table_frame = tk.Frame(self.toplevel, bg="black")
        table_frame.pack(pady=10)
        
        # ခေါင်းစဉ်
        headers = ["အိမ်", "ဂြိုဟ်များ"]
        for i, header in enumerate(headers):
            label = tk.Label(
                table_frame, text=header, bg="black", fg="white",
                font=("Myanmar Text", 12, "bold"), padx=20
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # အိမ်များနှင့် ဂြိုဟ်များ ဖော်ပြခြင်း
        lagna_angle = planets["Lagna"]
        house_planets = {i: [] for i in range(1, 13)}
        
        for planet, angle in planets.items():
            if planet == "Lagna":
                continue
                
            relative_angle = (angle - lagna_angle) % 360
            house_num = int(relative_angle // 30) + 1
            house_planets[house_num].append(planet)
        
        for house_num in range(1, 13):
            # အိမ်နံပါတ်
            house_label = tk.Label(
                table_frame, text=f"အိမ် {house_num}", bg="black", fg="white",
                font=("Myanmar Text", 11), padx=20
            )
            house_label.grid(row=house_num, column=0, padx=5, pady=2, sticky="w")
            
            # ဂြိုဟ်များ
            planets_text = ", ".join(house_planets[house_num]) if house_planets[house_num] else "-"
            planets_label = tk.Label(
                table_frame, text=planets_text, bg="black", fg="white",
                font=("Pyidaungsu", 10), padx=20
            )
            planets_label.grid(row=house_num, column=1, padx=5, pady=2, sticky="w")

        # Lagna နှင့် ဂြိုဟ်များအကြား ချိတ်ဆက်မှု
        for planet, angle in planets.items():
            if planet == "Lagna":
                continue

            relative_angle = (angle - lagna_angle) % 360
            house_num = int(relative_angle // 30) + 1

            # အိမ်နံပါတ်နှင့် ဂြိုဟ်အကြား ချိတ်ဆက်မှု
           
      

if __name__ == "__main__":
    toplevel = tk.Tk()
    app = KPChartApp(toplevel)
    toplevel.mainloop()