# Media Downloader

Media Downloader is a simple yet powerful GUI application built using **PyQt** and **yt-dlp** that allows users to download videos and audio from multiple platforms like **YouTube, Facebook, Twitter, Instagram, and more**.

![MediaDownloader](https://github.com/devsubrata/Media-Downloader/blob/main/Media%20Downloader.jpg)

## 🚀 Features
- Download videos in **MP4** format
- Extract and download **MP3** audio from videos
- Supports **YouTube, Facebook, Twitter, Instagram, and more**
- Live progress updates
- Automatic file saving to **Desktop**
- User-friendly **PyQt GUI**

## 📦 Installation
### Prerequisites
Make sure you have the following installed on your system:
- **Python 3.7+**
- **pip** (Python package manager)
- **ffmpeg** (Required for video and audio conversion)

### Install Dependencies
```sh
pip install -r requirements.txt
```

## ▶️ Usage
Run the application by executing:
```sh
python media_downloader.py
```

### 🎯 How to Use
1. Paste the **video URL** into the input field.
2. Select either **Video (.mp4)** or **Audio (.mp3)** format.
3. Click **Download** and wait for the process to complete.
4. The file will be saved to your **Desktop** by default.

## ⚙️ Configuration
To change the download directory, modify the `outtmpl` option in the `options` dictionary inside `media_downloader.py`:
```python
import os
custom_path = "C:/Users/YourUsername/Downloads"
options = {
    'outtmpl': os.path.join(custom_path, '%(title)s.%(ext)s'),
}
```

## 🔗 Dependencies
- [PyQt](https://pypi.org/project/PyQt5/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Fork of youtube-dl)
- [ffmpeg](https://ffmpeg.org/download.html)

## 📝 Credits
This project uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video and audio downloading. Special thanks to the developers of yt-dlp!

## 📜 License
This project is licensed under the **MIT License**.
