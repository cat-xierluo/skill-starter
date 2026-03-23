# Git 命令速查表

本文档按场景分类，列出最常用的 Git 命令。快速上手，无需记忆所有细节。

---

## 1. 日常操作

### `git status` — 查看状态
查看当前仓库的修改状态（哪些文件被修改、暂存或未追踪）。

```bash
git status                  # 查看完整状态
git status -s              # 简洁模式（推荐）
git status --short         # 同 -s
```

**简洁模式输出示例：**
```
 M README.md        # M = 已修改（Modified）
A  new-file.js      # A = 已添加（Added）
 D old-file.txt     # D = 已删除（Deleted）
?? untracked.txt    # ?? = 未追踪（Untracked）
```

---

### `git add` — 暂存文件
将修改标记为待提交（staged）。

```bash
git add filename.txt           # 暂存单个文件
git add .                       # 暂存所有修改（包括新文件）
git add -A                      # 同上，暂存所有修改
git add -u                      # 只暂存已追踪文件的修改（不包括新文件）
git add -p                      # 交互式暂存（逐个文件/区块选择）
```

---

### `git commit` — 提交快照
将暂存的文件保存为一个快照（版本）。

```bash
git commit -m "提交说明"           # 提交并写明改动
git commit -am "提交说明"          # 自动 add 已追踪文件的修改 + 提交（不包含新文件）
git commit --amend                # 修改上一次提交（追加修改/改提交信息）
git commit --amend --no-edit      # 追加修改到上次提交（不换 commit hash）
```

---

### `git push` — 推送到远程
将本地提交上传到远程仓库。

```bash
git push                         # 推送到默认分支（之后只需这条）
git push origin main            # 推送到远程 main 分支
git push -u origin feature-x    # 首次推送并记住上游分支
git push --force                # 强制推送（⚠️ 危险，仅在确定时使用）
git push --tags                  # 推送所有标签
```

---

### `git pull` — 拉取并合并
从远程仓库拉取最新代码，并自动合并到当前分支。

```bash
git pull                        # 拉取当前分支的远程更新
git pull origin main           # 指定分支拉取
git pull --rebase              # 以 rebase 模式拉取（避免多余 merge 记录）
```

---

### `git clone` — 克隆仓库
将远程仓库完整下载到本地。

```bash
git clone git@github.com:user/repo.git           # SSH 方式克隆
git clone https://github.com/user/repo.git       # HTTPS 方式克隆
git clone git@github.com:user/repo.git my-folder # 克隆到指定文件夹
git clone --depth 1 git@github.com:user/repo.git # 浅克隆（只下载最新一次提交）
```

---

## 2. 分支操作

### `git branch` — 分支管理
查看、创建、删除分支。

```bash
git branch                        # 查看本地所有分支（* 为当前分支）
git branch -a                     # 查看所有分支（包括远程）
git branch feature-login           # 创建新分支（但不切换）
git branch -d feature-login       # 删除已合并的分支
git branch -D feature-login       # 强制删除分支（未合并也可删）
git branch -m old-name new-name   # 重命名当前分支
```

---

### `git checkout` — 切换分支
切换到指定分支，或还原文件。

```bash
git checkout main                  # 切换到 main 分支
git checkout feature-login          # 切换到已有分支
git checkout -b new-feature         # 创建并切换到新分支
git checkout -- filename.txt        # 还原文件（丢弃本地修改）
git checkout HEAD -- filename.txt   # 同上
```

---

### `git switch` — 切换分支（新版）
`checkout` 的替代命令，更直观，不易误操作。

```bash
git switch main                    # 切换到 main
git switch -c new-feature          # 创建并切换（新分支）
git switch -                       # 切换到上一个分支
```

---

### `git merge` — 合并分支
将指定分支合并到当前分支。

```bash
git checkout main                  # 先切换到目标分支
git merge feature-login            # 把 feature-login 合并进来
git merge --no-ff feature-login   # 禁止 fast-forward，保留分支历史
git merge --squash feature-login  # 压缩合并（把所有提交合并为一个）
```

---

### `git rebase` — 变基
将当前分支的提交"移动"到另一个分支的顶部。**⚠️ 不要对已推送到远程的提交执行 rebase。**

```bash
git rebase main                   # 把当前分支变基到 main 上
git rebase -i HEAD~3             # 交互式变基（合并/修改/删除最近 3 个提交）
```

**交互式变基常用命令：**
```
pick = 保留这个提交
squash = 合并到上一个提交
reword = 修改提交信息
drop = 删除提交
```

---

## 3. 查看历史

### `git log` — 查看提交历史

```bash
git log                           # 查看完整提交历史
git log --oneline                 # 每行一个提交（简洁，推荐）
git log --oneline -10             # 最近 10 条
git log --graph --oneline         # 可视化分支图
git log --author="name"           # 只看某个人的提交
git log --since="2024-01-01"      # 查看某个时间之后的提交
git log --grep="关键字"           # 按提交信息关键字搜索
git log -p filename.txt           # 查看某个文件的历史（带 diff）
```

---

### `git diff` — 查看差异

