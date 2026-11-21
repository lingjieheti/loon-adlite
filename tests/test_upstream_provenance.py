"""Verify source reachability, license identity and no-change source evidence offline."""
import subprocess
import unittest
from unittest.mock import call, patch

import test_synced_hosts as fixtures
from test_publication_audit import example_files
import audit_host_update as audit
import sync_ad_hosts as sync


class UpstreamProvenanceTests(unittest.TestCase):
    def test_candidate_matches_only_the_complete_selection_from_the_reported_revision(self):
        recorded = "b" * 40
        other = "c" * 40
        files = example_files(sorted(fixtures.EXPECTED))
        with patch.object(audit, "snapshot", return_value=(recorded, fixtures.SNAPSHOT)) as fetch:
            evidence = audit.verify_source(files, recorded)
            self.assertEqual(evidence["核验上游域名数"], len(fixtures.EXPECTED))
            fetch.assert_called_once_with(recorded)
            with self.assertRaisesRegex(ValueError, "reported source"):
                audit.verify_source(files, other)
            with self.assertRaisesRegex(ValueError, "complete selection"):
                audit.verify_source(example_files(sorted(fixtures.EXPECTED - {"adsview2.qq.com"})), recorded)
            with self.assertRaisesRegex(ValueError, "complete selection"):
                audit.verify_source(example_files(sorted(fixtures.EXPECTED | {"adsview3.qq.com"})), recorded)

    def test_no_change_verifies_latest_and_recorded_revisions_without_rewriting_the_source(self):
        recorded, current = "b" * 40, "c" * 40
        published = example_files(sorted(fixtures.EXPECTED))
        initial = dict(published)
        with patch.object(audit, "snapshot", side_effect=lambda revision: (revision, fixtures.SNAPSHOT)) as fetch:
            evidence = audit.verify_source(published, current, unchanged=True)
            self.assertEqual(fetch.call_args_list, [call(current), call(recorded)])
            self.assertEqual(evidence["核验上游提交"], current)
            self.assertEqual(evidence["插件标记的上游提交"], recorded)
            self.assertEqual(published, initial)
        with patch.object(audit, "snapshot", return_value=(recorded, fixtures.SNAPSHOT)):
            with self.assertRaisesRegex(ValueError, "complete selection"):
                audit.verify_source(published, current, unchanged=True)

    def test_pinned_fetch_checks_license_and_accepts_only_upstream_branch_ancestors(self):
        fixture = fixtures.SyncTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        source, older = fixture.git_fixture()
        _, abandoned = fixture.git_fixture(jd=b"jd.com\nunused.jd.com @ads")
        replacement = b"jd.com\nad-server.invalid @ads"
        _, latest = fixture.git_fixture(jd=replacement, parent=older)
        real_git = sync.git

        def offline_git(directory, *args, **kwargs):
            if args[0] != "fetch":
                return real_git(directory, *args, **kwargs)
            self.assertEqual(args[-2:], ("https://github.com/v2ray/domain-list-community.git",
                                         "refs/heads/master:refs/heads/upstream"))
            return subprocess.check_output(["git", "-C", directory, *args[:-2], source.as_uri(), args[-1]])

        with patch.object(sync, "git", side_effect=offline_git):
            self.assertEqual(sync.snapshot(older), (older, fixtures.SNAPSHOT))
            self.assertEqual(sync.snapshot(latest)[1]["jd"], replacement.decode())
            with self.assertRaises(subprocess.CalledProcessError):
                sync.snapshot(abandoned)
            for license_text in (None, b"changed license"):
                with self.subTest(license_text=license_text):
                    _, revision = fixture.git_fixture(license_text=license_text, parent=latest)
                    with self.assertRaisesRegex(ValueError, "LICENSE|missing"):
                        sync.snapshot(revision)
