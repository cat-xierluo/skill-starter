# 决策记录与工作日志

## 决策记录

### [DEC-025] - 2026-07-28 - Wave 4 OTA：首批严格遵循 WRITING-GUIDE 的文章，review 仅 1 Critical

**背景** Wave 3 把 review 教训 codify 进 `docs/WRITING-GUIDE.md` 后，Wave 4 是首轮 worker 被要求「先 Read WRITING-GUIDE + CONTENT-MATRIX 再动笔」的批次。

**决策** Wave 4 三个 worker prompt 都加了「务必先 Read docs/WRITING-GUIDE.md 与 docs/CONTENT-MATRIX.md 再动笔」，从源头约束结构/计数/术语/收尾/跨篇/事实。

**影响** 7 篇产出 + merge（0.17.0）。writing-reviewer 本轮 **1 Critical（错字）+ ~12 Important**——结构/计数/术语括注/收尾/跨篇引用高度合规（前几轮的「计数错、收尾同质、术语不括注」共性问题基本消除）。剩余 Important 多为事实/逻辑/模板一致性（LICENSE.txt 模板不带、todos.json 路径、`/skill` 语义、自动备份 vs 裸 git 等），PM 已修。这进一步证明「规范前置 + worker 遵循」是可复制的质量改进闭环，比逐轮 review 返工更高效。

### [DEC-024] - 2026-07-28 - Wave 3 课程结构前置：PM 直接做（规范工作）

**背景** Wave 1/2 内容批次后，TASKS P1 要求先做课程结构前置（内容矩阵 / 统一结构 / README 双入口）再继续写文章，避免边写边重排编号。

**决策** PM 直接做，不派 OTA worker。理由：① 规范文档连贯性强，1 个任务无并行优势；② 需全局视角（梳理已写 10 篇 + 规划剩余 + codify 两轮 review 教训），PM 掌握全貌；③ §2 例外允许 PM 写编排/规范文档。

**影响** 新增 `docs/CONTENT-MATRIX.md`（编号单一事实源）、`docs/WRITING-GUIDE.md`（统一结构 + 示例项目 todo.py + 跨平台 + Wave 1/2 review 教训 codify），README 加双入口。后续 Wave 写文章须先查 CONTENT-MATRIX 定编号、遵循 WRITING-GUIDE，从源头降低 review 返工。

### [DEC-023] - 2026-07-28 - Wave 2 OTA 内容批次：3 worker 并行写 4 篇安全/可靠性文章，review 0 Critical

**背景** Wave 1（DEC-022）跑通 OTA 流程后，启动 Wave 2（P2 第二批安全与可靠性）。

**决策** 复用 Wave 1 验证的 spawn 配置（mcp 配置文件 + `tmux set-environment` 注入 provider env + send Escape 关 MCP dialog + prompt 内 date/commit 自检），3 worker × glm-5.2 并行：W4 密钥安全、W5 验证AI+上下文生命周期、W6 第三方 Skill 审查。**关键改进：Wave 2 prompt 内置 Wave 1 review 教训**（计数准确/标题名实相符/术语首次括注/收尾别用"不是X而是Y"/macOS-Linux 差异标注/commit 后 `git log` 自检）。

**影响** 4 篇产出 + merge（0.15.0）。writing-reviewer 本轮 **0 Critical + 3 Important**（Wave 1 是 3 Critical + 9 Important）——证明把 review 教训前置进 prompt 能显著降质量风险，是可复制的质量改进闭环。3 Important（`gh auth token` 语义、`lint` 括注、2 类上下文 vs 7 层映射）PM 已修。事实核对全部通过（第三方 Skill 来源/许可证/issue 与 SOURCE-INDEX 一致，无编造）。

### [DEC-022] - 2026-07-28 - Wave 1 OTA 内容批次：3 个 tmux worktree worker 并行写 6 篇地基文章

**背景**
工程批次（DEC-021）后，按用户「用 OTA 推进内容写作」要求，启动 Wave 1 试点（P2 第一批 6 篇地基文章）。`multi-agent-orchestration` skill 把内容写作归为「长上下文、独立提交」场景，应用 tmux 独立 worktree worker（非 Sub Agent）。

**决策**
- 3 个 worker × glm-5.2（同宿主 claude-code，继承 PM 智谱 provider env），按目录分工：W1 写 01-概念入门 2 篇、W2 写 02-工具指南 3 篇、W3 写 03-AI协作 1 篇。文件域天然隔离。
- 每个 worker：独立 worktree + 分支 + tmux session，`templates/worker-prompt.md` 骨架（Isolation Gate / 10 分钟 Heartbeat / Commit 强制 / `status="done"` 字面值），PM 用 sentinel + cron 双层监测、不代写，收口用 writing-reviewer（文档项目）。
- worker 只 commit 到隔离分支，不开 PR、不 push；PM 验收后 merge 到 main。

**理由**
内容写作是项目质量生命线，长上下文 + 风格统一 + 独立提交正是 tmux worker 场景（用户明确指出 Sub Agent 承载不了）。worktree 物理隔离 + scope-guard + sentinel 收口把并行风险控到最低。

