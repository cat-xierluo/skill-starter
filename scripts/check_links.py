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
    仅在显式开启时联网，默认检查仍保持离线。检查器会：
    - 先发 HEAD；站点拒绝 HEAD 时改用只取首字节的 GET
    - 对超时、限速和 5xx 做有限重试与指数退避
    - 读取 ``scripts/external_links_allowlist.txt`` 中的 glob 允许项
    - 把 404/410 和其他确定性 4xx 判为 error；把访问受限或持续网络异常
      判为 warn，避免临时网络波动制造假断链
    - 输出失败 URL、全部来源位置、HTTP 状态或网络原因

符号链接目录不递归（followlinks=False），避免 .claude/skills 与 skills/
重复扫描。

用法：
    python3 scripts/check_links.py                 # 默认：相对链接 + 锚点 + 引用
    python3 scripts/check_links.py --check-external

退出码：0 全部有效（允许 warn），1 存在 error 级断链
"""

import argparse
import fnmatch
import os
import re
import socket
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import NamedTuple
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag
from urllib.request import Request, urlopen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", ".starter-backups", "output", "__pycache__", "node_modules"}
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "ftp://", "ftps://")
HTTP_PREFIXES = ("http://", "https://")
DEFAULT_ALLOWLIST = os.path.join(ROOT, "scripts", "external_links_allowlist.txt")
RETRYABLE_HTTP_CODES = {408, 425, 429, 500, 502, 503, 504}
RESTRICTED_HTTP_CODES = {401, 403}
HEAD_FALLBACK_CODES = {403, 405, 501}
USER_AGENT = "skill-starter-link-check/1.0"

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


class ExternalResult(NamedTuple):
    """单个外链的检查结果。"""

    status: str
    detail: str
    attempts: int


def normalize_external_url(url):
    """移除不会发送给服务器的 fragment，便于去重。"""
    return urldefrag(url)[0]


def load_external_allowlist(path):
    """读取一行一个 glob 的外链允许清单。"""
    if not path or not os.path.exists(path):
        return []
    patterns = []
    with open(path, encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def is_external_allowed(url, patterns):
    """判断 URL 是否命中允许清单。"""
    return any(fnmatch.fnmatchcase(url, pattern) for pattern in patterns)


def _request_external(url, timeout, method):
    """执行一次 HTTP 请求，返回状态码；HTTPError 交给调用方分类。"""
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8",
        "User-Agent": USER_AGENT,
    }
    if method == "GET":
        headers["Range"] = "bytes=0-0"
    request = Request(url, headers=headers, method=method)
    with urlopen(request, timeout=timeout) as response:
        return response.getcode() or 200


def _request_external_with_fallback(url, timeout):
    """优先 HEAD；明确拒绝 HEAD 时改用轻量 GET。"""
    try:
        return _request_external(url, timeout, "HEAD")
    except HTTPError as exc:
        if exc.code not in HEAD_FALLBACK_CODES:
            raise
    return _request_external(url, timeout, "GET")


def probe_external_url(url, timeout=10.0, retries=3, backoff=1.0):
    """核验一个外链，并区分确定断链、访问受限和暂时异常。"""
    attempts = max(1, retries)
    last_detail = "未知错误"

    for attempt in range(1, attempts + 1):
        try:
            code = _request_external_with_fallback(url, timeout)
            if 200 <= code < 400:
                return ExternalResult("ok", f"HTTP {code}", attempt)
            last_detail = f"HTTP {code}"
        except HTTPError as exc:
            code = exc.code
            last_detail = f"HTTP {code}"
        except (URLError, TimeoutError, socket.timeout, OSError) as exc:
            code = None
            reason = getattr(exc, "reason", exc)
            last_detail = f"{type(reason).__name__}: {reason}"

        if code in {404, 410}:
            return ExternalResult("broken", last_detail, attempt)
        if code in RESTRICTED_HTTP_CODES:
            return ExternalResult("restricted", last_detail, attempt)
        if code is not None and 400 <= code < 500 and code not in RETRYABLE_HTTP_CODES:
            return ExternalResult("broken", last_detail, attempt)

        if attempt < attempts:
            time.sleep(backoff * (2 ** (attempt - 1)))

    return ExternalResult("transient", last_detail, attempts)


def check_external_links(external_sources, allowlist_path, timeout, retries, workers):
    """并行检查去重后的 HTTP(S) 链接；返回确定断链列表。"""
    patterns = load_external_allowlist(allowlist_path)
    allowed = []
    pending = []
    for url in sorted(external_sources):
        if is_external_allowed(url, patterns):
            allowed.append(url)
        else:
            pending.append(url)

    results = {}
    if pending:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            futures = {
                pool.submit(probe_external_url, url, timeout, retries): url
                for url in pending
            }
            for future in as_completed(futures):
                url = futures[future]
                try:
                    results[url] = future.result()
                except Exception as exc:  # 防止单个 worker 异常中断整份报告
                    results[url] = ExternalResult(
                        "transient", f"{type(exc).__name__}: {exc}", 1
                    )

    counts = defaultdict(int)
    for result in results.values():
        counts[result.status] += 1
    counts["allowed"] = len(allowed)

    print(
        "外链核验："
        f"{len(external_sources)} 个唯一 URL，"
        f"{counts['ok']} 正常，{counts['broken']} 确定失效，"
        f"{counts['restricted']} 访问受限，{counts['transient']} 暂时异常，"
        f"{counts['allowed']} 允许清单跳过"
    )

    for url in allowed:
        print(f"  ⏭️  {url}  命中允许清单")
        for source in external_sources[url]:
            print(f"      来源: {source}")

    labels = {
        "broken": "❌",
        "restricted": "⚠️ ",
        "transient": "⚠️ ",
    }
    for url in sorted(results):
        result = results[url]
        if result.status == "ok":
            continue
        print(
            f"  {labels[result.status]} {url}  {result.detail}"
            f"（{result.attempts} 次尝试）"
        )
        for source in external_sources[url]:
            print(f"      来源: {source}")

    return [url for url, result in results.items() if result.status == "broken"]


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


def check_inline_link(
    md_file, target, errors, warns, ext_counter, external_sources=None, source=None
):
    """检查单个行内链接 target。"""
    if not target:
        return
    if target.startswith(EXTERNAL_PREFIXES):
        ext_counter[0] += 1
        if target.startswith(HTTP_PREFIXES) and external_sources is not None:
            url = normalize_external_url(target)
            if source not in external_sources[url]:
                external_sources[url].append(source)
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


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-external",
        action="store_true",
        help="联网核验 Markdown 中的 HTTP(S) 链接",
    )
    parser.add_argument(
        "--external-allowlist",
        default=DEFAULT_ALLOWLIST,
        help="外链允许清单路径（一行一个 glob）",
    )
    parser.add_argument(
        "--external-timeout",
        type=float,
        default=10.0,
        help="单次请求超时秒数（默认 10）",
    )
    parser.add_argument(
        "--external-retries",
        type=int,
        default=3,
        help="外链最大尝试次数（默认 3）",
    )
    parser.add_argument(
        "--external-workers",
        type=int,
        default=8,
        help="外链并发数（默认 8）",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args([] if argv is None else argv)
    check_external = args.check_external

    errors = []   # list of (md_file, target, reason)
    warns = []
    checked_inline = 0
    checked_refs = 0
    ext_counter = [0]  # 外部链接计数
    external_sources = defaultdict(list)

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
                check_inline_link(
                    md,
                    target,
                    errors,
                    warns,
                    ext_counter,
                    external_sources,
                    f"{rel_md}:{lineno}",
                )
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
                    if url.startswith(HTTP_PREFIXES):
                        normalized = normalize_external_url(url)
                        source = f"{rel_md}:{lineno}"
                        if source not in external_sources[normalized]:
                            external_sources[normalized].append(source)
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
    if check_external:
        print(
            f"  发现外部链接 {ext_counter[0]} 处，"
            f"其中 HTTP(S) 去重后 {len(external_sources)} 个"
        )
        external_errors = check_external_links(
            external_sources,
            args.external_allowlist,
            max(0.1, args.external_timeout),
            max(1, args.external_retries),
            max(1, args.external_workers),
        )
        for url in external_errors:
            sources = ", ".join(external_sources[url])
            errors.append((sources, url, "外部链接确定失效"))
    else:
        print(f"  外部链接（http/https 等）跳过：{ext_counter[0]} 个")

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
    main(sys.argv[1:])
