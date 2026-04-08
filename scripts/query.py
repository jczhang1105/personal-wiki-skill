#!/usr/bin/env python3
"""
知识库查询脚本
功能：搜索 Wiki → 读取页面 → 综合回答
用法：python query.py "{问题}"
"""

import sys
import re
from pathlib import Path

def read_index(wiki_path):
    """读取索引文件"""
    index_file = wiki_path / "index.md"
    if not index_file.exists():
        return []
    
    content = index_file.read_text(encoding="utf-8")
    return parse_index(content)

def parse_index(content):
    """解析索引，提取页面信息"""
    items = []
    
    # 提取表格中的页面
    table_pattern = r'\| \[([^\]]+)\]\(([^)]+)\) \| ([^|]+) \| ([^|]+) \|'
    matches = re.findall(table_pattern, content)
    
    for title, path, type_, date in matches:
        items.append({
            "title": title,
            "path": path.replace("wiki/", ""),
            "type": type_.strip(),
            "date": date.strip()
        })
    
    # 提取链接格式的页面
    link_pattern = r'- \[\[([^\]]+)\]\] - (.+)'
    matches = re.findall(link_pattern, content)
    
    for title, desc in matches:
        items.append({
            "title": title,
            "path": f"topics/{title}.md",
            "type": "topic",
            "desc": desc.strip()
        })
    
    return items

def search_index(items, query, top_k=5):
    """搜索索引，返回相关页面"""
    query_lower = query.lower()
    
    # 简单的相关性评分
    scored = []
    for item in items:
        score = 0
        title_lower = item["title"].lower()
        desc_lower = item.get("desc", "").lower()
        type_lower = item.get("type", "").lower()
        
        # 标题匹配
        if query_lower in title_lower:
            score += 10
        
        # 描述匹配
        if query_lower in desc_lower:
            score += 5
        
        # 类型匹配
        if query_lower in type_lower:
            score += 3
        
        # 关键词匹配
        query_words = query_lower.split()
        for word in query_words:
            if word in title_lower:
                score += 2
            if word in desc_lower:
                score += 1
        
        if score > 0:
            scored.append((score, item))
    
    # 按分数排序
    scored.sort(reverse=True, key=lambda x: x[0])
    return [item for score, item in scored[:top_k]]

def read_page(wiki_path, page_path):
    """读取页面内容"""
    full_path = wiki_path / page_path
    if not full_path.exists():
        return None
    
    content = full_path.read_text(encoding="utf-8")
    
    # 提取核心内容
    sections = extract_sections(content)
    return {
        "title": extract_title(content),
        "content": content,
        "sections": sections,
        "core_points": sections.get("核心观点", [])
    }

def extract_title(content):
    """提取标题"""
    match = re.search(r'^# (.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "Unknown"

def extract_sections(content):
    """提取章节"""
    sections = {}
    current_section = "简介"
    current_content = []
    
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_content:
                sections[current_section] = current_content
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_content:
        sections[current_section] = current_content
    
    return sections

def synthesize_answer(query, pages):
    """综合多个页面生成答案"""
    if not pages:
        return "抱歉，知识库中没有找到相关内容。"
    
    # 构建答案
    answer = f"根据知识库中的 {len(pages)} 篇相关内容：\n\n"
    
    # 提取关键信息
    all_points = []
    sources = []
    
    for page in pages:
        title = page["title"]
        sources.append(title)
        
        # 提取核心观点
        if page.get("core_points"):
            for point in page["core_points"]:
                all_points.append(f"- {point} (来源：{title})")
    
    # 组织答案
    if all_points:
        answer += "📌 **核心要点**:\n"
        answer += "\n".join(all_points)
        answer += "\n\n"
    
    # 添加详细内容
    answer += "📖 **详细内容**:\n"
    for page in pages:
        title = page["title"]
        content = page["content"][:500]  # 限制长度
        answer += f"\n### {title}\n{content}...\n"
    
    # 添加来源
    answer += "\n\n📚 **来源**:\n"
    for source in sources:
        answer += f"- [[{source}]]\n"
    
    return answer

def main():
    if len(sys.argv) < 2:
        print("用法：python query.py \"{问题}\"")
        print("示例：python query.py \"Karpathy 的知识库方法是什么？\"")
        sys.exit(1)
    
    query = sys.argv[1]
    wiki_path = Path.cwd() / "wiki"
    
    if not wiki_path.exists():
        # 尝试父目录
        wiki_path = Path.cwd().parent / "wiki"
    
    print(f"🔍 搜索：{query}")
    print("=" * 50)
    
    # 1. 搜索索引
    index_items = read_index(wiki_path)
    relevant = search_index(index_items, query, top_k=5)
    
    if not relevant:
        print("❌ 未找到相关内容")
        sys.exit(0)
    
    print(f"✅ 找到 {len(relevant)} 篇相关页面\n")
    
    # 2. 读取页面
    pages = []
    for item in relevant:
        page = read_page(wiki_path, item["path"])
        if page:
            pages.append(page)
            print(f"- {page['title']}")
    
    # 3. 生成答案
    print("\n" + "=" * 50)
    answer = synthesize_answer(query, pages)
    print(answer)

if __name__ == "__main__":
    main()
