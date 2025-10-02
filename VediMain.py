
import tkinter as tk
import tkinter.ttk as ttk
import ctypes
import os
import subprocess
import sys
from tkinter import Menu, font as tkfont, messagebox, filedialog
from PIL import Image, ImageTk
from About import AboutWindow
import swisseph as swe  
import datetime
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
import newBuild as nb

class BirthChartCalculator:
    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback
        
        # Create child window
        self.win = tk.Toplevel(parent)
        self.win.title("ဇာတာတွက်ရန်")
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
        # Get the application directory
        app_dir = os.environ.get('APP_DIR', os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(app_dir, "dataCSV.csv")
        
        # CSV ဖတ်ခြင်း
        try:
            self.df = pd.read_csv(csv_path, encoding='utf-8')
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
        except Exception as e:
            messagebox.showerror("Data Error", f"Could not load location data: {e}")
            self.states = []
            self.town_data = {}
            self.df = pd.DataFrame(columns=['SRName', 'TownName', 'Latitude', 'Longitude'])
        
    def setup_ui(self):
        # Get the application directory
        app_dir = os.environ.get('APP_DIR', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(app_dir, "VediIcon.ico")
        
        try:
            self.win.iconbitmap(icon_path)
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
            app_dir = os.environ.get('APP_DIR', os.path.dirname(os.path.abspath(__file__)))
            csv_path = os.path.join(app_dir, "dataCSV.csv")
            
            try:
                self.df.to_csv(csv_path, index=False, encoding='utf-8')
                messagebox.showinfo("အောင်မြင်ပါသည်", f"{new_town} ကို အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ။")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save data: {e}")
            
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
       
        VedicAstrologyCalculator.calculate_vedic_chart

        name = self.name_text.get("1.0", tk.END).strip()
        hour = self.hour_entry.get()
        minute = self.minute_entry.get()
        town = self.town_combo.get()
        lat = self.lat_value.get()
        lon = self.lon_value.get()
        timezone = self.timezone_entry.get()
        
        # Create a dictionary with the data
        data = {
            'name': name,
            'time': f"{hour}:{minute}",
            'town': town,
            'latitude': lat,
            'longitude': lon,
            'timezone': timezone
        }
        
        # Call the callback if provided
        if self.callback:
            self.callback(data)
        
        # Close the window
        self.win.destroy()
    
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


class VediApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Vedi")
        self.setup_icon()
        
        # Myanmar Unicode Font ရွေးချယ်ခြင်း
        self.myanmar_font_family = self.get_myanmar_font()
        
        # Create menu bar
        self.create_menu()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create A4 frame
        self.create_enhanced_a4_frame()
        
        # Set fullscreen mode
        self.after(100, self.set_zoomed)
        
        # Keyboard shortcuts
        self.bind('<Control-p>', lambda e: print("Print clicked"))
        self.bind('<Alt-F4>', lambda e: self.quit())
        self.bind('<Control-n>', lambda e: self.open_birth_chart_calculator())
        
    def setup_icon(self):
        # Get the application directory
        app_dir = os.environ.get('APP_DIR', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(app_dir, "VediIcon.ico")
        
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.vedic.app")
        except Exception as e:
            print(f"Taskbar Icon Error: {e}")
            
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        else:
            print(f"Icon file not found at: {icon_path}")
    
    def get_myanmar_font(self):
        # စနစ်တွင်ရှိသော font များစစ်ဆေးခြင်း
        available_fonts = tkfont.families()
        
        # ဦးစွာကြိုက်တဲ့ Myanmar Unicode fonts
        preferred_fonts = [
            "Myanmar Text",
            "Pyidaungsu",
            "Noto Sans Myanmar",
            "Myanmar3",
            "Masterpiece Uni Sans",
        ]
        
        # စနစ်တွင်ရှိသော font ရှာခြင်း
        for font_name in preferred_fonts:
            if font_name in available_fonts:
                return font_name
        
        # မရှိရင် default font သုံးခြင်း
        return "Pyidaungsu"
    
    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)
        
        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.open_birth_chart_calculator, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=lambda: print("Open clicked"))
        file_menu.add_command(label="Save", command=lambda: print("Save clicked"))
        file_menu.add_command(label="Print", command=lambda: print("Print clicked"), accelerator="Ctrl+P")
        file_menu.add_separator()
        file_menu.add_command(label="Exit (Alt+F4)", command=self.quit)
        
        # View Menu
        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Option 1", command=lambda: print("View Option 1 clicked"))
        view_menu.add_command(label="Option 2", command=lambda: print("View Option 2 clicked"))
        
        # Ephemeris Menu
        ephemeris_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ephemeris", menu=ephemeris_menu)
        ephemeris_menu.add_command(label="Generate", command=lambda: print("Ephemeris Generate clicked"))
        ephemeris_menu.add_command(label="Settings", command=lambda: print("Ephemeris Settings clicked"))
        
        # About Menu
        about_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="Version", command=self.show_about)
        about_menu.add_command(label="Help", command=lambda: print("About Help clicked"))
    
    def create_toolbar(self):
        # Toolbar Frame ဖန်တီးခြင်း
        toolbar_frame = ctk.CTkFrame(self, height=40)
        toolbar_frame.pack(side="top", fill="x", padx=5, pady=5)
        
        # New Button
        new_button = ctk.CTkButton(
            toolbar_frame, 
            text="New", 
            width=60, 
            height=30,
            command=self.open_birth_chart_calculator
        )
        new_button.pack(side="left", padx=2)
        
        # Open Button
        open_button = ctk.CTkButton(
            toolbar_frame, 
            text="Open", 
            width=60, 
            height=30,
            command=lambda: print("Open clicked")
        )
        open_button.pack(side="left", padx=2)
        
        # Save Button
        save_button = ctk.CTkButton(
            toolbar_frame, 
            text="Save", 
            width=60, 
            height=30,
            command=lambda: print("Save clicked")
        )
        save_button.pack(side="left", padx=2)
        
        # Separator
        separator = ctk.CTkFrame(toolbar_frame, width=2, height=30)
        separator.pack(side="left", padx=5, fill="y")
        
        # Print Button
        print_button = ctk.CTkButton(
            toolbar_frame, 
            text="Print", 
            width=60, 
            height=30,
            command=lambda: print("Print clicked")
        )
        print_button.pack(side="left", padx=2)
        
        # Separator
        separator2 = ctk.CTkFrame(toolbar_frame, width=2, height=30)
        separator2.pack(side="left", padx=5, fill="y")
    
    def create_enhanced_a4_frame(self):
        # Main content frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Calculate A4 aspect ratio (1:√2)
        a4_width = 595
        a4_height = 842
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate maximum size while maintaining aspect ratio
        max_width = screen_width - 100  # Account for padding
        max_height = screen_height - 150  # Account for toolbar and padding
        
        # Calculate scaled dimensions
        width_ratio = max_width / a4_width
        height_ratio = max_height / a4_height
        scale_factor = min(width_ratio, height_ratio)
        
        scaled_width = int(a4_width * scale_factor)
        scaled_height = int(a4_height * scale_factor)
        
        # A4 Frame with scrollbars
        self.a4_container = ctk.CTkScrollableFrame(
            self.main_frame,
            width=scaled_width,
            height=scaled_height,
            border_width=2,
            border_color="gray",
            fg_color="white"
        )
        
        # A4 Frame ကို screen အလယ်တွင်ချိန်ခြင်း
        self.a4_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Ruler (အပေါ်ကအတိုင်း)
        ruler = ctk.CTkFrame(self.a4_container, height=20, fg_color="#f0f0f0")
        ruler.pack(fill="x", padx=2, pady=(2, 0))
        
        # Ruler marks - scaled to match the A4 paper size
        for i in range(0, scaled_width, int(50 * scale_factor)):  # Scaled intervals
            mark = ctk.CTkFrame(ruler, width=1, height=10, fg_color="gray")
            mark.place(x=i, y=5)
            
            # Number labels - show original mm measurement
            if i % int(100 * scale_factor) == 0:
                original_pos = int(i / scale_factor)
                label = ctk.CTkLabel(ruler, text=str(original_pos), font=("Pyidaungsu", 8))
                label.place(x=i-10, y=0)
        
        # Content area with margins
        self.content_frame = ctk.CTkFrame(self.a4_container, fg_color="white")
        self.content_frame.pack(fill="both", expand=True, padx=int(20 * scale_factor), pady=int(10 * scale_factor))
        
        # Text area
        self.content_text = ctk.CTkTextbox(
            self.content_frame,
            font=(self.myanmar_font_family, int(12 * scale_factor)),  # Scale font size
            fg_color="white",
            text_color="black",
            wrap="word"
        )
        self.content_text.pack(fill="both", expand=True)
        
        # Sample content
        self.content_text.insert("1.0", 
            "A4 Paper Simulation\n"
            "==================\n\n"
            "This is a simulated A4 paper with:\n"
            "• Standard A4 dimensions (595x842px)\n"
            "• Printable area with margins\n"
            "• Ruler at the top\n"
            "• Scrollable content\n\n"
            "You can type your document content here..."
        )
        
        # Function to handle window resize
        def on_resize(event):
            try:
                # Calculate scale factor with bounds
                base_width, base_height = 1200, 800
                scale_x = max(0.05, event.width / base_width)  # Minimum 5% scale
                scale_y = max(0.05, event.height / base_height)
                new_scale_factor = min(scale_x, scale_y)
                
                # Calculate padding with minimum values
                padx_value = max(1, int(20 * new_scale_factor))
                pady_value = max(1, int(10 * new_scale_factor))
                
                self.content_frame.pack_configure(padx=padx_value, pady=pady_value)
                
            except Exception as e:
                print(f"Resize error: {e}")
                # Fallback to safe values
                self.content_frame.pack_configure(padx=5, pady=5)
        
        # Bind resize event to the main frame
        self.main_frame.bind("<Configure>", on_resize)
    
    def set_zoomed(self):
        self.state('zoomed')
    
    def open_new_build(self):
        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Prepare environment variables to pass to the subprocess
            env = os.environ.copy()
            env['APP_DIR'] = script_dir  # Pass the app directory
            
            # Start the new process with the correct working directory
            subprocess.Popen(
                [sys.executable, os.path.join(script_dir, "newBi.py")],
                cwd=script_dir,  # Set working directory
                env=env          # Pass environment variables
            )
        except Exception as e:
            print(f"Error opening newBi.py: {e}")
            messagebox.showerror("Error", f"Cannot open New Chart Form: {e}")
    
    def show_about(self):
        # Get the application directory
        app_dir = os.environ.get('APP_DIR', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(app_dir, "VediIcon.ico")
        
        about_window = AboutWindow(self, icon_path=icon_path, font_family=self.myanmar_font_family)
        about_window.show()
        
        # Set about window icon
        icon_set = False
        try:
            about_window.iconbitmap(self.iconbitmap())
            icon_set = True
        except:
            pass
        
        if not icon_set and os.path.exists(icon_path):
            try:
                about_window.iconbitmap(icon_path)
                icon_set = True
            except:
                pass
        
        if not icon_set and os.path.exists(icon_path):
            try:
                icon_image = Image.open(icon_path)
                icon_photo = ImageTk.PhotoImage(icon_image)
                about_window.iconphoto(True, icon_photo)
                icon_set = True
            except Exception as e:
                print(f"PIL Icon Error: {e}")
        
        if not icon_set:
            print("Could not set icon for about window")
        
        # About window content
        frame = ctk.CTkFrame(about_window)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        title_label = ctk.CTkLabel(
            frame, 
            text="Vedi Application", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Version
        version_label = ctk.CTkLabel(
            frame, 
            text="Version 1.0.0", 
            font=ctk.CTkFont(size=14)
        )
        version_label.pack(pady=5)
        
        # Description
        desc_label = ctk.CTkLabel(
            frame, 
            text="မြန်မာ့ရိုးရာဇာတာဖွဲ့ ပရိုဂရမ်\n\n© 2025 ဘရဏီကုမ္ပဏီ", 
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        desc_label.pack(pady=10)
        
        # Logo
        if os.path.exists(icon_path):
            try:
                logo_image = Image.open(icon_path)
                logo_image = logo_image.resize((64, 64), Image.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_image)
                logo_label = ctk.CTkLabel(frame, image=logo_photo, text="")
                logo_label.image = logo_photo  # Keep a reference
                logo_label.pack(pady=10)
            except Exception as e:
                print(f"Logo Error: {e}")
        
        # Close button
        close_button = ctk.CTkButton(
            frame, 
            text="Close", 
            command=about_window.destroy,
            width=100
        )
        close_button.pack(pady=20)

#+++++++++++++++++++===================တွက်ချက်မှု လုပ်မယ် +++++++++++++++++++++++++++++++++++++++++++++++    


    def open_birth_chart_calculator(self):
        # Open the birth chart calculator as a child window
        BirthChartCalculator(self, callback=self.update_chart_data)
    
    def update_chart_data(self, data):
        # Update the A4 frame with the data from the birth chart calculator
        self.content_text.delete("1.0", tk.END)  # Clear existing content
        
        # Format and insert the new data
        chart_info = (
            f"မွေးဖွားဇာတာ အချက်အလက်များ\n"
            f"========================\n\n"
            f"အမည်: {data['name']}\n"
            f"မွေးချိန်: {data['time']}\n"
            f"မွေးရာဇာတိ: {data['town']}\t\t"
            f"လတ္တီကျူ:P {data['latitude']}\t"
            f" လောင်ဂျီကျူ: {data['longitude']}\t"
            f" အချိန်ဇုန်:  {data['timezone']}\n\n"
            f"တွက်ချက်ထားသော ဇာတာအချက်အလက်များကို ဤနေရာတွင် ဖော်ပြပါမည်။\n"
        )

        print("Chart data updated.")
        print("===========================================================================================")
        (VedicAstrologyCalculator.calculate_vedic_chart(
            data['name'], data['time'], float(data['latitude']), float(data['longitude']))       )

        self.content_text.insert("1.0", chart_info)
        
        # Here you would add your actual chart calculation logic
        # For example:
        # self.calculate_and_display_chart(data)

class VedicAstrologyCalculator:
    def __init__(self):
        self.setup_ephemeris_path()
        
    def setup_ephemeris_path(self):
        """Ephemeris file path ကို သတ်မှတ်ခြင်း"""
        possible_paths = [
            r"C:\sweph\ephe",
            r"D:\sweph\ephe", 
            r"E:\sweph\ephe",
            r"./ephe",
            "../ephe",
            os.path.join(os.path.dirname(__file__), "ephe"),
            "/usr/share/swissephemeris/ephe",
            "/usr/local/share/swissephemeris/ephe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                # Check if the path contains at least one ephemeris file
                if any(fname.endswith('.se1') for fname in os.listdir(path)):
                    swe.set_ephe_path(path)
                    print(f"Ephemeris path set to: {path}")
                    return
        
        self.ask_ephemeris_path()
    
    def ask_ephemeris_path(self):
        """User ကို ephemeris path ရွေးခိုင်းခြင်း"""
        toplevel = tk.Tk()
        toplevel.withdraw()
        
        messagebox.showinfo("Ephemeris Path", 
                          "Please select the folder containing Swiss Ephemeris files (usually named 'ephe')")
        
        ephe_path = filedialog.askdirectory(title="Select Ephemeris Files Folder")
        
        if ephe_path:
            swe.set_ephe_path(ephe_path)
            messagebox.showinfo("Success", f"Ephemeris path set to: {ephe_path}")
        else:
            messagebox.showerror("Error", "Ephemeris path is required.")
            exit()
    
    def calculate_vedic_chart(self, name, birth_datetime, lat, lon):
        """
        Vehlow Equal + True Rahu + Sidereal စနစ်ဖြင့် တွက်ချက်ခြင်း
        """
        try:
            # Julian Day Number သို့ ပြောင်းလဲခြင်း
            jd = swe.julday(birth_datetime.year, 
                          birth_datetime.month, 
                          birth_datetime.day,
                          birth_datetime.hour + birth_datetime.minute/60.0 + birth_datetime.second/3600.0)
            
            print(f"JD: {jd}")
            
            # Lahiri ayanamsa ဖြင့် Sidereal mode သတ်မှတ်ခြင်း
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            ayanamsa = swe.get_ayanamsa(jd)
            print(f"Ayanamsa: {ayanamsa}")
            
            # Vehlow Equal House စနစ်ဖြင့် အိမ်ထောင့်များ တွက်ချက်ခြင်း
            hsys = b'V'  # Vehlow Equal House system
            cusps, ascmc = swe.houses(jd, lat, lon, hsys)
            
            print(f"Houses calculated successfully")
            print(f"Cusps length: {len(cusps)}")
            print(f"Cusps: {cusps}")
            
            # ဂြိုဟ်များ၏ နေရာများ တွက်ချက်ခြင်း (Sidereal + True Node)
            planets = []
            planet_ids = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
                         swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO,
                         swe.TRUE_NODE]  # True Rahu/Ketu
            
            for planet_id in planet_ids:
                try:
                    # True Node အတွက် special flags
                    if planet_id == swe.TRUE_NODE:
                        flags = swe.FLG_SIDEREAL | swe.FLG_TRUEPOS
                    else:
                        flags = swe.FLG_SIDEREAL
                    
                    # ဂြိုဟ်၏ နေရာ တွက်ချက်ခြင်း
                    xx, retflags = swe.calc_ut(jd, planet_id, flags)
                    if retflags == -1:
                        print(f"Error calculating {swe.get_planet_name(planet_id)}")
                        continue
                    
                    longitude = xx[0] % 360
                    
                    # အိမ်ရှာခြင်း (safe method)
                    house_num = self.find_house_safe(longitude, cusps)
                    
                    planets.append({
                        'name': swe.get_planet_name(planet_id),
                        'longitude': longitude,
                        'sign': self.get_zodiac_sign(longitude),
                        'house': house_num,
                        'position': xx
                    })
                    
                except Exception as e:
                    print(f"Error with planet {planet_id}: {e}")
                    continue
            
            # ရလဒ်များ ပြင်ဆင်ခြင်း
            results = {
                'name': name,
                'birth_datetime': birth_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'location': f"Lat: {lat}, Lon: {lon}",
                'ayanamsa': ayanamsa,
                'houses': self.prepare_houses_data_safe(cusps),
                'ascendant': {
                    'longitude': ascmc[0],
                    'sign': self.get_zodiac_sign(ascmc[0])
                },
                'mc': {
                    'longitude': ascmc[1],
                    'sign': self.get_zodiac_sign(ascmc[1])
                },
                'planets': planets,
                'calculation_method': "Vehlow Equal House + True Rahu + Sidereal (Lahiri)"
            }
            
            return results
            
        except Exception as e:
            print(f"Detailed error: {str(e)}")
            raise Exception(f"Calculation error: {str(e)}")
    
    def get_zodiac_sign(self, longitude):
        """ဒီဂရီကို ရာသီခွင်အမည်သို့ ပြောင်းလဲခြင်း"""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        sign_index = int(longitude // 30)
        degrees_in_sign = longitude % 30
        return f"{signs[sign_index]} {degrees_in_sign:.2f}°"
    
    def find_house_safe(self, longitude, cusps):
        """အိမ်ရှာခြင်း (safe version)"""
        try:
            # Cusps array ကို check လုပ်ခြင်း
            if len(cusps) < 13:
                print(f"Warning: cusps array too short: {len(cusps)}")
                return 1
                
            for i in range(1, 13):
                start_cusp = cusps[i]
                end_cusp = cusps[i + 1] if i < 12 else 360 + cusps[1]
                
                # Normalize longitudes for comparison
                norm_long = longitude % 360
                norm_start = start_cusp % 360
                norm_end = end_cusp % 360
                
                if norm_end < norm_start:
                    norm_end += 360
                
                if norm_start <= norm_long < norm_end:
                    return i
                    
            return 1  # default to 1st house
            
        except IndexError:
            print("Index error in find_house")
            return 1
    
    def prepare_houses_data_safe(self, cusps):
        """အိမ်ထောင့်များကို စနစ်တကျပြင်ဆင်ခြင်း (safe version)"""
        houses = []
        try:
            for i in range(1, 13):
                if i < len(cusps):
                    houses.append({
                        'house': i,
                        'cusp': cusps[i],
                        'sign': self.get_zodiac_sign(cusps[i])
                    })
                else:
                    houses.append({
                        'house': i,
                        'cusp': 0.0,
                        'sign': "Unknown"
                    })
            return houses
        except IndexError:
            print("Index error in prepare_houses_data")
            return [{'house': i, 'cusp': 0.0, 'sign': "Error"} for i in range(1, 13)]

class AstrologyGUI:



    
    def create_widgets(self):
        # Input Frame
        input_frame = tk.Frame(self.toplevel)
        input_frame.pack(pady=10)
        
        # Name
        tk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        self.name_entry.insert(0, "Test User")
        
        # Birth Date
        tk.Label(input_frame, text="Birth Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.date_entry = tk.Entry(input_frame, width=20)
        self.date_entry.grid(row=1, column=1, padx=5, pady=2)
        self.date_entry.insert(0, "1990-01-01")
        
        # Birth Time
        tk.Label(input_frame, text="Time (HH:MM:SS):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.time_entry = tk.Entry(input_frame, width=20)
        self.time_entry.grid(row=2, column=1, padx=5, pady=2)
        self.time_entry.insert(0, "12:00:00")
        
        # Location
        tk.Label(input_frame, text="Latitude:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.lat_entry = tk.Entry(input_frame, width=15)
        self.lat_entry.grid(row=3, column=1, padx=5, pady=2)
        self.lat_entry.insert(0, "16.7967")
        
        tk.Label(input_frame, text="Longitude:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.lon_entry = tk.Entry(input_frame, width=15)
        self.lon_entry.grid(row=4, column=1, padx=5, pady=2)
        self.lon_entry.insert(0, "96.1608")
        
        # Calculate Button
        self.calc_button = tk.Button(input_frame, text="Calculate Chart", 
                                   command=self.calculate_chart, bg="lightblue", font=("Pyidaungsu", 12))
        self.calc_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Results Text Area
        result_frame = tk.Frame(self.toplevel)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(result_frame, text="Results:", font=("Pyidaungsu", 14, "bold")).pack(anchor="w")
        
        self.result_text = tk.Text(result_frame, height=25, width=100, font=("Courier New", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
    
    def calculate_chart(self):
        try:
            # Get data from entries
            # name = self.name_entry.get()
            # birth_date = self.date_entry.get()
            # birth_time = self.time_entry.get()
            # lat = float(self.lat_entry.get())
            # lon = float(self.lon_entry.get())
            name = self.newBuild.name_text.get("1.0", tk.END).strip()
            birth_date = self.newBuild.date_entry.get()
            birth_time = self.newBuild.time_entry.get()
            lat = float(self.newBuild.lat_entry.get())
            lon = float(self.newBuild.lon_entry.get())
            
            
            # Parse datetime
            birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
            
            # Calculate chart
            results = self.calculator.calculate_vedic_chart(name, birth_datetime, lat, lon)
            
            # Display results
            self.display_results(results)
            
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Please check your input values:\n{ve}")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred:\n{e}")
    
    def display_results(self, results):
        self.result_text.delete(1.0, tk.END)
        
        # Basic info
        self.result_text.insert(tk.END, f"Name: {results['name']}\n")
        self.result_text.insert(tk.END, f"Birth: {results['birth_datetime']}\n")
        self.result_text.insert(tk.END, f"Location: {results['location']}\n")
        self.result_text.insert(tk.END, f"Ayanamsa (Lahiri): {results['ayanamsa']:.6f}°\n")
        self.result_text.insert(tk.END, f"Method: {results['calculation_method']}\n")
        self.result_text.insert(tk.END, "-" * 70 + "\n\n")
        
        # Ascendant and MC
        self.result_text.insert(tk.END, f"Ascendant : {results['ascendant']['sign']}\n")
        self.result_text.insert(tk.END, f"MC        : {results['mc']['sign']}\n\n")
        
        # Houses (Vehlow Equal)
        self.result_text.insert(tk.END, "HOUSE CUSPS (Vehlow Equal):\n")
        for house in results['houses']:
            self.result_text.insert(tk.END, f"House {house['house']:2}: {house['sign']}\n")
        self.result_text.insert(tk.END, "\n")
        
        # Planets
        self.result_text.insert(tk.END, "PLANETARY POSITIONS (Sidereal + True Rahu):\n")
        for planet in results['planets']:
            house_info = f" in House {planet['house']}" if planet.get('house') else ""
            self.result_text.insert(tk.END, f"{planet['name']:12}: {planet['sign']}{house_info}\n")
        
        self.result_text.insert(tk.END, "\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    # Set the application directory for subprocesses
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ['APP_DIR'] = app_dir
    
    app = VediApp()
    app.mainloop()