import tkinter as tk
import tkinter as ttk




WIDTH, HEIGHT = 300, 300
ROWS, COLS = 3, 3
PADDING = 5



def draw_grid(canvas, center_label):
    cell_w = (WIDTH - 2 * PADDING) / COLS
    cell_h = (HEIGHT - 2 * PADDING) / ROWS

    canvas.create_text(WIDTH/2, 10, font=("Myanmar Text", 12, "bold"))

    for r in range(ROWS):
        for c in range(COLS):
            x1 = PADDING + c * cell_w
            y1 = 20 + PADDING + r * cell_h  # shift down for title
            x2 = x1 + cell_w
            y2 = y1 + cell_h

            canvas.create_rectangle(x1, y1, x2, y2, outline="#000", width=1)

            # Corner triangles
            if (r, c) == (0,0):
                canvas.create_polygon(x1, y1, x2, y1, x2, y2, fill="#f0f0f0", outline="#000")
                canvas.create_polygon(x1, y1, x1, y2, x2, y2, fill="#faf9cd", outline="#011")
            elif (r, c) == (0,2):
                canvas.create_polygon(x1, y1, x2, y1, x1, y2, fill="#f0f0f0", outline="#000")
                canvas.create_polygon(x2, y1, x2, y2, x1, y2, fill="#d7f4e2", outline="#011")
            elif (r, c) == (2,0):
                canvas.create_polygon(x1, y1, x2, y1, x1, y2, fill="#f0f0f0", outline="#000")
                canvas.create_polygon(x2, y1, x2, y2, x1, y2, fill="#bcedfa", outline="#001")
            elif (r, c) == (2,2):
                canvas.create_polygon(x1, y1, x2, y1, x2, y2, fill="#f0f0f0", outline="#000")
                canvas.create_polygon(x1, y1, x1, y2, x2, y2, fill="#d5bdf6", outline="#011")

            # Center label
            if (r, c) == (1, 1):
                canvas.create_text((x1 + x2)/2, (y1 + y2)/2, text=center_label, font=("Myanmar Text", 11, "bold"))






root = tk.Tk()
root.title("တြိစက္ကဇာတာ")
root.state('zoomed') 

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)


left_frame = ttk.Frame(paned_window, width=420,background="lightblue", relief=tk.SUNKEN)
paned_window.add(left_frame)

# ဘယ်ဘက်အပိုင်းအတွက် label
left_label = ttk.Label(left_frame, text="ဇာတာဖွဲ့ခြင်း", background="lightblue")
left_label.pack(pady=20)

# ညာဘက်အပိုင်း အတွက် ရေးပါ
right_frame = ttk.Frame(paned_window,background="white", relief=tk.SUNKEN)
paned_window.add(right_frame)

right_label = ttk.Label(right_frame, text="တြိစက္က", background="white", font=("Myanmar Text", 14, "bold"))
right_label.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew")


paned_window.paneconfigure(left_frame, width=400)


# Define titles and center labels for each chart
charts = [
    ("ရာသီစက်"),
    ("ဘာဝစက်"),
    ("နဝင်းစက်")
]

# Charts တွေကို grid နဲ့ထည့်ပါ
for i, center_label in enumerate(charts):
    canvas = tk.Canvas(right_frame, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0)
    canvas.grid(row=1, column=i, padx=5, pady=5)
   
    draw_grid(canvas, center_label)  # title မပါတော့ဘူး

right_frame.grid_columnconfigure(2, weight=5)
right_frame.grid_columnconfigure(2, weight=5)
right_frame.grid_columnconfigure(2, weight=5)
right_frame.grid_rowconfigure(2, weight=5)





root.mainloop()