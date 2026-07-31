# Skill 来源与许可证索引（SOURCE-INDEX）

> Last updated: 2026-07-30
>
> 本文件是仓库级"第三方来源清单（source lock）"的事实层：记录 `skills/` 下每个 Skill 的来源类型、上游 URL、同步 commit SHA、许可证、本地补丁与最近核对日期。
>
> 本文件**只记录事实**，不替仓库选定具体 LICENSE 条款。仓库级许可证方案见 [LICENSE-PLAN.md](./LICENSE-PLAN.md)；选定条款的决策权属于仓库维护者（参见 `docs/DECISIONS.md` DEC-013）。

## 总表

| 目录名 | 来源类型 | 上游 URL | 同步 commit SHA / tag | 许可证 | 本地补丁 | 最近核对 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `skills/skill-template` | starter 原创 | —（本仓库原创） | 本地模板 0.2.0 | MIT（frontmatter + 目录 `LICENSE.txt`） | —（原创） | 2026-07-30 |
| `skills/todo` | starter 原创 | —（本仓库原创） | 本地基线 0.1.0 | MIT（frontmatter + 目录 `LICENSE.txt`） | —（原创） | 2026-07-30 |
| `skills/find-skills` | 第三方收录 | https://github.com/vercel-labs/skills （`skills/find-skills/SKILL.md`） | 本地基线 `66a7b901`；上游最近核对 `7cb7db64` | MIT（同步上游根 LICENSE 到目录） | 基线内容无本地补丁；落后于上游 `773fb2c7` 的教程更新 | 2026-07-30 |
| `skills/git-batch-commit` | legal-skills 同步 | https://github.com/cat-xierluo/legal-skills | `efde445`（版本 1.4.1） | MIT（frontmatter；上游仓库根 LICENSE） | 无；当前内容与 `legal-skills/main` 一致 | 2026-07-30 |
| `skills/skill-creator` | 第三方收录 | https://github.com/anthropics/skills （`skills/skill-creator/`） | 本地基线 `3d595115`；上游最近核对 `b29e7cf6` | Apache-2.0（目录 `LICENSE.txt`，版权行同步自 `b9e19e6f`） | 基线代码无本地补丁；上游存在后续功能更新 | 2026-07-30 |
| `skills/skill-manager` | legal-skills 同步后的 **fork/派生版** | https://github.com/cat-xierluo/legal-skills | 上游基线 `f801450`（1.7.0）；本地派生版 1.8.0 | MIT（`LICENSE.txt`；frontmatter 指向完整条款） | **有**：更新器 registry 回退、失败传播、旧子目录元数据迁移、内容差异识别与可回滚切换（DEC-020、DEC-034） | 2026-07-30 |

## 各 Skill 详情

### `skills/skill-template`

- **来源类型**：starter 原创（本仓库维护的模板骨架）。
- **上游**：无。本目录是仓库原创内容，定位为 Skill 仓库起点模板。
- **目录内容**：`SKILL.md`、`LICENSE.txt`、`CHANGELOG.md`、`DECISIONS.md`、`ROADMAP.md`、`TASKS.md`、`.env.example`、`.gitignore`、`assets/`、`output/`、`references/`、`scripts/`。
- **许可证现状**：MIT。`SKILL.md` frontmatter 与目录 `LICENSE.txt` 已一致；复制到独立目录后仍携带完整授权文本（DEC-035）。
- **本地补丁**：不适用（原创）。
- **风险与待办**：模板许可证问题已关闭。复制者如果改用其他许可证，必须同时替换 `LICENSE.txt` 与 frontmatter `license`。

### `skills/todo`

