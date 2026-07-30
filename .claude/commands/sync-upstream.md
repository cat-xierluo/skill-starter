# Sync Skills from Upstream

从只读上游 remote 精确同步 `skills/<name>`。支持新增、无本地补丁镜像更新和带本地补丁派生版合并；默认保留无关工作树改动，不允许整棵 `skills/` 覆盖。

## 适用请求

- “从 legal-skills 同步最新的 git-batch-commit”
- “检查 skill-manager 上游变化并保留 starter 补丁”
- “从某个上游拉一个新 Skill”
- “跨仓库拉一批 Skill 子目录”

## 不变量

1. remote 只用于 fetch；必须显式设置不可用的 push URL，并在同步前验证。
2. 只操作用户点名且上游真实存在的 `skills/<name>`；禁止 checkout 整个 `skills/`。
3. 目标目录有未提交改动时停止，不用备份掩盖脏工作树。
4. 备份路径同时包含 UTC 时间和 upstream short SHA，且有清单文件；不得复用旧备份目录。
5. 无本地补丁的镜像才可整目录 checkout；fork/派生版只能导出候选后定向合并。
6. 同步后检查 Skill 自身、目录外依赖、许可证、来源记录和全仓严格检查。
7. 任一步失败都保留候选与备份，先恢复再报告；不删除无关文件。

本仓库的特殊边界：

- `skills/git-batch-commit` 当前是 legal-skills 镜像，可在预检仍确认无本地补丁时覆盖同步。
- `skills/skill-manager` 是带 DEC-020、DEC-034 本地补丁的派生版，**禁止**执行 `git checkout legal-skills/main -- skills/skill-manager`；只能走“派生版合并”。
- `04-创建Skill/SKILL-*-GUIDE.md` 不属于本命令默认范围。
- 根 `AGENTS.md` 已有同步规则时只读取，不为留痕重复改写；用户明确要求改变项目规则时才修改。

## 执行流程

按顺序执行。输入、来源分类或目标路径不明确时停止，不从标题猜测。

### 1. 固定输入并校验路径

先明确：

- `REMOTE`：remote 名称
- `UPSTREAM_URL`：上游 Git URL
- `BRANCH`：默认分支
- `SKILLS`：一个或多个 Skill 名称

remote 和 Skill 名只允许字母、数字、点、下划线、连字符。拒绝空值、`..`、斜杠、绝对路径和 glob，防止目标越出 `skills/<name>`。

先读 `docs/SOURCE-INDEX.md` 和 `AGENTS.md` 的上游同步段，把每个目标标成：

| 类型 | 判定 | 后续路径 |
|---|---|---|
| 新增 | 本地不存在，上游存在 | 新增拉取 |
| 镜像 | 本地存在，来源索引确认无本地补丁 | 覆盖同步 |
| 派生版 | 来源索引记录 fork、本地补丁或独立版本 | 候选导出 + 定向合并 |

来源索引缺失或与实际 diff 冲突时按“派生版”处理，不能按镜像覆盖。

### 2. 确认 remote 并锁死 push

如果 remote 不存在才添加；如果存在，先比较 URL，不一致就停止：

```bash
git remote get-url <remote-name>
git remote add <remote-name> <upstream-url>  # 仅 remote 不存在时
```

无论 remote 是否新建，都设置并核对不可用的 push URL：

```bash
git remote set-url --push <remote-name> DISABLED
git remote get-url --push <remote-name>
```

输出必须精确为 `DISABLED`。不要用“团队约定不推送”替代这道技术保护。

确认默认分支，不假设是 `main`：

```bash
git ls-remote --symref <remote-name> HEAD
git fetch --prune <remote-name> <default-branch>
git rev-parse --verify <remote-name>/<default-branch>^{commit}
```

### 3. 核实上游子树、SHA 和目录外依赖

对每个目标逐一运行：

```bash
git cat-file -e <remote>/<branch>:skills/<name>/SKILL.md
git ls-tree -r --name-only <remote>/<branch> -- skills/<name>
git show <remote>/<branch>:skills/<name>/SKILL.md | sed -n '1,40p'
```

不存在 `SKILL.md`、目录为空或发现目录本身是符号链接时停止。

预检目录外依赖：

```bash
git grep -nE '\]\((\.\./|/)' <remote>/<branch> -- 'skills/<name>/*.md'
git ls-tree -r --name-only <remote>/<branch> -- LICENSE LICENSE.txt NOTICE requirements.txt pyproject.toml package.json
```

逐项判断 `SKILL.md`/references/scripts 是否引用：

- 上游仓库根许可证或 NOTICE；
- 根级依赖清单、共享脚本或目录外相对链接；
- 未包含在目标子树里的模板、assets 或测试夹具。

不得只拉 `SKILL.md` 后假定依赖完整。需要附带文件时，先向用户列出并扩大**精确路径清单**；不能用整个仓库兜底。

### 4. 脏工作树门槛与差异预览

目标路径必须干净：

```bash
git status --short --untracked-files=all -- skills/<name>
git diff -- skills/<name>
git diff --cached -- skills/<name>
```

任一输出非空就停止，说明是未提交修改、暂存修改还是未跟踪文件。无关路径可以保持原状，但同步前后都要保存 `git status --short` 快照，用于识别意外副作用。

对本地已有目标展示差异：

