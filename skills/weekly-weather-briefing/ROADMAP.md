# 项目路线图

> Last updated: 2026-03-30

## 项目愿景

把 `weekly-weather-briefing` 作为 starter 仓库里的完整参考样例，展示一个 Skill 如何从模板进化到可维护仓库。

## 阶段状态速览

| 阶段 | 目标摘要 | 当前状态 | 备注 |
| :--- | :--- | :--- | :--- |
| 阶段一 | 跑通一个零依赖 Demo | 🟢 已完成 | 当前脚本可直接运行 |
| 阶段二 | 接入真实天气数据源 | ⚪ 未开始 | 后续可接天气 API |
| 阶段三 | 增加发送和自动化场景 | ⚪ 未开始 | 如飞书、邮件、定时运行 |

## 任务详情

### 阶段一：零依赖 Demo

- [x] 编写 `SKILL.md`
- [x] 提供 `.env.example`
- [x] 提供 `assets/config.yaml.example`
- [x] 跑通 `scripts/main.py`
- [x] 建立 `ROADMAP.md`、`TASKS.md`、`DECISIONS.md`、`CHANGELOG.md`

### 阶段二：真实数据接入

- [ ] 选定天气 API
- [ ] 增加错误处理和降级逻辑
- [ ] 补充真实输出示例

## 进度日志

- **2026-03-30**
  - 初始化完整示例 Skill
  - 使用静态天气数据保证脚本可直接运行
