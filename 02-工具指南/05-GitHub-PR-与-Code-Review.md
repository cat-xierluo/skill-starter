# GitHub PR 与 Code Review

这篇文档解决的是：

**改动已经推到分支了，接下来怎样发起 Pull Request、怎样做 Code Review、怎样合并。**

如果你还没把改动推上去，先看 [提交到 GitHub 与 Commit 规范](./04-提交到-GitHub-与-Commit-规范.md)。

---

## 1. PR 的最小闭环

```text
本地分支
  ↓
git push -u origin <分支>
  ↓
Open PR（指向 main）
  ↓
自检 + Review
  ↓
Merge
  ↓
删分支
```

PR 的本质是"一次有上下文的合并请求"：它把一组 commit、改动 diff、讨论、检查状态打包在一起，让 reviewer 在合并前能看清"改了什么、为什么改、有没有问题"。

---

## 2. 发起一个 PR

### 第一步：建分支

分支命名遵循本仓库约定（见 `AGENTS.md`）：

```text
feature/xxx    # 新功能
bugfix/xxx     # 修复
refactor/xxx   # 重构
docs/xxx       # 纯文档
```

```bash
git checkout -b feature/add-pr-tutorial
```

### 第二步：提交并推送

```bash
git add .
git commit -m "feat: 新增 PR 教程"
git push -u origin feature/add-pr-tutorial
```

`-u` 只在第一次推送时需要，它把本地分支和远程分支关联起来，之后 `git push` 不用再写分支名。

### 第三步：打开 PR

两种方式：

**方式一：用 gh CLI（推荐）**

```bash
gh pr create --base main --title "feat: 新增 PR 教程" --body "..."
```

**方式二：网页**

推送后 GitHub 会在终端和仓库主页给出一个 `Create pull request` 链接，点进去填标题和描述即可。

---

## 3. PR 描述模板

好的 PR 描述让 reviewer 不用猜。推荐结构：

```markdown
## 背景
为什么做这个改动？关联哪个 Issue 或任务。

## 改动
- 要点 1
- 要点 2

## 验证
跑了什么检查、结果如何。例如：
- `bash scripts/check.sh` 通过
- 手动验证了 xxx 场景

## 关联
Refs #12
```

几个要点：

- **标题**用约定式 commit 前缀（`feat:` / `fix:` / `docs:`），和 commit 规范一致
- **背景**一句话讲清动机，reviewer 不熟悉上下文时尤其重要
- **验证**写明怎么确认它真的能用，别只写"已测试"
- **关联 Issue** 用 `Refs #N` 引用；只有真正要在合并时关闭 Issue 才写 `Closes #N`

---

## 4. Code Review 检查清单

无论你是 reviewer 还是 author，心里有这张清单会更高效。

### 功能正确性

- 改动是否真的解决了标题声称的问题
- 边界情况是否考虑（空输入、异常、并发）
- 有没有"看起来对、实际跑不通"的逻辑

### 可读性与结构

- 命名是否清楚（变量、函数、文件）
- 是否重复造轮子——已有工具能否复用
- 单个 commit / PR 是否聚焦在一件事上

### 安全与副作用

- 有没有硬编码的密钥、Token、绝对路径
- 是否引入了不必要的依赖或大文件
- 删除 / 覆盖操作是否会误伤现有数据

### 一致性

- 是否符合本仓库的目录命名、commit 规范、文档约定
- 文档是否同步更新（`CHANGELOG.md`、`docs/`）
- 改动涉及文档时，相对链接是否还能打开

---

## 5. 怎么回应 Review 意见

reviewer 留下评论后，author 有三种典型回应：

| 情景 | 做法 |
|------|------|
| 同意，要改 | 改完在同一行回复 `已修复` 或 `done`，再 push 新 commit |
| 不同意 | 解释理由，给依据（链接、代码、测试输出），不要只说"不用改" |
| 需要讨论 | 标记为讨论中，把分歧讲清楚，必要时拉到语音 / Issue |

几个习惯：

