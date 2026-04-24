#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 转 HTML 脚本
将 Markdown 文件转换为可部署的 HTML 文件
支持 daily 文件拼接生成战报
"""

import os
import re
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


def assemble_daily_files(daily_dir: Path) -> str:
    """
    拼接 daily 目录下所有文件，生成完整战报内容
    返回：拼接后的 Markdown 文本（含索引）
    """
    if not daily_dir.exists():
        return ""
    
    # 读取 header
    header_file = daily_dir / 'header.md'
    if header_file.exists():
        with open(header_file, 'r', encoding='utf-8') as f:
            header = f.read()
    else:
        header = "# 2026 年美以伊战争战报\n"
    
    # 读取所有 daily 文件并排序
    daily_files = sorted([
        f for f in daily_dir.glob('D*.md')
        if f.name.startswith('D') and f.name[1].isdigit()
    ])
    
    if not daily_files:
        return header
    
    # 拼接：header + 索引 + 所有 daily 内容
    parts = [header]
    
    for f in daily_files:
        with open(f, 'r', encoding='utf-8') as fh:
            parts.append(fh.read())
        parts.append('')  # 空行分隔
    
    return '\n'.join(parts)


def slugify(value: str, separator: str = '-') -> str:
    """将标题转换为无空格的 ID"""
    import html
    value = html.unescape(value)
    value = re.sub(r'\s+', separator, value.strip())
    value = re.sub(r'[^\w\u4e00-\u9fff\-]', '', value)
    return value.lower()


def fix_href_spaces(html_content: str) -> str:
    """修复 HTML 中所有 href 链接的空格问题"""
    def fix_href(match):
        href = match.group(1)
        if href.startswith('#'):
            fixed = re.sub(r'\s+', '-', href)
            return f'href="{fixed}"'
        return match.group(0)
    
    return re.sub(r'href="([^"]*)"', fix_href, html_content)


def generate_html(md_content: str, title: str, template: str, css_rel_path: str) -> str:
    """生成 HTML 内容"""
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
    html_content = fix_href_spaces(html_content)
    toc_html = md.toc

    html = template.replace('{{ title }}', title)
    html = html.replace('{{ content }}', html_content)
    html = html.replace('{{ toc }}', toc_html)
    html = html.replace('{{ css_path }}', css_rel_path)
    html = html.replace('{{ head_extra }}', '')
    html = html.replace('{{ js_extra }}', '')

    return html


def convert_file(md_file: Path, output_dir: Path, template: str, css_rel_path: str, content_dir: Path) -> None:
    """转换单个 Markdown 文件"""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 注入动态内容（仅对 index.md 处理）
    if md_file.name == 'index.md':
        md_content = inject_dynamic_content(md_content, content_dir)

    title = extract_title(md_content)
    html_content = generate_html(md_content, title, template, css_rel_path)

    relative_path = md_file.parent.relative_to(md_file.parent.parent / 'content')
    output_path = output_dir / relative_path / (md_file.stem + '.html')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ {md_file.name} -> {output_path.relative_to(output_dir.parent)}")


def convert_assembled(daily_dir: Path, output_dir: Path, template: str, css_rel_path: str) -> None:
    """将 daily 文件拼接后转换为战报 HTML"""
    print("\n📦 拼接 daily 文件...")
    assembled = assemble_daily_files(daily_dir)
    
    if not assembled:
        print("⚠ 无 daily 文件可拼接")
        return
    
    title = extract_title(assembled)
    html_content = generate_html(assembled, title, template, css_rel_path)
    
    # 输出为 战报.html
    output_path = output_dir / '美以伊战争 - 战报.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    daily_count = len(list(daily_dir.glob('D*.md')))
    print(f"✓ daily 拼接 ({daily_count} 个文件) -> {output_path.name}")
    print(f"  总大小：{len(assembled):,} chars -> {len(html_content):,} chars HTML")


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
    
    base_dir = Path(__file__).parent.parent
    input_dir = base_dir / args.input
    output_dir = base_dir / args.output
    template_path = base_dir / args.template
    css_path = base_dir / args.css
    
    if not input_dir.exists():
        print(f"错误：输入目录不存在：{input_dir}")
        exit(1)
    
    if not template_path.exists():
        print(f"错误：模板文件不存在：{template_path}")
        exit(1)
    
    if not css_path.exists():
        print(f"错误：CSS 文件不存在：{css_path}")
        exit(1)
    
    template = load_template(template_path)
    css_rel_path = './styles/wechat.css'
    
    print(f"\n📁 输入目录：{input_dir}")
    print(f"📁 输出目录：{output_dir}")
    print(f"📄 模板文件：{template_path}")
    print(f"🎨 CSS 文件：{css_path}")
    print()
    
    output_dir.mkdir(parents=True, exist_ok=True)

    # 复制 CSS
    output_css_dir = output_dir / 'styles'
    output_css_dir.mkdir(parents=True, exist_ok=True)
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    with open(output_css_dir / 'wechat.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"✓ CSS 已复制到 {output_css_dir / 'wechat.css'}")
    print()
    
    # 转换普通 Markdown 文件（跳过 daily 目录和旧的 战报.md）
    md_files = [
        f for f in input_dir.rglob('*.md')
        if 'AI' not in f.parts
        and 'daily' not in f.parts
        and f.name != '美以伊战争 - 战报.md'  # 旧文件，跳过
    ]

    if md_files:
        print(f"📝 转换 {len(md_files)} 个普通 Markdown 文件\n")
        for md_file in md_files:
            convert_file(md_file, output_dir, template, css_rel_path, input_dir)
    
    # 拼接 daily 文件生成战报
    daily_dir = input_dir / 'daily'
    if daily_dir.exists():
        print()
        convert_assembled(daily_dir, output_dir, template, css_rel_path)
    
    print(f"\n✅ 完成！")
    print(f"📂 输出位置：{output_dir}")


if __name__ == '__main__':
    main()
