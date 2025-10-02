import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class GridApplication:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.chart_data = None  # Will hold the latest chart (dict or list)
        self.setup_ui()

    def setup_ui(self):
        # Main frame for controls
        control_frame = ttk.Frame(self.toplevel)
        control_frame.pack(padx=10, pady=10)

        # Demo buttons
        ttk.Button(
            control_frame,
            text="Single Grid Click Demo",
            command=self.create_single_grid
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            control_frame,
            text="Multiple Grid Demo",
            command=self.create_multiple_grids
        ).pack(side=tk.LEFT, padx=5)

        # Export JSON button
        ttk.Button(
            control_frame,
            text="Export Chart JSON",
            command=lambda: export_to_json(self.chart_data, self.toplevel)
        ).pack(side=tk.LEFT, padx=5)

    def create_single_grid(self):
        # Replace this stub with real astrology logic
        grid = self.generate_grid_data(seed=1)
        self.chart_data = grid
        self.show_grid(grid)

    def create_multiple_grids(self):
        # Example: generate 3 charts
        charts = []
        for i in range(3):
            grid = self.generate_grid_data(seed=i+1)
            charts.append(grid)
            self.show_grid(grid)
        self.chart_data = charts

    def generate_grid_data(self, seed):
        """
        Stub method. Replace with:
          • Calculations for East-Indian style chart
          • Navāṃśa or Dasha divisions
          • City coordinates, timezones, etc.
        """
        return {
            "chart_id": seed,
            "signs": ["Aries", "Taurus", "Gemini", "Cancer"],
            "placements": {
                "Sun": "Aries",
                "Moon": "Cancer"
            }
        }

    def show_grid(self, data):
        """
        Stub visualization. Hook into your SVG/matplotlib code or
        Tkinter Canvas drawing routines here.
        """
        print("Displaying grid:", data)


def export_to_json(data, parent):
    """
    Opens a Save As dialog, writes `data` as pretty-printed JSON
    with UTF-8 encoding, and shows a success/error message.
    """
    if data is None:
        messagebox.showwarning(
            "Nothing to Export",
            "Please generate a chart before exporting."
        )
        return

    file_path = filedialog.asksaveasfilename(
        parent=parent,
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        initialfile="astrology_chart_data.json"
    )
    if not file_path:
        return  # User cancelled

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo(
            "Export Successful",
            f"Chart exported to:\n{file_path}"
        )
    except Exception as e:
        messagebox.showerror("Export Failed", str(e))


if __name__ == "__main__":
    toplevel = tk.Tk()
    toplevel.title("Burmese Astrology Chart Generator")
    app = GridApplication(toplevel)
    toplevel.mainloop()