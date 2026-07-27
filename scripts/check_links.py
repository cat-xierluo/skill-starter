#!/usr/bin/env python3
"""检查仓库内所有 Markdown 文件的相对链接是否指向真实存在的文件。

抓两类问题：
- 幽灵链接：[text](../xxx.md) 指向不存在的文件（如被删除的示例 skill）
- 命名漂移：链接里的目录名与实际目录不符

外部链接（http/https/mailto）和纯锚点（#xxx）跳过。
符号链接目录不递归（followlinks=False），避免 .claude/skills 与 skills/ 重复扫描。

用法：python3 scripts/check_links.py
退出码：0 全部有效，1 存在断链
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", ".starter-backups", "output", "__pycache__", "node_modules"}
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "ftp://", "ftps://")


def iter_md_files():
    """遍历仓库内所有 .md 文件，剪枝排除目录，不跟随符号链接。"""
    for dirpath, dirnames, filenames in os.walk(ROOT, followlinks=False):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.endswith(".md"):
                yield os.path.join(dirpath, fname)


def link_target_exists(md_file, target):
    """判断 markdown 链接目标是否存在。"""
    target = target.split("#", 1)[0].strip()  # 去掉锚点
    if not target:
        return True  # 纯锚点，视为有效
    if target.startswith(EXTERNAL_PREFIXES):
        return True  # 外部链接，跳过
    base = os.path.dirname(md_file)
    resolved = os.path.normpath(os.path.join(base, target))
    return os.path.exists(resolved)


def main():
    errors = []
    checked = 0
    for md in iter_md_files():
        try:
            with open(md, encoding="utf-8") as fh:
                content = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        rel_md = os.path.relpath(md, ROOT)
        for lineno, line in enumerate(content.splitlines(), 1):
            for _text, target in LINK_RE.findall(line):
                if not target or target.startswith(EXTERNAL_PREFIXES):
                    continue
                if target.startswith("#"):
                    continue
                checked += 1
                if not link_target_exists(md, target):
                    errors.append(f"  {rel_md}:{lineno} → {target}")

    print(f"检查了 {checked} 个 Markdown 相对链接")
    if errors:
        print(f"❌ 发现 {len(errors)} 处断链：")
        for e in errors:
            print(e)
        sys.exit(1)
    print("✅ 所有 Markdown 相对链接有效")


if __name__ == "__main__":
    main()