**影响 / 经验**
- 6 篇文章全部产出、check.sh 通过、merge 到 main（0.14.0）。
- 踩 6 个坑全解（见 CHANGELOG 0.14.0 Notes），为后续 Wave 沉淀可复用 spawn 配置：mcp 配置文件 + `tmux set-environment -g` 注入 provider env + send Escape 关 MCP dialog + prompt 内置 date 处理说明。
- W1 限流中断漏 commit（§11 Hard Fail #4），PM 手动补；后续 worker prompt 已强化 commit 自检（`git log --oneline main..HEAD` 非空）。
- 待办：writing-reviewer 批量 review 6 篇 + 读者实操验收（P2 真正完成标准）；Wave 2/3 按此模式推进剩余目录。

### [DEC-021] - 2026-07-27 - 用多代理编排并行推进 TASKS.md：工程批次走 Sub Agent，内容批次升级为 OTA tmux worker

**背景**
用户要求按 `docs/TASKS.md` 用 Multi-Agent Orchestration 并行推进，直至完成。TASKS 体量极大，混合了工程修复（P0）、校验/模板/同步（P1）、约 30 篇零基础教程写作（P1 学习主线）与需读者实操的验收（P2）。本仓库已收录 `legal-skills` 的 `multi-agent-orchestration` skill，其 §2 把执行模式分为 PM 直接处理 / 同宿主 Subagent / tmux 独立 CLI session 等，并明确「短任务一发跑完」用 Subagent、长上下文独立提交用 tmux worker。

**选项**
1. 全部任务统一用一种模式（要么全 Sub Agent，要么全 tmux worker）。
2. 按任务性质分流：工程修复（窄范围、可一发跑完、文件域独立）用同宿主 Sub Agent 并行；内容写作（长上下文、独立提交、需风格统一）升级为 OTA tmux worktree worker。
3. 串行逐个推进，不用多代理。

**决策**
选择选项 2。第一批「工程修复 + 校验 + 文档一致性 + 来源索引」拆成 6 个文件域互不重叠的工作包（WP1–WP6），用 Claude Code 同宿主 Sub Agent 并行执行，PM（主会话）负责派工、验收、跑 `check.sh`、收口治理文档。该批次符合 skill §2「同宿主 Subagent = 窄范围/短任务一发跑完」场景。后续内容写作批次将升级为 OTA tmux worktree worker（每目录一 worker、独立分支+PR、`writing-reviewer` review）。

**理由**
- 工程修复是确定性、可客观验证（check.sh / bash -n / 真实场景测试）的短任务，Sub Agent 足够且启动成本低；skill 自身也把这类任务划给 Subagent。
- 内容写作是项目质量生命线，长上下文 + 独立提交 + 风格一致性要求，正是 tmux worktree worker 的场景；Sub Agent 难以承载其复杂度（用户明确指出）。
- 文件域隔离（skills/git-batch-commit、skills/skill-manager/scripts、README+AGENTS、scripts/、docs/ROADMAP+ARCHITECTURE、新建 docs 文件）保证并行安全，收口验证全绿。

**影响 / upstream 处理**
- `skills/git-batch-commit/`：通过 `git checkout legal-skills/main --` 整目录同步至 upstream v1.4.1，**无本地补丁**，符合 AGENTS upstream 优先原则。
- `skills/skill-manager/scripts/update.sh`：upstream 仍有 `grep -oP` + 安装/更新矛盾，**本地修复偏离 upstream**（POSIX sed + `update_via_registry` 双路径），属可回馈 upstream 的本地补丁；待按 TASKS P1 正式标记为 fork/派生版。
- 新增 `docs/SOURCE-INDEX.md`、`docs/LICENSE-PLAN.md`；许可证方案给三选项，**未替仓库选定 LICENSE**（遵循 DEC-013）。
- 收口验证：`update.sh bash -n` PASS、`check.sh` EXIT 0（149 链接有效、5 skill 必需项全齐、严格模式亦通过），仅 7 条 license/CHANGELOG 缺失 warn（真实存量，已入 SOURCE-INDEX）。
- 后续：内容写作批次按 OTA `templates/worker-prompt.md` 骨架启动 worktree worker，PM 不直接写业务内容，收口用 `writing-reviewer`。

### [DEC-020] - 2026-07-27 - 从 legal-skills upstream 同步 `git-batch-commit` 与 `skill-manager`，保留 4 个 starter 原创 skill

**背景**
starter 仓库此前 `skills/` 下有 5 个 skill,其中 `git-batch-commit` 与 upstream(`cat-xierluo/legal-skills`)同名但版本偏旧;`skill-manager` 在 starter 中缺失但 upstream 已成熟(`v1.7.0`),补齐后能让 starter 完整覆盖"创建 → 管理 → 同步"的 Skill 工作流。

**选项**
1. 全量从 legal-skills/skills/ 镜像 65 个 skill
2. 只 cherry-pick 同名 6 个 skill,无差别覆盖本地版本
3. 先 diff、再 cherry-pick、保留备份
4. 只同步确实存在于 upstream 的 skill(用 `git ls-tree` 先核实),其他保留原创

**决策**
选择选项 4 的变体:执行选项 2 的命令,但用 `git ls-tree legal-skills/main skills/` 先核实 upstream 实际目录,发现 `find-skills` / `skill-creator` / `skill-start-update` / `skill-template` 在 upstream 不存在,这 4 个为 starter 原创,保留本地版本不动;只同步 `git-batch-commit` 和 `skill-manager` 两个确实存在的。

