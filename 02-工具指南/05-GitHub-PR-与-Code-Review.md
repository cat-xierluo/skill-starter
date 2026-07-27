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

## 相关链接

- [提交到 GitHub 与 Commit 规范](./04-提交到-GitHub-与-Commit-规范.md)
- [GitHub 入门](./02-GitHub-入门.md)
- [什么是 GitHub](../01-概念入门/03-什么是-GitHub.md)
