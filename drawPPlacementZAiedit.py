import tkinter as tk
import random
# --- Config ---
CELL_SIZE = 50
CANVAS_SIZE = CELL_SIZE * 6
zodiac_signs = [
    "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
    "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
]
# --- Planet Degrees (Sample)
planet_degrees = {
    "လ": 110.695277777778,
    "၁": 100.486912833333,
    "၂": 26.5020220833333,
    "၃": 63.196193833333,
    "၅": 126.123213972222,
    "၆": 96.3435823333333,
    "၀": 3.49313661111111,
    "၈": 7.268938444444,
    "၉": 188.268938444444,
    "U": 44.7123589722222,
    "N": 342.327093833333,
    "P": 41.743067666667
}
# --- Utilities ---
def deg_to_dms(degree):
    d = int(degree)
    m = int((degree - d) * 60)
    s = int(((degree - d) * 60 - m) * 60)
    return d, m, s
# ဒီကုဒ်က နဂို ကုဒ်ပါ။ သူက စက္ကန့်ထိ ပြပါတယ်. မလိုလို့ပြင်ထားပါတယ်
# def map_planet_to_sign(name, degree):
#     index = int(degree // 30) % 12
#     sign = zodiac_signs[index]
#     offset = degree % 30
#     d, m, s = deg_to_dms(offset)
#     return {
#         "planet": name,
#         "sign": sign,
#         "offset": f"{d}° {m}' {s}\"",
#         "mm_offset": f"{d} ဒီဂရီ {m} အံသာ {s} လိတ္တာ",
#         "degree": degree
#     }

def map_planet_to_sign(name, degree):
    index = int(degree // 30) % 12
    sign = zodiac_signs[index]
    offset = degree % 30
    d, m, s = deg_to_dms(offset)
    return {
        "planet": name,
        "sign": sign,
        "offset": f"{d}° {m}'\"",
        "mm_offset": f"{d} ဒီဂရီ {m} အံသာ ",
        "degree": degree
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


# Reigion mapဒီဇိုင်းပါ။ ၁၂ ရာသီအတွက် ၁၂ ကြောင်းရှိပါတယ်။ နောက်ဆုံး "",မိဿ "" ကို ဖြုတ်ထားတယ်
#region_map["ကရကဋ်"] = draw_square(canvas, 0, 2 * CELL_SIZE, "LightBlue", "ကရကဋ်")
# --- Region Definitions ---
region_map = {}
region_map["မိဿ"] = draw_square(canvas, 2 * CELL_SIZE, 0, "LightBlue")
region_map["ကရကဋ်"] = draw_square(canvas, 0, 2 * CELL_SIZE, "LightBlue", "")
region_map["တူ"] = draw_square(canvas, 2 * CELL_SIZE, 4 * CELL_SIZE, "LightBlue", "")
region_map["မကာရ"] = draw_square(canvas, 4 * CELL_SIZE, 2 * CELL_SIZE, "LightBlue", "")
region_map["ပြိဿ"] = draw_triangle(canvas, [(0, 0), (2 * CELL_SIZE, 2 * CELL_SIZE), (2 * CELL_SIZE, 0)], "lightblue", "")
region_map["မေထုန်"] = draw_triangle(canvas, [(0, 0), (2 * CELL_SIZE, 2 * CELL_SIZE), (0, 2 * CELL_SIZE)], "lightblue", "")
region_map["သိဟ်"] = draw_triangle(canvas, [(0, 4 * CELL_SIZE), (0, 6 * CELL_SIZE), (2 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "")
region_map["ကန်"] = draw_triangle(canvas, [(0, 6 * CELL_SIZE), (2 * CELL_SIZE, 6 * CELL_SIZE), (2 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "")
region_map["ဗြိစ္ဆာ"] = draw_triangle(canvas, [(4 * CELL_SIZE, 4 * CELL_SIZE), (6 * CELL_SIZE, 6 * CELL_SIZE), (4 * CELL_SIZE, 6 * CELL_SIZE)], "lightblue", "")
region_map["ဓနု"] = draw_triangle(canvas, [(4 * CELL_SIZE, 4 * CELL_SIZE), (6 * CELL_SIZE, 6 * CELL_SIZE), (6 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "")
region_map["ကုမ်"] = draw_triangle(canvas, [(6 * CELL_SIZE, 2 * CELL_SIZE), (4 * CELL_SIZE, 2 * CELL_SIZE), (6 * CELL_SIZE, 0)], "lightblue", "")
region_map["မိန်"] = draw_triangle(canvas, [(4 * CELL_SIZE, 0), (4 * CELL_SIZE, 2 * CELL_SIZE), (6 * CELL_SIZE, 0)], "lightblue", "")

# --- Center Label ---
center_x = CANVAS_SIZE // 2
center_y = CANVAS_SIZE // 2
canvas.create_text(center_x, center_y, text="ရာသီ", font=("Myanmar Text", 12), fill="black", anchor="center")

# --- Group planets by sign ---
planets_by_sign = {}
for name, deg in planet_degrees.items():
    result = map_planet_to_sign(name, deg)
    sign = result["sign"]
    
    if sign not in planets_by_sign:
        planets_by_sign[sign] = []
    
    planets_by_sign[sign].append(result)

# --- Planet Placement ---
for sign, planets in planets_by_sign.items():
    if sign in region_map:
        cx, cy = get_centroid(region_map[sign])
        
        # Sort planets by degree for consistent ordering
        planets.sort(key=lambda p: p["degree"])
        
        # Calculate vertical spacing based on number of planets
        num_planets = len(planets)
        if num_planets > 1:
            # Distribute planets vertically
            spacing = 15
            start_y = cy - ((num_planets - 1) * spacing) // 2
            
            for i, planet in enumerate(planets):
                y_pos = start_y + i * spacing
                # Display planet name with degree
                planet_text = f"{planet['planet']} ({planet['offset']})"
                canvas.create_text(cx, y_pos + 15, text=planet_text, font=("Myanmar Text", 9), fill="blue", anchor="center")
        else:
            # Single planet, display as before
            planet = planets[0]
            planet_text = f"{planet['planet']} ({planet['offset']})"
            canvas.create_text(cx, cy + 15, text=planet_text, font=("Myanmar Text", 9), fill="blue", anchor="center")

toplevel.mainloop()