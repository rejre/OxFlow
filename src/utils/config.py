"""
OxFlow - Configuration Manager
Handles persistent settings with safe read/write and auto-migration.
"""

import json
import os
import shutil
import platform
import logging

logger = logging.getLogger(__name__)

VALID_QUALITIES = ["2160p", "1440p", "1080p", "720p", "480p", "360p"]
VALID_LANGUAGES = ["en", "zh_CN", "ja"]


class ConfigManager:
    CONFIG_VERSION = 2

    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.expanduser("~/.oxflow_config.json")
        self.defaults = {
            "_version": self.CONFIG_VERSION,
            "language": "zh_CN",
            "download_path": os.path.expanduser("~/Downloads"),
            "ffmpeg_path": self._auto_find_ffmpeg(),
            "default_quality": "1080p",
            "low_power_mode": False,
            "max_retries": 10,
            "concurrent_fragments": 4,
            "history": [],
        }
        self.settings: dict = {}
        self.load()

    def _auto_find_ffmpeg(self) -> str:
        found = shutil.which("ffmpeg")
        if found:
            return os.path.dirname(found)

        candidates = []
        if platform.system() == "Darwin":
            candidates = ["/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg", "/opt/local/bin/ffmpeg"]
        elif platform.system() == "Linux":
            candidates = ["/usr/bin/ffmpeg", "/usr/local/bin/ffmpeg"]
        elif platform.system() == "Windows":
            candidates = [r"C:\ffmpeg\bin\ffmpeg.exe", r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"]

        for p in candidates:
            if os.path.exists(p):
                return os.path.dirname(p)
        return ""

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                merged = {**self.defaults, **raw}
                self.settings = self._validate(merged)
                self._migrate(self.settings)
                return
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Config load error ({e}), using defaults.")
        self.settings = dict(self.defaults)

    def save(self, data: dict = None):
        if data:
            self.settings.update(data)
            self.settings = self._validate(self.settings)
        self.settings["_version"] = self.CONFIG_VERSION
        tmp_path = self.config_path + ".tmp"
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.config_path)), exist_ok=True)
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            os.replace(tmp_path, self.config_path)
        except IOError as e:
            logger.error(f"Config save failed: {e}")

    def _validate(self, cfg: dict) -> dict:
        if cfg.get("language") not in VALID_LANGUAGES: cfg["language"] = "zh_CN"
        if cfg.get("default_quality") not in VALID_QUALITIES: cfg["default_quality"] = "1080p"
        dp = cfg.get("download_path", "")
        if not dp or not os.path.isdir(dp): cfg["download_path"] = os.path.expanduser("~/Downloads")
        cfg["max_retries"] = max(1, min(int(cfg.get("max_retries", 10)), 50))
        cfg["concurrent_fragments"] = max(1, min(int(cfg.get("concurrent_fragments", 4)), 16))
        if not isinstance(cfg.get("history"), list): cfg["history"] = []
        return cfg

    def _migrate(self, cfg: dict):
        version = cfg.get("_version", 1)
        if version < 2:
            ffmpeg = cfg.get("ffmpeg_path", "")
            if ffmpeg and os.path.isfile(ffmpeg):
                cfg["ffmpeg_path"] = os.path.dirname(ffmpeg)
            cfg["_version"] = 2

    def add_history(self, entry: dict, max_items: int = 100):
        history: list = self.settings.setdefault("history", [])
        history.insert(0, entry)
        self.settings["history"] = history[:max_items]
        self.save()
