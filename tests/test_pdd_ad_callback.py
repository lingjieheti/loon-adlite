"""Check the Pinduoduo DSP callback and ordinary shopping flows offline."""
from test_suite import ShoppingAdRequests


CALLBACK = "https://t-dsp.pinduoduo.com/dspcb/i/mrk_union"


class PinduoduoAdCallback(ShoppingAdRequests):
    def test_alliance_callback_get(self):
        for query in ("", "?id=fixture", "?id=123&slot=sample-7&tag="):
            url = CALLBACK + query
            self.assert_passes(url)
            for dest in ("document", "iframe", "empty", "video", "script"):
                self.assert_passes(url, headers={"Sec-Fetch-Dest": dest})
            rule, = [r for r in self.rules if r.matches(url, headers={"sec-fetch-dest": "image"})]
            self.assertEqual((rule.phase, rule.action), ("request", "reject_img(200)"))
            for method in ("HEAD", "POST", "PUT", "OPTIONS", "DELETE"):
                self.assert_passes(url, method, headers={"Sec-Fetch-Dest": "image"})

    def test_other_vendor_operations_and_navigation(self):
        for suffix in ("/", "/order", "-extra", "?id=42&next=order", "?redirect_url=shop",
                       "?id=1&returnUrl=order", "?Callback=cart", "?action=click", "?%75rl=item",
                       "?id=42;url=shop", "?id=42&url=https%3A%2F%2Fexample.org", "#item"):
            self.assert_passes(CALLBACK + suffix, headers={"Sec-Fetch-Dest": "document"})
        for url in (CALLBACK + "/", CALLBACK + "/order", CALLBACK + "-extra", CALLBACK + "#item",
                    CALLBACK.replace("/i/", "/c/"), CALLBACK.replace("t-dsp.", "api."),
                    CALLBACK.replace(".com/", ".com.example/"), CALLBACK.replace("https:", "http:"),
                    "https://mobile.yangkeduo.com/goods.html?goods_id=42",
                    "https://mobile.yangkeduo.com/duo_coupon_landing.html",
                    "https://api.pinduoduo.com/order/prepay", "https://api.yangkeduo.com/order/checkout",
                    "https://api.pinduoduo.com/api/ad/coupon", "https://video.pddpic.com/shop/product.mp4"):
            self.assert_passes(url, headers={"Sec-Fetch-Dest": "image"})
            self.assert_passes(url, method="POST")
