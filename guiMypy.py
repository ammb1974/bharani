import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# CSV ဖတ်ခြင်း
df = pd.read_csv('dataCSV.csv', encoding='utf-8')

# Data cleaning
df['TownName'] = df['TownName'].fillna('').str.strip()
df['SRName'] = df['SRName'].fillna('').str.strip()
df['Latitude'] = df['Latitude'].fillna('0.0').astype(str).str.strip()
df['Longitude'] = df['Longitude'].fillna('0.0').astype(str).str.strip()

# Valid rows only
df = df[(df['TownName'] != '') & (df['SRName'] != '')]

# Unique states
states = sorted(df['SRName'].unique().tolist())

# Town data dictionary
town_data = {
    row['TownName']: {
        'state': row['SRName'],
        'lat': row['Latitude'],
        'lon': row['Longitude']
    }
    for _, row in df.iterrows()
}

# GUI setup
toplevel = tk.Tk()
toplevel.title("မွေးဖွားဇာတာ တွက်ရန်")
toplevel.iconbitmap('VediIcon.ico')
toplevel.geometry("600x500")

# မြန်မာစာအတွက် Font သတ်မှတ်ခြင်း
myanmar_font = ('Pyidaungsu', 12)  # သို့မဟုတ် ('Noto Sans Myanmar', 12)

# ကော်လံများကို ညီမျှစေရန် ပြင်ဆင်ခြင်း
toplevel.grid_columnconfigure(0, weight=0)  # ဘယ်ဘက်ကော်လံ (Label)
toplevel.grid_columnconfigure(1, weight=1)  # ညာဘက်ကော်လံ (Entry/ComboBox)

# Style ဖန်တီးခြင်း
style = ttk.Style()
style.configure('Myanmar.TLabelframe.Label', font=myanmar_font)  # LabelFrame ရဲ့ label အတွက်
style.configure('Myanmar.TLabelframe', font=myanmar_font)  # LabelFrame အတွက်

# Edit mode flag
edit_mode = False

# Function to toggle edit mode
def toggle_edit_mode():
    global edit_mode
    edit_mode = not edit_mode
    
    if edit_mode:
        # Edit mode ဖွင့်ခြင်း
        # State နဲ့ Town ကို disable လုပ်ခြင်း
        state_combo.config(state="disabled")
        town_combo.config(state="disabled")
        
        # Label တွေကို ဖျောက်ခြင်း
        lat_value.grid_remove()
        lon_value.grid_remove()
        
        # Entry တွေကို ပြခြင်း
        lat_entry.grid()
        lon_entry.grid()
        
        # Entry တွေမှာ လက်ရှိတန်ဖိုးထည့်ပေးခြင်း
        lat_entry.delete(0, tk.END)
        lat_entry.insert(0, lat_value.get())
        lon_entry.delete(0, tk.END)
        lon_entry.insert(0, lon_value.get())
        
        # Direction buttons ကို enable လုပ်ခြင်း
        lat_nvalue.config(state="normal")
        lon_svalue.config(state="normal")
        
        # Button ကို Save ပြောင်းခြင်း
        edit_button.config(text="Save")
    else:
        # Save mode ဖွင့်ခြင်း
        # Entry တွေကနေ တန်ဖိုးယူခြင်း
        new_lat = lat_entry.get()
        new_lon = lon_entry.get()
        
        # တန်ဖိုးမှန်မမှန် စစ်ဆေးခြင်း
        try:
            float(new_lat)
            float(new_lon)
        except ValueError:
            messagebox.showerror("အမှား", "လတ္တီကျူ/လောင်ဂျီကျူ မှန်ကန်စွာ ဖြည့်ပါ")
            # Edit mode ပြန်ဖွင့်ခြင်း
            toggle_edit_mode()
            return
        
        # Town data ကို update လုပ်ခြင်း
        selected_town = town_combo.get()
        if selected_town in town_data:
            town_data[selected_town]['lat'] = new_lat
            town_data[selected_town]['lon'] = new_lon
            
            # DataFrame ကိုလည်း update လုပ်ခြင်း
            df.loc[(df['TownName'] == selected_town), 'Latitude'] = new_lat
            df.loc[(df['TownName'] == selected_town), 'Longitude'] = new_lon
        
        # Label တွေကို update လုပ်ခြင်း
        lat_value.config(text=new_lat)
        lon_value.config(text=new_lon)
        
        # Entry တွေကို ဖျောက်ခြင်း
        lat_entry.grid_remove()
        lon_entry.grid_remove()
        
        # Label တွေကို ပြခြင်း
        lat_value.grid()
        lon_value.grid()
        
        # Direction buttons ကို disable လုပ်ခြင်း
        lat_nvalue.config(state="disabled")
        lon_svalue.config(state="disabled")
        
        # State နဲ့ Town ကို enable လုပ်ခြင်း
        state_combo.config(state="readonly")
        town_combo.config(state="normal")
        
        # Button ကို Edit ပြောင်းခြင်း
        edit_button.config(text="Edit")
        
        # CSV ဖိုင်ကို update လုပ်ခြင်း
        df.to_csv('dataCSV.csv', index=False, encoding='utf-8')
        messagebox.showinfo("အောင်မြင်ပါသည်", "တည်နေရာအချက်အလက်များ ပြင်ဆင်ပြီးပါပြီ")

