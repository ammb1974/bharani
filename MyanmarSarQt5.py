import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QLabel, QPushButton, 
                            QComboBox, QSpinBox)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt

class MyanmarTextTester(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("မြန်မာစာ စမ်းသပ်ခြင်း (PyQt5)")
        self.setGeometry(100, 100, 600, 400)
        
        # မြန်မာဖောင့်များစာရင်း
        self.myanmar_fonts = [
            "Noto Sans Myanmar",
            "Pyidaungsu",
            "TharLon",
            "Myanmar3",
            "Myanmar Text",
            "Masterpiece Uni Round"
        ]
        
        # အဓိက UI တည်ဆောက်ခြင်း
        self.init_ui()
        
        # စနစ်မှာ ရှိတဲ့ ဖောင့်များကို စစ်ဆေးခြင်း
        self.check_available_fonts()
    
    def init_ui(self):
        # အဓိက widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # ဖောင့်ရွေးချယ်မှု အပိုင်း
        font_layout = QHBoxLayout()
        font_label = QLabel("ဖောင့်:")
        self.font_combo = QComboBox()
        self.font_combo.addItems(self.myanmar_fonts)
        self.font_combo.currentTextChanged.connect(self.change_font)
        
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(14)
        self.size_spin.valueChanged.connect(self.change_font)
        
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_combo)
        font_layout.addWidget(QLabel("Size:"))
        font_layout.addWidget(self.size_spin)
        main_layout.addLayout(font_layout)
        
        # စာရိုက်နိုင်သော နေရာ
        input_label = QLabel("စာရိုက်ထည့်ပါ:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("မြန်မာစာ ရိုက်ထည့်ပါ...")
        self.input_field.textChanged.connect(self.update_output)
        main_layout.addWidget(input_label)
        main_layout.addWidget(self.input_field)
        
        # ရလဒ်ပြသရန် နေရာ
        output_label = QLabel("ရလဒ်:")
        self.output_label = QLabel()
        self.output_label.setWordWrap(True)
        self.output_label.setAlignment(Qt.AlignTop)
        self.output_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;")
        main_layout.addWidget(output_label)
        main_layout.addWidget(self.output_label)
        
        # လုပ်ဆောင်ချက်ခလုတ်များ
        button_layout = QHBoxLayout()
        clear_btn = QPushButton("ရှင်းလင်းရန်")
        clear_btn.clicked.connect(self.clear_fields)
        copy_btn = QPushButton("ကူးယူရန်")
        copy_btn.clicked.connect(self.copy_text)
        
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(copy_btn)
        main_layout.addLayout(button_layout)
        
        # စနစ်သတင်းအချက်အလက်
        self.info_label = QLabel()
        self.info_label.setStyleSheet("color: #666; font-size: 10px;")
        main_layout.addWidget(self.info_label)
        
        # မူလဖောင့်သတ်မှတ်ခြင်း
        self.change_font(self.myanmar_fonts[0])
    
    def check_available_fonts(self):
        """စနစ်မှာ ရှိတဲ့ ဖောင့်များကို စစ်ဆေးခြင်း"""
        available_fonts = QFontDatabase().families()
        available_myanmar = [f for f in self.myanmar_fonts if f in available_fonts]
        
        info_text = f"စနစ်မှာရှိတဲ့ မြန်မာဖောင့်များ: {', '.join(available_myanmar) or 'မရှိပါ'}"
        self.info_label.setText(info_text)
        
        if not available_myanmar:
            self.info_label.setStyleSheet("color: red; font-size: 10px;")
            self.info_label.setText("သတိပေးချက်: စနစ်မှာ မြန်မာဖောင့်မရှိပါ။ ဖောင့်များကို ဦးစွာထည့်သွင်းပါ။")
    
    def change_font(self, font_name):
        """ဖောင့်ပြောင်းလဲခြင်း"""
        font_size = self.size_spin.value()
        font = QFont(font_name, font_size)
        
        self.input_field.setFont(font)
        self.output_label.setFont(font)
        
        # လက်ရှိရွေးချယ်ထားတဲ့ ဖောင့်ကို ပြသခြင်း
        self.info_label.setText(
            f"လက်ရှိဖောင့်: {font_name} (Size: {font_size}) | " +
            f"စနစ်မှာရှိတဲ့ မြန်မာဖောင့်များ: {', '.join([f for f in self.myanmar_fonts if f in QFontDatabase().families()]) or 'မရှိပါ'}"
        )
    
    def update_output(self, text):
        """စာသားပြောင်းလဲမှုကို အလိုအလျောက်ပြန်ပြခြင်း"""
        self.output_label.setText(text)
    
    def clear_fields(self):
        """စာကွက်များကို ရှင်းလင်းခြင်း"""
        self.input_field.clear()
        self.output_label.clear()
    
    def copy_text(self):
        """စာသားကို ကူးယူခြင်း"""
        text = self.input_field.text()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.info_label.setText(f"'{text}' ကို ကူးယူပြီးပါပြီ")
        else:
            self.info_label.setText("ကူးယူဖို့ စာမရှိပါ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # ခေတ်ပေါ်ပုံစံ
    window = MyanmarTextTester()
    window.show()
    sys.exit(app.exec_())