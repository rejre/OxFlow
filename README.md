# OxFlow — Universal Downloader

A clean, dark-themed media & file downloader built with Python + CustomTkinter.

## Project Structure

```
ChameleonDownloader/
├── src/
│   ├── ui/
│   │   └── main_window.py      # Application entry point & full UI
│   ├── core/
│   │   └── downloader.py       # DownloadEngine (yt-dlp + requests)
│   └── utils/
│       ├── config.py            # ConfigManager (atomic JSON persistence)
│       └── i18n.py              # I18nManager (en / zh_CN / ja)
├── icon.png
└── requirements.txt
```

## Quick Start

```bash
pip install -r requirements.txt
python src/ui/main_window.py
```

FFmpeg is required for audio extraction (MP3) and video merging.  
Install via Homebrew on macOS: `brew install ffmpeg`

## Features

- YouTube, Bilibili, TikTok, Vimeo and 1000+ sites via yt-dlp  
- Direct file download (ZIP, EXE, DMG, ...) via streaming requests  
- Resolution picker: 2160p → 360p + MP3 audio-only  
- Live progress bar with speed & ETA  
- Auto thumbnail loading & History tracking
- Multi-language UI: English / 简体中文 / 日本語  
- Atomic config file writes & Low-power mode support
