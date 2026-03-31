---
name: find-skill
description: |
  搜索外部 Skill 的安装与使用引导。本技能应在用户准备开发新功能、想先查有没有现成 Skill、或需要了解独立 find-skills 项目如何接入时使用。
  不要用于：伪造搜索结果、替代真实的 Skills CLI 搜索、或在没有验证来源的情况下直接推荐第三方项目。
metadata:
  openclaw:
    emoji: "🔍"
    requires: []
    triggers:
      - "有没有现成的"
      - "搜索 skill"
      - "有没有类似的"
      - "找方案"
      - "search for skill"
      - "find a skill"
      - "有没有现成方案"
---

# Find Skill

在动手开发前，先搜搜有没有现成方案。

> 注意：本仓库采用 `.claude/skills -> ../skills` 的符号链接结构。也就是说，`skills/find-skill/SKILL.md` 既是仓库里的源文件，也是 Claude Code 通过 `.claude/skills/find-skill/` 读取到的 project-local Skill 定义。

## 什么时候用

当用户说：
- "有没有做 XXX 的 skill？"
- "找找有没有类似的"
- "搜索一下 XXX 功能"
- "这是不是已经有现成方案了？"
- 开始一个新功能开发之前

**核心原则：先搜，再做。**

## 先决定你用哪种搜索方式

### 方式一：直接使用 Skills CLI

Skills CLI（`npx skills`）可以直接搜索：

```bash
npx skills find [关键词]
```

### 方式二：先安装独立 `find-skills` 项目

如果你的团队工作流依赖独立 Skill 版本，请先按所选仓库 README 安装：

```bash
npx skills add <仓库地址> --skill find-skills -g -y
```

安装完成后，再按对应项目的说明调用它。

## Skills CLI 常用命令

`npx skills` 是 Agent Skill 生态的包管理器。Skill 是模块化能力包，每个 Skill 包含 specialized knowledge、workflows 和 tools。

| 命令 | 作用 |
|------|------|
| `npx skills find [关键词]` | 搜索 Skill |
| `npx skills add <包名>` | 安装 Skill |
| `npx skills list` | 列出已安装的 Skill |
| `npx skills check` | 检查更新 |

**浏览 Skill 市场：** https://skills.sh/

## 搜索流程

### 第一步：理解需求

抓住三个要素：
1. **领域** - React？测试？部署？设计？
2. **具体任务** - 写测试？创建动画？Review PR？
3. **通用性** - 这个任务够常见吗？有没有现成 skill 的可能性？

### 第二步：先看 Leaderboard

在运行 CLI 搜索前，先看一眼 [skills.sh leaderboard](https://skills.sh/)，看该领域是否已有知名 skill。
Leaderboard 按安装量排序，最靠谱的方案在最前面。

常见优质来源：
- `vercel-labs/agent-skills` — React、Next.js、Web 设计（100K+ 安装）
- `anthropics/skills` — 前端设计、文档处理（100K+ 安装）

### 第三步：执行搜索

```bash
npx skills find [关键词]
```

示例：
- 用户问 "React 性能优化" → `npx skills find react performance`
- 用户问 "帮我做 PR review" → `npx skills find pr review`
- 用户问 "创建 changelog" → `npx skills find changelog`

### 第四步：推荐前先验证质量

**不要仅凭搜索结果就直接推荐。** 先确认：

1. **安装量** — 优先选 1K+ 安装的。100 以下要谨慎。
2. **来源可靠性** — 官方来源（`vercel-labs`、`anthropics`、`microsoft`）比不知名作者更可信。
3. **GitHub Stars** — 去源仓库看一眼。Stars < 100 的 skill 要打折扣。

### 第五步：呈现结果

告诉用户：
1. Skill 名称和功能
2. 安装量和来源
3. 安装命令
4. 了解更多链接

示例：

```
找到一个可能合适的 skill！"react-best-practices" skill 提供 React 和 Next.js 性能优化指南，来自 Vercel 工程团队（185K 安装）。

安装命令：
npx skills add vercel-labs/agent-skills@react-best-practices

了解更多：https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### 第六步：帮助安装

如果用户决定安装：

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` 表示全局安装（用户级别），`-y` 跳过确认。

## 常见搜索分类

| 分类 | 搜索关键词 |
|------|-----------|
| Web 开发 | react, nextjs, typescript, css, tailwind |
| 测试 | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| 文档 | docs, readme, changelog, api-docs |
| 代码质量 | review, lint, refactor, best-practices |
| 设计 | ui, ux, design-system, accessibility |
| 效率工具 | workflow, automation, git |

## 搜索技巧

1. **关键词要具体** — "react testing" 比单独的 "testing" 更精准
2. **同义词替换** — "deploy" 搜不到试试 "deployment" 或 "ci-cd"
3. **查热门来源** — 很多 skill 来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`

## 搜不到怎么办

如果确实没有现成方案：

1. 坦诚告知没找到匹配结果
2. 表示可以直接用现有能力帮用户完成这个任务
3. 建议用户可以自己创建 skill：`npx skills init my-xyz-skill`

示例回复：

```
我搜了 "xyz" 相关的 skill，没有找到匹配结果。
不过我可以直接帮你做这件事！需要我动手吗？

如果你经常需要这个功能，也可以自己创建一个 skill：
npx skills init my-xyz-skill
```

## 相关链接

- [Skills.sh 市场](https://skills.sh/)
- [Vercel Skills 官方仓库](https://github.com/vercel-labs/skills)
- [本项目 Skill 开发规范](../../04-创建Skill/SKILL-DEV-GUIDE.md)
