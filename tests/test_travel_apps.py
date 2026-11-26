"""Verify the dedicated travel and delivery ad routes against nearby business paths."""
import unittest
from urllib.parse import urlsplit

from test_suite import ROOT, Rewrite, read_sections


class TravelAds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sections = read_sections(ROOT / "iPad-AdSuite.lpx")
        cls.rules = [Rewrite.parse(line) for line in sections["rewrite"]]

    def test_dedicated_ad_routes(self):
        cases = {
            "https://homefront.qunar.com/front/splash/ad": "reject_dict(200)",
        }
        for url, action in cases.items():
            for suffix in ("", "?channel=ios"):
                with self.subTest(url=url + suffix):
                    rule, = [rule for rule in self.rules if rule.matches(url + suffix)]
                    self.assertEqual((rule.phase, rule.action), ("request", action))
            host = urlsplit(url).hostname
            self.assertFalse(any(rule.matches(url.replace(host, host + ".example.org")) for rule in self.rules))

    def test_delivery_booking_and_flight_paths_do_not_match(self):
        cases = {
            "ccsp-egmas.sf-express.com": (
                "/cx-app-base/base/app/waybill/query", "/cx-app-base/base/app/ad/queryInfoFlowHistory",
                "/cx-app-base/base/app/waybill/query?next=/cx-app-base/base/app/ad/queryInfoFlow",
            ),
            "homefront.qunar.com": (
                "/front/splash/address", "/front/splash/ad/booking", "/front/flight/query",
            ),
            "app.variflight.com": (
                "/v1/flight/status", "/v1/advertisement/status", "/v2/advert/", "/address/detail",
                "/ad/../flight/status", "/v1/advert/%2e%2e/flight/status", "/ad//flight",
            ),
            "3g.csair.com": (
                "/CSMBP/bookProcess/homepopup/queryAdvertisementPolicy",
                "/CSMBP/bookProcess/homepopup/queryAdvertisement/checkin",
                "/CSMBP/bookProcess/boardingPass", "/CSMBP/bookProcess/pay",
            ),
        }
        for host, paths in cases.items():
            for path in paths:
                with self.subTest(host=host, path=path):
                    self.assertFalse(any(rule.matches("https://" + host + path) for rule in self.rules))
