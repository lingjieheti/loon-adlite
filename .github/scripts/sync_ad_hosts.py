"""Sync a small reviewed set of exact ad hosts from v2ray/domain-list-community (MIT)."""
from hashlib import sha1, sha256
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
PLUGINS = ("iPad-AdLite.lpx", "iPad-AdSuite.lpx")
REPOSITORY = "v2ray/domain-list-community"
CANDIDATES = {
    "jd": ("jd.com", {"ads-union.jd.com"}),
    "tencent": ("qq.com", {"adsview.qq.com", *(f"adsview{i}.qq.com" for i in range(1, 10))}),
    "youku": ("youku.com", {"ad.api.3g.youku.com", "ad.api.mobile.youku.com"}),
}
APPROVED = set.union(*(hosts for _, hosts in CANDIDATES.values()))
START = "# BEGIN synced ad hosts"
END = "# END synced ad hosts"
SOURCE = f"# Source: {REPOSITORY}@"
OID = re.compile(r"[0-9a-f]{40}")
RULE = re.compile(r"DOMAIN,([a-z0-9.-]+),REJECT")
MAX_FILE = 256 * 1024
# Reviewed MIT license at 564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8.
LICENSE_SHA256 = "b9d84a22870d3f21c91a4c6e410c9cc51d00902f5233ad0c84011479244bf7d2"


def git(directory, *args, timeout=15):
    # This public fetch must not inherit checkout credentials, URL rewrites or Git object overrides.
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith(("GIT_", "GH_", "GITHUB_"))}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0",
               GIT_ALLOW_PROTOCOL="https", GIT_NO_REPLACE_OBJECTS="1")
    return subprocess.check_output(["git", "-C", str(directory), "-c", "credential.helper=",
                                    "-c", "http.followRedirects=false", "-c", "fetch.fsckObjects=true", *args],
                                   env=env, timeout=timeout)


def read_snapshot(repo, commit):
    if not OID.fullmatch(commit):
        raise ValueError("Invalid upstream commit")
    paths = {"data/" + name: name for name in CANDIDATES}
    paths["LICENSE"] = "LICENSE"
    entries = git(repo, "ls-tree", "-z", commit, "--", *paths)
    files = {}
    for entry in filter(None, entries.split(b"\0")):
        meta, _, path_bytes = entry.partition(b"\t")
        path = path_bytes.decode("ascii")
        regular = re.fullmatch(rb"100644 blob ([a-f0-9]{40})", meta)
        if path not in paths or not regular:
            raise ValueError(f"Expected a regular upstream file: {path}")
        blob = regular[1].decode("ascii")
        size = int(git(repo, "cat-file", "-s", blob))
        if not 0 < size <= MAX_FILE:
            raise ValueError(f"Invalid size for {path}")
        data = git(repo, "cat-file", "blob", blob)
        digest = sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if len(data) != size or digest != blob:
            raise ValueError(f"Invalid Git blob for {path}")
        if path == "LICENSE" and sha256(data).hexdigest() != LICENSE_SHA256:
            raise ValueError("Upstream LICENSE changed and requires review")
        files[paths[path]] = data.decode("utf-8")
    if set(files) != set(paths.values()):
        raise ValueError("Required upstream files are missing")
    del files["LICENSE"]
    return files


def snapshot(revision=None):
    if revision is not None and not OID.fullmatch(revision):
        raise ValueError("Invalid upstream commit")
    with tempfile.TemporaryDirectory() as directory:
        git(directory, "init", "--bare", "--quiet", "--object-format=sha1", "--template=")
        remote = f"https://github.com/{REPOSITORY}.git"
        branch = "refs/heads/master:refs/heads/upstream"
        git(directory, "fetch", "--quiet", "--depth=1", "--no-tags", "--no-recurse-submodules",
            remote, branch, timeout=90)
        commit = git(directory, "rev-parse", "--verify", "refs/heads/upstream^{commit}").decode("ascii").strip()
        if revision is not None and revision != commit:
            # Only trust commits reachable from the named upstream branch. A raw hash
            # fetch alone can also resolve objects from other refs or a GitHub fork.
            git(directory, "fetch", "--quiet", "--unshallow", "--no-tags", "--no-recurse-submodules",
                remote, branch, timeout=90)
            if git(directory, "cat-file", "-t", revision).strip() != b"commit":
                raise ValueError("Expected an upstream commit object")
            git(directory, "merge-base", "--is-ancestor", revision, "refs/heads/upstream")
            commit = revision
        return commit, read_snapshot(directory, commit)