**理由**
- 选项 1 会把法律/专利/OCR/音视频等 60 多个垂直领域 skill 塞进 starter,破坏 starter 定位,且会带入符号链接死链
- 选项 2 缺乏核实步骤,可能误覆盖
- 选项 3 仍不能解决"upstream 根本没有这个 skill"的问题,反而徒增工作量
- 选项 4 既保证同步内容真实存在,又明确每个 skill 的来源(同步 vs 原创),后续维护可追溯

**影响**
- `skills/git-batch-commit/` 从 starter 自有版本升级到 `v1.4.1`(upstream `main` HEAD)
- `skills/skill-manager/` 新增,`v1.7.0`,包含 10 个 scripts + 1 个示例注册表
- 5 个同名 starter skill 备份到 `.starter-backups/<name>/`(`.gitignore` 已排除)
- 新增只读 remote `legal-skills`,URL `https://github.com/cat-xierluo/legal-skills.git`
- `README.md` 项目结构新增同步 vs 原创标注,新增"与 legal-skills 的同步关系"小节
- `AGENTS.md` "上游同步文件"约定扩展到 `skills/` 目录,明确 `git-batch-commit` 和 `skill-manager` 走 upstream
- `CHANGELOG.md` 记录为 `0.9.0 - 2026-07-27`

### [DEC-019] - 2026-07-27 - 为多 Agent 共享同一技能来源，新增 `.codex` / `.openclaw` / `.workbuddy` / `.qoderworkcn` 四个相对符号链接

**背景**
starter 仓库此前只暴露 `.claude/skills` 给 Claude Code,Codex / OpenClaw / WorkBuddy / QoderWork 等 Agent 在本仓库里看不到项目内 Skill,需要各自复制或重新安装。`legal-skills` 生态已经在用 `skill-manager` 的 `init.sh` 处理多 Agent 符号链接,但本仓库希望以最小、可追踪的方式手动落地。

**选项**
1. 跑 `skill-manager init.sh` 自动建链,顺便用 `--gitignore` 把整个 `.{agent}/` 加进 `.gitignore`
2. 手动 `mkdir` + `ln -s` 建四个相对符号链接,`.gitignore` 只忽略本地配置
3. 不创建任何目录,只在文档里说明"请自行运行 skill-manager init"

**决策**
选择选项 2。

**理由**
- 链接是仓库源码的一部分(单一来源),和 `.claude/skills` 一样应该纳入版本管理;选项 1 把整个 Agent 目录忽略会丢掉符号链接本身
- 选项 3 把责任推给下游用户,starter 自身缺乏多 Agent 实操样板
- 手动建链可审计、可回滚,不需要额外依赖已安装的 `skill-manager`

**影响**
- 项目根目录新增 `.codex/`、`.openclaw/`、`.workbuddy/`、`.qoderworkcn/` 四个目录,各自携带 `skills -> ../.claude/skills` 相对符号链接
- `.gitignore` 按现有 `.claude/*` 模式追加各 Agent 的 `settings.local.json` / `*.local.*` / `.DS_Store` 忽略项
- `README.md` 项目结构和"多 Agent 共享"小节、`AGENTS.md` Project-local Skills 约定小节同步更新
- `CHANGELOG.md` 记录为 0.8.0 版本

### [DEC-001] - 2026-03-30 - 协作文档默认纳入 starter 和模板

**背景**
仓库此前只有教学文档和基础模板，缺少路线图、任务状态和决策日志，导致长期维护和多 Agent 协作缺少上下文。

**选项**
1. 只给 starter 仓库补文档，不改模板
2. 同时给 starter 和模板都补上协作文档骨架

**决策**
选择选项 2。

**理由**
如果只有仓库本身有协作文档，用户复制模板出去以后仍然要自己重搭一遍；把这套结构直接放进模板，复用价值更高。

**影响**
`skill-template` 会更完整，示例 Skill 也能展示完整维护方式。

### [DEC-002] - 2026-03-30 - `.env.example` 与 `assets/` 配置模板分开维护

**背景**
现有文档把所有模板都笼统归入 `assets/`，但环境变量模板和结构化配置模板在维护方式上不同。

**选项**
1. 所有模板文件都放 `assets/`
2. `.env.example` 放 Skill 根目录，结构化配置模板放 `assets/`

**决策**
选择选项 2。

**理由**
`.env.example` 更适合作为仓库根目录的显式入口，便于用户复制为 `.env`；`config.yaml.example` 之类的结构化配置模板保留在 `assets/` 更清晰。

**影响**
相关指南、模板和示例都按这个约定统一。

### [DEC-003] - 2026-03-30 - `find-skill` 在 starter 中定位为引导文档

**背景**
仓库内已有 `skills/find-skill/`，容易让人误以为外部搜索能力已经内置在 starter 里。

**选项**
1. 保持原状
2. 将其明确为搜索引导文档，并说明实际搜索可用 Skills CLI 或先安装独立项目

**决策**
选择选项 2。

**理由**
这样既保留教学价值，也避免误导使用者。

**影响**
README、教程和 `skills/find-skill/SKILL.md` 都需要同步调整。

### [DEC-004] - 2026-03-30 - 单个 Skill 内部协作文档采用根目录扁平结构

