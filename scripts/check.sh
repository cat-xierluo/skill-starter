#!/bin/bash
# skill-starter 仓库自检：脚本语法检查 + Markdown 链接检查 + Skill 完整性检查
#
# 建议在提交前运行：
#   bash scripts/check.sh
#
# 退出码：0 全部通过（warn 允许），1 存在 error 级失败项

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
cd "$ROOT" || exit 1

FAIL=0

if ! command -v python3 &>/dev/null; then
    echo "❌ 需要 Python 3"
    exit 1
fi

echo "=== 1/3 脚本语法检查 ==="
# 设计权衡：
# - .py 必须能编译（error，失败则整体 FAIL）：本次升级新增/修改的 Python 脚本是核心，
#   数量少、易修复，编译失败必须阻断提交。
# - .sh 仅做语法告警（warn，不阻断）：仓库中存在历史遗留的 shell 语法问题
#   （如 skills/skill-manager/scripts/update.sh 单引号内嵌单引号导致 bash -n 报错），
#   修复需要超出自检脚本的文件域。为避免新校验上线即把现有 skill 全挂掉，先以 warn 暴露，
#   后续单独治理。若想切回严格模式，导出 STRICT_SH_SYNTAX=1 即可。
STRICT_SH="${STRICT_SH_SYNTAX:-0}"
sh_failed=0
sh_warns=0
sh_count=0
py_count=0
while IFS= read -r -d '' f; do
    sh_count=$((sh_count + 1))
    if ! err_out=$(bash -n "$f" 2>&1); then
        sh_warns=$((sh_warns + 1))
        echo "$err_out" | sed 's/^/    /'
        if [ "$STRICT_SH" = "1" ]; then
            echo "  ❌ $f bash 语法错误（严格模式）"
            sh_failed=1
        else
            echo "  ⚠️  $f bash 语法错误（warn，不阻断；STRICT_SH_SYNTAX=1 可切严格）"
        fi
    fi
done < <(find "$ROOT" -type f -name "*.sh" -not -path "*/.git/*" \
         -not -path "*/.starter-backups/*" -not -path "*/node_modules/*" \
         -print0)

py_failed=0
while IFS= read -r -d '' f; do
    py_count=$((py_count + 1))
    if ! python3 -m py_compile "$f" 2>/dev/null; then
        echo "  ❌ $f Python 语法错误"
        py_failed=1
    fi
done < <(find "$ROOT" -type f -name "*.py" -not -path "*/.git/*" \
         -not -path "*/.starter-backups/*" -not -path "*/node_modules/*" \
         -not -path "*/__pycache__/*" -print0)

echo "  检查了 $sh_count 个 .sh（$sh_warns 个语法 warn）、$py_count 个 .py"
if [ "$py_failed" -ne 0 ] || [ "$sh_failed" -ne 0 ]; then
    FAIL=1
fi

echo ""
echo "=== 2/3 Markdown 相对链接检查 ==="
# 与 .sh 语法检查同样的权衡：仓库存在历史断链（如 docs/SOURCE-INDEX.md
# 引用了未创建的 LICENSE-PLAN.md），修复需超文件域。默认 STRICT_LINKS=0
# 时仅 warn 不阻断；想强制严格，导出 STRICT_LINKS=1。
STRICT_LINKS="${STRICT_LINKS:-0}"
link_out=$(python3 "$SCRIPT_DIR/check_links.py" 2>&1)
link_rc=$?
echo "$link_out"
if [ "$link_rc" -ne 0 ]; then
    if [ "$STRICT_LINKS" = "1" ]; then
        echo "  ❌ 链接检查存在 error（严格模式）"
        FAIL=1
    else
        echo "  ⚠️  链接检查存在 error（warn，不阻断；STRICT_LINKS=1 可切严格）"
    fi
fi

echo ""
echo "=== 3/3 Skill 完整性检查 ==="
python3 "$SCRIPT_DIR/check_skills.py" || FAIL=1

echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "✅ 全部检查通过"
else
    echo "❌ 存在失败项，请修复后再提交"
fi
exit "$FAIL"