def selected(files):
    if set(files) != set(CANDIDATES):
        raise ValueError("Incomplete upstream snapshot")
    hosts = set()
    for category, (main_domain, candidates) in CANDIDATES.items():
        # Project data files are not Loon configuration. Ignore includes, regexps, extra tags
        # and comments. Even upstream suffix entries emit one literal hostname only.
        rows = [line.partition("#")[0].split() for line in files[category].splitlines()]
        if [main_domain] not in rows or not any(len(row) == 2 and row[1] == "@ads" for row in rows):
            raise ValueError(f"Unrecognized or incomplete {category} category")
        for row in rows:
            if len(row) == 2 and row[1] == "@ads":
                host = row[0].removeprefix("full:")
                if host in candidates:
                    hosts.add(host)
    if not hosts:
        raise ValueError("Empty candidate intersection, retaining published rules")
    return hosts


def read_block(text):
    lines = text.splitlines(keepends=True)
    labels = [line.rstrip("\r\n") for line in lines]
    if labels.count(START) != 1 or labels.count(END) != 1:
        raise ValueError("Missing or repeated managed block")
    first, last = labels.index(START), labels.index(END)
    sections = [line for line in labels[:first] if line.startswith("[")]
    if first >= last or sections[-1:] != ["[Rule]"]:
        raise ValueError("Managed block must be inside [Rule]")
    interior = labels[first + 1:last]
    hosts = set()
    if interior:
        if len(interior) < 2 or not interior[0].startswith(SOURCE) or not OID.fullmatch(interior[0][len(SOURCE):]):
            raise ValueError("Invalid managed block provenance")
        for line in interior[1:]:
            match = RULE.fullmatch(line)
            if not match or match[1] not in APPROVED or match[1] in hosts:
                raise ValueError("Unexpected published rule in managed block")
            hosts.add(match[1])
    return "".join(lines[:first + 1]), "".join(lines[last:]), hosts


def update(root, commit, files):
    if not OID.fullmatch(commit):
        raise ValueError("Invalid upstream commit")
    hosts = selected(files)
    original = {root / name: (root / name).read_bytes() for name in PLUGINS}
    edits = {}
    before = None
    for path, data in original.items():
        prefix, suffix, current = read_block(data.decode("utf-8"))
        if before is not None and before != current:
            raise ValueError("Published plugins disagree on managed hosts")
        before = current
        manual_hosts = {m[1] for line in (prefix + suffix).splitlines() if (m := RULE.fullmatch(line))}
        if manual_hosts & hosts:
            raise ValueError("Managed hosts overlap manually maintained rules")
        if hosts == current:
            continue
        if (current and len(hosts ^ current) > 3) or (not current and len(hosts) > 6):
            raise ValueError("Unexpected number of changes, preserving published rules")
        newline = "\r\n" if prefix.endswith("\r\n") else "\n"
        block = [SOURCE + commit, *(f"DOMAIN,{host},REJECT" for host in sorted(hosts))]
        edits[path] = (prefix + newline.join(block) + newline + suffix).encode()
    if not edits:
        return False
    # Only publish after both inputs and both prospective files have been validated.
    with tempfile.TemporaryDirectory(dir=root) as temp:
        replaced = []
        for path, data in edits.items():
            (Path(temp) / path.name).write_bytes(data)
        try:
            for path in edits:
                (Path(temp) / path.name).replace(path)
                replaced.append(path)
        except OSError:
            for path in replaced:
                path.write_bytes(original[path])
            raise
    return True


if __name__ == "__main__":
    revision, contents = snapshot()
    if dest := os.environ.get("GITHUB_OUTPUT"):
        with open(dest, "a", encoding="utf-8") as output:
            output.write(f"upstream_sha={revision}\n")
    changed = update(ROOT, revision, contents)
    print(f"Upstream {revision}, {len(selected(contents))} reviewed ad hosts, changed={changed}")
