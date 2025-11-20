"""
Tkinter app: Gregorian -> Myanmar date converter
Requires: mmcal.py (place in same folder)

Usage: python tk_mm_converter.py

Provides: year/month/day selectors, language toggle (Burmese/English), Convert button,
shows Myanmar date and weekday.
"""
import sys
import calendar
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Define English month names
monthsEN = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

# Try importing mmcal (user's provided file)
try:
    from mmcal import to_myanmar, monthsMM, months, weekDay
except Exception as e:
    message = (
        "Could not import mmcal.py.\n"
        "Make sure mmcal.py is in the same folder as this script and is importable.\n"
        f"Import error: {e}"
    )
    # Minimal fallback so the module still starts but conversion won't work
    def to_myanmar(dt, lang='mm'):
        return "(mmcal not available)"
    monthsMM = ["", "ပဝါဆို", "တန်ခူး", "ကဆုန်", "နယုန်", "ဝါဆို", "ဝါခေါင်",
                "တော်သလင်း", "သီတင်းကျွတ်", "တန်ဆောင်မုန်း", "နတ်တော်", "ပြာသို", "တပို့တွဲ", "တပေါင်း"]
    months = ["", 'January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    weekDay = ["စနေနေ့", "တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ကြာသာပတေး", "သောကြာ"]

    # show warning after GUI loads
    def import_warning():
        messagebox.showwarning("Import warning", message)

class MyanmarConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gregorian → Myanmar Date Converter")
        self.resizable(False, False)
        self.build_ui()
        # if mmcal failed import, warn user
        if 'Import warning' in globals():
            self.after(100, import_warning)

    def build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.grid(row=0, column=0, sticky="nsew")

        # Year
        ttk.Label(frm, text="Year:").grid(row=0, column=0, sticky="w")
        self.year_var = tk.IntVar(value=datetime.now().year)
        self.year_spin = ttk.Spinbox(frm, from_=1900, to=3000, textvariable=self.year_var, width=6, command=self.update_days)
        self.year_spin.grid(row=0, column=1, sticky="w")

        # Month - Using English month names
        ttk.Label(frm, text="Month:").grid(row=1, column=0, sticky="w")
        self.month_var = tk.StringVar()
        # Use monthsEN instead of months from mmcal
        self.month_cb = ttk.Combobox(frm, values=monthsEN, state="readonly", textvariable=self.month_var, width=12)
        self.month_cb.current(datetime.now().month - 1)
        self.month_cb.grid(row=1, column=1, sticky="w")
        self.month_cb.bind('<<ComboboxSelected>>', lambda e: self.update_days())

        # Day
        ttk.Label(frm, text="Day:").grid(row=2, column=0, sticky="w")
        self.day_var = tk.IntVar(value=datetime.now().day)
        self.day_cb = ttk.Combobox(frm, values=list(range(1,32)), state="readonly", textvariable=self.day_var, width=4)
        self.day_cb.grid(row=2, column=1, sticky="w")

        # Language (mm / en)
        ttk.Label(frm, text="Output language:").grid(row=3, column=0, sticky="w")
        self.lang_var = tk.StringVar(value='mm')
        lang_frame = ttk.Frame(frm)
        lang_frame.grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(lang_frame, text="Burmese", variable=self.lang_var, value='mm').pack(side='left')
        ttk.Radiobutton(lang_frame, text="English", variable=self.lang_var, value='en').pack(side='left')

        # Convert button
        self.convert_btn = ttk.Button(frm, text="Convert →", command=self.convert)
        self.convert_btn.grid(row=4, column=0, columnspan=2, pady=(8, 4))

        # Result display
        self.result_var = tk.StringVar(value="Myanmar date will appear here")
        self.result_lbl = ttk.Label(frm, textvariable=self.result_var, font=(None, 11, 'bold'))
        self.result_lbl.grid(row=5, column=0, columnspan=2, pady=(6,0))

        # Weekday display
        self.week_var = tk.StringVar(value="Weekday: -")
        self.week_lbl = ttk.Label(frm, textvariable=self.week_var)
        self.week_lbl.grid(row=6, column=0, columnspan=2)

        # Copy to clipboard
        self.copy_btn = ttk.Button(frm, text="Copy Result", command=self.copy_result)
        self.copy_btn.grid(row=7, column=0, columnspan=2, pady=(6,0))

        # initialize day list correctly
        self.update_days()

    def update_days(self):
        try:
            y = int(self.year_var.get())
        except Exception:
            y = datetime.now().year
        month_name = self.month_var.get()
        if not month_name:
            month_index = datetime.now().month
        else:
            try:
                # Find month index using monthsEN list
                month_index = monthsEN.index(month_name) + 1  # +1 because monthsEN is 0-indexed
            except ValueError:
                month_index = datetime.now().month
        days_in_month = calendar.monthrange(y, month_index)[1]
        self.day_cb['values'] = list(range(1, days_in_month + 1))
        # clamp current day
        cur = int(self.day_var.get()) if self.day_var.get() else 1
        if cur > days_in_month:
            self.day_var.set(days_in_month)

    def convert(self):
        try:
            y = int(self.year_var.get())
            # Get month index from monthsEN list
            m = monthsEN.index(self.month_var.get()) + 1  # +1 because monthsEN is 0-indexed
            d = int(self.day_var.get())
        except Exception:
            messagebox.showerror("Input error", "Please enter a valid year, month and day")
            return
        try:
            dt = datetime(y, m, d)
        except ValueError:
            messagebox.showerror("Date error", "Invalid Gregorian date")
            return

        # get myanmar date string
        try:
            mm_str = to_myanmar(dt, lang=self.lang_var.get())
        except Exception as e:
            mm_str = f"Conversion error: {e}"

        # weekday mapping: Python weekday() => Monday=0..Sunday=6
        py_wd = dt.weekday()
        # mmcal.weekDay has index 0=Saturday,1=Sunday,2=Monday ...
        mm_idx = (py_wd + 2) % 7
        weekday_mm = weekDay[mm_idx] if 0 <= mm_idx < len(weekDay) else '-'

        self.result_var.set(mm_str)
        self.week_var.set(f"Weekday: {weekday_mm}")

    def copy_result(self):
        res = self.result_var.get()
        if res:
            self.clipboard_clear()
            self.clipboard_append(res)
            messagebox.showinfo("Copied", "Myanmar date copied to clipboard")

if __name__ == '__main__':
    app = MyanmarConverterApp()
    app.mainloop()