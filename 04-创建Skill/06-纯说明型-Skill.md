# 06 纯说明型 Skill

上一篇 [03 基于模板创建](./03-基于模板创建.md) 给了从模板复制出 Skill 的最短路径。但模板默认带 `scripts/`、`assets/`，容易让人以为「一个 Skill 必须有脚本」。其实最常见的 Skill 形态恰恰相反——**只有说明书，没有脚本**。这篇讲清这种最简形态：什么时候该用它、`SKILL.md` 怎么写、`references/` 怎么组织、没有脚本时触发质量靠什么保证。我们用一个真实小例子「团队 commit 规范说明卡」贯穿。

## 本篇目标

读完这篇，你能：

- 说清「纯说明型 Skill」是什么，并判断一个需求该不该用这种形态；
- 写出一个合格的纯说明型 `SKILL.md`：精简正文 + 按需加载的 `references/`；
- 把一整份规范合理地拆进 `references/`，而不是全塞进 `SKILL.md`；
- 解释为什么纯说明型 Skill 的触发质量**完全**取决于 `description`，并按清单把它写到位。

命令以 macOS / Linux 为主；本篇几乎不涉及命令行操作，Windows 读者照抄文件内容即可。

## 前置知识

- [一个 Skill 是怎样工作的？](../01-概念入门/06-一个-Skill-是怎样工作的.md)：知道 Skill 是文件夹，由 `SKILL.md`、`scripts/`、`references/`、`assets/` 组成，以及「发现 → 触发 → 加载 → 执行 → 输出」的流程。本篇反复用到其中两个概念——**frontmatter**（`SKILL.md` 开头被 `---` 包起来的、给 AI 读的元信息）和**按需加载**（`references/` 平时不读，用到才读）。
- [03 基于模板创建](./03-基于模板创建.md)：知道怎么从 `skills/skill-template/` 复制出一个新 Skill、怎么命名。
- [04 提交到 GitHub 与 Commit 规范](../02-工具指南/04-提交到-GitHub-与-Commit-规范.md)：本篇例子「团队 commit 规范说明卡」打包的就是这类规范，读过更好懂背景。

## 核心概念：纯说明型 Skill 是什么，什么时候选它

### 三种形态，先定位

创建 Skill 时，按「要不要执行代码」分成三个层级（编号 06/07/08 对应这三层）：

| 层级 | 形态 | 会什么 | 本文 / 编号 |
|------|------|--------|-------------|
| 第一层 | **纯说明型**：只有 `SKILL.md`（+ 可选 `references/`），无 `scripts/` | 只会「说」——把知识/规范/流程教给 AI | 本篇 06 |
| 第二层 | **带脚本型**：`SKILL.md` + `scripts/` | 还会「做」——读写文件、跑命令、算结果 | [07 带脚本 Skill](./07-带脚本-Skill.md) |
| 第三层 | **多 Skill 编排**：多个 Skill 串成一条流程 | 把多个「会说/会做」的 Skill 组合起来 | [08 多 Skill 编排](./08-多Skill编排.md) |

判断该用哪一层，只问一个问题：**这个任务，AI 光靠「想」能完成吗？**

- 能——任务本质是把一套知识或规范交给 AI，让它照着做（写提交信息按团队格式、把需求按模板拆解、回答 FAQ）。→ 纯说明型。
- 不能——必须读文件、跑命令、算结果。→ 带脚本型（见 07）。
- 要把好几步串起来，每步可能调用不同 Skill。→ 编排（见 [08 多 Skill 编排](./08-多Skill编排.md)）。

> 一条经验：拿不准时，**先做纯说明型**。能用知识解决的，别急着写脚本；脚本意味着依赖、跨平台、退出码契约（见 07），维护成本立刻上来。纯说明型只有一个文件要维护，出错面最小。

### 「执行」靠的是 description 和正文质量

纯说明型没有 `scripts/`，所以它**全部的价值都在文字里**：`description` 决定它会不会被启用，`SKILL.md` 正文决定启用后 AI 做得对不对。这带来一个直接推论：**触发质量是纯说明型的命根子**——带脚本型至少还有脚本能兜底「做」这件事，纯说明型如果没被触发，就什么都没有。所以本篇把「触发怎么保证」单独拿出来讲（见下方专节）。

## 实例分析：仓库里的纯说明型 Skill 长什么样

讲概念前，先看一个真实样本。仓库里的 `skills/find-skills/` 就是一个纯说明型 Skill——帮你发现和安装其它 Skill。打开它的目录（来源事实见 [`docs/SOURCE-INDEX.md`](../docs/SOURCE-INDEX.md)）：

```text
find-skills/
└── SKILL.md        # 只有这一个文件
```