- **不要 force push 打乱讨论**：review 进行中尽量避免 `git push --force`，否则评审意见会错位
- **小步追加 commit**：按评审意见改时，每次 push 一个聚焦的 commit，而不是反复 amend
- **resolve 后再说一句**：标记 resolved 前最好留一句结论，方便日后追溯

---

## 6. 合并策略

GitHub 提供三种合并方式，取舍如下：

| 策略 | 特点 | 适合 |
|------|------|------|
| Merge commit | 保留所有 commit，多一个合并节点 | 分支上有多个有意义的 commit |
| Squash | 把分支上所有 commit 压成一个 | 一堆零碎 commit，想合并成一条干净记录 |
| Rebase | 把分支 commit 逐个放到 main 顶部，无合并节点 | 想要线性历史、commit 干净 |

本仓库建议：

- 常规功能：**Squash and merge**，把开发过程的零碎 commit 收敛成一条
- 涉及多个独立改动的 PR：**Merge commit**，保留每条 commit 的语义
- 合并后删除源分支，保持分支列表干净

---

## 7. 合并之后

```bash
git checkout main
git pull
git branch -d feature/add-pr-tutorial        # 删本地分支
git push origin --delete feature/add-pr-tutorial  # 删远程分支（若未自动删）
```

最后别忘了：

- 对应的 Issue 是否需要关闭或推进
- `docs/TASKS.md` 里相关任务是否要勾掉
- 用户可见的改动是否已记入 `CHANGELOG.md`

---

## 8. 常见坑

- **PR 指错 base**：发起时确认 base 是 `main`，不要指向自己的特性分支
- **PR 太大**：一个 PR 改了 30 个文件跨多个主题，review 成本极高。拆成多个聚焦的小 PR
- **忘了拉最新 main**：分支落后太多容易冲突，定期 `git fetch origin && git rebase origin/main`
- **CI / 自检红了还强行合并**：先让检查变绿，本仓库对应 `bash scripts/check.sh`
- **沉默合并**：没有描述、没有验证记录的 PR，日后出了问题无人能追溯

---

## 9. 动手练习：用 todo.py 走一遍 PR 全流程

前面八节讲了 PR 的规则，但规则要落到一次真实的改动上才记得住。这个练习用贯穿全系列的 `todo.py`（Python 3 标准库、存 `todos.json`、`add/list/done` 三命令，见 [带脚本 Skill](../04-创建Skill/07-带脚本-Skill.md)）做素材，让你完整走一遍：从建分支到合并删分支，分别扮演 **author（作者）** 和 **reviewer（审查者）** 两个角色。

练习要求一台装好 Git 和 GitHub CLI（`gh`）的机器（安装见 [Git 入门](./01-Git-入门.md) 的前置部分），以及一个能 push 的 GitHub 仓库。如果你只想过流程、不真的开 PR，本地照抄命令即可，最后跳到验收自查。

> 平台说明：下面的 `bash` 代码块在 macOS（默认 `zsh`）、Linux（默认 `bash`）、Windows 的 **Git Bash** 里都能直接敲。Windows 若用 **PowerShell**，主要差别是提示符（`>` 而非 `$` / `%`）、路径分隔符（PowerShell 接受 `/`，老工具只认 `\`）和退出码（数字退出码看 `$LASTEXITCODE`），详见 [终端与命令行入门](./06-终端与命令行入门.md)。本文用 `python3`；若你的系统只有 `python`，把它替换成 `python` 即可（macOS/Linux 习惯 `python3`，Windows 常是 `python`）。

### 9.1 作者视角：建分支 → 改代码 → 提交 → 开 PR → 自我 Review

我们要给 `todo.py` 加一个小功能：`list --pending` 只列出**未完成**的待办。改动小而完整，正好适合练 PR。

**第一步：建 feature 分支**

先确认在 `main` 上、且与远程同步，再切分支（命名遵循 §2 的 `feature/xxx` 约定）：

```bash
git checkout main
git pull
git checkout -b feature/list-pending
```

**第二步：改代码（加 `list --pending`）**

打开 `scripts/todo.py`（即 [07 带脚本 Skill](../04-创建Skill/07-带脚本-Skill.md) 里那段）。原 `list` 分支长这样：

```python
    if cmd == "list":
        for t in todos:
            mark = "x" if t["done"] else " "
            print(f"[{mark}] {t['id']}: {t['text']}")
        return 0
