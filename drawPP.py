import tkinter as tk
import random

   
# Grid settings
CELL_SIZE = 50
GRID_RANGE = 5  # Draw from -5 to +5 in both directions

# Canvas setup
toplevel = tk.Tk()
toplevel.title("Centered Grid Drawing")
canvas = tk.Canvas(toplevel, width=300, height=300, bg="white")
canvas.pack()

# Center point
center_x = 300//2
center_y = 300//2

def get_random_hex_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'#{r:02x}{g:02x}{b:02x}'

rndfill = get_random_hex_color()
# Draw grid squares
for dx in range(-GRID_RANGE, GRID_RANGE + 1):
    for dy in range(-GRID_RANGE, GRID_RANGE + 1):
        x1 = center_x + dx * CELL_SIZE
        y1 = center_y + dy * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline="black")

canvas.create_rectangle(2*CELL_SIZE, 0, 4* CELL_SIZE, 2*CELL_SIZE, outline="black", fill=rndfill)  #East 
canvas.create_rectangle( 4*CELL_SIZE, 2*CELL_SIZE,6*CELL_SIZE, 4*CELL_SIZE, outline="black", fill=rndfill) #South
canvas.create_rectangle(0,2*CELL_SIZE, 2* CELL_SIZE, 4*CELL_SIZE, outline="black", fill=rndfill) # wwest
canvas.create_rectangle( 2*CELL_SIZE, 4*CELL_SIZE,4*CELL_SIZE, 6*CELL_SIZE, outline="black", fill=rndfill) #North

canvas.create_polygon((0,0,2*CELL_SIZE,2 *CELL_SIZE, 2*CELL_SIZE,0), outline="black", fill="LightBlue") #ပြိဿ
canvas.create_polygon((0,0,2*CELL_SIZE,2*CELL_SIZE, 0,2*CELL_SIZE), outline="black", fill="LightBlue") #မေထုန်

canvas.create_polygon((0,4*CELL_SIZE,0,6*CELL_SIZE, 2*CELL_SIZE,4*CELL_SIZE), outline="black", fill="LightBlue")#သိဟ်
canvas.create_polygon((0,6*CELL_SIZE,2*CELL_SIZE,6*CELL_SIZE, 2*CELL_SIZE,4*CELL_SIZE), outline="black", fill="LightBlue")#သိ

canvas.create_polygon((4*CELL_SIZE,4*CELL_SIZE,6*CELL_SIZE,6 *CELL_SIZE, (4*CELL_SIZE,6*CELL_SIZE)), outline="black", fill="LightBlue")#ဗြိစ္ဆာ
canvas.create_polygon((4*CELL_SIZE,4*CELL_SIZE,6*CELL_SIZE,6 *CELL_SIZE, (6*CELL_SIZE,4*CELL_SIZE)), outline="black", fill="LightBlue")#ဓနု

canvas.create_polygon((4*CELL_SIZE,0,4*CELL_SIZE,2 *CELL_SIZE, (6*CELL_SIZE,0)), outline="black", fill="LightBlue")#ကုမ်
canvas.create_polygon((6*CELL_SIZE,2*CELL_SIZE,4*CELL_SIZE,2 *CELL_SIZE, (6*CELL_SIZE,0)), outline="black", fill="LightBlue")#မိန်


# Optional: draw center marker
canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill="red")

toplevel.mainloop()