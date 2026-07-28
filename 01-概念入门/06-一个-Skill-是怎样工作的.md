# 一个 Skill 是怎样工作的？

## 本篇目标

读完这篇，你能说清楚：

- 一个 Skill 由哪些文件组成，每个文件干什么；
- 从「你说了一句话」到「AI 给出结果」，Skill 内部经历了哪几步；
- 哪一步最常出问题，以及失败时是什么样子。

上一篇我们讲了 Skill 和工具、MCP、Plugin、Workflow 的关系。这篇钻进 Skill 内部，看它从「被发现」到「出结果」的全过程。先从 [什么是 Skill？](./01-什么是-Skill.md) 的「App 类比」接着往下。

## 前置知识

- [什么是 Skill？](./01-什么是-Skill.md)：知道 Skill 是给 AI 装的 App。
- [工具、Skill、MCP、Plugin、Workflow 到底什么关系？](./05-工具-Skill-MCP-Plugin-Workflow-关系.md)：知道 Skill 在整套体系里的位置。

## 核心概念：一个 Skill 长什么样

Skill 不是单单一句话或一段提示词，它是一个**文件夹**。我们拿仓库里真实存在的模板 `skills/skill-template/` 来看：

```text
skill-template/
├── SKILL.md                 # 说明书：这个 Skill 是什么、什么时候用、怎么做
├── scripts/
│   └── main.py              # 可执行脚本：干「动手」的活
├── references/
│   └── README.md            # 详细参考资料：平时不读，用到才读
└── assets/
    ├── config.yaml.example  # 配置模板
    └── requirements.txt     # 依赖清单
```

四个核心部分，各司其职：

### 1. SKILL.md：说明书（最重要）

SKILL.md 是 Skill 的「身份证 + 说明书」。它最关键的是开头一段 frontmatter：

```yaml
---
name: skill-template
description: |
  Skill 开发起点模板。本技能应在用户需要新建一个 Skill……时使用。
  不要用于：直接替代具体业务 Skill……
---
```

这里有两件事决定 Skill 的「命运」：

- **name**：这个 Skill 叫什么（英文、小写、和目录名一致）。
- **description**：什么时候该用它。AI 就是靠这句话判断「现在这个需求，要不要启用这个 Skill」。

> description 是 Skill 能否被正确触发的命根子。写得太模糊，该用的时候用不上；写得太宽，不该用的时候乱插嘴。

SKILL.md 正文则是「说明书」：先做什么、再做什么、遇到情况怎么办。它要保持精简，详细内容拆到 references/。

### 2. scripts/：干活的脚本

有些事光靠「想」不够，得真动手：读文件、跑命令、生成结果。这些「动手」的活交给 scripts/ 里的脚本。

比如 `scripts/main.py` 可以被 AI 调用来执行一个具体动作，并把结果返回。脚本让 Skill 不只是「会说」，还能「会做」。

### 3. references/：按需读取的详细资料

不是所有内容都要塞进 SKILL.md。太长的说明、复杂的规则、参考资料，放进 references/。

关键是「按需」：平时这些文件不会被读进上下文，**只有 SKILL.md 正文里明确说「详细规则见 references/xxx」并且真的用到时，才会被加载**。这样既保留了大量知识，又不让大脑被无关内容塞满。

### 4. assets/：模板和静态资源

配置模板（如 `config.yaml.example`）、依赖清单（如 `requirements.txt`）、示例数据、模板文件，放在 assets/。它们是「原材料」，Skill 运行时按需取用。

一句话记住分工：

| 部分 | 角色 | 类比 |
|------|------|------|
| SKILL.md | 说明书 + 身份证 | 产品使用手册 + 名片 |
| scripts/ | 干活的程序 | 工具箱里的电动工具 |
| references/ | 详细资料（按需读） | 备查的厚手册 |
| assets/ | 模板和原材料 | 备用零件和原料 |

## 动手步骤：一次完整的执行流程

知道了结构，再看 Skill 怎么「跑起来」。从你说一句话，到 AI 给出结果，中间有 6 步。

### 第 1 步：发现（Discovery）

Agent 启动时，会在约定的 skills 目录里扫描，把每个 Skill 文件夹读一遍——但**只读 SKILL.md 的 frontmatter（name 和 description）**，不读正文。

> 为什么只读 frontmatter？因为如果每次都把所有 Skill 的全文塞进来，大脑会被撑爆。所以先只看「名片」，需要时再翻「说明书」。

