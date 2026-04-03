"""
OxFlow - 网络和下载优化配置
用于改进网络稳定性和下载可靠性
"""

# yt-dlp 优化选项
YTDLP_OPTIMIZATIONS = {
    # 连接和超时设置
    'socket_timeout': 60,           # Socket 超时 60 秒
    'retries': 10,                  # 最大重试次数
    'fragment_retries': 10,         # 碎片重试次数
    
    # 断点续传和恢复
    'continuedl': True,             # 启用断点续传
    'skip_unavailable_fragments': True,  # 跳过不可用碎片
    
    # 并发设置
    'concurrent_fragment_downloads': 4,  # 限制并发下载数
    
    # HTTP 块大小优化
    'http_chunk_size': 1024 * 1024,     # 1 MB 块大小
    
    # 用户代理
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
}

# 网络重试策略
RETRY_STRATEGY = {
    'max_retries': 3,
    'initial_backoff': 2,      # 初始等待 2 秒
    'max_backoff': 60,         # 最大等待 60 秒
    'backoff_multiplier': 2,   # 指数退避乘数
}

# 可重试的网络错误
RETRYABLE_ERRORS = [
    'bytes read',
    'connection',
    'timeout',
    'HTTP 503',
    'HTTP 429',
    'Connection reset',
    'Connection aborted',
    'Broken pipe',
    'Network unreachable',
]

# 不可重试的错误
NON_RETRYABLE_ERRORS = [
    'HTTP 404',
    'HTTP 403',
    'Access denied',
    'Invalid URL',
    'File not found',
]

# 下载块大小
DOWNLOAD_CHUNK_SIZES = {
    'direct_file': 256 * 1024,      # 直接文件：256 KB
    'streaming': 64 * 1024,         # 流媒体：64 KB
    'large_file': 1024 * 1024,      # 大文件：1 MB
}

# 超时设置（秒）
TIMEOUT_SETTINGS = {
    'socket': 60,               # Socket 超时
    'download': 300,            # 单个块下载超时
    'connection': 30,           # 连接超时
}

# 代理配置示例
PROXY_CONFIG = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

# yt-dlp 格式优先级（降序）
FORMAT_PRIORITY = [
    # 4K
    "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best[height<=2160]",
    # 1440p
    "bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best[height<=1440]",
    # 1080p
    "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    # 720p
    "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]",
    # 480p
    "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]",
    # 360p
    "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]",
    # 降级方案
    "best",
]
