# Issue: GitHub 基础模块 - 从注册到第一个 PR

## 背景

新手需要一步步的实操指南，才能真正上手使用 GitHub。本模块提供"手把手"式的操作指引。

## 任务描述

在项目目录创建 `github-guide/` 目录，新增以下文档：

### 1. `github-guide/SETUP.md` - 账号与环境配置
- 注册 GitHub 账号（截图+步骤）
- 配置 Git（安装、基础配置）
- 生成 SSH Key 并添加到 GitHub
- 验证连接是否成功

### 2. `github-guide/CLONE-PUSH.md` - 克隆与提交
- 什么是 Clone？为什么需要？
- 如何 Clone 一个项目到本地
- 什么是 Commit？（保存快照）
- 如何 Commit（git add + git commit）
- 什么是 Push？（上传到云端）
- 如何 Push（git push）

### 3. `github-guide/BRANCH-PR.md` - 分支与协作
- 什么是 Branch？（分支=平行世界）
- 为什么需要分支？
- 如何创建分支（git branch / git checkout -b）
- 什么是 Pull Request？（请求合并）
- 如何创建 PR
- 如何 Review PR

### 4. `github-guide/CHEATSHEET.md` - 命令速查表
常用 Git 命令速查，按场景分类：
- 日常操作：status, add, commit, push, pull
- 分支操作：branch, checkout, merge
- 查看历史：log, diff, show

## 验收标准

- [ ] `github-guide/SETUP.md` 完成，有截图位置说明
- [ ] `github-guide/CLONE-PUSH.md` 完成，每步有命令示例
- [ ] `github-guide/BRANCH-PR.md` 完成，有完整流程图（ASCII 或文字描述）
- [ ] `github-guide/CHEATSHEET.md` 完成，至少 15 个常用命令
- [ ] 所有文档中文，命令用代码块展示

## 分配给
openclaw

## 优先级
P0

## 标签
github, tutorial, hands-on
