# Changelog

本文件记录本仓库对外可见的变更。
即使当前还没有正式对外发布，也按内部迭代版本记录，例如 `0.1.0`、`0.2.0`，而不是只维护一个 `Unreleased` 段落。

## 0.24.0 - 2026-07-29

### Changed

本轮 3 篇并行扩写（3 个 subagent 同时，PM 统一 review + 修复 + 提交）：

- `01-概念入门/01-什么是-Skill.md`：从 43 行纯类比扩写为概念入门教程（约 3000 字）。补 Skill 生命周期概念（发现/触发/加载/执行/输出/失败，点到为止，深度留给 05/06）；保留手机 App 类比 + Plugin/Extension 表 + 为什么重要 4 点；6 条常见误解 + 5 题自测。
- `01-概念入门/04-术语表.md`：增量补充 21 个高频词（shell/路径/环境变量/依赖/frontmatter/YAML/JSON/MCP/hook/eval/CI/Lint/退出码/符号链接/虚拟环境/语义化版本/tag/release/回滚/baseline/near-miss），零重复，保持字母分节表格格式，每个词括注指向对应教程。
- `02-工具指南/05-GitHub-PR-与-Code-Review.md`：保留原 8 大节，新增第 9 节「动手练习」（作者视角 5 步 + 审查者视角 5 步 + 验收 5 条），用 todo.py 的 `list --pending` 改动做练习素材。

### Fixed

- 修复 05 篇断链：`./01-GitHub-入门.md`（不存在）→ `./01-Git-入门.md`（Git 安装在 01-Git，不在 02-GitHub）。**CI 严格门禁首次拦下 subagent 引用的不存在文件**，证明门禁链路有效。

### Notes

- 本轮 review 三个核心风险点全通过：01 边界控制（grep 验证未重复 05/06 的分步流程和层级表）、04 去重（21 词零重复）、05 原内容保留（8 大节全在）。断链是 subagent 弄混 Git/GitHub 文件编号所致，已被门禁拦下并修复。

## 0.23.0 - 2026-07-28

### Changed

本轮 3 篇旧短文并行扩写到新风格（3 个 subagent 同时扩写，PM 统一 review + 提交）。三篇都从 57-79 行短文升级到 2500-4500 字教程，H1 去数字、补 7 段骨架（5 步 / 6 错 / 5 题）、保留原有精华骨架、修正平台事实：

- `04-创建Skill/01-需求分析.md`：保留复杂度表 + 需求文档模板 + 新建 vs 合并条件；用 `todo.py` 贯穿「模糊想法 → 可验收需求」。
- `04-创建Skill/02-搜索现成方案.md`：保留搜索顺序 + 五维评估表；补 `-g -y` 全局安装安全提醒（引用 05 第三方审查）；ClawHub 未引入。
- `04-创建Skill/04-调试与发布.md`：保留调试问题表 + 发布检查清单 + 仓库结构；主推 Skills CLI + GitHub Release；ClawHub 标「待核对」（核实其仅出现在上游 `skills/git-batch-commit/references/clawhub-sync-check.md`，README 未背书）；用本仓库 CHANGELOG 0.1.0→0.22.0 作版本管理活教材。

### Notes

