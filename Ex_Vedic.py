# Parent.py
import tkinter as tk
from Ex_newBuild import open_child_window  # Child.py က function ကို import

def open_child():
    open_child_window(root)  # Parent root ကို ပေးပို့

# Main Parent Window
root = tk.Tk()
root.title("Parent Window")
#root.attributes('-fullscreen', True)  # Fullscreen
root.configure(bg='white')  
root.state('zoomed')  # Maximized
root.minsize(1024, 768  )

# Button to open child window
btn = tk.Button(root, text="Open Child Window", command=open_child, font=("Pyidaungsu", 14))
btn.pack(expand=True)

root.mainloop()