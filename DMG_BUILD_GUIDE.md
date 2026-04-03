# OxFlow DMG 构建指南

本指南介绍如何为 macOS 构建 OxFlow 安装文件（DMG）。

## 📋 前置要求

- macOS 10.14 或更高版本
- Python 3.10+
- 已安装 OxFlow 项目依赖

## 🚀 快速开始

### 方式 1: 使用 Makefile（推荐）

```bash
cd ~/ai-workspace/oxflow-improvement
make dmg
```

### 方式 2: 使用 Shell 脚本

```bash
cd ~/ai-workspace/oxflow-improvement
chmod +x scripts/build_dmg.sh
./scripts/build_dmg.sh
```

### 方式 3: 使用 Python 脚本

```bash
cd ~/ai-workspace/oxflow-improvement
python3 scripts/build_dmg.py
```

## 📦 构建流程

构建过程分为 5 个步骤：

1. **检查依赖** - 验证 PyInstaller、Python 和 macOS 工具
2. **安装依赖** - 安装项目的 Python 依赖库
3. **构建应用** - 使用 PyInstaller 将 Python 代码编译成 .app 文件
4. **创建 DMG** - 打包 .app 文件和应用快捷方式为 DMG 文件
5. **完成** - 输出最终的 DMG 安装文件

## 📊 构建细节

### PyInstaller 配置

构建脚本使用以下 PyInstaller 选项：

```
--name OxFlow              # 应用名称
--onefile                  # 单文件打包（可选）
--windowed                 # GUI 应用（无控制台窗口）
--icon icon.png           # 应用图标
--osx-bundle-identifier   # macOS Bundle ID
--target-architecture universal2  # 支持 Intel 和 Apple Silicon
```

### 包含的资源

构建时自动包含：
- `src/utils/` - 工具模块
- `src/core/` - 核心下载逻辑
- `src/resources/` - 资源文件
- 所有依赖库（customtkinter, yt-dlp, 等）

### DMG 结构

生成的 DMG 包含：
```
OxFlow-2.1.0.dmg
├── OxFlow.app           # 应用程序
└── Applications/        # Applications 文件夹快捷方式
```

## 🎯 输出文件

构建完成后，DMG 文件位置：

```
dist/OxFlow-2.1.0.dmg
```

文件大小通常在 150-200 MB 之间（取决于依赖库）。

## 💿 安装和使用

### 对用户

1. 下载 `OxFlow-2.1.0.dmg`
2. 双击打开 DMG 文件（自动挂载）
3. 拖拽 **OxFlow.app** 到 **Applications** 文件夹
4. 从 Launchpad 或 Applications 启动 OxFlow

### 第一次运行

macOS 首次运行可能会显示安全警告，此时：
1. 打开**系统偏好设置** → **安全性与隐私**
2. 点击**仍要打开**允许运行应用

## 🔧 故障排查

### 构建失败: PyInstaller 未找到

```bash
pip install pyinstaller
```

### 构建失败: 图标格式错误

确保 `icon.png` 存在且有效：
```bash
ls -lh icon.png
file icon.png
```

### 构建失败: hdiutil 错误（非 macOS）

DMG 只能在 macOS 系统上构建。Windows/Linux 用户需要：
- 在 macOS 上构建，或
- 使用虚拟机/远程 macOS 系统

### DMG 大小过大

如果 DMG 文件超过 300 MB：

1. 减少依赖库（删除不需要的库）
2. 使用 `--onedir` 而不是 `--onefile`
3. 移除调试符号：
   ```bash
   strip -x dist/OxFlow.app/Contents/MacOS/OxFlow
   ```

## 📝 代码签名和公证（可选）

用于在 Apple 应用商店发行：

### 1. 创建证书

```bash
# 使用开发者证书签名
codesign -s "Developer ID Application" dist/OxFlow.app
```

### 2. 公证应用

```bash
# 提交公证
xcrun notarytool submit OxFlow-2.1.0.dmg --apple-id <apple-id> --password <app-password> --team-id <team-id>
```

## 🔐 安全性考虑

- DMG 文件不含恶意代码（开源项目）
- 应用通过 PyInstaller 打包，为标准 macOS 应用
- 用户可验证源代码：[GitHub - rejre/OxFlow](https://github.com/rejre/OxFlow)

## 📊 技术规格

| 项目 | 值 |
|------|-----|
| 应用格式 | macOS .app bundle |
| DMG 格式 | UDZO (压缩) |
| 最低系统 | macOS 10.14 (可选配置) |
| 架构 | universal2 (Intel/Apple Silicon) |
| 依赖库 | 自包含在 .app 中 |

## 🔄 自动化构建

### GitHub Actions

可在 CI/CD 工作流中自动构建 DMG：

```yaml
- name: Build DMG
  if: runner.os == 'macOS'
  run: make dmg
  
- name: Upload DMG
  uses: actions/upload-artifact@v3
  with:
    name: OxFlow-DMG
    path: dist/*.dmg
```

## 📚 相关资源

- [PyInstaller 文档](https://pyinstaller.org/)
- [macOS 应用打包指南](https://developer.apple.com/documentation/bundleresources)
- [hdiutil 手册](https://ss64.com/osx/hdiutil.html)

## 🆘 获取帮助

遇到问题？

1. 查看构建日志输出
2. 检查 [GitHub Issues](https://github.com/rejre/OxFlow/issues)
3. 查看本文档的故障排查部分

## 📝 许可证

OxFlow 采用 MIT 许可证。所有构建的应用均包含此许可证。

---

**最后更新**: 2024-04-03
