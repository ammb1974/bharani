import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os   
import tkinter.font as tkfont


   

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
toplevel.geometry("450x550")
toplevel.resizable(False, False)
toplevel.attributes('-toolwindow', True)
toplevel.iconify()  # Windows မှာ minimize/maximize button မပါစေဖို့



try:
    toplevel.iconbitmap('VediIcon.ico')
except tk.TclError:
    print("Icon ဖိုင်မတွေ့ပါ။ ဖိုင်ကို စီမံပါ။")


# မြန်မာစာအတွက် Font သတ်မှတ်ခြင်း
myanmar_font = tkfont.Font(family="Pyidaungsu", size=12)

# ကော်လံများကို ညီမျှစေရန် ပြင်ဆင်ခြင်း
toplevel.grid_columnconfigure(0, weight=0)
toplevel.grid_columnconfigure(1, weight=1)

# Style ဖန်တီးခြင်း
style = ttk.Style()
style.configure('Myanmar.TLabelframe.Label', font=myanmar_font)
style.configure('Myanmar.TLabelframe', font=myanmar_font)

# Edit mode flag
edit_mode = False

# Function to toggle edit mode
def toggle_edit_mode():
    global edit_mode
    edit_mode = not edit_mode
    
    if edit_mode:
        # Edit mode ဖွင့်ခြင်း
        state_combo.config(state="readonly")
        town_combo.config(state="normal")
        
        # Clear entries for new input
        town_combo.set('')
        lat_entry.delete(0, tk.END)
        lon_entry.delete(0, tk.END)
        
        # Label တွေကို ဖျောက်ခြင်း
        lat_value.grid_remove()
        lon_value.grid_remove()
        
        # Entry တွေကို ပြခြင်း
        lat_entry.grid()
        lon_entry.grid()
        
        # Direction buttons ကို enable လုပ်ခြင်း
        lat_nvalue.config(state="normal")
        lon_svalue.config(state="normal")
        
        # Disable personal info
        name_text.config(state="disabled")
        hour_entry.config(state="disabled")
        minute_entry.config(state="disabled")
        
        # Button ကို Save ပြောင်းခြင်း
        edit_button.config(text="Save")
        
    else:
        # Save mode ဖွင့်ခြင်း
        new_state = state_combo.get()
        new_town = town_combo.get()
        new_lat = lat_entry.get()
        new_lon = lon_entry.get()
        
        # Validation
        if not new_state or not new_town or not new_lat or not new_lon:
            messagebox.showerror("အမှား", "အားလုံးဖြည့်ပါ။")
            toggle_edit_mode()  # revert
            return
        
        try:
            float(new_lat)
            float(new_lon)
        except ValueError:
            messagebox.showerror("အမှား", "လတ္တီကျူ/လောင်ဂျီကျူ မှန်ကန်စွာ ဖြည့်ပါ")
            toggle_edit_mode()
            return
        
        # Check if town already exists
        if new_town in town_data:
            messagebox.showwarning("သတိပြုပါ", f"{new_town} ကို အရင်ဖြည့်ပြီးပါပြီ။ Update လုပ်မလား?")
        
        # Add to DataFrame and town_data
        new_row = pd.DataFrame([{
            'SRName': new_state,
            'TownName': new_town,
            'Latitude': new_lat,
            'Longitude': new_lon
        }])
        global df
        df = pd.concat([df, new_row], ignore_index=True)
        
        town_data[new_town] = {
            'state': new_state,
            'lat': new_lat,
            'lon': new_lon
        }
        
        # Save to CSV
        df.to_csv('dataCSV.csv', index=False, encoding='utf-8')
        messagebox.showinfo("အောင်မြင်ပါသည်", f"{new_town} ကို အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ။")
        
        # Update state combo and towns
        if new_state not in states:
            states.append(new_state)
            state_combo['values'] = sorted(states)
        update_towns(None)
        
        # Revert UI
        lat_entry.grid_remove()
        lon_entry.grid_remove()
        
        lat_value.grid()
        lon_value.grid()
        
        lat_value.config(state="normal")
        lat_value.delete(0, tk.END)
        lat_value.insert(0, new_lat)
        lat_value.config(state="readonly")
        
        lon_value.config(state="normal")
        lon_value.delete(0, tk.END)
        lon_value.insert(0, new_lon)
        lon_value.config(state="readonly")
        
        lat_nvalue.config(state="disabled")
        lon_svalue.config(state="disabled")
        
        name_text.config(state="normal")
        hour_entry.config(state="normal")
        minute_entry.config(state="normal")
        
        state_combo.config(state="readonly")
        town_combo.config(state="disabled")
        
        edit_button.config(text="မြို့ / ရွာ ဒေသ အသစ်ဖြည့်ရန်")

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

