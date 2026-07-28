# Changelog

本文件记录本仓库对外可见的变更。
即使当前还没有正式对外发布，也按内部迭代版本记录，例如 `0.1.0`、`0.2.0`，而不是只维护一个 `Unreleased` 段落。

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