```bash
git diff --stat HEAD <remote>/<branch> -- skills/<name>
git diff HEAD <remote>/<branch> -- skills/<name>
```

如果来源索引称“镜像”，实际却出现 starter 独有逻辑、测试或版本号，升级为“派生版”处理。

### 5. 创建不可冲突的时间/SHA 备份

先解析确定的 upstream commit：

```bash
UPSTREAM_SHA=$(git rev-parse <remote>/<branch>^{commit})
SHORT_SHA=$(git rev-parse --short=12 <remote>/<branch>^{commit})
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
BACKUP_ROOT=".starter-backups/${STAMP}-${SHORT_SHA}"
mkdir -p "$BACKUP_ROOT"
```

每个本地已有目标使用 `cp -a`，保留隐藏文件、权限和符号链接属性：

```bash
cp -a "skills/<name>" "$BACKUP_ROOT/<name>"
```

写入 `$BACKUP_ROOT/MANIFEST.txt`，至少记录：UTC 时间、remote、fetch URL、branch、完整 upstream SHA、本地 `HEAD` SHA、目标列表和每个目标的来源类型。确认 `.gitignore` 已精确忽略 `.starter-backups/`。

新 Skill 没有本地目录，不伪造内容备份，但仍写 manifest，以便审计新增来源。

### 6A. 新增或镜像：精确 checkout

只有“新增”和再次确认无本地补丁的“镜像”可以执行：

```bash
git checkout <remote>/<branch> -- skills/<name>
```

一次可以列多个已确认同类型目标，但每个路径都必须显式写出。禁止：

```bash
git checkout <remote>/<branch> -- skills/
```

### 6B. 派生版：候选导出和定向合并

派生版不直接 checkout。导出上游候选到临时目录：

```bash
CANDIDATE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/skill-sync.XXXXXX")
git archive <remote>/<branch> skills/<name> | tar -x -C "$CANDIDATE_DIR"
diff -ruN "skills/<name>" "$CANDIDATE_DIR/skills/<name>" || true
```

根据本地基线、当前本地版和 upstream 候选做三方判断，只定向合并确认需要的文件或补丁。对 `skill-manager` 必须复验 DEC-020、DEC-034 对应的失败传播、registry 迁移、内容差异识别和回滚测试仍存在；不能用“随后再补”作为覆盖理由。

### 7. 验证依赖、结构和实际行为

先限定目标检查：

```bash
find skills/<name> -type l -print
git diff --name-status -- skills/<name>
git diff --cached --name-status -- skills/<name>
python3 scripts/check_skills.py
python3 scripts/check_links.py
```

- 新 Skill 出现符号链接时停止并调查其目标，不提交机器本地路径。
- `license`、目录 `LICENSE.txt`、上游根许可证/NOTICE 和 `docs/SOURCE-INDEX.md` 必须相互一致。
- 运行该 Skill 自带的测试、代表性脚本正常路径和错误路径；只有静态文件时说明无法验证的行为边界。

最后运行项目门禁：

```bash
STRICT_LINKS=1 STRICT_SH_SYNTAX=1 STRICT_SKILL_YAML=1 bash scripts/check.sh
```

检查同步前后状态快照，允许变化仅限点名 Skill、明确附带的依赖文件和本次确实需要同步的项目文档。

### 8. 失败回退

不要在原路径上覆盖式回拷。先把失败候选移入同一备份根，再恢复：

```bash
mkdir -p "$BACKUP_ROOT/failed-current"
mv "skills/<name>" "$BACKUP_ROOT/failed-current/<name>"
cp -a "$BACKUP_ROOT/<name>" "skills/<name>"  # 本地原先存在时
git restore --staged -- "skills/<name>"
```

新增 Skill 原先不存在时，只把失败候选移到 `failed-current/`，再执行 `git restore --staged -- "skills/<name>"` 清除新增的 index 记录。回退后重新运行目标状态检查和严格门禁。

备份不自动删除；由维护者确认交付稳定后再决定是否清理。

### 9. 文档和报告

只同步事实变化影响的现有文档：

- `docs/SOURCE-INDEX.md`：来源、baseline/upstream SHA、许可证、本地补丁与核对日期；
- `CHANGELOG.md`：用户可见的新增或升级结果；
- `docs/DECISIONS.md`：只有真的形成新的长期同步取舍时才记录；
- `README.md`：仅新 Skill 进入公开资源导航时更新。

报告必须包含：

- 每个目标的新增/镜像/派生分类；
- remote、branch、完整 upstream SHA；
- 实际变更文件和保留的本地补丁；
- 备份目录、manifest 和精确恢复方式；
- 运行过的测试、命令输出摘要与 `NOT_VERIFIED`；
- 任何意外副作用及处理结果。

## 停止条件速查

| 情况 | 处理 |
|---|---|
| remote URL 与用户指定不一致 | 停止，不改 remote |
| push URL 不是 `DISABLED` | 停止，不 fetch/checkout |
| 上游无 `SKILL.md` 或目标不存在 | 停止，报告重命名/删除可能性 |
| 目标路径脏 | 停止，保留用户改动 |
| 来源分类不清或发现本地独有补丁 | 按派生版处理 |
| 目录外依赖未列入精确路径 | 停止，先补依赖清单 |
| `skill-manager` 被要求整目录覆盖 | 拒绝，改走候选导出与定向合并 |
| 严格检查或代表性行为失败 | 回退并保留失败候选 |
