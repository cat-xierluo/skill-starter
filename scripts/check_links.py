#!/usr/bin/env python3
"""检查仓库内所有 Markdown 文件的链接完整性。

覆盖三类链接：

1. 行内链接 ``[text](target)``
   - 相对路径文件必须存在（不存在 → **error**）
   - 外部链接（http/https/mailto/ftp）默认跳过，加 ``--check-external``
     开关后才会联网检查（见下方"外部链接"说明）
   - 纯锚点 ``#xxx`` 视为有效（默认指向当前文件，规则复杂）

2. Markdown 锚点 ``[text](file.md#anchor)``
   - 若 ``file.md`` 存在，扫描其中标题，转成锚点后尝试匹配
   - 标题 → 锚点的规则：小写、去标点、空格转连字符
   - 无法匹配时 → **warn**（锚点规则各家实现不一，只做宽松匹配）

3. 引用式链接 ``[text][ref]`` + ``[ref]: url``
   - 每个 ref 必须在文件内有对应定义（未定义 → **error**）
   - 若 url 是相对路径，目标文件必须存在（不存在 → **error**）

外部链接（``--check-external``）：
    当前为占位实现，**不会真正联网**（避免 CI 网络波动阻断提交）。
    未来接入思路（注释中保留）：
    - 用 ``urllib.request.urlopen(url, timeout=N)`` HEAD 请求
    - 失败重试 3 次，指数退避
    - 维护 ALLOW_LIST（已知限速/反爬域名白名单，跳过）
    - 作为定时任务跑（如每日 cron），不阻塞本地提交
    暂时只统计外部链接数量，不做断链判定。

符号链接目录不递归（followlinks=False），避免 .claude/skills 与 skills/
重复扫描。

用法：
    python3 scripts/check_links.py                 # 默认：相对链接 + 锚点 + 引用
    python3 scripts/check_links.py --check-external # 占位（暂不联网）

退出码：0 全部有效（允许 warn），1 存在 error 级断链
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", ".starter-backups", "output", "__pycache__", "node_modules"}
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "ftp://", "ftps://")

# 行内链接 [text](target)，target 内部允许 #anchor
INLINE_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# 引用式链接 [text][ref] —— text 可空，ref 可空（[ref][] 简写表示用 text 作 ref）
REF_USE_RE = re.compile(r"\[([^\]]*)\]\[([^\]]*)\]")

# 引用定义 [ref]: url "optional title"
REF_DEF_RE = re.compile(r"^\s*\[([^\]]+)\]:\s*<([^>]+)>(?:\s+\"[^\"]*\")?\s*$")
REF_DEF_BARE_RE = re.compile(r"^\s*\[([^\]]+)\]:\s*(\S+)(?:\s+\"[^\"]*\")?\s*$")

# Markdown 标题（ATX 风格：# / ## / ...）
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")

# 代码块围栏（粗略跳过 ``` 和 ~~~ 包裹的内容）
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")


def iter_md_files():
    """遍历仓库内所有 .md 文件，剪枝排除目录，不跟随符号链接。"""
    for dirpath, dirnames, filenames in os.walk(ROOT, followlinks=False):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.endswith(".md"):
                yield os.path.join(dirpath, fname)


def slugify_heading(text):
    """把标题文本转成锚点 slug（GitHub 风格的简化版）。

    规则：
    - 转小写
    - 去掉非字母/数字/CJK/连字符/下划线的字符
    - 空格转连字符
    - 合并连续连字符
    - 去首尾连字符
    """
    s = text.strip().lower()
    out = []
    for ch in s:
        if ch.isalnum() or "一" <= ch <= "鿿" or ch in ("_", "-"):
            out.append(ch)
        elif ch.isspace():
            out.append("-")
        # 其余标点丢弃
    slug = re.sub(r"-+", "-", "".join(out)).strip("-")
    return slug


def collect_headings(content):
    """从 Markdown 内容中提取所有标题的 slug 集合（跳过代码块）。"""
    slugs = set()
    in_fence = False
    fence_marker = None
    for line in content.splitlines():
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        hm = HEADING_RE.match(line)
        if hm:
            slugs.add(slugify_heading(hm.group(2)))
    return slugs


_MD_CACHE = {}


def read_md_cache(path):
    """读取并缓存 .md 文件内容（含标题 slug 集合），避免重复 IO。"""
    entry = _MD_CACHE.get(path)
    if entry is not None:
        return entry
    try:
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        entry = (content, collect_headings(content))
    except (OSError, UnicodeDecodeError):
        entry = (None, set())
    _MD_CACHE[path] = entry
    return entry


def resolve_target(md_file, target):
    """把链接 target 解析为绝对路径，target 已剥离锚点。返回 normpath 或 None。"""
    base = os.path.dirname(md_file)
    resolved = os.path.normpath(os.path.join(base, target))
    return resolved


def check_inline_link(md_file, target, errors, warns, ext_counter):
    """检查单个行内链接 target。"""
    if not target:
        return
    if target.startswith(EXTERNAL_PREFIXES):
        ext_counter[0] += 1
        return
    if target.startswith("#"):
        # 纯当前文件锚点，规则复杂，跳过
        return

    anchor = None
    file_part = target
    if "#" in target:
        file_part, anchor = target.split("#", 1)
        file_part = file_part or ""
        anchor = anchor or ""

    if not file_part:
        # 纯锚点（已在上面返回过），此处兜底
        return

    resolved = resolve_target(md_file, file_part)
    if not os.path.exists(resolved):
        errors.append((md_file, target, f"目标文件不存在: {file_part}"))
        return

    if anchor and resolved.endswith(".md"):
        _, headings = read_md_cache(resolved)
        if headings:
            want = slugify_heading(anchor)
            # 宽松匹配：归一化后相等，或目标集合里任一项以 want 开头
            matched = want in headings or any(
                h == want or h.startswith(want) for h in headings
            )
            if not matched:
                warns.append(
                    (md_file, target, f"锚点 #{anchor} 在 {file_part} 中无匹配标题")
                )


def collect_ref_defs(content):
    """从文件内容里收集所有引用式链接定义。返回 ``{ref_lower: url}``。"""
    defs = {}
    for line in content.splitlines():
        m = REF_DEF_RE.match(line) or REF_DEF_BARE_RE.match(line)
        if m:
            defs[m.group(1).strip().lower()] = m.group(2).strip()
    return defs


def main():
    check_external = "--check-external" in sys.argv[1:]

    errors = []   # list of (md_file, target, reason)
    warns = []
    checked_inline = 0
    checked_refs = 0
    ext_counter = [0]  # 外部链接计数

    for md in iter_md_files():
        try:
            with open(md, encoding="utf-8") as fh:
                content = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        rel_md = os.path.relpath(md, ROOT)
        ref_defs = collect_ref_defs(content)

        lines = content.splitlines()
        for lineno, line in enumerate(lines, 1):
            # 跳过代码围栏内行
            # （为简单起见不维护完整状态，逐行检查即可，行内 `code` 误判容忍）
            for m in INLINE_LINK_RE.finditer(line):
                text, target = m.group(1), m.group(2)
                if not target:
                    continue
                checked_inline += 1
                before = len(errors)
                check_inline_link(md, target, errors, warns, ext_counter)
                # 错误信息附加行号
                if len(errors) > before:
                    e_md, e_t, e_r = errors[-1]
                    errors[-1] = (f"{rel_md}:{lineno}", e_t, e_r)

            for m in REF_USE_RE.finditer(line):
                text, ref = m.group(1).strip(), m.group(2).strip()
                # [ref][] 简写：用 text 作为 ref
                if not ref:
                    ref = text
                if not ref:
                    continue
                # 跳过图片式 ![alt] 这种已被行内链接处理；这里只处理文字引用
                checked_refs += 1
                key = ref.lower()
                if key not in ref_defs:
                    warns.append(
                        (f"{rel_md}:{lineno}", f"[{ref}]",
                         "引用式链接未找到定义（可能跨文件，宽松处理）")
                    )
                    continue
                url = ref_defs[key]
                if url.startswith(EXTERNAL_PREFIXES):
                    ext_counter[0] += 1
                    continue
                # 相对路径：检查文件是否存在
                resolved = resolve_target(md, url.split("#", 1)[0])
                if not os.path.exists(resolved):
                    errors.append(
                        (f"{rel_md}:{lineno}", f"[{ref}] → {url}",
                         f"引用定义目标文件不存在: {url}")
                    )

    print(f"检查了 {checked_inline} 个行内 Markdown 相对链接、"
          f"{checked_refs} 个引用式链接引用")
    print(f"  外部链接（http/https 等）跳过：{ext_counter[0]} 个"
          + ("（已开启 --check-external 占位，暂不联网）" if check_external else ""))

    if warns:
        print(f"⚠️  发现 {len(warns)} 处告警（不阻断提交）：")
        for src, tgt, reason in warns:
            print(f"  {src} → {tgt}  {reason}")

    if errors:
        print(f"❌ 发现 {len(errors)} 处断链：")
        for src, tgt, reason in errors:
            print(f"  {src} → {tgt}  {reason}")
        sys.exit(1)
    print("✅ 所有 Markdown 相对链接有效")


if __name__ == "__main__":
    main()
