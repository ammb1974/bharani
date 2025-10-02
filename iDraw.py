import tkinter as tk
from tkinter import ttk
import math

# BurmeseGrid simulation since we don't have the actual DChart module
class BurmeseGrid:
    def __init__(self, parent, width=250, height=250):
        self.parent = parent
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(parent, width=width, height=height, bg='white')
        
    def draw_grid(self, title):
        # Draw a simplified Burmese-style grid
        w, h = self.width, self.height
        c = self.canvas
        
        # Draw outer rectangle
        c.create_rectangle(10, 10, w-10, h-10, outline='#CC7722', width=2)
        
        # Draw decorative corners
        c.create_arc(5, 5, 35, 35, start=0, extent=90, outline='#8B4513', width=1, style=tk.ARC)
        c.create_arc(w-35, 5, w-5, 35, start=90, extent=90, outline='#8B4513', width=1, style=tk.ARC)
        c.create_arc(5, h-35, 35, h-5, start=270, extent=90, outline='#8B4513', width=1, style=tk.ARC)
        c.create_arc(w-35, h-35, w-5, h-5, start=180, extent=90, outline='#8B4513', width=1, style=tk.ARC)
        
        # Draw grid lines
        for i in range(1, 5):
            x = 10 + (i * (w-20) / 5)
            c.create_line(x, 10, x, h-10, fill='#E8C19A', dash=(2, 2))
            
        for i in range(1, 5):
            y = 10 + (i * (h-20) / 5)
            c.create_line(10, y, w-10, y, fill='#E8C19A', dash=(2, 2))
        
        # Add title
        c.create_text(w/2, 25, text=title, font=('Myanmar Text', 14, 'bold'), fill='#8B4513')
        
        # Add some Burmese text as decoration
        c.create_text(w/2, h/2, text="ဗမာ", font=('Myanmar Text', 32), fill='#CC7722')
        c.create_text(w/2, h/2 + 40, text="ဇယား", font=('Myanmar Text', 18), fill='#8B4513')
        
        return self.canvas

class ExampleApp:   
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("BurmeseGrid Component Example")
        self.toplevel.geometry("900x700")
        self.toplevel.configure(bg='#F5F5DC') # Set background color

        main_frame = ttk.Frame(toplevel, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        example1_frame = ttk.LabelFrame(main_frame, text="Example 1: Basic Usage", padding="10")
        example1_frame.pack(fill=tk.X, pady=10)

        grid1 = BurmeseGrid(example1_frame, width=250, height=250)
        grid1.draw_grid("ရာသီ").pack(pady=10)
        
        # Add more examples
        example2_frame = ttk.LabelFrame(main_frame, text="Example 2: Different Sizes", padding="10")
        example2_frame.pack(fill=tk.X, pady=10)
        
        frame2 = ttk.Frame(example2_frame)
        frame2.pack(fill=tk.X)
        
        grid2 = BurmeseGrid(frame2, width=200, height=200)
        grid2.draw_grid("ဥက္ကာပျံ").pack(side=tk.LEFT, padx=10)
        
        grid3 = BurmeseGrid(frame2, width=300, height=150)
        grid3.draw_grid("နက္ခတ်").pack(side=tk.LEFT, padx=10)
        
        # Add some information text
        info_frame = ttk.LabelFrame(main_frame, text="About Burmese Grids", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = """
        Burmese grids are traditional decorative elements used in Myanmar (Burmese) art and architecture.
        They often feature intricate geometric patterns and are used in various cultural contexts.
        
        This example demonstrates a simplified version of a Burmese grid pattern.
        """
        
        info_label = ttk.Label(info_frame, text=info_text, wraplength=800, justify=tk.LEFT)
        info_label.pack()
        
        # Add a footer
        footer = ttk.Label(main_frame, text="မြန်မာ့ရိုးရာ ဇယားပုံစံများ", font=('Myanmar Text', 10))
        footer.pack(pady=20)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ExampleApp(root)
    root.mainloop()