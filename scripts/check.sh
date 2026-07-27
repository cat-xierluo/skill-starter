#!/bin/bash
# skill-starter 仓库自检：Markdown 断链检查 + Skill 完整性检查
#
# 建议在提交前运行：
#   bash scripts/check.sh
#
# 退出码：0 全部通过，1 存在失败项

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
cd "$ROOT" || exit 1

FAIL=0

if ! command -v python3 &>/dev/null; then
    echo "❌ 需要 Python 3"
    exit 1
fi

echo "=== 1/2 Markdown 相对链接检查 ==="
python3 "$SCRIPT_DIR/check_links.py" || FAIL=1

echo ""
echo "=== 2/2 Skill 完整性检查 ==="
python3 "$SCRIPT_DIR/check_skills.py" || FAIL=1

echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "✅ 全部检查通过"
else
    echo "❌ 存在失败项，请修复后再提交"
fi
exit "$FAIL"
