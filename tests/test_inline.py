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


PLUGIN = Path(__file__).resolve().parents[1] / "iPad-InlineAds.lpx"
WX_AD = "https://mp.weixin.qq.com/mp/getappmsgad"
WX_EXT = "https://mp.weixin.qq.com/mp/getappmsgext"
APP_FEED = "https://app.bilibili.com/x/v2/feed/index"
WEB_FEED = "https://api.bilibili.com/x/web-interface/wbi/index/top/feed/rcmd"
BIG_ID = 123456789012345678901234567891


def read_rules():
    rules = []
    in_rewrite = False
    url_regex = re.compile(r"\$\{url\}\s*~=\s*/((?:\\.|[^/\\])*)/([i]?)")
    action = re.compile(r"\bthen\s+response\.json\.jq\(`([^`]+)`\)\s*$")
    for lineno, raw in enumerate(PLUGIN.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if line.startswith("[") and line.endswith("]"):
            in_rewrite = line.lower() == "[rewrite]"
        elif in_rewrite and line and not line.startswith("#"):
            pattern, program = url_regex.search(line), action.search(line)
            if not line.startswith("response if ") or not (pattern and program):
                raise ValueError(f"Unsupported rewrite at line {lineno}: {line}")
            flags = re.IGNORECASE if pattern.group(2) == "i" else 0
            rules.append((re.compile(pattern.group(1), flags), program.group(1), line.split(" then ", 1)[0]))
    if not rules:
        raise ValueError(f"No rewrite rules in {PLUGIN}")
    return rules


class InlineAds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = read_rules()
        cls.jq = os.environ.get("JQ") or shutil.which("jq")
        if not cls.jq:
            raise RuntimeError("Install jq or set JQ to the path of its executable.")

    def matching_rules(self, url):
        return [rule for rule in self.rules if rule[0].search(url)]

    def rewrite(self, url, source):
        rules = self.matching_rules(url)
        self.assertEqual(len(rules), 1, f"Expected exactly one rule for {url}")
        _, program, _ = rules[0]
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
        for url in (WX_AD, WX_EXT, APP_FEED, WEB_FEED):
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
        for url in (WX_AD, WX_EXT, APP_FEED, WEB_FEED):
            (_, _, condition), = self.matching_rules(url)
            self.assertRegex(condition, r"&&\s*\$\{response\.status\}\s*==\s*200(?:\s|$)")
            if url in (APP_FEED, WEB_FEED):
                header = re.search(
                    r"\$\{response\.header\['Content-Type'\]\}\s*~=\s*/((?:\\.|[^/\\])*)/i", condition,
                )
                self.assertIsNotNone(header)
                mime = re.compile(header[1], re.I)
                for good in ("application/json", "Application/JSON; charset=utf-8"):
                    self.assertRegex(good, mime)
                for bad in ("text/html", "application/grpc", "application/jsonp"):
                    self.assertNotRegex(bad, mime)

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

    def test_bilibili_errors_and_changed_shapes(self):
        for url, key, ad in (
            (APP_FEED, "items", {"card_type": "cm_v2", "card_goto": "ad_av"}),
            (WEB_FEED, "item", {"goto": "ad"}),
        ):
            wrong_key = "item" if key == "items" else "items"
            for payload in (
                {"code": -101, "data": {key: [ad]}},
                {"code": "0", "data": {key: [ad]}},
                {"data": {key: [ad]}},
                {"code": 0, "data": {wrong_key: [ad]}},
                {"code": 0, "data": {key: {"unexpected": ad}}},
                {"code": 0, "data": None}, [],
            ):
                with self.subTest(url=url, payload=payload):
                    self.check_result(url, payload, payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
