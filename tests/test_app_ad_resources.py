"""Check that exact ad hosts and bank artwork rules spare nearby services."""
import unittest

import test_suite as shared


class AdResources(unittest.TestCase):
    def test_domain_rules_leave_devices_quotes_and_messages_available(self):
        ad_hosts = {"sdkconfig.ad.xiaomi.com", "adm.10jqka.com.cn", "ad.line-scdn.net"}
        keep = {"api.io.mi.com", "account.xiaomi.com", "10jqka.com.cn", "stockpage.10jqka.com.cn",
                "line-scdn.net", "profile.line-scdn.net", "obs.line-scdn.net"}
        for name in ("iPad-AdLite.lpx", "iPad-AdSuite.lpx"):
            sections = shared.read_sections(shared.ROOT / name)
            blocked = {line.split(",")[1] for line in sections["rule"]}
            self.assertTrue(ad_hosts <= blocked)
            self.assertTrue(blocked.isdisjoint(keep | {"www." + host for host in ad_hosts}))

    def test_dedicated_creative_and_sdk_hosts_leave_business_traffic_available(self):
        adverts = {"ad.maoyan.com", "ads-img-al.xhscdn.com", "sdk.1rtb.net", "zlsdk.1rtb.net", "opehs.tanx.com"}
        business = {
            "www.maoyan.com", "api.maoyan.com", "wx.maoyan.com", "p0.pipi.cn",
            "edith.xiaohongshu.com", "sns-webpic-qc.xhscdn.com", "ci.xiaohongshu.com",
            "www.1rtb.net", "1rtb.net", "1rtb.com", "ssp-svr.1rtb.com", "tanx.com",
            "api.m.jd.com", "janapi.jd.com", "m.360buyimg.com", "guide-acs.m.taobao.com",
            "acs.m.taobao.com", "msgacs.m.taobao.com", "acs.m.goofish.com", "api.yangkeduo.com",
            "p0.meituan.net", "img.meituan.net", "m5.amap.com", "tiebac.baidu.com",
        }
        for name in ("iPad-AdLite.lpx", "iPad-AdSuite.lpx"):
            sections = shared.read_sections(shared.ROOT / name)
            blocked = {line.split(",")[1] for line in sections["rule"]}
            mitm = {host.strip() for line in sections.get("mitm", [])
                    for host in line.partition("=")[2].split(",")}
            with self.subTest(plugin=name):
                self.assertTrue(adverts <= blocked)
                self.assertTrue(blocked.isdisjoint(business | {host + ".example.org" for host in adverts}))
                self.assertTrue(mitm.isdisjoint(adverts))

    def test_bank_images_only_and_no_sensitive_gateways(self):
        suite = shared.read_sections(shared.ROOT / "iPad-AdSuite.lpx")
        rules = [shared.Rewrite.parse(line) for line in suite["rewrite"]]
        roots = (
            ("https://cdn-xyk-app.bankofbeijing.com.cn/cdn/resource/image/", "advertise"),
        )
        for prefix, directory in roots:
            for path in ("launch.jpg", "ios/ver_1/Banner-2.webp?version=1"):
                with self.subTest(url=prefix + directory + "/" + path):
                    hit, = [rule.action for rule in rules if rule.matches(prefix + directory + "/" + path)]
                    self.assertEqual(hit, "reject_img(200)")
            for other in ("statement/bill.png", "security/notice.png", directory + "Other/test.jpg",
                          directory + "/2026../banner.jpg", directory + "/../statement/bill.png",
                          directory + "/%2e%2e/statement/bill.png", directory + "/account.json",
                          directory + "/pay.png.json", directory + "/statement.pdf"):
                self.assertFalse(any(rule.matches(prefix + other) for rule in rules), prefix + other)
        hosts = set(suite["mitm"][0].split("=", 1)[1].strip().split(", "))
        for host in ("api-sams.walmartmobile.cn", "acs.m.taobao.com", "3g.csair.com",
                     "ccsp-egmas.sf-express.com", "apps.api.ke.com"):
            self.assertNotIn(host, hosts)