- 扩写 review 重点核查了三个风险点并全部通过：（1）原文精华骨架未丢失；（2）平台事实修正到位（ClawHub 弱化 / OpenClaw 保留 / `-g -y` 加提醒）；（3）代码块围栏正确（01 篇模板示例内的伪 H1 `# 需求：待办管理 Skill` 确在 ```text 围栏内，非真 H1）。
- **04-创建Skill 主线（01→02→03→04→05→06→07→08→09）现全部对齐新风格**，仅 03-基于模板创建 仍标「待拆最小版/维护版」。

## 0.22.0 - 2026-07-28

### Added

本轮 3 篇并行产出（3 个 subagent 同时写作，PM 统一 review + 接入 + 提交）：

- `02-工具指南/10-测试LintCI.md`：测试/Lint/CI 入门。用本仓库刚接入的 `.github/workflows/check.yml` + `scripts/check.sh` 做活教材，讲透「本地门禁 vs 远程门禁」和「检查通过 ≠ 功能真实可用」。5 步动手 / 6 错 / 5 题。
- `03-AI协作与上下文/10-多Agent协作入门.md`：多 Agent 协作四件事（角色边界 / 任务所有权 / 并行条件 / 交接格式）。用本仓库 `.claude/orchestration/` 的 OTA 编排（PM + 多 tmux worktree worker）做活教材。实例分析 4 子节 / 6 错 / 5 题（checkbox 清单）。
- `03-AI协作与上下文/11-贯穿案例.md`：AI 协作主线收尾篇。6 阶段（澄清/计划/实现/验证/文档/PR）用全系列统一项目 `todo.py` 贯穿，把 05/06/07/08/09 方法论串成一次完整协作。6 阶段 / 6 错 / 5 题。

### Fixed

- 接入交叉引用：09-任务拆解、10-多Agent 的「下一篇」指向 11-贯穿案例（去「暂未发布」加实链接）；02-工具指南/09「下一步看什么」补指向 10-测试LintCI。

### Notes

- 本轮首次用 3 个 subagent 真正并行写作（DEC-029）。PM 发现并确认一个跨目录惯例差异：`04-创建Skill/` 用「第 1 步」（阿拉伯数字），`02-工具指南/` 用「第一步」（中文数字）—— subagent 正确遵循了各自目录的本地惯例，未强行统一。
- **两条主线收尾**：03-AI协作与上下文（05→11）主线完成；02-工具指南的测试/Lint/CI 缺口补齐。

## 0.21.0 - 2026-07-28

### Added

- `04-创建Skill/09-触发质量与eval.md`：触发质量教程，对齐 06/07/08 的 7 段骨架（5 步动手 / 6 条错误 / 5 题自测）。贯穿示例用 06 的 `commit-style` 跑 trigger eval 流程（trigger-evals.json 17 条：7 正 / 7 负含 3 near-miss / 3 边界）。核心概念用一张表对齐三套同义说法（CONTENT-MATRIX「正例/负例/边界/基线」/ skill-creator「should-trigger/should-not-trigger/near-miss/with-skill baseline」/ SKILL-DEV-GUIDE §13「正向/负向/边缘」）。

### Fixed

- `06-纯说明型-Skill.md`（两处）、`07-带脚本-Skill.md`（一处）、`08-多Skill编排.md`（两处，含 08 的下一篇主线）共 5 处「09 触发质量与 eval（暂未发布）」改为实链接。Wave 5 第二篇落地，「04-创建Skill」主线教程 06-09 全部成链。

### Notes

- 09 沿用 DEC-028 的 PM 单线程单篇方案；权威依据来自 `skills/skill-creator/SKILL.md` L333-405（trigger eval + run_loop 自动优化）和 `references/schemas.md`（evals.json），均为仓库内现成可读。不真跑 run_loop.py（依赖 Claude Code 子进程，超出教学范围）。

## 0.20.0 - 2026-07-28

### Added

- `04-创建Skill/08-多Skill编排.md`：第三层 Skill 创建教程，对齐 06/07 的 7 段骨架（5 步动手 / 6 条错误 / 5 题自测）。贯穿示例把 06 的 `commit-style`（会说）和 07 的 `todo`（会做）串成「待办提交编排」。核心概念引用 `SKILL-ORCHESTRATION-GUIDE.md` §2 三机制；实例分析引用 `skills/git-batch-commit/SKILL.md` 的职责边界表。

### Fixed

- `06-纯说明型-Skill.md`（两处）和 `07-带脚本-Skill.md`（一处）的「08 多 Skill 编排（暂未发布）」改为实链接，去掉暂未发布标注。09 相关标注保留（09 暂未发布）。

### Notes

- Wave 5 范围决策（DEC-028）：本轮 PM 单线程只写 08 一篇，不走 OTA 并行（避免一次性万字级后半篇质量风险）；09 触发质量与 eval 下一轮基于同模板产出。

## 0.19.0 - 2026-07-28

### Added

- `.github/workflows/check.yml`：GitHub Actions 合并前门禁，在 push 到 main 和 PR 时运行 `scripts/check.sh`（严格模式：`STRICT_LINKS=1` + `STRICT_SH_SYNTAX=1`，断链 / shell 语法 / py 编译 / Skill frontmatter 任一失败即 CI 红）。CI 首次运行通过（8s）。
- main 分支保护：把 `scripts/check.sh（严格模式）` 设为 required status check（app_id=15368，GitHub Actions）；`enforce_admins=false`、`required_approving_review_count=0`（单人维护友好）。**P0 唯一残留闭环。**

### Fixed

- `docs/CONTENT-MATRIX.md` 与实际产出文件偏差：Wave 4 已写的 7 篇（概念入门 07/08/09、AI 协作 08/09、创建Skill 06/07）勾 ✅；03-AI协作「多 Agent 协作入门」「贯穿案例」顺延为 10/11（实际 08=分工、09=任务拆解已占用）。

### Notes

- 仓库现具备完整质量门禁链路：本地 `scripts/check.sh` + 远端 GitHub Actions + 分支保护。CI 无第三方依赖（仅用 Python 标准库），`ubuntu-latest` + `python-version: 3.x` 即可运行。

## 0.18.0 - 2026-07-28

### Added

- 根 `LICENSE.txt`（MIT，含第三方内容声明：git-batch-commit/skill-manager=MIT、skill-creator=Apache-2.0、find-skills=待确认，均保留原许可）。
- README 新增「许可证」段（原创 MIT + 第三方 Skill 许可证表 + 指向 SOURCE-INDEX/LICENSE-PLAN）。

### Changed

- `docs/LICENSE-PLAN.md` 标记已选定 MIT（DEC-026），第 5 节决策清单闭环。
- 清理已合并的 worktree/分支：Wave 1-4 全部 worker 分支（收口时已删）+ 历史分支 `worktree-suitagent-vscode-extension`（已合并 main，删除）；`.claude/worktrees/` 残留目录清空。

### Notes

- DEC-013 待决策项闭环（用户拍板 MIT）。仓库现具备完整许可证方案：原创 MIT + 第三方保留原许可 + 来源索引。

## 0.17.0 - 2026-07-28

### Added

- Wave 4（OTA 3 worker × glm-5.2 并行）产出 7 篇，worker 遵循 WRITING-GUIDE + CONTENT-MATRIX：
  - `01-概念入门/07-复用改造还是新建.md`、`08-权限与信任边界.md`、`09-版本来源与维护.md`
  - `03-AI协作与上下文/08-Prompt-Rules-Commands-Skills-MCP-Hooks-分工.md`、`09-任务拆解与迭代.md`
  - `04-创建Skill/06-纯说明型-Skill.md`、`07-带脚本-Skill.md`

### Fixed

- writing-reviewer review 后 PM 修 1 Critical（08 错字「偻」→「做」）+ ~12 Important：08 `-g -y` 标志补 CLI 来源、hooks 改「以 Claude Code 为例」；09 自动备份 vs 裸 git 区分、覆盖补丁前另存、find-skills 对比 skill-creator(Apache-2.0)；08-分工 `/skill` 触发语义修正；09-任务拆解 阶段4 归类（保留回退点贯穿阶段3）；06/07 LICENSE.txt 补「模板不带、需自行新增」；07 计数「三个要素」→「下面几条」、`todos.json` 路径改 Skill 根目录 + `.gitignore` 说明。

### Notes

- Wave 4 是首轮 worker 严格遵循 WRITING-GUIDE 的批次，review 仅 1 Critical（错字）+ ~12 Important（多为事实/逻辑/模板一致性），结构/计数/术语括注/收尾/跨篇引用高度合规，证明规范前置进一步降质量风险。

## 0.16.0 - 2026-07-28

### Added

- 课程结构前置（PM 直接做，Wave 3）：
  - `docs/CONTENT-MATRIX.md`：「读者阶段 × 前置知识 × 学习结果 × 对应文章」内容矩阵（已写 10 篇 ✅ + 规划 ⏳ + 编号规则），作为新增文章编号的单一事实源。
  - `docs/WRITING-GUIDE.md`：教程统一最小结构（7 段骨架）+ 统一示例项目 `todo.py` + 跨平台标注规范 + Wave 1/2 review 教训 codify（计数准确 / 标题名实相符 / 术语首次括注 / 收尾别用"不是X而是Y" / 命令占位符 / 断言有据）。
  - README 新增「学习入口」双入口（零基础顺序学习 + 已有经验按问题查阅）。

### Notes

- 课程结构前置为规范性工作（连贯、需全局视角、无并行优势），PM 直接做而非 OTA worker（DEC-024，§2 例外）。后续 Wave 写文章须先查 CONTENT-MATRIX 定编号、遵循 WRITING-GUIDE。

## 0.15.0 - 2026-07-28

### Added

- Wave 2（OTA）产出 P2 第二批 4 篇安全/可靠性文章（3 个 tmux worktree worker × glm-5.2 并行）：
  - `02-工具指南/09-环境变量与密钥安全.md`
  - `03-AI协作与上下文/06-验证-AI-的工作.md`
  - `03-AI协作与上下文/07-上下文生命周期.md`
  - `04-创建Skill/05-第三方-Skill-安全审查.md`

### Fixed

- writing-reviewer review 后 PM 修 3 Important：09 `gh auth token` 语义（打印 token 非撤销）、06 `lint` 首次括注、07「2 类上下文」与 03 篇「7 层来源」显式映射。

### Notes

- Wave 2 prompt 内置 Wave 1 review 教训，本轮 writing-reviewer **0 Critical**（Wave 1 是 3 Critical），质量提升明显。
- 事实核对：4 篇引用的第三方 Skill 来源/许可证/issue 与 `docs/SOURCE-INDEX.md` 全部一致，无编造 URL/SHA；假 Token 规范（`sk-fake-DEMO1234`）。

## 0.14.0 - 2026-07-28

### Added

- Wave 1（OTA 多代理编排）产出 P2 第一批 6 篇地基文章，3 个 tmux worktree worker × glm-5.2 并行写作、PM 收口 merge：
  - `01-概念入门/05-工具-Skill-MCP-Plugin-Workflow-关系.md`
  - `01-概念入门/06-一个-Skill-是怎样工作的.md`
  - `02-工具指南/06-终端与命令行入门.md`
  - `02-工具指南/07-项目目录与文件格式入门.md`
  - `02-工具指南/08-开发环境与依赖入门.md`
  - `03-AI协作与上下文/05-从需求到验收标准.md`

### Notes

- 按 `multi-agent-orchestration` skill 用 3 个独立 worktree worker（分支 `docs/concept-skill-mcp` / `docs/tools-terminal-env` / `docs/collab-acceptance`）并行写作，PM 不代写；sentinel（事件驱动）+ cron（兜底）双层监测。
- 踩坑与解法：inline JSON 转义→mcp 配置文件；authority receipt→彻底清理；MCP 选择 dialog→send Escape；tmux server 继承错 provider→`tmux set-environment -g` 注入智谱凭据；`date` 被门禁拦→git 全套已 safe + 固定 timestamp；GLM 529 限流→send-keys 重投换时机。
- W1 worker 因限流中断漏 commit，PM 按 §11 Hard Fail #4 手动补 commit。
- 文章 `bash scripts/check.sh` 通过；待 writing-reviewer 批量 review + 读者实操验收（P2）。

## 0.13.0 - 2026-07-27

### Added

- 新增 `docs/SOURCE-INDEX.md`：`skills/` 下 5 个 skill 的来源类型、来源 URL、同步 commit SHA、许可证、本地补丁、最近核对日期的事实索引（source lock）。
- 新增 `docs/LICENSE-PLAN.md`：仓库级许可证方案（区分原创 vs 第三方内容），给出 MIT / MIT+CC-BY-4.0 / CC-BY-NC-SA-4.0 三个选项与利弊，附第三方声明模板；未替仓库选定具体 LICENSE（遵循 DEC-013）。
- README 新增「当前成熟度与已知限制」小节，诚实说明早期迭代状态、check.sh 仅静态检查（通过≠可用）、CI 与端到端验证仍在建设。
- `scripts/check.sh` 新增「脚本语法检查」段：所有 `.sh` 跑 `bash -n`，所有 `.py` 跑 `python3 -m py_compile`。

### Changed

- `skills/git-batch-commit/` 通过 `git checkout legal-skills/main --` 整目录同步至 upstream v1.4.1（SKILL.md version 1.2.4→1.4.1，顺带同步 CHANGELOG/references/scripts 的版本演进）；与根 CHANGELOG 0.9.0、DEC-020 记录一致，无本地补丁。
- `skills/skill-manager/scripts/update.sh`：`grep -oP` 改 POSIX `sed -nE`（macOS BSD + GNU 兼容）；新增 `update_via_registry()` 回退路径，解决「安装删 `.git`、更新依赖 `.git`」矛盾流程；`((count++))` 改算术展开；`file://` 真实场景更新测试通过。偏离 upstream（本地补丁）。
- `scripts/check_skills.py`：正则 → 标准 YAML 校验（PyYAML 可用走 `safe_load`，否则内置 fallback，非硬依赖）；新增 warn 规则（name 与目录名一致、name 字符/长度、description 质量、license 声明），存量只 warn 不阻断，兼容扩展字段。
- `scripts/check_links.py`：新增 Markdown 锚点检查与引用式链接检查；外部链接默认只计数，留 `--check-external` 开关占位与接入注释。
- README / AGENTS 纠正第三方 Skill 来源：`find-skills`（vercel-labs/skills）、`skill-creator`（anthropics/skills）不再标为 starter 原创，附来源链接；AGENTS 变更历史追加 v1.2.6。
- `docs/ROADMAP.md` / `docs/ARCHITECTURE.md` 文档一致性修复：ROADMAP 阶段四速览表与任务详情矛盾消除、`status/` 幽灵路径清理 4 处、`weekly-weather-briefing`/完整示例幽灵引用修正、更新时间刷新到 2026-07-27。

