"""Check Dianping's dedicated ad host and the brand banner used by the city website."""
import unittest

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

    def test_only_the_city_banner_request_is_replaced(self):
        section = read_sections(ROOT / "iPad-AdSuite.lpx")
        rewrites = [Rewrite.parse(line) for line in section["rewrite"]]
        site = "https://www.dianping.com"
        for suffix in ("/ajax/brandad", "/ajax/brandad?cityId=1"):
            with self.subTest(suffix=suffix):
                rule, = [r for r in rewrites if r.matches(site + suffix)]
                self.assertEqual((rule.phase, rule.action), ("request", "reject_dict(200)"))
        for url in (site + "/shanghai", site + "/ajax/userinfo", site + "/shop/123",
                    site + "/shop/123/review_all", site + "/search/keyword/1/food",
                    site + "/ajax/brandadvice", site + "/ajax/brandad/order",
                    site + "/ajax/userinfo?next=/ajax/brandad", site + ".example.org/ajax/brandad",
                    "https://mapi.dianping.com/ajax/brandad", "https://mapi.dianping.com/mapi/pay/order"):
            with self.subTest(url=url):
                self.assertFalse(any(r.matches(url) for r in rewrites))
