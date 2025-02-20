import sys
import os
import yt_dlp
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon

class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)  # Sends progress updates
    complete_signal = pyqtSignal(str)  # Sends completion message

    def __init__(self, url, format_choice):
        super().__init__()
        self.url = url
        self.format_choice = format_choice

    def run(self):
        """ Runs the download process in a separate thread """
        ouput_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        options = {
            'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]' if "Video" in self.format_choice else 'bestaudio',            'outtmpl': '%(title)s.%(ext)s',
            'outtmpl': os.path.join(ouput_dir, '%(title)s.%(ext)s'),
            # Attach progress function
            'progress_hooks': [self.update_progress],
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }] if "Video" in self.format_choice else [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([self.url])

        self.complete_signal.emit("✅ Download Complete! Saved in desktop!")

    def update_progress(self, d):
        """ Emits progress updates in real-time """
        if d['status'] == 'downloading':
            progress_msg = f"📶 {d['_percent_str']} completed! - {d['_eta_str']} remaining"
            self.progress_signal.emit(progress_msg)


class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Media Downloader by Subrata K. Dev")
        self.setGeometry(300, 200, 500, 400)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'logo.png')))

        layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel("Media Downloader (audio/video)", self)
        self.title_label.setObjectName("titleLabel")
        layout.addWidget(
            self.title_label,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Input Field
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Paste media URL here...")
        layout.addWidget(self.url_input)

        # Format Selection
        self.format_combo = QComboBox(self)
        self.format_combo.addItems(["Video (.mp4)", "Audio (.mp3)"])
        layout.addWidget(self.format_combo)

        # Download Button
        self.download_btn = QPushButton("Download", self)
        self.download_btn.clicked.connect(self.download_video)
        layout.addWidget(self.download_btn)

        # Log Output
        self.output_log = QTextEdit(self)
        self.output_log.setReadOnly(True)
        layout.addWidget(self.output_log)

        self.setLayout(layout)

    def download_video(self):
        url = self.url_input.text().strip()
        if not url:
            self.output_log.append("❌ Please enter a valid YouTube URL!")
            return

        format_choice = self.format_combo.currentText()
        self.output_log.append(f"🔽 Downloading: {url} ({format_choice})...")

        # Start the download in a separate thread
        self.thread = DownloadThread(url, format_choice)
        self.thread.progress_signal.connect(self.output_log.append)  # Update log in real-time
        self.thread.complete_signal.connect(self.output_log.append)  # Show completion message
        self.thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    def load_stylesheet(file_path):
        with open(file_path, "r") as file:
            return file.read()

    stylesheet = load_stylesheet(os.path.join(
        os.path.dirname(__file__), 'styles.qss'))
    app.setStyleSheet(stylesheet)

    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())
