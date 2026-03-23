# Find Skill 新手指南

> 如何在开发新功能前找到现成方案

---

## 为什么要先搜索？

**重复造轮子是最常见的效率杀手。**

在你决定花时间开发一个新功能前，先问自己：这件事有没有人已经做过了？

- 搜索只需要 1 分钟
- 开发可能需要 10 小时
- **用现成方案省下的时间，可以花在真正独特的事情上**

---

## 在哪里搜索？

### 1. Skills.sh（主战场）

**地址：** https://skills.sh/

这是 Vercel 维护的 Skill 市场，汇聚了大量社区贡献的 Skill。
每个 Skill 都有安装量、来源仓库和功能说明。

**安装量 > 10K 的 Skill，基本经过了社区验证。**

### 2. Vercel Skills CLI（命令行）

```bash
# 安装 Skills CLI（内置在 Node.js 环境）
npx skills find [关键词]

# 安装 Skill
npx skills add <owner/repo@skill> -g -y
```

适合在开发过程中快速搜索。

### 3. GitHub

直接搜 Claude Code / OpenClaw / Agent 相关的仓库：
- `site:github.com claude code skill`
- `site:github.com openclaw skill`
- `awesome-claude-skills`

### 4. Claude Code 官方插件

https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev

官方出品的 Skill 模板和开发规范，最权威的参考。

---

## 搜索流程

```
用户提出需求
     │
     ▼
┌─────────────────────────────────┐
│ 第一步：理解需求                   │
│  · 领域是什么？                   │
│  · 具体任务是什么？                │
│  · 这个任务常见吗？                │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│ 第二步：查 Skills.sh Leaderboard │
│  https://skills.sh/             │
│  看该领域是否有知名 Skill         │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│ 第三步：CLI 搜索                 │
│  npx skills find [关键词]        │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│ 第四步：验证质量                  │
│  · 安装量 > 1K？                 │
│  · 来源可靠（vercel/anthropics）？│
│  · GitHub Stars > 100？          │
└─────────────┬───────────────────┘
              │
              ▼
      ┌───────┴───────┐
      │               │
   找到合适方案        找不到
      │               │
      ▼               ▼
  推荐给用户        告知用户 + 
                   直接帮忙做
```

---

## 搜索技巧

### 关键词要具体

| ❌ 不好 | ✅ 好 |
|--------|------|
| `testing` | `react testing` |
| `deploy` | `vercel deploy` |
| `docs` | `api-docs generator` |

### 同义词替换

搜索不到时，换个说法：
- `deploy` → `deployment` / `ci-cd` / `pipeline`
- `design` → `ui` / `ux` / `design-system`
- `review` → `pr-review` / `code-review`

### 看来源

| 来源 | 可靠性 |
|------|--------|
| `vercel-labs/agent-skills` | ⭐⭐⭐⭐⭐ 官方维护 |
| `anthropics/skills` | ⭐⭐⭐⭐⭐ 官方出品 |
| `microsoft/` | ⭐⭐⭐⭐ 大厂出品 |
| 个人仓库 | ⭐⭐ 谨慎对待 |

### 看安装量

| 安装量 | 建议 |
|--------|------|
| 100K+ | 🟢 强烈推荐，经过大量验证 |
| 10K - 100K | 🟢 靠谱，可以放心用 |
| 1K - 10K | 🟡 可以用，但要做尽职调查 |
| < 1K | 🔴 谨慎，可能不成熟 |
| < 100 | 🔴 不推荐，风险太高 |

---

## 搜不到时怎么办

**不代表这件事做不了，只代表没有现成包。**

1. **我可以直接帮你做** — 用现有能力完成任务
2. **你可以自己创建 Skill** — `npx skills init` 快速起步
3. **参考官方模板** — 看看 `skills/skill-template/` 怎么写

---

## 常见问题

**Q: Skills CLI 在哪安装？**
A: 不需要单独安装。`npx skills` 会自动拉取最新版本（需要 Node.js 环境）。

**Q: 安装的 Skill 放在哪里？**
A: 全局安装（`-g`）在用户目录，`npx skills list` 可以看到路径。

**Q: 搜到的 Skill 装了很多，有冲突怎么办？**
A: `npx skills check` 检查版本，`npx skills update` 更新到最新。

**Q: 我自己开发的 Skill 能发布吗？**
A: 可以。参考 [SKILL-DEV-GUIDE.md](../SKILL-DEV-GUIDE.md)，发布到 GitHub 后通过 `npx skills add` 安装。

---

## 下一步

- 搜索到一个合适的 Skill？→ 看它的 SKILL.md 了解如何使用
- 决定自己开发？→ 阅读 [SKILL-DEV-GUIDE.md](../SKILL-DEV-GUIDE.md)
- 基于模板快速开始？→ 参考 [skills/skill-template/](skills/skill-template/SKILL.md)
