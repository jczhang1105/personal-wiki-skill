#!/usr/bin/env python3
"""
知识库健康检查脚本
功能：扫描 Wiki → 发现问题 → 生成报告
用法：python lint.py [--auto-fix]
"""

import sys
import re
from pathlib import Path
from datetime import datetime

def scan_wiki(wiki_path):
    """扫描所有 Wiki 页面"""
    pages = {
        "topics": [],
        "sources": [],
        "concepts": []
    }
    
    # 扫描 topics
    topics_dir = wiki_path / "topics"
    if topics_dir.exists():
        for f in topics_dir.glob("*.md"):
            pages["topics"].append(parse_page(f))
    
    # 扫描 sources
    sources_dir = wiki_path / "sources"
    if sources_dir.exists():
        for f in sources_dir.glob("*.md"):
            pages["sources"].append(parse_page(f))
    
    # 扫描 concepts
    concepts_dir = wiki_path / "concepts"
    if concepts_dir.exists():
        for f in concepts_dir.glob("*.md"):
            pages["concepts"].append(parse_page(f))
    
    return pages

def parse_page(file_path):
    """解析页面，提取元数据"""
    content = file_path.read_text(encoding="utf-8")
    
    return {
        "path": str(file_path),
        "title": extract_title(content),
        "content": content,
        "links": extract_links(content),
        "tags": extract_tags(content),
        "priority": extract_priority(content),
        "date": file_path.stat().st_mtime
    }

