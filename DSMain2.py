import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from  DCharter import BurmeseGrid

plt.rcParams['font.family'] = 'Myanmar Text'  # For Windows; use 'Noto Sans Myanmar' on Linux/macOS


# ၁၂ ရာသီ
signs = ["မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
         "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"]



# ဂြိုဟ် data example
planets = [
    {"symbol": "၁", "sign": "မိန်", "deg": 10, "min": 15, "sec": 0, "retro": False},  # Sun
    {"symbol": "၂", "sign": "မိန်", "deg": 10, "min": 15, "sec": 0, "retro": False},  # Moon
    {"symbol": "၃", "sign": "မိဿ", "deg": 28, "min": 57, "sec": 0, "retro": False},  # Mမျေ
    {"symbol": "၄", "sign": "မိန်", "deg": 28, "min": 57, "sec": 0, "retro": False},  # Mercury
    {"symbol": "၆", "sign": "မိန်", "deg": 10, "min": 50, "sec": 0, "retro": False},  # Venus
    {"symbol": "၈", "sign": "မိန်", "deg": 27, "min": 24, "sec": 0, "retro": True},   # Rahu
    {"symbol": "၀", "sign": "မိန်", "deg": 21, "min": 2, "sec": 0, "retro": True}     # Saturn
]

def draw_burmese_grid():
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    # Circle layout
    angles = np.linspace(0, 2*np.pi, 12, endpoint=False)[::-1]  # Anticlockwise
    radius = 1

    for i, (angle, sign) in enumerate(zip(angles, signs)):
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        ax.text(x, y, sign, ha='center', va='center', fontsize=12, bbox=dict(boxstyle="circle", facecolor="lightyellow"))

    # Planet placement
    for planet in planets:
        idx = signs.index(planet["sign"])
        angle = angles[idx]
        r = 0.7  # inner radius for planet placement
        x = r * np.cos(angle)
        y = r * np.sin(angle)
        label = f"{planet['symbol']}\n{planet['deg']}°{planet['min']}'{planet['sec']}\""
        ax.text(x, y, label, ha='center', va='center', fontsize=10, color='blue')

    return fig

# Tkinter UI
toplevel = tk.Tk()
toplevel.title("BurmeseGrid Astrology")


fig = draw_burmese_grid()
canvas = FigureCanvasTkAgg(fig, master=toplevel)
canvas.draw()
canvas.get_tk_widget().pack()

toplevel.mainloop()