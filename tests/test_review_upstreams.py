from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
import review_upstreams as review


PIN = "a" * 40
HEAD = "b" * 40


def link(repo, path, revision=PIN):
    return f"https://github.com/{repo}/blob/{revision}/{path}"


class SourceReviewTests(unittest.TestCase):
    def test_deduplicates_same_pin_across_guides_but_keeps_other_versions(self):
        sources = "\n".join([link("Owner/Repo", "A%20B.js#L4"),
                             link("lingjieheti/loon-adlite", "self.js")])
        coverage = "\n".join([link("owner/repo", "A%20B.js#L99"),
                              link("owner/repo", "A%20B.js", HEAD), link("owner/repo", "branch.js", "main")])
        self.assertEqual(review.cited_files(sources, coverage),
                         {"owner/repo": {(PIN, "A B.js"), (HEAD, "A B.js")}})

    def test_both_revisions_in_queries_are_immutable(self):
        data = {"defaultBranchRef": {"target": {"oid": HEAD}}}
        with patch.object(review, "repository_fields", side_effect=[data, {}]) as query:
            self.assertEqual(review.file_states("abc/repo", [(PIN, "a.js")]), (HEAD, {}))
        expressions = query.call_args_list[1].args[1]
        self.assertIn(f'"{PIN}:a.js"', expressions[0])
        self.assertIn(f'"{HEAD}:a.js"', expressions[1])

    def test_report_distinguishes_changes_withdrawals_and_unverified_pins(self):
        files = ["changed.js", "gone.js", "same.js", "unreadable.js"]
        old_blob = {"__typename": "Blob", "oid": "c" * 40}
        new_blob = {"__typename": "Blob", "oid": "d" * 40}
        states = {"old0": old_blob, "current0": new_blob, "old1": old_blob, "current1": None,
                  "old2": old_blob, "current2": old_blob, "old3": None, "current3": new_blob}
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "SOURCES.md").write_text(link("abc/repo", files[0]), encoding="utf-8")
            (root / "COVERAGE.md").write_text("\n".join(link("abc/repo", f) for f in files), encoding="utf-8")
            captured = StringIO()
            with (patch.object(review, "ROOT", root), patch.object(review, "file_states", return_value=(HEAD, states)) as fetch,
                  patch.object(review.os, "environ", {}), redirect_stdout(captured)):
                self.assertTrue(review.compare())
            fetch.assert_called_once_with("abc/repo", [(PIN, f) for f in files])
            report = captured.getvalue()
            self.assertIn("4 项固定文件记录。内容相同 1 项，内容变化 1 项，原路径已无对应文件 1 项，无法核实 1 项", report)
            self.assertIn(link("abc/repo", "changed.js", HEAD), report)
            self.assertIn(link("abc/repo", "gone.js"), report)
            self.assertIn(link("abc/repo", "unreadable.js"), report)
