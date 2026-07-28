# 07 带脚本 Skill

上一篇 [06 纯说明型 Skill](./06-纯说明型-Skill.md) 解决了「AI 光靠想就能完成」的任务。但很多事光靠想不够——要读文件、跑命令、算结果、生成产物。这时就得给 Skill 配脚本。这篇讲清带脚本型：脚本怎么写、退出码怎么约定、输入输出契约长什么样、依赖怎么处理、`assets/` 怎么用。我们用贯穿全系列的 `todo.py`（一个本地待办脚本）做一个「待办管理」Skill。

## 本篇目标

读完这篇，你能：

- 判断一个任务什么时候该从纯说明型升级到带脚本型；
- 写出一个能让 AI 稳定调用的脚本：成功的走 stdout、错误的走 stderr、退出码诚实反映成败；
- 说清「输入输出契约」是什么，并按契约设计脚本的参数和输出格式；
- 处理依赖：什么时候需要 `requirements.txt` 和虚拟环境，跨平台要注意什么；
- 正确使用 `assets/`，并说清它和 `.env.example`、`references/` 各自的职责边界。

命令区分 macOS / Linux 与 Windows，差异处逐一标注（[终端入门](../02-工具指南/06-终端与命令行入门.md) 讲过退出码基础，这里直接用）。

## 前置知识

- [06 纯说明型 Skill](./06-纯说明型-Skill.md)：知道三种形态的分工，以及为什么「能不写脚本就别写」。
- [一个 Skill 是怎样工作的？](../01-概念入门/06-一个-Skill-是怎样工作的.md)：尤其是其中「失败边界」一节——**退出码**（脚本结束时返回给调用方的数字：0 表示成功，非 0 表示失败）是 Agent 判断这一步成败的唯一信号。本篇反复用到这个概念。
- [开发环境与依赖入门](../02-工具指南/08-开发环境与依赖入门.md)：知道虚拟环境（venv）和「全局安装 vs 项目安装」的区别，依赖处理一节直接用到。
- [03 基于模板创建](./03-基于模板创建.md)：知道怎么从模板复制出 Skill。

## 核心概念：带脚本型多了什么

### 多了一个「会做」的零件

纯说明型只有说明书，AI「会说」；带脚本型多了 `scripts/`，AI 还能「会做」——真正去执行代码、改文件、算结果。多出来的能力全来自这个目录：

```text
todo-skill/
├── SKILL.md          # 说明书：何时调用、契约怎么约定
├── scripts/
│   └── todo.py       # 干活的脚本（会被真正执行）
├── assets/           # 静态资源：配置模板、依赖清单、示例数据
├── references/       # 详细资料（按需读，同纯说明型）
└── .env.example      # 环境变量模板（放根目录）
```

什么时候从纯说明型升级到带脚本？还是那个问题——**AI 光靠想能完成吗？** 当任务需要读写文件、运行命令、计算或生成产物时，答案是「不能」，就该写脚本。典型场景：解析日志、批量改文件、调用外部工具、跑测试、生成报告。

### 契约：脚本和 AI 之间的约定

脚本不是写完能跑就行——它要被 AI 反复调用，所以得有一份**输入输出契约**，让 AI 知道「给它什么、它还什么、怎么知道成没成」。三个要素：

| 要素 | 放什么 | 谁在看 |
|------|--------|--------|
| 输入 | 命令行参数（argv）或 stdin 的 JSON | 脚本接收 |
| stdout（标准输出） | 成功的结果 | AI 解析——最好结构化（JSON），别输出半句人话半句数据 |
| stderr（标准错误） | 错误和诊断信息 | 人看；Agent 不解析内容，靠退出码判断失败 |
| 退出码 | 0 = 成功；非 0 = 失败 | Agent **只看是否为 0** |

这里最常被忽略的一条：**stdout 和 stderr 要分开**。成功的结果走 stdout 且尽量结构化（JSON 最稳，AI 好解析）；出错的信息走 stderr，并让退出码非 0。混在一起，或者出错却往 stdout 打字、退出码还是 0，AI 就会误判成功——这正是 [一个 Skill 是怎样工作的？](../01-概念入门/06-一个-Skill-是怎样工作的.md) 里「失败边界」强调的坑。

