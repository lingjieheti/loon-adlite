"""Validate desktop-to-mobile coupon conversion through the Loon notification."""

import unittest

from test_checkin import COUPON, GUIDE, SINGLE_COUPON, run_reminder


DESKTOP = "https://coupon.jd.com/ilink/couponSendFront/send_index.action"
PAIR = "key=Ab_2-9&roleId=123"


class DesktopCouponTests(unittest.TestCase):
    def assert_notifications(self, inputs, expected):
        settings = [{"destination": SINGLE_COUPON, "coupon": link} for link in inputs]
        results = run_reminder("shopping-reminder.js", settings)
        self.assertEqual(len(results), len(inputs))
        for link, (notification, done) in zip(inputs, results):
            with self.subTest(link=link):
                self.assertEqual(notification[0], "notify")
                self.assertEqual(notification[-1], {"openUrl": expected})
                self.assertEqual(done, ["done"])

    def test_links_are_rebuilt_locally_for_safari(self):
        self.assert_notifications([
            DESKTOP + "?" + PAIR,
            DESKTOP + "?roleId=123&to=jiahu.jd.com&key=Ab_2-9",
            # Old shop links also circulate as HTTP text. The resulting URL is always HTTPS.
            DESKTOP.replace("https:", "http:") + "?" + PAIR + "&to=mall.jd.com/index-821028.html",
            DESKTOP + "?utm_source=test&" + PAIR + "&sceneval=2",
        ], COUPON + "?" + PAIR + "#loon-coupon")

    def test_other_origins_routes_and_ambiguous_parameters_fall_back(self):
        self.assert_notifications([
            DESKTOP.replace("coupon.jd.com", "coupon.jd.com.example.org") + "?" + PAIR,
            DESKTOP.replace("coupon.jd.com", "coupon.jd.com@example.org") + "?" + PAIR,
            DESKTOP.replace("send_index", "claim") + "?" + PAIR,
            DESKTOP + "?linkKey=abc",
            DESKTOP + "?roleId=12",
            DESKTOP + "?" + PAIR + "&key=second",
            DESKTOP + "?" + PAIR + "&to=mall.jd.com&to=jiahu.jd.com",
            DESKTOP + "?" + PAIR + "&to=mall.jd.com.example.org",
            DESKTOP + "?" + PAIR + "&to=mall.jd.com/offer?key=injected",
            DESKTOP + "?" + PAIR + "&to=mall.jd.com%2Foffer%3Fkey%3Dinjected",
            DESKTOP + "?" + PAIR + "&to=mall.jd.com//foreign.example",
            DESKTOP + "?" + PAIR + "&to=mall.jd.com#foreign",
            DESKTOP + "?" + PAIR + "&unknown=1",
            COUPON + "?" + PAIR + "&to=mall.jd.com",
            COUPON.replace("https:", "http:") + "?" + PAIR,
        ], GUIDE)
