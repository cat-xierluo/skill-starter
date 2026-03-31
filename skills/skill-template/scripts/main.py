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
        help="Optional output directory. Defaults to OUTPUT_DIR env var or ./output.",
    )
    return parser.parse_args()


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
    output_dir = Path(args.output_dir or os.getenv("OUTPUT_DIR") or (skill_root / "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "result.md"
    output_path.write_text(build_output(args.task), encoding="utf-8")

    print(f"Wrote scaffold output to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
