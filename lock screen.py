from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout,
    QSizePolicy, QLayout
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys, os, subprocess


class LockScreen(QWidget):
    def __init__(self, correct_pin="1234"):
        super().__init__()
        self.correct_pin = correct_pin
        self.entered_pin = ""
        self.image_path = "image/home screen.jpg"  

        # --- FILES ---
        self.home_file = r"D:\infotainment system\home screen.py"   # Open by swipe
        self.main_file = r"D:\infotainment system\main menu.py"     # Open by PIN

        self.start_pos = None  # for swipe detection

        self.setWindowTitle("Lock Screen")
        self.setGeometry(100, 100, 800, 480)

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
        self.keypad_layout.setHorizontalSpacing(24)
        self.keypad_layout.setVerticalSpacing(24)
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
        layout.setContentsMargins(40, 50, 40, 50)

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
                self.open_main_screen()   # ✅ PIN correct → main screen
            else:
                self.title_label.setText("Wrong PIN. Try again.")
                self.entered_pin = ""
        else:
            if len(self.entered_pin) < 4:
                self.entered_pin += key

        if self.entered_pin:
            self.title_label.setText("•" * len(self.entered_pin))
        elif key != "E":
            self.title_label.setText("Enter your pin")

    def mousePressEvent(self, event):
        """Detect swipe start"""
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()

    def mouseReleaseEvent(self, event):
        """Detect swipe end"""
        if self.start_pos:
            delta = self.start_pos - event.pos()
            # Right → Left swipe (movement in X > 80px)
            if delta.x() > 80:
                self.open_home_screen()  # ✅ Always go to home screen
            self.start_pos = None

    def open_home_screen(self):
        """Open home screen by swipe"""
        if os.path.exists(self.home_file):
            print(f"Opening {self.home_file}")
            subprocess.Popen(["python", self.home_file])
            QApplication.quit()
        else:
            print("Home screen file not found!")

    def open_main_screen(self):
        """Open main screen by correct PIN"""
        if os.path.exists(self.main_file):
            print(f"Opening {self.main_file}")
            subprocess.Popen(["python", self.main_file])
            QApplication.quit()
        else:
            print("Main screen file not found!")


# --- Run Standalone LockScreen ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LockScreen()
    window.showFullScreen()
    sys.exit(app.exec_())
