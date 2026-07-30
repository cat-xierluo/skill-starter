from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
COMMAND_PATH = ROOT / ".claude" / "commands" / "sync-upstream.md"


def run_git(repo, *args, check=True):
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def write_skill(repo, name, version):
    skill_dir = Path(repo) / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        f"description: Test skill version {version}.\n"
        "---\n\n"
        f"version: {version}\n",
        encoding="utf-8",
    )


class SyncUpstreamCommandTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tempdir.name)
        self.upstream = self.base / "upstream"
        self.consumer = self.base / "consumer"

        for repo in (self.upstream, self.consumer):
            repo.mkdir()
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Sync Test")
            run_git(repo, "config", "user.email", "sync@example.test")

        write_skill(self.upstream, "demo", "2")
        write_skill(self.upstream, "new-demo", "1")
        run_git(self.upstream, "add", "skills")
        run_git(self.upstream, "commit", "-m", "add upstream skills")

        write_skill(self.consumer, "demo", "1")
        run_git(self.consumer, "add", "skills")
        run_git(self.consumer, "commit", "-m", "add local mirror")

        run_git(self.consumer, "remote", "add", "upstream", str(self.upstream))
        run_git(
            self.consumer,
            "remote",
            "set-url",
            "--push",
            "upstream",
            "DISABLED",
        )
        run_git(self.consumer, "fetch", "upstream", "main")

    def tearDown(self):
        self.tempdir.cleanup()

    def test_command_contains_required_safety_gates(self):
        content = COMMAND_PATH.read_text(encoding="utf-8")
        required = (
            "git remote set-url --push <remote-name> DISABLED",
            ".starter-backups/${STAMP}-${SHORT_SHA}",
            "目录外依赖",
            "skill-manager",
            "禁止",
            "STRICT_LINKS=1 STRICT_SH_SYNTAX=1 STRICT_SKILL_YAML=1",
            "git restore --staged",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_mirror_sync_is_read_only_and_backup_can_restore(self):
        push_url = run_git(
            self.consumer, "remote", "get-url", "--push", "upstream"
        ).stdout.strip()
        self.assertEqual(push_url, "DISABLED")
        failed_push = run_git(
            self.consumer, "push", "upstream", "main", check=False
        )
        self.assertNotEqual(failed_push.returncode, 0)

        short_sha = run_git(
            self.consumer, "rev-parse", "--short=12", "upstream/main"
        ).stdout.strip()
        backup_root = (
            self.consumer / ".starter-backups" / f"20260730T000000Z-{short_sha}"
        )
        backup_root.mkdir(parents=True)
        shutil.copytree(
            self.consumer / "skills" / "demo", backup_root / "demo", symlinks=True
        )

        run_git(
            self.consumer,
            "checkout",
            "upstream/main",
            "--",
            "skills/demo",
        )
        synced = (self.consumer / "skills" / "demo" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("version: 2", synced)

        failed_current = backup_root / "failed-current"
        failed_current.mkdir()
        shutil.move(
            str(self.consumer / "skills" / "demo"),
            str(failed_current / "demo"),
        )
        shutil.copytree(backup_root / "demo", self.consumer / "skills" / "demo")
        run_git(self.consumer, "restore", "--staged", "--", "skills/demo")

        restored = (self.consumer / "skills" / "demo" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("version: 1", restored)
        status = run_git(
            self.consumer, "status", "--porcelain", "--", "skills/demo"
        ).stdout
        self.assertEqual(status, "")

    def test_new_skill_checkout_can_rollback_without_index_residue(self):
        run_git(
            self.consumer,
            "checkout",
            "upstream/main",
            "--",
            "skills/new-demo",
        )
        self.assertTrue((self.consumer / "skills" / "new-demo" / "SKILL.md").is_file())

        short_sha = run_git(
            self.consumer, "rev-parse", "--short=12", "upstream/main"
        ).stdout.strip()
        backup_root = (
            self.consumer / ".starter-backups" / f"20260730T000001Z-{short_sha}"
        )
        failed_current = backup_root / "failed-current"
        failed_current.mkdir(parents=True)
        shutil.move(
            str(self.consumer / "skills" / "new-demo"),
            str(failed_current / "new-demo"),
        )
        run_git(self.consumer, "restore", "--staged", "--", "skills/new-demo")

        self.assertFalse((self.consumer / "skills" / "new-demo").exists())
        status = run_git(
            self.consumer, "status", "--porcelain", "--", "skills/new-demo"
        ).stdout
        self.assertEqual(status, "")


if __name__ == "__main__":
    unittest.main()
