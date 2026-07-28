#!/bin/bash

# Skill & Command Manager - Update Script
# 更新已安装的 skills，支持两条路径：
#   1. 本地 .git 仓库        → git pull（用户手动 git clone 安装的 skill）
#   2. 无 .git 但有注册表记录 → 从远程来源重新下载覆盖（install.sh 删除 .git 后的回退路径）
# 注意：符号链接的 skills/commands 会自动与源同步，无需更新

ITEM_NAME="$1"
ORIGINAL_PWD="$PWD"
# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANAGER_DIR="$(dirname "$SCRIPT_DIR")"
TARGET_HELPER="$SCRIPT_DIR/target.sh"
REGISTRY_FILE="$MANAGER_DIR/assets/skill-registry.json"

# 读取 SKILL.md 中的 version 字段（POSIX 兼容；不依赖 GNU grep -P）
# 用法：read_skill_version <path/to/SKILL.md>
read_skill_version() {
    local skill_md="$1"
    if [ -z "$skill_md" ] || [ ! -f "$skill_md" ]; then
        return 0
    fi
    # 仅取第一处匹配；兼容 "1.2.3" / '1.2.3' / 1.2.3 / 带前后空格
    sed -nE 's/^[[:space:]]*version:[[:space:]]*["'\''"]?([0-9][0-9.]*)["'\''"]?.*/\1/p' "$skill_md" 2>/dev/null | head -n1
}

# 从注册表（skill-registry.json）读取一个字段
# 用法：get_meta_field <skill_name> <field_name>
# 输出空串表示无记录或字段为空；注册表不存在时也输出空串
get_meta_field() {
    local name="$1"
    local field="$2"
    if [ -z "$name" ] || [ -z "$field" ] || [ ! -f "$REGISTRY_FILE" ]; then
        return 0
    fi
    if ! command -v python3 >/dev/null 2>&1; then
        return 0
    fi
    command python3 -c '
import json, sys
from pathlib import Path
reg_path = Path(sys.argv[1])
name = sys.argv[2]
field = sys.argv[3]
try:
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    entry = data.get(name) or {}
    val = entry.get(field)
    print("" if val is None else val)
except Exception:
    print("")
' "$REGISTRY_FILE" "$name" "$field" 2>/dev/null
}

# 更新记录函数
record_update() {
    local skill_name="$1"
    local old_version="$2"
    local new_version="$3"

    if command -v python3 &> /dev/null; then
        RECORD_SCRIPT="$SCRIPT_DIR/record.py"
        if [ -f "$RECORD_SCRIPT" ]; then
            python3 "$RECORD_SCRIPT" update "$skill_name" --from "$old_version" --to "$new_version" 2>/dev/null || true
        fi
    fi
}

if [ -f "$TARGET_HELPER" ]; then
    # shellcheck source=target.sh
    source "$TARGET_HELPER"
else
    echo "❌ 错误: 找不到目标目录识别模块: $TARGET_HELPER"
    exit 1
fi

SCRIPT_AGENT_DIR="$(find_agent_config_dir "$MANAGER_DIR" "$PWD/.claude")"
AGENT_DIR="$(find_agent_config_dir "$ORIGINAL_PWD" "$SCRIPT_AGENT_DIR")"
SKILLS_DIR="$AGENT_DIR/skills"

if [ ! -d "$SKILLS_DIR" ]; then
    echo "❌ 错误: $SKILLS_DIR 目录不存在"
    exit 1
fi

# 路径 1：本地 .git → git pull（与原逻辑兼容）
update_via_git() {
    local skill_path="$1"
    local skill_name
    skill_name=$(basename "$skill_path")

    echo "▶ 更新 (git): $skill_name"

    cd "$skill_path" || return 1

    # 记录更新前的版本
    local old_version
    old_version=$(read_skill_version "$skill_path/SKILL.md")

    git fetch -q origin 2>/dev/null || {
        echo "  ❌ 无法获取更新（git fetch 失败）"
        cd - > /dev/null || return 1
        echo ""
        return 1
    }
    local local_rev remote_rev
    local_rev=$(git rev-parse HEAD)
    remote_rev=$(git rev-parse '@{u}' 2>/dev/null)

    if [ "$local_rev" != "$remote_rev" ] && [ -n "$remote_rev" ]; then
        git pull -q

        local new_version
        new_version=$(read_skill_version "$skill_path/SKILL.md")
        echo "  ✓ 已更新 ($old_version → $new_version)"
        record_update "$skill_name" "$old_version" "$new_version"
    else
        echo "  ○ 已是最新"
    fi

    cd - > /dev/null || return 0
    echo ""
    return 0
}

