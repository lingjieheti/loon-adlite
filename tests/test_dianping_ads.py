"""Check Dianping ad isolation and transport for its shared gateways and image CDN."""
import unittest
from urllib.parse import urlsplit

from test_suite import ROOT, Rewrite, read_sections


class DianpingAds(unittest.TestCase):
    def test_ad_service_does_not_block_general_services(self):
        for name in ("iPad-AdSuite.lpx", "iPad-AdLite.lpx"):
            with self.subTest(plugin=name):
                rules = read_sections(ROOT / name)["rule"]
                self.assertIn("DOMAIN,ad.api.dianping.com,REJECT", rules)
                for host in ("www.dianping.com", "api.dianping.com", "search.api.dianping.com",
                             "tuangou.api.dianping.com", "waimai.api.dianping.com", "mapi.dianping.com"):
                    self.assertNotIn(f"DOMAIN,{host},REJECT", rules)

    def test_shared_gateways_and_image_hosts_bypass_the_plugin(self):
        urls = (
            "https://www.dianping.com/shanghai",
            "https://www.dianping.com/shop/123/review_all",
            "https://www.dianping.com/search/keyword/1/food",
            "https://www.dianping.com/ajax/userinfo",
            "https://www.dianping.com/ajax/brandad?cityId=1",
            "https://mapi.dianping.com/mapi/pay/order",
            "https://mapi.dianping.com/mapi/operating/loadsplashconfig",
            "https://p0.meituan.net/400.0/tdchoteldark/6585110463be8ea41647eb9877d021b85812516.jpg",
            "https://p1.meituan.net/400.0/tdchotel/552eb6ffdf6f113aa25ce631fb80aeeb503760.jpg",
            "https://img.meituan.net/mallimages/50e80a6d146c08c2c2bbd6efeba08465213674.png",
            "https://p0.meituan.net/adunion/example.webp",
            "https://img.meituan.net/bizad/bizad_brandCpt_123456.jpg",
        )
        for name in ("iPad-AdLite.lpx", "iPad-InlineAds.lpx", "iPad-AdSuite.lpx"):
            sections = read_sections(ROOT / name)
            rules = sections.get("rule", [])
            decrypted = {host.strip() for line in sections.get("mitm", [])
                         for host in line.partition("=")[2].split(",")}
            rewrites = [Rewrite.parse(line) for line in sections.get("rewrite", [])]
            for url in urls:
                with self.subTest(plugin=name, url=url):
                    host = urlsplit(url).hostname
                    self.assertNotIn(f"DOMAIN,{host},REJECT", rules)
                    self.assertNotIn(host, decrypted)
                    for method in ("GET", "POST"):
                        self.assertFalse(any(rule.matches(url, method=method) for rule in rewrites))
