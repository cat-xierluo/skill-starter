#!/usr/bin/env python3
"""
skill-start-update: 检查 skill-starter 项目是否有远程更新
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path.home() / ".myagents" / ".skill-starter-last-check.json"
DEFAULT_INTERVAL_HOURS = 48


def load_env() -> int:
    """加载环境变量中的检测间隔"""
    env_file = SKILL_ROOT / ".env"
    interval = DEFAULT_INTERVAL_HOURS

    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("CHECK_INTERVAL_HOURS="):
                val = line.split("=", 1)[1].strip()
                if val:
                    interval = int(val)
                break

    return interval


def should_check(interval_hours: int) -> bool:
    """检查是否应该执行检测"""
    if not CONFIG_PATH.exists():
        return True

    try:
        data = json.loads(CONFIG_PATH.read_text())
        last_check = datetime.fromisoformat(data["last_check"])
        next_check = last_check + timedelta(hours=interval_hours)
        return datetime.now() >= next_check
    except (json.JSONDecodeError, KeyError, ValueError):
        return True


def update_check_timestamp():
    """更新检测时间戳"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({"last_check": datetime.now().isoformat()}))


def get_remote_commits(repo_path: Path, branch: str = "main") -> list[dict]:
    """获取远程相对本地的领先 commit"""
    try:
        # git fetch origin
        subprocess.run(
            ["git", "fetch", "origin", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=30,
        )

        # 获取领先 commits
        result = subprocess.run(
            ["git", "log", f"HEAD..origin/{branch}", "--format=%h - %s", "--reverse"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return []

        commits = []
        for line in result.stdout.strip().splitlines():
            if line:
                commits.append({"message": line})

        return commits

    except (subprocess.TimeoutExpired, Exception):
        return []


def check_updates() -> list[dict]:
    """检查 skill-starter 是否有更新"""
    return get_remote_commits(SKILL_ROOT)


def main() -> int:
    interval_hours = load_env()

    if not should_check(interval_hours):
        return 0

    commits = check_updates()

    if commits:
        print(f"📦 skill-starter 有 {len(commits)} 个新提交\n")
        print("最近更新:")
        for commit in commits[:5]:
            print(f"- {commit['message']}")
        if len(commits) > 5:
            print(f"- ... 还有 {len(commits) - 5} 个提交")
        print(f"\n提示: cd {SKILL_ROOT} && git pull")

    update_check_timestamp()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
