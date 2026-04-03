# OxFlow v2.1.0 macOS 发行说明

**发布日期**: 2024-04-03
**版本**: 2.1.0  
**平台**: macOS 10.14+

## 📦 安装包信息

| 项目 | 详情 |
|------|------|
| **文件名** | OxFlow-2.1.0.dmg |
| **文件大小** | 89 MB |
| **文件格式** | UDZO 压缩 DMG |
| **架构** | Apple Silicon + Intel |
| **最低系统** | macOS 10.14 或更高 |

## 🚀 安装步骤

### 第一步：下载
点击下载 `OxFlow-2.1.0.dmg` 文件。

### 第二步：挂载
双击 DMG 文件，macOS 会自动挂载并打开安装窗口。

### 第三步：安装
将 **OxFlow.app** 拖拽到 **Applications** 文件夹。

```
📂 OxFlow-2.1.0.dmg
├── 📱 OxFlow.app ← 拖这个到 Applications 文件夹
└── 📁 Applications (快捷方式)
```

### 第四步：运行
从以下任一方式启动：
- **Launchpad**: 搜索并点击 "OxFlow"
- **Finder**: 打开 Applications 文件夹，双击 OxFlow
- **命令行**: `open /Applications/OxFlow.app`

## ⚙️ 系统要求

- **操作系统**: macOS 10.14 (Mojave) 或更高
- **处理器**: Intel 或 Apple Silicon（M1/M2/M3 等）
- **内存**: 2 GB RAM（推荐 4 GB）
- **磁盘空间**: 500 MB（用于应用和缓存）
- **网络**: 互联网连接（用于下载视频）

### 可选
- **FFmpeg**: 用于视频转码和音频提取
  ```bash
  brew install ffmpeg
  ```

## ✨ 此版本新增功能

### 代码质量改进
- ✅ 完整的单元测试框架 (35+ 测试用例)
- ✅ 自动化 CI/CD 流程 (GitHub Actions)
- ✅ 代码质量工具集成 (Black, isort, Flake8, mypy)
- ✅ Pre-commit 钩子自动检查

### 日志和错误处理
- ✅ 改进的日志系统（自动轮转）
- ✅ 自定义异常体系（7+ 异常类）
- ✅ 更详细的错误消息

### 文档和用户体验
- ✅ 完整的项目文档 (8000+ 字)
- ✅ 快速开始指南和 API 文档
- ✅ 贡献者指南
- ✅ 改进的版本管理

## 🔍 首次运行

### macOS 安全警告

首次运行时，macOS 可能显示：
```
"OxFlow" 无法打开，因为 Apple 无法检查其中是否存在恶意软件
```

**解决方法**:
1. 打开 **系统偏好设置** → **安全性与隐私**
2. 在 **通用** 标签中找到 OxFlow
3. 点击 **仍要打开** 按钮

或使用终端：
```bash
xattr -d com.apple.quarantine /Applications/OxFlow.app
```

## 📝 使用指南

### 下载视频

1. 复制视频链接（支持 1000+ 网站）
2. 粘贴到 OxFlow 的 URL 输入框
3. 选择视频质量（360p - 4K）
4. 点击下载按钮

### 支持的网站

- YouTube, Vimeo, Dailymotion
- Bilibili (B站), 爱奇艺, 腾讯视频
- TikTok, Douyin (抖音)
- Facebook, Instagram, Twitter (X)
- 以及 1000+ 其他网站

完整列表: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

### 配置

配置文件位置：
```
~/.oxflow/config.json
```

或在应用内通过设置窗口修改。

## 🆘 故障排查

### 问题：应用无法启动
**解决**: 
```bash
# 检查权限
chmod +x /Applications/OxFlow.app/Contents/MacOS/OxFlow

# 从终端启动查看错误
/Applications/OxFlow.app/Contents/MacOS/OxFlow
```

### 问题：下载失败
**原因和解决**:
- 网络连接: 检查互联网连接
- 网站限制: 使用代理或更新 yt-dlp
- 权限问题: 确保下载文件夹可写

### 问题：视频无法播放或转码
**解决**:
```bash
# 安装 FFmpeg
brew install ffmpeg

# 在 OxFlow 设置中指定 FFmpeg 路径
# 通常在: /usr/local/bin 或 /opt/homebrew/bin
```

### 问题：某个网站无法下载
**解决**:
1. 更新 yt-dlp:
   ```bash
   pip install --upgrade yt-dlp
   ```
2. 使用浏览器 Cookie:
   在 OxFlow 设置中选择浏览器并重启

## 📊 性能建议

- **低功耗模式**: 在设置中启用以降低 CPU 占用
- **内存**: 下载大文件时可能需要 1-2 GB RAM
- **磁盘**: 确保下载目录有足够空间
- **网络**: 使用有线网络以获得更好的下载速度

## 🔐 隐私和安全

- ✅ 开源项目 - 源代码可审计
- ✅ 无数据收集 - 所有处理在本地进行
- ✅ 无广告 - 完全免费和无干扰
- ✅ MIT 许可 - 开放和可修改

## 📖 更多资源

- **GitHub**: https://github.com/rejre/OxFlow
- **问题报告**: https://github.com/rejre/OxFlow/issues
- **完整文档**: 项目 README 和 DOCUMENTATION.md
- **许可证**: MIT - 自由使用和修改

## ✨ 致谢

感谢以下开源项目的支持：
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 视频下载引擎
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - 现代 GUI 框架
- [PyInstaller](https://github.com/pyinstaller/pyinstaller) - Python 打包工具

## 📞 联系和支持

有问题或建议？
- 📝 提交 Issue: https://github.com/rejre/OxFlow/issues
- 💬 讨论: https://github.com/rejre/OxFlow/discussions
- ⭐ 如果有帮助，请给个 Star！

---

**版本**: 2.1.0
**最后更新**: 2024-04-03
**状态**: ✅ 生产就绪
