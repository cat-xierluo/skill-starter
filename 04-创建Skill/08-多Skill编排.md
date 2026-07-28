# 08 多 Skill 编排

上一篇 [07 带脚本 Skill](./07-带脚本-Skill.md) 解决了「单个 Skill 能干实事」的问题。但现实任务常常一个 Skill 干不完——读个文件、跑个脚本、查个状态、再生成一段文字，串起来才完整。这篇讲**多 Skill 编排**：怎么让多个 Skill 接力完成一件更复杂的事、边界画在哪里、什么时候该拆、什么时候不该拆。我们把 [06 纯说明型 Skill](./06-纯说明型-Skill.md) 造的「团队 commit 规范说明卡」`commit-style`（会说型）和 [07 带脚本 Skill](./07-带脚本-Skill.md) 造的「待办管理」`todo`（会做型）串成一条「扫未完成项 → 生成 commit message → 校验格式」的小编排。

## 本篇目标

读完之后你将能够：

- 区分「编排」和「在脚本里调另一个 Skill」的差别，并判断什么时候该编排、什么时候不该。
- 用三机制（description 配合 / SKILL.md「与其他技能配合」章节 / `references/workflow.md`）让 AI 理解你的编排意图。
- 画清楚两个 Skill 之间的职责边界，避免功能重叠或断档。
- 从模板创建一个真正可用的编排型 Skill，包含 `references/workflow.md`。
- 识别 6 类常见编排陷阱，并知道怎么避免。

## 前置知识

- [06 纯说明型 Skill](./06-纯说明型-Skill.md)：知道「会说型 Skill」长什么样，本文会用 `commit-style` 作示例。
- [07 带脚本 Skill](./07-带脚本-Skill.md)：知道「会做型 Skill」长什么样，脚本契约怎么写，本文会用 `todo` 作示例。
- [SKILL-ORCHESTRATION-GUIDE.md](./SKILL-ORCHESTRATION-GUIDE.md)：本文核心概念的理论骨架都来自这份上游指南，建议先扫一遍 §1（编排概述）和 §2（AI 如何理解编排）。
- [基于模板创建](./03-基于模板创建.md)：动手步骤会复制模板，模板用法见这篇。

## 核心概念：编排是描述接力，不是把脚本串起来

### 「编排」是什么，不是什么

**编排（orchestration）**指让多个 Skill 在一次任务里**接力完成**不同子步骤，由 AI 根据上下文判断「下一步该交给谁」。这里有个关键原则（来自 `SKILL-DEV-GUIDE.md` §10 技能间协作）：**Skill 之间通过 AI 智能协调，不直接在脚本里 `import` 或调用别的 Skill 的内部脚本**。

为什么？因为脚本里硬调别 Skill 路径，会带来三个硬伤：路径依赖（对方目录结构一改你就崩）、平台耦合（对方的退出码约定你得自己复刻）、职责不清（对方改了职责你跟着错）。编排把这些事交给 AI 看 SKILL.md 和 `references/workflow.md` 自然协调，比硬编码稳得多。

### 三机制：让 AI 看得懂你的编排

AI 怎么知道「这个任务应该这样接力」？三种机制，按复杂度递进：

| 机制 | 用在哪 | 优点 | 局限 |
|------|-------|------|------|
| description 配合 | 两个 Skill 都触发时用 | 零额外文件，AI 自然识别 | 多步骤、有条件判断时 AI 可能漏 |
| SKILL.md「与其他技能配合」章节 | 简单协作、一句话交接 | 写在正文里，AI 总会看到 | 长流程塞进正文会膨胀 |
| `references/workflow.md` | 复杂多步骤、有条件判断 | 详细流程按需加载，不污染 SKILL.md | 多一个文件，AI 不一定自动去看 |

完整定义见 `SKILL-ORCHESTRATION-GUIDE.md` §2，下面用一个反例和一个正例说清差别。

**反例**（脚本里硬调别 Skill）：

```python
# ❌ 不要这样写：在 todo/scripts/todo.py 里直接调 commit-style 的脚本
import subprocess
result = subprocess.run([
    "../commit-style/scripts/check_msg.py",  # 路径硬编码
    msg
], capture_output=True)
```

**正例**（让 AI 看 SKILL.md 自然协调）：

```markdown
# todo

## 何时调用
...（省略）

## 与其他技能配合
当用户说「把今天做完的待办一次性提交」时：
1. 用本 Skill 的 `list --pending` 拿到未完成项
2. 按类别生成 commit message（草案）
3. 调用 [commit-style] 校验格式，不合规则修订
```

