# Git 入门

这篇文档只解决一件事：

**让你第一次真正把 Git 用起来。**

如果你只记住一句话：

> Git 是记录文件变化历史的工具。

## 本篇目标

读完这篇，你能：

- 在自己电脑上装好 Git，并完成一次「姓名 + 邮箱」的基础配置
- 说清 Git 的 3 个核心区域（工作区 / 暂存区 / 仓库历史）各自装什么
- 用 `git status → git add → git commit → git log` 走完一次完整提交
- 在分支上改东西再合并回 `main`，并手动解决一次简单的合并冲突
- 在 `restore / revert / reset` 之间选对「往回退」的安全命令

## 前置知识

会用终端敲命令（`mkdir`、`cd`、`echo`、`ls` 这几个）。还没摸过命令行的话，照抄示例也能跑，但建议先看 [终端与命令行入门](./06-终端与命令行入门.md)，至少知道「在哪个文件夹里敲」这件事。

本篇示例统一用贯穿小项目 `todo.py`（本地命令行待办脚本，存 `todos.json`，有 `add/list/done` 三个命令）当练习素材，命令示例会标注 macOS / Windows / Linux 的差异。

## 什么时候你会需要 Git

- 想保存每次改动
- 想回到某个旧版本
- 想和别人同时改一个项目
- 想让 AI 改完代码以后还能回退

## 安装 Git

### macOS

```bash
brew install git
```

### Windows

