---
任务编号: 任务-1
任务名称: 加入一个markdown生成html的脚本
---

## 任务描述

- 这个脚本可以把 content 下的 markdown 文件生成 html 文件.
- 这个脚本可以配置 markdown 文件的生成路径和 html 文件的生成路径.
- 生成的 html 脚本可以引入 css 文件, 引入 js 文件, 并且可以直接部署在 vercel 等站点上.
- css 默认应该看齐 `微信公众号` 的样式
- 我接受 python 和 nodejs 技术栈
- 要简洁的，不要用太多第三方库
- 最后给一个.sh脚本, 可以一键生成

## 实施要求

1. 先评估任务, 给我整体方案
2. 确认后实做
3. 如果后端有新增接口, 需要在 `backend/tests` 下 委托 `rest-tester` 创建接口测试脚本, 名字参考 `backend.{{path}}.{{subpath}}.http`
4. 完成后在此文档写入 `实施说明` 章节, 并记录`用户`的一些重要选择
5. 必要时更新 `DEPLOYMENT.md`, `README.md`

## 实施说明

### 实施日期

2026 年 3 月 26 日

### 用户选择

| 选项 | 选择 |
|------|------|
| 技术栈 | Python + markdown 库 |
| CSS 风格 | 微信公众号风格 |
| 依赖要求 | 简洁，仅使用 `markdown` 一个第三方库 |

### 实施内容

#### 1. 项目结构

```
美以伊战争/
├── scripts/
│   └── md2html.py          # 核心转换脚本
├── templates/
│   └── default.html        # HTML 模板
├── styles/
│   └── wechat.css          # 微信公众号风格 CSS
├── content/                # Markdown 源文件
├── public/                 # 生成的 HTML 输出
└── build.sh                # 一键构建脚本
```

#### 2. 文件说明

| 文件 | 说明 |
|------|------|
| `scripts/md2html.py` | Python 转换脚本，支持配置输入/输出目录、模板、CSS 路径 |
| `templates/default.html` | HTML 模板，使用 `{{ title }}`、`{{ content }}` 等占位符 |
| `styles/wechat.css` | 微信公众号风格样式，绿色主题、合适行距、代码块样式 |
| `build.sh` | 一键构建脚本，自动检查 Python 和依赖并执行转换 |

#### 3. 使用方法

```bash
# 一键构建
./build.sh

# 或直接用 Python 脚本（可配置参数）
python scripts/md2html.py -i content -o public
```

#### 4. 可配置参数

```
-i, --input     Markdown 输入目录 (默认：content)
-o, --output    HTML 输出目录 (默认：public)
-t, --template  HTML 模板路径 (默认：templates/default.html)
-c, --css       CSS 文件路径 (默认：styles/wechat.css)
```

#### 5. Vercel 部署

生成的 `public` 目录和 `styles` 目录可直接部署到 Vercel：
- `public/` 包含所有 HTML 文件
- `styles/` 包含 CSS 文件
- HTML 文件通过相对路径引用 CSS

#### 6. 依赖安装

```bash
pip install markdown
```
