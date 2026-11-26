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

    def test_message_and_shared_commerce_hosts_bypass_the_plugin(self):
        # Offline route probes. Paths and ports do not establish current iOS endpoints.
        urls = (
            MTOP + "mtop.taobao.wireless.home.newface.awesome.get/1.0/",
            "https://guide-acs.m.taobao.com/gw/mtop.trade.order.create/1.0/",
            "https://guide-acs.m.taobao.com/gw/mtop.taobao.wireless.home.splash.awesome.get/1.0/",
            "https://guide-acs.m.taobao.com/gw/mtop.cainiao.adx.flyad.getad/1.0/",
            "https://msgacs.m.taobao.com/accs/auth",
            "https://amdc.m.taobao.com/",
            "https://wss-cntaobao.dingtalk.com/",
            "https://acs.m.goofish.com/gw/mtop.taobao.idlemessage.session.sync/3.0/",
            "https://acs.m.goofish.com/gw/mtop.taobao.idlecommerce.splash.ads/1.0/",
            "https://acs.m.goofish.com/gw/mtop.taobao.idlecommerce.splash.async.ads/1.0/",
            "https://wss-goofish.dingtalk.com/",
            "https://courier.push.apple.com:5223/",
            "https://courier.push.apple.com:443/",
        )
        for name in ("iPad-AdSuite.lpx", "iPad-AdLite.lpx", "iPad-InlineAds.lpx"):
            sections = shared.read_sections(shared.ROOT / name)
            blocked = {line.split(",")[1] for line in sections.get("rule", [])}
            decrypted = {host.strip() for line in sections.get("mitm", [])
                         for host in line.partition("=")[2].split(",")}
            rewrites = [shared.Rewrite.parse(line) for line in sections.get("rewrite", [])]
            for url in urls:
                with self.subTest(plugin=name, url=url):
                    host = urlsplit(url).hostname
                    self.assertNotIn(host, blocked)
                    self.assertNotIn(host, decrypted)
                    for method in ("GET", "POST"):
                        self.assertFalse(any(rule.matches(url, method=method) for rule in rewrites))

    def test_sams_club_business_and_cdn_traffic_bypasses_the_plugin(self):
        urls = (
            "https://www.samsclub.cn/",
            "https://cms.samsclub.cn/",
            "https://m-sams.walmartmobile.cn/common/terms-of-agreement?agreementType=3",
            "https://api-sams.walmartmobile.cn/api/v1/sams/trade/order/getOftenBuyGoods",
            "https://api-sams.walmartmobile.cn/api/v1/sams/goods-portal/spu/searchRecommendPool",
            "https://sams-home-online-1302115363.file.myqcloud.com/",
            "https://mcdn-sams.walmartmobile.cn/assets/index.e0ab9c1d.js",
            "https://decoration-sams.walmartmobile.cn/",
            "https://hub-kefu.walmartmobile.cn/",
            "https://sam-retail-static-1302115363.file.myqcloud.com/",
            "https://ssl.captcha.qq.com/",
        )
        for name in ("iPad-AdLite.lpx", "iPad-InlineAds.lpx", "iPad-AdSuite.lpx"):
            sections = shared.read_sections(shared.ROOT / name)
            blocked = {line.split(",")[1] for line in sections.get("rule", [])}
            decrypted = {host.strip() for line in sections.get("mitm", [])
                         for host in line.partition("=")[2].split(",")}
            rewrites = [shared.Rewrite.parse(line) for line in sections.get("rewrite", [])]
            for url in urls:
                with self.subTest(plugin=name, url=url):
                    host = urlsplit(url).hostname
                    self.assertNotIn(host, blocked)
                    self.assertNotIn(host, decrypted)
                    for method in ("GET", "POST"):
                        self.assertFalse(any(rule.matches(url, method=method) for rule in rewrites))

    def test_other_apps_message_and_transaction_requests_are_not_rewritten_or_rejected(self):
        blocked = {line.split(",")[1] for line in self.suite["rule"]}
        for url in (
            "https://long.weixin.qq.com/",
            "https://short.weixin.qq.com/",
            "https://jpushjd.m.jd.com/",
            "https://jpushsc.m.jd.com/",
            "https://api.m.jd.com/client.action?functionId=submitOrder",
            "https://api.pinduoduo.com/order/prepay",
            "https://api.weibo.cn/2/direct_messages/user_list",
            "https://api.zhihu.com/notifications/v3/message",
        ):
            with self.subTest(url=url):
                self.assertNotIn(urlsplit(url).hostname, blocked)
                for method in ("GET", "POST"):
                    self.assertEqual(self.matches(url, method=method), [])

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
