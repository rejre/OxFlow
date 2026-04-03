# OxFlow — 变色牛万能下载器 (v2.1.1)

[English](./README.md) | **简体中文**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)]()
[![Latest Release](https://img.shields.io/badge/Latest-v2.1.1-brightgreen.svg)](https://github.com/rejre/OxFlow/releases)
[![Tests](https://img.shields.io/badge/Tests-35%2B-brightgreen.svg)](./tests/)

**OxFlow (变色牛)** 是一款基于 Python 和 CustomTkinter 开发的极简、现代风万能下载工具。它不仅支持全球 1000+ 视频网站的音视频抓取，还能像专业下载器一样处理各种直接文件链接。

> 💡 **v2.1.1 新版本：** 现已支持自动重试、断点续传、网络优化！即使网络不稳定，下载也能稳定进行！

---

### ✨ v2.1.1 新增特性 (下载稳定性提升)

#### 🔄 自动重试机制
- 网络中断自动重试，最多 3 次
- 指数退避策略：2秒 → 4秒 → 8秒
- 智能错误分类，区分可重试和不可重试的错误

#### 🔗 断点续传支持
- 启用 HTTP Range 请求
- 网络中断后从断点继续下载
- 节省时间和带宽

#### 🌐 网络优化
- Socket 超时：60 秒
- HTTP 块大小：1 MB
- 并发片段限制：4

#### 📊 完整的测试框架
- 35+ 个测试用例
- pytest 框架集成
- GitHub Actions CI/CD 自动化

#### 📚 完整的文档
- 用户故障排查指南：[DOWNLOAD_TROUBLESHOOTING.md](./DOWNLOAD_TROUBLESHOOTING.md)
- 技术实现说明：[DOWNLOAD_FIX.md](./DOWNLOAD_FIX.md)
- 完整项目文档：[DOCUMENTATION.md](./DOCUMENTATION.md)

---

### 🌟 核心亮点

-   **全平台视频抓取**：集成强大的 `yt-dlp` 内核，支持 YouTube、Bilibili (B站)、TikTok、Vimeo、Twitter (X)、Facebook 等 1000 多个主流网站。
-   **智能直接下载**：自动识别 `.exe`, `.dmg`, `.zip`, `.jpg`, `.pdf` 等直接文件链接。针对 GitHub Release 等加密/重定向链接进行了深度优化，精准提取文件名。
-   **外观自定义**：支持**透明度调节**和**深浅色主题**切换，打造属于你的下载器。
-   **超清画质选择**：支持从 360p 到 4K (2160p) 的全分辨率选择，并支持一键提取最高码率的 MP3 音频。
-   **极致 UI 体验**：采用精心设计的现代界面，支持封面图预览、下载历史记录、以及实时下载速度/剩余时间显示。
-   **多语言支持**：原生支持 简体中文、英语、日语 切换。
-   **性能优化**：提供“低功耗模式”，显著降低 CPU 占用。

---

### 🚀 快速开始

#### macOS 用户（推荐）

**选项 1: 使用 DMG 安装包（最简单）**
1. 下载最新版本：[OxFlow-2.1.1.dmg](https://github.com/rejre/OxFlow/releases) (90 MB)
2. 双击挂载 DMG 文件
3. 将 OxFlow 拖到 Applications 文件夹
4. 打开 Applications，双击 OxFlow 启动

**选项 2: 从源代码运行**
```bash
# 1. 克隆仓库
git clone https://github.com/rejre/OxFlow.git
cd OxFlow

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动程序
python src/ui/main_window.py
```

#### Windows 和 Linux 用户

```bash
# 1. 克隆仓库
git clone https://github.com/rejre/OxFlow.git
cd OxFlow

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动程序
python src/ui/main_window.py
```

> **⚠️ 依赖要求**
> - Python 3.10 或更高版本
> - FFmpeg（用于视频合并和 MP3 提取）
>   - macOS: `brew install ffmpeg`
>   - Windows: [下载](https://ffmpeg.org/download.html)
>   - Linux: `sudo apt install ffmpeg`

---

### 📂 项目结构

```
OxFlow/
├── src/
│   ├── ui/
│   │   └── main_window.py          # 程序入口与 UI 界面
│   ├── core/
│   │   └── downloader.py           # 下载引擎 (yt-dlp + requests + 重试机制)
│   └── utils/
│       ├── config.py                # 配置管理 (原子化 JSON 存储)
│       ├── i18n.py                  # 多语言管理中心
│       ├── logging_config.py         # 日志系统（带轮转）
│       ├── exceptions.py             # 自定义异常类
│       └── network_config.py         # 网络和重试配置
├── tests/
│   ├── test_downloader.py           # 下载引擎测试
│   ├── test_config.py               # 配置管理测试
│   └── test_i18n.py                 # 国际化测试
├── .github/
│   └── workflows/
│       └── tests.yml                # GitHub Actions CI/CD
├── dist/
│   └── OxFlow-2.1.1.dmg            # macOS DMG 安装包
├── DOCUMENTATION.md                 # 完整项目文档
├── DOWNLOAD_FIX.md                 # 下载修复技术说明
├── DOWNLOAD_TROUBLESHOOTING.md      # 下载故障排查指南
├── QUICK_START.md                  # 快速开始指南
├── requirements.txt                # 生产依赖
├── requirements-dev.txt            # 开发依赖
├── Makefile                        # 开发命令集
└── LICENSE                         # MIT 许可证
```

---

### 🛡️ 开源协议
本项目采用 [MIT](./LICENSE) 协议开源。欢迎提交 Pull Request 或 Issue 来帮助 OxFlow 变得更好！

---

### 📥 下载和安装

#### 最新版本 (v2.1.1)

**macOS DMG 安装包**
- [OxFlow-2.1.1.dmg](https://github.com/rejre/OxFlow/releases/download/v2.1.1/OxFlow-2.1.1.dmg) (90 MB)
- 包含完整的运行时依赖
- 支持 Apple Silicon (M1/M2) 和 Intel Mac

**源代码**
- [GitHub 仓库](https://github.com/rejre/OxFlow)
- 支持 macOS、Windows、Linux

#### 历史版本

- v2.1.0 - 原始版本 (UI 改进)
- v2.0.x - 旧版本系列

详见 [GitHub Releases](https://github.com/rejre/OxFlow/releases)

---

### 🐛 故障排查

遇到下载问题？参考：
- [DOWNLOAD_TROUBLESHOOTING.md](./DOWNLOAD_TROUBLESHOOTING.md) - 常见错误和解决方案
- [DOWNLOAD_FIX.md](./DOWNLOAD_FIX.md) - 技术实现细节

---

### 📈 推广与支持
如果你觉得这个工具好用，请给一个 **Star** ⭐！这对我非常重要。
