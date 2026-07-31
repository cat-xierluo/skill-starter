"""todo 标准示例 Skill 的回归测试。

复用 test_skill_template.py 的 git-tracked 复制法 + 临时目录隔离 + 断言风格。
覆盖 T-007 验收：正常路径、错误路径、守恒性（防假绿）、干净隔离。
"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TODO_ROOT = ROOT / "skills" / "todo"
TODO_SCRIPT = TODO_ROOT / "scripts" / "todo.py"


class SkillTodoCopyTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tempdir.name)
        self.copy = self.base / "todo"
        self.copy_tracked_todo()

    def tearDown(self):
        self.tempdir.cleanup()

    def copy_tracked_todo(self):
        """用 git ls-files 拿到 todo Skill 的已跟踪文件，复制到临时目录。

        天然排除 todos.json、__pycache__ 等未跟踪产物，模拟干净安装。
        """
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "skills/todo",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        for raw_path in result.stdout.splitlines():
            source = ROOT / raw_path
            relative = source.relative_to(TODO_ROOT)
            target = self.copy / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    def run_todo(self, *args, cwd=None):
        """在指定目录运行 todo.py，返回 CompletedProcess（stdout/stderr 分开）。"""
        return subprocess.run(
            [sys.executable, str(self.copy / "scripts" / "todo.py"), *args],
            cwd=cwd or self.base,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_add_normal_returns_json_on_stdout(self):
        result = self.run_todo("add", "买牛奶")
        self.assertEqual(result.returncode, 0, result.stderr)
        todo = json.loads(result.stdout)  # stdout 必须是合法 JSON
        self.assertEqual(todo["text"], "买牛奶")
        self.assertFalse(todo["done"])
        self.assertEqual(todo["id"], 1)
        # todos.json 写到 cwd（self.base），含该条
        db = self.base / "todos.json"
        self.assertTrue(db.is_file())
        records = json.loads(db.read_text(encoding="utf-8"))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["text"], "买牛奶")

    def test_list_shows_added_item(self):
        self.run_todo("add", "读概念入门")
        result = self.run_todo("list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("读概念入门", result.stdout)

    def test_done_marks_item_true_not_fake_green(self):
        """防 11 篇讲的「假绿」bug：done 后 todos.json 里该条 done 必须真的变 true。"""
        self.run_todo("add", "写测试")
        result = self.run_todo("done", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        done_record = json.loads(result.stdout)
        self.assertTrue(done_record["done"])
        # 守恒性：落盘的数据也变 true
        db = self.base / "todos.json"
        records = json.loads(db.read_text(encoding="utf-8"))
        self.assertTrue(records[0]["done"])

    def test_done_missing_id_returns_nonzero_on_stderr(self):
        self.run_todo("add", "一条待办")
        result = self.run_todo("done", "99")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.returncode, 1)  # 运行时失败 = 1
        self.assertIn("找不到", result.stderr)
        # 错误不能污染 stdout
        self.assertEqual(result.stdout, "")

    def test_done_missing_id_is_not_returning_zero(self):
        """契约最关键的验证：失败绝不能返回 0（否则 AI 被骗成「假绿」）。"""
        result = self.run_todo("done", "99")
        self.assertNotEqual(result.returncode, 0)

    def test_add_empty_text_returns_usage_error(self):
        result = self.run_todo("add")
        self.assertEqual(result.returncode, 2)  # 用法错误 = 2
        self.assertIn("不能为空", result.stderr)

    def test_no_args_returns_usage_error(self):
        result = self.run_todo()
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage", result.stderr)

    def test_unknown_command_returns_usage_error(self):
        result = self.run_todo("frobnicate")
        self.assertEqual(result.returncode, 2)
        self.assertIn("未知命令", result.stderr)

    def test_source_directory_not_polluted_by_run(self):
        """干净隔离：在临时目录运行后，Skill 源目录不出现 todos.json。"""
        # 在 self.base 跑一次
        self.run_todo("add", "隔离测试")
        # 源目录（仓库内 skills/todo/）不应被写入数据
        self.assertFalse((TODO_ROOT / "todos.json").exists())
        # 数据确实写到了 cwd
        self.assertTrue((self.base / "todos.json").is_file())

    def test_required_files_present(self):
        """T-007 验收：必需文件齐全（name=目录名、license、契约文档、协作文档四件套）。"""
        for required in (
            "SKILL.md",
            "LICENSE.txt",
            "CHANGELOG.md",
            "ROADMAP.md",
            "TASKS.md",
            "DECISIONS.md",
            "scripts/todo.py",
            "assets/todos.example.json",
            ".gitignore",
        ):
            self.assertTrue((self.copy / required).is_file(), required)


if __name__ == "__main__":
    unittest.main()