def extract_title(content):
    """提取标题"""
    match = re.search(r'^# (.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "Unknown"

def extract_links(content):
    """提取维基链接"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)

def extract_tags(content):
    """提取标签"""
    pattern = r'#([a-zA-Z0-9_-]+)'
    return re.findall(pattern, content)

def extract_priority(content):
    """提取优先级"""
    match = re.search(r'优先级 [::]\s*P([0-3])', content)
    return match.group(1) if match else None

def find_orphan_pages(pages):
    """查找孤立页面（无入链）"""
    # 收集所有链接
    all_links = set()
    for category, page_list in pages.items():
        for page in page_list:
            all_links.update(page["links"])
    
    # 查找孤立页面
    orphans = []
    for category, page_list in pages.items():
        for page in page_list:
            title = page["title"]
            if title not in all_links and title != "Index":
                orphans.append({
                    "title": title,
                    "path": page["path"],
                    "category": category
                })
    
    return orphans

def find_missing_concepts(pages):
    """查找缺失的概念页"""
    # 收集所有提到的概念
    mentioned = set()
    for category, page_list in pages.items():
        for page in page_list:
            # 从内容中提取潜在概念
            content = page["content"]
            # 查找加粗的术语
            bold_terms = re.findall(r'\*\*([^*]+)\*\*', content)
            for term in bold_terms:
                if len(term) < 50:  # 排除长文本
                    mentioned.add(term)
    
    # 检查是否有对应的概念页
    existing_concepts = {p["title"] for p in pages["concepts"]}
    missing = mentioned - existing_concepts
    
    # 过滤掉常见词汇
    common_words = {"核心观点", "详细内容", "来源", "行动项", "关联"}
    missing = missing - common_words
    
    return list(missing)[:10]  # 返回最多 10 个

def find_contradictions(pages):
    """查找可能的矛盾内容"""
    contradictions = []
    
    # 简单实现：查找相同术语的不同定义
    definitions = {}
    for category, page_list in pages.items():
        for page in page_list:
            content = page["content"]
            # 查找定义模式
            defs = re.findall(r'(\w+)[：:](.+?)(?:\.|。)', content)
            for term, definition in defs:
                if term in definitions:
                    if definitions[term] != definition:
                        contradictions.append({
                            "term": term,
                            "definition1": definitions[term],
                            "definition2": definition,
                            "page": page["title"]
                        })
                else:
                    definitions[term] = definition
    
    return contradictions

def find_outdated_info(pages):
    """查找可能过时的信息"""
    outdated = []
    
    now = datetime.now().timestamp()
    six_months_ago = now - (6 * 30 * 24 * 60 * 60)
    
    for category, page_list in pages.items():
        for page in page_list:
            if page["date"] < six_months_ago:
                outdated.append({
                    "title": page["title"],
                    "path": page["path"],
                    "category": category,
                    "age_days": int((now - page["date"]) / (24 * 60 * 60))
                })
    
    return outdated

def find_missing_refs(pages):
    """查找缺失的交叉引用"""
    missing_refs = []
    
    for category, page_list in pages.items():
        for page in page_list:
            links = page["links"]
            # 如果页面没有引用其他页面
            if len(links) == 0 and category == "sources":
                missing_refs.append({
                    "title": page["title"],
                    "path": page["path"],
                    "suggestion": "添加相关主题链接"
                })
    
    return missing_refs

def generate_report(issues):
    """生成健康检查报告"""
    report = "📊 Wiki 健康报告\n"
    report += "=" * 50 + "\n\n"
    
    # ✅ 好的方面
    report += "✅ **好的方面**:\n"
    total_pages = sum(len(pages) for pages in issues["pages"].values())
    report += f"- 总页面数：{total_pages} 篇\n"
    report += f"- 来源页：{len(issues['pages']['sources'])} 篇\n"
    report += f"- 主题页：{len(issues['pages']['topics'])} 篇\n"
    report += f"- 概念页：{len(issues['pages']['concepts'])} 篇\n\n"
    
    # ⚠️ 需要修复
    report += "⚠️ **需要修复**:\n"
    
    if issues["orphans"]:
        report += f"- {len(issues['orphans'])} 个孤立页面（无入链）\n"
        for orphan in issues["orphans"][:5]:
            report += f"  - {orphan['title']} ({orphan['category']})\n"
    
    if issues["missing_concepts"]:
        report += f"- {len(issues['missing_concepts'])} 个概念缺少独立页面\n"
        for concept in issues["missing_concepts"][:5]:
            report += f"  - {concept}\n"
    
    if issues["contradictions"]:
        report += f"- {len(issues['contradictions'])} 处可能的矛盾\n"
        for con in issues["contradictions"][:3]:
            report += f"  - \"{con['term']}\" 定义不一致\n"
    
    if issues["missing_refs"]:
        report += f"- {len(issues['missing_refs'])} 篇缺少交叉引用\n"
    
    if issues["outdated"]:
        report += f"- {len(issues['outdated'])} 篇可能过时（>6 个月）\n"
    
    # 💡 建议
    report += "\n💡 **建议操作**:\n"
    if issues["orphans"]:
        report += "1. 为孤立页面添加入链\n"
    if issues["missing_concepts"]:
        report += "2. 为重要概念创建独立页面\n"
    if issues["contradictions"]:
        report += "3. 统一矛盾描述\n"
    if issues["missing_refs"]:
        report += "4. 添加缺失的交叉引用\n"
    
    return report

def auto_fix(issues):
    """自动修复问题"""
    print("\n🔧 开始自动修复...\n")
    
    # 这里可以实现自动修复逻辑
    # 例如：自动添加缺失的链接
    print("自动修复功能开发中...")

def main():
    wiki_path = Path.cwd() / "wiki"
    
    if not wiki_path.exists():
        wiki_path = Path.cwd().parent / "wiki"
    
    if not wiki_path.exists():
        print("❌ 未找到 wiki 目录")
        sys.exit(1)
    
    auto_fix_flag = "--auto-fix" in sys.argv
    
    print(f"🔍 扫描 Wiki: {wiki_path}")
    print("=" * 50)
    
    # 1. 扫描所有页面
    pages = scan_wiki(wiki_path)
    
    # 2. 查找问题
    issues = {
        "pages": pages,
        "orphans": find_orphan_pages(pages),
        "missing_concepts": find_missing_concepts(pages),
        "contradictions": find_contradictions(pages),
        "outdated": find_outdated_info(pages),
        "missing_refs": find_missing_refs(pages)
    }
    
    # 3. 生成报告
    report = generate_report(issues)
    print(report)
    
    # 4. 可选：自动修复
    if auto_fix_flag:
        auto_fix(issues)

if __name__ == "__main__":
    main()
