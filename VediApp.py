import customtkinter as ctk
import tkinter as tk
import ctypes

import os
import subprocess
import sys

from tkinter import Menu, Toplevel, font as tkfont, ttk
from PIL import Image, ImageTk
from About import AboutWindow

import swisseph as swe  
import datetime
from typing import Dict, List, Tuple
import importlib
import runpy
import newBuild


# Main application setup
app = ctk.CTk()
app.title("Vedi")
# Fullscreen mode

def set_zoomed():
    try:
        app.state('zoomed')
    except Exception:
        pass

def open_new_build():
    """
    Try to open newBuild.py as a child window:
    1) Prefer importing newBuild and calling a create_window / NewBuildWindow / main API if available.
    2) Fallback to launching newBuild.py as a separate process.
    """
    try:
        import importlib.util

        # Try to import newBuild as a module
        spec = importlib.util.find_spec("newBuild")
        if spec is not None:
            newBuild = importlib.import_module("newBuild")

            # If newBuild exposes a dedicated creator, use it
            if hasattr(newBuild, "create_window"):
                # create_window(parent) is expected to create a Toplevel on the given parent
                newBuild.create_window(app)
                return

            if hasattr(newBuild, "NewBuildWindow"):
                # NewBuildWindow(parent) expected to return a window instance or create on its own
                try:
                    newBuild.NewBuildWindow(app)
                except TypeError:
                    # try without parent
                    newBuild.NewBuildWindow()
                return

            if hasattr(newBuild, "main"):
                # Try to call main with a Toplevel parent if it accepts one
                win = tk.Toplevel(app)
                win.transient(app)
                win.grab_set()
                try:
                    newBuild.main(win)
                except TypeError:
                    # main() might not accept args; call it anyway (it may create its own window)
                    newBuild.main()
                return

            # If module exists but none of the above, attempt to execute its code within a Toplevel namespace
            win = tk.Toplevel(app)
            win.transient(app)
            win.grab_set()
            # run the file in a fresh globals dict so widgets created will attach to the current Tcl interpreter
            mod_path = spec.origin
            try:
                # Ensure the working directory is the module's folder so relative imports/resources work
                cwd = os.getcwd()
                os.chdir(os.path.dirname(mod_path) or cwd)
                runpy.run_path(mod_path, run_name="__main__")
            finally:
                os.chdir(cwd)
            return

        # If not importable, fallback to launching as a separate process
        script_path = os.path.join(os.path.dirname(__file__), "newBuild.py")
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"newBuild.py not found at {script_path}")

        subprocess.Popen([sys.executable, script_path])
    except Exception as e:
        print(f"Error opening newBuild.py: {e}")
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Cannot open New Build: {e}")
        except Exception:
            pass
        # Alternative: messagebox နဲ့ error ပြခြင်း
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", f"Cannot open New Build: {e}")

# Toolbar creation function ကို ပြင်ဆင်ခြင်း
def create_toolbar(parent):
    # Toolbar Frame ဖန်တီးခြင်း
    toolbar_frame = ctk.CTkFrame(parent, height=40)
    toolbar_frame.pack(side="top", fill="x", padx=5, pady=5)
    
    # New Button - command ကို open_new_build သတ်မှတ်ခြင်း
    new_button = ctk.CTkButton(
        toolbar_frame, 
        text="New", 
        width=60, 
        height=30,
        command=open_new_build  # ဒီမှာ ပြင်ဆင်လိုက်ပါ
    )
    new_button.pack(side="left", padx=2)

# Icon setup
icon_path = "VediIcon.ico"
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.vedic.app")
except Exception as e:
    print(f"Taskbar Icon Error: {e}")

if os.path.exists(icon_path):
    app.iconbitmap(icon_path)
else:
    print(f"Icon file not found at: {icon_path}")

# Myanmar Unicode Font ရွေးချယ်ခြင်း
def get_myanmar_font():
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


# Menu bar creation
menubar = Menu(app)
app.config(menu=menubar)

# File Menu
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New", command=open_new_build, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=lambda: print("Open clicked"))
file_menu.add_command(label="Save", command=lambda: print("Save clicked"))
file_menu.add_command(label="Print", command=lambda: print("Print clicked"), accelerator="Ctrl+P")
file_menu.add_separator()
file_menu.add_command(label="Exit (Alt+F4)", command=app.quit)

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

# About window function
def show_about():
    about_window = AboutWindow(app, icon_path=icon_path, font_family=get_myanmar_font())
    about_window.show()
    # Set about window icon
    icon_set = False
    try:
        about_window.iconbitmap(app.iconbitmap())
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

about_menu.add_command(label="Version", command=show_about)
about_menu.add_command(label="Help", command=lambda: print("About Help clicked"))

# Toolbar creation function
def create_toolbar(parent):
    # Toolbar Frame ဖန်တီးခြင်း
    toolbar_frame = ctk.CTkFrame(parent, height=40)
    toolbar_frame.pack(side="top", fill="x", padx=5, pady=5)
    
    # Toolbar Buttons ဖန်တီးခြင်း
    # New Button
    new_button = ctk.CTkButton(
        toolbar_frame, 
        text="New", 
        width=60, 
        height=30,
        command=lambda: print("New clicked")
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
    
    return toolbar_frame

def create_enhanced_a4_frame(parent):
    # Main content frame
    main_frame = ctk.CTkFrame(parent)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Calculate A4 aspect ratio (1:√2)
    a4_width = 595
    a4_height = 842
    
    # Get screen dimensions
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    
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
    a4_container = ctk.CTkScrollableFrame(
        main_frame,
        width=scaled_width,
        height=scaled_height,
        border_width=2,
        border_color="gray",
        fg_color="white"
    )
    
    # A4 Frame ကို screen အလယ်တွင်ချိန်ခြင်း
    a4_container.place(relx=0.5, rely=0.5, anchor="center")
    
    # Ruler (အပေါ်ကအတိုင်း)
    ruler = ctk.CTkFrame(a4_container, height=20, fg_color="#f0f0f0")
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
    content_frame = ctk.CTkFrame(a4_container, fg_color="white")
    content_frame.pack(fill="both", expand=True, padx=int(20 * scale_factor), pady=int(10 * scale_factor))
    
    # Text area
    content_text = ctk.CTkTextbox(
        content_frame,
        font=("Myanmar Text", int(12 * scale_factor)),  # Scale font size
        fg_color="white",
        text_color="black",
        wrap="word"
    )
   # content_text.pack(fill="both", expand=True)
    
    # Sample content
    content_text.insert("1.0", 
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
            
            content_frame.pack_configure(padx=padx_value, pady=pady_value)
            
        except Exception as e:
            print(f"Resize error: {e}")
            # Fallback to safe values
            content_frame.pack_configure(padx=5, pady=5)
    
    # Bind resize event to the main frame
    main_frame.bind("<Configure>", on_resize)
    
    return main_frame, a4_container, content_frame

# Toolbar ဖန်တီးခြင်း
#toolbar = create_toolbar(app)

# A4 Frame ဖန်တီးခြင်း
main_frame, a4_frame, content_frame = create_enhanced_a4_frame(app)

# Keyboard shortcuts
app.bind('<Control-p>', lambda e: print("Print clicked"))
app.bind('<Alt-F4>', lambda e: app.quit())

#app.state('zoomed')
app.after(100, set_zoomed)
# Run the application
app.mainloop()