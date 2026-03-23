# Skill 开发官方指南（完整版）

> 本文档翻译自 Claude Code 官方 plugin-dev 的 skill-development skill，是 Skill 开发的权威参考文档。

---

## 什么是 Skill？

Skill 是模块化、自包含的包，通过提供专业知识、工作流程和工具来扩展 AI 的能力。

把它们想象成特定领域的"入门指南"——它们把通用 AI 变成配备专业流程知识的专精 AI。

### Skill 能提供什么？

1. **专业工作流** - 特定领域的多步骤流程
2. **工具集成** - 特定文件格式或 API 的操作说明
3. **领域知识** - 公司专属知识、模式、业务逻辑
4. **打包资源** - 复杂重复任务的脚本、参考资料和资产

---

## Skill 的结构

每个 Skill 由必需的 `SKILL.md` 文件和可选的打包资源组成：

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter 元数据 (必需)
│   │   ├── name: (必需)
│   │   └── description: (必需)
│   └── Markdown 指令 (必需)
│
└── 打包资源 (可选)
    ├── scripts/       - 可执行代码 (Python/Bash 等)
    ├── references/  - 按需加载的参考资料
    └── assets/      - 输出中使用的文件
```

### SKILL.md（必需）

**元数据质量**：`name` 和 `description` 决定 AI 何时使用该 Skill。

**描述格式**：使用第三人称（如 "This skill should be used when..." 而不是 "Use this skill when..."）

---

## 渐进式披露设计原则

Skill 使用三级加载系统来高效管理上下文：

| 层级 | 内容 | 加载时机 |
|------|------|----------|
| **元数据** | name + description | 始终加载（约100词） |
| **SKILL.md 主体** | 核心指令 | Skill 触发时（<5k词） |
| **打包资源** | references/examples/scripts | 按需加载（无限*） |

*无限，因为脚本可以不加载到上下文直接执行

---

## Skill 创建流程

### 第一步：理解 Skill 的具体示例

理解 Skill 将如何使用的具体示例。可以通过用户直接提供或生成的经验证示例来获得理解。

**示例问题**：
- "这个 Skill 应该支持什么功能？"
- "能否举例说明这个 Skill 将如何使用？"
- "我想象用户会说'xxx'或'yyy'，还有其他用法吗？"

### 第二步：规划可复用 Skill 内容

将具体示例转化为有效 Skill，分析每个示例：

1. 考虑如何从头执行这个示例
2. 识别哪些脚本、参考资料、资产在重复执行这些工作流时会很有帮助

**示例分析**：
- 构建 `pdf-editor` Skill → 需要 `scripts/rotate_pdf.py`
- 构建 `frontend-webapp-builder` Skill → 需要 `assets/hello-world/` 模板
- 构建 `big-query` Skill → 需要 `references/schema.md` 模式文档

### 第三步：创建 Skill 结构

```bash
mkdir -p skill-name/{references,examples,scripts}
touch skill-name/SKILL.md
```

### 第四步：编写 Skill

#### 开始前：明确可复用 Skill 内容

从 `scripts/`、`references/`、`assets/` 开始实现。

#### SKILL.md 编写要点

**书写风格**：使用**祈使语/不定式**（动词开头的指令），不用第二人称。

```markdown
# 正确（祈使语）
要旋转 PDF，先读取文件。
配置 MCP 服务器需要认证信息。
使用前验证设置。

# 错误（第二人称）
你应该先读取配置文件。
你需要配置 MCP 服务器。
你可以使用 grep 工具搜索。
```

**Frontmatter 描述**：使用第三人称，包含具体触发短语：

```yaml
---
name: skill-name
description: |
  This skill should be used when the user asks to "create X",
  "configure Y", "add Z". Include exact phrases users would say.
version: 0.1.0
---
```

**好的描述示例**：
```yaml
description: |
  This skill should be used when the user asks to "create a hook",
  "add a PreToolUse hook", "validate tool use", or mentions hook events.
```

**保持 SKILL.md 精简**：目标 1,500-2,000 词，详细内容移到 references/

```markdown
## 其他资源

### 参考文件

详细模式和技巧见：
- **`references/patterns.md`** - 常见模式
- **`references/advanced.md`** - 高级用法

### 示例文件

`examples/` 中的工作示例：
- **`example-script.sh`** - 工作示例
```

### 第五步：验证和测试

**验证清单**：
- [ ] SKILL.md 存在且有有效 YAML frontmatter
- [ ] frontmatter 有 `name` 和 `description` 字段
- [ ] 包含具体触发短语
- [ ] 使用祈使语书写
- [ ] 内容精简（1,500-2,000 词）
- [ ] 引用的文件都存在
- [ ] 示例完整可运行
- [ ] 脚本可执行

### 第六步：迭代

**迭代工作流**：
1. 在实际任务中使用 Skill
2. 发现困难或低效之处
3. 识别 SKILL.md 或打包资源应如何改进
4. 实现更改并再次测试

**常见改进**：
- 加强 description 中的触发短语
- 将长段落从 SKILL.md 移到 references/
- 添加缺失的示例或脚本
- 澄清模糊指令
- 添加边界情况处理

---

## 常见错误

### 错误 1：弱触发描述

❌ **错误**：
```yaml
description: Provides guidance for working with hooks.
```

✅ **正确**：
```yaml
description: |
  This skill should be used when the user asks to "create a hook",
  "add a PreToolUse hook", "validate tool use", or mentions hook events.
```

### 错误 2：把所有内容都放在 SKILL.md

❌ **错误**：
```
skill-name/
└── SKILL.md  (8,000 词 - 全在一个文件)
```

✅ **正确**：
```
skill-name/
├── SKILL.md  (1,800 词 - 核心内容)
└── references/
    ├── patterns.md (2,500 词)
    └── advanced.md (3,700 词)
```

### 错误 3：第二人称书写

❌ **错误**：
```markdown
You should start by reading the configuration file.
You need to validate the input.
```

✅ **正确**：
```markdown
Start by reading the configuration file.
Validate the input before processing.
```

---

## 快速参考

### 最小 Skill

```
skill-name/
└── SKILL.md
```

适合：简单知识，不需要复杂资源

### 标准 Skill（推荐）

```
skill-name/
├── SKILL.md
├── references/
│   └── detailed-guide.md
└── examples/
    └── working-example.sh
```

适合：大多数需要详细文档的 Plugin Skill

### 完整 Skill

```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── advanced.md
├── examples/
│   ├── example1.sh
│   └── example2.json
└── scripts/
    └── validate.sh
```

适合：复杂领域，需要验证工具

---

## 最佳实践总结

| 应该 | 不应该 |
|------|--------|
| description 使用第三人称 | 使用第二人称 |
| 包含具体触发短语 | 触发条件模糊 |
| SKILL.md 保持精简（1,500-2,000词） | 所有内容放 SKILL.md（>3,000词） |
| 使用渐进式披露（详细内容移到 references/） | - |
| 使用祈使语书写 | - |
| 清晰引用支持文件 | 资源未引用 |
| 提供可运行的示例 | 包含破损或不完整的示例 |
| 创建常用操作的工具脚本 | - |

---

*翻译整理自 [GitHub - Claude Code plugin-dev skill-development](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev/skills/skill-development)*
