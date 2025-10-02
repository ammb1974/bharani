import tkinter as tk
import json

# --- Config ---
CELL_SIZE = 50
CANVAS_SIZE = CELL_SIZE * 6
MAX_LINE_HEIGHT = 3  # Max planets per anchor before switching

zodiac_signs = [
    "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
    "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
]

planet_degrees = {
    "လ": 110.695, "၁": 100.486, "၂": 26.502, "၃": 63.196,
    "၄": 126.123, "၅": 96.343, "၀": 3.493, "၈": 7.268,
    "၉": 187.268, "U": 44.712, "N": 342.327, "P": 41.743
}

# --- Utilities ---
def deg_to_dms(degree):
    d = int(degree)
    m = int((degree - d) * 60)
    s = int(((degree - d) * 60 - m) * 60)
    return d, m, s

def map_planet_to_sign(name, degree):
    index = int(degree // 30) % 12
    sign = zodiac_signs[index]
    offset = degree % 30
    d, m, s = deg_to_dms(offset)
    return {
        "planet": name,
        "sign": sign,
        "offset": f"{d}° {m}' {s}\"",
        "mm_offset": f"{d} ဒီဂရီ {m} အံသာ {s} လိတ္တာ"
    }

def get_centroid(points):
    x = sum([pt[0] for pt in points]) / len(points)
    y = sum([pt[1] for pt in points]) / len(points)
    return int(x), int(y)

def draw_square(canvas, x1, y1, color="white", label=None):
    x2 = x1 + CELL_SIZE * 2
    y2 = y1 + CELL_SIZE * 2
    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
    if label:
        canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=label, font=("Myanmar Text", 10), anchor="center")
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

def draw_triangle(canvas, points, color="lightblue", label=None):
    canvas.create_polygon(points, outline="black", fill=color)
    if label:
        cx, cy = get_centroid(points)
        canvas.create_text(cx, cy, text=label, font=("Myanmar Text", 10), anchor="center")
    return points

# --- Main App ---
toplevel = tk.Tk()
toplevel.title("Astrology Chart with Planet Placement")
canvas = tk.Canvas(toplevel, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
canvas.pack()

region_map = {}
anchor_map = {}
anchor_usage = {}

# --- Region Definitions ---
def register_region(name, points):
    region_map[name] = points
    anchor_map[name] = []
    anchor_usage[name] = []

    # Define 3 anchor points per region (top, middle, bottom)
    cx, cy = get_centroid(points)
    anchor_map[name].append((cx, cy - 15))
    anchor_map[name].append((cx, cy))
    anchor_map[name].append((cx, cy + 15))
    anchor_usage[name] = [0, 0, 0]

# Squares
register_region("မိဿ", draw_square(canvas, 2 * CELL_SIZE, 0, "LightBlue", "မိဿ"))
register_region("ကရကဋ်", draw_square(canvas, 0, 2 * CELL_SIZE, "LightBlue", "ကရကဋ်"))
register_region("တူ", draw_square(canvas, 2 * CELL_SIZE, 4 * CELL_SIZE, "LightBlue", "တူ"))
register_region("မကာရ", draw_square(canvas, 4 * CELL_SIZE, 2 * CELL_SIZE, "LightBlue", "မကာရ"))

# Triangles
register_region("ပြိဿ", draw_triangle(canvas, [(0, 0), (2 * CELL_SIZE, 2 * CELL_SIZE), (2 * CELL_SIZE, 0)], "lightblue", "ပြိဿ"))
register_region("မေထုန်", draw_triangle(canvas, [(0, 0), (2 * CELL_SIZE, 2 * CELL_SIZE), (0, 2 * CELL_SIZE)], "lightblue", "မေထုန်"))
register_region("သိဟ်", draw_triangle(canvas, [(0, 4 * CELL_SIZE), (0, 6 * CELL_SIZE), (2 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "သိဟ်"))
register_region("ကန်", draw_triangle(canvas, [(0, 6 * CELL_SIZE), (2 * CELL_SIZE, 6 * CELL_SIZE), (2 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "ကန်"))
register_region("ဗြိစ္ဆာ", draw_triangle(canvas, [(4 * CELL_SIZE, 4 * CELL_SIZE), (6 * CELL_SIZE, 6 * CELL_SIZE), (4 * CELL_SIZE, 6 * CELL_SIZE)], "lightblue", "ဗြိစ္ဆာ"))
register_region("ဓနု", draw_triangle(canvas, [(4 * CELL_SIZE, 4 * CELL_SIZE), (6 * CELL_SIZE, 6 * CELL_SIZE), (6 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "ဓနု"))
register_region("ကုမ်", draw_triangle(canvas, [(6 * CELL_SIZE, 2 * CELL_SIZE), (4 * CELL_SIZE, 2 * CELL_SIZE), (6 * CELL_SIZE, 0)], "lightblue", "ကုမ်"))
register_region("မိန်", draw_triangle(canvas, [(4 * CELL_SIZE, 0), (4 * CELL_SIZE, 2 * CELL_SIZE), (6 * CELL_SIZE, 0)], "lightblue", "မိန်"))

# --- Center Label ---
canvas.create_text(CANVAS_SIZE // 2, CANVAS_SIZE // 2, text="ရာသီ", font=("Myanmar Text", 12), fill="black", anchor="center")

# --- Planet Placement ---
planet_positions = []

def place_planet(name, sign):
    anchors = anchor_map[sign]
    usage = anchor_usage[sign]
    for i, (x, y) in enumerate(anchors):
        if usage[i] < MAX_LINE_HEIGHT:
            canvas.create_text(x, y + usage[i] * 12, text=name, font=("Myanmar Text", 9), fill="blue", anchor="center")
            usage[i] += 1
            planet_positions.append({"planet": name, "sign": sign, "x": x, "y": y + usage[i] * 12})
            return
    # fallback: try next region clockwise
    next_index = (zodiac_signs.index(sign) + 1) % 12
    next_sign = zodiac_signs[next_index]
    place_planet(name, next_sign)

for name, deg in planet_degrees.items():
    result = map_planet_to_sign(name, deg)
    sign = result["sign"]
    if sign in anchor_map:
        place_planet(name, sign)

# --- Click to Save JSON ---
def on_click(event):
    for sign, points in region_map.items():
        if canvas.find_closest(event.x, event.y):
            with open("PositionPlanet.json", "w", encoding="utf-8") as f:
                json.dump(planet_positions, f, ensure_ascii=False, indent=2)
            print(f"Saved planet positions for {sign}")
            break

canvas.bind("<Button-1>", on_click)

toplevel.mainloop()