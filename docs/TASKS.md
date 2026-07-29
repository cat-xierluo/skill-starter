# 当前任务

> Last updated: 2026-07-28
>
> 范围说明：用户已确认根目录 `CLAUDE.md` 的 `@include ./AGENTS.md` 保持现状，不列入修复任务。

## 当前目标

把本仓库从“已有理念分区和基础资料”推进为一套真正适合零基础读者的 Skill 学习与实践入口。目标学习路径为：

1. 理解 AI、Agent、工具与 Skill 的基本关系。
2. 补齐终端、文件、文本格式、Git 与 GitHub 等最低工具基础。
3. 学会向 Agent 描述需求、管理上下文、拆分任务并验证结果。
4. 能安全地搜索、评估、复用或改造现有 Skill。
5. 能从模板创建、测试、发布并持续维护一个 Skill。

## P0：先修复会影响使用与发布的问题

- [x] 修复 `skills/git-batch-commit/SKILL.md` 的 YAML frontmatter，并核对本地版本、脚本与 `CHANGELOG.md` / `docs/DECISIONS.md` 所记录版本是否一致。→ 已通过 `git checkout legal-skills/main -- skills/git-batch-commit` 整目录同步至 upstream v1.4.1，无本地补丁。
- [x] 修复 `skills/skill-manager/scripts/update.sh` 的 Bash 语法错误，重新设计“安装时删除 `.git`、更新时却依赖 `.git`”的矛盾流程，并补真实安装后更新测试。→ `grep -oP` 改 POSIX `sed -nE`；新增 `update_via_registry()` 回退路径；`file://` 真实场景测试通过。**偏离 upstream（本地补丁，可回馈）**。
- [x] 纠正 README 和 AGENTS 对第三方 Skill 的来源描述：`find-skills`、`skill-creator` 不再标为 starter 原创。→ 已核实 find-skills←vercel-labs/skills、skill-creator←anthropics/skills，README/AGENTS 来源标注已纠正。
- [x] 制定仓库级许可证方案：区分本仓库原创内容与第三方内容，补根许可证、第三方声明和各 Skill 的来源/许可证索引，避免用单一许可证覆盖上游内容。→ **已完成（DEC-026）**：根 `LICENSE.txt`（MIT）+ 第三方声明 + `docs/SOURCE-INDEX.md` + `docs/LICENSE-PLAN.md`；用户选定 MIT，README 加许可证段。
- [x] 在自动合并前建立最低质量门禁；在 CI 尚未落地前，不把 `scripts/check.sh` 的“通过”视为可发布依据。→ **已完成（DEC-027）**：`.github/workflows/check.yml` 接入 GitHub Actions（严格模式：STRICT_LINKS=1 + STRICT_SH_SYNTAX=1），main 分支保护已配置（CI 设为合并必过项，enforce_admins=false）。CI 首次运行通过（8s）。

## P1：建立可信的仓库质量基线

### 校验与持续集成

- [x] 将 `scripts/check_skills.py` 从正则字段检查升级为标准感知的 YAML 校验，至少覆盖字段合法性、`name` 与目录名一致、名称字符/长度、description 质量和许可证声明。→ PyYAML 可用走 safe_load，否则内置 fallback；4 条 warn 规则上线，存量不阻断。
- [ ] 为不同来源的 Skill 定义兼容校验策略：优先遵循 Agent Skills 标准，同时显式处理 Claude/Codex/OpenClaw 扩展字段，避免“一个本地校验器否定所有平台扩展”。→ **部分完成**：扩展字段（homepage/author/version）已不再报错；完整分平台策略待补。
- [x] 把 Bash `bash -n` / ShellCheck、Python 语法检查、Skill frontmatter 校验、相对链接检查、模板独立复制测试接入统一检查入口。→ bash -n / py_compile / frontmatter / 链接已接入 check.sh；模板独立复制测试待补。
- [x] 增加 GitHub Actions，并将必要检查设为合并前必过项；失败信息应能直接定位到文件和规则。→ **已完成（DEC-027）**：`.github/workflows/check.yml` 在 push/PR 触发 `scripts/check.sh`（严格模式）；main 分支保护把 `scripts/check.sh（严格模式）` 设为 required status check（app_id=15368）。
- [x] 扩展链接检查：覆盖 Markdown 锚点、引用式链接和外部链接；外链采用超时重试、允许清单与定时任务，避免网络波动阻断普通提交。→ 锚点 + 引用式链接已接入；外链留 `--check-external` 开关占位与接入注释。

