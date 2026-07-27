# Skills Starter

Skill 开发启动模板仓库，面向 OpenClaw、Claude Code 和 Skills CLI 生态。

这个仓库现在承担六件事：

- 解释 Skill 的核心概念和基础工具链
- 作为一个需求分流入口，先判断是否已有现成 Skill 可复用
- 提供一个可直接复制的 `skill-template`
- 提供一个带 `CHANGELOG.md`、`ROADMAP.md`、`TASKS.md`、`DECISIONS.md` 的完整示例 Skill
- 整理 Claude 官方 Skills / context / best practices / PDF 资料
- 为本仓库自身提供可持续迭代的协作文档体系

## 适合谁

- AI 新手：想先理解 Skill 是什么、怎么触发、怎么组织目录
- Skill 开发者：想快速搭一个规范、可维护的 Skill 仓库
- 团队维护者：想给多个 Agent 留下可追踪的任务、决策和路线图

## 你会得到什么

- 一份可复用的 Skill 模板
- 一份完整示例 `skills/weekly-weather-briefing/`
- 一套协作文档骨架：`CHANGELOG.md`、`docs/`
- 一组从概念到实操的中文文档
- 一份 Claude 官方 Skills / context / best practices 资料导航

## 与 legal-skills 的同步关系

`skills/git-batch-commit/` 和 `skills/skill-manager/` 通过 `git fetch legal-skills main` + `git checkout legal-skills/main -- skills/<name>` 从 [legal-skills](https://github.com/cat-xierluo/legal-skills) 同步最新内容;另外 3 个(`skill-template` / `find-skills` / `skill-creator`)是 starter 仓库原创,不从 upstream 同步。

- legal-skills 作为只读 remote:`git remote add legal-skills https://github.com/cat-xierluo/legal-skills.git`
- 同步命令:`git fetch legal-skills main && git checkout legal-skills/main -- skills/git-batch-commit skills/skill-manager`
- 同步前可对比:`git diff skill-starter/main legal-skills/main -- skills/<name>`

## 默认使用路径

这个仓库不是只教你“怎么从零写 Skill”，而是先帮你判断要不要自己写。

1. 先用自然语言说清楚你的需求、目标和约束。
2. 先用项目内置 `find-skill` 或 Skills CLI 搜现成方案。
3. 如果已有 Skill 基本可用，优先直接使用，或在现有方案上做定向调整。
4. 只有在找不到合适方案，或者你明确需要自定义实现时，再进入 `04-创建Skill/` 和 `skills/skill-template/` 的创建流程。

## 5 分钟快速开始

### 第一步：先搜现成方案

如果你在这个仓库里用 Claude Code，项目已经按 `legal-skills` 的方式把根目录 `skills/` 暴露给了 `.claude/skills`：

```text
.claude/skills -> ../skills
.claude/skills/find-skill/
```

也可以直接用 Skills CLI 自带搜索：

```bash
npx skills find react performance
```

也就是说，Claude Code 实际从 `.claude/skills/` 读取项目内 Skill，而仓库里真正维护的源文件在根目录 `skills/` 中。

### 多 Agent 共享

为了支持多个 Agent 在同一个项目里协作，本仓库还为以下 Agent 创建了相对符号链接：

```text
.codex/skills       -> ../.claude/skills
.openclaw/skills    -> ../.claude/skills
.workbuddy/skills   -> ../.claude/skills
```

`.claude/skills` 仍是唯一的技能来源；其他 Agent 通过两层符号链接共享同一套 Skill，**不复制、不双写**。本地配置（如 `.codex/settings.local.json`）继续按 `.gitignore` 约定被忽略。

### 第二步：复制模板

在当前 starter 仓库内练习：

```bash
cp -r skills/skill-template skills/my-awesome-skill
cd skills/my-awesome-skill
```

如果你要新开一个独立 Skill 仓库：

```bash
cp -r skills/skill-template ../my-awesome-skill
cd ../my-awesome-skill
```

### 第三步：至少改这几类文件

1. `SKILL.md`：填写 `name` 和 `description`
2. `scripts/`：实现核心逻辑
3. `references/`：补充按需加载的参考资料
4. `.env.example`：环境变量模板
5. `assets/config.yaml.example`：结构化配置模板
6. `LICENSE.txt`：许可证文本
7. `ROADMAP.md`、`TASKS.md`、`DECISIONS.md`
8. `CHANGELOG.md`

### 第四步：跑通一个最小流程

```bash
python3 scripts/main.py --task "describe what this skill should do"
```

### 第五步：看完整示例

如果你想直接参考一个带协作文档体系的实际样例，优先看：

- `skills/weekly-weather-briefing/`

## 项目结构

```text
skill-starter/
├── README.md
├── CHANGELOG.md
├── AGENTS.md
├── CLAUDE.md
├── .claude/
│   └── skills -> ../skills
├── .codex/
│   └── skills -> ../.claude/skills
├── .openclaw/
│   └── skills -> ../.claude/skills
├── .workbuddy/
│   └── skills -> ../.claude/skills
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   ├── ROADMAP.md
│   └── TASKS.md
├── 01-概念入门/
├── 02-工具指南/
├── 03-AI协作与上下文/
├── 04-创建Skill/
│   ├── SKILL-DEV-GUIDE.md
│   ├── SKILL-ORCHESTRATION-GUIDE.md
│   ├── 01-需求分析.md
│   ├── 02-搜索现成方案.md
│   ├── 03-基于模板创建.md
│   └── 04-调试与发布.md
├── 05-参考资料/
└── skills/
    ├── skill-template/        # starter 原创：Skill 仓库骨架模板
    ├── find-skills/           # starter 原创：仓库内 Skill 检索
    ├── git-batch-commit/      # 同步自 legal-skills：批量提交拆分
    ├── skill-creator/         # starter 原创：Skill 创建工作流
    └── skill-manager/         # 同步自 legal-skills：多 Agent 安装管理
```

## 资源导航

| 你想做什么 | 去哪里 |
|-----------|--------|
| 理解 Skill 是什么 | `01-概念入门/01-什么是-Skill.md` |
| 理解许可证和开源授权 | `01-概念入门/02-什么是-许可证.md` |
| 补 Git 和 GitHub 基础 | `02-工具指南/` |
| 学提交规范与推送流程 | `02-工具指南/04-提交到-GitHub-与-Commit-规范.md` |
| 理解 AGENTS.md / CLAUDE.md | `03-AI协作与上下文/02-什么是-AGENTS和-CLAUDE.md` |
| 学 Vibe Coding / 上下文工程 / Rules | `03-AI协作与上下文/` |
| 从零创建一个 Skill | `04-创建Skill/03-基于模板创建.md` |
| 搜现成 Skill 方案 | `04-创建Skill/02-搜索现成方案.md` |
| 看完整开发规范 | `04-创建Skill/SKILL-DEV-GUIDE.md` |
| 看多 Skill 编排 | `04-创建Skill/SKILL-ORCHESTRATION-GUIDE.md` |
| 看 Claude 官方 Skill 资料 | `05-参考资料/08-Claude-官方-Skill-资料导航.md` |
| 看 Claude 官方最佳实践清单 | `05-参考资料/10-Claude-Skill-最佳实践清单.md` |
| 看 Claude Code 的上下文 / memory / settings | `05-参考资料/09-Claude-Code-上下文与记忆.md` |
| 看许可证官方参考 | `05-参考资料/12-许可证与开源授权参考.md` |
| 直接用项目内置 find-skill | `.claude/skills/find-skill/`（源文件在 `skills/find-skill/`） |
| 复制模板 | `skills/skill-template/` |
| 参考完整示例 | `skills/weekly-weather-briefing/` |
| 查看项目路线图 | `docs/ROADMAP.md` |

## 推荐外部资源

- [skills](https://github.com/vercel-labs/skills)
- [skills.sh](https://skills.sh/)
- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
- [Claude Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

## 维护说明

本仓库本身也按 Skill 项目来维护：

- 对外可见的变更写入 `CHANGELOG.md`
- 中长期规划写入 `docs/ROADMAP.md`
- 当前任务写入 `docs/TASKS.md`
- 决策和工作日志写入 `docs/DECISIONS.md`

单个 Skill 内部则参考 `legal-skills` 的扁平做法：

- `CHANGELOG.md`
- `ROADMAP.md`
- `TASKS.md`
- `DECISIONS.md`

## 致谢

基于 [legal-skills](https://github.com/cat-xierluo/legal-skills) 的实践经验整理，并结合 Skills CLI 生态做了补充。
