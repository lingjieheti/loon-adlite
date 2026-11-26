"""Check the narrowly scoped Baidu ad rules and preserve ordinary map and Tieba services."""
import unittest

import test_suite as shared


class ContentAppAds(unittest.TestCase):
    def test_baidu_ad_endpoints_leave_location_navigation_and_forums_available(self):
        for name in ("iPad-AdLite.lpx", "iPad-AdSuite.lpx"):
            rules = shared.read_sections(shared.ROOT / name)["rule"]
            blocked = {line.split(",")[1] for line in rules}
            self.assertTrue({"afd.baidu.com", "afdconf.baidu.com"} <= blocked)
            self.assertTrue(blocked.isdisjoint({
                "baidu.com", "map.baidu.com", "newclient.map.baidu.com", "api.map.baidu.com",
                "lc.map.baidu.com", "httpdns.baidubce.com", "tiebac.baidu.com", "tieba.baidu.com",
                "passport.baidu.com", "afd.baidu.com.example.org",
            }))
            self.assertNotIn("180.76.76.200", blocked)
