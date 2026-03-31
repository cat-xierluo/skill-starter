# 提交到 GitHub 与 Commit 规范

这篇文档解决的是：

**你已经会改文件了，接下来怎样把改动规范地提交、推送到 GitHub。**

---

## 1. 先记住最小闭环

日常最常见的流程就是这 6 步：

```text
改文件
  ↓
git status
  ↓
git diff
  ↓
git add
  ↓
git commit
  ↓
git push
```

如果是多人协作，再多两步：

```text
git push
  ↓
Open PR
  ↓
Review / Merge
```

---

## 2. 每次提交前先做这 3 个检查

### `git status`

看哪些文件改了，哪些文件已经进入暂存区。

```bash
git status
```

### `git diff`

看还没有暂存的改动。

```bash
git diff
```

### `git diff --staged`

看准备提交的内容到底是什么。

```bash
git diff --staged
```

很多“我怎么把不该提交的东西也交上去了”，就是因为跳过了这一步。

---

## 3. 新手最稳妥的提交流程

```bash
git status
git diff
git add README.md docs/guide.md
git diff --staged
git commit -m "docs: 补充 Git 提交流程说明"
git push
```

如果是第一次推某个分支：

```bash
git push -u origin 分支名
```

---

## 4. Commit message 到底怎么写

推荐用这种格式：

```text
type: 一句话说明改了什么
```

常用 `type`：

- `feat`: 新功能
- `fix`: 修复问题
- `docs`: 文档更新
- `refactor`: 重构
- `chore`: 杂项维护
- `test`: 测试相关

示例：

```text
feat: 新增天气播报示例 Skill
fix: 修复模板中的相对路径错误
docs: 补充 AGENTS 与 CLAUDE 入门说明
refactor: 收敛参考资料目录命名规则
chore: 更新仓库协作文档状态
```

---

## 5. 什么样的 commit message 算差

不推荐：

```text
update
fix bug
改一下
提交
final
```

这些问题都一样：

- 看不出改了什么
- 看不出改动类型
- 以后回头翻历史几乎没价值

---

## 6. 什么样的 commit message 算够用

够用的标准不是“文采很好”，而是：

- 一眼知道改动类型
- 一眼知道改动对象
- 一眼知道这次提交的大致范围

例如：

```text
docs: 重写 GitHub 入门文档中的认证流程
feat: 为模板增加 TASKS 与 DECISIONS 文件
fix: 修复 skill-template 脚本输出路径
```

---

## 7. 一次提交里应该放多少东西

推荐原则：

**一次提交只表达一件主要事情。**

例如：

- 只改文档，单独一个 `docs` 提交
- 只修路径错误，单独一个 `fix` 提交
- 只新增示例 Skill，单独一个 `feat` 提交

不推荐把这些混在一次提交里：

- 改了教程
- 改了脚本
- 改了模板
- 顺手重构一堆旧文件

这样 review 很难看，回退也很难做。

---

## 8. 一个推荐的分支与提交节奏

如果你要做一个小功能，可以这样：

```bash
git switch -c feature/add-context-guide
```

开发过程中：

```bash
git add 03-AI协作与上下文/03-上下文工程入门.md
git commit -m "docs: 新增上下文工程入门指南"
```

如果后面又补了一篇 Rules 教程：

```bash
git add 03-AI协作与上下文/04-Rules-编写指南.md
git commit -m "docs: 补充 Rules 编写指南"
```

最后推到 GitHub：

```bash
git push -u origin feature/add-context-guide
```

---

## 9. 提交到 GitHub 之后做什么

单人项目：

- 推上去就行
- 至少确认 GitHub 页面看得到改动

协作项目：

- 开 Pull Request
- 写清楚改动、原因和验证方式
- 等 review 再合并

一个够用的 PR 描述：

```text
## 改动
- 新增上下文工程入门
- 新增 Rules 编写指南
- 更新 README 导航

## 原因
- 补齐基础教程中的上下文工程部分

## 验证
- 相对链接检查通过
- README 导航已更新
```

---

## 10. 新手最容易犯的错误

### 错误 1：不看 diff 就提交

结果常常是把 `.env`、临时文件、无关格式化一起交上去。

### 错误 2：一口气 `git add .`

不是永远不能用，但新手更稳妥的做法是先指定文件。

### 错误 3：commit message 太随便

短期看省事，长期看非常难维护。

### 错误 4：直接在 `main` 上乱改

尤其是多人协作时，很容易把主分支搞乱。

### 错误 5：push 之后不检查

本地成功不等于 GitHub 页面上就是你想要的结果。

---

## 11. 推荐实践

1. 每次提交前先看 `git status`
2. 每次提交前都看一遍 `git diff --staged`
3. commit message 使用 `type: summary`
4. 一次提交只做一件主要事情
5. 推送后去 GitHub 页面确认分支和文件都对

---

## 12. 建议继续读

- [Git 入门](./01-Git-入门.md)
- [GitHub 入门](./02-GitHub-入门.md)
- [SSH 配置](./03-SSH-配置.md)
- [上下文工程入门](../03-AI协作与上下文/03-上下文工程入门.md)

---

## 一句话总结

规范提交不是为了“显得专业”，而是为了让你自己、你的队友和未来的 AI 都能看懂项目历史。
