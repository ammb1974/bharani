import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QPushButton, QLabel, QVBoxLayout, QWidget
from ggconverter import convert_to_myanmar

class MyanmarCalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Myanmar Calendar")
        self.setGeometry(100, 100, 400, 400)

        self.calendar = QCalendarWidget()
        self.button = QPushButton("Convert to Myanmar Date")
        self.label = QLabel("Myanmar Date will appear here")

        self.button.clicked.connect(self.show_myanmar_date)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_myanmar_date(self):
        date = self.calendar.selectedDate()
        year = date.year()
        month = date.month()
        day = date.day()

        my_date = convert_to_myanmar(year, month, day)
        text = f"Myanmar Date: {my_date.year}-{my_date.month}-{my_date.day}\n"
        text += f"Waxing: {my_date.waxing}, Moon Phase: {my_date.moon_phase}\n"
        text += f"Month Type: {my_date.month_type.name}"
        self.label.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyanmarCalendarApp()
    window.show()
    sys.exit(app.exec_())