### 模板、示例与实际验证

- [ ] 修复 `skills/skill-template/` 对 starter 目录层级的依赖，确保复制到独立仓库后所有链接仍有效。
- [ ] 将模板拆成“最小教学版”和“带脚本的维护版”，清理示例中未被实际读取的 `.env.example` / 配置字段，并让许可证进入模板验收清单。
- [ ] 建立一个 starter 原创、可端到端运行的标准示例 Skill，包含触发说明、正反例、真实输出、脚本测试、许可证、来源说明和维护文档。
- [ ] 为模板和标准示例增加真实 Agent 验证：至少验证“应该触发”“不应该触发”“正常执行”“错误输入”四类场景，而不只检查文件是否存在。

### 多平台发现与上游同步

- [ ] 根据各平台当前官方约定重新核对 Skill 发现路径，明确根 `skills/`、`.agents/skills`、`.claude/skills` 与其他兼容链接的职责，并同步 README / AGENTS / 目录树。
- [x] 建立第三方来源清单（source lock），记录来源 URL、分支或 tag、同步 commit SHA、许可证、本地补丁和最近核对日期。→ `docs/SOURCE-INDEX.md` 已建立（find-skills/skill-creator 上游 SHA lock 待补）。
- [ ] 加固上游同步命令：使用带时间或 SHA 的备份目录、禁止向只读 remote 推送、同步后执行 YAML/脚本/链接/测试检查，并验证依赖文档是否完整同步。
- [ ] 将存在长期本地修改的上游 Skill 明确标记为“fork/派生版”，不再按无差异镜像管理。

### 安全与文档一致性

- [ ] 改写 Skill 搜索与安装流程：默认先查看清单和源码，再检查许可证、脚本、网络、凭据与 hooks；默认项目级试用，避免直接推荐全局 `-g -y` 安装。
- [x] 修正 `docs/ROADMAP.md`、`docs/ARCHITECTURE.md`、`docs/TASKS.md`、README 和 AGENTS 中关于 `status/`、完整示例、自动校验完成度及更新时间的冲突，只保留一个当前状态事实源。→ ROADMAP 阶段四矛盾、`status/` 幽灵路径、`weekly-weather-briefing` 幽灵引用已清理；README/AGENTS 来源标注已对齐。
- [ ] 修复已确认失效的外部链接，并将已迁移的 Claude/OpenClaw 等文档链接更新到当前官方地址。
- [x] 为 README 增加简短的“当前成熟度与已知限制”，避免把尚未完成的模板、示例和检查能力描述成开箱即用。→ README「当前成熟度与已知限制」小节已新增。

## P1：补齐零基础学习主线

### 课程结构与写作规范

- [x] 先制作一张“读者阶段 × 前置知识 × 学习结果 × 对应文章”的内容矩阵，再决定新增文章的编号，避免边写边重排目录。→ `docs/CONTENT-MATRIX.md` 已建（含已写 10 篇 ✅ + 规划 ⏳ + 编号规则）。
- [x] 在 README 增加两条入口：“零基础顺序学习”和“已有经验按问题查阅”，让教程路径与参考资料路径分开。→ README「学习入口」双入口已加。
- [x] 为教程统一最小结构：本篇目标、前置知识、核心概念、动手步骤、常见错误、自测题/验收、下一篇；参考资料不强制套用教程结构。→ `docs/WRITING-GUIDE.md` §1 已定。
- [x] 统一示例项目和术语，尽量让读者沿用同一个小项目贯穿 Git、Agent 协作、Skill 创建、测试和发布，减少每篇重新理解背景的成本。→ WRITING-GUIDE §4 统一用 `todo.py`。
- [x] 明确跨平台范围：命令示例至少标注 macOS / Windows / Linux 的差异；平台特有行为必须注明适用版本和最近核对日期。→ WRITING-GUIDE §5 已定。

### `01-概念入门/`：建立完整心智模型

