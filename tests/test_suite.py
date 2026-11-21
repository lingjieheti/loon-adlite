"""Offline checks of the URL patterns and jq programs in iPad-AdSuite.lpx.

Run with Python 3.8+ and jq on PATH, or set JQ to the jq executable.
No requests, Apple devices or TLS certificates are used.
"""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import unittest
from urllib.parse import urlsplit


TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent
BIG_ID = 123456789012345678901234567891
URL_PATTERN = r"\$\{url\} ~= /((?:\\.|[^/\\])*)/(i?)"
MIME_PATTERN = r"\$\{response\.header\['Content-Type'\]\} ~= /((?:\\.|[^/\\])*)/(i?)"
HOST = re.compile(r"(?:[a-z0-9]+(?:-+[a-z0-9]+)*\.)+[a-z]{2,}")

REQUEST_CASES = {
    "https://api3-core-c.amemv.com/api/ad/v16/splash/preload": "reject(404)",
    "https://wmapi.meituan.com/api/v7/openscreen": "reject_dict(200)",
    "https://wmapi.meituan.com/api/v7/startpicture": "reject_dict(200)",
    "https://p0.meituan.net/adunion/example.jpg": "reject_img(200)",
    "https://p1.meituan.net/adunion/example.jpg": "reject_img(200)",
    "https://img.meituan.net/bizad/bizad_brandCpt_123.jpg": "reject_img(200)",
    "https://bdsp-x.jd.com/adx/auction": "reject(404)",
    "https://api.pinduoduo.com/api/cappuccino/splash": "reject(404)",
    "https://api.yangkeduo.com/api/cappuccino/splash": "reject(404)",
    "https://acs.m.goofish.com/gw/mtop.taobao.idlecommerce.splash.ads/1.0/": "reject_dict(200)",
    "https://acs.m.goofish.com/gw/mtop.taobao.idlecommerce.splash.async.ads/1.0/": "reject_dict(200)",
    "https://mapi.dianping.com/mapi/operating/loadsplashconfig": "reject(404)",
    "https://m5.amap.com/ws/shield/dsp/app/startup/init": "reject_dict(200)",
    "https://amap-aos-info-nogw.amap.com/ws/aos/alimama/splash_screen_rt": "reject(404)",
}

XHS = "https://edith.xiaohongshu.com/api/sns/v6/homefeed"
ZHIHU = "https://api.zhihu.com/topstory/recommend"
RESPONSE_URLS = (
    "https://api3-core-c.amemv.com/aweme/v1/feed",
    "https://api3-normal-c.amemv.com/aweme/v2/feed",
    "https://api.amemv.com/aweme/v1/feed",
    "https://aweme.snssdk.com/aweme/v1/feed",
    "https://api.weibo.cn/2/statuses/friends/timeline",
    "https://api.weibo.cn/2/statuses/container_timeline",
    "https://api.weibo.cn/2/ad/weibointl",
    "https://api.coolapk.com/v6/main/dataList",
    "https://mop.meituan.com/api/entryModule/startupPicture",
    "https://wmapi.meituan.com/api/v7/loadInfo",
    "https://rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement",
    XHS, XHS.replace("edith", "rec"), ZHIHU,
    "https://mp.weixin.qq.com/mp/getappmsgad", "https://mp.weixin.qq.com/mp/getappmsgext",
    "https://app.bilibili.com/x/v2/feed/index",
    "https://api.bilibili.com/x/web-interface/wbi/index/top/feed/rcmd",
    "https://api.m.jd.com/client.action?functionId=start",
    "https://api.m.jd.com/client.action?functionId=welcomeHome",
    "https://guide-acs.m.taobao.com/gw/mtop.taobao.wireless.home.splash.awesome.get/1.0/",
    "https://guide-acs.m.taobao.com/gw/mtop.cainiao.adx.flyad.getad/1.0/",
)


def read_sections(path):
    sections = {}
    current = None
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current = line[1:-1].lower()
            if current in sections:
                raise ValueError(f"Repeated section [{current}] in {path.name}")
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
        else:
            raise ValueError(f"Line outside section in {path.name}: {line}")
    return sections


def compile_regex(match):
    return re.compile(match[1], re.IGNORECASE if match[2] else 0)


