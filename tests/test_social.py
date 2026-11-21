"""Offline checks for Weibo and Coolapk. Run with python tests/test_social.py."""

import unittest
from urllib.parse import urlsplit

import test_suite as shared


WEIBO = "https://api.weibo.cn/2/"
FRIENDS = (WEIBO + "statuses/friends/timeline", WEIBO + "statuses/unread_friends_timeline")
HOME = tuple(WEIBO + "statuses/" + path for path in (
    "container_timeline", "container_timeline_unread", "container_timeline_hot",
))
INTL = WEIBO + "ad/weibointl"
COOLAPK = ("https://api.coolapk.com/v6/main/dataList", "https://api.coolapk.com/v6/main/indexV8")
ALL_URLS = (*FRIENDS, *HOME, INTL, *COOLAPK)


class Social(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shared.AdSuite.setUpClass()
        cls.rules = shared.AdSuite.rules
        cls.sections = shared.AdSuite.sections
        cls.jq = shared.AdSuite.jq

    matches = shared.AdSuite.matches
    check_body = shared.AdSuite.check_body

    def test_weibo_friends_keeps_organic_statuses(self):
        organic = [
            {"id": shared.BIG_ID, "text": "广告行业观察", "promotion": {"type": "coupon"}},
            {"is_ad": "1", "mblogtypename": "热推"}, {"is_ad": True},
            {"mblogtypename": "广告研究"}, {"mblogtypename": "广告 "},
            {"promotion": {"type": "ad"}}, {"ads_material_info": {"is_ads": True}},
            {"retweeted_status": {"is_ad": 1}, "text": "我的转发"},
            {"user": {"name": "广告"}, "goods": [{"id": 17}]}, None, "unknown",
        ]
        for url in FRIENDS:
            mixed = [*organic[:2], {"is_ad": 1}, *organic[2:], {"mblogtypename": "广告"}]
            props = {"next_cursor": shared.BIG_ID, "items": [{"data": {"is_ad": 1}}], "ok": 1}
            with self.subTest(url=url):
                self.check_body(url, {**props, "statuses": mixed}, {**props, "statuses": organic})

    def test_weibo_home_uses_direct_data_or_status(self):
        keep = [
            {"data": {"text": "广告", "id": shared.BIG_ID, "promotion": {"type": "ad"}}},
            {"data": {"is_ad": "1"}, "status": {"is_ad": 1}},
            {"data": {}, "status": {"mblogtypename": "广告"}},
            {"data": False, "status": {"is_ad": 1}},
            {"data": [], "status": {"is_ad": 1}},
            {"data": {"retweeted_status": {"is_ad": 1}, "mblogtypename": "广告业"}},
            {"is_ad": 1}, {"status": {"is_ad": True}}, {"children": [{"data": {"is_ad": 1}}]},
            {"data": {"goods": [{"id": 34}], "user": {"name": "广告"}}}, None, 0,
        ]
        ads = [
            {"data": {"is_ad": 1}, "status": {"is_ad": 0}},
            {"status": {"mblogtypename": "广告"}}, {"data": None, "status": {"is_ad": 1}},
        ]
        common = {"error_code": 0, "statuses": [{"is_ad": 1}], "cursor": shared.BIG_ID}
        for url in HOME:
            with self.subTest(url=url):
                self.check_body(url, {**common, "items": [*keep[:2], *ads, *keep[2:]]},
                                {**common, "items": keep})

    def test_international_weibo_keeps_envelope(self):
        source = {"data": [{"id": 1}, {"unknown_ad_shape": True}], "paging": {"next": shared.BIG_ID}}
        self.check_body(INTL, source, {**source, "data": []})
        for value in (None, {}, "future", []):
            payload = {**source, "data": value}
            self.check_body(INTL, payload, payload)

    def test_coolapk_sponsor_template_only(self):
        ordinary = [
            {"entityTemplate": "imageScaleCard", "title": "值得买红包"},
            {"entityTemplate": "feed", "id": shared.BIG_ID},
            {"entityTemplate": "sponsorCardPreview"}, {"entityTemplate": "SponsorCard"},
            {"entityType": "sponsorCard"}, {"title": "赞助"}, {"title": "精选配件"},
            {"entityTemplate": "feed", "children": [{"entityTemplate": "sponsorCard"}]},
            None, "opaque",
        ]
        for url in COOLAPK:
            common = {"status": 1, "paging": {"cursor": shared.BIG_ID}}
            with self.subTest(url=url):
                self.check_body(url, {**common, "data": [{"entityTemplate": "sponsorCard"}, *ordinary]},
                                {**common, "data": ordinary})

    def test_common_business_status_guards(self):
        routes = (
            (FRIENDS[0], "statuses", {"is_ad": 1}), (HOME[0], "items", {"data": {"is_ad": 1}}),
            (INTL, "data", {"slot": 1}), (COOLAPK[0], "data", {"entityTemplate": "sponsorCard"}),
        )
        accepted = [
            {"error": None, "errno": 0, "error_code": 0, "success": True, "ok": 1, "status": 0, "errmsg": ""},
            {"ok": True, "status": 1, "errmsg": None},
        ]
        rejected = [
            {"error": {"code": 401}}, {"error_code": 401}, {"error_code": "0"},
            {"errno": -200}, {"errno": "0"}, {"success": 1}, {"success": False},
            {"ok": 0}, {"ok": "1"}, {"status": -1}, {"status": "1"}, {"errmsg": "invalid"},
        ]
        for url, key, ad in routes:
            for flags in accepted:
                with self.subTest(url=url, accepted=flags):
                    self.check_body(url, {**flags, key: [ad]}, {**flags, key: []})
            for flags in rejected:
                payload = {**flags, key: [ad]}
                with self.subTest(url=url, rejected=flags):
                    self.check_body(url, payload, payload)
            for payload in ({"other": [ad]}, {key: {"items": [ad]}}, None, ["error"], True):
                self.check_body(url, payload, payload)

    def test_url_host_status_and_content_type(self):
        expected_hosts = {"api.weibo.cn", "api.coolapk.com"}
        line, = self.sections["mitm"]
        hosts = {h.strip() for h in line.split("=", 1)[1].split(",")}
        self.assertTrue(expected_hosts.issubset(hosts))
        blocked = {line.split(",")[1] for line in self.sections["rule"]}
        self.assertFalse(expected_hosts & blocked)
        for url in ALL_URLS:
            for suffix in ("", "?page=2&count=10"):
                route = url + suffix
                with self.subTest(url=route):
                    rule, = self.matches(route)
                    self.assertEqual(rule.phase, "response")
                    self.assertTrue(rule.matches(route, mime="Application/JSON; charset=utf-8"))
                    for status in (204, 403, 500):
                        self.assertFalse(rule.matches(route, status=status))
                    for mime in ("text/html", "application/grpc", "application/jsonp"):
                        self.assertFalse(rule.matches(route, mime=mime))
            host = urlsplit(url).hostname
            for near in (url + "Extra", url + "/nested", url.replace("https://", "http://"),
                         url.replace(host, host + ".example.org"), url.replace(host, host + "@bad.example")):
                with self.subTest(url=near):
                    self.assertEqual(self.matches(near), [])
        for near in (
            WEIBO + "statuses/repost_timeline", WEIBO + "favorites", WEIBO + "comments/build_comments",
            WEIBO + "statuses/show", "https://api.coolapk.com/v6/feed/detail?id=7",
            "https://api.coolapk.com/v6/page/dataList", "https://api.coolapk.com/v6/account/loadConfig",
        ):
            with self.subTest(url=near):
                self.assertEqual(self.matches(near), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