- **来源类型**：starter 原创（本仓库维护的端到端标准示例 Skill）。
- **上游**：无。本目录是仓库原创内容，定位为 T-007 端到端标准示例——把教程 `04-创建Skill/07-带脚本-Skill.md` 里散落的 `todo.py` 片段落盘成完整可运行的带脚本型 Skill。
- **目录内容**：`SKILL.md`、`LICENSE.txt`、`CHANGELOG.md`、`DECISIONS.md`、`ROADMAP.md`、`TASKS.md`、`.gitignore`、`assets/todos.example.json`、`references/README.md`、`scripts/todo.py`。采用 skill-template 双 profile 中的「带脚本维护型最简变体」：无配置需求，故不含 `.env.example`、`config.yaml.example`、`requirements.txt`。
- **许可证现状**：MIT。`SKILL.md` frontmatter 与目录 `LICENSE.txt` 一致。
- **本地补丁**：不适用（原创）。
- **数据位置**：`todos.json` 写到运行目录（cwd），不进仓库（`.gitignore` 已忽略），便于在临时目录隔离测试。回归测试 `tests/test_skill_todo.py` 覆盖正常路径、4 类错误路径、守恒性（防假绿）和干净隔离。

### `skills/find-skills`

- **来源类型**：第三方收录。
- **上游**：`https://github.com/vercel-labs/skills`，对应路径 `skills/find-skills/SKILL.md`。本目录内容是 vercel-labs 维护的 "open agent skills" 生态（即 `npx skills` CLI 与 https://skills.sh/ 背后的仓库）中的同名 Skill。
- **同步 SHA**：本地 `SKILL.md` 的 Git blob 与上游提交 `66a7b901aad3b30f541f646199ff0df3050b764b` 完全一致。2026-07-30 核对时上游 HEAD 为 `7cb7db64dc1201052dea305e508a2fc490f7e5e2`，最近一次修改该文件的提交为 `773fb2c7bbf16781670a3520affc4abd0c6151ae`。
- **许可证现状**：MIT。上游现已在仓库根提供 MIT LICENSE（Copyright 2026 Vercel, Inc.），本目录同步保留为 `LICENSE.txt`。
- **本地补丁**：相对锁定基线无补丁。
- **风险与待办**：上游 `0b8fb22a`、`773fb2c7` 增加质量核验、leaderboard 和命令更新，本地尚未同步。应先评估其中安装量/Star 阈值是否适合本仓库的安全口径，再决定整体升级，不能只改 SHA。

### `skills/git-batch-commit`

- **来源类型**：legal-skills 同步。
- **上游**：`https://github.com/cat-xierluo/legal-skills`，对应路径 `skills/git-batch-commit/`。
- **同步 SHA**：`efde445`（`legal-skills/main` 最新一次触碰 `skills/git-batch-commit` 的提交：`feat(git-batch-commit): 新增同 Skill 内伴随变更合并规则`，版本 `1.4.1`）。
  - 通过 `git log --oneline legal-skills/main -- skills/git-batch-commit` 取得。
- **许可证现状**：MIT。
  - `SKILL.md` frontmatter：`license: MIT`。
  - 上游仓库 `legal-skills` 根 LICENSE 为 MIT，署名 `杨卫薪律师（微信ywxlaw）`。
- **本地补丁**：无。当前仓库内容与 `legal-skills/main` 一致，1.4.1 同步已经进入仓库历史。
- **风险与待办**：后续同步仍按 AGENTS.md 的备份、对比和整目录覆盖流程执行。

### `skills/skill-creator`

- **来源类型**：第三方收录。
- **上游**：`https://github.com/anthropics/skills`，对应路径 `skills/skill-creator/SKILL.md`（Anthropic 官方维护的 meta-skill，用于创建、迭代和评估 Skill）。
- **同步 SHA**：除许可证版权行外，本地目录（排除 `.DS_Store` / `__pycache__`）与上游提交 `3d59511518591fa82e6cfcf0438d68dd5dad3e76` 完全一致。2026-07-30 核对时上游 HEAD 为 `b29e7cf65e5cb78a5ac33d582270551bc74a14eb`。
- **许可证现状**：Apache-2.0。
  - 目录内 `skills/skill-creator/LICENSE.txt` 为完整的 Apache License 2.0 文本，版权占位符已按上游 `b9e19e6f` 修正为 `Copyright 2026 Anthropic, PBC.`。
  - `SKILL.md` frontmatter 未显式声明 `license` 字段。
