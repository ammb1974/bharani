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

            # Draw main square
            canvas.create_rectangle(x1, y1, x2, y2, outline="#000", width=1)

            # Corner cells: draw correct diagonal triangles
            if (r, c) == (0,0):  # top-left
                canvas.create_polygon(x1, y1, x2, y1, x2, y2, fill="#f0f0f0", outline="#000000")  # top triangle
                canvas.create_polygon(x1, y1, x1, y2, x2, y2, fill="#e0e0e0", outline="#000000")  # bottom triangle
         

            elif (r, c) == (0, 2):  # top-right
                canvas.create_polygon(x1, y1, x2, y1, x1, y2, fill="#f0f0f0", outline="#000000")  # top triangle
                canvas.create_polygon(x2, y1, x2, y2, x1, y2, fill="#e0e0e0", outline="#000000")  # bottom triangle
               
            elif (r, c) == (2, 0):  # bottom-left
                canvas.create_polygon(x1, y1, x2, y1, x1, y2, fill="#f0f0f0", outline="#000000")  # top triangle
                canvas.create_polygon(x2, y1, x2, y2, x1, y2, fill="#e0e0e0", outline="#000000")  # bottom trian                
 
            elif (r, c) == (2, 2):  # bottom-right
                canvas.create_polygon(x1, y1, x2, y1, x2, y2, fill="#f0f0f0", outline="#000000")  # top triangle
                canvas.create_polygon(x1, y1, x1, y2, x2, y2, fill="#e0e0e0", outline="#000000")  # bottom triangle

# def place_symbols(canvas):
#     cell_w = (WIDTH - 2 * PADDING) / COLS
#     cell_h = (HEIGHT - 2 * PADDING) / ROWS

#     symbols = {
#         (0,0): ["၁ ၂၃° ၃၂", "သ"],
#         (0,1): ["အ"],
#         (0,2): ["ပ", "ဗ"],
#         (1,0): ["က"],
#         (1,1): [],  # center
#         (1,2): ["ဂ"],
#         (2,0): ["စ", "ည"],
#         (2,1): ["တ"],
#         (2,2): ["ဃ", "ဈ"]
#     }

#     for (r, c), chars in symbols.items():
#         x1 = PADDING + c * cell_w
#         y1 = PADDING + r * cell_h
#         x2 = x1 + cell_w
#         y2 = y1 + cell_h

#         if len(chars) == 1:
#             canvas.create_text((x1+x2)/2, (y1+y2)/2, text=chars[0],
#                                font=("Noto Sans Myanmar", 9), fill="#111")
#         elif len(chars) == 2:
#             canvas.create_text((x1+x2)/2 - 20, (y1+y2)/2, text=chars[0],
#                                font=("Noto Sans Myanmar", 9), fill="#111")
#             canvas.create_text((x1+x2)/2 + 20, (y1+y2)/2, text=chars[1],
#                                font=("Noto Sans Myanmar", 9), fill="#111")

def main():
    root = tk.Tk()
    root.title("မြန်မာ ဇာတာ")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#fff")
    canvas.pack()

    draw_grid(canvas)
    #place_symbols(canvas)

    root.mainloop()

if __name__ == "__main__":
    main()