```

把它换成下面这段——加一个 `--pending` 开关，命中就只输出未完成项：

```python
    if cmd == "list":
        only_pending = rest and rest[0] == "--pending"
        shown = [t for t in todos if not only_pending or not t["done"]]
        for t in shown:
            mark = "x" if t["done"] else " "
            print(f"[{mark}] {t['id']}: {t['text']}")
        return 0
```

顺手把开头的 usage 字符串也更新，免得文档与实现脱节：

```python
        print("usage: todo.py [add <text> | list [--pending] | done <id>]", file=sys.stderr)
```

改完先本地验证一遍（`done` 标记后 `--pending` 应把它过滤掉）：

```bash
python3 scripts/todo.py add 读书
python3 scripts/todo.py add 写代码
python3 scripts/todo.py done 1
python3 scripts/todo.py list            # 看到 1、2 两条
python3 scripts/todo.py list --pending  # 只看到「写代码」这一条
```

**第三步：按规范提交并推送**

提交信息遵循约定式 commit（详见 [提交到 GitHub 与 Commit 规范](./04-提交到-GitHub-与-Commit-规范.md)）。`feat:` 前缀对上新功能，正文一句话说清改了什么：

```bash
git add scripts/todo.py
git commit -m "feat: todo list 新增 --pending 只列未完成项"
git push -u origin feature/list-pending
```

**第四步：开 PR（用 §3 的描述模板）**

用 `gh` 开 PR，正文直接套 §3 模板——背景、改动、验证、关联一项不缺：

```bash
gh pr create --base main \
  --title "feat: todo list 新增 --pending 只列未完成项" \
  --body "$(cat <<'EOF'
## 背景
查待办时经常只想看「还没做完的」，现在 `list` 一股脑全列出来，得自己用眼睛挑。加个 `--pending` 过滤更顺手。

## 改动
- `scripts/todo.py` 的 `list` 命令支持 `--pending`，只输出 `done=false` 的项
- 同步更新 usage 字符串

## 验证
- `python3 scripts/todo.py add 读书` / `add 写代码` / `done 1` / `list --pending` 只输出「写代码」，符合预期
- 不带 `--pending` 时行为与原来一致

