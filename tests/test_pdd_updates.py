"""Exercise the Pinduoduo search filter with synthetic paid and organic product cards."""
import unittest

import test_suite as shared


SEARCH = "https://api.pinduoduo.com/search"
URL = SEARCH + "?q=%E4%B9%A6&page=1"
ORGANIC = {"goods_id": 10, "goods_name": "A", "mall_id": 99, "coupon": {"id": shared.BIG_ID}}
PAID = {"goods_id": 20, "goods_name": "B",
        "ad": {"goods_id": 20, "creative_id": 50, "mall_id": 99, "ocpcBid": 3.5}}


class PinduoduoSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shared.AdSuite.setUpClass()
        cls.rules = shared.AdSuite.rules
        cls.jq = shared.AdSuite.jq

    matches = shared.AdSuite.matches
    check_body = shared.AdSuite.check_body

    def test_mixed_results_preserve_order_cursor_and_ordinary_copies_of_a_paid_product(self):
        second_listing = {"goods_id": PAID["goods_id"], "goods_name": "B", "ad": None}
        keep = [ORGANIC, second_listing, {"type": "coupon", "id": shared.BIG_ID}, None]
        envelope = {"flip": "opaque-next-page", "total": 120, "filters": {"mall_id": 99},
                    "expansion": {"title": "Other shops"}, "server_time_ms": shared.BIG_ID}
        source = {**envelope, "items": [PAID, *keep, PAID]}
        expected = {**envelope, "items": keep}
        self.check_body(URL, source, expected)
        self.check_body(SEARCH + "/?page=2&size=50&q=new%20books", source, expected)

    def test_unsupported_marks_all_paid_pages_and_errors_are_preserved(self):
        unknown = [
            {**PAID, "ad": {"mall_id": 99}},
            {**PAID, "ad": {"goods_id": 20, "creative_id": 50, "mall_id": 99}},
            *({**PAID, "ad": {**PAID["ad"], "ocpcBid": bid}} for bid in (0, -1, "3.5", True)),
            {**PAID, "ad": {**PAID["ad"], "goods_id": 30}},
            {**PAID, "ad": "广告"},
            {**PAID, "ad": {**PAID["ad"], "creative_id": False}},
            {**PAID, "ad": {**PAID["ad"], "mall_id": "99"}},
            {**PAID, "ad": {**PAID["ad"], "creative_id": 3.1}},
            {**PAID, "ad": {**PAID["ad"], "creative_id": shared.BIG_ID}},
            {**PAID, "goods_name": ""},
            {"goods_id": 60, "goods_name": "C", "is_ad": True},
        ]
        body = {"flip": "next", "items": [ORGANIC, PAID, *unknown]}
        self.check_body(URL, body, {**body, "items": [ORGANIC, *unknown]})
        for override in ({"success": False}, {"error_code": 40001, "empty_reason": 1},
                         {"code": 403}, {"error": {"message": "login"}}, {"error_msg": "请登录"},
                         {"empty_reason": 1}, {"items": [PAID, PAID]}, {"items": [PAID, None]},
                         {"items": {}}, {"flip": None}):
            with self.subTest(override=override):
                source = {**body, **override}
                self.check_body(URL, source, source)

    def test_search_endpoint_query_and_response_guards(self):
        rule, = self.matches(URL)
        self.assertEqual(rule.phase, "response")
        for url in (SEARCH, SEARCH + "?q=", SEARCH + "?q=a&q=b", SEARCH + "?q=a&Q=b",
                    SEARCH + "?cb=x&q=a", SEARCH + "?q=a&jsoncallback=x",
                    SEARCH + "?q=a&%63allback=x", SEARCH + "?q=a;cb=x",
                    SEARCH + "_hotquery?q=a", SEARCH + "/order?q=a",
                    URL.replace("api.pinduoduo.com", "api.pinduoduo.com.example.org")):
            with self.subTest(url=url):
                self.assertEqual(self.matches(url), [])
        for status, mime in ((403, "application/json"), (200, "application/jsonp"), (200, "text/html")):
            self.assertEqual(self.matches(URL, status=status, mime=mime), [])
