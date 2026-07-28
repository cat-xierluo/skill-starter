# 09 触发质量与 eval

上一篇 [08 多 Skill 编排](./08-多Skill编排.md) 解决了「多个 Skill 怎么接力」的问题。但整条链要能跑通，有个前提一直没回答——**AI 真能在该触发某个 Skill 的时候触发它、不该触发的时候别误触发吗？** 这就是触发质量。本篇讲清怎么用 eval（evaluation，评估）量化「触发准不准」，让你改 `description`（触发命根子，见 [06](./06-纯说明型-Skill.md)）时有的放矢、改完知道有没有变好。我们拿 [06 纯说明型 Skill](./06-纯说明型-Skill.md) 造的 `commit-style`（团队 commit 规范说明卡）跑一遍 trigger eval 流程。

## 本篇目标

读完之后你将能够：

- 区分「触发质量 eval」和「执行质量 eval」，知道各自测什么、用哪种数据格式。
- 用四件事（正例 / 负例 / 边界例 / 基线）给任意 Skill 写一份合格的触发评估集。
- 识别「near-miss（近邻负例）」并理解为什么它比明显无关的负例有价值得多。
- 读懂官方 skill-creator 的 `run_loop.py` 自动优化循环，知道它怎么防过拟合。
- 识别 6 类常见触发评估陷阱，避免「分数涨了但实际更糟」的假绿。

## 前置知识

- [06 纯说明型 Skill](./06-纯说明型-Skill.md)：本篇直接用 06 造的 `commit-style` 作示例；知道 `description` 是触发命根子。
- [07 带脚本 Skill](./07-带脚本-Skill.md)：知道 frontmatter 长什么样、`name` 和 description 字段怎么写。
- [08 多 Skill 编排](./08-多Skill编排.md)：编排链越长，单个 Skill 触发不准的代价越大，本篇会回到编排场景设计 near-miss。
- [SKILL-DEV-GUIDE.md](./SKILL-DEV-GUIDE.md) §13 技能验证规范：本篇核心概念的中文化权威来源（这份是上游同步文件，只引用不修改）。

## 核心概念：触发质量的四件事

### 先分清两种 eval

Skill 的 eval 有两种，别混：

| 类型 | 测什么 | 数据格式 | 例子 |
|------|-------|---------|------|
| **触发质量 eval**（trigger eval，本篇主题） | AI 在这条用户输入下，**会不会触发**这个 Skill | `[{"query": "...", "should_trigger": true/false}]` | 用户说「帮我拆 commit」→ 应触发 `git-batch-commit` |
| **执行质量 eval**（完整 eval，另一回事） | 触发了之后，**输出对不对** | `evals/evals.json`（带 `id` / `prompt` / `expected_output` / `expectations`） | 触发 `commit-style` 后，给出的提交类型前缀是否符合 Conventional Commits |

本篇只讲前者。后者见 `skills/skill-creator/references/schemas.md` 的 `evals.json` schema 定义（仓库内现成可读）。混淆这两种，会导致你用执行质量的数据格式去测触发，写得很重却测不到点上。

### 四件事：正例 / 负例 / 边界例 / 基线

触发质量用四件事来量化。下面这张表对齐三套同义说法——它们说的是同一回事，只是出处不同：

| 本篇用词 | skill-creator 官方说法（英文） | `SKILL-DEV-GUIDE.md` §13 中文说法 | 它测什么 |
|---------|------------------------------|----------------------------------|---------|
| **正例** | should-trigger | 正向测试 | 该触发的，确实触发了 |
| **负例** | should-not-trigger | 负向测试 | 不该触发的，确实没触发 |
| **边界例** | near-miss（最有价值的一类负例） | 边缘案例（异常输入、边界条件） | 共享关键词但意图不同，最难判 |
| **基线** | with-skill vs without-skill baseline | （隐含：正向/负向都需要对照） | 有 Skill 比「没有 Skill / 旧版 Skill」好多少 |

前三件是「测什么」，第四件「基线」是「拿什么比」。基线这个词后面括注解释：你改了 `description` 之后想知道有没有变好，必须有个**对照物**——要么是「完全没装这个 Skill」，要么是「旧版 description 的 Skill」。`skills/skill-creator/SKILL.md` L169-186 明确要求 with-skill（有 Skill）和 baseline（无 Skill 或旧版）**在同一个 turn 里并行跑**，避免时间差引入的随机性。

### 为什么 near-miss 是最有价值的负例

`skills/skill-creator/SKILL.md` L348-358 有段权威论述：**should-not-trigger 里最有价值的是 near-miss（近邻负例）——共享关键词或概念、但实际意图不同的输入**。原因是明显的负例（比如「写个 fibonacci 函数」测 PDF skill）太容易，AI 不触发它证明不了什么；near-miss 才能测出 AI 是真懂意图还是只在做关键词匹配。

