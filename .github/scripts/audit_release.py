"""Audit the exact release diff and write a reviewable GitHub Actions summary."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

from audit_host_update import audit_commits, audit_pairs, managed_block, verify_source
from sync_ad_hosts import OID, PLUGINS, ROOT, START, read_block

sys.path.insert(0, str(ROOT / "tests"))
from test_privacy import PROFILES, audit as audit_plugin
from test_suite import read_sections


RECORD = "SECURITY-AUDIT.md"
FIELD = re.compile(r"^\s*-\s*(范围|风险|验证)\s*[:：]\s*(.+?)\s*$")


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def blob(revision, name):
    entry = git("ls-tree", revision, "--", name)
    if not entry:
        return None
    if entry.split(maxsplit=2)[:2] != [b"100644", b"blob"]:
        raise ValueError(f"{name}: expected a regular non-executable file")
    return git("show", revision + ":" + name)


def has_new_record(previous, current):
    # All three fields must form a single new list, with newly written text for each field.
    older = {m[2].strip() for line in previous.splitlines() if (m := FIELD.fullmatch(line))}
    record = {}
    for line in current.splitlines():
        item = FIELD.fullmatch(line)
        if not item or item[1] in record:
            record.clear()
        if item:
            value = item[2].strip()
            if value in older or len(re.sub(r"\s+", "", value)) < 6 or value in record.values():
                record.clear()
                continue
            record[item[1]] = value
            if len(record) == 3:
                return True
    return False


def sensitive(path):
    # Unrecognized file types require review too. Passive docs may ship by themselves.
    return not (path.endswith(".md") or path.startswith("licenses/") and path.endswith(".txt"))


def metrics(path):
    sections = read_sections(path)
    hosts = {line.split(",")[1] for line in sections["rule"]}
    text = path.read_text(encoding="utf-8-sig")
    managed = read_block(text)[2] if START in text else set()
    tls = {host.strip() for line in sections.get("mitm", []) for host in line.partition("=")[2].split(",")}
    return hosts, managed, tls, set(sections.get("rewrite", []))


def delta(old, new):
    return {"新增": sorted(new - old), "移除": sorted(old - new)}


def run(base, head, managed, report, upstream=None):
    if not OID.fullmatch(base) or not (head == "HEAD" or OID.fullmatch(head)):
        raise ValueError("Expected a full base SHA and full head SHA or HEAD")
    candidate = git("rev-parse", "--verify", "HEAD^{commit}").decode().strip()
    if head not in ("HEAD", candidate) or git("rev-parse", "--verify", base + "^{commit}").decode().strip() != base:
        raise ValueError("The checked-out commit or supplied base is not the requested revision")
    if git("diff", "--name-only", candidate, "--"):
        raise ValueError("Tracked files differ from the revision being audited")
    paths = git("diff", "--no-renames", "--name-only", "-z", base, candidate).decode().split("\0")
    paths = sorted(filter(None, paths))
    report.update({"基线": base, "受测提交": candidate, "变更文件": paths,
                   "运行时脚本变更": [p for p in paths if p.endswith((".js", ".mjs", ".ts"))],
                   "自动化或来源变更": [p for p in paths if p.startswith(".github/") or p == "SOURCES.md"]})

    for name in PROFILES:
        audit_plugin(ROOT / name)
    suite = ROOT / "iPad-AdSuite.lpx"
    hosts, generated, tls, rewrites = metrics(suite)
    lite_hosts, lite_generated, _, _ = metrics(ROOT / "iPad-AdLite.lpx")
    if (hosts, generated) != (lite_hosts, lite_generated) or any(START not in (ROOT / n).read_text(encoding="utf-8") for n in PLUGINS):
        raise ValueError("Review both subscription variants: their manual or managed hosts do not agree")
    with TemporaryDirectory() as directory:
        old = Path(directory) / suite.name
        old_bytes = blob(base, suite.name)
        if old_bytes is None:
            old_hosts, old_tls, old_rewrites = set(), set(), set()
        else:
            old.write_bytes(old_bytes)
            old_hosts, _, old_tls, old_rewrites = metrics(old)
    report.update({"手工精确域名数": len(hosts - generated), "自动精确域名数": len(generated),
                   "全部精确域名数": len(hosts), "精确域名变更": delta(old_hosts, hosts),
                   "HTTPS 主机数": len(tls), "HTTPS 主机变更": delta(old_tls, tls), "复写条数": len(rewrites),
                   "复写新增行数": len(rewrites - old_rewrites), "复写移除行数": len(old_rewrites - rewrites)})

    if managed:
        report.update(audit_commits(base, candidate, upstream))
        report["类别"] = "自动发布，已校验两个受管区及父提交"
        return

    # Compare Git blob bytes across both revisions, independent of checkout EOL settings.
    after = {name: blob(candidate, name) for name in PLUGINS}
    blocks = {name: managed_block(data) for name, data in after.items()}
    if len(set(blocks.values())) != 1:
        raise ValueError("Subscriptions disagree on managed contents or upstream revision")
    if upstream is not None:
        if base != candidate:
            raise ValueError("A no-change upstream check must use the current release as its base")
        report.update(verify_source(after, upstream, unchanged=True))
        report["类别"] = "上游轮询，已独立核对本次来源与已发布名单，无需发版"
        return

    before = {name: blob(base, name) for name in PLUGINS if name in paths}
    for name, previous in before.items():
        old = managed_block(previous) if previous and START.encode() in previous else b""
        if old != blocks[name]:
            # A manual audit entry cannot override a false source declaration, even
            # when the PR also updates scripts, docs or manually maintained rules.
            report.update(verify_source(after))
            break
    if set(paths) == set(PLUGINS):
        # A PR merge may have two parents. Its two validated blobs can still be a pure managed diff.
        if all(v is not None for v in (*before.values(), *after.values())):
            try:
                audit_pairs(before, after)
            except ValueError:
                pass
            else:
                report["类别"] = "仅受管域名区变更，已逐字节核对其余内容"
                return

    protected = [p for p in paths if sensitive(p)]
    if not protected:
        report["类别"] = "文档或无内容变更"
        return
    report["类别"] = "需专项安全审计记录的变更"
    report["需审查的文件"] = protected
    if RECORD not in paths:
        raise ValueError("Sensitive changes require a new scope, risk and verification entry in SECURITY-AUDIT.md")
    before = (blob(base, RECORD) or b"").decode("utf-8")
    after = (blob(candidate, RECORD) or b"").decode("utf-8")
    if not has_new_record(before, after):
        raise ValueError("Add a new review with three adjacent bullet lines: 范围、风险、验证")
    report["专项审计记录"] = RECORD


def publish_summary(report):
    # Repository-controlled filenames must remain data inside the Markdown code block.
    payload = json.dumps(report, ensure_ascii=False, indent=2).replace("`", "\\u0060")
    print(payload)
    if dest := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(dest, "a", encoding="utf-8") as stream:
            stream.write("\n### 发布安全审计\n\n```json\n" + payload + "\n```\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--managed", action="store_true")
    parser.add_argument("--upstream", help="Independently verify this scheduled upstream snapshot")
    args = parser.parse_args()
    report = {"结果": "失败"}
    try:
        run(args.base, args.head, args.managed, report, args.upstream)
        report["结果"] = "通过"
    except Exception as exc:
        # An unexpected parser or Git failure must also leave a failed audit in the run summary.
        report["错误"] = type(exc).__name__ + ": " + str(exc)
    publish_summary(report)
    return int(report["结果"] != "通过")


if __name__ == "__main__":
    raise SystemExit(main())
