# GitHub 入门

这篇文档面向第一次真正使用 GitHub 的人。

目标只有一个：

**让你从“只有账号”走到“能创建仓库、连接本地、提交代码”。**

## 第一步：注册并完成基础设置

1. 打开 [GitHub](https://github.com)
2. 注册账号
3. 验证邮箱
4. 补头像和基本资料

邮箱验证这一步很重要。很多 GitHub 功能在未验证邮箱时会受限。

## 第二步：创建你的第一个仓库

登录后：

1. 点击右上角 `+`
2. 选择 `New repository`
3. 填写仓库名
4. 选择 `Public` 或 `Private`
5. 点击 `Create repository`

### 仓库名建议

- 简洁
- 小写
- 用连字符分词

例如：

- `skill-starter`
- `weekly-weather-briefing`
- `legal-text-format`

## 第三步：选认证方式

你把本地 Git 和 GitHub 连起来，通常有 2 种方式。

### 方式 A：SSH

适合：

- 你自己的长期开发电脑
- 日常频繁 `push/pull`

优点：

- 配一次后比较顺手
- 不需要每次输入 Token

建议阅读：

- [SSH 配置](./03-SSH-配置.md)

### 方式 B：HTTPS + Token

适合：

- 临时环境
- 某些公司网络或机器限制 SSH
- 你明确要走 HTTPS

## GitHub 现在更推荐什么 Token

根据 GitHub 官方文档，日常需要 Token 时，优先使用 **fine-grained personal access token**，而不是旧的 classic token。

原因是：

- 权限更细
- 可限制到指定仓库
- 风险更小

如果你只是日常本地开发，通常更推荐：

1. Git 操作走 SSH
2. API、CLI 或特定 HTTPS 场景再用 fine-grained PAT

## 如果你选择 HTTPS + Token

### 创建 fine-grained PAT

当前 GitHub 页面路径大致是：

1. 右上角头像
2. `Settings`
3. 左侧 `Developer settings`
4. `Personal access tokens`
5. `Fine-grained tokens`
6. `Generate new token`

创建时重点看这几项：

- Token name
- Expiration
- Repository access
- Permissions

### 新手最容易踩的坑

- 选了错误仓库，结果没权限
- 权限开太少，`push` 或 API 调用失败
- Token 没保存，刷新页面后找不到
- 公司组织开启 SSO，需要额外授权

### 如何使用

当你用 HTTPS 方式克隆或推送时，GitHub 不再接受密码，应该使用 Token。

例如：

```bash
git clone https://github.com/用户名/仓库名.git
```

提示输入密码时，填你的 Token。

## 第四步：把仓库和本地连起来

### 情况 1：先在 GitHub 建仓库，再克隆到本地

```bash
git clone git@github.com:用户名/仓库名.git
cd 仓库名
```

如果你走 HTTPS：

```bash
git clone https://github.com/用户名/仓库名.git
cd 仓库名
```

### 情况 2：本地已有项目，再推到 GitHub

```bash
git init
git add .
git commit -m "feat: initial commit"
git branch -M main
git remote add origin git@github.com:用户名/仓库名.git
git push -u origin main
```

如果你走 HTTPS，把 remote URL 换成 HTTPS 地址即可。

如果你想把“本地提交怎么写得更规范、怎么推到 GitHub 更稳”单独补强，继续看：

- [提交到 GitHub 与 Commit 规范](./04-提交到-GitHub-与-Commit-规范.md)

## 第五步：学会最小协作流程

### 单人项目

最小闭环：

1. 本地修改
2. `git add`
3. `git commit`
4. `git push`

### 多人协作

推荐闭环：

1. 拉最新主分支
2. 新建分支
3. 在分支开发
4. 推到 GitHub
5. 开 PR
6. Review
7. 合并

## Pull Request 到底怎么用

当你把分支推到 GitHub 后，页面通常会提示：

`Compare & pull request`

你点进去后，通常需要补 3 类信息：

- 这次改了什么
- 为什么要改
- 有什么需要别人注意

### 一个够用的 PR 描述模板

```text
## 改动
- 新增天气播报脚本
- 更新模板文档

## 原因
- 让 starter 仓库有完整示例

## 验证
- 本地运行脚本通过
- 链接检查通过
```

## GitHub 新手必会页面

### Code

看代码和文件。

### Issues

记问题、任务、需求。

### Pull requests

提合并请求和看 review。

### Settings

配置仓库权限、分支规则、Secrets 等。

## 常见问题

### 1. `remote: Permission to xxx denied`

通常是：

- 你没有仓库权限
- Token 权限不够
- SSH key 没配置好
- 推错账号了

### 2. `Repository not found`

检查：

- 仓库名是否拼错
- 账号是否拼错
- 仓库是不是私有
- 当前账号有没有权限

### 3. `Support for password authentication was removed`

意思是：

**不能再用账号密码推 GitHub 了。**

要么改用 SSH，要么用 Token。

### 4. 为什么我明明 push 了，看不到改动

检查：

- 你推的是不是正确分支
- 当前 GitHub 页面看的是否也是同一分支
- 本地 commit 是否真的成功

## 新手推荐实践

1. 日常开发优先用 SSH
2. 需要 Token 时优先 fine-grained PAT
3. 不要把 Token 提交进仓库
4. 不要直接在主分支乱改
5. 每次 push 前先看 `git status`

## 官方资料

- GitHub 官方认证说明：[About authentication to GitHub](https://docs.github.com/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)
- GitHub 官方 Token 说明：[Managing your personal access tokens](https://docs.github.com/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## 一句话总结

GitHub 入门最重要的不是“记住所有页面”，而是：

**会创建仓库、会连接本地、会安全地提交和协作。**
