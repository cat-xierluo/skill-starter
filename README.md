# 🆕 Skills Starter

**Skill 开发启动模板** — 让你从零到一快速掌握 OpenClaw / Claude Code 的 Skill 开发

> ✨ 不管你是 AI 小白还是开发者，这个模板都能帮你少走弯路，直接上手！

---

## 👀 谁适合用这个项目？

- **AI 新手**：想了解什么是 Skill、怎么让 AI 助手更强大
- **开发者**：想为 OpenClaw 或 Claude Code 开发自己的 Skill
- **效率控**：想把重复工作封装成可复用的 Skill

---

## 🎓 你能学到什么？

- ✅ **Skill 是什么**：理解 OpenClaw Skill 的核心概念和设计理念
- ✅ **规范开发**：掌握 SKILL.md 怎么写、目录怎么组织
- ✅ **模块化思维**：学会把大脚本拆成独立可复用的小模块
- ✅ **快速启动**：用模板 5 分钟跑通一个可用的 Skill
- ✅ **协作流程**：了解 Git 分支管理和 Pull Request 规范

---

## 🚀 5 分钟快速体验

### 第一步：找个现成的用用

直接使用 `skills/find-skill/` 搜索外部现成 Skill，不重复造轮子：

```bash
# 搜索 ClawHub 上的 Skill
# （由 find-skill 工具自动完成）
```

### 第二步：基于模板创建你自己的 Skill

```bash
# 复制模板
cp -r skills/skill-template skills/my-awesome-skill

# 进入目录，修改 SKILL.md 中的 name 和 description
cd skills/my-awesome-skill
```

### 第三步：启动开发

1. 修改 `SKILL.md` 的 frontmatter（名称 + 描述）
2. 在 `scripts/` 下写你的核心逻辑
3. 在 `references/` 下放参考文档
4. 在 `assets/` 下放配置文件模板

### 第四步：验证一下

对着检查清单过一遍：

- [ ] frontmatter 格式正确（`name` + `description`）
- [ ] `description` 包含负向触发条件（什么时候**不该**用）
- [ ] `SKILL.md` 正文不超过 500 行
- [ ] `references/` 目录保持扁平（一级目录）

---

## 📁 项目结构

```
skill-starter/
├── README.md                        # 📖 你现在看的这本
├── SKILL-DEV-GUIDE.md               # 📚 完整的 Skill 开发指南
├── SKILL-ORCHESTRATION-GUIDE.md     # 🔗 Skill 编排与组合指南
├── AGENTS.md                         # 🤝 项目规范和协作约定
├── CLAUDE.md                         # 🤖 Claude Code 上下文说明
│
├── skills/                           # 🧰 Skills 集合
│   ├── skill-template/               # 🌀 Skill 开发起点模板
│   │   ├── SKILL.md                 # Skill 定义（必填）
│   │   ├── references/              # 参考文档（按需加载）
│   │   ├── scripts/                 # 可执行脚本
│   │   └── assets/                  # 静态资源
│   └── find-skill/                   # 🔍 搜索外部现成方案
│
├── references/                        # 📂 参考资料
│   ├── SKILL-ANATOMY.md             # Skill 内部结构详解
│   ├── FIND-SKILL-GUIDE.md          # 新手搜索指南
│   └── OFFICIAL-DOCS.md             # 官方文档索引
│
├── concepts/                         # 💡 核心概念
│   ├── WHAT-IS-SKILL.md            # 什么是 Skill？
│   ├── WHAT-IS-VIBE-CODING.md      # 什么是 Vibe Coding？
│   └── WHAT-IS-GITHUB.md            # GitHub 协作入门
│
└── github-guide/                     # 🛠️ GitHub 协作指南
    ├── SETUP.md                     # 仓库配置
    ├── BRANCH-PR.md                  # 分支与 PR 管理
    ├── CLONE-PUSH.md                 # 克隆与推送
    └── CHEATSHEET.md                 # 常用命令速查
```

---

## 📖 资源导航

| 你想做什么 | 去哪里 |
|-----------|--------|
| 完整的开发规范 | `SKILL-DEV-GUIDE.md` |
| 多个 Skill 怎么组合 | `SKILL-ORCHESTRATION-GUIDE.md` |
| 从零创建一个新 Skill | `skills/skill-template/SKILL.md` |
| 找现成的 Skill 方案 | `skills/find-skill/SKILL.md` |
| 理解 Skill 核心概念 | `concepts/WHAT-IS-SKILL.md` |
| GitHub 协作流程 | `github-guide/BRANCH-PR.md` |

---

## 🔧 推荐工具

- **[ClawHub](https://clawhub.com)** — Skill 市场，找现成方案
- **[OpenClaw](https://openclaw.ai)** — 开源 AI 助手框架
- **[Claude Code](https://claude.com/code)** — AI 编程助手

---

## 🤝 一起完善

发现 bug 或有好的想法？欢迎提交 Issue 和 Pull Request！

---

**基于 [legal-skills](https://github.com/cat-xierluo/legal-skills) 规范模板构建**
