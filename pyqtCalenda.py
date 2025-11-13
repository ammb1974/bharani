from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QDateEdit, QPushButton
from PyQt5.QtCore import QDate
from burmesedate import burmesedate
import sys

class DateConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("မြန်မာ ရက်စွဲ ပြောင်းရန်")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(QLabel("အင်္ဂလိပ် ရက်စွဲ ရွေးပါ"))
        layout.addWidget(self.date_edit)

        self.convert_button = QPushButton("ပြောင်းမယ်")
        self.convert_button.clicked.connect(self.convert_date)
        layout.addWidget(self.convert_button)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)
        self.result_label.setStyleSheet("font-family: 'Myanmar Text'; font-size: 14pt;")

        self.setLayout(layout)

    def convert_date(self):
        qdate = self.date_edit.date()
        year = qdate.year()
        month = qdate.month()
        day = qdate.day()

        bd = burmesedate(year, month, day)
        self.result_label.setText(f"မြန်မာ ရက်စွဲ: {str(bd)}")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DateConverter()
    window.show()
    sys.exit(app.exec_())