# Function to toggle latitude direction
def toggle_lat_dir():
    current_text = lat_nvalue.cget("text")
    if current_text == "N":
        lat_nvalue.config(text="S")
    else:
        lat_nvalue.config(text="N")

# Function to toggle longitude direction
def toggle_lon_dir():
    current_text = lon_svalue.cget("text")
    if current_text == "E":
        lon_svalue.config(text="W")
    else:
        lon_svalue.config(text="E")

# Group 1: ကိုယ်ရေးအချက်အလက်များ
personal_frame = ttk.LabelFrame(toplevel, text="ကိုယ်ရေးအချက်အလက်များ", style='Myanmar.TLabelframe')
personal_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Name ဖော်ပြပါ
name_label = ttk.Label(personal_frame, text="အမည်     : ", font=myanmar_font)
name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")  # Right align
name_text = ttk.Entry(personal_frame, width=30, font=myanmar_font)
name_text.grid(row=0, column=1, padx=10, pady=10, sticky="ew")  # အကျယ်တူအောင်

# Time Entry (00:00 ပုံစံ)
time_label = ttk.Label(personal_frame, text="မွေးချိန်   :", font=myanmar_font)
time_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")  # Right align

# Time Entry အတွက် Frame ဖန်တီးခြင်း
time_frame = ttk.Frame(personal_frame)
time_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Hour Entry
hour_entry = ttk.Entry(time_frame, width=5, font=myanmar_font)
hour_entry.pack(side=tk.LEFT, padx=2)
hour_entry.insert(0, "00")

# Colon Label
colon_label = ttk.Label(time_frame, text=":", font=myanmar_font)
colon_label.pack(side=tk.LEFT)

# Minute Entry
minute_entry = ttk.Entry(time_frame, width=5, font=myanmar_font)
minute_entry.pack(side=tk.LEFT, padx=2)
minute_entry.insert(0, "00")

# Group 2: တည်နေရာနဲ့ လတ္တီကျူ/လောင်ဂျီကျူ (တစ်ခုတည်း)
location_coord_frame = ttk.LabelFrame(toplevel, text="တည်နေရာနဲ့ လတ္တီကျူ/လောင်ဂျီကျူ", style='Myanmar.TLabelframe')
location_coord_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# State ComboBox
state_label = ttk.Label(location_coord_frame, text="တိုင်းနယ်/ပြည်နယ်   :", font=myanmar_font)
state_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")  # Right align
state_combo = ttk.Combobox(location_coord_frame, values=states, state="readonly", font=myanmar_font)
state_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")  # အကျယ်တူအောင်

# Town ComboBox (ရိုက်ရှာလို့ရအောင် ပြင်ဆင်ခြင်း)
town_label = ttk.Label(location_coord_frame, text="မြို့ အမည်   :", font=myanmar_font)
town_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")  # Right align
town_combo = ttk.Combobox(location_coord_frame, state="normal", font=myanmar_font)  # ပြောင်းခဲ့တယ်
town_combo.grid(row=1, column=1, padx=10, pady=10, sticky="ew")  # အကျယ်တူအောင်

# Latitude Label (ဘယ်ဘက်)
lat_label1 = ttk.Label(location_coord_frame, text="လတ္တီကျူ :", font=myanmar_font)
lat_label1.grid(row=2, column=0, padx=10, pady=10, sticky="e")  # Right align

# Latitude Frame (Entry နဲ့ Button အတွက်)
lat_frame = ttk.Frame(location_coord_frame)
lat_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Latitude Entry (display mode)
lat_value = ttk.Entry(lat_frame, width=15, font=myanmar_font)
lat_value.pack(side=tk.LEFT, padx=2)
lat_value.config(state="readonly")  # ပထမမှာ readonly ထားမည်

# Latitude Entry (edit mode)
lat_entry = ttk.Entry(lat_frame, width=15, font=myanmar_font)
lat_entry.pack(side=tk.LEFT, padx=2)
lat_entry.grid_remove()  # ပထမမှာ ဖျောက်ထားမည်

# Latitude Direction Button
lat_nvalue = ttk.Button(lat_frame, text="N", width=3, command=toggle_lat_dir)
lat_nvalue.pack(side=tk.LEFT, padx=2)
lat_nvalue.config(state="disabled")  # ပထမမှာ disabled ထားမည်

# Longitude Label (ဘယ်ဘက်)
lon_label1 = ttk.Label(location_coord_frame, text="လောင်ဂျီကျူ :", font=myanmar_font)
lon_label1.grid(row=3, column=0, padx=10, pady=10, sticky="e")  # Right align

# Longitude Frame (Entry နဲ့ Button အတွက်)
lon_frame = ttk.Frame(location_coord_frame)
lon_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Longitude Entry (display mode)
lon_value = ttk.Entry(lon_frame, width=15, font=myanmar_font)
lon_value.pack(side=tk.LEFT, padx=2)
lon_value.config(state="readonly")  # ပထမမှာ readonly ထားမည်

