# GitHub 入门

## 注册 GitHub 账号

1. 访问 https://github.com
2. 点击 **Sign up**（注册）
3. 填写邮箱、密码、用户名
4. 验证邮箱完成注册

> 📍 **截图位置**：注册页面右上角有 "Sign up" 按钮

## 登录 GitHub

1. 访问 https://github.com
2. 点击 **Sign in**
3. 输入用户名/邮箱和密码

> 📍 **截图位置**：登录页面输入框

## 创建 Personal Access Token

Personal Access Token 是让本地电脑安全连接 GitHub 的方式。

### 步骤

1. 点击右上角头像 → **Settings**
   > 📍 **截图位置**：右上角头像下拉菜单

2. 左侧菜单找到 **Developer settings**（最底部）
   > 📍 **截图位置**：Settings 左侧菜单

3. 点击 **Personal access tokens** → **Generate new token (classic)**
   > 📍 **截图位置**：Developer settings 页面

4. 设置 Token 名称和过期时间
   - **Note**：给 Token 起个名字，如 "my-laptop"
   - **Expiration**：选择过期时间，建议 30 天或 90 天

5. 勾选权限（Scopes）
   - ✅ **repo** - 完整访问私有仓库
   - ✅ **workflow** - 管理 GitHub Actions

6. 点击 **Generate token**
   > 📍 **截图位置**：页面底部的绿色按钮

7. **重要**：立即复制 Token 保存到安全的地方！
   - 页面刷新后 Token 将无法再次查看
   > 📍 **截图位置**：绿色 Token 显示区域

## Token 存储到本地

### Windows (Git Bash / CMD)

```bash
# 方式 1：环境变量（推荐）
# 在 ~/.bashrc 或 ~/.zshrc 添加：
export GITHUB_TOKEN="github_pat_xxxxxxxxxxxx"

# 方式 2：Git Credential Storage
git config --global credential.helper store
# 下次 push 时会提示输入用户名和 Token
```

### Mac / Linux

```bash
# 方式 1：环境变量
export GITHUB_TOKEN="github_pat_xxxxxxxxxxxx"

# 方式 2：Git Credential Storage
git config --global credential.helper osxkeychain  # Mac
git config --global credential.helper store         # Linux
```

### 验证连接

```bash
# 用 Token 克隆一个私有仓库测试
git clone https://github.com/用户名/仓库名
# 输入用户名：你的 GitHub 用户名
# 密码：粘贴你的 Personal Access Token
```

## 注意事项

- ❌ **不要**把 Token 提交到 Git 仓库
- ❌ **不要**把 Token 发给别人
- ✅ Token 泄露后立即在 GitHub Settings → Developer settings → Personal access tokens 中撤销
- ✅ 定期更新 Token
