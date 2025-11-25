import pyswisseph as swe
import tkinter as tk
from datetime import datetime
import math

# Burmese zodiac sign names
burmese_signs = [
    "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
    "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်",
]

planet_names = [
    ("Sun", "နေ"), ("Moon", "လ"), ("Mars", "အင်္ဂါ"),
    ("Mercury", "ဗုဒ္ဓဟူး"), ("Jupiter", "ကြာသပတေး"),
    ("Venus", "သောကြာ"), ("Saturn", "စနေ"),
    ("Rahu", "ရာဟု"), ("Ketu", "ကိတ်"),
]

# --- Planet Position Calculation (This part remains the same) ---
now = datetime.now()
jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)

planet_codes = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
    "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
}

planet_positions = {}
rahu_pos = None

for eng, mm in planet_names:
    if eng in planet_codes:
        pos = swe.calc_ut(jd, planet_codes[eng])[0][0]
        idx = int(pos // 30)
        planet_positions[mm] = idx
    elif eng == "Rahu":
        rahu_pos = swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_TRUEPOS)[0][0]
        idx = int(rahu_pos // 30)
        planet_positions[mm] = idx
    elif eng == "Ketu":
        if rahu_pos is not None:
            ketu_pos = (rahu_pos + 180) % 360
            idx = int(ketu_pos // 30)
            planet_positions[mm] = idx

# --- Canvas Drawing (Rewritten for the new grid design) ---
root = tk.Tk()
root.title("Burmese Astrology Chart (Grid)")

canvas_width = 500
canvas_height = 500
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# --- မောက်စ်အနေအထားပြဖို့ Label ---
coord_label = tk.Label(root, text="Mouse X: 0, Y: 0", font=('Arial', 10), bd=1, relief=tk.SUNKEN, anchor=tk.W)
coord_label.pack(fill=tk.X)

def show_coords(event):
    x, y = event.x, event.y
    coord_label.config(text=f"Mouse X: {x}, Y: {y}")

canvas.bind('<Motion>', show_coords)


# Define grid and margin
margin = 50
grid_size = 3
grid_left = margin
grid_top = margin
grid_right = canvas_width - margin
grid_bottom = canvas_height - margin
cell_width = (grid_right - grid_left) / grid_size
cell_height = (grid_bottom - grid_top) / grid_size

# 1. Draw the outer square frame
canvas.create_rectangle(grid_left, grid_top, grid_right, grid_bottom, outline="#888888", width=8)

# 2. Draw the grid lines (vertical and horizontal)
for i in range(1, grid_size):
    # Vertical lines
    x = grid_left + i * cell_width
    canvas.create_line(x, grid_top, x, grid_bottom, fill='#888888',width=2)
    # Horizontal lines
    y = grid_top + i * cell_height
    canvas.create_line(grid_left, y, grid_right, y, fill='#888888',width=2)

# 3. Draw the center text
center_x, center_y = canvas_width / 2, canvas_height / 2
canvas.create_text(center_x, center_y, text="ရာသီ", font=('Arial', 18, 'bold'))

# 4. Draw ONLY the specific diagonals requested by the user
# အရင်ကလို အလိုလိုမဆွဲတော့ဘဲ သတ်မှတ်ထားတဲ့ အမှတ်တွေမှာပဲ ဆွဲပေးလိုက်တာဖြစ်ပါတယ်။
canvas.create_line(50, 50, 183, 183, fill="#5D5C5C",width=2)
canvas.create_line(318, 183, 450, 50, fill='#5D5C5C',width=2)
canvas.create_line(183, 318, 50, 450, fill='#5D5C5C',width=2)
canvas.create_line(318, 318, 450, 450, fill='#5D5C5C',width=2)


# 5. Draw the zodiac signs around the perimeter
sign_radius = (canvas_width / 2) - margin - 20
for i, sign in enumerate(burmese_signs):
    angle_deg = (i / 12) * 360 - 90
    angle_rad = math.radians(angle_deg)
    x = center_x + sign_radius * math.cos(angle_rad)
    y = center_y + sign_radius * math.sin(angle_rad)
    canvas.create_text(x, y, text=sign, font=('Myanmar Text', 14, 'bold'))

# 6. Draw the planets inside the 8 outer grid cells
cell_centers = []
for row in range(grid_size):
    for col in range(grid_size):
        if not (row == 1 and col == 1): # Avoid the center cell
            cx = grid_left + col * cell_width + cell_width / 2
            cy = grid_top + row * cell_height + cell_height / 2
            cell_centers.append((cx, cy))

planets_to_place = list(planet_positions.keys())
for i, planet_name in enumerate(planets_to_place):
    if i < len(cell_centers):
        x, y = cell_centers[i]
        canvas.create_text(x, y, text=planet_name, font=('Myanmar Text', 12), fill='blue')

root.mainloop()