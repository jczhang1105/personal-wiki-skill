# Personal Wiki - 工作流示例

---

## 📥 工作流 1: 碎片化学习流程

### 场景
用户在多个平台收藏内容（小红书/推特/浏览器），希望自动整理到知识库。

### 流程

```
┌─────────────────────────────────────────────────────────────┐
│  输入层                                                      │
│  • 小红书收藏                                                │
│  • 浏览器剪藏                                                │
│  • 微信转发                                                  │
│  • 推特点赞                                                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  收集层 (Collectors)                                         │
│  • xhs-favorites.py - 小红书收集器                           │
│  • browser-clipper.py - 浏览器剪藏                           │
│  • wechat-forward.py - 微信转发处理                          │
│  • 输出：raw/inbox/{timestamp}_{title}.md                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  处理层 (Process)                                            │
│  1. 读取 inbox 文件                                          │
│  2. 提取元数据（标题/来源/类型）                             │
│  3. LLM 总结（3-5 个核心观点）                               │
│  4. 打标签（领域 + 难度 + 优先级）                           │
│  5. 创建 wiki/sources/{slug}.md                             │
│  6. 更新相关主题页                                           │
│  7. 移动文件到 archive                                       │
│  8. 更新 index.md + log.md                                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  输出层 (Output)                                             │
│  • 微信推送："今日处理 X 篇，高优先级 Y 篇"                    │
│  • 待学习队列更新                                            │
│  • 知识库统计更新                                            │
└─────────────────────────────────────────────────────────────┘
```

### 代码示例

```python
# scripts/ingest.py
def process_inbox():
    inbox_dir = Path("raw/inbox")
    archive_dir = Path("raw/archive/articles")
    
    for file in inbox_dir.glob("*.md"):
        # 1. 读取内容
        content = file.read_text()
        meta = extract_metadata(content)
        
        # 2. LLM 总结
        summary = llm_summarize(content)
        
        # 3. 打标签
        tags = classify_tags(summary)
        
        # 4. 创建来源页
        create_source_page(meta, summary, tags)
        
        # 5. 更新索引
        update_index(meta)
        update_log(meta)
        
        # 6. 归档
        move_to_archive(file)
    
    # 7. 推送摘要
    push_summary()
```

---

## 🔍 工作流 2: 知识问答流程

### 场景
用户对知识库提问，需要综合多个页面给出答案。

### 流程

```
用户提问
    ↓
┌─────────────────────────────────────────────────────────────┐
│  1. 搜索相关页面                                             │
│  • 搜索 index.md                                             │
│  • 匹配标题/标签/描述                                        │
│  • 返回 top-k 相关页面                                       │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  2. 读取页面内容                                             │
│  • 读取来源页                                                │
│  • 读取主题页                                                │
│  • 读取概念页（如有）                                        │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  3. 综合回答                                                 │
│  • 提取关键信息                                              │
│  • 整合多个来源                                              │
│  • 标注引用来源                                              │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  4. 可选：答案回存                                           │
│  • 保存到 wiki/outputs/                                      │
│  • 添加到相关主题页                                          │
└─────────────────────────────────────────────────────────────┘
```

### 代码示例

```python
# scripts/query.py
def answer_question(question):
    # 1. 搜索
    index = read_file("wiki/index.md")
    relevant = search_index(index, question, top_k=5)
    
    # 2. 读取
    pages = []
    for item in relevant:
        content = read_file(item.path)
        pages.append(content)
    
    # 3. 综合
    answer = llm_synthesize(question, pages)
    
    # 4. 引用
    answer += "\n\n来源:\n"
    for item in relevant:
        answer += f"- [[{item.title}]]\n"
    
    return answer
```

---

## 🔧 工作流 3: 健康检查流程

### 场景
定期扫描知识库，发现并修复问题。

### 流程

```
┌─────────────────────────────────────────────────────────────┐
│  1. 扫描所有页面                                             │
│  • wiki/topics/                                              │
│  • wiki/sources/                                             │
│  • wiki/concepts/                                            │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  2. 检查问题                                                 │
│  • 孤立页面（无入链）                                        │
│  • 矛盾内容（同一概念不同描述）                              │
│  • 过时信息（新资料推翻旧结论）                              │
│  • 缺失交叉引用                                              │
│  • 重要概念无独立页面                                        │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  3. 生成报告                                                 │
│  • ✅ 好的方面                                               │
│  • ⚠️ 需要修复                                               │
│  • 💡 建议优化                                               │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  4. 可选：自动修复                                           │
│  • 添加缺失的交叉引用                                        │
│  • 创建概念页                                                │
│  • 统一描述                                                  │
└─────────────────────────────────────────────────────────────┘
```

