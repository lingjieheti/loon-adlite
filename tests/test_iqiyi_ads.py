"""Exercise the iQIYI card and placement rules from the published subscription."""

import unittest

import test_suite as shared


HOME = "https://cards.iqiyi.com/views_home/3.0/qy_home"
SEARCH = "https://cards.iqiyi.com/views_search/3.0/search"
HOT = "https://cards.iqiyi.com/views_search/3.0/hot_query_search"
MIXER = "https://t7z.cupid.iqiyi.com/mixer"


class IqiyiAds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shared.AdSuite.setUpClass()
        cls.rules = shared.AdSuite.rules
        cls.jq = shared.AdSuite.jq

    matches = shared.AdSuite.matches
    check_body = shared.AdSuite.check_body

    def test_home_and_search_use_their_own_explicit_ad_markers(self):
        home_ad = {"alias_name": "ad_trueview"}
        search_ad = {"strategy_com_id": "search_small_card_ad"}
        ordinary = [
            {"alias_name": "focus", "id": shared.BIG_ID}, {"alias_name": "qy_home_vip_opr_banner"},
            {"strategy_com_id": "search_com_related_query"}, {"strategy_com_id": "search_onebox_v2"},
            {"strategy_com_id": {}}, {"title": "广告行业纪录片"}, None, "unknown",
        ]
        meta = {"code": "0", "cursor": shared.BIG_ID, "base": {"statistics": {"ad_str": "keep"}}}
        for url, recognized, other in (
            (HOME, [home_ad, {"alias_name": "ad_mobile_flow"}], search_ad),
            (SEARCH, [search_ad, {"strategy_com_id": "ad_mobile_flow"}, {"strategy_com_id": "search_mid_text_ad"}], home_ad),
            (HOT, [{"strategy_com_id": "hot_query_search_top_ad"}], home_ad),
        ):
            keep = [*ordinary, other]
            self.check_body(url, dict(meta, cards=[*recognized, *keep]), dict(meta, cards=keep))
            for status in ({"code": "4"}, {"success": False}, {"stackTrace": []}, {"error": "bad request"}):
                body = dict(status, cards=recognized)
                self.check_body(url, body, body)
            for body in ({"cards": {"items": recognized}}, {}, [], 1, None):
                self.check_body(url, body, body)

    def test_mixer_keeps_unknown_mixed_empty_and_rewarded_placements(self):
        roll = {"creativeType": "roll", "templateType": "roll", "orderItemType": 11, "timePosition": "1"}
        focus = {"adZoneId": "1000000000406", "type": 0, "duration": 0, "startTime": 0, "ads": [roll]}
        card = dict(focus, adZoneId="1000000000822", ads=[roll, roll])
        keep = [
            {"adZoneId": "1000000001035", "ads": [roll]}, {"adZoneId": "1000000000947", "ads": []},
            dict(focus, ads=[roll, {"templateType": "reward", "creativeType": "reward"}]),
            dict(card, ads=[None]), dict(focus, ads=[]), dict(focus, ads={"templateType": "roll"}),
            dict(card, ads=[{"templateType": "roll"}]), {"adZoneId": 1000000000406, "ads": [roll]}, None,
            dict(card, type=1), dict(card, duration=30), dict(card, startTime=120), dict(card, startTime=None),
            dict(card, ads=[dict(roll, timePosition="2")]), dict(card, ads=[dict(roll, orderItemType=12)]),
        ]
        context = {"errorCode": 0, "serverError": "", "midrollPoints": {}, "futureSlots": {"next": 1},
                   "config": {"retry": False}, "videoId": shared.BIG_ID}
        self.check_body(MIXER, dict(context, adSlots=[focus, *keep, card]), dict(context, adSlots=keep))
        for status in ({"errorCode": None}, {"errorCode": 1}, {"errorCode": "0"}, {"error": "bad"},
                       {"serverError": "failed"}, {"midrollPoints": {"120": 30}}, {"midrollPoints": []}):
            body = {**context, **status, "adSlots": [focus]}
            self.check_body(MIXER, body, body)
        for field in ("errorCode", "serverError", "midrollPoints"):
            body = {**context, "adSlots": [focus]}
            del body[field]
            self.check_body(MIXER, body, body)

    def test_only_named_endpoints_and_json_are_rewritten(self):
        for url in (HOME, SEARCH, HOT, MIXER):
            self.assertEqual(len(self.matches(url + "?source=app")), 1)
            for mime in ("text/plain", "application/javascript", "video/mp4"):
                self.assertEqual(self.matches(url, mime=mime), [])
            self.assertEqual(self.matches(url, status=403), [])
            self.assertEqual(self.matches(url + "/extra"), [])
            self.assertEqual(self.matches(url.replace("iqiyi.com/", "iqiyi.com.example.org/")), [])
        for url in (
            "https://cache.video.iqiyi.com/dash", "https://i.vip.iqiyi.com/client/check",
            "https://passport.iqiyi.com/user/info", "https://cards.iqiyi.com/views_plt/3.0/player_tabs_v2",
            "https://t7z.cupid.iqiyi.com/show2?e=1", "https://t7z.cupid.iqiyi.com/track2",
            "https://t7z.cupid.iqiyi.com/video/episode.m3u8", "https://cards.iqiyi.com/views_comment/3.0/long_video_comments",
        ):
            self.assertEqual(self.matches(url), [])
        for query in ("cb=foo&v=1", "v=1&cb=foo", "callBack=x", "v=1&jsonp=x", "c%62=foo", "v=1;cb=foo"):
            self.assertEqual(self.matches(MIXER + "?" + query), [])
        self.assertEqual(len(self.matches(MIXER + "?azd=1%7C2&v=2")), 1)


if __name__ == "__main__":
    unittest.main()
