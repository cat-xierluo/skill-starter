#!/bin/bash
# skill-starter 仓库自检：脚本静态检查 + 回归测试 + Markdown 链接 + Skill 完整性
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

echo "=== 1/4 脚本语法检查 ==="
# 设计权衡：
# - .py 编译失败必须阻断。
# - .sh 同时运行 bash -n 与 ShellCheck error 级规则；style/warning 级历史项不阻断。
# - 普通本地检查允许 shell 工具缺失或失败只告警；CI 通过 STRICT_SH_SYNTAX=1
#   要求 bash 语法、ShellCheck error 级规则和 ShellCheck 可用性全部通过。
STRICT_SH="${STRICT_SH_SYNTAX:-0}"
sh_failed=0
sh_warns=0
sh_count=0
shellcheck_count=0
shellcheck_failed=0
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

if command -v shellcheck &>/dev/null; then
    while IFS= read -r -d '' f; do
        shellcheck_count=$((shellcheck_count + 1))
        if ! err_out=$(shellcheck --severity=error "$f" 2>&1); then
            echo "$err_out" | sed 's/^/    /'
            if [ "$STRICT_SH" = "1" ]; then
                echo "  ❌ $f ShellCheck error（严格模式）"
                shellcheck_failed=1
            else
                echo "  ⚠️  $f ShellCheck error（warn，不阻断）"
            fi
        fi
    done < <(find "$ROOT" -type f -name "*.sh" -not -path "*/.git/*" \
             -not -path "*/.starter-backups/*" -not -path "*/node_modules/*" \
             -print0)
elif [ "$STRICT_SH" = "1" ]; then
    echo "  ❌ 严格 shell 检查需要 ShellCheck"
    shellcheck_failed=1
else
    echo "  ⚠️  未安装 ShellCheck，仅运行 bash -n"
fi

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

echo "  检查了 $sh_count 个 .sh（$sh_warns 个 bash 语法 warn；$shellcheck_count 个 ShellCheck）、$py_count 个 .py"
if [ "$py_failed" -ne 0 ] || [ "$sh_failed" -ne 0 ] || [ "$shellcheck_failed" -ne 0 ]; then
    FAIL=1
fi

echo ""
echo "=== 2/4 自动化回归测试 ==="
if ! python3 -m unittest discover -s tests -p 'test_*.py'; then
    FAIL=1
fi

echo ""
echo "=== 3/4 Markdown 相对链接检查 ==="
# 普通本地检查保留非阻断模式，便于编辑中随时运行；CI 设置 STRICT_LINKS=1，
# 任何相对断链都必须失败。
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
echo "=== 4/4 Skill 完整性检查 ==="
python3 "$SCRIPT_DIR/check_skills.py" || FAIL=1

echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "✅ 全部检查通过"
else
    echo "❌ 存在失败项，请修复后再提交"
fi
exit "$FAIL"
