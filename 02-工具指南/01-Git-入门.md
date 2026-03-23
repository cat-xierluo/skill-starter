# Git 入门

## 什么是 Git？

Git 是一个分布式版本控制系统，用于跟踪文件变化、协作开发。它可以记录谁在什么时候修改了什么内容，方便回溯和合并。

## 安装 Git

### Windows
1. 访问 https://git-scm.com/download/win
2. 下载安装包，运行安装
3. 安装完成，右键菜单会出现 "Git Bash Here"

### Mac
```bash
# 如果已安装 Homebrew
brew install git

# 或者下载安装包
# 访问 https://git-scm.com/download/mac
```

### Linux
```bash
# Ubuntu / Debian
sudo apt update && sudo apt install git

# CentOS / Fedora
sudo yum install git
```

## 基础配置

安装完成后，需要设置用户名和邮箱：

```bash
git config --global user.name "你的名字"
git config --global user.email "your.email@example.com"
```

验证配置：
```bash
git config --list
```

## 基础命令

### 初始化仓库
```bash
git init
```
在当前目录创建一个新的 Git 仓库。

### 查看状态
```bash
git status
```
查看工作区的文件状态（已修改、已暂存等）。

### 暂存文件
```bash
# 暂存单个文件
git add 文件名

# 暂存所有文件
git add .

# 暂存所有修改
git add -A
```

### 提交记录
```bash
git commit -m "提交说明"
```

### 查看提交历史
```bash
git log
git log --oneline    # 简洁模式
```

## 核心概念

### 工作区（Working Directory）
你正在编辑文件的地方，即项目的文件夹。

### 暂存区（Staging Area）
也称为索引（Index）。文件修改后，先暂存到这里，表示这些修改将被提交。

### 仓库（Repository）
`.git` 目录，存放所有的版本历史和提交记录。

### 工作流程
```
工作区 → git add → 暂存区 → git commit → 仓库
```

## 常用操作示例

```bash
# 1. 初始化
git init

# 2. 创建/编辑文件后，查看状态
git status

# 3. 暂存文件
git add .

# 4. 提交
git commit -m "第一次提交"

# 5. 查看历史
git log
```
