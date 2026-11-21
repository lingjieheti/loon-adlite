"""Exercise the publication guard on valid and out-of-scope automated changes."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
from audit_host_update import audit_pairs
from sync_ad_hosts import END, PLUGINS, SOURCE, START


def example_files(hosts):
    result = {}
    body = [SOURCE + "b" * 40, *("DOMAIN," + host + ",REJECT" for host in hosts)] if hosts else []
    for name in PLUGINS:
        text = (ROOT / name).read_bytes()
        left, rest = text.split(START.encode() + b"\n")
        _, right = rest.split(END.encode())
        block = "\n".join([START, *body, END]).encode()
        result[name] = left + block + right
    return result


class PublicationAudit(unittest.TestCase):
    def test_valid_change(self):
        audit_pairs(example_files([]), example_files(["ads-union.jd.com"]))
        audit_pairs(example_files(["adsview2.qq.com"]), example_files(["adsview3.qq.com"]))

    def test_outside_edits_are_blocked_on_either_plugin(self):
        before = example_files([])
        for name in PLUGINS:
            with self.subTest(name=name):
                changed = example_files(["adsview.qq.com"])
                changed[name] = changed[name].replace(b"DOMAIN,dsp-x.jd.com,REJECT", b"DOMAIN,jd.com,REJECT")
                with self.assertRaisesRegex(ValueError, "outside"):
                    audit_pairs(before, changed)

    def test_scope_and_cross_plugin_integrity(self):
        before = example_files([])
        for forbidden in ("jd.com", "*.qq.com"):
            with self.subTest(forbidden=forbidden), self.assertRaises(ValueError):
                audit_pairs(before, example_files([forbidden]))
        after = example_files(["adsview2.qq.com"])
        after[PLUGINS[0]] = after[PLUGINS[0]].replace(b"b" * 40, b"c" * 40)
        with self.assertRaisesRegex(ValueError, "revisions differ"):
            audit_pairs(before, after)
        with self.assertRaisesRegex(ValueError, "large"):
            audit_pairs(example_files(["adsview.qq.com"]),
                        example_files([f"adsview{i}.qq.com" for i in range(1, 5)]))
