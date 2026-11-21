"""Run Pinduoduo's native response filters against synthetic shopping responses."""
import unittest

import test_suite as shared


HOST = "https://api.pinduoduo.com"
HOME = HOST + "/api/alexa/homepage/hub"
PROFILE = HOST + "/api/philo/personal/hub"


class PinduoduoAds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shared.AdSuite.setUpClass()
        cls.rules = shared.AdSuite.rules
        cls.jq = shared.AdSuite.jq

    matches = shared.AdSuite.matches
    check_body = shared.AdSuite.check_body

    def test_only_explicit_home_ad_modules(self):
        keep = [{"module_name": "goods", "goods_id": shared.BIG_ID},
                {"module_name": "billion_subsidy_entrance"}, {"module_name": "ad_module_v2"},
                {"module_name": "icon_set", "title": "广告行业资讯"}, None, 42, "ad_module"]
        result = {"bottom_tabs": ["home", "chat"], "coupons": [123], "dy_module": {"ad_module": {"meta": 1}}}
        expected = {"success": True, "result": {**result, "module_order": keep}}
        source = {"success": True, "result": {**result, "module_order": [
            *keep[:2], {"module_name": "ad_module", "id": 2}, *keep[2:], {"module_name": "ad_module"},
        ]}}
        for url in (HOME, HOME + "/refresh?region=1"):
            with self.subTest(url=url):
                self.check_body(url, source, expected)
                self.check_body(url, expected, expected)

    def test_personal_center_and_pickup_notices_pass_through(self):
        payload = {"success": True, "icon_set": {"orders": {}}, "personal_banner": {"items": [
            {"type": "order_notice", "order_id": shared.BIG_ID, "title": "待自提订单取货码"},
            {"type": "promotion", "title": "新人折扣"},
        ]}}
        self.assertEqual(self.matches(PROFILE), [])
        self.check_body(PROFILE, payload, payload)

    def test_failures_and_unknown_payloads_pass_through(self):
        home = {"result": {"module_order": [{"module_name": "ad_module"}]}}
        for flag in ({"success": False}, {"success": "true"}, {"code": 500}, {"error_code": 40001},
                     {"error_msg": "请登录"}, {"error": {"message": "failed"}}):
            with self.subTest(flag=flag):
                body = {**home, **flag}
                self.check_body(HOME, body, body)
        for body in (None, [], "future", {"data": home}, {"result": 1},
                     {"result": {"module_order": {"module_name": "ad_module"}}}):
            self.check_body(HOME, body, body)

    def test_exact_endpoints_http_status_and_mime(self):
        for path in (HOME, HOME + "/refresh"):
            rule, = self.matches(path + "/?app=1", mime="Application/JSON; charset=utf-8")
            self.assertEqual(rule.phase, "response")
            for options in ({"status": 401}, {"status": 500}, {"mime": "application/jsonp"},
                            {"mime": "text/html"}, {"mime": "application/octet-stream"}):
                self.assertEqual(self.matches(path, **options), [])
            for near in (path + "-v2", path + "/order", path.replace("api.", "mobile."),
                         path.replace(".com/", ".com.example/"), path.replace("https:", "http:")):
                self.assertEqual(self.matches(near), [])
        for path in ("/order/1001-1002/shipping", "/api/caterham/v3/query/my_order_group",
                     "/api/alexa/goods/back_up", "/api/growth/nagato/app/index/gather",
                     "/api/leporis/notification/clear_tab_red_dot", "/order/checkout",
                     "/api/philo/personal/order", "/coupon/claim", "/api/zaire_biz/chat/resource/get_list_data"):
            self.assertEqual(self.matches(HOST + path), [])


if __name__ == "__main__":
    unittest.main()
