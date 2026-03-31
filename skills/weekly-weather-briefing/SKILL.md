---
name: weekly-weather-briefing
description: |
  生成每周天气播报摘要。本技能应在用户需要准备周会天气提醒、为团队同步一周天气概览、或输出一份可发送的天气 Markdown 周报时使用。
  不要用于：实时单次天气查询、分钟级降雨预警、长期气候趋势分析。
---

# Weekly Weather Briefing

一个完整示例 Skill，用来演示：

- `SKILL.md` 怎么写
- `scripts/` 怎么组织
- `CHANGELOG.md`、`ROADMAP.md`、`TASKS.md`、`DECISIONS.md` 如何协同工作

## 适用场景

- 团队每周例会前，需要一份天气概览
- 需要把天气摘要写成 Markdown 文件再转发
- 需要一个可运行但不依赖外部 API 的 Skill 示例

## 不适用场景

- “帮我查一下今天下午 3 点会不会下雨”
- “帮我分析过去 10 年气候变化”
- “帮我调用真实天气 API 并做分钟级预警”

## 输入

- `location`：地点，默认读取环境变量 `DEFAULT_LOCATION`，未设置则用 `苏州`
- `audience`：播报对象，默认 `团队成员`
- `output_dir`：输出目录，默认读取环境变量 `OUTPUT_DIR`，未设置则写入 `./output`

## 输出

- 一个 Markdown 文件：`weekly-weather-briefing.md`
- 终端打印输出路径

## 快速开始

```bash
python3 scripts/main.py --location 上海 --audience 产品团队
```

生成后可在 `output/weekly-weather-briefing.md` 查看结果。

## 与其他技能配合

- 生成 Markdown 后，可以交给发送类 Skill 发到飞书或邮件
- 如果后续接入真实天气源，可以配合抓取或 API Skill 做数据层扩展

## 目录说明

```text
weekly-weather-briefing/
├── SKILL.md
├── CHANGELOG.md
├── ROADMAP.md
├── TASKS.md
├── DECISIONS.md
├── .env.example
├── assets/config.yaml.example
├── references/
├── scripts/main.py
```

## 依赖

当前示例零外部依赖，只使用 Python 标准库。

## 维护说明

如果你把这个示例改造成真实 Skill，至少同步更新：

- `CHANGELOG.md`
- `ROADMAP.md`
- `TASKS.md`
- `DECISIONS.md`