# Main Stream Here ----------------------------------------------------------------------------
'''တွက်ချက်မှု လုပ်ရန်နေရာ အစ'''
def calculate_planet():
    # Example implementation for calculation
    name = name_text.get("1.0", tk.END).strip()
    hour = hour_entry.get()
    minute = minute_entry.get()
    town = town_combo.get()

    if not name or not hour or not minute or not town:
        messagebox.showerror("အမှား", "အားလုံးဖြည့်ပါ။")
        return

    messagebox.showinfo("Info", f"တွက်ချက်မှုစတင်ပါမည်။\nအမည်: {name}\nမွေးချိန်: {hour}:{minute}\nမြို့: {town}")
"""တွက်ချက်မှု လုပ်ရန်နေရာ အဆုံး"""

# Group 1: ကိုယ်ရေးအချက်အလက်များ
personal_frame = ttk.LabelFrame(toplevel, text="ကိုယ်ရေးအချက်အလက်များ", style='Myanmar.TLabelframe')
personal_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Name ဖော်ပြပါ
name_label = ttk.Label(personal_frame, text="အမည်     : ", font=myanmar_font)
name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
name_text = tk.Text(personal_frame, height=1, width=30, font=myanmar_font)
name_text.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Time Entry
time_label = ttk.Label(personal_frame, text="မွေးချိန်   :", font=myanmar_font)
time_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

time_frame = ttk.Frame(personal_frame)
time_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

hour_entry = ttk.Entry(time_frame, width=5, font=myanmar_font)
hour_entry.grid(row=0, column=0, padx=2)
hour_entry.insert(0, "00")

colon_label = ttk.Label(time_frame, text=":", font=myanmar_font)
colon_label.grid(row=0, column=1, padx=2    )

minute_entry = ttk.Entry(time_frame, width=5, font=myanmar_font)
minute_entry.grid(row=0, column=2, padx=2)  
minute_entry.insert(0, "00")

# Group 2: တည်နေရာနဲ့ လတ္တီကျူ/လောင်ဂျီကျူ
location_coord_frame = ttk.LabelFrame(toplevel, text="တည်နေရာနဲ့ လတ္တီကျူ/လောင်ဂျီကျူ", style='Myanmar.TLabelframe')
location_coord_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# State ComboBox
state_label = ttk.Label(location_coord_frame, text="တိုင်းနယ်/ပြည်နယ်   :", font=myanmar_font)
state_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
state_combo = ttk.Combobox(location_coord_frame, values=states, state="readonly", font=myanmar_font)
state_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Town ComboBox
town_label = ttk.Label(location_coord_frame, text="မြို့ အမည်   :", font=myanmar_font)
town_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
town_combo = ttk.Combobox(location_coord_frame, state="normal", font=myanmar_font)
town_combo.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Latitude
lat_label1 = ttk.Label(location_coord_frame, text="လတ္တီကျူ :", font=myanmar_font)
lat_label1.grid(row=2, column=0, padx=10, pady=10, sticky="e")

lat_frame = ttk.Frame(location_coord_frame)
lat_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Latitude Entry (display mode)
lat_value = ttk.Entry(lat_frame, width=15, font=myanmar_font, state="readonly")
lat_value.grid(row=0, column=0, padx=2)
# Latitude Entry (edit mode)
lat_entry = ttk.Entry(lat_frame, width=15, font=myanmar_font)
lat_entry.grid(row=0, column=0, padx=2) 
lat_entry.grid_remove()  # hidden initially

# Latitude Direction Button
lat_nvalue = ttk.Button(lat_frame, text="N", width=3, command=toggle_lat_dir)
lat_nvalue.grid(row=0, column=1, padx=2)    
lat_nvalue.config(state="disabled")

