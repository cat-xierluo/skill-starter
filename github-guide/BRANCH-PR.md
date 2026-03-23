# 分支与 Pull Request

本篇讲解 Git 分支的概念，以及如何通过 Pull Request（PR）安全地合并代码。

---

## 1. 什么是 Branch（分支）？

### 类比理解

**分支 = 平行世界** 🌳

想象你正在写一本书，突然有了一个新章节的想法——但你不确定这个想法好不好。

- **方案 A**：直接在原书上改（危险，可能改坏）
- **方案 B**：把书复印一份，在副本上写新章节（安全，原书不受影响）
- **合并后**：如果新章节好，就把新章节加回原书

Git 分支就是**方案 B**，让你在不影响主线的情况下安全地尝试新功能。

### 分支的可视化

```
        HEAD (当前位置)
           ↓
  ───●───●───●─── main（主分支）
           │
           └──●─── feature-login（新功能分支）
```

---

## 2. 为什么需要分支？

| 场景 | 不用分支 | 用分支 |
|------|----------|--------|
| 开发新功能 | 可能弄乱正在运行的代码 | 新功能在独立分支，不影响主分支 |
| Bug 修复 | 修复 bug 和开发新功能混在一起 | 分别在各自的分支，互不干扰 |
| 多人协作 | 两个人同时改同一处，冲突难解 | 各自在分支工作，最后合并 |
| 代码审查 | 直接 push 到主分支，无法审核 | PR 发起合并，需 review 通过 |

---

## 3. 如何创建和切换分支

### 查看当前分支

```bash
git branch        # 查看本地所有分支（* 表示当前分支）
```

### 创建新分支

```bash
# 创建分支（但不会自动切换）
git branch feature-login
```

### 切换到新分支

```bash
git checkout feature-login

# 切换后的提示通常类似：
# Switched to branch 'feature-login'
```

### 创建并切换（一行搞定）

```bash
# 创建新分支并立即切换过去（推荐）
git checkout -b feature-login
```

### 新建分支并关联远程

```bash
git checkout -b feature-login
git push -u origin feature-login
```

### 查看分支（包括远程分支）

```bash
git branch -a       # 查看所有分支（本地 + 远程）
```

### 删除分支

```bash
# 删除本地分支（必须在其他分支上才能删除）
git branch -d feature-login

# 强制删除（如果分支还没合并）
git branch -D feature-login
```

---

## 4. 什么是 Pull Request（PR）？

### 类比理解

**Pull Request = 申请把代码合并回去** ✅

就像写完新章节后，向出版社主编提交审稿申请：
1. 你完成了新章节（在分支上开发）
2. 提交合并申请（创建 PR）
3. 主编 review 你的内容（Code Review）
4. 确认没问题后，合并进原书（Merge PR）

### PR 的完整流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    Pull Request 完整流程                      │
└─────────────────────────────────────────────────────────────┘

  开发者                      GitHub                      审查者
    │                           │                            │
    │  1. 从 main 创建分支       │                            │
    │  ──────────────────────►   │                            │
    │       feature-login        │                            │
    │                           │                            │
    │  2. 在分支上开发           │                            │
    │  ──────────────────────►   │                            │
    │       多次 commit          │                            │
    │                           │                            │
    │  3. Push 分支到远程        │                            │
    │  ──────────────────────►   │                            │
    │                           │  仓库出现新分支              │
    │                           │                            │
    │  4. 创建 Pull Request      │                            │
    │  ──────────────────────►   │                            │
    │                           │  通知审查者                  │
    │                           │ ─────────────────────────►  │
    │                           │                            │
    │                           │  5. Review 代码              │
    │                           │ ◄─────────────────────────  │
    │                           │    提出意见/批准              │
    │                           │                            │
    │  6. 根据反馈修改            │                            │
    │  ──────────────────────►   │                            │
    │       更新 PR              │                            │
    │                           │                            │
    │                           │  7. 批准 Merge              │
    │                           │ ◄─────────────────────────  │
    │                           │                            │
    │  8. 分支合并到 main        │                            │
    │                           │  main 分支更新              │
    │                           │                            │
    │  9. 删除功能分支（可选）    │                            │
    │  ──────────────────────►   │                            │
