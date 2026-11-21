"""Compare Git blob IDs for pinned GitHub file links in the source guide."""

from collections import defaultdict
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import quote, unquote


ROOT = Path(__file__).resolve().parents[2]
FILE_LINK = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)/blob/([a-f0-9]{40})/([^\s#)?<>]+)")


def cited_files(guide):
    repos = defaultdict(set)
    for repo, revision, path in FILE_LINK.findall(guide):
        if repo.lower() != "lingjieheti/loon-adlite":
            repos[repo].add((revision, unquote(path)))
    if not repos:
        raise ValueError("SOURCES.md has no pinned upstream files")
    return repos


def file_states(repo, entries):
    # GitHub resolves the expressions server-side. Only file type and object IDs are returned.
    queries = ["defaultBranchRef { target { oid } }"]
    for i, (rev, path) in enumerate(entries):
        for prefix, ref in (("old", rev), ("current", "HEAD")):
            expr = json.dumps(f"{ref}:{path}")
            queries.append(f"{prefix}{i}:object(expression:{expr}) {{ __typename oid }}")
    query = ("query($owner:String!,$name:String!){repository(owner:$owner,name:$name){"
             + " ".join(queries) + "}}")
    owner, name = repo.split("/")
    response = subprocess.run(
        ["gh", "api", "graphql", "-f", "query=" + query, "-f", "owner=" + owner, "-f", "name=" + name],
        stdout=subprocess.PIPE, check=True, encoding="utf-8", timeout=45,
    )
    data = json.loads(response.stdout)["data"]["repository"]
    if not data or not data["defaultBranchRef"]:
        raise ValueError("default branch unavailable")
    return data


def compare():
    files = cited_files((ROOT / "SOURCES.md").read_text(encoding="utf-8"))
    rows, problems = [], []
    same = changed = 0
    for repo, sources in sorted(files.items()):
        entries = sorted(sources)
        try:
            state = file_states(repo, entries)
        except (ValueError, KeyError, subprocess.SubprocessError) as error:
            problems.append(f"{repo} · 无法读取 GitHub 记录（{type(error).__name__}）")
            continue
        head = state["defaultBranchRef"]["target"]["oid"]
        for i, (revision, path) in enumerate(entries):
            before, after = state[f"old{i}"], state[f"current{i}"]
            url = f"https://github.com/{repo}/blob/{revision}/{quote(path)}"
            link = f"[{repo} · {quote(path)}]({url})"
            if not before or before["__typename"] != "Blob":
                problems.append(f"{link} · 请核对引用版本或路径")
            elif not after or after["__typename"] != "Blob":
                changed += 1
                rows.append(f"{link} · 当前默认分支没有同路径的普通文件")
            elif before["oid"] != after["oid"]:
                changed += 1
                current = f"https://github.com/{repo}/blob/{head}/{quote(path)}"
                rows.append(f"{link} · [查看默认分支文件]({current})")
            else:
                same += 1
    summary = ["## 上游文件复核", "", f"内容相同 {same} 项，有改动 {changed} 项。"]
    if rows:
        summary += ["", "以下为文件级变化。采纳前请核对本插件实际使用的规则、权限和测试。", ""]
        summary += ["- " + row for row in rows]
    if problems:
        summary += ["", "以下来源本次未完成比对。", ""] + ["- " + item for item in problems]
    report = "\n".join(summary) + "\n"
    print(report)
    if location := os.getenv("GITHUB_STEP_SUMMARY"):
        with open(location, "a", encoding="utf-8") as output:
            output.write(report)
    return bool(problems)


if __name__ == "__main__":
    raise SystemExit(compare())
