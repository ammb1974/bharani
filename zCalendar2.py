"""
Tkinter app: Gregorian -> Myanmar date converter
Requires: mmcal.py (place in same folder)

Usage: python tk_mm_converter.py

Provides: year/month/day selectors, language toggle (Burmese/English), Convert button,
shows Myanmar date and weekday with moon phase (လဆန်း/လဆုတ်).
"""
import sys
import calendar
import re # Import regex for robust parsing
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Define English month names for the input combobox
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
        if 'import_warning' in globals():
            self.after(100, import_warning)

    def _mm_digit_to_int(self, s):
        """Converts a string of Myanmar digits to an integer."""
        myanmar_digit_map = {'၀':'0','၁':'1','၂':'2','၃':'3','၄':'4','၅':'5','၆':'6','၇':'7','၈':'8','၉':'9'}
        try:
            return int(''.join([myanmar_digit_map.get(d, d) for d in s]))
        except (ValueError, TypeError):
            return -1 # Return -1 on error

    def build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.grid(row=0, column=0, sticky="nsew")

        # Year
        ttk.Label(frm, text="Year:").grid(row=0, column=0, sticky="w")
        self.year_var = tk.IntVar(value=datetime.now().year)
        self.year_spin = ttk.Spinbox(frm, from_=1900, to=3000, textvariable=self.year_var, width=6, command=self.update_days)
        self.year_spin.grid(row=0, column=1, sticky="w")

        # Month - Using English month names for correct Gregorian mapping
        ttk.Label(frm, text="Month:").grid(row=1, column=0, sticky="w")
        self.month_var = tk.StringVar()
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
                # Find month index using monthsEN list for correct Gregorian mapping
                month_index = monthsEN.index(month_name) + 1
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
            # Get month index from monthsEN list for correct Gregorian mapping
            m = monthsEN.index(self.month_var.get()) + 1
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
            self.result_var.set(mm_str)
            self.week_var.set("Weekday: -")
            return

        # --- New logic to add moon phase (လဆန်း/လဆုတ်) ---
        # Use regex to robustly parse month, day, and the rest of the string
        match = re.search(r'(\S+)\s+([၀၁-၉]+|\d+)\s*(.*)', mm_str)
        if match:
            month_name = match.group(1)
            day_str = match.group(2)
            rest_of_str = match.group(3).strip()

            day_num = self._mm_digit_to_int(day_str)

            if day_num > 0:
                # Determine the moon phase in Burmese
                phase = "လဆန်း" if day_num <= 15 else "လဆုတ်"
                
                # Rebuild the string with the phase
                if rest_of_str:
                    new_mm_str = f"{month_name} {phase} {day_str} {rest_of_str}"
                else:
                    new_mm_str = f"{month_name} {phase} {day_str}"
                
                self.result_var.set(new_mm_str)
            else:
                # If day parsing fails, show original string
                self.result_var.set(mm_str)
        else:
            # If format is unexpected, show original string
            self.result_var.set(mm_str)

        # weekday mapping: Python weekday() => Monday=0..Sunday=6
        py_wd = dt.weekday()
        # mmcal.weekDay has index 0=Saturday,1=Sunday,2=Monday ...
        mm_idx = (py_wd + 2) % 7
        weekday_mm = weekDay[mm_idx] if 0 <= mm_idx < len(weekDay) else '-'
        self.week_var.set(f"Weekday: {weekday_mm}")

    def copy_result(self):
        res = self.result_var.get()
        if res and res != "Myanmar date will appear here":
            self.clipboard_clear()
            self.clipboard_append(res)
            messagebox.showinfo("Copied", "Myanmar date copied to clipboard")
        else:
            messagebox.showwarning("Nothing to Copy", "Please convert a date first.")

if __name__ == '__main__':
    app = MyanmarConverterApp()
    app.mainloop()