**背景**
先前模板和示例把协作文档放到了 `docs/`、`status/` 二级目录中，但用户确认希望对齐 `legal-skills` 的内部组织方式。

**选项**
1. 继续在单个 Skill 内使用 `docs/` 和 `status/`
2. 保留 starter 仓库级别的 `docs/`、`status/`，但单个 Skill 改为根目录扁平文档

**决策**
选择选项 2。

**理由**
这样既保留 starter 仓库自身的项目级治理结构，也让模板和示例更贴近 `legal-skills` 的真实维护方式。

**影响**
`skill-template` 和 `weekly-weather-briefing` 需要改为根目录 `ROADMAP.md`、`TASKS.md`、`DECISIONS.md`。

### [DEC-005] - 2026-03-30 - 基础教程按“能独立上手”而非“仅概念解释”重写

**背景**
现有 `Vibe Coding`、`GitHub`、`Git`、`SSH` 教程偏概念化，对新手来说知道名词，但仍然不知道第一次具体该怎么做。

**选项**
1. 继续保持轻量概念文档
2. 重写为“概念 + 第一次操作流程 + 常见错误 + 下一步阅读”

**决策**
选择选项 2。

**理由**
starter 仓库的目标是让用户少走弯路，基础教程如果不能支持第一次独立操作，就很难真正成为启动模板。

**影响**
`01-概念入门/` 与 `02-工具指南/` 中的多篇文档会显著扩写，并增加彼此之间的交叉引用。

### [DEC-006] - 2026-03-30 - 将官方 Skills 生态资料和上下文机制纳入 starter 默认学习路径

**背景**
当前仓库虽然已经有概念入门、工具指南和创建流程，但还缺少 Claude 官方关于 Skills 的资料地图，以及 `CLAUDE.md`、`settings.json`、上下文记忆机制的系统解释。

**选项**
1. 继续只保留本地二手总结
2. 把官方文档、官方博客、官方 PDF、最佳实践和 context 机制一起纳入仓库

**决策**
选择选项 2。

**理由**
starter 不只是模板仓库，也承担“知识地图”职责。没有官方一手资料导航，用户容易停留在零散经验；没有上下文机制说明，用户会混淆 `AGENTS.md`、`CLAUDE.md` 和 `.claude/settings.json` 的职责。

**影响**
需要新增官方资料导航、最佳实践清单、context 文档，并同步修正旧的官方链接和 `CLAUDE.md` 说明页。

### [DEC-007] - 2026-03-30 - 每个二级目录的文档编号独立从 `01` 开始

**背景**
当前仓库已经把 `01-概念入门`、`02-工具指南`、`03-创建Skill` 做成了目录内独立编号，但 `04-参考资料` 仍保留了全局累加编号和未编号文件，排序逻辑不一致。

**选项**
1. 继续保留全局累加编号和混合命名
2. 每个二级目录都独立从 `01` 开始，并把未编号文件一起纳入排序

**决策**
选择选项 2。

**理由**
目录内独立编号更符合阅读直觉，也更便于后续在单个目录内插入新文档；同时把未编号文件纳入排序，可以让结构和命名规范保持一致。

**影响**
`04-参考资料/` 内的文件需要整体重命名，并同步修正 README、概念文档和参考文档中的相对链接。

### [DEC-008] - 2026-03-31 - 工具指南优先补 Git 提交流程与上下文工程，不展开 GitHub Actions

**背景**
用户明确希望基础工具指南继续下沉到“真正会用 Git、会提交到 GitHub、会写规范 commit、会管理上下文”的层面，而不是扩展到 GitHub Actions 这类更偏平台自动化的话题。

**选项**
1. 继续按 GitHub 功能面扩展，包括 Actions
2. 优先补 Git 提交流程、commit 规范、上下文工程、Rules 编写

**决策**
选择选项 2。

**理由**
对 starter 仓库的目标用户来说，Git、GitHub 提交协作、`AGENTS.md` / `CLAUDE.md` / Rules 的理解属于“基础中的基础”，比自动化平台能力更先影响使用体验和成功率。

**影响**
`02-工具指南/` 将新增 Git 提交规范、上下文工程、Rules 编写三篇文档；现有入口文档会把学习路径导向这些内容，并弱化对 GitHub Actions 的讨论。

### [DEC-009] - 2026-03-31 - 将 Vibe Coding 与上下文工程从工具指南中拆出为独立目录

**背景**
在新增上下文工程和 Rules 文档后，`02-工具指南/` 同时承载了 Git / GitHub 工具和 AI 协作方法，目录职责开始混杂。用户明确希望工具指南聚焦 Git、GitHub 和 commit 规范，而将 Vibe Coding、`AGENTS.md`、`CLAUDE.md`、Rules 归入单独一组。

**选项**
1. 保持现状，让 `02-工具指南/` 同时容纳 Git 工具与上下文工程
2. 拆出独立目录，形成“概念入门 / 工具指南 / AI 协作与上下文 / 创建 Skill / 参考资料”的层次

**决策**
选择选项 2。

**理由**
Git / GitHub / SSH / commit 是开发工具链；Vibe Coding、`AGENTS.md`、`CLAUDE.md`、上下文工程、Rules 是 AI 协作方法。两者相关，但认知层次不同。拆开后阅读路径更清晰，也更符合仓库的教学目标。

