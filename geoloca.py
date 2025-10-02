import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime
import csv
import os

class BirthInfoApp:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("မွေးဖွားမှတ်တမ်းစနစ်")  # "Birth Information System" in Myanmar
        self.toplevel.geometry("650x550")
        
        # Set Myanmar font for the entire application
        try:
            self.my_font = font.Font(family="Myanmar Text", size=10)
            self.my_bold_font = font.Font(family="Myanmar Text", size=10, weight="bold")
        except:
            self.my_font = font.Font(family="Pyidaungsu", size=10)
            self.my_bold_font = font.Font(family="Pyidaungsu", size=10, weight="bold")
            messagebox.showwarning("သတိပြုရန်", "Myanmar Text font မတွေ့ပါ။ Pyidaungsu font ကိုအစားသုံးထားပါသည်။")
        
        # Apply font to all widgets
        self.toplevel.option_add("*Font", self.my_font)
        
        # Data storage
        self.records = []
        self.load_records()
        
        # Variables
        self.day_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.hour_var = tk.StringVar(value="00")
        self.minute_var = tk.StringVar(value="00")
        self.state_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.lat_var = tk.StringVar()
        self.lon_var = tk.StringVar()
        self.lat_dir_var = tk.StringVar(value="မြောက်")  # "North" in Myanmar
        self.lon_dir_var = tk.StringVar(value="အရှေ့")  # "East" in Myanmar
        self.timezone_var = tk.StringVar()
        self.dst_var = tk.BooleanVar(value=False)
        
        # Create widgets
        self.create_widgets()
        
        # Update days when month changes
        self.month_var.trace_add('write', self.update_days)
        self.year_var.trace_add('write', self.update_days)
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.toplevel, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Date of Birth Section
        dob_frame = ttk.LabelFrame(main_frame, text="မွေးနေ့", padding="10")  # "Date of Birth"
        dob_frame.pack(fill=tk.X, pady=5)
        
        # Month combobox
        ttk.Label(dob_frame, text="လ:").grid(row=0, column=0, sticky=tk.W)  # "Month"
        months = ["ဇန်နဝါရီ", "ဖေဖော်ဝါရီ", "မတ်", "ဧပြီ", "မေ", "ဇွန်", 
                 "ဇူလိုင်", "ဩဂုတ်", "စက်တင်ဘာ", "အောက်တိုဘာ", "နိုဝင်ဘာ", "ဒီဇင်ဘာ"]
        month_cb = ttk.Combobox(dob_frame, textvariable=self.month_var, values=months, state="readonly")
        month_cb.grid(row=0, column=1, sticky=tk.W)
        month_cb.current(0)
        
        # Day combobox
        ttk.Label(dob_frame, text="ရက်:").grid(row=0, column=2, padx=(10,0), sticky=tk.W)  # "Day"
        self.day_cb = ttk.Combobox(dob_frame, textvariable=self.day_var, state="readonly")
        self.day_cb.grid(row=0, column=3, sticky=tk.W)
        self.update_days()
        
        # Year combobox
        ttk.Label(dob_frame, text="နှစ်:").grid(row=0, column=4, padx=(10,0), sticky=tk.W)  # "Year"
        years = [str(y) for y in range(1900, 2051)]
        year_cb = ttk.Combobox(dob_frame, textvariable=self.year_var, values=years, state="readonly")
        year_cb.grid(row=0, column=5, sticky=tk.W)
        year_cb.current(50)  # Default to 1950
        
        # Time Section
        time_frame = ttk.LabelFrame(main_frame, text="အချိန် (ဒေသစံတော်ချိန်)", padding="10")  # "Time (local time)"
        time_frame.pack(fill=tk.X, pady=5)
        
        # Hour combobox
        ttk.Label(time_frame, text="နာရီ:").grid(row=0, column=0, sticky=tk.W)  # "Hour"
        hours = [f"{h:02d}" for h in range(24)]
        hour_cb = ttk.Combobox(time_frame, textvariable=self.hour_var, values=hours, state="readonly")
        hour_cb.grid(row=0, column=1, sticky=tk.W)
        
        # Minute combobox
        ttk.Label(time_frame, text="မိနစ်:").grid(row=0, column=2, padx=(10,0), sticky=tk.W)  # "Minute"
        minutes = [f"{m:02d}" for m in range(60)]
        minute_cb = ttk.Combobox(time_frame, textvariable=self.minute_var, values=minutes, state="readonly")
        minute_cb.grid(row=0, column=3, sticky=tk.W)
        
        # State and City Section
        state_city_frame = ttk.LabelFrame(main_frame, text="မွေးရပ်ဒေသ", padding="10")  # "Birth Place"
        state_city_frame.pack(fill=tk.X, pady=5)
        
        # State entry
        ttk.Label(state_city_frame, text="တိုင်းဒေသကြီး/ပြည်နယ်:").grid(row=0, column=0, sticky=tk.W)  # "State/Region"
        state_entry = ttk.Entry(state_city_frame, textvariable=self.state_var)
        state_entry.grid(row=0, column=1, sticky=tk.EW, columnspan=4, padx=(0,5))
        
        # City entry
        ttk.Label(state_city_frame, text="မြို့:").grid(row=1, column=0, sticky=tk.W)  # "City"
        city_entry = ttk.Entry(state_city_frame, textvariable=self.city_var)
        city_entry.grid(row=1, column=1, sticky=tk.EW, columnspan=3, padx=(0,5))
        
        # Search button
        search_btn = ttk.Button(state_city_frame, text="ရှာဖွေရန်", command=self.search_location)  # "Search"
        search_btn.grid(row=1, column=4, padx=(5,0))
        
        # Coordinates Section
        coord_frame = ttk.Frame(main_frame)
        coord_frame.pack(fill=tk.X, pady=5)
        
        # Latitude
        ttk.Label(coord_frame, text="လတ္တီကျု:").grid(row=0, column=0, sticky=tk.W)  # "Latitude"
        lat_entry = ttk.Entry(coord_frame, textvariable=self.lat_var, width=10)
        lat_entry.grid(row=0, column=1, sticky=tk.W)
        
        lat_dir_cb = ttk.Combobox(coord_frame, textvariable=self.lat_dir_var, 
                                 values=["မြောက်", "တောင်"], state="readonly", width=6)  # "North", "South"
        lat_dir_cb.grid(row=0, column=2, padx=(5,0), sticky=tk.W)
        
        # Longitude
        ttk.Label(coord_frame, text="လောင်ဂျီကျု:").grid(row=0, column=3, padx=(10,0), sticky=tk.W)  # "Longitude"
        lon_entry = ttk.Entry(coord_frame, textvariable=self.lon_var, width=10)
        lon_entry.grid(row=0, column=4, sticky=tk.W)
        
        lon_dir_cb = ttk.Combobox(coord_frame, textvariable=self.lon_dir_var, 
                                 values=["အရှေ့", "အနောက်"], state="readonly", width=6)  # "East", "West"
        lon_dir_cb.grid(row=0, column=5, padx=(5,0), sticky=tk.W)
        
        # Timezone Section
        tz_frame = ttk.Frame(main_frame)
        tz_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(tz_frame, text="အချိန်ဇုံ:").grid(row=0, column=0, sticky=tk.W)  # "Timezone"
        tz_entry = ttk.Entry(tz_frame, textvariable=self.timezone_var, width=15)
        tz_entry.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Checkbutton(tz_frame, text="နေ့အလင်းရောင်ထိန်းသိမ်းချိန်", variable=self.dst_var).grid(row=0, column=2, padx=(10,0))  # "Daylight Saving Time"
        
        # Buttons Frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        save_btn = ttk.Button(btn_frame, text="သိမ်းဆည်းရန်", command=self.save_record)  # "Save Record"
        save_btn.pack(side=tk.LEFT, padx=5)
        
        new_btn = ttk.Button(btn_frame, text="မှတ်တမ်းအသစ်", command=self.new_record)  # "New Record"
        new_btn.pack(side=tk.LEFT, padx=5)
        
        # Records List
        records_frame = ttk.LabelFrame(main_frame, text="သိမ်းဆည်းထားသောမှတ်တမ်းများ", padding="10")  # "Saved Records"
        records_frame.pack(fill=tk.BOTH, expand=True)
        
        self.records_list = tk.Listbox(records_frame, font=self.my_font)
        self.records_list.pack(fill=tk.BOTH, expand=True)
        self.records_list.bind('<<ListboxSelect>>', self.load_selected_record)
        
        # Update records list
        self.update_records_list()
        
    def update_days(self, *args):
        month = self.month_var.get()
        year = self.year_var.get()
        
        if not month or not year:
            return
            
        try:
            year_int = int(year)
        except ValueError:
            return
            
        month_num = ["ဇန်နဝါရီ", "ဖေဖော်ဝါရီ", "မတ်", "ဧပြီ", "မေ", "ဇွန်", 
                    "ဇူလိုင်", "ဩဂုတ်", "စက်တင်ဘာ", "အောက်တိုဘာ", "နိုဝင်ဘာ", "ဒီဇင်ဘာ"].index(month) + 1
        
        # Handle February with leap years
        if month_num == 2:
            if (year_int % 400 == 0) or (year_int % 100 != 0 and year_int % 4 == 0):
                days = 29
            else:
                days = 28
        elif month_num in [4, 6, 9, 11]:
            days = 30
        else:
            days = 31
            
        day_values = [str(d) for d in range(1, days+1)]
        self.day_cb['values'] = day_values
        if not self.day_var.get() or int(self.day_var.get()) > days:
            self.day_var.set("1")
            
    def search_location(self):
        state = self.state_var.get()
        city = self.city_var.get()
        if not city:
            messagebox.showwarning("သတိပြုရန်", "မြို့အမည်ထည့်သွင်းပါ")  # "Please enter a city name"
            return
            
        try:
            geolocator = Nominatim(user_agent="birth_info_app")
            location_query = f"{city}, {state}" if state else city
            location = geolocator.geocode(location_query)
            
            if location:
                self.lat_var.set(str(round(location.latitude, 6)))
                self.lon_var.set(str(round(location.longitude, 6)))
                
                # Set direction comboboxes
                self.lat_dir_var.set("မြောက်" if location.latitude >= 0 else "တောင်")  # "North"/"South"
                self.lon_dir_var.set("အရှေ့" if location.longitude >= 0 else "အနောက်")  # "East"/"West"
                
                # Get timezone
                tf = TimezoneFinder()
                timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
                if timezone_str:
                    tz = pytz.timezone(timezone_str)
                    now = datetime.now(tz)
                    utc_offset = now.utcoffset().total_seconds() / 3600
                    self.timezone_var.set(f"UTC{'+' if utc_offset >=0 else ''}{utc_offset:.1f}")
            else:
                messagebox.showwarning("သတိပြုရန်", "တည်နေရာမတွေ့ပါ။ လတ္တီကျု/လောင်ဂျီကျုကိုကိုယ်တိုင်ထည့်ပါ။")  # "Location not found. Please enter coordinates manually."
        except Exception as e:
            messagebox.showerror("အမှား", f"တည်နေရာရှာဖွေရာတွင်အမှားဖြစ်သည်: {str(e)}")  # "Error in location search"
            
    def save_record(self):
        # Validate data
        if not all([self.day_var.get(), self.month_var.get(), self.year_var.get(),
                   self.city_var.get(), self.lat_var.get(), self.lon_var.get()]):
            messagebox.showwarning("သတိပြုရန်", "လိုအပ်သောအချက်အလက်အားလုံးကိုဖြည့်ပါ")  # "Please fill in all required fields"
            return
            
        try:
            # Convert coordinates to decimal with direction
            lat = float(self.lat_var.get())
            lon = float(self.lon_var.get())
            
            if self.lat_dir_var.get() == "တောင်":  # "South"
                lat = -lat
            if self.lon_dir_var.get() == "အနောက်":  # "West"
                lon = -lon
                
            # Create record
            record = {
                "day": self.day_var.get(),
                "month": self.month_var.get(),
                "year": self.year_var.get(),
                "hour": self.hour_var.get(),
                "minute": self.minute_var.get(),
                "state": self.state_var.get(),
                "city": self.city_var.get(),
                "latitude": lat,
                "longitude": lon,
                "timezone": self.timezone_var.get(),
                "dst": self.dst_var.get()
            }
            
            # Add or update record
            if hasattr(self, 'selected_index'):
                self.records[self.selected_index] = record
            else:
                self.records.append(record)
                
            self.save_records()
            self.save_to_csv(record)  # Save to CSV file
            self.update_records_list()
            self.new_record()  # Clear form
            
            messagebox.showinfo("အောင်မြင်", "မှတ်တမ်းသိမ်းဆည်းပြီးပါပြီ")  # "Record saved successfully"
        except ValueError:
            messagebox.showerror("အမှား", "လတ္တီကျု သို့မဟုတ် လောင်ဂျီကျု တန်ဖိုးမမှန်ပါ")  # "Invalid latitude or longitude value"
            
    def save_to_csv(self, record):
        file_path = "CityData.csv"
        file_exists = os.path.isfile(file_path)
        
        try:
            with open(file_path, mode='a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['day', 'month', 'year', 'hour', 'minute', 'state', 'city', 
                            'latitude', 'longitude', 'timezone', 'dst']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(record)
        except Exception as e:
            messagebox.showerror("အမှား", f"CSV ဖိုင်သိမ်းဆည်းရာတွင်အမှားဖြစ်သည်: {str(e)}")  # "Error saving to CSV file"
            
    def new_record(self):
        # Clear all fields
        self.day_var.set("1")
        self.month_var.set("ဇန်နဝါရီ")  # "January"
        self.year_var.set("1950")
        self.hour_var.set("00")
        self.minute_var.set("00")
        self.state_var.set("")
        self.city_var.set("")
        self.lat_var.set("")
        self.lon_var.set("")
        self.lat_dir_var.set("မြောက်")  # "North"
        self.lon_dir_var.set("အရှေ့")  # "East"
        self.timezone_var.set("")
        self.dst_var.set(False)
        
        if hasattr(self, 'selected_index'):
            del self.selected_index
            
    def load_selected_record(self, event):
        selection = self.records_list.curselection()
        if not selection:
            return
            
        index = selection[0]
        self.selected_index = index
        record = self.records[index]
        
        # Load data into form
        self.day_var.set(record['day'])
        self.month_var.set(record['month'])
        self.year_var.set(record['year'])
        self.hour_var.set(record['hour'])
        self.minute_var.set(record['minute'])
        self.state_var.set(record.get('state', ''))  # Handle older records without state
        self.city_var.set(record['city'])
        
        # Handle coordinates
        lat = record['latitude']
        lon = record['longitude']
        
        self.lat_var.set(str(abs(lat)))
        self.lon_var.set(str(abs(lon)))
        self.lat_dir_var.set("မြောက်" if lat >= 0 else "တောင်")  # "North"/"South"
        self.lon_dir_var.set("အရှေ့" if lon >= 0 else "အနောက်")  # "East"/"West"
        
        self.timezone_var.set(record['timezone'])
        self.dst_var.set(record['dst'])
        
    def update_records_list(self):
        self.records_list.delete(0, tk.END)
        for i, record in enumerate(self.records):
            display_text = f"{record['day']} {record['month']} {record['year']} - {record.get('state', '')} {record['city']}"
            self.records_list.insert(tk.END, display_text)
            
    def save_records(self):
        with open('birth_records.json', 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False)
            
    def load_records(self):
        try:
            with open('birth_records.json', 'r', encoding='utf-8') as f:
                self.records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.records = []
            
if __name__ == "__main__":
    toplevel = tk.Tk()
    app = BirthInfoApp(toplevel)
    toplevel.mainloop()