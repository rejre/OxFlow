# OxFlow 版本管理说明

本文档说明如何在每次修复后更新版本、DMG 文件和说明文档。

---

## 📋 版本更新流程

### 1. 修改代码并测试

```bash
# 进行必要的代码修改
# 运行测试确保没有破坏
make test

# 代码质量检查
make quality
```

### 2. 更新版本号

**修改以下文件：**

#### a) README.md
```markdown
# OxFlow — 变色牛万能下载器 (vX.Y.Z)

> 💡 **vX.Y.Z 新版本：** [新增功能描述]
```

#### b) CHANGELOG.md
在顶部添加新版本条目：
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- 新增功能 1
- 新增功能 2

### Fixed
- 修复问题 1
- 修复问题 2

### Changed
- 改进 1
- 改进 2
```

#### c) 应用版本（如果有）
搜索代码中的版本号字符串并更新

### 3. 构建新的 DMG 文件

```bash
# 进入项目目录
cd /Users/belfort/ai-workspace/oxflow-improvement

# 激活虚拟环境
source venv/bin/activate

# 构建 DMG
make dmg

# 验证 DMG 大小
ls -lh dist/OxFlow-*.dmg
```

### 4. 重命名并保存 DMG 文件

```bash
# 保留旧版本（可选）
mkdir -p releases
cp dist/OxFlow-2.1.0.dmg releases/OxFlow-2.1.0.dmg 2>/dev/null || true

# 新 DMG 文件应该自动生成为正确的版本号
# 示例：dist/OxFlow-2.1.1.dmg
```

### 5. 提交代码更改

```bash
# 添加所有修改
git add -A

# 提交（使用语义化提交信息）
git commit -m "feat: [功能描述] (vX.Y.Z)

详细说明...

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# 或修复提交
git commit -m "fix: [修复说明] (vX.Y.Z)

详细说明...

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

**常见提交类型：**
- `feat:` - 新功能
- `fix:` - 修复
- `docs:` - 文档
- `style:` - 格式（不影响代码逻辑）
- `refactor:` - 重构
- `perf:` - 性能优化
- `test:` - 测试

### 6. 创建版本标签

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z: [描述]

Features:
- 功能1
- 功能2

Improvements:
- 改进1
- 改进2

Download: dist/OxFlow-X.Y.Z.dmg (XYZ MB)"
```

### 7. 推送到 GitHub

```bash
# 推送提交
git push origin main

# 推送标签
git push origin vX.Y.Z

# 查看最新的提交和标签
git log --oneline -3
git tag -l -n5
```

### 8. 创建 GitHub Release

访问：https://github.com/rejre/OxFlow/releases

1. 点击 "Draft a new release"
2. 选择刚创建的标签 (vX.Y.Z)
3. 填写发行说明（可参考 RELEASES.md）
4. 上传 DMG 文件作为二进制资源
5. 发布 Release

---

## 📊 版本号管理

### 语义版本规则

```
vMAJOR.MINOR.PATCH
 │      │      └── 错误修复、补丁（向后兼容）
 │      └────────── 新功能、向后兼容
 └───────────────── 大版本、可能不兼容
```

**示例：**
- v2.0.0 → v2.1.0 (新功能，向后兼容)
- v2.1.0 → v2.1.1 (修复，向后兼容)
- v2.1.1 → v3.0.0 (重大改动，可能不兼容)

### 版本号决策

| 变更类型 | 新增测试 | 新功能 | 破坏性改动 | 版本增量 |
|---------|--------|--------|----------|---------|
| Bug 修复 | - | ❌ | ❌ | PATCH |
| 新功能 | ✅ | ✅ | ❌ | MINOR |
| 重构 | ✅ | ❌ | ✅ | MAJOR |

---

## 📦 DMG 文件管理

### 命名规范

```
OxFlow-X.Y.Z.dmg
```

**示例：**
- OxFlow-2.1.1.dmg ✅ 正确
- OxFlow_2.1.1.dmg ❌ 错误
- OxFlow-Latest.dmg ❌ 错误

### 文件位置

```
/Users/belfort/ai-workspace/oxflow-improvement/
├── dist/
│   ├── OxFlow-2.1.1.dmg     ← 最新版本
│   └── OxFlow.app           ← 应用包（临时）
├── releases/
│   ├── OxFlow-2.1.0.dmg     ← 归档版本（可选）
│   └── OxFlow-2.0.dmg       ← 归档版本（可选）
```

### 保留策略

**保留方式：**

1. **最新 3 个版本** - 保留在 dist/ 目录
2. **历史版本** - 通过 Git 标签保存（可随时重建）
3. **发行页面** - GitHub Releases 中有所有版本下载链接

**不需要：**
- 在仓库中存储多个 DMG 文件（太大）
- 手动维护版本列表（GitHub Releases 自动管理）

### 重建历史版本

如需重新构建旧版本的 DMG：

```bash
# 1. 检出旧版本
git checkout v2.1.0

