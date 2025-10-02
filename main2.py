import tkinter as tk
from tkinter import ttk
import swisseph as swe
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Setup Swiss Ephemeris
swe.set_ephe_path('./ephe')
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Burmese Rāśi names
rasi_names_mm = [
    "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်",
    "သိဟ်", "ကန်", "တူ", "ဗြိစ္ဆာ",
    "ဓနု", "မကာရ", "ကုမ်", "မိန်"
]

def convert_to_rasi(degree):
    rasi_index = int(degree // 30)
    rasi_name = rasi_names_mm[rasi_index]
    rasi_deg = degree % 30
    deg = int(rasi_deg)
    min_float = (rasi_deg - deg) * 60
    minute = int(min_float)
    second = int((min_float - minute) * 60)
    return rasi_name, deg, minute, second

def calculate_chart():
    year, month, day = 1937, 6, 15
    hour, minute = 23, 0
    tz_offset = -6.5
    lat, lon = 33.916, -102.3167

    ut = hour + minute / 60.0
    jd = swe.julday(year, month, day, ut - tz_offset)

    planets = {
        "၁": swe.SUN,
        "၂": swe.MOON,
        "၃": swe.MARS,
        "၄": swe.MERCURY,
        "၅": swe.JUPITER,
        "၆": swe.VENUS,
        "၀": swe.SATURN,
        "U": swe.URANUS,
        "N": swe.NEPTUNE,
        "P": swe.PLUTO,
        "၈": swe.MEAN_NODE
    }

    output.delete(1.0, tk.END)
    output.insert(tk.END, "📍 ဂြိုဟ်ရာသီ:\n")
    planet_positions = []

    for name, pid in planets.items():
        pos, _ = swe.calc(jd, pid)
        lon = pos[0] % 360
        rasi, deg, minute, second = convert_to_rasi(lon)
        output.insert(tk.END, f"{name}: {rasi} {deg}° {minute}′ {second}″\n")
        planet_positions.append((name, lon))

    # Ketu
    rahu_lon = planet_positions[-1][1]
    ketu_lon = (rahu_lon + 180) % 360
    rasi, deg, minute, second = convert_to_rasi(ketu_lon)
    output.insert(tk.END, f"ကိတ်: {rasi} {deg}° {minute}′ {second}″\n")

    # Chart
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_title("ရာသီ Wheel", fontsize=14)

    for i in range(12):
        angle = i * 30
        x = 1 * swe.dcos(angle)
        y = 1 * swe.dsin(angle)
        ax.text(x, y, rasi_names_mm[i], ha='center', va='center', fontsize=12)

    for name, lon in planet_positions:
        angle = lon
        x = 0.8 * swe.dcos(angle)
        y = 0.8 * swe.dsin(angle)
        ax.text(x, y, name, fontsize=10, color='blue')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# GUI Window
window = tk.Tk()
window.title("မြန်မာဇာတာ")
window.geometry("600x700")

ttk.Label(window, text="မြန်မာဇာတာဖွဲ့ခြင်း", font=("Myanmar Text", 16)).pack(pady=10)
ttk.Button(window, text="တွက်မယ်", command=calculate_chart).pack(pady=5)

def get_navamsa_rasi(degree):
    rasi_index = int(degree // 30)
    within_rasi = degree % 30
    navamsa_index = int(within_rasi // (30 / 9))

    # Movable signs start from same sign
    # Fixed signs start from 9th sign
    # Dual signs start from 5th sign
    start_map = [0, 8, 4]  # Aries, Taurus, Gemini → Movable, Fixed, Dual
    sign_type = rasi_index % 3
    start = (rasi_index + start_map[sign_type]) % 12
    navamsa_rasi = (start + navamsa_index) % 12

    return rasi_names_mm[navamsa_rasi]

output = tk.Text(window, height=15, font=("Myanmar Text", 12))
output.pack(pady=10)

window.mainloop()