### assets/ 的边界

带脚本型常需要静态资源，但三个容易混的位置各有职责（模板 `skills/skill-template/SKILL.md` 已立过规矩）：

| 位置 | 放什么 | 例子 |
|------|--------|------|
| `assets/` | 配置模板、依赖清单、示例数据、模板文件 | `config.yaml.example`、`requirements.txt`、`todos.example.json` |
| `.env.example`（根目录） | 环境变量模板 | `API_KEY=`、`OUTPUT_DIR=` |
| `references/` | 给 AI 读的详细资料 | 架构说明、规则细节 |

一条容易记的分界：**配置和数据模板进 `assets/`，密钥类环境变量进 `.env.example`，给人/给 AI 读的说明进 `references/`**。运行时生成的数据（如 `todos.json`）两者都不是——它由脚本在运行目录里现写，不进仓库。

## 实例分析：todo.py 的契约长什么样

贯穿系列的 `todo.py` 是一个本地待办脚本（Python 3 标准库、存 `todos.json`、`add/list/done` 三命令）。先看它的契约，再动手包成 Skill。

**输入**：命令行参数。`add` 带一段文本，`done` 带一个 id，`list` 不带参数。

**输出**：`add` 和 `done` 成功时，把那条待办以 JSON 打到 stdout（结构化，AI 好解析）；`list` 打易读的文本列表；出错信息一律走 stderr。

**退出码**：`0` 成功；`1` 运行时失败（如 `done` 找不到 id）；`2` 用法错误（参数不对）。Agent 只需要知道「0 与非 0」，1 和 2 的细分是给人调试用的，属于可选增强。

下面是完整脚本（只用标准库，无外部依赖）：

```python
#!/usr/bin/env python3
"""最小待办脚本：add / list / done，数据存 todos.json。"""
import json
import sys
from pathlib import Path

DB = Path(__file__).parent / "todos.json"


def load():
    if DB.exists():
        return json.loads(DB.read_text(encoding="utf-8"))
    return []


def save(todos):
    DB.write_text(json.dumps(todos, ensure_ascii=False, indent=2), encoding="utf-8")


def next_id(todos):
    return max((t["id"] for t in todos), default=0) + 1


def main(argv):
    if not argv:
        print("usage: todo.py [add <text> | list | done <id>]", file=sys.stderr)
        return 2
    cmd, rest = argv[0], argv[1:]
    todos = load()
    if cmd == "add":
        text = " ".join(rest).strip()
        if not text:
            print("error: 待办内容不能为空", file=sys.stderr)
            return 2
        todo = {"id": next_id(todos), "text": text, "done": False}
        todos.append(todo)
        save(todos)
        print(json.dumps(todo, ensure_ascii=False))  # 成功结果走 stdout
        return 0
    if cmd == "list":
        for t in todos:
            mark = "x" if t["done"] else " "
            print(f"[{mark}] {t['id']}: {t['text']}")
        return 0
    if cmd == "done":
        if not rest or not rest[0].isdigit():
            print("error: 用法 done <id>", file=sys.stderr)
            return 2
        tid = int(rest[0])
        for t in todos:
            if t["id"] == tid:
                t["done"] = True
                save(todos)
                print(json.dumps(t, ensure_ascii=False))
                return 0
        print(f"error: 找不到 id={tid}", file=sys.stderr)  # 错误走 stderr
        return 1
    print(f"error: 未知命令 {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

对着契约表逐条核对：成功结果走 stdout 且是 JSON；错误走 stderr；退出码诚实（找不到返回 1，参数错返回 2，成功返回 0）。这份契约就是下一步写 `SKILL.md` 时要告诉 AI 的内容。

## 动手步骤：创建「待办管理」Skill

把上面的 `todo.py` 包成一个完整 Skill。

### 第 1 步：复制模板，摆好目录

```bash
cp -r skills/skill-template skills/todo
cd skills/todo
```

把核心脚本放进 `scripts/todo.py`（内容就是上面那段）。最终目录：

```text
todo/
├── SKILL.md
├── scripts/
│   └── todo.py
├── assets/
│   └── todos.example.json
├── LICENSE.txt
├── CHANGELOG.md
├── ROADMAP.md
├── TASKS.md
├── DECISIONS.md
└── .env.example
```

`assets/todos.example.json` 放一份示例数据形态（空数组 `[ ]` 或一两条示例待办），给读者参考数据长什么样。真正的 `todos.json` 由脚本运行时生成，**不进仓库**（写进 `.gitignore`）。

### 第 2 步：写 frontmatter

和纯说明型一样，`name` 与目录名一致，`description` 写正向触发、负向触发和多种问法——只是这里点明「通过运行脚本」：

```markdown
---
name: todo
description: |
  本技能应在用户要管理本地待办（新增 / 查看 / 完成）、说「记一下」「加个待办」
  「我有什么待办」「把某项标完成」时使用。通过运行 scripts/todo.py 读写 todos.json。
  不要用于：团队协作看板、带截止时间提醒、日历事件、跨设备同步。
