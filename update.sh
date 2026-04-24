#!/bin/bash
# 更新战报内容
# 使用 qwen 读取提示词并执行搜索更新

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

qwen -p @content/战报更新.md -y