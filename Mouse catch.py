import tkinter as tk

# ဝင်းဒိုးဖန်တီးပါမယ်
toplevel = tk.Tk()
toplevel.title("Mouse Click Tracker with Dots")
toplevel.geometry("800x600")
toplevel.resizable(True, True)

# Canvas ကို အသုံးပြုပါမယ် (အစက်တွေချဖို့)
canvas = tk.Canvas(toplevel, bg="white", width=800, height=600)
canvas.pack(fill="both", expand=True)

# နှိပ်ထားတဲ့အမှတ်တွေကို သိမ်းဖို့ list
dots = []

# မောက်စ်နှိပ်တဲ့အခါ အစက်နဲ့ တန်ဖိုးပြပေးမယ်
def on_click(event):
    # Screen ပေါ်က absolute position (လိုချင်တာဆိုရင်)
    abs_x = toplevel.winfo_pointerx()
    abs_y = toplevel.winfo_pointery()
    
    # ဒါမှမဟုတ် window အတွင်းက relative position ကိုသုံးချင်ရင်
    # abs_x, abs_y = event.x, event.y
    
    # အစက်လေးကို canvas ပေါ်မှာ ဆွဲပါမယ် (အရွယ် 6x6)
    dot = canvas.create_oval(
        event.x - 3, event.y - 3, event.x + 3, event.y + 3,
        fill='red', outline='darkred', width=1
    )
    
    # X,Y စာကို အစက်ဘေးမှာ ပြပါမယ်
    text = canvas.create_text(
        event.x + 10, event.y,
        text=f"({abs_x}, {abs_y})",
        font=("Pyidaungsu", 10), anchor="w", fill="blue"
    )
    
    # နောက်ပိုင်းမှာ ဖျက်ဖို့လွယ်အောင် သိမ်းပါမယ်
    dots.append((dot, text))

# မောက်စ်နှိပ်ခြင်းကို ဖမ်းပါမယ်
canvas.bind("<Button-1>", on_click)

# အစက်တွေအားလုံးကို ဖျက်ဖို့ function (optional)
def clear_all():
    for dot, text in dots:
        canvas.delete(dot)
        canvas.delete(text)
    dots.clear()

# Clear ခလုတ်လေးထည့်ပေးပါမယ်
clear_btn = tk.Button(toplevel, text="Clear All", command=clear_all, bg="red", fg="white")
clear_btn.window = canvas.create_window(10, 10, anchor="nw", window=clear_btn)