```bash
git diff                          # 查看所有未暂存的修改
git diff --staged                 # 查看已暂存的修改（add 之后）
git diff HEAD                     # 查看工作区 vs 最新提交
git diff main feature-login       # 比较两个分支的差异
git diff HEAD~5 HEAD              # 查看最近 5 个提交的差异
git diff --stat                   # 只看文件列表，不看具体改动
```

---

### `git show` — 查看某次提交

```bash
git show HEAD                     # 查看上一次提交的全部内容
git show HEAD~1                  # 查看上上次提交
git show abc1234                 # 查看指定 commit hash 的提交
git show --stat HEAD             # 只看统计信息（不改动行）
```

---

### `git blame` — 逐行追责
查看某文件每行代码的最后修改者。

```bash
git blame filename.txt            # 查看文件的逐行修改历史
git blame -L 10,20 filename.txt  # 只看第 10-20 行
```

---

### `git stash` — 暂存工作现场
临时保存当前工作目录和暂存区的修改，稍后可以恢复。

```bash
git stash                         # 暂存当前所有修改
git stash save "暂存说明"          # 暂存并添加说明
git stash list                    # 查看所有暂存
git stash pop                     # 恢复最新暂存并删除
git stash apply                   # 恢复暂存（保留记录）
git stash drop                    # 删除最新暂存
git stash clear                   # 清空所有暂存
```

---

## 4. 标签（Tag）

### `git tag` — 管理标签
标签用于标记特定的提交版本（如 v1.0.0）。

```bash
git tag                           # 查看所有标签
git tag v1.0.0                    # 给当前提交打轻量标签
git tag -a v1.0.0 -m "版本 1.0.0"  # 打附注标签（推荐，有说明）
git tag -d v1.0.0                 # 删除本地标签
git push origin v1.0.0           # 推送标签到远程
git push origin --tags            # 推送所有标签
```

---

## 5. 撤销与回退

### `git reset` — 重置 HEAD

```bash
git reset HEAD                    # 取消暂存（unstage），不改文件
git reset --soft HEAD~1           # 撤销上次提交，保留修改在暂存区
git reset --mixed HEAD~1          # 撤销上次提交 + 取消暂存（默认）
git reset --hard HEAD~1           # 撤销上次提交 + 删除修改（⚠️ 危险）
```

> **安全撤销建议**：`git reset --hard` 只用于本地未 push 的提交。已 push 的提交用 `git revert`。

---

### `git revert` — 反做提交
安全地撤销某个提交，生成一个新提交来"反做"它，不会改变历史。

```bash
git revert HEAD                   # 反做上一次提交
git revert abc1234               # 反做指定提交
```

---

### `git checkout` — 还原文件

```bash
git checkout -- filename.txt      # 丢弃工作区的修改（未 add）
git checkout HEAD -- filename.txt # 丢弃工作区和暂存区的修改（⚠️ 危险）
```

---

## 6. 远程仓库

### `git remote` — 管理远程仓库

```bash
git remote -v                     # 查看远程仓库地址
git remote add origin git@github.com:user/repo.git  # 添加远程仓库
git remote remove origin          # 删除远程仓库
git remote set-url origin git@github.com:user/repo.git # 修改远程地址
```

---

## 7. 辅助命令

### `git clean` — 清理未追踪文件

```bash
git clean -n                      # 预览要删除的文件（不实际删除）
git clean -f                      # 删除未追踪的文件
git clean -fd                     # 删除未追踪的文件和文件夹
```

### `git reflog` — 查看所有操作历史

```bash
git reflog                        # 查看所有操作记录（包括 reset、checkout）
# 用于恢复误删的分支或误 reset 的提交
git checkout abc1234              # 从 reflog 找到的 hash，可以恢复到那个状态
```

---

## 命令速查表

| 场景 | 命令 |
|------|------|
| 查看状态 | `git status` |
| 暂存文件 | `git add .` |
| 提交快照 | `git commit -m "说明"` |
| 推送到远程 | `git push` |
| 拉取更新 | `git pull` |
| 克隆仓库 | `git clone <地址>` |
| 查看分支 | `git branch` |
| 创建分支 | `git checkout -b <分支名>` |
| 切换分支 | `git checkout <分支名>` |
| 删除分支 | `git branch -d <分支名>` |
| 合并分支 | `git merge <分支名>` |
| 查看历史 | `git log --oneline` |
| 查看差异 | `git diff` |
| 查看提交 | `git show <commit>` |
| 暂存工作 | `git stash` |
| 取消暂存 | `git reset HEAD` |
| 还原文件 | `git checkout -- <文件>` |
| 标签 | `git tag <版本号>` |

---

## 常见错误处理

| 错误信息 | 解决方法 |
|----------|----------|
| `Please commit your changes or stash them` | 先 `git stash` 或 `git commit` |
| `src refspec main does not match` | 检查当前分支名：`git branch` |
| `Permission denied (publickey)` | SSH Key 未配置，参考 SETUP.md |
| `Merge conflict` | 手动解决冲突后 `git add` + `git commit` |
| `fatal: not a git repository` | 没有在 Git 仓库目录中执行，进入项目目录 |
| `Your branch is ahead of 'origin/main' by N commits` | 需要 `git push` |

