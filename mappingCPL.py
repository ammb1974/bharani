import tkinter as tk
from tkinter import messagebox

class MarkerApp:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("Area Marker Application")
        self.toplevel.geometry("800x600")
        
        # သတ်မှတ်ထားသော area များ (x, y, width, height)
        self.areas = [
            (100, 100, 200, 150),  # area 1
            (400, 200, 150, 200),  # area 2
            (200, 400, 250, 100)   # area 3
        ]
        
        # အမှတ်စက်များကို သိမ်းဆည်းရန် list
        self.markers = []
        
        # Canvas ဖန်တီးခြင်း
        self.canvas = tk.Canvas(toplevel, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Area များကို စတုဂံအဖြစ် ရေးဆွဲခြင်း
        for area in self.areas:
            x, y, w, h = area
            self.canvas.create_rectangle(x, y, x+w, y+h, outline="blue", dash=(4, 4), tags="area")
        
        # ကလစ်လုပ်လျှင် အမှတ်စက်ထည့်ရန် bind လုပ်ခြင်း
        self.canvas.bind("<Button-1>", self.add_marker)
        
        # ဖျက်နိုင်ရန် button
        self.clear_btn = tk.Button(toplevel, text="Markers များ ဖျက်ရန်", command=self.clear_markers)
        self.clear_btn.pack(pady=10)
        
        # ညွှန်ပြချက် label
        self.label = tk.Label(toplevel, text="Area များအတွင်း ကလစ်လုပ်ပါ (သို့) Marker များကို ဖျက်ပါ")
        self.label.pack(pady=5)
    
    def add_marker(self, event):
        # ကလစ်လုပ်သည့် နေရာသည် area အတွင်းရှိမရှိ စစ်ဆေးခြင်း
        for area in self.areas:
            x, y, w, h = area
            if x <= event.x <= x + w and y <= event.y <= y + h:
                # အမှတ်စက်ထည့်ခြင်း (အနီရောင် ဝိုင်းငယ်)
                marker = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, 
                                               fill="red", outline="darkred")
                self.markers.append(marker)
                
                # Marker အကြောင်း အချက်အလက် ပြသခြင်း
                info = f"Marker at ({event.x}, {event.y}) in area {self.areas.index(area)+1}"
                self.label.config(text=info)
                return
        
        # Area အတွင်းမဟုတ်လျှင်
        self.label.config(text="Area အတွင်းသို့ ကလစ်လုပ်ပါ")
    
    def clear_markers(self):
        # Marker အားလုံးကို ဖျက်ခြင်း
        for marker in self.markers:
            self.canvas.delete(marker)
        self.markers = []
        self.label.config(text="Marker များ ဖျက်ပြီးပါပြီ")

if __name__ == "__main__":
    toplevel = tk.Tk()
    app = MarkerApp(toplevel)
    toplevel.mainloop()