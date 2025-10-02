import tkinter as tk
import random

# --- Config ---
CELL_SIZE = 50
GRID_WIDTH = 6
#GRID_HEIGHT = 6
CANVAS_SIZE = CELL_SIZE * GRID_WIDTH

# --- Utilities ---
def get_random_hex_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

def draw_square(canvas, x1, y1, color="white", label=None):
    x2 = x1 + CELL_SIZE * 2
    y2 = y1 + CELL_SIZE * 2
    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
    if label:
        canvas.create_text(
            (x1 + x2) // 2,
            (y1 + y2) // 2,
            text=label,
            font=("Myanmar Text", 10),
            anchor="center"
        )


def draw_triangle(canvas, points, color="lightblue", label=None):
    canvas.create_polygon(points, outline="black", fill=color)
    if label:
        cx = sum([pt[0] for pt in points]) // 3
        cy = sum([pt[1] for pt in points]) // 3
        canvas.create_text(cx, cy, text=label, font=("Myanmar Text", 10))

# --- Main App ---
toplevel = tk.Tk()
toplevel.title("Astrology Grid Prototype")
canvas = tk.Canvas(toplevel, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
canvas.pack()

# --- Draw Cardinal Squares ---
rndfill = get_random_hex_color()
#Draw Swuqre
draw_square(canvas, 2 * CELL_SIZE, 0,"LightBlue", "မိဿ")
draw_square(canvas, 0, 2 * CELL_SIZE,"LightBlue", "ကရကဋ်")
draw_square(canvas, 2 * CELL_SIZE, 4 * CELL_SIZE, "LightBlue", "တူ")
draw_square(canvas, 4 * CELL_SIZE, 2 * CELL_SIZE, "LightBlue", "မကာရ")


# --- Draw Triangle Regions ---
draw_triangle(canvas, [(0, 0), (2 * CELL_SIZE, 2 * CELL_SIZE), (2 * CELL_SIZE, 0)], "lightblue", "ပြိဿ")
draw_triangle(canvas, [(0, 0), (2 * CELL_SIZE, 2 * CELL_SIZE), (0, 2 * CELL_SIZE)], "lightblue", "မေထုန်")

draw_triangle(canvas, [(0, 4 * CELL_SIZE), (0, 6 * CELL_SIZE), (2 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "သိဟ်")
draw_triangle(canvas, [(0, 6 * CELL_SIZE), (2 * CELL_SIZE, 6 * CELL_SIZE), (2 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "ကန်")

draw_triangle(canvas, [(4 * CELL_SIZE, 4 * CELL_SIZE), (6 * CELL_SIZE, 6 * CELL_SIZE), (4 * CELL_SIZE, 6 * CELL_SIZE)], "lightblue", "ဗြိစ္ဆာ")
draw_triangle(canvas, [(4 * CELL_SIZE, 4 * CELL_SIZE), (6 * CELL_SIZE, 6 * CELL_SIZE), (6 * CELL_SIZE, 4 * CELL_SIZE)], "lightblue", "ဓနု")

draw_triangle(canvas, [(6 * CELL_SIZE, 2 * CELL_SIZE), (4 * CELL_SIZE, 2 * CELL_SIZE), (6 * CELL_SIZE, 0)], "lightblue", "ကုမ်")
draw_triangle(canvas, [(4 * CELL_SIZE, 0), (4 * CELL_SIZE, 2 * CELL_SIZE), (6 * CELL_SIZE, 0)], "lightblue", "မိန်")


# --- Center Marker ---
center_x = CANVAS_SIZE // 2
center_y = CANVAS_SIZE // 2
#canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill="red")
canvas.create_text(center_x, center_y , text="ရာသီ", font=("Myanmar Text", 12), fill="black", anchor="center")


toplevel.mainloop()