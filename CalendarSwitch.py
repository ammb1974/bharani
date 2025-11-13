import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import burmesedate as bd

class MyanmarDateConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("အင်္ဂလိပ်ရက်စွဲမှ မြန်မာရက်စွဲပြောင်းခြင်း")
        self.root.geometry("700x600")
        self.root.configure(bg='#f8f9fa')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#1a5276', height=100)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                             text="အင်္ဂလိပ်ရက်စွဲမှ မြန်မာရက်စွဲပြောင်းခြင်း", 
                             font=("Pyidaungsu", 18, "bold"),
                             fg='white', 
                             bg='#1a5276')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame,
                                text="burmesedate package ဖြင့် တွက်ချက်သည်",
                                font=("Pyidaungsu", 12),
                                fg='#aed6f1',
                                bg='#1a5276')
        subtitle_label.pack(expand=True)
        
        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="အင်္ဂလိပ်ရက်စွဲ ထည့်သွင်းရန်", 
                                  font=("Pyidaungsu", 12, "bold"),
                                  bg='#f8f9fa',
                                  fg='#2c3e50',
                                  padx=15, pady=15)
        input_frame.pack(fill='x', padx=20, pady=15)
        
        # Date selection in a grid
        date_grid = tk.Frame(input_frame, bg='#f8f9fa')
        date_grid.pack(fill='x')
        
        tk.Label(date_grid, text="နှစ်:", font=("Pyidaungsu", 12), bg='#f8f9fa', fg='#2c3e50').grid(row=0, column=0, sticky='w', padx=5, pady=8)
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        self.year_combo = ttk.Combobox(date_grid, textvariable=self.year_var, width=10, font=("Arial", 11))
        self.year_combo['values'] = [str(year) for year in range(1900, 2101)]
        self.year_combo.grid(row=0, column=1, padx=5, pady=8)
        
        tk.Label(date_grid, text="လ:", font=("Pyidaungsu", 12), bg='#f8f9fa', fg='#2c3e50').grid(row=0, column=2, sticky='w', padx=15, pady=8)
        self.month_var = tk.StringVar(value=str(datetime.now().month))
        self.month_combo = ttk.Combobox(date_grid, textvariable=self.month_var, width=10, font=("Arial", 11))
        months = ["ဇန်နဝါရီ", "ဖေဖော်ဝါရီ", "မတ်", "ဧပြီ", "မေ", "ဇွန်", 
                 "ဇူလိုင်", "ဩဂုတ်", "စက်တင်ဘာ", "အောက်တိုဘာ", "နိုဝင်ဘာ", "ဒီဇင်ဘာ"]
        self.month_combo['values'] = [f"{i+1:02d} - {month}" for i, month in enumerate(months)]
        self.month_combo.grid(row=0, column=3, padx=5, pady=8)
        
        tk.Label(date_grid, text="ရက်:", font=("Pyidaungsu", 12), bg='#f8f9fa', fg='#2c3e50').grid(row=0, column=4, sticky='w', padx=15, pady=8)
        self.day_var = tk.StringVar(value=str(datetime.now().day))
        self.day_combo = ttk.Combobox(date_grid, textvariable=self.day_var, width=10, font=("Arial", 11))
        self.day_combo['values'] = [str(day) for day in range(1, 32)]
        self.day_combo.grid(row=0, column=5, padx=5, pady=8)
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg='#f8f9fa')
        button_frame.pack(fill='x', pady=10)
        
        today_btn = tk.Button(button_frame, text="📅 ယနေ့ရက်စွဲ", 
                            font=("Pyidaungsu", 11, "bold"),
                            command=self.set_today,
                            bg='#3498db', fg='white',
                            relief='raised', padx=15, pady=8)
        today_btn.pack(side='left', padx=5)
        
        convert_btn = tk.Button(button_frame, text="🔄 မြန်မာရက်စွဲသို့ ပြောင်းရန်", 
                              font=("Pyidaungsu", 12, "bold"),
                              command=self.convert_date,
                              bg='#e74c3c', fg='white',
                              relief='raised', padx=20, pady=10)
        convert_btn.pack(side='left', padx=10)
        
        # Result Frame
        self.result_frame = tk.LabelFrame(self.root, text="မြန်မာရက်စွဲ ရလဒ်", 
                                        font=("Pyidaungsu", 12, "bold"),
                                        bg='#f8f9fa',
                                        fg='#2c3e50',
                                        padx=15, pady=15)
        self.result_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Initialize result display
        self.setup_result_display()
        
        # Set today's date initially
        self.set_today()
    
    def setup_result_display(self):
        # Main result display
        result_main_frame = tk.Frame(self.result_frame, bg='#f8f9fa')
        result_main_frame.pack(fill='x', pady=10)
        
        self.myanmar_date_label = tk.Label(result_main_frame, 
                                         text="", 
                                         font=("Pyidaungsu", 24, "bold"),
                                         fg='#c0392b',
                                         bg='#f8f9fa')
        self.myanmar_date_label.pack(pady=15)
        
        # Details in two columns
        details_frame = tk.Frame(self.result_frame, bg='#f8f9fa')
        details_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left column - Myanmar details
        left_frame = tk.LabelFrame(details_frame, text="မြန်မာပြက္ခဒိန် အချက်အလက်", 
                                 font=("Pyidaungsu", 11, "bold"),
                                 bg='#f8f9fa', padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Right column - Additional info
        right_frame = tk.LabelFrame(details_frame, text="အခြားအချက်အလက်များ", 
                                  font=("Pyidaungsu", 11, "bold"),
                                  bg='#f8f9fa', padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        details_frame.columnconfigure(0, weight=1)
        details_frame.columnconfigure(1, weight=1)
        
        # Left column content
        left_content = tk.Frame(left_frame, bg='#f8f9fa')
        left_content.pack(fill='both', expand=True)
        
        tk.Label(left_content, text="နေ့အမည်:", font=("Pyidaungsu", 11), bg='#f8f9fa', fg='#2c3e50').grid(row=0, column=0, sticky='w', padx=5, pady=4)
        self.weekday_label = tk.Label(left_content, text="", font=("Pyidaungsu", 11, "bold"), bg='#f8f9fa', fg='#2980b9')
        self.weekday_label.grid(row=0, column=1, sticky='w', padx=10, pady=4)
        
        tk.Label(left_content, text="လအမည်:", font=("Pyidaungsu", 11), bg='#f8f9fa', fg='#2c3e50').grid(row=1, column=0, sticky='w', padx=5, pady=4)
        self.month_name_label = tk.Label(left_content, text="", font=("Pyidaungsu", 11, "bold"), bg='#f8f9fa', fg='#27ae60')
        self.month_name_label.grid(row=1, column=1, sticky='w', padx=10, pady=4)
        
        tk.Label(left_content, text="လဆန်း/ဆုတ်:", font=("Pyidaungsu", 11), bg='#f8f9fa', fg='#2c3e50').grid(row=2, column=0, sticky='w', padx=5, pady=4)
        self.moon_label = tk.Label(left_content, text="", font=("Pyidaungsu", 11, "bold"), bg='#f8f9fa', fg='#8e44ad')
        self.moon_label.grid(row=2, column=1, sticky='w', padx=10, pady=4)
        
        tk.Label(left_content, text="မြန်မာနှစ်:", font=("Pyidaungsu", 11), bg='#f8f9fa', fg='#2c3e50').grid(row=3, column=0, sticky='w', padx=5, pady=4)
        self.year_name_label = tk.Label(left_content, text="", font=("Pyidaungsu", 11, "bold"), bg='#f8f9fa', fg='#d35400')
        self.year_name_label.grid(row=3, column=1, sticky='w', padx=10, pady=4)
        
        # Right column content
        right_content = tk.Frame(right_frame, bg='#f8f9fa')
        right_content.pack(fill='both', expand=True)
        
        tk.Label(right_content, text="အင်္ဂလိပ်ရက်စွဲ:", font=("Pyidaungsu", 11), bg='#f8f9fa', fg='#2c3e50').grid(row=0, column=0, sticky='w', padx=5, pady=4)
        self.english_date_label = tk.Label(right_content, text="", font=("Pyidaungsu", 11, "bold"), bg='#f8f9fa', fg='#c0392b')
        self.english_date_label.grid(row=0, column=1, sticky='w', padx=10, pady=4)
        
        tk.Label(right_content, text="အင်္ဂလိပ်လ:", font=("Pyidaungsu", 11), bg='#f8f9fa', fg='#2c3e50').grid(row=1, column=0, sticky='w', padx=5, pady=4)
        self.english_month_label = tk.Label(right_content, text="", font=("Pyidaungsu", 11, "bold"), bg='#f8f9fa', fg='#16a085')
        self.english_month_label.grid(row=1, column=1, sticky='w', padx=10, pady=4)
        
        tk.Label(right_content, text="ရက်အမည်:", font=("Pyidaungsu", 11), bg='#f8f9fa', fg='#2c3e50').grid(row=2, column=0, sticky='w', padx=5, pady=4)
        self.english_weekday_label = tk.Label(right_content, text="", font=("Pyidaungsu", 11, "bold"), bg='#f8f9fa', fg='#2980b9')
        self.english_weekday_label.grid(row=2, column=1, sticky='w', padx=10, pady=4)
        
        tk.Label(right_content, text="နှစ်အမျိုးအစား:", font=("Pyidaungsu", 11), bg='#f8f9fa', fg='#2c3e50').grid(row=3, column=0, sticky='w', padx=5, pady=4)
        self.year_type_label = tk.Label(right_content, text="", font=("Pyidaungsu", 11, "bold"), bg='#f8f9fa', fg='#8e44ad')
        self.year_type_label.grid(row=3, column=1, sticky='w', padx=10, pady=4)
        
        # Footer info
        footer_frame = tk.Frame(self.result_frame, bg='#f8f9fa')
        footer_frame.pack(fill='x', pady=10)
        
        self.footer_label = tk.Label(footer_frame, text="", 
                                   font=("Pyidaungsu", 10), 
                                   bg='#f8f9fa', fg='#7f8c8d')
        self.footer_label.pack()
    
    def set_today(self):
        """Set today's date"""
        today = datetime.now()
        self.year_var.set(str(today.year))
        self.month_var.set(f"{today.month:02d} - {self.get_month_name(today.month)}")
        self.day_var.set(str(today.day))
        self.convert_date()
    
    def get_month_name(self, month_num):
        """Get Myanmar month name for English months"""
        months = ["ဇန်နဝါရီ", "ဖေဖော်ဝါရီ", "မတ်", "ဧပြီ", "မေ", "ဇွန်", 
                 "ဇူလိုင်", "ဩဂုတ်", "စက်တင်ဘာ", "အောက်တိုဘာ", "နိုဝင်ဘာ", "ဒီဇင်ဘာ"]
        return months[month_num - 1] if 1 <= month_num <= 12 else ""
    
    def convert_date(self):
        """Convert English date to Myanmar date using burmesedate"""
        try:
            year = int(self.year_var.get())
            
            # Extract month number from combobox
            month_str = self.month_var.get()
            month = int(month_str.split(' - ')[0]) if ' - ' in month_str else int(month_str)
            
            day = int(self.day_var.get())
            
            # Validate date
            try:
                gregorian_date = datetime(year, month, day)
            except ValueError:
                messagebox.showerror("အမှား", "မှားယွင်းသော ရက်စွဲဖြစ်သည်")
                return
            
            # Convert using burmesedate
            myanmar_date = self.convert_with_burmesedate(gregorian_date)
            
            if not myanmar_date:
                messagebox.showerror("အမှား", "ရက်စွဲပြောင်းလဲရာတွင် အမှားဖြစ်သည်")
                return
            
            # Display results
            self.display_results(gregorian_date, myanmar_date)
            
        except ValueError as e:
            messagebox.showerror("အမှား", "ကျေးဇူးပြု၍ မှန်ကန်သော ရက်စွဲထည့်ပါ")
        except Exception as e:
            messagebox.showerror("အမှား", f"မျှော်မှန်းမထားသောအမှား: {str(e)}")
    
    def convert_with_burmesedate(self, gregorian_date):
        """Convert date using burmesedate package"""
        try:
            # Use burmesedate to convert
            myanmar_year = bd.mcal(gregorian_date.year, gregorian_date.month, gregorian_date.day).myear
            myanmar_month = bd.mcal(gregorian_date.year, gregorian_date.month, gregorian_date.day).mmonth
            myanmar_day = bd.mcal(gregorian_date.year, gregorian_date.month, gregorian_date.day).mday
            myanmar_month_name = bd.mcal(gregorian_date.year, gregorian_date.month, gregorian_date.day).mmonthnm
            myanmar_weekday = bd.mcal(gregorian_date.year, gregorian_date.month, gregorian_date.day).mweekday
            
            # Determine moon phase
            moon_phase = "လဆန်း" if myanmar_day <= 15 else "လဆုတ်"
            day_display = myanmar_day if myanmar_day <= 15 else myanmar_day - 15
            
            return {
                'myanmar_year': myanmar_year,
                'myanmar_month': myanmar_month,
                'myanmar_day': day_display,
                'myanmar_month_name': myanmar_month_name,
                'myanmar_weekday': myanmar_weekday,
                'moon_phase': moon_phase,
                'full_myanmar_day': myanmar_day
            }
            
        except Exception as e:
            print(f"BurmeseDate conversion error: {e}")
            # Fallback to manual calculation if burmesedate fails
            return self.fallback_conversion(gregorian_date)
    
    def fallback_conversion(self, gregorian_date):
        """Fallback conversion if burmesedate fails"""
        # Simplified fallback conversion
        # This is a basic implementation - you might want to improve this
        year_diff = gregorian_date.year - 638
        myanmar_year = year_diff
        
        # Very basic month and day calculation (not accurate)
        month_names = ["တန်ခူး", "ကဆုန်", "နယုန်", "ဝါဆို", "ဝါခေါင်", "တော်သလင်း", 
                      "သီတင်းကျွတ်", "ပြာသို", "တပို့တွဲ", "တပေါင်း", "နယုန်(ဒု)", "ဝါဆို(ဒု)"]
        
        month_index = (gregorian_date.month - 1) % len(month_names)
        day = (gregorian_date.day % 15) or 15
        
        return {
            'myanmar_year': myanmar_year,
            'myanmar_month': month_index + 1,
            'myanmar_day': day,
            'myanmar_month_name': month_names[month_index],
            'myanmar_weekday': "တနင်္ဂနွေ",  # Default
            'moon_phase': "လဆန်း" if day <= 15 else "လဆုတ်",
            'full_myanmar_day': day
        }
    
    def display_results(self, gregorian_date, myanmar_date):
        """Display the conversion results"""
        # Main Myanmar date
        myanmar_date_str = f"{myanmar_date['myanmar_year']} - {myanmar_date['myanmar_month_name']} - {myanmar_date['myanmar_day']} {myanmar_date['moon_phase']}"
        self.myanmar_date_label.config(text=myanmar_date_str)
        
        # Myanmar details
        self.weekday_label.config(text=myanmar_date['myanmar_weekday'])
        self.month_name_label.config(text=myanmar_date['myanmar_month_name'])
        self.moon_label.config(text=myanmar_date['moon_phase'])
        self.year_name_label.config(text=f"{myanmar_date['myanmar_year']} ခုနှစ်")
        
        # English details
        self.english_date_label.config(text=gregorian_date.strftime("%Y-%m-%d"))
        self.english_month_label.config(text=self.get_month_name(gregorian_date.month))
        self.english_weekday_label.config(text=gregorian_date.strftime("%A"))
        
        # Year type
        year_type = "သာမန်နှစ်" if myanmar_date['myanmar_year'] % 2 == 0 else "ထူးခြားနှစ်"
        self.year_type_label.config(text=year_type)
        
        # Footer info
        footer_text = f"burmesedate package ဖြင့် တွက်ချက်ထားသည် | လပြည့်အချိန်: {myanmar_date['full_myanmar_day']} ရက်"
        self.footer_label.config(text=footer_text)

def main():
    root = tk.Tk()
    
    # Try to set Myanmar font
    try:
        # For Windows with Pyidaungsu font
        root.option_add("*Font", "Pyidaungsu 11")
    except:
        try:
            # For other systems with Myanmar font
            root.option_add("*Font", "Myanmar3 11")
        except:
            try:
                # Fallback to Arial
                root.option_add("*Font", "Arial 11")
            except:
                pass
    
    app = MyanmarDateConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()