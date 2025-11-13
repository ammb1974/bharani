# ui_mainwindow.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QDateEdit, QGridLayout, QFrame)
from PyQt5.QtCore import QDate, Qt
from zburmese_clendar import convert
from zconstants import MYANMAR_WEEKDAYS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("မြန်မာပြက္ခဒိန်")
        self.setGeometry(100, 100, 500, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.init_ui()
        
    def init_ui(self):
        # Input Section
        input_layout = QHBoxLayout()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        
        self.convert_button = QPushButton("ပြောင်းမည်")
        
        input_layout.addWidget(QLabel("အင်္ဂလိပ်ရက်စွဲ:"))
        input_layout.addWidget(self.date_edit)
        input_layout.addWidget(self.convert_button)
        input_layout.addStretch()
        
        # Output Section
        self.output_frame = QFrame()
        self.output_frame.setFrameShape(QFrame.StyledPanel)
        output_layout = QVBoxLayout(self.output_frame)
        
        self.result_label = QLabel("ရလဒ်ကို ဒီမှာကြည့်ပါ")
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        self.result_label.setAlignment(Qt.AlignCenter)
        
        output_layout.addWidget(self.result_label)
        
        # Calendar View Section
        self.calendar_grid = QGridLayout()
        self.calendar_grid.setSpacing(2)
        
        # Add weekday headers
        for i, day_name in enumerate(MYANMAR_WEEKDAYS):
            header = QLabel(day_name)
            header.setStyleSheet("font-weight: bold; background-color: #f0f0f0; padding: 5px;")
            header.setAlignment(Qt.AlignCenter)
            self.calendar_grid.addWidget(header, 0, i)
            
        # Add empty labels for days
        for row in range(1, 7):
            for col in range(7):
                day_label = QLabel("")
                day_label.setAlignment(Qt.AlignCenter)
                day_label.setStyleSheet("border: 1px solid #ccc; padding: 5px;")
                self.calendar_grid.addWidget(day_label, row, col)

        # Add all sections to main layout
        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.output_frame)
        self.layout.addLayout(self.calendar_grid)
        
        # Connect signals
        self.convert_button.clicked.connect(self.update_conversion)
        self.date_edit.dateChanged.connect(self.update_conversion)
        
        # Initial conversion
        self.update_conversion()

    def update_conversion(self):
        gregorian_date = self.date_edit.date().toPyDate()
        
        try:
            burmese_date = convert(gregorian_date)
            self.result_label.setText(str(burmese_date))
            # TODO: Update calendar view here
            # self.update_calendar_view(burmese_date)
        except Exception as e:
            self.result_label.setText(f"အမှား: {e}")
            
    def update_calendar_view(self, burmese_date):
        # This is a placeholder for updating the monthly calendar grid
        # You would need to calculate the start day of the month and the number of days
        # and then populate the grid accordingly.
        # For now, it's left as an exercise.
        pass