# 2. 构建 DMG
make dmg

# 3. 返回最新版本
git checkout main
```

---

## 📄 文档更新清单

每个版本发布时，更新以下文件：

- [ ] **README.md** - 更新版本号和新增功能
- [ ] **CHANGELOG.md** - 添加版本条目
- [ ] **RELEASES.md** - 添加发行说明
- [ ] **DMG_RELEASE_NOTES.md** - 用户使用说明（可选）
- [ ] **VERSION_MANAGEMENT.md** - 本文档（如需）

---

## 🔍 验证清单

发布前检查：

```bash
# 1. 代码质量
make quality      # ✅ 通过

# 2. 测试
make test        # ✅ 通过

# 3. DMG 构建
make dmg         # ✅ 成功

# 4. Git 历史
git log --oneline -5  # ✅ 正确

# 5. 标签
git tag -l       # ✅ 新标签存在

# 6. 远程状态
git push origin main  # ✅ 成功
git push origin vX.Y.Z  # ✅ 成功
```

---

## 🎯 完整发布流程示例

### 场景：修复下载稳定性，发布 v2.1.1

```bash
# 1. 修改代码
vim src/core/downloader.py

# 2. 运行测试
make test

# 3. 更新版本号
vim README.md          # 更新版本号和新增功能
vim CHANGELOG.md       # 添加版本条目

# 4. 构建 DMG
make dmg               # 生成 OxFlow-2.1.1.dmg

# 5. 提交
git add -A
git commit -m "feat: Add download retry and resume (v2.1.1)
...
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# 6. 创建标签
git tag -a v2.1.1 -m "Release v2.1.1: ..."

# 7. 推送
git push origin main
git push origin v2.1.1

# 8. 创建 GitHub Release
# 浏览器访问：https://github.com/rejre/OxFlow/releases
# 上传 dist/OxFlow-2.1.1.dmg
# 填写发行说明
# 发布
```

---

## 📞 常见问题

### Q: 如何回滚到旧版本？

```bash
# 查看可用的版本标签
git tag -l

# 检出旧版本
git checkout v2.1.0

# 重新构建 DMG
make dmg
```

### Q: 如何更新依赖版本？

```bash
# 编辑 requirements.txt 或 requirements-dev.txt
vim requirements.txt

# 安装更新的依赖
pip install -r requirements.txt --upgrade

# 运行测试验证
make test

# 提交更新
git add requirements.txt
git commit -m "deps: Update dependencies"
```

### Q: DMG 文件太大怎么办？

DMG 大小正常（~90 MB）。这是因为：
- 包含完整 Python 运行时
- 捆绑所有依赖库
- 包含国际化资源

可通过以下方式优化（高级）：
```bash
# 编辑构建脚本减少依赖
vim scripts/build_dmg.sh

# 调整 hdiutil 压缩参数
hdiutil create ... -format UDZO ...  # 改为 UDBZ (更高压缩率)
```

### Q: 版本不匹配怎么办？

如果 DMG 和代码版本不匹配：

```bash
# 重新构建匹配的 DMG
rm dist/OxFlow*.dmg
make dmg

# 验证生成的 DMG 名称
ls -lh dist/
```

---

## 总结

✅ 遵循语义版本控制  
✅ 使用 Git 标签管理版本  
✅ 通过 GitHub Releases 分发  
✅ 保持文档同步更新  
✅ 清晰的版本历史和升级路径
