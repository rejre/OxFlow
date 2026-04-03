# OxFlow 版本发布历史

## 版本管理政策

OxFlow 采用语义版本控制 (Semantic Versioning)：
- **主版本号** (Major): 重大功能更新或不兼容改动
- **次版本号** (Minor): 新增功能或改进
- **修订号** (Patch): 错误修复

---

## v2.1.1 (最新) ⭐

**发布日期:** 2024-04-04  
**版本标签:** `v2.1.1`  
**GitHub 链接:** https://github.com/rejre/OxFlow/releases/tag/v2.1.1

### 📦 下载

#### macOS DMG 安装包（推荐）
- **文件名:** `OxFlow-2.1.1.dmg`
- **大小:** 90 MB
- **格式:** 压缩 DMG (UDZO)
- **兼容性:** macOS 10.13+ (支持 Intel 和 Apple Silicon)
- **包含内容:** 完整的 Python 运行时 + 所有依赖

#### 源代码
- 在 GitHub 仓库的 `main` 分支
- 支持 macOS、Windows、Linux

### ✨ 新增功能

#### 🔄 自动重试机制
```
• 最多 3 次自动重试
• 指数退避策略：2秒 → 4秒 → 8秒
• 智能错误分类（可重试 vs 不可重试）
• 适应网络不稳定环境
```

#### 🔗 断点续传支持
```
• 启用 HTTP Range 请求
• 网络中断后自动恢复
• 大文件下载友好
• 节省时间和带宽
```

#### 🌐 网络优化
```
• socket_timeout: 60 秒（防止超时）
• http_chunk_size: 1 MB（提高稳定性）
• concurrent_fragments: 4（避免过载）
• 完善的错误消息
```

#### 🧪 测试框架
```
• 35+ 个测试用例
• pytest 框架集成
• GitHub Actions CI/CD（3 OS × 3 Python 版本）
```

#### 📚 完整文档
```
• 8000+ 字完整项目文档
• 用户故障排查指南
• 技术实现细节说明
• 开发者贡献指南
```

### 🔧 改进

- 添加网络配置模块 (`src/utils/network_config.py`)
- 实现自定义异常层次结构 (`src/utils/exceptions.py`)
- 完善日志系统，支持轮转 (`src/utils/logging_config.py`)
- 代码质量工具集成 (Black, isort, Flake8, mypy)
- GitHub Actions 自动化测试流程

### 📋 修复的问题

| 问题 | 描述 | 状态 |
|------|------|------|
| 网络中断 | 下载到一定进度时停止 | ✅ 已修复 |
| 无法恢复 | "bytes read X, Y more expected" 错误 | ✅ 已修复 |
| 重复下载 | 网络失败需从头再来 | ✅ 已修复 |
| 不稳定 | 弱网下载失败率高 | ✅ 已修复 |

### 📊 技术信息

**构建环境:**
- Python 3.14.3
- PyInstaller 6.19.0
- yt-dlp 2026.3.17
- customtkinter 5.2.2
- Pillow 12.2.0

**依赖更新:**
- yt-dlp: 更新到最新版本（2026.3.17）
- 所有生产依赖版本锁定

**文件大小:**
- DMG 安装包: 90 MB
- macOS 应用包: 200+ MB（包含所有依赖）

### 🔗 相关文档

- [DOWNLOAD_FIX.md](./DOWNLOAD_FIX.md) - 技术实现细节
- [DOWNLOAD_TROUBLESHOOTING.md](./DOWNLOAD_TROUBLESHOOTING.md) - 故障排查指南
- [CHANGELOG.md](./CHANGELOG.md) - 版本更新日志

---

## v2.1.0

**发布日期:** 之前  
**版本标签:** `v2.1`  
**GitHub 链接:** https://github.com/rejre/OxFlow/releases/tag/v2.1

### ✨ 功能

- UI 改进：透明度调节和深浅色主题
- 下载引擎完善
- 多语言支持增强

### 📦 下载

- 源代码仅发布（无 DMG）

---

## v2.0

**发布日期:** 早期版本  
**版本标签:** `v2.0`  
**GitHub 链接:** https://github.com/rejre/OxFlow/releases/tag/v2.0

### 功能

- 基础视频下载功能
- 直链下载支持
- 多网站兼容

---

## 版本支持政策

| 版本 | 状态 | 支持期 |
|------|------|--------|
| v2.1.1 | 🟢 活跃 | 当前 |
| v2.1.0 | 🟡 维护 | 有限支持 |
| v2.0 | 🔴 已停用 | 不支持 |

**更新建议:** 所有用户应升级到 v2.1.1 以获得最新的功能和安全修复

---

## 如何升级

### macOS DMG 用户

1. 下载新版本 DMG
2. 关闭旧版 OxFlow
3. 打开新 DMG，拖拽到 Applications 覆盖旧版本
4. 重新启动应用

### 源代码用户

```bash
# 1. 更新代码
git pull origin main

# 2. 更新依赖
pip install -r requirements.txt --upgrade

# 3. 重新运行
python src/ui/main_window.py
```

---

## 反馈与报告

- **发现 Bug:** 提交 [Issue](https://github.com/rejre/OxFlow/issues)
- **功能建议:** 讨论区或 Discussions
- **贡献代码:** 提交 [Pull Request](https://github.com/rejre/OxFlow/pulls)

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 版本文件位置

| 文件 | 位置 | 说明 |
|------|------|------|
| v2.1.1 DMG | `dist/OxFlow-2.1.1.dmg` | 最新安装包 |
| v2.1.0 DMG | 已删除 | 使用 git tag 查看历史 |
| 源代码 | GitHub main | 随时可用 |
| 发行说明 | GitHub Releases | 完整的发行历史 |

---

## 总结

✅ 采用语义版本管理  
✅ 每个版本都有明确的标签  
✅ 完整的历史记录  
✅ 清晰的升级路径  
✅ 持续的维护和支持
