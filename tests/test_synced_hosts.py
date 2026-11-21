"""Verify the compiled plugin rules and exercise update, withdrawal and failed snapshots offline."""
import base64
from hashlib import sha1
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
import sync_ad_hosts as sync


# Excerpts from the reviewed upstream data at 564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8.
SNAPSHOT = {
    "jd": "jd.com\nads-union.jd.com @ads\nimg-x.jd.com @ads\nstat.m.jd.com @ads @telemetry",
    "tencent": "qq.com\nadsview.qq.com @ads\nadsview2.qq.com @ads\npush.qq.com @ads",
    "youku": "youku.com\nad.api.3g.youku.com @ads\nad.api.mobile.youku.com @ads\nmsg.youku.com @ads",
}
FIRST = "564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8"
NEXT = "b" * 40
EXPECTED = {"ads-union.jd.com", "adsview.qq.com", "adsview2.qq.com", "ad.api.3g.youku.com", "ad.api.mobile.youku.com"}


class SyncTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        for name in sync.PLUGINS:
            before, after, _ = sync.read_block((ROOT / name).read_text(encoding="utf-8"))
            (self.root / name).write_bytes((before + after).encode())

    def copies(self):
        return [(self.root / name).read_bytes() for name in sync.PLUGINS]

    def test_shipped_rule_blocks(self):
        versions = []
        for name in sync.PLUGINS:
            raw = (ROOT / name).read_text(encoding="utf-8")
            prefix, suffix, hosts = sync.read_block(raw)
            manual = [m[1] for line in (prefix + suffix).splitlines() if (m := sync.RULE.fullmatch(line))]
            self.assertEqual(len(manual), 45)
            self.assertFalse(set(manual) & hosts)
            versions.append(raw[len(prefix):len(raw) - len(suffix)])
        self.assertEqual(*versions)

    def test_two_snapshots_and_no_churn(self):
        self.assertEqual(sync.selected(SNAPSHOT), EXPECTED)
        self.assertTrue(sync.update(self.root, FIRST, SNAPSHOT))
        initial = self.copies()
        self.assertFalse(sync.update(self.root, NEXT, SNAPSHOT))
        self.assertEqual(initial, self.copies())
        files = dict(SNAPSHOT)
        files["tencent"] = "qq.com\nadsview.qq.com @ads\nfull:adsview3.qq.com @ads # newly reviewed by upstream"
        self.assertTrue(sync.update(self.root, NEXT, files))
        for name, data in zip(sync.PLUGINS, self.copies()):
            prefix, suffix, hosts = sync.read_block(data.decode())
            self.assertIn(sync.SOURCE + NEXT, data.decode())
            self.assertEqual(hosts, EXPECTED - {"adsview2.qq.com"} | {"adsview3.qq.com"})
            original_prefix, original_suffix, _ = sync.read_block((ROOT / name).read_text(encoding="utf-8"))
            self.assertEqual((prefix, suffix), (original_prefix, original_suffix))

    def test_only_reviewed_exact_matches_in_correct_category(self):
        mock = dict(SNAPSHOT)
        mock["tencent"] = ("qq.com\nfoo.qq.com @ads\n*.adsview3.qq.com @ads\ninclude:adsview4.qq.com @ads\n"
                           "adsview3.qq.com @ads @telemetry\nregexp:adsview5.qq.com @ads\n"
                           "adsview2.qq.com # @ads\nadsview10.qq.com @ads\nadsview3.qq.com.example.org @ads\n"
                           "adsview.qq.com @ads\nadsview.qq.com @ads\n[Script]\nscript-url=https://example.org")
        mock["jd"] += "\nadsview4.qq.com @ads"
        self.assertEqual(sync.selected(mock), EXPECTED - {"adsview2.qq.com"})

    def test_suspicious_snapshots_and_broken_second_plugin_preserve_files(self):
        sync.update(self.root, FIRST, SNAPSHOT)
        empty = {n: src.splitlines()[0] + "\nunrelated.example @ads" for n, src in SNAPSHOT.items()}
        for files in ({}, dict(SNAPSHOT, jd=""), empty, dict(empty, jd=SNAPSHOT["jd"])):
            with self.subTest(files=files):
                before = self.copies()
                with self.assertRaises(ValueError):
                    sync.update(self.root, NEXT, files)
                self.assertEqual(before, self.copies())
        second = self.root / sync.PLUGINS[1]
        second.write_bytes(second.read_bytes().replace(sync.END.encode(), b""))
        before = self.copies()
        with self.assertRaises(ValueError):
            sync.update(self.root, NEXT, SNAPSHOT)
        self.assertEqual(before, self.copies())

    def test_git_contents_integrity_and_immutable_urls(self):
        def github(path):
            if path == "git/ref/heads/master":
                return {"ref": "refs/heads/master", "object": {"sha": FIRST, "type": "commit"}}
            name, query = path.split("?", 1)
            self.assertEqual(query, "ref=" + FIRST)
            dataset = name.split("/")[-1]
            data = SNAPSHOT[dataset].encode()
            digest = sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            return {"path": "data/" + dataset, "type": "file", "encoding": "base64", "size": len(data),
                    "sha": digest, "content": base64.b64encode(data).decode()}

        with patch.object(sync, "github", side_effect=github):
            self.assertEqual(sync.snapshot(), (FIRST, SNAPSHOT))

        def corrupted(path):
            item = github(path)
            if path.startswith("contents/"):
                item["sha"] = "0" * 40
            return item

        with patch.object(sync, "github", side_effect=corrupted), self.assertRaises(ValueError):
            sync.snapshot()
