# Issue: 官方资源整合 - 把官方文档引进来

## 背景

项目中需要包含官方 Skill 的讲解和示例，让新手不仅能动手做，还能理解原理。

## 任务描述

### 1. 创建 `references/OFFICIAL-DOCS.md`

汇总所有官方资源链接：
- OpenClaw 官方文档
- Claude Code 官方 Skill 文档
- ClawHub Skill 市场
- 官方 Skill 示例（pdf、skill-creator 等）

每个链接包含：
- 标题
- URL
- 一句话说明
- 适合人群（新手/进阶）

### 2. 增强 `skills/skill-template/SKILL.md`

当前模板比较简单，需要增强：
- 添加更详细的 description
- 添加"适用场景"和"不适用场景"
- 添加更完整的示例
- 添加"常见错误"章节

### 3. 创建 `references/SKILL-ANATOMY.md`

解剖一个官方 Skill（比如 pdf 或 skill-creator）：
- 文件结构
- Frontmatter 字段解释
- description 怎么写
- 工作流程怎么描述
- 触发条件怎么写

让新手通过"解剖示例"来学习。

## 验收标准

- [ ] `references/OFFICIAL-DOCS.md` 完成，至少 10 个官方资源链接
- [ ] `skills/skill-template/SKILL.md` 增强版完成
- [ ] `references/SKILL-ANATOMY.md` 完成，解剖至少 2 个官方 Skill

## 分配给
openclaw

## 优先级
P1

## 标签
official, documentation, reference
