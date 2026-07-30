# GitHub 入门

这篇文档面向第一次真正使用 GitHub 的人。

目标只有一个：

**让你从“只有账号”走到“能创建仓库、连接本地、提交代码”。**

## 本篇目标

读完这篇，你能：

- 注册 GitHub 账号并完成邮箱验证、基础资料设置
- 在 GitHub 上创建一个仓库，并用 SSH 或 HTTPS + Token 把它和本地连起来
- 说清 fine-grained personal access token（细粒度个人访问令牌）比 classic token 好在哪、什么场景该用哪种
- 把本地改动 `push` 到 GitHub，并看懂 Code / Issues / Pull requests / Settings 四个核心页面
- 用 Issue 跟踪任务，用 `Closes #编号` 让 commit 合并后自动关 Issue

## 前置知识

先看 [Git 入门](./01-Git-入门.md)：本篇会用到的 `git init`、`git add`、`git commit`、`git push`、`git remote` 都在那篇讲过，这里默认你已经能在本地完成一次提交。

命令行示例标注了平台差异（macOS / Windows Git Bash / Linux）；其中连接 GitHub 需要认证，本篇会分别讲 SSH 和 HTTPS + Token 两条路，SSH 的详细配置在 [SSH 配置](./03-SSH-配置.md)。

## 第一步：注册并完成基础设置

