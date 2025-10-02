import tkinter as tk
from tkinter import ttk

class BurmeseGrid:
    """
    Tkinter canvas ကို အခြေခံပြီး မြန်မာဗေဒင်ဇယားကွက်ကို ဆွဲပေးသည့် component တစ်ခု။
    """
    def __init__(self, parent, width=50, height=250, cell_size=250, bg="white"):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.cell_size = cell_size

    def draw_grid(self, label_text="မြန်မာ"):
        """
        အကွက်ပုံစံ ဇယားကွက်ကို ဆွဲပေးသည်။
        :param label_text: အလယ်ဗဟိုတွင် ထည့်မည့် စာသား။
        """
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
        self.canvas.create_text(c_x, c_y, text=label_text, font=("Myanmar Text", 14, "bold"), fill="black")

        return self

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)
        return self

    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)
        return self

    def place(self, **kwargs):
        self.canvas.place(**kwargs)
        return self

    def get_canvas(self):
        return self.canvas

class GridApplication:
    """
    ဇယားကွက် component သုံးခုကို ပြသသည့် အဓိက application class
    """
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("Burmese Grid Components")
        self.toplevel.geometry("1000x800")
        
        # အဓိက frame ကို ဖန်တီးသည်
        main_frame = ttk.Frame(toplevel, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ခေါင်းစဉ်ထည့်သည်
        title_label = ttk.Label(main_frame, text="Burmese Grid Components - ActiveX Style", 
                                font=("Pyidaungsu", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # ဇယားကွက်များအတွက် frame ကို ဖန်တီးသည်
        grid_container = ttk.Frame(main_frame)
        grid_container.pack(fill=tk.BOTH, expand=True)
        
        # ဇယားကွက် component သုံးခုကို ဖန်တီးသည်
        self.grid1 = BurmeseGrid(grid_container, width=250, height=250)
        self.grid2 = BurmeseGrid(grid_container, width=250, height=250)
        self.grid3 = BurmeseGrid(grid_container, width=250, height=250)
        
        # ဇယားကွက်များကို စာသားများဖြင့် ဆွဲသည်။
        self.grid1.draw_grid("ရာသီ").grid(row=0, column=0, padx=20, pady=10)
        self.grid2.draw_grid("ဘာဝ").grid(row=0, column=1, padx=20, pady=10)
        self.grid3.draw_grid("နဝင်း").grid(row=0, column=2, padx=20, pady=10)
        
        # ဇယားကွက်တစ်ခုစီအောက်တွင် ခေါင်းစဉ်များ ထည့်သည်။
        ttk.Label(grid_container, text="Grid 1 - ရာသီ", font=("Myanmar Text", 12)).grid(row=1, column=0)
        ttk.Label(grid_container, text="Grid 2 - ဘာဝ", font=("Myanmar Text", 12)).grid(row=1, column=1)
        ttk.Label(grid_container, text="Grid 3 - နဝင်း", font=("Myanmar Text", 12)).grid(row=1, column=2)
        
if __name__ == "__main__":
    toplevel = tk.Tk()
    app = GridApplication(toplevel)
    toplevel.mainloop()