**影响**
需要新增 `03-AI协作与上下文/`，把相关文档迁入其中；原 `03-创建Skill/` 和 `04-参考资料/` 顺延为 `04`、`05`，并同步更新 README、架构说明与全部相对链接。

### [DEC-010] - 2026-03-31 - 将 `find-skill` 以内置 project-local Skill 方式随仓库分发

**背景**
用户希望 `find-skill` 在这个 starter 仓库里开箱即用，而不是要求使用者进入项目后再手动安装。与此同时，仓库当前将整个 `.claude/` 目录加入了 `.gitignore`，这会阻止 project-local Skill 被跟踪。

**选项**
1. 继续只保留 `skills/find-skill/` 作为可读范例，不提供内置安装版本
2. 在 `.claude/skills/find-skill/` 中增加 project-local Skill，并调整 `.gitignore`

**决策**
选择选项 2。

**理由**
这更符合 starter 仓库“开箱即用”的目标。将可运行版本放在 `.claude/skills/`，同时保留 `skills/find-skill/` 作为仓库内可读范例，可以兼顾直接使用和教学说明。

**影响**
需要新增 `.claude/skills/find-skill/SKILL.md`，调整 `.gitignore` 只忽略 `.claude` 下的本地配置和元数据文件，并同步更新 README 与“先搜索现成方案”相关文档。

### [DEC-011] - 2026-03-31 - 将 README 的人类使用路径转成 AGENTS 的 AI 检索与分流协议

**背景**
仓库当前已经在 `README.md` 中说明了“先搜现成 Skill，再决定是否创建”的思路，但 `AGENTS.md` 仍停留在通用规范层，没有把这条路径转成 AI 可执行的检索与分流规则。

**选项**
1. 继续保持 `AGENTS.md` 为通用写作与协作规范
2. 将 `AGENTS.md` 升级为与 README 对齐的执行协议，明确默认工作流、目录检索顺序和 project-local Skill 约定

**决策**
选择选项 2。

**理由**
`README.md` 面向人类读者，`AGENTS.md` 面向 AI 代理。如果两者不一致，AI 就无法稳定执行仓库真正的目标。把 README 中的需求分流逻辑写成 AI 协议，才能让“先检索、再复用、最后再创建”真正落地。

**影响**
需要同步更新 `README.md` 与 `AGENTS.md`，并在变更日志与任务状态中记录这一轮协议收敛。

### [DEC-012] - 2026-03-31 - `CHANGELOG.md` 即使未发布也按内部版本号迭代

**背景**
当前 `CHANGELOG.md` 采用单一 `Unreleased` 段落记录改动。用户希望即使仓库尚未正式发布，也要按 `0.1.0`、`0.2.0` 这类版本号来组织迭代历史，便于后续回看阶段性变化。

**选项**
1. 继续维持单一 `Unreleased` 段落
2. 改为按内部迭代版本记录，即使尚未正式发布也使用 `0.x.0` 版本号

**决策**
选择选项 2。

**理由**
这个仓库本身就是一个持续演进的 starter。按版本号记录比单一 `Unreleased` 更容易对应阶段性目标、结构调整和对外可见变化，也更利于后续从 `0.1.0` 平滑推进到 `0.2.0`、`0.3.0`。

**影响**
需要将当前 changelog 内容收敛到 `0.1.0` 版本段，并把这条约定同步写入 `AGENTS.md`，作为后续维护规范的一部分。

### [DEC-013] - 2026-03-31 - 先补许可证说明与落地规范，不擅自替仓库选择具体许可证

**背景**
用户明确指出许可证是重要缺口，需要在 starter 仓库里进行解释说明。当前仓库既缺少许可证概念文档，也缺少在 Skill 创建流程中如何落地 `license` 字段和 `LICENSE.txt` 的说明。

**选项**
1. 直接替仓库默认选择一个具体许可证，并据此生成 `LICENSE`
2. 先补齐许可证概念、官方参考和创建流程说明，但不在用户未指定前擅自替项目选择法律条款

**决策**
选择选项 2。

**理由**
许可证属于重要的法律与分发约定。没有用户明确选择前，不应擅自替仓库决定 `MIT`、`Apache-2.0` 或其他具体条款；但 starter 必须把“为什么需要许可证”“常见差异是什么”“在 Skill 项目里怎么写”讲清楚。

**影响**
需要新增许可证概念文档和官方参考页，并同步修改 README、开发指南、模板说明和创建流程文档；本轮不新增根目录 `LICENSE`，具体许可证由用户后续明确。

### [DEC-014] - 2026-03-31 - 参照 `legal-skills` 抽取许可证管理规范，但不照搬法律项目的特定条款

**背景**
用户要求参照 `legal-skills` 项目中的文档进行抽取后更新。`legal-skills` 已经形成了较成熟的许可证管理规范，但其中包含面向法律技能仓库的特定分类和特定联系信息，不适合直接原样迁入 starter。

**选项**
1. 原样复制 `legal-skills` 的许可证分类、联系人和条款文本
2. 只抽取其中通用的方法论：许可证分类思路、`license`/`LICENSE.txt` 配套规则、README 许可证展示和迁移 Skill 保持原许可

**决策**
选择选项 2。

