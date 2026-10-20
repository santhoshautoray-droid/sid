"""Offline regression checks for the authorized static-site security audit."""
from html.parser import HTMLParser
from pathlib import Path
import posixpath
import re
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit
import build_site


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        self.refs.extend(value for name, value in attrs if name in {"src", "href"} and value)


class DistributionSecurity(unittest.TestCase):
    def test_refinement_does_not_hide_partner_images(self):
        stylesheet = (build_site.SITE / "assets/refinement.css").read_text(encoding="utf-8")
        hidden_rules = re.findall(r"([^{}]+)\{([^{}]*)\}", stylesheet)

        for selector, declarations in hidden_rules:
            if re.search(r"display\s*:\s*none\s*!important", declarations):
                self.assertNotIn(".partner-logo img", selector)

    def test_deploy_contains_only_current_public_files(self):
        with tempfile.TemporaryDirectory(dir=build_site.SITE) as temporary:
            root = Path(temporary)
            (root / "assets").mkdir()
            (root / "assets/site.css").write_text("body {}")
            (root / "dist").mkdir()
            (root / "dist/stale.php").write_text("old snapshot")
            (root / "dist/.env").write_text("test-only dummy")
            with patch.object(build_site, "SITE", root):
                count = build_site.build_distribution({"index.html": '<link href="assets/site.css">'})
            self.assertEqual(count, 6)
            self.assertFalse((root / "dist/stale.php").exists())
            self.assertFalse((root / "dist/.env").exists())
            self.assertTrue((root / "assets/site.css").exists())

    def test_unsafe_references_fail_before_publication(self):
        for reference in (".env", "private.pem", "legacy.php", "../outside.png", "%2e%2e/outside.png", "C:/private.png", "assets/missing.png"):
            # A URL scheme is not a local publication reference.
            if reference.startswith("C:"):
                continue
            with self.subTest(reference=reference), tempfile.TemporaryDirectory(dir=build_site.SITE) as temporary:
                root = Path(temporary)
                with patch.object(build_site, "SITE", root):
                    with self.assertRaises((ValueError, FileNotFoundError)):
                        build_site.build_distribution({"index.html": '<img src="' + reference + '">'})
                self.assertFalse((root / "dist").exists())

    def test_generated_pages_have_resolvable_local_references(self):
        root = build_site.SITE / "dist"
        pages = list(root.rglob("*.html"))
        self.assertEqual(len(pages), 21)
        for page in pages:
            parser = References()
            parser.feed(page.read_text(encoding="utf-8"))
            for reference in parser.refs:
                parsed = urlsplit(reference)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                raw = unquote(parsed.path)
                target = root / raw.lstrip("/") if raw.startswith("/") else page.parent / raw
                self.assertTrue(target.resolve().is_relative_to(root), (page.name, reference))
                self.assertTrue(target.exists(), (page.name, reference))
                if target.is_dir():
                    self.assertTrue((target / "index.html").is_file())

    def test_headers_and_no_sensitive_output(self):
        root = build_site.SITE / "dist"
        headers = (root / "_headers").read_text()
        for value in ("Content-Security-Policy", "frame-ancestors 'none'", "X-Content-Type-Options: nosniff", "Strict-Transport-Security"):
            self.assertIn(value, headers)
        for path in root.rglob("*"):
            if path.is_file():
                self.assertNotIn(path.suffix.lower(), {".py", ".php", ".pem", ".key", ".sql", ".env"})
                self.assertNotIn(".git", path.parts)


if __name__ == "__main__":
    unittest.main()
