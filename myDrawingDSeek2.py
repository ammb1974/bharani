import tkinter as tk
from tkinter import ttk

class BurmeseGrid:
    def __init__(self, parent, width=200, height=200, bg="lightgray"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = min(width, height) // 5
        
    def draw_grid(self, label_text):
        """Draw the complete grid with lines and a single centered label"""
        c_x, c_y = self.center_x, self.center_y
        cell = self.cell_size
        
        # Draw vertical lines
        self.canvas.create_line(c_x - cell, c_y - 1.5*cell, 
                               c_x - cell, c_y + 1.5*cell, 
                               fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y - 1.5*cell, 
                               c_x + cell, c_y + 1.5*cell, 
                               fill="black", width=1)
        
        # Draw horizontal lines
        self.canvas.create_line(c_x - 1.5*cell, c_y - cell, 
                               c_x + 1.5*cell, c_y - cell, 
                               fill="black", width=1)
        self.canvas.create_line(c_x - 1.5*cell, c_y + cell, 
                               c_x + 1.5*cell, c_y + cell, 
                               fill="black", width=1)
        
        # Draw diagonal lines
        self.canvas.create_line(c_x - 1.5*cell, c_y - 1.5*cell, 
                               c_x - cell, c_y - cell, 
                               fill="black", width=1)
        self.canvas.create_line(c_x + 1.5*cell, c_y - 1.5*cell, 
                               c_x + cell, c_y - cell, 
                               fill="black", width=1)
        self.canvas.create_line(c_x - cell, c_y + cell, 
                               c_x - 1.5*cell, c_y + 1.5*cell, 
                               fill="black", width=1)
        self.canvas.create_line(c_x + cell, c_y + cell, 
                               c_x + 1.5*cell, c_y + 1.5*cell, 
                               fill="black", width=1)
        
        # Add the single centered label
        self.canvas.create_text(c_x, c_y, text=label_text, 
                               font=("Myanmar Text", 14, "bold"), fill="black")
        
        return self
    
    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)
    
    def place(self, **kwargs):
        self.canvas.place(**kwargs)


class CenteredGridApplication:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("Burmese Grid Application")
        self.toplevel.geometry("700x400")
        self.toplevel.configure(bg='white')
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='white')
        self.style.configure('Header.TLabel', background='white', 
                            font=('Pyidaungsu', 14, 'bold'))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = ttk.Frame(self.toplevel)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header, text="Burmese Grid System with Centered Labels", 
                 style='Header.TLabel').pack(pady=5)
        
        # Main content area with three grids
        main_frame = ttk.Frame(self.toplevel)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create three grid instances with different labels
        self.grid1 = BurmeseGrid(main_frame, width=180, height=180)
        self.grid2 = BurmeseGrid(main_frame, width=180, height=180)
        self.grid3 = BurmeseGrid(main_frame, width=180, height=180)
        
        # Draw grids with centered labels
        self.grid1.draw_grid("ရာသီ").grid(row=0, column=0, padx=10, pady=10)
        self.grid2.draw_grid("ဘာဝ").grid(row=0, column=1, padx=10, pady=10)
        self.grid3.draw_grid("နဝင်း").grid(row=0, column=2, padx=10, pady=10)
        
        # Add descriptive labels below each grid
        ttk.Label(main_frame, text="Grid 1").grid(row=1, column=0)
        ttk.Label(main_frame, text="Grid 2").grid(row=1, column=1)
        ttk.Label(main_frame, text="Grid 3").grid(row=1, column=2)


if __name__ == "__main__":
    toplevel = tk.Tk()
    app = CenteredGridApplication(toplevel)
    toplevel.mainloop()