直接搬 skill-creator SKILL.md L348-356 的好/坏例对比（权威样本，不要自己编）：

**坏负例**（太明显，无意义）：

```text
"Format this data"
"Extract text from PDF"
"Create a chart"
```

**好负例 / near-miss**（共享关键词、意图不同，真正考验）：

```text
"ok so my boss just sent me this xlsx file (its in my downloads, called
something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a
column that shows the profit margin as a percentage. The revenue is in
column C and costs are in column D i think"
```

第二条虽长，但它是 near-miss 的样板：带文件路径、带个人背景、带列名、带具体细节——这才是真实用户会发的输入。skill-creator 强调 eval 数据「**必须真实，而不是抽象**」。

### 正例也要有讲究

正例（should-trigger，8-10 条）不是简单堆叠，要**覆盖**：同一个意图的不同措辞（正式 / 口语）、用户没点名 Skill 名字但显然需要、不常见用法、以及「这个 Skill 跟另一个 Skill 竞争，但应该由它赢」的场景。如果 10 条正例全是「帮我按团队格式写 commit」的变体，覆盖面太窄。

## 实例分析：仓库里能跑的 eval 闭环

仓库里现成的权威实现是 `skills/skill-creator/SKILL.md` 的「Description Optimization」段（L333-405）。它给了一套完整的 trigger eval 闭环：

1. **生成 20 条 trigger eval**（L337-358）：should-trigger 8-10 条 + should-not-trigger 8-10 条，存成 `[{"query": "...", "should_trigger": true}]` 的简单 JSON。
2. **用户确认**（L360+）：让用户审一遍、勾选 should-trigger、增删条目。
3. **`run_loop.py` 自动迭代**（L377-394）：自动改 description、每条跑 3 次取稳定触发率、**60% 训练集 / 40% 留出测试集**、迭代 5 轮、**按测试集分数**选 `best_description`。

最后一点是防过拟合的关键：如果你只看训练集分数，AI 可能死记硬背这 20 条，换个说法就不触发。留出 40% 当测试集，按测试集分数选最优 description，才算真学会了意图、而不是背题。

完整的 evals.json 结构定义见 `skills/skill-creator/references/schemas.md`（仓库内可读），配套脚本在 `skills/skill-creator/scripts/`（`run_eval.py`、`run_loop.py`、`aggregate_benchmark.py` 等）。本篇不展开这些脚本的具体用法——它们依赖 Claude Code 子进程，超出「触发质量」主题；有兴趣的读者按文内引用去 skill-creator 自己看。

## 动手步骤：给 commit-style 跑一次 trigger eval

下面 5 步演示用 06 的 `commit-style` 跑 trigger eval 流程。**全程在独立工作目录，不在仓库 `skills/` 下真造文件**（避免污染仓库），只展示数据和命令形态。

### 第 1 步：复制 commit-style 到独立工作目录

把 06 教程里 `commit-style` 的 SKILL.md 复制到独立目录（比如 `~/skill-eval-demo/commit-style/`），保留 06 写的正文，**只准备改 `description`**。这一步是为了「在已有 Skill 上做触发质量评估」，不是从零造 Skill。

```bash
# macOS / Linux
mkdir -p ~/skill-eval-demo/commit-style
cp <你的 commit-style SKILL.md> ~/skill-eval-demo/commit-style/SKILL.md
```

Windows 在 PowerShell 里把 `~/skill-eval-demo` 换成 `$HOME\skill-eval-demo`，`cp` 换成 `Copy-Item`（见 [终端与命令行入门](../02-工具指南/06-终端与命令行入门.md)）。

记下当前 description 的版本号（比如 `v1`），作为后面基线对照。

### 第 2 步：手写 trigger eval 数据

新建 `~/skill-eval-demo/commit-style/trigger-evals.json`，按 skill-creator SKILL.md L339-345 的格式。下面给一份针对 `commit-style` 的样本——**7 条 should-trigger + 7 条 should-not-trigger（含 3 条 near-miss）+ 3 条边界**，共 17 条（凑整 20 条可各补几条，这里示例精简）：