### Notes

- 收口验证：`bash scripts/check.sh` EXIT 0（脚本语法 0 warn、149 链接有效、5 skill 必需项全齐；`STRICT_SH_SYNTAX=1 STRICT_LINKS=1` 严格模式亦通过）。仅 7 条 license/CHANGELOG 缺失 warn（真实历史存量，已记录于 SOURCE-INDEX，根 LICENSE 待用户选定）。
- 本批次按 `multi-agent-orchestration` skill 用 6 个并行同宿主 Sub Agent 推进（DEC-021）；后续内容写作批次将升级为 OTA tmux worktree worker。

## 0.12.0 - 2026-07-27

### Added

- 新增 `scripts/check_links.py`：扫描所有 Markdown 相对链接，抓幽灵引用与目录命名漂移。
- 新增 `scripts/check_skills.py`：校验 `skills/` 下每个 skill 的 `SKILL.md` 与 frontmatter 必需字段，推荐文件缺失告警。
- 新增 `scripts/check.sh`：聚合入口，提交前一键自检。
- 新增 `02-工具指南/05-GitHub-PR-与-Code-Review.md`：PR 创建、描述模板、Code Review 检查清单、合并策略与常见坑。

### Changed

- 文档一致性修复：移除当前规范文档中对不存在的 `weekly-weather-briefing` 的幽灵引用（README、docs/ARCHITECTURE、skill-template、05-参考资料），历史记录保留。
- 命名统一：当前规范文档中 `find-skill`（单数）统一为实际目录名 `find-skills`（复数）。
- README 项目结构补 `scripts/` 与 `skill-creator`，"完整示例"卖点改为参考 `skills/` 下真实在用的 Skill。
- README 维护说明、AGENTS Git 工作流新增"提交前自检"约定（`bash scripts/check.sh`）。
- AGENTS 仓库检索协议 `02-工具指南` 适用问题补"PR / Code Review"。
- README 资源导航新增 PR 教程入口。

