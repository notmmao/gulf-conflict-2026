#!/bin/bash
# Markdown 转 HTML 一键构建脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo "  Markdown 转 HTML 构建工具"
echo "========================================"
echo ""

# 检查 Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ 错误：未找到 Python，请先安装 Python"
    exit 1
fi

echo "✓ Python 版本：$($PYTHON_CMD --version)"

# 检查 markdown 库
if ! $PYTHON_CMD -c "import markdown" 2>/dev/null; then
    echo ""
    echo "📦 正在安装 markdown 库..."
    pip3 install markdown || pip install markdown
fi

echo "✓ markdown 库已安装"
echo ""

# 执行转换
$PYTHON_CMD "$SCRIPT_DIR/scripts/md2html.py"

echo ""
echo "========================================"
echo "  构建完成!"
echo "========================================"