1. 打开 [GitHub](https://github.com)
2. 注册账号
3. 验证邮箱
4. 补头像和基本资料

邮箱验证这一步很重要。很多 GitHub 功能在未验证邮箱时会受限。

## 第二步：创建你的第一个仓库

登录后：

1. 点击右上角 `+`
2. 选择 `New repository`
3. 填写仓库名
4. 选择 `Public` 或 `Private`
5. 点击 `Create repository`

### 仓库名建议

- 简洁
- 小写
- 用连字符分词

例如：

- `skill-starter`
- `weekly-weather-briefing`
- `legal-text-format`

## 第三步：选认证方式

你把本地 Git 和 GitHub 连起来，通常有 2 种方式。

### 方式 A：SSH

适合：

- 你自己的长期开发电脑
- 日常频繁 `push/pull`

优点：

- 配一次后比较顺手
- 不需要每次输入 Token

建议阅读：

- [SSH 配置](./03-SSH-配置.md)

### 方式 B：HTTPS + Token

适合：

- 临时环境
- 某些公司网络或机器限制 SSH
- 你明确要走 HTTPS

## GitHub 现在更推荐什么 Token

根据 GitHub 官方文档，日常需要 Token 时，优先使用 **fine-grained personal access token**，而不是旧的 classic token。

原因是：

- 权限更细
- 可限制到指定仓库
- 风险更小

如果你只是日常本地开发，通常更推荐：

1. Git 操作走 SSH
2. API、CLI 或特定 HTTPS 场景再用 fine-grained PAT

## 如果你选择 HTTPS + Token

### 创建 fine-grained PAT

当前 GitHub 页面路径大致是：

1. 右上角头像
2. `Settings`
3. 左侧 `Developer settings`
4. `Personal access tokens`
5. `Fine-grained tokens`
6. `Generate new token`

创建时重点看这几项：

- Token name
- Expiration
- Repository access
- Permissions

### 新手最容易踩的坑

- 选了错误仓库，结果没权限
- 权限开太少，`push` 或 API 调用失败
- Token 没保存，刷新页面后找不到
- 公司组织开启 SSO，需要额外授权

### 如何使用

当你用 HTTPS 方式克隆或推送时，GitHub 不再接受密码，应该使用 Token。

例如：

```bash
git clone https://github.com/用户名/仓库名.git
```

提示输入密码时，填你的 Token。

## 第四步：把仓库和本地连起来

### 情况 1：先在 GitHub 建仓库，再克隆到本地

```bash
git clone git@github.com:用户名/仓库名.git
cd 仓库名
```

如果你走 HTTPS：

```bash
git clone https://github.com/用户名/仓库名.git
cd 仓库名
```

### 情况 2：本地已有项目，再推到 GitHub

```bash
git init
git add .
git commit -m "feat: initial commit"
git branch -M main
git remote add origin git@github.com:用户名/仓库名.git
git push -u origin main
```

如果你走 HTTPS，把 remote URL 换成 HTTPS 地址即可。

如果你想把“本地提交怎么写得更规范、怎么推到 GitHub 更稳”单独补强，继续看：

- [提交到 GitHub 与 Commit 规范](./04-提交到-GitHub-与-Commit-规范.md)

## 第五步：学会最小协作流程

### 单人项目

最小闭环：

1. 本地修改
2. `git add`
3. `git commit`
4. `git push`

### 多人协作

推荐闭环：

1. 拉最新主分支
2. 新建分支
3. 在分支开发
4. 推到 GitHub
5. 开 PR
6. Review
7. 合并

## Pull Request 到底怎么用

当你把分支推到 GitHub 后，页面通常会提示：

`Compare & pull request`

你点进去后，通常需要补 3 类信息：

- 这次改了什么
- 为什么要改
- 有什么需要别人注意

### 一个够用的 PR 描述模板

```text
## 改动
- 新增天气播报脚本
- 更新模板文档

## 原因
- 让 starter 仓库有完整示例

## 验证
- 本地运行脚本通过
- 链接检查通过
```

## GitHub 新手必会页面

### Code

看代码和文件。

### Issues

记问题、任务、需求。

### Pull requests

提合并请求和看 review。

### Settings

配置仓库权限、分支规则、Secrets 等。

## 常见问题

### 1. `remote: Permission to xxx denied`

通常是：

- 你没有仓库权限
- Token 权限不够
- SSH key 没配置好
- 推错账号了

### 2. `Repository not found`

检查：

- 仓库名是否拼错
- 账号是否拼错
- 仓库是不是私有
- 当前账号有没有权限

### 3. `Support for password authentication was removed`

意思是：

**不能再用账号密码推 GitHub 了。**

要么改用 SSH，要么用 Token。

### 4. 为什么我明明 push 了，看不到改动

检查：

- 你推的是不是正确分支
- 当前 GitHub 页面看的是否也是同一分支
- 本地 commit 是否真的成功

## 新手推荐实践

1. 日常开发优先用 SSH
2. 需要 Token 时优先 fine-grained PAT
3. 不要把 Token 提交进仓库
4. 不要直接在主分支乱改
5. 每次 push 前先看 `git status`

## 自测题

用贯穿小项目 `todo.py`（待办脚本，存 `todos.json`，`add/list/done` 三命令）当素材。仓库可以先建成 `Private`，避免练习内容外泄。

1. **建仓 + 连本地**：在 GitHub 建一个 `todo-demo` 仓库；本地新建目录、`git init`、放一个 `todo.py`（暂时 `print("todo")` 也行），用 SSH（或 HTTPS + Token）把 `remote` 连好，`git push -u origin main` 成功，GitHub 页面能看到文件。
2. **配好认证**：在本地 `git remote -v` 看清走的是 SSH 还是 HTTPS；若走 HTTPS，建一个 fine-grained PAT（只给 `todo-demo` 这一个仓库的 `Contents` 读写权限），用它完成一次 `push`。
3. **开 Issue 并关联 commit**：用 `gh issue create` 开一个 Issue，标题「list 命令在空列表时报错」；本地建分支改一行 `todo.py`，commit message 里写 `Closes #<编号>`，push 后记下编号，等合并到 `main` 时验证它被自动关闭（本篇还讲不到 PR 合并，做到「commit 带上 Closes」即可，合并留给下一篇）。
4. **分清四个页面**：在仓库页依次打开 Code / Issues / Pull requests / Settings，各说一句话它们管什么；找到 `Settings` → `Developer settings` → `Personal access tokens` → `Fine-grained tokens` 的路径。

> 验收：第 1 题 GitHub 页面出现 `todo.py`；第 2 题能说出自己用的是哪种认证、PAT 限定了哪些仓库；第 3 题 `git log` 里能看到带 `Closes #<编号>` 的那条 commit。

## Issue：跟踪要做的事

Issue（议题）是 GitHub 仓库里的「待办/问题」单元，用来记录 bug、需求、任务、想法。它挂在仓库的 `Issues` 标签页下，每个 Issue 有编号（如 `#12`）、标题、正文、状态（open / closed）。

### 怎么开一个 Issue

网页：仓库页 → `Issues` → `New issue` → 填标题和正文 → `Submit new issue`。

命令行（gh CLI，macOS / Linux / Windows 通用，Windows 在 PowerShell 或 Git Bash 里都能跑）：

```bash
gh issue create --title "修复：list 命令在空列表时报错" --body "复现步骤：…"
```

一个够用的 Issue 正文模板：

```text
## 现象
（发生了什么）

## 复现步骤
1. …
2. …

## 期望
（应该是什么样）

## 环境
（系统、版本）
```

### 标签与里程碑

- **Label（标签）**：给 Issue 分类，如 `bug`、`enhancement`、`documentation`、`good first issue`（适合新手的简单任务）。仓库主人可以在 `Issues` → `Labels` 自定义。
- **Milestone（里程碑）**：把一组 Issue 归到一个版本/迭代下，如 `v1.0`、`2026-08 sprint`，方便看「离发版还差几个」。

### Issue 和 commit 怎么关联

在 commit message 里写 `Closes #12`（或 `Fixes #12`、`Resolves #12`），当这个 commit 进到默认分支（通常是 `main`）后，GitHub 会**自动关闭** `#12` 这个 Issue。这是 Issue 自动化的核心机制，后面的实战会用到。

```bash
git commit -m "fix: list 命令兼容空列表

Closes #12"
```

想深入协作流程，继续看 [GitHub PR 与 Code Review](./05-GitHub-PR-与-Code-Review.md)。

## Fork 与 Pull Request

### Fork 是什么

Fork（派生）是把**别人的仓库**复制一份到你**自己的 GitHub 账号下**。它和 clone 的区别：

| 操作 | 复制到哪 | 谁的仓库 | 能不能直接改原仓库 |
| --- | --- | --- | --- |
| clone | 你的本地电脑 | 原作者 | 不能（除非有写权限） |
| Fork | 你的 GitHub 账号 | 你自己 | 不能直接改原仓库，但能提 PR |

典型场景：你想给一个开源项目改 bug，但你不是成员。先 Fork 一份到自己账号，在自己的副本里随便改，再向原仓库提 PR（Pull Request，合并请求）。

### Fork → 改 → PR 流程

1. **Fork**：原仓库页右上角 `Fork` → 选你的账号 → 得到 `github.com/你的用户名/仓库名`。
2. **克隆你 fork 出来的仓库**到本地：

   ```bash
   git clone git@github.com:你的用户名/仓库名.git
   cd 仓库名
   ```

3. **关联上游**（方便日后同步原作者的更新）：

   ```bash
   git remote add upstream git@github.com:原作者/仓库名.git
   ```

4. **建分支、改代码、提交、推送**（推到你的 fork）：

   ```bash
   git checkout -b fix-typo
   # 改文件
   git add .
   git commit -m "docs: 修复 README 拼写"
   git push -u origin fix-typo
   ```

5. **开 PR**：GitHub 会在你的 fork 页提示 `Compare & pull request`，点进去把目标选成**原仓库的 `main`**，写好描述提交。

PR 的描述怎么写、Review 怎么做，详见 [GitHub PR 与 Code Review](./05-GitHub-PR-与-Code-Review.md)。

## Release 与 Tag

### Release 是什么

Release（发布）是 GitHub 上给仓库某个版本打「正式包裹」的功能，常用来发布可下载的产物（编译好的程序、安装包、changelog）。它的底层是 **Tag（标签）**——给某个 commit 打一个有名字的标记，如 `v1.2.0`。

Tag 是 Git 概念，Release 是 GitHub 在 Tag 之上加的「发布说明 + 附件」一层。

### 语义化版本（Semantic Versioning）

版本号 `MAJOR.MINOR.PATCH`（主.次.修订）：

- `MAJOR`（主版本）：不兼容的改动（breaking change）
- `MINOR`（次版本）：向后兼容的新功能
- `PATCH`（修订）：向后兼容的 bug 修复

例子：`1.2.0` → `1.2.1`（修 bug）、`1.3.0`（加功能）、`2.0.0`（破坏性改动）。

### 怎么发一个 Release

命令行（gh CLI，macOS / Linux / Windows 通用）：

```bash
# 1. 先打 tag
git tag v1.0.0
git push origin v1.0.0

# 2. 基于 tag 创建 Release
gh release create v1.0.0 --title "v1.0.0" --notes "首个正式版本"
```

网页：仓库页 → `Releases` → `Draft a new release` → 选 tag → 填标题和说明 → `Publish release`。

## GitHub Actions 与 CI

### Actions 是什么

GitHub Actions 是 GitHub 内置的**自动化引擎**：你在仓库里放一个 workflow 文件，它就会在指定事件（push、PR、定时、手动等）触发时，自动起一台虚拟机（叫 **runner**，运行器）跑你定义的步骤。常用来做 **CI（Continuous Integration，持续集成）**——每次提交自动跑测试/检查，红了就阻止合并。

**workflow**（工作流）就是描述「什么时候、在哪台机器、跑哪些步骤」的那个 YAML 文件，放在仓库的 `.github/workflows/` 目录下。

### workflow.yml 的结构

一个 workflow 文件大致长这样：

```yaml
name: <工作流名字>

on:                  # 触发条件
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:                # 一组任务
  <job 名>:
    runs-on: ubuntu-latest        # 在哪种 runner 上跑
    steps:                        # 一步步执行
      - uses: actions/checkout@v4  # 拉代码
      - run: echo "hello"           # 跑命令
```

四个关键块：`on`（触发）、`jobs`（任务）、`runs-on`（运行环境）、`steps`（步骤）。

### 本仓库的真实例子

本仓库的 `.github/workflows/check.yml` 就是一个真实在跑的 CI。它做的事：

- **触发**：`push` 或 `pull_request` 到 `main` 时跑。
- **runner**：`ubuntu-latest`（GitHub 提供的 Linux 虚拟机）。
- **步骤**：检出代码 → 配置 Python → 运行 `bash scripts/check.sh`（带严格模式环境变量 `STRICT_LINKS=1`、`STRICT_SH_SYNTAX=1`），检查断链、shell 语法、Python 编译、Skill frontmatter。

它的 job 名叫 `scripts/check.sh（严格模式）`——这个名字后面分支保护会引用。

本地想对齐 CI 的复跑方式（macOS / Linux / Windows 通用）：

```bash
STRICT_LINKS=1 STRICT_SH_SYNTAX=1 bash scripts/check.sh
```

### CI 通过 ≠ 功能可用

这是新手最容易踩的认知坑。`check.yml` 跑的 `scripts/check.sh` 只验证「断链、语法、frontmatter」这类**静态属性**，它**不会**真的去运行你的程序看功能对不对。

换句话说：

- CI 绿 = 「我定义的检查脚本跑完了，没报错」。
- CI 绿 ≠ 「这个功能在真实环境下能正常工作」。

功能对不对，得靠**测试**（写用例验证行为）+ 真机验证。测试、Lint、CI 的区别详见 [测试、Lint 与 CI 入门](./10-测试LintCI.md)。

## 分支保护

### 为什么要保护 main

`main` 是仓库的默认主干分支，通常是「随时可发布」的稳定版本。如果谁都能直接 `git push` 到 `main`，很容易把没测过的代码、半成品推进去，主干就乱了。

**分支保护（branch protection，分支保护规则）** 就是给 `main`（或任何分支）加门禁，让不符合条件的改动进不来。

### 常见的保护项

- **Require a pull request before merging**：必须走 PR，不能直接 push。
- **Require status checks to pass**（required check，必需检查）：指定的 CI 检查必须绿才能合并。
- **Require approvals**：PR 需要至少 N 个人 approve。
- **Require branches to be up to date**：合并前必须基于最新 `main`。

### 本仓库的真实配置

本仓库的 `main` 分支已经配了保护规则（可通过 `gh api repos/:owner/:repo/branches/main/protection` 查到），实际生效的关键项：

- 开启了 **required pull request**：必须走 PR，不能直接 push 到 `main`。
- 设了 **required status check**：`scripts/check.sh（严格模式）`——也就是上一节那个 CI job 名。它必须通过才能合并。
- 审批数（`required_approving_review_count`）当前为 `0`，意味着单人项目可以自己合并自己的 PR（CI 过即可）。

配 required check 的入口：仓库 `Settings` → `Branches` → `Branch protection rules` → `Add rule` → 勾选 `Require status checks to pass before merging` → 在列表里选 `scripts/check.sh（严格模式）`。

> 注意一个细节：required check 名字必须和 workflow 里 job 的 `name`（或 status 显示的 context）**一字不差**，否则 GitHub 认不出这是同一条检查，保护规则会失效。

## 实战：从 Issue 到 PR 合并

把前面几节串起来，走一个端到端小例子。目标：发现 `todo.py` 的 `list` 命令在空列表时报错，从开 Issue 到合并、Issue 自动关闭，共 **6 步**。

前置：你已经 clone 了仓库、配好了 SSH 或 Token、装了 gh CLI（`gh auth login` 登录过）。

**第 1 步：开 Issue**

```bash
gh issue create --title "bug: list 命令在空列表时报错" --body "空 todos.json 时 `todo.py list` 抛 IndexError。"
```

记下编号，假设是 `#12`。

**第 2 步：基于 main 建分支**

```bash
git checkout main
git pull
git checkout -b fix-12-empty-list
```

分支名带 Issue 号（`fix-12-...`），方便对照。

**第 3 步：改代码并提交（带 Closes #12）**

```bash
# 编辑 todo.py，让 list 在空列表时打印 "（空）" 而不是报错
git add todo.py
git commit -m "fix: list 命令兼容空列表

Closes #12"
```

commit message 里的 `Closes #12` 是关键——合并进 main 后 GitHub 会自动关闭 `#12`。

**第 4 步：推送并开 PR**

```bash
git push -u origin fix-12-empty-list
gh pr create --base main --head fix-12-empty-list --title "fix: list 命令兼容空列表" --body "修复 #12"
```

PR 一开，`.github/workflows/check.yml` 会自动触发，在 runner 上跑 `scripts/check.sh`。

**第 5 步：等 CI 过**

在 PR 页面等 `scripts/check.sh（严格模式）` 变绿。如果红了，按日志改完再 `git push`，CI 会重跑。

注意：CI 绿只代表静态检查过了，**功能对不对要你自己本地再跑一遍** `todo.py list`（空列表场景）确认。

**第 6 步：合并（CI 过 + 分支保护放行）**

因为 `main` 设了 required check `scripts/check.sh（严格模式）`，CI 必须绿才能合并。CI 绿了之后：

```bash
gh pr merge 12 --squash --delete-branch
```

合并后两件事自动发生：

- commit 进了 `main`，`Closes #12` 生效，**Issue `#12` 自动关闭**。
- 分支 `fix-12-empty-list` 被删除（`--delete-branch`）。

到此一个完整闭环走完：Issue → 分支 → 改 → PR → CI → 合并 → Issue 自动关。这就是 GitHub 上绝大多数日常协作的标准路径。

## 官方资料

- GitHub 官方认证说明：[About authentication to GitHub](https://docs.github.com/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)
- GitHub 官方 Token 说明：[Managing your personal access tokens](https://docs.github.com/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## 下一篇

仓库连上、能 push 之后，下一步是把「提交」这件事做规范——每次 `git commit` 写什么、一次提交放多少东西、push 之后去 GitHub 检查什么。

继续看 [提交到 GitHub 与 Commit 规范](./04-提交到-GitHub-与-Commit-规范.md)，它会给你一套照着用就够的 commit message 写法。

> 想直接进协作流程（PR、Code Review、合并策略）的，可以跳到 [GitHub PR 与 Code Review](./05-GitHub-PR-与-Code-Review.md)；认证那块若打算长期用 SSH，先补 [SSH 配置](./03-SSH-配置.md)。其它工具篇随时可从 [README](../README.md) 回查。

## 一句话总结

GitHub 入门最重要的不是“记住所有页面”，而是：

**会创建仓库、会连接本地、会安全地提交和协作。**
