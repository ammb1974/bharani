import tkinter as tk
import math

# မူလဝင်းဒိုးဖန်တီးခြင်း
toplevel = tk.Tk()
toplevel.title("မြန်မာ့ဗေဒင် ဇာတာအဝိုင်း")
toplevel.geometry("800x800")
toplevel.configure(bg="#f0f0f0")

# Canvas ဖန်တီးခြင်း
canvas = tk.Canvas(toplevel, width=700, height=700, bg="white", highlightthickness=0)
canvas.pack(padx=50, pady=50)

# စက်ဝိုင်းဗဟိုနှင့် အချင်း
center_x, center_y = 350, 350
radius = 300

# အပြင်ဘက်စက်ဝိုင်းဆွဲခြင်း
canvas.create_oval(
    center_x - radius, center_y - radius,
    center_x + radius, center_y + radius,
    outline="black", width=3
)

# အတွင်းစက်ဝိုင်းဆွဲခြင်း
inner_radius = radius - 40
canvas.create_oval(
    center_x - inner_radius, center_y - inner_radius,
    center_x + inner_radius, center_y + inner_radius,
    outline="gray", width=1, dash=(4, 2)
)

# ဗဟိုစာတန်း
canvas.create_text(
    center_x, center_y, text="ရာသီ",
    font=("Myanmar Text", 20, "bold"), fill="maroon"
)

# ၁၂ ရာသီအမည်များ
zodiac_signs = ["မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်", 
                "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုံ", "မိန်"]

# ရာသီများနှင့် ခွဲမျဉ်းများဆွဲခြင်း
for i in range(12):
    # ရာသီတစ်ခုစီအတွက် ထောင့်တွက်ချက်ခြင်း (ထိပ်မှစတင်)
    angle = math.radians(-90 + i * 30)
    
    # ရာသီအမည်ရေးရန် တည်နေရာ
    text_radius = radius - 50
    x = center_x + text_radius * math.cos(angle)
    y = center_y + text_radius * math.sin(angle)
    
    # ရာသီအမည်ရေးခြင်း
    canvas.create_text(
        x, y, text=zodiac_signs[i],
        font=("Myanmar Text", 14, "bold"), fill="navy"
    )
    
    # ရာသီခွဲမျဉ်းဆွဲခြင်း
    line_angle = math.radians(-90 + i * 30 - 15)
    line_start_x = center_x
    line_start_y = center_y
    line_end_x = center_x + (radius + 20) * math.cos(line_angle)
    line_end_y = center_y + (radius + 20) * math.sin(line_angle)
    
    canvas.create_line(
        line_start_x, line_start_y,
        line_end_x, line_end_y,
        fill="black", width=2
    )

# စက္ကန့်အမှတ်များဆွဲခြင်း (၁ စက္ကန့်စီ ပါးမျဉ်း)
for i in range(360):
    # စက္ကန့်တစ်ခုစီအတွက် ထောင့်တွက်ချက်ခြင်း
    angle = math.radians(-90 + i)
    
    # စက္ကန့်မျဉ်းအစပြုရာနေရာ
    start_x = center_x + radius * math.cos(angle)
    start_y = center_y + radius * math.sin(angle)
    
    # ၅ စက္ကန့်စီကို အထူးမျဉ်းအဖြစ်ဆွဲခြင်း
    if i % 5 == 0:
        end_x = center_x + (radius + 10) * math.cos(angle)
        end_y = center_y + (radius + 10) * math.sin(angle)
        canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill="red", width=3
        )
    # ၁ စက္ကန့်စီကို ပါးမျဉ်းအဖြစ်ဆွဲခြင်း
    else:
        end_x = center_x + (radius + 5) * math.cos(angle)
        end_y = center_y + (radius + 5) * math.sin(angle)
        canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill="blue", width=1
        )

# ခေါင်းစဉ်နှင့် ဖော်ပြချက်
title_label = tk.Label(
    toplevel, text="မြန်မာ့ဗေဒင် ဇာတာအဝိုင်း",
    font=("Myanmar Text", 18, "bold"), bg="#f0f0f0"
)
title_label.pack(pady=(0, 5))

desc_label = tk.Label(
    toplevel, text="စက္ကန့်အမှတ်များ - အနီရောင်: ၅ စက္ကန့်စီ, အပြာရောင်: ၁ စက္ကန့်စီ",
    font=("Myanmar Text", 12), bg="#f0f0f0"
)
desc_label.pack(pady=(0, 10))

# အပလီကေးရှင်းလည်ပတ်စေခြင်း
toplevel.mainloop()