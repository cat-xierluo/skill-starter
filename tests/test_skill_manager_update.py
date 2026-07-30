import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANAGER_SOURCE = ROOT / "skills" / "skill-manager"
REAL_GIT = shutil.which("git")
REAL_CP = shutil.which("cp")
REAL_MV = shutil.which("mv")


class SkillManagerUpdateTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tempdir.name)
        self.manager = self.base / "skill-manager"
        shutil.copytree(MANAGER_SOURCE, self.manager)
        self.agent_dir = self.base / "project" / ".claude"
        self.skills_dir = self.agent_dir / "skills"
        self.skills_dir.mkdir(parents=True)
        self.registry = self.manager / "assets" / "skill-registry.json"
        self.env = os.environ.copy()
        self.env["SKILL_MANAGER_TARGET_DIR"] = str(self.agent_dir)

    def tearDown(self):
        self.tempdir.cleanup()

    def git(self, *args, cwd=None):
        return subprocess.run(
            [REAL_GIT, *args],
            cwd=cwd,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.strip()

    def make_remote(self, marker="old", version="1.0.0"):
        remote = self.base / "remote"
        remote.mkdir()
        self.git("init", cwd=remote)
        self.git("config", "user.name", "Skill Manager Test", cwd=remote)
        self.git("config", "user.email", "test@example.invalid", cwd=remote)
        self.write_remote_skill(remote, marker, version)
        self.git("add", ".", cwd=remote)
        self.git("commit", "-m", "initial", cwd=remote)
        self.git("branch", "-M", "main", cwd=remote)
        return remote, self.git("rev-parse", "HEAD", cwd=remote)

    def write_remote_skill(self, remote, marker, version="1.0.0"):
        skill = remote / "skills" / "demo"
        skill.mkdir(parents=True, exist_ok=True)
        (skill / "SKILL.md").write_text(
            textwrap.dedent(
                f"""\
                ---
                name: demo
                description: A demo skill used by updater tests.
                version: "{version}"
                ---

                # Demo
                """
            ),
            encoding="utf-8",
        )
        (skill / "marker.txt").write_text(marker, encoding="utf-8")

    def advance_remote(self, remote, marker, version="1.0.0"):
        self.write_remote_skill(remote, marker, version)
        self.git("add", ".", cwd=remote)
        self.git("commit", "-m", f"update {marker}", cwd=remote)
        return self.git("rev-parse", "HEAD", cwd=remote)

    def install_snapshot(self, remote, name="demo"):
        shutil.copytree(remote / "skills" / "demo", self.skills_dir / name)

    def write_registry(self, entries):
        self.registry.write_text(
            json.dumps(entries, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def registry_entry(self, remote_url, commit, subpath="skills/demo"):
        return {
            "name": "demo",
            "source": remote_url,
            "install_type": "remote",
            "installed_at": "2026-07-30T00:00:00+08:00",
            "last_updated": "2026-07-30T00:00:00+08:00",
            "installed_version": "1.0.0",
            "current_version": "1.0.0",
            "install_commit": commit,
            "install_branch": "main",
            "remote_url": remote_url,
            "remote_subpath": subpath,
        }

    def run_update(self, name=None, env=None):
        command = ["bash", str(self.manager / "scripts" / "update.sh")]
        if name:
            command.append(name)
        return subprocess.run(
            command,
            cwd=self.base / "project",
            env=env or self.env,
            text=True,
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

    def git_url_wrapper_env(
        self,
        remote,
        directory_name,
        remote_source_url="https://github.com/test/monorepo",
    ):
        fake_bin = self.base / directory_name
        fake_bin.mkdir()
        git_wrapper = fake_bin / "git"
        git_wrapper.write_text(
            textwrap.dedent(
                f"""\
                #!{sys.executable}
                import os
                import sys
                args = [os.environ.get("REMOTE_REPLACEMENT") if arg == os.environ.get("REMOTE_SOURCE_URL") else arg for arg in sys.argv[1:]]
                os.execv({REAL_GIT!r}, [{REAL_GIT!r}, *args])
                """
            ),
            encoding="utf-8",
        )
        git_wrapper.chmod(0o755)
        env = self.env.copy()
        env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
        env["REMOTE_REPLACEMENT"] = remote.as_uri()
        env["REMOTE_SOURCE_URL"] = remote_source_url
        return fake_bin, env

    def test_same_version_content_change_updates_and_records_commit(self):
        remote, old_commit = self.make_remote(marker="old")
        self.install_snapshot(remote)
        new_commit = self.advance_remote(remote, marker="new", version="1.0.0")
        remote_url = remote.as_uri()
        self.write_registry({"demo": self.registry_entry(remote_url, old_commit)})

        result = self.run_update("demo")

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual((self.skills_dir / "demo" / "marker.txt").read_text(), "new")
        backups = list(self.skills_dir.glob("demo.backup.*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / "marker.txt").read_text(), "old")
        saved = json.loads(self.registry.read_text(encoding="utf-8"))["demo"]
        self.assertEqual(saved["install_commit"], new_commit)

        second = self.run_update("demo")
        self.assertEqual(second.returncode, 0, second.stdout)
        self.assertIn("已是最新", second.stdout)
        self.assertEqual(len(list(self.skills_dir.glob("demo.backup.*"))), 1)

    def test_invalid_remote_returns_failure_without_touching_skill(self):
        skill = self.skills_dir / "demo"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: demo\ndescription: demo skill text\n---\n")
        (skill / "marker.txt").write_text("keep")
        bad_url = (self.base / "missing-repository").as_uri()
        self.write_registry({"demo": self.registry_entry(bad_url, "missing")})

        result = self.run_update("demo")

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("更新失败", result.stdout)
        self.assertEqual((skill / "marker.txt").read_text(), "keep")

    def test_invalid_registry_returns_failure(self):
        skill = self.skills_dir / "demo"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: demo\ndescription: demo skill text\n---\n")
        self.registry.write_text("{not valid json", encoding="utf-8")

        result = self.run_update("demo")

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("无远程来源记录", result.stdout)

    def test_copy_failure_keeps_original_skill(self):
        remote, old_commit = self.make_remote(marker="old")
        self.install_snapshot(remote)
        self.advance_remote(remote, marker="new")
        remote_url = remote.as_uri()
        self.write_registry({"demo": self.registry_entry(remote_url, old_commit)})
        fake_bin = self.base / "fake-bin"
        fake_bin.mkdir()
        fake_cp = fake_bin / "cp"
        fake_cp.write_text("#!/bin/sh\nexit 74\n", encoding="utf-8")
        fake_cp.chmod(0o755)
        env = self.env.copy()
        env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"

        result = self.run_update("demo", env=env)

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("复制失败", result.stdout)
        self.assertEqual((self.skills_dir / "demo" / "marker.txt").read_text(), "old")

    def test_stage_copy_interruption_keeps_original_skill(self):
        remote, old_commit = self.make_remote(marker="old")
        self.install_snapshot(remote)
        self.advance_remote(remote, marker="new")
        remote_url = remote.as_uri()
        self.write_registry({"demo": self.registry_entry(remote_url, old_commit)})
        fake_bin = self.base / "stage-copy-fake-bin"
        fake_bin.mkdir()
        counter = self.base / "cp-count"
        fake_cp = fake_bin / "cp"
        fake_cp.write_text(
            textwrap.dedent(
                f"""\
                #!{sys.executable}
                import os
                import sys
                from pathlib import Path
                counter = Path(os.environ["CP_COUNTER"])
                count = int(counter.read_text() or "0") if counter.exists() else 0
                count += 1
                counter.write_text(str(count))
                if count == 2:
                    sys.exit(74)
                os.execv({REAL_CP!r}, [{REAL_CP!r}, *sys.argv[1:]])
                """
            ),
            encoding="utf-8",
        )
        fake_cp.chmod(0o755)
        env = self.env.copy()
        env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
        env["CP_COUNTER"] = str(counter)

        result = self.run_update("demo", env=env)

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("更新暂存区", result.stdout)
        self.assertEqual((self.skills_dir / "demo" / "marker.txt").read_text(), "old")
        self.assertEqual(list(self.skills_dir.glob("demo.backup.*")), [])

    def test_switch_failure_restores_original_skill(self):
        remote, old_commit = self.make_remote(marker="old")
        self.install_snapshot(remote)
        self.advance_remote(remote, marker="new")
        remote_url = remote.as_uri()
        self.write_registry({"demo": self.registry_entry(remote_url, old_commit)})
        fake_bin = self.base / "switch-fake-bin"
        fake_bin.mkdir()
        counter = self.base / "mv-count"
        fake_mv = fake_bin / "mv"
        fake_mv.write_text(
            textwrap.dedent(
                f"""\
                #!{sys.executable}
                import os
                import sys
                from pathlib import Path
                counter = Path(os.environ["MV_COUNTER"])
                count = int(counter.read_text() or "0") if counter.exists() else 0
                count += 1
                counter.write_text(str(count))
                if count == 2:
                    sys.exit(75)
                os.execv({REAL_MV!r}, [{REAL_MV!r}, *sys.argv[1:]])
                """
            ),
            encoding="utf-8",
        )
        fake_mv.chmod(0o755)
        env = self.env.copy()
        env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
        env["MV_COUNTER"] = str(counter)

        result = self.run_update("demo", env=env)

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("正在恢复原 Skill", result.stdout)
        self.assertEqual((self.skills_dir / "demo" / "marker.txt").read_text(), "old")
        self.assertEqual(list(self.skills_dir.glob("demo.backup.*")), [])

    def test_downloaded_candidate_without_skill_file_is_rejected(self):
        remote, old_commit = self.make_remote(marker="old")
        self.install_snapshot(remote)
        (remote / "skills" / "demo" / "SKILL.md").unlink()
        self.git("add", "-A", cwd=remote)
        self.git("commit", "-m", "remove skill definition", cwd=remote)
        remote_url = remote.as_uri()
        self.write_registry({"demo": self.registry_entry(remote_url, old_commit)})

        result = self.run_update("demo")

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("找不到有效 Skill", result.stdout)
        self.assertEqual((self.skills_dir / "demo" / "marker.txt").read_text(), "old")

    def test_batch_update_reports_partial_failure(self):
        remote, commit = self.make_remote(marker="current")
        self.install_snapshot(remote)
        remote_url = remote.as_uri()
        entries = {"demo": self.registry_entry(remote_url, commit)}

        bad = self.skills_dir / "broken"
        bad.mkdir()
        (bad / "SKILL.md").write_text("---\nname: broken\ndescription: broken test skill\n---\n")
        entries["broken"] = self.registry_entry(
            (self.base / "missing").as_uri(), "missing"
        )
        self.write_registry(entries)

        result = self.run_update()

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("成功 1，失败 1", result.stdout)

    def test_batch_update_reports_all_success(self):
        remote, commit = self.make_remote(marker="current")
        self.install_snapshot(remote)
        remote_url = remote.as_uri()
        self.write_registry({"demo": self.registry_entry(remote_url, commit)})

        result = self.run_update()

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("成功 1，失败 0", result.stdout)

    def test_legacy_tree_url_is_migrated_during_update(self):
        remote, old_commit = self.make_remote(marker="old")
        self.install_snapshot(remote)
        new_commit = self.advance_remote(remote, marker="new")
        legacy_url = "https://github.com/test/monorepo/tree/main/skills/demo"
        entry = self.registry_entry(legacy_url, old_commit, subpath=None)
        self.write_registry({"demo": entry})
        _, env = self.git_url_wrapper_env(remote, "legacy-fake-bin")

        result = self.run_update("demo", env=env)

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("兼容迁移旧式", result.stdout)
        self.assertEqual((self.skills_dir / "demo" / "marker.txt").read_text(), "new")
        saved = json.loads(self.registry.read_text(encoding="utf-8"))["demo"]
        self.assertEqual(saved["remote_url"], "https://github.com/test/monorepo")
        self.assertEqual(saved["remote_subpath"], "skills/demo")
        self.assertEqual(saved["install_commit"], new_commit)

    def test_legacy_tree_url_preserves_branch_with_slash(self):
        remote, old_commit = self.make_remote(marker="old")
        self.install_snapshot(remote)
        self.git("checkout", "-b", "feature/demo", cwd=remote)
        new_commit = self.advance_remote(remote, marker="new")
        legacy_url = (
            "https://github.com/test/monorepo/tree/feature/demo/skills/demo"
        )
        entry = self.registry_entry(legacy_url, old_commit, subpath=None)
        entry["install_branch"] = "feature/demo"
        self.write_registry({"demo": entry})
        _, env = self.git_url_wrapper_env(remote, "slash-branch-fake-bin")

        result = self.run_update("demo", env=env)

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual((self.skills_dir / "demo" / "marker.txt").read_text(), "new")
        saved = json.loads(self.registry.read_text(encoding="utf-8"))["demo"]
        self.assertEqual(saved["remote_url"], "https://github.com/test/monorepo")
        self.assertEqual(saved["install_branch"], "feature/demo")
        self.assertEqual(saved["remote_subpath"], "skills/demo")
        self.assertEqual(saved["install_commit"], new_commit)

    def test_subdirectory_install_records_cloneable_repository_url(self):
        remote, _ = self.make_remote(marker="installed")
        fake_bin, env = self.git_url_wrapper_env(remote, "install-fake-bin")
        python_log = self.base / "python-calls.log"
        python_wrapper = fake_bin / "python3"
        python_wrapper.write_text(
            "#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"$PYTHON_CALL_LOG\"\nexit 0\n",
            encoding="utf-8",
        )
        python_wrapper.chmod(0o755)
        env["PYTHON_CALL_LOG"] = str(python_log)
        source = "https://github.com/test/monorepo/tree/main/skills/demo"

        result = subprocess.run(
            [
                "bash",
                str(self.manager / "scripts" / "install.sh"),
                "--target",
                str(self.agent_dir),
                source,
            ],
            cwd=self.base / "project",
            env=env,
            text=True,
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(
            (self.skills_dir / "demo" / "marker.txt").read_text(), "installed"
        )
        calls = python_log.read_text(encoding="utf-8")
        record_call = next(line for line in calls.splitlines() if "record.py install" in line)
        self.assertIn("--remote-url https://github.com/test/monorepo", record_call)
        self.assertIn("--remote-subpath skills/demo", record_call)
        self.assertNotIn("/tree/main/skills/demo --remote-subpath", record_call)

    def test_whole_repository_install_still_records_remote_metadata(self):
        remote = self.base / "root-skill-remote"
        remote.mkdir()
        self.git("init", cwd=remote)
        self.git("config", "user.name", "Skill Manager Test", cwd=remote)
        self.git("config", "user.email", "test@example.invalid", cwd=remote)
        (remote / "SKILL.md").write_text(
            "---\nname: root-skill\ndescription: Root repository test skill.\n---\n",
            encoding="utf-8",
        )
        (remote / "marker.txt").write_text("installed", encoding="utf-8")
        self.git("add", ".", cwd=remote)
        self.git("commit", "-m", "initial root skill", cwd=remote)
        self.git("branch", "-M", "main", cwd=remote)
        source = "https://github.com/test/root-skill"
        fake_bin, env = self.git_url_wrapper_env(
            remote,
            "root-install-fake-bin",
            remote_source_url=source,
        )
        python_log = self.base / "root-python-calls.log"
        python_wrapper = fake_bin / "python3"
        python_wrapper.write_text(
            "#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"$PYTHON_CALL_LOG\"\nexit 0\n",
            encoding="utf-8",
        )
        python_wrapper.chmod(0o755)
        env["PYTHON_CALL_LOG"] = str(python_log)

        result = subprocess.run(
            [
                "bash",
                str(self.manager / "scripts" / "install.sh"),
                "--target",
                str(self.agent_dir),
                source,
            ],
            cwd=self.base / "project",
            env=env,
            text=True,
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self.assertEqual(result.returncode, 0, result.stdout)
        installed = self.skills_dir / "root-skill"
        self.assertEqual((installed / "marker.txt").read_text(), "installed")
        self.assertFalse((installed / ".git").exists())
        calls = python_log.read_text(encoding="utf-8")
        record_call = next(line for line in calls.splitlines() if "record.py install" in line)
        self.assertIn(f"--remote-url {source}", record_call)
        self.assertIn("--install-branch main", record_call)
        self.assertNotIn("--remote-subpath", record_call)

    def test_shorthand_subdirectory_install_separates_branch_and_path(self):
        remote, _ = self.make_remote(marker="installed")
        fake_bin, env = self.git_url_wrapper_env(remote, "shorthand-install-fake-bin")
        python_log = self.base / "shorthand-python-calls.log"
        python_wrapper = fake_bin / "python3"
        python_wrapper.write_text(
            "#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"$PYTHON_CALL_LOG\"\nexit 0\n",
            encoding="utf-8",
        )
        python_wrapper.chmod(0o755)
        env["PYTHON_CALL_LOG"] = str(python_log)

        result = subprocess.run(
            [
                "bash",
                str(self.manager / "scripts" / "install.sh"),
                "--target",
                str(self.agent_dir),
                "test/monorepo/main/skills/demo",
            ],
            cwd=self.base / "project",
            env=env,
            text=True,
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(
            (self.skills_dir / "demo" / "marker.txt").read_text(), "installed"
        )
        calls = python_log.read_text(encoding="utf-8")
        record_call = next(line for line in calls.splitlines() if "record.py install" in line)
        self.assertIn("--install-branch main", record_call)
        self.assertIn("--remote-subpath skills/demo", record_call)
        self.assertNotIn("--remote-subpath main/skills/demo", record_call)


if __name__ == "__main__":
    unittest.main()
