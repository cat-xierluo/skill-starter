# Changelog

本文件记录本 Skill 对外可见的变更。

## 0.1.0 - 2026-07-30

### Added

- 初始版本：`add` / `list` / `done` 三命令，纯标准库实现。
- `scripts/todo.py`：成功结果走 stdout（JSON），错误走 stderr，退出码诚实（0 成功 / 1 找不到 id / 2 用法错误）。
- 作为 skill-starter 仓库的端到端标准示例落盘（对应 TASKS T-007），同时是 [07 带脚本 Skill](../../04-创建Skill/07-带脚本-Skill.md) 教程里 todo.py 片段的完整可运行版。
- 配套回归测试见仓库根 `tests/test_skill_todo.py`。