**理由**
starter 是通用 Skill 创作仓库，不应继承法律项目的业务特定条款或联系人信息；但 `legal-skills` 在许可证治理上的结构化做法很值得复用。抽取方法论、去掉特定业务约束，能让 starter 更通用也更稳。

**影响**
需要更新 `AGENTS.md`、`SKILL-DEV-GUIDE.md`、许可证概念文档与参考文档；本轮不引入 `legal-skills` 中的特定版权署名、商用联系信息或非通用许可证模板。

### [DEC-015] - 2026-03-31 - 许可证说明以授权目标和商业化策略为主线，而不是以 Skill 类型为主线

**背景**
用户指出，starter 的许可证说明不应过多沿用 `legal-skills` 的分类方式，因为很多开发者就是想直接开源；更重要的是让他们理解不同许可证对应怎样的开放方式，以及后续如果想商业化、做授权收益、控制署名和商用边界，需要提前考虑什么。

**选项**
1. 继续保留“工具型 / 内容型 / 迁移型”这类偏类型化的分类思路
2. 改为以授权目标为主线：是否允许商用、是否要求署名、是否要求同协议共享、是否保留后续商业授权空间

**决策**
选择选项 2。

**理由**
starter 面向更广泛的 Skill 开发者，许可证选择首先是授权策略问题，而不是内容类型问题。把重点放在商用权、署名义务、share-alike 和后续商业化空间，更能帮助用户做长期决策。

**影响**
需要重写 `AGENTS.md`、`SKILL-DEV-GUIDE.md`、许可证概念文档和参考文档中的许可证说明结构，使其更偏决策维度而非类型套用。

### [DEC-016] - 2026-03-31 - 根目录 `SKILL-*-GUIDE.md` 作为上游同步文件维护，不在 starter 中手动改写

**背景**
用户明确说明 `SKILL-DEV-GUIDE.md` 这类 guide 文件后续会从 `legal-skills` 项目同步，因此不希望在 starter 仓库里继续手动修改，避免后续同步时出现冲突和漂移。

**选项**
1. 继续在 starter 本地直接维护这些 guide 文件
2. 将根目录 `SKILL-*-GUIDE.md` 视为上游同步文件，默认不手动修改；需要补解释时改其他文档

**决策**
选择选项 2。

**理由**
这类 guide 文件承担“上游规范镜像”的角色。既然后续会从 `legal-skills` 同步，就不应该继续在 starter 中做本地分叉；否则每次同步都会引入额外对齐成本。

**影响**
需要撤回本轮对 `SKILL-DEV-GUIDE.md` 的本地修改，并在 `AGENTS.md` 中明确 `SKILL-*-GUIDE.md` 的维护规则。后续如需补充解释，应优先改 `README.md`、概念文档和参考资料。

### [DEC-017] - 2026-03-31 - 在许可证文档中保留常见许可证对比表，并把派生条款写清楚

**背景**
用户明确希望常见许可证对比表保留下来，并要求把一些“派生 / 衍生”相关的协议条款解释清楚，方便读者在开源、商用和后续授权收益之间做判断。

**选项**
1. 只保留抽象说明，不做表格对照
2. 在许可证文档中加入常见许可证对比表，并单独解释 `SA`、`GPL`、`AGPL`、`ND`、`NC` 这类派生相关条款

**决策**
选择选项 2。

**理由**
许可证最容易让人混淆的就是“表面上都能分享，但派生版本和商用边界差很多”。对比表能让人快速建立整体认知，派生条款说明则能避免用户把“允许看”误解成“允许任意改造并重新分发”。

**影响**
需要更新许可证概念文档与参考资料文档，但不修改上游同步的 `SKILL-DEV-GUIDE.md`。本轮说明继续保持为工程决策参考，而非法律意见。

### [DEC-018] - 2026-03-31 - `skills/` 作为单一来源，通过 `.claude/skills` 符号链接暴露给 Claude Code

**背景**
用户指出当前 starter 仓库把 Skill 同时放在根目录 `skills/` 和 `.claude/skills/` 的双轨模式并不理想。正常能被 Claude Code 直接使用的 Skill 应该位于 `.claude/skills/`，但仓库又需要保留根目录 `skills/` 作为模板、示例和后续新增 Skill 的集中维护位置。

**选项**
1. 继续维护 `.claude/skills/` 与根目录 `skills/` 两套目录
2. 保留根目录 `skills/` 作为单一来源，通过 `.claude/skills -> ../skills` 的符号链接对外暴露

**决策**
选择选项 2。

**理由**
这与 `legal-skills` 的结构一致，也避免了 `find-skill` 这类 Skill 同时存在“可读版”和“可用版”两份副本的问题。以后新增真正可调用的 Skill，只需要放到根目录 `skills/`，Claude Code 就能通过符号链接直接读取。

**影响**
需要将 `SKILL-DEV-GUIDE.md`、`SKILL-ORCHESTRATION-GUIDE.md` 一并收拢到 `04-创建Skill/`，统一 README、AGENTS、教程和参考资料中的路径说明，并把 `.claude/skills` 改为可提交的符号链接。

## 工作日志

### 2026-03-30 11:31 (Codex)

