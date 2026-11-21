"""Keep Safari helpers limited to their reviewed sites, permissions and update files."""

from collections import defaultdict
import os
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = "https://github.com/lingjieheti/loon-adlite"
UPDATE_BASE = "https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/"
MATCHES = {
    "web/pornhub.user.js": ["https://*.pornhub.com/*"],
    "youtube/youtube.user.js": ["https://m.youtube.com/*", "https://www.youtube.com/*"],
}
OPEN = "// ==UserScript=="
CLOSE = "// ==/UserScript=="


def read_metadata(source):
    lines = source.splitlines()
    if not lines or lines[0] != OPEN or source.count(OPEN) != 1 or source.count(CLOSE) != 1 or CLOSE not in lines:
        raise ValueError("Expected one unambiguous userscript header at the start of the file")
    metadata = defaultdict(list)
    # Userscripts recognizes both // @key and bare @key. Parse every line of our header.
    for line in lines[1:lines.index(CLOSE)]:
        item = re.fullmatch(r"[ \t]*(?://)?[ \t]*@([\w-]+)(?:[ \t]+([^\t\r\n]+?))?[ \t]*", line)
        if not item:
            raise ValueError(f"Unrecognized metadata line: {line!r}")
        metadata[item[1]].append(item[2] or "")
    return metadata


def update_version(path, metadata):
    values = metadata.get("version", [])
    if len(values) != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", values[0], flags=re.ASCII):
        raise ValueError(f"{path}: expected one three-part numeric update version")
    version = tuple(map(int, values[0].split(".")))
    # Userscripts compares each component using Swift's signed Int on iOS.
    if any(n > 2**63 - 1 for n in version):
        raise ValueError(f"{path}: version component is too large for Userscripts")
    return version


def check_header(path, source):
    metadata = read_metadata(source)
    expected = {
        "namespace": [PROJECT],
        "match": sorted(MATCHES[path]),
        "run-at": ["document-end" if path == "web/pornhub.user.js" else "document-idle"],
        "grant": ["none"],
        "inject-into": ["content"],
        "noframes": [""],
        "updateURL": [UPDATE_BASE + path],
    }
    if set(metadata) != set(expected) | {"name", "description", "version"}:
        raise ValueError(f"{path}: unexpected or missing metadata: {sorted(metadata)}")
    for key, values in expected.items():
        if sorted(metadata[key]) != values:
            raise ValueError(f"{path}: unexpected @{key}: {metadata[key]}")
    for key in ("name", "description"):
        if len(metadata[key]) != 1 or not metadata[key][0].strip():
            raise ValueError(f"{path}: expected one @{key} value")
    update_version(path, metadata)


def require_version_bump(path, previous, current):
    new = update_version(path, read_metadata(current))
    if previous is None or previous == current:
        return
    old = update_version(path, read_metadata(previous))
    if new <= old:
        raise ValueError(f"{path}: changed script must increase @version beyond {'.'.join(map(str, old))}")


class SafariPermissions(unittest.TestCase):
    def test_every_published_userscript_has_reviewed_permissions(self):
        files = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.user.js")}
        self.assertEqual(files, set(MATCHES))
        for path in sorted(files):
            with self.subTest(path=path):
                check_header(path, (ROOT / path).read_text(encoding="utf-8"))

    @unittest.skipUnless("RELEASE_BASE" in os.environ, "Release comparison needs a base commit")
    def test_changed_scripts_increment_their_published_version(self):
        base = os.environ["RELEASE_BASE"]
        self.assertRegex(base, r"\A[0-9a-f]{40}\Z", "Expected the base commit SHA from the release event")
        git = ["git", "-C", str(ROOT)]
        # Missing commits/trees must fail. Only a path absent from a readable tree is new.
        tracked = subprocess.check_output([*git, "ls-tree", "-r", "--name-only", "-z",
                                           base + "^{commit}", "--", *MATCHES]).decode().split("\0")
        for path in MATCHES:
            with self.subTest(path=path):
                previous = subprocess.check_output([*git, "show", f"{base}:{path}"], text=True,
                                                   encoding="utf-8") if path in tracked else None
                current = (ROOT / path).read_text(encoding="utf-8")
                require_version_bump(path, previous, current)

    def test_new_unchanged_and_updated_versions(self):
        path = "youtube/youtube.user.js"
        old = f"{OPEN}\n// @version 1.9.0\n{CLOSE}\n"
        require_version_bump(path, None, old)
        require_version_bump(path, old, old)
        require_version_bump(path, old, old.replace("1.9.0", "1.10.0") + "doWork();")
        for version in ("1.8.1", "1.9.0", "1.9", "1.9.9223372036854775808"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                require_version_bump(path, old, old.replace("1.9.0", version) + "doWork();")

    def test_unreviewed_headers_are_rejected(self):
        path = "youtube/youtube.user.js"
        source = (ROOT / path).read_text(encoding="utf-8")
        check_header(path, source)
        for directive in (
            "// @grant GM_xmlhttpRequest", "\t@require https://example.org/latest.js",
            "// @resource tracking https://example.org/pixel", "// @connect *",
            "// @include https://*/*", "// @match https://accounts.google.com/*",
            "// @downloadURL https://example.org/helper.user.js",
            "// @updateURL " + UPDATE_BASE + path, "// @noframes",
        ):
            with self.subTest(directive=directive), self.assertRaises(ValueError):
                check_header(path, source.replace(CLOSE, directive + "\n" + CLOSE, 1))
        for before, after in (
            (UPDATE_BASE, "https://raw.githubusercontent.com/example/fork/main/"),
            (UPDATE_BASE + path, UPDATE_BASE + "youtube/another.user.js"),
            ("// @inject-into  content", "// @inject-into  page"),
            ("// @noframes\n", ""),
            (CLOSE, CLOSE + "\n" + OPEN + "\n// @grant GM_openInTab\n" + CLOSE),
        ):
            with self.subTest(change=after), self.assertRaises(ValueError):
                check_header(path, source.replace(before, after, 1))