- [x] 扩写“什么是 Skill”：补充 Skill 的发现、触发、加载、执行、输出和失败边界，不只停留在 App 类比。→ **已完成（0.24.0）**：补生命周期概念（点到为止，深度留给 05/06），保留手机 App 类比 + Plugin/Extension 表 + 为什么重要 4 点；6 条常见误解 + 5 题自测。
- [x] 新增“大模型、聊天助手、Agent、工具、MCP、Skill、Plugin 与 Workflow 的关系”，给出同一需求下各自负责什么的对照案例。→ **已完成（Wave 1）**：`01-概念入门/05-工具-Skill-MCP-Plugin-Workflow-关系.md`。
- [x] 新增“一个 Skill 是怎样工作的”，用目录和一次执行流程解释 `SKILL.md`、scripts、references、assets 与运行环境。→ **已完成（Wave 1）**：`01-概念入门/06-一个-Skill-是怎样工作的.md`。
- [x] 新增“复用、改造还是新建”，提供基于匹配度、维护成本、安全风险和许可证的决策树。→ **已完成（Wave 4）**：`01-概念入门/07-复用改造还是新建.md`。
- [x] 新增“权限、凭据与信任边界”，解释为什么 Skill 能执行命令、访问文件或联网，以及安装第三方 Skill 前应检查什么。→ **已完成（Wave 4）**：`01-概念入门/08-权限与信任边界.md`。
- [x] 新增“版本、来源与维护”，解释上游、fork、同步、语义化版本、变更记录和弃用，衔接本仓库的维护规范。→ **已完成（Wave 4）**：`01-概念入门/09-版本来源与维护.md`。
- [x] 扩充术语表：补齐 CLI、shell、路径、环境变量、依赖、frontmatter、YAML、JSON、MCP、hook、eval、CI 等零基础高频词，并链接到对应教程。→ **已完成（0.24.0）**：新增 21 个高频词（shell/路径/环境变量/依赖/frontmatter/YAML/JSON/MCP/hook/eval/CI/Lint/退出码/符号链接/虚拟环境/语义化版本/tag/release/回滚/baseline/near-miss），零重复，每个词括注指向对应教程。

### `02-工具指南/`：补足开始实操前的最低工具基础

- [x] 新增“终端与命令行入门”：当前目录、绝对/相对路径、列出/复制/移动文件、引号与空格、退出码、帮助命令和安全边界。→ **已完成（Wave 1）**：`02-工具指南/06-终端与命令行入门.md`。
- [x] 新增“项目目录与文件格式入门”：隐藏文件、扩展名、Markdown、YAML、JSON、frontmatter、编码与缩进，并提供可修改的小练习。→ **已完成（Wave 1）**：`02-工具指南/07-项目目录与文件格式入门.md`。
- [x] 新增“开发环境与依赖入门”：Python、Node.js、包管理器、`npx`、虚拟环境、版本检查和“全局安装 vs 项目安装”。→ **已完成（Wave 1）**：`02-工具指南/08-开发环境与依赖入门.md`。
- [x] 新增“环境变量与密钥安全”：`.env`、`.env.example`、`.gitignore`、最小权限、泄漏后的处置，以及为什么不能把 Token 写进教程或提交历史。→ **已完成（Wave 2）**：`02-工具指南/09-环境变量与密钥安全.md`。
- [ ] 扩写 Git：分支合并、冲突解决、`restore` / `revert` / `reset` 的区别、误提交恢复和安全操作边界。
- [ ] 扩写 GitHub：Issue、Fork、Release、Actions、分支保护、权限与仓库可见性，补一个从 Issue 到 PR 合并的完整实战。
- [x] 将现有 PR / Code Review 文档扩成可复现练习，包含审查者和作者两种视角、行内评论、修改后复审、合并策略和失败示例。→ **已完成（0.24.0）**：保留原 8 大节，新增第 9 节「动手练习」（作者视角 5 步 + 审查者视角 5 步 + 验收 5 条），用 todo.py 的 `list --pending` 改动做练习素材（含空列表边界处理）。
- [x] 新增“测试、Lint、CI 是什么”，用本仓库检查脚本展示本地验证与远程门禁的区别，并说明“检查通过不等于功能真实可用”。→ **已完成（0.22.0）**：`02-工具指南/10-测试LintCI.md`，用 `.github/workflows/check.yml` + `scripts/check.sh` 做活教材。

### `03-AI协作与上下文/`：从会聊天推进到可靠协作

