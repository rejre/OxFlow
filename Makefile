.PHONY: help install install-dev test lint format type-check clean build run pre-commit-install dmg

help:
	@echo "OxFlow - 开发命令"
	@echo "===================="
	@echo ""
	@echo "安装和依赖:"
	@echo "  make install           - 安装生产依赖"
	@echo "  make install-dev       - 安装开发依赖"
	@echo ""
	@echo "代码质量:"
	@echo "  make lint              - 运行代码检查 (flake8)"
	@echo "  make format            - 自动格式化代码 (black, isort)"
	@echo "  make type-check        - 类型检查 (mypy)"
	@echo "  make test              - 运行单元测试"
	@echo "  make test-cov          - 运行测试并生成覆盖率报告"
	@echo "  make quality           - 运行所有质量检查"
	@echo ""
	@echo "项目操作:"
	@echo "  make run               - 运行 OxFlow"
	@echo "  make build             - 构建发布包"
	@echo "  make dmg               - 构建 macOS DMG 安装文件"
	@echo "  make clean             - 清理构建文件"
	@echo "  make pre-commit-install - 安装 pre-commit 钩子"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest -v

test-cov:
	pytest --cov=src --cov-report=term-missing --cov-report=html

lint:
	flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/ --ignore-missing-imports || true

quality: lint type-check test
	@echo "✅ 所有质量检查完成！"

run:
	python src/ui/main_window.py

build: clean
	python -m pip install --upgrade build
	python -m build
	@echo "✅ 构建完成！"

dmg:
	chmod +x scripts/build_dmg.sh
	bash scripts/build_dmg.sh

clean:
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/ htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ 清理完成！"

pre-commit-install:
	pre-commit install
	@echo "✅ Pre-commit 钩子已安装！"

# 开发者快速命令
dev: install-dev pre-commit-install
	@echo "✅ 开发环境已设置！"

check: quality
	@echo "✅ 所有检查通过！"
