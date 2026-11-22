"""Test the mobile Taobao homepage's JSONP banner exposure separately from navigation."""
from test_suite import ShoppingAdRequests


HOST = "https://ifs.tanx.com"
PATH = "/display_ifs"
PACKET = "A" * 16 + "%2F" + "B" * 17 + "%3D%3D"
QUERY = "?i=x%42+._-9&p=" + PACKET + "&callback=__jp0"


class TaobaoAdCallbacks(ShoppingAdRequests):
    def test_homepage_banner_jsonp_exposures(self):
        self.assertIn("ifs.tanx.com", self.mitm_hosts)
        self.assertNotIn("ifs.tanx.com", self.blocked_hosts)
        # Match the raw i lengths of the two homepage templates without storing identifiers.
        for size, suffix in ((3360, "0"), (3363, "123")):
            encoded = "%AB" * (size // 3)
            url = HOST + PATH + f"?i={encoded}&p={PACKET}&callback=__jp{suffix}"
            hit, = [rule for rule in self.rules if rule.matches(url, method="GET")]
            self.assertEqual((hit.phase, hit.action), ("request", "reject(404)"))
        for method in ("POST", "HEAD", "PUT", "OPTIONS", "DELETE"):
            self.assert_passes(HOST + PATH + QUERY, method)

    def test_ambiguous_or_unrelated_requests(self):
        for query in ("", "?i=demo", QUERY.replace("x%42+._-9", ""),
                      QUERY.replace("%42", "%4G"), QUERY.replace("%3D%3D", "%3D"),
                      QUERY.replace(PACKET, "x"), QUERY.replace("&p=", "&i=foo&p="),
                      QUERY.replace("&callback=__jp0", ""), QUERY.replace("__jp0", "showItem"),
                      QUERY.replace("__jp0", "__jp01"), QUERY + "&target=next", QUERY + "#destination"):
            self.assert_passes(HOST + PATH + query)
        for endpoint in (HOST + PATH + "/", HOST + PATH + ".js", HOST + "/click",
                         "http://ifs.tanx.com" + PATH, "https://sub.ifs.tanx.com" + PATH,
                         "https://ifs.tanx.com.example" + PATH, "https://ifs.tanx.com@example.org" + PATH):
            self.assert_passes(endpoint + QUERY)

    def test_homepage_clicks_coupons_and_transaction_flows(self):
        for url in ("https://click.mz.simba.taobao.com/necpm?eadt=149&p=",
                    "https://click.simba.taobao.com/cc", "https://redirect.simba.taobao.com/rd?c=un",
                    "https://m.taobao.com/tbopen/index.html?action=ali.open.nav",
                    "https://uland.taobao.com/coupon/edetail", "https://login.m.taobao.com/login.htm",
                    "https://detail.tmall.com/item.htm?id=42", "https://cart.taobao.com/cart.htm",
                    "https://acs.m.taobao.com/gw/mtop.trade.order.create/1.0/",
                    "https://cashier.alipay.com/standard/payment/",
                    "https://wcp.taobao.com/adstrack/track.json?action=2&app=1&channel=demo"
                    "&oaidMd5=demo&advertiserId=123&adid=456&cid=789&requestId=example"):
            self.assert_passes(url)
            self.assert_passes(url, method="POST")
