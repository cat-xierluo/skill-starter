---
name: skill-start-update
description: |
  本技能应在用户每次首次运行 Claude Code 时自动检查 skill-starter 项目是否有远程更新。
  不要用于：主动发起 Git 操作（commit/push/pull）、非 skill-starter 仓库检查。
---

# skill-start-update

检查 skill-starter 项目相对远程分支是否有更新，在有更新时提示用户。

## 核心逻辑

1. 检查距离上次检测是否超过配置的间隔（默认 48 小时）
2. 若超过，执行 `git fetch` + 对比本地 HEAD 与远程分支
3. 若有更新，输出提示信息（含 commit 历史摘要）
4. 更新检测记录到 `~/.myagents/.skill-starter-last-check.json`

## 使用方式

Skill 被调度时会自动运行，无需手动触发。

## 输出格式

有更新时：

```
📦 skill-starter 有 {n} 个新提交

最近更新:
- {commit_hash} - {commit_message}
- ...

提示: cd {path} && git pull
```

无更新时：静默退出，不输出任何内容。