# Longitude
lon_label1 = ttk.Label(location_coord_frame, text="လောင်ဂျီကျူ :", font=myanmar_font)
lon_label1.grid(row=3, column=0, padx=10, pady=10, sticky="e")

lon_frame = ttk.Frame(location_coord_frame)
lon_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Longitude Entry (display mode)
lon_value = ttk.Entry(lon_frame, width=15, font=myanmar_font, state="readonly")
lon_value.grid(row=0, column=0, padx=2)

# Longitude Entry (edit mode)
lon_entry = ttk.Entry(lon_frame, width=15, font=myanmar_font)
lon_entry.grid(row=0, column=0, padx=2)
lon_entry.grid_remove()  # hidden initially

# Longitude Direction Button
lon_svalue = ttk.Button(lon_frame, text="E", width=3, command=toggle_lon_dir)
lon_svalue.grid(row=0, column=1, padx=2)
lon_svalue.config(state="disabled")

# Timezone
timezone_label = ttk.Label(location_coord_frame, text="အချိန် ဇုန် :", font=myanmar_font)
timezone_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

timezone_frame = ttk.Frame(location_coord_frame)
timezone_frame.grid(row=4, column=1, padx=10, pady=10, sticky="w")

timezone_entry = ttk.Entry(timezone_frame, width=15, font=myanmar_font, state="normal")
timezone_entry.grid(row=0, column=0, padx=2)
timezone_entry.insert(0, "UTC + 6:30")
timezone_entry.config(state="readonly")


# Edit/Save Button
edit_button = ttk.Button(location_coord_frame, text="မြို့ / ရွာ ဒေသအသစ်ဖြည့်ရန်", command=toggle_edit_mode)
edit_button.grid(row=5, column=1, padx=10, pady=10, sticky="e")

# Calculate button (အောက်ဆုံးမှာ ကြီးကြီး)
calculate_button = ttk.Button(toplevel, text="တွက်ပါ", command=calculate_planet)
calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20, ipady=10, sticky="ew")



# Function to update towns based on selected state
def update_towns(event=None):
    selected_state = state_combo.get()
    filtered_towns = df[df['SRName'] == selected_state]['TownName'].unique().tolist()
    town_combo['values'] = sorted(filtered_towns)
    town_combo.set('')
    
    lat_value.config(state="normal")
    lat_value.delete(0, tk.END)
    lat_value.config(state="readonly")
    
    lon_value.config(state="normal")
    lon_value.delete(0, tk.END)
    lon_value.config(state="readonly")

# Function to update lat/lon based on selected town
def update_lat_lon(event=None):
    selected_town = town_combo.get()
    if selected_town in town_data:
        lat = town_data[selected_town]['lat']
        lon = town_data[selected_town]['lon']
        
        lat_value.config(state="normal")
        lat_value.delete(0, tk.END)
        lat_value.insert(0, lat)
        lat_value.config(state="readonly")
        
        lon_value.config(state="normal")
        lon_value.delete(0, tk.END)
        lon_value.insert(0, lon)
        lon_value.config(state="readonly")

# Function to filter towns as user types
def filter_towns(event):
    current_text = town_combo.get()
    selected_state = state_combo.get()
    
    if selected_state:
        all_towns = sorted(df[df['SRName'] == selected_state]['TownName'].unique().tolist())
        if current_text == "":
            town_combo['values'] = all_towns
        else:
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
        if 0 <= hour <= 23:
            hour_entry.delete(0, tk.END)
            hour_entry.insert(0, f"{hour:02d}")

# Function to format minute entry
def format_minute(event):
    current_text = minute_entry.get()
    if current_text != "":
        minute = int(current_text)
        if 0 <= minute <= 59:
            minute_entry.delete(0, tk.END)
            minute_entry.insert(0, f"{minute:02d}")


# Bind events for formatting
hour_entry.bind("<FocusOut>", format_hour)
minute_entry.bind("<FocusOut>", format_minute)

# Bind selections
state_combo.bind("<<ComboboxSelected>>", update_towns)
town_combo.bind("<<ComboboxSelected>>", update_lat_lon)
town_combo.bind("<KeyRelease>", filter_towns)

# Initialize
if states:
    state_combo.set(states[0])
    update_towns()
    if town_combo['values']:
        town_combo.set(town_combo['values'][0])
        update_lat_lon()

# Run GUI
toplevel.mainloop()