### Removed

- 清理 `skills/skill-start-update/output/` 孤儿目录（git 层此前已删，工作目录残留）。

### Notes

- `docs/ROADMAP.md` 阶段四（自动校验）标记为已完成。

## 0.11.0 - 2026-07-27

### Removed

- 删除 `.qoderworkcn/skills` 符号链接及 `.qoderworkcn/` 目录。starter 仓库不再内置 QoderWork 的多 Agent 符号链接；如需 QoderWork 支持，可由 `skills/skill-manager` 的 `init.sh --qoderwork` 按需生成。

### Changed

- 默认分支从 `master` 重命名为 `main`（GitHub 默认分支、本地分支、upstream 跟踪均已同步）。
- `README.md` 项目结构和多 Agent 共享说明移除 `.qoderworkcn`，保留 `.codex` / `.openclaw` / `.workbuddy` 三个。
- `AGENTS.md` "Project-local Skills 约定"中的相对符号链接列表移除 `.qoderworkcn`。
- `.gitignore` 移除 `.qoderworkcn/.DS_Store`、`.qoderworkcn/settings.local.json`、`.qoderworkcn/*.local.*` 三条忽略规则。

### Notes

- `skills/skill-manager/` 是从 legal-skills 同步的上游 skill，其内部仍完整支持 `.qoderworkcn` 目录（`init.sh` / `target.sh` / `install.sh` 等），这是 skill-manager 的功能定义，不受 starter 仓库自身移除 `.qoderworkcn` 影响。

