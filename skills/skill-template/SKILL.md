---
name: skill-template
description: "Skill 开发起点模板 — 用于快速创建新的 Skill。当需要新建一个 Skill、处理 Skill 相关的工作（如整理目录、编写 SKILL.md、审核现有 Skill）、或需要了解 Skill 开发规范时使用。本技能提供完整的目录结构、Frontmatter 格式、工作流程和最佳实践。不要用于已有明确工具对应的工作（如发送消息、查询日历）。"
---

# Skill 模板

> 这是一个最小可用的 Skill 模板，经过增强以涵盖真实开发场景所需的所有关键章节。

---

## 简介

本模板用于快速创建一个符合 OpenClaw 规范的 Skill。它提供完整的目录结构、Frontmatter 格式规范，以及开发过程中常用的参考模板。

**与其他模板的区别**：本模板专注于 **Skill 本身**的开发起点，而非完整的应用项目结构。

---

## 适用场景

✅ **应该使用**：
- 创建一个新的 Skill（从零开始）
- 审核/整理已有的 Skill（检查目录结构、Frontmatter、依赖规范）
- 编写或重构 SKILL.md（学习官方规范）
- 理解 Skill 的模块化设计原则

❌ **不应该使用**：
- 需要直接执行特定工具的任务（发送消息、查询日历等）—— 直接使用对应工具
- 构建完整的应用程序或网站（用相应的开发框架）
- 简单的单次问答或信息检索

---

## 目录结构

```
skill-name/
├── SKILL.md           # 必需：Skill 定义文件（见下方 Frontmatter 规范）
├── LICENSE.txt        # 可选：许可证声明
├── references/        # 可选：参考文档（扁平结构，一级目录）
│   ├── README.md
│   └── api-guide.md
├── scripts/          # 可选：可执行脚本（Python/Bash/Node 等）
│   ├── main.py
│   └── utils.py
└── assets/          # 可选：输出资源（模板、图标、字体等，不加载到上下文）
    ├── config.yaml.example
    └── requirements.txt
```

**层级规则**：`references/`、`scripts/`、`assets/` 下保持**扁平结构**，不允许二级子目录。

---

## Frontmatter 规范

SKILL.md 必须以 YAML frontmatter 开头，包含以下字段：

```yaml
---
name: skill-name          # 必需：Skill 名称（唯一标识，英文）
description: |             # 必需：触发描述（见下方详细规范）
  本技能应在...时使用。
  不要用于：...。
---
```

### description 写作规范

1. **使用第三人称**：`本技能应在...时使用`，而非"当...时使用"
2. **添加负向触发条件**：明确说明何时**不应该**使用本技能
3. **长度限制**：不超过 1024 字符，理想在 200-400 字符
4. **精准触发词**：包含用户可能说的关键词

**完整示例**：

```yaml
---
name: legal-text-format
description: |
  将法律文本转换为规范的 Markdown 格式。本技能应在用户需要处理法律条文（如民法典、刑法）、整理法律案例（如最高法典型案例）、或从粘贴文本中格式化法律文档时使用。
  不要用于：代码格式化、普通文章润色、非中文法律文档。
---
```

---

## 快速开始

### 第一步：创建目录结构

```bash
mkdir -p skill-name/{references,scripts,assets}
touch skill-name/SKILL.md
```

### 第二步：编写 SKILL.md

复制本模板的 Frontmatter 和各章节，根据实际 Skill 功能修改内容。

### 第三步：定义触发条件

在 frontmatter 的 `description` 中清晰描述触发场景：

- **触发词**：用户可能说的关键词（如"创建 Skill"、"整理文档"）
- **负向条件**：明确排除的场景（如"不要用于简单的问答"）

### 第四步：实现核心功能

将可执行代码放在 `scripts/` 目录，避免在 SKILL.md 中堆砌大段代码。

### 第五步：验证 Skill

检查清单：
- [ ] Frontmatter 格式正确（`name` + `description` 字段完整）
- [ ] description 包含负向触发条件
- [ ] SKILL.md 正文不超过 500 行
- [ ] `references/` 目录保持扁平结构
- [ ] 无硬编码的敏感信息

---

## 示例

### 示例一：从零创建一个"每日天气播报" Skill

**目标**：创建一个 Skill，每周一向用户播报当周天气。

**Step 1：创建目录**
```bash
mkdir -p weather-briefing/{scripts,assets}
```

**Step 2：编写 SKILL.md**

```yaml
---
name: weather-briefing
description: |
  生成定期天气播报摘要。本技能应在用户需要周期性天气总结（如每周一播报当周天气、节假日出行天气提醒）时使用。
  不要用于：实时单次天气查询（用 weather skill）、长期气候分析。
---
```

**Step 3：实现脚本** `scripts/weather.py`

```python
import sys
import json
from datetime import datetime, timedelta

def get_week_forecast(location: str = "苏州") -> dict:
    """获取未来7天预报（示例占位）"""
    return {
        "location": location,
        "forecast": [
            {"day": "周一", "weather": "晴", "temp": "15-22°C"},
            {"day": "周二", "weather": "多云", "temp": "16-23°C"},
            # ...
        ],
        "generated_at": datetime.now().isoformat()
    }

def format_briefing(data: dict) -> str:
    lines = [f"📍 {data['location']} 本周天气预告",
             f"生成时间：{data['generated_at']}", ""]
    for day in data["forecast"]:
        lines.append(f"• {day['day']}：{day['weather']} {day['temp']}")
    return "\n".join(lines)

if __name__ == "__main__":
    loc = sys.argv[1] if len(sys.argv) > 1 else "苏州"
    result = get_week_forecast(loc)
    print(format_briefing(result))
```

