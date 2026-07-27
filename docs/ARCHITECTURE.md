# 项目架构

> Last updated: 2026-03-31

## 定位

`skill-starter` 是一个面向 Skill 开发的教学型脚手架仓库，不是单个 Skill。它同时提供：

- 学习资料
- 可复制模板
- 完整示例
- 协作文档规范

## 架构分层

### 1. 学习内容层

负责解释概念、工具和工作流。

- `01-概念入门/`：Skill、GitHub、术语等基础概念
- `02-工具指南/`：Git、GitHub、SSH、commit 规范等基础工具
- `03-AI协作与上下文/`：Vibe Coding、`AGENTS.md`、`CLAUDE.md`、上下文工程、Rules
- `04-创建Skill/`：从搜索到创建、调试、发布的实操流程
- `05-参考资料/`：官方文档、结构拆解和外部资源索引

### 2. 模板与示例层

负责把规范变成可复制资产。

- `.claude/skills -> ../skills`：Claude Code 实际读取的 project-local Skill 入口
- `skills/skill-template/`：标准起点模板
- `skills/weekly-weather-briefing/`：完整示例 Skill
- `skills/find-skill/`：搜索外部 Skill 的引导文档

### 3. 仓库治理层

负责项目本身的迭代和协作。

- `CHANGELOG.md`：记录对外可见变更
- `docs/ROADMAP.md`：阶段目标和路线图
- `docs/TASKS.md`：当前任务状态
- `docs/DECISIONS.md`：决策与工作日志

## 设计原则

### 文档优先

Starter 的核心价值在于把经验沉淀为可复制文档，而不是只放一个模板目录。

### 概念、工具、上下文分层

Git / GitHub / commit 属于基础工具；Vibe Coding、`AGENTS.md`、`CLAUDE.md`、Rules 属于 AI 协作方法。两者相关，但不应混在同一层里。

### 模板与示例分离

模板负责最小可用结构，示例负责展示一套完整做法。这样既不让模板过重，也不让新人缺少参考。

### 协作文档默认存在

复杂 Skill 或长期维护的 Skill，默认应该带上 `docs/` 和 `CHANGELOG.md`，这样未来的人类或 Agent 才能接上上下文。

## 后续演进方向

- 增加自动化校验脚本，检查断链、目录结构和模板完整性
- 增加更多不同类型的示例 Skill
- 增加与 Skills CLI、Claude Code、OpenClaw 的实测安装说明
