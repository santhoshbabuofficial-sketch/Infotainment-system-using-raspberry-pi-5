import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QSlider, QFrame, 
                            QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QSize, QUrl, QRectF
from PyQt5.QtGui import QPainter, QPen, QFont, QColor, QLinearGradient, QBrush, QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class BatteryRing(QWidget):
    def __init__(self, parent=None, percentage=75):
        super().__init__(parent)
        self.percentage = percentage
        self.setFixedSize(150, 150)  # Smaller size for top left corner

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Gradient background for battery ring
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(200, 240, 255))  # Light blue
        gradient.setColorAt(1, QColor(200, 255, 220))  # Light green
        painter.fillRect(self.rect(), QBrush(gradient))

        # Circle bounds
        margin = 20
        rect = QRectF(margin, margin, self.width() - 2 * margin, self.height() - 2 * margin)

        # Background ring
        pen_bg = QPen(QColor(220, 220, 220), 12)  # Thinner ring
        painter.setPen(pen_bg)
        painter.drawArc(rect, 0, 360 * 16)

        # Determine color based on battery percentage
        if self.percentage > 70:
            battery_color = QColor(0, 200, 0)  # Green
        elif self.percentage > 30:
            battery_color = QColor(255, 165, 0)  # Orange
        else:
            battery_color = QColor(255, 0, 0)  # Red

        # Foreground ring (progress)
        pen_fg = QPen(battery_color, 12)  # Thinner ring
        painter.setPen(pen_fg)
        span_angle = int(360 * 16 * self.percentage / 100)
        painter.drawArc(rect, 90 * 16, -span_angle)

        # Centered percentage text
        painter.setPen(Qt.darkBlue)
        painter.setFont(QFont("Arial", 16, QFont.Bold))  # Smaller font
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.percentage}%")

    def update_battery(self, percentage):
        """Update battery percentage and repaint"""
        self.percentage = max(0, min(100, percentage))  # Clamp between 0-100
        self.update()

