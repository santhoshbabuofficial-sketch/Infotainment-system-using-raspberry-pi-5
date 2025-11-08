from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QDateTime, QSize, QEvent
import sys
import os

class ClockWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Screen")   # ✅ Changed title here
        self.image_path = "image/home screen.jpg"

        # Path to your background image
        if not os.path.exists(self.image_path):
            print("Background image not found!")
            sys.exit()

        # Setup background label
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)  # Scale pixmap with label
        self.background_label.lower()  # Send label to back

        # Setup time label
        self.time_label = QLabel(self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("color: white;")
        self.time_label.setFont(QFont("Segoe UI", 100, QFont.Light))
        self.time_label.raise_()  # Ensure it's above background

        # Setup date label
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setStyleSheet("color: white;")
        self.date_label.setFont(QFont("Segoe UI", 30))
        self.date_label.raise_()

        # Timer to refresh every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()  # Initial time update

        # Install event filter for resize events
        self.installEventFilter(self)
        # Trigger initial resize handling
        self.resizeEvent(None)
        self.showFullScreen()  # Enter fullscreen mode immediately

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            self.handle_resize(event.size())
        return super().eventFilter(obj, event)

    def handle_resize(self, new_size: QSize):
        # Scale and display background
        pixmap = QPixmap(self.image_path).scaled(
            new_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, new_size.width(), new_size.height())

        # Center time label
        self.time_label.setGeometry(
            0,
            new_size.height() // 2 - 150,
            new_size.width(),
            150
        )
        # Place date label below time
        self.date_label.setGeometry(
            0,
            new_size.height() // 2 + 20,
            new_size.width(),
            100
        )

    def resizeEvent(self, event):
        # Override resizeEvent to handle initial geometry without QEvent
        size = event.size() if event else self.size()
        self.handle_resize(size)

    def update_time(self):
        current = QDateTime.currentDateTime()
        self.time_label.setText(current.toString("hh:mm"))
        self.date_label.setText(current.toString("dd MMMM, dddd"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClockWindow()
    window.show()
    sys.exit(app.exec_())
