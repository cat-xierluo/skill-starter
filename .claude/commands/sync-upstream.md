# Sync Skills from Upstream

把仓库根目录 `skills/` 下的某些 skill 与一个上游只读 remote 同步最新内容,支持两种模式:

- **同步已有 skill**:本地已经有同名 skill,upstream 有更新,覆盖式拉取最新版。
- **拉取新 skill**:本地没有,upstream 有,把它新增到本地仓库。

典型场景:从 `cat-xierluo/legal-skills` 同步 `git-batch-commit`、`skill-manager` 等通用 skill,或从中拉取 `subtree-publish`、`cross-agent-coordination` 等新 skill。

## 触发场景

- "从 legal-skills 同步最新的 git-batch-commit"
- "帮我 cherry-pick 这几个 skill"
- "把 legal-skills 的 skill-manager 拉过来"
- "从 legal-skills 拉一个新 skill:subtree-publish"
- "跨仓库拉一批文件过来"

## 执行流程

按顺序执行,任何一步出问题先停下来问用户,不要擅自跳步。

### 1. 确认 upstream remote

- 如果已经存在 `<remote-name>` 指向目标 upstream,跳过。
- 否则:
  ```bash
  git remote add <remote-name> <upstream-url>
  git fetch <remote-name> <default-branch>
  ```
- **坑**:upstream 默认分支可能是 `main` 而不是 `master`。先用 `git remote show <remote-name>` 或 `git ls-remote --symref <remote-name> HEAD` 确认,不要假设。

### 2. 核实 upstream 实际有什么 + 拆分两种模式

**这一步不能跳过**。盲目拉取会把整个 `skills/` 目录连同符号链接一起拉过来。

```bash
git ls-tree -d --name-only <remote-name>/<default-branch> skills/
```

向用户列出 upstream 实际有的 skill,把请求拆成两组:

- **已有同步组**:本地 `skills/<name>` 存在,且 upstream 也有 → 走第 3 步"备份"和第 4 步"覆盖拉取"。
- **新拉取组**:本地 `skills/<name>` 不存在,但 upstream 有 → 跳过第 3 步"备份",直接走第 4b 步"新增拉取"。

如果用户请求的 skill 在 upstream 中**根本不存在**,停下来告知用户,可能是上游重命名 / 删除 / 用户记错名字。

### 3. 备份本地版本

把每个本地同名 skill 复制到仓库根的 `.starter-backups/<name>/`(或 `<backup-dir>/<name>/`,**不要放在 `skills/` 内**)。

```bash
mkdir -p .starter-backups
for skill in <list-of-local-skills-to-backup>; do
  cp -R "skills/$skill" ".starter-backups/$skill"
done
```

**坑**:`.gitignore` 里加上 `<backup-dir>/` 防止备份目录被 commit。备份目录**必须**放在 Claude Code 扫描 `SKILL.md` 的范围之外,否则 Claude 会把备份目录里的旧 `SKILL.md` 当作可用 skill 加载,污染触发词。

### 4. 精确拉取

```bash
git checkout <remote-name>/<default-branch> -- skills/<skill-a> skills/<skill-b> ...
```

只列要同步的子目录,不要写整个 `skills/`。`git checkout <ref> -- <paths>` 是跨仓库取子树的正确方式;真正的 `git cherry-pick` 不能用,因为独立仓库没有 common ancestor。

等价写法:

| 命令 | 效果 |
|---|---|
| `git checkout <ref> -- <paths>` | 覆盖 index + 工作区 |
| `git read-tree <ref> -- <paths>` | 只更新 index |
| `git restore --source=<ref> <paths>` | 只恢复工作区 |

### 4b. 新增拉取(新 skill 模式)

只对**新拉取组**生效,已有同步组跳过本节。

```bash
# 拉取
git checkout <remote-name>/<default-branch> -- skills/<new-skill>

# 验证 SKILL.md 完整
head -20 skills/<new-skill>/SKILL.md

# 看目录结构
find skills/<new-skill> -maxdepth 2 -type f
```

检查点:

- `SKILL.md` 的 frontmatter 有 `name` 和 `description`
- 目录结构合理(`scripts/`、`references/`、`assets/` 至少有一个或可为空)
- 文件**不是符号链接**(如果是符号链接,说明 upstream 用了本地路径别名,**不要拉**,告知用户)

### 5. 检查意外副作用

```bash
git status
```

重点关注三类异常:

- **意外的 `D` 状态**:HEAD 跟踪但工作目录缺失的文件(可能是 commit message 与实际改动不符,或本地 hook 副作用)。用 `git checkout HEAD -- <paths>` 从 HEAD 恢复。
- **意外的 `??` 文件**:不在备份里、也不在 upstream 里的游离文件,通常是临时工具产物。**先看内容再决定**,简单的占位文件可以直接 `rm`。
- **`UU`/`AA`/`DD` 冲突标记**:几乎不会出现(因为是覆盖式拉取),出现说明 HEAD 与 upstream 都有改动,需要手动解决。

新拉取组还会出现 `A skills/<new-skill>/...` 状态,这正是预期的新增文件。

### 6. 登记同步约定 + 新 skill 入库(必做)

在 `AGENTS.md` 的"上游同步文件"约定里追加本次同步的 skill 列表,明确:

- 哪个 remote / branch 是来源
- 同步命令
- 哪些 skill 是同步自 upstream,哪些是仓库原创

**对新拉取组额外要做**:

- 把新 skill 加进 `README.md` 项目结构小节,标注"同步自 <upstream>"
- 如果新 skill 有 `LICENSE.txt`,确认 `SKILL.md` 的 `license` 字段与之一致
- 在 `CHANGELOG.md` 新增一个 `0.x.0` 段落记录此次拉取

### 7. 报告

向用户总结:

- 同步了哪些 skill,版本号变化
- 备份位置和恢复命令(`mv .starter-backups/<name> skills/<name>`)
- 任何意外副作用及处理方式

## 备份恢复命令

```bash
# 完整恢复某个 skill
rm -rf skills/<name>
mv .starter-backups/<name> skills/<name>

# 仅恢复某个文件
cp .starter-backups/<name>/<path> skills/<name>/<path>
```

备份目录**不保证**包含 `CLAUDE.md` 等嵌套文件(它们可能在备份前就已从工作目录缺失),恢复时如果 `git status` 还显示 `D`,用 `git checkout HEAD -- <path>` 兜底。

## 已知坑点速查

| 坑 | 现象 | 解法 |
|---|---|---|
| 默认分支不是 master | `git fetch <remote> master` 报 "couldn't find remote ref" | `git remote show <remote>` 先查 |
| 拉整个 `skills/` | 把 50+ skill + 符号链接全拉过来 | `git ls-tree` 核实后再写路径 |
| 备份放在 `skills/` 内 | 备份的旧 SKILL.md 被 Claude 误识别 | 备份放到 `.starter-backups/` 等扫描范围外 |
| 嵌套 CLAUDE.md 突然 `D` | commit message 与实际改动不符,HEAD 仍跟踪 | `git checkout HEAD -- <path>` 恢复 |
| 真正的 `cherry-pick` 失败 | 独立仓库没有 common ancestor | 改用 `git checkout <ref> -- <paths>` |