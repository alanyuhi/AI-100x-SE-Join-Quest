# Makefile for AI-100x-SE-Join-Quest Project

.PHONY: help test behave pytest reports clean install

# 預設目標
help:
	@echo "可用的命令："
	@echo "  make install    - 安裝依賴"
	@echo "  make test       - 運行所有測試"
	@echo "  make behave     - 運行 Behave BDD 測試"
	@echo "  make pytest     - 運行 Pytest 單元測試"
	@echo "  make reports    - 生成所有測試報告"
	@echo "  make clean      - 清理緩存和報告文件"
	@echo "  make help       - 顯示此幫助信息"

# 安裝依賴
install:
	@echo "📦 安裝 Python 依賴..."
	pip install -r requirements.txt

# 運行所有測試
test: behave pytest
	@echo "✅ 所有測試完成"

# 運行 Behave BDD 測試
behave:
	@echo "🔄 運行 Behave BDD 測試..."
	behave --tags=~wip --format=pretty

# 運行 Pytest 單元測試
pytest:
	@echo "🔄 運行 Pytest 單元測試..."
	python -m pytest tests/ -v

# 生成所有報告
reports:
	@echo "📊 生成測試報告..."
	python scripts/generate_reports.py

# 生成 Behave 報告
behave-report:
	@echo "📊 生成 Behave 報告..."
	mkdir -p reports
	behave --format=html-pretty --outfile=reports/behave-report.html --tags=~wip

# 生成 Pytest 報告
pytest-report:
	@echo "📊 生成 Pytest 報告..."
	mkdir -p reports
	python -m pytest tests/ -v --html=reports/pytest-report.html --self-contained-html

# 生成覆蓋率報告
coverage-report:
	@echo "📊 生成覆蓋率報告..."
	mkdir -p reports/coverage
	python -m pytest tests/ --cov=src --cov-report=html:reports/coverage --cov-report=term-missing

# 清理文件
clean:
	@echo "🧹 清理緩存和報告文件..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf reports/*.html reports/*.log 2>/dev/null || true
	@echo "✅ 清理完成"

# 完整清理（包括虛擬環境）
clean-all: clean
	@echo "🧹 完整清理..."
	rm -rf venv/ 2>/dev/null || true
	rm -rf reports/ 2>/dev/null || true
	@echo "✅ 完整清理完成"

# 檢查代碼質量
lint:
	@echo "🔍 檢查代碼質量..."
	flake8 src/ tests/ --max-line-length=100 --ignore=E501,W503
	pylint src/ tests/ --disable=C0114,C0116

# 格式化代碼
format:
	@echo "🎨 格式化代碼..."
	black src/ tests/ --line-length=100
	isort src/ tests/

# 運行特定功能測試
test-chinese-chess:
	@echo "🎯 測試中國象棋功能..."
	behave features/chinesechess.feature --format=pretty

test-order:
	@echo "🎯 測試訂單功能..."
	behave features/order.feature --format=pretty

test-double11:
	@echo "🎯 測試雙十一功能..."
	behave features/double11.feature --format=pretty

# 開發模式：監視文件變化並自動運行測試
dev:
	@echo "👨‍💻 開發模式：監視文件變化..."
	@echo "按 Ctrl+C 停止"
	watchmedo auto-restart --patterns="*.py" --recursive -- python scripts/generate_reports.py 