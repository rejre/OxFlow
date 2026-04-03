# OxFlow - 发布说明和改进日志

## 🎉 v2.1 改进概览

本版本着重于提高代码质量、可维护性和用户体验。

### ✨ 新增功能

- ✅ 完整的测试框架和测试套件
- ✅ 自动化 CI/CD 流程 (GitHub Actions)
- ✅ 代码质量检查 (linting, formatting, type checking)
- ✅ 改进的日志系统和错误处理
- ✅ 完整的项目文档

### 🔧 改进

- ✅ 依赖版本锁定，确保一致性
- ✅ 更好的错误消息和异常处理
- ✅ 日志轮转机制，防止日志文件无限增长
- ✅ 更详细的注释和类型提示
- ✅ 改进的 .gitignore 和项目配置

### 📚 文档

- ✅ [DOCUMENTATION.md](DOCUMENTATION.md) - 完整的项目文档
- ✅ [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- ✅ [LICENSE](LICENSE) - MIT 许可证

## 项目结构改进

```
OxFlow/
├── src/
│   ├── ui/
│   │   └── main_window.py
│   ├── core/
│   │   └── downloader.py
│   └── utils/
│       ├── config.py
│       ├── i18n.py
│       ├── logging_config.py        # 新增：日志管理
│       └── exceptions.py            # 新增：异常处理
├── tests/                           # 新增：测试套件
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_downloader.py
│   └── test_i18n.py
├── .github/
│   └── workflows/
│       └── tests.yml                # 新增：CI/CD 工作流
├── .pre-commit-config.yaml          # 新增：Pre-commit 配置
├── pyproject.toml                   # 新增：项目配置
├── setup.py                         # 新增：包配置
├── requirements.txt                 # 已更新：版本锁定
├── requirements-dev.txt             # 新增：开发依赖
├── LICENSE                          # 新增
├── CONTRIBUTING.md                  # 新增
├── DOCUMENTATION.md                 # 新增
└── README.md
```

## 使用指南

### 安装

```bash
# pip 安装
pip install oxflow

# 或从源代码安装
git clone https://github.com/rejre/OxFlow.git
cd OxFlow
pip install -r requirements.txt
python src/ui/main_window.py
```

### 开发环境

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 安装 pre-commit 钩子
pre-commit install

# 运行测试
pytest

# 代码质量检查
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

### 贡献代码

请参考 [CONTRIBUTING.md](CONTRIBUTING.md)

## 质量指标

- ✅ **代码覆盖率**: >80% (目标)
- ✅ **Python 版本**: 3.10+
- ✅ **跨平台**: macOS, Windows, Linux
- ✅ **CI/CD**: GitHub Actions (Python 3.10, 3.11, 3.12)

## 下一步计划

- [ ] 增加更多单元测试
- [ ] CLI 版本开发
- [ ] 字幕下载支持
- [ ] 性能优化
- [ ] 国际化改进
- [ ] 插件系统

## 常见问题

**Q: 如何升级 OxFlow？**

A: 
```bash
pip install --upgrade oxflow
```

**Q: 我发现了 Bug，应该怎么做？**

A: 请在 [GitHub Issues](https://github.com/rejre/OxFlow/issues) 上报告。

**Q: 我想贡献代码，怎样开始？**

A: 请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 开发指南。

## 致谢

感谢所有贡献者和用户的支持！

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

**最后更新**: 2024-04-03
