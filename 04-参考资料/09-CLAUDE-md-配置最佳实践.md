# CLAUDE.md 配置最佳实践

> 本文档整理自 Claude Code 高阶配置指南，是配置 CLAUDE.md 的权威参考。

---

## CLAUDE.md 的作用

CLAUDE.md 是 Claude Code 的项目配置文件，定义了 Claude 在该项目中的行为规则、技能触发和工作方式。

### 核心功能

| 功能 | 说明 |
|------|------|
| **行为定制** | 定义 Claude 的工作风格和规则 |
| **上下文注入** | 提供项目背景信息 |
| **技能注册** | 配置可用的自定义技能 |
| **触发规则** | 设置关键词自动触发 |

### 文件位置

```
项目根目录/
├── CLAUDE.md           ← 项目配置文件
├── .claude/
│   └── skills/         ← 技能定义目录
├── src/
└── ...
```

---

## 推荐配置结构

```markdown
# CLAUDE.md - Project Guidelines

<identity>
你是世界顶级程序员，精通 Python/JavaScript/Go。
- 模式：启用深度思考
- 语言：中文优先，技术术语保留英文
- 风格：精准、务实、追求卓越
</identity>

## Meta Rules（元规则）
核心规则定义

## Cognitive Architecture（认知架构）
思维模型定义

## Execution Habits（执行习惯）
行为约束

## Design Philosophy（设计哲学）
设计理念

## Auto-Trigger Rules（自动触发）
关键词触发配置

## Skills（技能库）
可用技能列表

## File Organization（项目结构）
目录结构说明

## Memory System（记忆系统）
记忆配置

## Workflow Guidelines（工作流指南）
工作流程说明
```

---

## 核心配置项详解

### 1. 身份定义（Identity）

```markdown
<identity>
你是世界顶级程序员，精通 Python/JavaScript/Go。
- 模式：启用深度思考
- 语言：中文优先，技术术语保留英文
- 风格：精准、务实、追求卓越
</identity>
```

**配置要点**：
- 明确角色定位
- 指定语言偏好
- 描述工作风格

### 2. 元规则（Meta Rules）

```markdown
## Meta Rules

1. **优先级**：安全 > 规则 > 逻辑 > 偏好
2. **深度推理**：内部推理要深入，输出要简洁
3. **工具约束**：
   - 读取文件前不修改
   - 优先使用专用工具
   - 编辑前确认文件存在
4. **错误处理**：失败时分析原因后重试
5. **代码质量**：函数 < 20行，嵌套 ≤ 3层
```

### 3. 执行习惯（Execution Habits）

```markdown
## Execution Habits

### 八不原则

1. **不猜接口** - 必须确认 API 签名
2. **不糊涂干活** - 不明白就问
3. **不臆想逻辑** - 以代码/文档为准
4. **不凭空创造** - 使用已有定义
5. **不跳过验证** - 改完必测
6. **不越边界** - 遵循分层设计
7. **不假装理解** - 承认不确定性
8. **不盲目重构** - 改动有据可依
```

### 4. 设计哲学（Design Philosophy）

```markdown
## Design Philosophy

### 核心原则

| 原则 | 描述 |
|------|------|
| **好品味** | 消除特殊情况，追求通用解决方案 |
| **实用主义** | 先解决问题，再考虑扩展 |
| **简洁性** | 最简实现优先 |

### 代码异味

1. 僵化 - 难以修改
2. 重复 - 违反 DRY
3. 循环依赖
4. 脆弱 - 改一处坏多处
5. 晦涩 - 难以理解
```

---

## 技能配置

### 技能目录结构

```markdown
## Skills

### design/ - 设计文档

| Skill | Location | Description |
|-------|----------|-------------|
| `/high-level-design` | `.claude/skills/design/high-level-design.md` | 概要设计 |
| `/detailed-design` | `.claude/skills/design/detailed-design.md` | 详细设计 |
| `/api-design` | `.claude/skills/design/api-design.md` | 接口设计 |

### testing/ - 测试文档

| Skill | Location | Description |
|-------|----------|-------------|
| `/test-plan` | `.claude/skills/testing/test-plan.md` | 测试方案 |
| `/test-report` | `.claude/skills/testing/test-report.md` | 测试报告 |
```

### 技能文件示例

位置：`.claude/skills/design/api-design.md`

