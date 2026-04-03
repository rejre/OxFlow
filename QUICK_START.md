# OxFlow 快速开始指南

## 🎯 5 分钟快速上手

### 对于最终用户

#### 步骤 1: 安装
```bash
pip install oxflow
```

#### 步骤 2: 运行
```bash
oxflow
```

#### 步骤 3: 下载
1. 粘贴 YouTube/B站/直接链接
2. 选择质量
3. 点击下载

---

## 💻 对于开发者

### 快速环境设置（3 分钟）

```bash
# 1. 克隆项目
git clone https://github.com/rejre/OxFlow.git
cd OxFlow

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
make install-dev

# 4. 运行程序
make run
```

### 常用命令

```bash
# 运行所有检查 (必做)
make quality

# 运行单项检查
make test           # 运行测试
make lint           # 代码检查
make format         # 自动格式化

# 代码提交前
make quality        # 全面检查
git add .
git commit -m "描述您的改动"
git push
```

### 代码提交前检查清单

- [ ] `make quality` 全部通过
- [ ] 添加了相应的测试
- [ ] 更新了文档
- [ ] 提交信息清晰明了

---

## 📂 项目结构一览

```
OxFlow/
├── src/             # 源代码
│   ├── ui/         # 界面层
│   ├── core/       # 业务逻辑
│   └── utils/      # 工具模块
├── tests/          # 测试
├── docs/           # 文档
├── Makefile        # 开发命令
└── setup.py        # 包配置
```

---

## 🆘 遇到问题？

### 常见问题

**Q: 导入错误？**
```bash
# 重新安装依赖
pip install -r requirements-dev.txt
```

**Q: 测试失败？**
```bash
# 查看详细错误
pytest -v
```

**Q: 代码格式问题？**
```bash
# 自动修复
make format
```

---

## 📚 更多资源

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目概览 |
| [DOCUMENTATION.md](DOCUMENTATION.md) | 完整文档 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献指南 |
| [IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md) | 改善说明 |

---

## 🚀 下一步

1. 📖 阅读 [DOCUMENTATION.md](DOCUMENTATION.md) 了解详情
2. 💡 查看 [CONTRIBUTING.md](CONTRIBUTING.md) 学习贡献流程
3. 🔍 探索 `src/` 了解代码结构
4. ✍️ 编写测试和代码

---

**祝您开发愉快！🎉**