@dataclass
class Rewrite:
    phase: str
    url: re.Pattern
    action: str
    jq: str = ""
    mime: re.Pattern = None

    @classmethod
    def parse(cls, line):
        condition, action = line.split(" then ", 1)
        phase, condition = condition.split(" if ", 1)
        pieces = condition.split(" && ")
        match = re.fullmatch(URL_PATTERN, pieces[0])
        if not match:
            raise ValueError(f"Invalid URL expression: {pieces[0]}")
        rule = cls(phase, compile_regex(match), action)
        if phase == "request":
            if len(pieces) != 1 or action not in {"reject(404)", "reject_dict(200)", "reject_img(200)"}:
                raise ValueError(f"Unsupported request rule: {line}")
        elif phase == "response":
            if len(pieces) not in (2, 3) or pieces[1] != "${response.status} == 200":
                raise ValueError(f"Missing or unsupported status guard: {line}")
            if len(pieces) == 3:
                header = re.fullmatch(MIME_PATTERN, pieces[2])
                if not header:
                    raise ValueError(f"Unsupported header guard: {pieces[2]}")
                rule.mime = compile_regex(header)
            program = re.fullmatch(r"response\.json\.jq\(`([^`]+)`\)", action)
            if not program:
                raise ValueError(f"Unrecognized jq action: {action}")
            rule.jq = program[1]
        else:
            raise ValueError(f"Unknown phase: {phase}")
        return rule

    def matches(self, url, status=200, mime="application/json"):
        return bool(self.url.search(url)) and (
            self.phase == "request" or (status == 200 and (self.mime is None or bool(self.mime.search(mime))))
        )


class AdSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sections = read_sections(ROOT / "iPad-AdSuite.lpx")
        cls.rules = [Rewrite.parse(line) for line in cls.sections["rewrite"]]
        cls.shopping = json.loads((TESTS / "shopping_cases.json").read_text("utf-8"))
        cls.jq = os.environ.get("JQ") or shutil.which("jq")
        if not cls.jq:
            raise RuntimeError("Set JQ to a jq executable or install jq on PATH")

    def matches(self, url, **options):
        return [r for r in self.rules if r.matches(url, **options)]

    def check_body(self, url, source, expected):
        matches = self.matches(url)
        self.assertLessEqual(len(matches), 1, url)
        result = source
        if matches:
            rule = matches[0]
            self.assertEqual(rule.phase, "response", url)
            for _ in range(2):
                ran = subprocess.run(
                    [self.jq, "-c", rule.jq], input=json.dumps(result),
                    encoding="utf-8", capture_output=True, timeout=10,
                )
                self.assertEqual(ran.returncode, 0, ran.stderr)
                result = json.loads(ran.stdout)
                self.assertEqual(json.dumps(result, sort_keys=True), json.dumps(expected, sort_keys=True))
        else:
            self.assertEqual(json.dumps(source, sort_keys=True), json.dumps(expected, sort_keys=True))

    def test_original_domains_and_inline_rules_are_preserved(self):
        domains = read_sections(ROOT / "iPad-AdLite.lpx")["rule"]
        inline = read_sections(ROOT / "iPad-InlineAds.lpx")["rewrite"]
        self.assertEqual(len(domains), 22)
        self.assertEqual(len(inline), 3)
        self.assertTrue(set(domains).issubset(self.sections["rule"]))
        self.assertTrue(set(inline).issubset(self.sections["rewrite"]))

    def test_hosts_and_all_rule_entry_points(self):
        self.assertEqual(set(self.sections), {"rule", "rewrite", "mitm"})
        rejected = []
        for line in self.sections["rule"]:
            kind, host, action = line.split(",")
            self.assertEqual((kind, action), ("DOMAIN", "REJECT"))
            self.assertIsNotNone(HOST.fullmatch(host))
            rejected.append(host)
        self.assertEqual(len(set(rejected)), len(rejected))
        hostname_line, = self.sections["mitm"]
        key, value = hostname_line.split("=", 1)
        self.assertEqual(key.strip(), "hostname")
        intercepted = [x.strip() for x in value.split(",")]
        self.assertEqual(len(set(intercepted)), len(intercepted))
        self.assertTrue(all(HOST.fullmatch(h) for h in intercepted))
        self.assertFalse(set(intercepted) & set(rejected))
        urls = [*REQUEST_CASES, *RESPONSE_URLS]
        self.assertEqual({urlsplit(u).hostname for u in urls}, set(intercepted))
        for url in urls:
            self.assertEqual(len(self.matches(url)), 1, url)
        for rule in self.rules:
            self.assertTrue(any(rule.matches(u) for u in urls), rule.url.pattern)
            if rule.phase == "response":
                witness = next(u for u in urls if rule.matches(u))
                self.check_body(witness, None, None)
                self.assertFalse(rule.matches(witness, status=204))
                self.assertFalse(rule.matches(witness, status=403))
                if rule.mime:
                    self.assertTrue(rule.matches(witness, mime="Application/JSON; charset=UTF-8"))
                    for mime in ("text/html", "application/jsonp", "application/grpc", "image/jpeg"):
                        self.assertFalse(rule.matches(witness, mime=mime))

    def test_shopping_responses(self):
        self.assertEqual(len(self.shopping), 45)
        for idx, case in enumerate(self.shopping):
            with self.subTest(case=idx, url=case["url"]):
                self.check_body(case["url"], case["input"], case["expected"])

    def test_exact_request_actions(self):
        for url, action in REQUEST_CASES.items():
            for suffix in ("", "?test=1"):
                with self.subTest(url=url + suffix):
                    rule, = self.matches(url + suffix)
                    self.assertEqual((rule.phase, rule.action), ("request", action))

    def test_checkout_coupons_playback_navigation_and_similar_urls(self):
        urls = [
            "https://api.m.jd.com/client.action?functionId=submitOrder",
            "https://api.m.jd.com/client.action?functionId=getShopCoupon",
            "https://guide-acs.m.taobao.com/gw/mtop.trade.order.create/1.0/",
            "https://guide-acs.m.taobao.com/gw/mtop.taobao.coupon.receive/1.0/",
            "https://acs.m.goofish.com/gw/mtop.taobao.idle.trade.create/1.0/",
            "https://api.yangkeduo.com/api/cappuccino/splash-extra",
            "https://api.pinduoduo.com/order/prepay", "https://mapi.dianping.com/mapi/pay/order",
            "https://img.alicdn.com/imgextra/i1/example.jpg",
            "https://m.360buyimg.com/mobilecms/s1125x2436_jfs/example.jpg",
            "https://music.163.com/weapi/song/enhance/player/url/v1",
            "https://isure.stream.qqmusic.qq.com/music.m4a",
            "https://m5.amap.com/ws/mapapi/navigation/route",
            "https://m5.amap.com/ws/shield/dsp/app/startup/initMore",
            "https://amap-aos-info-nogw.amap.com/ws/aos/alimama/splash_screen_rt/other",
            "https://api.zhihu.com/questions/123/answers",
            "https://edith.xiaohongshu.com/api/sns/v6/note/feed",
            "https://api.bilibili.com/x/player/wbi/playurl",
        ]
        for url in REQUEST_CASES:
            host = urlsplit(url).hostname
            urls.extend([url.replace(host, host + ".example.org"), url.replace("https://", "http://")])
        blocked = {line.split(",")[1] for line in self.sections["rule"]}
        for url in urls:
            with self.subTest(url=url):
                self.assertNotIn(urlsplit(url).hostname, blocked)
                self.assertEqual(self.matches(url), [])

    def test_xiaohongshu_homefeed(self):
        keep = [
            {"model_type": "live_v2", "id": BIG_ID}, {"has_related_goods": True},
            {"ads_info": {}}, {"ads_info": None}, {"ads_info": "unknown"}, None, "opaque",
        ]
        mixed = [*keep, {"ads_info": {"id": "fixture"}}]
        for host in ("edith", "rec"):
            url = XHS.replace("edith", host)
            for envelope in ({"code": 0}, {"code": 0, "success": True}, {"success": True}):
                self.check_body(url, {**envelope, "data": mixed}, {**envelope, "data": keep})
            for envelope in ({"code": 403}, {"code": 0, "success": False}, {"code": "0"}, {}):
                payload = {**envelope, "data": mixed}
                self.check_body(url, payload, payload)
            self.check_body(url, {"code": 0, "data": {}}, {"code": 0, "data": {}})

    def test_zhihu_explicit_feed_advert(self):
        keep = [
            {"type": "ComponentCard", "id": BIG_ID}, {"type": "feed", "target": {"type": "article"}},
            {"type": "future", "ad_info": {}}, {"children": [{"type": "feed_advert"}]}, None,
        ]
        mixed = [*keep, {"type": "feed_advert"}]
        self.check_body(ZHIHU, {"data": mixed, "paging": {"next": BIG_ID}},
                        {"data": keep, "paging": {"next": BIG_ID}})
        for payload in ({"data": mixed, "error": {"code": 401}}, {"data": {"items": mixed}}, []):
            self.check_body(ZHIHU, payload, payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