```

### 分支 → PR → 合并的简易流程

```
main 分支 ────●───●───●───●
                 │       ↑
                 │       │
              创建 PR    合并
                 ↓
          feature-login 分支
          ●───●───●───●
          (开发中)
```

---

## 5. 如何创建 PR

### 前提条件

1. 已将分支 push 到 GitHub
2. 在 GitHub 仓库页面

### 步骤

**方法一：在 GitHub 网站上创建**

1. 推送分支到 GitHub 后，页面顶部会出现一条提示：
   > **Compare & pull request**（Compare and pull request）
2. 点击该按钮
3. 填写 PR 信息：
   - **Title**：PR 标题，简洁描述这次改了什么
   - **Description**：详细说明（改了什么、为什么改、怎么测试）
4. 选择 reviewers（审查者，可选）
5. 点击 **Create pull request**

**方法二：使用命令行创建草稿 PR**

```bash
# 安装 GitHub CLI（可选）
brew install gh

# 登录
gh auth login

# 创建 PR（自动打开编辑器填写信息）
gh pr create --base main --head feature-login
```

### PR 模板示例

```markdown
## 描述
<!-- 简述这次 PR 做了什么 -->

## 改动内容
<!-- 列出具体改动 -->
- 新增用户登录页面
- 添加登录表单验证
- 集成 JWT token

## 测试方式
<!-- 如何验证这些改动 -->
1. 运行 `npm test`
2. 手动测试登录流程

## 截图（如有 UI 改动）
<!-- 附上截图 -->
```

---

## 6. 如何 Review PR

### 作为审查者

1. **打开 PR 页面**
   进入 GitHub 仓库 → **Pull requests** → 选择要 review 的 PR

2. **查看文件改动**
   点击 **Files changed**，查看每一行代码的增删

3. **添加评论**
   - 点击行号旁的 `+` 按钮添加单行评论
   - 或在 PR 正文添加整体评论

4. **提交 Review**
   - **Comment**：只评论，不阻止合并
   - **Approve**：批准，可以合并
   - **Request changes**：要求修改，不能直接合并

### 评论语法示例

```markdown
<!-- 单行评论示例 -->
这个函数名可以更清晰，建议改为 `getUserById`

<!-- 多行评论示例 -->
这个实现有个问题：
1. 没有处理空数组的情况
2. 边界条件可能导致异常

建议：
```javascript
if (!Array.isArray(data) || data.length === 0) {
  return [];
}
```
```

### 作为开发者（回复 Review）

```bash
# 1. 根据反馈修改代码
git checkout feature-login
# ... 修改代码 ...

# 2. 提交修改
git add .
git commit -m "根据 review 反馈优化代码"
git push
```

### 合并 PR

审查通过后，点击 **Merge pull request** → **Confirm merge**

PR 合并后，**记得删除功能分支**（不再需要了）：
- 页面会有提示删除分支
- 或命令行：
  ```bash
  git checkout main
  git pull origin main          # 拉取最新代码
  git branch -d feature-login  # 删除本地分支
  ```

---

## 📋 命令速查

```bash
# 分支操作
git branch                          # 查看本地分支
git branch -a                       # 查看所有分支
git checkout -b feature-name        # 创建并切换到新分支
git checkout main                   # 切换到主分支
git branch -d feature-name          # 删除本地分支

# 推送分支
git push -u origin feature-name     # 首次推送并关联

# 合并分支（需要先切换到目标分支）
git checkout main
git merge feature-name

# 查看分支状态
git log --oneline --graph --all     # 可视化分支图
```

---

## ✅ 下一步

掌握分支和 PR 后，来快速查阅常用命令：

- [命令速查表](./CHEATSHEET.md)