```json
[
  {"query": "把我刚才改的几个文件提交一下，按团队规范", "should_trigger": true},
  {"query": "这几行改动该怎么写 commit message 啊", "should_trigger": true},
  {"query": "commit 类型前缀我老分不清 feat 和 fix", "should_trigger": true},
  {"query": "帮我把 staged 的东西整理成规范提交", "should_trigger": true},
  {"query": "team lead 说我的 commit message 不规范，帮我看看", "should_trigger": true},
  {"query": "怎么按 conventional commits 写这条", "should_trigger": true},
  {"query": "review 说我提交标题格式不对", "should_trigger": true},

  {"query": "把我刚才改的几个文件 push 到远程", "should_trigger": false, "note": "near-miss：共享'提交'关键词，但意图是推送"},
  {"query": "这几个改动能不能 merge 进 main", "should_trigger": false, "note": "near-miss：共享'改动'，但意图是合并门禁"},
  {"query": "帮我看看 git log 为什么这么乱", "should_trigger": false, "note": "near-miss：共享 git 语境，但意图是查看历史"},
  {"query": "今天的天气怎么样", "should_trigger": false},
  {"query": "帮我写一个 fibonacci 函数", "should_trigger": false},
  {"query": "这道菜怎么做", "should_trigger": false},
  {"query": "推荐几本机器学习的书", "should_trigger": false},

  {"query": "commit", "should_trigger": "ambiguous", "note": "边界：极短，可能只是说命令名"},
  {"query": "帮我提交", "should_trigger": "ambiguous", "note": "边界：缺上下文，无法判断是否要规范"},
  {"query": "这几个文件提交一下顺便看看能不能合 PR 顺便push", "should_trigger": "ambiguous", "note": "边界：三件事混在一起，触发冲突"}
]
```

三个要点（对应 §核心概念）：

- **正例覆盖不同措辞**：口语、正式、带团队背景、不点名 Skill 都有。
- **负例含 3 条 near-miss**：前 3 条 should-trigger=false 都是「共享 git 语境但意图不同」，这才是 near-miss；后面 4 条明显无关的只是凑数。
- **边界例标注 `ambiguous`**：这些输入本身就含糊，AI 怎么判都算合理——它们的价值在于提醒你「这类输入需要 Skills 之间协商」，不是用来计分。

跨平台提示：JSON 文件用 UTF-8 保存（中文 query 才不会乱码）；Windows 上用记事本默认可能是 GBK，建议用 VS Code 或 `Set-Content -Encoding utf8`（见 [项目目录与文件格式入门](../02-工具指南/07-项目目录与文件格式入门.md)）。

### 第 3 步：拍 description 优化前快照

把当前 `description` 单独存一份，作为基线对照物：

```bash
# macOS / Linux
git -C ~/skill-eval-demo/commit-style init 2>/dev/null
git -C ~/skill-eval-demo/commit-style add SKILL.md
git -C ~/skill-eval-demo/commit-style commit -m "snapshot: description v1（基线）" 2>/dev/null
```

这一步看起来多余，但**没基线就没法说有没有变好**——这是后面跑分对比的前提。如果你跳过这步直接改 description，改完发现分数 90%，你根本不知道原来是多少。

### 第 4 步：跑 run_loop.py 迭代（引用命令，不展开）

按 `skills/skill-creator/SKILL.md` L382 的官方命令格式（仓库内可读原文，这里只引用形态）：

```bash
python -m scripts.run_loop \
  --skill-path ~/skill-eval-demo/commit-style \
  --evals-file ~/skill-eval-demo/commit-style/trigger-evals.json \
  --iterations 5
```

`run_loop.py` 会自动做四件事（详见 skill-creator SKILL.md L377-394）：

1. 把 17 条 eval **切 60% 训练 / 40% 测试**。
2. 每条跑 3 次取稳定触发率（避免单次随机）。
3. 迭代 5 轮，每轮自动微调 description。
4. **按测试集分数**选 `best_description`（不是训练集——这是防过拟合的关键）。

注意：本步骤依赖 Claude Code 子进程，在你的本地环境未必能直接跑通。跑不通也没关系——**前 3 步的数据准备才是触发质量评估的核心**，第 4 步是把它自动化。你完全可以手动对照 17 条 eval，逐条判断 AI 触发与否，自己记分。

### 第 5 步：跑分对比 with-skill vs baseline

迭代跑完后，对比三组分数：

| 组别 | description | 测试集触发准确率 |
|------|------------|----------------|
| baseline（无 skill） | — | 假设 40%（AI 靠猜） |
| v1（基线） | 06 原版 description | 假设 72% |
| best（run_loop 选出） | 优化后 description | 假设 88% |

三组对比回答三个问题：

- **baseline vs v1**：「装这个 Skill」本身有没有用？（v1 明显高于 baseline，说明 description 起作用了）
- **v1 vs best**：「优化 description」有没有用？（best 高于 v1，说明 run_loop 有效）
- **best - baseline**：「这个 Skill 整体」值不值得装？（差距太小就该考虑是不是 description 本身就没区分度）

如果 best 分数高但**测试集分数反而低于训练集**——警惕过拟合：AI 在背题，换个说法就废。这也是为什么 skill-creator 强制按测试集分数选 best_description。

## 常见错误

下面 6 条按症状命名，展开说为什么错、怎么改。

### 负例太明显，不算 near-miss

