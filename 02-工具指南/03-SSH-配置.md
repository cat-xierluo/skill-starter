# SSH 配置

如果你打算长期在自己的电脑上使用 GitHub，通常推荐配 SSH。

它解决的是：

**你的本地电脑如何安全地和 GitHub 建立可信连接。**

## 本篇目标

读完这篇，你能：

- 说清 SSH 用「一对密钥」代替反复输密码 / Token 是怎么回事，公钥和私钥各放在哪
- 在 macOS / Windows Git Bash / Linux 上生成一对 `ed25519` 密钥，并把公钥加到 GitHub
- 用 `ssh -T git@github.com` 验证连接成功
- 把一个仓库的 remote 从 HTTPS 改成 SSH，让 `git push/pull` 走 SSH
- 在 `~/.ssh/config` 里给多个 GitHub 账号配不同密钥

## 前置知识

先看 [Git 入门](./01-Git-入门.md) 和 [GitHub 入门](./02-GitHub-入门.md)：本篇默认你已经有 GitHub 账号、本地装好了 Git，并且知道 `git remote` 是连本地和远程的那根线。命令示例标注了 macOS / Windows Git Bash / Linux 的差异。

## 什么是 SSH

SSH 是一种安全连接协议。

在 GitHub 场景里，你可以把它简单理解成：

> 用一对密钥，代替反复输密码或 Token。

## 为什么推荐 SSH

- 日常 `pull/push` 更顺手
- 不需要每次输入 Token
- 长期开发体验更稳定

## 第一步：检查是否已有密钥

```bash
ls -al ~/.ssh
```

如果你已经看到类似文件：

- `id_ed25519`
- `id_ed25519.pub`

说明你可能已经有 SSH key 了。

## 第二步：生成新的 SSH key

推荐使用 `ed25519`。

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

生成过程中会问你几件事：

### 保存位置

一般直接回车，用默认路径：

```text
~/.ssh/id_ed25519
```

### passphrase

可以理解成“给私钥再加一层密码”。

建议：

- 自己长期使用的电脑，最好设置
- 临时环境可按需决定

## 第三步：启动 ssh-agent 并加载密钥

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

如果你设置了 passphrase，这里会提示输入。

## 第四步：复制公钥

公钥文件通常是：

```text
~/.ssh/id_ed25519.pub
```

### macOS

```bash
pbcopy < ~/.ssh/id_ed25519.pub
```

### Windows Git Bash

```bash
clip < ~/.ssh/id_ed25519.pub
```

### Linux

```bash
cat ~/.ssh/id_ed25519.pub
```

然后手动复制输出内容。

## 第五步：把公钥添加到 GitHub

GitHub 页面路径通常是：

1. 右上角头像
2. `Settings`
3. `SSH and GPG keys`
4. `New SSH key`

填写时：

- `Title`：写机器名，例如 `MacBook-Air`
- `Key type`：认证用途
- `Key`：粘贴刚才复制的公钥

然后保存。

## 第六步：验证连接

```bash
ssh -T git@github.com
```

第一次连接时，可能会提示你确认主机：

```text
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

输入：

```text
yes
```

如果成功，通常会看到类似信息：

```text
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

这表示认证已经成功。

## 第七步：确认仓库 remote 用的是 SSH

查看当前仓库 remote：

```bash
git remote -v
```

如果你看到的是：

```text
https://github.com/用户名/仓库名.git
```

说明当前还是 HTTPS。

改成 SSH：

```bash
git remote set-url origin git@github.com:用户名/仓库名.git
```

## 多账号怎么配

如果你有多个 GitHub 账号，可以在 `~/.ssh/config` 里分开配置。

示例：

```sshconfig
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
```

这样第二个账号的仓库地址可以写成：

```bash
git@github-work:用户名/仓库名.git
```

## 常见问题

### 1. `Permission denied (publickey)`

最常见。

按这个顺序检查：

1. 公钥是否真的添加到 GitHub
2. 当前 remote 是否是 SSH
3. `ssh-agent` 是否加载了密钥
4. 是否推错了 GitHub 账号

### 2. 我明明配了 SSH，为什么还是走 HTTPS

因为仓库 remote URL 还是 HTTPS。

执行：

```bash
git remote -v
```

确认后再用 `git remote set-url origin ...` 改掉。

### 3. 每次开新终端都要重新输 passphrase

这通常和本地的 agent 或钥匙串设置有关。

最小处理办法：

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 4. `Host key verification failed`

通常是本机记录的 GitHub 主机信息有冲突，或者第一次连接没确认好。

这种情况先不要乱删文件，优先确认：

- 你连接的是不是真的 `github.com`
- 网络环境是否正常

## 新手推荐实践

1. 一台长期开发机器用一把清晰命名的 SSH key
2. 不要把私钥发给任何人
3. 公钥可以上传，私钥绝不能泄露
4. 配完后先用 `ssh -T git@github.com` 验证
5. 再去 clone / push

## 自测题

照着做完一遍算过关。

1. **生成并加公钥**：生成一对 `ed25519` 密钥，用 `pbcopy`（macOS）/ `clip`（Windows Git Bash）/ `cat`（Linux）把**公钥**复制出来，加到 GitHub 的 `SSH and GPG keys`。
2. **验证连接**：执行 `ssh -T git@github.com`，看到 `Hi <用户名>! You've successfully authenticated` 那一行；第一次连接时正确回应主机确认提示。
3. **切到 SSH**：挑一个现有仓库，`git remote -v` 看到是 HTTPS，用 `git remote set-url` 改成 SSH，再做一次 `git pull` 不再要求输 Token。
4. **分清公私钥**：说出 `id_ed25519`（私钥）和 `id_ed25519.pub`（公钥）分别该放哪——哪个绝对不能发给别人、哪个要上传到 GitHub。

> 验收：第 2 题看到成功认证提示；第 3 题改完 remote 后 `git pull` / `git push` 不再提示输密码或 Token。

## 官方资料

- GitHub 官方 SSH 文档：[Adding a new SSH key to your GitHub account](https://docs.github.com/authentication/connecting-to-github-with-ssh)

## 下一篇

SSH 配好后，认证这条路就通了，接下来可以把改动规范地提交、推送到 GitHub。

继续看 [提交到 GitHub 与 Commit 规范](./04-提交到-GitHub-与-Commit-规范.md)：它会给你一套照着用就够的 commit message 写法和「一次提交只做一件事」的节奏。

> 推送之后想进入协作流程（PR、Review、合并），再看 [GitHub PR 与 Code Review](./05-GitHub-PR-与-Code-Review.md)；其它工具篇随时可从 [README](../README.md) 回查。

## 一句话总结

SSH 配置的目标不是“生成一个神秘文件”，而是：

**让你的电脑成为 GitHub 认可的可信设备。**
