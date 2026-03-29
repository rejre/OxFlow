# OxFlow — 变色牛万能下载器

[English](./README.md) | **简体中文**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)]()

**OxFlow (变色牛)** 是一款基于 Python 和 CustomTkinter 开发的极简、现代风万能下载工具。它不仅支持全球 1000+ 视频网站的音视频抓取，还能像专业下载器一样处理各种直接文件链接。

---

### 🌟 核心亮点

-   **全平台视频抓取**：集成强大的 `yt-dlp` 内核，支持 YouTube、Bilibili (B站)、TikTok、Vimeo、Twitter (X)、Facebook 等 1000 多个主流网站。
-   **智能直接下载**：自动识别 `.exe`, `.dmg`, `.zip`, `.jpg`, `.pdf` 等直接文件链接。针对 GitHub Release 等加密/重定向链接进行了深度优化，精准提取文件名。
-   **超清画质选择**：支持从 360p 到 4K (2160p) 的全分辨率选择，并支持一键提取最高码率的 MP3 音频。
-   **极致 UI 体验**：采用精心设计的深色系界面，支持封面图预览、下载历史记录、以及实时下载速度/剩余时间显示。
-   **多语言支持**：原生支持 简体中文、英语、日语 切换。
-   **性能优化**：提供“低功耗模式”，显著降低 CPU 占用，延长笔记本续航。

---

### 🚀 快速开始

#### 1. 运行环境
确保你的电脑已安装 Python 3.10 或更高版本。

#### 2. 安装依赖
```bash
pip install -r requirements.txt
```

#### 3. 启动程序
```bash
python src/ui/main_window.py
```

> **注意**：为了合并高清视频和提取 MP3，系统必须安装 **FFmpeg**。
> - macOS: `brew install ffmpeg`
> - Windows: 请前往 ffmpeg.org 下载并配置环境变量。

---

### 📂 项目结构

```
ChameleonDownloader/
├── src/
│   ├── ui/
│   │   └── main_window.py      # 程序入口与 UI 界面
│   ├── core/
│   │   └── downloader.py       # 下载引擎 (yt-dlp + requests)
│   └── utils/
│       ├── config.py            # 配置管理 (原子化 JSON 存储)
│       └── i18n.py              # 多语言管理中心
├── icon.png                     # 应用图标
└── requirements.txt             # 依赖清单
```

---

### 🛡️ 开源协议
本项目采用 [MIT](./LICENSE) 协议开源。欢迎提交 Pull Request 或 Issue 来帮助 OxFlow 变得更好！

---

### 📈 推广与支持
如果你觉得这个工具好用，请给一个 **Star** ⭐！这对我非常重要。
