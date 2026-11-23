"""Exercise the release gate against real Git diffs and the checked-out plugin files."""
import contextlib
import io
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
import audit_release as gate
import audit_host_update
from sync_ad_hosts import CANDIDATES


ENTRY = "- 范围：审核网页广告脚本更新\n- 风险：保持设备权限不变\n- 验证：运行实际脚本测试\n"


class ReleaseAuditTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        for name in gate.PROFILES:
            shutil.copyfile(ROOT / name, self.repo / name)
        (self.repo / gate.RECORD).write_text("# 审计记录\n", encoding="utf-8")
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "false")
        self.base = self.commit()
        location = patch.object(gate, "ROOT", self.repo)
        location.start()
        self.addCleanup(location.stop)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), "-c", "user.name=Test", "-c",
                                       "user.email=test@example.org", "-c", "commit.gpgSign=false", *args])

    def commit(self):
        self.git("add", "--all")
        self.git("commit", "-qm", "test revision")
        return self.git("rev-parse", "HEAD").decode().strip()

    def test_regular_docs_get_visible_metrics_and_summary(self):
        (self.repo / "README.md").write_text("Example", encoding="utf-8")
        head = self.commit()
        report = {}
        with patch.object(audit_host_update, "snapshot", side_effect=AssertionError("unrelated release fetched source")):
            gate.run(self.base, head, False, report)
        self.assertEqual(report["变更文件"], ["README.md"])
        self.assertEqual(report["手工精确域名数"], 77)
        self.assertEqual(report["HTTPS 主机数"], 41)
        self.assertEqual(report["复写条数"], 48)
        with self.assertRaises(ValueError):
            gate.run(self.base, self.base, False, {})
        with self.assertRaises(ValueError):
            gate.run("main", head, False, {})

    def test_runtime_change_requires_new_review(self):
        (self.repo / "sample.js").write_text("// local helper", encoding="utf-8")
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "new scope"):
            gate.run(self.base, head, False, {})
        (self.repo / gate.RECORD).write_text(ENTRY, encoding="utf-8")
        head = self.commit()
        report = {}
        gate.run(self.base, head, False, report)
        self.assertEqual(report["专项审计记录"], gate.RECORD)
        self.assertEqual(report["运行时脚本变更"], ["sample.js"])
        self.assertFalse(gate.has_new_record(ENTRY, "# relocated\n" + ENTRY))
        self.assertFalse(gate.has_new_record("", ENTRY.replace("风险", "范围")))
        self.assertFalse(gate.has_new_record("", ENTRY.replace("保持设备权限不变", "已看")))

    def test_scheduled_poll_verifies_same_head_and_propagates_origin_failures(self):
        current = "c" * 40
        with patch.object(gate, "verify_source", return_value={"核验上游提交": current}) as verify:
            report = {}
            gate.run(self.base, self.base, False, report, current)
            self.assertIn("无需发版", report["类别"])
            self.assertEqual(report["核验上游提交"], current)
            self.assertEqual(verify.call_args.args[1], current)
            self.assertEqual(verify.call_args.kwargs, {"unchanged": True})
        with patch.object(gate, "verify_source", side_effect=ValueError("source unavailable")):
            with self.assertRaisesRegex(ValueError, "source unavailable"):
                gate.run(self.base, self.base, False, {}, current)
        (self.repo / "README.md").write_text("Changed", encoding="utf-8")
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "current release"):
            gate.run(self.base, head, False, {}, current)

    def test_automated_mode_never_falls_back_to_manual_review(self):
        (self.repo / gate.RECORD).write_text(ENTRY, encoding="utf-8")
        head = self.commit()
        with patch.object(gate, "audit_commits", side_effect=ValueError("restricted")) as guard:
            with self.assertRaisesRegex(ValueError, "restricted"):
                gate.run(self.base, "HEAD", True, {})
        guard.assert_called_once_with(self.base, head, None)

    def test_pure_managed_diff_needs_no_manual_record(self):
        for name in gate.PLUGINS:
            path = self.repo / name
            before, after, hosts = gate.read_block(path.read_bytes().decode())
            new = hosts ^ {"adsview3.qq.com"}
            if not new:
                new.add("adsview2.qq.com")
            block = ["# Source: v2ray/domain-list-community@" + "a" * 40,
                     *(f"DOMAIN,{h},REJECT" for h in sorted(new))]
            newline = "\r\n" if before.endswith("\r\n") else "\n"
            path.write_bytes((before + newline.join(block) + newline + after).encode())
        head = self.commit()
        report = {}
        sources = {key: domain + "\n" + "\n".join(f"{h} @ads" for h in new & allowed)
                   for key, (domain, allowed) in CANDIDATES.items()}
        with patch.object(audit_host_update, "snapshot", return_value=("a" * 40, sources)) as fetch:
            gate.run(self.base, head, False, report)
        fetch.assert_called_once_with("a" * 40)
        self.assertIn("仅受管", report["类别"])
        (self.repo / gate.RECORD).write_text(ENTRY, encoding="utf-8")
        (self.repo / "sample.js").write_text("// unrelated local change", encoding="utf-8")
        head = self.commit()
        with patch.object(audit_host_update, "snapshot", side_effect=ValueError("source is missing")):
            with self.assertRaisesRegex(ValueError, "source is missing"):
                gate.run(self.base, head, False, {})

    def test_failure_reports_without_rendering_filename_markup(self):
        dest = self.repo / "summary"
        with patch.object(gate.os, "environ", {"GITHUB_STEP_SUMMARY": str(dest)}), contextlib.redirect_stdout(io.StringIO()):
            with patch.object(sys, "argv", ["audit", "--base", "invalid", "--head", "HEAD"]):
                self.assertEqual(gate.main(), 1)
            gate.publish_summary({"file": "```malformed"})
        text = dest.read_text(encoding="utf-8")
        self.assertIn('"结果": "失败"', text)
        self.assertNotIn("```malformed", text)
