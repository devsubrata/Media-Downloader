import sys
import os
import yt_dlp
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QTextEdit, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QCursor

class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)  # Sends progress updates
    complete_signal = pyqtSignal(str)  # Sends completion message

    def __init__(self, url, format_choice, output_dir):
        super().__init__()
        self.url = url
        self.format_choice = format_choice
        self.output_dir = output_dir

    def run(self):
        """ Runs the download process in a separate thread """
        try:
            options = {
                'format': '270+bestaudio/best[ext=mp4]',
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [self.update_progress],
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }] if "Video" in self.format_choice else [{
                    'key': 'FFmpegExtractAudio',
                    'preferedcodec': 'mp3',
                    'preferedquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([self.url])

            self.complete_signal.emit(f"✅ Saved in {self.output_dir}\n✅ Download Complete!")

        except Exception as e:
            self.complete_signal.emit(f"❌ Error: {str(e)}")

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
        self.setGeometry(300, 200, 500, 450)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'logo.png')))

        self.output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        layout = QVBoxLayout()

        self.title_label = QLabel("Media Downloader (audio/video)", self)
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Paste media URL here...")
        layout.addWidget(self.url_input)

        self.format_combo = QComboBox(self)
        self.format_combo.addItems(["Video (.mp4)", "Audio (.mp3)"])
        layout.addWidget(self.format_combo)

        self.download_btn = QPushButton("Download", self)
        self.download_btn.clicked.connect(self.download_video)
        self.url_input.returnPressed.connect(self.download_btn.click)
        layout.addWidget(self.download_btn)

        row = QHBoxLayout()
        set_out_dir = QPushButton("SetOutDir", self)
        clear = QPushButton("Clear", self)
        open_out_dir = QPushButton("OpenOutDir", self)

        for btn in [self.download_btn, set_out_dir, clear, open_out_dir]:
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            if btn != self.download_btn:
                btn.setObjectName("btn_group")

        set_out_dir.clicked.connect(self.set_output_directory)
        clear.clicked.connect(self.clear)
        open_out_dir.clicked.connect(self.open_output_directory)

        row.addWidget(clear)
        row.addWidget(set_out_dir)
        row.addWidget(open_out_dir)
        layout.addLayout(row)

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

        self.thread = DownloadThread(url, format_choice, self.output_dir)
        self.thread.progress_signal.connect(self.output_log.append)
        self.thread.complete_signal.connect(self.output_log.append)
        self.thread.start()

    def clear(self):
        self.url_input.clear()
        self.output_log.clear()

    def set_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select an output directory", self.output_dir)
        if dir_path:
            self.output_dir = dir_path

    def open_output_directory(self):
        os.startfile(self.output_dir)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    def load_stylesheet(file_path):
        with open(file_path, "r") as file:
            return file.read()

    stylesheet_path = os.path.join(os.path.dirname(__file__), 'styles.qss')
    if os.path.exists(stylesheet_path):
        app.setStyleSheet(load_stylesheet(stylesheet_path))

    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())