负例全是「今天天气怎么样」「写个 fibonacci」——AI 不触发它们证明不了任何事，因为它们和 Skill 八竿子打不着。改法：至少 1/3 的负例要 near-miss，共享关键词或语境但意图不同（如「push 到远程」对 `commit-style`）。`skills/skill-creator/SKILL.md` L358 原话：「负例应当 genuinely tricky」。

### 只看训练集，不留测试集，过拟合

把所有 eval 都拿来训练 description 优化，迭代 5 轮后训练集准确率 100%——但你换个说法就不触发。这是过拟合（overfitting，模型记住了题面却没学会规律）。改法：严格 60/40 切分，**按测试集分数**选最优 description（skill-creator SKILL.md L377-394 的标准做法）。

### 改了 description 不跑回归

description 改了一个字就上线，没重新跑 eval——你以为只是润色，实际上可能让某个 near-miss 开始误触发。改法：**每次改 description 都重跑 trigger eval**，把 evals 数据当回归测试用，而不是一次性测试。这也是为什么第 2 步的 trigger-evals.json 要存进 Skill 目录长期维护。

### 没有 baseline，没法说有没有变好

跑出 88% 准确率就宣布「触发质量很好」——88% 是和谁比？如果原来就 90%，你反而变差了。改法：永远带上 baseline（无 skill 或旧版 description）一起跑，三个数字一起看（见第 5 步的三组对比表）。`skills/skill-creator/SKILL.md` L169-186 要求 with-skill 和 baseline 同 turn 并行跑，就是为了这个对照。

### 把 evals.json 当一次性测试，不复用

跑完一次就把 trigger-evals.json 删了——下次改 description 又得重新想 20 条，而且没法对比历史。改法：把 evals 数据**纳入版本管理**（连同 SKILL.md 一起 commit），每次迭代追加新发现的 near-miss。久而久之，你的 eval 集就是 Skill 触发质量的事实记录。

### 边界例忽略了噪音关键词

边界例只放「极短」「极长」，忽略了「**包含噪音关键词**」这类——比如「这几个文件提交一下顺便看看能不能合 PR 顺便 push」，同时触发 `commit-style`、`git-workflow`、`git-batch-commit` 三个 Skill 的关键词。这种输入才是真实场景里最难的。改法：边界例至少覆盖三类——长度极端、上下文缺失、**多 Skill 关键词冲突**（编排场景尤其多，见 [08](./08-多Skill编排.md)）。

## 自测题 / 验收

1. **分清两种 eval**：拿到一个需求「我想测 AI 触发 `commit-style` 之后给的提交类型对不对」，你该用 trigger eval（`[{"query", "should_trigger"}]`）还是完整 eval（`evals/evals.json` 带 `expected_output`）？为什么？
2. **三套术语对齐**：把「正例 / 负例 / 边界例 / 基线」分别翻译成 skill-creator 英文说法和 `SKILL-DEV-GUIDE.md` §13 中文说法，能对上吗？
3. **写 near-miss**：给你的某个 Skill 设计 3 条 near-miss 负例——每条都要解释「它共享了什么关键词、为什么意图其实不同」。
4. **识别过拟合**：某次 run_loop 迭代后，训练集准确率从 80% 涨到 99%，测试集准确率从 78% 掉到 70%。这是变好了还是变差了？该怎么选 description？
5. **编排场景的 near-miss**：在 [08](./08-多Skill编排.md) 的 `todo-commit` 编排里，`todo` 和 `commit-style` 都可能被「帮我把待办 commit 掉」触发。给这个场景设计 2 条边界例，标注 `ambiguous` 并说明该由谁触发。

第 4 题能判断出「测试集掉分 = 过拟合 = 该回退」，说明你已经掌握 trigger eval 防假绿的核心了。

## 下一篇

**下一篇（主线）**：[04 调试与发布](./04-调试与发布.md)——触发质量过了，Skill 就要走出本地：怎么调试、怎么打 tag、怎么写安装说明、怎么回滚。

- 回看三层形态：[06 纯说明型 Skill](./06-纯说明型-Skill.md) / [07 带脚本 Skill](./07-带脚本-Skill.md) / [08 多 Skill 编排](./08-多Skill编排.md)。
- 第一次用第三方 Skill 前先审查：[05 第三方 Skill 安全审查](./05-第三方-Skill-安全审查.md)。
- 想做完整端到端协作案例：10 多 Agent 协作入门、11 贯穿案例（均暂未发布）。

---

**收尾给一个动作**：打开你手里任意一个 Skill，给它写 10 条 trigger eval（7 正 3 负，负例至少 1 条 near-miss），存进 `evals/trigger-evals.json`。下次你手痒想改 description 时，先跑一遍这 10 条——这就是触发质量评估的全部起点。