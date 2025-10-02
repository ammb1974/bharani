import tkinter as tk
from tkinter import ttk

Import @DCharter import BurmeseGrid  # BurmeseGrid component ကို import လုပ်ပါ

class ExampleApp:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("BurmeseGrid Component Example")
        self.toplevel.geometry("900x700")
        
        # Main frame
        main_frame = ttk.Frame(toplevel, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="BurmeseGrid Component အသုံးပြုနည်း", 
                               font=("Myanmar Text", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Example 1: Basic usage
        example1_frame = ttk.LabelFrame(main_frame, text="Example 1: Basic Usage", padding="10")
        example1_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(example1_frame, text="grid = BurmeseGrid(parent_frame)\ngrid.draw_grid(\"ရာသီ\").pack()").pack(pady=5)
        
        # Create the grid
        grid1 = BurmeseGrid(example1_frame, width=250, height=250)
        grid1.draw_grid("ရာသီ").pack(pady=10)
        
        # Example 2: Custom size and placement
        example2_frame = ttk.LabelFrame(main_frame, text="Example 2: Custom Size and Placement", padding="10")
        example2_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(example2_frame, text="grid = BurmeseGrid(parent_frame, width=200, height=200, bg=\"white\")\ngrid.draw_grid(\"ဘာဝ\").grid(row=0, column=0)").pack(pady=5)
        
        # Create a frame for grid placement
        grid_container = ttk.Frame(example2_frame)
        grid_container.pack(pady=10)
        
        grid2 = BurmeseGrid(grid_container, width=200, height=200, bg="white")
        grid2.draw_grid("ဘာဝ").grid(row=0, column=0, padx=10)
        
        # Example 3: Canvas manipulation
        example3_frame = ttk.LabelFrame(main_frame, text="Example 3: Canvas Manipulation", padding="10")
        example3_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(example3_frame, text="canvas = grid.get_canvas()\ncanvas.create_oval(10, 10, 20, 20, fill=\"red\")").pack(pady=5)
        
        grid3 = BurmeseGrid(example3_frame, width=300, height=300)
        grid3.draw_grid("နဝင်း").pack(pady=10)
        
        # Get the canvas and add custom elements
        canvas = grid3.get_canvas()
        canvas.create_oval(50, 50, 70, 70, fill="red")  # Add a red circle
        canvas.create_rectangle(180, 180, 200, 200, fill="blue")  # Add a blue square
        
        # Multiple grids example
        multi_frame = ttk.LabelFrame(main_frame, text="Multiple Grids Example", padding="10")
        multi_frame.pack(fill=tk.X, pady=10)
        
        multi_container = ttk.Frame(multi_frame)
        multi_container.pack(pady=10)
        
        # Create multiple grids
        labels = ["ရာသီ", "ဘာဝ", "နဝင်း"]
        for i, label in enumerate(labels):
            grid = BurmeseGrid(multi_container, width=150, height=150)
            grid.draw_grid(label).grid(row=0, column=i, padx=10)
            ttk.Label(multi_container, text=f"Grid {i+1}").grid(row=1, column=i)

if __name__ == "__main__":
    toplevel = tk.Tk()
    app = ExampleApp(toplevel)
    toplevel.mainloop()