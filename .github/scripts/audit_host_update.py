"""Check the exact release diff independently of the updater's write operation."""
from pathlib import Path
import subprocess
import sys

from sync_ad_hosts import OID, PLUGINS, read_block


def audit_pairs(before, after):
    managed_blocks = []
    for filename in PLUGINS:
        original = before[filename]
        proposed = after[filename]
        before_prefix, before_suffix, before_hosts = read_block(original.decode("utf-8"))
        after_prefix, after_suffix, after_hosts = read_block(proposed.decode("utf-8"))
        if (before_prefix, before_suffix) != (after_prefix, after_suffix):
            raise ValueError(f"{filename}: update changed content outside the synced domain block")
        if not after_hosts or after_hosts == before_hosts:
            raise ValueError(f"{filename}: expected a change to reviewed ad hosts")
        limit = 3 if before_hosts else 6
        if len(before_hosts ^ after_hosts) > limit:
            raise ValueError(f"{filename}: unusually large host change")
        start = len(after_prefix.encode())
        end = len(proposed) - len(after_suffix.encode())
        managed_blocks.append(proposed[start:end])
    if managed_blocks[0] != managed_blocks[1]:
        raise ValueError("Generated host lists or source revisions differ across subscriptions")


def audit_commits(base, candidate):
    if not all(OID.fullmatch(sha) for sha in (base, candidate)):
        raise ValueError("Expected full commit hashes")
    repo = Path(__file__).resolve().parents[2]
    def git(*args):
        return subprocess.check_output(["git", "-C", str(repo), *args])
    if git("rev-list", "--parents", "-1", candidate).decode().split() != [candidate, base]:
        raise ValueError("Candidate must be a direct, single-parent update of the checked base")
    paths = git("diff", "--no-renames", "--name-status", base, candidate).decode().splitlines()
    if sorted(paths) != sorted("M\t" + name for name in PLUGINS):
        raise ValueError("Only the two existing Loon subscriptions may change")
    copies = []
    for sha in (base, candidate):
        files = {}
        for name in PLUGINS:
            entry = git("ls-tree", sha, "--", name).split(maxsplit=2)
            if entry[:2] != [b"100644", b"blob"]:
                raise ValueError(f"{name}: expected a regular non-executable file")
            files[name] = git("show", f"{sha}:{name}")
        copies.append(files)
    audit_pairs(*copies)


if __name__ == "__main__":
    audit_commits(*sys.argv[1:])
    print("Audited candidate diff: only reviewed exact ad hosts and their source revision changed.")
