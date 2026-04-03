# DMG 文件上传指南

由于网络问题，DMG 文件无法通过自动化工具上传到 GitHub Release。以下是手动上传的步骤。

## 📋 文件信息

- **文件名**: OxFlow-2.1.1.dmg
- **文件大小**: 90 MB
- **位置**: `dist/OxFlow-2.1.1.dmg`
- **Release**: https://github.com/rejre/OxFlow/releases/tag/v2.1.1

## 🚀 手动上传步骤

### 方式 1: 网页浏览器（最简单）

1. **访问 Release 页面**
   - https://github.com/rejre/OxFlow/releases/tag/v2.1.1

2. **进入编辑模式**
   - 点击右上角的编辑按钮（铅笔图标）

3. **上传文件**
   - 在 Release 说明下方找到 "Attach binaries" 区域
   - 或者直接拖拽文件到该区域
   - 选择 `dist/OxFlow-2.1.1.dmg` 文件

4. **发布更新**
   - 点击 "Update release" 按钮
   - 完成！

### 方式 2: 命令行（if 网络恢复）

```bash
cd /Users/belfort/ai-workspace/oxflow-improvement

# 重新尝试上传
gh release upload v2.1.1 dist/OxFlow-2.1.1.dmg --clobber
```

### 方式 3: 替代分发

如果上传一直失败，可以：

1. **本地分享**
   - 文件位置: `dist/OxFlow-2.1.1.dmg`
   - 可以直接分享给用户

2. **从源代码构建**
   ```bash
   git clone https://github.com/rejre/OxFlow.git
   cd OxFlow
   pip install -r requirements.txt
   make dmg  # 生成 DMG
   ```

## 📊 上传进度

- ✅ Release 页面已创建
- ✅ 发行说明已添加（简洁版）
- ✅ 版本标签已创建 (v2.1.1)
- ✅ 源代码已推送
- ⏳ DMG 文件待上传

## 💡 为什么网络出现问题?

GitHub 的上传 API 有时会遇到连接重置问题，特别是在上传大文件（90MB）时。

**解决方案：**
1. 使用网页浏览器直接拖拽上传（最稳定）
2. 分块上传（见下方脚本）
3. 等待网络稳定后重试

## 🔧 分块上传脚本（可选）

```bash
#!/bin/bash
FILE="dist/OxFlow-2.1.1.dmg"
CHUNK_SIZE=$((10 * 1024 * 1024))  # 10 MB chunks

TOKEN=$(gh auth token)
RELEASE_ID=$(curl -s -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/rejre/OxFlow/releases/tags/v2.1.1" | \
  grep '"id":' | head -1 | grep -oE '[0-9]+')

echo "分块上传 $FILE..."
# 完整的分块上传逻辑（复杂，通常不需要）
```

## ✨ 总结

- Release 页面已全部准备好
- 发行说明已简化到位
- 只需上传 DMG 文件即可完成发布
- 推荐用网页浏览器直接拖拽上传
