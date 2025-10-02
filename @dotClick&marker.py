import tkinter as tk
import json
from datetime import datetime

CELL_SIZE = 50
CANVAS_SIZE = CELL_SIZE * 6

zodiac_signs = [
    "မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
    "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုမ်", "မိန်"
]

toplevel = tk.Tk()
toplevel.title("Planet Position Registration")

canvas = tk.Canvas(toplevel, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
canvas.pack()

# Create status label first
status_label = tk.Label(toplevel, text="Click twice in each zodiac region", font=("Myanmar Text", 12))
status_label.pack()

region_map = {}
planet_data = {}     # Store planet position data
click_counts = {}    # Track number of clicks per zodiac
dot_objects = {}     # Store canvas objects for dots

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

def register_region(name, points):
    region_map[name] = points
    # Initialize planet data for this zodiac
    planet_data[name] = []
    click_counts[name] = 0
    dot_objects[name] = []

# --- Define Regions ---
register_region("မိဿ", draw_square(canvas, 2 * CELL_SIZE, 0, "LightBlue", "မိဿ"))
register_region("ကရကဋ်", draw_square(canvas, 0, 2 * CELL_SIZE, "LightBlue", "ကရကဋ်"))
register_region("တူ", draw_square(canvas, 2 * CELL_SIZE, 4 * CELL_SIZE, "LightBlue", "တူ"))
register_region("မကာရ", draw_square(canvas, 4 * CELL_SIZE, 2 * CELL_SIZE, "LightBlue", "မကာရ"))
register_region("ပြိဿ", draw_triangle(canvas, [(0, 0), (2 * CELL_SIZE, 2 * CELL_SIZE), (2 * CELL_SIZE, 0)], "lightblue", "ပြိဿ"))
register_region("မေထုန်", draw_triangle(canvas, [(0, 0), (2 * CELL_SIZE, 2 * CELL_SIZE), (0, 2 * CELL_SIZE)], "lightblue", "မေထုန်"))
register_region("သိဟ်", draw_triangle(canvas, [(0, 4 * CELL_SIZE), (0, 6 * CELL_SIZE), (2 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "သိဟ်"))
register_region("ကန်", draw_triangle(canvas, [(0, 6 * CELL_SIZE), (2 * CELL_SIZE, 6 * CELL_SIZE), (2 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "ကန်"))
register_region("ဗြိစ္ဆာ", draw_triangle(canvas, [(4 * CELL_SIZE, 4 * CELL_SIZE), (6 * CELL_SIZE, 6 * CELL_SIZE), (4 * CELL_SIZE, 6 * CELL_SIZE)], "lightblue", "ဗြိစ္ဆာ"))
register_region("ဓနု", draw_triangle(canvas, [(4 * CELL_SIZE, 4 * CELL_SIZE), (6 * CELL_SIZE, 6 * CELL_SIZE), (6 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "ဓနု"))
register_region("ကုမ်", draw_triangle(canvas, [(6 * CELL_SIZE, 2 * CELL_SIZE), (4 * CELL_SIZE, 2 * CELL_SIZE), (6 * CELL_SIZE, 0)], "lightblue", "ကုမ်"))
register_region("မိန်", draw_triangle(canvas, [(4 * CELL_SIZE, 0), (4 * CELL_SIZE, 2 * CELL_SIZE), (6 * CELL_SIZE, 0)], "lightblue", "မိန်"))

def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def on_click(event):
    # Record current time
    click_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if click is in any zodiac region
    for sign, polygon in region_map.items():
        if point_in_polygon((event.x, event.y), polygon):
            # Check if we can record more clicks for this zodiac
            if click_counts[sign] < 2:
                # Record the click
                click_order = click_counts[sign] + 1
                click_counts[sign] += 1
                
                # Add to planet data
                planet_data[sign].append({
                    "order": click_order,
                    "x": event.x,
                    "y": event.y,
                    "timestamp": click_time
                })
                
                # Draw a dot at the click position
                dot = canvas.create_oval(
                    event.x - 5, event.y - 5, 
                    event.x + 5, event.y + 5, 
                    fill="red", outline="black"
                )
                dot_objects[sign].append(dot)
                
                # Save planet data to planetposition.json
                with open("planetposition.json", "w", encoding="utf-8") as f:
                    json.dump(planet_data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Click {click_order} recorded for {sign} at ({event.x}, {event.y})")
                
                # Update status
                total_clicks = sum(click_counts.values())
                status_text = f"Total clicks: {total_clicks}/24 | {sign}: {click_counts[sign]}/2"
                status_label.config(text=status_text)
                
                # If we have 2 clicks for this zodiac, show completion message
                if click_counts[sign] == 2:
                    print(f"✅ {sign} region complete (2/2 clicks)")
            else:
                print(f"❌ {sign} region already has 2 clicks")
            
            return  # Exit after processing the first valid region
    
    # If click is not in any region
    print(f"❌ Click at ({event.x}, {event.y}) is not in any zodiac region")

def load_planet_positions():
    try:
        with open("planetposition.json", "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        # Clear existing dots
        for sign in zodiac_signs:
            for dot in dot_objects[sign]:
                canvas.delete(dot)
            dot_objects[sign] = []
            click_counts[sign] = 0
        
        # Update planet_data with loaded data
        for sign, clicks in loaded_data.items():
            if sign in planet_data:
                planet_data[sign] = clicks
                click_counts[sign] = len(clicks)
                
                # Display each click as a dot on canvas
                for click in clicks:
                    dot = canvas.create_oval(
                        click["x"] - 5, click["y"] - 5, 
                        click["x"] + 5, click["y"] + 5, 
                        fill="red", outline="black"
                    )
                    dot_objects[sign].append(dot)
                    
        # Update status
        total_clicks = sum(click_counts.values())
        status_text = f"Loaded {total_clicks} saved positions. Total: {total_clicks}/24"
        status_label.config(text=status_text)
        print(f"✅ Loaded {total_clicks} saved positions from planetposition.json")
    except FileNotFoundError:
        status_label.config(text="No saved data found. Click twice in each zodiac region.")
        print("ℹ️ No existing planetposition.json file found.")
    except json.JSONDecodeError:
        status_label.config(text="Error reading saved data. Starting fresh.")
        print("⚠️ Error reading planetposition.json.")

# Add Open button
open_button = tk.Button(toplevel, text="Open Saved Positions", command=load_planet_positions)
open_button.pack()

# Add reset button
def reset_session():
    # Reset data
    for sign in zodiac_signs:
        planet_data[sign] = []
        click_counts[sign] = 0
        # Remove all dot objects for this sign
        for dot in dot_objects[sign]:
            canvas.delete(dot)
        dot_objects[sign] = []
    
    # Reset status
    status_label.config(text="Session reset. Click twice in each zodiac region.")
    
    # Clear file
    with open("planetposition.json", "w", encoding="utf-8") as f:
        json.dump(planet_data, f, ensure_ascii=False, indent=2)
    
    print("Session reset")

reset_button = tk.Button(toplevel, text="Reset Session", command=reset_session)
reset_button.pack()

# Bind click event
canvas.bind("<Button-1>", on_click)

toplevel.mainloop()