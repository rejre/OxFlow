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
    def __init__(self, progress_callback=None, log_callback=None, ffmpeg_path=None, max_retries=10, concurrent_fragments=4, proxy=None, cookies_browser=None):
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.max_retries = max_retries
        self.concurrent_fragments = concurrent_fragments
        self.proxy = proxy
        self.cookies_browser = cookies_browser
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

    def _get_proxies(self):
        return {"http": self.proxy, "https": self.proxy} if self.proxy else None

    def get_info(self, url: str) -> dict:
        """Triple-insurance info discovery for direct files vs yt-dlp platforms."""
        try:
            headers = {'User-Agent': BROWSER_UA, 'Accept': '*/*'}
            filename = None
            
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            if 'filename' in params: filename = unquote(params['filename'][0])

            if any(platform in parsed_url.netloc for platform in VIDEO_PLATFORMS):
                pass 
            else:
                resp = requests.head(url, headers=headers, allow_redirects=True, timeout=10, proxies=self._get_proxies())
                content_type = resp.headers.get('content-type', '').lower()
                content_length = int(resp.headers.get('content-length', 0))
                
                cd = resp.headers.get('content-disposition', '')
                if 'filename=' in cd: filename = unquote(cd.split('filename=')[-1].strip(' "'))
                
                if not filename:
                    base = os.path.basename(parsed_url.path)
                    if '.' in base: filename = base

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

        return self._extract_ydl_info(url)

    def _extract_ydl_info(self, url):
        opts = {
            'quiet': True, 'no_warnings': True, 'nocheckcertificate': True, 'noplaylist': True,
            'headers': {'User-Agent': BROWSER_UA}
        }
        if self.proxy: opts['proxy'] = self.proxy
        
        # 尝试带 Cookie 运行
        if self.cookies_browser and self.cookies_browser.lower() != "none":
            try:
                copts = opts.copy()
                copts['cookiesfrombrowser'] = (self.cookies_browser, None, None, None)
                with yt_dlp.YoutubeDL(copts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    info['is_direct'] = False
                    return info
            except Exception as e:
                if "Operation not permitted" in str(e) or "Permission denied" in str(e):
                    self._log(f"[WARN] Cookie access denied for {self.cookies_browser}, falling back...")
                else:
                    self._log(f"[DEBUG] Info with cookies failed: {e}")

        # 无 Cookie 降级
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            info['is_direct'] = False
            return info

    def download(self, url, options):
        with self._lock: self._is_cancelled = False
        if self.proxy: options['proxy'] = self.proxy
        if self.cookies_browser: options['cookies_browser'] = self.cookies_browser
        if options.get('is_direct'):
            threading.Thread(target=self._download_direct, args=(url, options), daemon=True).start()
        else:
            threading.Thread(target=self._download_media, args=(url, options), daemon=True).start()

    def _download_media(self, url, options):
        res = options.get('resolution', '1080p')
        out_tmpl = options.get('outtmpl', '%(title)s.%(ext)s')
        proxy = options.get('proxy', self.proxy)
        cookies_browser = options.get('cookies_browser', self.cookies_browser)
        
        ydl_opts = {
            'format': RESOLUTION_FORMAT_MAP.get(res, RESOLUTION_FORMAT_MAP["1080p"]),
            'outtmpl': out_tmpl,
            'progress_hooks': [self._ydl_hook],
            'nocheckcertificate': True,
            'continuedl': True,              # ✅ 启用断点续传
            'retries': self.max_retries,     # ✅ 增加重试次数
            'fragment_retries': self.max_retries,  # ✅ 碎片重试
            'skip_unavailable_fragments': True,    # ✅ 跳过不可用的碎片
            'socket_timeout': 60,             # ✅ socket 超时时间
            'http_chunk_size': 1024*1024,    # ✅ 增加 HTTP 块大小到 1MB
            'concurrent_fragment_downloads': min(options.get('concurrent_fragments', self.concurrent_fragments), 4),  # ✅ 限制并发
            'ffmpeg_location': self.ffmpeg_path,
            'headers': {'User-Agent': BROWSER_UA},
            'quiet': True,
            'no_warnings': True,
        }
        if proxy: ydl_opts['proxy'] = proxy
        if options.get('audio_only'):
            ydl_opts['format'] = 'bestaudio/best'
            if self.has_ffmpeg():
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}]

        # 核心修复：下载时的 Cookie 权限检测和重试机制
        success = False
        retry_count = 0
        max_attempts = 3
        
        while retry_count < max_attempts and not self._is_cancelled:
            try:
                if cookies_browser and cookies_browser.lower() != "none":
                    try:
                        copts = ydl_opts.copy()
                        copts['cookiesfrombrowser'] = (cookies_browser, None, None, None)
                        self._log(f"[START] Media download with {cookies_browser} cookies... (attempt {retry_count + 1}/{max_attempts})")
                        with yt_dlp.YoutubeDL(copts) as ydl: ydl.download([url])
                        success = True
                        break
                    except Exception as e:
                        if "Operation not permitted" in str(e) or "Permission denied" in str(e):
                            self._log(f"[WARN] Cookie access denied, retrying without cookies...")
                        else:
                            self._log(f"[WARN] Download with cookies failed: {e}, retrying...")
                            retry_count += 1

                if not success and not self._is_cancelled:
                    self._log(f"[START] Media download (Universal mode)... (attempt {retry_count + 1}/{max_attempts})")
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
                    success = True
                    break
                    
            except Exception as e:
                error_msg = str(e)
                # 判断是网络问题还是其他问题
                if any(x in error_msg for x in ['bytes read', 'connection', 'timeout', 'HTTP 503', 'HTTP 429']):
                    retry_count += 1
                    if retry_count < max_attempts:
                        wait_time = min(2 ** retry_count, 60)  # 指数退避：2s, 4s, 8s... 最多60s
                        self._log(f"[WARN] Network error: {error_msg}. Retrying in {wait_time}s... (attempt {retry_count + 1}/{max_attempts})")
                        time.sleep(wait_time)
                    else:
                        self._log(f"[ERROR] {error_msg}" if not self._is_cancelled else "[CANCELLED] Task cancelled.")
                        break
                else:
                    # 非网络问题，不重试
                    self._log(f"[ERROR] {error_msg}" if not self._is_cancelled else "[CANCELLED] Task cancelled.")
                    break

        if success and not self._is_cancelled:
            self._log("[SUCCESS] Download finished.")
        elif not self._is_cancelled and not success:
            self._log("[ERROR] Download failed after multiple retries.")

    def _download_direct(self, url, options):
        title = options.get('title', 'file')
        raw_tmpl = options.get('outtmpl', '%(title)s.%(ext)s')
        proxy = options.get('proxy', self.proxy)
        
        d_dir = os.path.dirname(raw_tmpl) or "."
        if "%" in d_dir: d_dir = os.path.expanduser("~/Downloads")
        os.makedirs(d_dir, exist_ok=True)
        dest = os.path.join(d_dir, title)
        
        proxies = {"http": proxy, "https": proxy} if proxy else None

        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries and not self._is_cancelled:
            try:
                self._log(f"[START] Direct download: {title} (attempt {retry_count + 1}/{max_retries})")
                
                # 如果文件已部分下载，支持断点续传
                resume_header = {}
                if os.path.exists(dest):
                    downloaded_size = os.path.getsize(dest)
                    resume_header = {'Range': f'bytes={downloaded_size}-'}
                    self._log(f"[INFO] Resuming from {self.format_size(downloaded_size)}")
                
                with requests.get(
                    url, 
                    stream=True, 
                    timeout=60, 
                    headers={**{'User-Agent': BROWSER_UA}, **resume_header},
                    allow_redirects=True, 
                    proxies=proxies
                ) as r:
                    r.raise_for_status()
                    total = int(r.headers.get('content-length', 0) or 0)
                    downloaded = 0
                    start = time.monotonic()
                    
                    # 如果是续传，添加已下载的大小
                    if resume_header and os.path.exists(dest):
                        downloaded = os.path.getsize(dest)
                        total += downloaded
                    
                    open_mode = 'ab' if resume_header and os.path.exists(dest) else 'wb'
                    with open(dest, open_mode) as f:
                        for chunk in r.iter_content(chunk_size=1024*256):  # 增加到 256KB
                            if self._is_cancelled: break
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total > 0:
                                    p = (downloaded / total) * 100
                                    spd = downloaded / (time.monotonic() - start + 0.1)
                                    self._on_progress({'_percent_str': f"{p:.1f}%", '_speed_str': self.format_size(spd)+"/s"})
                
                if not self._is_cancelled:
                    self._log("[SUCCESS] Direct download finished.")
                    break
                    
            except requests.exceptions.ConnectionError as e:
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = min(2 ** retry_count, 60)
                    self._log(f"[WARN] Connection error: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    self._log(f"[ERROR] Connection failed after {max_retries} retries.")
                    
            except requests.exceptions.Timeout as e:
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = min(2 ** retry_count, 60)
                    self._log(f"[WARN] Download timeout. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    self._log(f"[ERROR] Timeout after {max_retries} retries.")
                    
            except Exception as e:
                self._log(f"[ERROR] {e}" if not self._is_cancelled else "[CANCELLED] Direct download cancelled.")

    def _ydl_hook(self, d):
        if self._is_cancelled: raise Exception("User cancelled")
        if d.get('status') == 'downloading': self._on_progress(d)

    def cancel(self):
        with self._lock: self._is_cancelled = True

    def _on_progress(self, d):
        if self.progress_callback: self.progress_callback(d)

    def _log(self, msg):
        logger.info(msg)
        if self.log_callback: self.log_callback(msg)

    @staticmethod
    def format_size(bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024: return f"{bytes:.1f}{unit}"
            bytes /= 1024
        return f"{bytes:.1f}TB"

    @staticmethod
    def format_eta(seconds):
        if not seconds: return "00:00"
        m, s = divmod(int(seconds), 60); h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
