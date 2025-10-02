import tkinter as tk

# Constants for canvas dimensions
CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300
CW = 50

def draw_grid():
    # ဝင်းဒိုးဖန်တီးခြင်း
    toplevel = tk.Tk()
    toplevel.title("Graph with 50px Grid")
    
    # Canvas ဖန်တီးခြင်း (အရွယ်အစား 800x600)
    canvas = tk.Canvas(toplevel, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack()
    
    # ဂရစ်လိုင်းများဆွဲခြင်း
    grid_spacing = 50  # အကွာအဝေး ၅၀ pixels
    
    # အလျားလိုက်လိုင်းများ
    for x in range(0, CANVAS_WIDTH, grid_spacing):
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill="lightgray")
    
    # ဒေါင်လိုက်လိုင်းများ
    for y in range(0, CANVAS_HEIGHT, grid_spacing):
        canvas.create_line(0, y, CANVAS_WIDTH, y, fill="lightgray")
    
    # ဥပမာအနေဖြင့် အလယ်တွင် အမှတ်တစ်ခု ဆွဲခြင်း
    center_x, center_y = 150, 150
    radius = 5
    
    # Draw a red marker at the center point
    try:
        canvas.create_oval(center_x - radius, center_y - radius,
                          center_x + radius, center_y + radius,
                          fill="red", tags="center_marker")
    except Exception as e:
        print(f"Error drawing center marker: {e}")
    
    # Draw border with increased width
    try:
        canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 
                              outline="black", width=3, tags="border")
    except Exception as e:
        print(f"Error drawing border: {e}")
    
    # Mouse hover event များကို bind လုပ်ခြင်း
    def on_enter(event, rect_id, text_id=None):
        # Mouse လေးထောင့်ကွက်ထဲဝင်လာတဲ့အခါ
        try:
            canvas.itemconfig(rect_id, fill="#bfce8a")  # အရောင်ပြောင်းခြင်း
            if text_id:  # စာသားရှိရင် စာသားအရောင်လည်းပြောင်း
                canvas.itemconfig(text_id, fill="darkgreen")
        except Exception as e:
            print(f"Error in hover enter event: {e}")
     
    def on_leave(event, rect_id, text_id=None):
        # Mouse လေးထောင့်ကွက်မှထွက်သွားတဲ့အခါ
        try:
            canvas.itemconfig(rect_id, fill="lightblue")  # မူလအရောင်ပြန်ခြင်း
            if text_id:  # စာသားရှိရင် စာသားအရောင်လည်းပြန်ပြောင်း
                canvas.itemconfig(text_id, fill="black")
        except Exception as e:
            print(f"Error in hover leave event: {e}")
    
    # Draw rectangles for Rasi positions
    try:
        # Create rectangles for different positions
        # Top-right quadrant
        rasi_1 = canvas.create_rectangle(2*CW, 0, 4*CW, 2*CW, fill="lightblue", tags="rasi")
        
        # rasi_1 အကွက်ထဲမှာ စာသားထည့်ခြင်း
        # အကွက်ရဲ့ အလယ်ဗဟိုကိုတွက်ချက်ခြင်း
        rasi_1_center_x = (2*CW + 4*CW) / 2
        rasi_1_center_y = (0 + 2*CW) / 2
        rasi_1_text = canvas.create_text(
            rasi_1_center_x, rasi_1_center_y, 
            text="မိဿ", 
            font=("Myanmar Text", 10, "bold"),
            fill="black"
        )
        
        canvas.tag_bind(rasi_1, "<Enter>", lambda e: on_enter(e, rasi_1, rasi_1_text))  # Mouse ဝင်လာတဲ့အခါ
        canvas.tag_bind(rasi_1, "<Leave>", lambda e: on_leave(e, rasi_1, rasi_1_text))  # Mouse ထွက်သွားတဲ့အခါ
        
        # Bottom-left quadrant
        rasi_2 = canvas.create_rectangle(0, 2*CW, 2*CW, 4*CW, fill="lightblue", tags="rasi")
        
        rasi_2_center_x = (0 + 2*CW) / 2
        rasi_2_center_y = (2*CW + 4*CW) / 2
        rasi_2_text = canvas.create_text(
            rasi_2_center_x, rasi_2_center_y, 
            text="ကရကဋ်", 
            font=("Myanmar Text", 10, "bold"),
            fill="black"
        )
        canvas.tag_bind(rasi_2, "<Enter>", lambda e: on_enter(e, rasi_2))  # Mouse ဝင်လာတဲ့အခါ
        canvas.tag_bind(rasi_2, "<Leave>", lambda e: on_leave(e, rasi_2))  # Mouse ထွက်သွားတဲ့အခါ
        

        rasi_3 = canvas.create_rectangle(2*CW, 4*CW, 4*CW, 6*CW, fill="lightblue", tags="rasi")
        
        rasi_3_center_x = ( 2*CW + 4*CW) / 2
        rasi_3_center_y = (4*CW + 6*CW) / 2
        rasi_3_text = canvas.create_text(
            rasi_3_center_x, rasi_3_center_y, 
            text="တူ", 
            font=("Myanmar Text", 10, "bold"),
            fill="black"
        )   
    
        canvas.tag_bind(rasi_3, "<Enter>", lambda e: on_enter(e, rasi_3))  # Mouse ဝင်လာတဲ့အခါ
        canvas.tag_bind(rasi_3, "<Leave>", lambda e: on_leave(e, rasi_3))  # Mouse ထွက်သွားတဲ့အခါ
        
        rasi_4 = canvas.create_rectangle(4*CW, 2*CW, 6*CW, 4*CW, fill="lightblue", tags="rasi")
        
        rasi_4_center_x =250
        rasi_4_center_y = 150
        rasi_4_text = canvas.create_text(
            rasi_4_center_x, rasi_4_center_y, 
            text="မကာရ", 
            font=("Myanmar Text", 10, "bold"),
            fill="black"
        )   

        canvas.tag_bind(rasi_4, "<Enter>", lambda e: on_enter(e, rasi_4))  # Mouse ဝင်လာတဲ့အခါ
        canvas.tag_bind(rasi_4, "<Leave>", lambda e: on_leave(e, rasi_4))  # Mouse ထွက်သွားတဲ့အခါ
    except Exception as e:
        print(f"Error creating rectangles: {e}")
    
    # ဝင်းဒိုးပြသခြင်း
    toplevel.mainloop()

# ဖန်ရှင်ကိုခေါ်ခြင်း
draw_grid()