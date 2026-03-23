# 克隆与提交

本篇讲解如何把 GitHub 上的项目下载到本地，以及如何保存（commit）你的修改并上传（push）到云端。

---

## 1. 什么是 Clone？为什么需要？

### 类比理解

想象你在网上看到一本好书（GitHub 上的项目），**Clone 就是把这本书完整复印一本放到你家里（本地电脑）**。

- 你可以在家随时阅读和修改（不影响原书）
- 修改完后可以把新版本寄回去（Push）

### 为什么需要 Clone？

| 场景 | 说明 |
|------|------|
| 下载完整项目 | 把别人或自己仓库的代码完整下载到本地 |
| 离线工作 | 没有网络时也能查看和编辑代码 |
| 本地开发 | 在本地运行、调试、测试代码 |
| 协作开发 | 参与开源项目，先 clone 再提交修改 |

---

## 2. 如何 Clone 一个项目到本地

### 获取仓库地址

在 GitHub 仓库页面，点击绿色的 **Code** 按钮，复制 **SSH** 地址（前提是已配置 SSH Key）：

```
git@github.com:username/repository.git
```

### 执行 Clone

```bash
# 替换为你想克隆的仓库地址
git clone git@github.com:username/repository.git

# 例如：克隆 skills-starter 项目
git clone git@github.com:cat-xierluo/skills-starter.git
```

Clone 完成后，项目会出现在当前目录下的一个新文件夹里：

```
当前目录/
└── skills-starter/   # 新文件夹
    ├── README.md
    ├── SKILL-DEV-GUIDE.md
    └── ...
```

### 进入项目目录

```bash
cd skills-starter          # 进入项目目录
git status                  # 查看当前状态
```

---

## 3. 什么是 Commit？

### 类比理解

**Commit = 拍照** 📸

每次 `commit` 就像给项目的当前状态拍了一张照片，并附上说明（"这次改了什么"）。

- **可以后悔**：之后可以从任意一个"拍照点"重新开始
- **有记录**：谁在什么时候改了什么，一目了然
- **不会丢**：即使电脑坏了，照片在云端（GitHub）

### Commit 的生命周期

```
工作目录 → git add（暂存）→ git commit（保存快照）→ git push（上传云端）
   ↓
你的修改文件    标记要保存的文件      真正生成一个"版本"
```

---

## 4. 如何 Commit（git add + git commit）

### 第一步：查看当前状态

```bash
git status
```

常见输出：

```
On branch main
Changes not staged for commit:
  modified:   README.md        # 已修改但未暂存
  deleted:    SKILL.md         # 已删除但未暂存
Untracked files:
  new-feature.js               # 新文件，未被 Git 追踪
```

### 第二步：git add（暂存文件）

**暂存单个文件：**
```bash
git add README.md
```

**暂存所有修改：**
```bash
git add .          # 暂存所有改动（包括新文件、修改、删除）
```

**只暂存修改的文件（不包括新文件）：**
```bash
git add -u
```

### 第三步：git commit（提交保存）

```bash
# 基本格式
git commit -m "提交说明"

# 实际例子
git commit -m "修复了登录页面的按钮样式问题"
```

### 完整的提交流程示例

```bash
# 1. 查看状态
git status

# 2. 暂存要提交的文件
git add README.md

# 3. 提交（生成一个版本快照）
git commit -m "更新了 README 的安装步骤"

# 4. 查看提交历史（确认提交成功）
git log
```

### 📸 截图位置说明

- git status 输出截图：放在 `images/clone-push/git-status-output.png`
- git commit 成功截图：放在 `images/clone-push/git-commit-success.png`
- git log 历史截图：放在 `images/clone-push/git-log-output.png`

---

## 5. 什么是 Push？

### 类比理解

**Push = 寄快递** 📦

Commit 只是把"照片"存在你家里的相册（本地），**Push 是把这张照片寄到云端相册（GitHub）**，让其他人也能看到。

### 为什么需要 Push？

- **备份**：本地硬盘坏了，云端还有
- **共享**：其他人可以看到你的修改
- **协作**：你 push 的代码可以被别人 pull 下去

---

## 6. 如何 Push（git push）

### 首次 Push（设置上游分支）

```bash
git push -u origin main
```

解释：
- `origin`：远程仓库的默认名称（你 clone 的那个地址）
- `main`：分支名（也可能是 `master`，取决于仓库设置）
- `-u`：记住这个对应关系，以后直接 `git push` 即可

### 后续 Push

```bash
# 之后每次 push 只需要
git push
```

### 完整示例

```bash
# 1. 修改文件后，查看状态
git status

# 2. 暂存所有修改
git add .

# 3. 提交，并写明做了什么
git commit -m "添加了新功能：用户注册表单"

# 4. 推送到 GitHub
git push

# 5. 在 GitHub 仓库页面刷新，确认看到新提交
```

### 遇到 Push 失败？

常见原因和解决方法：

| 问题 | 解决方法 |
|------|----------|
| 需要登录认证 | 配置 SSH Key（参考 [SETUP.md](./SETUP.md)） |
| 远程有更新，本地落后 | 先 `git pull` 拉取最新代码，再 push |
| 分支名不存在 | 检查分支名是否正确：`git branch` |

```bash
# 如果远程有更新，先拉取再推送
git pull origin main
git push origin main
```

---

## 🔄 完整工作流程回顾

```bash
# 1. 克隆项目到本地（首次）
git clone git@github.com:username/repo.git

# 2. 进入项目目录
cd repo

# 3. 修改文件...

# 4. 查看修改内容
git status

# 5. 暂存修改
git add .

# 6. 提交（生成版本快照）
git commit -m "描述这次改了什么"

# 7. 推送到云端
git push
```

---

## ✅ 下一步

掌握克隆和提交后，下一篇学习如何用**分支**来安全地进行多人协作：

- [分支与 Pull Request](./BRANCH-PR.md)