### 第 2 步：触发（Trigger）

你输入一句话。Agent 拿这句话，和所有 Skill 的 description 比对，判断「这个需求该用哪个 Skill」。

- description 写得准 → 命中率高；
- description 写得模糊 → 要么用不上，要么乱触发。

这就是为什么 description 要写「正向触发（什么时候用）」和「负向触发（什么时候不用）」。

### 第 3 步：加载（Load）

决定用某个 Skill 后，Agent 把它的 **SKILL.md 正文**加载进上下文。这一刻，「说明书」才被翻开。

注意：到这一步，references/ 和 scripts/ 通常**还没被读取**。它们是「按需加载」的，SKILL.md 正文说到要用时才会读。

### 第 4 步：执行（Execute）

Agent 按 SKILL.md 里的步骤做事。需要算的时候自己算；需要「动手」时，调用 scripts/ 里的脚本，或调用其它工具。

比如 SKILL.md 写「生成结果文件」，Agent 就会运行 `scripts/main.py`，把产出写到 `output/`。

### 第 5 步：输出（Output）

执行完，Skill 把结果交出来：可能是一段文字、一个文件、一次操作。这就是你最终看到的东西。

### 第 6 步：失败边界（Failure boundary）

不是每次都顺利。失败可能发生在好几处：

| 出问题的环节 | 表现 | 通常原因 |
|--------------|------|----------|
| 触发 | 该用没用 / 不该用却用了 | description 写得模糊或太宽 |
| 加载 | 正文读不进来或读错版本 | SKILL.md 格式错误、frontmatter 写错 |
| 执行 | 脚本报错、缺依赖 | scripts/ 脚本失败、缺依赖、权限不足 |
| 输出 | 结果对不上预期 | 步骤写错、输出格式没约定 |

失败时的关键信号是**退出码**：脚本正常跑完返回 0，出错返回非 0。Agent 靠这个判断「这一步到底成没成」。所以写脚本时，出错要让退出码 ≠ 0，并打印清楚错误原因，别让失败「悄悄发生」。

> 一句话流程：发现 → 触发 → 加载 → 执行 → 输出，外加一条「失败边界」兜底。

## 常见错误

### 错误 1：description 随便写

把 description 写成「一个有用的技能」。结果该触发时不触发，不该触发时乱来。正确做法：写清正向和负向触发，覆盖多种问法。

### 错误 2：把所有内容塞进 SKILL.md

SKILL.md 越长，加载越慢、越占上下文。正确做法：正文保持精简，详细内容拆到 references/，按需读取。

### 错误 3：脚本失败却返回成功

脚本出错但退出码是 0，Agent 会以为成功了，给出错误结果。正确做法：出错时退出码 ≠ 0，并打印错误原因。

### 错误 4：以为 references/ 会被自动全读

不会。references/ 是按需读取的，只有 SKILL.md 正文指明、且真的用到时才加载。指望「放进去就生效」是误区。

### 错误 5：name 和目录名不一致

发现和加载都依赖 name 与目录名对应。不一致会导致找不到、加载错。

## 自测题 / 验收

1. 一个 Skill 文件夹里，哪四个部分最核心？各自干什么？
2. 发现阶段，Agent 读的是 SKILL.md 的哪一部分？为什么不读全文？
3. 从「你说一句话」到「出结果」，完整列出 6 步。
4. description 写得太模糊，会在哪一步出问题？
5. 脚本出错时，为什么必须让退出码 ≠ 0？

如果第 3 题你能不看文章背出来，说明执行流程你已经掌握了。

## 下一篇

这篇讲的是 Skill 内部怎么跑。接下来可以：

- 看真实 Skill 的结构解剖：[Skill 解剖课：认识一个 Skill 的组成](../05-参考资料/02-Skill-结构解剖.md)
- 想动手写一个：[Skill 开发总指南](../04-创建Skill/SKILL-DEV-GUIDE.md)
- 回顾概念关系：[工具、Skill、MCP、Plugin、Workflow 到底什么关系？](./05-工具-Skill-MCP-Plugin-Workflow-关系.md)

---

**一句话理解**：Skill 是一个文件夹——SKILL.md 是说明书兼身份证，scripts/ 干活，references/ 存详细资料按需读，assets/ 放模板原料。它的工作流程是「发现 → 触发 → 加载 → 执行 → 输出」，再用「失败边界」兜底。写好 description、保持 SKILL.md 精简、让脚本诚实报错，是 Skill 能稳定跑起来的三条命根子。
