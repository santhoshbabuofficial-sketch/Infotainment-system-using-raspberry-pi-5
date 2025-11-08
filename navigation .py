import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

class NavigationUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Full Screen Map")

        # ---------------- FULL SCREEN ----------------
        self.showFullScreen()  # Make the window full screen

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Map widget
        self.map_view = QWebEngineView()
        self.map_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        url = QUrl(
            "https://www.google.com/maps/@9.9178368,78.1228236,10z?entry=ttu&g_ep=EgoyMDI1MDkyMy4wIKXMDSoASAFQAw%3D%3D"
        )
        self.map_view.load(url)

        main_layout.addWidget(self.map_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NavigationUI()
    window.show()
    sys.exit(app.exec_())
