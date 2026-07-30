#!/usr/bin/env python3
"""
Skill 模板脚手架脚本
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the starter skill scaffold.")
    parser.add_argument("--task", required=True, help="Describe the task this skill should handle.")
    parser.add_argument(
        "--output-dir",
        help="Override output directory. Priority: CLI, OUTPUT_DIR, config, ./output.",
    )
    parser.add_argument(
        "--config",
        help="Optional config path. Defaults to assets/config.yaml.example.",
    )
    return parser.parse_args()


def load_simple_config(path: Path) -> dict[str, str]:
    """读取模板使用的顶层 ``key: value`` 配置，不引入第三方依赖。"""
    if not path.is_file():
        return {}
    result: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("\"'")
    return result


def resolve_output_dir(args: argparse.Namespace, skill_root: Path) -> Path:
    config_path = (
        Path(args.config)
        if args.config
        else skill_root / "assets" / "config.yaml.example"
    )
    config = load_simple_config(config_path)
    configured_dir = config.get("default_output_dir")
    selected = args.output_dir or os.getenv("OUTPUT_DIR") or configured_dir or "./output"
    output_dir = Path(selected).expanduser()
    if not output_dir.is_absolute():
        output_dir = skill_root / output_dir
    return output_dir


def build_output(task: str) -> str:
    timestamp = datetime.now().isoformat(timespec="seconds")
    return "\n".join(
        [
            "# Skill Scaffold Result",
            "",
            f"- Generated at: {timestamp}",
            f"- Task: {task}",
            "",
            "## Next Steps",
            "",
            "1. Rewrite SKILL.md to match the actual domain.",
            "2. Replace this script with real logic.",
            "3. Update ROADMAP.md and TASKS.md.",
        ]
    )


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    output_dir = resolve_output_dir(args, skill_root)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "result.md"
    output_path.write_text(build_output(args.task), encoding="utf-8")

    print(f"Wrote scaffold output to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
