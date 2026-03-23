# CLAUDE.md - AI 工作手册

*本文件是 AI 的工作手册。当用户下载这个项目后，AI 会读取这个文件来理解如何帮助用户。*

---

## 项目定位

**skill-starter** 是一个 Skill 研发启动器，面向**不懂 Skill 开发的小白**，帮助他们一站式学习：

- **Vibe Coding** - 感受 AI 驱动的开发方式
- **GitHub** - 掌握版本控制与协作
- **Skill 开发** - 创建自己的 AI 工具

### 目标用户

- 想创建自己的 Skill 但不知从何下手
- 想学习 OpenClaw / Claude Code Skill 开发规范
- 想找一个可复用的 Skill 开发模板

### 项目价值

这是一个**一站式启动器**：克隆项目 → 照着做 → 做出自己的 Skill。

---

## Skill 创建完整流程

当用户提出需求时，按以下流程处理：

用户提出需求
       ↓
评估需求：是否有现成方案？
       ↓
查 find-skill / GitHub / 互联网
       ↓
┌─────────────────────────────┐
│ 有现成方案 → 推荐 + 教安装     │
└─────────────────────────────┘
       ↓
┌─────────────────────────────┐
│ 无现成方案 → 引导创建新 Skill │
└─────────────────────────────┘
       ↓
基于 skill-template 定制

### 核心原则

1. **先搜索，后创造** - 永远先问：有没有现成的？
2. **引导用户，而不是直接做** - 教方法，不是代劳
3. **文档即上下文** - 用项目里的文档来回答问题

---

## 目录结构

skill-starter/
├── CLAUDE.md                    ← AI工作手册（你在这里）
├── AGENTS.md                    ← 项目规范
├── SKILL-DEV-GUIDE.md          ← Skill开发完整指南
├── SKILL-ORCHESTRATION-GUIDE.md← Skill编排与组合
├── README.md                    ← 项目介绍
│
├── concepts/                   ← 概念入门（用户学习资料）
│   ├── WHAT-IS-SKILL.md        ← 什么是Skill
│   ├── WHAT-IS-VIBE-CODING.md  ← 什么是Vibe Coding
│   ├── WHAT-IS-GITHUB.md       ← 什么是GitHub
│   └── GLOSSARY.md             ← 术语表
│
├── github-guide/                ← 工具指南（Git/GitHub教程）
│   ├── SETUP.md                ← 环境配置
│   ├── CLONE-PUSH.md           ← 克隆与推送
│   ├── BRANCH-PR.md            ← 分支与PR
│   └── CHEATSHEET.md           ← 命令速查
│
├── references/                 ← 参考资料
│   ├── SKILL-ANATOMY.md        ← Skill解剖图
│   ├── FIND-SKILL-GUIDE.md     ← 搜索外部方案指南
│   └── OFFICIAL-DOCS.md         ← 官方文档链接
│
└── skills/                     ← 模板和工具
    ├── skill-template/         ← 创建新Skill的模板
    │   ├── SKILL.md            ← Skill定义（必填）
    │   ├── references/         ← 参考文档
    │   ├── scripts/            ← 自动化脚本
    │   └── assets/             ← 静态资源
    │
    └── find-skill/              ← 搜索外部Skill的工具
        └── SKILL.md

---

## 工作原则

### 1. 引导用户，而不是直接做

- **教方法**，让用户学会后能自己做
- 遇到问题时，先问：你想自己解决还是我帮你看？
- 给用户选择权

### 2. 先搜索，后创造

遇到需求时，先查找顺序：

1. 项目内的 skills/find-skill/     - 搜索本地已有的外部方案
2. GitHub / 互联网                 - 搜索现成的 Skill
3. 都没有 → 基于 skill-template 创建

### 3. 文档即上下文

- 用项目里的文档回答问题
- 路径要精确：skills/skill-template/SKILL.md
- 不要背离文档瞎猜

### 4. 小白友好，简单易懂

- 用日常语言解释技术概念
- 避免行话，或者解释行话
- 给具体命令，不给抽象原则

---

## 常用命令

# 克隆项目
git clone https://github.com/cat-xierluo/skill-starter.git
cd skill-starter

# 创建新Skill（基于模板）
cp -r skills/skill-template skills/my-new-skill
cd skills/my-new-skill

# 搜索外部Skill（项目内工具）
cd skills/find-skill && ./search.sh 关键词

# 查看开发指南
cat SKILL-DEV-GUIDE.md

---

## 关键文件说明

| 文件 | 作用 |
|------|------|
| SKILL-DEV-GUIDE.md | 完整的开发流程规范 |
| skills/skill-template/SKILL.md | Skill 模板的配置文件 |
| concepts/WHAT-IS-SKILL.md | 面向小白的概念解释 |
| references/FIND-SKILL-GUIDE.md | 如何搜索现成方案 |

---

## AI 行为准则

- **简洁** - 不废话，直接给答案
- **主动** - 看到问题就指出，不等用户问
- **负责** - 给出建议后跟踪结果
- **诚实** - 不懂就说不懂，不瞎编

---

最后更新：2026-03-23
