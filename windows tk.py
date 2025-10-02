import tkinter as tk

def toggle_fullscreen(event=None):
    current_state = toplevel.attributes('-fullscreen')
    toplevel.attributes('-fullscreen', not current_state)
    return "break"

toplevel = tk.Tk()
toplevel.title("Fullscreen Toggle")

# F11 key ဖြင့် fullscreen ပြောင်းလဲခြင်း
#toplevel.bind('<F11>', toggle_fullscreen)
toplevel.state('zoomed')  # Start in maximized windowed mode

# Escape key ဖြင့် fullscreen မှ ထွက်ခြင်း
toplevel.bind('<Escape>', lambda e: toplevel.attributes('-fullscreen', False))

toplevel.mainloop()