## 0.10.0 - 2026-07-27

### Removed

- 删除 `skills/skill-start-update/` 整个目录（原 starter 原创 skill，用于检查远程更新）。`AGENTS.md` 中的"按需检查更新"原则改为直接通过 `git fetch origin && git status` 自行确认。
- 清理项目内 30 处冗余的嵌套 `CLAUDE.md` 文件（均为 claude-mem 自动生成的空模板，root `CLAUDE.md` 之外的副本）。`.gitignore` 已有 `**/CLAUDE.md` + `!CLAUDE.md` 规则抑制继续生成。

### Changed

- 协作文档路径对齐：把 `status/TASKS.md` 迁移到 `docs/TASKS.md`，`status/DECISIONS.md` 迁移到 `docs/DECISIONS.md`，删除空的 `status/` 目录。
- `.gitignore` 移除对 `docs/` 和 `status/` 的整体排除，新迁移的协作文档纳入版本管理。
- `AGENTS.md` 中更新协作文档约定与项目结构相关的路径引用。
- `README.md` 项目结构小节移除 `skill-start-update/`，更新 `docs/` 子目录与原创 skills 列表。
- `docs/ARCHITECTURE.md` "仓库治理层"与"协作文档默认存在"两节更新路径引用。

## 0.9.0 - 2026-07-27

