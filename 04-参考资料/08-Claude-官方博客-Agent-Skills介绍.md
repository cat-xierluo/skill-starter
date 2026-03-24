# Introducing Agent Skills | Claude 官方博客

> 原文地址：https://www.anthropic.com/news/skills
> 发布日期：2025年10月16日
> 更新：2025年12月18日（新增组织级管理和开放标准）

---

## 什么是 Agent Skills？

Claude 现在可以使用 Skills 来提升执行特定任务的能力。Skills 是包含指令、脚本和资源的文件夹，Claude 可以在需要时加载。

Claude 只会在任务相关时访问 Skill——保持快速同时获取专业知识。

当使用 Skills 时，Claude 在处理 Excel 或遵循组织品牌指南等专业任务时表现得更好。

---

## Skills 的特点

| 特点 | 说明 |
|------|------|
| **可组合** | Skills 可以堆叠。Claude 自动识别需要哪些 Skills 并协调使用 |
| **可移植** | Skills 各地使用相同格式。构建一次，可在 Claude 应用、Claude Code 和 API 中使用 |
| **高效** | 只在需要时加载所需内容，保持 Claude 快速响应 |
| **强大** | Skills 可以包含可执行代码，适用于传统编程比 token 生成更可靠的任务 |

把 Skills 想象成定制化的入职材料，让你可以打包专业知识，使 Claude 成为你最关心领域的专家。

---

## Skills 工作原理

在执行任务时，Claude 会扫描可用的 Skills 来找到相关匹配。当找到匹配时，它只加载所需的最小信息和文件——在访问专业知识的同时保持快速。

**技术深度**：关于 Agent Skills 设计模式、架构和开发最佳实践，请阅读[工程博客](https://www.anthropic.com/news)。

---

## Skills 支持所有 Claude 产品

### Claude 应用

Skills 对 Pro、Max、Team 和 Enterprise 用户可用。

- 提供常见任务的 Skills（如文档创建）
- 提供可自定义的示例
- 支持创建自己的自定义 Skills
- Claude 自动根据任务调用相关 Skills——无需手动选择
- 在 Claude 的思维链中甚至可以看到 Skills

创建 Skills 很简单。"skill-creator" Skill 提供交互式指导：
- Claude 询问你的工作流程
- 生成文件夹结构
- 格式化 SKILL.md 文件
- 捆绑你需要的资源
- **无需手动编辑文件**

在设置中启用 Skills。

### Claude Developer Platform (API)

Agent Skills 可以添加到 Messages API 请求中，新的 `/v1/skills` 端点为开发者提供自定义 Skill 版本控制和管理的编程方式。

Skills 需要 Code Execution Tool beta，它提供了运行所需的安全环境。

### Claude Code

Skills 通过团队专业知识和工作流扩展 Claude Code。

- 通过 anthropics/skills 市场插件安装 Skills
- Claude 在相关时自动加载
- 通过版本控制与团队共享 Skills
- 也可以通过添加到 `~/.claude/skills` 手动安装

### Anthropic Agent SDK

为构建自定义代理提供相同的 Agent Skills 支持。

---

## 官方 Skills 示例

### Box

Skills 教 Claude 如何处理 Box 内容。用户可以将存储的文件转换为遵循组织标准的 PowerPoint 演示文稿、Excel 电子表格和 Word 文档——节省数小时工作。

### Canva

Canva 计划利用 Skills 自定义代理并扩展其功能。这为更深入地参与代理工作流程开辟了新方式——帮助团队捕获独特背景并轻松创建令人惊叹的高质量设计。

### Notion

使用 Skills，Claude 与 Notion 无缝协作——让用户更快从问题到行动。在复杂任务上减少提示词编写，获得更可预测的结果。

### 管理会计和财务工作流

Skills 简化了管理会计和财务工作流。Claude 处理多个电子表格，捕捉关键异常，并使用组织的程序生成报告。以前需要一天完成的工作，现在一小时内就能完成。

---

## 技术资源

| 资源 | 链接 |
|------|------|
| Claude 应用用户指南 | Settings 中启用 |
| API 开发者文档 | Messages API + /v1/skills 端点 |
| Claude Code 文档 | `~/.claude/skills` |
| Skills 食谱 | GitHub 仓库 |
| Anthropic Academy | 学习路径 |

---

## 常见问题

**安全提醒**：此功能让 Claude 有权访问执行代码。虽然强大，但请注意你使用的 Skills——坚持使用可信来源以保护数据安全。

---

## 下一步

我们正在简化 Skill 创建工作流和企业级部署能力，使组织更容易在团队中分发 Skills。

---

*翻译整理自 [Anthropic 官方博客 - Introducing Agent Skills](https://www.anthropic.com/news/skills)*
