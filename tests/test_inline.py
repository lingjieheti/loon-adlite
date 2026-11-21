"""Exercise the URL regexes and jq programs shipped in iPad-InlineAds.lpx.

Run with Python 3 and a jq executable on PATH, or set JQ to its full path.
These offline fixtures exercise the filters, not the Loon app or its TLS stack.
"""

import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import unittest
from urllib.parse import urlsplit

from test_suite import Rewrite, WECHAT_IMPRESSION_ACTION, read_sections


PLUGIN = Path(__file__).resolve().parents[1] / "iPad-InlineAds.lpx"
WX_AD = "https://mp.weixin.qq.com/mp/getappmsgad"
WX_EXT = "https://mp.weixin.qq.com/mp/getappmsgext"
APP_FEED = "https://app.bilibili.com/x/v2/feed/index"
APP_SPLASH = "https://app.bilibili.com/x/v2/splash/list"
WEB_FEED = "https://api.bilibili.com/x/web-interface/wbi/index/top/feed/rcmd"
BIG_ID = 123456789012345678901234567891


def read_rules():
    return [Rewrite.parse(line) for line in read_sections(PLUGIN)["rewrite"]]


class InlineAds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = read_rules()
        cls.jq = os.environ.get("JQ") or shutil.which("jq")
        if not cls.jq:
            raise RuntimeError("Install jq or set JQ to the path of its executable.")

    def matching_rules(self, url):
        return [rule for rule in self.rules if rule.matches(url)]

    def rewrite(self, url, source):
        rules = self.matching_rules(url)
        self.assertEqual(len(rules), 1, f"Expected exactly one rule for {url}")
        program = rules[0].jq
        self.assertTrue(program, f"Expected a jq response for {url}")
        run = subprocess.run(
            [self.jq, "-c", program],
            input=json.dumps(source),
            encoding="utf-8",
            capture_output=True,
            timeout=10,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        return json.loads(run.stdout)

    def check_result(self, url, source, expected):
        # JSON serialization also distinguishes false from 0 and true from 1.
        wanted = json.dumps(expected, sort_keys=True)
        result = self.rewrite(url, source)
        self.assertEqual(json.dumps(result, sort_keys=True), wanted)
        self.assertEqual(json.dumps(self.rewrite(url, result), sort_keys=True), wanted)

    def test_url_scope(self):
        for url in (WX_AD, WX_EXT, APP_FEED, APP_SPLASH, WEB_FEED):
            for suffix in ("", "?a=1&b=2"):
                with self.subTest(url=url + suffix):
                    self.assertEqual(len(self.matching_rules(url + suffix)), 1)
            for near in (
                url + "-new", url + "/child", url.replace("https://", "http://"),
                url.replace(".com/", ".com.example.org/"),
                url.replace(".com/", ".com@other.example/"),
            ):
                with self.subTest(url=near):
                    self.assertEqual(self.matching_rules(near), [])
        for near in (
            "https://mp.weixin.qq.com/mp/relatedarticle",
            "https://mp.weixin.qq.com/cgi-bin/bizlogin",
            "https://mp.weixin.qq.com/s?next=/mp/getappmsgad",
            "https://app.bilibili.com/x/v2/feed/index/story",
            "https://app.bilibili.com/x/v2/splash/show",
            "https://app.bilibili.com/x/v2/splash/brand/list",
            "https://app.bilibili.com/x/v2/splash/event/list2",
            "https://api.bilibili.com/x/v2/splash/list",
            "https://app.bilibili.com/x/v2/splash/listing?mobi_app=ipad",
            "https://api.bilibili.com/x/player/wbi/playurl",
            "https://api.bilibili.com/x/web-interface/index/top/feed/rcmd",
        ):
            with self.subTest(url=near):
                self.assertEqual(self.matching_rules(near), [])

    def test_response_guards_and_mitm_hosts(self):
        text = PLUGIN.read_text(encoding="utf-8-sig")
        hosts = re.findall(r"^hostname\s*=\s*(.+)$", text, re.I | re.M)
        self.assertEqual(len(hosts), 1)
        self.assertEqual(
            {entry.strip() for entry in hosts[0].split(",")},
            {urlsplit(url).hostname for url in (WX_AD, APP_FEED, WEB_FEED)},
        )
        for url in (WX_AD, WX_EXT, APP_FEED, APP_SPLASH, WEB_FEED):
            rule, = self.matching_rules(url)
            self.assertTrue(rule.jq)
            self.assertIsNotNone(rule.mime)
            for status in (201, 204, 403, 500):
                self.assertFalse(rule.matches(url, status=status))
            for good in ("application/json", "Application/JSON; charset=utf-8"):
                self.assertTrue(rule.matches(url, mime=good))
            for bad in ("text/html; charset=UTF-8", "application/grpc", "application/jsonp",
                        "text/javascript", "text/plain", "application/octet-stream", ""):
                self.assertFalse(rule.matches(url, mime=bad))
        self.assertEqual(len(self.rules), 7)
        self.assertEqual(sum(bool(rule.jq) for rule in self.rules), 4)
        self.assertEqual(sum(rule.phase == "request" for rule in self.rules), 2)
        self.assertEqual(sum(rule.action == WECHAT_IMPRESSION_ACTION for rule in self.rules), 1)

    def test_wechat_preserves_article_fields(self):
        source = {
            "base_resp": {"ret": 0, "errmsg": "ok"},
            "advertisement_num": 2,
            "advertisement_info": [{"id": 11}, {"id": 12}],
            "appmsgstat": {"read_num": 234, "like_num": 9},
            "can_comment": True,
            "future_id": BIG_ID,
        }
        expected = {**source, "advertisement_num": 0, "advertisement_info": []}
        for url in (WX_AD, WX_EXT):
            with self.subTest(url=url):
                self.check_result(url + "?scene=1", source, expected)

    def test_wechat_unknown_shapes_and_errors(self):
        examples = [
            {"base_resp": {"exportkey_token": "", "ret": -2}},
            {"base_resp": {"ret": 1}, "advertisement_num": 1, "advertisement_info": [1]},
            {"appmsgstat": {"ret": 13}, "advertisement_num": 1, "advertisement_info": [1]},
            {"ret": -1, "advertisement_num": 1, "advertisement_info": [1]},
            {"advertisement_num": "1", "advertisement_info": [1]},
            {"advertisement_num": False, "advertisement_info": [1]},
            {"advertisement_num": -1, "advertisement_info": [1]},
            {"advertisement_num": 1, "advertisement_info": {"items": [1]}},
            {"advertisement_num": 1}, {"advertisement_info": [1]}, {"article": BIG_ID}, [],
        ]
        for url in (WX_AD, WX_EXT):
            for payload in examples:
                with self.subTest(url=url, payload=payload):
                    self.check_result(url, payload, payload)

    def test_wechat_token_only_base_response(self):
        source = {
            "base_resp": {"wxtoken": 777}, "appmsgstat": {"ret": 0, "read_num": 19},
            "advertisement_num": 1, "advertisement_info": [{"id": BIG_ID}],
        }
        expected = {**source, "advertisement_num": 0, "advertisement_info": []}
        self.check_result(WX_EXT, source, expected)

    def test_app_cards_and_mixed_banners(self):
        keep = [
            {"card_type": "small_cover_v9", "card_goto": "av", "ad_info": {"id": 7}, "id": BIG_ID},
            {"card_type": "cm_v2", "card_goto": "unknown"},
            {"card_type": "future_card", "card_goto": "ad_av"},
            {"card_type": "unknown", "card_goto": "future", "meta": [1, 2]},
            None, "opaque", 7,
        ]
        ads = [
            {"card_type": "cm_v1", "card_goto": "ad_av"},
            {"card_type": "cm_v2", "card_goto": "ad_web_s"},
            {"card_type": "cm_v2", "card_goto": "ad_web_gif"},
            {"card_type": "cm_v2", "card_goto": "ad_inline_3d"},
            {"card_type": "cm_double_v9", "card_goto": "ad_inline_av"},
        ]
        for kind in ("banner_v8", "banner_ipad_v8"):
            banner = {
                "card_type": kind, "card_goto": "banner", "hash": 17,
                "banner_item": [{"type": "banner", "id": BIG_ID}, {"type": "ad"},
                                {"type": "ad_inline"}, {"type": "future"}, None],
            }
            source = {
                "code": 0, "data": {"items": [keep[0], *ads, banner, *keep[1:]], "cursor": BIG_ID},
                "message": "ok",
            }
            expected = copy.deepcopy(source)
            clean_banner = {**banner, "banner_item": [banner["banner_item"][0], {"type": "future"}, None]}
            expected["data"]["items"] = [keep[0], clean_banner, *keep[1:]]
            with self.subTest(banner=kind):
                self.check_result(APP_FEED, source, expected)

    def test_web_feed_requires_explicit_goto(self):
        organic = {"goto": "av", "id": BIG_ID, "business_info": {"is_ad_loc": True}}
        preserved = [organic, {"goto": "live"}, {"is_ad": True}, None, "opaque"]
        source = {"code": 0, "data": {"item": [*preserved, {"goto": "ad"}], "other": BIG_ID}}
        expected = {"code": 0, "data": {"item": preserved, "other": BIG_ID}}
        self.check_result(WEB_FEED, source, expected)

    def test_splash_commercial_material_and_same_response_references(self):
        # Fields in the published splash/list response, including the ad flag and cm_mark.
        ad = {"id": 9460, "card_type": 39, "source": 929, "is_ad": True, "cm_mark": 1, "is_ad_loc": True}
        keep = [
            {"id": 12, "thumb": "season.png", "logo_url": "logo.png"},
            {"id": 13, "is_ad_loc": True, "ad_cb": "receipt", "cm_mark": 1},
            {"id": 14, "is_ad": True, "cm_mark": 0}, {"id": 15, "is_ad": 1, "cm_mark": 1},
            {"id": 16, "is_ad": True, "cm_mark": "1"}, {"id": 17, "is_ad": True},
            {"is_ad": True, "cm_mark": 1}, {"id": False, "is_ad": True, "cm_mark": 1},
            {"id": "18", "is_ad": True, "cm_mark": 1}, {"id": 1.5, "is_ad": True, "cm_mark": 1},
            {"id": BIG_ID, "is_ad": True, "cm_mark": 1}, None, ["unknown"],
        ]
        schedule = [{"id": 12, "probability": 50}, {"id": "9460"}, {"next": BIG_ID}, None]
        retained = [12, "9460", False, 999, None, {"id": 9460}]
        data = {"list": [*keep[:2], ad, *keep[2:]], "show": [schedule[0], {"id": 9460}, *schedule[1:]],
                "keep_ids": [9460, *retained], "min_interval": 14400, "pull_interval": 900,
                "max_time": 4, "splash_request_id": "request", "other": {"list": [ad], "id": BIG_ID}}
        source = {"code": 0, "message": "0", "ttl": 1, "data": data}
        expected = {**source, "data": {**data, "list": keep, "show": schedule, "keep_ids": retained}}
        self.check_result(APP_SPLASH + "?mobi_app=ipad&platform=ios", source, expected)
        # The full published example has a null cache list and no display schedule.
        for refs in ({}, {"keep_ids": None}, {"show": {"id": 9460}, "keep_ids": "9460"}):
            self.check_result(APP_SPLASH, {"code": 0, "data": {"list": [ad], **refs}},
                              {"code": 0, "data": {"list": [], **refs}})

    def test_splash_never_removes_a_shared_or_unknown_display_reference(self):
        ad = {"id": 1031, "is_ad": True, "cm_mark": 1}
        for material_id in (1031, 1031.0, "1031", "1031.00", "01031"):
            organic = {"id": material_id, "thumb": "illustration.png"}
            for rows in ([ad, organic], [organic, ad]):
                data = {"list": rows, "show": [{"id": 1031}, {"id": 27}], "keep_ids": [1031, 27]}
                self.check_result(APP_SPLASH, {"code": 0, "data": data},
                                  {"code": 0, "data": {**data, "list": [organic]}})
        refs = {"show": [{"id": 1031, "ad_cb": "receipt"}], "keep_ids": [1031]}
        for fields in (refs, {**refs, "list": None}, {**refs, "list": [{"id": 1031, "is_ad_loc": True}]}):
            unchanged = {"code": 0, "data": fields}
            self.check_result(APP_SPLASH, unchanged, unchanged)

    def test_bilibili_errors_and_changed_shapes(self):
        for url, key, ad in (
            (APP_FEED, "items", {"card_type": "cm_v2", "card_goto": "ad_av"}),
            (WEB_FEED, "item", {"goto": "ad"}),
            (APP_SPLASH, "list", {"id": 9460, "is_ad": True, "cm_mark": 1}),
        ):
            wrong_key = "item" if key == "items" else "items"
            for payload in (
                {"code": -101, "data": {key: [ad]}},
                {"code": "0", "data": {key: [ad]}},
                {"code": 0, "success": False, "data": {key: [ad]}},
                {"code": 0, "error": {"code": 403}, "data": {key: [ad]}},
                {"data": {key: [ad]}},
                {"code": 0, "data": {wrong_key: [ad]}},
                {"code": 0, "data": {key: {"unexpected": ad}}},
                {"code": 0, "data": None}, [],
            ):
                with self.subTest(url=url, payload=payload):
                    self.check_result(url, payload, payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
