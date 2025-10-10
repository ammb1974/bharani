import tkinter as tk
from tkinter import ttk, messagebox
import sys

def check_tkinter():
    """Tkinter ကို စစ်ဆေးသည်"""
    try:
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception as e:
        print(f"Tkinter error: {e}")
        return False

def get_available_font():
    """စနစ်မှာ ရနိုင်တဲ့ Font ကို ရှာသည်"""
    try:
        font_list = ["TkDefaultFont", "Arial", "Times New Roman", "Helvetica", "Courier"]
        myanmar_fonts = ["Pyidaungsu", "Myanmar Text", "Myanmar3", "Masterpiece Uni Sans"]
        font_list.extend(myanmar_fonts)
        
        for font in font_list:
            try:
                test_font = tk.font.Font(family=font, exists=True)
                if test_font:
                    print(f"Using font: {font}")
                    return font
            except:
                continue
        
        print("Using default font")
        return "TkDefaultFont"
    except Exception as e:
        print(f"Font error: {e}")
        return "TkDefaultFont"

class SimpleBurmeseGrid:
    """ရိုးရှင်းတဲ့ ဇယားကွက် component"""
    def __init__(self, parent, width=250, height=250, cell_size=30, bg="white"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg, highlightthickness=1)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = cell_size
        self.regions = {}
        self.font_family = get_available_font()
        print(f"Grid created with font: {self.font_family}")

    def draw_grid(self, label_text="Grid"):
        """ဇယားကွက်ကို ဆွဲသည်"""
        try:
            c_x, c_y = self.center_x, self.center_y
            cell = self.cell_size
            
            # ဒေါင်လိုက်မျဉ်းများ
            self.canvas.create_line(c_x - cell, c_y - (5*cell), c_x - cell, c_y + (5*cell), fill="black", width=1)
            self.canvas.create_line(c_x + cell, c_y - 5*cell, c_x + cell, c_y + 5*cell, fill="black", width=1)
            
            # အလျားလိုက်မျဉ်းများ
            self.canvas.create_line(c_x - 5*cell, c_y - cell, c_x + 5*cell, c_y - cell, fill="black", width=1)
            self.canvas.create_line(c_x - 5*cell, c_y + cell, c_x + 5*cell, c_y + cell, fill="black", width=1)
            
            # ထောင့်ဖြတ်မျဉ်းများ
            self.canvas.create_line(c_x - 5*cell, c_y - 5*cell, c_x - cell, c_y - cell, fill="black", width=1)
            self.canvas.create_line(c_x + 5*cell, c_y - 5*cell, c_x + cell, c_y - cell, fill="black", width=1)
            self.canvas.create_line(c_x - cell, c_y + cell, c_x - 5*cell, c_y + 5*cell, fill="black", width=1)
            self.canvas.create_line(c_x + cell, c_y + cell, c_x + 5*cell, c_y + 5*cell, fill="black", width=1)
            
            # အလယ်တွင် စာသားထည့်ခြင်း
            self.canvas.create_text(c_x, c_y, text=label_text, 
                                   font=(self.font_family, 14, "bold"), 
                                   fill="black")
            
            print("Grid drawn successfully")
            return self
        except Exception as e:
            print(f"Error drawing grid: {e}")
            messagebox.showerror("Error", f"Error drawing grid: {e}")
            return self

    def add_triangle_region(self, name, points, fill_color="", outline_color="blue", width=2):
        """တြိဂံ region ထည့်သည်"""
        try:
            triangle = self.canvas.create_polygon(points, fill=fill_color, outline=outline_color, width=width)
            self.regions[name] = triangle
            print(f"Triangle region '{name}' added")
            return triangle
        except Exception as e:
            print(f"Error adding triangle: {e}")
            return None

    def highlight_region(self, name, color="yellow"):
        """Region ကို ရောင်ပြန်းသည်"""
        try:
            region = self.regions.get(name)
            if region:
                self.canvas.itemconfig(region, fill=color)
                print(f"Region '{name}' highlighted with {color}")
        except Exception as e:
            print(f"Error highlighting region: {e}")

    def clear_region_highlight(self, name):
        """Region ရဲ့ ရောင်ပြန်းမှုကို ဖယ်ရှားသည်"""
        try:
            region = self.regions.get(name)
            if region:
                self.canvas.itemconfig(region, fill="")
                print(f"Region '{name}' highlight cleared")
        except Exception as e:
            print(f"Error clearing highlight: {e}")

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)
        return self

    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)
        return self

    def get_canvas(self):
        return self.canvas


