"""Keep all three sponsorship pages aligned with the owner's verified QR codes."""

import hashlib
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
QR_BASE = "https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/assets/sponsor/"
PAYMENT_LINKS = {
    "https://www.paypal.com/qrcodes/p2pqrc/8CZSV4VY73PB2",
}
TRON_ADDRESS = "TXE2VuxUSFsenJvmz3Z8oSm7dqPLAUWfRE"
# These images were decoded and checked against the maintainer's original payment codes.
QR_HASHES = {
    "paypal.png": "507ba236f084b1e3b0c31a67c8696a0f4ca013fae53fbd6bd4f4218dc047c9ae",
    "usdt-tron.png": "5e40b0665731164843190e0202a79dbdff7024e22aa9b9c13d969aeac93f20ac",
}


class SponsorshipTests(unittest.TestCase):
    def test_published_images_match_verified_codes(self):
        for filename, digest in QR_HASHES.items():
            with self.subTest(filename=filename):
                code = (ROOT / "assets" / "sponsor" / filename).read_bytes()
                self.assertEqual(hashlib.sha256(code).hexdigest(), digest)

    def test_payment_destinations_and_language_navigation(self):
        pages = {"SPONSOR.md", "SPONSOR.en.md", "SPONSOR.ja.md"}
        for page in pages:
            with self.subTest(page=page):
                readme = page.replace("SPONSOR", "README")
                self.assertIn(f"]({page})", (ROOT / readme).read_text(encoding="utf-8"))
                body = (ROOT / page).read_text(encoding="utf-8")
                links = set(re.findall(r"\]\(([^)]+)\)", body))
                expected = (pages - {page}) | {readme} | PAYMENT_LINKS
                expected.update(QR_BASE + name for name in QR_HASHES)
                self.assertFalse(expected - links, f"Missing links: {expected - links}")
                self.assertEqual(re.findall(r"^`([^`\n]+)`$", body, flags=re.MULTILINE), [TRON_ADDRESS])
                self.assertNotIn("![", body)
                self.assertNotIn("<img", body.lower())
