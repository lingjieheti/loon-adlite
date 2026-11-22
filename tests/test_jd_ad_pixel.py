"""Check JD exposure pixels separately from ad clicks, coupons and orders."""
from test_suite import ShoppingAdRequests


HOST = "https://im-x.jd.com"
PIXEL = HOST + "/dsp/np"
QUERY = "?log=synthetic_Ad-42&v=404"


class JDAdPixel(ShoppingAdRequests):
    def test_reviewed_get_pixel_returns_one_local_image(self):
        self.assertIn("im-x.jd.com", self.mitm_hosts)
        self.assertNotIn("im-x.jd.com", self.blocked_hosts)
        for length in (1579, 1600, 1622):
            token = ("aB9_-" * 325)[:length]
            url = PIXEL + "?log=" + token + "&v=404"
            with self.subTest(length=length):
                hit, = [rule for rule in self.rules if rule.matches(url, method="GET")]
                self.assertEqual((hit.phase, hit.action), ("request", "reject_img(200)"))
        for method in ("POST", "HEAD", "PUT", "OPTIONS"):
            self.assert_passes(PIXEL + QUERY, method)

    def test_other_query_shapes_paths_and_authorities(self):
        for query in ("", "?log=&v=404", "?log=a", "?v=404&log=a", "?log=a&v=405",
                      "?log=a&v=404&v=404", "?log=a&log=b&v=404", "?log=a%26v%3D404&v=404",
                      "?log=a;clicktype=1&v=404", QUERY + "&url=next", QUERY + "#item"):
            self.assert_passes(PIXEL + query)
        for near in (HOST + "/dsp/nc", HOST + "/dsp/np/", HOST + "/np",
                     PIXEL.replace("https:", "http:"), PIXEL.replace(".com/", ".com.example/"),
                     PIXEL.replace(".com/", ".com@example.org/"), PIXEL.replace("im-x.", "sub.im-x.")):
            self.assert_passes(near + QUERY)

    def test_landing_click_coupon_and_core_services(self):
        urls = (
            "https://ccc-x.jd.com/dsp/nc?ext=sample&log=sample&v=404&clicktype=0",
            "https://pro.m.jd.com/mall/active/example/index.html", "https://item.m.jd.com/product/123.html",
            "https://u.jd.com/example", "https://coupon.m.jd.com/coupons/show.action?key=sample",
            "https://passport.jd.com/new/login.aspx", "https://blackhole.m.jd.com/getinfo",
            "https://api.m.jd.com/client.action?functionId=wareBusiness",
            "https://api.m.jd.com/client.action?functionId=cart",
            "https://api.m.jd.com/client.action?functionId=submitOrder",
            "https://pay.m.jd.com/", "https://chat1.jd.com/checkChat",
            "https://vod.300hu.com/video/example.mp4",
        )
        for url in urls:
            self.assert_passes(url)
            self.assert_passes(url, method="POST")