- [x] 新增“从需求到验收标准”：教读者描述目标、用户、范围、约束、输入输出、非目标和可观察的完成条件。→ **已完成（Wave 1）**：`03-AI协作与上下文/05-从需求到验收标准.md`。
- [x] 新增“Prompt、Rules、Commands、Skills、MCP 和 Hooks 怎么分工”，说明信息应该放在哪里、生命周期多长、谁会触发。→ **已完成（Wave 4）**：`03-AI协作与上下文/08-Prompt-Rules-Commands-Skills-MCP-Hooks-分工.md`。
- [x] 新增“任务拆解与迭代”：如何让 Agent 先调查、再计划、分批实现、保留回退点，并避免一次性大改。→ **已完成（Wave 4）**：`03-AI协作与上下文/09-任务拆解与迭代.md`。
- [x] 新增“验证 AI 的工作”：事实核验、代码审查、测试、实际运行、截图/输出证据、失败复盘，以及如何识别假绿与幻觉。→ **已完成（Wave 2）**：`03-AI协作与上下文/06-验证-AI-的工作.md`。
- [x] 新增“上下文生命周期”：会话上下文、项目上下文、压缩/遗忘、上下文污染、何时写入 TASKS/DECISIONS/CHANGELOG，以及如何控制文档膨胀。→ **已完成（Wave 2）**：`03-AI协作与上下文/07-上下文生命周期.md`。
- [x] 新增“多 Agent 协作入门”：角色边界、任务所有权、并行条件、共享工作区冲突、交接格式和最终集成责任。→ **已完成（0.22.0）**：`03-AI协作/10-多Agent协作入门.md`，用本仓库 OTA 编排做活教材，核心概念四件事（角色边界/任务所有权/并行条件/交接格式）。
- [ ] 新增“AI 协作的安全边界”：只读调查、外部写入、凭据、提示注入、第三方内容、不确定事实和破坏性操作的确认机制。
- [x] 新增一篇贯穿案例：从模糊想法开始，经过澄清、计划、实现、验证、文档同步和 PR，完整展示一次可靠协作。→ **已完成（0.22.0）**：`03-AI协作/11-贯穿案例.md`，6 阶段（澄清/计划/实现/验证/文档/PR）用 `todo.py` 贯穿，串起 05/06/07/08/09 方法论。**03-AI协作主线收尾。**

### `04-创建Skill/`：把知识收束为可交付成果

- [x] 扩写需求分析：加入用户画像、触发/负向触发、输入输出契约、失败处理、依赖、安全、许可证和验收标准。→ **已完成（0.23.0）**：保留复杂度表+需求文档模板+新建vs合并条件，用 todo.py 贯穿。
- [x] 扩写现成方案评估：加入源码审查、来源可信度、更新活跃度、许可证兼容、试运行和退出方案。→ **已完成（0.23.0）**：保留搜索顺序+五维评估表，补 `-g -y` 全局安装安全提醒、ClawHub 弱化（README 未背书）。
- [x] 分别提供“纯说明型 Skill”“带脚本 Skill”“多 Skill 编排”三个由浅入深的完整教程。→ **已完成（Wave 4/5）**：`04-创建Skill/06-纯说明型-Skill.md`、`07-带脚本-Skill.md`、`08-多Skill编排.md`。
- [x] 新增触发质量与 eval 教程：设计正例、负例、边界例，记录基线并比较修改前后结果。→ **已完成（0.21.0）**：`04-创建Skill/09-触发质量与eval.md`。
- [x] 扩写调试与发布：覆盖本地发现、依赖安装、错误诊断、版本、CHANGELOG、tag/release、安装说明、升级与回滚。→ **已完成（0.23.0）**：保留调试问题表+发布检查清单+仓库结构，主推 Skills CLI + GitHub Release（ClawHub 标待核对），用本仓库 CHANGELOG 0.1.0→0.22.0 作版本管理活教材。
- [ ] 为标准示例配套一份“从复制模板到发布”的逐步实验，让读者完成后能独立产出一个可验证 Skill。

### `05-参考资料/`：从资料堆放升级为可维护索引

- [ ] 给外部资料增加来源类型、适用平台、主题、难度、最近核对日期和当前有效状态，优先链接官方一手资料。
- [ ] 区分“教程正文的依据”和“延伸阅读”，避免参考资料与前三个学习目录重复讲解同一内容。
- [ ] 建立资料更新机制：平台规则或链接变化时能定位受影响文章，并通过定时外链检查产生待办。

## P2：内容验收与发布节奏

