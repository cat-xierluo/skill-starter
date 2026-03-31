#!/usr/bin/env python3
"""
Generate a simple weekly weather briefing in Markdown.
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path


FORECAST = [
    ("周一", "晴", "15-22°C", "适合安排外出会议"),
    ("周二", "多云", "16-23°C", "通勤友好，注意早晚温差"),
    ("周三", "小雨", "14-20°C", "建议带伞，室外活动预留备选方案"),
    ("周四", "阴", "13-19°C", "适合室内协作和长时间会议"),
    ("周五", "晴", "16-24°C", "适合安排拍摄、拜访和线下活动"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a weekly weather briefing.")
    parser.add_argument("--location", help="Briefing location override.")
    parser.add_argument("--audience", help="Who this briefing is for.")
    parser.add_argument("--output-dir", help="Output directory override.")
    return parser.parse_args()


def build_markdown(location: str, audience: str) -> str:
    generated_at = datetime.now().isoformat(timespec="seconds")
    lines = [
        f"# {location} 一周天气播报",
        "",
        f"- 生成时间：{generated_at}",
        f"- 面向对象：{audience}",
        "",
        "## 本周概览",
        "",
    ]

    for day, weather, temperature, note in FORECAST:
        lines.append(f"- **{day}**：{weather}，{temperature}。{note}")

    lines.extend(
        [
            "",
            "## 建议",
            "",
            "- 周三有雨，外出任务优先安排备选方案。",
            "- 周一、周五天气较稳，适合安排线下活动。",
            "- 温差较大，提醒团队注意增减衣物。",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    location = args.location or os.getenv("DEFAULT_LOCATION") or "苏州"
    audience = args.audience or os.getenv("AUDIENCE") or "团队成员"
    output_dir = Path(args.output_dir or os.getenv("OUTPUT_DIR") or (skill_root / "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "weekly-weather-briefing.md"
    output_path.write_text(build_markdown(location, audience), encoding="utf-8")

    print(f"Wrote briefing to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
