# Contributing to OxFlow

首先感谢您对 OxFlow 的兴趣！我们欢迎各种形式的贡献。

## 开发环境设置

### 1. 克隆仓库
```bash
git clone https://github.com/rejre/OxFlow.git
cd OxFlow
```

### 2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements-dev.txt
```

### 4. 安装 Pre-commit 钩子
```bash
pre-commit install
```

## 代码风格

我们使用以下工具维护代码质量：

- **Black**: 代码格式化
  ```bash
  black src/
  ```

- **isort**: Import 排序
  ```bash
  isort src/
  ```

- **Flake8**: 代码检查
  ```bash
  flake8 src/
  ```

- **mypy**: 类型检查
  ```bash
  mypy src/
  ```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行单个测试文件
pytest tests/test_downloader.py

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

## 提交代码

1. 创建新分支：`git checkout -b feature/your-feature`
2. 进行代码修改并编写测试
3. 运行 `black`, `isort`, `flake8` 检查代码
4. 运行测试确保通过：`pytest`
5. 提交并推送：`git push origin feature/your-feature`
6. 创建 Pull Request

## Pull Request 指南

- 描述 PR 的目的和改动
- 关联相关的 Issue
- 确保所有测试通过
- 添加必要的文档更新

## 报告 Bug

创建 Issue 时，请包含：

- 系统信息（OS、Python 版本）
- 错误堆栈跟踪
- 复现步骤
- 预期行为 vs 实际行为

## 代码审查

所有提交都需要经过代码审查。我们会：

- 检查代码质量
- 验证测试覆盖率
- 确保符合项目标准

感谢您的贡献！🎉