## 关联
Refs #todo-cli
EOF
)"
```

**第五步：开 PR 后先自我 Review**

请人审之前，先用 §4 的检查清单**自己过一遍**（这是省别人时间、也省自己返工的关键一步）：

- **功能正确性**：`--pending` 在有待办时过滤对了；但 `todos.json` 还不存在（数据库为空）时会怎样？自己跑一次——目前它会什么也不打印、退出码 0，对脚本来说算「诚实的空结果」，但要不要给一行提示（如 `（暂无待办）`）值得想一下。
- **可读性**：`only_pending = rest and rest[0] == "--pending"` 一行讲清意图，没有重复造轮子。
- **一致性**：usage 字符串已同步更新；commit 用了 `feat:` 前缀。

自检没大问题就请人审；如果自己已经想改（比如加空结果提示），先改完再邀请 reviewer，别让对方审一个你自己都不满意的版本。

### 9.2 审查者视角：收到 PR → 按清单审 → 提意见 → 复审 → 合并

现在换你当 reviewer。收到上面这个 PR，按下面五步走。

**第一步：先看描述和改动范围**

打开 PR，读一遍描述，确认动机清楚；扫一眼「Files changed」看改了几个文件。这个 PR 只动 `scripts/todo.py` 一个文件、改了几行——范围小、聚焦，是个健康的小 PR（要是它顺手又改了 `SKILL.md` 和别的脚本，就要提醒 author 拆 PR，对应 §8 的「PR 太大」）。

**第二步：按 §4 检查清单逐项过**

在 diff 上逐行读，心里对照 §4 四个维度：

- **功能正确性**：过滤逻辑 `not only_pending or not t["done"]` 看着对；但边界情况要想——`todos.json` 为空时会怎样？
- **可读性**：命名清楚，复用了已有的 `todos` 列表。
- **安全与副作用**：只读不改数据，无密钥无新依赖。
- **一致性**：usage 已更新，commit 前缀规范。

**第三步：提具体意见**

别只写「有问题」，要写清「在什么情况下、我预期什么、实际什么」。给两条模拟意见：

- 意见 1（边界情况，对应 §4 功能正确性）：
  > `todos.json` 还不存在时（首次运行），`list --pending` 什么都不打印就返回了。脚本场景下退出码 0 算诚实，但用户体验上空跑没反馈容易以为是 bug。建议空列表时打印一行 `（暂无待办）`，或者至少在 PR 描述里说明「空结果即合法输出」。

- 意见 2（一致性，对应 §4 一致性）：
  > [带脚本 Skill](../04-创建Skill/07-带脚本-Skill.md) 里 `SKILL.md` 描述的 `list` 行为是「列出全部」，现在多了 `--pending`。如果这个 Skill 已经发布给别人用了，`SKILL.md` 的命令说明要同步补上 `--pending`，否则文档与实现脱节。

意见要落到具体行号或文件，让 author 能直接照着改。

**第四步：作者改后复审**

author 同意意见 1，追加一个聚焦的 commit（遵循 §5「小步追加 commit」，不要 force push 把讨论打乱）：

```python
    if cmd == "list":
        only_pending = rest and rest[0] == "--pending"
        shown = [t for t in todos if not only_pending or not t["done"]]
        if not shown:
            print("（暂无待办）")
            return 0
        for t in shown:
            mark = "x" if t["done"] else " "
            print(f"[{mark}] {t['id']}: {t['text']}")
        return 0
```

push 后你在 PR 里能看到新 commit。复审只需看这次改动：空列表现在打印 `（暂无待办）`，正常列表不受影响——意见解决了，标记 resolved，回复一句「已确认，空列表有提示，其他行为不变」留个结论（§5 的「resolve 后再说一句」）。意见 2 如果 author 给出理由（如 Skill 还没发布），也可接受、留结论关闭。

**第五步：选合并策略，合并后删分支**

意见全部 resolved、自检（如有）变绿，就可以合并。这是一个聚焦的小功能 PR，按 §6 选 **Squash and merge**，把开发过程的几个 commit 收敛成一条。点合并后，按 §7 清理分支：

```bash
git checkout main
git pull
git branch -d feature/list-pending
git push origin --delete feature/list-pending   # 若 GitHub 未自动删远程分支
```

最后按 §7 核对收尾项：相关任务是否在 `docs/TASKS.md` 勾掉、用户可见的改动是否记进 `CHANGELOG.md`（这里 `--pending` 是用户可见的新行为，应补一条）。

### 9.3 练习验收

做完这个练习，你应该能：

1. **独立走完一次 PR 闭环**：从 `git checkout -b` 到 merge 后删分支，每一步知道为什么这么做，不照着教程也能复现。
2. **写出能让人不猜的 PR 描述**：背景 / 改动 / 验证 / 关联四段齐全，验证部分给的是真跑过的命令和结果，而不是「已测试」。
3. **开着 PR 先自检再请人审**：能用 §4 的清单自己找出至少一处边界情况（如 `list --pending` 在空数据库下的行为），不把烂摊子丢给 reviewer。
4. **提具体、可操作的 review 意见**：每条意见带「在什么情况下、预期什么、实际什么」和明确行号，author 能直接照着改。
5. **按 PR 性质选合并策略并收尾**：知道这个 `--pending` PR 该选 Squash，合并后会删分支、补 `CHANGELOG.md`，不留下僵尸分支和遗漏记录。

---

## 相关链接

- [提交到 GitHub 与 Commit 规范](./04-提交到-GitHub-与-Commit-规范.md)
- [GitHub 入门](./02-GitHub-入门.md)
- [什么是 GitHub](../01-概念入门/03-什么是-GitHub.md)
