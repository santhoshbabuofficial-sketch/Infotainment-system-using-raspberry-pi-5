import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QMainWindow, QFrame
)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont, QPixmap, QIcon


class InfotainmentUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Infotainment UI")
        self.showFullScreen()
        # --- Central widget & layout ---
        self.central = QWidget(self)
        self.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout(self.central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

         # --- Background Image ---
        self.bg_label = QLabel(self.central)
        self.bg_pixmap = QPixmap("image/main menu.jpg")
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        if not self.bg_pixmap.isNull():
            self.bg_label.setPixmap(
                self.bg_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            )
        self.bg_label.lower()

        # --- Foreground UI ---
        self.frame = QFrame(self.central)
        
        # File paths for other applications
        self.control_panel_path = "D:/infotainment system/control panel.py"
        self.navigation_path = "D:/infotainment system/navigation menu.py"
        self.model_path = r"D:\infotainment system\3d model\smart electric bicycle fixed.glb"
        
        # Initialize 3D model attributes
        self.model_placeholder = None
        self.launch_3d_btn = None
        
        self.init_ui()

    def resizeEvent(self, event):
        # Resize background to fill window
        if hasattr(self, 'bg_pixmap') and not self.bg_pixmap.isNull():
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
            self.bg_label.setPixmap(
                self.bg_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            )
        
        # Keep 3D placeholder centered if it exists
        if hasattr(self, 'model_placeholder') and self.model_placeholder:
            center_x = (self.width() - 800) // 2
            center_y = (self.height() - 600) // 2
            self.model_placeholder.setGeometry(center_x, center_y, 800, 600)
            
        if hasattr(self, 'launch_3d_btn') and self.launch_3d_btn:
            center_x = (self.width() - 800) // 2
            center_y = (self.height() - 600) // 2
            self.launch_3d_btn.setGeometry(center_x + 300, center_y - 50, 200, 40)
        
        super().resizeEvent(event)

    def launch_3d_viewer(self):
        """Launch Open3D viewer in separate process"""
        try:
            # Create a temporary Python file with the Open3D code
            open3d_code = '''
import open3d as o3d
import sys

model_path = r"D:\\infotainment system\\3d model\\smart electric bicycle fixed.glb"

try:
    # Initialize the GUI application
    o3d.visualization.gui.Application.instance.initialize()

    # Create a window
    window = o3d.visualization.gui.Application.instance.create_window("3D Vehicle Model", 800, 600)

    # Create a scene widget
    scene_widget = o3d.visualization.gui.SceneWidget()
    scene_widget.scene = o3d.visualization.rendering.Open3DScene(window.renderer)

    # Load GLB model with materials and textures
    model = o3d.io.read_triangle_model(model_path)
    scene_widget.scene.add_model("model", model)

    # Setup camera
    bounds = scene_widget.scene.bounding_box
    scene_widget.setup_camera(35, bounds, bounds.get_center())

    # Add scene widget to the window
    window.add_child(scene_widget)

    # Run the GUI app
    o3d.visualization.gui.Application.instance.run()
except Exception as e:
    print(f"Error: {e}")
    input("Press Enter to close...")
'''
            
            # Write the code to a temporary file
            temp_file = "temp_3d_viewer.py"
            with open(temp_file, 'w') as f:
                f.write(open3d_code)
            
            # Launch in separate process
            subprocess.Popen([sys.executable, temp_file])
            
        except Exception as e:
            print(f"Error launching 3D viewer: {e}")

    # ---- UI elements ----
    def init_ui(self):
        # --- 3D Model Placeholder in Center ---
        self.model_placeholder = QLabel("3D Model Viewer\n(Open3D requires separate window)", self.central)
        center_x = (self.width() - 800) // 2
        center_y = (self.height() - 600) // 2
        self.model_placeholder.setGeometry(center_x, center_y, 800, 600)
        self.model_placeholder.setAlignment(Qt.AlignCenter)
        self.model_placeholder.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0.7);
                color: white;
                font-size: 24px;
                border: 2px solid #3498db;
                border-radius: 10px;
            }
        """)
        self.model_placeholder.setFont(QFont("Arial", 16, QFont.Bold))

        # Launch 3D Viewer Button
        self.launch_3d_btn = QPushButton("Launch 3D Model", self.central)
        self.launch_3d_btn.setGeometry(center_x + 300, center_y - 50, 200, 40)
        self.launch_3d_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.launch_3d_btn.clicked.connect(self.launch_3d_viewer)

        # Power Button
        self.power_btn = QPushButton("⏻", self.central)
        self.power_btn.setGeometry(20, 20, 50, 50)
        self.power_btn.setStyleSheet("font-size: 30px; color: black; background: transparent; border: none;")
        self.power_btn.clicked.connect(self.show_black_screen)

        # Clock & Date
        self.clock_label = QLabel(self.central)
        self.clock_label.setAlignment(Qt.AlignCenter)
        self.clock_label.setFont(QFont("Arial", 60, QFont.Bold))
        self.clock_label.setGeometry(825, 100, 300, 80)
        self.clock_label.setStyleSheet("color: black; background: transparent;")

        self.date_label = QLabel(self.central)
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setFont(QFont("Arial", 16))
        self.date_label.setGeometry(825, 180, 330, 30)
        self.date_label.setStyleSheet("color: black; background: transparent;")

        # Update Clock
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

        # Indicators
        self.left_indicator = QPushButton(self.central)
        self.left_indicator.setGeometry(20, 120, 100, 100)
        self.left_indicator.setStyleSheet("background: transparent; border: none;")
        self.left_indicator.setIcon(QIcon("image/left indicator off.png"))
        self.left_indicator.setIconSize(self.left_indicator.size())
        self.left_blink = False
        self.left_timer = QTimer(self)
        self.left_timer.timeout.connect(self.toggle_left_indicator)
        self.left_stop_timer = QTimer(self)
        self.left_stop_timer.setSingleShot(True)
        self.left_stop_timer.timeout.connect(self.stop_left_indicator)
        self.left_indicator.clicked.connect(self.start_left_blink)

        self.right_indicator = QPushButton(self.central)
        self.right_indicator.setGeometry(1800, 120, 100, 100)
        self.right_indicator.setStyleSheet("background: transparent; border: none;")
        self.right_indicator.setIcon(QIcon("image/right indicator off.png"))
        self.right_indicator.setIconSize(self.right_indicator.size())
        self.right_blink = False
        self.right_timer = QTimer(self)
        self.right_timer.timeout.connect(self.toggle_right_indicator)
        self.right_stop_timer = QTimer(self)
        self.right_stop_timer.setSingleShot(True)
        self.right_stop_timer.timeout.connect(self.stop_right_indicator)
        self.right_indicator.clicked.connect(self.start_right_blink)

        # Hazard
        self.warning_label = QPushButton(self.central)
        self.warning_label.setGeometry(950, 20, 60, 60)
        self.warning_label.setStyleSheet("background: transparent; border: none;")
        self.warning_label.setIcon(QIcon("image/hazard off.png"))
        self.warning_label.setIconSize(self.warning_label.size())
        self.warning_blink = False
        self.warning_timer = QTimer(self)
        self.warning_timer.timeout.connect(self.toggle_warning)
        self.warning_label.clicked.connect(self.start_warning_blink)

        # Left Bulbs
        self.left_bulb1 = QPushButton(self.central)
        self.left_bulb1.setGeometry(20, 240, 100, 100)
        self.left_bulb1.setStyleSheet("background: transparent; border: none;")
        self.left_bulb1.setIcon(QIcon("image/high beam off.png"))
        self.left_bulb1.setIconSize(self.left_bulb1.size())
        self.left_bulb1.setCheckable(True)
        self.left_bulb1.clicked.connect(self.toggle_left_bulb1)

        self.left_bulb2 = QPushButton(self.central)
        self.left_bulb2.setGeometry(20, 360, 100, 100)
        self.left_bulb2.setStyleSheet("background: transparent; border: none;")
        self.left_bulb2.setIcon(QIcon("image/low beam off.png"))
        self.left_bulb2.setIconSize(self.left_bulb2.size())
        self.left_bulb2.setCheckable(True)
        self.left_bulb2.clicked.connect(self.toggle_left_bulb2)

    
        # Right Bulbs
        self.right_bulb1 = QPushButton(self.central)
        self.right_bulb1.setGeometry(1800, 240, 100, 100)
        self.right_bulb1.setStyleSheet("background: transparent; border: none;")
        self.right_bulb1.setIcon(QIcon("image/charging off.png"))
        self.right_bulb1.setIconSize(self.right_bulb1.size())
        self.right_bulb1.setCheckable(True)
        self.right_bulb1.clicked.connect(self.toggle_right_bulb1)

        # Control Panel Button
        self.control_panel_btn = QPushButton(self.central)
        self.control_panel_btn.setGeometry(1800, 360, 100, 100)
        self.control_panel_btn.setStyleSheet("background: transparent; border: none;")
        self.control_panel_btn.setIcon(QIcon("image/control panel menu.png"))
        self.control_panel_btn.setIconSize(self.control_panel_btn.size())
        self.control_panel_btn.clicked.connect(self.open_control_panel)

        # Navigation Button
        self.navigation_btn = QPushButton(self.central)
        self.navigation_btn.setGeometry(1800, 480, 100, 100)
        self.navigation_btn.setStyleSheet("background: transparent; border: none;")
        self.navigation_btn.setIcon(QIcon("image/navigation menu.png"))
        self.navigation_btn.setIconSize(self.navigation_btn.size())
        self.navigation_btn.clicked.connect(self.open_navigation)

        # Bottom Labels
        self.bottom_left = QLabel("Left", self.central)
        self.bottom_left.setGeometry(100, 900, 200, 40)
        self.bottom_left.setAlignment(Qt.AlignCenter)
        self.bottom_left.setFont(QFont("Arial", 18))
        self.bottom_left.setStyleSheet("color: black; background: transparent;")

        self.bottom_center = QLabel("Center", self.central)
        self.bottom_center.setGeometry(900, 900, 200, 40)
        self.bottom_center.setAlignment(Qt.AlignCenter)
        self.bottom_center.setFont(QFont("Arial", 18))
        self.bottom_center.setStyleSheet("color: black; background: transparent;")

        self.bottom_right = QLabel("Right", self.central)
        self.bottom_right.setGeometry(1600, 900, 200, 40)
        self.bottom_right.setAlignment(Qt.AlignCenter)
        self.bottom_right.setFont(QFont("Arial", 18))
        self.bottom_right.setStyleSheet("color: black; background: transparent;")

    # ---- Functions ----
    def update_clock(self):
        now = QDateTime.currentDateTime()
        self.clock_label.setText(now.toString("hh:mm"))
        self.date_label.setText(now.toString("dd MMMM, dddd"))

    def show_black_screen(self):
        self.bg_label.setStyleSheet("background-color: black;")
        self.bg_label.setPixmap(QPixmap())
        for child in self.central.findChildren((QLabel, QPushButton)):
            if child is not self.bg_label:
                child.hide()

    def toggle_left_indicator(self):
        self.left_indicator.setIcon(QIcon("image/left indicator on.png" if self.left_blink else "image/left indicator off.png"))
        self.left_blink = not self.left_blink

    def start_left_blink(self):
        # Stop right indicator if active
        if self.right_timer.isActive():
            self.stop_right_indicator()
        
        # Start left indicator
        if not self.left_timer.isActive():
            self.left_timer.start(500)
            self.left_stop_timer.start(10000)  # 10 seconds
            self.left_blink = True
            self.left_indicator.setIcon(QIcon("image/left indicator on.png"))

    def stop_left_indicator(self):
        self.left_timer.stop()
        self.left_stop_timer.stop()
        self.left_indicator.setIcon(QIcon("image/left indicator off.png"))
        self.left_blink = False

    def toggle_right_indicator(self):
        self.right_indicator.setIcon(QIcon("image/right indicator on.png" if self.right_blink else "image/right indicator off.png"))
        self.right_blink = not self.right_blink

    def start_right_blink(self):
        # Stop left indicator if active
        if self.left_timer.isActive():
            self.stop_left_indicator()
        
        # Start right indicator
        if not self.right_timer.isActive():
            self.right_timer.start(500)
            self.right_stop_timer.start(10000)  # 10 seconds
            self.right_blink = True
            self.right_indicator.setIcon(QIcon("image/right indicator on.png"))

    def stop_right_indicator(self):
        self.right_timer.stop()
        self.right_stop_timer.stop()
        self.right_indicator.setIcon(QIcon("image/right indicator off.png"))
        self.right_blink = False

    def toggle_warning(self):
        self.warning_label.setIcon(QIcon("image/hazard on.png" if self.warning_blink else "image/hazard off.png"))
        self.warning_blink = not self.warning_blink

        # Also blink left and right indicators when hazard is active
        if self.warning_blink:
            self.left_indicator.setIcon(QIcon("image/left indicator on.png"))
            self.right_indicator.setIcon(QIcon("image/right indicator on.png"))
        else:
            self.left_indicator.setIcon(QIcon("image/left indicator off.png"))
            self.right_indicator.setIcon(QIcon("image/right indicator off.png"))

    def start_warning_blink(self):
        if self.warning_timer.isActive():
            # Stop hazard
            self.warning_timer.stop()
            self.warning_label.setIcon(QIcon("image/hazard off.png"))

            # Stop both indicators
            self.left_timer.stop()
            self.right_timer.stop()
            self.left_stop_timer.stop()
            self.right_stop_timer.stop()
            self.left_indicator.setIcon(QIcon("image/left indicator off.png"))
            self.right_indicator.setIcon(QIcon("image/right indicator off.png"))
        else:
            # Start hazard
            self.warning_timer.start(500)

            # Also start both indicators blinking
            self.left_timer.start(500)
            self.right_timer.start(500)

    def toggle_left_bulb1(self):
        self.left_bulb1.setIcon(QIcon("image/high beam on.png" if self.left_bulb1.isChecked() else "image/high beam off.png"))

    def toggle_left_bulb2(self):
        self.left_bulb2.setIcon(QIcon("image/low beam on.png" if self.left_bulb2.isChecked() else "image/low beam off.png"))

    def toggle_right_bulb1(self):
        self.right_bulb1.setIcon(QIcon("image/charging on.png" if self.right_bulb1.isChecked() else "image/charging off.png"))

    def open_control_panel(self):
        """Open the control panel application"""
        try:
            if os.path.exists(self.control_panel_path):
                # Close current application
                self.close()
                # Open control panel application
                subprocess.Popen([sys.executable, self.control_panel_path])
            else:
                print(f"Control panel file not found: {self.control_panel_path}")
                # You can show a message to the user here
        except Exception as e:
            print(f"Error opening control panel: {e}")

    def open_navigation(self):
        """Open the navigation application"""
        try:
            if os.path.exists(self.navigation_path):
                # Close current application
                self.close()
                # Open navigation application
                subprocess.Popen([sys.executable, self.navigation_path])
            else:
                print(f"Navigation file not found: {self.navigation_path}")
                # You can show a message to the user here
        except Exception as e:
            print(f"Error opening navigation: {e}")

    def set_bottom_left_text(self, text):
        self.bottom_left.setText(text)

    def set_bottom_center_text(self, text):
        self.bottom_center.setText(text)

    def set_bottom_right_text(self, text):
        self.bottom_right.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InfotainmentUI()
    window.show()

    # Example dynamic text
    window.set_bottom_left_text("20 km")
    window.set_bottom_center_text("Battery: 75%")
    window.set_bottom_right_text("Range: 30 km")

    sys.exit(app.exec_())
