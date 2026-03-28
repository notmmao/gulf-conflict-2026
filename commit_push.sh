#!/bin/bash


# 检查是否有变更
git add -A
if git diff --staged --quiet; then
    echo "✓ 没有变更，跳过提交"
else
    # 生成提交信息
    COMMIT_MSG="chore: 手动发布 - $(date '+%Y-%m-%d %H:%M:%S')"
    
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
echo "更新地址: https://gulf-conflict-2026.notmmao.com/"
echo "========================================"
echo "  🎉 手动发布全部完成!"
echo "========================================"