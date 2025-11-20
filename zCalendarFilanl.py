"""
Tkinter app: Gregorian -> Myanmar date converter
Requires: mmcal.py (place in same folder)

Usage: python tk_mm_converter.py

Provides: year/month/day selectors, language toggle (Burmese/English), Convert button,
shows Myanmar date, weekday, and moon age (လရုပ်).
Handles intercalary months (e.g., ဒုတိယ ဝါဆို) and special days (လပြည့်/လကွယ်).
"""
import sys
import calendar
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
    # This 'months' list is a fallback for English Myanmar month names
    months = ["", "Tagu", "Kason", "Nayon", "Waso", "Wagaung", "Second Wagaung", "Tawthalin", "Thadingyut", "Tazaungmon", "Nadaw", "Pyatho", "Tabodwe", "Tabaung"]
    weekDay = ["စနေနေ့", "တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ကြာသာပတေး", "သောကြာ"]

    # show warning after GUI loads
    def import_warning():
        messagebox.showwarning("Import warning", message)

class MyanmarConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gregorian → Myanmar Date Converter")
        self.resizable(False, False)

        # --- Create a map for Myanmar month names (English to Burmese) ---
        self.mm_month_map = {}
        if 'months' in globals() and 'monthsMM' in globals():
            # The first element is usually a placeholder, so we start from index 1
            self.mm_month_map = {en: mm for en, mm in zip(months[1:], monthsMM[1:])}

        self.build_ui()
        # if mmcal failed import, warn user
        if 'import_warning' in globals():
            self.after(100, import_warning)

    def _int_to_mm_digit(self, n):
        """Converts an integer to a string of Myanmar digits."""
        myanmar_digits = "၀၁၂၃၄၅၆၇၈၉"
        return ''.join([myanmar_digits[int(d)] for d in str(n)])

    def _en_month_to_mm(self, en_month):
        """
        Maps English Myanmar month name to Burmese month name, 
        including intercalary months, with robust parsing.
        """
        # Check for intercalary months (e.g., "First Waso", "Second Wagaung")
        if en_month.startswith('First') or en_month.startswith('Second'):
            prefix_map = {'First': 'ပထမ', 'Second': 'ဒုတိယ'}
            prefix = 'First' if en_month.startswith('First') else 'Second'
            base_month = en_month.replace(f'{prefix} ', '')
            # Get the Burmese name for the base month (e.g., "Waso" -> "ဝါဆို")
            mm_base_month = self.mm_month_map.get(base_month, base_month)
            return f'{prefix_map[prefix]} {mm_base_month}'
        
        # Then use the generated map for standard months
        return self.mm_month_map.get(en_month, en_month) # Fallback to original if not found

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

        # Language (mm / en) - Note: Output is now fixed to Burmese format
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

        # Moon Age display
        self.moon_age_var = tk.StringVar(value="လရုပ်: -")
        self.moon_age_lbl = ttk.Label(frm, textvariable=self.moon_age_var)
        self.moon_age_lbl.grid(row=7, column=0, columnspan=2)

        # Copy to clipboard
        self.copy_btn = ttk.Button(frm, text="Copy Result", command=self.copy_result)
        self.copy_btn.grid(row=8, column=0, columnspan=2, pady=(6,0))

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

        # --- REVISED LOGIC FOR FULL MOON AND NEW MOON ---
        try:
            # 1. Get the English version. Expected format: "Day MonthName, YearNumber"
            en_str = to_myanmar(dt, lang='en')
            parts = en_str.replace(',', '').split()
            
            if len(parts) >= 3:
                day_num_str = parts[0]
                year_num_str = parts[-1]
                # Month name is everything in between
                en_month = ' '.join(parts[1:-1])
            else:
                self.result_var.set(f"Error: Could not parse date from '{en_str}'")
                self.moon_age_var.set("လရုပ်: -")
                return

            # 2. Convert components
            mm_month = self._en_month_to_mm(en_month) # Using the robust function
            mm_year_num_str = self._int_to_mm_digit(int(year_num_str))
            
            # 3. Calculate phase and day from the cumulative day number
            cumulative_day = int(day_num_str)
            mm_cumulative_day_str = self._int_to_mm_digit(cumulative_day)
            
            final_str = ""
            # Special cases for Full Moon and New Moon
            if cumulative_day == 15:
                # Full Moon Day
                final_str = f"{mm_month} လပြည့်နေ့ {mm_year_num_str}"
            elif cumulative_day > 15:
                waning_day = cumulative_day - 15
                if waning_day >= 14: # Covers both 14 and 15 waning days
                    # New Moon Day
                    final_str = f"{mm_month} လကွယ်နေ့ {mm_year_num_str}"
                else:
                    # Regular Waning Day
                    mm_phase = "လဆုတ်"
                    mm_day_str = self._int_to_mm_digit(waning_day)
                    final_str = f"{mm_month} {mm_phase} {mm_day_str} ရက် {mm_year_num_str}"
            else: # cumulative_day < 15
                # Regular Waxing Day
                mm_phase = "လဆန်း"
                mm_day_str = self._int_to_mm_digit(cumulative_day)
                final_str = f"{mm_month} {mm_phase} {mm_day_str} ရက် {mm_year_num_str}"
            
            self.result_var.set(final_str)
            self.moon_age_var.set(f"လရုပ်: {mm_cumulative_day_str} ရက်")
                
        except Exception as e:
            # If anything else fails, show the error
            self.result_var.set(f"Error during conversion: {e}")
            self.moon_age_var.set("လရုပ်: -")

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