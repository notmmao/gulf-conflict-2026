#!/bin/bash
# 自动发布脚本 - 更新内容 + 生成 HTML + Git 发布

set -e

# 获取脚本所在目录，确保在任何位置执行都能正确运行
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  自动发布脚本"
echo "  工作目录：$SCRIPT_DIR"
echo "========================================"
echo ""

# 检查 Git 状态
if ! git status &>/dev/null; then
    echo "❌ 错误：当前目录不是 Git 仓库"
    exit 1
fi

# ========================================
# 步骤 1: 更新内容
# ========================================
echo "📝 步骤 1/3: 更新内容..."
echo ""

if [ -f "$SCRIPT_DIR/update.sh" ]; then
    bash "$SCRIPT_DIR/update.sh"
    echo ""
    echo "✓ 内容更新完成"
else
    echo "⚠️  警告：未找到 update.sh，跳过内容更新"
fi

echo ""

# ========================================
# 步骤 2: 生成 HTML
# ========================================
echo "🔨 步骤 2/3: 生成 HTML..."
echo ""

if [ -f "$SCRIPT_DIR/build.sh" ]; then
    bash "$SCRIPT_DIR/build.sh"
    echo ""
    echo "✓ HTML 生成完成"
else
    echo "⚠️  警告：未找到 build.sh，跳过 HTML 生成"
fi

echo ""

# ========================================
# 步骤 3: Git 提交并发布
# ========================================
echo "🚀 步骤 3/3: Git 提交并发布..."
echo ""

# 检查是否有变更
git add -A
if git diff --staged --quiet; then
    echo "✓ 没有变更，跳过提交"
else
    # 生成提交信息
    COMMIT_MSG="chore: 自动发布 - $(date '+%Y-%m-%d %H:%M:%S')"
    
    echo "提交信息：$COMMIT_MSG"
    git commit -m "$COMMIT_MSG"
    
    echo ""
    echo "✓ 提交完成"
    
    # Push 到远程
    echo ""
    echo "正在推送到远程仓库..."
    git push origin master
    
    echo ""
    echo "✓ 发布完成"
fi

echo ""
echo "========================================"
echo "  🎉 自动发布全部完成!"
echo "========================================"
