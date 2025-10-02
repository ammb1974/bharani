import tkinter as tk
from tkinter import ttk

class WindowStateDemo:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.toplevel.title("Window State Control Demo")
        self.toplevel.geometry("600x400")
        
        # Center the window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        
        # Initial window state
        self.window_state = "normal"
        
    def center_window(self):
        """Center the window on screen"""
        self.toplevel.update_idletasks()
        screen_width = self.toplevel.winfo_screenwidth()
        screen_height = self.toplevel.winfo_screenheight()
        window_width = self.toplevel.winfo_width()
        window_height = self.toplevel.winfo_height()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.toplevel.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.toplevel, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Window State Control", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Control buttons
        ttk.Button(
            button_frame, 
            text="Show Minimize Button", 
            command=self.enable_minimize_button
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Hide Minimize Button", 
            command=self.disable_minimize_button
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Show Maximize Button", 
            command=self.enable_maximize_button
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Hide Maximize Button", 
            command=self.disable_maximize_button
        ).pack(side=tk.LEFT, padx=5)
        
        # State control buttons
        state_frame = ttk.Frame(main_frame)
        state_frame.pack(pady=10)
        
        ttk.Button(
            state_frame, 
            text="Minimize Window", 
            command=self.minimize_window
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            state_frame, 
            text="Maximize Window", 
            command=self.maximize_window
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            state_frame, 
            text="Restore Window", 
            command=self.restore_window
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            state_frame, 
            text="Iconify Window", 
            command=self.iconify_window
        ).pack(side=tk.LEFT, padx=5)
        
        # Toggle fullscreen
        ttk.Button(
            state_frame, 
            text="Toggle Fullscreen", 
            command=self.toggle_fullscreen
        ).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame, 
            text="Current State: Normal",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=10)
        
        # Window attributes control
        attr_frame = ttk.Frame(main_frame)
        attr_frame.pack(pady=10)
        
        ttk.Button(
            attr_frame, 
            text="Make Window Tool", 
            command=self.make_tool_window
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            attr_frame, 
            text="Remove Window Tool", 
            command=self.remove_tool_window
        ).pack(side=tk.LEFT, padx=5)
        
        # Info text
        info_text = tk.Text(
            main_frame, 
            height=8, 
            width=70,
            font=("Consolas", 9)
        )
        info_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        info_content = """
Window State Control Methods:
- toplevel.attributes('-toolwindow', 1/0)  : Show/hide minimize/maximize buttons
- toplevel.state('iconic')                 : Minimize window
- toplevel.state('zoomed')                 : Maximize window
- toplevel.state('normal')                 : Restore window
- toplevel.iconify()                       : Minimize to taskbar
- toplevel.deiconify()                     : Restore from taskbar
- toplevel.attributes('-fullscreen', True/False) : Toggle fullscreen

Window Style Flags (Windows only):
- toplevel.attributes('-disabled', 1/0)    : Disable/enable window
- toplevel.attributes('-topmost', 1/0)     : Always on top
        """
        info_text.insert(tk.END, info_content)
        info_text.config(state=tk.DISABLED)
    
    def enable_minimize_button(self):
        """Enable minimize button"""
        self.toplevel.attributes('-toolwindow', False)
        self.update_status("Minimize button enabled")
    
    def disable_minimize_button(self):
        """Disable minimize button"""
        self.toplevel.attributes('-toolwindow', True)
        self.update_status("Minimize button disabled")
    
    def enable_maximize_button(self):
        """Enable maximize button"""
        self.toplevel.resizable(True, True)
        self.toplevel.attributes('-toolwindow', False)
        self.update_status("Maximize button enabled")
    
    def disable_maximize_button(self):
        """Disable maximize button"""
        self.toplevel.resizable(False, False)
        self.update_status("Maximize button disabled")
    
    def minimize_window(self):
        """Minimize the window"""
        self.toplevel.state('iconic')
        self.window_state = 'iconic'
        self.update_status("Window minimized")
    
    def maximize_window(self):
        """Maximize the window"""
        self.toplevel.state('zoomed')
        self.window_state = 'zoomed'
        self.update_status("Window maximized")
    
    def restore_window(self):
        """Restore the window"""
        self.toplevel.state('normal')
        self.window_state = 'normal'
        self.update_status("Window restored")
    
    def iconify_window(self):
        """Iconify the window (minimize to taskbar)"""
        self.toplevel.iconify()
        self.window_state = 'iconic'
        self.update_status("Window iconified")
    
    def deiconify_window(self):
        """Deiconify the window"""
        self.toplevel.deiconify()
        self.window_state = 'normal'
        self.update_status("Window deiconified")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current_state = self.toplevel.attributes('-fullscreen')
        new_state = not current_state
        self.toplevel.attributes('-fullscreen', new_state)
        
        if new_state:
            self.update_status("Fullscreen enabled")
        else:
            self.update_status("Fullscreen disabled")
    
    def make_tool_window(self):
        """Make window a tool window (no minimize/maximize)"""
        self.toplevel.attributes('-toolwindow', True)
        self.update_status("Window set as tool window")
    
    def remove_tool_window(self):
        """Remove tool window attribute"""
        self.toplevel.attributes('-toolwindow', False)
        self.update_status("Tool window attribute removed")
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=f"Current State: {self.window_state} | {message}")

if __name__ == "__main__":
    toplevel = tk.Tk()
    app = WindowStateDemo(toplevel)
    toplevel.mainloop()