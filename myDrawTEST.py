import tkinter as tk
from tkinter import ttk

class BurmeseGrid:
    def __init__(self, parent, width=300, height=300, bg="lightgray"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = min(width, height) // 5

    def draw_grid(self, label_text="မြန်မာ"):
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size

        # Vertical lines (commented out)
        self.canvas.create_line(c_x - cell, c_y - 5*cell, c_x - cell, c_y + 5*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y - 5*cell, c_x + cell, c_y + 5*cell, fill="black", width=1)

        # Horizontal lines (only this one is uncommented - this is the line you see)
        # self.canvas.create_line(c_x - 1.5*cell, c_y - cell, c_x + 1.5*cell, c_y - cell, fill="black", width=1)
        
        # Other horizontal line (commented out)
        self.canvas.create_line(c_x - 5*cell, c_y + cell, c_x + 5*cell, c_y + cell, fill="black", width=1)
        self.canvas.create_line(c_x - 5*cell, c_y - cell, c_x + 5*cell, c_y - cell, fill="black", width=1)

        # Diagonal lines (all commented out)
        self.canvas.create_line(c_x - 5*cell, c_y - 5*cell, c_x - cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x + 5*cell, c_y - 5*cell, c_x + cell, c_y - cell, fill="black", width=1)
        self.canvas.create_line(c_x - cell, c_y + cell, c_x - 5*cell, c_y + 5*cell, fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y + cell, c_x + 5*cell, c_y + 5*cell, fill="black", width=1)

        # Center label (commented out)
        self.canvas.create_text(c_x, c_y, text=label_text, font=("Myanmar Text", 14, "bold"), fill="black")
        
        # Dot calculations (but dot is not drawn)
       

        return self.canvas

# Main application
def main():
    toplevel = tk.Tk()
    toplevel.title("မြန်မာ Grid UI")

    grid_frame = ttk.Frame(toplevel, padding=10)
    grid_frame.pack()

    grid = BurmeseGrid(grid_frame)
    canvas_widget = grid.draw_grid("ရာသီတော်\n စည်ကြီး")
    canvas_widget.pack()

    toplevel.mainloop()

if __name__ == "__main__":
    main()