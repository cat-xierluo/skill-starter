# 决策记录与工作日志

## 决策记录

### [DEC-001] - 2026-07-30 - todos.json 写到运行目录（cwd）而非 Skill 源目录

**背景**

教程版 `todo.py` 把数据写到 `Path(__file__).parent.parent / "todos.json"`（Skill 根目录）。落盘成可测 Skill 时，仓库级验收（TASKS T-008）要求「在独立临时目录安装和运行」——若数据写到 Skill 源目录，每次测试都会污染工作树。

**决策**

改为 `Path.cwd() / "todos.json"`：数据写到运行命令时的当前工作目录。

**理由**

- 在临时目录里跑测试时，数据天然写在临时目录内，测试结束自动清理，不污染 Skill 源代码。
- 这正是 [07 带脚本 Skill](../../04-创建Skill/07-带脚本-Skill.md) 常见错误「硬编码路径，换个目录就崩」的正确实践。
- 让 Skill 在任意目录都能跑，符合「可移植」的默认期望。

**影响**

`scripts/todo.py` 的 `DB` 定义；`SKILL.md` 的「数据位置」段已说明。教程篇脚本片段已同步。

### [DEC-002] - 2026-07-30 - 采用带脚本维护型的最简变体，删除 .env.example / config.yaml.example / requirements.txt

**背景**

`todo.py` 只用标准库、不读配置、无外部依赖。若照搬模板的 `.env.example`、`assets/config.yaml.example`、`assets/requirements.txt`，会违反 skill-template 验收清单「配置字段必须被实现实际读取」的约束。

**决策**

删掉这三个文件，只保留 `assets/todos.example.json`（数据形态示例）。

**理由**

- 宁缺毋滥：模板验收清单要求配置字段必须被真实读取，todo 没有配置需求就不该留空壳配置文件。
- 符合 skill-template 双 profile 设计：这是「带脚本维护型」的最简变体（无配置、无依赖）。

**影响**

`skills/todo/` 目录不包含 `.env.example`、`assets/config.yaml.example`、`assets/requirements.txt`。

## 工作日志

### 2026-07-30 (skill-starter 维护者)

- **目标:** 落盘 starter 原创端到端标准示例 Skill（仓库 TASKS T-007）。
- **操作:** 创建 `skills/todo/` 全部文件；脚本契约对齐 07 篇教程；配套回归测试。
- **结果:** add/list/done 可运行，错误路径退出码诚实，测试覆盖正常/错误/守恒/隔离四类。
- **下一步:** 进入 T-008 真实 Agent 触发验证（需可隔离 Agent 环境）。
