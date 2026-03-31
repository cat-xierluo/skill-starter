---
name: skill-template
description: |
  Skill 开发起点模板。本技能应在用户需要新建一个 Skill、补齐 Skill 仓库结构、整理 SKILL.md、或为长期维护的 Skill 加入 CHANGELOG/ROADMAP/TASKS/DECISIONS 协作文档时使用。
  不要用于：直接替代具体业务 Skill、执行某个垂直领域任务、或在没有明确需求时生成大量无关模板文件。
---

# Skill 模板

这是一个偏实战的起点模板，目标不是只给你一个 `SKILL.md`，而是给你一套能长期维护的 Skill 仓库骨架。

单个 Skill 内部的文档组织，参照 `legal-skills` 里的常见做法：文档尽量平铺在 Skill 根目录，不再额外拆 `docs/`、`status/` 二级目录。

## 适用场景

✅ 应该使用：

- 从零创建一个新的 Skill
- 把已有 Skill 从“单文件说明”整理为“可维护仓库”
- 为 Skill 加入根目录的 `ROADMAP.md`、`TASKS.md`、`DECISIONS.md`
- 统一 `.env.example`、`assets/config.yaml.example` 和脚本入口

❌ 不应该使用：

- 直接执行垂直任务，比如发消息、查天气、抓网页
- 构建完整 Web 应用或插件系统
- 只做一次性的问答，不需要沉淀为 Skill

## 推荐目录结构

```text
skill-name/
├── SKILL.md
├── CHANGELOG.md
├── ROADMAP.md
├── TASKS.md
├── DECISIONS.md
├── .env.example
├── .gitignore
├── references/
│   └── README.md
├── scripts/
│   └── main.py
├── assets/
│   ├── config.yaml.example
│   └── requirements.txt
```

规则：

- `references/`、`scripts/`、`assets/` 保持扁平
- `.env.example` 放根目录，作为环境变量模板
- `config.yaml.example` 等结构化配置模板放 `assets/`
- 协作文档直接放 Skill 根目录，不要把重要上下文只留在聊天里

## Frontmatter 规范

必需字段：

```yaml
---
name: skill-name
description: |
  本技能应在...时使用。
  不要用于：...。
---
```

写作要求：

1. `name` 用英文，目录名通常与之保持一致
2. `description` 写清正向触发和负向触发
3. 不要只写“用于 XXX”
4. 不要把实现细节塞进 frontmatter

## 快速开始

### 1. 复制模板

```bash
cp -r skills/skill-template skills/my-skill
cd skills/my-skill
```

### 2. 先改这些文件

- `SKILL.md`
- `CHANGELOG.md`
- `.env.example`
- `assets/config.yaml.example`
- `ROADMAP.md`
- `TASKS.md`
- `DECISIONS.md`

### 3. 跑一下示例脚本

```bash
python3 scripts/main.py --task "describe the skill goal"
```

脚本会在 `output/` 下生成一个最小结果文件，方便你确认目录和路径是通的。

## 协作文档怎么用

### `CHANGELOG.md`

记录对外可见的变更，比如：

- 新增功能
- 调整触发逻辑
- 修复输出格式

### `ROADMAP.md`

记录阶段目标和里程碑，用来回答“这个 Skill 还准备做什么”。

### `TASKS.md`

记录当前待办，避免下一位维护者重新猜一遍。

### `DECISIONS.md`

记录关键决策和工作日志，用来回答“为什么这样做”。

## 配置约定

### 环境变量模板

`.env.example` 放在 Skill 根目录，例如：

```dotenv
API_KEY=
MODEL_NAME=
OUTPUT_DIR=
```

### 结构化配置模板

`assets/config.yaml.example` 适合这种内容：

```yaml
default_output_dir: ./output
mode: demo
max_items: 5
```

## 验收清单

- [ ] `name` 和目录名一致
- [ ] `description` 有负向触发条件
- [ ] `SKILL.md` 保持精简，详细内容移到 `references/`
- [ ] `.env.example` 与 `assets/config.yaml.example` 职责分离
- [ ] `CHANGELOG.md`、`ROADMAP.md`、`TASKS.md`、`DECISIONS.md` 已初始化
- [ ] `scripts/main.py` 可以直接跑通

## 参考示例

需要一个完整参考时，优先看：

- [weekly-weather-briefing](../weekly-weather-briefing/SKILL.md)

## 相关链接

- [Skill 开发总指南](../../SKILL-DEV-GUIDE.md)
- [Skill 编排指南](../../SKILL-ORCHESTRATION-GUIDE.md)
- [Skills.sh](https://skills.sh/)
