---
任务编号: Task-4
任务名称: 自动发布
---

## 任务描述

给我一个简单脚本, 串联

1. 更新内容 -- 参考 update.sh
2. 生成 html -- 参考 build.sh
3. 完成发布 git commit + git push origin master

注意一定要在当前目录下运行, 因为我可能作为windows 开机任务/自动任务用.

## 实施要求

1. 先评估任务, 给我整体方案
2. 确认后实做
4. 完成后在此文档写入 `实施说明` 章节, 并记录`用户`的一些重要选择

## 实施说明

### 实施日期

2026 年 3 月 26 日

### 用户选择

| 选项 | 选择 |
|------|------|
| 脚本执行目录 | 脚本所在目录 (自动切换) |
| Windows 任务调度 | 支持 (脚本内自动处理目录) |

### 实施内容

#### 创建的脚本

**文件**: `publish.sh`

#### 脚本功能

1. **步骤 1 - 更新内容**: 执行 `update.sh` 调用 qwen 处理战报更新
2. **步骤 2 - 生成 HTML**: 执行 `build.sh` 将 Markdown 转换为 HTML
3. **步骤 3 - Git 发布**: 自动 `git add` + `commit` + `push origin master`

#### 关键特性

- ✅ 自动切换到脚本所在目录，支持 Windows 任务调度从任意位置调用
- ✅ 错误处理：任一步骤失败则停止执行
- ✅ 智能提交：无变更时自动跳过 commit
- ✅ 时间戳提交信息：格式为 `chore: 自动发布 - YYYY-MM-DD HH:MM:SS`

#### 使用方法

**手动执行**:
```bash
bash publish.sh
```

**Windows 任务计划程序**:
```
程序/脚本：bash
参数：D:\work\me\美以伊战争\publish.sh
起始目录：D:\work\me\美以伊战争
```

#### 依赖项

- Git Bash (Windows)
- 已配置的 Git 远程仓库 (origin)
- `update.sh` 和 `build.sh` 脚本
