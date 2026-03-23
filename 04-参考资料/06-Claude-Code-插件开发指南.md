# Claude Code 插件开发官方指南

> 本文档翻译自 [anthropics/claude-code](https://github.com/anthropics/claude-code) 的 plugin-dev 插件开发工具包。

---

## 概述

插件开发工具包提供了 7 个专业技能，帮助你构建高质量的 Claude Code 插件：

1. **Hook 开发** - 高级 Hooks API 和事件驱动自动化
2. **MCP 集成** - Model Context Protocol 服务器集成
3. **插件结构** - 插件组织和 manifest 配置
4. **插件设置** - 使用 .claude/plugin-name.local.md 文件的配置模式
5. **命令开发** - 创建带 frontmatter 和参数的斜杠命令
6. **Agent 开发** - 创建具有 AI 辅助生成的自主代理
7. **Skill 开发** - 使用渐进式披露和强触发器的 Skill 创建

---

## 插件结构

### 标准目录结构

```
plugin-name/
├── plugin.json              # 插件清单（必需）
├── README.md                # 插件说明
├── skills/                  # 技能目录
│   └── my-skill/
│       └── SKILL.md
├── commands/                # 命令目录
│   └── my-command.md
├── agents/                  # Agent 目录
│   └── my-agent.md
├── hooks/                   # Hook 脚本目录
│   └── my-hook.sh
└── references/              # 参考文档目录
    └── overview.md
```

### plugin.json manifest

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "插件描述",
  "authors": ["Name <email>"],
  "homepage": "https://github.com/..."
}
```

---

## Skill 开发

### SKILL.md 结构

每个 Skill 由 `SKILL.md`（必需）和其他资源组成：

```
skill-name/
├── SKILL.md              # 必需：Skill 定义和触发条件
├── references/           # 可选：详细参考资料
├── examples/             # 可选：示例
└── scripts/             # 可选：可执行脚本
```

### Frontmatter（必需）

```yaml
---
name: skill-name
description: |
  Skill 的描述，说明何时触发。
  包含具体的触发短语。
  用第三人称书写。
---
```

### description 编写要点

1. **包含具体触发短语**：列出用户可能说的关键句子
2. **明确边界**：说明能做什么、不能做什么
3. **简洁**：description 不是详细文档，只是触发条件

### 渐进式披露原则

| 层级 | 内容 | 说明 |
|------|------|------|
| **元数据** | name + description | AI 判断何时触发 |
| **核心文档** | SKILL.md 主体 | AI 执行任务时的指导 |
| **详细资源** | references/ | 按需加载的参考资料 |

### 触发短语示例

```yaml
description: |
  创建和编辑 Skill。适用于以下场景：
  - "创建一个新的 Skill"
  - "写一个 Skill"
  - "改进这个 Skill"
  - "审核 Skill"
```

---

## 命令开发

### 命令结构

命令是一个带有 YAML frontmatter 的 Markdown 文件：

```yaml
---
name: command-name
description: 命令描述
argument-hint: <arg1> <arg2>
allowed-tools:
  - Read
  - Edit
  - Bash
---
# 命令内容
```

### 参数定义

```yaml
---
argument-hint: <filename> <search_term>
description: 在文件中搜索并替换文本
---
```

---

## Agent 开发

### Agent 文件结构

Agent 是带有 YAML frontmatter 的 Markdown 文件：

```yaml
---
name: agent-name
description: Agent 描述，包含何时使用此 Agent
model: opus
color: "#ffffff"
tools:
  - Read
  - Edit
  - Bash
---

# Agent 的系统提示
```

### frontmatter 字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | Agent 名称 | `code-reviewer` |
| `description` | 何时使用此 Agent | "代码审查和重构建议" |
| `model` | 使用的模型 | `opus` / `sonnet` |
| `color` | UI 显示颜色 | `"#4A90E2"` |
| `tools` | 允许使用的工具 | `Read`, `Edit`, `Bash` |

---

## Hook 开发

### Hook 类型

| 事件 | 时机 | 用途 |
|------|------|------|
| `PreToolUse` | 工具执行前 | 验证、阻止、修改参数 |
| `PostToolUse` | 工具执行后 | 记录、日志、后处理 |
| `Stop` | Agent 停止时 | 清理资源 |
| `SessionStart` | 会话开始时 | 初始化 |
| `SessionEnd` | 会话结束时 | 保存状态 |

### Hook 脚本示例

```bash
#!/bin/bash
# Hook 脚本接收环境变量和 stdin 输入

TOOL_NAME="$1"
TOOL_INPUT="$2"

# 基于工具名称做决策
if [ "$TOOL_NAME" = "Bash" ]; then
  # 检查命令安全性
  if echo "$TOOL_INPUT" | grep -q "rm -rf"; then
    echo '{"error": "危险命令被阻止"}'
    exit 1
  fi
fi

exit 0
```

---

## MCP 集成

### .mcp.json 配置

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@my/mcp-server"],
      "env": {
        "API_KEY": "${MCP_API_KEY}"
      }
    }
  }
}
```

### 服务器类型

| 类型 | 用途 | 示例 |
|------|------|------|
| `stdio` | 本地命令 | `npx -y @my/server` |
| `SSE` | 托管服务/OAuth | 第三方 API |
| `HTTP` | REST API | 自托管服务 |
| `WebSocket` | 实时通信 | 实时数据 |

---

## 资源链接

| 资源 | 链接 |
|------|------|
| GitHub 仓库 | https://github.com/anthropics/claude-code |
| 官方文档 | https://docs.anthropic.com/en/docs/claude-code |
| Plugin Dev 工具包 | https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev |

---

*翻译整理自 [GitHub - Claude Code plugin-dev](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev)*
