import json
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox

from CMap import DrawGrid  # သင့်ရဲ့ grid drawing logic

class GridEditor(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Myanmar Grid Editor")
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        self.status_label = tk.Label(self, text="", anchor="w")
        self.status_label.pack(fill="x", pady=(5,0))

        ctrl = tk.Frame(self)
        ctrl.pack(pady=10)
        tk.Button(ctrl, text="Open JSON", command=self.load_json).pack(side="left", padx=5)
        tk.Button(ctrl, text="Save JSON", command=self.save_json).pack(side="left", padx=5)
        tk.Button(ctrl, text="Draw Grid", command=self.draw_grid).pack(side="left", padx=5)

        edit = tk.Frame(self)
        edit.pack(pady=5)
        tk.Label(edit, text="Center X").grid(row=0, column=0)
        self.cx_entry = tk.Entry(edit, width=5)
        self.cx_entry.grid(row=0, column=1)
        self.cx_entry.insert(0, "150")

        tk.Label(edit, text="Center Y").grid(row=0, column=2)
        self.cy_entry = tk.Entry(edit, width=5)
        self.cy_entry.grid(row=0, column=3)
        self.cy_entry.insert(0, "150")

        tk.Label(edit, text="Cell Size").grid(row=1, column=0)
        self.cell_entry = tk.Entry(edit, width=5)
        self.cell_entry.grid(row=1, column=1)
        self.cell_entry.insert(0, "50")

        tk.Label(edit, text="Color").grid(row=1, column=2)
        self.color_entry = tk.Entry(edit, width=8)
        self.color_entry.grid(row=1, column=3)
        self.color_entry.insert(0, "black")

        self.mapping_data = {}
        self.hover_labels = {}

    def draw_grid(self):
        try:
            cx = int(self.cx_entry.get())
            cy = int(self.cy_entry.get())
            cell = int(self.cell_entry.get())
            color = self.color_entry.get()

            self.canvas.delete("all")
            DrawGrid(self.canvas, center_x=cx, center_y=cy, cell_size=cell, color=color)

            self.hover_labels.clear()

            for cell_data in self.mapping_data.get("cells", []):
                gx = cell_data["x"]
                gy = cell_data["y"]
                rasi = cell_data.get("rasi", "")
                highlight = cell_data.get("highlight", False)

                x1 = cx + gx * cell
                y1 = cy + gy * cell
                x2 = x1 + cell
                y2 = y1 + cell

                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color)
                if highlight:
                    self.canvas.itemconfig(rect, fill="lightyellow")

                self.hover_labels[rect] = rasi

            self.canvas.bind("<Motion>", self.on_hover)
            self.status_label.config(text="Grid ဆွဲပြီးပါပြီ")

        except Exception as e:
            messagebox.showerror("DrawGrid Error", str(e))

    def on_hover(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        rasi = self.hover_labels.get(item[0], "")
        self.status_label.config(text=f"Rasi: {rasi}" if rasi else "")

    def load_json(self):
        file_path = filedialog.askopenfilename(
            title="JSON ဖိုင်ရွေးပါ",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except Exception as e:
            print(traceback.format_exc())
            messagebox.showerror("ဖိုင်ဖွင့်ရာ အမှား", str(e))
            return

        self.mapping_data = data
        self.cx_entry.delete(0, tk.END)
        self.cx_entry.insert(0, str(data.get("center_x", 150)))
        self.cy_entry.delete(0, tk.END)
        self.cy_entry.insert(0, str(data.get("center_y", 150)))
        self.cell_entry.delete(0, tk.END)
        self.cell_entry.insert(0, str(data.get("cell_size", 50)))
        self.color_entry.delete(0, tk.END)
        self.color_entry.insert(0, data.get("color", "blue"))

        self.draw_grid()
        self.status_label.config(text=f"{file_path} မှ ဖတ်ပြီး ဆွဲပြီးပါပြီ")

    def save_json(self):
        try:
            data = {
                "center_x": int(self.cx_entry.get()),
                "center_y": int(self.cy_entry.get()),
                "cell_size": int(self.cell_entry.get()),
                "color": self.color_entry.get(),
                "cells": self.mapping_data.get("cells", [])
            }
            file_path = filedialog.asksaveasfilename(
                title="Save JSON",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if not file_path:
                return

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.status_label.config(text=f"{file_path} သို့ သိမ်းပြီးပါပြီ")
            messagebox.showinfo("အောင်မြင်မှု", "JSON ဖိုင်သိမ်းပြီးပါပြီ")
        except Exception as e:
            messagebox.showerror("သိမ်းဆည်းရာ အမှား", str(e))

if __name__ == "__main__":
    toplevel = tk.Tk()
    app = GridEditor(toplevel)
    toplevel.mainloop()