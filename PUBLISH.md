# Personal Wiki Skill - 发布指南

---

## 📦 发布前检查清单

### 1. 文件完整性

- [x] `SKILL.md` - 核心说明文件
- [x] `workflows.md` - 工作流示例
- [x] `README.md` - 使用文档
- [x] `skill.json` - 元数据配置
- [x] `scripts/init_wiki.py` - 初始化脚本
- [ ] `scripts/ingest.py` - 摄入脚本
- [ ] `scripts/query.py` - 查询脚本
- [ ] `scripts/lint.py` - Lint 脚本
- [ ] `scripts/export.py` - 导出脚本
- [ ] `templates/` - 模板文件

### 2. 功能测试

- [x] Ingest 流程 - 处理 inbox 测试通过
- [x] 目录结构创建 - 验证成功
- [ ] Query 流程 - 待实现
- [ ] Lint 流程 - 待实现
- [ ] Export 流程 - 待实现

### 3. 文档完善

- [x] SKILL.md 使用说明
- [x] workflows.md 工作流
- [x] README.md 快速开始
- [ ] API 文档
- [ ] 常见问题 FAQ

---

## 🚀 发布到 ClawHub

### 方式 1: 使用 clawhub publish 命令

```bash
cd C:\Users\16603\.openclaw\workspace\skills\personal-wiki

npx clawhub@latest publish . \
  --slug personal-wiki \
  --name "Personal Wiki - 个人知识库" \
  --version 1.0.0 \
  --tags "knowledge-management,learning,wiki,chinese" \
  --description "基于 Karpathy LLM Wiki 理念的个人知识管理技能"
```

### 方式 2: 手动上传

1. 访问 [ClawHub](https://clawhub.ai)
2. 登录账号
3. 点击 "Publish Skill"
4. 上传 `personal-wiki` 目录
5. 填写元数据（name/description/tags）
6. 提交审核

---

## 📝 ClawHub 元数据

```json
{
  "name": "personal-wiki",
  "displayName": "Personal Wiki - 个人知识库",
  "version": "1.0.0",
  "description": "基于 Karpathy LLM Wiki 理念的个人知识管理技能，支持碎片化学习、自动整理、智能问答",
  "author": "张家诚 (诚)",
  "tags": ["knowledge-management", "learning", "wiki", "productivity", "chinese"],
  "category": "productivity"
}
```

---

## 🎯 发布后的推广

### 1. ClawHub 社区

- 在 ClawHub Discord 发布介绍
- 回复用户问题
- 收集反馈迭代

### 2. 社交媒体

**小红书文案**:
```
🔥 我开发了一个 OpenClaw 技能！
基于 Karpathy 的 LLM Wiki 理念
自动整理碎片化知识，越用越聪明✨

功能：
✅ 自动收集小红书/微信收藏
✅ 智能分类+打标签
✅ 知识库问答
✅ 每周学习报告

开源免费，欢迎试用！
#AI #知识管理 #OpenClaw #效率工具
```

**推特文案**:
```
Just published my first OpenClaw skill: Personal Wiki! 📚

Based on @karpathy's LLM Wiki concept:
- Auto-collect from social media
- Smart tagging & categorization
- Knowledge Q&A
- Weekly learning reports

Free & open source! 
#AI #KnowledgeManagement #OpenClaw
```

### 3. 技术社区

- V2EX 分享
- 知乎专栏文章
- 掘金技术文章

---

## 📊 版本规划

### v1.0.0 (当前)
- ✅ Ingest 流程
- ✅ 目录结构创建
- ✅ 基础文档
- 🔄 Query 流程（设计中）
- 🔄 Lint 流程（设计中）

### v1.1.0 (计划)
- [ ] Query 流程实现
- [ ] Lint 流程实现
- [ ] 智能分类优化

### v1.2.0 (计划)
- [ ] Export 流程（周报/总结）
- [ ] 多平台收集器
- [ ] 图表生成

### v2.0.0 (愿景)
- [ ] Web UI
- [ ] 知识图谱可视化
- [ ] 协作功能

---

## 💡 使用示例（用于文档）

### 示例 1: 从零搭建

**用户**: 帮我搭建一个 AI 产品学习的知识库

**助手**:
```
好的！正在创建 AI 产品学习知识库...

✅ 已创建:
- my-wiki/raw/inbox/
- my-wiki/raw/archive/
- my-wiki/wiki/topics/
- my-wiki/wiki/sources/
- my-wiki/wiki/concepts/
- my-wiki/AGENTS.md
- my-wiki/wiki/index.md
- my-wiki/wiki/log.md

主题页已初始化:
- AI 产品
- 机器学习
- 产品设计
- 大厂研究

现在可以开始添加内容了！
```

### 示例 2: 处理收藏

**用户**: 处理 inbox

**助手**:
```
✅ 已处理 5 篇文章

📊 统计:
- AI 产品：3 篇（P1）
- 投资：1 篇（P2）
- 生活：1 篇（P3）

已创建 wiki 页面:
- [[收 offer 网站推荐]]
- [[手搓 agent 面 AI 产品岗]]
- [[Vibe Coding 简历 + 个人网站]]
- [[Python 量化入门]]
- [[红烧鸡块食谱]]

高优先级内容已推送到微信！
```

### 示例 3: 知识问答

**用户**: Karpathy 的知识库方法是什么？

**助手**:
```
根据知识库中的 3 篇 Karpathy 相关文章：

🎯 核心理念
让 LLM 像图书管理员一样，帮你持续维护一个 Markdown 知识库，而不是临时检索。

📁 三层架构
1. raw/ - 原始资料（只读）
2. wiki/ - 结构化知识（LLM 维护）
3. AGENTS.md - 维护规则

⚙️ 三个操作
1. Ingest - 摄入资料→总结→归档
2. Query - 搜索 Wiki→综合回答
3. Lint - 健康检查→修复建议

📚 来源:
- [[Karpathy 亲自教你搭建知识库]]
- [[Karpathy 分享个人知识库思路]]
- [[Karpathy AI 知识库经验分享]]
```

---

## 🔧 开发环境

### 本地测试

```bash
# 克隆技能目录
cd C:\Users\16603\.openclaw\workspace\skills\personal-wiki

# 测试初始化脚本
python scripts/init_wiki.py 测试知识库

# 验证技能格式
npx clawhub@latest validate .
```

### 调试模式

在 OpenClaw 中加载本地技能：
```
用户：加载本地技能 personal-wiki
助手：好的，已从本地加载技能...
```

---

## 📞 联系方式

- **GitHub**: [你的 GitHub](https://github.com/你的用户名)
- **小红书**: 橘子 7lj
- **邮箱**: 你的邮箱

---

_创建时间：2026-04-07_
_版本：v1.0.0_