class SimpleGridApplication:
    """ရိုးရှင်းတဲ့ application"""
    def __init__(self, toplevel):
        print("Starting application...")
        
        self.toplevel = toplevel
        self.toplevel.title("Burmese Grid Test")
        self.toplevel.geometry("800x600")
        
        # အဓိက frame
        main_frame = ttk.Frame(toplevel, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ခေါင်းစဉ်
        try:
            title_label = ttk.Label(main_frame, text="Burmese Grid Test Application", 
                                   font=(get_available_font(), 16, "bold"))
            title_label.pack(pady=(0, 20))
            print("Title added")
        except Exception as e:
            print(f"Error with title: {e}")
            title_label = ttk.Label(main_frame, text="Grid Test Application", 
                                   font=("Arial", 16, "bold"))
            title_label.pack(pady=(0, 20))
        
        # ဇယားကွက်များ
        grid_container = ttk.Frame(main_frame)
        # *** ဒီနေရာမှာ ပြင်ဆင်ချက်ကို ကြည့်ပါ ***
        # အောက်က လိုင်းကို expand=True ကို ဖယ်ထုတ်လိုက်ပါတယ်။
        grid_container.pack(fill=tk.BOTH, expand=False, pady=10) 
        
        # ဇယားကွက်တစ်ခုကို စမ်းကြည့်သည်
        print("Creating test grid...")
        self.test_grid = SimpleBurmeseGrid(grid_container, width=250, height=250)
        self.test_grid.draw_grid("Test").pack()
        
        # ရိုးရှင်းတဲ့ region တစ်ခု ထည့်သည်
        c_x, c_y = self.test_grid.center_x, self.test_grid.center_y
        cell = self.test_grid.cell_size
        
        self.test_grid.add_triangle_region(
            "test_triangle",
            [(c_x - 2*cell, c_y - 2*cell), (c_x + 2*cell, c_y - 2*cell), (c_x, c_y + 2*cell)],
            outline_color="blue"
        )
        
        # ထိန်းချုပ်မှု button များ
        print("Creating buttons...")
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=20) # ဒီနေရာမှာ pack လုပ်ထားတာ သေချာပါတယ်။
        
        ttk.Button(control_frame, text="Highlight", 
                  command=self.highlight_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear", 
                  command=self.clear_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Test Message", 
                  command=self.show_test_message).pack(side=tk.LEFT, padx=5)
        
        print("Application setup complete")
    
    def highlight_test(self):
        """စမ်းသပ်မှု ရောင်ပြန်းခြင်း"""
        self.test_grid.highlight_region("test_triangle", "lightblue")
    
    def clear_test(self):
        """စမ်းသပ်မှု ရောင်ပြန်းမှု ဖယ်ရှားခြင်း"""
        self.test_grid.clear_region_highlight("test_triangle")
    
    def show_test_message(self):
        """စမ်းသပ်မှု မက်ဆေ့ချ် ပြသခြင်း"""
        messagebox.showinfo("Test", "Application is working!")


def main():
    """အဓိက function"""
    print("Checking system...")
    
    if not check_tkinter():
        print("Error: Tkinter is not properly installed!")
        messagebox.showerror("Error", "Tkinter is not properly installed!")
        return
    
    print("Tkinter is working")
    font = get_available_font()
    print(f"Using font: {font}")
    
    try:
        print("Starting application...")
        root = tk.Tk()
        app = SimpleGridApplication(root)
        print("Application started successfully")
        root.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Application Error", f"Error: {e}")


if __name__ == "__main__":
    main()