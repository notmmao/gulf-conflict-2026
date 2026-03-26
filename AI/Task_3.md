---
任务编号: Task-3
任务名称: 发布到Vercel
---

## 任务描述

- 我有 vercel 账号, 如果我要发布是不是必须要建立了github仓库?
- 目前我的 public 和 styles 文件夹都需要发布, 是否放在一起(相同父目录)会比较好? 
- 给我必要的配置文件, 例如 vercel.json

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
| 目录结构 | 移动到 public/styles |
| GitHub 仓库 | 已创建，请给我配置 |

### 实施内容

#### 1. 目录结构调整

- 将 `styles/` 移动到 `public/styles/`
- 所有静态资源统一在 `public` 目录下，便于 Vercel 部署

#### 2. 创建 vercel.json 配置

```json
{
  "buildCommand": "bash build.sh",
  "outputDirectory": "public",
  "installCommand": "echo 'No dependencies to install'"
}
```

#### 3. 更新 CSS 路径引用

- `public/index.html`: `../styles/wechat.css` → `styles/wechat.css`
- `scripts/md2html.py`: CSS 输出路径和相对路径已更新

#### 4. 部署步骤

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "配置 Vercel 部署"
   git push
   ```

2. **在 Vercel 导入项目**
   - 登录 Vercel (vercel.com)
   - 点击 "Add New Project"
   - 选择你的 GitHub 仓库
   - 导入并部署

3. **后续更新**
   - 每次 push 代码后，Vercel 自动构建和部署
   - 本地运行 `build.sh` 可测试构建