没有 `scripts/`、没有 `assets/`、没有 `references/`——连子目录都没有。它的工作全写在 `SKILL.md` 里：什么情况下用它、安装 Skill 的标准步骤、每一步该敲什么命令。AI 读到这份说明书，就「会」了帮你找 Skill 这件事。这是纯说明型的**最简形态**：单文件，零依赖，审查也最快（见 [05 第三方 Skill 安全审查](./05-第三方-Skill-安全审查.md) 里对它的审查）。

当 `SKILL.md` 写不下时，才需要第二个零件——`references/`。于是从「单文件」升级到「`SKILL.md` + `references/`」，这就是下面要动手做的形态。

## 动手步骤：创建「团队 commit 规范说明卡」

下面用一个真实需求把纯说明型的完整创建走一遍。需求：团队每次提交代码，commit message 都要按 Conventional Commits（一种提交信息书写约定，形如 `feat: 新增导出功能`）写，但 AI 默认不知道**你们团队**的具体约定（用哪些类型前缀、scope 怎么填、breaking change 怎么标）。把它做成一个 Skill，AI 写提交信息时就会自动照办。

这个任务 AI 光靠「想」就能完成（输出一段符合规范的文字），不需要读写文件、不需要算——典型的纯说明型。

### 第 1 步：从模板复制，删掉用不上的部分

```bash
cp -r skills/skill-template skills/commit-style
cd skills/commit-style
```

复制完，删掉本次用不到的：`scripts/`、`assets/`、`.env.example`、`assets/config.yaml.example`（模板里 `assets/` 整个目录都可删）。剩下的核心是 `SKILL.md`，再加一个 `references/`。最终目录：

```text
commit-style/
├── SKILL.md
├── LICENSE.txt   # 需自行新增（模板不预选许可证）
├── CHANGELOG.md
├── ROADMAP.md
├── TASKS.md
├── DECISIONS.md
└── references/
    └── commit-format.md
```

协作文档（`CHANGELOG.md` 等）保留——纯说明型也是要长期维护的 Skill，谁改过说明书、为什么改，照样得记。

### 第 2 步：写 frontmatter——这是触发的命根子

打开 `SKILL.md`，先写开头这段被 `---` 包起来的 frontmatter。**把 `description` 当成唯一入口来写**，覆盖三件事：正向触发（什么时候用）、负向触发（什么时候不用）、多种问法。

```markdown
---
name: commit-style
description: |
  本技能应在用户要写或修改 Git 提交信息（commit message）、
  说「帮我提交」「生成 commit」「写个提交信息」时使用。
  按团队 Conventional Commits 约定给出 message，并提醒附上 scope。
  不要用于：写代码、做代码审查、写 PR 描述、普通聊天。
---
```

注意三点：`name` 与目录名 `commit-style` 完全一致（发现和加载都依赖这个对应，不一致会找不到）；`description` 同时写了正向和负向触发；列举了「帮我提交 / 生成 commit / 写个提交信息」几种真实问法，提高命中率。关于为什么这样写，见下方「触发怎么保证」专节。

### 第 3 步：写正文——只放最常用的 20%

正文不要把整份规范抄进来。只放 AI 每次都会用到的核心规则——类型前缀清单和一个例子，其余指向 `references/`：

```markdown
# commit-style

写 Git 提交信息时，按团队约定生成 message。

## 类型前缀（最常用）

- feat：新增功能
- fix：修复缺陷
- docs：仅文档
- refactor：重构（不改功能、不改缺陷）
- chore：构建/依赖/杂项

完整格式（scope、breaking change footer、多行 body、每类的反例）
见 references/commit-format.md，需要时再读。

## 一个例子

feat(auth): 支持邮箱登录
```

这条「正文精简、细节进 `references/`」的边界，是纯说明型能不能轻快跑起来的关键——原因见下一步。

### 第 4 步：把细节拆进 references/

把完整规范写进 `references/commit-format.md`：scope 的取值范围、breaking change 怎么用 `BREAKING CHANGE:` footer 标注、多行 body 的空行要求、每种类型的好例子和反例。内容可以详细，不用省。

关键在于**理解 `references/` 的加载方式**：发现阶段 AI 只读 frontmatter；触发后只加载 `SKILL.md` 正文；`references/commit-format.md` **平时根本不读**，只有当 `SKILL.md` 正文里写了「见 references/commit-format.md」**并且这次真的需要那段细节**时，才会被加载进来。

这条机制解释了第 3 步为什么要克制：

- 全塞进 `SKILL.md` → 每次触发都把一整份规范加载进上下文，慢、占地方，AI 还容易被长文带偏。
- 拆进 `references/` → 平时只加载精简正文；偶尔遇到复杂情况（要写 breaking change），才把那一段细节拉进来。

> 一句话记住分工：`SKILL.md` 是「总是要看的摘要」，`references/` 是「偶尔才查的厚手册」。摘要越精简，厚手册越能放得下细节。

### 第 5 步：本地走查

纯说明型没有脚本能 `python3 scripts/main.py` 跑一下，验证方式换成「脑内走查 + 实测触发」：

