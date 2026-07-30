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
    local install_commit="${4:-}"
    local remote_url="${5:-}"
    local install_branch="${6:-}"
    local remote_subpath="${7:-}"

    if command -v python3 &> /dev/null; then
        RECORD_SCRIPT="$SCRIPT_DIR/record.py"
        if [ -f "$RECORD_SCRIPT" ]; then
            local args=(update "$skill_name" --from "$old_version" --to "$new_version")
            [ -n "$install_commit" ] && args+=(--install-commit "$install_commit")
            [ -n "$remote_url" ] && args+=(--remote-url "$remote_url")
            [ -n "$install_branch" ] && args+=(--install-branch "$install_branch")
            [ -n "$remote_subpath" ] && args+=(--remote-subpath "$remote_subpath")
            if ! python3 "$RECORD_SCRIPT" "${args[@]}" >/dev/null 2>&1; then
                echo "  ⚠️  Skill 已更新，但注册表写入失败"
                return 1
            fi
        fi
    fi
    return 0
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
        if ! git pull -q; then
            echo "  ❌ 拉取更新失败（git pull）"
            cd "$ORIGINAL_PWD" >/dev/null 2>&1 || true
            echo ""
            return 1
        fi

        local new_version
        new_version=$(read_skill_version "$skill_path/SKILL.md")
        echo "  ✓ 已更新 ($old_version → $new_version)"
        if ! record_update "$skill_name" "$old_version" "$new_version" "$remote_rev"; then
            cd "$ORIGINAL_PWD" >/dev/null 2>&1 || true
            echo ""
            return 1
        fi
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

    local remote_url branch recorded_branch subpath installed_commit
    remote_url=$(get_meta_field "$skill_name" "remote_url")
    [ -z "$remote_url" ] && remote_url=$(get_meta_field "$skill_name" "source")
    branch=$(get_meta_field "$skill_name" "install_branch")
    recorded_branch="$branch"
    [ -z "$branch" ] && branch="main"
    subpath=$(get_meta_field "$skill_name" "remote_subpath")
    installed_commit=$(get_meta_field "$skill_name" "install_commit")

    # 兼容 1.5.0 旧注册表：当 remote_url 错误保存为 GitHub /tree/ 或 /blob/
    # 网页地址时，拆回可克隆仓库 URL + branch + subpath。新安装不会再写入这种格式。
    if [[ "$remote_url" =~ ^(https?://github\.com/[^/]+/[^/]+)(\.git)?/(tree|blob)/(.+)$ ]]; then
        local legacy_tail legacy_branch legacy_subpath
        legacy_tail="${BASH_REMATCH[4]}"
        remote_url="${BASH_REMATCH[1]}"
        if [ -n "$recorded_branch" ] && [[ "$legacy_tail" == "$recorded_branch/"* ]]; then
            # 已记录的 branch 可以消除 feature/name/path 中 ref 与 subpath 的歧义。
            legacy_branch="$recorded_branch"
            legacy_subpath="${legacy_tail#"$recorded_branch/"}"
        else
            legacy_branch="${legacy_tail%%/*}"
            legacy_subpath="${legacy_tail#*/}"
        fi
        [ -z "$recorded_branch" ] && branch="$legacy_branch"
        [ -z "$subpath" ] && subpath="$legacy_subpath"
        echo "  ℹ 已兼容迁移旧式 GitHub 子目录来源记录"
    fi

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

    local tmp_dir clone_dir source_dir candidate_dir remote_commit
    if ! tmp_dir=$(mktemp -d); then
        echo "  ❌ 无法创建临时目录"
        echo ""
        return 1
    fi
    clone_dir="$tmp_dir/repository"
    candidate_dir="$tmp_dir/candidate"

    # 与 install.sh 一致：子目录使用 sparse checkout，整仓直接浅克隆。
    if [ -n "$subpath" ]; then
        mkdir -p "$clone_dir"
        if ! (
            cd "$clone_dir" &&
            git init -q &&
            git remote add origin "$remote_url" &&
            git config core.sparseCheckout true &&
            printf '%s\n' "$subpath" > .git/info/sparse-checkout &&
            git fetch --depth 1 origin "$branch" -q 2>/dev/null &&
            git checkout --detach FETCH_HEAD -q
        ); then
            echo "  ❌ 无法获取更新（git fetch 失败）"
            rm -rf "$tmp_dir"
            echo ""
            return 1
        fi
        source_dir="$clone_dir/$subpath"
    else
        if ! git clone --depth 1 -q -b "$branch" "$remote_url" "$clone_dir" 2>/dev/null; then
            echo "  ❌ 无法获取更新（git clone 失败）"
            rm -rf "$tmp_dir"
            echo ""
            return 1
        fi
        source_dir="$clone_dir"
    fi

    remote_commit=$(git -C "$clone_dir" rev-parse HEAD 2>/dev/null || true)
    if [ ! -d "$source_dir" ] || { [ ! -f "$source_dir/SKILL.md" ] && [ ! -f "$source_dir/skill.md" ]; }; then
        echo "  ❌ 远程来源中找不到有效 Skill: ${subpath:-仓库根目录}"
        rm -rf "$tmp_dir"
        echo ""
        return 1
    fi
    if ! cp -R "$source_dir" "$candidate_dir"; then
        echo "  ❌ 无法准备候选版本（复制失败）"
        rm -rf "$tmp_dir"
        echo ""
        return 1
    fi
    rm -rf "$candidate_dir/.git"

    local old_version new_version
    old_version=$(read_skill_version "$skill_path/SKILL.md")
    new_version=$(read_skill_version "$candidate_dir/SKILL.md")

    # commit 相同并不足以证明本地目录没被改动，因此最终以目录内容为准。
    # 这也覆盖“版本号未提升但上游内容已变化”的场景。
    if diff -qr "$skill_path" "$candidate_dir" >/dev/null 2>&1; then
        if [ -n "$remote_commit" ] && [ "$installed_commit" != "$remote_commit" ]; then
            if ! record_update "$skill_name" "$old_version" "$new_version" "$remote_commit" "$remote_url" "$branch" "$subpath"; then
                rm -rf "$tmp_dir"
                echo ""
                return 1
            fi
            echo "  ○ 内容已是最新，已刷新 commit 记录"
        else
            echo "  ○ 已是最新${new_version:+ (v$new_version)}"
        fi
        rm -rf "$tmp_dir"
        echo ""
        return 0
    fi

    # 先把完整候选版本复制到目标同一文件系统，再切换目录；任何准备失败都不触碰旧 Skill。
    local stage_root stage_skill backup_path
    if ! stage_root=$(mktemp -d "${skill_path}.update.XXXXXX"); then
        echo "  ❌ 无法在目标目录旁创建更新暂存区"
        rm -rf "$tmp_dir"
        echo ""
        return 1
    fi
    stage_skill="$stage_root/$skill_name"
    if ! cp -R "$candidate_dir" "$stage_skill"; then
        echo "  ❌ 无法写入更新暂存区；原 Skill 未改变"
        rm -rf "$stage_root" "$tmp_dir"
        echo ""
        return 1
    fi

    backup_path="${skill_path}.backup.$(date +%Y%m%d%H%M%S).$$"
    if ! mv "$skill_path" "$backup_path"; then
        echo "  ❌ 无法备份当前 Skill；更新已取消"
        rm -rf "$stage_root" "$tmp_dir"
        echo ""
        return 1
    fi
    if ! mv "$stage_skill" "$skill_path"; then
        echo "  ❌ 无法启用候选版本，正在恢复原 Skill"
        mv "$backup_path" "$skill_path" 2>/dev/null || {
            echo "  ❌ 自动恢复失败，原版本保留在: $backup_path"
        }
        rm -rf "$stage_root" "$tmp_dir"
        echo ""
        return 1
    fi
    rm -rf "$stage_root" "$tmp_dir"

    echo "  ✓ 已更新 ($old_version → $new_version)"
    echo "  (旧版本已备份至 $backup_path)"
    if ! record_update "$skill_name" "$old_version" "$new_version" "$remote_commit" "$remote_url" "$branch" "$subpath"; then
        echo ""
        return 1
    fi
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
    success_count=0
    fail_count=0
    for item in "$SKILLS_DIR"/*; do
        [ -e "$item" ] || continue   # 空目录通配保护
        [ -L "$item" ] && continue   # 符号链接跳过
        if [ -d "$item" ]; then
            count=$((count + 1))
            if update_skill "$item"; then
                success_count=$((success_count + 1))
            else
                fail_count=$((fail_count + 1))
            fi
        fi
    done

    if [ "$count" -eq 0 ]; then
        echo "没有需要更新的 skills"
    else
        echo "更新检查完成：成功 ${success_count}，失败 ${fail_count}，共 ${count} 个 skills"
    fi
    if [ "$fail_count" -gt 0 ]; then
        exit 1
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

    if update_skill "$TARGET_PATH"; then
        echo "✓ 更新检查完成"
    else
        echo "❌ 更新失败: $ITEM_NAME"
        exit 1
    fi
fi
