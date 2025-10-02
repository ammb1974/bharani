# about.py
import tkinter as ctk

import os
from PIL import Image, ImageTk

class AboutWindow:
    def __init__(self, parent, icon_path="VediIcon.ico", font_family=None, font_size=12):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Vedi အကြောင်း")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Window ကို screen အလယ်မှာချိန်ခြင်း
        self.window.transient(parent)
        self.window.grab_set()
        
        # Font ချိန်းတားခြင်း
        if font_family:
            self.font = ctk.CTkFont(family=font_family, size=font_size)
        else:
            self.font = ctk.CTkFont(size=font_size)
        
        # Icon path ကိုသိမ်းဆည်းခြင်း
        self.icon_path = icon_path
        
        # About window ရဲ့ icon ချိန်းတားခြင်း
        self.set_window_icon()
        
        # Content ထည့်ခြင်း
        self.create_widgets()
    
    def set_window_icon(self):
        icon_set = False
        
        # နည်းလမ်း ၁: Parent window ရဲ့ icon ကိုအတူသုံးခြင်း
        try:
            self.window.iconbitmap(self.window.master.iconbitmap())
            icon_set = True
        except:
            pass
        
        # နည်းလမ်း ၂: တိုက်ရိုက် icon file ကိုသုံးခြင်း
        if not icon_set and self.icon_path and os.path.exists(self.icon_path):
            try:
                self.window.iconbitmap(self.icon_path)
                icon_set = True
            except:
                pass
        
        # နည်းလမ်း ၃: PIL ကိုသုံးခြင်း
        if not icon_set and self.icon_path and os.path.exists(self.icon_path):
            try:
                icon_image = Image.open(self.icon_path)
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.window.iconphoto(True, icon_photo)
                icon_set = True
            except Exception as e:
                print(f"PIL Icon Error: {e}")
        
        if not icon_set:
            print("Could not set icon for about window")
    
    def create_widgets(self):
        frame = ctk.CTkFrame(self.window)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        title_label = ctk.CTkLabel(
            frame, 
            text="Vedi App", 
            font=ctk.CTkFont(family=self.font.cget("family"), size=20, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Version
        version_label = ctk.CTkLabel(
            frame, 
            text="Version 1.0.0", 
            font=self.font
        )
        version_label.pack(pady=5)
        
        # Description
        desc_label = ctk.CTkLabel(
            frame, 
            text="ဇာတာ တွက်ချက်ခြင်း \n© ၂၀၂၅ သူရိန်မင်းကုမ္ပဏီ", 
            font=self.font,
            justify="center"
        )
        desc_label.pack(pady=10)
        
        # Logo
        if self.icon_path and os.path.exists(self.icon_path):
            try:
                logo_image = Image.open(self.icon_path)
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
            text="ပိတ်မည်", 
            font=self.font,
            command=self.window.destroy,
            width=100
        )
        close_button.pack(pady=20)
    
    def show(self):
        self.window.mainloop()