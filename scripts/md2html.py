#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 转 HTML 脚本
将 Markdown 文件转换为可部署的 HTML 文件
"""

import os
import argparse
from pathlib import Path

try:
    import markdown
except ImportError:
    print("错误：请先安装 markdown 库：pip install markdown")
    exit(1)


def load_template(template_path: str) -> str:
    """加载 HTML 模板"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_title(md_content: str) -> str:
    """从 Markdown 内容中提取标题"""
    for line in md_content.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    return "未命名文档"


def inject_dynamic_content(md_content: str, content_dir: Path) -> str:
    """
    注入动态内容
    支持语法：<!-- include: filename.md -->
    """
    import re
    
    pattern = r'<!-- include:\s*(\S+\.md)\s*-->'
    
    def replace_include(match):
        filename = match.group(1)
        file_path = content_dir / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f'<!-- 文件不存在：{filename} -->'
    
    return re.sub(pattern, replace_include, md_content)


def slugify(value: str, separator: str = '-') -> str:
    """将标题转换为无空格的 ID"""
    import html
    import re
    # 先解码 HTML 实体
    value = html.unescape(value)
    # 移除空格，用连字符替换
    value = re.sub(r'\s+', separator, value.strip())
    # 只保留字母、数字、连字符、下划线和中文
    value = re.sub(r'[^\w\u4e00-\u9fff\-]', '', value)
    return value.lower()


def fix_href_spaces(html_content: str) -> str:
    """修复 HTML 中所有 href 链接的空格问题"""
    import re
    
    def fix_href(match):
        href = match.group(1)
        # 只处理锚点链接
        if href.startswith('#'):
            # 将 href 中的空格替换为连字符
            fixed = re.sub(r'\s+', '-', href)
            return f'href="{fixed}"'
        return match.group(0)
    
    return re.sub(r'href="([^"]*)"', fix_href, html_content)


def generate_html(md_content: str, title: str, template: str, css_rel_path: str) -> str:
    """生成 HTML 内容"""
    # 配置 Markdown 扩展
    md = markdown.Markdown(extensions=[
        'toc',
        'tables',
        'fenced_code',
        'nl2br',
    ], extension_configs={
        'toc': {
            'permalink': False,
            'separator': '-',
            'slugify': slugify,
        }
    })

    html_content = md.convert(md_content)
    
    # 后处理：修复所有 href 中的空格
    html_content = fix_href_spaces(html_content)

    # 获取生成的目录 HTML
    toc_html = md.toc

    # 替换模板占位符
    html = template.replace('{{ title }}', title)
    html = html.replace('{{ content }}', html_content)
    html = html.replace('{{ toc }}', toc_html)
    html = html.replace('{{ css_path }}', css_rel_path)
    html = html.replace('{{ head_extra }}', '')
    html = html.replace('{{ js_extra }}', '')

    return html


def calculate_css_rel_path(output_path: Path) -> str:
    """计算 CSS 文件的相对路径"""
    # 默认 CSS 在 ../styles/wechat.css
    depth = len(output_path.relative_to(output_path.parent).parts)
    return '../styles/wechat.css'


def convert_file(md_file: Path, output_dir: Path, template: str, css_rel_path: str, content_dir: Path) -> None:
    """转换单个 Markdown 文件"""
    # 读取 Markdown 内容
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 注入动态内容（仅对 index.md 处理）
    if md_file.name == 'index.md':
        md_content = inject_dynamic_content(md_content, content_dir)

    # 提取标题
    title = extract_title(md_content)

    # 生成 HTML
    html_content = generate_html(md_content, title, template, css_rel_path)

    # 确定输出路径
    relative_path = md_file.parent.relative_to(md_file.parent.parent / 'content')
    output_path = output_dir / relative_path / (md_file.stem + '.html')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入 HTML 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ {md_file.name} -> {output_path.relative_to(output_dir.parent)}")


def main():
    parser = argparse.ArgumentParser(description='Markdown 转 HTML 转换器')
    parser.add_argument('--input', '-i', default='content',
                        help='Markdown 文件输入目录 (默认：content)')
    parser.add_argument('--output', '-o', default='public',
                        help='HTML 文件输出目录 (默认：public)')
    parser.add_argument('--template', '-t', default='templates/default.html',
                        help='HTML 模板路径 (默认：templates/default.html)')
    parser.add_argument('--css', '-c', default='public/styles/wechat.css',
                        help='CSS 文件路径 (默认：public/styles/wechat.css)')
    
    args = parser.parse_args()
    
    # 路径处理
    base_dir = Path(__file__).parent.parent
    input_dir = base_dir / args.input
    output_dir = base_dir / args.output
    template_path = base_dir / args.template
    css_path = base_dir / args.css
    
    # 验证路径
    if not input_dir.exists():
        print(f"错误：输入目录不存在：{input_dir}")
        exit(1)
    
    if not template_path.exists():
        print(f"错误：模板文件不存在：{template_path}")
        exit(1)
    
    if not css_path.exists():
        print(f"错误：CSS 文件不存在：{css_path}")
        exit(1)
    
    # 加载模板
    template = load_template(template_path)

    # 计算 CSS 相对路径 (从 public 到 styles)
    # CSS 在 public/styles/wechat.css，所以相对路径是 ./styles/wechat.css
    css_rel_path = './styles/wechat.css'
    
    print(f"\n📁 输入目录：{input_dir}")
    print(f"📁 输出目录：{output_dir}")
    print(f"📄 模板文件：{template_path}")
    print(f"🎨 CSS 文件：{css_path}")
    print()
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 复制 CSS 到输出目录 (public/styles)
    output_css_dir = output_dir / 'styles'
    output_css_dir.mkdir(parents=True, exist_ok=True)
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    with open(output_css_dir / 'wechat.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"✓ CSS 已复制到 {output_css_dir / 'wechat.css'}")
    print()
    
    # 查找并转换所有 Markdown 文件
    md_files = list(input_dir.rglob('*.md'))

    if not md_files:
        print("⚠ 未找到 Markdown 文件")
        return

    print(f"📝 找到 {len(md_files)} 个 Markdown 文件\n")

    for md_file in md_files:
        # 跳过 AI 目录
        if 'AI' in md_file.parts:
            continue
        convert_file(md_file, output_dir, template, css_rel_path, input_dir)
    
    print(f"\n✅ 完成！共转换 {len(md_files)} 个文件")
    print(f"📂 输出位置：{output_dir}")


if __name__ == '__main__':
    main()
