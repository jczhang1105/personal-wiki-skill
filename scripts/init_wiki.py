#!/usr/bin/env python3
"""
初始化个人知识库
用法：python init_wiki.py [主题名称]
"""

import sys
from pathlib import Path

def create_directories(base_path):
    """创建目录结构"""
    dirs = [
        "raw/inbox",
        "raw/archive/articles",
        "raw/archive/videos",
        "raw/archive/notes",
        "wiki/topics",
        "wiki/sources",
        "wiki/concepts",
        "wiki/queue",
        "outputs",
        "collectors",
    ]
    
    for d in dirs:
        path = base_path / d
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建：{d}")

def create_files(base_path, topic):
    """创建核心文件"""
    
    # AGENTS.md
    agents_md = f"""# {topic}知识库 Schema

## 这是什么
一个关于 {topic} 的个人知识库

## 目录结构
- raw/ 原始资料（只读）
- wiki/ 结构化知识（LLM 维护）
- outputs/ 生成的报告

## 标签规范
- 领域：#ai-product #investing #research #tools #life
- 难度：#beginner #intermediate #advanced
- 类型：#tutorial #news #opinion #data

## 优先级规则
- P0: 紧急重要 → 立即推送
- P1: 重要不紧急 → 每日摘要
- P2: 一般 → 每周报告
- P3: 参考材料 → 仅归档
"""
    (base_path / "AGENTS.md").write_text(agents_md, encoding="utf-8")
    
    # index.md
    index_md = f"""# {topic}知识库 Index

_最后更新：初始化完成_

## 📚 来源 (Sources)

_暂无内容，开始添加你的第一个知识！_

**快速开始**:
1. 转发文章/视频到微信
2. 或手动创建文件到 `raw/inbox/`
3. 告诉 Agent："处理 inbox"

## 🏷️ 主题 (Topics)

### {topic}
- [[{topic}基础]] - 待创建

## 💡 概念 (Concepts)

_待积累_

## ⏳ 待学习 (Queue)

_暂无待学习内容_

## 📊 统计

| 类别 | 数量 |
|------|------|
| 来源 | 0 |
| 主题 | 1 |
| 概念 | 0 |
| 待学习 | 0 |

---

[📓 查看日志 →](log.md)
"""
    (base_path / "wiki" / "index.md").write_text(index_md, encoding="utf-8")
    
    # log.md
    log_md = f"""# {topic}知识库 Log

_操作日志 - 追加式记录_

---

## [初始化] 知识库创建
- 主题：{topic}
- 状态：✅ 完成

---

## 日志格式

### Ingest（摄入）
```
## [YYYY-MM-DD HH:mm] ingest | 内容标题
- 来源：URL
- 类型：article
- 领域：#tags
- 优先级：P0/P1/P2/P3
- 页面：[[wiki/sources/xxx.md]]
```

### Query（查询）
```
## [YYYY-MM-DD HH:mm] query | 用户问题
- 相关页面：[[wiki/xxx.md]]
- 输出：[[wiki/outputs/xxx.md]]
```

### Lint（检查）
```
## [YYYY-MM-DD HH:mm] lint | daily/weekly
- 发现：...
- 建议：...
```
"""
    (base_path / "wiki" / "log.md").write_text(log_md, encoding="utf-8")
    
    # README.md
    readme_md = f"""# {topic}知识库

_个人知识管理系统 - 基于 Karpathy LLM Wiki 理念_

## 快速开始

1. **添加内容**: 把任何内容放到 `raw/inbox/`
2. **触发处理**: 告诉 Agent "处理 inbox"
3. **查看结果**: 检查 `wiki/sources/` 和 `wiki/log.md`

## 目录结构

```
{topic}-wiki/
├── raw/
│   ├── inbox/          ← 放新内容这里
│   └── archive/        ← 已处理归档
├── wiki/
│   ├── index.md        ← 总目录
│   ├── log.md          ← 操作日志
│   ├── topics/         ← 主题页
│   ├── sources/        ← 来源页
│   └── concepts/       ← 概念页
└── outputs/            ← 生成的报告
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `处理 inbox` | 处理待处理内容 |
| `查看 index` | 显示总目录 |
| `搜索 {{关键词}}` | 搜索知识库 |
| `生成周报` | 本周学习总结 |
| `检查 wiki 健康` | Lint 检查 |

---

_创建时间：{Path.home().parent.name}_
"""
    (base_path / "README.md").write_text(readme_md, encoding="utf-8")
    
    print("✅ 创建核心文件")

def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else "个人"
    base_path = Path(f"{topic}-wiki".replace(" ", "-").lower())
    
    print(f"🚀 初始化 {topic} 知识库...")
    print("=" * 50)
    
    create_directories(base_path)
    create_files(base_path, topic)
    
    print("=" * 50)
    print(f"✅ 知识库初始化完成！")
    print(f"📁 位置：{base_path.absolute()}")
    print(f"\n下一步：告诉 Agent '处理 inbox' 开始添加内容")

if __name__ == "__main__":
    main()
