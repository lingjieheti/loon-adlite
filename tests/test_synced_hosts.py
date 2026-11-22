"""Verify the compiled plugin rules and exercise update, withdrawal and failed snapshots offline."""
from pathlib import Path
from hashlib import sha256
import subprocess
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
FIXTURE_LICENSE = b"Reviewed test license\n"


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.license_pin = patch.object(sync, "LICENSE_SHA256", sha256(FIXTURE_LICENSE).hexdigest())
        self.license_pin.start()
        self.addCleanup(self.license_pin.stop)
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
            self.assertEqual(len(manual), 78)
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

    def git_fixture(self, mode="100644", jd=SNAPSHOT["jd"].encode(), license_text=FIXTURE_LICENSE, parent=None):
        # Construct Git objects directly so symlink tests also run on Windows without link privileges.
        repo = self.root / "upstream.git"
        repo.mkdir(exist_ok=True)

        def write(*args, payload=b""):
            command = ["git", "-C", str(repo), "-c", "user.name=Test", "-c", "user.email=test@example.org",
                       "-c", "commit.gpgSign=false", *args]
            return subprocess.check_output(command, input=payload).strip()

        write("init", "--bare", "--quiet", "--object-format=sha1", "--template=")
        entries = []
        for name, contents in SNAPSHOT.items():
            if name == "jd" and jd is None:
                continue
            oid = write("hash-object", "-w", "--stdin", payload=jd if name == "jd" else contents.encode())
            entry_mode = mode if name == "jd" else "100644"
            entries.append(entry_mode.encode() + b" blob " + oid + b"\t" + name.encode() + b"\n")
        data = write("mktree", payload=b"".join(entries))
        contents = b"040000 tree " + data + b"\tdata\n"
        if license_text is not None:
            license_blob = write("hash-object", "-w", "--stdin", payload=license_text)
            contents += b"100644 blob " + license_blob + b"\tLICENSE\n"
        tree = write("mktree", payload=contents)
        parents = ["-p", parent] if parent else []
        commit = write("commit-tree", tree.decode(), *parents, "-m", "fixture").decode()
        write("update-ref", "refs/heads/master", commit)
        return repo, commit

    def test_anonymous_shallow_snapshot_reads_pinned_regular_blobs(self):
        source, commit = self.git_fixture()
        real_git = sync.git

        def offline_git(directory, *args, **kwargs):
            if args[0] == "fetch":
                self.assertIn("--depth=1", args)
                self.assertIn("--no-tags", args)
                self.assertEqual(args[-2:], ("https://github.com/v2ray/domain-list-community.git",
                                             "refs/heads/master:refs/heads/upstream"))
                # Only the test substitutes a file transport for the public HTTPS source.
                return subprocess.check_output(["git", "-C", directory, *args[:-2], source.as_uri(), args[-1]])
            return real_git(directory, *args, **kwargs)

        with patch.object(sync, "git", side_effect=offline_git):
            self.assertEqual(sync.snapshot(), (commit, SNAPSHOT))
        self.git_fixture(jd=b"jd.com\nchanged.example @ads")
        self.assertEqual(sync.read_snapshot(source, commit), SNAPSHOT)

    def test_refuses_symlinks_missing_oversized_and_changed_git_blobs(self):
        for mode, payload in (("120000", b"../../elsewhere"), ("100755", b"script"),
                              ("100644", None), ("100644", b""), ("100644", b"x" * (sync.MAX_FILE + 1))):
            with self.subTest(mode=mode, size=len(payload) if payload is not None else None):
                repo, commit = self.git_fixture(mode, payload)
                with self.assertRaises(ValueError):
                    sync.read_snapshot(repo, commit)
        repo, commit = self.git_fixture()
        real_git = sync.git

        def damaged_git(directory, *args):
            data = real_git(directory, *args)
            return b"X" + data[1:] if args[:2] == ("cat-file", "blob") else data

        with patch.object(sync, "git", side_effect=damaged_git), self.assertRaisesRegex(ValueError, "Git blob"):
            sync.read_snapshot(repo, commit)
