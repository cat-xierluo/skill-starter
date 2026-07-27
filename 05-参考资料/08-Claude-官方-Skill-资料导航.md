# Claude 官方 Skill 资料导航

> 本文整理 Claude / Anthropic 官方的 Skill 相关资料，优先收录官方文档、官方博客、工程文章、官方 PDF 和官方 Webinar。
> 最后核对时间：2026-03-30

---

## 1. 先看哪几篇

如果你是第一次系统了解 Skills，建议按这个顺序看：

1. 官方产品介绍：`Introducing Agent Skills`
2. Claude Code 官方文档：`Skills`
3. 官方最佳实践：`Skill authoring best practices`
4. 工程深度文章：`Equipping agents for the real world with Agent Skills`
5. 实操文章：`How to create Skills`
6. 官方 PDF / Complete Guide：`A complete guide to building skills for Claude`

这样你会先知道：

- Skills 是什么
- Claude Code 里怎么用
- 为什么这样设计
- 怎么真的写一个 Skill
- 官方推荐的后续资料有哪些

---

## 2. 官方文档

### 2.1 Claude Code 技能文档

- **标题**：Skills
- **链接**：[docs.claude.com/en/docs/claude-code/skills](https://docs.claude.com/en/docs/claude-code/skills)
- **适合什么时候看**：要在 Claude Code 里创建、发现、调用和管理 Skills 时
- **你会学到什么**：
  - Skills 在 Claude Code 里的位置和工作方式
  - `SKILL.md` 基本结构
  - Skills 存放目录
  - 自动发现机制
  - 支持文件、动态上下文、子代理执行等进阶能力

### 2.2 Claude API 技能文档

- **标题**：Agent Skills
- **链接**：[platform.claude.com/docs/en/agents-and-tools/agent-skills/overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- **适合什么时候看**：要通过 API 上传或使用 Skills 时
- **你会学到什么**：
  - Claude API 中预置 Skill 与自定义 Skill 的区别
  - `/v1/skills` 的定位
  - API 使用 Skills 需要的 beta headers
  - Claude.ai / Claude Code / Agent SDK / API 之间的差异

### 2.3 Claude Code Quickstart

- **标题**：Quickstart
- **链接**：[docs.claude.com/en/docs/claude-code/quickstart](https://docs.claude.com/en/docs/claude-code/quickstart)
- **适合什么时候看**：刚开始使用 Claude Code 时
- **为什么和 Skill 有关**：
  - Quickstart 里会把 Skills 放进 Claude Code 的整体工作流里理解
  - 也能看到官方对“新手怎么和 Claude Code 协作”的建议

### 2.4 Skill 编写最佳实践

- **标题**：Skill authoring best practices
- **链接**：[docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- **适合什么时候看**：已经准备真正动手写 Skill，但想先避开常见坑时
- **你会学到什么**：
  - `description` 如何写得更容易触发
  - `SKILL.md` 应该保持多短
  - 什么时候拆到 `references/`
  - 什么时候该用脚本而不是继续堆提示词

---

## 3. 官方博客与工程文章

### 3.1 产品发布文章

#### Introducing Agent Skills

- **链接**：[claude.com/blog/skills](https://claude.com/blog/skills)
- **发布日期**：2025-10-16
- **更新**：2025-12-18 增加组织级管理、目录和开放标准
- **看点**：
  - Skills 的产品定位
  - 为什么 Skills 可组合、可移植、按需加载
  - Claude.ai、Claude Code、API、Agent SDK 的整体支持情况

#### Skills for organizations, partners, the ecosystem

- **链接**：[claude.com/blog/organization-skills-and-directory](https://claude.com/blog/organization-skills-and-directory)
- **发布日期**：2025-12-18
- **看点**：
  - 组织级 Skill 管理
  - 伙伴 Skill 目录
  - Skills 开放标准生态

### 3.2 工程深度文章

#### Equipping agents for the real world with Agent Skills

- **链接**：[claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- **发布日期**：2025-10-16
- **看点**：
  - Skill 的设计动机
  - Skill anatomy
  - 为什么要把知识、脚本、资源打包成文件夹
  - 如何迭代和评估 Skill
  - 安全注意事项

### 3.3 实操与解释文章

#### How to create Skills: Key steps, limitations, and examples

- **链接**：[claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples](https://claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples)
- **发布日期**：2025-11-19
- **看点**：
  - 写 Skill 的步骤
  - 技能触发限制
  - 文件大小与拆分建议
  - 真实 Skill 示例

#### Building Skills for Claude Code: Automating your procedural knowledge

- **链接**：[claude.com/blog/building-skills-for-claude-code](https://claude.com/blog/building-skills-for-claude-code)
- **发布日期**：2025-12-02
- **看点**：
  - 为什么团队流程、schema、业务术语很适合打包成 Skill
  - 如何把“组织里的隐性知识”变成 Claude Code 可用的显性流程
  - 适合拿来理解团队内部 Skill 的价值

#### Skills explained: How Skills compares to prompts, Projects, MCP, and subagents

- **链接**：[claude.com/blog/skills-explained](https://claude.com/blog/skills-explained)
- **发布日期**：2025 年底，当前官网可访问
- **看点**：
  - Skills 和 Prompt、Projects、MCP、Subagents 的边界
  - 在 Claude Code 中 subagent 与 Skills 如何协作

#### Building agents with Skills: Equipping agents for specialized work

- **链接**：[claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work](https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work)
- **发布日期**：2026-01-22
- **看点**：
  - 站在 Claude Code 视角理解 Skills 如何把通用代理变成专用代理
  - 更偏“为什么团队要用 Skills”

#### Improving skill-creator: Test, measure, and refine Agent Skills

- **链接**：[claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)
- **发布日期**：2026-03-03
- **看点**：
  - Skill 不是只写完就算结束
  - 官方开始强调测试、回归、描述优化和评估

#### Improving frontend design through Skills

- **链接**：[claude.com/blog/improving-frontend-design-through-skills](https://claude.com/blog/improving-frontend-design-through-skills)
- **发布日期**：2025-11-12
- **看点**：
  - 很直观地展示了 Skill 如何改变 Claude 的默认输出质量
  - 适合理解“为什么把领域偏好写成 Skill，比每次重复提示更有效”
  - 也适合作为“如何把抽象偏好沉淀成可复用 Skill”的案例

#### A complete guide to building skills for Claude

- **链接**：[claude.com/blog/complete-guide-to-building-skills-for-claude](https://claude.com/blog/complete-guide-to-building-skills-for-claude)
- **发布日期**：2026-01-29
- **看点**：
  - 把“规划、结构、测试、分发”串成完整流程
  - 单独覆盖了 MCP + Skills 的组合方式
  - 是官方目前最接近“总览指南”的文章

---

## 4. 官方 PDF 指南

### The Complete Guide to Building Skills for Claude

- **链接**：[resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
- **适合什么时候看**：想系统补齐资料、把碎片博客串起来时
- **价值**：
  - 它像一个总索引，把文档、博客、仓库、工具都串在一起
  - 还包含一份快速检查清单
  - 明确建议先看 Best Practices，再看 API 文档

### 从 PDF 里特别值得注意的几条

根据 PDF 中的资源章节：

- 初学者应先读 Best Practices Guide，再按需查 API 文档
- 资源列表里明确列出了：
  - `Introducing Agent Skills`
  - `Equipping agents for the real world with Agent Skills`
  - `Skills Explained`
  - `How to Create Skills`
  - `Building Skills for Claude Code`
  - `Improving Frontend Design through Skills`
- `skill-creator` 被官方当作首选创建和评估工具之一

---

## 5. 官方 Webinar / 直播资料

### Agent Skills: Transform Claude from Assistant to Specialized Agent

- **链接**：[anthropic.com/webinars/agent-skills-transform-claude-from-assistant-to-specialized-agent](https://www.anthropic.com/webinars/agent-skills-transform-claude-from-assistant-to-specialized-agent)
- **发布日期**：2025-11-12
- **适合什么时候看**：想从“实战工作流”角度理解 Skill
- **看点**：
  - Skills 心智模型
  - 真实应用场景
  - 技术架构
  - Skill Creator、API、Claude Code 三种创建方式
  - 最佳实践：scope、examples、composition

---

## 6. 官方仓库与工具

### Anthropic Skills 仓库

- **链接**：[github.com/anthropics/skills](https://github.com/anthropics/skills)
- **适合什么时候看**：想直接看 Anthropic 做的 Skill 例子时

### skill-creator

- 在官方 PDF 和官方博客里都被反复提到
- 用途：
  - 从描述生成 Skill 初稿
  - 审查和改进已有 Skill
  - 在新版本里加入测试、回归和评估

---

## 7. 你在这个项目里应该怎么用这些资料

推荐做法：

1. 先看 [03-Skill-官方编写指南.md](./03-Skill-官方编写指南.md)
2. 再看 [10-Claude-Skill-最佳实践清单.md](./10-Claude-Skill-最佳实践清单.md)
3. 然后按本文里的官方原始资料顺序阅读
4. 接着看 [04-创建Skill/SKILL-DEV-GUIDE.md](../04-创建Skill/SKILL-DEV-GUIDE.md)
5. 最后回到模板：
   - [skills/skill-template/SKILL.md](../skills/skill-template/SKILL.md)

---

## 8. 哪些资料最值得长期跟踪

如果你只想持续关注少数几项，优先跟：

- `docs.claude.com/en/docs/claude-code/skills`
- `docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices`
- `platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`
- `claude.com/blog/skills`
- `claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills`
- `claude.com/blog/complete-guide-to-building-skills-for-claude`
- `The Complete Guide to Building Skills for Claude.pdf`

---

## 一句话总结

Claude 官方关于 Skills 的资料已经不止一篇博客，而是一整套：产品介绍、工程文章、API 文档、Claude Code 文档、PDF 总指南和 Webinar。这个项目应该把它们当成“官方知识地图”，而不是零散链接。
