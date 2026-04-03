"""
OxFlow - Custom Exceptions
Comprehensive exception hierarchy for OxFlow.
"""


class OxFlowError(Exception):
    """Base exception for all OxFlow errors."""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        super().__init__(self.message)


class ConfigError(OxFlowError):
    """Configuration related errors."""
    
    def __init__(self, message: str):
        super().__init__(message, "CONFIG_ERROR")


class DownloadError(OxFlowError):
    """Download operation related errors."""
    
    def __init__(self, message: str, error_code: str = "DOWNLOAD_ERROR"):
        super().__init__(message, error_code)


class URLError(DownloadError):
    """Invalid or unsupported URL errors."""
    
    def __init__(self, message: str):
        super().__init__(message, "URL_ERROR")


class NetworkError(DownloadError):
    """Network connectivity errors."""
    
    def __init__(self, message: str):
        super().__init__(message, "NETWORK_ERROR")


class FFmpegError(DownloadError):
    """FFmpeg related errors."""
    
    def __init__(self, message: str):
        super().__init__(message, "FFMPEG_ERROR")


class DownloadCancelledError(DownloadError):
    """Download was cancelled by user."""
    
    def __init__(self, message: str = "Download cancelled"):
        super().__init__(message, "DOWNLOAD_CANCELLED")


class TimeoutError(DownloadError):
    """Operation timeout."""
    
    def __init__(self, message: str):
        super().__init__(message, "TIMEOUT_ERROR")


class I18nError(OxFlowError):
    """Internationalization errors."""
    
    def __init__(self, message: str):
        super().__init__(message, "I18N_ERROR")


# Error message templates
ERROR_MESSAGES = {
    "INVALID_URL": "无效的 URL: {url}",
    "UNSUPPORTED_URL": "暂不支持的网站: {url}",
    "NETWORK_ERROR": "网络错误: {error}",
    "FFMPEG_NOT_FOUND": "未找到 FFmpeg，请先安装",
    "DOWNLOAD_FAILED": "下载失败: {error}",
    "PERMISSION_ERROR": "无权访问下载目录: {path}",
    "DISK_SPACE_ERROR": "磁盘空间不足",
    "PROXY_ERROR": "代理连接失败: {error}",
    "TIMEOUT": "请求超时 ({timeout}s)",
    "CANCELLED": "下载已取消",
}


def get_error_message(error_key: str, **kwargs) -> str:
    """Get localized error message."""
    template = ERROR_MESSAGES.get(error_key, error_key)
    try:
        return template.format(**kwargs)
    except KeyError:
        return template
