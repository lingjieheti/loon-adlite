"""Protect public business traffic on hosts freed from whole-host decryption."""

from urllib.parse import urlsplit
import unittest

from test_suite import ROOT, Rewrite, read_sections


BUSINESS_URLS = (
    "https://api.m.jd.com/client.action?functionId=isvObfuscator",
    "https://aweme.snssdk.com/aweme/v1/play/",
    "https://tiebac.baidu.com/c/f/pb/page",
    "https://m5.amap.com/ws/mapapi/navigation/auto",
    "https://app.variflight.com/trip/",
    "https://app.dewu.com/.well-known/apple-app-site-association",
    "https://app.dewu.com/api/v1/h5/index/fire/flow/product/detailV3",
    "https://p0.pipi.cn/basicdata/25bfd6d753706dc7ed8077fa5007898cf9e86.jpg?imageMogr2/thumbnail/2500x2500%3E",
    "https://app.zhuanzhuan.com/zz/transfer/search",
    "https://static.95508.com/cgbstatic/POCM/commercialPensionFile/20260710/202607101010403506981409129447.pdf",
)

RETIRED_AD_URLS = (
    "https://api.m.jd.com/client.action?functionId=start",
    "https://api.m.jd.com/client.action?functionId=welcomeHome",
    "https://aweme.snssdk.com/aweme/v1/feed",
    "https://aweme.snssdk.com/api/ad/v16/splash/preload",
    "https://tiebac.baidu.com/tiebaads/commonbatch?adcmd=1",
    "https://api.yangkeduo.com/api/cappuccino/splash",
    "https://m5.amap.com/ws/shield/dsp/app/startup/init",
    "https://app.variflight.com/v1/advert/",
    "https://app.dewu.com/api/v1/app/advertisement",
    "https://p0.pipi.cn/adAdmin/promo45.gif",
    "https://app.zhuanzhuan.com/zz/v2/zzlogic/getOpenScreen",
    "https://static.95508.com/mmg/ciop/sysabbr/cmep/images/popupads/ad.png",
)


class SharedBusinessGateways(unittest.TestCase):
    def test_business_and_retired_ad_urls_bypass_all_subscriptions(self):
        for name in ("iPad-AdSuite.lpx", "iPad-AdLite.lpx", "iPad-InlineAds.lpx"):
            sections = read_sections(ROOT / name)
            blocked = {line.split(",")[1] for line in sections.get("rule", [])}
            decrypted = {host.strip() for line in sections.get("mitm", [])
                         for host in line.partition("=")[2].split(",")}
            rewrites = [Rewrite.parse(line) for line in sections.get("rewrite", [])]
            for url in (*BUSINESS_URLS, *RETIRED_AD_URLS):
                with self.subTest(plugin=name, url=url):
                    host = urlsplit(url).hostname
                    self.assertNotIn(host, blocked)
                    self.assertNotIn(host, decrypted)
                    for method in ("GET", "POST"):
                        self.assertFalse(any(rule.matches(url, method=method) for rule in rewrites))


    def test_pinduoduo_splash_uses_the_original_response_on_both_gateways(self):
        suite = read_sections(ROOT / "iPad-AdSuite.lpx")
        rewrites = [Rewrite.parse(line) for line in suite["rewrite"]]
        for host in ("api.pinduoduo.com", "api.yangkeduo.com"):
            url = f"https://{host}/api/cappuccino/splash"
            for method in ("GET", "POST"):
                with self.subTest(host=host, method=method):
                    self.assertFalse(any(rule.matches(url, method=method) for rule in rewrites))