# Longitude Entry (edit mode)
lon_entry = ttk.Entry(lon_frame, width=15, font=myanmar_font)
lon_entry.pack(side=tk.LEFT, padx=2)
lon_entry.grid_remove()  # ပထမမှာ ဖျောက်ထားမည်

# Longitude Direction Button
lon_svalue = ttk.Button(lon_frame, text="E", width=3, command=toggle_lon_dir)
lon_svalue.pack(side=tk.LEFT, padx=2)
lon_svalue.config(state="disabled")  # ပထမမှာ disabled ထားမည်

# Timezone Label
timezone_label = ttk.Label(location_coord_frame, text="အချိန်ဇုန် :", font=myanmar_font)
timezone_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")  # Right align

# Timezone Value
timezone_value = ttk.Label  (location_coord_frame, text="UTC + ၆:၃၀", state="readonly", width=20 )
timezone_value.grid(row=4, column=1, padx=10, pady=10, sticky="w")  # ဘယ်ဘက်ချိတ်ဆွဲ

# Edit/Save Button
edit_button = ttk.Button(location_coord_frame, text="Edit", command=toggle_edit_mode)
edit_button.grid(row=5, column=1, padx=10, pady=10, sticky="e")

# Function to update towns based on selected state
def update_towns(event):
    selected_state = state_combo.get()
    filtered_towns = df[df['SRName'] == selected_state]['TownName'].unique().tolist()
    town_combo['values'] = sorted(filtered_towns)
    town_combo.set('')
    lat_value.delete(0, tk.END)
    lon_value.delete(0, tk.END)

# Function to update lat/lon based on selected town
def update_lat_lon(event):
    selected_town = town_combo.get()
    if selected_town in town_data:
        lat = town_data[selected_town]['lat']
        lon = town_data[selected_town]['lon']
        lat_value.delete(0, tk.END)
        lat_value.insert(0, lat)
        lon_value.delete(0, tk.END)
        lon_value.insert(0, lon)
    else:
        lat_value.delete(0, tk.END)
        lon_value.delete(0, tk.END)

# Function to filter towns as user types
def filter_towns(event):
    current_text = town_combo.get()
    selected_state = state_combo.get()
    
    if selected_state:
        all_towns = sorted(df[df['SRName'] == selected_state]['TownName'].unique().tolist())
        if current_text == "":
            town_combo['values'] = all_towns
        else:
            # ရိုက်ထည့်တဲ့စာလုံးနဲ့ ကိုက်ညီတဲ့ မြို့များကို ရှာခြင်း
            filtered_towns = [town for town in all_towns if current_text.lower() in town.lower()]
            town_combo['values'] = filtered_towns

# Function to validate hour entry
def validate_hour(new_value):
    if new_value == "" or (new_value.isdigit() and 0 <= int(new_value) <= 23):
        return True
    return False

# Function to validate minute entry
def validate_minute(new_value):
    if new_value == "" or (new_value.isdigit() and 0 <= int(new_value) <= 59):
        return True
    return False

# Register validation commands
vcmd_hour = (toplevel.register(validate_hour), '%P')
vcmd_minute = (toplevel.register(validate_minute), '%P')

# Configure validation for hour and minute entries
hour_entry.config(validate="key", validatecommand=vcmd_hour)
minute_entry.config(validate="key", validatecommand=vcmd_minute)

# Function to format hour entry
def format_hour(event):
    current_text = hour_entry.get()
    if current_text != "":
        hour = int(current_text)
        if hour < 10:
            hour_entry.delete(0, tk.END)
            hour_entry.insert(0, f"0{hour}")
        else:
            hour_entry.delete(0, tk.END)
            hour_entry.insert(0, str(hour))

# Function to format minute entry
def format_minute(event):
    current_text = minute_entry.get()
    if current_text != "":
        minute = int(current_text)
        if minute < 10:
            minute_entry.delete(0, tk.END)
            minute_entry.insert(0, f"0{minute}")
        else:
            minute_entry.delete(0, tk.END)
            minute_entry.insert(0, str(minute))

# Bind events for formatting
hour_entry.bind("<FocusOut>", format_hour)
minute_entry.bind("<FocusOut>", format_minute)

# Bind selections
state_combo.bind("<<ComboboxSelected>>", update_towns)
town_combo.bind("<<ComboboxSelected>>", update_lat_lon)
town_combo.bind("<KeyRelease>", filter_towns)  # စာရိုက်တိုင်း ရှာပေးမယ်

# ပထမဆုံး state နဲ့ town ကို select လုပ်ပေးခြင်း
if states:
    state_combo.set(states[0])  # ပထမဆုံး state ကို select လုပ်ခြင်း
    update_towns(None)  # towns ကို update လုပ်ခြင်း
    if town_combo['values']:
        town_combo.set(town_combo['values'][0])  # ပထမဆုံး town ကို select လုပ်ခြင်း
        update_lat_lon(None)  # lat/lon ကို update လုပ်ခြင်း

# Run GUI
toplevel.mainloop()