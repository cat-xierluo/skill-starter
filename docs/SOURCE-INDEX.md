# Skill 来源与许可证索引（SOURCE-INDEX）

> Last updated: 2026-07-27
>
> 本文件是仓库级"第三方来源清单（source lock）"的事实层：记录 `skills/` 下每个 Skill 的来源类型、上游 URL、同步 commit SHA、许可证、本地补丁与最近核对日期。
>
> 本文件**只记录事实**，不替仓库选定具体 LICENSE 条款。仓库级许可证方案见 [LICENSE-PLAN.md](./LICENSE-PLAN.md)；选定条款的决策权属于仓库维护者（参见 `docs/DECISIONS.md` DEC-013）。

## 总表

| 目录名 | 来源类型 | 上游 URL | 同步 commit SHA / tag | 许可证 | 本地补丁 | 最近核对 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `skills/skill-template` | starter 原创 | —（本仓库原创） | — | 未声明（SKILL.md frontmatter 未填 `license`，目录无 `LICENSE.txt`） | —（原创） | 2026-07-27 |
| `skills/find-skills` | 第三方收录 | https://github.com/vercel-labs/skills （`skills/find-skills/SKILL.md`） | 待确认（未做 SHA lock） | 待确认（仓库根未提供 LICENSE，GitHub API `license=null`，见 [vercel-labs/skills#946](https://github.com/vercel-labs/skills/issues/946)） | 待核对 | 2026-07-27 |
| `skills/git-batch-commit` | legal-skills 同步 | https://github.com/cat-xierluo/legal-skills | `efde445`（`legal-skills/main` 上游最新：`feat(git-batch-commit): 新增同 Skill 内伴随变更合并规则`，版本 1.4.1） | MIT（frontmatter `license: MIT`；上游仓库根 LICENSE 为 MIT） | 当前工作目录内容与 `legal-skills/main` 一致；历史提交里曾滞后于 upstream（HEAD 提交版本为 1.2.4，工作目录已升级到 1.4.1，**未提交**） | 2026-07-27 |
| `skills/skill-creator` | 第三方收录 | https://github.com/anthropics/skills （`skills/skill-creator/SKILL.md`） | 待确认（未做 SHA lock） | Apache-2.0（目录内 `LICENSE.txt` 为 Apache License 2.0；frontmatter 未显式声明 `license` 字段） | 待核对 | 2026-07-27 |
| `skills/skill-manager` | legal-skills 同步 | https://github.com/cat-xierluo/legal-skills | `f801450`（`legal-skills/main` 上游最新：`fix(skill-manager): install.sh 对同路径 skills 去重`，版本 1.7.0） | MIT（`LICENSE.txt` 头部为 MIT；frontmatter 写 `license: Complete terms in LICENSE.txt`） | 无（`git diff HEAD legal-skills/main -- skills/skill-manager` 为空） | 2026-07-27 |

## 各 Skill 详情

### `skills/skill-template`

- **来源类型**：starter 原创（本仓库维护的模板骨架）。
- **上游**：无。本目录是仓库原创内容，定位为 Skill 仓库起点模板。
- **目录内容**：`SKILL.md`、`CHANGELOG.md`、`DECISIONS.md`、`ROADMAP.md`、`TASKS.md`、`.env.example`、`.gitignore`、`assets/`、`output/`、`references/`、`scripts/`。
- **许可证现状**：未声明。`SKILL.md` frontmatter 中 `license` 字段仅作为注释示例出现（`# license: MIT  # 示例值，按实际选择`），未填写实际条款；目录无 `LICENSE.txt`。
- **本地补丁**：不适用（原创）。
- **风险与待办**：模板自身缺许可证声明。仓库级方案落地后，需要决定模板是否预置 `LICENSE.txt` 占位与 `license` 字段示例（见 [LICENSE-PLAN.md](./LICENSE-PLAN.md) "待用户决策清单"）。

### `skills/find-skills`

