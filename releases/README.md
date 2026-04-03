# OxFlow 历史版本

本目录用于存放和管理 OxFlow 的版本发布记录。

## 版本存储策略

### 保留版本
- **最新版本** (v2.1.1) - 在 `dist/` 目录
- **历史版本** - 通过 Git 标签保存

### 为什么不在仓库中存储 DMG？
1. **文件大小** - 每个 DMG 约 90 MB，会大幅增加仓库大小
2. **版本管理** - Git 不适合管理二进制文件版本控制
3. **发行管理** - GitHub Releases 更适合管理发行版本

## 获取历史版本

### 方法 1: 从 GitHub Releases 下载
访问：https://github.com/rejre/OxFlow/releases

### 方法 2: 重建历史版本
```bash
# 查看所有版本标签
git tag -l

# 检出指定版本
git checkout v2.1.0

# 构建该版本的 DMG
make dmg

# 返回最新版本
git checkout main
```

## 版本历史

| 版本 | 日期 | 发行链接 | 说明 |
|------|------|--------|------|
| v2.1.1 | 2024-04-04 | [GitHub](https://github.com/rejre/OxFlow/releases/tag/v2.1.1) | 最新：自动重试、断点续传 |
| v2.1.0 | 之前 | [GitHub](https://github.com/rejre/OxFlow/releases/tag/v2.1) | UI 改进 |
| v2.0 | 早期 | [GitHub](https://github.com/rejre/OxFlow/releases/tag/v2.0) | 基础功能 |

## 文件结构

```
releases/
├── README.md          ← 本文件
└── [历史版本 DMG]     ← 可选存放位置
```

注：实际的 DMG 文件保存在 GitHub Releases 中，不占用仓库空间。
