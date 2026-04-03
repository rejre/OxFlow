# OxFlow 项目文档

## 📚 目录

1. [安装指南](#安装指南)
2. [快速开始](#快速开始)
3. [配置说明](#配置说明)
4. [开发指南](#开发指南)
5. [常见问题](#常见问题)
6. [项目架构](#项目架构)

## 安装指南

### 系统要求

- **Python**: 3.10 或更高版本
- **操作系统**: macOS, Windows, Linux
- **FFmpeg**: 用于视频合并和音频提取（可选但推荐）

### 方式 1：pip 安装（推荐）

```bash
pip install oxflow
oxflow
```

### 方式 2：源代码运行

```bash
# 克隆仓库
git clone https://github.com/rejre/OxFlow.git
cd OxFlow

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行程序
python src/ui/main_window.py
```

### 安装 FFmpeg

#### macOS (使用 Homebrew)
```bash
brew install ffmpeg
```

#### Windows
1. 从 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载
2. 解压到 `C:\ffmpeg`
3. 将 `C:\ffmpeg\bin` 添加到系统环境变量 `PATH`

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install ffmpeg
```

## 快速开始

### 基本用法

1. **启动应用**
   ```bash
   python src/ui/main_window.py
   ```

2. **输入下载链接**
   - YouTube: `https://www.youtube.com/watch?v=...`
   - B站: `https://www.bilibili.com/video/...`
   - 直接文件: `https://example.com/file.zip`

3. **选择质量和格式**
   - 视频：360p - 4K (2160p)
   - 音频：提取 MP3

4. **开始下载**
   - 点击下载按钮
   - 监控进度

### 支持的网站

OxFlow 支持 1000+ 视频网站，包括：

- YouTube, Vimeo
- Bilibili (B站), Douyin (抖音)
- TikTok
- Facebook, Instagram
- Twitter (X)
- 以及更多...

完整列表请查看 [yt-dlp 支持的网站](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

## 配置说明

### 配置文件位置

配置文件存储在用户主目录下：

- **macOS/Linux**: `~/.oxflow/config.json`
- **Windows**: `%APPDATA%\OxFlow\config.json`

### 配置项说明

```json
{
  "language": "zh_CN",              // 语言: en, zh_CN, ja
  "appearance_mode": "Dark",        // 外观: Light, Dark, System
  "window_opacity": 1.0,            // 窗口透明度: 0.4-1.0
  "download_path": "/Users/user/Downloads",
  "ffmpeg_path": "/usr/local/bin",
  "proxy_url": "",                  // 代理 URL (可选)
  "cookies_browser": "none",        // 浏览器 Cookie 来源
  "default_quality": "1080p",       // 默认分辨率
  "low_power_mode": false           // 低功耗模式
}
```

### 高级配置

#### 使用代理

在设置中填入代理 URL，格式：
```
http://127.0.0.1:7890
https://user:password@proxy.com:8080
```

#### 浏览器 Cookie 支持

支持从以下浏览器导入 Cookie：
- Chrome / Chromium
- Firefox
- Safari
- Edge
- Opera
- Vivaldi

此功能用于访问需要登录的视频（如私密视频、付费内容等）

## 开发指南

### 开发环境设置

```bash
# 克隆和进入项目
git clone https://github.com/rejre/OxFlow.git
cd OxFlow

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -r requirements-dev.txt

# 安装 pre-commit 钩子
pre-commit install
```

### 代码风格

遵循 PEP 8 规范，项目使用以下工具：

```bash
# 自动格式化
black src/ tests/
isort src/ tests/

# 代码检查
flake8 src/ tests/
mypy src/

# 运行测试
pytest
pytest --cov=src              # 生成覆盖率报告
```

### 项目结构

```
OxFlow/
├── src/
│   ├── ui/                    # UI 界面
│   │   └── main_window.py
│   ├── core/                  # 核心下载逻辑
│   │   └── downloader.py
│   └── utils/                 # 工具模块
│       ├── config.py          # 配置管理
│       └── i18n.py            # 国际化
├── tests/                     # 单元测试
├── .github/
│   └── workflows/             # CI/CD 配置
├── requirements.txt           # 生产依赖
├── requirements-dev.txt       # 开发依赖
└── setup.py                   # 包配置
```

### 贡献流程

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 编写代码和测试
4. 运行测试确保通过 (`pytest`)
5. 提交更改 (`git commit -m 'Add amazing feature'`)
6. 推送到分支 (`git push origin feature/amazing-feature`)
7. 创建 Pull Request

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 常见问题

### Q: 下载速度很慢？
**A**: 
- 检查网络连接
- 尝试使用代理
- 确保 FFmpeg 已安装

### Q: 某个网站无法下载？
**A**:
- 该网站可能限制了爬虫
- 尝试更新 yt-dlp：`pip install --upgrade yt-dlp`
- 提交 Issue 或使用浏览器 Cookie

### Q: 如何在 Linux 服务器上使用（无 GUI）？
**A**:
- 目前 OxFlow 是 GUI 应用，CLI 版本还在规划中
- 可以考虑直接使用 yt-dlp CLI 工具

### Q: 支持字幕下载吗？
**A**:
- 目前主要支持视频和音频
- 字幕功能在开发计划中

### Q: 如何卸载？
**A**:
```bash
pip uninstall oxflow
```

## 项目架构

### 核心模块

#### 1. DownloadEngine (core/downloader.py)
- 视频/音频信息获取
- 直接文件链接识别
- 多线程下载
- 代理支持
- FFmpeg 集成

#### 2. ConfigManager (utils/config.py)
- 配置文件管理
- 原子化 JSON 存储
- 跨平台路径处理

#### 3. I18nManager (utils/i18n.py)
- 多语言支持
- 字符串翻译管理
- 动态语言切换

#### 4. MainWindow (ui/main_window.py)
- CustomTkinter UI
- 设置窗口
- 下载历史
- 实时进度显示

### 依赖关系图

```
MainWindow
├── DownloadEngine
│   ├── yt-dlp
│   ├── requests
│   └── psutil
├── ConfigManager
│   └── (JSON files)
├── I18nManager
│   └── (Translation JSON)
└── CustomTkinter
```

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 支持和反馈

- 📝 提交 Issue: [GitHub Issues](https://github.com/rejre/OxFlow/issues)
- 💬 讨论: [GitHub Discussions](https://github.com/rejre/OxFlow/discussions)
- ⭐ 如果觉得有用，请给个 Star！

## 路线图

- [ ] CLI 版本
- [ ] 字幕下载支持
- [ ] 批量下载队列
- [ ] 下载历史导出
- [ ] 插件系统
- [ ] 国际化改进

感谢使用 OxFlow！🎉