- **目标:** 收敛 starter 仓库的文档结构，并把协作文档模板下沉到模板与示例
- **操作:** 修正根 README、教程路径和链接；新增 starter 级别的 `CHANGELOG.md`、`docs/`、`status/`；增强 `skills/skill-template/`；新增 `skills/weekly-weather-briefing/`；完成脚本 smoke test 与相对链接检查
- **结果:** starter 仓库、模板和示例 Skill 已形成一致的协作文档体系，主要断链与路径问题已消除
- **下一步:** 增加自动断链检查脚本，并继续扩展示例 Skill 类型

### 2026-03-30 12:24 (Codex)

- **目标:** 补强 `Vibe Coding`、`Git`、`GitHub`、`SSH` 等基础教程
- **操作:** 重写概念文档与工具指南，补充首次上手流程、认证方式、常见报错排查和交叉引用；扩展术语表
- **结果:** 基础教程已从“概念说明”提升为“新手可独立走通”的版本
- **下一步:** 可继续补充更进阶的 GitHub PR / Review / Actions 教程

### 2026-03-30 13:21 (Codex)

- **目标:** 把 Claude 官方 Skills 资料、最佳实践和上下文机制纳入 starter
- **操作:** 新增官方 Skill 资料导航、官方最佳实践清单、`AGENTS.md` / `CLAUDE.md` 入门说明与 Claude Code context 文档；重写 `CLAUDE.md` 最佳实践页；统一 README 和官方资源索引中的官方链接
- **结果:** 仓库现在不仅有基础教程和模板，也补上了官方一手资料、PDF 指南、best practices 和 context 机制说明
- **下一步:** 继续补进阶 GitHub 协作教程，并增加自动断链检查

### 2026-03-30 13:58 (Codex)

- **目标:** 统一二级目录的编号规则，修正 `04-参考资料/` 的排序混乱
- **操作:** 将 `04-参考资料/` 改为目录内从 `01` 开始的连续编号，并把原先未编号的文件一并重命名；同步更新 README 与各文档中的相对链接
- **结果:** 参考资料目录现在和其他二级目录保持相同的编号规则，排序与命名更一致
- **下一步:** 如需继续收口，可再为 `04-参考资料/` 增加一个目录索引页，明确推荐阅读顺序

### 2026-03-31 11:23 (Codex)

- **目标:** 把 Git 提交流程、commit 规范、上下文工程和 Rules 写法补进工具指南
- **操作:** 新增“提交到 GitHub 与 Commit 规范”“上下文工程入门”“Rules 编写指南”三篇文档；调整 `GitHub 入门`、`Vibe Coding`、`AGENTS / CLAUDE` 和 README 的学习路径；移除对 GitHub Actions 的展开
- **结果:** 工具指南现在不只讲 GitHub 账号和仓库，而是把“怎么提交、怎么写规则、怎么管理上下文”也纳入了基础教程
- **下一步:** 如果继续扩展，最值得补的是更接近真实协作场景的 PR / Code Review 实战教程

### 2026-03-31 11:35 (Codex)

- **目标:** 重新编排学习目录，让工具指南与上下文工程分层
- **操作:** 新增 `03-AI协作与上下文/` 目录，并将 `Vibe Coding`、`AGENTS / CLAUDE`、上下文工程、Rules 文档迁入；将 `03-创建Skill/`、`04-参考资料/` 顺延为 `04`、`05`；同步更新 README、`docs/ARCHITECTURE.md` 与全仓库相对链接
- **结果:** 学习路径已调整为“概念入门 → 工具指南 → AI 协作与上下文 → 创建 Skill → 参考资料”，目录职责更清晰
- **下一步:** 如果还要继续收口，可以给 `03-AI协作与上下文/` 增加一篇目录索引或推荐阅读顺序

### 2026-03-31 11:35 (Codex)

- **目标:** 让 `find-skill` 随仓库内置，避免使用者进入项目后还要手动安装
- **操作:** 新增 `.claude/skills/find-skill/SKILL.md` 作为 project-local 版本；保留 `skills/find-skill/` 作为可读范例；调整 `.gitignore`，不再整体忽略 `.claude/`
- **结果:** 在这个仓库里使用 Claude Code 时，`find-skill` 已可开箱即用，同时本地配置文件仍保持忽略
- **下一步:** 如果后面还要补更多 project-local Skills，建议统一放在 `.claude/skills/` 下管理

### 2026-03-31 14:40 (Codex)

- **目标:** 让 `AGENTS.md` 与 `README.md` 的功能定位一致，并把仓库用法转成 AI 可执行协议
- **操作:** 调整 `README.md`，补充“先描述需求、先检索、能复用不重造、否则再创建”的默认使用路径；重写 `AGENTS.md` 的项目定位，新增 AI 默认工作流、目录检索协议和 project-local Skill 约定；同步更新 `CHANGELOG.md` 与 `status/TASKS.md`
- **结果:** 现在人类读者看 `README.md` 能理解仓库入口逻辑，AI 代理看 `AGENTS.md` 也能按同一条分流和检索路径执行
- **下一步:** 后续可继续把高频文档的关键词和适用场景再标准化，进一步增强按需检索效果

### 2026-03-31 14:43 (Codex)

- **目标:** 把 changelog 维护方式从 `Unreleased` 切换为内部版本号迭代
- **操作:** 将 `CHANGELOG.md` 改写为 `0.1.0` 版本段，并补充“未正式发布也按 `0.x.0` 记录”的说明；在 `AGENTS.md` 中写入 changelog 版本化约定；同步更新 `status/TASKS.md`
- **结果:** changelog 现在已经从单一未发布段落切换到版本化维护方式，后续可以直接按 `0.2.0`、`0.3.0` 继续追加
- **下一步:** 下一轮对外可见改动开始时，直接新开 `0.2.0` 段即可，不需要再回到 `Unreleased`

