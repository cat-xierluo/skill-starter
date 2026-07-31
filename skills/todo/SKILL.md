---
name: todo
description: |
  本技能应在用户要管理本地待办（新增 / 查看 / 完成）、说「记一下」「加个待办」
  「我有什么待办」「把某项标完成」时使用。通过运行 scripts/todo.py 读写运行目录下的 todos.json。
  不要用于：团队协作看板、带截止时间提醒、日历事件、跨设备同步。
license: MIT
---

# todo

管理本地待办列表，数据存在运行目录（cwd）下的 `todos.json`。

本 Skill 是 skill-starter 仓库的**端到端标准示例**：从触发、契约、脚本、错误路径、测试到维护文档都完整可运行，用于演示一个真实的带脚本型 Skill 长什么样。完整教程见 [07 带脚本 Skill](../../04-创建Skill/07-带脚本-Skill.md)。

## 何时调用

- 用户要新增、查看或完成一条待办时，调用 `scripts/todo.py`。
- 涉及到期提醒、多人协作、跨设备同步时不要用。

## 脚本契约

`scripts/todo.py` 三个命令：

- `add <text>`：新增一条。成功时 stdout 输出该条 JSON，退出码 0。
- `list`：列出全部。stdout 输出易读列表，退出码 0。
- `done <id>`：标记完成。成功时 stdout 输出该条 JSON，退出码 0；
  找不到 id 时退出码 1。

约定：成功信息走 stdout（结构化 JSON，便于你解析）；错误信息走 stderr；
退出码 0 表示成功，非 0 表示失败——非 0 时不要当成功处理，去读 stderr 找原因。

## 数据位置

`todos.json` 写在**运行命令时的当前工作目录**（cwd），而不是 Skill 源目录。这样在任意目录都能跑，也便于在临时目录里隔离测试，不污染 Skill 源代码。

## 依赖

只用 Python 3 标准库（`json`、`sys`、`pathlib`），无外部依赖，复制过去就能跑。
