import tkinter as tk
from tkinter import ttk

class BurmeseGrid:
    def __init__(self, parent, width=500, height=500, bg="lightgray"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.labels = {}
        
    def draw_grid(self, center_x=10, center_y=10, cell_size=5):
        """Draw the complete grid with lines and default labels"""
        # Draw vertical lines
        self.canvas.create_line(center_x - cell_size, center_y - 2*cell_size, 
                               center_x - cell_size, center_y + 2*cell_size, 
                               fill="black", width=1)
        self.canvas.create_line(center_x + cell_size, center_y - 2*cell_size, 
                               center_x + cell_size, center_y + 2*cell_size, 
                               fill="black", width=1)
        
        # Draw horizontal lines
        self.canvas.create_line(center_x - 2*cell_size, center_y - cell_size, 
                               center_x + 2*cell_size, center_y - cell_size, 
                               fill="black", width=1)
        self.canvas.create_line(center_x - 2*cell_size, center_y + cell_size, 
                               center_x + 2*cell_size, center_y + cell_size, 
                               fill="black", width=1)
        
        # Draw diagonal lines
        self.canvas.create_line(center_x - 2*cell_size, center_y - 2*cell_size, 
                               center_x - cell_size, center_y - cell_size, 
                               fill="black", width=1)
        self.canvas.create_line(center_x + 2*cell_size, center_y - 2*cell_size, 
                               center_x + cell_size, center_y - cell_size, 
                               fill="black", width=1)
        self.canvas.create_line(center_x - cell_size, center_y + cell_size, 
                               center_x - 2*cell_size, center_y + 2*cell_size, 
                               fill="black", width=1)
        self.canvas.create_line(center_x + cell_size, center_y + cell_size, 
                               center_x + 2*cell_size, center_y + 2*cell_size, 
                               fill="black", width=1)
        
        # Add default labels
        self.add_label("ရာသီ", center_x - cell_size/2, center_y - cell_size/2)
        self.add_label("ဘာဝ", center_x + cell_size/2, center_y - cell_size/2)
        self.add_label("နဝင်း", center_x, center_y)
        
        return self
    
    def add_label(self, text, x, y, font=("Myanmar Text", 13), fill="black"):
        """Add a text label to the grid"""
        label_id = self.canvas.create_text(x, y, text=text, font=font, fill=fill)
        self.labels[text] = label_id
        return label_id
    
    def update_label(self, text, new_text=None, new_position=None):
        """Update an existing label's text or position"""
        if text in self.labels:
            if new_text:
                self.canvas.itemconfig(self.labels[text], text=new_text)
            if new_position:
                self.canvas.coords(self.labels[text], new_position[0], new_position[1])
    
    def pack(self, **kwargs):
        """Pack the canvas with optional parameters"""
        self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the canvas with optional parameters"""
        self.canvas.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the canvas with optional parameters"""
        self.canvas.place(**kwargs)


class GridApplication:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("Professional Burmese Grid Application")
        self.toplevel.geometry("800x600")
        
        # Create a style for ttk widgets
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('Header.TLabel', background='#f0f0f0', font=('Pyidaungsu', 14, 'bold'))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = ttk.Frame(self.toplevel)
        header.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header, text="Burmese Grid System", style='Header.TLabel').pack(pady=10)
        
        # Main content area
        main_frame = ttk.Frame(self.toplevel)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create three grid instances
        self.grid1 = BurmeseGrid(main_frame, width=300, height=300)
        self.grid2 = BurmeseGrid(main_frame, width=300, height=300)
        self.grid3 = BurmeseGrid(main_frame, width=300, height=300)
        
        # Draw grids with different parameters
        self.grid1.draw_grid(150, 150, 70).grid(row=0, column=0, padx=5, pady=5)
        self.grid2.draw_grid(150, 150, 60).grid(row=0, column=1, padx=5, pady=5)
        self.grid3.draw_grid(150, 150, 80).grid(row=0, column=2, padx=5, pady=5)
        
        # Add some additional labels to demonstrate functionality
        #self.grid1.add_label("အပိုဒ်", 150, 50)
       # self.grid2.add_label("စာသား", 150, 250)
        #self.grid3.add_label("ဒေတာ", 250, 150)
        
        # Control panel
        control_frame = ttk.Frame(self.toplevel)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="Update Labels", command=self.update_labels).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Add New Grid", command=self.add_new_grid).pack(side=tk.RIGHT, padx=5)
        
    def update_labels(self):
        """Example method to update labels"""
        self.grid1.update_label("ရာသီ", "ပြောင်းလဲ")
        self.grid2.update_label("နဝင်း", "အသစ်")
        
    def reset(self):
        """Reset all grids to default"""
        for widget in self.toplevel.winfo_children():
            if isinstance(widget, ttk.Frame) and widget.winfo_children():
                if hasattr(widget.winfo_children()[0], 'delete'):
                    widget.winfo_children()[0].delete("all")
        
        # Reinitialize the grids
        self.create_widgets()
        
    def add_new_grid(self):
        """Add a new grid to the application"""
        new_window = tk.Toplevel(self.toplevel)
        new_window.title("Additional Grid")
        new_window.geometry("400x400")
        
        grid = BurmeseGrid(new_window, width=350, height=350)
        grid.draw_grid(175, 175, 75).pack(padx=20, pady=20)
        grid.add_label("အသစ်", 175, 75)


if __name__ == "__main__":
    toplevel = tk.Tk()
    app = GridApplication(toplevel)
    toplevel.mainloop()