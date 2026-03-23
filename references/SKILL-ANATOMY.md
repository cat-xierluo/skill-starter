# Skill 解剖课：认识一个 Skill 的组成

> 通过解剖真实 Skill 来学习 Skill 的结构。本文档以官方 Skill 为例，带你逐个了解每个部分的作

---

## 为什么要解剖 Skill？

学写代码要读源码，学写 Skill 要读 SKILL.md。

解剖一个真实的 Skill，你会学到：
- SKILL.md 的标准格式是什么
- description 怎么写才能被正确触发
- 什么样的结构最容易被 AI 理解和使用

---

## 案例一：find-skills（搜索技能）

**来源**：vercel-labs/skills

**定位**：帮用户找到现成的 Agent Skill，避免重复造轮子。

### 文件结构

```
find-skills/
└── SKILL.md        # 只有一个文件，但它很完整
```

### Frontmatter

```yaml
---
name: find-skills
description: |
  Helps users discover and install agent skills when they ask questions like
  "how do I do X", "find a skill for X", "is there a skill that can...",
  or express interest in extending capabilities. This skill should be used
  when the user is looking for functionality that might exist as an
  installable skill.
---
```

**分析**：
- `name`：简洁、英文、全小写
- `description`：用了 3 种触发表达（"how do I do X"、"find a skill for X"、"is there a skill for X"），覆盖用户可能说的不同问法
- 注意：description 是英文的，因为这是面向全球用户的

### 正文结构

```markdown
# Find Skills

## When to Use This Skill
（什么时候触发）

## What is the Skills CLI?
（背景知识：什么是 Skills CLI）

## How to Help Users Find Skills
（核心逻辑：6 个步骤）

## Common Skill Categories
（分类表格：方便快速查找）

## Tips for Effective Searches
（搜索技巧：提高成功率）

## When No Skills Are Found
（找不到怎么办）
```

**分析**：
- 用标题直接点明"这是什么"
- 每个章节都很短，便于快速定位
- 提供了流程步骤（How to...）
- 包含了边界情况（When No Skills Are Found）

---

## 案例二：skill-creator（技能创建）

**来源**：OpenClaw 官方

**定位**：帮助用户从零创建一个新的 Skill。

### 文件结构

```
skill-creator/
├── SKILL.md              # 主文件
└── scripts/
    └── skillcreator.ts   # 辅助脚本（可选）
```

### Frontmatter

```yaml
---
name: skill-creator
description: |
  This skill guides you through the process of creating a new Claude Code
  skill. It should be used when a user asks to create a skill, build a
  skill, or make a new capability for Claude Code.
  This skill should not be used for general programming tasks or questions
  unrelated to skill development.
---
```

**分析**：
- description 分两条写：**正向**（做什么）和**负向**（不做什么）
- 负向条件很重要：避免 Skill 被错误触发
- 触发词很具体："create a skill"、"build a skill"、"make a new capability"

### 正文结构

```markdown
# Skill Creator

## When to use this skill
（什么时候用）

## Before you start
（开始之前要准备什么）

## Step 1: Design
（步骤1：设计）

## Step 2: Create the SKILL.md
（步骤2：创建核心文件）

## Step 3: Add resources
（步骤3：添加资源）

## Step 4: Test
（步骤4：测试）

## Best practices
（最佳实践）
```

**分析**：
- 用"步骤"组织内容，符合人的思维习惯
- 每个步骤标题都是动词开头（Design、Create、Add、Test）
- 提供了前置条件（Before you start）

---

## 案例三：pdf（文档处理）

**来源**：OpenClaw 官方

**定位**：处理 PDF 文件，提取内容、总结、搜索等。

### Frontmatter

```yaml
---
name: pdf
description: |
  This skill is used when you need to work with PDF files. This includes
  extracting text, summarizing, searching within, or converting PDFs.
  This skill should be used when a user asks to read a PDF, summarize
  a PDF, extract content from a PDF, or search within a PDF file.
  This skill should not be used for creating PDFs or editing existing ones.
---
```

**分析**：
- 触发条件列得很细：read / summarize / extract / search
- 负向条件也写了：不用于创建和编辑

### 正文特点

```markdown
# PDF Skill

## Overview
（概览：Skill 能做什么）

## Usage
（使用方法）

## Examples
（示例：让 AI 知道怎么调用）
```

---

## 通用结构总结

通过解剖 3 个 Skill，我们发现它们都遵循类似的结构：

### 1. Frontmatter（必须）

```yaml
---
name: skill-name
description: |
  【正向】本技能在...时使用。
  【负向】不要用于...。
---
```

### 2. 主标题

```markdown
# Skill 名称

一句话说明这是什么 Skill
```

### 3. 适用场景（When to use）

- 明确什么时候触发
- 包含正向和负向条件

### 4. 核心内容

按需组织，常见模式：
- **教程型**：步骤 1、2、3...
- **参考型**：命令列表、配置说明
- **流程型**：如何做某事的完整流程

### 5. 示例（Examples）

提供 1-2 个具体示例，让 AI 知道怎么用

### 6. 边界情况

- 找不到结果怎么办
- 不适用的情况怎么处理

---

## 写作技巧

### description 写法

| ✅ 好 | ❌ 差 |
|-------|-------|
| "当用户说'帮我创建 Skill'时触发" | "用于创建" |
| "不要用于简单问答" | "可用于各种任务" |
| 覆盖多种表达方式 | 只有一种触发词 |

### 触发词要多样

```yaml
# ✅ 好：覆盖多种问法
description: |
  本技能应在用户要求"创建 Skill"、"新建技能"、
  "帮我做一个可以..."、"build a skill"时触发。

# ❌ 差：只有一种
description: "当用户说'创建 Skill'时使用。"
```

### 正文要短

- SKILL.md 正文 **≤ 500 行**
- 超过的拆到 `references/` 目录
- 代码示例要精简，完整代码放 `scripts/`

### 用自然段落

- 不要列表嵌套列表
- 不要表格嵌套表格
- 一件事一段话，说清楚就行

---

## 练习：你能发现这个 SKILL.md 的问题吗？

```yaml
---
name: my-skill
description: "A useful skill for various tasks."
---
```

**问题**：
1. description 太短（没有说明什么时候用）
2. 没有负向条件
3. 触发词太模糊（"various tasks"是什么？）
4. 没有实际内容

---

## 下一步

- 查看 [SKILL-DEV-GUIDE.md](../SKILL-DEV-GUIDE.md) 了解完整规范
- 查看 [skills/skill-template/](../skills/skill-template/SKILL.md) 使用模板
- 去 [ClawHub](https://clawhub.com) 看看更多真实 Skill

---

**解剖日期：2026-03-23 | 版本：1.0.0**
