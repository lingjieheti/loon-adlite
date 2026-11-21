"""Keep all three sponsorship pages aligned with the owner's verified QR codes."""

import hashlib
from html import unescape
from pathlib import Path
import re
import subprocess
import unittest
from urllib.parse import unquote


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
LEGACY_PAYPAL_JPG = "5779fce8c99512817e135a4c1535680f1d4cb48d7b08659e199a425e553d541a"
# SHA-256 fingerprints allow checking renamed copies without including the old payment links or images.
WITHDRAWN_IMAGES = {
    "c2a83d82d48f9432a58f995d452f40bb3e3cfd295055e934a29ba294e456bab1",
    "6508037243e1a0236df8e56ff2cd0297ce13b34ea49b6af05dc8b67512814c9f",
    "56be3cffa81c8ebf5eb5e2dbce327f69603ff8891809c202ad56351102491a91",
    "5180dea67d37f87525a9b3238677033b091eacffd8426567f1470adf1e44e5c7",
}
WITHDRAWN_LINK = re.compile(r"\b(?:qr[.]alipay[.]com/|wxp://|weixin://wxpay/)[a-z0-9]", re.I)
INLINE_LINK = re.compile(r"\[([^\[\]\n<>\\]+)\]\(([^()\s<>\\]+)\)")


def page_links(body):
    """The sponsorship pages use plain text and inline Markdown links only."""
    destinations = []

    def replace(link):
        destinations.append(link[2])
        return link[1]

    remaining = INLINE_LINK.sub(replace, body)
    if "![" in body or re.search(r"[<>\[\]\\]|://|\bwww[.]|\b[\w.+-]+@[\w.-]+[.]\w+", unescape(remaining), re.I):
        raise ValueError("Unexpected image, HTML, link or contact address on sponsorship page")
    return destinations


def has_withdrawn_data(data):
    if data.startswith((b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff")):
        return hashlib.sha256(data).hexdigest() in WITHDRAWN_IMAGES
    if b"\0" in data:
        return False
    return bool(WITHDRAWN_LINK.search(unquote(unescape(data.decode("utf-8", errors="replace")))))


class SponsorshipTests(unittest.TestCase):
    def test_published_images_match_verified_codes(self):
        folder = ROOT / "assets" / "sponsor"
        self.assertEqual({file.name for file in folder.iterdir()}, set(QR_HASHES) | {"paypal.jpg"})
        for filename, digest in {**QR_HASHES, "paypal.jpg": LEGACY_PAYPAL_JPG}.items():
            with self.subTest(filename=filename):
                code = (folder / filename).read_bytes()
                self.assertEqual(hashlib.sha256(code).hexdigest(), digest)

    def test_payment_destinations_and_language_navigation(self):
        pages = {"SPONSOR.md", "SPONSOR.en.md", "SPONSOR.ja.md"}
        for page in pages:
            with self.subTest(page=page):
                readme = page.replace("SPONSOR", "README")
                self.assertIn(f"]({page})", (ROOT / readme).read_text(encoding="utf-8"))
                body = (ROOT / page).read_text(encoding="utf-8")
                links = page_links(body)
                expected = (pages - {page}) | {readme} | PAYMENT_LINKS
                expected.update(QR_BASE + name for name in QR_HASHES)
                self.assertCountEqual(links, expected)
                self.assertEqual(re.findall(r"^`([^`\n]+)`$", body, flags=re.MULTILINE), [TRON_ADDRESS])

    def test_no_withdrawn_codes_in_tracked_files(self):
        paths = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-z"]).decode().split("\0")
        for path in filter(None, paths):
            with self.subTest(path=path):
                self.assertFalse(has_withdrawn_data((ROOT / path).read_bytes()), "Withdrawn payment material")

    def test_other_link_formats_cannot_add_destinations(self):
        for markup in ("https://example.org/donate", "<https://example.org>", "[give][id]\n[id]: /new",
                       '<a href="/new">Give</a>', "![code](https://example.org/qr.png)",
                       "www.example.org/donate", "give@example.org"):
            with self.subTest(markup=markup), self.assertRaises(ValueError):
                page_links(markup)
        self.assertEqual(page_links("[Give](/allowed)"), ["/allowed"])

    def test_detects_encoded_receiving_links_without_matching_app_docs(self):
        for link in (b"qr.alipay." + b"com/example", b"wxp:" + b"//example",
                     b"weixin%3A" + b"%2F%2Fwxpay%2Fexample", b"wxp&#58;" + b"//example"):
            self.assertTrue(has_withdrawn_data(link))
        self.assertFalse(has_withdrawn_data(b"Documentation about WeChat and Alipay"))
