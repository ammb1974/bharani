# Child.py
import tkinter as tk

def open_child_window(parent_root):
    # Toplevel window ဖန်တီး
    child_window = tk.Toplevel(parent_root)
    child_window.title("Child Window")
    child_window.geometry("550x600")

    # Parent ရဲ့ center မှာ ပေါ်အောင် တွက်ချက်
    parent_x = parent_root.winfo_x()
    parent_y = parent_root.winfo_y()
    parent_width = parent_root.winfo_width()
    parent_height = parent_root.winfo_height()

    # Child အလယ်ချိန်ညှိ
    x = parent_x + (parent_width // 2) - (550 // 2)
    y = parent_y + (parent_height // 2) - (600 // 2)

    child_window.geometry(f"550x600+{x}+{y}")
    child_window.grab_set()  # Modal behavior
    child_window.tk_strictMotif(True)  # Strict Motif style

    child_window.transient(parent_root)  # Parent window အပေါ်မှာပေါ်အောင်

    # ဥပမာ - label တစ်ခုထည့်ပါမယ်
    label = tk.Label(child_window, text="This is Child Window", font=("Myanmar Text", 16))
    label.pack(expand=True)

    return child_window