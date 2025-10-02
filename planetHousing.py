import tkinter as tk
from tkinter import ttk, messagebox
import math
import datetime
from PIL import Image, ImageDraw, ImageFont
import io

class MyanmarAstrologyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("မြန်မာဇာတာပုံ - Advanced Version")
        self.root.geometry("1000x900")
        self.root.configure(bg="#f0f0f0")
        
        # ဇာတာပုံဆွဲရန် canvas
        self.canvas = tk.Canvas(root, width=800, height=800, bg="white", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # ရာသီအမည်များ
        self.zodiac_signs = ["မိဿ", "ပြိဿ", "မေထုန်", "ကြကဋ်", "သိဟ်", "ကန်", 
                            "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"]
        
        # ဘာဝအမည်များ
        self.bhavas = ["လက္ခဏ", "ဓန", "ပရိသတ်", "သုခ", "သားသမီး", "ရန်သူ", 
                       "ဇနီး/ခင်ပွန်း", "အသက်", "ဘာသာ", "အလုပ်", "အကျိုးအမြတ်", "ကံ"]
        
        # ဂြိုဟ်အမည်များနှင့်အရောင်များ
        self.planets = {
            "နေ": {"color": "#FFD700", "symbol": "☉"},
            "လ": {"color": "#C0C0C0", "symbol": "☽"},
            "အင်္ဂါ": {"color": "#FF4500", "symbol": "♂"},
            "ဗုဒ္ဓဟူး": {"color": "#90EE90", "symbol": "☿"},
            "ကြာသပတေး": {"color": "#FFA500", "symbol": "♃"},
            "သောကြာ": {"color": "#FFC0CB", "symbol": "♀"},
            "စနေ": {"color": "#DAA520", "symbol": "♄"}
        }
        
        # ဂြိုဟ်တွေရဲ့ ယာယီတည်နေရာများ (ဒီမှာ ဥပမာအနေနဲ့သာပြထားတယ်)
        self.planet_positions = {
            "နေ": {"sign": 0, "degree": 19, "minute": 57, "bhava": 1},
            "လ": {"sign": 2, "degree": 8, "minute": 5, "bhava": 3},
            "အင်္ဂါ": {"sign": 5, "degree": 14, "minute": 23, "bhava": 6},
            "ဗုဒ္ဓဟူး": {"sign": 7, "degree": 3, "minute": 42, "bhava": 8},
            "ကြာသပတေး": {"sign": 9, "degree": 27, "minute": 15, "bhava": 10},
            "သောကြာ": {"sign": 11, "degree": 12, "minute": 30, "bhava": 12},
            "စနေ": {"sign": 1, "degree": 5, "minute": 18, "bhava": 2}
        }
        
        # နဝင်းအမှတ်များ (ဥပမာ)
        self.navamsa_positions = {
            "နေ": {"navamsa": 3, "strength": "အားကောင်း"},
            "လ": {"navamsa": 7, "strength": "အားပျော့"},
            "အင်္ဂါ": {"navamsa": 1, "strength": "အားကောင်း"},
            "ဗုဒ္ဓဟူး": {"navamsa": 9, "strength": "အားပျော့"},
            "ကြာသပတေး": {"navamsa": 5, "strength": "အားကောင်း"},
            "သောကြာ": {"navamsa": 11, "strength": "အားကောင်း"},
            "စနေ": {"navamsa": 8, "strength": "အားပျော့"}
        }
        
        # မဟာဘောဂများ (ဥပမာ)
        self.mahabhagas = [
            {"name": "ဂုရုမဟာဘောဂ", "planets": ["ကြာသပတေး", "သောကြာ"], "type": "ကောင်း"},
            {"name": "စန္ဒီမဟာဘောဂ", "planets": ["လ", "ဗုဒ္ဓဟူး"], "type": "ကောင်း"},
            {"name": "မင်းမဟာဘောဂ", "planets": ["နေ", "အင်္ဂါ"], "type": "ဆိုး"}
        ]
        
        # ဇာတာပုံဆွဲမယ်
        self.draw_chart()
        
        # အချက်အလက်များထည့်ရန် frame
        self.create_input_frame()
        
        # ဇာတာအကျဉ်းချုပ်ကိုပြရန် frame
        self.create_summary_frame()
    
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="ဇာတာအချက်အလက်များ", padding=10)
        input_frame.pack(pady=10, fill=tk.X, padx=20)
        
        # မွေးသက္ကရာဇ်
        ttk.Label(input_frame, text="မွေးသက္ကရာဇ် (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, "1990-01-01")
        
        # မွေးချိန်
        ttk.Label(input_frame, text="မွေးချိန် (HH:MM):").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.time_entry = ttk.Entry(input_frame, width=10)
        self.time_entry.grid(row=0, column=3, padx=5, pady=5)
        self.time_entry.insert(0, "12:00")
        
        # တည်နေရာ
        ttk.Label(input_frame, text="တည်နေရာ:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.location_entry = ttk.Entry(input_frame, width=20)
        self.location_entry.grid(row=1, column=1, padx=5, pady=5)
        self.location_entry.insert(0, "ရန်ကုန်")
        
        # နာမည်
        ttk.Label(input_frame, text="နာမည်:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(input_frame, width=15)
        self.name_entry.grid(row=1, column=3, padx=5, pady=5)
        self.name_entry.insert(0, "မောင်မောင်")
        
        # ဇာတာပုံတင်မယ့် button
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        calculate_btn = ttk.Button(button_frame, text="ဇာတာပုံတင်မည်", command=self.calculate_chart)
        calculate_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = ttk.Button(button_frame, text="ပုံသိမ်းမည်", command=self.save_chart)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        print_btn = ttk.Button(button_frame, text="ပုံထုတ်မည်", command=self.print_chart)
        print_btn.pack(side=tk.LEFT, padx=5)
    
    def create_summary_frame(self):
        summary_frame = ttk.LabelFrame(self.root, text="ဇာတာအကျဉ်းချုပ်", padding=10)
        summary_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        
        # ဇာတာအကျဉ်းချုပ်ကိုပြရန် text widget
        self.summary_text = tk.Text(summary_frame, height=8, width=80, wrap=tk.WORD, font=("Myanmar Text", 10))
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL, command=self.summary_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_text.config(yscrollcommand=scrollbar.set)
        
        # ဇာတာအကျဉ်းချုပ်ကိုဖြည့်မယ်
        self.update_summary()
    
    def draw_chart(self):
        # အရှေ့ကိုရှင်းလင်းပါ
        self.canvas.delete("all")
        
        # ဇာတာပုံအလယ်ဗဟို
        center_x, center_y = 400, 400
        radius = 300
        
        # နောက်ခံအရောင်
        self.canvas.create_rectangle(0, 0, 800, 800, fill="#FFF8DC", outline="")
        
        # အပြင်ဘက်စကွာကွဲဆွဲမယ်
        self.canvas.create_oval(center_x-radius, center_y-radius, 
                               center_x+radius, center_y+radius, 
                               outline="#8B4513", width=3)
        
        # ၁၂ ရာသီအတွက်အပိုင်းလေးများဆွဲမယ်
        for i in range(12):
            # ရာသီတစ်ခုစီရဲ့ထောင့်ကိုတွက်ချက်
            angle1 = i * 30
            angle2 = (i + 1) * 30
            
            # ရာသီအပိုင်းလေးဆွဲမယ်
            self.draw_zodiac_section(center_x, center_y, radius, angle1, angle2, i)
        
        # ဘာဝများကိုဆွဲမယ်
        self.draw_bhavas(center_x, center_y, radius)
        
        # ဗဟိုမှာစကွာကွဲဆွဲမယ်
        self.draw_center_info(center_x, center_y)
        
        # ဂြိုဟ်များထည့်မယ်
        self.draw_planets(center_x, center_y, radius)
        
        # မဟာဘောဂများကိုဆွဲမယ်
        self.draw_mahabhagas(center_x, center_y, radius)
        
        # နဝင်းအမှတ်များကိုဆွဲမယ်
        self.draw_navamsa_info(center_x, center_y, radius)
    
    def draw_zodiac_section(self, cx, cy, radius, angle1, angle2, index):
        # ရာသီအပိုင်းလေးဆွဲမယ်
        angle1_rad = math.radians(angle1)
        angle2_rad = math.radians(angle2)
        
        # အပြင်ဘက်အနားလေးဆွဲမယ်
        x1 = cx + radius * math.cos(angle1_rad)
        y1 = cy - radius * math.sin(angle1_rad)
        x2 = cx + radius * math.cos(angle2_rad)
        y2 = cy - radius * math.sin(angle2_rad)
        
        # အတွင်းဘက်အနားလေးဆွဲမယ်
        inner_radius = radius * 0.6
        x3 = cx + inner_radius * math.cos(angle1_rad)
        y3 = cy - inner_radius * math.sin(angle1_rad)
        x4 = cx + inner_radius * math.cos(angle2_rad)
        y4 = cy - inner_radius * math.sin(angle2_rad)
        
        # အပိုင်းလေးဆွဲမယ်
        self.canvas.create_polygon(x1, y1, x2, y2, x4, y4, x3, y3, 
                                   outline="#8B4513", fill="", width=2)
        
        # ရာသီနာမည်ထည့်မယ်
        mid_angle = math.radians((angle1 + angle2) / 2)
        text_radius = radius * 0.85
        text_x = cx + text_radius * math.cos(mid_angle)
        text_y = cy - text_radius * math.sin(mid_angle)
        
        # ရာသီနံပါတ်
        self.canvas.create_text(text_x, text_y-15, text=f"{index+1}", 
                               font=("Myanmar Text", 12, "bold"), fill="#8B4513")
        
        # ရာသီအမည်
        self.canvas.create_text(text_x, text_y, text=self.zodiac_signs[index], 
                               font=("Myanmar Text", 14, "bold"), fill="#8B4513")
    
    def draw_bhavas(self, cx, cy, radius):
        # ဘာဝများကိုဆွဲမယ်
        inner_radius = radius * 0.6
        bhava_radius = radius * 0.4
        
        # ဘာဝစကွာ
        self.canvas.create_oval(cx-bhava_radius, cy-bhava_radius, 
                               cx+bhava_radius, cy+bhava_radius, 
                               outline="#8B4513", width=2)
        
        # ဘာဝများကိုပြမယ်
        for i in range(12):
            angle = i * 30
            angle_rad = math.radians(angle)
            
            # ဘာဝအမှတ်
            text_radius = bhava_radius * 0.8
            text_x = cx + text_radius * math.cos(angle_rad)
            text_y = cy - text_radius * math.sin(angle_rad)
            
            self.canvas.create_text(text_x, text_y, text=f"{i+1}", 
                                   font=("Myanmar Text", 12, "bold"), fill="#8B4513")
            
            # ဘာဝအမည် (အချို့ကိုသာပြမယ်)
            if i % 3 == 0:  # 1, 4, 7, 10 ဘာဝများကိုသာပြမယ်
                name_radius = bhava_radius * 0.6
                name_x = cx + name_radius * math.cos(angle_rad)
                name_y = cy - name_radius * math.sin(angle_rad)
                
                self.canvas.create_text(name_x, name_y, text=self.bhavas[i], 
                                       font=("Myanmar Text", 10), fill="#8B4513")
    
    def draw_center_info(self, cx, cy):
        # ဗဟိုမှာစကွာကွဲဆွဲမယ်
        inner_radius = 120
        
        # အတွင်းစကွာ
        self.canvas.create_oval(cx-inner_radius, cy-inner_radius, 
                               cx+inner_radius, cy+inner_radius, 
                               outline="#8B4513", width=2, fill="#FFF8DC")
        
        # စနစ်အမည်ပြမယ်
        self.canvas.create_text(cx, cy-40, text="မြန်မာဇာတာ", 
                               font=("Myanmar Text", 16, "bold"), fill="#8B4513")
        self.canvas.create_text(cx, cy-20, text="MOTAA V2.0", 
                               font=("Arial", 12, "bold"), fill="#8B4513")
        self.canvas.create_text(cx, cy, text="Sidereal", 
                               font=("Arial", 10), fill="#8B4513")
        self.canvas.create_text(cx, cy+20, text="Vehlow_Equal", 
                               font=("Arial", 10), fill="#8B4513")
        
        # နေ့စွဲချိန်
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M")
        self.canvas.create_text(cx, cy+40, text=date_str, 
                               font=("Arial", 10), fill="#8B4513")
    
    def draw_planets(self, cx, cy, radius):
        # ဂြိုဟ်တွေကိုပြမယ်
        for planet_name, planet_data in self.planet_positions.items():
            # ဂြိုဟ်ရဲ့တည်နေရာကိုတွက်ချက်
            sign = planet_data["sign"]
            degree = planet_data["degree"]
            minute = planet_data["minute"]
            bhava = planet_data["bhava"]
            
            # ရာသီအတွင်းမှာဂြိုဟ်ရဲ့တည်နေရာ
            angle1 = sign * 30
            planet_angle = angle1 + (degree + minute/60) * 30/30
            planet_angle_rad = math.radians(planet_angle)
            
            planet_radius = radius * 0.75
            planet_x = cx + planet_radius * math.cos(planet_angle_rad)
            planet_y = cy - planet_radius * math.sin(planet_angle_rad)
            
            # ဂြိုဟ်ရဲ့အရောင်
            planet_color = self.planets[planet_name]["color"]
            
            # ဂြိုဟ်ရဲ့သင်္ကေတ
            planet_symbol = self.planets[planet_name]["symbol"]
            
            # ဂြိုဟ်သင်္ကေတကိုဆွဲမယ်
            self.canvas.create_oval(planet_x-15, planet_y-15, planet_x+15, planet_y+15, 
                                   fill=planet_color, outline="#8B4513", width=2)
            
            # ဂြိုဟ်သင်္ကေတ
            self.canvas.create_text(planet_x, planet_y, text=planet_symbol, 
                                   font=("Arial", 14, "bold"), fill="black")
            
            # ဂြိုဟ်နာမည်နဲ့ဒီဂရီပြမယ်
            planet_text = f"{planet_name} {degree}°{minute}'"
            self.canvas.create_text(planet_x, planet_y+25, text=planet_text, 
                                   font=("Myanmar Text", 10), fill="#8B4513")
            
            # ဘာဝအမှတ်
            bhava_text = f"ဘာဝ {bhava}"
            self.canvas.create_text(planet_x, planet_y+40, text=bhava_text, 
                                   font=("Myanmar Text", 9), fill="#8B4513")
    
    def draw_mahabhagas(self, cx, cy, radius):
        # မဟာဘောဂများကိုဆွဲမယ်
        y_pos = 50
        
        for bhaga in self.mahabhagas:
            # မဟာဘောဂအမည်
            name_text = f"{bhaga['name']}: {', '.join(bhaga['planets'])}"
            
            # အရောင်ကိုရွေးမယ်
            if bhaga['type'] == 'ကောင်း':
                color = "#008000"
            else:
                color = "#FF0000"
            
            # မဟာဘောဂကိုပြမယ်
            self.canvas.create_text(400, y_pos, text=name_text, 
                                   font=("Myanmar Text", 12, "bold"), fill=color)
            
            y_pos += 25
    
    def draw_navamsa_info(self, cx, cy, radius):
        # နဝင်းအမှတ်များကိုဆွဲမယ်
        x_pos = 50
        y_pos = 700
        
        self.canvas.create_text(x_pos, y_pos, text="နဝင်းအမှတ်များ:", 
                               font=("Myanmar Text", 12, "bold"), fill="#8B4513", anchor=tk.W)
        
        y_pos += 25
        for planet_name, navamsa_data in self.navamsa_positions.items():
            navamsa_text = f"{planet_name}: နဝင်း {navamsa_data['navamsa']} ({navamsa_data['strength']})"
            
            # အားအလိုက်အရောင်ခွဲခြား
            if navamsa_data['strength'] == 'အားကောင်း':
                color = "#008000"
            else:
                color = "#FF0000"
            
            self.canvas.create_text(x_pos, y_pos, text=navamsa_text, 
                                   font=("Myanmar Text", 10), fill=color, anchor=tk.W)
            y_pos += 20
    
    def calculate_chart(self):
        # ဒီနေရာမှာ မွေးသက္ကရာဇ်၊ မွေးချိန်၊ တည်နေရာအရ ဂြိုဟ်တွေရဲ့တည်နေရာကိုတွက်ချက်ရမယ်
        # အခုဒီ code မှာတော့ ဥပမာအနေနဲ့သာထားပါတယ်
        
        # အချက်အလက်ယူမယ်
        birth_date = self.date_entry.get()
        birth_time = self.time_entry.get()
        location = self.location_entry.get()
        name = self.name_entry.get()
        
        # ဒီမှာတကယ့်ဂြိုဟ်တွေရဲ့တည်နေရာကိုတွက်ချက်တဲ့ code ထည့်ရမယ်
        # ဥပမာအနေနဲ့ PyEphem သို့မဟုတ် Swiss Ephemeris ကိုသုံးနိုင်ပါတယ်
        
        # တွက်ချက်ပြီးရင် chart ပြန်ဆွဲမယ်
        self.draw_chart()
        
        # ဇာတာအကျဉ်းချုပ်ကိုပြန်ဖြည့်မယ်
        self.update_summary(name, birth_date, birth_time, location)
        
        messagebox.showinfo("ဇာတာပုံ", "ဇာတာပုံတင်ပြီးပါပြီ")
    
    def update_summary(self, name="မောင်မောင်", birth_date="1990-01-01", birth_time="12:00", location="ရန်ကုန်"):
        # ဇာတာအကျဉ်းချုပ်ကိုဖြည့်မယ်
        self.summary_text.delete(1.0, tk.END)
        
        summary = f"နာမည်: {name}\n"
        summary += f"မွေးသက္ကရာဇ်: {birth_date}\n"
        summary += f"မွေးချိန်: {birth_time}\n"
        summary += f"တည်နေရာ: {location}\n\n"
        
        summary += "ဂြိုဟ်တွေရဲ့တည်နေရာ:\n"
        for planet_name, pos in self.planet_positions.items():
            summary += f"  {planet_name}: {self.zodiac_signs[pos['sign']]} {pos['degree']}°{pos['minute']}' (ဘာဝ {pos['bhava']})\n"
        
        summary += "\nမဟာဘောဂများ:\n"
        for bhaga in self.mahabhagas:
            summary += f"  {bhaga['name']}: {', '.join(bhaga['planets'])} ({bhaga['type']})\n"
        
        summary += "\nနဝင်းအမှတ်များ:\n"
        for planet_name, navamsa_data in self.navamsa_positions.items():
            summary += f"  {planet_name}: နဝင်း {navamsa_data['navamsa']} ({navamsa_data['strength']})\n"
        
        self.summary_text.insert(tk.END, summary)
    
    def save_chart(self):
        # ဇာတာပုံကိုပုံအဖြစ်သိမ်းဆည်းမယ်
        try:
            # Canvas ကို PostScript အဖြစ်ပြောင်းမယ်
            ps = self.canvas.postscript(colormode='color')
            
            # ဖိုင်နာမည်
            filename = f"ဇာတာပုံ_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.ps"
            
            # သိမ်းဆည်းမယ်
            with open(filename, 'w') as f:
                f.write(ps)
            
            messagebox.showinfo("သိမ်းဆည်းခြင်း", f"ဇာတာပုံကို {filename} အဖြစ်သိမ်းဆည်းပြီးပါပြီ")
        except Exception as e:
            messagebox.showerror("အမှား", f"သိမ်းဆည်းရာမအောင်မြင်ပါ: {str(e)}")
    
    def print_chart(self):
        # ဇာတာပုံကိုပုံနှိပ်မယ်
        try:
            # Canvas ကို PostScript အဖြစ်ပြောင်းမယ်
            ps = self.canvas.postscript(colormode='color')
            
            # ပုံနှိပ်မယ်
            import subprocess
            subprocess.Popen(['lpr'], stdin=subprocess.PIPE).communicate(ps.encode())
            
            messagebox.showinfo("ပုံနှိပ်ခြင်း", "ဇာတာပုံကိုပုံနှိပ်ပြီးပါပြီ")
        except Exception as e:
            messagebox.showerror("အမှား", f"ပုံနှိပ်ရာမအောင်မြင်ပါ: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyanmarAstrologyApp(root)
    root.mainloop()