- **本地补丁**：基线代码无本地补丁；许可证版权行同步了基线之后的上游修正。
- **风险与待办**：
  - Apache-2.0 包含专利授权条款与 NOTICE 文件义务；若仓库选择 MIT 作为根许可证，需要在第三方声明中显式说明"本目录内容仍按 Apache-2.0 提供"。
  - 应保留 `LICENSE.txt` 与（若存在）`NOTICE` 文件，不可被根 LICENSE 覆盖。
  - 上游 `b0cbd3df` 以后改用 `claude -p`、补现有 Skill 更新指引等，本地尚未同步；需单独跑 eval/脚本测试后升级。

### `skills/skill-manager`

- **来源类型**：legal-skills 同步（**fork/派生版**，存在长期本地修改，不按无差异镜像管理）。
- **上游**：`https://github.com/cat-xierluo/legal-skills`，对应路径 `skills/skill-manager/`。
- **同步 SHA / 派生版本**：上游基线为 `f801450`（`legal-skills/main` 最新一次触碰 `skills/skill-manager` 的提交：`fix(skill-manager): install.sh 对同路径 skills 去重`，版本 `1.7.0`）；starter 本地派生版为 `1.8.0`。
  - 通过 `git log --oneline legal-skills/main -- skills/skill-manager` 取得。
- **许可证现状**：MIT。
  - 目录内 `LICENSE.txt` 为 MIT 文本，署名 `杨卫薪律师（微信ywxlaw）`。
  - `SKILL.md` frontmatter 写 `license: Complete terms in LICENSE.txt`（指向同目录 LICENSE.txt，即 MIT）。
- **本地补丁**：**有**。除 DEC-020 的 POSIX `sed` 和 registry 回退外，DEC-034 又补充：clone URL / branch / subpath 分字段、简写来源解析、旧 `/tree/...` 记录迁移（含已记录分支名中的 `/`）、单项与批量失败传播、commit + 内容差异识别、目标旁暂存与失败回滚、14 个网络隔离回归测试。该目录不按无差异镜像管理。
- **风险与待办**：下次同步 upstream 时需三方合并（不能直接 `git checkout` 覆盖，会丢失本地补丁）；同步流程见 `/sync-upstream` 命令与 AGENTS.md 上游同步约定。适合把通用修复回馈 upstream，减少长期 fork 成本。

## 跨仓库来源汇总

本仓库当前引入了 **3 个**上游来源：

1. **cat-xierluo/legal-skills** — 本仓库已配置为 git remote（`git remote -v` 可见 `legal-skills`）。提供 `git-batch-commit` 和 `skill-manager`，均为 MIT。
2. **vercel-labs/skills** — 提供 `find-skills`。未配置长期 git remote；本地基线已锁定到 `66a7b901`，最近核对的上游 HEAD 为 `7cb7db64`。
3. **anthropics/skills** — 提供 `skill-creator`。未配置长期 git remote；本地基线已锁定到 `3d595115`，最近核对的上游 HEAD 为 `b29e7cf6`。

## 核对方法备忘

下次核对时建议执行：

```bash
# 1. 拉取最新上游
git fetch legal-skills

# 2. 查看 legal-skills 同步的 Skill 最新 commit
git log --oneline -1 legal-skills/main -- skills/git-batch-commit
git log --oneline -1 legal-skills/main -- skills/skill-manager

# 3. 比对本地与上游差异（空输出 = 完全一致）
git diff --stat HEAD legal-skills/main -- skills/git-batch-commit
git diff --stat HEAD legal-skills/main -- skills/skill-manager

# 4. 对于第三方收录（find-skills / skill-creator），需要手动 clone 上游再 diff；
#    同时记录“本地基线 SHA”和“最近核对的上游 HEAD”，不要混为同一版本。
git clone --depth 1 https://github.com/vercel-labs/skills /tmp/vercel-skills
diff -r skills/find-skills /tmp/vercel-skills/skills/find-skills

git clone --depth 1 https://github.com/anthropics/skills /tmp/anthropic-skills
diff -r skills/skill-creator /tmp/anthropic-skills/skills/skill-creator
```

## 待核对清单（Open Items）

- [ ] 评估是否把 `find-skills` 从锁定基线 `66a7b901` 升级到当前上游；先审查新增的安装量/Star 阈值。
- [ ] 评估是否把 `skill-creator` 从锁定基线 `3d595115` 升级到当前上游，并为 `claude -p` 优化链路补回归测试。