# 路径 2：无 .git，但注册表里有远程来源 → 重新下载覆盖
# 适用：install.sh 用 GitHub 来源安装时已删除 .git 的 skill
update_via_registry() {
    local skill_path="$1"
    local skill_name
    skill_name=$(basename "$skill_path")

    local remote_url branch subpath
    remote_url=$(get_meta_field "$skill_name" "remote_url")
    [ -z "$remote_url" ] && remote_url=$(get_meta_field "$skill_name" "source")
    branch=$(get_meta_field "$skill_name" "install_branch")
    [ -z "$branch" ] && branch="main"
    subpath=$(get_meta_field "$skill_name" "remote_subpath")

    if [ -z "$remote_url" ]; then
        echo "⚠ 跳过: $skill_name 既无 .git 也无远程来源记录（无法更新）"
        echo "   如需重新安装: skill-manager install <source>"
        echo ""
        return 1
    fi

    echo "▶ 更新 (远程): $skill_name"
    echo "  来源: $remote_url"
    [ -n "$subpath" ] && echo "  子路径: $subpath"
    echo "  分支: $branch"

    local tmp_dir clone_name
    tmp_dir=$(mktemp -d)
    clone_name="$skill_name"

    # 与 install.sh 一致的克隆策略：有 subpath 用 sparse checkout，否则整仓克隆
    if [ -n "$subpath" ]; then
        cd "$tmp_dir" || { rm -rf "$tmp_dir"; return 1; }
        git init -q
        git remote add origin "$remote_url"
        git config core.sparseCheckout true
        echo "$subpath" > .git/info/sparse-checkout
        if ! git fetch --depth 1 origin "$branch" -q 2>/dev/null; then
            echo "  ❌ 无法获取更新（git fetch 失败）"
            cd - > /dev/null || return 1
            rm -rf "$tmp_dir"
            echo ""
            return 1
        fi
        git checkout "$branch" -q
        if [ "$tmp_dir/$subpath" != "$tmp_dir/$clone_name" ]; then
            mv "$tmp_dir/$subpath" "$tmp_dir/$clone_name"
        fi
        cd - > /dev/null || return 0
    else
        if ! git clone --depth 1 -q -b "$branch" "$remote_url" "$tmp_dir/$clone_name" 2>/dev/null; then
            echo "  ❌ 无法获取更新（git clone 失败）"
            rm -rf "$tmp_dir"
            echo ""
            return 1
        fi
    fi

    # 版本号相同 → 视为已是最新；不同或缺失 → 覆盖更新
    local old_version new_version
    old_version=$(read_skill_version "$skill_path/SKILL.md")
    new_version=$(read_skill_version "$tmp_dir/$clone_name/SKILL.md")

    if [ -n "$old_version" ] && [ -n "$new_version" ] && [ "$old_version" = "$new_version" ]; then
        echo "  ○ 已是最新 (v$new_version)"
        rm -rf "$tmp_dir"
        echo ""
        return 0
    fi

    # 备份旧目录、覆盖为新版本；与 install.sh 保持一致：安装后不带 .git
    rm -rf "$tmp_dir/$clone_name/.git"
    if [ -d "$skill_path" ]; then
        rm -rf "${skill_path}.backup"
        mv "$skill_path" "${skill_path}.backup"
        echo "  (旧版本已备份至 ${skill_path}.backup)"
    fi
    cp -R "$tmp_dir/$clone_name" "$skill_path"
    rm -rf "$tmp_dir"

    echo "  ✓ 已更新 ($old_version → $new_version)"
    record_update "$skill_name" "$old_version" "$new_version"
    echo ""
    return 0
}

# 统一入口：按 skill 类型分派到对应更新路径
update_skill() {
    local skill_path="$1"

    # 符号链接：自动同步（外层循环也会跳过，这里兜底）
    if [ -L "$skill_path" ]; then
        echo "ℹ $(basename "$skill_path") 是符号链接，会自动与源同步，无需更新"
        echo ""
        return 0
    fi

    # 路径 1：本地 .git 仓库（用户手动 git clone 装的）
    if [ -d "$skill_path/.git" ]; then
        update_via_git "$skill_path"
        return $?
    fi

    # 路径 2：回退到注册表远程来源（install.sh GitHub 安装会走到这里）
    update_via_registry "$skill_path"
}

if [ -z "$ITEM_NAME" ]; then
    # 更新所有 skills
    echo "🔄 更新所有 skills..."
    echo ""
    echo "注意: 符号链接的 skills/commands 会自动与源同步，无需手动更新"
    echo ""

    count=0
    for item in "$SKILLS_DIR"/*; do
        [ -e "$item" ] || continue   # 空目录通配保护
        [ -L "$item" ] && continue   # 符号链接跳过
        if [ -d "$item" ]; then
            update_skill "$item"
            count=$((count + 1))
        fi
    done

    if [ "$count" -eq 0 ]; then
        echo "没有需要更新的 skills"
    else
        echo "✓ 更新完成，共检查 $count 个 skills"
    fi
else
    # 更新指定 skill
    TARGET_PATH="$SKILLS_DIR/$ITEM_NAME"

    if [ ! -e "$TARGET_PATH" ]; then
        echo "❌ 错误: Skill '$ITEM_NAME' 不存在"
        exit 1
    fi

    if [ -L "$TARGET_PATH" ]; then
        echo "ℹ '$ITEM_NAME' 是符号链接，会自动与源同步，无需手动更新"
        echo "   指向: $(readlink "$TARGET_PATH")"
        exit 0
    fi

    if [ ! -d "$TARGET_PATH" ]; then
        echo "❌ 错误: '$ITEM_NAME' 不是目录，无法更新"
        exit 1
    fi

    update_skill "$TARGET_PATH"
    echo "✓ 更新完成"
fi
