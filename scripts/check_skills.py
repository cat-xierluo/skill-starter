#!/usr/bin/env python3
"""检查 skills/ 下每个 Skill 的结构完整性（标准 YAML 版）。

YAML 解析模式：
- 优先模式：若环境可用 PyYAML，则用 ``yaml.safe_load`` 解析 frontmatter，
  字段类型、引号、多行（``|`` / ``>``）等完全遵循 YAML 1.1/1.2 规范。
- 兜底模式：若 PyYAML 未安装，使用本文件内置的极简 frontmatter 解析器
  （支持顶层 ``key: value``、单/双引号字符串、``|`` / ``|``- / ``>`` / ``>-``
  块字面量），覆盖现有 skill 全部写法。

普通本地检查允许在 PyYAML 缺失时使用 fallback；设置
``STRICT_SKILL_YAML=1`` 后，PyYAML 缺失或 YAML 语法错误都会失败。只要
PyYAML 已安装，其解析错误就不会再被 fallback 掩盖。

校验规则：
- error（必需项缺失 → 退出码 1）
  * SKILL.md 存在
  * frontmatter 含 ``name`` 且非空
  * frontmatter 含 ``description`` 且非空
- warn（推荐项不达标，仅告警不影响退出码）
  * ``name`` 与目录名一致
  * ``name`` 字符合法（小写字母 / 数字 / 连字符）且长度 ≤ 64
  * ``description`` 非空且长度 > 10 字符
  * 许可证：有 ``license`` 字段 或 目录下有 ``LICENSE.txt``
  * 推荐文件 ``CHANGELOG.md`` / ``LICENSE.txt`` 存在

兼容 Claude / Codex / OpenClaw 扩展字段（``homepage`` / ``author`` /
``version`` 等），不因扩展字段而报错。

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
NAME_VALID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
NAME_MAX_LEN = 64
DESCRIPTION_MIN_LEN = 10
STRICT_YAML_ENV = "STRICT_SKILL_YAML"


class FrontmatterParseError(ValueError):
    """frontmatter 不能按所声明的 YAML 模式可靠解析。"""


def _try_import_yaml():
    """探测 PyYAML 是否可用。"""
    try:
        import yaml  # type: ignore
        return yaml
    except Exception:
        return None


YAML_LIB = _try_import_yaml()


def extract_frontmatter_text(content):
    """从 SKILL.md 文本中抽出 frontmatter 原文（不含首尾 ``---`` 分隔行）。

    返回 ``(fm_text, has_fm)``：``has_fm`` 标识是否识别到合法 frontmatter 块。
    """
    if not content.startswith("---"):
        return "", False
    # 允许首行就是 ---\n
    rest = content[3:]
    if rest.startswith("\r\n"):
        rest = rest[2:]
    elif rest.startswith("\n"):
        rest = rest[1:]
    # 找闭合 ---（独占一行）
    end_match = re.search(r"\n---\s*(\r?\n|$)", rest)
    if not end_match:
        return "", False
    fm_text = rest[: end_match.start()]
    return fm_text, True


def fallback_parse(fm_text):
    """内置极简 frontmatter 解析器（不依赖 PyYAML）。

    支持：
    - 顶层 ``key: value``
    - 单/双引号字符串（保留引号内原值）
    - ``|`` / ``|-`` / ``>|`` 等块字面量（按缩进收集多行）
    - ``>`` / ``>-`` 折叠块（简化为按换行拼接，足以判断长度/非空）
    - 忽略注释行（``#`` 开头）与空行
    - 不解析列表 / 字典 / 锚点等高级特性（这些字段在判断 name/description
      时不会用到，遇到时按字符串原样保留即可）

    返回 ``dict[str, str]``（值统一为字符串）。
    """
    result = {}
    lines = fm_text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        # 只处理顶层（无缩进）的 key
        if line[:1] in (" ", "\t"):
            i += 1
            continue
        m = FRONTMATTER_KV.match(line)
        if not m:
            i += 1
            continue
        key = m.group(1)
        val = m.group(2).strip()
        if val in ("|", "|-", "|+", ">", ">-", ">+"):
            block_lines = []
            i += 1
            while i < n:
                bl = lines[i]
                if bl.strip() == "":
                    block_lines.append("")
                    i += 1
                    continue
                if bl[:1] in (" ", "\t"):
                    block_lines.append(bl.strip())
                    i += 1
                else:
                    break
            while block_lines and block_lines[-1] == "":
                block_lines.pop()
            result[key] = "\n".join(block_lines)
        elif (
            len(val) >= 2
            and val[0] == '"'
            and val[-1] == '"'
        ):
            inner = val[1:-1]
            inner = inner.replace('\\"', '"').replace("\\\\", "\\")
            result[key] = inner
        elif (
            len(val) >= 2
            and val[0] == "'"
            and val[-1] == "'"
        ):
            result[key] = val[1:-1].replace("''", "'")
        else:
            # 裸值：去掉行内注释（YAML 规则：` # ...` 视为注释，需空格分隔）
            ci = val.find(" #")
            if ci != -1:
                val = val[:ci].rstrip()
            result[key] = val
        i += 1
    return result


def parse_frontmatter(content, strict=False):
    """解析 frontmatter，返回 ``dict``。

    PyYAML 可用时返回其解析结果（值可能是 str/int/dict/list 等）；
    不可用时，非严格模式返回 fallback 字符串字典。PyYAML 已安装但解析
    失败时直接抛出 ``FrontmatterParseError``，避免非法 YAML 假绿。
    """
    fm_text, has_fm = extract_frontmatter_text(content)
    if not has_fm:
        return {}
    if YAML_LIB is not None:
        try:
            data = YAML_LIB.safe_load(fm_text)
            if isinstance(data, dict):
                return data
            return {}
        except Exception as e:
            raise FrontmatterParseError(f"YAML 语法错误: {e}") from e
    if strict:
        raise FrontmatterParseError(
            f"严格模式需要 PyYAML；请安装 requirements-check.txt"
        )
    return fallback_parse(fm_text)


def field_to_str(val):
    """把任意字段值统一为字符串（用于长度/字符合法性检查）。"""
    if val is None:
        return ""
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, str):
        return val
    # list/dict 等：取第一个字符串元素，否则序列化
    try:
        if isinstance(val, list) and val:
            return field_to_str(val[0])
        import json as _json
        return _json.dumps(val, ensure_ascii=False)
    except Exception:
        return str(val)


def main():
    if not os.path.isdir(SKILLS_DIR):
        print("❌ skills/ 目录不存在")
        sys.exit(1)

    strict_yaml = os.environ.get(STRICT_YAML_ENV, "0") == "1"
    if strict_yaml and YAML_LIB is None:
        print("❌ 严格 YAML 校验需要 PyYAML，请安装 requirements-check.txt")
        sys.exit(1)

    mode = "PyYAML safe_load" if YAML_LIB is not None else "fallback（PyYAML 未安装，非严格）"
    if strict_yaml:
        mode += " + strict"
    print(f"YAML 解析模式：{mode}")

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
                content = fh.read()
        except (OSError, UnicodeDecodeError):
            errors.append(f"skills/{name}/SKILL.md 读取失败")
            continue

        try:
            fm = parse_frontmatter(content, strict=strict_yaml)
        except FrontmatterParseError as exc:
            errors.append(f"skills/{name}/SKILL.md {exc}")
            continue

        # === error 规则：name / description 必须存在且非空 ===
        name_val = field_to_str(fm.get("name"))
        desc_val = field_to_str(fm.get("description"))
        if not fm.get("name"):
            errors.append(f"skills/{name}/SKILL.md frontmatter 缺少 name")
        elif not name_val.strip():
            errors.append(f"skills/{name}/SKILL.md frontmatter name 为空")
        if not fm.get("description"):
            errors.append(f"skills/{name}/SKILL.md frontmatter 缺少 description")
        elif not desc_val.strip():
            errors.append(f"skills/{name}/SKILL.md frontmatter description 为空")

        # === warn 规则 ===
        # name 与目录名一致
        if name_val and name_val != name:
            warns.append(
                f"skills/{name}/SKILL.md name={name_val!r} 与目录名 {name!r} 不一致"
            )
        # name 字符合法 + 长度
        if name_val and not NAME_VALID_RE.match(name_val):
            warns.append(
                f"skills/{name}/SKILL.md name={name_val!r} 含非法字符"
                f"（仅允许小写字母/数字/连字符）"
            )
        if name_val and len(name_val) > NAME_MAX_LEN:
            warns.append(
                f"skills/{name}/SKILL.md name 长度 {len(name_val)} > {NAME_MAX_LEN}"
            )
        # description 质量
        if desc_val and len(desc_val) <= DESCRIPTION_MIN_LEN:
            warns.append(
                f"skills/{name}/SKILL.md description 过短"
                f"（{len(desc_val)} 字符 ≤ {DESCRIPTION_MIN_LEN}）"
            )
        # 许可证：license 字段 或 LICENSE.txt
        has_license_field = bool(field_to_str(fm.get("license")).strip())
        has_license_file = os.path.isfile(os.path.join(path, "LICENSE.txt"))
        if not has_license_field and not has_license_file:
            warns.append(
                f"skills/{name}/ 缺少许可证声明（既无 frontmatter license 字段，"
                f"也无 LICENSE.txt）"
            )
        # 推荐文件
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
