"""
OxFlow - Internationalization Manager
Loads translations from resources/locales/*.json
"""

import json
import os
import sys
import logging

logger = logging.getLogger(__name__)

DEFAULT_LANG = "en"
DEFAULT_VERSION = "v2.1"

class I18nManager:
    def __init__(self, lang: str = "en"):
        self.version = DEFAULT_VERSION
        self._lang = lang
        self._strings: dict = {}
        
        # 确定资源路径 (兼容 PyInstaller 打包)
        if hasattr(sys, '_MEIPASS'):
            self.base_path = os.path.join(sys._MEIPASS, 'resources', 'locales')
        else:
            # 开发环境下定位到 src/resources/locales
            self.base_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'locales')
        
        self.set_language(lang)

    def set_language(self, lang: str):
        self._lang = lang
        file_path = os.path.join(self.base_path, f"{lang}.json")
        
        if not os.path.exists(file_path):
            logger.warning(f"Locale file not found: {file_path}, falling back to English.")
            file_path = os.path.join(self.base_path, f"{DEFAULT_LANG}.json")
            self._lang = DEFAULT_LANG

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self._strings = json.load(f)
            self.version = self._strings.get("version", DEFAULT_VERSION)
        except Exception as e:
            logger.error(f"Failed to load translation {lang}: {e}")
            self._strings = {}

    @property
    def current_language(self) -> str: return self._lang

    def get(self, key: str, default: str = "") -> str:
        value = self._strings.get(key)
        if value is None:
            # 如果当前语言没有，尝试找英文
            return default or key
        return value

    def __getitem__(self, key: str) -> str: return self.get(key)