class ControlCenter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Center")
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f0f8ff, stop:1 #e6f3ff);")   
        
        # Dictionary to track button states
        self.button_states = {}
        
        self.init_ui()
        self.showFullScreen()  # Full screen

    # --- BUTTON CREATION ---
    def create_button(self, icon_path, radius=20, button_name=""):
        btn = QPushButton(self)
        if icon_path:  # Only set icon if path is provided
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(40, 40))
        
        # Initial style - Aquamarine theme
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #CFF9E8, stop:1 #CFF9E8);
                border-radius: {radius}px;
                border: 2px solid #48d1cc;
                color: #CFF9E8;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #CFF9E8, stop:1 #CFF9E8);
                border: 2px solid #CFF9E8;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #CFF9E8, stop:1 #CFF9E8);
            }}
        """)
        
        # Store initial state
        self.button_states[button_name] = False
        
        # Connect click event
        btn.clicked.connect(lambda: self.toggle_button(button_name, btn))
        
        return btn

    def toggle_button(self, button_name, button):
        """Toggle button state"""
        # Toggle state
        self.button_states[button_name] = not self.button_states[button_name]
        
        # Update button appearance
        if self.button_states[button_name]:
            # Active state (ON) - White with aquamarine border
            button.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ffffff, stop:1 #f8f8ff);
                    border-radius: {button.geometry().width()//2}px;
                    border: 3px solid #CFF9E8;
                    color: #CFF9E8;
                    font-weight: bold;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    border: 3px solid #CFF9E8;
                }}
            """)
        else:
            # Inactive state (OFF) - Aquamarine
            button.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #CFF9E8, stop:1 #CFF9E8);
                    border-radius: {button.geometry().width()//2}px;
                    border: 2px solid #CFF9E8;
                    color: #CFF9E8;
                    font-weight: bold;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #CFF9E8, stop:1 #CFF9E8);
                    border: 2px solid #CFF9E8;
                }}
            """)

    # --- SLIDER CREATION ---
    def create_slider(self, label_text, icon_path=None, frame_radius=30, handle_radius=30,
                      slider_width=100, slider_height=500, groove_width=40):
        frame = QFrame(self)
        frame.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #ffffff, stop:1 #CFF9E8);
            border-radius: {frame_radius}px;
            border: 2px solid #7fffd4;
        """)
        frame.setFixedSize(slider_width, slider_height)

        # Label
        label = QLabel(frame)
        label.setFont(QFont("Arial", 10, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        if icon_path:
            pix = QPixmap(icon_path)
            label.setPixmap(pix.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            label.setText(label_text)
            label.setStyleSheet("color: #2f4f4f; background: transparent;")

        # Slider
        slider = QSlider(Qt.Vertical, frame)
        slider.setRange(0, 100)
        slider.setValue(50)

        # Center slider inside frame
        slider.setGeometry((slider_width - groove_width) // 2, 30, groove_width, slider_height - 30)

        slider.setStyleSheet(f"""
            QSlider::groove:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e0ffff, stop:1 #b0e0e6);
                width: {groove_width}px; 
                border-radius: {groove_width//2}px;
                border: 1px solid #48d1cc;
            }}
            QSlider::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7fffd4, stop:1 #40e0d0);
                border: 2px solid #20b2aa;
                height: 40px; 
                margin: -10px 0; 
                border-radius: {handle_radius}px;
            }}
            QSlider::sub-page:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7fffd4, stop:1 #40e0d0);
                border-radius: {groove_width//2}px;
            }}
        """)

        # Position label on top
        label.setGeometry((slider_width - 30) // 2, 5, 30, 30)

        return frame

    # --- MUSIC PLAYER INTEGRATION ---
    def create_music_player(self):
        # 👇 Fixed music folder path (change this to your folder)
        self.music_folder = r"D:\infotainment system\songs"  # Update this path

        self.playlist = []
        self.current_index = 0
        self.player = QMediaPlayer()

        # Create music player widget
        music_widget = QWidget(self.music_frame)
        music_widget.setGeometry(10, 50, 610, 240)
        music_widget.setStyleSheet("background: transparent;")

        # Title
        title = QLabel("🎵 Music Player", music_widget)
        title.setGeometry(0, 0, 610, 30)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #2f4f4f; background: transparent;")

        # Song label
        self.song_label = QLabel("No song loaded", music_widget)
        self.song_label.setGeometry(0, 30, 610, 30)
        self.song_label.setAlignment(Qt.AlignCenter)
        self.song_label.setFont(QFont("Arial", 10))
        self.song_label.setStyleSheet("color: #2f4f4f; background: transparent;")

        # --- Center Circular Play Button ---
        self.play_btn = QPushButton("▶", music_widget)
        self.play_btn.setFont(QFont("Arial", 20, QFont.Bold))
        self.play_btn.setGeometry(245, 80, 120, 120)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7fffd4, stop:1 #40e0d0);
                color: #2f4f4f;
                border-radius: 60px;
                border: 3px solid #48d1cc;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #98fb98, stop:1 #7fffd4);
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor("#48d1cc"))
        shadow.setOffset(0, 0)
        self.play_btn.setGraphicsEffect(shadow)
        self.play_btn.clicked.connect(self.play_pause)

        # --- Left / Right Buttons ---
        self.left_btn = QPushButton("◀", music_widget)
        self.right_btn = QPushButton("▶", music_widget)

        # Left button
        self.left_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.left_btn.setGeometry(155, 100, 60, 60)
        self.left_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7fffd4, stop:1 #40e0d0);
                color: #2f4f4f;
                border-radius: 30px;
                border: 2px solid #48d1cc;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #98fb98, stop:1 #7fffd4);
            }
        """)
        self.left_btn.clicked.connect(self.prev_song)

        # Right button (next)
        self.right_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.right_btn.setGeometry(395, 100, 60, 60)
        self.right_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7fffd4, stop:1 #40e0d0);
                color: #2f4f4f;
                border-radius: 30px;
                border: 2px solid #48d1cc;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #98fb98, stop:1 #7fffd4);
            }
        """)
        self.right_btn.clicked.connect(self.next_song)

        # Load songs
        self.load_songs()

    def load_songs(self):
        if os.path.exists(self.music_folder):
            self.playlist = [
                os.path.join(self.music_folder, f)
                for f in os.listdir(self.music_folder)
                if f.lower().endswith(('.mp3', '.wav', '.ogg'))
            ]
            if self.playlist:
                self.current_index = 0
                self.load_song(self.playlist[self.current_index])
            else:
                self.song_label.setText("No audio files in folder.")
        else:
            self.song_label.setText("Music folder not found.")

    def load_song(self, path):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.song_label.setText(os.path.basename(path))
        self.player.play()
        self.play_btn.setText("⏸")

    def play_pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_btn.setText("▶")
        else:
            if not self.playlist:
                return
            if self.player.media().isNull():
                self.load_song(self.playlist[self.current_index])
            else:
                self.player.play()
                self.play_btn.setText("⏸")

    def next_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.load_song(self.playlist[self.current_index])

    def prev_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.load_song(self.playlist[self.current_index])

    # --- INIT UI ---
    def init_ui(self):
        # === Battery Indicator in Top Left ===
        self.battery_widget = BatteryRing(self, percentage=85)
        self.battery_widget.setGeometry(50, 20, 150, 150)
        
        # Battery label
        battery_label = QLabel("Battery", self)
        battery_label.setGeometry(50, 170, 150, 30)
        battery_label.setAlignment(Qt.AlignCenter)
        battery_label.setFont(QFont("Arial", 12, QFont.Bold))
        battery_label.setStyleSheet("color: #2f4f4f; background: transparent;")

        # === Top Row Buttons ===
        self.bluetooth_btn = self.create_button("", radius=50, button_name="bluetooth")
        self.bluetooth_btn.setGeometry(1160, 20, 300, 150)
        self.bluetooth_btn.setText("Bluetooth")

        self.wifi_btn = self.create_button("", radius=50, button_name="wifi")
        self.wifi_btn.setGeometry(1530, 20, 300, 150)
        self.wifi_btn.setText("WiFi")

        # === Music Player Block ===
        self.music_frame = QFrame(self)
        self.music_frame.setGeometry(450, 20, 630, 300)
        self.music_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #ffffff, stop:1 #f0f8ff);
            border-radius: 20px;
            border: 2px solid #7fffd4;
        """)
        
        self.music_label = QLabel("Music Player", self.music_frame)
        self.music_label.setGeometry(10, 10, 140, 30)
        self.music_label.setAlignment(Qt.AlignCenter)
        self.music_label.setStyleSheet("""
            color: #2f4f4f; 
            font-size: 14pt; 
            font-weight: bold;
            background: transparent;
        """)

        # Create the music player inside the music frame
        self.create_music_player()

        # === Middle Row Buttons ===
        self.lock_btn = self.create_button("", radius=50, button_name="lock")  
        self.lock_btn.setGeometry(50, 360, 300, 150)
        self.lock_btn.setText("Lock")

        self.moon_btn = self.create_button("", radius=50, button_name="moon")  
        self.moon_btn.setGeometry(420, 360, 300, 150)
        self.moon_btn.setText("Dark Mode")

        self.screen_btn = self.create_button("", radius=50, button_name="screen")  
        self.screen_btn.setGeometry(790, 360, 300, 150)
        self.screen_btn.setText("Screen\nRotation")

        # === Sliders ===
        self.brightness_slider = self.create_slider("", 
                                                    frame_radius=40, handle_radius=25,
                                                    slider_width=85, slider_height=350,
                                                    groove_width=85)
        self.brightness_slider.setGeometry(1715, 200, 100, 500)

        self.volume_slider = self.create_slider("", 
                                                frame_radius=40, handle_radius=25,
                                                slider_width=85, slider_height=350,
                                                groove_width=85)
        self.volume_slider.setGeometry(1530, 200, 100, 500)

        # === Bottom Row Buttons ===
        self.flashlight_btn = self.create_button("", radius=50, button_name="flashlight")
        self.flashlight_btn.setGeometry(50, 720, 300, 150)
        self.flashlight_btn.setText("Flashlight")

        self.timer_btn = self.create_button("", radius=50, button_name="timer")
        self.timer_btn.setGeometry(420, 720, 300, 150)
        self.timer_btn.setText("Timer")

        self.calculator_btn = self.create_button("", radius=50, button_name="calculator")
        self.calculator_btn.setGeometry(790, 720, 300, 150)
        self.calculator_btn.setText("Calculator")

    def keyPressEvent(self, event):
        # Press Escape to exit full screen
        if event.key() == Qt.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

# --- MAIN ---
def main():
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont("Arial", 10)
    app.setFont(font)
    
    win = ControlCenter()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
