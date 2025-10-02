import tkinter as tk
from tkinter import font

toplevel = tk.Tk()
toplevel.title("မြန်မာစာ စမ်းသပ်ခြင်း")

# မှန်ကန်သော font အမည်များ
myanmar_fonts = ["Noto Sans Myanmar", "Pyidaungsu", "TharLon", "Myanmar3", "Myanmar Text", "Masterpiece Uni Round","Myanmar Census"]

# စနစ်တွင်ရှိသော font များကို စစ်ဆေးခြင်း
available_fonts = [f for f in myanmar_fonts if f in font.families()]

if available_fonts:
    selected_font = available_fonts[0]
    myanmar_font = font.Font(family=selected_font, size=14)
    print(f"အသုံးပြုမည့် font: {selected_font}")
else:
    print("မြန်မာစာအတွက် font မရှိပါ။ font များကို install လုပ်ပါ။")
    myanmar_font = font.Font(size=14)
    # Default font အမည်ကို ပြသပါ
    print(f"Default font: {myanmar_font.actual()['family']}")

# Font ရွေးချယ်ရန် Listbox
font_list = tk.Listbox(toplevel, height=6, exportselection=False)
font_list.pack(pady=10, padx=20, fill=tk.X)

# Listbox တွင် font များထည့်ခြင်း
for f in available_fonts:
    font_list.insert(tk.END, f)

# Font ရွေးချယ်မှုကို ဖမ်းယူခြင်း
def on_font_select(event):
    selected_index = font_list.curselection()
    if selected_index:
        selected_font_name = font_list.get(selected_index)
        # ရွေးချယ်လိုက်သော font ကို အသုံးပြုခြင်း
        myanmar_font.config(family=selected_font_name)
        # စာလုံးပုံစ်ကို ပြောင်းလဲခြင်း
        label.config(font=myanmar_font)
        entry.config(font=myanmar_font)
        text.config(font=myanmar_font)
        print(f"Font ပြောင်းလဲပြီး: {selected_font_name}")

# Listbox တွင် event ချိတ်ဆက်ခြင်း
font_list.bind('<<ListboxSelect>>', on_font_select)

# Widget များကို ဖန်တီးခြင်း
label = tk.Label(toplevel, text="မြန်မာစာ:", font=myanmar_font)
label.pack(pady=10)

entry = tk.Entry(toplevel, font=myanmar_font)
entry.pack(pady=10, padx=20, fill=tk.X)

text = tk.Text(toplevel, font=myanmar_font, height=5)
text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

toplevel.mainloop()