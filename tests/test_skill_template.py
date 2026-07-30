import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "skills" / "skill-template"
LINK_CHECK_PATH = ROOT / "scripts" / "check_links.py"
SPEC = importlib.util.spec_from_file_location("check_links_for_template", LINK_CHECK_PATH)
check_links = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_links)


class SkillTemplateCopyTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tempdir.name)
        self.copy = self.base / "skill-template"
        self.copy_tracked_template()

    def tearDown(self):
        self.tempdir.cleanup()

    def copy_tracked_template(self):
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "skills/skill-template",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        for raw_path in result.stdout.splitlines():
            source = ROOT / raw_path
            relative = source.relative_to(TEMPLATE_ROOT)
            target = self.copy / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    def assert_links_valid(self):
        old_root = check_links.ROOT
        try:
            check_links.ROOT = str(self.copy)
            check_links._MD_CACHE.clear()
            with contextlib.redirect_stdout(io.StringIO()):
                check_links.main()
        finally:
            check_links.ROOT = old_root
            check_links._MD_CACHE.clear()

    def test_independent_copy_has_no_broken_relative_links(self):
        self.assertTrue((self.copy / "LICENSE.txt").is_file())
        self.assert_links_valid()

    def test_maintained_profile_runs_and_consumes_config(self):
        config = self.copy / "assets" / "config.yaml.example"
        config.write_text("default_output_dir: ./generated\n", encoding="utf-8")

        result = subprocess.run(
            [
                sys.executable,
                str(self.copy / "scripts" / "main.py"),
                "--task",
                "verify independent template",
            ],
            cwd=self.base,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self.assertEqual(result.returncode, 0, result.stdout)
        output = self.copy / "generated" / "result.md"
        self.assertTrue(output.is_file())
        self.assertIn("verify independent template", output.read_text(encoding="utf-8"))

    def test_minimal_profile_remains_self_contained(self):
        shutil.rmtree(self.copy / "scripts")
        shutil.rmtree(self.copy / "assets")
        (self.copy / ".env.example").unlink()

        for required in (
            "SKILL.md",
            "LICENSE.txt",
            "CHANGELOG.md",
            "ROADMAP.md",
            "TASKS.md",
            "DECISIONS.md",
        ):
            self.assertTrue((self.copy / required).is_file(), required)
        self.assert_links_valid()


if __name__ == "__main__":
    unittest.main()