正例里 AI 知道「接下来交给 `commit-style`」，但实际动作由 AI 在调用时执行，不会因为 `commit-style` 目录改名就崩。

### 编排的边界：什么时候该编排

不是所有任务都该拆成多 Skill。判断标准有三条：

1. **职责是否真的不同**：如果两个 Skill 干的事 80% 重叠，合并成一个；剩下的 20% 用分支处理。
2. **是否独立可复用**：被调的那个 Skill，如果别的场景也要用，就独立编排；如果只为这一处存在，就合进来。
3. **是否需要独立维护**：如果两个 Skill 的演进节奏不同（比如一个改格式约定、一个改存储格式），拆开编排更省事。

反过来说，**不该编排**的常见情形：两个 Skill 强耦合、改一个必改另一个；或者任务量太小，多一个 Skill 反而是负担。

## 实例分析：仓库里的编排长什么样

仓库里现成可用的编排样本是 `skills/git-batch-commit/SKILL.md` 的「与 git-workflow 的职责边界」表。它没有用 `references/workflow.md`，而是把编排意图写在 SKILL.md 里——这是**简单协作**的典型形态。

```markdown
## 与 git-workflow 的职责边界

`git-batch-commit` 是提交拆分工具，不是完整 Git 工作流控制器。

| 场景 | 使用哪个 Skill | 说明 |
|------|---------------|------|
| 将已暂存的混合变更拆成多个 commit | `git-batch-commit` | 本 Skill 的核心职责 |
| 判断是否能 merge / push / close PR | `git-workflow` | 本 Skill 不做合并门禁 |
| PR 合入 main 的 commit 标题是否带 `(#N)` | `git-workflow` | 本 Skill 只在生成普通 commit 时保留 Issue/Task 引用 |
| 直接解决 GitHub Issue 是否应写 `Closes #N` | `git-workflow` | 本 Skill 只写 `Refs #N`，不关闭 Issue |
| 项目本地任务引用 | `cross-agent-collab` 定任务来源，`git-batch-commit` 写引用 | 使用 `--local-ref "project-task Issue #13"` |

当用户只是说"把这些改动提交一下 / 拆分提交"，使用本 Skill；
当用户说"合并 PR / 拉 PR 到 main / 推送 / 关闭 issue"，同时遵循 `git-workflow`。
```

`SKILL-ORCHESTRATION-GUIDE.md` §2.2 给了**复杂编排**的样本（GitHub Star 周报），用 `references/workflow.md` 分四步描述——本文动手步骤会照这个模式造一个。

## 动手步骤：创建「待办提交编排」Skill

我们要造一个编排型 Skill `todo-commit`（演示用，不实际放到 `skills/`），把 `todo` 和 `commit-style` 串起来。下面是 5 步。

### 第 1 步：从模板复制，定边界

照 [基于模板创建](./03-基于模板创建.md) 复制 `skills/skill-template/` 到独立目录。命名用 `todo-commit`（目录名与 `name` 字段保持一致，参见 `scripts/check_skills.py` 的强制规则）。

**定边界**这一步比命名更重要。先在纸上画清楚：

| 步骤 | 谁负责 | 产物 |
|------|-------|------|
| 1. 取未完成项 | `todo` | `todos.json` 里的 `pending` 列表 |
| 2. 生成 commit message 草案 | `todo-commit` 自己 | 一段文字 |
| 3. 校验格式 | `commit-style` | 通过 / 不通过 + 修订建议 |
| 4. 写 commit | 用户或 Agent | 一个 commit |

**两个边界要守住**：

- `todo-commit` **不读 `todos.json` 的存储格式**——那是 `todo` 的事。`todo-commit` 只调 `todo` 的脚本接口（`list --pending`）。
- `todo-commit` **不校验 Conventional Commits 格式**——那是 `commit-style` 的事。`todo-commit` 只生成草案，把校验交给 `commit-style`。

边界画清，下一步写 frontmatter 才能精准描述意图。

### 第 2 步：写 frontmatter，把编排意图写进 description

`name` 固定为 `todo-commit`，`description` 要体现**编排意图**——AI 是靠 description 触发 Skill 的。

```markdown
---
name: todo-commit
description: |
  当用户要把"待办管理 Skill（todo）里的未完成项一次性提交"时使用。
  本 Skill 不自己读 todos.json，也不校验 commit 格式：
  取未完成项交给 todo、生成 commit message 草案、校验格式交给 commit-style。
  触发关键词：批量提交待办、把待办 commit 掉、按 todos 提交。
---
```

三个要点：

1. **说明编排链**：AI 读到 description 就知道要接力两个别的 Skill。
2. **划清「不做什么」**：明确不读存储、不校验格式，避免功能重叠。
3. **给触发关键词**：帮助 AI 判断何时触发（更系统的触发质量优化见 [09 触发质量与 eval](./09-触发质量与eval.md)）。

### 第 3 步：在正文里写「与其他技能配合」章节

复杂流程不要塞进 SKILL.md 正文，但**短交接必须写进正文**——AI 不会主动翻 `references/`，除非正文告诉它去看。

```markdown
# todo-commit

## 何时调用

用户说「把今天做完的待办一次性提交」「按 todos 生成一批 commit」「批量提交待办」时使用。

## 工作流概览

1. 调 [todo] 的 `list --pending` 拿到未完成项。
2. 按类别聚合，生成 commit message 草案（草案格式见 references/workflow.md 第 2 步）。
3. 调 [commit-style] 校验草案，不合规按其反馈修订。
4. 产出最终 commit message 列表，由用户或 Agent 实际执行 `git commit`。

## 与其他技能配合

- [todo]：本 Skill 的数据来源。**只通过其脚本接口调用**，不直接读 `todos.json`。
- [commit-style]：本 Skill 的格式守门员。**草案生成后必调**，合规才进入下一步。

边界：本 Skill 不维护待办数据，不校验 commit 格式；详见 references/workflow.md 的职责分工说明。
```

正文里**必须出现**「详见 references/workflow.md」这种引导句——否则 AI 不知道 `references/workflow.md` 存在（`SKILL-ORCHESTRATION-GUIDE.md` §2.2 强调过这一点）。

### 第 4 步：把流程拆进 references/workflow.md

`SKILL-ORCHESTRATION-GUIDE.md` §2.2 推荐把复杂多步骤、有条件判断的流程放进 `references/workflow.md`。我们的 `todo-commit` 有四步 + 修订分支，正好适用。

新建 `references/workflow.md`：

````markdown
# 待办提交编排流程

## 职责分工

| 步骤 | 谁做 | 做什么 | 产物 |
|------|-----|-------|------|
| 1 | todo | 列出未完成项 | pending 列表（JSON） |
| 2 | todo-commit | 按类别聚合并生成草案 | commit message 草案文本 |
| 3 | commit-style | 校验 Conventional Commits 格式 | 通过 / 不通过 + 修订建议 |
| 4 | 用户 / Agent | 实际执行 `git commit` | 一个或多个 commit |

> **不要越界**：todo-commit 不读 todos.json 的存储格式，不校验 commit 格式。

## Step 1：取未完成项

```bash
python3 ../todo/scripts/todo.py list --pending
```

输出示例：

```text
[1] [ ] 修 CI 门禁报错
[2] [ ] 写 08 多 Skill 编排
[3] [ ] 更新 README 许可证段
```

## Step 2：生成 commit message 草案

按以下规则聚合：

- 文档类改动 → `docs: ...`
- 工程类改动 → `feat:` / `fix:` / `refactor:` / `ci:` ...
- 多类别混合 → 按文件数最多的类别为主，其余拆为独立 commit

输出示例：

```text
docs: 更新 CONTENT-MATRIX 与实际产出文件的偏差
ci: 接入 GitHub Actions 合并前门禁
```

## Step 3：校验格式

把草案交给 commit-style：

```bash
# 由 AI 按 commit-style 的 SKILL.md 调用，此处不展开其脚本
```

- 通过 → 进入 Step 4。
- 不通过 → 按 commit-style 反馈修订后重跑本步。

## Step 4：执行 commit

由用户或 Agent 按草案逐条执行 `git commit`。**本 Skill 不自动执行**——避免误提交。
````

注意两个细节：

- **不要把别的 Skill 的脚本路径写死**（如 `../commit-style/scripts/...`）。第 3 步写「由 AI 按 commit-style 的 SKILL.md 调用」就够了。
- **不要自动执行 commit**。编排 Skill 只产方案，最后一步留给人或 Agent，避免误操作。

### 第 5 步：本地走查编排触发

写完跑三件事：

1. **描述完整性**：把 `todo-commit/SKILL.md` 的 description 单独看一遍，问自己：「AI 只看这段文字，能判断该交给 `todo` 和 `commit-style` 吗？」如果不能，补一句。
2. **正文引导**：确认 SKILL.md 正文的「与其他技能配合」章节**明确提到**「详见 references/workflow.md」。
3. **跑一遍 `scripts/check.sh`**：

```bash
bash scripts/check.sh
```

通过即代表：frontmatter 合法、相对链接有效、计数与正文一致（5 步、6 条错误、5 题自测）。

跨平台提示：上面命令里的 `python3` 在 macOS 和 Linux 自带；Windows 通常要敲 `python`（且需先装好 Python，见 [开发环境与依赖入门](../02-工具指南/08-开发环境与依赖入门.md)）。`scripts/check.sh` 是 Bash，Windows 推荐用 Git Bash 或 WSL（见 [终端与命令行入门](../02-工具指南/06-终端与命令行入门.md)）。

## 常见错误

下面 6 条按症状命名，展开说为什么错、怎么改。

### 在脚本里 `import` 或 `subprocess` 调别 Skill

`todo/scripts/todo.py` 里写 `from commit_style import check` 或 `subprocess.run(["../commit-style/scripts/check_msg.py", ...])`——一改路径全崩。改用 SKILL.md + `references/workflow.md` 描述接力关系，让 AI 在调用时按 SKILL.md 协调。

### 把编排写死成 if-else 脚本

为了"可控"，把所有分支判断写进 Python 脚本里：先 `if user_says == "批量提交"`，再嵌套 N 层 `elif` 调不同 Skill。这本质是把编排从 SKILL.md 挪进了脚本，AI 的灵活性归零。正确做法是把判断交给 AI，脚本只负责**确定性操作**（读文件、跑命令、算结果）。

### 角色边界重叠

`todo-commit` 既读 `todos.json` 又校验 commit 格式——两个 Skill 都不需要了。编排的价值在于**职责清晰**：`todo-commit` 只做「聚合 + 草案」，别的都不碰。重叠了就没必要编排，合并回 `todo` 一个 Skill 就够了。

### workflow.md 不在正文引导就失效

把详细流程写进 `references/workflow.md`，但 SKILL.md 正文**没提到**这个词——AI 不会主动去翻 `references/`（除非说明文字告诉它）。务必在「与其他技能配合」章节写一句「详见 references/workflow.md」。

### description 没体现编排意图

`description` 写「`todo-commit`：帮你提交待办」——AI 只知道你干「提交待办」，不知道还要接力 `todo` 和 `commit-style`。结果可能直接调 `todo` 自己，或者跳过 `commit-style` 校验。description 必须**点出依赖的 Skill 名字**，AI 才能协调。

### 以为编排越多越好

为了"灵活"，把 7 个 Skill 串成一个长链——每多一个 Skill，AI 的协调成本指数级上升（理解 7 个职责边界、决定接力顺序）。三条建议：（1）能用一个 Skill 解决的别编排；（2）编排链尽量 ≤ 3 个；（3）能合并的相邻步骤合并。

## 自测题 / 验收

1. **判定编排必要性**：拿到一个需求「把 GitHub Issue 转成待办项并按周提醒」，你能用三条边界规则（职责真不同 / 独立可复用 / 独立演进）判断该不该拆成两个 Skill 吗？
2. **三机制选择**：两种情形——「用户说『把待办 commit 掉』时顺便提醒格式」和「每周日生成 GitHub Star 周报」。各该用三机制（description / SKILL.md 配合章节 / workflow.md）里的哪种？为什么？
3. **画职责边界**：如果让你编排 `commit-style` + `todo`，能写出像 `git-batch-commit` 那样的「职责边界表」吗？至少列 3 行场景对照。
4. **找越界**：看自己刚写的 `todo-commit/SKILL.md`，问：有没有哪句描述让 AI 误以为本 Skill 直接读 `todos.json`？如果有，改 description。
5. **数清边界**：自己 review 上面动手步骤里写的 `references/workflow.md`，确认「职责分工」表的行数等于 Step 数（4 行 = 4 步），并且没有任何行说"todo-commit 自己校验 commit 格式"。

第 5 题能发现「表格行数 ≠ Step 数」或「边界越权」，说明你已经把编排的职责问题想透了。

## 下一篇

**下一篇（主线）**：[09 触发质量与 eval](./09-触发质量与eval.md)——编排搭好了，下一步要回答「AI 真能在该触发的时候触发、不该触发的时候别触发吗」。正例 / 负例 / 边界 / 基线四件事一起讲。

- [06 纯说明型 Skill](./06-纯说明型-Skill.md)：编排链里被调的「会说型」参考。
- [07 带脚本 Skill](./07-带脚本-Skill.md)：编排链里被调的「会做型」参考，以及它的契约约定。
- [04 调试与发布](./04-调试与发布.md)：编排 Skill 怎么调试、怎么打 tag、怎么写安装说明。

---

**收尾给一个动作**：打开仓库里 `skills/git-batch-commit/SKILL.md`，把它的「职责边界」表抄到你手头的编排项目里——能抄明白，你就真的理解编排了。