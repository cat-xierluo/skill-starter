# GitHub 账号与环境配置

本篇帮助你从零开始配置 GitHub 开发环境，包括账号注册、Git 安装、SSH Key 配置和连接验证。

---

## 1. 注册 GitHub 账号

### 步骤

1. **访问 GitHub**
   打开浏览器，访问 [https://github.com](https://github.com)

2. **填写注册信息**
   - **邮箱**（推荐使用 Gmail 或企业邮箱）
   - **密码**（建议 12 位以上，包含大小写和数字）
   - **用户名**（Username，将成为你的 GitHub 地址，如 `github.com/yourname`，谨慎选择，之后可改）

3. **验证邮箱**
   GitHub 会向你的邮箱发送验证链接，点击链接完成验证

4. **选择计划**
   选择 **Free** 计划（足够个人开发使用，私有仓库也无限制）

### 📸 截图位置说明

- 注册表单截图：放在 `images/setup/github-signup-form.png`
- 邮箱验证截图：放在 `images/setup/github-verify-email.png`
- 计划选择截图：放在 `images/setup/github-choose-plan.png`

> **提示**：截图建议使用 `Cmd+Shift+4`（macOS）或 `Win+Shift+S`（Windows）快速截取。

---

## 2. 配置 Git

### 什么是 Git？

Git 是一个**版本控制系统**，用来追踪文件的修改历史、协同多人开发。GitHub 是基于 Git 的代码托管平台。

### 安装 Git

**macOS：**
```bash
# 方式一：使用 Homebrew（推荐）
brew install git

# 方式二：检查是否已安装
git --version
```

**Windows：**
下载安装包：[https://git-scm.com/download/win](https://git-scm.com/download/win)

**Linux（Ubuntu/Debian）：**
```bash
sudo apt update && sudo apt install git
```

### 基础配置

安装完成后，设置你的身份信息（**必须**，每次提交时会用到）：

```bash
# 设置用户名（建议与 GitHub 用户名一致）
git config --global user.name "你的 GitHub 用户名"

# 设置邮箱（建议与注册 GitHub 的邮箱一致）
git config --global user.email "your@email.com"

# 查看所有配置
git config --list
```

### 📸 截图位置说明

- Git 安装成功验证截图：放在 `images/setup/git-install-success.png`
- 配置命令执行截图：放在 `images/setup/git-config.png`

---

## 3. 生成 SSH Key 并添加到 GitHub

### 什么是 SSH Key？

SSH Key 是一种加密方式，让你的电脑与 GitHub 之间建立安全连接，而不需要每次输入用户名和密码。

### 生成 SSH Key

```bash
# 生成新的 SSH Key（使用 RSA 算法，邮箱与 GitHub 注册邮箱一致）
ssh-keygen -t ed25519 -C "your@email.com"
```

执行后会提示：

```
Generating public/private ed25519 key pair.
Enter file in which to save key (/Users/you/.ssh/id_ed25519):   # 直接回车
Enter passphrase (empty for no passphrase):                     # 输入密码（可留空）
Enter same passphrase again:                                    # 确认密码
```

> **推荐**： passphrase 留空，直接回车跳过。否则每次 push 都需输入密码。

### 查看生成的公钥

```bash
# 查看公钥内容
cat ~/.ssh/id_ed25519.pub
```

输出类似：
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBLABLABLABLABLABLABLABLABLABLABLABLAB your@email.com
```

### 将公钥添加到 GitHub

1. 登录 GitHub，点击右上角头像 → **Settings**
2. 左侧菜单选择 **SSH and GPG keys**
3. 点击 **New SSH key**
4. 填写：
   - **Title**：给这个 key 起个名字（如 `MacBook Pro`）
   - **Key type**：保持默认
   - **Key**：粘贴刚才 `cat` 命令输出的公钥内容（以 `ssh-ed25519` 开头）
5. 点击 **Add SSH key**

### 📸 截图位置说明

- GitHub SSH Key 添加页面截图：放在 `images/setup/github-ssh-key-add.png`
- New SSH Key 表单截图：放在 `images/setup/github-ssh-key-form.png`

---

## 4. 验证连接是否成功

### 测试 SSH 连接

```bash
ssh -T git@github.com
```

首次连接会看到以下提示（输入 `yes` 回车）：

```
The authenticity of host 'github.com (20.200.245.246)' can't be established.
RSA key fingerprint is SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8.
Are you sure you want to continue connecting (yes/no)?
```

输入 `yes`，正常情况下会看到：

```
Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
```

看到这行字说明**连接成功**！

### 如果失败了

1. 检查公钥是否正确复制（不要漏掉开头的 `ssh-`）
2. 检查 GitHub SSH Key 页面是否已添加该公钥
3. 重新生成一次 SSH Key：
   ```bash
   rm ~/.ssh/id_ed25519*    # 删除旧 key
   ssh-keygen -t ed25519 -C "your@email.com"   # 重新生成
   cat ~/.ssh/id_ed25519.pub   # 重新复制公钥
   ```

---

## ✅ 下一步

环境配置完成后，你可以：

- [克隆项目到本地](./CLONE-PUSH.md)
- [创建分支进行开发](./BRANCH-PR.md)

