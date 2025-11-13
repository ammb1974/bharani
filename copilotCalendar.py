import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime
import myanmar_calendar  # pip install myanmar-calendar

def convert_to_myanmar_date():
    eng_date = cal.get_date()
    myanmar_date = myanmar_calendar.from_gregorian(eng_date.year, eng_date.month, eng_date.day)
    result_label.config(text=f"မြန်မာ ရက်စွဲ: {myanmar_date['myanmar_date']}")

root = tk.Tk()
root.title("မြန်မာ ရက်စွဲ ပြောင်းရန်")

tk.Label(root, text="အင်္ဂလိပ် ရက်စွဲ ရွေးပါ").pack(pady=10)
cal = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
cal.pack(pady=5)

tk.Button(root, text="ပြောင်းမယ်", command=convert_to_myanmar_date).pack(pady=10)
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()