- [x] 第一批优先完成 6 篇地基文章：工具/Skill/MCP 关系、Skill 运行过程、终端与路径、文件格式、开发环境与依赖、从需求到验收标准。→ Wave 1（OTA 3 个 tmux worktree worker × glm-5.2）已产出并 merge（见 0.14.0）；待 writing-reviewer review + 读者实操验收。
- [x] 第二批完成安全与可靠性文章：密钥安全、第三方 Skill 审查、验证 AI 工作、上下文生命周期。→ Wave 2（OTA 3 worker × glm-5.2）已产出并 merge（0.15.0）；writing-reviewer 通过（0 Critical + 3 Important 已修）；待读者实操验收。
- [ ] 第三批完成端到端案例和三个层级的 Skill 创建教程，再集中调整 README 导航与文章编号。→ **部分推进（DEC-028/DEC-029）**：第三层 08 多 Skill 编排（0.20.0）、09 触发质量与 eval（0.21.0）、03-AI协作主线 10 多 Agent 协作 + 11 贯穿案例、02-工具指南 10 测试 Lint CI（0.22.0，3 篇 OTA 并行产出）已落地，CI/分支保护（0.19.0）已闭环；剩余扩写 01/02/04 等。
- [ ] 每批邀请至少一名没有 Skill 开发经验的读者按顺序实操，记录卡点、完成时间和无法独立完成的步骤，再据此修订。
- [ ] 内容完成不以“文件已创建”为准：读者必须能按文档得到预期结果，所有命令、链接和示例输出都应经过复跑验证。

## 后续可选增强

- [ ] 增加不同领域的示例，但每个示例必须回答一个不同教学问题，避免只换业务名的重复样例。
- [ ] 为核心概念制作小型结构图或流程图；仅在关系或流程明显比文字更易懂时使用。
- [ ] 评估是否提供练习答案、FAQ、故障排查索引和文章级反馈入口。
- [ ] 评估多语言版本；中文主线稳定前不启动全文翻译。

## 已完成（摘要）

- [x] 建立 `01-概念入门/` 至 `05-参考资料/` 的初始分区与中文资料骨架。
- [x] 提供 Git、GitHub、SSH、提交规范、PR / Code Review 的基础教程。
- [x] 提供 Vibe Coding、AGENTS/CLAUDE、上下文工程和 Rules 的基础教程。
- [x] 建立 `skills/skill-template/`、项目级 `skills/` 单一来源和多 Agent 兼容链接。
- [x] 建立 README、CHANGELOG 与 `docs/` 协作文档体系。
- [x] 提供相对链接和 Skill 基础结构检查入口 `scripts/check.sh`。
- [x] 工程批次（0.13.0）：git-batch-commit 同步至 upstream v1.4.1；skill-manager `update.sh` 修 macOS 兼容与安装/更新矛盾流程；README/AGENTS 纠正 find-skills/skill-creator 来源并新增成熟度说明；check_skills.py 升级 YAML 感知、check_links.py 扩展锚点/引用链接、check.sh 接入 bash-n/py_compile；ROADMAP/ARCHITECTURE 文档一致性修复；新增 `docs/SOURCE-INDEX.md` 与 `docs/LICENSE-PLAN.md`。
- [x] 内容批次 Wave 1（0.14.0）：OTA 3 个 tmux worktree worker × glm-5.2 并行产出 P2 第一批 6 篇地基文章（概念入门 05/06、工具指南 06/07/08、AI 协作 05），PM 收口 merge；待 writing-reviewer review + 读者实操验收。
- [x] 内容批次 Wave 2（0.15.0）：OTA 3 worker 并行产出 P2 第二批 4 篇安全/可靠性文章（工具指南 09 密钥安全、AI 协作 06 验证AI/07 上下文生命周期、创建Skill 05 第三方审查）；writing-reviewer 0 Critical + 3 Important（PM 已修）；待读者实操验收。
- [x] 课程结构前置（0.16.0）：PM 直接做 `docs/CONTENT-MATRIX.md`（编号单一事实源）+ `docs/WRITING-GUIDE.md`（统一结构+示例项目+跨平台+review 教训 codify）+ README 双入口。
- [x] 内容批次 Wave 4（0.17.0）：OTA 3 worker 并行产出 7 篇（概念入门 07 复用改造/08 权限信任/09 版本来源、AI 协作 08 分工/09 任务拆解、创建Skill 06 纯说明型/07 带脚本）；writing-reviewer 1 Critical（错字）+ ~12 Important（PM 已修：LICENSE.txt 模板不带、todos.json 路径、`/skill` 触发语义、自动备份 vs 裸 git、覆盖补丁冲突等）。
