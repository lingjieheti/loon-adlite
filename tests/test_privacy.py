"""Check the published plugins' declared network permissions without loading Loon or using the network."""

import re
import unittest
from unittest.mock import Mock

import test_suite as shared


INLINE_HOSTS = frozenset({"mp.weixin.qq.com", "app.bilibili.com", "api.bilibili.com"})
REVIEWED_HOSTS = INLINE_HOSTS | frozenset("""
    api.m.jd.com bdsp-x.jd.com guide-acs.m.taobao.com
    api3-core-c.amemv.com api3-normal-c.amemv.com api.amemv.com aweme.snssdk.com
    api.weibo.cn api.coolapk.com mop.meituan.com wmapi.meituan.com
    p0.meituan.net p1.meituan.net img.meituan.net rms.meituan.com
    api.pinduoduo.com api.yangkeduo.com acs.m.goofish.com mapi.dianping.com www.dianping.com
    m5.amap.com amap-aos-info-nogw.amap.com edith.xiaohongshu.com
    rec.xiaohongshu.com api.zhihu.com cards.iqiyi.com t7z.cupid.iqiyi.com
    cdn-xyk-app.bankofbeijing.com.cn static.95508.com app.dewu.com
    p0.pipi.cn app.zhuanzhuan.com api-ios.zhipin.com
    homefront.qunar.com app.variflight.com tiebac.baidu.com
""".split())
PROFILES = {
    "iPad-AdSuite.lpx": {"rule", "rewrite", "mitm"},
    "iPad-InlineAds.lpx": {"rewrite", "mitm"},
    "iPad-AdLite.lpx": {"rule"},
}
METADATA = {"name", "desc", "author", "date", "loon_version", "homepage"}
JQ_STRING = re.compile(r'"(?:\\.|[^"\\])*"')
JQ_IO = re.compile(r"(?<![\w.$])(?:import|include|module|env|input|inputs|debug|stderr)\b"
                   r"|\$(?:ENV|httpClient|task|httpAPI)\b")


def audit(path):
    sections = shared.read_sections(path)
    if set(sections) != PROFILES[path.name]:
        raise ValueError(f"{path.name}: unexpected plugin sections {list(sections)}")
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line.startswith("#!"):
            key, separator, _ = line[2:].partition("=")
            if not separator or key.strip() not in METADATA:
                raise ValueError(f"{path.name}: unreviewed plugin directive {key}")
    for rule in sections.get("rule", []):
        fields = [field.strip() for field in rule.split(",")]
        if len(fields) != 3 or fields[0] != "DOMAIN" or fields[2] != "REJECT" or not shared.HOST.fullmatch(fields[1]):
            raise ValueError(f"{path.name}: expected a local reject for one exact domain: {rule}")
    if "mitm" in sections:
        declaration, = sections["mitm"]
        key, _, value = declaration.partition("=")
        hosts = [host.strip() for host in value.split(",")]
        allowed = INLINE_HOSTS if path.name == "iPad-InlineAds.lpx" else REVIEWED_HOSTS
        if key.strip() != "hostname" or len(hosts) != len(set(hosts)) or not set(hosts) <= allowed:
            raise ValueError(f"{path.name}: unexpected TLS decryption declaration: {declaration}")
    for line in sections.get("rewrite", []):
        # The shared parser accepts only local reject actions and a single response.json.jq action.
        rule = shared.Rewrite.parse(line)
        if rule.phase == "response":
            # A quoted asset URL is data. jq string interpolation can itself contain executable filters.
            code = JQ_STRING.sub(lambda m: m[0] if r"\(" in m[0] else '""', rule.jq)
            if JQ_IO.search(code):
                raise ValueError(f"{path.name}: external input, logging or client reference in jq")


class PluginPrivacy(unittest.TestCase):
    def test_every_published_plugin_has_only_its_reviewed_permissions(self):
        self.assertEqual({p.relative_to(shared.ROOT).as_posix() for p in shared.ROOT.rglob("*.lpx")},
                         set(PROFILES))
        self.assertEqual(len(REVIEWED_HOSTS), 39)
        for name in PROFILES:
            with self.subTest(name=name):
                audit(shared.ROOT / name)

    def test_changes_that_expand_permissions_are_rejected(self):
        for name, before, after in (
            ("iPad-AdLite.lpx", "[Rule]", "[Rule]\nDOMAIN-SUFFIX,example.org,REJECT"),
            ("iPad-AdLite.lpx", "[Rule]", "[Rule]\nDOMAIN,*.example.org,REJECT"),
            ("iPad-AdLite.lpx", "[Rule]", "[Rule]\nDOMAIN,example.org,PROXY"),
            ("iPad-AdLite.lpx", "[Rule]", "[MitM]\nhostname = example.org\n[Rule]"),
            ("iPad-AdSuite.lpx", "[Rule]", "[Remote Rule]\nhttps://example.org/rules\n[Rule]"),
            ("iPad-AdSuite.lpx", "[Rule]", "[Script]\nhttp-request .* script-path=https://example.org/log.js\n[Rule]"),
            ("iPad-AdSuite.lpx", "#!author", "#!icon = https://example.org/pixel.png\n#!author"),
            ("iPad-AdSuite.lpx", "hostname = mp.weixin.qq.com", "hostname = *.weixin.qq.com"),
            ("iPad-AdSuite.lpx", "hostname = mp.weixin.qq.com,", "hostname = api.example.org,"),
            ("iPad-InlineAds.lpx", "hostname =", "hostname = api.m.jd.com,"),
            ("iPad-AdSuite.lpx", "then reject(404)", "then redirect(https://example.org/log)"),
            ("iPad-AdSuite.lpx", "then reject(404)", "then reject(404) | request.header.set(\"X\", \"y\")"),
            ("iPad-InlineAds.lpx", "then response.json.jq(", "then response.body.mock("),
            ("iPad-InlineAds.lpx", "def ok:", 'include "external"; def ok:'),
            ("iPad-InlineAds.lpx", "def ok:", "$httpClient.get | def ok:"),
        ):
            with self.subTest(name=name, change=after):
                path = shared.ROOT / name
                original = path.read_text(encoding="utf-8-sig")
                self.assertIn(before, original)
                changed = Mock()
                changed.name = name
                changed.read_text.return_value = original.replace(before, after, 1)
                with self.assertRaises(ValueError):
                    audit(changed)

    def test_informational_links_and_literal_asset_urls_are_allowed(self):
        path = shared.ROOT / "iPad-InlineAds.lpx"
        fixture = Mock()
        fixture.name = path.name
        fixture.read_text.return_value = '#!homepage = https://example.org/docs\n' + path.read_text(
            encoding="utf-8-sig"
        ).replace("def ok:", 'def asset: . == "https://cdn.example.org/input"; def ok:', 1)
        audit(fixture)


if __name__ == "__main__":
    unittest.main()
