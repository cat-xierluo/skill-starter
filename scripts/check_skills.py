#!/usr/bin/env python3
"""检查 skills/ 下每个 Skill 的结构完整性。

必需项（error，缺失则失败）：
- SKILL.md 存在
- SKILL.md frontmatter 含 name 和 description

推荐项（warn，缺失仅告警）：
- CHANGELOG.md
- LICENSE.txt

用法：python3 scripts/check_skills.py
退出码：0 必需项全齐，1 有必需项缺失
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")
FRONTMATTER_KV = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$")
RECOMMENDED_FILES = ("CHANGELOG.md", "LICENSE.txt")
REQUIRED_FIELDS = ("name", "description")


def parse_frontmatter(content):
    """提取 YAML frontmatter 中的顶层 key（只关心 key 是否存在）。"""
    if not content.startswith("---"):
        return set()
    end = content.find("\n---", 3)
    if end == -1:
        return set()
    fm = content[3:end]
    keys = set()
    for line in fm.splitlines():
        m = FRONTMATTER_KV.match(line)
        if m and not line.startswith((" ", "\t", "-")):
            keys.add(m.group(1))
    return keys


def main():
    if not os.path.isdir(SKILLS_DIR):
        print("❌ skills/ 目录不存在")
        sys.exit(1)

    skills = sorted(
        d for d in os.listdir(SKILLS_DIR)
        if os.path.isdir(os.path.join(SKILLS_DIR, d)) and not d.startswith(".")
    )

    errors, warns = [], []
    for name in skills:
        path = os.path.join(SKILLS_DIR, name)
        skill_md = os.path.join(path, "SKILL.md")
        if not os.path.isfile(skill_md):
            errors.append(f"skills/{name}/ 缺少 SKILL.md")
            continue
        try:
            with open(skill_md, encoding="utf-8") as fh:
                keys = parse_frontmatter(fh.read())
        except (OSError, UnicodeDecodeError):
            errors.append(f"skills/{name}/SKILL.md 读取失败")
            continue
        for field in REQUIRED_FIELDS:
            if field not in keys:
                errors.append(f"skills/{name}/SKILL.md frontmatter 缺少 {field}")
        for rec in RECOMMENDED_FILES:
            if not os.path.isfile(os.path.join(path, rec)):
                warns.append(f"skills/{name}/ 缺少推荐文件 {rec}")

    print(f"检查了 {len(skills)} 个 skill：{', '.join(skills)}")
    for w in warns:
        print(f"⚠️  {w}")
    if errors:
        print(f"❌ 发现 {len(errors)} 个必需项缺失：")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    print("✅ 所有 skill 必需项完整")


if __name__ == "__main__":
    main()