- **来源类型**：第三方收录。
- **上游**：`https://github.com/vercel-labs/skills`，对应路径 `skills/find-skills/SKILL.md`。本目录内容是 vercel-labs 维护的 "open agent skills" 生态（即 `npx skills` CLI 与 https://skills.sh/ 背后的仓库）中的同名 Skill。
- **同步 SHA**：待确认。当前未对该 Skill 做 commit SHA 锁定；本轮核对未执行 `git fetch` 与 SHA 比对。
- **许可证现状**：待确认。
  - 本目录无 `LICENSE.txt`，frontmatter 也未声明 `license`。
  - vercel-labs/skills 仓库根目前**未提供显式 LICENSE 文件**：GitHub API 返回 `"license": null`，社区已有 [issue #946 "Add explicit LICENSE file"](https://github.com/vercel-labs/skills/issues/946) 索要 LICENSE。
  - 第三方资料曾提到 MIT，但通常指发布到 npm 的 CLI 包，不能直接套用到 `skills/find-skills` 目录内容。
- **本地补丁**：待核对（未做差异比对）。
- **风险与待办**：上游许可证缺失意味着从严理解时本目录处于"未授权使用"灰区。建议在仓库级方案中明确：在用户决定是否继续分发该 Skill 前，先到上游确认许可证状态或考虑替换为来源清晰的等价 Skill。

### `skills/git-batch-commit`

- **来源类型**：legal-skills 同步。
- **上游**：`https://github.com/cat-xierluo/legal-skills`，对应路径 `skills/git-batch-commit/`。
- **同步 SHA**：`efde445`（`legal-skills/main` 最新一次触碰 `skills/git-batch-commit` 的提交：`feat(git-batch-commit): 新增同 Skill 内伴随变更合并规则`，版本 `1.4.1`）。
  - 通过 `git log --oneline legal-skills/main -- skills/git-batch-commit` 取得。
- **许可证现状**：MIT。
  - `SKILL.md` frontmatter：`license: MIT`。
  - 上游仓库 `legal-skills` 根 LICENSE 为 MIT，署名 `杨卫薪律师（微信ywxlaw）`。
- **本地补丁**：当前工作目录与 `legal-skills/main` 内容一致（无本地修改）。
  - 但仓库 HEAD 提交里的 `skills/git-batch-commit/SKILL.md` 仍是旧版本 `1.2.4`，工作目录里已升级到 `1.4.1` 但**尚未 commit**（`git status` 显示为已暂存修改）。
  - 即：相对 upstream 无派生补丁，但相对仓库 HEAD 是一次进行中的同步升级。
- **风险与待办**：完成同步后应补一次提交，并在 DECISIONS 中记录"由 1.2.4 升级到 1.4.1"。

### `skills/skill-creator`

- **来源类型**：第三方收录。
- **上游**：`https://github.com/anthropics/skills`，对应路径 `skills/skill-creator/SKILL.md`（Anthropic 官方维护的 meta-skill，用于创建、迭代和评估 Skill）。
- **同步 SHA**：待确认。当前未做 SHA 锁定。
- **许可证现状**：Apache-2.0。
  - 目录内 `skills/skill-creator/LICENSE.txt` 为完整的 Apache License 2.0 文本。
  - `SKILL.md` frontmatter 未显式声明 `license` 字段。
- **本地补丁**：待核对（未做差异比对）。
- **风险与待办**：
  - Apache-2.0 包含专利授权条款与 NOTICE 文件义务；若仓库选择 MIT 作为根许可证，需要在第三方声明中显式说明"本目录内容仍按 Apache-2.0 提供"。
  - 应保留 `LICENSE.txt` 与（若存在）`NOTICE` 文件，不可被根 LICENSE 覆盖。

### `skills/skill-manager`

- **来源类型**：legal-skills 同步。
- **上游**：`https://github.com/cat-xierluo/legal-skills`，对应路径 `skills/skill-manager/`。
- **同步 SHA**：`f801450`（`legal-skills/main` 最新一次触碰 `skills/skill-manager` 的提交：`fix(skill-manager): install.sh 对同路径 skills 去重`，版本 `1.7.0`）。
  - 通过 `git log --oneline legal-skills/main -- skills/skill-manager` 取得。
- **许可证现状**：MIT。
  - 目录内 `LICENSE.txt` 为 MIT 文本，署名 `杨卫薪律师（微信ywxlaw）`。
  - `SKILL.md` frontmatter 写 `license: Complete terms in LICENSE.txt`（指向同目录 LICENSE.txt，即 MIT）。
- **本地补丁**：无。`git diff --stat HEAD legal-skills/main -- skills/skill-manager` 输出为空，HEAD 与 upstream 完全一致。
- **风险与待办**：无紧急项。

## 跨仓库来源汇总

本仓库当前引入了**两**个上游来源：

1. **cat-xierluo/legal-skills** — 本仓库已配置为 git remote（`git remote -v` 可见 `legal-skills`）。提供 `git-batch-commit` 和 `skill-manager`，均为 MIT。
2. **vercel-labs/skills** — 提供 `find-skills`。尚未配置为 git remote，未做 SHA 锁定。
3. **anthropics/skills** — 提供 `skill-creator`。尚未配置为 git remote，未做 SHA 锁定。

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

# 4. 对于第三方收录（find-skills / skill-creator），需要手动 clone 上游再 diff
git clone --depth 1 https://github.com/vercel-labs/skills /tmp/vercel-skills
diff -r skills/find-skills /tmp/vercel-skills/skills/find-skills

git clone --depth 1 https://github.com/anthropics/skills /tmp/anthropic-skills
diff -r skills/skill-creator /tmp/anthropic-skills/skills/skill-creator
```

## 待核对清单（Open Items）

- [ ] `find-skills` 上游 SHA lock 与许可证状态确认（vercel-labs/skills 仓库根目前无 LICENSE）。
- [ ] `skill-creator` 上游 SHA lock 与本地差异核对。
- [ ] `git-batch-commit` 工作目录中已升级到 1.4.1 的同步尚未 commit，需要尽快落盘。
- [ ] 仓库根尚未决定具体 LICENSE 条款（见 [LICENSE-PLAN.md](./LICENSE-PLAN.md)）。
- [ ] `skill-template` 自身是否预置 LICENSE 占位与 `license` 字段示例。
