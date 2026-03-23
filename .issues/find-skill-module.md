# Issue: Find Skill 模块 - 搜索外部 Skill，避免重复造轮子

## 背景

我们不需要从零开始重复造轮子。在动手开发之前，应该先搜索是否有现成的解决方案。

## 任务描述

### 1. 创建 `skills/find-skill/SKILL.md`

创建一个用于"搜索外部 Skill"的 Skill，能力包括：
- 搜索 ClawHub（clawhub.com）上的 Skill
- 搜索 GitHub 上的相关项目
- 提供"有没有现成方案"的快速判断

SKILL.md 示例结构：
```yaml
---
name: find-skill
description: |
  搜索外部 Skill 和解决方案。在用户想要开发新功能时，
  先搜索是否有现成方案，避免重复造轮子。
  本技能应在用户要求"找找有没有类似的 skill"、
  "搜索 XXX 功能"、或开始新项目之前触发。
---
```

### 2. 创建 `references/FIND-SKILL-GUIDE.md`

给新手看的"如何找现成方案"指南：
- 为什么要先搜索？
- 在哪里搜索？（ClawHub、GitHub、Claude Code 官方）
- 搜索技巧
- 搜索流程图

### 3. 更新 README.md

在项目 README 中添加"找方案"步骤：
```markdown
## 开发流程

1. **找方案** - 先看有没有现成的 → `skills/find-skill/`
2. **学规范** - 阅读开发指南 → `SKILL-DEV-GUIDE.md`
3. **动手做** - 基于模板开发 → `skills/skill-template/`
```

## 验收标准

- [ ] `skills/find-skill/SKILL.md` 完成，符合 Skill 规范
- [ ] `skills/find-skill/references/` 目录存在（可后续填充）
- [ ] `references/FIND-SKILL-GUIDE.md` 完成
- [ ] README.md 更新，包含"找方案"步骤

## 分配给
openclaw

## 优先级
P1

## 标签
skill, search, efficiency
