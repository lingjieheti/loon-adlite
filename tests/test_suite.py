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
    "https://cdn-xyk-app.bankofbeijing.com.cn/cdn/resource/image/advertise/2026/banner.jpg": "reject_img(200)",
    "https://static.95508.com/mmg/ciop/sysabbr/cmep/images/popupads/brand1.png": "reject_img(200)",
    "https://app.dewu.com/api/v1/app/advertisement": "reject(404)",
    "https://p0.pipi.cn/adAdmin/promo_45.gif": "reject_img(200)",
    "https://app.zhuanzhuan.com/zz/v2/zzlogic/getOpenScreen": "reject_dict(200)",
    "https://api-ios.zhipin.com/api/zpCommon/user/startupAd/": "reject_dict(200)",
    "https://homefront.qunar.com/front/splash/ad": "reject_dict(200)",
    "https://app.variflight.com/v1/advert/": "reject(404)",
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
    "https://www.dianping.com/ajax/brandad?cityId=1": "reject_dict(200)",
    "https://m5.amap.com/ws/shield/dsp/app/startup/init": "reject_dict(200)",
    "https://amap-aos-info-nogw.amap.com/ws/aos/alimama/splash_screen_rt": "reject(404)",
}

XHS = "https://edith.xiaohongshu.com/api/sns/v6/homefeed"
ZHIHU = "https://api.zhihu.com/topstory/recommend"
RESPONSE_URLS = (
    "https://tiebac.baidu.com/tiebaads/commonbatch?adcmd=1",
    "https://app.bilibili.com/x/v2/splash/list",
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
    "https://api.pinduoduo.com/api/alexa/homepage/hub",
    "https://cards.iqiyi.com/views_home/3.0/qy_home",
    "https://cards.iqiyi.com/views_search/3.0/search",
    "https://t7z.cupid.iqiyi.com/mixer",
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
        lite = read_sections(ROOT / "iPad-AdLite.lpx")
        self.assertEqual(set(lite), {"rule"})
        self.assertEqual(lite["rule"], self.sections["rule"])
        self.assertEqual(len(set(lite["rule"])), len(lite["rule"]))
        original_hosts = {
            "googleads.g.doubleclick.net", "pubads.g.doubleclick.net", "securepubads.g.doubleclick.net",
            "pagead2.googlesyndication.com", "mobads.baidu.com", "adscdn.baidu.com",
            "mobads-pre-config.cdn.bcebos.com", "mi.gdt.qq.com", "pgdt.gtimg.cn", "adsmind.apdcdn.tc.qq.com",
            "ad.tencentmusic.com", "tmead.y.qq.com", "ad.zijieapi.com", "pangolin.snssdk.com",
            "pangolin-hl.snssdk.com", "pangolin-lf.snssdk.com", "pangolin-lq.snssdk.com",
            "ali-ad.a.yximgs.com", "tx-ad.a.yximgs.com", "hw-ot-ad.a.yximgs.com",
            "adstrategy.biz.weibo.com", "api-ad-adapter.wps.com",
        }
        self.assertTrue({f"DOMAIN,{host},REJECT" for host in original_hosts}.issubset(lite["rule"]))
        inline = read_sections(ROOT / "iPad-InlineAds.lpx")["rewrite"]
        self.assertEqual(len(inline), 4)
        self.assertTrue(set(inline).issubset(self.sections["rewrite"]))

    def test_web_ad_hosts_and_normal_web_traffic(self):
        ad_hosts = (
            "a.adtng.com", "ads.trafficjunky.net", "hbopenbid.pubmatic.com",
            "grid-bidder.criteo.com", "tlx.3lift.com", "dup.baidustatic.com",
        )
        rules = self.sections["rule"]
        for host in ad_hosts:
            self.assertIn(f"DOMAIN,{host},REJECT", rules)

        untouched = {
            "pornhub.com", "www.pornhub.com", "ei.phncdn.com", "ev.phncdn.com",
            "www.pubmatic.com", "www.criteo.com", "www.trafficjunky.com", "cdn.jsdelivr.net",
            "www.triplelift.com", "www.baidu.com", "passport.baidu.com", "s.bdstatic.com",
            "cpro.baidustatic.com", "ecomcbjs.jomodns.com",
        }
        for host in ad_hosts:
            untouched.update((host.partition(".")[2], f"sub.{host}", f"{host}.example.org"))

        for host in untouched:
            with self.subTest(host=host):
                self.assertNotIn(f"DOMAIN,{host},REJECT", rules)
                self.assertEqual(self.matches(f"https://{host}/video/test.mp4"), [])

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

    def test_taobao_splash_material_url(self):
        api = "mtop.taobao.wireless.home.splash.awesome.get"
        url = f"https://guide-acs.m.taobao.com/gw/{api}/1.0/"
        valid = (
            "https://img.alicdn.com/imgextra/i1/asset.jpg_800x800.jpg",
            "//gw.alicdn.com/tfs/asset%20name.jpg?quality=80&from=app#preview",
            "HTTP://cdn.example:8080/video.mp4", "https://cdn.example.?asset=1",
            "http://192.0.2.4/asset", "https://[2001:db8::1]:443/asset",
            "//[::ffff:192.0.2.4]/asset",
        )
        unknown = (
            None, 12, [], "", " ", "#", "about:blank", "data:image/png,placeholder",
            "https://", "//", "///img", "https:///asset", "//?asset=x", "https://#fragment",
            "/∕/cdn.example/asset", "https:// cdn.example/asset", "https://cdn.example/a b",
            "https://cdn.example/a\n", "https://cdn.example\\@other.example/asset",
            "//./asset", "//../asset", "//user@/asset", "//user@cdn.example/asset", "//cdn..example/asset",
            "//-cdn.example/asset", "//cdn-.example/asset", "//:443/asset",
            "//cdn.example:/asset", "//cdn.example:port/asset", "//cdn.example:65536/asset",
            "//999.1.1.1/asset", "//[broken/asset", "//[1:::2]/asset", "//[1:2:3]/asset",
        )
        keep = [{"imgUrl": value, "link": "https://example.com/coupon"} for value in unknown]
        keep.append({"link": "https://gw.alicdn.com/landing"})
        creatives = [{"videoUrl": value} for value in valid]
        creatives.append({"imgUrl": valid[0], "videoUrl": "placeholder"})

        def envelope(items):
            section = {"bizData": {"taobao-splash": {"data": items}}}
            return {"api": api, "v": "1.0", "ret": ["SUCCESS::调用成功"],
                    "data": {"containers": {"splash_home_base": {"base": {"sections": [section]}}}}}

        self.check_body(url, envelope([*keep[:4], *creatives, *keep[4:]]), envelope(keep))

    def test_exact_request_actions(self):
        for url, action in REQUEST_CASES.items():
            for suffix in ("", "?test=1"):
                with self.subTest(url=url + suffix):
                    rule, = self.matches(url + suffix)
                    self.assertEqual((rule.phase, rule.action), ("request", action))

    def test_mtop_nested_business_error_passes_through(self):
        splash = {"bizData": {"taobao-splash": {"data": [{"imgUrl": "https://gw.alicdn.com/ad.jpg"}]}}}
        endpoints = {
            "mtop.taobao.wireless.home.splash.awesome.get":
                {"containers": {"splash_home_base": {"base": {"sections": [splash]}}}},
            "mtop.cainiao.adx.flyad.getad": {"creative": {"id": BIG_ID}},
        }
        for api, data in endpoints.items():
            url = f"https://guide-acs.m.taobao.com/gw/{api}/1.0/"
            for flags in ({"success": False}, {"errmsg": "business error", "status": "1"}):
                payload = {"api": api, "v": "1.0", "ret": ["SUCCESS::调用成功"], "data": {**data, **flags}}
                with self.subTest(api=api, flags=flags):
                    self.check_body(url, payload, payload)

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
            "https://passport.baidu.com/v2/?login",
            "https://cpro.baidustatic.com/cpro/ui/c.js",
            "https://cpro.baidustatic.com/cpro/ui/cm.js",
        ]
        for url in REQUEST_CASES:
            host = urlsplit(url).hostname
            urls.extend([url.replace(host, host + ".example.org"), url.replace("https://", "http://")])
        blocked = {line.split(",")[1] for line in self.sections["rule"]}
        for url in urls:
            with self.subTest(url=url):
                self.assertNotIn(urlsplit(url).hostname, blocked)
                self.assertEqual(self.matches(url), [])

    def test_jd_ambiguous_operation_names_preserve_business_requests(self):
        prefix = "https://api.m.jd.com/client.action?"
        for operation in ("start", "welcomeHome"):
            regular = f"functionId={operation}"
            for second in ("function%49d=submitOrder", "%66unctionId=getShopCoupon", "functionId"):
                for query in (regular + "&" + second, second + "&" + regular):
                    with self.subTest(query=query):
                        self.assertEqual(self.matches(prefix + query), [])
            for query in (regular, regular + "&next=functionId%3DgetShopCoupon",
                          "body=%7B%22path%22%3A%22foo%22%7D&" + regular):
                self.assertEqual(len(self.matches(prefix + query)), 1, query)

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
            for envelope in ({"code": 403}, {"code": 0, "success": False}, {"code": 0, "success": 0},
                             {"code": 0, "success": None}, {"code": 0, "success": "true"}, {"code": "0"},
                             {"code": 0, "success": True, "error": {"code": 403}}, {}):
                payload = {**envelope, "data": mixed}
                self.check_body(url, payload, payload)
            self.check_body(url, {"code": 0, "data": {}}, {"code": 0, "data": {}})

    def test_zhihu_explicit_feed_advert(self):
        keep = [
            {"type": "ComponentCard", "id": BIG_ID}, {"type": "feed", "target": {"type": "article"}},
            {"type": "future", "ad_info": {}}, {"children": [{"type": "feed_advert"}]}, None,
        ]
        mixed = [*keep, {"type": "feed_advert"}]
        for envelope in ({}, {"success": True}, {"code": 0}, {"code": 0, "success": True}):
            self.check_body(ZHIHU, {**envelope, "data": mixed, "paging": {"next": BIG_ID}},
                            {**envelope, "data": keep, "paging": {"next": BIG_ID}})
        for envelope in ({"code": 403, "success": False}, {"code": 403}, {"success": False},
                         {"code": None}, {"code": "0"}, {"success": 0}, {"success": None}, {"success": "true"}):
            payload = {**envelope, "data": mixed}
            self.check_body(ZHIHU, payload, payload)
        for payload in ({"data": mixed, "error": {"code": 401}}, {"data": {"items": mixed}}, []):
            self.check_body(ZHIHU, payload, payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