**Step 4：使用**

```bash
python scripts/weather.py "北京"
```

---

### 示例二：审核已有 Skill 的规范性

**目标**：检查现有 Skill 是否符合开发规范。

**触发描述**：
> "帮我检查一下 legal-skills 中的 legal-text-format 是否符合规范"

**执行流程**：

1. **读取 SKILL.md**：检查 frontmatter 格式
2. **检查目录结构**：是否符合标准结构
3. **验证 description**：是否包含负向触发条件
4. **检查行数**：SKILL.md 正文是否超过 500 行
5. **检查依赖**：是否在 SKILL.md 中明确列出系统依赖

**审核检查清单**（输出格式）：

```markdown
## 审核报告：legal-text-format

### ✅ 通过项
- Frontmatter 格式正确
- 包含负向触发条件
- 目录结构符合规范

### ⚠️ 需改进
- SKILL.md 正文章节超过 500 行（当前 623 行）
  → 建议：将详细 API 文档移至 `references/api-reference.md`
- 依赖列表缺少 `python-docx` 安装说明

### ❌ 缺失项
- 无 LICENSE.txt（如需开源）
```

---

## 常见问题

### Q1：Skill 目录应该放在哪里？

**答**：放在 `~/.openclaw/skills/` 目录下，或通过 ClawHub 安装到项目 `skills/` 目录。符号链接也支持。

### Q2：SKILL.md 正文章节超 500 行怎么办？

**答**：将详细文档拆分为多个 `references/` 下的文件，在 SKILL.md 中用引用指向它们。SKILL.md 只保留核心工作流程和关键示例。

### Q3：一个 Skill 能否调用另一个 Skill？

**答**：不能直接调用。通过 AI 协调层先调用 Skill A，再调用 Skill B。SKILL.md 中用自然语言描述协作关系（如"可与 weather skill 配合使用"），而非直接引用内部脚本路径。

### Q4：description 中的负向触发条件必须写吗？

**答**：建议写，但不强制。负向触发条件帮助 AI 更精准地判断何时**不**应该触发本 Skill，尤其在多个 Skill 可能重叠的场景下很有价值。

### Q5：scripts/ 中的脚本语言有要求吗？

**答**：无限制，只要系统能执行即可。常见选择：Python（通用）、Bash（轻量任务）、Node.js（JavaScript 生态）。优先选择最轻量的方案。

### Q6：Skill 能否输出文件到本地？

**答**：能。所有涉及文件输出的 Skill 都应支持可配置输出路径。优先输出到 skill 内部 `output/` 目录，或通过配置指定路径。

---

## 最佳实践

### 1. 渐进式加载（Progressive Disclosure）

**原则**：按需加载，而非一次性全部加载到上下文。

| 层级 | 内容 | 何时加载 |
|------|------|----------|
| Level 0 | Frontmatter（name + description） | 始终加载 |
| Level 1 | SKILL.md 正文 | 技能被触发时 |
| Level 2 | `references/` 下的文档 | AI 主动引用时 |
| Level 3 | `scripts/` + `assets/` | 直接执行，不占上下文 |

### 2. 模块化设计

将独立、可复用的功能抽取为单独脚本：

```
# ✅ 好：独立模块可复用
skill/
├── evaluator.py      # 主流程：评价
├── summarizer.py    # 主流程：摘要
└── pdf_ocr.py       # 独立模块：OCR（可复用）

# ❌ 差：所有逻辑混在一起
skill/
└── main.py          # 500 行大文件
```

### 3. 自包含原则

每个 Skill 是独立项目，所有依赖和配置在内部管理：

- ✅ 依赖写在 SKILL.md 的"依赖"章节
- ✅ 配置文件模板放在 `assets/config.yaml.example`
- ❌ 不要要求用户复制到外部目录（如 `~/.xxx/`）

### 4. 安全审计

- ❌ 不在代码中硬编码 API keys（用环境变量或 `.env` 文件）
- ❌ 不使用 `rm -rf ~`、`rm -rf /` 等危险命令
- ✅ 优先使用 `trash` 而非 `rm` 删除文件
- ✅ 最小权限原则：只请求必要的工具权限

### 5. 触发词设计

description 中的触发词要具体且多样，覆盖不同表达方式：

```yaml
# ✅ 好：覆盖多种表达
description: |
  本技能应在用户需要创建新 Skill、整理现有 Skill 目录、
  或审核 Skill 规范性时使用。
  触发词包括："创建 skill"、"新建一个技能"、
  "帮我整理下 skills"、"检查这个 skill 合规吗"。

# ❌ 差：触发词太少或太模糊
description: "用于 Skill 开发。"
```

---

## 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [SKILL-DEV-GUIDE.md](../SKILL-DEV-GUIDE.md)（本地完整规范）
- [SKILL-ORCHESTRATION-GUIDE.md](../SKILL-ORCHESTRATION-GUIDE.md)（多技能编排）
- [ClawHub Skill 市场](https://clawhub.com)
- [skill-creator 官方示例](/opt/homebrew/lib/node_modules/openclaw/skills/skill-creator/SKILL.md)

---

**基于 Skill 模板创建 | 版本: 2.0.0**