### 代码示例

```python
# scripts/lint.py
def health_check():
    issues = {
        "orphan_pages": find_orphan_pages(),
        "contradictions": find_contradictions(),
        "outdated": find_outdated_info(),
        "missing_refs": find_missing_references(),
        "concepts_needed": suggest_concepts()
    }
    
    report = generate_report(issues)
    print(report)
    
    # 可选：自动修复
    if auto_fix:
        fix_orphan_pages(issues["orphan_pages"])
        add_missing_refs(issues["missing_refs"])
```

---

## 📊 工作流 4: 生成报告流程

### 场景
生成周报/学习总结/知识图谱。

### 流程

```
┌─────────────────────────────────────────────────────────────┐
│  1. 读取日志                                                 │
│  • wiki/log.md                                               │
│  • 筛选时间范围（本周/本月）                                 │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  2. 分类统计                                                 │
│  • 按领域分组（AI 产品/投资/研究...）                        │
│  • 按优先级分组（P1/P2/P3）                                  │
│  • 计算数量/趋势                                             │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  3. 生成报告                                                 │
│  • 📊 统计概览                                               │
│  • 🎯 高优先级内容                                           │
│  • 📝 待学习清单                                             │
│  • 💡 学习建议                                               │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  4. 输出                                                     │
│  • 保存到 outputs/weekly-report-{date}.md                   │
│  • 可选：微信推送摘要                                        │
│  • 可选：生成图表                                            │
└─────────────────────────────────────────────────────────────┘
```

### 代码示例

```python
# scripts/export.py
def generate_weekly_report():
    # 1. 读取日志
    log = read_file("wiki/log.md")
    this_week = filter_by_date(log, days=7)
    
    # 2. 统计
    stats = {
        "total": len(this_week),
        "by_field": group_by_field(this_week),
        "by_priority": group_by_priority(this_week),
        "pending": get_pending_items()
    }
    
    # 3. 生成报告
    report = f"""# 周报 ({get_date_range()})

## 📊 统计
- 新增来源：{stats['total']} 篇
- AI 产品：{stats['by_field']['ai-product']} 篇
- 投资：{stats['by_field']['investing']} 篇

## 🎯 高优先级
{format_high_priority(stats['by_priority']['P1'])}

## 📝 待学习
{format_pending(stats['pending'])}
"""
    
    # 4. 保存
    save_report(report)
    return report
```

---

## 🔄 定时任务配置

### Cron 配置示例

```json
{
  "jobs": [
    {
      "name": "每日收藏收集",
      "schedule": {"kind": "cron", "expr": "0 20 * * *", "tz": "Asia/Shanghai"},
      "payload": {
        "kind": "agentTurn",
        "message": "收集小红书收藏并保存到 inbox"
      }
    },
    {
      "name": "每日自动处理",
      "schedule": {"kind": "cron", "expr": "30 20 * * *", "tz": "Asia/Shanghai"},
      "payload": {
        "kind": "agentTurn",
        "message": "处理 inbox 中的内容"
      }
    },
    {
      "name": "每周健康检查",
      "schedule": {"kind": "cron", "expr": "0 10 * * 0", "tz": "Asia/Shanghai"},
      "payload": {
        "kind": "agentTurn",
        "message": "检查 wiki 健康并生成报告"
      }
    },
    {
      "name": "每周学习报告",
      "schedule": {"kind": "cron", "expr": "0 18 * * 5", "tz": "Asia/Shanghai"},
      "payload": {
        "kind": "agentTurn",
        "message": "生成本周学习报告"
      }
    }
  ]
}
```

---

## 📝 最佳实践

### 1. 标签规范

```markdown
# 领域标签
- #ai-product - AI 产品相关
- #investing - 投资（crypto/stocks）
- #research - 研究（论文/技术）
- #tools - 工具/技能
- #life - 生活/其他

# 难度标签
- #beginner - 入门
- #intermediate - 进阶
- #advanced - 高级

# 类型标签
- #tutorial - 教程
- #news - 新闻
- #opinion - 观点
- #data - 数据/报告
```

### 2. 优先级规则

| 优先级 | 推送时机 | 示例 |
|--------|----------|------|
| P0 | 立即推送 | 紧急通知 |
| P1 | 每日摘要 | 高质量教程 |
| P2 | 每周报告 | 一般资讯 |
| P3 | 仅归档 | 参考材料 |

### 3. 文件命名

```
{YYYYMMDD}_{source}_{slug}.md

示例:
- 20260407_xhs_karpathy-tutorial.md
- 20260407_wechat_crypto-analysis.md
- 20260407_browser_llm-wiki.md
```

---

_版本：v1.0.0_
_创建时间：2026-04-07_
