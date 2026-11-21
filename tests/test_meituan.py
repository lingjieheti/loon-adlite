"""Offline Meituan regression checks. Run with python tests/test_meituan.py."""

import copy
import unittest
from urllib.parse import urlsplit

import test_suite as shared


MAIN = "https://mop.meituan.com/api/entryModule/startupPicture"
DELIVERY = "https://wmapi.meituan.com/api/v7/loadInfo"
MINI = "https://rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement"
REQUESTS = {
    "https://wmapi.meituan.com/api/v7/openscreen": "reject_dict(200)",
    "https://wmapi.meituan.com/api/v7/startpicture": "reject_dict(200)",
    "https://p0.meituan.net/adunion/example.webp": "reject_img(200)",
    "https://p1.meituan.net/adunion/opaque-synthetic-id": "reject_img(200)",
    "https://p1.meituan.net/adunion/example.png@800w": "reject_img(200)",
    "https://img.meituan.net/bizad/bizad_brandCpt_123456.jpg": "reject_img(200)",
    "https://img.meituan.net/adunion/example.jpg.webp": "reject_img(200)",
    "https://img.meituan.net/adunion/example.gif.webp": "reject_img(200)",
}


class Meituan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shared.AdSuite.setUpClass()
        cls.rules = shared.AdSuite.rules
        cls.sections = shared.AdSuite.sections
        cls.jq = shared.AdSuite.jq

    matches = shared.AdSuite.matches
    check_body = shared.AdSuite.check_body

    def test_response_guards(self):
        for url in (MAIN, DELIVERY, MINI):
            for suffix in ("", "?city=1&source=app"):
                with self.subTest(url=url + suffix):
                    rule, = self.matches(url + suffix)
                    self.assertEqual(rule.phase, "response")
                    self.assertTrue(rule.matches(url + suffix, mime="Application/JSON; charset=utf-8"))
                    self.assertFalse(rule.matches(url + suffix, status=403))
                    self.assertFalse(rule.matches(url + suffix, status=500))
                    for mime in ("image/jpeg", "text/html", "application/jsonp"):
                        self.assertFalse(rule.matches(url + suffix, mime=mime))

    def test_main_splash_arrays(self):
        for nested in (False, True):
            for key in ("resource", "resourcesMap"):
                resource = {key: {"startupPicArea": [{"asset": "creative"}], "coupons": ["keep"]},
                            "unrelated": {"startupPicArea": ["keep"]}}
                source = {"code": 0, "data": resource} if nested else {"code": 200, **resource}
                expected = copy.deepcopy(source)
                (expected["data"] if nested else expected)[key]["startupPicArea"] = []
                with self.subTest(nested=nested, key=key):
                    self.check_body(MAIN, source, expected)
        holders = {
            "resource": {"startupPicArea": [1], "store": 2},
            "resourcesMap": {"startupPicArea": [3], "order": shared.BIG_ID},
        }
        cleared = {
            "resource": {"startupPicArea": [], "store": 2},
            "resourcesMap": {"startupPicArea": [], "order": shared.BIG_ID},
        }
        self.check_body(MAIN, {**holders, "data": holders}, {**cleared, "data": cleared})

    def test_main_unknown_and_error_data_survive(self):
        for area in (None, "unknown", {"asset": 1}, []):
            payload = {"resource": {"startupPicArea": area, "checkout": shared.BIG_ID}}
            self.check_body(MAIN, payload, payload)
        for flags in ({"code": 503}, {"success": False}, {"error": {"code": 10000}},
                      {"systemError": True}):
            payload = {**flags, "data": {"resourcesMap": {"startupPicArea": [1]}}}
            self.check_body(MAIN, payload, payload)
        for payload in ({"data": None}, {"resource": "future"}, {"resource": [1]}, [], None):
            self.check_body(MAIN, payload, payload)

    def test_delivery_changes_only_explicit_ad_array(self):
        splash = {"ad": [{"material": 1}], "mk": ["campaign"], "coupon": {"value": 5}}
        for flags in ({}, {"code": 0}, {"code": 200, "success": True}):
            source = {**flags, "data": {"startpicture": splash, "orderId": shared.BIG_ID}}
            expected = copy.deepcopy(source)
            expected["data"]["startpicture"]["ad"] = []
            self.check_body(DELIVERY, source, expected)
        for flags in ({"code": 403}, {"success": False}, {"systemError": True}, {"error": "blocked"}):
            payload = {**flags, "data": {"startpicture": splash}}
            self.check_body(DELIVERY, payload, payload)
        for unknown in (None, "creative", {"ad": {}}, {"ad": 7}, {"mk": ["coupon"]}, []):
            payload = {"code": 0, "data": {"startpicture": unknown}}
            self.check_body(DELIVERY, payload, payload)

    def test_restaurant_mini_program_filters_explicit_placements(self):
        retained = [None, {"adSiteId": "adunit-"}, {"adSiteId": "adunit-?"}, {"adSiteId": "merchant-coupon"},
                    {"adSiteId": 8}, {"futurePlacement": shared.BIG_ID}]
        ad = {"adSiteId": "adunit-synthetic-123", "adIntervals": 30}
        source = {
            "code": 200, "success": True, "systemError": False,
            "data": {"adSiteList": [ad, *retained], "store": 17}, "gray": "",
        }
        expected = copy.deepcopy(source)
        expected["data"]["adSiteList"] = retained
        self.check_body(MINI, source, expected)
        for flags in ({"code": 0}, {"success": False}, {"success": None}, {"systemError": True},
                      {"error": {"code": 401}}):
            payload = {**source, **flags}
            self.check_body(MINI, payload, payload)
        for field in ("code", "success"):
            payload = {key: val for key, val in source.items() if key != field}
            self.check_body(MINI, payload, payload)
        for data in (None, {"adSiteList": {}}, {"adSiteList": []}, {"couponList": [ad]}):
            payload = {**source, "data": data}
            self.check_body(MINI, payload, payload)

    def test_request_actions(self):
        for url, expected in REQUESTS.items():
            for suffix in ("", "?v=1"):
                with self.subTest(url=url + suffix):
                    rule, = self.matches(url + suffix)
                    self.assertEqual((rule.phase, rule.action), ("request", expected))

    def test_meals_coupons_payment_and_nearby_paths_are_kept(self):
        normal = [
            MAIN + "Extra", DELIVERY + "/child", MINI + "Config",
            "https://wmapi.meituan.com/api/v7/submitOrder",
            "https://wmapi.meituan.com/api/v7/openscreen-extra",
            "https://wmapi.meituan.com/api/v7/coupon/list",
            "https://wmapi.meituan.com/api/v7/startpicture/other",
            "https://rms.meituan.com/api/v1/rmsmina/c/checkout",
            "https://rms.meituan.com/api/v1/rmsmina/c/queryCoupon",
            "https://p0.meituan.net/xianfu/restaurant.jpg",
            "https://p1.meituan.net/adunion-extra/menu.jpg",
            "https://p2.meituan.net/adunion/example.webp",
            "https://img.meituan.net/bizad/bizad_brandCpt_bonus.jpg",
            "https://img.meituan.net/wmbanner/bizad_brandCpt_123456.jpg",
            "https://img.meituan.net/bizad/bizad_brandCpt_123456.jpg.more",
            "https://img.meituan.net/adunion/example.jpg",
            "https://img.meituan.net/adunion/example.gif.webp.disabled",
            "https://img.meituan.net/adunion2/example.jpg.webp",
        ]
        for url in (MAIN, DELIVERY, MINI, *REQUESTS):
            host = urlsplit(url).hostname
            normal.extend([url.replace(host, host + ".example.org"), url.replace("https://", "http://")])
        blocked = {line.split(",")[1] for line in self.sections["rule"]}
        for url in normal:
            with self.subTest(url=url):
                self.assertNotIn(urlsplit(url).hostname, blocked)
                self.assertEqual(self.matches(url), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
