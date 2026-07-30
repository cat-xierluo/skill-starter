# 仓库级许可证方案（LICENSE-PLAN）

> Last updated: 2026-07-30
>
> ✅ **已选定：选项 A（MIT）**——仓库维护者已于 2026-07-28 拍板采用 MIT 覆盖原创内容（见 DEC-026 与根 `LICENSE.txt`）。本文件保留为方案推导记录，第 5 节决策清单已据此闭环。
>
> 本文件是仓库级许可证的**方案文档**，不是许可证文本本身。最终选哪个条款由仓库维护者拍板（原约束见 DEC-013）。
>
> 各 Skill 的来源与许可证事实见 [SOURCE-INDEX.md](./SOURCE-INDEX.md)。本文件基于该索引的事实层做方案推导。

## 1. 现状

仓库当前的状态可以归纳为三点：

1. **仓库根已采用 MIT。** 根目录 `LICENSE.txt` 覆盖本仓库原创内容；第三方与上游内容仍保留各自原许可证。
2. **内容是混合的。** 仓库里同时存在三类内容：
   - **starter 原创内容**：根目录的教程 Markdown（`01-概念入门/`、`02-工具指南/`、`03-AI协作与上下文/`、`04-创建Skill/`、`05-参考资料/`）、`README.md`、`AGENTS.md`、`CHANGELOG.md`、`docs/`、`scripts/`、`skills/skill-template/`。
   - **legal-skills 同步内容**：`skills/git-batch-commit/`、`skills/skill-manager/`，均来自 https://github.com/cat-xierluo/legal-skills ，许可证为 MIT。
   - **第三方收录内容**：`skills/find-skills/`（来自 vercel-labs/skills，MIT）、`skills/skill-creator/`（来自 anthropics/skills，Apache-2.0）。
3. **第三方内容保留了各自的原许可证**：`skills/find-skills/LICENSE.txt`（MIT）、`skills/skill-creator/LICENSE.txt`（Apache-2.0）和 `skills/skill-manager/LICENSE.txt`（MIT）均保留在对应目录；`skills/git-batch-commit/` 的 MIT 许可证事实来自其 frontmatter 与 legal-skills 上游根 LICENSE。

## 2. 核心原则

下列原则在本仓库落地许可证时必须遵循，**与最终选哪个条款无关**：

1. **不能用单一许可证覆盖上游 / 第三方内容。** 仓库根 LICENSE 只对**本仓库原创内容**生效；同步和收录进来的 Skill 仍按其原许可证提供。
2. **第三方内容保留原 LICENSE 与署名。** 不得删除或改写 `skills/skill-creator/LICENSE.txt`、`skills/skill-manager/LICENSE.txt` 等已有许可证文本；不得在 README 或根 LICENSE 里宣称对这些内容拥有版权。
3. **MIT 与 Apache-2.0 等条款的派生义务必须显式履行。** 例如 Apache-2.0 要求保留 `LICENSE` 与（若存在）`NOTICE` 文件；MIT 要求保留版权声明与本许可文本。
4. **来源与许可证分开核对。** 第三方 Skill 必须同时记录本地基线 SHA、最近核对的上游版本和许可证来源；核对过最新版本不等于已经升级本地内容。
5. **仓库根 LICENSE 与第三方声明配套出现。** 一旦在仓库根放置 LICENSE，必须同时在 README 增加"第三方内容与许可证声明"段，指向 [SOURCE-INDEX.md](./SOURCE-INDEX.md)，避免读者误以为根 LICENSE 覆盖整个仓库。
6. **决策权属于维护者。** 本文件给选项与利弊，不替维护者拍板（见 DEC-013）。

## 3. 方案选项

下面三个选项都**只覆盖仓库原创内容**（教程、scripts、`skill-template`、`docs/`、根级 Markdown）。无论选哪个，第三方 Skill 目录都按其原许可证处理，不受根 LICENSE 影响。

