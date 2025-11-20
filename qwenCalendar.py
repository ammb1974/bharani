import sys
import requests
import json
import datetime # လိုအပ်လာပါသည်
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# --- မှန်ကန်တဲ့ Library ကို Import လုပ်ခြင်း ---
from mmcal import to_myanmar


# --- Horoscope ဆိုင်ရာ Function ---

def get_horoscope(sign: str, day: str = "today") -> str:
    """
    API မှ Horoscope အချက်အလက်များယူရန်။
    """
    url = f"http://sandipbgt.com/theastrologer/api/horoscope/{sign}/{day}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('horoscope', "ဟောစာတမ်းမတွေ့ပါ။")
    except requests.exceptions.RequestException as e:
        return f"ကွန်ယက်ချိတ်ဆက်မှုမအောင်မြင်ပါ: {e}"
    except Exception as e:
        return f"အမှားတစ်ခုဖြစ်ပွားခဲ့သည်: {e}"

# --- Myanmar Calendar ဆိုင်ရာ Functions ---

def get_myanmar_calendar_info() -> dict:
    """
    လက်ရှိရက်စွဲအတွက် မြန်မာပြက္ခဒိန်အချက်အလက်များရယူခြင်း။
    """
    try:
        # MyanmarDateConverter ကို စတင်ခြင်း
        converter = to_myanmar()
        
        # လက်ရှိ Gregorian ရက်စွဲကို မြန်မာပြက္ခဒိန်သို့ ပြောင်းလဲခြင်း
        today_gregorian = datetime.date.today()
        myanmar_date = converter.gregorian_to_myanmar(today_gregorian)
        
        # ပြက္ခဒိန်အချက်အလက်များထုတ်ယူခြင်း
        year = myanmar_date.year
        year_name = myanmar_date.year_name
        month_name = myanmar_date.month_name
        moon_phase = myanmar_date.moon_phase_name # လကွာ/လဆန်း/လပြည့်
        fortnight_day = myanmar_date.fortnight_day # ရက်နံပါတ်
        weekday = myanmar_date.weekday_name # တနင်္ဂနွေ/တနင်္လာ...
        
        # နေ့ထူးနေ့မြတ် (Sabbath) ကိုစစ်ဆေးခြင်း
        sabbath = "နေ့ထူးနေ့မြတ်" if myanmar_date.is_sabbath else ""

        return {
            "year": year,
            "year_name": year_name,
            "month_name": month_name,
            "moon_phase": moon_phase,
            "fortnight_day": fortnight_day,
            "weekday": weekday,
            "sabbath": sabbath,
            "is_watat": myanmar_date.is_watat # Library ကိုယ်တိုင် ပေးတဲ့ ဝါထပ်နှစ်ဖြစ်မဖြစ်
        }
    except Exception as e:
        return {"error": f"မြန်မာပြက္ခဒိန်ဖတ်ရာတွင်အမှား: {e}"}

# --- PyQt5 GUI Application ---

class HoroscopeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("မြန်မာပြက္ခဒိန်နှင့် ဟောစာတမ်း")
        self.setGeometry(200, 200, 600, 500)

        # မြန်မာစာအတွက် Font ဆက်တင်
        self.myanmar_font = QFont("Myanmar Text", 12) 
        self.label_font = QFont("Myanmar Text", 10, QFont.Bold)

        # Main Widget နှင့် Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- မြန်မာပြက္ခဒိန်အပိုင်း ---
        myanmar_info_layout = QVBoxLayout()
        myanmar_title = QLabel("ယနေ့ မြန်မာပြက္ခဒိန်")
        myanmar_title.setFont(self.label_font)
        myanmar_title.setAlignment(Qt.AlignCenter)
        
        self.myanmar_date_label = QLabel()
        self.myanmar_date_label.setFont(self.myanmar_font)
        self.myanmar_date_label.setAlignment(Qt.AlignCenter)
        self.myanmar_date_label.setWordWrap(True)
        
        myanmar_info_layout.addWidget(myanmar_title)
        myanmar_info_layout.addWidget(self.myanmar_date_label)
        main_layout.addLayout(myanmar_info_layout)

        # --- Horoscope ရွေးချယ်ရေးအပိုင်း ---
        horoscope_select_layout = QHBoxLayout()
        zodiac_label = QLabel("သင့်ရာသီကိုရွေးပါ:")
        zodiac_label.setFont(self.myanmar_font)
        
        self.zodiac_combo = QComboBox()
        self.zodiac_combo.setFont(self.myanmar_font)
        zodiac_names_my = {
            "aries": "မိန်ခါ", "taurus": "ဝေဿ", "gemini": "ပြိတ္တာ", "cancer": "ကရကဋ",
            "leo": "သိဟ်", "virgo": "ကန်ည", "libra": "တူလာ", "scorpio": "ဝိစ္ဆိက",
            "sagittarius": "ဓနု", "capricorn": "မကာ", "aquarius": "ကုမ္ဘ", "pisces": "မိန"
        }
        self.zodiac_combo.clear()
        for key, value in zodiac_names_my.items():
            self.zodiac_combo.addItem(value, key)

        self.get_button = QPushButton("ဟောစာတမ်းကြည့်ရှုရန်")
        self.get_button.setFont(self.myanmar_font)
        self.get_button.clicked.connect(self.show_horoscope)

        horoscope_select_layout.addWidget(zodiac_label)
        horoscope_select_layout.addWidget(self.zodiac_combo)
        horoscope_select_layout.addWidget(self.get_button)
        main_layout.addLayout(horoscope_select_layout)

        # --- ရလဒ်ပြရေးအပိုင်း ---
        self.result_text = QTextEdit()
        self.result_text.setFont(self.myanmar_font)
        self.result_text.setPlaceholderText("ဟောစာတမ်းရလဒ်ကို ဤနေရာတွင်ပြပေးပါမည်။")
        main_layout.addWidget(self.result_text)

        # Application စတင်တိုင်း မြန်မာပြက္ခဒိန်အချက်အလက်ကို အလိုလို update လုပ်ပေးခြင်း
        self.update_myanmar_date()

    def update_myanmar_date(self):
        """မြန်မာပြက္ခဒိန် Label ကို အပ်ဒိတ်လုပ်ခြင်း"""
        info = get_myanmar_calendar_info()
        if "error" in info:
            self.myanmar_date_label.setText(info["error"])
        else:
            date_str = (
                f"သက္ကရာဇ် - {info['year_name']}၊ "
                f"လ - {info['month_name']} {info['moon_phase']} {info['fortnight_day']}ရက်၊ "
                f"{info['weekday']}နေ့"
            )
            if info['sabbath']:
                date_str += f" ({info['sabbath']})"
            
            # --- ဝါထပ်နှစ်စစ်ဆေးခြင်း (Library ကိုယ်တိုင်ပေးတဲ့ တန်ဖိုးနဲ့) ---
            if info['is_watat']:
                date_str += " (ဝါထပ်နှစ်ဖြစ်ပါသည်)"
            
            self.myanmar_date_label.setText(date_str)

    def show_horoscope(self):
        """Button ကိုနှိပ်လိုက်လျှင် Horoscope ကိုပြခြင်း"""
        selected_sign_key = self.zodiac_combo.currentData()
        selected_sign_name = self.zodiac_combo.currentText()
        
        self.result_text.setText(f"{selected_sign_name}ရာသီအတွက် ဟောစာတမ်းကို ရယူနေသည်...")
        
        horoscope_text = get_horoscope(selected_sign_key)
        
        final_text = f"--- {selected_sign_name} ရာသီနေ့စဉ်ဟောစာတမ်း ---\n\n{horoscope_text}"
        self.result_text.setText(final_text)

# --- Main Execution ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HoroscopeApp()
    window.show()
    sys.exit(app.exec_())