import tkinter as tk

WIDTH, HEIGHT = 300, 300
ROWS, COLS = 3, 3
PADDING = 5

def draw_grid(canvas):
    cell_w = (WIDTH - 2 * PADDING) / COLS
    cell_h = (HEIGHT - 2 * PADDING) / ROWS

    for r in range(ROWS):
        for c in range(COLS):
            x1 = PADDING + c * cell_w
            y1 = PADDING + r * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h

            # Draw cells
            canvas.create_rectangle(x1, y1, x2, y2, outline="#000", width=1)
            # Diagonal triangles for corners
            if (r, c) == (0,0):
                canvas.create_polygon(x1, y1, x2, y1, x2, y2, fill="#f0f0f0", outline="#000000")
                canvas.create_polygon(x1, y1, x1, y2, x2, y2, fill="#e0e0e0", outline="#000000")
            elif (r, c) == (0, 2):
                canvas.create_polygon(x1, y1, x2, y1, x1, y2, fill="#f0f0f0", outline="#000000")
                canvas.create_polygon(x2, y1, x2, y2, x1, y2, fill="#e0e0e0", outline="#000000")
            elif (r, c) == (2, 0):
                canvas.create_polygon(x1, y1, x2, y1, x1, y2, fill="#f0f0f0", outline="#000000")
                canvas.create_polygon(x2, y1, x2, y2, x1, y2, fill="#e0e0e0", outline="#000000")
            elif (r, c) == (2, 2):
                canvas.create_polygon(x1, y1, x2, y1, x2, y2, fill="#f0f0f0", outline="#000000")
                canvas.create_polygon(x1, y1, x1, y2, x2, y2, fill="#e0e0e0", outline="#000000")

click_positions = [
    (114, 13), (50, 13), (10, 41), (14, 109),
    (14, 206), (65, 250), (112, 207), (205, 244),
    (255, 205), (244, 108), (255, 55), (207, 13)
]
def place_symbols(canvas):
    cell_w = (WIDTH - 2 * PADDING) / COLS
    cell_h = (HEIGHT - 2 * PADDING) / ROWS

    symbols = {
        (0,0): ["၁" ],
        (0,1): ["၂"],
        (0,2): ["၃", "ဂြိုဟ်3"],
        (1,0): ["၄"],
        (1,1): ["အလယ်"],
        (1,2): ["၅"],
        (2,0): ["၆", "ဂြိုဟ်6"],
        (2,1): ["၇"],
        (2,2): ["၈", "ဂြိုဟ်8"]
    }

    for (r, c), texts in symbols.items():
        x1 = PADDING + c * cell_w
        y1 = PADDING + r * cell_h
        x2 = x1 + cell_w
        y2 = y1 + cell_h

        if len(texts) == 1:
            canvas.create_text((x1+x2)/2, (y1+y2)/2, text=texts[0], font=("Noto Sans Myanmar", 12), fill="#111")
        elif len(texts) == 2:
            canvas.create_text((x1+x2)/2 - 20, (y1+y2)/2, text=texts[0], font=("Noto Sans Myanmar", 12), fill="#111")
            canvas.create_text((x1+x2)/2 + 20, (y1+y2)/2, text=texts[1], font=("Noto Sans Myanmar", 12), fill="#111")

def on_click(event):
    # event.x, event.y는 클릭한 정확한 좌표입니다.
    print(f"Mouse clicked at x={event.x}, y={event.y}")

def place_symbols(canvas):
    # Your symbol placing code (optional)
    pass

def draw_red_dots(canvas):
    radius = 5
    for (x, y) in click_positions:
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red", outline="")

def on_click(event, canvas):
    click_positions.append((event.x, event.y))
    print(f"Mouse clicked at x={event.x}, y={event.y}")
    canvas.delete("dots")  # Clear previous dots
    draw_red_dots(canvas)
    canvas.tag_lower("dots")  # send dots beneath texts etc.

def draw_red_dots(canvas):
    radius = 5
    for (x, y) in click_positions:
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red", outline="")


def main():
    root = tk.Tk()
    root.title("[translate:မြန်မာ ဇာတာ]")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#fff")
    canvas.pack()

    draw_grid(canvas)
    place_symbols(canvas)  # place your texts
    draw_red_dots(canvas)
    

    canvas.bind("<Button-1>", on_click)# bind mouse left click

    root.mainloop()

if __name__ == "__main__":
    main()
