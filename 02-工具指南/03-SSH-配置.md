# SSH 配置

如果你打算长期在自己的电脑上使用 GitHub，通常推荐配 SSH。

它解决的是：

**你的本地电脑如何安全地和 GitHub 建立可信连接。**

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

## 官方资料

- GitHub 官方 SSH 文档：[Adding a new SSH key to your GitHub account](https://docs.github.com/authentication/connecting-to-github-with-ssh)

## 一句话总结

SSH 配置的目标不是“生成一个神秘文件”，而是：

**让你的电脑成为 GitHub 认可的可信设备。**