> 关于"派生条款"的术语（SA、NC、ND、GPL、AGPL 等）已在 `05-参考资料/` 的许可证参考文档中解释，本文件不重复。

### 选项 A：原创内容统一用 MIT

**条款**：根 LICENSE 采用 MIT；原创文档与原创代码统一 MIT。

**利**：
- 与本仓库已收录的两个 legal-skills 同步 Skill（`git-batch-commit`、`skill-manager`）许可证一致，整体观感统一。
- 最宽松，允许商用、闭源派生、再分发，传播阻力最低。
- 维护成本低：只需保留版权声明一行。

**弊**：
- 不要求派生作品开源，也不强制署名以外的 reciprocity；后续若想收回某些商用权益，法律上几乎不可能撤回已授予的 MIT。
- 对纯文档而言，MIT 不是为文档设计的许可证（虽然可用），社区惯例更倾向 CC 系列。

**对"教程被他人转载 / 商用"的影响**：MIT 允许任意商用、转载、修改、闭源再发布，只需保留版权声明。**无法阻止**他人将教程打包售卖或纳入付费课程；只能要求署名。

**对"后续商业化空间"的影响**：MIT 几乎不限制未来任何商业化形式（自己商用、授权、双重许可都可以），但也意味着无法把"独家商用权"作为筹码卖给任何一方——因为你已经向所有人授予了商用权。

---

### 选项 B：原创代码用 MIT、原创文档用 CC-BY-4.0（代码 / 文档分流）

**条款**：根 LICENSE 说明"原创代码（`scripts/`、`skills/skill-template/scripts/` 等）采用 MIT；原创文档（根级 Markdown、`docs/`、`01-概念入门/`~`05-参考资料/`、`skills/skill-template/` 内模板文档）采用 CC-BY-4.0"。仓库根同时放置 MIT LICENSE 和 CC-BY-4.0 的法律文本（或链接到对应的 SPDX 文本）。

**利**：
- 代码和文档分别用各自生态最常用的许可证，符合社区惯例。
- CC-BY-4.0 要求署名、标明更改，对文档转载有更清晰的 attribution 机制；MIT 对代码的宽松度也得以保留。
- 与 Anthropic 官方 `skill-creator`（Apache-2.0）和 legal-skills（MIT）的代码许可证体系可以共存。

**弊**：
- 仓库出现两种许可证，读者需要判断"我用的这段是代码还是文档"。
- 在 Skill 这种代码-文档-配置混合的目录里，划分边界会比纯软件项目更费力（例如 `SKILL.md` 是文档还是配置？`scripts/main.py` 的 docstring 算文档吗？）。
- CC-BY-4.0 仍允许商用，依然无法阻止付费课程化。

**对"教程被他人转载 / 商用"的影响**：CC-BY-4.0 允许商用与改编，但要求署名 + 标明更改。转载方必须在显著位置标注原作者和修改点，比 MIT 多了一道可执行的署名链路。

**对"后续商业化空间"的影响**：和选项 A 类似，CC-BY-4.0 已授予商用权，无法事后收回。但因文档要求署名，对"原作者声誉绑定"略有保护。

---

### 选项 C：原创内容用 CC-BY-NC-SA-4.0

**条款**：根 LICENSE 采用 CC-BY-NC-SA-4.0（署名-非商用-相同方式共享）。适用于原创文档；对原创代码（`scripts/`、模板脚本），如果选这一项，建议同样采用 CC-BY-NC-SA-4.0，或显式声明"代码部分采用另一许可证（待定）"。

**利**：
- 显式禁止他人商用，**能阻止**他人把教程或模板打包售卖、纳入付费课程。
- SA（Share-Alike）要求派生作品采用相同许可证，形成 reciprocity。
- 对希望长期保留商业化或声誉控制的维护者更友好。

