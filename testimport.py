# test_path.py
try:
    import pyswisseph as swe
    print("✅ 'pyswisseph' ကို 'swe' အဖြစ် အောင်စွမ်းစွာ import လုပ်နိုင်ပါတယ်။")
    
    # --- အရေးကြီးဆုံးစစ်ဆေးချက် ---
    print(f"\n'pyswisseph' module ကို ဤနေရာမှ ရယူထားပါသည်:")
    print(swe.__file__)
    
    print("\n" + "="*50)
    print("အထက်က ပေါ်တဲ့ path ကို ကူးပြီး ကျွန်တော့်ကို ပြန်ပေးပါ။")
    print("ဥပမာ - C:\\Python39\\lib\\site-packages\\pyswisseph\\__init__.py လို့ပေါ်ရင် မှန်ပါတယ်။")
    print("ဒါမှမဟုတ် သင့်ရဲ့ project folder ထဲက path ပေါ်ရင် ပြဿနာပါ။")

except Exception as e:
    print(f"❌ Error: {e}")