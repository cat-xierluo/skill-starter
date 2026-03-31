# Git 入门

这篇文档只解决一件事：

**让你第一次真正把 Git 用起来。**

如果你只记住一句话：

> Git 是记录文件变化历史的工具。

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

### 1. 工作区

你正在编辑文件的地方。

### 2. 暂存区

你准备提交的改动会先进入这里。

### 3. 仓库历史

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

### 1. 创建测试目录

```bash
mkdir git-demo
cd git-demo
```

### 2. 初始化 Git 仓库

```bash
git init
```

这会在当前目录生成 `.git/`，表示 Git 开始管理这个文件夹。

### 3. 创建一个文件

```bash
echo "# Git Demo" > README.md
```

### 4. 查看状态

```bash
git status
```

你会看到 `README.md` 还没有被提交。

### 5. 暂存文件

```bash
git add README.md
```

### 6. 提交

```bash
git commit -m "feat: 初始化 Git Demo"
```

### 7. 查看历史

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

## 常见错误

### 1. `fatal: not a git repository`

原因：你不在 Git 仓库目录里。

解决：

```bash
pwd
ls -la
```

确认当前目录是否有 `.git/`。

### 2. `nothing to commit`

原因：

- 没有改动
- 改了但没 `git add`

先执行：

```bash
git status
```

### 3. 提交作者信息不对

重新设置：

```bash
git config --global user.name "你的名字"
git config --global user.email "your.email@example.com"
```

### 4. 把不该提交的文件加进去了

先补 `.gitignore`，再处理跟踪状态。

## 新手推荐实践

1. 小步提交，不要攒很大一坨改动
2. 提交前先 `git status`
3. 提交前先 `git diff --staged`
4. 别直接在 `main` 上乱改
5. 配合 GitHub 使用时，优先走分支 + PR

## 下一步看什么

读完这篇，建议接着看：

- [GitHub 入门](./02-GitHub-入门.md)
- [SSH 配置](./03-SSH-配置.md)
- [提交到 GitHub 与 Commit 规范](./04-提交到-GitHub-与-Commit-规范.md)

## 一句话总结

Git 的核心不是“会背命令”，而是：

**学会安全地记录、比较、回退和协作。**
