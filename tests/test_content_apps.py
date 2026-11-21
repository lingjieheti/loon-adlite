"""Check the narrowly scoped Baidu ad rules and preserve ordinary map and Tieba services."""
import unittest

import test_suite as shared


TIEBA = "https://tiebac.baidu.com"
BATCH = TIEBA + "/tiebaads/commonbatch"


class ContentAppAds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shared.AdSuite.setUpClass()
        cls.rules = shared.AdSuite.rules
        cls.jq = shared.AdSuite.jq

    matches = shared.AdSuite.matches
    check_body = shared.AdSuite.check_body

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

    def test_tieba_image_ad_list_preserves_envelope_and_unrelated_data(self):
        url = BATCH + "?pid=123&adcmd=1&ext=a%2Fb"
        extras = {"photo_list": [{"id": shared.BIG_ID}], "req": "original"}
        for status in ({"error_code": 0}, {"errno": 0, "errmsg": ""}, {"errno": 0, "error_code": 0}):
            source = {**status, "res": {**extras, "ad": [{"id": 12}, {"id": 24}]}, "cursor": shared.BIG_ID}
            expected = {**source, "res": {**extras, "ad": []}}
            self.check_body(url, source, expected)
        for invalid in ({"error_code": "0"}, {"errno": 250107, "errmsg": "pid id empty."},
                        {"errno": 0, "error_code": 4}, {"errno": 0, "errmsg": "login required"},
                        {"errno": 0, "error": {"code": 403}}, {"errno": 0, "success": False},
                        {"errno": 0, "code": 403}, {"errno": 0, "error_msg": "expired"}, {}):
            source = {**invalid, "res": {"ad": [{"id": 1}]}}
            self.check_body(url, source, source)
        for items in (None, [], {}, ["future schema"], [{"id": 1}, 2]):
            source = {"error_code": 0, "res": {"ad": items}, "other": [{"ad": "keep"}]}
            self.check_body(url, source, source)

    def test_tieba_scope_is_limited_to_named_endpoint_and_json(self):
        url = BATCH + "?adcmd=1"
        self.assertEqual(len(self.matches(url)), 1)
        self.assertEqual(self.matches(url, status=403), [])
        for mime in ("application/grpc", "application/jsonp", "application/x-javascript", "text/html"):
            self.assertEqual(self.matches(url, mime=mime), [])
        for near in (BATCH, BATCH + "?pid=1", BATCH + "?pid=adcmd=1", BATCH + "?adcmd=",
                     BATCH + "?c%62=x&adcmd=1", url + "&callBack=show", BATCH + "?jsonp=fn&adcmd=1",
                     BATCH + "/more?adcmd=1", url.replace("baidu.com", "baidu.com.example.org"),
                     TIEBA + "/c/f/frs/page?cmd=1", TIEBA + "/c/f/pb/picpage", TIEBA + "/c/s/login",
                     "https://newclient.map.baidu.com/client/phpui2/?qt=route"):
            self.assertEqual(self.matches(near), [], near)

    def test_tieba_requires_a_single_ad_command_even_in_long_queries(self):
        params = "item=1&" * 1024
        self.assertEqual(len(self.matches(BATCH + "?" + params + "adcmd=1")), 1)
        self.assertEqual(len(self.matches(BATCH + "?adcmd=1&" + params + "tail=1")), 1)
        for query in ("adcmd=1&adcmd=1", "adcmd=&adcmd=2", "adcmd=1&AdCmd=2",
                      params + "adcmd=1&callback=cb", "adcmd=1&" * 1024 + "%bad"):
            self.assertEqual(self.matches(BATCH + "?" + query), [])
