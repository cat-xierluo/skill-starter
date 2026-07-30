# 项目架构

> Last updated: 2026-07-30
>
> 当前缺陷与验收状态以 [TASKS.md](./TASKS.md) 为准；本文只描述稳定的结构与职责边界。

## 定位

`skill-starter` 是一个面向 Skill 开发的教学型脚手架仓库，不是单个 Skill。它同时提供：

- 学习资料
- 可复制模板
- `skills/` 下真实在用的 Skill 参考
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
- `.agents/skills`、`.codex/skills`、`.openclaw/skills`、`.workbuddy/skills`：复用同一来源的其他 Agent 入口
- `skills/skill-template/`：支持最小说明型与带脚本维护型两种 profile 的标准起点模板
- `skills/find-skills/`：搜索外部 Skill 的引导文档
- `skills/git-batch-commit/`、`skills/skill-manager/`：来自 legal-skills 的实际维护工具，其中 skill-manager 是带本地补丁的派生版
- `skills/skill-creator/`：收录自 Anthropic 的 Skill 创建与 eval 工作流

### 3. 仓库治理层

负责项目本身的迭代和协作。

- `CHANGELOG.md`：记录对外可见变更
- `docs/ROADMAP.md`：阶段目标和路线图
- `docs/TASKS.md`：当前任务状态
- `docs/DECISIONS.md`：决策与工作日志
- `docs/CONTENT-MATRIX.md`：文章编号与发布状态
- `docs/SOURCE-INDEX.md`：内置 Skill 的来源、版本和许可证事实
- `.claude/commands/sync-upstream.md`：按新增、镜像和派生版三类处理上游同步，固定只读 remote、时间/SHA 备份、依赖核对和失败回退协议

### 4. 质量验证层

负责阻止断链、非法 frontmatter 和更新器假成功进入主线。

- `scripts/check.sh`：本地与 CI 共用的统一入口
- `scripts/check_links.py`：默认离线检查 Markdown 相对链接、锚点和引用式链接；显式 `--check-external` 时并行核验外链，支持重试、允许清单和来源定位
- `scripts/external_links_allowlist.txt`：记录已由官方入口交叉确认、但不适合自动请求判断的外链 glob
- `scripts/check_skills.py`：严格 YAML 与 Skill 结构检查
- `tests/`：skill-manager、YAML 解析、模板独立复制、外链故障分级和上游同步 Git 协议回归测试
- `.github/workflows/check.yml`：安装固定检查依赖并运行严格模式
- `.github/workflows/check-external-links.yml`：每周或手动运行外链核验，与普通 push / PR 门禁解耦

## 设计原则

### 文档优先

Starter 的核心价值在于把经验沉淀为可复制文档，而不是只放一个模板目录。

### 概念、工具、上下文分层

Git / GitHub / commit 属于基础工具；Vibe Coding、`AGENTS.md`、`CLAUDE.md`、Rules 属于 AI 协作方法。两者相关，但不应混在同一层里。

### 模板与示例分离

模板负责最小可用结构，示例负责展示一套完整做法。这样既不让模板过重，也不让新人缺少参考。

### 协作文档默认存在

复杂 Skill 或长期维护的 Skill，默认应该带上 `ROADMAP.md`、`TASKS.md`、`DECISIONS.md` 和 `CHANGELOG.md`；是否再使用 `docs/` 子目录由具体项目规模决定。重要上下文不能只留在聊天里。

## 后续演进方向

- 建立一个 starter 原创、可端到端运行的标准示例 Skill
- 增加真实 Agent 的正例、负例、执行和错误输入验证
- 复核较早教程结构并完成零基础读者实操验收