去 [git-scm.com](https://git-scm.com/download/win) 下载安装。

### Linux

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install git
```

安装完成后检查：

```bash
git --version
```

## 第一次必须做的配置

```bash
git config --global user.name "你的名字"
git config --global user.email "your.email@example.com"
```

检查是否生效：

```bash
git config --global --list
```

这两项会写进提交记录里。

## Git 的 3 个核心区域

这是新手最应该先理解的东西。

### 工作区

你正在编辑文件的地方。

### 暂存区

你准备提交的改动会先进入这里。

### 仓库历史

真正提交成功后，改动会进入 Git 历史。

## 最常用的工作流

```text
改文件
  ↓
git status
  ↓
git add
  ↓
git commit
  ↓
git push
```

## 你第一次可以完整跑一遍的例子

下面用贯穿小项目 `todo.py`（待办脚本，存 `todos.json`）当素材，第一次跑只需建一个仓库、放一个文件、提交一次。一共 7 步。

### 第一步：创建测试目录

```bash
mkdir git-demo
cd git-demo
```

### 第二步：初始化 Git 仓库

```bash
git init
```

这会在当前目录生成 `.git/`，表示 Git 开始管理这个文件夹。

### 第三步：创建一个文件

先用一个简单的 `README.md` 代替 `todo.py`（脚本本身后面再写），把仓库跑起来：

```bash
echo "# Git Demo" > README.md
```

### 第四步：查看状态

```bash
git status
```

你会看到 `README.md` 还没有被提交。

### 第五步：暂存文件

```bash
git add README.md
```

### 第六步：提交

```bash
git commit -m "feat: 初始化 Git Demo"
```

### 第七步：查看历史

```bash
git log --oneline
```

到这里，你已经完成第一次 Git 提交了。

## 5 个最高频命令

### `git status`

最常用。

它会告诉你：

- 哪些文件改了
- 哪些文件已暂存
- 当前所在分支

### `git add`

把改动放进暂存区。

```bash
git add 文件名
git add .
git add -A
```

### `git commit`

提交暂存区里的改动。

```bash
git commit -m "docs: 更新 Git 教程"
```

### `git log`

看提交历史。

```bash
git log --oneline
```

### `git diff`

看改动内容。

```bash
git diff
git diff --staged
```

## commit message 怎么写

推荐写法：

```text
feat: 新增天气播报脚本
fix: 修复路径错误
docs: 更新 GitHub 入门文档
refactor: 重构输出逻辑
```

重点是：

- 让别人一眼看懂
- 让未来的你一眼看懂

## 分支是什么，为什么要用

分支可以理解成“平行开发线”。

比如你在 `main` 上的代码是稳定的，但你想尝试一个新功能，就可以开一个分支。

### 创建和切换分支

```bash
git switch -c feature/add-readme-section
```

### 查看分支

```bash
git branch
```

### 切回主分支

```bash
git switch main
```

## `.gitignore` 是什么

它用来告诉 Git：

**哪些文件不要纳入版本管理。**

典型例子：

- `.env`
- `node_modules/`
- `dist/`
- `output/`
- `__pycache__/`

示例：

```gitignore
.env
node_modules/
dist/
output/
```

## 几个安全的“撤销”命令

新手不要一上来就学破坏性命令，先记这几个更安全的。

### 撤销工作区改动

```bash
git restore 文件名
```

### 撤销暂存

```bash
git restore --staged 文件名
```

### 看看当前 HEAD

```bash
git rev-parse --short HEAD
```

## 分支与合并

前面讲了「分支是什么」的概念，这一节把它跑起来。继续用 `git-demo` 那个项目，先准备一个能合并的场景。

### 第一步：开一条分支改东西

```bash
git switch -c feature/add-todo
echo "- 买咖啡" >> README.md
git add README.md
git commit -m "feat: 加一条待办"
```

### 第二步：切回主分支再合并

```bash
git switch main
git merge feature/add-todo
```

> Windows（Git Bash）下命令完全一致；如果你在 PowerShell 里，`echo` 默认会按 UTF-16 写入，建议用 `Add-Content README.md "- 买咖啡"` 或直接用编辑器改文件。

### Fast-forward 合并 vs 三方合并

合并的时候 Git 会用两种策略之一：

- **Fast-forward 合并**（快进合并）：主分支自你开分支以来没有新提交，Git 只需要把 `main` 指针往前挪到分支的最新提交，不产生额外的合并提交。历史是一条直线。
- **三方合并**（three-way merge）：主分支和你开的分支都各自有新提交，Git 会找一个公共祖先节点，把两边的改动合并起来，并生成一个新的「合并提交」（merge commit）。

```text
Fast-forward:        三方合并:
main → A → B          main    → A → C → M (合并提交)
              \              \      /
fea →  C          fea      → B
```

绝大多数个人项目里你遇到的是 Fast-forward；多人协作或长时间分支，容易出现三方合并，也就容易出现下一节说的冲突。

### 合并完要不要删分支

```bash
git branch -d feature/add-todo   # 已合并才允许删，安全
git branch -D feature/add-todo   # 强制删，即便没合并
```

推荐用 `-d`（小写），它会拦住你删掉还没合并的分支。

## 冲突解决

### 什么时候会冲突

当两条分支改了**同一个文件的同一块区域**，Git 没法替你决定保留哪一边，就会报 `CONFLICT`，把合并或 rebase 暂停下来等你处理。

注意是「同一块区域」。如果你改第 10 行、同事改第 100 行，Git 通常能自己合并，不会冲突。

### 冲突标记长什么样

冲突时，Git 会把冲突文件改成这样：

```text
<<<<<<< HEAD
- 买咖啡
=======
- 买牛奶
>>>>>>> feature/add-todo
```

三组标记的含义：

- `<<<<<<< HEAD`：当前分支（你所在的那条，比如 `main`）的内容开始
- `=======`：分隔线，上面是「当前分支」，下面是「要合并进来的分支」
- `>>>>>>> feature/add-todo`：要合并进来的分支的内容结束

### 手动解决冲突的 5 步

下面用一个具体冲突走一遍。假设你在 `main` 上把那一行改成了「买咖啡」，分支上改成了「买牛奶」。

1. **看状态，确认哪些文件冲突**

   ```bash
   git status
   ```

   会列出 `Unmerged paths`（未合并的文件）。

2. **打开冲突文件，保留想要的内容**

   用编辑器打开 `README.md`，把三组冲突标记和不要的那一边删掉。比如你想两样都买，改成：

   ```text
   - 买咖啡
   - 买牛奶
   ```

   关键：**最后留下的文件里不能再有任何 `<<<<<<<`、`=======`、`>>>>>>>` 标记**。

3. **暂存解决后的文件**

   ```bash
   git add README.md
   ```

   `git add` 在这里的作用是告诉 Git「我改完了，冲突已解决」。

4. **完成合并**

   ```bash
   # 如果是 merge：
   git commit
   # 如果是 rebase，改用：
   git rebase --continue
   ```

   merge 时 Git 会自动弹出合并提交信息，保存退出即可。

5. **想放弃，回到冲突前的状态**

   ```bash
   git merge --abort    # 撤销本次 merge
   git rebase --abort   # 撤销本次 rebase
   ```

   这两条能让你干净地退回合冲突前的那一刻，是最常用的「兜底」。

冲突解决多了会有手感，新手第一次遇到别慌，走完上面 5 步就行。

## 撤销操作：restore / revert / reset 怎么选

这三个命令都能「往回退」，但作用范围和影响差别很大。先用一张表对比：

| 命令 | 作用范围 | 是否改写历史 | 安全等级 | 典型场景 |
| --- | --- | --- | --- | --- |
| `git restore <文件>` | 只动工作区或暂存区，不碰仓库历史 | 否 | 高 | 改乱了文件想还原；`git add` 加错想撤回暂存 |
| `git revert <提交>` | 新增一个「反向提交」来抵消某次提交 | 否（追加历史） | 高 | 已经 push 的提交想撤销，又不能影响别人 |
| `git reset <提交>` | 把当前分支指针挪到指定提交 | 是（默认丢弃之后的提交） | 低～中 | 本地还没 push 的提交想整体丢掉 |

三句话记法：

- **没提交的改动**想丢 → `restore`
- **已经 push / 共享的提交**想撤销 → `revert`
- **纯本地、还没 push 的提交**想整体回退 → `reset`

### restore 详解

```bash
git restore README.md             # 丢弃工作区改动，恢复成暂存区或 HEAD 的样子
git restore --staged README.md    # 把文件从暂存区拿回来，改动保留在工作区
git restore --source=HEAD~1 README.md  # 恢复成上一个提交的样子
```

它只动你的工作区/暂存区，不会改任何提交记录，所以最安全。

### revert 详解

```bash
git revert HEAD            # 撤销最近一次提交，会新建一个反向提交
git revert <commit-hash>   # 撤销指定提交
```

revert 不删历史，它是「再提交一次把上一次的改动抵消掉」，所以历史里会看到「提交 A → 反向提交」。**已经推送到远程、可能有别人在用的分支，应该用 revert 而不是 reset**。

### reset 详解

```bash
git reset --soft HEAD~1    # 指针回退，改动留在暂存区
git reset --mixed HEAD~1   # 指针回退，改动留在工作区（默认）
git reset --hard HEAD~1    # 指针回退，工作区和暂存区的改动全部丢弃（危险）
```

`--hard` 会**永久丢弃**未提交的改动，执行前一定想清楚。reset 会改写历史，所以只能用在还没 push 的本地提交上；一旦 push 过，再 reset 会导致远程和你本地历史分叉，需要强制推送（见下一节的风险）。

## 误提交恢复与安全边界

新手最容易踩的坑是：`reset --hard` 一下，发现刚才那次提交还没 push，是不是永远丢了？

**没有。Git 还留着。**

### 用 reflog 找回丢失的提交

`git reflog`（reference log，引用日志）记录的是 HEAD 和分支指针的每一次移动，包括你刚才那次 reset。哪怕 `git log` 已经看不到了，reflog 里通常还在。

```bash
git reflog
# 输出类似:
# a1b2c3d HEAD@{0}: reset: moving to HEAD~1
# e4f5g6h HEAD@{1}: commit: feat: 加一条待办   ← 这就是被 reset 掉的那次
```

找到那条提交的 hash（比如 `e4f5g6h`），把它救回来：

```bash
git reset --hard e4f5g6h
```

reflog 默认保留 90 天左右，是 Git 给你的一道安全网。但有几条边界要记住：

- reflog 是**本地的**，不在远程仓库上；别人电脑上没有你的 reflog。
- reflog 只记录**已提交**的内容；只在工作区改过、没 `git add`/`git commit` 的改动，被 `restore` 或 `reset --hard` 丢掉后是找不回来的。
- reflog 不覆盖「强制推送覆盖远程」造成的协作事故。

### 强制推送（force push）的风险

「强制推送」（force push）是指用本地的历史直接覆盖远程历史，常见命令 `git push --force` 或 `git push -f`。

它最大的风险是：**会覆盖远程上别人已经拉取、已经基于它工作的提交**，让同事本地突然「多出」或「丢掉」提交，引发难以恢复的混乱。

安全做法：

```bash
git push --force-with-lease       # 只在远程没人动过时才强制推送，更安全
```

`--force-with-lease` 会在远程分支被别人更新过时拒绝推送，是强制推送的推荐写法。即便如此，**`main` 这类共享分支永远不要强制推送**；个人 feature 分支要 force 前最好先通知协作者。

### 「破坏性操作先备份」原则

涉及会改写历史或丢弃改动的命令（`reset --hard`、`git checkout .`、`git push -f`、`git clean -fd`），养成两个习惯：

1. **操作前打一个标签或开一条备份分支**

   ```bash
   git branch backup-before-reset   # 当前状态整条存下来
   git tag v-before-cleanup
   ```

   哪怕操作搞砸了，`git switch backup-before-reset` 就能原样回来。

2. **拿不准时，先 `git status` + `git log` 看清楚再下手**

   多数「误操作」其实是没看清当前在哪个分支、哪些改动还没提交。

记住一句话：**Git 的历史一旦提交、且推送到远程共享，就尽量当成「不可改」来对待；只在本地、未推送的部分用 reset 这类工具。**

## 常见错误

### 不在 Git 仓库目录里：`fatal: not a git repository`

原因：你不在 Git 仓库目录里。

解决：

```bash
pwd
ls -la
```

确认当前目录是否有 `.git/`。

### 提交时显示 `nothing to commit`

原因：

- 没有改动
- 改了但没 `git add`

先执行：

```bash
git status
```

### 提交作者信息不对

`git config` 设的姓名 / 邮箱会写进每条提交记录，错了要重新设置：

```bash
git config --global user.name "你的名字"
git config --global user.email "your.email@example.com"
```

### 把不该提交的文件加进去了

先把该忽略的写进 `.gitignore`，再处理已经被 Git 跟踪的文件状态。

## 新手推荐实践

1. 小步提交，不要攒很大一坨改动
2. 提交前先 `git status`
3. 提交前先 `git diff --staged`
4. 别直接在 `main` 上乱改
5. 配合 GitHub 使用时，优先走分支 + PR

## 自测题

照着做一遍，能答上来就算过关。素材继续用 `todo.py`（没写脚本也没关系，先用一个 `todos.json` 文件代替）。

1. **跑通一次提交**：新建 `todo-demo` 目录，`git init` 后放进一个 `todos.json`（内容随意），用 `git status → git add → git commit` 提交一次，再用 `git log --oneline` 看到这条提交。
2. **看懂三个区域**：改一下 `todos.json` 但先不 `add`。此时分别执行 `git status`、`git diff`、`git diff --staged`，说出三者各自看的是哪个区域（工作区 / 暂存区 / 仓库历史）。
3. **走一次分支 + 合并**：开一条分支 `feature/add-done-cmd`，在 `todos.json` 里加一行内容并提交；切回 `main`，把它 `git merge` 进来。用 `git log --oneline --graph` 看历史长什么样。
4. **故意制造一次冲突并解决**：在 `main` 和分支上改 `todos.json` 的同一行，合并时触发 `CONFLICT`；手动删掉三组冲突标记，`git add` 后完成合并。
5. **练一次安全回退**：提交一条「误操作」的 commit（还没 push），分别用 `git reset --soft HEAD~1` 和 `git reset --mixed HEAD~1` 各试一次，用 `git status` 说出两种模式下改动分别落在哪个区域。

> 验收：第 1、3 题完成后 `git log` 能看到对应提交；第 4 题最终文件里没有任何 `<<<<<<<` 标记、`git status` 显示 clean。

## 下一篇

Git 在本地跑通后，自然的一步是把项目放到 GitHub 上——既当备份，也打开协作入口。

继续看 [GitHub 入门](./02-GitHub-入门.md)，它会带你从「只有账号」走到「创建仓库、连接本地、推送代码」。

> 连 GitHub 需要先配认证。日常长期开发推荐 SSH，那条线放在 [SSH 配置](./03-SSH-配置.md)，看完 GitHub 入门再补；其它工具篇随时可从 [README](../README.md) 回查。

## 一句话总结

Git 的核心不是“会背命令”，而是：

**学会安全地记录、比较、回退和协作。**
