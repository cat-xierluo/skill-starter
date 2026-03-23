# 🆕 Skills Starter

> Skill 研发启动模板 - 帮助开发者快速开始 Skill 开发

## 📖 简介

Skills Starter 是一个 Skill 研发启动模板，帮助开发者快速开始 OpenClaw / Claude Code 的 Skill 开发。本项目沉淀了 Skill 开发的核心规范、最佳实践和实用工具。

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/skills-starter.git
cd skills-starter
```

### 2. 选择你的路径

- **想创建一个新 Skill**：直接使用 `skills/skill-template/` 模板
- **想学习 Skill 开发规范**：阅读 `SKILL-DEV-GUIDE.md`

### 3. 基于模板创建新 Skill

```bash
cp -r skills/skill-template skills/your-new-skill
cd skills/your-new-skill
# 修改 SKILL.md 中的 name 和 description
```

## 开发流程

1. **找方案** - 先看有没有现成的 → `skills/find-skill/`
2. **学规范** - 阅读开发指南 → `SKILL-DEV-GUIDE.md`
3. **动手做** - 基于模板开发 → `skills/skill-template/`

## 📁 项目结构

```
skills-starter/
├── AGENTS.md                    # 项目规范
├── CLAUDE.md                    # Claude 上下文
├── SKILL-DEV-GUIDE.md          # Skill 开发指南
├── SKILL-ORCHESTRATION-GUIDE.md # Skill 编排指南
├── README.md                     # 本文件
│
├── skills/                      # Skills 目录
│   ├── skill-template/          # Skill 模板
│   │   ├── SKILL.md            # Skill 定义
│   │   ├── references/         # 参考文档
│   │   ├── scripts/            # 自动化脚本
│   │   └── assets/             # 静态资源
│   └── find-skill/              # 搜索外部方案工具
│       └── SKILL.md            # Skill 定义
│
└── references/                  # 参考资料
    └── FIND-SKILL-GUIDE.md     # 新手搜索指南
```

## 📚 核心规范

### SKILL.md 必填字段

```yaml
---
name: skill-name          # Skill 名称（英文）
description: "描述"       # 简短描述
metadata:
  openclaw:
    emoji: "🎯"           # Emoji 图标
    requires: []          # 前置依赖
    triggers: []           # 触发关键词
---
```

### 目录结构规范

每个 Skill 应包含：

| 文件/目录 | 说明 |
|-----------|------|
| `SKILL.md` | **必填**，Skill 定义和使用说明 |
| `references/` | 参考文档（可选） |
| `scripts/` | 自动化脚本（可选） |
| `assets/` | 静态资源（可选） |

## 🔧 开发工具

### 推荐工具

- [ClawHub](https://clawhub.com) - Skill 市场
- [Claude Code](https://claude.com/code) - AI 编程助手
- [OpenClaw](https://openclaw.ai) - 开源 AI 助手框架

### 官方资源

- [OpenClaw 文档](https://docs.openclaw.ai)
- [Claude Code Plugin Dev](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev)
- [Skill Creator 官方指南](https://clawhub.com/skills?search=skill-creator)

## 📖 文档

| 文档 | 说明 |
|------|------|
| `SKILL-DEV-GUIDE.md` | 完整的 Skill 开发指南 |
| `SKILL-ORCHESTRATION-GUIDE.md` | Skill 编排和组合指南 |
| `AGENTS.md` | 项目规范和约定 |
| `references/FIND-SKILL-GUIDE.md` | 新手指南：如何搜索外部现成方案 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**基于 [legal-skills](https://github.com/cat-xierluo/legal-skills) 规范模板**
