"""Exercise the WeChat article ad beacons while preserving article and click navigation."""
import unittest
from urllib.parse import quote

from test_suite import ROOT, Rewrite, read_sections


HOST = "https://mp.weixin.qq.com"
PIXEL = HOST + "/mp/ad_report?action=see_report&aid=314&tid=trace_42&"
REPORT = HOST + "/mp/advertisement_report?"
EXTRA = REPORT + "action=extra_report"
EXPOSURE = REPORT + "report_type=1&tid=trace_42&aid=314&gh_id=&adver_group_id=7&apurl=https%3A%2F%2Fexample.org"
# The article AJAX wrapper appends available session fields, followed by x5 and f.
# All values here are synthetic placeholders in the source serialization order.
AJAX = ("&uin=1&key=sample&pass_ticket=example%2Bvalue&wxtoken=1"
        "&devicetype=iOS&clientversion=example&appmsg_token=sample&x5=0&f=json")
SIGNED_EXPOSURE = (EXPOSURE + "&__biz=Example%3D&ascene=0&pos_type=0&exp_id=&exp_value=%5B%5D&r=0.1"
                   "&ad_sign_data=sample%2Bsignature&ad_sign_k1=A&ad_sign_k2=B&ad_sign_md5=C" + AJAX)
ACK = 'response.body.mock("json", `{"ret":0}`, 200)'


class WechatAdReports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = {}
        for name in ("iPad-InlineAds.lpx", "iPad-AdSuite.lpx"):
            cls.rules[name] = [Rewrite.parse(line) for line in read_sections(ROOT / name)["rewrite"]]

    def assert_actions(self, url, actions, method="GET"):
        for name, rules in self.rules.items():
            with self.subTest(plugin=name, url=url[:170], method=method):
                self.assertEqual([rule.action for rule in rules if rule.matches(url, method=method)], actions)

    def test_viewability_pixels_match_only_known_positions_and_durations(self):
        for position in (1, 2, 3):
            self.assert_actions(PIXEL + f"seepos={position}&report_type=0", ["reject_img(200)"])
        for duration in (500, 1000, 2000):
            self.assert_actions(PIXEL + f"seetime={duration}&report_type=1", ["reject_img(200)"])
        for method in ("POST", "HEAD", "OPTIONS"):
            self.assert_actions(PIXEL + "seepos=1&report_type=0", [], method=method)
            self.assert_actions(PIXEL + "seetime=500&report_type=1", [], method=method)
        for change in ("seepos=0&report_type=0", "seepos=1&report_type=1", "seetime=500&report_type=0",
                       "seetime=750&report_type=1", "seetime=500&report_type=1&action=follow"):
            self.assert_actions(PIXEL + change, [])

    def test_extra_click_and_exposure_time_notifications(self):
        for body in ('{"biz_ad_exposure_time":[{"aid":314,"staytime":500}]}',
                     '{"biz_click_add":[{"aid":314,"clktime":12345}]}'):
            sample = EXTRA + "&extra_data=" + quote(body, safe="") + "&__biz=Example%3D"
            self.assert_actions(sample + AJAX, ["reject_dict(200)"])
        self.assert_actions(EXTRA + AJAX, ["reject_dict(200)"], method="POST")
        for tail in ("&action=follow", "&a%63tion=follow", "&report_type=3", "&callback=test",
                     "&__biz=abc&jump_url=about:blank", "&extra_data=x;report_type=2&__biz=abc"):
            self.assert_actions(EXTRA + tail, [])

    def test_only_get_with_unambiguous_ad_exposure_gets_local_ack(self):
        self.assert_actions(SIGNED_EXPOSURE, [ACK])
        self.assert_actions(EXPOSURE, [ACK])
        self.assert_actions(EXPOSURE + "&__biz=b&pos_type=1&ad_sign_data=a%2Bb", [ACK])
        self.assert_actions(EXPOSURE.replace("&gh_id=", ""), [ACK])
        for method in ("POST", "PUT", "HEAD"):
            self.assert_actions(SIGNED_EXPOSURE, [], method=method)
        for old, new in (("tid=trace_42", "tid="), ("aid=314", "aid="), ("&aid=314", ""),
                         ("apurl=https%3A%2F%2Fexample.org", "apurl="), ("report_type=1", "report_type=2"),
                         ("report_type=1", "report_type=3"), ("aid=314", "aid=314&aid=315"),
                         ("aid=314", "aid=314&%61id=315"), ("report_type", "report%5ftype")):
            self.assert_actions(EXPOSURE.replace(old, new), [])
        for tail in ("&report_type=3", "&REPORT_TYPE=1", "&action=extra_report", "&callback=cb",
                     "&ad_sign_data=a;action=complain", "&r=1#redirect", "&r=1" * 1024 + "&action=follow"):
            self.assert_actions(EXPOSURE + tail, [])

    def test_article_interactions_complaints_and_deliberate_navigation(self):
        for path in ("/mp/ad_complaint?action=report", "/mp/ad_redirect?url=example", "/mp/ad_report?action=follow",
                     "/mp/advertisement_report?report_type=2&type=4&tid=7", "/mp/advertisement_report?report_type=3",
                     "/mp/report", "/mp/appmsgreport", "/mp/appmsg_comment", "/s/article", "/cgi-bin/login"):
            self.assert_actions(HOST + path, [])
        for url in (EXPOSURE, EXTRA, PIXEL + "seepos=1&report_type=0"):
            self.assert_actions(url.replace(HOST, "https://mp.weixin.qq.com.example.org"), [])
            self.assert_actions(url.replace(HOST, "https://mp.weixin.qq.com@example.org"), [])
            self.assert_actions(url.replace("https://", "http://"), [])
        for path in ("/mp/getappmsgext", "/mp/getappmsgad"):
            for name, rules in self.rules.items():
                with self.subTest(plugin=name, path=path):
                    rule, = [rule for rule in rules if rule.matches(HOST + path)]
                    self.assertTrue(rule.action.startswith("response.json.jq("))