### Added

- 新增 `skills/skill-manager/`,从 [legal-skills](https://github.com/cat-xierluo/legal-skills) `main` 分支通过 `git checkout legal-skills/main -- skills/skill-manager` 同步,版本 `1.7.0`,覆盖 `scripts/{install,list,remove,update,check,init,target,security,record,auto-check}.sh` / `*.py` 及 `assets/skill-registry.example.json`。

### Changed

- `skills/git-batch-commit/` 同步自 legal-skills `main`,版本由 starter 自有版本升至 `1.4.1`。本次拉取更新了 `SKILL.md`、`CHANGELOG.md`、`scripts/generate_commit_message.py`、`scripts/interactive_commit.py`,并新增 3 个 references(`clawhub-sync-check.md`、`message-data.yaml`、`subtree-push-check.md`)和更新 `references/conventional-commits.md`。
- 新增只读 remote `legal-skills`,仅用于拉取上游 Skill,从不向其推送。
- `README.md` 项目结构小节标注每个 skill 的来源(同步自 legal-skills 或 starter 原创),并新增"与 legal-skills 的同步关系"小节记录同步命令与约定。
- `AGENTS.md` 中"上游同步文件"约定扩展到 `skills/`,明确 `git-batch-commit` 和 `skill-manager` 走 upstream,其他 4 个 skill 不从 upstream 同步。

### Notes

- 同步前对 starter 本地 5 个同名 skill(`find-skills`、`git-batch-commit`、`skill-creator`、`skill-start-update`、`skill-template`)做了完整备份到 `.starter-backups/<name>/`。该目录被 `.gitignore` 排除,不纳入版本管理,需要时可手动 `mv` 回 `skills/` 即恢复。
- legal-skills upstream 不含 `find-skills`、`skill-creator`、`skill-start-update`、`skill-template`,这 4 个 skill 为 starter 仓库原创。

## 0.8.0 - 2026-07-27

### Added

- 在项目根目录新增 `.codex/`、`.openclaw/`、`.workbuddy/`、`.qoderworkcn/` 四个目录,各自携带相对符号链接 `skills -> ../.claude/skills`,让 Codex / OpenClaw / WorkBuddy / QoderWork 在本仓库内都能发现同一套 Skill。`.claude/skills` 仍是唯一来源,不复制、不双写。

### Changed

- `.gitignore` 在现有 `.claude/*` 本地配置忽略模式上,按相同规则为每个新 Agent 目录追加 `settings.local.json` / `*.local.*` / `.DS_Store` 的忽略项;Agent 目录本身和其中的 skills 符号链接仍纳入版本管理。
- `README.md` 项目结构小节补充四个 Agent 目录及相对链接说明,并新增"多 Agent 共享"小节解释两层符号链接的工作方式。
- `AGENTS.md` 中"Project-local Skills 约定"小节补充四个 Agent 的相对符号链接约定及 `.gitignore` 处理说明。

## 0.7.0 - 2026-03-31

### Changed

- 将 `SKILL-DEV-GUIDE.md` 与 `SKILL-ORCHESTRATION-GUIDE.md` 统一移入 `04-创建Skill/`，作为创建与规范文档的一部分
- 将 `.claude/skills` 调整为指向根目录 `skills/` 的符号链接，对齐 `legal-skills` 的单一来源结构
- 更新 README、AGENTS、创建流程、参考资料和模板中的路径说明，移除 `find-skill` 双副本叙事

## 0.6.0 - 2026-03-31

### Added

- 为许可证文档补充常见许可证对比表

### Changed

- 增补派生版本 / 衍生作品相关说明，明确 `SA`、`GPL`、`AGPL`、`ND`、`NC` 等条款在 Skill 场景下的区别
- 将许可证说明进一步对齐到“开源方式、商用边界、署名义务和后续授权策略”的决策维度

## 0.5.0 - 2026-03-31

### Changed

- 撤回对 `SKILL-DEV-GUIDE.md` 的本地改动，避免与后续从 `legal-skills` 同步的内容发生漂移
- 在 `AGENTS.md` 中新增上游同步文件约定，明确根目录 `SKILL-*-GUIDE.md` 默认不手动修改

## 0.4.0 - 2026-03-31

### Changed

- 重写许可证说明结构，不再主要按 Skill 类型分类，而改为围绕商用边界、署名义务、同协议共享和后续商业授权空间来解释
- 更新 `AGENTS.md`、`SKILL-DEV-GUIDE.md`、许可证概念文档和参考资料，使许可证选择逻辑更通用、更适合 starter

## 0.3.0 - 2026-03-31

### Added

- 参照 `legal-skills` 抽取并补充许可证管理规范，覆盖 `AGENTS.md`、开发指南与参考资料

### Changed

- 更新许可证概念文档，增加按 Skill 类型选择许可证的实战分类
- 更新许可证参考文档，补充 `legal-skills` 中值得继承的多 Skill 许可证展示与迁移规则
- 更新 `AGENTS.md` 与 `SKILL-DEV-GUIDE.md`，把许可证从“说明事项”提升为维护规范

## 0.2.0 - 2026-03-31

### Added

- 新增许可证基础说明文档：`01-概念入门/02-什么是-许可证.md`
- 新增许可证官方参考导航：`05-参考资料/12-许可证与开源授权参考.md`

### Changed

- 更新 `README.md` 资源导航和快速开始，明确 `LICENSE.txt` 也是创建 Skill 时应处理的关键文件
- 更新 `SKILL-DEV-GUIDE.md`、`04-创建Skill/03-基于模板创建.md` 和 `skills/skill-template/SKILL.md`，补充许可证选择、`license` 字段和 `LICENSE.txt` 的落地说明
- 更新 `04-创建Skill/02-搜索现成方案.md`，强调许可证不明确时不要直接复制第三方实现

## 0.1.0 - 2026-03-31

### Added

- 为 starter 仓库补充 `docs/`、`status/` 和 `CHANGELOG.md` 协作文档体系
- 为 `skills/skill-template/` 增加协作文档模板、配置模板和更实用的脚手架脚本
- 新增完整示例 Skill：`skills/weekly-weather-briefing/`
- 补强 `Vibe Coding`、`Git`、`GitHub`、`SSH` 基础教程，加入首次上手流程与常见问题说明
- 新增 Claude 官方 Skills 资料导航、上下文 / memory / settings 说明和 `AGENTS.md` / `CLAUDE.md` 入门文档
- 新增一份基于官方文档、博客和 PDF 的 Claude Skill 最佳实践清单
- 统一 `04-参考资料/` 的文件编号和命名规则，改为目录内独立从 `01` 开始排序
- 新增“提交到 GitHub 与 Commit 规范”“上下文工程入门”“Rules 编写指南”三篇基础工具教程
- 新增 `03-AI协作与上下文/` 目录，将 Vibe Coding、`AGENTS.md`、`CLAUDE.md`、上下文工程和 Rules 单独成组
- 新增项目内置 `.claude/skills/find-skill/`，让 `find-skill` 在仓库内开箱即用
- 新增 AI 需求分流与目录检索协议，明确 `AGENTS.md` 中的默认工作流和 project-local Skill 使用规则
- 新增 changelog 版本化约定，即使未正式发布也按 `0.x.0` 迭代记录

### Changed

- 调整 `README.md`，明确“先描述需求 -> 先检索现成 Skill -> 能复用不重造 -> 否则进入创建流程”的默认使用路径
- 修正 `README.md`、教程文档和模板文档中的目录结构、复制路径和相对链接
- 统一 `find-skill` 相关说明，明确本仓库提供的是引导文档，实际搜索可使用 Skills CLI 或先安装独立 `find-skills` 项目
- 明确 `.env.example` 是环境变量模板，和 `assets/` 中的配置模板分开维护
- 将单个 Skill 内的协作文档改为根目录扁平组织，参照 `legal-skills` 项目结构
- 扩充术语表，补充 Git / GitHub / 协作相关术语
- 更新 Claude 官方参考链接，统一到当前官方文档 / 博客地址，并重写 `CLAUDE.md` 最佳实践页
- 将 `04-参考资料/` 中未编号或全局累加编号的文件重命名为一致的本地顺序，并同步修正内部链接
- 调整 `GitHub 入门` 与 `Vibe Coding` 等入口文档的学习路径，强调 Git 提交流程与上下文工程，而不展开 GitHub Actions
- 重新编排学习目录：`02-工具指南/` 聚焦 Git / GitHub / SSH / commit，`03-AI协作与上下文/` 承接 Vibe Coding 与上下文工程，原 `03-创建Skill/`、`04-参考资料/` 顺延为 `04`、`05`
- 调整 `.gitignore`，不再整体忽略 `.claude/`，改为只忽略本地配置与仓库元数据
