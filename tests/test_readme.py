"""Check the public ad-blocking subscription on every language homepage."""

from pathlib import Path
import re
import unittest
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[1]
RAW = "https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/"
SUBSCRIPTION = RAW + "iPad-AdSuite.lpx"
IMPORT = "https://www.nsloon.com/openloon/import"
LANGUAGES = "ar en es fr id ja ko ru th vi zh-Hant".split()


class ReadmeTests(unittest.TestCase):
    def test_one_ad_subscription_in_every_language(self):
        pages = sorted(ROOT.glob("README*.md"))
        required = {"README.md"} | {f"README.{lang}.md" for lang in LANGUAGES}
        self.assertEqual(required.difference(page.name for page in pages), set())
        self.assertTrue((ROOT / "iPad-AdSuite.lpx").is_file())
        rewards = {path.relative_to(ROOT).as_posix() for path in (ROOT / "checkin").glob("*.lpx")}
        reward_links = rewards | {RAW + path for path in rewards}

        for page in pages:
            with self.subTest(page=page.name):
                contents = page.read_text(encoding="utf-8")
                imports = []
                for link in re.findall(r"\]\(([^\s()]+)\)", contents):
                    url = urlsplit(link)
                    if url.path == "/openloon/import":
                        self.assertEqual(url._replace(query="", fragment="").geturl(), IMPORT)
                        targets = parse_qs(url.query, keep_blank_values=True).get("plugin", [])
                        self.assertEqual(len(targets), 1, link)
                        if targets[0] not in reward_links:
                            imports.append(targets[0])
                    elif url.path.endswith(".lpx") and link not in reward_links:
                        self.assertEqual(link, SUBSCRIPTION)
                self.assertEqual(imports, [SUBSCRIPTION])