**弊**：
- NC 条款会**同时限制**社区贡献者（例如某公司员工无法在公司项目中使用本仓库教程，因为算"商用"），传播阻力显著上升。
- 与本仓库已收录的 MIT / Apache-2.0 第三方 Skill **不兼容**：在同一个仓库里，原创内容禁止商用、第三方内容允许商用，会让使用者困惑。
- CC-BY-NC-SA-4.0 不是开源许可证（OSI 不认可 NC 条款），不能贴"开源"标签。
- 对纯代码而言，CC 系列并非为代码设计，可能会让下游开发者不愿集成。

**对"教程被他人转载 / 商用"的影响**：能法律上禁止商用转载与付费课程化；非商用转载允许，但必须署名 + 相同许可证共享。

**对"后续商业化空间"的影响**：保留了维护者自身的独家商用权（因为只对"他人商用"设限），可以做付费版、双授权或商业服务。但代价是社区传播显著降低，且对未来"转为更宽松许可证"造成阻力（已经授予 NC-SA 的版本无法收回）。

## 4. 第三方声明模板

下面是已经落地到 `README.md` 的第三方声明结构，保留在这里作为维护模板：

```markdown
## 第三方内容与许可证声明

本仓库为混合来源仓库：

- **原创内容**（根级 Markdown 教程、`docs/`、`scripts/`、`skills/skill-template/`）
  采用 MIT 许可证（见根目录 `LICENSE.txt`）。
- **第三方 Skill** 各自保留原许可证，**不受**根 LICENSE 覆盖：

  | 目录 | 上游 | 许可证 |
  | :--- | :--- | :--- |
  | `skills/git-batch-commit` | https://github.com/cat-xierluo/legal-skills | MIT |
  | `skills/skill-manager` | https://github.com/cat-xierluo/legal-skills | MIT |
  | `skills/skill-creator` | https://github.com/anthropics/skills | Apache-2.0 |
  | `skills/find-skills` | https://github.com/vercel-labs/skills | MIT |

  各 Skill 目录内的 `LICENSE.txt` / frontmatter `license` 字段以原件为准。

- 完整的来源、同步 commit SHA、本地补丁与最近核对日期见
  `docs/SOURCE-INDEX.md`（相对于仓库根；这段文字将来放入 README 后即可作为相对链接点击）。

使用或再分发本仓库时，请同时遵守根 LICENSE 与各第三方目录内的许可证条款；
若两者冲突，针对相应目录的内容以第三方许可证优先。
```

## 5. 决策结果与剩余增强

以下决策已经落地：

1. 仓库原创内容采用 MIT，并已创建根 `LICENSE.txt`（DEC-026）。
2. README 已增加第三方许可证表；各目录继续保留原许可证，不受根 LICENSE 覆盖。
3. `skills/find-skills/` 上游许可证已确认为 MIT，目录已同步完整许可证文本；本地内容基线与上游现状分别记录在 `SOURCE-INDEX.md`（DEC-036）。
4. `skills/skill-template/` 预置 MIT `LICENSE.txt`，frontmatter 同步写 `license: MIT`；复制者改用其他许可证时必须同时替换两处声明（DEC-035）。
5. `skills/git-batch-commit` 1.4.1 已进入仓库历史，当前内容与 `legal-skills/main` 一致。

仍可继续增强，但不影响当前授权事实：

- 扩展 `scripts/check_skills.py`，进一步检查 frontmatter 与目录许可证文本的一致性。
- 分别评估 `find-skills`、`skill-creator` 的上游功能更新；评估完成前保留已锁定的本地基线，不把“已核对上游”写成“已升级”。

## 6. 不在本文件处理的事

- 不替第三方上游变更授权条款；目录许可证保留上游原文。
- 不在没有功能测试或 eval 的情况下自动升级第三方 Skill。
- 不把本方案文档当作许可证文本；实际授权仍以根目录和各 Skill 目录的 LICENSE 文件为准。
