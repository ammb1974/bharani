import tkinter as tk
import childChart as cc
from childChart import ChartWindow



class MainWindow:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("Main Window")
        
        # Child window ကိုဖွင့်မည့် button
        self.btn_open_chart = tk.Button(toplevel, text="Open Chart", command=self.open_chart_window)
        self.btn_open_chart.pack(pady=20)
        
        # Chart data ကိုပြမည့် frame
        self.chart_frame = tk.Frame(toplevel)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
    def open_chart_window(self):
        # Child window ကိုဖွင့်ရာတွင် callback ဖန်ရှင်ကိုပေးပို့သည်
        chart_window = ChartWindow(self.toplevel, self.update_chart_data)
        
    def update_chart_data(self, chart_data, calculation_results):
        # Child window မှလာသော data ကိုပြသည်
        # ဒီနေရာတွင် A4 format ဖြင့်ပြသမည့် code ရေးသည်
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        # A4 အချိုးအစားဖြင့် frame ဖန်တီးခြင်း
        a4_frame = tk.Frame(self.chart_frame, width=595, height=842, bg="white")  # A4 pixels (72dpi)
        a4_frame.pack_propagate(False)  # Frame size ကိုမပြောင်းစေရန်
        a4_frame.pack()
        
        # Header
        header_label = tk.Label(a4_frame, text="Chart Results", font=("Pyidaungsu", 16, "bold"))
        header_label.pack(pady=10)
        
        # Chart data
        data_label = tk.Label(a4_frame, text=f"Chart Data: {chart_data}", font=("Pyidaungsu", 12))
        data_label.pack(pady=5, anchor="w")
        
        # Calculation results
        results_label = tk.Label(a4_frame, text="Calculation Results:", font=("Pyidaungsu", 12, "bold"))
        results_label.pack(pady=(10,5), anchor="w")
        
        for key, value in calculation_results.items():
            result_item = tk.Label(a4_frame, text=f"{key}: {value}", font=("Pyidaungsu", 10))
            result_item.pack(anchor="w", padx=20)
        
        # Print button
        print_button = tk.Button(a4_frame, text="Print", command=lambda: self.print_a4(a4_frame))
        print_button.pack(pady=20)
        
    def print_a4(self, frame):
        # Frame ကို PostScript အဖြစ်ပြောင်းခြင်း
        ps = frame.postscript(colormode='color')
        
        # ဖိုင်ကိုရေးသားခြင်း
        with open("chart_output.ps", "w") as f:
            f.write(ps)
        
        # ပုံနှိပ်ခြင်း
        import os
        try:
            os.startfile("chart_output.ps", "print")
        except:
            print("Printing not available on this system")

if __name__ == "__main__":
    toplevel = tk.Tk()
    app = MainWindow(toplevel)
    toplevel.mainloop()