### 2026-03-31 14:57 (Codex)

- **目标:** 补上许可证与开源授权说明，避免 starter 只讲结构不讲分发规则
- **操作:** 新增“什么是许可证”和“许可证与开源授权参考”两篇文档；更新 `README.md`、`SKILL-DEV-GUIDE.md`、`04-创建Skill/03-基于模板创建.md`、`04-创建Skill/02-搜索现成方案.md` 和 `skills/skill-template/SKILL.md`，补充 `LICENSE.txt`、`license` 字段和许可证筛选说明；将本轮改动记入 `0.2.0`
- **结果:** 仓库现在已经覆盖许可证基础概念、官方参考入口和 Skill 创建时的实际落地方式，但没有在未确认前擅自替项目选定具体许可证
- **下一步:** 如果用户确认本仓库要采用哪一种许可证，再补根目录 `LICENSE` 即可

### 2026-03-31 15:04 (Codex)

- **目标:** 参照 `legal-skills` 抽取更成熟的许可证治理经验，并更新到 starter
- **操作:** 阅读 `legal-skills` 中的 `AGENTS.md`、`README.md`、`SKILL-DEV-GUIDE.md` 和许可证模板，提炼其中通用的方法论；将许可证分类、`license`/`LICENSE.txt` 配套规则、README 许可证列和迁移 Skill 保持原许可等规则写回 starter 的 `AGENTS.md`、`SKILL-DEV-GUIDE.md`、概念文档和参考资料；将本轮变更记入 `0.3.0`
- **结果:** starter 现在已经继承了 `legal-skills` 中可复用的许可证治理方法，但没有硬塞法律项目专属的联系方式、版权署名或许可证条款
- **下一步:** 如果后面你希望 starter 进一步提供可复制的许可证模板，可以再补一个 `templates/` 目录

### 2026-03-31 15:56 (Codex)

- **目标:** 把许可证说明从“按 Skill 类型分类”调整为“按授权目标和商业化策略分类”
- **操作:** 重写 `AGENTS.md`、`SKILL-DEV-GUIDE.md`、许可证概念文档和参考文档中的许可证段落，改为围绕商用权、署名义务、同协议共享、专利表述和后续商业授权空间来解释；将本轮改动记入 `0.4.0`
- **结果:** starter 现在对许可证的说明更中性、更通用，也更适合帮助用户做后续开源与商业化决策
- **下一步:** 如果你后面确定本仓库自己的许可证，再继续补根目录 `LICENSE` 和对应的 README 声明

### 2026-03-31 16:48 (Codex)

- **目标:** 避免 `SKILL-DEV-GUIDE.md` 与后续从 `legal-skills` 同步的上游内容产生漂移
- **操作:** 撤回 `SKILL-DEV-GUIDE.md` 的本地改动；在 `AGENTS.md` 中新增“上游同步文件”约定，明确根目录 `SKILL-*-GUIDE.md` 默认不手动修改；同步更新 `CHANGELOG.md` 与 `status/TASKS.md`
- **结果:** `SKILL-DEV-GUIDE.md` 已恢复到仓库原始状态，后续这类 guide 文件将按上游同步方式维护
- **下一步:** 如需补充说明，优先放到 `README.md`、概念文档和参考资料，不在同步文件中做本地分叉

### 2026-03-31 17:06 (Codex)

- **目标:** 为许可证说明保留可快速检索的对比表，并补清派生 / 衍生相关条款
- **操作:** 更新许可证概念文档与参考资料文档，新增常见许可证对比表，补充 `SA`、`GPL`、`AGPL`、`ND`、`NC` 等条款解释；同步更新 `CHANGELOG.md`、`status/TASKS.md` 和决策记录；保持 `SKILL-DEV-GUIDE.md` 不变
- **结果:** 仓库现在既保留了许可证的策略性说明，也补上了快速对照和派生条款解释，便于读者判断开源、商用和后续授权边界
- **下一步:** 如果后面要继续增强，可再补一份“代码许可证 vs 文档许可证”组合示例，但仍应放在概念文档或参考资料中

### 2026-03-31 17:21 (Codex)

- **目标:** 统一 starter 的 Skill 暴露方式，并把规范性 guide 收拢到 `04-创建Skill/`
- **操作:** 对照 `legal-skills`，将 `04-创建Skill/SKILL-DEV-GUIDE.md` 和 `04-创建Skill/SKILL-ORCHESTRATION-GUIDE.md` 作为规范文档入口；把 `.claude/skills` 改为指向根目录 `skills/` 的符号链接；更新 README、AGENTS、`find-skill`、参考资料和模板文档中的路径与语义
- **结果:** starter 现在以根目录 `skills/` 为单一来源，Claude Code 通过 `.claude/skills` 直接读取这些 Skill；guide 也已经并入 `04-创建Skill/`，结构更贴合仓库用途
- **下一步:** 可继续补一篇“如何把单个示例 Skill 提升成仓库内正式 project-local Skill”的说明，但不用再维护双副本目录