```markdown
# Skill: API Design

## 描述
生成符合 RESTful 规范的 API 设计文档。

## 触发条件
- 用户提及 `/api-design`
- 用户说"接口设计"、"API 设计"

## 输出模板

### 接口概述
[接口用途描述]

### 接口列表
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/xxx | 查询 |
| POST | /api/v1/xxx | 创建 |

### 接口详情
[每个接口的详细规格]
```

---

## 自动触发配置

### 关键词触发

```markdown
## Auto-Trigger Rules

| Keywords | Skill | Action |
|----------|-------|--------|
| 概要设计、高层设计 | `/high-level-design` | 读取技能并执行 |
| 详细设计、模块设计 | `/detailed-design` | 读取技能并执行 |
| API设计、接口文档 | `/api-design` | 读取技能并执行 |
| 测试方案、测试计划 | `/test-plan` | 读取技能并执行 |
| 画图、流程图 | `/drawio` | 使用 Draw.io |
```

---

## 项目结构配置

### 目录结构说明

```markdown
## File Organization

项目根目录/
├── CLAUDE.md           # 项目配置
├── .claude/
│   └── skills/        # 技能目录
│       ├── design/     # 设计文档
│       ├── testing/    # 测试文档
│       └── tools/      # 工具类
├── src/               # 源代码
│   ├── controllers/    # 控制器
│   ├── models/        # 数据模型
│   ├── services/     # 业务逻辑
│   └── utils/        # 工具函数
├── tests/             # 测试文件
└── docs/              # 文档输出
```

### 技术栈说明

```markdown
## Tech Stack

| 类别 | 技术 |
|------|------|
| 后端 | Node.js + Express |
| 数据库 | PostgreSQL + Redis |
| 前端 | React + TypeScript |
| 部署 | Docker + K8s |
```

---

## 记忆系统配置

### 记忆层级

```markdown
## Memory System

### 自动记忆（主力）

claude-mem → 全自动捕获 & 注入
├── 自动记录：对话、工具调用、代码变更
├── 自动注入：新会话加载相关上下文
└── 保留策略：默认7天

### 手动记忆（辅助）

| 层级 | 用途 | 使用场景 |
|------|------|----------|
| Memory MCP | 永久知识 | 重要决策 |
| HANDOFF.md | 任务交接 | 紧急情况 |

### 触发词

| 触发词 | 动作 |
|--------|------|
| 继续、接上次 | 加载上下文 |
| 记住这个 | 保存到 Memory |
```

---

## 工作流指南

### 任务接收

```markdown
## Workflow Guidelines

### 接收任务时

1. 确认理解需求，不明确则询问
2. 检查是否匹配 Auto-Trigger Rules
3. 评估复杂度，必要时拆分
4. 使用 TodoWrite 追踪进度
```

### 代码编写

```markdown
### 编写代码时

1. 先读后改，理解现有代码
2. 遵循项目既有风格
3. 保持单一职责
4. 避免安全漏洞
```

### 任务完成

```markdown
### 完成任务时

1. 验证改动符合预期
2. 检查是否有遗漏
3. 提供测试建议
4. 简洁总结完成内容
```

---

## 完整示例

### 最小配置

```markdown
# CLAUDE.md

## 项目信息
- 名称：My Project
- 技术栈：Node.js + Express

## 规则
- 读取文件后再修改
- 代码要有注释
- 使用中文回复
```

### 标准配置

```markdown
# CLAUDE.md - Project Guidelines

<identity>
你是专业的 Node.js 开发者。
语言：中文优先
</identity>

## 核心规则
1. 先读后改
2. 函数保持简短
3. 遵循 RESTful 规范

## 技能

| Skill | Description |
|-------|-------------|
| `/commit` | Git 提交 |
| `/test` | 运行测试 |

## 项目结构

src/ - 源代码
tests/ - 测试文件
docs/ - 文档
```

---

## 最佳实践

### 配置原则

| 原则 | 说明 |
|------|------|
| **精简** | 只包含必要信息，避免冗长 |
| **明确** | 规则表述清晰，不留歧义 |
| **实用** | 配置要解决实际问题 |
| **迭代** | 根据使用反馈持续优化 |

### 常见错误

| 错误 | 问题 | 解决 |
|------|------|------|
| 配置过长 | 消耗上下文 | 精简内容 |
| 规则冲突 | Claude 困惑 | 明确优先级 |
| 技能未定义 | 触发失败 | 补充技能文件 |

### 维护建议

- **版本记录**：使用修订表记录变更
- **定期审查**：删除过时配置
- **团队同步**：确保配置同步

---

*整理自 Claude Code 高阶配置指南*
