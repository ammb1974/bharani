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
region_items = {}   # Store canvas item IDs for regions
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
    rect = canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
    if label:
        canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=label, font=("Myanmar Text", 10), anchor="center")
    return rect, [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

def draw_triangle(canvas, points, color="lightblue", label=None):
    poly = canvas.create_polygon(points, outline="black", fill=color)
    if label:
        cx, cy = get_centroid(points)
        canvas.create_text(cx, cy, text=label, font=("Myanmar Text", 10), anchor="center")
    return poly, points

def register_region(name, points, item):
    region_map[name] = points
    region_items[name] = item
    # Initialize planet data for this zodiac
    planet_data[name] = []
    click_counts[name] = 0
    dot_objects[name] = []

# --- Define Regions ---
item, points = draw_square(canvas, 2 * CELL_SIZE, 0, "LightBlue", "မိဿ")
register_region("မိဿ", points, item)

item, points = draw_square(canvas, 0, 2 * CELL_SIZE, "LightBlue", "ကရကဋ်")
register_region("ကရကဋ်", points, item)

item, points = draw_square(canvas, 2 * CELL_SIZE, 4 * CELL_SIZE, "LightBlue", "တူ")
register_region("တူ", points, item)

item, points = draw_square(canvas, 4 * CELL_SIZE, 2 * CELL_SIZE, "LightBlue", "မကာရ")
register_region("မကာရ", points, item)

item, points = draw_triangle(canvas, [(0, 0), (2 * CELL_SIZE, 2 * CELL_SIZE), (2 * CELL_SIZE, 0)], "lightblue", "ပြိဿ")
register_region("ပြိဿ", points, item)

item, points = draw_triangle(canvas, [(0, 0), (2 * CELL_SIZE, 2 * CELL_SIZE), (0, 2 * CELL_SIZE)], "lightblue", "မေထုန်")
register_region("မေထုန်", points, item)

item, points = draw_triangle(canvas, [(0, 4 * CELL_SIZE), (0, 6 * CELL_SIZE), (2 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "သိဟ်")
register_region("သိဟ်", points, item)

item, points = draw_triangle(canvas, [(0, 6 * CELL_SIZE), (2 * CELL_SIZE, 6 * CELL_SIZE), (2 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "ကန်")
register_region("ကန်", points, item)

item, points = draw_triangle(canvas, [(4 * CELL_SIZE, 4 * CELL_SIZE), (6 * CELL_SIZE, 6 * CELL_SIZE), (4 * CELL_SIZE, 6 * CELL_SIZE)], "lightblue", "ဗြိစ္ဆာ")
register_region("ဗြိစ္ဆာ", points, item)

item, points = draw_triangle(canvas, [(4 * CELL_SIZE, 4 * CELL_SIZE), (6 * CELL_SIZE, 6 * CELL_SIZE), (6 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "ဓနု")
register_region("ဓနု", points, item)

item, points = draw_triangle(canvas, [(6 * CELL_SIZE, 2 * CELL_SIZE), (4 * CELL_SIZE, 2 * CELL_SIZE), (6 * CELL_SIZE, 0)], "lightblue", "ကုမ်")
register_region("ကုမ်", points, item)

item, points = draw_triangle(canvas, [(4 * CELL_SIZE, 0), (4 * CELL_SIZE, 2 * CELL_SIZE), (6 * CELL_SIZE, 0)], "lightblue", "မိန်")
register_region("မိန်", points, item)

def on_click(event):
    # Record current time
    click_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Find which region was clicked
    clicked_sign = None
    overlapping = canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
    
    for item in overlapping:
        for sign, region_item in region_items.items():
            if item == region_item:
                clicked_sign = sign
                break
        if clicked_sign:
            break
    
    if clicked_sign:
        # Check if we can record more clicks for this zodiac
        if click_counts[clicked_sign] < 2:
            # Record the click
            click_order = click_counts[clicked_sign] + 1
            click_counts[clicked_sign] += 1
            
            # Add to planet data
            planet_data[clicked_sign].append({
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
            dot_objects[clicked_sign].append(dot)
            
            # Save planet data to planetposition.json
            with open("planetpositionV2.json", "w", encoding="utf-8") as f:
                json.dump(planet_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Click {click_order} recorded for {clicked_sign} at ({event.x}, {event.y})")
            
            # Update status
            total_clicks = sum(click_counts.values())
            status_text = f"Total clicks: {total_clicks}/24 | {clicked_sign}: {click_counts[clicked_sign]}/2"
            status_label.config(text=status_text)
            
            # If we have 2 clicks for this zodiac, show completion message
            if click_counts[clicked_sign] == 2:
                print(f"✅ {clicked_sign} region complete (2/2 clicks)")
        else:
            print(f"❌ {clicked_sign} region already has 2 clicks")
    else:
        # If click is not in any region
        print(f"❌ Click at ({event.x}, {event.y}) is not in any zodiac region")
        status_label.config(text=f"Click not in any region. Try again. Total: {sum(click_counts.values())}/24")

def load_planet_positions():
    try:
        with open("planetpositionV2.json", "r", encoding="utf-8") as f:
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
        print(f"✅ Loaded {total_clicks} saved positions from planetpositionV2.json")
    except FileNotFoundError:
        status_label.config(text="No saved data found. Click twice in each zodiac region.")
        print("ℹ️ No existing planetpositionV2.json file found.")
    except json.JSONDecodeError:
        status_label.config(text="Error reading saved data. Starting fresh.")
        print("⚠️ Error reading planetpositionV2.json.")

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
    with open("planetpositionV2.json", "w", encoding="utf-8") as f:
        json.dump(planet_data, f, ensure_ascii=False, indent=2)
    
    print("Session reset")

reset_button = tk.Button(toplevel, text="Reset Session", command=reset_session)
reset_button.pack()

# Bind click event
canvas.bind("<Button-1>", on_click)

toplevel.mainloop()