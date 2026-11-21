"""Sync a small reviewed set of exact ad hosts from v2ray/domain-list-community (MIT)."""
import base64
from hashlib import sha1
import json
from pathlib import Path
import re
import tempfile
from urllib.request import Request, urlopen


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


def github(path):
    url = f"https://api.github.com/repos/{REPOSITORY}/{path}"
    request = Request(url, headers={"User-Agent": "loon-adlite-rule-sync", "Accept": "application/vnd.github+json"})
    with urlopen(request, timeout=20) as response:
        if response.geturl() != url:
            raise ValueError("Unexpected upstream redirect")
        data = response.read(MAX_FILE + 1)
    if len(data) > MAX_FILE:
        raise ValueError("Upstream response too large")
    return json.loads(data)


def snapshot():
    reference = github("git/ref/heads/master")
    commit = reference["object"]["sha"]
    if reference["ref"] != "refs/heads/master" or reference["object"]["type"] != "commit" or not OID.fullmatch(commit):
        raise ValueError("Invalid upstream ref")
    files = {}
    for category in CANDIDATES:
        path = "data/" + category
        item = github(f"contents/{path}?ref={commit}")
        if item["path"] != path or item["type"] != "file" or item["encoding"] != "base64":
            raise ValueError(f"Unexpected source record for {path}")
        data = base64.b64decode(item["content"].replace("\n", ""), validate=True)
        digest = sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if not data or len(data) != item["size"] or len(data) > MAX_FILE or digest != item["sha"]:
            raise ValueError(f"Invalid Git blob for {path}")
        files[category] = data.decode("utf-8")
    return commit, files


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
    changed = update(ROOT, revision, contents)
    print(f"Upstream {revision}, {len(selected(contents))} reviewed ad hosts, changed={changed}")
