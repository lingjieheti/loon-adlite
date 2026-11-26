"""Offline Douyin regressions for the shared iPhone and iPad Loon plugin."""

import unittest
from urllib.parse import urlsplit

import test_suite as shared


HOSTS = (
    "api3-core-c.amemv.com", "api3-normal-c.amemv.com", "api.amemv.com",
)
FEEDS = ("/aweme/v1/feed", "/aweme/v2/feed")
SPLASH = (
    "/api/ad/v1/splash/stock",
    "/api/ad/v16/splash/preload",
    "/api/ad/splash/stock/realtime/v14",
    "/api/ad/splash/stock/realtime/v15",
    "/api/ad/splash/aweme/v15",
)


class Douyin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shared.AdSuite.setUpClass()
        cls.rules = shared.AdSuite.rules
        cls.sections = shared.AdSuite.sections
        cls.jq = shared.AdSuite.jq

    matches = shared.AdSuite.matches
    check_body = shared.AdSuite.check_body

    def test_feed_routes_and_content_types(self):
        for host in HOSTS:
            for path in FEEDS:
                for suffix in ("", "/", "?count=10", "/?cursor=123&count=10"):
                    url = f"https://{host}{path}{suffix}"
                    with self.subTest(url=url):
                        rule, = self.matches(url)
                        self.assertEqual(rule.phase, "response")
                        self.assertTrue(rule.matches(url, mime="Application/JSON; charset=utf-8"))
                        for status in (204, 304, 403, 500):
                            self.assertFalse(rule.matches(url, status=status))
                        for mime in ("application/x-protobuf", "application/protobuf", "application/grpc+proto",
                                     "application/octet-stream", "application/jsonp", "video/mp4", "text/html", ""):
                            self.assertFalse(rule.matches(url, mime=mime), mime)

    def test_splash_routes_reject_without_loading_the_response(self):
        for host in HOSTS:
            for path in SPLASH:
                for suffix in ("", "/", "?version=15", "/?version=15"):
                    url = f"https://{host}{path}{suffix}"
                    with self.subTest(url=url):
                        rule, = self.matches(url)
                        self.assertEqual((rule.phase, rule.action), ("request", "reject(404)"))

    def test_media_search_comments_and_near_matches(self):
        normal_paths = (
            "/aweme/v1/play/", "/aweme/v1/aweme/detail/", "/aweme/v1/search/item/",
            "/aweme/v2/comment/list/", "/aweme/v1/feed/follow/", "/aweme/v2/feedExtra",
            "/aweme/v3/feed", "/aweme/v1/feed/next", "/aweme/v1/feed.json",
            "/video/tos/cn/example.mp4", "/live/room/enter", "/shop/product/detail",
            "/api/ad/splash/aweme/v14", "/api/ad/splash/stock/realtime/v16",
            "/api/ad/v16/splash/preloader", "/api/ad/v1/splash/stock/history",
            "/other?next=/aweme/v1/feed", "/api/ad/config?next=/api/ad/v1/splash/stock",
        )
        blocked = {line.split(",")[1] for line in self.sections["rule"]}
        intercepted = {h.strip() for h in self.sections["mitm"][0].split("=", 1)[1].split(",")}
        douyin_hosts = {h for h in intercepted if h in ("amemv.com", "snssdk.com")
                        or h.endswith((".amemv.com", ".snssdk.com"))}
        self.assertEqual(set(HOSTS), douyin_hosts)
        self.assertFalse(set(HOSTS) & blocked)
        urls = [f"https://{host}{path}" for host in HOSTS for path in normal_paths]
        for host in HOSTS:
            for path in (*FEEDS, *SPLASH):
                urls.extend([
                    f"https://{host}.example.org{path}", f"https://{host}@example.org{path}",
                    f"https://test.{host}{path}", f"http://{host}{path}",
                ])
        for host in ("api4-normal-c.amemv.com", "api3-core.amemv.com", "aweme-snssdk.com", "aweme.snssdk.com"):
            urls.extend(f"https://{host}{path}" for path in (*FEEDS, *SPLASH))
        for url in urls:
            with self.subTest(url=url):
                self.assertNotIn(urlsplit(url).hostname, blocked)
                self.assertEqual(self.matches(url), [])

    def test_only_explicit_top_level_ad_cards_are_removed(self):
        ads = [{"is_ads": True, "aweme_id": "ad-a"}, {"is_ads": 1, "aweme_id": "ad-b"}]
        keep = [
            {"aweme_id": shared.BIG_ID, "video": {"play_addr": {"url_list": ["video"]}}},
            {"is_ads": False, "live_room": {"id": shared.BIG_ID}},
            {"is_ads": 0, "product_promotions": [{"id": "shop", "is_ads": True}]},
            {"aweme_id": "organic", "raw_ad_data": {"is_ads": 1}},
            {"author": {"is_ads": True}, "children": [ads[0]]},
            {"is_ads": "1"}, {"is_ads": "true"}, {"is_ads": None}, {"is_ads": 2}, {"is_ads": -1},
            {"is_ads": {}}, {"is_ads": [1]}, {}, None, "unknown", 7, False, [ads[1]],
        ]
        metadata = {
            "has_more": 1, "max_cursor": shared.BIG_ID, "min_cursor": 12,
            "extra": {"log_id": str(shared.BIG_ID), "aweme_list": ads},
            "is_ads": True,
        }
        for path in FEEDS:
            for flags in ({"status_code": 0}, {"status_code": 0, "error_code": 0, "success": True}):
                source = {**flags, **metadata, "aweme_list": [ads[0], *keep[:3], ads[1], *keep[3:]]}
                expected = {**source, "aweme_list": keep}
                with self.subTest(path=path, flags=flags):
                    self.check_body(f"https://{HOSTS[0]}{path}", source, expected)

    def test_all_ad_page_preserves_original_items_and_cursor(self):
        for host in HOSTS:
            url = f"https://{host}/aweme/v2/feed/?count=2"
            for has_more in (0, 1):
                source = {"status_code": 0, "aweme_list": [{"is_ads": True}, {"is_ads": 1}],
                          "has_more": has_more, "max_cursor": shared.BIG_ID, "next": {"page": 2}}
                with self.subTest(host=host, has_more=has_more):
                    self.check_body(url, source, source)

    def test_placeholder_pages_preserved_and_only_recognized_content_permits_removal(self):
        url = f"https://{HOSTS[0]}{FEEDS[0]}"
        ad = {"is_ads": True, "aweme_id": "123456789"}
        placeholders = [
            None, False, [], {}, {"cursor": "next"}, {"k": 2}, {"id": "123"},
            {"video": {}}, {"live_room": {}}, {"live_room": {"id": {}}},
            {"room_id": []}, {"room_id": 0}, {"room_id": "0"}, {"room_id": "00"},
            {"aweme_id": None}, {"aweme_id": True}, {"aweme_id": -3}, {"aweme_id": 1.5},
            {"aweme_id": ""}, {"aweme_id": " "}, {"aweme_id": "normal"}, {"aweme_id": "934\n"},
        ]
        for items in ([ad, None], [ad, {"cursor": "next"}, {"k": 2}], [ad, *placeholders]):
            source = {"status_code": 0, "aweme_list": items, "has_more": 1, "max_cursor": shared.BIG_ID}
            with self.subTest(items=items):
                self.check_body(url, source, source)
        for content in ({"aweme_id": shared.BIG_ID}, {"aweme_id": "123456789"},
                        {"room_id": "123456789"}, {"live_room": {"id": shared.BIG_ID}},
                        {"live_room": {"id_str": "987654321"}}):
            source = {"status_code": 0, "aweme_list": [ad, *placeholders, content], "max_cursor": shared.BIG_ID}
            with self.subTest(content=content):
                self.check_body(url, source, {**source, "aweme_list": [*placeholders, content]})

    def test_large_ordinary_and_mixed_pages_preserve_order_and_content(self):
        url = f"https://{HOSTS[0]}{FEEDS[0]}?count=100"
        items = [{"aweme_id": str(shared.BIG_ID + i), "video": {"play_addr": {"url_list": [str(i)]}},
                  "author": {"id": shared.BIG_ID - i, "is_ads": True}} for i in range(100)]
        page = {"status_code": 0, "aweme_list": items, "has_more": 1, "max_cursor": shared.BIG_ID}
        self.check_body(url, page, page)
        ad = {"is_ads": 1, "aweme_id": "819923456789"}
        self.check_body(url, {**page, "aweme_list": [*items[:48], ad, *items[48:]]}, page)

    def test_targeted_shares_are_preserved_and_general_queries_are_filtered(self):
        organic = {"aweme_id": str(shared.BIG_ID), "is_ads": 0}
        source = {"status_code": 0, "aweme_list": [{"is_ads": True}, organic],
                  "max_cursor": shared.BIG_ID, "has_more": 1}
        for path in FEEDS:
            base = f"https://{HOSTS[0]}{path}/"
            for query in ("aweme_id=123", "aweme_ids=123%2C456&count=1",
                          "count=2&aweme_id=123", "offset=8&aweme_ids=123&from=share",
                          "aweme%5Fid=7", "count=2&%61weme_id=7", "from=share&aweme_id%73=7",
                          "aweme_id", "count=2&aweme_ids&from=share", "count=2&aweme_id=",
                          "count=1&cur%73or=7", "aweme_ids#fragment"):
                with self.subTest(path=path, query=query):
                    self.assertEqual(self.matches(base + "?" + query), [])
                    self.check_body(base + "?" + query, source, source)
            for query in ("count=10&cursor=456", "previous_aweme_id=123", "aweme_id_hint=123",
                          "source=aweme_ids", "cursor=456&count=2", "cursor=%31%32",
                          "from=aweme%5Fid%3D88", "link=%26aweme_id%3D7&count=1"):
                with self.subTest(path=path, query=query):
                    self.check_body(base + "?" + query, source, {**source, "aweme_list": [organic]})

    def test_errors_missing_status_and_changed_envelopes_survive(self):
        url = f"https://{HOSTS[0]}{FEEDS[0]}"
        mixed = [{"is_ads": True}, {"aweme_id": "782000000000001"}]
        for flags in (
            {}, {"error_code": 0}, {"status_code": None}, {"status_code": "0"},
            {"status_code": False}, {"status_code": 403, "error_code": 0},
            {"status_code": 0, "error_code": 403}, {"status_code": 0, "error_code": "0"},
            {"status_code": 0, "error_code": None}, {"status_code": 0, "error_code": False},
            {"status_code": 0, "error": {"code": 403}}, {"status_code": 0, "success": False},
            {"status_code": 0, "success": 0}, {"status_code": 0, "success": None},
            {"status_code": 0, "systemError": True},
        ):
            source = {**flags, "aweme_list": mixed, "max_cursor": shared.BIG_ID}
            with self.subTest(flags=flags):
                self.check_body(url, source, source)
        for source in (
            None, [], False, {"status_code": 0}, {"status_code": 0, "data": {"aweme_list": mixed}},
            {"status_code": 0, "aweme_list": None}, {"status_code": 0, "aweme_list": "future"},
            {"status_code": 0, "aweme_list": {"items": mixed}}, {"status_code": 0, "aweme_list": []},
        ):
            with self.subTest(source=source):
                self.check_body(url, source, source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