---
```

### 第 3 步：在正文里写清契约

正文的关键不是讲业务，而是**把脚本契约交代给 AI**——什么时候调、传什么、读什么、怎么判断成败。直接把契约写进正文：

```markdown
# todo

管理本地待办列表，数据存在 todos.json。

## 何时调用

- 用户要新增、查看或完成一条待办时，调用 scripts/todo.py。
- 涉及到期提醒、多人协作、跨设备同步时不要用。

## 脚本契约

scripts/todo.py 三个命令：

- add <text>：新增一条。成功时 stdout 输出该条 JSON，退出码 0。
- list：列出全部。stdout 输出易读列表，退出码 0。
- done <id>：标记完成。成功时 stdout 输出该条 JSON，退出码 0；
  找不到 id 时退出码 1。

约定：成功信息走 stdout（结构化 JSON，便于你解析）；错误信息走 stderr；
退出码 0 表示成功，非 0 表示失败——非 0 时不要当成功处理，去读 stderr 找原因。
```

注意正文里写死了契约细节（哪条命令输出什么、退出码含义）。这是带脚本型和纯说明型的最大区别：**纯说明型的正文讲「知识」，带脚本型的正文还要讲「怎么调脚本、怎么判读结果」**。契约不写清，AI 调完脚本不知道该不该信结果。

### 第 4 步：跑通并验证退出码

带脚本型有脚本能直接跑，验证比纯说明型实在。挨个跑一遍，确认 stdout/stderr/退出码都符合契约（退出码用 macOS/Linux 的 `echo $?` 看，Windows PowerShell 用 `$LASTEXITCODE`）：

```bash
python3 scripts/todo.py add 读完概念入门
python3 scripts/todo.py list
python3 scripts/todo.py done 1
python3 scripts/todo.py done 99   # 故意失败：应退出码非 0、stderr 报错
```

最后一条是关键验证：它必须**返回非 0**并在 stderr 报「找不到 id」。如果它返回 0，说明契约没守住，AI 会被骗——回去改脚本。

> 跨平台提示：macOS 和大多数 Linux 自带 `python3`；Windows 上通常要敲 `python`（且需先装好 Python，见 [开发环境与依赖入门](../02-工具指南/08-开发环境与依赖入门.md)）。`SKILL.md` 里统一写 `python3`，Windows 用户自行替换。

### 第 5 步：处理依赖

`todo.py` 只用标准库（`json`、`sys`、`pathlib`），**没有外部依赖**——这是最省心的情形：不需要 `requirements.txt`，也不需要虚拟环境，复制过去就能跑。

一旦脚本 `import` 了第三方库（比如 `requests` 联网、`rich` 美化输出），就必须做两件事：

1. 在 `assets/requirements.txt` 声明依赖，写清包名和版本（如 `requests==2.32.3`——版本号是示例，按你实际用的写）。
2. 建议在**虚拟环境**里安装，不要假设用户全局已经装好。虚拟环境把依赖隔离在项目目录内，避免污染系统 Python（[开发环境与依赖入门](../02-工具指南/08-开发环境与依赖入门.md) 讲过原理）。

跨平台激活虚拟环境的命令不同，是 Windows 用户的常见拦路点：

| 平台 | 创建 | 激活 |
|------|------|------|
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |
| Windows (PowerShell) | `python -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |

Windows 上 `Activate.ps1` 可能撞上执行策略（ExecutionPolicy）报错，解法见 [开发环境与依赖入门](../02-工具指南/08-开发环境与依赖入门.md)。处理凭据时（比如脚本要读 API Token），别写死在代码里，走环境变量（`.env.example` + `.gitignore`，见 [09 环境变量与密钥安全](../02-工具指南/09-环境变量与密钥安全.md)）。

## 常见错误

### 脚本出错却返回 0

最致命的一条。脚本失败但退出码是 0，Agent 就会当成成功、拿着错误结果往下走。正确做法：所有错误路径 `return` 非 0（或 `sys.exit(非0)`），并往 stderr 打印原因。上面 `done 99` 那条验证就是专门防它的。

### 成功结果和错误信息都往 stdout 打

AI 靠 stdout 取结果、靠退出码判成败、靠 stderr 看失败原因。把错误也打到 stdout、退出码还是 0，三条信号全乱。正确做法：成功走 stdout、错误走 stderr、退出码如实反映。

### stdout 输出半句人话半句数据

比如成功时打印「好的，已新增：{"id":1,...}」。AI 没法稳定解析这种混合文本。正确做法：要给 AI 解析就输出纯 JSON；要给人看就说明这是展示用、别让 AI 解析。

### 依赖没声明，假设全局装了

脚本 `import requests`，但既没写 `requirements.txt`，也没提示装到虚拟环境。换台机器就 `ModuleNotFoundError`。正确做法：外部依赖一律进 `assets/requirements.txt`，并在 `SKILL.md` 写明安装步骤。

### 凭据写死在脚本里

把 Token、密码直接写进 `scripts/todo.py` 提交进仓库——等于把钥匙交出去。正确做法：凭据走环境变量，仓库只留 `.env.example` 模板，真值写进被 `.gitignore` 忽略的 `.env`（见 [09 环境变量与密钥安全](../02-工具指南/09-环境变量与密钥安全.md)）。

### 硬编码路径，换个目录就崩

脚本里写死 `/Users/your-name/...` 这类绝对路径，换机器或换目录就找不到文件。正确做法：用相对路径或基于脚本自身位置定位（`Path(__file__).parent`），让 Skill 在任意目录都能跑。

## 自测题 / 验收

1. 对照「输入输出契约」那张表，说清 stdout、stderr、退出码各自放什么、谁在看。
2. 跑 `python3 scripts/todo.py done 99`，它应该返回什么退出码、信息走哪个通道？如果它返回了 0，说明什么问题？
3. `todo.py` 没有外部依赖。如果你给它加一个 `import requests`，必须同步做哪两件事？
4. `assets/`、`.env.example`、`references/` 各放什么？运行时生成的 `todos.json` 该放哪、为什么？
5. 给下面这段脚本指出契约问题（至少两处）：成功时 `print("done: " + data)` 且 `sys.exit(0)`，失败时 `print("出错了")` 且 `sys.exit(0)`。

第 5 题能指出「成功输出不是纯结构化、失败退出码仍是 0」，说明契约你已经吃透了。

## 下一篇

本篇让 Skill「会做」了一件事。当一条流程需要把好几个「会说/会做」的 Skill 串起来（先查、再改、再验证），就进入第三层：

- **下一篇（主线）**：08 多 Skill 编排（暂未发布）——把多个 Skill 串成一条流程，讲角色边界与交接。
- 想回看最简形态：[06 纯说明型 Skill](./06-纯说明型-Skill.md)。
- 触发质量想做得更系统：09 触发质量与 eval（暂未发布）。
- 做完要调试和发布：[04 调试与发布](./04-调试与发布.md)；第一次用前先审查：[05 第三方 Skill 安全审查](./05-第三方-Skill-安全审查.md)。

---

**收尾给一个动作**：拿本文的 `todo.py` 在本地跑一遍那四条命令，重点看 `done 99` 的退出码——亲眼确认「失败真的返回非 0」，你就能把这条契约刻进肌肉记忆，以后写任何脚本都会自觉守住它。
