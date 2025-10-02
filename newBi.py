import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os   
import tkinter.font as tkfont

class BirthChartCalculator:
    def __init__(self, parent=None):
        # Create child window if parent exists, otherwise create main window
        if parent:
            self.win = tk.Toplevel(parent)
        else:
            self.win = tk.Tk()
            
        self.win.title("မွေးဖွားဇာတာ တွက်ရန်")
        self.win.geometry("450x600")
        
        # Load data
        self.load_data()
        
        # Initialize variables
        self.edit_mode = False
        
        # Setup UI
        self.setup_ui()
        
        # Center window
        self.center_window()
        
        # Bind window close event
        self.win.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def load_data(self):
        # CSV ဖတ်ခြင်း
        self.df = pd.read_csv('dataCSV.csv', encoding='utf-8')
        # Data cleaning
        self.df['TownName'] = self.df['TownName'].fillna('').str.strip()
        self.df['SRName'] = self.df['SRName'].fillna('').str.strip()
        self.df['Latitude'] = self.df['Latitude'].fillna('0.0').astype(str).str.strip()
        self.df['Longitude'] = self.df['Longitude'].fillna('0.0').astype(str).str.strip()
        # Valid rows only
        self.df = self.df[(self.df['TownName'] != '') & (self.df['SRName'] != '')]
        # Unique states
        self.states = sorted(self.df['SRName'].unique().tolist())
        # Town data dictionary
        self.town_data = {
            row['TownName']: {
                'state': row['SRName'],
                'lat': row['Latitude'],
                'lon': row['Longitude']
            }
            for _, row in self.df.iterrows()
        }
        
    def setup_ui(self):
        try:
            self.win.iconbitmap('VediIcon.ico')
        except tk.TclError:
            print("Icon ဖိုင်မတွေ့ပါ။ ဖိုင်ကို စီမံပါ။")

        # မြန်မာစာအတွက် Font သတ်မှတ်ခြင်း
        self.myanmar_font = tkfont.Font(family="Pyidaungsu", size=12)
        # ကော်လံများကို ညီမျှစေရန် ပြင်ဆင်ခြင်း
        self.win.grid_columnconfigure(0, weight=0)
        self.win.grid_columnconfigure(1, weight=1)
        # Style ဖန်တီးခြင်း
        self.style = ttk.Style()
        self.style.configure('Myanmar.TLabelframe.Label', font=self.myanmar_font)
        self.style.configure('Myanmar.TLabelframe', font=self.myanmar_font)
        
        # Group 1: ကိုယ်ရေးအချက်အလက်များ
        self.personal_frame = ttk.LabelFrame(self.win, text="ကိုယ်ရေးအချက်အလက်များ", style='Myanmar.TLabelframe')
        self.personal_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Name ဖော်ပြပါ
        self.name_label = ttk.Label(self.personal_frame, text="အမည်     : ", font=self.myanmar_font)
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.name_text = tk.Text(self.personal_frame, height=1, width=30, font=self.myanmar_font)
        self.name_text.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Time Entry
        self.time_label = ttk.Label(self.personal_frame, text="မွေးချိန်   :", font=self.myanmar_font)
        self.time_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.time_frame = ttk.Frame(self.personal_frame)
        self.time_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.hour_entry = ttk.Entry(self.time_frame, width=5, font=self.myanmar_font)
        self.hour_entry.grid(row=0, column=0, padx=2)
        self.hour_entry.insert(0, "00")
        self.colon_label = ttk.Label(self.time_frame, text=":", font=self.myanmar_font)
        self.colon_label.grid(row=0, column=1, padx=2)
        self.minute_entry = ttk.Entry(self.time_frame, width=5, font=self.myanmar_font)
        self.minute_entry.grid(row=0, column=2, padx=2)
        self.minute_entry.insert(0, "00")
        
        # Group 2: တည်နေရာနဲ့ လတ္တီကျူ/လောင်ဂျီကျူ
        self.location_coord_frame = ttk.LabelFrame(self.win, text="တည်နေရာနဲ့ လတ္တီကျူ/လောင်ဂျီကျူ", style='Myanmar.TLabelframe')
        self.location_coord_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # State ComboBox
        self.state_label = ttk.Label(self.location_coord_frame, text="တိုင်းနယ်/ပြည်နယ်   :", font=self.myanmar_font)
        self.state_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.state_combo = ttk.Combobox(self.location_coord_frame, values=self.states, state="readonly", font=self.myanmar_font)
        self.state_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Town ComboBox
        self.town_label = ttk.Label(self.location_coord_frame, text="မြို့ အမည်   :", font=self.myanmar_font)
        self.town_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.town_combo = ttk.Combobox(self.location_coord_frame, state="normal", font=self.myanmar_font)
        self.town_combo.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Latitude
        self.lat_label1 = ttk.Label(self.location_coord_frame, text="လတ္တီကျူ :", font=self.myanmar_font)
        self.lat_label1.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.lat_frame = ttk.Frame(self.location_coord_frame)
        self.lat_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        # Latitude Entry (display mode)
        self.lat_value = ttk.Entry(self.lat_frame, width=15, font=self.myanmar_font, state="readonly")
        self.lat_value.grid(row=0, column=0, padx=2)
        # Latitude Entry (edit mode)
        self.lat_entry = ttk.Entry(self.lat_frame, width=15, font=self.myanmar_font)
        self.lat_entry.grid(row=0, column=0, padx=2)
        self.lat_entry.grid_remove()  # hidden initially
        # Latitude Direction Button
        self.lat_nvalue = ttk.Button(self.lat_frame, text="N", width=3, command=self.toggle_lat_dir)
        self.lat_nvalue.grid(row=0, column=1, padx=2)
        self.lat_nvalue.config(state="disabled")
        
        # Longitude
        self.lon_label1 = ttk.Label(self.location_coord_frame, text="လောင်ဂျီကျူ :", font=self.myanmar_font)
        self.lon_label1.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.lon_frame = ttk.Frame(self.location_coord_frame)
        self.lon_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        # Longitude Entry (display mode)
        self.lon_value = ttk.Entry(self.lon_frame, width=15, font=self.myanmar_font, state="readonly")
        self.lon_value.grid(row=0, column=0, padx=2)
        # Longitude Entry (edit mode)
        self.lon_entry = ttk.Entry(self.lon_frame, width=15, font=self.myanmar_font)
        self.lon_entry.grid(row=0, column=0, padx=2)
        self.lon_entry.grid_remove()  # hidden initially
        # Longitude Direction Button
        self.lon_svalue = ttk.Button(self.lon_frame, text="E", width=3, command=self.toggle_lon_dir)
        self.lon_svalue.grid(row=0, column=1, padx=2)
        self.lon_svalue.config(state="disabled")
        
        # Timezone
        self.timezone_label = ttk.Label(self.location_coord_frame, text="အချိန် ဇုန် :", font=self.myanmar_font)
        self.timezone_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.timezone_frame = ttk.Frame(self.location_coord_frame)
        self.timezone_frame.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.timezone_entry = ttk.Entry(self.timezone_frame, width=15, font=self.myanmar_font, state="normal")
        self.timezone_entry.grid(row=0, column=0, padx=2)
        self.timezone_entry.insert(0, "UTC + 6:30")
        self.timezone_entry.config(state="readonly")
        
        # Edit/Save Button
        self.edit_button = ttk.Button(self.location_coord_frame, text="မြို့ / ရွာ ဒေသအသစ်ဖြည့်ရန်", command=self.toggle_edit_mode)
        self.edit_button.grid(row=5, column=1, padx=10, pady=10, sticky="e")
        
        # Calculate button (အောက်ဆုံးမှာ ကြီးကြီး)
        self.calculate_button = ttk.Button(self.win, text="တွက်ပါ", command=self.calculate_planet)
        self.calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20, ipady=10, sticky="ew")
        
        # Register validation commands
        self.vcmd_hour = (self.win.register(self.validate_hour), '%P')
        self.vcmd_minute = (self.win.register(self.validate_minute), '%P')
        
        # Configure validation for hour and minute entries
        self.hour_entry.config(validate="key", validatecommand=self.vcmd_hour)
        self.minute_entry.config(validate="key", validatecommand=self.vcmd_minute)
        
        # Bind events
        self.win.bind("<Configure>", self.center_window)
        self.hour_entry.bind("<FocusOut>", self.format_hour)
        self.minute_entry.bind("<FocusOut>", self.format_minute)
        self.state_combo.bind("<<ComboboxSelected>>", self.update_towns)
        self.town_combo.bind("<<ComboboxSelected>>", self.update_lat_lon)
        self.town_combo.bind("<KeyRelease>", self.filter_towns)
        
        # Initialize
        if self.states:
            self.state_combo.set(self.states[0])
            self.update_towns()
            if self.town_combo['values']:
                self.town_combo.set(self.town_combo['values'][0])
                self.update_lat_lon()
    
    def center_window(self, event=None):
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        window_width = self.win.winfo_width()
        window_height = self.win.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.win.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        
        if self.edit_mode:
            # Edit mode ဖွင့်ခြင်း
            self.state_combo.config(state="readonly")
            self.town_combo.config(state="normal")
            
            # Clear entries for new input
            self.town_combo.set('')
            self.lat_entry.delete(0, tk.END)
            self.lon_entry.delete(0, tk.END)
            
            # Label တွေကို ဖျောက်ခြင်း
            self.lat_value.grid_remove()
            self.lon_value.grid_remove()
            
            # Entry တွေကို ပြခြင်း
            self.lat_entry.grid()
            self.lon_entry.grid()
            
            # Direction buttons ကို enable လုပ်ခြင်း
            self.lat_nvalue.config(state="normal")
            self.lon_svalue.config(state="normal")
            
            # Disable personal info
            self.name_text.config(state="disabled")
            self.hour_entry.config(state="disabled")
            self.minute_entry.config(state="disabled")
            
            # Button ကို Save ပြောင်းခြင်း
            self.edit_button.config(text="Save")
            
        else:
            # Save mode ဖွင့်ခြင်း
            new_state = self.state_combo.get()
            new_town = self.town_combo.get()
            new_lat = self.lat_entry.get()
            new_lon = self.lon_entry.get()
            
            # Validation
            if not new_state or not new_town or not new_lat or not new_lon:
                messagebox.showerror("အမှား", "အားလုံးဖြည့်ပါ။")
                self.toggle_edit_mode()  # revert
                return
            
            try:
                float(new_lat)
                float(new_lon)
            except ValueError:
                messagebox.showerror("အမှား", "လတ္တီကျူ/လောင်ဂျီကျူ မှန်ကန်စွာ ဖြည့်ပါ")
                self.toggle_edit_mode()
                return
            
            # Check if town already exists
            if new_town in self.town_data:
                messagebox.showwarning("သတိပြုပါ", f"{new_town} ကို အရင်ဖြည့်ပြီးပါပြီ။ Update လုပ်မလား?")
            
            # Add to DataFrame and town_data
            new_row = pd.DataFrame([{
                'SRName': new_state,
                'TownName': new_town,
                'Latitude': new_lat,
                'Longitude': new_lon
            }])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            
            self.town_data[new_town] = {
                'state': new_state,
                'lat': new_lat,
                'lon': new_lon
            }
            
            # Save to CSV
            self.df.to_csv('dataCSV.csv', index=False, encoding='utf-8')
            messagebox.showinfo("အောင်မြင်ပါသည်", f"{new_town} ကို အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ။")
            
            # Update state combo and towns
            if new_state not in self.states:
                self.states.append(new_state)
                self.state_combo['values'] = sorted(self.states)
            self.update_towns(None)
            
            # Revert UI
            self.lat_entry.grid_remove()
            self.lon_entry.grid_remove()
            
            self.lat_value.grid()
            self.lon_value.grid()
            
            self.lat_value.config(state="normal")
            self.lat_value.delete(0, tk.END)
            self.lat_value.insert(0, new_lat)
            self.lat_value.config(state="readonly")
            
            self.lon_value.config(state="normal")
            self.lon_value.delete(0, tk.END)
            self.lon_value.insert(0, new_lon)
            self.lon_value.config(state="readonly")
            
            self.lat_nvalue.config(state="disabled")
            self.lon_svalue.config(state="disabled")
            
            self.name_text.config(state="normal")
            self.hour_entry.config(state="normal")
            self.minute_entry.config(state="normal")
            
            self.state_combo.config(state="readonly")
            self.town_combo.config(state="disabled")
            
            self.edit_button.config(text="မြို့ / ရွာ ဒေသ အသစ်ဖြည့်ရန်")
    
    def toggle_lat_dir(self):
        current_text = self.lat_nvalue.cget("text")
        if current_text == "N":
            self.lat_nvalue.config(text="S")
        else:
            self.lat_nvalue.config(text="N")
    
    def toggle_lon_dir(self):
        current_text = self.lon_svalue.cget("text")
        if current_text == "E":
            self.lon_svalue.config(text="W")
        else:
            self.lon_svalue.config(text="E")
    
    def calculate_planet(self):
        name = self.name_text.get("1.0", tk.END).strip()
        hour = self.hour_entry.get()
        minute = self.minute_entry.get()
        town = self.town_combo.get()
        
        messagebox.showinfo("Info", f"တွက်ချက်မှုစတင်ပါမည်။\nအမည်: {name}\nမွေးချိန်: {hour}:{minute}\nမြို့: {town}")
    
    def update_towns(self, event=None):
        selected_state = self.state_combo.get()
        filtered_towns = self.df[self.df['SRName'] == selected_state]['TownName'].unique().tolist()
        self.town_combo['values'] = sorted(filtered_towns)
        self.town_combo.set('')
        
        self.lat_value.config(state="normal")
        self.lat_value.delete(0, tk.END)
        self.lat_value.config(state="readonly")
        
        self.lon_value.config(state="normal")
        self.lon_value.delete(0, tk.END)
        self.lon_value.config(state="readonly")
    
    def update_lat_lon(self, event=None):
        selected_town = self.town_combo.get()
        if selected_town in self.town_data:
            lat = self.town_data[selected_town]['lat']
            lon = self.town_data[selected_town]['lon']
            
            self.lat_value.config(state="normal")
            self.lat_value.delete(0, tk.END)
            self.lat_value.insert(0, lat)
            self.lat_value.config(state="readonly")
            
            self.lon_value.config(state="normal")
            self.lon_value.delete(0, tk.END)
            self.lon_value.insert(0, lon)
            self.lon_value.config(state="readonly")
    
    def filter_towns(self, event):
        current_text = self.town_combo.get()
        selected_state = self.state_combo.get()
        
        if selected_state:
            all_towns = sorted(self.df[self.df['SRName'] == selected_state]['TownName'].unique().tolist())
            if current_text == "":
                self.town_combo['values'] = all_towns
            else:
                filtered_towns = [town for town in all_towns if current_text.lower() in town.lower()]
                self.town_combo['values'] = filtered_towns
    
    def validate_hour(self, new_value):
        if new_value == "" or (new_value.isdigit() and 0 <= int(new_value) <= 23):
            return True
        return False
    
    def validate_minute(self, new_value):
        if new_value == "" or (new_value.isdigit() and 0 <= int(new_value) <= 59):
            return True
        return False
    
    def format_hour(self, event):
        current_text = self.hour_entry.get()
        if current_text != "":
            hour = int(current_text)
            if 0 <= hour <= 23:
                self.hour_entry.delete(0, tk.END)
                self.hour_entry.insert(0, f"{hour:02d}")
    
    def format_minute(self, event):
        current_text = self.minute_entry.get()
        if current_text != "":
            minute = int(current_text)
            if 0 <= minute <= 59:
                self.minute_entry.delete(0, tk.END)
                self.minute_entry.insert(0, f"{minute:02d}")
    
    def on_close(self):
        # Clean up resources if needed
        self.win.destroy()

# Example usage:
if __name__ == "__main__":
    # Create main window
    main_app = tk.Tk()
    main_app.title("Main Application")
    main_app.geometry("300x200")
    
    # Button to open child window
    def open_child():
        BirthChartCalculator(main_app)
    
    open_button = ttk.Button(main_app, text="Open Birth Chart Calculator", command=open_child)
    open_button.pack(pady=50)
    
    main_app.mainloop()