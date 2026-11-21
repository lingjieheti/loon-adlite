"""Compare pinned GitHub files from both source guides with their upstream revisions."""

from collections import defaultdict
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import quote, unquote


ROOT = Path(__file__).resolve().parents[2]
GUIDES = ("SOURCES.md", "COVERAGE.md")
FILE_LINK = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)/blob/([a-f0-9]{40})/([^\s#)?<>]+)")


def cited_files(*guides):
    repos = defaultdict(set)
    for guide in guides:
        for repo, revision, path in FILE_LINK.findall(guide):
            repo = repo.lower()
            if repo != "lingjieheti/loon-adlite":
                repos[repo].add((revision, unquote(path)))
    if not repos:
        raise ValueError("No pinned upstream files found in the source guides")
    return repos


def repository_fields(repo, queries):
    query = ("query($owner:String!,$name:String!){repository(owner:$owner,name:$name){"
             + " ".join(queries) + "}}")
    owner, name = repo.split("/")
    response = subprocess.run(
        ["gh", "api", "graphql", "-f", "query=" + query, "-f", "owner=" + owner, "-f", "name=" + name],
        stdout=subprocess.PIPE, check=True, encoding="utf-8", timeout=45,
    )
    data = json.loads(response.stdout)["data"]["repository"]
    if not data:
        raise ValueError("upstream repository unavailable")
    return data


def file_states(repo, entries):
    branch = repository_fields(repo, ["defaultBranchRef { target { oid } }"])["defaultBranchRef"]
    if not branch or not re.fullmatch(r"[0-9a-f]{40}", branch["target"]["oid"]):
        raise ValueError("default branch revision unavailable")
    head = branch["target"]["oid"]
    # Compare against the SHA used in the report even if the branch moves mid-run.
    queries = []
    for i, (revision, path) in enumerate(entries):
        for prefix, ref in (("old", revision), ("current", head)):
            expr = json.dumps(f"{ref}:{path}")
            queries.append(f"{prefix}{i}:object(expression:{expr}) {{ __typename oid }}")
    return head, repository_fields(repo, queries)


def compare():
    files = cited_files(*((ROOT / name).read_text(encoding="utf-8") for name in GUIDES))
    changed, missing, problems = [], [], []
    same = 0
    for repo, sources in sorted(files.items()):
        entries = sorted(sources)
        try:
            head, state = file_states(repo, entries)
        except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
            problems.append(f"{repo} · {len(entries)} 项无法读取（{type(error).__name__}）")
            continue
        for i, (revision, path) in enumerate(entries):
            before, after = state[f"old{i}"], state[f"current{i}"]
            url = f"https://github.com/{repo}/blob/{revision}/{quote(path)}"
            link = f"[{repo} · {quote(path)}]({url})"
            if not before or before["__typename"] != "Blob":
                problems.append(f"{link} · 固定版本的原文件无法读取，请核对来源")
            elif not after or after["__typename"] != "Blob":
                missing.append(f"{link} · [所查上游版本](https://github.com/{repo}/tree/{head})")
            elif before["oid"] != after["oid"]:
                current = f"https://github.com/{repo}/blob/{head}/{quote(path)}"
                changed.append(f"{link} · [查看新版文件]({current})")
            else:
                same += 1
    total = sum(len(entries) for entries in files.values())
    unreadable = total - same - len(changed) - len(missing)
    summary = ["## 上游文件复核", "", f"两份来源说明共引用 {len(files)} 个仓库、{total} 项固定文件记录。"
               f"内容相同 {same} 项，内容变化 {len(changed)} 项，原路径已无对应文件 {len(missing)} 项，"
               f"无法核实 {unreadable} 项。"]
    if changed:
        summary += ["", "### 内容变化，待专项审查", "",
                    "采纳改动前请核对引用的规则、许可、权限和测试。", ""]
        summary += ["- " + row for row in changed]
    if missing:
        summary += ["", "### 上游路径消失或类型已变，待核对替代来源", ""]
        summary += ["- " + row for row in missing]
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
