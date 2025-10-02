import tkinter as tk
from tkinter import ttk, messagebox
import requests

# GeoNames username
GEONAMES_USERNAME = "phoekhwar"

def fetch_coordinates():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "မြို့အမည်ထည့်ပါ။")
        return

    search_url = f"http://api.geonames.org/searchJSON?q={city}&maxRows=1&username={GEONAMES_USERNAME}"
    try:
        response = requests.get(search_url)
        data = response.json()
        print("Search Response:", data)  # Debugging

        if 'status' in data:
            messagebox.showerror("API Error", f"GeoNames error: {data['status']['message']}")
            return

        if data.get('totalResultsCount', 0) == 0:
            messagebox.showerror("Not Found", f"မြို့ '{city}' ကို မတွေ့ပါ။")
            return

        geo = data['geonames'][0]
        lat = geo['lat']
        lng = geo['lng']

        lat_value.set(f"{lat}°")
        lon_value.set(f"{lng}°")

        # Fetch timezone using lat/lng
        tz_url = f"http://api.geonames.org/timezoneJSON?lat={lat}&lng={lng}&username={GEONAMES_USERNAME}"
        tz_response = requests.get(tz_url)
        tz_data = tz_response.json()
        print("Timezone Response:", tz_data)  # Debugging

        if 'timezoneId' in tz_data:
            timezone_value.set(tz_data['timezoneId'])
        else:
            timezone_value.set("Auto")

    except Exception as e:
        messagebox.showerror("Error", f"API error: {e}")

# GUI Setup
toplevel = tk.Tk()
toplevel.title("မွေးဖွားရာမြို့ ရွေးချယ်ခြင်း")

# City Input
ttk.Label(toplevel, text="မွေးဖွားရာမြို့:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
city_entry = ttk.Entry(toplevel, width=30)
city_entry.grid(row=0, column=1, padx=5, pady=5)

fetch_btn = ttk.Button(toplevel, text="Online မှ ရယူရန်", command=fetch_coordinates)
fetch_btn.grid(row=0, column=2, padx=5, pady=5)

# Latitude
ttk.Label(toplevel, text="Latitude:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
lat_value = tk.StringVar()
lat_entry = ttk.Entry(toplevel, textvariable=lat_value, width=20)
lat_entry.grid(row=1, column=1, padx=5, pady=5)

# Longitude
ttk.Label(toplevel, text="Longitude:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
lon_value = tk.StringVar()
lon_entry = ttk.Entry(toplevel, textvariable=lon_value, width=20)
lon_entry.grid(row=2, column=1, padx=5, pady=5)

# Timezone
ttk.Label(toplevel, text="Timezone:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
timezone_value = tk.StringVar(value="Auto")
timezone_entry = ttk.Entry(toplevel, textvariable=timezone_value, width=20)
timezone_entry.grid(row=3, column=1, padx=5, pady=5)

toplevel.mainloop()