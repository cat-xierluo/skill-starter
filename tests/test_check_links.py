import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from urllib.error import HTTPError, URLError


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "check_links.py"
SPEC = importlib.util.spec_from_file_location("check_links_external", MODULE_PATH)
check_links = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_links)


class ExternalLinkCheckTests(unittest.TestCase):
    def test_head_rejection_falls_back_to_lightweight_get(self):
        head_rejected = HTTPError(
            "https://example.com", 405, "method not allowed", {}, None
        )
        with mock.patch.object(
            check_links,
            "_request_external",
            side_effect=[head_rejected, 206],
        ) as request:
            code = check_links._request_external_with_fallback(
                "https://example.com", timeout=1
            )

        self.assertEqual(code, 206)
        self.assertEqual(request.call_args_list[0].args[2], "HEAD")
        self.assertEqual(request.call_args_list[1].args[2], "GET")

    def test_transient_failure_is_retried_then_succeeds(self):
        temporary = HTTPError(
            "https://example.com", 503, "unavailable", {}, None
        )
        with mock.patch.object(
            check_links,
            "_request_external_with_fallback",
            side_effect=[temporary, 204],
        ) as request:
            result = check_links.probe_external_url(
                "https://example.com", retries=3, backoff=0
            )

        self.assertEqual(result.status, "ok")
        self.assertEqual(result.attempts, 2)
        self.assertEqual(request.call_count, 2)

    def test_404_is_a_deterministic_broken_link(self):
        missing = HTTPError("https://example.com/missing", 404, "missing", {}, None)
        with mock.patch.object(
            check_links, "_request_external_with_fallback", side_effect=missing
        ):
            result = check_links.probe_external_url(
                "https://example.com/missing", retries=3, backoff=0
            )

        self.assertEqual(result.status, "broken")
        self.assertEqual(result.attempts, 1)

    def test_access_restriction_is_reported_without_false_broken_result(self):
        restricted = HTTPError(
            "https://example.com/private", 403, "forbidden", {}, None
        )
        with mock.patch.object(
            check_links, "_request_external_with_fallback", side_effect=restricted
        ):
            result = check_links.probe_external_url(
                "https://example.com/private", retries=3, backoff=0
            )

        self.assertEqual(result.status, "restricted")
        self.assertEqual(result.attempts, 1)

    def test_network_failure_retries_and_remains_transient(self):
        with mock.patch.object(
            check_links,
            "_request_external_with_fallback",
            side_effect=URLError("temporary dns failure"),
        ) as request:
            result = check_links.probe_external_url(
                "https://example.com", retries=2, backoff=0
            )

        self.assertEqual(result.status, "transient")
        self.assertEqual(result.attempts, 2)
        self.assertEqual(request.call_count, 2)

    def test_allowlist_supports_glob_patterns(self):
        with tempfile.TemporaryDirectory() as tempdir:
            allowlist = Path(tempdir) / "allowlist.txt"
            allowlist.write_text(
                "# comment\nhttps://discord.com/invite/*\n", encoding="utf-8"
            )
            patterns = check_links.load_external_allowlist(str(allowlist))

        self.assertTrue(
            check_links.is_external_allowed(
                "https://discord.com/invite/clawd", patterns
            )
        )
        self.assertFalse(
            check_links.is_external_allowed("https://discord.com/channels/1", patterns)
        )


if __name__ == "__main__":
    unittest.main()
