from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout,
    QSizePolicy, QLayout
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys


class LockScreen(QWidget):
    def __init__(self, correct_pin="1234"):
        super().__init__()
        self.correct_pin = correct_pin
        self.entered_pin = ""
        self.image_path = "image/home screen.jpg"  # Change this to your background image path

        self.setWindowTitle("Lock Screen")
        self.setGeometry(100, 100, 800, 480)  # Set default window size

        # Background
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(self.rect())

        # Title
        self.title_label = QLabel("Enter your pin", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Segoe UI", 28))
        self.title_label.setStyleSheet("color: white;")

        # Keypad Grid
        self.keypad_layout = QGridLayout()
        self.keypad_layout.setHorizontalSpacing(24)   # smaller horizontal gap
        self.keypad_layout.setVerticalSpacing(24)    # keep vertical spacing
        self.keypad_layout.setContentsMargins(0, 0, 0, 0)
        self.keypad_layout.setSizeConstraint(QLayout.SetFixedSize)

        buttons = [
            "1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",
            "C", "0", "E"
        ]

        for i, text in enumerate(buttons):
            btn = QPushButton()
            if text == "C":
                btn.setIcon(QIcon.fromTheme("edit-clear"))
            elif text == "E":
                btn.setIcon(QIcon.fromTheme("go-next"))
            else:
                btn.setText(text)

            btn.setFixedSize(120, 120)
            btn.setFont(QFont("Segoe UI", 20, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 60px;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.3);
                }
            """)
            btn.clicked.connect(lambda _, t=text: self.handle_input(t))
            self.keypad_layout.addWidget(btn, i // 3, i % 3)

        # Wrap grid inside a fixed-size container
        self.keypad_container = QWidget()
        self.keypad_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.keypad_container.setLayout(self.keypad_layout)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.title_label)
        layout.addSpacing(20)
        layout.addWidget(self.keypad_container, alignment=Qt.AlignHCenter)
        layout.addStretch(2)
        layout.setContentsMargins(40, 50, 40, 50)  # reduced margins

    def resizeEvent(self, event):
        # Resize background
        pixmap = QPixmap(self.image_path).scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def handle_input(self, key):
        if key == "C":
            self.entered_pin = self.entered_pin[:-1]
        elif key == "E":
            if self.entered_pin == self.correct_pin:
                self.title_label.setText("Access Granted")
                self.entered_pin = ""
            else:
                self.title_label.setText("Wrong PIN. Try again.")
                self.entered_pin = ""
        else:
            if len(self.entered_pin) < 4:
                self.entered_pin += key

        if self.entered_pin:
            self.title_label.setText("•" * len(self.entered_pin))
        else:
            self.title_label.setText("Enter your pin")


# --- Run Standalone LockScreen ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LockScreen()
    window.showFullScreen()  # or use window.show() to show in windowed mode
    sys.exit(app.exec_()) 
