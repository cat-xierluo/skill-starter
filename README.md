# Skills Starter

Skill 开发启动模板仓库，面向 OpenClaw、Claude Code 和 Skills CLI 生态。

这个仓库现在承担六件事：

- 解释 Skill 的核心概念和基础工具链
- 作为一个需求分流入口，先判断是否已有现成 Skill 可复用
- 提供一个可直接复制的 `skill-template`
- `skills/` 下提供多个真实在用的 Skill 可直接参考（`skill-template`、`find-skills`、`skill-creator`、`git-batch-commit`、`skill-manager`）
- 整理 Claude 官方 Skills / context / best practices / PDF 资料
- 为本仓库自身提供可持续迭代的协作文档体系

## 适合谁

- AI 新手：想先理解 Skill 是什么、怎么触发、怎么组织目录
- Skill 开发者：想快速搭一个规范、可维护的 Skill 仓库
- 团队维护者：想给多个 Agent 留下可追踪的任务、决策和路线图

## 你会得到什么

- 一份可复用的 Skill 模板
- 一套协作文档骨架：`CHANGELOG.md`、`docs/`
- 一组从概念到实操的中文文档
- 一份 Claude 官方 Skills / context / best practices 资料导航

## 与 legal-skills 的同步关系

`skills/git-batch-commit/` 和 `skills/skill-manager/` 的上游均为 [legal-skills](https://github.com/cat-xierluo/legal-skills)，但同步策略不同：前者当前是无本地补丁的镜像，可按目录覆盖；后者已经是带回归测试的本地派生版，必须先比较再合并，不能直接覆盖。其余 3 个来源不同：

- `skill-template/`:starter 仓库原创,不从 upstream 同步。
- `skill-creator/`:来自 Anthropic 官方 [anthropics/skills](https://github.com/anthropics/skills) 仓库,本仓库收录内置,暂不从 upstream 自动同步。
- `find-skills/`:来自第三方 [vercel-labs/skills](https://github.com/vercel-labs/skills) 仓库(即 Skills CLI / skills.sh 上游),本仓库收录内置,暂不从 upstream 自动同步。

- legal-skills 作为只读 remote:`git remote add legal-skills https://github.com/cat-xierluo/legal-skills.git`
- `git-batch-commit` 同步命令：`git fetch legal-skills main && git checkout legal-skills/main -- skills/git-batch-commit`
- `skill-manager` 同步前对比：`git fetch legal-skills main && git diff legal-skills/main -- skills/skill-manager`；保留 DEC-020、DEC-034 的本地补丁后再合并

## 学习入口

本仓库有两种用法，按你的情况选：

- **零基础顺序学习**：按 `docs/CONTENT-MATRIX.md` 的学习主线，从 `01-概念入门/` → `02-工具指南/` → `03-AI协作与上下文/` → `04-创建Skill/` 顺序读。新增主线文章普遍提供「前置知识」和「下一篇」；较早文章仍在按写作规范复核。
- **已有经验，按问题查阅**：看下方「资源导航」表格，直接跳到能回答你问题的文章。

教程写作遵循 `docs/WRITING-GUIDE.md`（统一结构、贯穿示例项目 `todo.py`、跨平台标注）。

## 默认使用路径

这个仓库不是只教你“怎么从零写 Skill”，而是先帮你判断要不要自己写。

1. 先用自然语言说清楚你的需求、目标和约束。
2. 先用项目内置 `find-skills` 或 Skills CLI 搜现成方案。
3. 如果已有 Skill 基本可用，优先直接使用，或在现有方案上做定向调整。
4. 只有在找不到合适方案，或者你明确需要自定义实现时，再进入 `04-创建Skill/` 和 `skills/skill-template/` 的创建流程。

## 5 分钟快速开始

### 第一步：先搜现成方案

如果你在这个仓库里用 Claude Code，项目已经按 `legal-skills` 的方式把根目录 `skills/` 暴露给了 `.claude/skills`：

```text
.claude/skills -> ../skills
.claude/skills/find-skills/
```

也可以直接用 Skills CLI 自带搜索：

```bash
npx skills find react performance
```

也就是说，Claude Code 实际从 `.claude/skills/` 读取项目内 Skill，而仓库里真正维护的源文件在根目录 `skills/` 中。

### 多 Agent 共享

为了支持多个 Agent 在同一个项目里协作，本仓库还为以下 Agent 创建了相对符号链接：

```text
.agents/skills      -> ../.claude/skills
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

### 第三步：按 profile 改文件

1. `SKILL.md`：填写 `name` 和 `description`
2. `LICENSE.txt`：确认许可证文本与 frontmatter 一致
3. `ROADMAP.md`、`TASKS.md`、`DECISIONS.md`、`CHANGELOG.md`：留下可维护上下文
4. 最小说明型可删除 `scripts/`、`assets/`、`.env.example` 和 `output/`
5. 带脚本维护型再实现 `scripts/`，并让 `.env.example`、`assets/config.yaml.example` 中的字段都被真实读取

### 第四步：跑通一个最小流程

```bash
python3 scripts/main.py --task "describe what this skill should do"
```

### 第五步：参考真实 Skill

`skills/` 下已有多个真实在用的 Skill 可直接参考,例如 `skill-template/`(starter 原创骨架模板)、`skill-creator/`(收录自 [anthropics/skills](https://github.com/anthropics/skills))、`git-batch-commit/`(同步自 [legal-skills](https://github.com/cat-xierluo/legal-skills))。

## 项目结构

```text
skill-starter/
├── README.md
├── CHANGELOG.md
├── AGENTS.md
├── CLAUDE.md
├── LICENSE.txt
├── requirements-check.txt
├── .claude/
│   └── skills -> ../skills
├── .agents/
│   └── skills -> ../.claude/skills
├── .codex/
│   └── skills -> ../.claude/skills
├── .openclaw/
│   └── skills -> ../.claude/skills
├── .workbuddy/
│   └── skills -> ../.claude/skills
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CONTENT-MATRIX.md
│   ├── DECISIONS.md
│   ├── ROADMAP.md
│   ├── SOURCE-INDEX.md
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
│   ├── 04-调试与发布.md
│   └── 05-第三方-Skill-安全审查.md … 09-触发质量与eval.md
├── 05-参考资料/
├── scripts/                  # 统一检查入口与静态校验
├── tests/                    # YAML、skill-manager、模板复制回归测试
└── skills/
    ├── skill-template/        # starter 原创：Skill 仓库骨架模板
    ├── find-skills/           # 收录自 vercel-labs/skills：仓库内 Skill 检索
    ├── git-batch-commit/      # 同步自 legal-skills：批量提交拆分
    ├── skill-creator/         # 收录自 anthropics/skills：Skill 创建工作流
    └── skill-manager/         # 同步自 legal-skills：多 Agent 安装管理
```

## 资源导航

| 你想做什么 | 去哪里 |
|-----------|--------|
| 理解 Skill 是什么 | `01-概念入门/01-什么是-Skill.md` |
| 理解许可证和开源授权 | `01-概念入门/02-什么是-许可证.md` |
| 补 Git 和 GitHub 基础 | `02-工具指南/` |
| 学提交规范与推送流程 | `02-工具指南/04-提交到-GitHub-与-Commit-规范.md` |
| 学 PR 与 Code Review | `02-工具指南/05-GitHub-PR-与-Code-Review.md` |
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
| 直接用项目内置 find-skills | `.claude/skills/find-skills/`（源文件在 `skills/find-skills/`） |
| 复制模板 | `skills/skill-template/` |
| 查看项目路线图 | `docs/ROADMAP.md` |

## 推荐外部资源

- [skills](https://github.com/vercel-labs/skills)
- [skills.sh](https://skills.sh/)
- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
- [Claude Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

## 当前成熟度与已知限制

本仓库仍在早期迭代，尚未正式发布，以下几点请知悉：

- `01-概念入门/` 至 `04-创建Skill/` 的主线文章已经落盘，但较早文章的统一结构复核、命令复跑和零基础读者实操仍未完成。
- `scripts/check.sh` 已覆盖脚本语法、自动化回归测试、Markdown 相对链接和 Skill frontmatter；CI 会安装 PyYAML 并按严格模式运行。**检查通过仍不代表真实 Agent 触发和真人学习体验已经验收。**
- `skill-manager` 的安装/更新、YAML 严格校验和模板独立复制已有自动化测试；标准示例和四类真实 Agent 触发验证仍待建设。
- main 已配置 required status check，但管理员仍可直接推送；当前门禁对管理员属于提交后检测，不应理解为所有改动都强制经过 PR。
- `skills/` 下收录的第三方 Skill(`find-skills`、`skill-creator`)以“可直接参考/调用”的方式内置,不保证与上游实时一致;如需最新版本,请到对应上游仓库获取。
- 整体处于“可用但仍在打磨”的阶段,欢迎使用和反馈,但暂不建议作为生产环境的强依赖。

## 许可证

本仓库为混合来源仓库：

- **原创内容**（根级教程 Markdown、`docs/`、`scripts/`、`skills/skill-template/`）采用 **MIT** 许可证（见根目录 `LICENSE.txt`）。
- **第三方 Skill** 各自保留原许可证，**不受**根 LICENSE 覆盖：

  | 目录 | 上游 | 许可证 |
  | :--- | :--- | :--- |
  | `skills/git-batch-commit` | [legal-skills](https://github.com/cat-xierluo/legal-skills) | MIT |
  | `skills/skill-manager` | [legal-skills](https://github.com/cat-xierluo/legal-skills) | MIT |
  | `skills/skill-creator` | [anthropics/skills](https://github.com/anthropics/skills) | Apache-2.0 |
  | `skills/find-skills` | [vercel-labs/skills](https://github.com/vercel-labs/skills) | MIT（目录已保留上游 LICENSE） |

  完整来源、同步 commit SHA、本地补丁见 `docs/SOURCE-INDEX.md`；方案讨论见 `docs/LICENSE-PLAN.md`。

使用或再分发时，请同时遵守根 LICENSE 与各第三方目录内的许可证条款；若两者冲突，针对相应目录的内容以第三方许可证优先。

## 维护说明

本仓库本身也按 Skill 项目来维护：

- 对外可见的变更写入 `CHANGELOG.md`
- 中长期规划写入 `docs/ROADMAP.md`
- 当前任务写入 `docs/TASKS.md`
- 决策和工作日志写入 `docs/DECISIONS.md`
- 提交前跑 `bash scripts/check.sh`；需与 CI 完全对齐时运行 `STRICT_LINKS=1 STRICT_SH_SYNTAX=1 STRICT_SKILL_YAML=1 bash scripts/check.sh`

单个 Skill 内部则参考 `legal-skills` 的扁平做法：

- `CHANGELOG.md`
- `ROADMAP.md`
- `TASKS.md`
- `DECISIONS.md`

## 致谢

基于 [legal-skills](https://github.com/cat-xierluo/legal-skills) 的实践经验整理，并结合 Skills CLI 生态做了补充。
