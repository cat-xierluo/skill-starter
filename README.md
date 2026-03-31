# Skills Starter

Skill 开发启动模板仓库，面向 OpenClaw、Claude Code 和 Skills CLI 生态。

这个仓库现在承担五件事：

- 解释 Skill 的核心概念和基础工具链
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
- 一套协作文档骨架：`CHANGELOG.md`、`docs/`、`status/`
- 一组从概念到实操的中文文档
- 一份 Claude 官方 Skills / context / best practices 资料导航

## 5 分钟快速开始

### 第一步：先搜现成方案

推荐先用 Skills CLI 自带搜索：

```bash
npx skills find react performance
```

如果你希望通过独立 Skill 方式引导搜索流程，请先安装你选择的 `find-skills` 项目；本仓库的 `skills/find-skill/SKILL.md` 是安装和使用说明，不是外部项目源码本体。

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
6. `ROADMAP.md`、`TASKS.md`、`DECISIONS.md`
7. `CHANGELOG.md`

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
├── SKILL-DEV-GUIDE.md
├── SKILL-ORCHESTRATION-GUIDE.md
├── docs/
│   ├── ARCHITECTURE.md
│   └── ROADMAP.md
├── status/
│   ├── TASKS.md
│   └── DECISIONS.md
├── 01-概念入门/
├── 02-工具指南/
├── 03-AI协作与上下文/
├── 04-创建Skill/
├── 05-参考资料/
└── skills/
    ├── skill-template/
    ├── find-skill/
    └── weekly-weather-briefing/
```

## 资源导航

| 你想做什么 | 去哪里 |
|-----------|--------|
| 理解 Skill 是什么 | `01-概念入门/01-什么是-Skill.md` |
| 补 Git 和 GitHub 基础 | `02-工具指南/` |
| 学提交规范与推送流程 | `02-工具指南/04-提交到-GitHub-与-Commit-规范.md` |
| 理解 AGENTS.md / CLAUDE.md | `03-AI协作与上下文/02-什么是-AGENTS和-CLAUDE.md` |
| 学 Vibe Coding / 上下文工程 / Rules | `03-AI协作与上下文/` |
| 从零创建一个 Skill | `04-创建Skill/03-基于模板创建.md` |
| 搜现成 Skill 方案 | `04-创建Skill/02-搜索现成方案.md` |
| 看完整开发规范 | `SKILL-DEV-GUIDE.md` |
| 看多 Skill 编排 | `SKILL-ORCHESTRATION-GUIDE.md` |
| 看 Claude 官方 Skill 资料 | `05-参考资料/08-Claude-官方-Skill-资料导航.md` |
| 看 Claude 官方最佳实践清单 | `05-参考资料/10-Claude-Skill-最佳实践清单.md` |
| 看 Claude Code 的上下文 / memory / settings | `05-参考资料/09-Claude-Code-上下文与记忆.md` |
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
- 当前任务写入 `status/TASKS.md`
- 决策和工作日志写入 `status/DECISIONS.md`

单个 Skill 内部则参考 `legal-skills` 的扁平做法：

- `CHANGELOG.md`
- `ROADMAP.md`
- `TASKS.md`
- `DECISIONS.md`

## 致谢

基于 [legal-skills](https://github.com/cat-xierluo/legal-skills) 的实践经验整理，并结合 Skills CLI 生态做了补充。
