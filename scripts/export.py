#!/usr/bin/env python3
"""
知识库导出脚本
功能：生成周报/学习总结/知识图谱
用法：python export.py [weekly|monthly|summary]
"""

import sys
import re
from pathlib import Path
from datetime import datetime, timedelta

def read_log(wiki_path):
    """读取操作日志"""
    log_file = wiki_path / "log.md"
    if not log_file.exists():
        return []
    
    content = log_file.read_text(encoding="utf-8")
    return parse_log(content)

def parse_log(content):
    """解析日志"""
    entries = []
    current_entry = None
    
    for line in content.split("\n"):
        # 匹配日志条目开始
        match = re.match(r'^## \[(\d{4}-\d{2}-\d{2} [^\]]+)\] (\w+) \| (.+)$', line)
        if match:
            if current_entry:
                entries.append(current_entry)
            current_entry = {
                "datetime": match.group(1),
                "type": match.group(2),
                "title": match.group(3),
                "details": []
            }
        elif current_entry and line.startswith("- "):
            current_entry["details"].append(line[2:])
    
    if current_entry:
        entries.append(current_entry)
    
    return entries

def filter_by_date(entries, days=7):
    """按日期过滤"""
    cutoff = datetime.now() - timedelta(days=days)
    filtered = []
    
    for entry in entries:
        try:
            entry_date = datetime.strptime(entry["datetime"].split()[0], "%Y-%m-%d")
            if entry_date >= cutoff:
                filtered.append(entry)
        except:
            pass
    
    return filtered

def categorize_entries(entries):
    """分类统计"""
    stats = {
        "total": len(entries),
        "by_type": {},
        "by_field": {},
        "ingest_count": 0,
        "query_count": 0,
        "lint_count": 0
    }
    
    for entry in entries:
        type_ = entry["type"]
        stats["by_type"][type_] = stats["by_type"].get(type_, 0) + 1
        
        if type_ == "ingest":
            stats["ingest_count"] += 1
            # 尝试提取领域
            for detail in entry["details"]:
                if "#ai-product" in detail:
                    stats["by_field"]["ai-product"] = stats["by_field"].get("ai-product", 0) + 1
                elif "#investing" in detail:
                    stats["by_field"]["investing"] = stats["by_field"].get("investing", 0) + 1
                elif "#research" in detail:
                    stats["by_field"]["research"] = stats["by_field"].get("research", 0) + 1
    
    return stats

def get_pending_items(wiki_path):
    """获取待学习项目"""
    queue_file = wiki_path / "queue" / "README.md"
    if not queue_file.exists():
        return []
    
    content = queue_file.read_text(encoding="utf-8")
    pending = re.findall(r'- \[ \] (.+)', content)
    return pending

def generate_weekly_report(entries, stats, pending):
    """生成周报"""
    date_range = f"{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} ~ {datetime.now().strftime('%Y-%m-%d')}"
    
    report = f"""# 周报 ({date_range})

_生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}_

---

## 📊 统计概览

- **总操作数**: {stats['total']} 次
- **新增来源**: {stats['ingest_count']} 篇
- **知识问答**: {stats['query_count']} 次
- **健康检查**: {stats['lint_count']} 次

### 按领域分类

"""
    
    for field, count in stats["by_field"].items():
        emoji = {"ai-product": "🤖", "investing": "💰", "research": "🔬"}.get(field, "📌")
        report += f"- {emoji} **{field}**: {count} 篇\n"
    
    if not stats["by_field"]:
        report += "_暂无分类数据_\n"
    
    report += """
---

## 🎯 高优先级内容

"""
    
    # 提取 P1 内容
    p1_items = []
    for entry in entries:
        if entry["type"] == "ingest":
            for detail in entry["details"]:
                if "P1" in detail:
                    p1_items.append(entry["title"])
    
    if p1_items:
        for i, item in enumerate(p1_items[:5], 1):
            report += f"{i}. {item}\n"
    else:
        report += "_暂无高优先级内容_\n"
    
    report += """
---

## 📝 待学习清单

"""
    
    if pending:
        for item in pending[:5]:
            report += f"- [ ] {item}\n"
    else:
        report += "_暂无待学习内容_\n"
    
    report += """
---

## 💡 学习建议

"""
    
    if stats["ingest_count"] > 10:
        report += "- 📚 本周学习量很大，建议安排时间复习\n"
    if stats["by_field"].get("ai-product", 0) > 5:
        report += "- 🤖 AI 产品内容较多，可以整理成专题\n"
    if len(pending) > 5:
        report += "- ⏳ 待学习内容较多，建议优先处理 P1 内容\n"
    
    report += """
---

_下周继续加油！_
"""
    
    return report

def generate_monthly_report(entries, stats, pending):
    """生成月报"""
    date_range = f"{(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')} ~ {datetime.now().strftime('%Y-%m-%d')}"
    
    report = f"""# 月报 ({date_range})

_生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}_

---

## 📊 月度统计

- **总操作数**: {stats['total']} 次
- **新增来源**: {stats['ingest_count']} 篇
- **日均学习**: {stats['ingest_count'] / 30:.1f} 篇/天

### 领域分布

"""
    
    for field, count in stats["by_field"].items():
        percentage = (count / stats["ingest_count"] * 100) if stats["ingest_count"] > 0 else 0
        report += f"- **{field}**: {count} 篇 ({percentage:.0f}%)\n"
    
    report += """
---

## 🎯 本月重点

_待补充_

---

## 📈 成长轨迹

_待补充_

---

_下月继续努力！_
"""
    
    return report

def main():
    report_type = sys.argv[1] if len(sys.argv) > 1 else "weekly"
    
    wiki_path = Path.cwd() / "wiki"
    if not wiki_path.exists():
        wiki_path = Path.cwd().parent / "wiki"
    
    if not wiki_path.exists():
        print("❌ 未找到 wiki 目录")
        sys.exit(1)
    
    print(f"📝 生成 {report_type} 报告...")
    print("=" * 50)
    
    # 1. 读取日志
    entries = read_log(wiki_path)
    
    # 2. 过滤
    if report_type == "weekly":
        entries = filter_by_date(entries, days=7)
    elif report_type == "monthly":
        entries = filter_by_date(entries, days=30)
    
    # 3. 统计
    stats = categorize_entries(entries)
    
    # 4. 待学习
    pending = get_pending_items(wiki_path)
    
    # 5. 生成报告
    if report_type == "weekly":
        report = generate_weekly_report(entries, stats, pending)
    elif report_type == "monthly":
        report = generate_monthly_report(entries, stats, pending)
    else:
        print(f"❌ 未知报告类型：{report_type}")
        sys.exit(1)
    
    # 6. 输出
    print(report)
    
    # 7. 保存
    output_file = Path.cwd() / "outputs" / f"{report_type}-report-{datetime.now().strftime('%Y%m%d')}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report, encoding="utf-8")
    
    print(f"\n✅ 报告已保存：{output_file}")

if __name__ == "__main__":
    main()
