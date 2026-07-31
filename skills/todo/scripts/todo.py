#!/usr/bin/env python3
"""最小待办脚本：add / list / done，数据存 todos.json。"""
import json
import sys
from pathlib import Path

DB = Path.cwd() / "todos.json"  # 写到运行目录（cwd），便于在临时目录测试隔离，不污染 Skill 源目录


def load():
    if DB.exists():
        return json.loads(DB.read_text(encoding="utf-8"))
    return []


def save(todos):
    DB.write_text(json.dumps(todos, ensure_ascii=False, indent=2), encoding="utf-8")


def next_id(todos):
    return max((t["id"] for t in todos), default=0) + 1


def main(argv):
    if not argv:
        print("usage: todo.py [add <text> | list | done <id>]", file=sys.stderr)
        return 2
    cmd, rest = argv[0], argv[1:]
    todos = load()
    if cmd == "add":
        text = " ".join(rest).strip()
        if not text:
            print("error: 待办内容不能为空", file=sys.stderr)
            return 2
        todo = {"id": next_id(todos), "text": text, "done": False}
        todos.append(todo)
        save(todos)
        print(json.dumps(todo, ensure_ascii=False))  # 成功结果走 stdout
        return 0
    if cmd == "list":
        for t in todos:
            mark = "x" if t["done"] else " "
            print(f"[{mark}] {t['id']}: {t['text']}")
        return 0
    if cmd == "done":
        if not rest or not rest[0].isdigit():
            print("error: 用法 done <id>", file=sys.stderr)
            return 2
        tid = int(rest[0])
        for t in todos:
            if t["id"] == tid:
                t["done"] = True
                save(todos)
                print(json.dumps(t, ensure_ascii=False))
                return 0
        print(f"error: 找不到 id={tid}", file=sys.stderr)  # 错误走 stderr
        return 1
    print(f"error: 未知命令 {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