1. 通读 `SKILL.md`，确认没有依赖任何 `scripts/`（一删脚本就该跟着删掉正文里所有「运行 xxx」的指示）。
2. 拿一句真实需求（「帮我把这次改动提交」）在心里走一遍：这句话能不能命中 `description`？命中后正文给的步骤够不够写出一条合规 message？
3. 想确认真实触发效果，就把 Skill 装到测试项目里试一次（安装与试用见 [05 第三方 Skill 安全审查](./05-第三方-Skill-安全审查.md) 的「项目级试用」）。

## 触发怎么保证（纯说明型的命根子）

纯说明型没有脚本兜底，**触发准不准几乎等于这个 Skill 有没有用**。把 `description` 按下面四条写到位：

1. **正向触发要具体到动作**。写「用户要写 commit message 时」，而不是「用于 Git」。越具体，越不容易和别的 Git 类 Skill 抢着触发。
2. **负向触发划清边界**。明确写「不要用于写代码、做代码审查、写 PR 描述」，避免它在不该说话时插嘴。
3. **覆盖多种问法**。用户不会说「请触发 commit-style Skill」，只会说「帮我提交」「写个 commit」「生成提交信息」。把几种真实说法列进 `description`，命中率明显提高。
4. **别写得太宽**。「用于开发相关任务」这种描述会让它到处乱触发——该用的时候用不上，不该用的时候瞎插嘴。

更系统的触发质量评估（正例/负例/边界/基线）见 [09 触发质量与 eval](./09-触发质量与eval.md)；本篇给的是写 `description` 时就能立刻自查的四条底线。

## 常见错误

### description 写成「一个有用的 Skill」

把 `description` 写成「用于提交相关任务」。结果该触发时不触发，或跟其它 Git 类 Skill 一起抢着触发。正确做法：写清正向触发、负向触发，并列出几种真实问法。

### 把整份规范全塞进 SKILL.md

规范越长，`SKILL.md` 加载越慢、越占上下文，AI 还容易被长文带偏重点。正确做法：正文只放最常用的核心规则，细节拆进 `references/`，靠按需加载。

### 以为 references/ 放进去就自动生效

不会。`references/` 是按需加载的，只有 `SKILL.md` 正文指明「见 references/xxx」**且这次真的用到**时才被读。放进去了却没在正文引导，等于没放。

### 删了 scripts/ 却没删正文里的「运行 xxx」

从模板复制后删掉 `scripts/`，但 `SKILL.md` 正文里还留着「运行 scripts/main.py 生成结果」之类指示。AI 照做就会去调一个不存在的脚本。正确做法：删脚本的同时，把正文里所有依赖该脚本的步骤一起清掉。

### name 和目录名不一致

发现和加载都靠 `name` 与目录名对应。`name: commit-style` 配目录 `commit-style/` 才行；写成 `commit_style` 或 `commitstyle` 会导致找不到或加载错。

### 误以为「纯说明型 = 简单 = 不用认真」

形态简单，不等于可以糊弄 `description`。恰恰相反——纯说明型的全部价值都在文字里，触发写歪了就等于没有这个 Skill。越是纯说明型，越要在 `description` 和正文质量上下功夫。

## 自测题 / 验收

1. 只看「三种形态」那张表，说清纯说明型、带脚本型、编排各自「会什么」，以及判断该用哪一层的那个问题是什么。
2. 拿你自己团队的一条规范（代码风格、命名约定、PR 模板都行），判断它该不该做成纯说明型——给出判断依据。
3. `references/commit-format.md` 在什么条件下才会被加载进上下文？为什么不能指望「放进去就生效」？
4. 给你的纯说明型 Skill 写一段 `description`，要同时包含正向触发、负向触发和至少两种真实问法。
5. 删掉 `scripts/` 之后，`SKILL.md` 正文里最容易漏删的是什么？

第 4 题能写出一段你自己敢用的 `description`，说明触发这块你已经过关了。

## 下一篇

本篇讲的是「只会说」的最简形态。当任务需要 AI 真正去「做」——读写文件、跑命令、算结果——就要给 Skill 配脚本：

- **下一篇（主线）**：[07 带脚本 Skill](./07-带脚本-Skill.md)——怎么写脚本、约定退出码和输入输出契约、处理依赖、用 `assets/`。
- 想看真实纯说明型样本的结构：[find-skills 的 SKILL.md](../skills/find-skills/SKILL.md)（仓库内）。
- 触发质量想做得更系统：[09 触发质量与 eval](./09-触发质量与eval.md)。
- 做完要发布：[04 调试与发布](./04-调试与发布.md)。

---

**收尾给一个动作**：挑一条你团队里「每次都要口头提醒 AI」的规范，花十分钟把它做成一个纯说明型 Skill——一个 `SKILL.md` 加一个 `references/` 就够了。做完你会发现，以后那句提醒再也不用说了。
