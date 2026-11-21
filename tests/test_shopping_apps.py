"""Check selected shopping, ticketing and local-service ads and adjacent business traffic."""
import unittest
from urllib.parse import urlsplit

import test_suite as shared


MTOP = "https://acs.m.taobao.com/gw/"
AD_HOSTS = {"baidu-union-js.xiachufang.com", "baidu-union-pos.xiachufang.com", "adui.tg.meitu.com"}
REQUESTS = {
    "https://app.dewu.com/api/v1/app/advertisement": "reject(404)",
    "https://p0.pipi.cn/adAdmin/movie42.jpg?imageMogr2/quality/85": "reject_img(200)",
    "https://p0.pipi.cn/mediaplus/maoyantong_ads_fe/A42.png?imageMogr2/thumbnail/!165x165": "reject_img(200)",
    "https://p0.pipi.cn/adAdmin/promo_45.gif?cache=1": "reject_img(200)",
    "https://app.zhuanzhuan.com/zz/v2/zzlogic/getOpenScreen?version=1": "reject_dict(200)",
    "https://api-ios.zhipin.com/api/zpCommon/user/startupAd/": "reject_dict(200)",
}


class ShoppingAppAds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.suite = shared.read_sections(shared.ROOT / "iPad-AdSuite.lpx")
        cls.rules = [shared.Rewrite.parse(line) for line in cls.suite["rewrite"]]

    matches = shared.AdSuite.matches

    def test_known_placements_and_spoofed_hosts(self):
        for url, action in REQUESTS.items():
            with self.subTest(url=url):
                rule, = self.matches(url)
                self.assertEqual((rule.phase, rule.action), ("request", action))
                host = urlsplit(url).hostname
                for other in (host + ".example.org", "www." + host, host + "@example.org"):
                    self.assertEqual(self.matches(url.replace(host, other, 1)), [])

    def test_checkout_coupons_tickets_jobs_and_listings_survive(self):
        keep = (
            "https://app.dewu.com/api/v1/app/advertisement/new/activity/receiveCoupon",
            "https://app.dewu.com/api/v1/app/advertisement-extra",
            "https://cdn.poizon.com/node-common/product.jpg",
            "https://p0.pipi.cn/movie/poster42.jpg?imageMogr2/quality/80",
            "https://p0.pipi.cn/adAdmin/film.png?imageMogr2/thumbnail/!165x1650",
            "https://p0.pipi.cn/adAdmin/film.gif.webp",
            "https://app.zhuanzhuan.com/zz/v2/zzlogic/getOpenScreenSettings",
            "https://app.zhuanzhuan.com/zzx/transfer/getConfigInfo",
            "https://api-ios.zhipin.com/api/zpCommon/user/startupAddress",
            "https://api-ios.zhipin.com/api/zpCommon/upgrade/check",
            "https://apps.api.ke.com/config/config/getactivityconfig",
            "https://apps.api.ke.com/config/config/bootpage/options",
            MTOP + "mtop.damai.wireless.home.welcome/1.0/orders",
            MTOP + "mtop.film.mtopadvertiseapi.queryadvertiseextra/1.0/",
            MTOP + "mtop.film.mtopitemadvertiseapi.queryadvertise/1.0/detail",
            MTOP + "mtop.damai.wireless.order.create/1.0/",
            MTOP + "mtop.film.ticket.order/1.0/?next=mtop.film.mtopadvertiseapi.queryadvertise",
            MTOP + "mtop.wdk.render.queryindexpage/1.0/",
        )
        for url in keep:
            with self.subTest(url=url):
                self.assertEqual(self.matches(url), [])

    def test_dedicated_ad_domains_are_exact_in_both_plugins(self):
        profiles = (self.suite, shared.read_sections(shared.ROOT / "iPad-AdLite.lpx"))
        for profile in profiles:
            for host in AD_HOSTS:
                self.assertIn(f"DOMAIN,{host},REJECT", profile["rule"])
                self.assertNotIn(f"DOMAIN-SUFFIX,{host},REJECT", profile["rule"])
            for host in ("xiachufang.com", "api.xiachufang.com", "meitu.com", "message.meitu.com",
                         "app.dewu.com", "p0.pipi.cn", "api-ios.zhipin.com", "apps.api.ke.com", "acs.m.taobao.com"):
                self.assertNotIn(f"DOMAIN,{host},REJECT", profile["rule"])


if __name__ == "__main__":
    unittest.main()
