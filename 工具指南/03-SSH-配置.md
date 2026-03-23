# SSH 配置

## 什么是 SSH？

SSH（Secure Shell）是一种加密网络协议，用于安全地访问远程服务器和服务。它通过公钥加密技术，在不传输密码的情况下验证身份。

## 为什么需要 SSH？

使用 SSH 连接 GitHub 的好处：
- 🔒 **安全**：不暴露密码
- 🚀 **便捷**：一次配置，长期使用
- 📈 **专业**：开发者标准工作方式

## 生成 SSH Key（Ed25519 算法）

Ed25519 是现代、快速、安全的 SSH 密钥算法，推荐使用。

### 步骤

1. 打开终端（Terminal / Git Bash）

2. 生成密钥
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

3. 当提示 "Enter a file in which to save the key" 时：
```
> Enter a file in which to save the key (/Users/you/.ssh/id_ed25519):
```
直接按 **Enter** 使用默认位置。

4. 设置密码（可选，建议设置）：
```
> Enter passphrase (empty for no passphrase):
> Enter same passphrase again:
```
输入密码并确认。

5. 看到类似输出表示成功：
```
Your public key has been saved in /Users/you/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx your.email@example.com
```

## 添加到 GitHub

1. **复制公钥内容**
```bash
# Mac
pbcopy < ~/.ssh/id_ed25519.pub

# Linux
cat ~/.ssh/id_ed25519.pub
# 手动复制输出内容

# Windows (Git Bash)
clip < ~/.ssh/id_ed25519.pub
```

2. **在 GitHub 添加公钥**
   - 登录 GitHub，点击右上角头像 → **Settings**
   - 左侧菜单点击 **SSH and GPG keys**
   - 点击 **New SSH key**
   - 填写：
     - **Title**：给你的密钥起个名字，如 "MacBook Pro"
     - **Key type**：Authentication Key
     - **Key**：粘贴刚才复制的公钥内容
   - 点击 **Add SSH key**

> 📍 **截图位置**：SSH Keys 页面，绿色 "New SSH key" 按钮

## 验证连接

在终端输入：
```bash
ssh -T git@github.com
```

首次连接会看到：
```
The authenticity of host 'github.com (xx.xx.xx.xx)' can't be established.
RSA key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
Are you sure you want to continue connecting (yes/no)?
```

输入 **yes** 并按 Enter。

看到以下消息表示成功：
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

## 配置多个 SSH Key

如果使用多个 GitHub 账号，创建配置文件 `~/.ssh/config`：

```bash
# ~/.ssh/config

# 默认账号
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

# 第二个账号
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
```

使用非默认账号时，remote URL 需要修改：
```bash
# 普通
git@github.com:username/repo.git

# 使用特定密钥
git@github-work:username/repo.git
```

## 常见问题

### Q: 每次重启终端都需要输入密码？
A: 启动 SSH Agent 并添加密钥：
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Q: Permission denied (publickey)？
A: 检查：
1. 公钥是否正确添加到 GitHub
2. 密钥文件路径是否正确
3. SSH Agent 是否加载了密钥
