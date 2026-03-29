"""
OxFlow - Download Engine (Merged & Optimized)
Universal media & direct-file downloading with triple-insurance discovery.
"""

import os
import shutil
import threading
import time
import logging
import requests
import yt_dlp
import re
from typing import Callable, Optional
from urllib.parse import urlparse, parse_qs, unquote

logger = logging.getLogger(__name__)

RESOLUTION_FORMAT_MAP = {
    "2160p": "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best[height<=2160]",
    "1440p": "bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best[height<=1440]",
    "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720p":  "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480p":  "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]",
    "360p":  "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]",
}

VIDEO_PLATFORMS = {
    "youtube.com", "youtu.be", "vimeo.com", "bilibili.com", "b23.tv",
    "tiktok.com", "facebook.com", "instagram.com", "twitter.com", "x.com",
}

BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

class DownloadEngine:
    def __init__(self, progress_callback=None, log_callback=None, ffmpeg_path=None, max_retries=10, concurrent_fragments=4):
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.max_retries = max_retries
        self.concurrent_fragments = concurrent_fragments
        self._is_cancelled = False
        self._lock = threading.Lock()
        self.ffmpeg_path = ffmpeg_path if ffmpeg_path else self._find_ffmpeg()

    def _find_ffmpeg(self):
        found = shutil.which("ffmpeg")
        if found: return os.path.dirname(found)
        for p in ("/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg", "/usr/bin/ffmpeg"):
            if os.path.exists(p): return os.path.dirname(p)
        return None

    def has_ffmpeg(self): return bool(self.ffmpeg_path)

    def get_info(self, url: str) -> dict:
        """Triple-insurance info discovery for direct files vs yt-dlp platforms."""
        try:
            headers = {'User-Agent': BROWSER_UA, 'Accept': '*/*'}
            filename = None
            
            # 1. Check URL parameters (Signed URLs / GitHub Assets)
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            for p in ['filename', 'response-content-disposition', 'rscd']:
                if p in params:
                    val = params[p][0]
                    filename = val.split('filename=')[-1].strip(' "') if 'filename=' in val else val
                    break
            
            # 2. Probe via GET stream (Asset detection)
            is_video_platform = any(domain in url.lower() for domain in VIDEO_PLATFORMS)
            if not is_video_platform:
                resp = requests.get(url, allow_redirects=True, timeout=10, headers=headers, stream=True)
                content_type = resp.headers.get('Content-Type', '').lower()
                content_length = int(resp.headers.get('Content-Length', 0) or 0)
                cd = resp.headers.get('Content-Disposition', '')
                
                if not filename and cd:
                    match = re.findall(r"filename\*?=['\"]?(?:UTF-8'')?([^'\"\n;]+)['\"]?", cd)
                    if match: filename = unquote(match[0])
                
                if not filename:
                    base = os.path.basename(parsed_url.path)
                    if '.' in base: filename = base

                # If it's a known asset host or definitely not HTML
                is_asset = any(d in url for d in ['githubusercontent.com', 'amazonaws.com', 'storage.googleapis.com'])
                if is_asset or (filename or 'text/html' not in content_type):
                    resp.close()
                    return {
                        'title': filename or "downloaded_file",
                        'is_direct': True,
                        'filesize': content_length,
                        'ext': (filename.split('.')[-1] if '.' in filename else '') if filename else '',
                        'url': url
                    }
                resp.close()
        except Exception as e:
            self._log(f"[DEBUG] Probe failed: {e}")

        # 3. Fallback to yt-dlp
        return self._extract_ydl_info(url)

    def _extract_ydl_info(self, url):
        opts = {
            'quiet': True, 'no_warnings': True, 'nocheckcertificate': True, 'noplaylist': True,
            'headers': {'User-Agent': BROWSER_UA}
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            info['is_direct'] = False
            return info

    def download(self, url, options):
        with self._lock: self._is_cancelled = False
        if options.get('is_direct'):
            threading.Thread(target=self._download_direct, args=(url, options), daemon=True).start()
        else:
            threading.Thread(target=self._download_media, args=(url, options), daemon=True).start()

    def _download_media(self, url, options):
        res = options.get('resolution', '1080p')
        out_tmpl = options.get('outtmpl', '%(title)s.%(ext)s')
        ydl_opts = {
            'format': RESOLUTION_FORMAT_MAP.get(res, RESOLUTION_FORMAT_MAP["1080p"]),
            'outtmpl': out_tmpl,
            'progress_hooks': [self._ydl_hook],
            'nocheckcertificate': True,
            'continuedl': True,
            'concurrent_fragment_downloads': options.get('concurrent_fragments', self.concurrent_fragments),
            'ffmpeg_location': self.ffmpeg_path,
            'headers': {'User-Agent': BROWSER_UA},
            'quiet': True,
        }
        if options.get('audio_only'):
            ydl_opts['format'] = 'bestaudio/best'
            if self.has_ffmpeg():
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}]
        try:
            self._log(f"[START] Media download → {res}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
            if not self._is_cancelled: self._log("[SUCCESS] Download finished.")
        except Exception as e:
            self._log(f"[ERROR] {e}" if not self._is_cancelled else "[CANCELLED] Task cancelled.")

    def _download_direct(self, url, options):
        title = options.get('title', 'file')
        raw_tmpl = options.get('outtmpl', '%(title)s.%(ext)s')
        d_dir = os.path.dirname(raw_tmpl) or "."
        if "%" in d_dir: d_dir = os.path.expanduser("~/Downloads")
        os.makedirs(d_dir, exist_ok=True)
        dest = os.path.join(d_dir, title)
        
        try:
            self._log(f"[START] Direct download: {title}")
            with requests.get(url, stream=True, timeout=60, headers={'User-Agent': BROWSER_UA}, allow_redirects=True) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0) or 0)
                downloaded = 0
                start = time.monotonic()
                with open(dest, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=65536):
                        if self._is_cancelled:
                            self._log("[CANCELLED] Task cancelled.")
                            return
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if self.progress_callback and total > 0:
                                elapsed = max(time.monotonic() - start, 1e-6)
                                speed = downloaded / elapsed
                                self.progress_callback({
                                    'status': 'downloading',
                                    '_percent_str': f"{(downloaded/total*100):.1f}%",
                                    '_speed_str': self.format_size(speed) + "/s",
                                    '_eta_str': self.format_eta((total - downloaded) / speed) if speed > 0 else "--:--",
                                    'downloaded_bytes': downloaded, 'total_bytes': total
                                })
            self._log("[SUCCESS] Download finished.")
        except Exception as e:
            self._log(f"[ERROR] {e}")

    def _ydl_hook(self, d):
        if self._is_cancelled: raise Exception("Cancelled")
        if d['status'] == 'downloading' and self.progress_callback:
            self.progress_callback({
                'status': 'downloading',
                '_percent_str': d.get('_percent_str', '0%'),
                '_speed_str': d.get('_speed_str', 'N/A'),
                '_eta_str': d.get('_eta_str', '--:--'),
                'downloaded_bytes': d.get('downloaded_bytes', 0),
                'total_bytes': d.get('total_bytes', 0)
            })

    def _log(self, msg):
        if self.log_callback: self.log_callback(msg)

    def cancel(self):
        with self._lock: self._is_cancelled = True

    @staticmethod
    def format_size(s):
        for u in ['B','KB','MB','GB','TB']:
            if s < 1024: return f"{s:.1f} {u}"
            s /= 1024
        return f"{s:.1f} PB"

    @staticmethod
    def format_eta(s):
        if s is None or s < 0: return "--:--"
        m, s = divmod(int(s), 60); h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
