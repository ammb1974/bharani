import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import requests
from datetime import datetime

class CityGeoApp:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("City Geolocation Information")
        self.csv_file = "CityGeo.csv"
        
        # Initialize city data
        self.city_data = {}
        self.load_city_data()
        
        # Create UI elements
        self.create_widgets()
        
    def load_city_data(self):
        """Load city data from CSV file"""
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    city_key = f"{row['City']}, {row['State']}" if row['State'] else row['City']
                    self.city_data[city_key] = {
                        'City': row['City'],
                        'State': row['State'],
                        'Country': row['Country'],
                        'Latitude': row['Latitude'],
                        'Longitude': row['Longitude'],
                        'LastUpdated': row.get('LastUpdated', '')
                    }
        else:
            # Create CSV file with header
            with open(self.csv_file, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    'City', 'State', 'Country', 'Latitude', 'Longitude', 'LastUpdated'
                ])
                writer.writeheader()
    
    def save_city_data(self):
        """Save city data to CSV file"""
        with open(self.csv_file, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'City', 'State', 'Country', 'Latitude', 'Longitude', 'LastUpdated'
            ])
            writer.writeheader()
            for city_info in self.city_data.values():
                writer.writerow(city_info)
    
    def fetch_geolocation(self, city_name, state_name=""):
        """Fetch geolocation data from Nominatim API"""
        try:
            query = f"{city_name}, {state_name}" if state_name else city_name
            url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json"
            headers = {'User-Agent': 'CityGeoApp/1.0'}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None
                
            location = data[0]
            return {
                'City': city_name,
                'State': state_name,
                'Country': location.get('display_name', '').split(',')[-1].strip(),
                'Latitude': location.get('lat', ''),
                'Longitude': location.get('lon', ''),
                'LastUpdated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to fetch geolocation: {str(e)}")
            return None
  #Widget Call လုပ်ဖို့ရန်  
    def create_widgets(self):
        """Create all GUI elements"""
        # Main frame
        main_frame = tk.Frame(self.toplevel, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search section
        search_frame = tk.LabelFrame(main_frame, text="Search City", padx=5, pady=5)
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="Enter city name:").grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        self.city_combo = ttk.Combobox(search_frame, 
                                      textvariable=self.search_var, 
                                      values=list(self.city_data.keys()))
        self.city_combo.grid(row=0, column=1, padx=5, sticky="ew")
        self.city_combo.bind("<<ComboboxSelected>>", self.show_city_info)
        
        tk.Button(search_frame, text="Search", command=self.search_city).grid(row=0, column=2, padx=5)
        
        # City info section
        info_frame = tk.LabelFrame(main_frame, text="City Information", padx=5, pady=5)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create info table
        self.info_labels = {}
        fields = ["City", "State", "Country", "Latitude", "Longitude", "LastUpdated"]
        for i, field in enumerate(fields):
            tk.Label(info_frame, text=f"{field}:", width=12, anchor="e").grid(row=i, column=0, sticky="e", pady=2)
            self.info_labels[field] = tk.Label(info_frame, text="", width=40, anchor="w")
            self.info_labels[field].grid(row=i, column=1, sticky="w", pady=2)
        
        # Action buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="Add New", command=self.add_city).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edit", command=self.edit_city).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Remove", command=self.remove_city).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh List", command=self.refresh_combobox).pack(side=tk.RIGHT, padx=5)
    
    def refresh_combobox(self):
        """Refresh the combobox with updated city list"""
        self.city_combo['values'] = list(self.city_data.keys())
    
    def search_city(self):
        """Search for a city in local data or online"""
        query = self.search_var.get().strip()
        if not query:
            return
            
        if query in self.city_data:
            self.show_city_info()
            return
            
        parts = [p.strip() for p in query.split(',')]
        city_name = parts[0]
        state_name = parts[1] if len(parts) > 1 else ""
        
        confirm = messagebox.askyesno("City Not Found", 
                                    f"'{query}' not found in local database.\nFetch from online geolocation service?")
        if confirm:
            geo_data = self.fetch_geolocation(city_name, state_name)
            if geo_data:
                city_key = f"{city_name}, {state_name}" if state_name else city_name
                self.city_data[city_key] = geo_data
                self.save_city_data()
                self.refresh_combobox()
                self.search_var.set(city_key)
                self.show_city_info()
                messagebox.showinfo("Success", "City data fetched and saved successfully!")
    
    def show_city_info(self, event=None):
        """Display information for the selected city"""
        city_key = self.search_var.get()
        if city_key in self.city_data:
            city_info = self.city_data[city_key]
            for field, label in self.info_labels.items():
                label.config(text=city_info.get(field, ""))
    
    def add_city(self):
        """Open dialog to add a new city"""
        dialog = tk.Toplevel(self.toplevel)
        dialog.title("Add New City")
        dialog.grab_set()  # Make dialog modal
        
        # Form fields
        tk.Label(dialog, text="City:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        city_entry = tk.Entry(dialog, width=30)
        city_entry.grid(row=0, column=1, padx=5, pady=5)
        city_entry.focus_set()
        
        tk.Label(dialog, text="State (optional):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        state_entry = tk.Entry(dialog, width=30)
        state_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Country:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        country_entry = tk.Entry(dialog, width=30)
        country_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Latitude:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        lat_entry = tk.Entry(dialog, width=30)
        lat_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Longitude:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        lon_entry = tk.Entry(dialog, width=30)
        lon_entry.grid(row=4, column=1, padx=5, pady=5)
        
        def save_new_city():
            city = city_entry.get().strip()
            state = state_entry.get().strip()
            country = country_entry.get().strip()
            lat = lat_entry.get().strip()
            lon = lon_entry.get().strip()
            
            if not city:
                messagebox.showerror("Error", "City name is required!")
                return
                
            city_key = f"{city}, {state}" if state else city
            if city_key in self.city_data:
                messagebox.showerror("Error", "This city already exists in the database!")
                return
                
            self.city_data[city_key] = {
                'City': city,
                'State': state,
                'Country': country,
                'Latitude': lat,
                'Longitude': lon,
                'LastUpdated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.save_city_data()
            self.refresh_combobox()
            self.search_var.set(city_key)
            self.show_city_info()
            dialog.destroy()
            messagebox.showinfo("Success", "City added successfully!")
        
        tk.Button(dialog, text="Save", command=save_new_city).grid(row=5, column=1, sticky="e", padx=5, pady=5)
        tk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=5, column=0, sticky="w", padx=5, pady=5)
    
    def edit_city(self):
        """Edit selected city with auto-update in main form"""
        city_key = self.search_var.get()
        if not city_key or city_key not in self.city_data:
            messagebox.showerror("Error", "Please select a city to edit!")
            return
            
        city_info = self.city_data[city_key]
        dialog = tk.Toplevel(self.toplevel)
        dialog.title("Edit City")
        dialog.grab_set()  # Make dialog modal
        
        # Form fields with current values
        tk.Label(dialog, text="City:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        city_entry = tk.Entry(dialog, width=30)
        city_entry.insert(0, city_info['City'])
        city_entry.grid(row=0, column=1, padx=5, pady=5)
        city_entry.focus_set()
        
        tk.Label(dialog, text="State:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        state_entry = tk.Entry(dialog, width=30)
        state_entry.insert(0, city_info['State'])
        state_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Country:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        country_entry = tk.Entry(dialog, width=30)
        country_entry.insert(0, city_info['Country'])
        country_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Latitude:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        lat_entry = tk.Entry(dialog, width=30)
        lat_entry.insert(0, city_info['Latitude'])
        lat_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Longitude:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        lon_entry = tk.Entry(dialog, width=30)
        lon_entry.insert(0, city_info['Longitude'])
        lon_entry.grid(row=4, column=1, padx=5, pady=5)
        
        def save_edited_city():
            new_city = city_entry.get().strip()
            new_state = state_entry.get().strip()
            new_country = country_entry.get().strip()
            new_lat = lat_entry.get().strip()
            new_lon = lon_entry.get().strip()
            
            if not new_city:
                messagebox.showerror("Error", "City name is required!")
                return
                
            new_city_key = f"{new_city}, {new_state}" if new_state else new_city
            
            if new_city_key != city_key and new_city_key in self.city_data:
                messagebox.showerror("Error", "This city/state combination already exists!")
                return
                
            # Update data
            if new_city_key != city_key:
                del self.city_data[city_key]
                
            self.city_data[new_city_key] = {
                'City': new_city,
                'State': new_state,
                'Country': new_country,
                'Latitude': new_lat,
                'Longitude': new_lon,
                'LastUpdated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.save_city_data()
            self.refresh_combobox()
            self.search_var.set(new_city_key)  # Update combobox selection
            self.show_city_info()  # Refresh displayed info
            dialog.destroy()
            messagebox.showinfo("Success", "City updated successfully!")
        
        tk.Button(dialog, text="Save", command=save_edited_city).grid(row=5, column=1, sticky="e", padx=5, pady=5)
        tk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=5, column=0, sticky="w", padx=5, pady=5)
    
    def remove_city(self):
        """Remove selected city with auto-update"""
        city_key = self.search_var.get()
        if not city_key or city_key not in self.city_data:
            messagebox.showerror("Error", "Please select a city to remove!")
            return
            
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove {city_key}?")
        if confirm:
            del self.city_data[city_key]
            self.save_city_data()
            self.refresh_combobox()
            self.search_var.set("")
            for label in self.info_labels.values():
                label.config(text="")
            messagebox.showinfo("Success", "City removed successfully!")

if __name__ == "__main__":
    toplevel = tk.Tk()
    app = CityGeoApp(toplevel)
    toplevel.mainloop()
