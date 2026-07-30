import importlib.util
import os
import unittest
from unittest import mock


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_PATH = os.path.join(ROOT, "scripts", "check_skills.py")
SPEC = importlib.util.spec_from_file_location("check_skills", MODULE_PATH)
check_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_skills)


class FrontmatterParsingTests(unittest.TestCase):
    def test_valid_yaml_supports_multiline_description(self):
        content = """---
name: demo-skill
description: |
  A useful demo skill.
  It has multiple lines.
---
"""
        parsed = check_skills.parse_frontmatter(content, strict=True)
        self.assertEqual(parsed["name"], "demo-skill")
        self.assertIn("multiple lines", parsed["description"])

    @unittest.skipIf(check_skills.YAML_LIB is None, "PyYAML is not installed")
    def test_invalid_yaml_is_not_accepted_by_fallback(self):
        content = """---
name: demo-skill
description: invalid: unquoted colon
---
"""
        with self.assertRaises(check_skills.FrontmatterParseError):
            check_skills.parse_frontmatter(content)

    def test_strict_mode_rejects_missing_pyyaml(self):
        content = """---
name: demo-skill
description: A useful demo skill.
---
"""
        with mock.patch.object(check_skills, "YAML_LIB", None):
            with self.assertRaises(check_skills.FrontmatterParseError):
                check_skills.parse_frontmatter(content, strict=True)

    def test_non_strict_mode_keeps_compatibility_fallback(self):
        content = """---
name: demo-skill
description: A useful demo skill.
---
"""
        with mock.patch.object(check_skills, "YAML_LIB", None):
            parsed = check_skills.parse_frontmatter(content, strict=False)
        self.assertEqual(parsed["name"], "demo-skill")


if __name__ == "__main__":
    unittest.main()
